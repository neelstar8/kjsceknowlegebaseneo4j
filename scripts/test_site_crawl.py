"""Integrity checks for the site crawl and anything it put in the graph.

Run this before and after every ingest. It is the same shape as
`scripts/test_policy_queries.py`: standalone, hand-rolled PASS/FAIL, non-zero exit on
failure, no test framework.

The checks are split in two. The first group proves the crawl did not damage
anything that was already there -- that is the one failure mode that matters most,
because a crawl touches far more of the graph than a hand-curated ingest does. The
second group proves the crawl's own output is coherent.

    .venv/bin/python -m scripts.test_site_crawl
"""
from __future__ import annotations

import json
import os
import sys
import urllib.parse as up

from crawl.manifest import Manifest, Status
from crawl.site_urls import KJ_DOWNLOAD_HOSTS, KJ_SITE_HOSTS
from graph.neo4j_driver import close_driver, run_query, verify_connection

#: Counts that existed before any crawl work began. None of these may move.
BASELINE = {
    "FacultyMember": 613, "PYQ": 164, "PYQFile": 162, "Subject": 81,
    "PolicyProvision": 432, "Policy": 41,
}

#: PolicyDocument count before the crawl. New site documents add to this; nothing
#: may ever reduce it.
PRE_CRAWL_DOCUMENTS = 42

# Keys that would mean a file's contents leaked into the graph. `text` is
# deliberately absent: `PolicyProvision.text` is the provision itself, which is the
# whole point of that node. This mirrors the list in scripts/test_policy_queries.py.
FORBIDDEN_CONTENT_KEYS = ["pdf", "content", "raw", "bytes", "body", "base64",
                          "pages_text", "extracted_text", "raw_pdf"]

# One document predates this crawl and has never had a parent: an
# `official_site_supplement` added by the policy pipeline. It is recorded here so the
# orphan check can assert "no NEW orphan" rather than silently tolerating any orphan.
KNOWN_PRE_EXISTING_ORPHANS = {"kjsit_exam_structure_coc"}

_passed = _failed = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global _passed, _failed
    if ok:
        _passed += 1
        print(f"  [PASS] {label}" + (f"  -- {detail}" if detail else ""))
    else:
        _failed += 1
        print(f"  [FAIL] {label}" + (f"  -- {detail}" if detail else ""))


def scalar(query: str, params: dict | None = None):
    rows = run_query(query, params or {})
    return list(rows[0].values())[0] if rows else None


def check_existing_knowledge_untouched() -> None:
    print("\n== existing knowledge untouched ==")
    for label, expected in BASELINE.items():
        actual = scalar(f"MATCH (n:{label}) RETURN count(n)")
        check(f"{label} still {expected}", actual == expected, f"found {actual}")

    docs = scalar("MATCH (d:PolicyDocument) RETURN count(d)")
    check("PolicyDocument count never shrank", docs >= PRE_CRAWL_DOCUMENTS,
          f"{docs} (was {PRE_CRAWL_DOCUMENTS} before the crawl)")

    orphans = {r["id"] for r in run_query("""
        MATCH (d:PolicyDocument) WHERE NOT (()-[:REFERENCES|DOCUMENTED_IN]->(d))
        RETURN d.doc_id AS id""")}
    new_orphans = sorted(orphans - KNOWN_PRE_EXISTING_ORPHANS)
    check("the crawl created no new orphaned document", not new_orphans,
          f"new orphans: {new_orphans}" if new_orphans
          else f"{len(orphans)} orphan(s), all pre-existing")


def check_graph_integrity() -> None:
    print("\n== graph integrity ==")
    total = scalar("MATCH (d:PolicyDocument) RETURN count(d)")
    ids = scalar("MATCH (d:PolicyDocument) RETURN count(DISTINCT d.doc_id)")
    urls = scalar("MATCH (d:PolicyDocument) WHERE d.source_url IS NOT NULL "
                  "RETURN count(DISTINCT d.source_url)")
    with_url = scalar("MATCH (d:PolicyDocument) WHERE d.source_url IS NOT NULL "
                      "RETURN count(d)")
    check("every document has a distinct doc_id", total == ids, f"{total}/{ids}")
    check("every document has a source_url", with_url == total,
          f"{with_url}/{total}")
    check("no two documents share a source_url", with_url == urls,
          f"{with_url}/{urls}")

    dup_sha = scalar("""
        MATCH (d:PolicyDocument) WHERE d.sha256 IS NOT NULL
        WITH d.sha256 AS s, count(*) AS n WHERE n > 1 RETURN count(s)""")
    check("no two documents share a checksum", dup_sha == 0,
          f"{dup_sha} duplicated checksums")

    unparented = scalar("""
        MATCH (d:PolicyDocument {discovered_by:'site_crawl'})
        WHERE NOT ((:Policy)-[:REFERENCES]->(d)) RETURN count(d)""")
    check("every crawled document hangs off a Policy", unparented == 0,
          f"{unparented} unparented")

    # Scoped to the policy corpus on purpose. The faculty directory legitimately
    # spans 16 Somaiya institutes; it is the policy/document graph that is
    # KJSIT-only, which is exactly what scripts/test_policy_queries.py asserts.
    bad_inst = scalar("""
        MATCH (n) WHERE (n:Policy OR n:PolicyProvision OR n:PolicyDocument
                         OR n:PolicyCategory OR n:PolicyHandbook)
        AND n.institution IS NOT NULL AND n.institution <> 'KJSIT'
        RETURN count(n)""")
    check("no policy-corpus node claims a non-KJSIT institution", bad_inst == 0,
          f"{bad_inst} nodes")

    carries = scalar(
        "MATCH (n) WHERE any(k IN keys(n) WHERE k IN $keys) RETURN count(n)",
        {"keys": FORBIDDEN_CONTENT_KEYS})
    check("no node carries document content", carries == 0, f"{carries} nodes")


def check_scope_held() -> None:
    print("\n== crawl scope held ==")
    allowed = sorted(KJ_DOWNLOAD_HOSTS | KJ_SITE_HOSTS | {"kjsit-files.somaiya.edu.in",
                                                          "kjsit.somaiya.edu.in",
                                                          "drive.google.com",
                                                          "www.mathworks.com",
                                                          "kjsce-old.somaiya.edu"})
    rows = run_query("""
        MATCH (d:PolicyDocument {discovered_by:'site_crawl'})
        RETURN d.source_url AS url""")
    offenders = sorted({up.urlsplit(r["url"]).netloc for r in rows
                        if up.urlsplit(r["url"]).netloc not in allowed})
    check("crawled documents only come from allowed hosts", not offenders,
          f"unexpected: {offenders}" if offenders else f"{len(rows)} documents")


def check_manifest() -> None:
    print("\n== crawl manifest ==")
    man = Manifest().load()
    if not man.rows:
        check("manifest exists", False, "no manifest found")
        return

    check("manifest replayed cleanly", getattr(man, "truncated_lines", 0) <= 1,
          f"{getattr(man, 'truncated_lines', 0)} truncated line(s)")

    # A refused document must never have been fetched -- that is the whole point of
    # gating before the download rather than filtering afterwards.
    leaked = [r for r in man.rows.values() if r.get("status") == Status.SKIPPED_PII
              and (r.get("sha256") or r.get("local_path") or r.get("bytes"))]
    check("no refused document was ever downloaded", not leaked,
          f"{len(leaked)} leaked" if leaked else "PII gate ran before fetch")

    ids = [r.get("resource_id") for r in man.rows.values()]
    check("manifest ids are unique", len(ids) == len(set(ids)), f"{len(ids)} rows")

    cov = man.coverage()
    check("coverage denominator is non-zero", cov["total_in_scope"] > 0,
          f"{cov['resolved']}/{cov['total_in_scope']} = {cov['coverage_pct']}%")
    check("every outstanding resource is named",
          len(cov["outstanding"]) == cov["total_in_scope"] - cov["resolved"],
          f"{len(cov['outstanding'])} listed")


def check_reconciliation() -> None:
    path = "data/crawl/site_reconciliation.json"
    if not os.path.exists(path):
        return
    print("\n== reconciliation decisions ==")
    payload = json.load(open(path, encoding="utf-8"))
    decisions = payload["decisions"]

    reuse_without_target = [d for d in decisions
                            if d["decision"] == "REUSE" and not d.get("matched_doc_id")
                            and d.get("matched_on") != "entity_url"]
    check("every REUSE names the document it matched", not reuse_without_target,
          f"{len(reuse_without_target)} without a target")

    new_with_match = [d for d in decisions
                      if d["decision"] == "NEW" and d.get("matched_doc_id")]
    check("no NEW decision matched an existing document", not new_with_match,
          f"{len(new_with_match)} contradictory")

    # A sha256 match is proof of identity; it must never be routed to NEW.
    sha_new = [d for d in decisions
               if d.get("matched_on") == "sha256" and d["decision"] == "NEW"]
    check("checksum matches always reuse, never create", not sha_new,
          f"{len(sha_new)} would have duplicated")


def main() -> int:
    verify_connection()
    try:
        check_existing_knowledge_untouched()
        check_graph_integrity()
        check_scope_held()
        check_manifest()
        check_reconciliation()
    finally:
        close_driver()

    total = _passed + _failed
    print(f"\n{_passed}/{total} checks passed")
    if _failed:
        print(f"{_failed} FAILED")
    return 1 if _failed else 0


if __name__ == "__main__":
    sys.exit(main())

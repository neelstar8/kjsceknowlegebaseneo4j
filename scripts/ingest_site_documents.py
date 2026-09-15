"""Write the reconciled crawl results into Neo4j.

    data/crawl/site_reconciliation.json -> Neo4j -> data/crawl/site_ingestion_report.json

Only two decisions ever touch the graph:

    NEW     create a :PolicyDocument under an existing :Policy parent
    REUSE   record the second URL on the document that already exists

REFERENCE_ONLY, SKIPPED_PII and REVIEW are deliberately inert here. A REVIEW row
blocks the run unless `--allow-review` is passed, because the whole point of that
state is that a person has not looked at it yet.

Idempotent: every write is a MERGE on `doc_id`, so a second run updates rather than
duplicates. Nothing is ever deleted.

    .venv/bin/python -m scripts.ingest_site_documents --dry-run
    .venv/bin/python -m scripts.ingest_site_documents --source-type ranking_report
"""
from __future__ import annotations

import argparse
import json
import hashlib
import os
import re
import uuid
from collections import Counter
from datetime import datetime, timezone

from crawl.classify import classify_document, ranking_metadata
from crawl.manifest import Manifest
from crawl.site_urls import canonical_url, filename_of
from graph import site_ingestion as gi
from graph.neo4j_driver import close_driver, run_query, verify_connection
from graph.site_reconcile import Decision

IN_PATH = "data/crawl/site_reconciliation.json"
REPORT = "data/crawl/site_ingestion_report.json"

BASELINE = {"FacultyMember": 613, "PYQ": 164, "PYQFile": 162, "Subject": 81,
            "PolicyProvision": 432, "Policy": 41}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(text: str, fallback: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", (text or "").lower()).strip("_")
    return (slug or fallback)[:60]


def doc_id_for(decision: dict, route: dict) -> str:
    """Deterministic id, unique per source URL.

    The readable slug alone is not enough: this site titles its NIRF submissions
    simply "Engineering", "Overall" and "Innovation" every year, and labels several
    different admission notices "Read Notice". Slugging the title alone gave the 2025
    and 2026 Engineering reports the same id, so the second MERGE silently overwrote
    the first. The short URL-derived suffix keeps the id readable and stable across
    runs while guaranteeing two different documents can never collide.
    """
    prefix = {"ranking_report": "rank", "accreditation_document": "accr",
              "mandatory_disclosure": "mdisc", "admission_document": "adm",
              "placement_document": "plc", "library_document": "lib",
              "scholarship_document": "schol", "hostel_document": "hostel",
              "research_document": "res", "examination_document": "exam_site",
              "academic_document": "acad_site", "development_plan": "devplan",
              "alumni_document": "alum", "transcript_document": "trn",
              }.get(route["source_type"], "site")
    name = decision.get("title") or filename_of(decision["canonical_url"])
    suffix = hashlib.sha1(
        canonical_url(decision["canonical_url"]).encode("utf-8")).hexdigest()[:8]
    return f"{prefix}_{slugify(name, decision['resource_id'])}_{suffix}"


def snapshot() -> dict:
    out = {}
    for label in BASELINE:
        out[label] = run_query(f"MATCH (n:{label}) RETURN count(n) AS c")[0]["c"]
    out["PolicyDocument"] = run_query(
        "MATCH (d:PolicyDocument) RETURN count(d) AS c")[0]["c"]
    return out


def build_props(decision: dict, route: dict, row: dict | None, meta: dict) -> dict:
    props = {
        "title": decision.get("title"),
        "source_url": decision["canonical_url"],
        "source_type": route["source_type"],
        "document_type": route["source_type"],
        "institution": "KJSIT",
        "institution_name_in_source": "K J Somaiya College/School of Engineering",
        "source_page": "https://kjsce.somaiya.edu/en/documents/",
        "discovered_by": "site_crawl",
        "crawl_matched_on": route.get("matched_on"),
        "knowledge_version": "1.0",
    }
    if row:
        props.update({
            "filename": filename_of(decision["canonical_url"]),
            "sha256": row.get("sha256"),
            "file_size_bytes": row.get("bytes"),
            "pages": row.get("pages"),
            "text_chars": row.get("text_chars"),
            "needs_visual_read": row.get("needs_visual_read", False),
        })
        if row.get("scanned_pages"):
            props["scanned_pages"] = row["scanned_pages"]
    if route["source_type"] == "ranking_report":
        props.update(ranking_metadata(decision.get("title"),
                                      decision["canonical_url"]))
    props.update(meta)
    return props


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="in_path", default=IN_PATH)
    ap.add_argument("--report", default=REPORT)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--source-type", default=None,
                    help="ingest only this source_type (batch by content family)")
    ap.add_argument("--allow-review", action="store_true",
                    help="proceed even though REVIEW rows are present")
    args = ap.parse_args()

    payload = json.load(open(args.in_path, encoding="utf-8"))
    decisions = payload["decisions"]
    man = Manifest().load()

    reviews = [d for d in decisions if d["decision"] == Decision.REVIEW]
    if reviews and not args.allow_review and not args.dry_run:
        print(f"\n  {len(reviews)} resource(s) are awaiting review and would be "
              "skipped silently. Inspect them first:")
        for d in reviews[:10]:
            print(f"    {(d.get('title') or '')[:50]:<52} {d.get('evidence','')[:60]}")
        raise SystemExit(
            "Refusing to run. Re-run with --allow-review once you have looked at them.")

    # Route every NEW row before touching the database, so a routing failure is a
    # planning error rather than a half-finished write.
    plan, unrouted = [], []
    for d in decisions:
        if d["decision"] != Decision.NEW:
            continue
        row = man.get(d["resource_id"]) or {}
        route = classify_document(title=d.get("title"), url=d["canonical_url"],
                                  discovered_via=row.get("discovered_via"))
        if not route["source_type"]:
            unrouted.append(d)
            continue
        if args.source_type and route["source_type"] != args.source_type:
            continue
        plan.append((d, route, row))

    reuses = [d for d in decisions if d["decision"] == Decision.REUSE
              and d.get("matched_doc_id") and d.get("alternate_url_to_record")]

    print(f"\n  NEW to create     : {len(plan)}")
    print(f"  REUSE to annotate : {len(reuses)}")
    print(f"  unrouted (skipped): {len(unrouted)}")
    print(f"  awaiting review   : {len(reviews)}")
    for d, route, _row in plan:
        print(f"    {route['source_type']:<22} {(d.get('title') or '')[:46]:<48} "
              f"-> {route['parent_policy_id']}")

    if args.dry_run:
        print("\nDRY RUN - nothing written")
        return

    verify_connection()
    batch_id = f"sitecrawl_{datetime.now(timezone.utc):%Y%m%dT%H%M%S}_{uuid.uuid4().hex[:6]}"
    now = _now()
    try:
        before = snapshot()

        missing = sorted({r["parent_policy_id"] for _d, r, _x in plan
                          if not gi.parent_exists(r["parent_policy_id"])})
        if missing:
            raise SystemExit(f"parent policies not in the graph: {missing}. "
                             "This script will not invent a parent node.")

        created = links = 0
        rows_out = []
        # Defence in depth. The dedup ladder compares each candidate against the
        # graph as it stood when the run began, so two candidates inside the same
        # batch carrying identical bytes would both be created. That is how the same
        # NIRF report arrived twice, linked once as http:// and once as https://.
        seen_sha: dict[str, str] = {}
        intra_batch_dupes = []

        for d, route, row in plan:
            sha = row.get("sha256")
            if sha and sha in seen_sha:
                intra_batch_dupes.append({
                    "doc_id": seen_sha[sha], "duplicate_url": d["canonical_url"],
                    "title": d.get("title"), "sha256": sha})
                gi.record_alternate_url(seen_sha[sha], d["canonical_url"], now)
                continue
            doc_id = doc_id_for(d, route)
            props = build_props(d, route, row, {})
            was_created = gi.upsert_document(doc_id, props, now, batch_id)
            linked = gi.link_document(doc_id, route["parent_policy_id"], now, batch_id)
            created += bool(was_created)
            links += linked
            if sha:
                seen_sha[sha] = doc_id
            rows_out.append({"doc_id": doc_id, "title": d.get("title"),
                             "source_url": d["canonical_url"],
                             "source_type": route["source_type"],
                             "parent_policy_id": route["parent_policy_id"],
                             "created": was_created, "linked": bool(linked)})

        annotated = []
        for d in reuses:
            info = gi.record_alternate_url(d["matched_doc_id"],
                                           d["alternate_url_to_record"], now)
            annotated.append({**info, "evidence": d.get("evidence")})

        after = snapshot()
        result = {
            "run_at": now, "ingest_batch_id": batch_id,
            "created": created, "updated": len(plan) - created,
            "links_merged": links,
            "alternate_urls_recorded": len(annotated),
            "intra_batch_duplicates": intra_batch_dupes,
            "unrouted": [u["canonical_url"] for u in unrouted],
            "awaiting_review": [r["canonical_url"] for r in reviews],
            "counts_before": before, "counts_after": after,
            "graph_counts": gi.counts(),
            "rows": rows_out, "reused": annotated,
        }
    finally:
        close_driver()

    print(f"\n  batch id          : {batch_id}")
    print(f"  created           : {result['created']}")
    print(f"  updated           : {result['updated']}")
    print(f"  REFERENCES merged : {result['links_merged']}")
    print(f"  alternate urls    : {result['alternate_urls_recorded']}")
    if result["intra_batch_duplicates"]:
        print(f"  same-bytes dupes  : {len(result['intra_batch_duplicates'])} "
              "collapsed into the first copy")
    print("\n  untouched baselines:")
    drift = {k: (before[k], after[k]) for k in BASELINE if before[k] != after[k]}
    for k in BASELINE:
        flag = "OK" if before[k] == after[k] else "CHANGED"
        print(f"    {k:<18} {before[k]:>5} -> {after[k]:>5}  {flag}")
    print(f"    {'PolicyDocument':<18} {before['PolicyDocument']:>5} -> "
          f"{after['PolicyDocument']:>5}  (+{after['PolicyDocument']-before['PolicyDocument']})")
    if drift:
        print(f"\n  WARNING: unrelated counts moved: {drift}")

    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, ensure_ascii=False)
    print(f"\nWrote {args.report}")
    print(f"To undo this batch:\n  MATCH (d:PolicyDocument {{ingest_batch_id: "
          f"'{batch_id}'}}) DETACH DELETE d")


if __name__ == "__main__":
    main()

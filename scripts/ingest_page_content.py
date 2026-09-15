"""Ingest the substantive content of crawled KJSCE webpages into Neo4j.

    cached page HTML -> content -> facts -> reconcile -> :PolicyDocument(webpage)

Resumes from the existing crawl manifest; no page is re-fetched, because the
previous run already cached all 366 of them. Every write is a MERGE on a
deterministic `doc_id`, so re-running updates rather than duplicates.

What this does NOT do, deliberately:

  * It does not store page prose. Only the page's own headings, its tables, and
    short fact-bearing sentences are kept -- the goal is retrievable knowledge, not
    a text dump, and the graph has never held document content.
  * It does not touch faculty. `/view-member` pages describe people already in
    FacultyMember, and `/view-publication` pages are faculty research output owned
    by the faculty pipeline. Re-deriving either here would create a second,
    disagreeing copy, so both are recorded and skipped.
  * It does not create PolicyProvisions. A page paragraph is not an ordinance; the
    provision tier stays reserved for the handbook, where rules carry page-level
    citations.

    .venv/bin/python -m scripts.ingest_page_content --dry-run
    .venv/bin/python -m scripts.ingest_page_content --limit 40
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import uuid
from collections import Counter
from datetime import datetime, timezone

from crawl import page_content as pc
from crawl import page_facts as pf
from crawl.classify import classify_page
from crawl.fetcher import read_cache
from crawl.manifest import Manifest, Status
from crawl.site_urls import canonical_url, section_of
from graph import site_ingestion as gi
from graph.neo4j_driver import close_driver, run_query, verify_connection

BOILERPLATE = "data/crawl/boilerplate_blocks.json"
GROUPS = "data/crawl/page_content_groups.json"
REPORT = "data/crawl/page_ingestion_report.json"
SOURCE_TYPE = "webpage"
RELATION = "official_site_page"

BASELINE = {"FacultyMember": 613, "PYQ": 164, "PYQFile": 162, "Subject": 81,
            "PolicyProvision": 432, "Policy": 41}

#: Sections whose content is already owned by another pipeline.
FACULTY_OWNED = ("/view-member/", "/view-publication/")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def slug(text: str, fallback: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", (text or "").lower()).strip("_")
    return (s or fallback)[:52]


def doc_id_for(url: str, title: str) -> str:
    """Readable and unique. The suffix is required: this site reuses titles
    ("Overall", "Read Notice") across entirely different pages."""
    digest = hashlib.sha1(canonical_url(url).encode("utf-8")).hexdigest()[:8]
    return f"page_{slug(title or section_of(url), digest)}_{digest}"


def snapshot() -> dict:
    out = {k: run_query(f"MATCH (n:{k}) RETURN count(n) AS c")[0]["c"] for k in BASELINE}
    out["PolicyDocument"] = run_query(
        "MATCH (d:PolicyDocument) RETURN count(d) AS c")[0]["c"]
    return out


def existing_index() -> dict:
    """What the graph already holds, so nothing is created twice."""
    idx = {"by_url": {}, "by_fingerprint": {}}
    for r in run_query("""
        MATCH (d:PolicyDocument)
        RETURN d.doc_id AS doc_id, d.source_url AS source_url,
               d.alternate_source_url AS alt, d.content_fingerprint AS fp,
               d.ingested_by = 'page_content' AS own"""):
        for u in (r["source_url"], r["alt"]):
            if u:
                idx["by_url"][u] = r
                idx["by_url"][canonical_url(u)] = r
        if r["fp"]:
            idx["by_fingerprint"][r["fp"]] = r
    return idx


def build(url: str, aliases: list[str], boilerplate: set) -> dict | None:
    body, _meta = read_cache(url)
    if body is None:
        return None
    html = body.decode("utf-8", "replace")
    content = pc.content_of(html, boilerplate)
    facts = pf.key_facts(content["blocks"])
    ok, why = pf.is_substantive(content, facts)
    all_text = " ".join(b["text"] for b in content["blocks"])
    route = classify_page(url)

    return {
        "url": url, "aliases": [a for a in aliases if a != url],
        "content": content, "facts": facts, "route": route,
        "substantive": ok, "reason": why,
        "academic_years": pf.academic_years(all_text),
        "years": pf.years_mentioned(all_text),
        "summary": pf.summarise(content),
    }


def props_for(item: dict) -> dict:
    c, route = item["content"], item["route"]
    props = {
        "title": c["title"] or section_of(item["url"]),
        "source_url": item["url"],
        "source_type": SOURCE_TYPE,
        "document_type": route["source_type"],
        "page_section": section_of(item["url"]),
        "institution": "KJSIT",
        "institution_name_in_source": "K J Somaiya College/School of Engineering",
        "discovered_by": "site_crawl",
        "ingested_by": "page_content",
        "content_fingerprint": c["content_fingerprint"],
        "content_chars": c["content_chars"],
        "summary": item["summary"],
        "headings": c["headings"],
        "headings_text": " | ".join(c["headings"]),
        "knowledge_version": "1.0",
        "crawl_matched_on": route.get("matched_on"),
    }
    if item["academic_years"]:
        props["academic_years"] = item["academic_years"]
        # The most recent year the page names, so retrieval can prefer current
        # material without ever rewriting what an older page actually says.
        props["latest_academic_year"] = max(item["academic_years"])
    if item["years"]:
        props["years_mentioned"] = item["years"]
    if item["aliases"]:
        props["alternate_source_url"] = item["aliases"][0]
        props["alias_urls"] = item["aliases"][:12]
        props["also_published_under"] = (
            f"{len(item['aliases'])} further URL(s) serve identical content "
            "(client-side tabs)")
    props.update(pf.flatten_facts(item["facts"]))
    props.update(pf.flatten_tables(item["content"]["tables"]))
    return {k: v for k, v in props.items() if v is not None}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--section", default=None, help="only pages in this URL section")
    ap.add_argument("--report", default=REPORT)
    args = ap.parse_args()

    boilerplate = set(json.load(open(BOILERPLATE, encoding="utf-8")))
    groups = json.load(open(GROUPS, encoding="utf-8"))
    man = Manifest().load()

    candidates = []
    skipped_faculty = []
    for _fp, urls in groups.items():
        primary = urls[0]
        if any(s in primary for s in FACULTY_OWNED):
            skipped_faculty.append(primary)
            continue
        candidates.append((primary, urls))
    if args.section:
        candidates = [c for c in candidates if section_of(c[0]) == args.section]

    items, not_substantive, unrouted = [], [], []
    for primary, urls in candidates:
        item = build(primary, urls, boilerplate)
        if item is None:
            continue
        if not item["substantive"]:
            not_substantive.append((primary, item["reason"]))
            continue
        if not item["route"]["source_type"]:
            unrouted.append(primary)
            continue
        items.append(item)
    if args.limit:
        items = items[:args.limit]

    print(f"\n  distinct content pages   : {len(groups)}")
    print(f"  faculty-owned (skipped)  : {len(skipped_faculty)}")
    print(f"  not substantive          : {len(not_substantive)}")
    print(f"  unrouted                 : {len(unrouted)}")
    print(f"  to ingest                : {len(items)}")
    by_type = Counter(i["route"]["source_type"] for i in items)
    for t, n in by_type.most_common():
        print(f"      {n:>4}  {t}")

    if args.dry_run:
        print("\nDRY RUN - nothing written")
        return

    verify_connection()
    batch_id = f"pages_{datetime.now(timezone.utc):%Y%m%dT%H%M%S}_{uuid.uuid4().hex[:6]}"
    now = _now()
    try:
        before = snapshot()
        idx = existing_index()

        missing = sorted({i["route"]["parent_policy_id"] for i in items
                          if not gi.parent_exists(i["route"]["parent_policy_id"])})
        if missing:
            raise SystemExit(f"parent policies absent: {missing}; refusing to invent one")

        created = updated = links = reused = 0
        seen_fp: dict[str, str] = {}
        rows, reuse_rows = [], []

        for item in items:
            url, fp = item["url"], item["content"]["content_fingerprint"]

            hit = idx["by_url"].get(url) or idx["by_url"].get(canonical_url(url))
            if hit and not hit.get("own"):
                # Someone else's document already covers this URL -- reuse it.
                reused += 1
                reuse_rows.append({"url": url, "matched_doc_id": hit["doc_id"],
                                   "matched_on": "existing source_url"})
                continue
            # A page this pipeline created before is refreshed, not skipped.
            # Skipping would freeze whatever the extractor got wrong on the first
            # pass -- which is exactly how the phantom "2026-24" academic year
            # survived a re-run until this branch existed.
            fp_hit = idx["by_fingerprint"].get(fp)
            if fp_hit and not fp_hit.get("own"):
                hit = fp_hit
                reused += 1
                gi.record_alternate_url(hit["doc_id"], url, now,
                                        "identical page content already in the graph")
                reuse_rows.append({"url": url, "matched_doc_id": hit["doc_id"],
                                   "matched_on": "content fingerprint"})
                continue
            if fp in seen_fp:
                reused += 1
                gi.record_alternate_url(seen_fp[fp], url, now,
                                        "identical page content within this batch")
                reuse_rows.append({"url": url, "matched_doc_id": seen_fp[fp],
                                   "matched_on": "fingerprint within batch"})
                continue

            doc_id = doc_id_for(url, item["content"]["title"])
            was_created = gi.upsert_document(doc_id, props_for(item), now, batch_id)
            linked = gi.link_document(doc_id, item["route"]["parent_policy_id"],
                                      now, batch_id)
            # link_document sets relation from site_ingestion; restate it for pages
            run_query("""
                MATCH (:Policy {policy_id:$p})-[r:REFERENCES]->(:PolicyDocument {doc_id:$d})
                SET r.relation = $rel""",
                {"p": item["route"]["parent_policy_id"], "d": doc_id, "rel": RELATION})
            created += bool(was_created)
            updated += (not was_created)
            links += linked
            seen_fp[fp] = doc_id
            rows.append({"doc_id": doc_id, "title": item["content"]["title"],
                         "source_url": url,
                         "source_type": item["route"]["source_type"],
                         "parent_policy_id": item["route"]["parent_policy_id"],
                         "facts": len(item["facts"]),
                         "tables": len(item["content"]["tables"]),
                         "academic_years": item["academic_years"],
                         "aliases": len(item["aliases"]),
                         "created": was_created})

            # Mark this page and every alias that serves the same content, so a
            # resumed run skips them and coverage reflects the ingest.
            covered = {url, *item["aliases"]}
            for r in man.rows.values():
                if r.get("canonical_url") in covered:
                    man.update(r["resource_id"], Status.INGESTED, doc_id=doc_id,
                               ingested_by="page_content")

        after = snapshot()
        result = {"run_at": now, "ingest_batch_id": batch_id,
                  "pages_created": created, "pages_updated": updated,
                  "links_merged": links, "reused": reused,
                  "faculty_owned_skipped": skipped_faculty,
                  "not_substantive": not_substantive, "unrouted": unrouted,
                  "counts_before": before, "counts_after": after,
                  "rows": rows, "reuse_rows": reuse_rows}
    finally:
        close_driver()

    print(f"\n  batch id        : {batch_id}")
    print(f"  pages created   : {created}")
    print(f"  pages updated   : {updated}")
    print(f"  reused          : {reused}")
    print(f"  REFERENCES      : {links}")
    print("\n  baselines:")
    for k in BASELINE:
        flag = "OK" if before[k] == after[k] else "CHANGED"
        print(f"    {k:<18} {before[k]:>5} -> {after[k]:>5}  {flag}")
    print(f"    {'PolicyDocument':<18} {before['PolicyDocument']:>5} -> "
          f"{after['PolicyDocument']:>5}  (+{after['PolicyDocument']-before['PolicyDocument']})")

    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, ensure_ascii=False)
    print(f"\nWrote {args.report}")
    print(f"Undo:\n  MATCH (d:PolicyDocument {{ingest_batch_id:'{batch_id}'}}) DETACH DELETE d")


if __name__ == "__main__":
    main()

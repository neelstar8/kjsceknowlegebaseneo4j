"""Write the official Academics documents into Neo4j.

    data/academics_documents.json -> Neo4j -> data/academics_ingestion_report.json

Idempotent. Every document is MERGEd on its `doc_id` (already unique-constrained)
and every link is MERGEd, so running this twice inserts nothing the second time.
Nothing is ever deleted. No :Faculty, :FacultyMember, :PYQ, :PYQFile, :Subject,
:PolicyProvision, :Policy or existing examination :PolicyDocument node is
created or modified -- the one exception is the single examination calendar the
Academics section republishes under a second URL, which gains an
`alternate_source_url` property instead of being duplicated.

    .venv/bin/python -m scripts.ingest_academics_documents --dry-run
    .venv/bin/python -m scripts.ingest_academics_documents
"""
import argparse
import json
import os
from datetime import datetime, timezone

from graph import academics_ingestion as gi
from graph.neo4j_driver import close_driver, verify_connection

IN_PATH = "data/academics_documents.json"
REPORT_PATH = "data/academics_ingestion_report.json"


def _now():
    return datetime.now(timezone.utc).isoformat()


def ingest(knowledge: dict, dry_run: bool = False) -> dict:
    now = _now()
    meta = knowledge["meta"]
    documents = knowledge["documents"]
    reuse = knowledge.get("duplicate_reuse", [])

    ids = [d["doc_id"] for d in documents]
    if len(set(ids)) != len(ids):
        raise SystemExit("duplicate doc_id in the knowledge file")
    urls = [d["source_url"] for d in documents]
    if len(set(urls)) != len(urls):
        raise SystemExit("duplicate source_url in the knowledge file")

    unknown = {d["source_type"] for d in documents} - set(gi.SOURCE_TYPES)
    if unknown:
        raise SystemExit(f"unexpected source_type(s): {sorted(unknown)}")

    if not dry_run:
        if not gi.parent_exists():
            raise SystemExit(
                f"Academic parent policy '{gi.ACADEMIC_PARENT_ID}' is not in the graph. "
                "This script will not invent a parent node.")
        for r in reuse:
            if not gi.document_exists(r["existing_doc_id"]):
                raise SystemExit(
                    f"reuse target '{r['existing_doc_id']}' is missing; refusing to "
                    "create a duplicate of an already-published document.")

    created = links = 0
    rows = []
    for doc in documents:
        props = gi.document_props(doc, meta)
        if dry_run:
            extra = ""
            if doc.get("event_count"):
                extra = f"{doc['event_count']:>3} events"
            elif doc.get("branch_link_count"):
                extra = f"{doc['branch_link_count']:>3} branch links"
            elif doc.get("goal_count"):
                extra = f"{doc['goal_count']:>3} goals"
            elif doc.get("section_count"):
                extra = f"{doc['section_count']:>3} sections"
            print(f"  {doc['doc_id']:<34} {doc['source_type']:<26} {extra}")
            rows.append({"doc_id": doc["doc_id"], "created": None, "linked": None})
            continue
        was_created = gi.upsert_document(doc["doc_id"], props, now)
        linked = gi.link_document(doc["doc_id"], now)
        created += bool(was_created)
        links += linked
        rows.append({"doc_id": doc["doc_id"], "title": doc["title"],
                     "source_url": doc["source_url"], "source_type": doc["source_type"],
                     "created": was_created, "linked": bool(linked)})

    reused = []
    for r in reuse:
        if dry_run:
            print(f"  REUSE {r['existing_doc_id']} (+ alternate url, + Academics link)")
            continue
        info = gi.record_alternate_url(r["existing_doc_id"], r["academics_url"], now)
        linked = gi.link_document(r["existing_doc_id"], now)
        links += linked
        reused.append({**r, "alternate_url_recorded": bool(info),
                       "linked_from_academics": bool(linked)})

    result = {
        "run_at": now, "dry_run": dry_run,
        "documents_in_file": len(documents),
        "documents_created": created,
        "documents_updated": len(documents) - created if not dry_run else None,
        "links_merged": links,
        "reused_documents": reused,
        "parent_policy": gi.ACADEMIC_PARENT_ID,
        "rows": rows,
    }
    if not dry_run:
        result["graph_counts"] = gi.counts()
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="in_path", default=IN_PATH)
    ap.add_argument("--report", default=REPORT_PATH)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    knowledge = json.load(open(args.in_path, encoding="utf-8"))
    if not args.dry_run:
        verify_connection()
    try:
        result = ingest(knowledge, dry_run=args.dry_run)
    finally:
        close_driver()

    print(f"\n  documents in file : {result['documents_in_file']}")
    if not args.dry_run:
        print(f"  created           : {result['documents_created']}")
        print(f"  updated           : {result['documents_updated']}")
        print(f"  reused (no dupe)  : {len(result['reused_documents'])}")
        print(f"  REFERENCES merged : {result['links_merged']}")
        print("\n  graph totals:")
        for k, v in (result.get("graph_counts") or {}).items():
            print(f"    {k:<24} {v}")
        os.makedirs(os.path.dirname(args.report), exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)
        print(f"\nWrote {args.report}")


if __name__ == "__main__":
    main()

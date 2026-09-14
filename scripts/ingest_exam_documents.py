"""Write the official Examination documents into Neo4j.

    data/examination_documents.json -> Neo4j -> data/exam_ingestion_report.json

Idempotent. Every document is MERGEd on its `doc_id` (already unique-constrained)
and the link to the existing Examination policy is MERGEd, so running this twice
inserts nothing the second time. Nothing is ever deleted, and no :Faculty,
:FacultyMember, :PYQ, :PYQFile, :Subject, :PolicyProvision or existing :Policy
node is touched -- this script only adds :PolicyDocument nodes and one
REFERENCES edge each.

    .venv/bin/python -m scripts.ingest_exam_documents --dry-run   # prints, writes nothing
    .venv/bin/python -m scripts.ingest_exam_documents
"""
import argparse
import json
import os
from datetime import datetime, timezone

from graph import exam_ingestion as gi
from graph.neo4j_driver import close_driver, verify_connection

IN_PATH = "data/examination_documents.json"
REPORT_PATH = "data/exam_ingestion_report.json"


def _now():
    return datetime.now(timezone.utc).isoformat()


def ingest(knowledge: dict, dry_run: bool = False) -> dict:
    now = _now()
    meta = knowledge["meta"]
    documents = knowledge["documents"]

    expected = meta.get("expected_document_count")
    if expected is not None and len(documents) != expected:
        raise SystemExit(
            f"{IN_PATH} holds {len(documents)} documents but meta says "
            f"{expected} were expected. Refusing to ingest a partial set.")

    doc_ids = [d["doc_id"] for d in documents]
    if len(set(doc_ids)) != len(doc_ids):
        raise SystemExit("duplicate doc_id in the knowledge file")
    urls = [d["source_url"] for d in documents]
    if len(set(urls)) != len(urls):
        raise SystemExit("duplicate source_url in the knowledge file")

    if not dry_run and not gi.exam_policy_exists():
        # The documents hang from an Examination policy that must already be
        # there. Creating a placeholder to hold PDFs is exactly what this
        # ingest must not do.
        raise SystemExit(
            f"Examination policy '{gi.EXAM_POLICY_ID}' is not in the graph. "
            "Run the policy ingest first; this script will not invent a parent node.")

    created = links = 0
    rows = []
    for doc in documents:
        props = gi.document_props(doc, meta)
        if dry_run:
            print(f"  {doc['doc_id']:<48} {doc['academic_year']:<8} "
                  f"{doc['pages']}p  {len(doc.get('events') or []):>2} events")
            rows.append({"doc_id": doc["doc_id"], "created": None, "linked": None})
            continue
        was_created = gi.upsert_document(doc["doc_id"], props, now)
        linked = gi.link_document(doc["doc_id"], now)
        created += bool(was_created)
        links += linked
        rows.append({"doc_id": doc["doc_id"], "title": doc["title"],
                     "source_url": doc["source_url"], "created": was_created,
                     "linked": bool(linked)})

    result = {
        "run_at": now,
        "dry_run": dry_run,
        "documents_in_file": len(documents),
        "documents_created": created,
        "documents_updated": len(documents) - created if not dry_run else None,
        "links_merged": links,
        "parent_policy": gi.EXAM_POLICY_ID,
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
        print(f"  REFERENCES merged : {result['links_merged']}")
        print("\n  graph totals:")
        for key, value in (result.get("graph_counts") or {}).items():
            print(f"    {key:<22} {value}")
        os.makedirs(os.path.dirname(args.report), exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)
        print(f"\nWrote {args.report}")


if __name__ == "__main__":
    main()

"""Stage 4: normalized JSON -> Neo4j.

Refuses to run if validation reports a severe error. Safe to re-run any number
of times: PYQFile nodes merge on the Google Drive file ID and PYQ nodes merge
on a deterministic pyq_id, so a second run updates rather than duplicates.

Stores metadata and Drive links only. No PDF bytes ever reach the graph.

Usage:
    python -m scripts.ingest_pyq --dry-run
    python -m scripts.ingest_pyq
    python -m scripts.ingest_pyq --report-stale
"""
import argparse
import json
import logging
import os
from datetime import datetime, timezone

from dotenv import load_dotenv

from graph.neo4j_driver import close_driver, verify_connection
from graph.pyq_ingestion import counts, ensure_schema, stale_files, upsert_pyq
from normalization.pyq_normalizer import (
    build_alias_index,
    load_subjects,
    to_neo4j_properties,
)
from scripts.validate_pyq import validate

load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
NORM_FILE = os.path.join(DATA_DIR, "pyq_normalized.json")
REPORT_FILE = os.path.join(DATA_DIR, "pyq_ingestion_report.json")
ERROR_FILE = os.path.join(DATA_DIR, "pyq_errors.json")
STALE_FILE = os.path.join(DATA_DIR, "pyq_stale_files.json")

COLLECTION = os.environ.get("PYQ_COLLECTION_NAME", "pyq")


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(os.path.join(LOG_DIR, "pyq_ingest.log"))],
    )


def subject_lookup() -> dict:
    return {s["subject_key"]: s for s in load_subjects()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="infile", default=NORM_FILE)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--report", default=REPORT_FILE)
    parser.add_argument("--collection", default=None,
                        help="overrides the collection used for --report-stale; "
                             "defaults to the one recorded in the input file")
    parser.add_argument("--dry-run", action="store_true",
                        help="print what would be written and touch nothing")
    parser.add_argument("--report-stale", action="store_true",
                        help="also list PYQFile nodes this run no longer saw")
    parser.add_argument("--stale-report", default=STALE_FILE)
    args = parser.parse_args()

    setup_logging()
    log = logging.getLogger("ingest_pyq")

    with open(args.infile, encoding="utf-8") as f:
        payload = json.load(f)
    records = payload["records"]
    if args.limit:
        records = records[: args.limit]

    report = validate(records, tuple(payload.get("allowed_exam_types", ["ISE"])))
    if not report["passed"]:
        print("Refusing to ingest -- validation failed:")
        for error in report["severe_errors"][:20]:
            print("  -", error)
        return 1

    subjects = subject_lookup()
    run_started = datetime.now(timezone.utc).isoformat()

    if args.dry_run:
        print(f"DRY RUN -- nothing will be written.\n")
        for record in records[:  args.limit or len(records)]:
            paper, file_part = record["paper"], record["file"]
            print(f"  PYQ  {paper['pyq_id']}")
            print(f"       {paper['title']}")
            print(f"  FILE {file_part['file_name']}  ->  {file_part['drive_url']}")
        print(f"\nWould write {len(records)} (paper, file) pairs, "
              f"{len({r['paper']['pyq_id'] for r in records})} distinct papers, "
              f"{len({r['file']['drive_file_id'] for r in records})} distinct files.")
        return 0

    print("Verifying Neo4j connection...")
    verify_connection()
    ensure_schema()
    print("Connected. Constraints + indexes ensured.")

    before = counts()
    print(f"Before: PYQ={before['pyq']} PYQFile={before['pyq_file']} "
          f"Subject={before['subject']} FacultyMember={before['faculty_member']}")

    inserted = updated = failed = 0
    errors = []

    for i, record in enumerate(records, 1):
        paper, file_part = record["paper"], record["file"]
        try:
            subject = subjects.get(paper["subject_key"], {})
            created = upsert_pyq(
                pyq_id=paper["pyq_id"],
                pyq_props=to_neo4j_properties(paper),
                file_props={k: v for k, v in file_part.items() if v is not None},
                edge_props={k: v for k, v in paper["edge"].items() if v is not None},
                subject_key=paper["subject_key"],
                subject_name=paper.get("subject_name_canonical"),
                subject_code=paper.get("subject_code"),
                subject_status=paper["subject_status"],
                aliases=subject.get("aliases"),
                now=run_started,
                is_bundle=bool(paper.get("is_bundle")),
            )
            inserted += int(created)
            updated += int(not created)
            log.debug("upsert %s created=%s exam_type=%s source=%s file=%s",
                      paper["pyq_id"], created, paper["exam_type"],
                      paper["exam_type_source"], file_part["file_name"])
        except Exception as e:
            failed += 1
            errors.append({
                "drive_file_id": file_part.get("drive_file_id"),
                "file_name": file_part.get("file_name"),
                "pyq_id": paper.get("pyq_id"),
                "stage": "ingest",
                "error": f"{type(e).__name__}: {e}",
            })
            log.exception("failed on %s", file_part.get("file_name"))
        print(f"  {i}/{len(records)}  inserted={inserted} updated={updated} "
              f"failed={failed}", end="\r", flush=True)
    print(" " * 70, end="\r")

    after = counts()

    stale = []
    if args.report_stale:
        # Scoped to this collection, so an ESE run can never report every ISE
        # file as missing.
        collection = args.collection or payload.get("collection") or COLLECTION
        stale = stale_files(collection, run_started)
        with open(args.stale_report, "w", encoding="utf-8") as f:
            json.dump({"generated_at": run_started, "count": len(stale),
                       "note": "Reported only. Nothing is ever deleted.",
                       "files": stale}, f, indent=2, ensure_ascii=False)

    ingestion_report = {
        "retrieval_timestamp": payload.get("retrieved_at"),
        "normalized_at": payload.get("normalized_at"),
        "ingested_at": run_started,
        "source_url": payload.get("source"),
        "collection": payload.get("collection"),
        "branch": payload.get("branch"),
        "allowed_exam_types": payload.get("allowed_exam_types"),
        "total_considered_this_run": len(records),
        "total_inserted": inserted,
        "total_updated": updated,
        "total_failed": failed,
        "unresolved_subject_count": report["unresolved_subject_count"],
        "warning_count": report["warning_count"],
        "counts_before": before,
        "counts_after": after,
        "stale_file_count": len(stale),
    }
    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(ingestion_report, f, indent=2, ensure_ascii=False)

    if errors:
        existing = {"errors": []}
        if os.path.exists(ERROR_FILE):
            with open(ERROR_FILE, encoding="utf-8") as f:
                existing = json.load(f)
        existing.setdefault("errors", []).extend(errors)
        with open(ERROR_FILE, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"Inserted: {inserted}")
    print(f"Updated:  {updated}")
    print(f"Failed:   {failed}")
    print(f"After:  PYQ={after['pyq']} PYQFile={after['pyq_file']} "
          f"Subject={after['subject']} FacultyMember={after['faculty_member']}")
    if args.report_stale:
        print(f"Stale files (reported, not deleted): {len(stale)}")
    print(f"\n-> {os.path.relpath(args.report)}")

    close_driver()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

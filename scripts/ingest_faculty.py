"""Stage 4: normalized JSON -> Neo4j.

Refuses to run if validation reports a severe error. Safe to re-run: nodes
are merged on the official faculty_id, and empty source values never erase
existing data.

Usage:
    python -m scripts.ingest_faculty --in data/faculty_normalized_batch10.json
    python -m scripts.ingest_faculty --limit 50
"""
import argparse
import json
import os
from datetime import datetime, timezone

from graph.faculty_ingestion import (
    count_faculty_members,
    ensure_schema,
    fetch_existing,
    merge_properties,
    upsert_faculty_member,
)
from graph.neo4j_driver import close_driver, verify_connection
from normalization.faculty_normalizer import to_neo4j_properties
from scripts.validate_faculty import validate

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
NORM_FILE = os.path.join(DATA_DIR, "faculty_normalized.json")
REPORT_FILE = os.path.join(DATA_DIR, "faculty_ingestion_report.json")
ERROR_FILE = os.path.join(DATA_DIR, "faculty_errors.json")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="infile", default=NORM_FILE)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--report", default=REPORT_FILE)
    args = parser.parse_args()

    with open(args.infile, encoding="utf-8") as f:
        payload = json.load(f)
    records = payload["faculty"]
    if args.limit:
        records = records[: args.limit]

    report = validate(records)
    if not report["passed"]:
        print("Refusing to ingest -- validation failed:")
        for e in report["severe_errors"]:
            print("  -", e)
        return 1

    print("Verifying Neo4j connection...")
    verify_connection()
    ensure_schema()
    print("Connected. Constraint + :Faculty root ensured.")

    before = count_faculty_members()
    print(f"FacultyMember nodes before: {before}")

    ids = [r["faculty_id"] for r in records if r.get("faculty_id")]
    existing = fetch_existing(ids)
    print(f"Already in graph: {len(existing)} of {len(ids)}")

    inserted = updated = failed = 0
    errors = []

    for i, record in enumerate(records, 1):
        fid = record.get("faculty_id")
        try:
            props = to_neo4j_properties(record)
            props = merge_properties(existing.get(fid, {}), props)
            props.pop("faculty_id", None)  # part of the MERGE key
            created = upsert_faculty_member(fid, props)
            if created:
                inserted += 1
            else:
                updated += 1
        except Exception as e:
            failed += 1
            errors.append({
                "source_id": fid,
                "name": record.get("name"),
                "stage": "ingest",
                "error": f"{type(e).__name__}: {e}",
            })
        print(f"  {i}/{len(records)}  inserted={inserted} updated={updated} "
              f"failed={failed}", end="\r", flush=True)
    print(" " * 70, end="\r")

    after = count_faculty_members()

    ingestion_report = {
        "retrieval_timestamp": payload.get("retrieved_at"),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "source_url": payload.get("source"),
        "total_discovered": payload.get("total_reported_by_source"),
        "total_normalized": len(payload["faculty"]),
        "total_considered_this_run": len(records),
        "total_inserted": inserted,
        "total_updated": updated,
        "total_failed": failed,
        "duplicate_count": report["duplicate_ids"],
        "missing_name_count": report["missing_names"],
        "missing_profile_count": report["missing_profile_urls"],
        "faculty_with_empty_profiles": report["faculty_with_empty_profiles"],
        "faculty_with_parsing_errors": report["parsing_errors"],
        "neo4j_count_before": before,
        "neo4j_count_after": after,
    }
    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(ingestion_report, f, indent=2, ensure_ascii=False)

    if errors:
        existing_errors = {"errors": []}
        if os.path.exists(ERROR_FILE):
            with open(ERROR_FILE, encoding="utf-8") as f:
                existing_errors = json.load(f)
        existing_errors.setdefault("errors", []).extend(errors)
        with open(ERROR_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_errors, f, indent=2, ensure_ascii=False)

    print(f"Inserted: {inserted}")
    print(f"Updated:  {updated}")
    print(f"Failed:   {failed}")
    print(f"Total:    {len(records)}")
    print(f"Neo4j FacultyMember count: {after}")
    print(f"\n-> {os.path.relpath(args.report)}")

    close_driver()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

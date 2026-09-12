"""Stage 3: validate the normalized dataset before it is allowed near Neo4j.

Writes data/faculty_validation_report.json and exits non-zero on a severe
problem (duplicate ids, missing ids/names) so the ingest step can refuse to run.

Usage:
    python -m scripts.validate_faculty
    python -m scripts.validate_faculty --in data/faculty_normalized_batch10.json \
                                       --out data/faculty_validation_report_batch10.json
"""
import argparse
import json
import os
from collections import Counter
from datetime import datetime, timezone

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
NORM_FILE = os.path.join(DATA_DIR, "faculty_normalized.json")
REPORT_FILE = os.path.join(DATA_DIR, "faculty_validation_report.json")


def validate(records: list[dict]) -> dict:
    ids = [r.get("faculty_id") for r in records]
    names = [(r.get("name") or "").strip() for r in records]

    id_counts = Counter(i for i in ids if i)
    name_counts = Counter(n.lower() for n in names if n)

    duplicate_ids = {k: v for k, v in id_counts.items() if v > 1}
    duplicate_names = {k: v for k, v in name_counts.items() if v > 1}

    empty_profiles = [
        r.get("faculty_id") for r in records if not r.get("profile_fetched")
    ]
    no_sections = [
        r.get("faculty_id")
        for r in records
        if not any(
            r.get(f)
            for f in ("education", "subjects_taught", "publications",
                      "professional_experience", "introduction")
        )
    ]

    report = {
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "total_records": len(records),
        "unique_ids": len(id_counts),
        "unique_names": len(name_counts),
        "duplicate_ids": len(duplicate_ids),
        "duplicate_names": len(duplicate_names),
        "missing_ids": sum(1 for i in ids if not i),
        "missing_names": sum(1 for n in names if not n),
        "missing_profile_urls": sum(1 for r in records if not r.get("profile_url")),
        "missing_emails": sum(1 for r in records if not r.get("official_email")),
        "missing_departments": sum(1 for r in records if not r.get("department")),
        "missing_designations": sum(1 for r in records if not r.get("designation")),
        "profiles_not_fetched": len(empty_profiles),
        "faculty_with_empty_profiles": len(no_sections),
        "parsing_errors": 0,
        "duplicate_id_values": duplicate_ids,
        "duplicate_name_values": dict(list(duplicate_names.items())[:20]),
    }

    # Severe = would corrupt the graph. Sparse optional fields are not severe;
    # plenty of real profiles genuinely have nothing filled in.
    severe = []
    if report["duplicate_ids"]:
        severe.append(f"{report['duplicate_ids']} duplicate faculty_id values")
    if report["missing_ids"]:
        severe.append(f"{report['missing_ids']} records without a faculty_id")
    if report["missing_names"]:
        severe.append(f"{report['missing_names']} records without a name")
    if report["total_records"] == 0:
        severe.append("no records at all")
    report["severe_errors"] = severe
    report["passed"] = not severe
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="infile", default=NORM_FILE)
    parser.add_argument("--out", dest="outfile", default=REPORT_FILE)
    args = parser.parse_args()

    with open(args.infile, encoding="utf-8") as f:
        records = json.load(f)["faculty"]

    report = validate(records)
    with open(args.outfile, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    for key in (
        "total_records", "unique_ids", "unique_names", "duplicate_ids",
        "duplicate_names", "missing_ids", "missing_names",
        "missing_profile_urls", "missing_emails", "missing_departments",
        "profiles_not_fetched", "faculty_with_empty_profiles", "parsing_errors",
    ):
        print(f"{key:30s} {report[key]}")

    print(f"\n-> {os.path.relpath(args.outfile)}")
    if report["passed"]:
        print("VALIDATION PASSED")
        return 0
    print("VALIDATION FAILED:")
    for e in report["severe_errors"]:
        print("  -", e)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

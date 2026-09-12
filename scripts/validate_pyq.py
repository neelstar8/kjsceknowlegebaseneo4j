"""Stage 3: pre-insert validation.

Severe errors block ingestion outright; warnings are reported and ingested.
Mirrors scripts/validate_faculty.py's contract, which scripts/ingest_pyq.py
relies on the same way scripts/ingest_faculty.py does.

Usage:
    python -m scripts.validate_pyq
"""
import argparse
import json
import os
from collections import Counter
from datetime import datetime, timezone

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
NORM_FILE = os.path.join(DATA_DIR, "pyq_normalized.json")
REPORT_FILE = os.path.join(DATA_DIR, "pyq_validation_report.json")

# A record without these cannot produce a usable answer for a student, so it
# must never reach the graph.
REQUIRED_FILE_FIELDS = ["drive_file_id", "drive_url"]
REQUIRED_PAPER_FIELDS = ["pyq_id", "subject_key", "exam_type"]


def validate(records: list[dict], allowed_exam_types=("ISE",)) -> dict:
    severe, warnings = [], []

    for i, record in enumerate(records):
        file_part, paper = record.get("file", {}), record.get("paper", {})
        label = file_part.get("file_name") or f"record #{i}"

        for field in REQUIRED_FILE_FIELDS:
            if not file_part.get(field):
                severe.append(f"{label}: missing file.{field}")
        for field in REQUIRED_PAPER_FIELDS:
            if not paper.get(field):
                severe.append(f"{label}: missing paper.{field}")

        if paper.get("exam_type") and paper["exam_type"] not in allowed_exam_types:
            severe.append(
                f"{label}: exam_type {paper['exam_type']} is not allowed in this phase"
            )

        url = file_part.get("drive_url") or ""
        if url and not url.startswith("https://drive.google.com/"):
            severe.append(f"{label}: drive_url is not a Google Drive URL ({url})")

        # Anything that would store paper content rather than a pointer to it.
        for forbidden in ("content", "text", "body", "binary", "base64", "pages_text"):
            if forbidden in file_part or forbidden in paper:
                severe.append(f"{label}: record carries '{forbidden}' -- PYQ nodes "
                              "must hold metadata and links only")

        if not paper.get("academic_year"):
            warnings.append(f"{label}: academic_year unknown")
        if not paper.get("semester"):
            warnings.append(f"{label}: semester unknown")
        if paper.get("subject_status") == "unresolved":
            warnings.append(f"{label}: subject unresolved ({paper.get('subject_raw')})")

    # The same (paper, file) pair appearing twice would make counts meaningless.
    pairs = Counter((r.get("paper", {}).get("pyq_id"),
                     r.get("file", {}).get("drive_file_id")) for r in records)
    duplicate_pairs = [p for p, c in pairs.items() if c > 1]
    for pyq_id, file_id in duplicate_pairs:
        severe.append(f"duplicate (pyq_id, drive_file_id) pair: {pyq_id} / {file_id}")

    return {
        "passed": not severe,
        "total_records": len(records),
        "severe_errors": severe,
        "warnings": warnings,
        "severe_error_count": len(severe),
        "warning_count": len(warnings),
        "duplicate_pair_count": len(duplicate_pairs),
        "distinct_papers": len({r.get("paper", {}).get("pyq_id") for r in records}),
        "distinct_files": len({r.get("file", {}).get("drive_file_id") for r in records}),
        "unresolved_subject_count": sum(
            1 for r in records
            if r.get("paper", {}).get("subject_status") == "unresolved"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="infile", default=NORM_FILE)
    parser.add_argument("--report", default=REPORT_FILE)
    args = parser.parse_args()

    with open(args.infile, encoding="utf-8") as f:
        payload = json.load(f)

    report = validate(payload["records"],
                      tuple(payload.get("allowed_exam_types", ["ISE"])))
    report["validated_at"] = datetime.now(timezone.utc).isoformat()

    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Records:          {report['total_records']}")
    print(f"Distinct papers:  {report['distinct_papers']}")
    print(f"Distinct files:   {report['distinct_files']}")
    print(f"Unresolved subj:  {report['unresolved_subject_count']}")
    print(f"Severe errors:    {report['severe_error_count']}")
    print(f"Warnings:         {report['warning_count']}")
    for error in report["severe_errors"][:10]:
        print("  ERROR:", error)
    print(f"\nPASSED: {report['passed']}")
    print(f"-> {os.path.relpath(args.report)}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

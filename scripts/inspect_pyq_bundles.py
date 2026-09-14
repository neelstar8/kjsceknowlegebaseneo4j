"""Stage 2.5: split semester-bundle PDFs into the subjects they actually hold.

Runs between normalize and validate, and only on records the normalizer marked
`is_bundle`. For each one it downloads the PDF, reads the pages, and asks
normalization/pyq_pdf_subjects which registry subjects the pages evidence.

  * subjects found  -> the bundle record is REPLACED by one subject-level
                       record per subject, carrying its page range on the
                       STORED_IN edge
  * nothing found   -> the bundle record is kept exactly as it was

The downloaded bytes are read in memory and dropped. No page text, no chunk and
no embedding is written anywhere; the only thing that survives is
{subject_key, page_start, page_end}.

Usage:
    .venv/bin/python -m scripts.inspect_pyq_bundles --in data/pyq_ese_normalized.json
    .venv/bin/python -m scripts.inspect_pyq_bundles --in ... --dry-run
"""
import argparse
import copy
import json
import logging
import os
from datetime import datetime, timezone

from dotenv import load_dotenv

from drive.client import close_service, download_file, verify_connection
from normalization.pyq_normalizer import (
    build_alias_index,
    build_pyq_id,
    build_title,
    load_subjects,
)
from normalization.pyq_pdf_subjects import extract_subject_pages

load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")

# Bundles run to a few MB; anything far past that is not a question paper.
MAX_PDF_BYTES = 60 * 1024 * 1024


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(
            os.path.join(LOG_DIR, "pyq_bundle_inspect.log"))])


def _subject_record(bundle_record, span, subject) -> dict:
    """One subject-level record carved out of a bundle."""
    record = copy.deepcopy(bundle_record)
    paper = record["paper"]
    semester = paper.get("semester")

    paper["subject_key"] = span["subject_key"]
    paper["subject"] = subject.get("name") or span["subject_key"]
    paper["subject_name_canonical"] = subject.get("name")
    paper["subject_raw"] = span["evidence"]
    # Established by reading the pages, not by guessing from the file name.
    paper["subject_status"] = "resolved"
    paper["subject_source"] = "pdf_inspection"
    paper["subject_evidence"] = span["evidence"]
    paper["is_bundle"] = False
    paper["from_bundle"] = True
    paper["subject_code"] = subject.get("code") or paper.get("subject_code")
    paper["pyq_id"] = build_pyq_id(
        span["subject_key"], paper.get("exam_type"), paper.get("academic_year"),
        paper.get("exam_term"), semester, paper.get("course_category"),
        paper.get("variant"))
    paper["title"] = build_title(
        paper["subject"], paper.get("exam_type"), semester,
        paper.get("academic_year"), paper.get("course_category"),
        paper.get("variant"))
    paper["edge"] = dict(paper.get("edge") or {})
    paper["edge"]["page_start"] = span["page_start"]
    paper["edge"]["page_end"] = span["page_end"]
    paper["edge"]["page_label"] = (
        f"pages {span['page_start']}-{span['page_end']}"
        if span["page_end"] > span["page_start"] else f"page {span['page_start']}")
    paper["edge"]["part_index"] = span["page_start"]
    paper["edge"]["section_label"] = paper["subject"]
    record["reasons"] = [r for r in record.get("reasons", [])
                         if r != "semester_bundle"] + ["split_from_bundle"]
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="infile", required=True)
    parser.add_argument("--out", default=None,
                        help="defaults to rewriting the input file in place")
    parser.add_argument("--report", default=None)
    parser.add_argument("--limit", type=int, default=None,
                        help="inspect at most this many bundles")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    setup_logging()
    log = logging.getLogger("inspect_pyq_bundles")

    out_file = args.out or args.infile
    report_file = args.report or os.path.join(
        DATA_DIR, os.path.basename(args.infile).replace(
            "normalized.json", "bundle_report.json"))

    with open(args.infile, encoding="utf-8") as f:
        payload = json.load(f)
    records = payload["records"]

    bundles = [r for r in records if r["paper"].get("is_bundle")]
    if args.limit:
        bundles = bundles[: args.limit]
    print(f"Bundles to inspect: {len(bundles)}")
    if not bundles:
        return 0

    alias_index = build_alias_index(load_subjects())
    subjects = load_subjects()
    by_key = {s["subject_key"]: s for s in subjects}

    if args.dry_run:
        for record in bundles:
            print(f"  {record['file']['file_name']}  ->  "
                  f"{record['file']['drive_url']}")
        print(f"\nWould download and inspect {len(bundles)} bundle(s).")
        return 0

    print("Verifying Google Drive connection...")
    verify_connection(payload.get("root_folder_id") or None)

    split_records, kept, split_count, failed = [], 0, 0, 0
    audit = []

    for i, record in enumerate(bundles, 1):
        file_part = record["file"]
        file_id = file_part["drive_file_id"]
        entry = {"file_name": file_part["file_name"],
                 "drive_file_id": file_id,
                 "drive_url": file_part["drive_url"]}
        try:
            pdf_bytes = download_file(file_id, max_bytes=MAX_PDF_BYTES)
            spans = extract_subject_pages(pdf_bytes, alias_index, subjects)
            del pdf_bytes  # nothing downloaded is retained
        except Exception as e:
            failed += 1
            entry.update({"outcome": "error", "error": f"{type(e).__name__}: {e}"})
            audit.append(entry)
            log.exception("bundle inspection failed for %s",
                          file_part["file_name"])
            print(f"  {i}/{len(bundles)}  split={split_count} kept={kept} "
                  f"failed={failed}", end="\r", flush=True)
            continue

        if spans:
            for span in spans:
                split_records.append(_subject_record(
                    record, span, by_key.get(span["subject_key"], {})))
            split_count += 1
            entry.update({"outcome": "split", "subjects": [
                {"subject_key": s["subject_key"], "page_start": s["page_start"],
                 "page_end": s["page_end"], "evidence": s["evidence"]}
                for s in spans]})
        else:
            kept += 1
            entry.update({"outcome": "kept_as_bundle",
                          "note": "no subject could be established from the pages"})
        audit.append(entry)
        print(f"  {i}/{len(bundles)}  split={split_count} kept={kept} "
              f"failed={failed}", end="\r", flush=True)
    print(" " * 70, end="\r")

    # Bundles that were split are replaced; every other record passes through.
    split_ids = {e["drive_file_id"] for e in audit if e.get("outcome") == "split"}
    rebuilt = [r for r in records
               if not (r["paper"].get("is_bundle")
                       and r["file"]["drive_file_id"] in split_ids)]
    rebuilt.extend(split_records)

    now = datetime.now(timezone.utc).isoformat()
    payload["records"] = rebuilt
    payload["total_papers"] = len(rebuilt)
    payload["bundles_inspected_at"] = now
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump({"generated_at": now,
                   "note": "PDFs were read to identify subjects. No page text, "
                           "chunk or embedding is stored anywhere.",
                   "bundles_inspected": len(bundles),
                   "bundles_split": split_count,
                   "bundles_kept_unresolved": kept,
                   "bundles_failed": failed,
                   "subject_papers_created": len(split_records),
                   "bundles": audit}, f, indent=2, ensure_ascii=False)

    print(f"Bundles inspected:    {len(bundles)}")
    print(f"  split into subjects:{split_count}  ({len(split_records)} papers)")
    print(f"  kept as bundles:    {kept}")
    print(f"  failed to read:     {failed}")
    print(f"\n-> {os.path.relpath(out_file)}")
    print(f"-> {os.path.relpath(report_file)}")
    close_service()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

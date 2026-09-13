"""Stage 2: raw Drive dump -> data/pyq_normalized.json plus review reports.

Nothing here touches the network or Neo4j, so it is cheap to re-run every time
you add a subject alias or an override.

Runs once per collection. `--tag` keeps each collection's outputs in their own
files, so normalizing the ESE corpus can never clobber the ISE one:

    python -m scripts.normalize_pyq
    python -m scripts.normalize_pyq --tag ese --in data/pyq_ese_drive_raw.json \
        --exam-types ESE --min-year 2019 --max-year 2025 \
        --collection ese_question_paper_kj_somaiya

Four reports come out alongside the normalized data:
    <tag>unknown_report.json    -- everything a human should look at
    <tag>filtered_report.json   -- parsed fine, but outside the exam-type/year scope
    <tag>collisions.json        -- distinct files that parsed to the same paper
    <tag>summary.json           -- the counts, for reporting on the run
"""
import argparse
import json
import os
from collections import defaultdict
from datetime import datetime, timezone

from dotenv import load_dotenv

from normalization.pyq_normalizer import (
    build_alias_index,
    load_overrides,
    load_subjects,
    normalize_pyq,
    year_in_window,
)

load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RAW_FILE = os.path.join(DATA_DIR, "pyq_drive_raw.json")

BRANCH = os.environ.get("PYQ_DEFAULT_BRANCH", "Computer Engineering")
COLLECTION = os.environ.get("PYQ_COLLECTION_NAME", "pyq")
ALLOWED_EXAM_TYPES = os.environ.get("PYQ_ALLOWED_EXAM_TYPES", "ISE")

# Reasons that mean "no node was created", as opposed to "node created, but
# look at it". ESE is no longer among them -- it is an ingestible exam type.
REJECTION_REASONS = {
    "excluded_syllabus", "excluded_archive", "excluded_mime",
    "exam_type_ambiguous", "exam_type_unknown",
}


def data_path(tag: str, name: str) -> str:
    prefix = f"pyq_{tag}_" if tag else "pyq_"
    return os.path.join(DATA_DIR, f"{prefix}{name}")


def _review_entry(raw_file, reasons, extra=None):
    entry = {
        "file_name": raw_file.get("file_name"),
        "folder_path": raw_file.get("folder_path"),
        "drive_file_id": raw_file.get("drive_file_id"),
        "drive_url": raw_file.get("drive_url"),
        "mime_type": raw_file.get("mime_type"),
        "reasons": reasons,
    }
    if extra:
        entry.update(extra)
    return entry


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="infile", default=RAW_FILE)
    parser.add_argument("--tag", default="",
                        help="names this collection's output files, e.g. 'ese'")
    parser.add_argument("--out", default=None)
    parser.add_argument("--collection", default=COLLECTION)
    parser.add_argument("--branch", default=BRANCH)
    parser.add_argument("--exam-types", default=ALLOWED_EXAM_TYPES,
                        help="comma-separated, e.g. 'ISE,ESE'")
    parser.add_argument("--default-exam-type", default=None,
                        help="exam type for files whose name and folder path "
                             "say nothing; the ESE tree names it nowhere, so "
                             "the operator asserts it per collection")
    parser.add_argument("--min-year", type=int, default=None,
                        help="drop papers whose every plausible year is earlier")
    parser.add_argument("--max-year", type=int, default=None)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    out_file = args.out or data_path(args.tag, "normalized.json")
    allowed = {t.strip().upper() for t in args.exam_types.split(",") if t.strip()}

    with open(args.infile, encoding="utf-8") as f:
        payload = json.load(f)
    raw_files = payload["files"]
    if args.limit:
        raw_files = raw_files[: args.limit]

    alias_index = build_alias_index(load_subjects())
    overrides = load_overrides()

    records, unknown, filtered, excluded = [], [], [], []
    reason_counts = defaultdict(int)
    by_pyq_id = defaultdict(list)
    # Counted per Drive file, which is what "how many PDFs" means to a human.
    seen_file_ids = set()
    repeat_file_ids = set()
    exam_type_files = defaultdict(set)
    skipped_year_files, skipped_unclassified_files = set(), set()
    mapped_file_ids = set()

    for raw in raw_files:
        file_id = raw.get("drive_file_id")
        if file_id in seen_file_ids:
            repeat_file_ids.add(file_id)
        seen_file_ids.add(file_id)

        result = normalize_pyq(raw, alias_index, branch=args.branch,
                               collection=args.collection, overrides=overrides,
                               default_exam_type=args.default_exam_type)
        reasons = [r for r in result["reasons"] if r]
        for reason in reasons:
            reason_counts[reason] += 1

        exam_type = (result.get("exam") or {}).get("exam_type")
        if exam_type:
            exam_type_files[exam_type].add(file_id)

        if any(r in REJECTION_REASONS for r in reasons):
            entry = _review_entry(raw, reasons)
            excluded.append(entry)
            if not any(r.startswith("excluded_") for r in reasons):
                # Could not be confidently classified, as opposed to being a
                # file type we never ingest.
                skipped_unclassified_files.add(file_id)
                unknown.append(entry)
            continue

        if reasons:
            unknown.append(_review_entry(raw, reasons))

        for paper in result["papers"]:
            if paper["exam_type"] not in allowed:
                reason_counts["filtered_exam_type"] += 1
                filtered.append(_review_entry(
                    raw, reasons + ["filtered_exam_type"],
                    {"exam_type": paper["exam_type"]}))
                continue

            in_window, year_reason = year_in_window(
                paper.get("academic_year"), paper.get("exam_year"),
                args.min_year, args.max_year)
            if not in_window:
                reason_counts[year_reason] += 1
                if year_reason == "year_unknown":
                    skipped_unclassified_files.add(file_id)
                else:
                    skipped_year_files.add(file_id)
                filtered.append(_review_entry(
                    raw, reasons + [year_reason],
                    {"exam_type": paper["exam_type"],
                     "academic_year": paper.get("academic_year"),
                     "exam_year": paper.get("exam_year")}))
                continue

            record = {"file": result["file"], "paper": paper, "reasons": reasons}
            records.append(record)
            mapped_file_ids.add(file_id)
            by_pyq_id[paper["pyq_id"]].append(record)

    # A file that produced at least one mapped paper is mapped, even if another
    # paper inside it fell outside the window.
    skipped_year_files -= mapped_file_ids
    skipped_unclassified_files -= mapped_file_ids

    # A pyq_id shared by several distinct Drive files is legitimate when the
    # paper was split across files, and a genuine ambiguity otherwise. Both are
    # merged (so every link stays reachable), but the ambiguous case is flagged.
    collisions = []
    for pyq_id, group in by_pyq_id.items():
        file_ids = {r["file"]["drive_file_id"] for r in group}
        if len(file_ids) < 2:
            continue
        parts = [r["paper"]["edge"].get("part_index") for r in group]
        explained = all(p is not None for p in parts) and len(set(parts)) == len(parts)
        collisions.append({
            "pyq_id": pyq_id,
            "files": [{"file_name": r["file"]["file_name"],
                       "drive_url": r["file"]["drive_url"],
                       "page_label": r["paper"]["edge"].get("page_label")}
                      for r in group],
            "explained_by_page_labels": explained,
            "note": ("one paper split across files -- expected"
                     if explained else
                     "distinct files parsed to the same paper -- please verify"),
        })
        if not explained:
            reason_counts["pyq_id_collision_unexplained"] += 1

    now = datetime.now(timezone.utc).isoformat()
    summary = {
        "generated_at": now,
        "source": payload.get("source"),
        "collection": args.collection,
        "allowed_exam_types": sorted(allowed),
        "year_window": {"min": args.min_year, "max": args.max_year},
        "default_exam_type": args.default_exam_type,
        "total_raw_files": len(raw_files),
        "distinct_drive_files": len(seen_file_ids),
        "repeated_drive_file_ids": len(repeat_file_ids),
        "files_by_detected_exam_type": {
            k: len(v) for k, v in sorted(exam_type_files.items())},
        "files_mapped": len(mapped_file_ids),
        "papers_mapped": len(records),
        "files_skipped_out_of_year_window": len(skipped_year_files),
        "files_skipped_unclassified": len(skipped_unclassified_files),
        "files_excluded_by_type": len(
            [e for e in excluded if any(r.startswith("excluded_")
                                        for r in e["reasons"])]),
        "pyq_id_collisions": len(collisions),
        "reason_counts": dict(sorted(reason_counts.items())),
    }

    out_payload = {
        "source": payload.get("source"),
        "retrieved_at": payload.get("retrieved_at"),
        "normalized_at": now,
        "branch": args.branch,
        "collection": args.collection,
        "allowed_exam_types": sorted(allowed),
        "year_window": {"min": args.min_year, "max": args.max_year},
        "total_raw_files": len(raw_files),
        "total_papers": len(records),
        "total_files_with_papers": len(mapped_file_ids),
        "reason_counts": dict(sorted(reason_counts.items())),
        "records": records,
    }
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, indent=2, ensure_ascii=False)

    for name, body in [
        ("unknown_report.json", {"generated_at": now, "count": len(unknown),
                                 "excluded": excluded, "needs_review": unknown}),
        ("filtered_report.json", {
            "generated_at": now, "count": len(filtered),
            "note": "Parsed successfully but outside the exam-type or year scope.",
            "papers": filtered}),
        ("collisions.json", {"generated_at": now, "count": len(collisions),
                             "collisions": collisions}),
        ("summary.json", summary),
    ]:
        with open(data_path(args.tag, name), "w", encoding="utf-8") as f:
            json.dump(body, f, indent=2, ensure_ascii=False)

    print(f"Raw files:          {len(raw_files)}")
    print(f"Detected exam types:{summary['files_by_detected_exam_type']}")
    print(f"Papers mapped:      {len(records)}")
    print(f"Files mapped:       {len(mapped_file_ids)}")
    print(f"Skipped (year):     {len(skipped_year_files)}")
    print(f"Skipped (unclass.): {len(skipped_unclassified_files)}")
    print(f"Filtered entries:   {len(filtered)}")
    print(f"Excluded:           {len(excluded)}")
    print(f"Needs review:       {len(unknown)}")
    print(f"Collisions:         {len(collisions)}")
    if reason_counts:
        print("\nReasons:")
        for reason, count in sorted(reason_counts.items()):
            print(f"  {reason:34} {count}")
    print(f"\n-> {os.path.relpath(out_file)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

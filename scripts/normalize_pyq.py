"""Stage 2: raw Drive dump -> data/pyq_normalized.json plus review reports.

Nothing here touches the network or Neo4j, so it is cheap to re-run every time
you add a subject alias or an override.

Three reports come out alongside the normalized data:
    pyq_unknown_report.json  -- everything a human should look at
    pyq_ese_report.json      -- ESE papers, deliberately not ingested in phase 1
    pyq_collisions.json      -- distinct files that parsed to the same paper

Usage:
    python -m scripts.normalize_pyq
    python -m scripts.normalize_pyq --in data/pyq_raw20.json
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
)

load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RAW_FILE = os.path.join(DATA_DIR, "pyq_drive_raw.json")
NORM_FILE = os.path.join(DATA_DIR, "pyq_normalized.json")
UNKNOWN_FILE = os.path.join(DATA_DIR, "pyq_unknown_report.json")
ESE_FILE = os.path.join(DATA_DIR, "pyq_ese_report.json")
COLLISION_FILE = os.path.join(DATA_DIR, "pyq_collisions.json")

BRANCH = os.environ.get("PYQ_DEFAULT_BRANCH", "Computer Engineering")
COLLECTION = os.environ.get("PYQ_COLLECTION_NAME", "pyq")
ALLOWED_EXAM_TYPES = {
    t.strip().upper()
    for t in os.environ.get("PYQ_ALLOWED_EXAM_TYPES", "ISE").split(",") if t.strip()
}

# Reasons that mean "no node was created", as opposed to "node created, but
# look at it".
REJECTION_REASONS = {
    "excluded_syllabus", "excluded_archive", "excluded_mime",
    "exam_type_ese", "exam_type_ambiguous", "exam_type_unknown",
}


def _review_entry(raw_file, reasons):
    return {
        "file_name": raw_file.get("file_name"),
        "folder_path": raw_file.get("folder_path"),
        "drive_file_id": raw_file.get("drive_file_id"),
        "drive_url": raw_file.get("drive_url"),
        "mime_type": raw_file.get("mime_type"),
        "reasons": reasons,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="infile", default=RAW_FILE)
    parser.add_argument("--out", default=NORM_FILE)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    with open(args.infile, encoding="utf-8") as f:
        payload = json.load(f)
    raw_files = payload["files"]
    if args.limit:
        raw_files = raw_files[: args.limit]

    alias_index = build_alias_index(load_subjects())
    overrides = load_overrides()

    records, unknown, ese, excluded = [], [], [], []
    reason_counts = defaultdict(int)
    by_pyq_id = defaultdict(list)

    for raw in raw_files:
        result = normalize_pyq(raw, alias_index, branch=BRANCH,
                               collection=COLLECTION, overrides=overrides)
        reasons = [r for r in result["reasons"] if r]
        for reason in reasons:
            reason_counts[reason] += 1

        if "exam_type_ese" in reasons:
            ese.append(_review_entry(raw, reasons))
            continue
        if any(r in REJECTION_REASONS for r in reasons):
            entry = _review_entry(raw, reasons)
            excluded.append(entry)
            if not any(r.startswith("excluded_") for r in reasons):
                unknown.append(entry)
            continue

        if reasons:
            unknown.append(_review_entry(raw, reasons))

        for paper in result["papers"]:
            if paper["exam_type"] not in ALLOWED_EXAM_TYPES:
                continue
            record = {"file": result["file"], "paper": paper, "reasons": reasons}
            records.append(record)
            by_pyq_id[paper["pyq_id"]].append(record)

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
    out_payload = {
        "source": payload.get("source"),
        "retrieved_at": payload.get("retrieved_at"),
        "normalized_at": now,
        "branch": BRANCH,
        "collection": COLLECTION,
        "allowed_exam_types": sorted(ALLOWED_EXAM_TYPES),
        "total_raw_files": len(raw_files),
        "total_papers": len(records),
        "total_files_with_papers": len({r["file"]["drive_file_id"] for r in records}),
        "reason_counts": dict(sorted(reason_counts.items())),
        "records": records,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, indent=2, ensure_ascii=False)

    for path, body in [
        (UNKNOWN_FILE, {"generated_at": now, "count": len(unknown),
                        "excluded": excluded, "needs_review": unknown}),
        (ESE_FILE, {"generated_at": now, "count": len(ese),
                    "note": "Detected and deliberately not ingested in phase 1.",
                    "papers": ese}),
        (COLLISION_FILE, {"generated_at": now, "count": len(collisions),
                          "collisions": collisions}),
    ]:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(body, f, indent=2, ensure_ascii=False)

    print(f"Raw files:        {len(raw_files)}")
    print(f"Papers:           {len(records)}")
    print(f"Files with papers:{out_payload['total_files_with_papers']:>4}")
    print(f"ESE (skipped):    {len(ese)}")
    print(f"Excluded:         {len(excluded)}")
    print(f"Needs review:     {len(unknown)}")
    print(f"Collisions:       {len(collisions)}")
    if reason_counts:
        print("\nReasons:")
        for reason, count in sorted(reason_counts.items()):
            print(f"  {reason:34} {count}")
    print(f"\n-> {os.path.relpath(args.out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

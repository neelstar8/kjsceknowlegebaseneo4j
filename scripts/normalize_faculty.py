"""Stage 2: raw snapshot -> common schema.

Reads data/faculty_directory_raw.json, writes data/faculty_normalized.json.
Purely deterministic -- no network, no LLM.

Usage:
    python -m scripts.normalize_faculty
    python -m scripts.normalize_faculty --in data/faculty_directory_raw_batch10.json \
                                        --out data/faculty_normalized_batch10.json
"""
import argparse
import json
import os
from datetime import date

from normalization.faculty_normalizer import normalize_faculty

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RAW_FILE = os.path.join(DATA_DIR, "faculty_directory_raw.json")
NORM_FILE = os.path.join(DATA_DIR, "faculty_normalized.json")
ERROR_FILE = os.path.join(DATA_DIR, "faculty_errors.json")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="infile", default=RAW_FILE)
    parser.add_argument("--out", dest="outfile", default=NORM_FILE)
    args = parser.parse_args()

    with open(args.infile, encoding="utf-8") as f:
        snapshot = json.load(f)

    last_verified = date.today().isoformat()
    normalized, errors = [], []

    for raw in snapshot["faculty"]:
        try:
            normalized.append(normalize_faculty(raw, last_verified))
        except Exception as e:
            errors.append({
                "source_id": raw.get("source_id"),
                "name": raw.get("name"),
                "profile_url": raw.get("profile_url"),
                "stage": "normalize",
                "error": f"{type(e).__name__}: {e}",
            })

    payload = {
        "source": snapshot.get("source"),
        "retrieved_at": snapshot.get("retrieved_at"),
        "normalized_at": last_verified,
        "total_reported_by_source": snapshot.get("total_reported_by_source"),
        "faculty": normalized,
    }
    with open(args.outfile, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    if errors:
        existing = {"errors": []}
        if os.path.exists(ERROR_FILE):
            with open(ERROR_FILE, encoding="utf-8") as f:
                existing = json.load(f)
        existing.setdefault("errors", []).extend(errors)
        with open(ERROR_FILE, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"Normalized: {len(normalized)}")
    print(f"Failed:     {len(errors)}")
    print(f"-> {os.path.relpath(args.outfile)}")


if __name__ == "__main__":
    main()

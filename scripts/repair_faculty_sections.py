"""Re-fetch and re-parse only the profiles whose sections parsed incompletely.

Cheaper than re-running full discovery: when a parser fix lands, this targets
just the records where a section has visible text but produced zero items, so
the source is hit ~150 times instead of ~613.

Usage:
    python -m scripts.repair_faculty_sections
    python -m scripts.repair_faculty_sections --dry-run
"""
import argparse
import json
import os
import time

from normalization.faculty_normalizer import is_placeholder
from scraper.somaiya_faculty import (
    REQUEST_DELAY,
    FetchError,
    fetch_profile,
    make_session,
    parse_profile,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RAW_FILE = os.path.join(DATA_DIR, "faculty_directory_raw.json")


def needs_repair(record: dict) -> list[str]:
    """Sections with real text but no parsed items -- i.e. a parser miss."""
    sections = (record.get("profile") or {}).get("sections") or {}
    broken = []
    for name, block in sections.items():
        text = (block.get("text") or "").strip()
        if text and not is_placeholder(text) and not block.get("items"):
            broken.append(name)
    return broken


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="infile", default=RAW_FILE)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with open(args.infile, encoding="utf-8") as f:
        snapshot = json.load(f)

    targets = [(r, needs_repair(r)) for r in snapshot["faculty"]]
    targets = [(r, s) for r, s in targets if s]

    print(f"Profiles needing repair: {len(targets)} of {len(snapshot['faculty'])}")
    if args.dry_run or not targets:
        for r, s in targets[:10]:
            print(f"  {r['name']}: {s}")
        return 0

    session = make_session()
    repaired = failed = 0
    for i, (record, broken) in enumerate(targets, 1):
        url = record.get("profile_url")
        try:
            html, used = fetch_profile(session, url, record.get("source_id"))
            record["profile"] = parse_profile(html)
            if used != url:
                record["profile_url_fetched"] = used
            repaired += 1
        except (FetchError, Exception):
            failed += 1
        print(f"  {i}/{len(targets)} repaired={repaired} failed={failed}",
              end="\r", flush=True)
        time.sleep(REQUEST_DELAY)
    print(" " * 60, end="\r")

    with open(args.infile, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)

    still_broken = sum(1 for r in snapshot["faculty"] if needs_repair(r))
    print(f"Repaired: {repaired}")
    print(f"Failed:   {failed}")
    print(f"Still incompletely parsed: {still_broken}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

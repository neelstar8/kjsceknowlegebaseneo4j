"""Stage 1: discover faculty records from the official Somaiya directory.

Writes a raw snapshot to data/faculty_directory_raw.json. Nothing touches
Neo4j here -- the graph must never depend on the scraper running.

Usage:
    python -m scripts.discover_faculty            # whole directory
    python -m scripts.discover_faculty --limit 10 # first 10 records
    python -m scripts.discover_faculty --limit 10 --no-profiles
"""
import argparse
import json
import os
import time
from datetime import datetime, timezone

from scraper.somaiya_faculty import (
    DIRECTORY_URL,
    REQUEST_DELAY,
    FetchError,
    discover_all,
    fetch_profile,
    make_session,
    parse_profile,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RAW_FILE = os.path.join(DATA_DIR, "faculty_directory_raw.json")
ERROR_FILE = os.path.join(DATA_DIR, "faculty_errors.json")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None,
                        help="Only discover the first N faculty records.")
    parser.add_argument("--no-profiles", action="store_true",
                        help="Skip fetching individual profile pages.")
    parser.add_argument("--out", default=RAW_FILE)
    args = parser.parse_args()

    session = make_session()

    print(f"Source: {DIRECTORY_URL}")
    print("Walking the directory listing...")

    def progress(done, total):
        print(f"  listing: {done}/{total}", end="\r", flush=True)

    result = discover_all(session, max_records=args.limit, progress=progress)
    records = result["records"]
    print(" " * 40, end="\r")
    print(f"Faculty records discovered: {len(records)}")
    print(f"Total reported by directory: {result['total_reported']}")
    print(f"Listing pages fetched: {result['pages_fetched']}")

    errors = []
    if not args.no_profiles:
        print(f"\nFetching {len(records)} profile pages "
              f"(~{REQUEST_DELAY}s apart, be patient)...")
        for i, rec in enumerate(records, 1):
            url = rec.get("profile_url")
            if not url:
                errors.append({
                    "source_id": rec.get("source_id"),
                    "name": rec.get("name"),
                    "profile_url": None,
                    "stage": "profile_fetch",
                    "error": "no profile URL on the directory card",
                })
                continue
            try:
                html, used_url = fetch_profile(session, url, rec.get("source_id"))
                rec["profile"] = parse_profile(html)
                if used_url != url:
                    rec["profile_url_fetched"] = used_url
            except FetchError as e:
                # One bad profile must not stop the run.
                errors.append({
                    "source_id": rec.get("source_id"),
                    "name": rec.get("name"),
                    "profile_url": url,
                    "stage": "profile_fetch",
                    "error": str(e),
                })
            except Exception as e:  # parsing blew up on an odd page
                errors.append({
                    "source_id": rec.get("source_id"),
                    "name": rec.get("name"),
                    "profile_url": url,
                    "stage": "profile_parse",
                    "error": f"{type(e).__name__}: {e}",
                })
            print(f"  profiles: {i}/{len(records)}  ok={i - len(errors)} "
                  f"failed={len(errors)}", end="\r", flush=True)
            time.sleep(REQUEST_DELAY)
        print(" " * 60, end="\r")

    snapshot = {
        "source": DIRECTORY_URL,
        "api_endpoint": "https://www.somaiya.edu/arigel_general/faculty_ajax_new/<offset>",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "total_reported_by_source": result["total_reported"],
        "pages_fetched": result["pages_fetched"],
        "profiles_fetched": not args.no_profiles,
        "faculty": records,
    }

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    with open(ERROR_FILE, "w", encoding="utf-8") as f:
        json.dump({"stage": "discovery", "errors": errors}, f, indent=2,
                  ensure_ascii=False)

    with_profiles = sum(1 for r in records if r.get("profile"))
    print(f"\nSuccessful: {with_profiles}")
    print(f"Failed:     {len(errors)}")
    print(f"Skipped:    {len(records) - with_profiles - len(errors)}")
    print(f"Total:      {len(records)}")
    print(f"\nRaw snapshot -> {os.path.relpath(args.out)}")
    if errors:
        print(f"Errors       -> {os.path.relpath(ERROR_FILE)}")


if __name__ == "__main__":
    main()

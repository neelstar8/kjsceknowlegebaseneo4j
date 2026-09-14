"""Stage 1: Google Drive -> data/pyq_drive_raw.json.

A faithful dump of the Drive tree with zero parsing, so every later re-parse is
offline and free. Exactly the role data/faculty_directory_raw.json plays for
the faculty pipeline.

Usage:
    python -m scripts.discover_pyq
    python -m scripts.discover_pyq --limit 20 --out data/pyq_raw20.json
"""
import argparse
import json
import logging
import os
from datetime import datetime, timezone

from drive.client import (
    DRIVE_ROOT_FOLDER_ID,
    close_service,
    get_file,
    service_account_email,
    verify_connection,
    walk_folder,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
RAW_FILE = os.path.join(DATA_DIR, "pyq_drive_raw.json")


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(os.path.join(LOG_DIR, "pyq_discover.log"))],
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default=DRIVE_ROOT_FOLDER_ID)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--out", default=RAW_FILE)
    parser.add_argument("--exclude-folder", action="append", default=[],
                        metavar="FOLDER_ID",
                        help="skip this folder and everything under it; "
                             "repeatable")
    args = parser.parse_args()

    setup_logging()
    log = logging.getLogger("discover_pyq")

    print("Verifying Google Drive connection...")
    verify_connection(args.folder)
    root = get_file(args.folder)
    print(f"Connected as {service_account_email()}")
    print(f"Root folder: {root.get('name')}")

    files = []
    for record in walk_folder(args.folder, root.get("name"),
                              exclude_ids=set(args.exclude_folder)):
        files.append(record)
        log.debug("found %s | %s", record["folder_path"], record["file_name"])
        print(f"  discovered {len(files)} files", end="\r", flush=True)
        if args.limit and len(files) >= args.limit:
            break
    print(" " * 60, end="\r")

    payload = {
        "source": f"https://drive.google.com/drive/folders/{args.folder}",
        "root_folder_id": args.folder,
        "root_folder_name": root.get("name"),
        "excluded_folder_ids": args.exclude_folder,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "total_files": len(files),
        "files": files,
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"Discovered: {len(files)} files")
    print(f"\n-> {os.path.relpath(args.out)}")
    close_service()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

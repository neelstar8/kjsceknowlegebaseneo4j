"""Stage 1: discover and fetch every policy document linked from the handbook.

    https://kjsit.somaiya.edu.in/en/handbook/   ->  data/policy_discovery.json

Zero interpretation happens here, deliberately -- the same reason
scripts/discover_faculty.py and scripts/discover_pyq.py exist as separate
stages. Once the raw manifest exists, every later re-read is free and offline.

The page is fully server-rendered, so the category -> document structure is
read straight out of the DOM (h3 headings, then the li items under them). A
category with no <a> is recorded with status NO_LINK_ON_PAGE rather than
dropped -- "the handbook has no HR Policies link" is itself a finding.

    .venv/bin/python -m scripts.discover_policies
    .venv/bin/python -m scripts.discover_policies --out data/other.json
"""
import argparse
import hashlib
import json
import os
import re
import urllib.parse
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

HANDBOOK_URL = "https://kjsit.somaiya.edu.in/en/handbook/"
PDF_DIR = "data/policy_pdfs"
OUT_PATH = "data/policy_discovery.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/120.0.0.0 Safari/537.36"}
# The site uses these as "no document yet" placeholders in href.
PLACEHOLDER_HREFS = {"---", "#", "", "javascript:void(0)"}


# A scanned page in this corpus still extracts ~22 characters, because the
# running header ("K J S I E I T" + the page number) is real text laid over a
# full-page image. Thresholding on text length alone therefore finds nothing.
# What actually distinguishes these pages is the image: a page-sized raster.
# Getting this right matters -- one annexure here is 15 scanned pages carrying
# the entire PhD sponsorship policy, and a length check silently drops all 15.
FULL_PAGE_PIXELS = 250_000
PAGE_TEXT_FLOOR = 200


def _image_areas(resources, depth=0):
    """Pixel areas of every image on a page, descending into Form XObjects."""
    if depth > 4 or not resources:
        return []
    xobjects = resources.get("/XObject")
    if xobjects is None:
        return []
    areas = []
    for name in xobjects.get_object():
        obj = xobjects.get_object()[name].get_object()
        subtype = obj.get("/Subtype")
        if subtype == "/Image":
            width, height = obj.get("/Width") or 0, obj.get("/Height") or 0
            areas.append(int(width) * int(height))
        elif subtype == "/Form":
            areas.extend(_image_areas(obj.get("/Resources"), depth + 1))
    return areas


def scanned_pages(reader) -> list[int]:
    """1-indexed pages whose content is a page-sized image, not text."""
    found = []
    for number, page in enumerate(reader.pages, 1):
        text = (page.extract_text() or "").strip()
        if len(text) >= PAGE_TEXT_FLOOR:
            continue
        try:
            areas = _image_areas(page.get("/Resources"))
        except Exception:                          # noqa: BLE001 - report, never fail
            areas = []
        if any(area >= FULL_PAGE_PIXELS for area in areas) or not text:
            found.append(number)
    return found


def _now():
    return datetime.now(timezone.utc).isoformat()


def fetch_handbook(url=HANDBOOK_URL) -> str:
    r = requests.get(url, headers=HEADERS, timeout=60)
    r.raise_for_status()
    return r.text


def parse_handbook(html: str) -> dict:
    """Pull the publication line and every category -> document entry."""
    soup = BeautifulSoup(html, "lxml")
    anchor = soup.find("a", href=re.compile(r"Institute\+Handbook"))
    if anchor is None:
        raise RuntimeError("No handbook document links found on the page. "
                           "The page structure has changed.")
    container = anchor
    while container is not None and len(
            container.find_all("a", href=re.compile(r"Institute\+Handbook"))) < 12:
        container = container.parent
    if container is None:
        raise RuntimeError("Could not locate the handbook container element.")

    publications, entries = [], []
    for p in container.find_all("p"):
        text = " ".join(p.get_text(" ", strip=True).split())
        if "Publication" in text or "Last Update" in text:
            a = p.find("a")
            href = a.get("href") if a else None
            publications.append({
                "label": text,
                "url": None if href in PLACEHOLDER_HREFS or href is None else href,
            })

    category = None
    for el in container.descendants:
        name = getattr(el, "name", None)
        if name == "h3":
            category = " ".join(el.get_text(" ", strip=True).split())
        elif name == "li" and category:
            label = " ".join(el.get_text(" ", strip=True).split())
            if not label:
                continue
            a = el.find("a")
            href = a.get("href") if a else None
            entries.append({
                "label": label,
                "category": category,
                "url": None if href in PLACEHOLDER_HREFS or href is None else href,
            })
    return {"publications": publications, "entries": entries}


def fetch_document(entry: dict, pdf_dir: str) -> dict:
    """Download one linked document and record what it actually is.

    Page count comes from the file, never from the link text -- one of these
    PDFs is a five-page extract of a document whose own footer says 54 pages,
    and that only shows up if the file itself is opened.
    """
    record = dict(entry)
    if not entry["url"]:
        record["status"] = "NO_LINK_ON_PAGE"
        return record

    filename = urllib.parse.unquote(entry["url"].rsplit("/", 1)[-1]).replace("+", " ")
    path = os.path.join(pdf_dir, filename)
    try:
        r = requests.get(entry["url"], headers=HEADERS, timeout=120)
        record["http_status"] = r.status_code
        record["content_type"] = r.headers.get("Content-Type")
        if r.status_code != 200 or not r.content.startswith(b"%PDF"):
            record["status"] = "FETCH_FAILED"
            return record
        os.makedirs(pdf_dir, exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(r.content)
        record.update(status="FETCHED", filename=filename, path=path,
                      bytes=len(r.content),
                      sha256=hashlib.sha256(r.content).hexdigest())
        reader = PdfReader(path)
        record["pages"] = len(reader.pages)
        record["scanned_pages"] = scanned_pages(reader)
    except Exception as exc:                       # noqa: BLE001 - reported, never fatal
        record["status"] = "ERROR"
        record["error"] = f"{type(exc).__name__}: {exc}"
    return record


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--url", default=HANDBOOK_URL)
    ap.add_argument("--out", default=OUT_PATH)
    ap.add_argument("--pdf-dir", default=PDF_DIR)
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    started = _now()
    print(f"Fetching {args.url}")
    parsed = parse_handbook(fetch_handbook(args.url))
    entries = parsed["entries"]
    if args.limit:
        entries = entries[:args.limit]
    print(f"  {len(entries)} handbook entries, "
          f"{sum(1 for e in entries if e['url'])} with a link")

    documents = [fetch_document(e, args.pdf_dir) for e in entries]
    for pub in parsed["publications"]:
        if pub["url"]:
            documents.append(fetch_document(
                {"label": pub["label"], "category": "Handbook Publication",
                 "url": pub["url"]}, args.pdf_dir))

    for d in documents:
        flag = f"  scanned={d['scanned_pages']}" if d.get("scanned_pages") else ""
        print(f"  {d['status']:<18} {str(d.get('pages', '-')):>4}p  "
              f"{d.get('filename') or d['label']}{flag}")

    payload = {
        "handbook_url": args.url,
        "run_started": started,
        "run_finished": _now(),
        "publications": parsed["publications"],
        "documents": documents,
        "totals": {
            "entries": len(entries),
            "fetched": sum(1 for d in documents if d["status"] == "FETCHED"),
            "no_link": sum(1 for d in documents if d["status"] == "NO_LINK_ON_PAGE"),
            "failed": sum(1 for d in documents
                          if d["status"] in ("FETCH_FAILED", "ERROR")),
            "pages": sum(d.get("pages", 0) for d in documents),
        },
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print(f"\n{payload['totals']}")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()

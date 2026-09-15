"""Crawl the official KJSCE site into a resumable manifest.

    sitemap.xml + the documents AJAX endpoint  ->  manifest  ->  fetch  ->  extract

Two phases, both re-runnable and both safe to interrupt:

    --discover   seed the manifest from the sitemap and the documents endpoint.
                 ~16 requests. Establishes the fixed 366-page denominator.
    --process    work the queue: fetch each page and harvest its links, download and
                 read each KJ-host document, record every other host as a reference.

`--process` resumes by default: it replays the event log, skips whatever already
reached a terminal state, and retries failures until their cross-run budget is spent.
Interrupting it is safe -- at worst one in-flight request is lost, and the next run
picks it up.

    .venv/bin/python -m scripts.crawl_site --discover
    .venv/bin/python -m scripts.crawl_site --process --limit 50
    .venv/bin/python -m scripts.crawl_site --status
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse as up

from crawl import extract, fetcher
from crawl.manifest import Manifest, Status
from crawl.site_urls import (HostClass, canonical_url, classify_host, filename_of,
                             is_document, resource_id, section_of, unescape)

SITE = "https://kjsce.somaiya.edu"
SITEMAP = f"{SITE}/sitemap.xml"
DOCUMENTS_PAGE = f"{SITE}/en/documents/"
AJAX_ENDPOINT = f"{SITE}/arigel_general/get_document"
INSTITUTE_ID = "16"

PDF_DIR = "data/crawl/pdfs"
REPORT = "data/crawl/crawl_report.json"


# --------------------------------------------------------------------- discover

def seed_from_sitemap(man: Manifest) -> int:
    """Every URL in sitemap.xml. These are the pages; the denominator is fixed here."""
    xml = fetcher.fetch(SITEMAP)["content"].decode("utf-8", "replace")
    # unescape() matters: <loc> holds &amp;, and fetching that verbatim asks the
    # server for a parameter literally named "amp;id".
    locs = [unescape(m) for m in re.findall(r"<loc>(.*?)</loc>", xml, re.S)]
    added = 0
    for raw in locs:
        canon = canonical_url(raw)
        if not canon:
            continue
        rid = resource_id(canon, "page")
        if man.get(rid) is None:
            added += 1
        man.discover(rid, canonical_url=canon, raw_url=raw, kind="page",
                     host_class=classify_host(canon), section=section_of(canon),
                     discovered_via=[{"source": "sitemap"}])
    return added


def ajax_pairs(html: str) -> list[tuple[str, str, str, str]]:
    """The (dept, dept_id, cat, cat_id) tuples the documents page can request."""
    seen, out = set(), []
    for t in re.findall(r"get_document\('([^']*)','([^']*)','([^']*)','([^']*)'\)", html):
        if t not in seen:
            seen.add(t)
            out.append(tuple(unescape(x) for x in t))
    return out


def seed_from_documents(man: Manifest) -> tuple[int, list[dict]]:
    """Replay every documents-page AJAX listing. Empty sections are recorded as facts."""
    html = fetcher.fetch(DOCUMENTS_PAGE)["content"].decode("utf-8", "replace")
    pairs = ajax_pairs(html)
    added, sections = 0, []

    for dept, dept_id, cat, cat_id in pairs:
        body = (f"page_no=0&department_id={dept_id}&category_id={cat_id}"
                f"&institute_id={INSTITUTE_ID}&dept_name={up.quote(dept)}"
                f"&cat_name={up.quote(cat)}&lang=en")
        text = fetcher.post_form(AJAX_ENDPOINT, body, referer=DOCUMENTS_PAGE)
        empty = "No Data Found" in text
        links = extract.html_links(text, DOCUMENTS_PAGE)
        sections.append({"department": dept, "department_id": dept_id,
                         "category": cat or "(section root)", "category_id": cat_id,
                         "items": len(links), "empty": empty})
        for link in links:
            canon = link["canonical_url"]
            kind = "document" if is_document(canon) else "external"
            rid = resource_id(canon, kind)
            if man.get(rid) is None:
                added += 1
            man.discover(rid, canonical_url=canon, raw_url=link["url"], kind=kind,
                         host_class=classify_host(canon),
                         title=link["text"] or filename_of(canon),
                         discovered_via=[{"source": "documents_ajax",
                                          "department": dept,
                                          "category": cat or "(section root)",
                                          "anchor_text": link["text"]}])
    return added, sections


# ---------------------------------------------------------------------- process

def record_link(man: Manifest, link: dict, parent: str) -> int:
    """Add a link found on a page. Returns 1 when it is newly discovered."""
    canon = link["canonical_url"]
    host_class = classify_host(canon)
    if host_class == HostClass.IGNORE:
        return 0

    if host_class == HostClass.SITE and not is_document(canon):
        # A site page not in the sitemap: recorded for audit, never fetched. The
        # sitemap is the page denominator; following these would make it unbounded.
        rid = resource_id(canon, "page")
        if man.get(rid) is None:
            man.discover(rid, canonical_url=canon, kind="page",
                         host_class=host_class, section=section_of(canon),
                         discovered_via=[{"source": "link", "parent": parent}])
            man.update(rid, Status.OUT_OF_SCOPE,
                       reason="same-host page not listed in sitemap.xml")
            return 1
        return 0

    kind = "document" if is_document(canon) else "external"
    rid = resource_id(canon, kind)
    new = man.get(rid) is None
    man.discover(rid, canonical_url=canon, raw_url=link["url"], kind=kind,
                 host_class=host_class,
                 title=link["text"] or filename_of(canon),
                 discovered_via=[{"source": "link", "parent": parent,
                                  "anchor_text": link["text"]}])
    return 1 if new else 0


def process_page(man: Manifest, row: dict) -> dict:
    """Fetch a site page and harvest its links."""
    url = row["canonical_url"]
    result = fetcher.fetch(url)
    html = result["content"].decode("utf-8", "replace")
    links = extract.html_links(html, url)
    found = sum(record_link(man, l, url) for l in links)
    man.update(row["resource_id"], Status.EXTRACTED,
               http_status=result.get("status"), sha256=result["sha256"],
               bytes=result["bytes"], from_cache=result["from_cache"],
               title=extract.page_title(html), links_found=len(links),
               new_resources=found)
    return {"links": len(links), "new": found}


def process_document(man: Manifest, row: dict) -> dict:
    """Download a KJ-host document, checksum it, read it, harvest embedded links."""
    url = row["canonical_url"]
    result = fetcher.fetch(url, is_document=True)
    content = result["content"]

    if not fetcher.looks_like_pdf(content):
        man.update(row["resource_id"], Status.EXTRACTED,
                   http_status=result.get("status"), sha256=result["sha256"],
                   bytes=result["bytes"], content_type=result.get("content_type"),
                   note="not a PDF; recorded as a link only")
        return {"pdf": False}

    os.makedirs(PDF_DIR, exist_ok=True)
    local = os.path.join(PDF_DIR, f"{row['resource_id']}.pdf")
    if not os.path.exists(local):
        with open(local, "wb") as fh:
            fh.write(content)

    from pypdf import PdfReader          # imported lazily: pages never need it
    pages, chars, scanned, embedded = None, 0, [], []
    try:
        reader = PdfReader(local)
        pages = len(reader.pages)
        per_page = []
        for p in reader.pages:
            try:
                t = (p.extract_text() or "").strip()
            except Exception:
                t = ""
            per_page.append(len(t))
        chars = sum(per_page)
        scanned = [i + 1 for i, n in enumerate(per_page) if n < 120]
        embedded = extract.pdf_links(reader, base_url=url)
    except Exception as e:                # a malformed PDF is data, not a crash
        man.update(row["resource_id"], Status.EXTRACTED,
                   sha256=result["sha256"], bytes=result["bytes"],
                   local_path=local, parse_error=str(e)[:300])
        return {"pdf": True, "parse_error": True}

    found = sum(record_link(man, l, url) for l in embedded)
    man.update(row["resource_id"], Status.EXTRACTED,
               http_status=result.get("status"), sha256=result["sha256"],
               bytes=result["bytes"], local_path=local, pages=pages,
               text_chars=chars, scanned_pages=scanned,
               needs_visual_read=bool(scanned and chars == 0),
               embedded_links=len(embedded), new_resources=found)
    return {"pdf": True, "pages": pages, "embedded": len(embedded), "new": found}


def process_one(man: Manifest, row: dict) -> str:
    """Route a single pending resource. Returns the status it reached."""
    rid, url = row["resource_id"], row.get("canonical_url", "")
    host_class = row.get("host_class") or classify_host(url)

    if host_class == HostClass.IGNORE:
        man.update(rid, Status.OUT_OF_SCOPE, reason="ignored host or scheme")
        return Status.OUT_OF_SCOPE

    # The PII gate runs before any fetch: the only way to be sure no student name is
    # stored is to never retrieve the file.
    if row.get("kind") in ("document", "external"):
        verdict, reason = extract.pii_verdict(url, row.get("title", ""))
        if verdict == "pii":
            man.update(rid, Status.SKIPPED_PII, pii_reason=reason)
            return Status.SKIPPED_PII
        if verdict == "review":
            man.update(rid, Status.NEEDS_REVIEW, review_reason=reason)
            return Status.NEEDS_REVIEW

    if host_class == HostClass.REFERENCE:
        man.update(rid, Status.RECORDED,
                   reason="non-KJ host: official link kept, never downloaded")
        return Status.RECORDED

    try:
        if host_class == HostClass.SITE and row.get("kind") == "page":
            process_page(man, row)
        else:
            process_document(man, row)
        return Status.EXTRACTED
    except Exception as e:
        man.fail(rid, e)
        return man.get(rid)["status"]


# ------------------------------------------------------------------------- CLI

def print_status(man: Manifest) -> None:
    cov = man.coverage()
    counts = cov["by_status"]
    print(f"\n  manifest: {len(man.rows)} resources")
    for status, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"    {status:<22} {n}")
    pages = [r for r in man.rows.values() if r.get("kind") == "page"]
    done_pages = [r for r in pages if r.get("status") not in
                  (Status.DISCOVERED, Status.FETCH_FAILED, Status.FETCHING)]
    print(f"\n  page coverage     : {len(done_pages)}/{len(pages)} sitemap+found pages")
    print(f"  resource coverage : {cov['resolved']}/{cov['total_in_scope']} "
          f"= {cov['coverage_pct']}%")
    if cov["outstanding"]:
        print(f"  outstanding       : {len(cov['outstanding'])} (listed in {REPORT})")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--discover", action="store_true",
                    help="seed the manifest from sitemap.xml and the documents endpoint")
    ap.add_argument("--process", action="store_true",
                    help="work the pending queue (resumes automatically)")
    ap.add_argument("--status", action="store_true", help="print progress and exit")
    ap.add_argument("--limit", type=int, default=None, help="process at most N resources")
    ap.add_argument("--kinds", default=None,
                    help="comma-separated kinds to process, e.g. page or document")
    ap.add_argument("--manifest", default=None)
    args = ap.parse_args()

    man = Manifest(args.manifest) if args.manifest else Manifest()
    man.load()
    if getattr(man, "truncated_lines", 0):
        print(f"  note: ignored {man.truncated_lines} truncated event line(s) "
              "from an interrupted run")

    if args.status:
        print_status(man)
        return

    if args.discover:
        print("Seeding from sitemap.xml …")
        n_pages = seed_from_sitemap(man)
        print(f"  pages added: {n_pages}")
        print("Replaying the documents AJAX listings …")
        n_docs, sections = seed_from_documents(man)
        print(f"  document resources added: {n_docs}")
        for s in sections:
            flag = "EMPTY" if s["empty"] else f"{s['items']:>3}"
            print(f"    {flag}  {s['department']} / {s['category']}")
        os.makedirs("data/crawl", exist_ok=True)
        with open("data/crawl/documents_sections.json", "w", encoding="utf-8") as fh:
            json.dump(sections, fh, indent=2, ensure_ascii=False)

    if args.process:
        kinds = set(args.kinds.split(",")) if args.kinds else None
        queue = man.pending(kinds=kinds)
        if args.limit:
            queue = queue[:args.limit]
        print(f"Processing {len(queue)} resource(s)…")
        tally: dict[str, int] = {}
        for i, row in enumerate(queue, 1):
            status = process_one(man, row)
            tally[status] = tally.get(status, 0) + 1
            label = (row.get("title") or row.get("canonical_url", ""))[:54]
            print(f"  [{i:>4}/{len(queue)}] {status:<16} {label}")
        print("\n  " + "  ".join(f"{k}={v}" for k, v in sorted(tally.items())))

    if args.discover or args.process:
        print_status(man)
        os.makedirs("data/crawl", exist_ok=True)
        with open(REPORT, "w", encoding="utf-8") as fh:
            json.dump(man.coverage(), fh, indent=2, ensure_ascii=False)
        print(f"\nWrote {REPORT}")
    fetcher.close_session()


if __name__ == "__main__":
    sys.exit(main())

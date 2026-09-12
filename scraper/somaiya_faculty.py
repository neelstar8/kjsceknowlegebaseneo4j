"""Scraper for the official Somaiya Faculty Directory.

How the directory actually works (verified 2026-09-10 by inspecting the page):

  The page https://www.somaiya.edu/en/contact-us/faculty-directory/ ships an
  empty container (`#facultylist` / `#refined`) and fills it via jQuery. The
  underlying request is:

      POST https://www.somaiya.edu/arigel_general/faculty_ajax_new/<offset>
      body (form-urlencoded):
          page_no=<offset>      # row offset, NOT a page index: 0, 10, 20, ...
          sortBy=               # optional
          keywords=             # free-text search
          gender=
          campus_check=         # comma separated ids
          institute_check=
          sub_institute_check=
          dept_check=
          desig_check=
          lang=en

  The response is an HTML fragment (not JSON) containing 10 `.svvuserdirectory`
  cards plus a pagination block whose `.of_result` div reads "10 of 613",
  which gives the total record count.

  Each card links to a profile at <sub-institute-host>/en/view-member/<id>/ .
  Profile pages are fully server-rendered: an info sidebar plus accordion
  panels whose `.panel-title` is the section name and `.panel-body` the
  content. That makes deterministic parsing possible -- no LLM needed.

Everything here is plain public HTTP against public pages. No auth is used or
bypassed, and requests are rate limited.
"""
import re
import time

import requests
from bs4 import BeautifulSoup

DIRECTORY_URL = "https://www.somaiya.edu/en/contact-us/faculty-directory/"
AJAX_URL = "https://www.somaiya.edu/arigel_general/faculty_ajax_new/"
PAGE_SIZE = 10

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)

# Be a good citizen: one request every REQUEST_DELAY seconds, with backoff.
REQUEST_DELAY = 1.0
TIMEOUT = 30
MAX_RETRIES = 4
BACKOFF_BASE = 2.0


class FetchError(Exception):
    """Raised when a URL could not be retrieved after all retries."""


def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": DIRECTORY_URL,
        }
    )
    return s


def _request(session, method, url, **kwargs):
    """One HTTP request with retries and exponential backoff."""
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = session.request(method, url, timeout=TIMEOUT, **kwargs)
            # 5xx and 429 are worth retrying; other 4xx are not.
            if resp.status_code >= 500 or resp.status_code == 429:
                last_error = f"HTTP {resp.status_code}"
            else:
                resp.raise_for_status()
                return resp
        except requests.RequestException as e:
            last_error = str(e)
        if attempt < MAX_RETRIES - 1:
            time.sleep(BACKOFF_BASE ** attempt)
    raise FetchError(f"{method} {url} failed after {MAX_RETRIES} attempts: {last_error}")


# --------------------------------------------------------------------------
# Directory listing
# --------------------------------------------------------------------------

def fetch_directory_page(session, offset: int, filters: dict | None = None) -> str:
    """Fetch one 10-record slice of the directory. Returns the HTML fragment."""
    data = {
        "page_no": str(offset),
        "sortBy": "",
        "keywords": "",
        "gender": "",
        "campus_check": "",
        "institute_check": "",
        "sub_institute_check": "",
        "dept_check": "",
        "desig_check": "",
        "lang": "en",
    }
    if filters:
        data.update({k: str(v) for k, v in filters.items()})
    resp = _request(
        session,
        "POST",
        AJAX_URL + str(offset),
        data=data,
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    return resp.text


def parse_total_count(html: str) -> int | None:
    """Read the total record count out of the pagination block ("10 of 613")."""
    m = re.search(r"of_result[^>]*>\s*\d+\s+of\s+([\d,]+)", html)
    if not m:
        return None
    return int(m.group(1).replace(",", ""))


def _clean(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def parse_directory_cards(html: str) -> list[dict]:
    """Extract one raw record per faculty card in a directory HTML fragment."""
    soup = BeautifulSoup(html, "lxml")
    records = []

    for card in soup.select("div.svvuserdirectory"):
        link = card.select_one("a.membername[href]") or card.select_one(
            'a[href*="view-member"]'
        )
        profile_url = link["href"].strip() if link else None
        source_id = None
        if profile_url:
            m = re.search(r"view-member/(\d+)", profile_url)
            if m:
                source_id = m.group(1)

        name_el = card.select_one("a.membername p") or card.select_one("a.membername")
        name = _clean(name_el.get_text()) if name_el else ""

        # "<designation> at <institute>" line.
        designation = institute = ""
        role_line = card.select_one("p.greyf14firamd")
        if role_line:
            spans = role_line.select("span.darkf14firamd")
            if len(spans) >= 1:
                designation = _clean(spans[0].get_text())
            if len(spans) >= 2:
                institute = _clean(spans[1].get_text())

        img = card.select_one("div.svvuserdir-img img[src]")
        photo_url = img["src"].strip() if img else None

        member_type_el = card.select_one("div.facultybox")
        member_type = _clean(member_type_el.get_text()) if member_type_el else ""

        email = ""
        mail_link = card.select_one('a[href^="mailto:"]')
        if mail_link:
            email = mail_link["href"].split("mailto:", 1)[1].strip()

        # The remaining <li> items are icon-prefixed free text: campus,
        # timings, office address, phone. Key them by their fa-* icon class.
        icon_fields = {}
        for li in card.select("ul.svvuserdir-lists li"):
            icon = li.select_one("i[class*=fa-]")
            key = None
            if icon:
                for cls in icon.get("class", []):
                    if cls.startswith("fa-"):
                        key = cls[3:]
                        break
            value = _clean(li.get_text())
            if key and value:
                icon_fields.setdefault(key, value)

        records.append(
            {
                "source_id": source_id,
                "name": name,
                "profile_url": profile_url,
                "raw_data": {
                    "name": name,
                    "designation": designation,
                    "institute": institute,
                    "email": email,
                    "photo_url": photo_url,
                    "member_type": member_type,
                    "campus": icon_fields.get("university", ""),
                    "phone": icon_fields.get("phone", ""),
                    "timings": icon_fields.get("clock-o", ""),
                    "office_address": icon_fields.get("map-marker", ""),
                },
            }
        )
    return records


def discover_all(session=None, max_records=None, progress=None) -> dict:
    """Walk the whole directory via the AJAX endpoint.

    Returns {"total_reported": int|None, "records": [...], "pages_fetched": int}.
    """
    session = session or make_session()
    first_html = fetch_directory_page(session, 0)
    total_reported = parse_total_count(first_html)

    records = parse_directory_cards(first_html)
    seen = {r["source_id"] for r in records if r["source_id"]}
    pages = 1

    limit = total_reported if total_reported is not None else 0
    if max_records is not None:
        limit = min(limit, max_records) if limit else max_records

    offset = PAGE_SIZE
    while len(records) < limit:
        time.sleep(REQUEST_DELAY)
        html = fetch_directory_page(session, offset)
        page_records = parse_directory_cards(html)
        pages += 1
        if not page_records:
            break
        new = [
            r for r in page_records
            if not r["source_id"] or r["source_id"] not in seen
        ]
        for r in new:
            if r["source_id"]:
                seen.add(r["source_id"])
        records.extend(new)
        if progress:
            progress(len(records), limit)
        if not new:
            # Endpoint started repeating itself -- stop rather than loop forever.
            break
        offset += PAGE_SIZE

    if max_records is not None:
        records = records[:max_records]

    return {
        "total_reported": total_reported,
        "records": records,
        "pages_fetched": pages,
    }


# --------------------------------------------------------------------------
# Individual profile pages
# --------------------------------------------------------------------------

def canonical_profile_url(source_id: str) -> str:
    return f"https://www.somaiya.edu/en/view-member/{source_id}/"


def fetch_profile(session, url: str, source_id: str | None = None) -> tuple[str, str]:
    """Fetch a profile page, returning (html, url_actually_used).

    Some sub-institute hosts (fll., skssa., ...) return HTTP 500 for profiles
    that the canonical www host serves fine, so fall back to www before
    giving up on a member.
    """
    try:
        return _request(session, "GET", url).text, url
    except FetchError:
        if not source_id:
            raise
        fallback = canonical_profile_url(source_id)
        if fallback.rstrip("/") == url.rstrip("/"):
            raise
        return _request(session, "GET", fallback).text, fallback


# Sidebar list items lead with a label, e.g. "Department:" / "Email Address:".
_SIDEBAR_LABELS = {
    "department": "department",
    "institute": "institute",
    "email address": "email",
    "contact details": "contact_details",
    "office address": "office_address",
    "timings for visitors": "timings",
}


def parse_profile(html: str) -> dict:
    """Deterministically pull the structured blocks off a profile page.

    Returns a dict of raw strings/lists keyed by the site's own section names.
    No interpretation or inference happens here.
    """
    soup = BeautifulSoup(html, "lxml")
    out: dict = {"sections": {}, "sidebar": {}, "links": {}}

    header = soup.select_one("div.viewmemberheader")
    if header:
        h3 = header.select_one("h3")
        h5 = header.select_one("h5")
        out["full_name"] = _clean(h3.get_text()) if h3 else ""
        out["role_line"] = _clean(h5.get_text()) if h5 else ""

    photo = soup.select_one("div.view_profile img[src]")
    if photo:
        out["photo_url"] = photo["src"].strip()

    member_type = soup.select_one("span.view_profile_desgn")
    if member_type:
        out["member_type"] = _clean(member_type.get_text())

    # Sidebar info list.
    for li in soup.select("div.cdfinfo li"):
        text = _clean(li.get_text())
        for label, key in _SIDEBAR_LABELS.items():
            if text.lower().startswith(label):
                out["sidebar"][key] = text[len(label):].lstrip(": ").strip()
                break

    mail = soup.select_one('div.cdfinfo a[href^="mailto:"]')
    if mail:
        out["sidebar"]["email"] = mail["href"].split("mailto:", 1)[1].strip()

    # External / academic profile links in the sidebar, plus the CV link.
    for a in soup.select("div.cdfinfo a[href], div.soc a[href]"):
        href = a["href"].strip()
        label = _clean(a.get_text())
        if not href.startswith("http"):
            continue
        if label:
            out["links"][label] = href

    # Accordion panels: heading -> body.
    for panel in soup.select("div.panel"):
        title_el = panel.select_one(".panel-title a")
        body_el = panel.select_one(".panel-body")
        if not title_el or not body_el:
            continue
        title = _clean(title_el.get_text())
        if not title:
            continue
        # Panels use three different markups for their entries, in this order
        # of specificity: publication rows (Research Papers / Proceedings /
        # Books / Book chapters / IPR), <li> lists, then loose <p> blocks.
        # Research Papers use .viewmemember-researchlist; Proceedings, Books,
        # Book chapters and IPR use .links-re. Both are one entry per div.
        items = [
            _clean(el.get_text())
            for el in body_el.select("div.viewmemember-researchlist, div.links-re")
            if _clean(el.get_text())
        ]
        if not items:
            items = [
                _clean(li.get_text())
                for li in body_el.select("li")
                if _clean(li.get_text())
            ]
        if not items:
            items = [
                _clean(p.get_text())
                for p in body_el.select("p")
                if _clean(p.get_text())
            ]
        out["sections"][title] = {
            "items": items,
            "text": _clean(body_el.get_text()),
        }

    return out

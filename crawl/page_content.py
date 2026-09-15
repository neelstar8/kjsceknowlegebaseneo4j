"""Turning a crawled HTML page into substantive content.

The hard part of this site is not parsing HTML, it is telling content from chrome.
A typical page is ~32,000 characters of text of which only ~12,000 is the thing a
student actually wants; the rest is the menu, the "How Can We Help You?" contact
modal, the footer and the same quick-links rail on every page.

Rather than hardcode selectors that break the moment the theme changes, boilerplate
is detected **statistically**: every page is split into blocks, and any block whose
exact text appears on a large share of pages is chrome by definition. That needs a
corpus pass first, which is why this module separates `blocks_of()` (per page) from
`learn_boilerplate()` (over the corpus) from `content_of()` (per page, filtered).

Nothing here writes to Neo4j and no page text is stored in the graph. The extracted
content feeds entity recognition; the graph keeps facts and provenance, not prose.
"""
from __future__ import annotations

import hashlib
import re
from collections import Counter

from bs4 import BeautifulSoup

# Structural elements that are never content.
DROP_TAGS = ["script", "style", "noscript", "nav", "header", "footer", "svg",
             "iframe", "form", "button", "select", "option"]

# Class/id fragments that mark site furniture on this theme.
DROP_HINTS = re.compile(
    r"(?i)\b(menu|navbar|nav-|breadcrumb|footer|header|cookie|modal|popup|"
    r"social|share|sidebar|quick-?link|back-?to-?top|search|carousel-control|"
    r"skip-link|offcanvas)\b")

#: A block shorter than this is a label or a stray word, not information.
MIN_BLOCK_CHARS = 40

#: A block appearing on more than this share of pages is site furniture.
BOILERPLATE_SHARE = 0.10

HEADING_TAGS = ("h1", "h2", "h3", "h4")


def _clean_soup(html: str) -> BeautifulSoup:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(DROP_TAGS):
        tag.decompose()
    # Collect first, decompose after. Removing a tag mid-iteration detaches its
    # descendants too, and BeautifulSoup leaves those dead nodes in the list with
    # `attrs` set to None -- touching one then raises.
    doomed = []
    for tag in soup.find_all(True):
        attrs = getattr(tag, "attrs", None)
        if not attrs:
            continue
        marker = " ".join(attrs.get("class") or []) + " " + str(attrs.get("id") or "")
        if DROP_HINTS.search(marker):
            doomed.append(tag)
    for tag in doomed:
        if tag.parent is not None:      # may already have gone with an ancestor
            tag.decompose()
    return soup


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def blocks_of(html: str) -> list[dict]:
    """Split a page into blocks, each tagged with the heading it sits under.

    The heading is what makes a fact answerable later: "75%" is noise, but
    "Attendance / 75%" can be retrieved and cited.
    """
    soup = _clean_soup(html)
    out: list[dict] = []
    heading = ""

    body = soup.body or soup
    for el in body.find_all(["h1", "h2", "h3", "h4", "p", "li", "td", "th",
                            "dd", "dt", "blockquote"]):
        text = _norm(el.get_text(" ", strip=True))
        if not text:
            continue
        if el.name in HEADING_TAGS:
            heading = text[:200]
            continue
        if len(text) < MIN_BLOCK_CHARS:
            continue
        out.append({"heading": heading, "text": text[:2000], "tag": el.name})
    return out


def tables_of(html: str) -> list[dict]:
    """Tables, kept as rows. Dates and fee structures on this site live in tables."""
    soup = _clean_soup(html)
    out = []
    for table in soup.find_all("table"):
        rows = []
        for tr in table.find_all("tr"):
            cells = [_norm(td.get_text(" ", strip=True))
                     for td in tr.find_all(["td", "th"])]
            cells = [c for c in cells if c]
            if cells:
                rows.append(cells)
        if len(rows) >= 2:
            caption = ""
            prev = table.find_previous(HEADING_TAGS)
            if prev:
                caption = _norm(prev.get_text(" ", strip=True))[:200]
            out.append({"caption": caption, "rows": rows[:60]})
    return out


def title_of(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    h1 = soup.find("h1")
    if h1:
        t = _norm(h1.get_text(" ", strip=True))
        if t:
            return t[:300]
    if soup.title and soup.title.string:
        return _norm(soup.title.string)[:300]
    return ""


def learn_boilerplate(all_blocks: dict[str, list[dict]],
                      share: float = BOILERPLATE_SHARE) -> set[str]:
    """Blocks repeated across the corpus are furniture, whatever they say.

    `all_blocks` maps page url -> blocks_of(page). Returns the set of normalised
    block texts to drop. This is what removes the contact modal and the quick-links
    rail without naming them.
    """
    pages = len(all_blocks) or 1
    counts = Counter()
    for blocks in all_blocks.values():
        for text in {b["text"] for b in blocks}:     # once per page
            counts[text] += 1
    threshold = max(3, int(pages * share))
    return {text for text, n in counts.items() if n >= threshold}


def content_of(html: str, boilerplate: set[str]) -> dict:
    """The substantive content of one page, with chrome removed."""
    blocks = [b for b in blocks_of(html) if b["text"] not in boilerplate]
    # Within a single page the same sentence often repeats across tabs.
    seen, unique = set(), []
    for b in blocks:
        key = b["text"]
        if key in seen:
            continue
        seen.add(key)
        unique.append(b)

    text = " ".join(b["text"] for b in unique)
    return {
        "title": title_of(html),
        "blocks": unique,
        "tables": tables_of(html),
        "headings": [h for h in dict.fromkeys(
            b["heading"] for b in unique if b["heading"])][:40],
        "content_chars": len(text),
        "content_fingerprint": hashlib.sha1(text.encode("utf-8")).hexdigest()[:16],
    }

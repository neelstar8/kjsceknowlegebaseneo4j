"""Pulling links and signals out of fetched content.

Three jobs:

  html_links()   every anchor on a page, resolved and canonicalised
  pdf_links()    the URLs embedded in a PDF's /Annots link annotations. This is how
                 the Syllabus, Class Time Table and Roll Call "documents" turn out to
                 be link hubs -- 41 per-branch Drive folders that exist nowhere in the
                 page HTML. Nothing in the repo could read these before.
  pii_verdict()  refuse student lists before they are ever downloaded

The PII gate deliberately runs on the URL and anchor text, i.e. *before* any fetch.
The only way to guarantee no student name is stored is to never retrieve the file.
Ambiguous matches are held for review rather than guessed either way.
"""
from __future__ import annotations

import re

from bs4 import BeautifulSoup

from crawl.site_urls import canonical_url, filename_of

# --------------------------------------------------------------- PII detection

# A document naming individual students. "Provisionally Admitted Students List
# July 2026 COMP" and "Provisionally Selected Phd candidates IT" are both real
# examples found on this site.
PII_STRONG = re.compile(
    r"(?i)\b(?:provisionally\s+)?(?:admitted|selected|shortlist(?:ed)?|merit|allotment|"
    r"waiting)\b[^/]{0,40}\b(?:list|students?|candidates?)\b"
    r"|\b(?:list|lists)\s+of\s+(?:admitted|selected|provisional|applicants?)"
    r"|\bstudents?\s+list\b"             # "24-25 Students List" names individuals
    r"|\broll\s*no\b"                    # a roll number is itself individual data
    r"|\bseat\s*(?:no|allotment)\b"
)

# Words that often appear on legitimate administrative documents ("Selection
# Committee", "Merit-cum-Means Scholarship"), so a hit here alone is not enough.
#
# "roll call" sits here rather than in PII_STRONG on purpose. The site's own
# "Roll Call List" is an index of per-branch Drive folders carrying no student data
# at all -- the graph already holds it with contains_personal_data = false -- and
# treating it as certain PII skipped a document we had previously verified as safe.
# The actual per-branch roll calls live inside those Drive folders, which this crawl
# never opens. So a roll-call title earns a human glance, not an automatic refusal.
PII_WEAK = re.compile(
    r"(?i)\b(admitted|selected|selection|merit|candidates?|shortlist|roll\s*call)\b")

PII_EXEMPT = re.compile(
    r"(?i)\b(committee|policy|procedure|criteria|process|guideline|scheme|"
    r"brochure|prospectus|notice|circular|calendar|syllabus|curriculum)\b"
)


def pii_verdict(url: str, anchor_text: str = "") -> tuple[str, str]:
    """Return (verdict, reason) where verdict is 'clear' | 'pii' | 'review'.

    Separators are flattened to spaces first. `_` is a word character, so in a name
    like `KJSCE_Roll Call.pdf` a `\\broll` anchor silently fails to match -- and these
    filenames are full of underscores, so that miss would be the common case rather
    than the edge case.
    """
    raw = f"{filename_of(url)} {anchor_text or ''}"
    haystack = re.sub(r"[_\-+.]+", " ", raw)
    if PII_STRONG.search(haystack):
        return "pii", f"names individual students: {haystack.strip()[:120]}"
    if PII_WEAK.search(haystack) and not PII_EXEMPT.search(haystack):
        return "review", f"ambiguous student-list wording: {haystack.strip()[:120]}"
    return "clear", ""


# ------------------------------------------------------------------ HTML links

SKIP_HREF = re.compile(r"(?i)^\s*(#|javascript:|mailto:|tel:|data:)")


def html_links(html: str, base_url: str) -> list[dict]:
    """Every anchor on a page as {url, canonical_url, text}, deduped by canonical URL."""
    soup = BeautifulSoup(html, "lxml")
    out: dict[str, dict] = {}
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or SKIP_HREF.match(href):
            continue
        canon = canonical_url(href, base=base_url)
        if not canon:
            continue
        text = re.sub(r"\s+", " ", a.get_text(" ", strip=True))[:300]
        if canon in out:
            # Keep the most descriptive anchor text we have seen for this target.
            if len(text) > len(out[canon]["text"]):
                out[canon]["text"] = text
        else:
            out[canon] = {"url": href, "canonical_url": canon, "text": text}
    return list(out.values())


def page_title(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    if soup.title and soup.title.string:
        return re.sub(r"\s+", " ", soup.title.string).strip()[:300]
    h1 = soup.find("h1")
    return re.sub(r"\s+", " ", h1.get_text(" ", strip=True))[:300] if h1 else ""


# ------------------------------------------------------- PDF link annotations

def pdf_links(reader, base_url: str | None = None) -> list[dict]:
    """URLs embedded as /Annots link annotations, with the anchor text under each.

    The rectangle of each annotation is intersected with the page's text positions,
    so a link can be reported together with the branch name it sits on rather than
    as a bare URL. Failures are per-page and non-fatal: a malformed annotation must
    not cost us the rest of the document.
    """
    out: list[dict] = []
    for pno, page in enumerate(reader.pages, start=1):
        try:
            annots = page.get("/Annots") or []
        except Exception:
            continue
        # Text chunks with positions, so an annotation rect can be labelled.
        chunks: list[dict] = []
        try:
            def _visit(text, cm, tm, font, size):
                if text and text.strip():
                    chunks.append({"t": text, "x": tm[4], "y": tm[5]})
            page.extract_text(visitor_text=_visit)
        except Exception:
            chunks = []

        for annot in annots:
            try:
                obj = annot.get_object()
                action = obj.get("/A")
                if not action:
                    continue
                uri = action.get_object().get("/URI")
                if not uri:
                    continue
                rect = [float(v) for v in (obj.get("/Rect") or [0, 0, 0, 0])]
            except Exception:
                continue

            x0, x1 = min(rect[0], rect[2]), max(rect[0], rect[2])
            y0, y1 = min(rect[1], rect[3]), max(rect[1], rect[3])
            inside = [c for c in chunks
                      if y0 - 3 <= c["y"] <= y1 + 1 and x0 - 3 <= c["x"] <= x1 + 3]
            label = re.sub(r"\s+", " ", "".join(
                c["t"] for c in sorted(inside, key=lambda z: (-z["y"], z["x"])))).strip()

            canon = canonical_url(str(uri), base=base_url)
            if canon:
                out.append({"page": pno, "url": str(uri),
                            "canonical_url": canon, "text": label[:200]})
    return out

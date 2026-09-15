"""Turning extracted page content into facts worth putting in the graph.

The instruction that shapes this module is "the goal is not to store the page text".
So nothing here keeps prose for its own sake. It keeps:

  * the page's own headings, which are the site's summary of itself
  * tables, which is where this site puts dates, fees and eligibility
  * short fact sentences -- the ones carrying a number, a date, a deadline or a
    requirement, since those are what a student actually asks about
  * academic years mentioned, so a 2024-25 page can never answer as 2026-27

Descriptive marketing prose is deliberately dropped. A sentence saying the college
has "a vibrant campus culture" is not a fact anyone can retrieve usefully, and
storing it only dilutes the evidence handed to the model.
"""
from __future__ import annotations

import re

# A sentence is a candidate fact when it carries something checkable.
NUMBERY = re.compile(
    r"(\b\d{1,3}\s?%|\b\d{1,2}(st|nd|rd|th)?\s+\w+\s+20\d{2}\b|\b20\d{2}\s*[-/]\s*\d{2}\b"
    r"|\bRs\.?\s?[\d,]+|\b₹\s?[\d,]+|\b\d+\s+(credits?|hours?|marks?|seats?|years?|"
    r"semesters?|weeks?|months?|days?)\b|\b\d{1,2}:\d{2}\b)")

REQUIREMENT = re.compile(
    r"(?i)\b(must|shall|required|requirement|mandatory|eligib|minimum|maximum|"
    r"not less than|at least|compulsory|prerequisite|deadline|last date|"
    r"apply before|should have|criteria)\b")

# Marketing language that adds nothing retrievable.
FLUFF = re.compile(
    r"(?i)\b(vibrant|world[- ]class|state[- ]of[- ]the[- ]art|nurtur|holistic|"
    r"delighted|proud|passion|journey|dream|excellence in all|welcome to)\b")

ACADEMIC_YEAR = re.compile(r"\b(20\d{2})\s*[-–/]\s*(20)?(\d{2})\b")
YEAR = re.compile(r"\b(20\d{2})\b")

MAX_FACTS = 40
MAX_FACT_CHARS = 400


def academic_years(text: str) -> list[str]:
    """Every academic year the page names, normalised to 2026-27 form.

    Kept so a page about 2024-25 is never allowed to answer a 2026-27 question --
    the single most damaging mistake this corpus could make.

    The consecutiveness check is not cosmetic. Without it, two unrelated numbers
    sitting next to each other in a fee table produce phantom years: the M.Tech
    admission page yielded "2026-24" and "2026-25" on the first pass. A phantom year
    is worse than a missing one, because it makes a page look authoritative for a
    year it never mentions.
    """
    out = []
    for m in ACADEMIC_YEAR.finditer(text or ""):
        start = int(m.group(1))
        end_short = int(m.group(3))
        expected = (start + 1) % 100
        if end_short == expected:
            out.append(f"{start}-{end_short:02d}")
    return sorted(set(out))


def years_mentioned(text: str) -> list[int]:
    return sorted({int(y) for y in YEAR.findall(text or "")})


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text or "") if s.strip()]


def key_facts(blocks: list[dict]) -> list[dict]:
    """Fact-bearing sentences, each kept with the heading it appeared under."""
    out: list[dict] = []
    seen: set[str] = set()
    for b in blocks:
        for s in _sentences(b["text"]):
            if len(s) < 25 or len(s) > MAX_FACT_CHARS:
                continue
            if FLUFF.search(s):
                continue
            if not (NUMBERY.search(s) or REQUIREMENT.search(s)):
                continue
            key = re.sub(r"\s+", " ", s.lower())[:160]
            if key in seen:
                continue
            seen.add(key)
            out.append({"heading": b.get("heading", "")[:160], "fact": s})
            if len(out) >= MAX_FACTS:
                return out
    return out


def flatten_facts(facts: list[dict]) -> dict:
    """Parallel arrays, the shape the rest of this graph uses for list data."""
    if not facts:
        return {"fact_count": 0}
    return {
        "fact_headings": [f["heading"] for f in facts],
        "fact_texts": [f["fact"] for f in facts],
        "facts_text": " | ".join(f"{f['heading']}: {f['fact']}" if f["heading"]
                                 else f["fact"] for f in facts),
        "fact_count": len(facts),
    }


def flatten_tables(tables: list[dict], limit: int = 6) -> dict:
    """Tables as one searchable line each. This site puts admission rounds, fee
    structures and important dates in tables, so losing them loses the answer."""
    if not tables:
        return {"table_count": 0}
    caps, texts = [], []
    for t in tables[:limit]:
        caps.append((t.get("caption") or "")[:160])
        rows = [" | ".join(r) for r in t.get("rows", [])[:25]]
        texts.append(" ;; ".join(rows)[:4000])
    return {"table_captions": caps, "table_rows_text": texts,
            "table_count": len(tables)}


def summarise(content: dict) -> str:
    """The page's own opening statement of what it is, for display."""
    for b in content.get("blocks", []):
        t = b["text"]
        if len(t) >= 80 and not FLUFF.search(t):
            return t[:600]
    for b in content.get("blocks", []):
        if len(b["text"]) >= 40:
            return b["text"][:600]
    return ""


def is_substantive(content: dict, facts: list[dict]) -> tuple[bool, str]:
    """Whether this page carries knowledge worth a node.

    A page of pure navigation, or one that is only an index of links already in the
    graph, gets recorded in the manifest rather than created as a node.
    """
    title = (content.get("title") or "").upper()
    if "404" in title or "NOT FOUND" in title:
        return False, "soft 404: page returns an error body"
    if content.get("content_chars", 0) < 200:
        return False, "no substantive content after removing navigation"
    if not facts and not content.get("tables") and len(content.get("headings", [])) < 2:
        return False, "descriptive prose only: no facts, tables or structure"
    return True, ""

"""Question -> Neo4j -> knowledge extracted from official KJSCE webpages.

Deterministic. No model call here; the caller may pass the result to a single
Ollama call for phrasing, which keeps the pipeline at one LLM call end to end.

Two things this service exists to get right.

**Relevance.** A Lucene OR query will answer anything plausibly -- searching
"attendance requirement" over page text returns Honours programme pages, because
they contain the word "requirement". So every hit must clear a term-coverage floor,
the same guard services/policy_service.py uses: a hit needs two matched terms with
at least one distinctive, or one distinctive term that the page is actually about.

**Years.** A page naming 2024-25 must never answer a 2026-27 question. When the
student names a year it is filtered on exactly; when they name a bare year like
"2026" it is resolved against the years the graph actually holds, and if that is
ambiguous the available years are returned rather than one being picked silently.
"""
from __future__ import annotations

import re

from graph import page_queries as pq

DOCUMENTS_PAGE = "https://kjsce.somaiya.edu/en/documents/"

# Words so common in this corpus that matching one proves nothing.
WEAK = {"the", "and", "for", "what", "where", "how", "which", "when", "who",
        "is", "are", "do", "does", "can", "i", "my", "me", "a", "an", "of", "in",
        "on", "to", "at", "requirement", "requirements", "information", "detail",
        "details", "page", "about", "need", "needs", "kjsce", "kjsse", "kjsit",
        "college", "engineering", "somaiya", "student", "students", "show", "find",
        "give", "tell", "please", "there", "any", "all", "get",
        # "year" is in almost every title on this site ("Principal for the Year
        # 2019", "First Year", "Academic Year"), so matching it proves nothing and
        # it was pulling an award citation into a lateral-entry admission query.
        # The level abbreviations are restored by SYNONYMS, so no signal is lost.
        "year", "years", "programme", "program", "course", "courses"}

MIN_COVERAGE = 2

# Student phrasing -> the vocabulary the site actually uses. Expanding the query
# rather than the stored text keeps the graph honest: the page still says what it
# says, we just search for more of the ways a student might ask.
SYNONYMS = {
    r"\bfy\b|\bfirst year\b|\b1st year\b": "FY first year",
    r"\bsy\b|\bsecond year\b|\b2nd year\b": "SY second year",
    r"\bty\b|\bthird year\b|\b3rd year\b": "TY third year",
    r"\bly\b|\blast year\b|\bfinal year\b": "LY final year",
    r"\bbtech\b|\bb\.?\s?tech\b": "B.Tech Bachelor Technology",
    r"\bmtech\b|\bm\.?\s?tech\b": "M.Tech Master Technology",
    r"\bfees?\b|\bcost\b|\bprice\b": "fees fee structure",
    r"\beligib\w*": "eligibility eligible criteria",
    r"\bplacement\w*|\bjob\w*|\brecruit\w*": "placement recruiters",
    r"\bsyllabus\b|\bcurriculum\b|\bcourses?\b": "curriculum syllabus",
    r"\bhostel\b|\baccommodation\b": "hostel accommodation",
    r"\bscholarship\w*|\bfinancial aid\b": "scholarship",
    r"\bdsy\b|\bdirect second year\b|\blateral\b": "direct second year lateral",
}

ACADEMIC_YEAR_RE = re.compile(r"\b(20\d{2})\s*[-–/]\s*(20)?(\d{2})\b")
BARE_YEAR_RE = re.compile(r"\b(20\d{2})\b")


def md_link(text: str, url: str) -> str:
    return f"[{text}](<{url}>)" if any(c in url for c in "() <>") else f"[{text}]({url})"


def expand(question: str) -> str:
    """Add the site's own vocabulary to the student's wording."""
    text = (question or "").lower()
    extra = [rep for pat, rep in SYNONYMS.items() if re.search(pat, text)]
    return " ".join([question or ""] + extra)


def terms_of(question: str) -> list[str]:
    """Scoring terms, taken from the EXPANDED question.

    Scoring the raw wording while searching the expanded one is inconsistent and
    silently loses abbreviations: "DSY admission" searched for "direct second year"
    but then scored only on "dsy", which appears nowhere in a page titled "Direct
    Second Year", so the right page could never rank first.
    """
    words = re.findall(r"[A-Za-z][A-Za-z0-9.&-]{2,}", expand(question).lower())
    return [w for w in dict.fromkeys(words) if w not in WEAK]


def resolve_year(question: str) -> tuple[str | None, list[str], str]:
    """Return (exact_year, candidates, note).

    An exact "2026-27" filters directly. A bare "2026" is matched against the years
    the graph holds: one hit is used, several are reported rather than guessed.
    """
    m = ACADEMIC_YEAR_RE.search(question or "")
    if m:
        start, end = int(m.group(1)), int(m.group(3))
        if end == (start + 1) % 100:
            return f"{start}-{end:02d}", [], ""

    held = [r["academic_year"] for r in pq.years_held()]
    bare = BARE_YEAR_RE.findall(question or "")
    if not bare:
        return None, [], ""
    year = bare[0]
    hits = [y for y in held if y.startswith(year) or y.endswith(year[-2:])]
    if len(hits) == 1:
        return hits[0], [], f"read '{year}' as the academic year {hits[0]}"
    if len(hits) > 1:
        return None, hits, (f"'{year}' could mean {', '.join(hits)} — "
                            "showing what is held rather than guessing")
    return None, [], ""


def _relevant(rows: list[dict], terms: list[str]) -> list[dict]:
    """Drop hits that share too little with the question to be an answer."""
    if not terms:
        return rows
    kept = []
    for row in rows:
        hay = " ".join(filter(None, [
            row.get("title") or "", " ".join(row.get("headings") or []),
            " ".join(row.get("fact_texts") or [])[:4000],
            row.get("summary") or "", row.get("page_section") or ""])).lower()
        title_hay = ((row.get("title") or "") + " " +
                     " ".join(row.get("headings") or [])).lower()
        matched = {t for t in terms if re.search(r"\b" + re.escape(t[:6]), hay)}
        on_topic = any(re.search(r"\b" + re.escape(t[:6]), title_hay) for t in matched)
        if len(matched) >= min(MIN_COVERAGE, len(terms)) or on_topic:
            row["_matched"] = len(matched)
            row["_on_topic"] = on_topic
            kept.append(row)
    kept.sort(key=lambda r: (r["_on_topic"], r["_matched"], r.get("score") or 0),
              reverse=True)
    return kept


def retrieve(question: str, *, limit: int = 6) -> dict:
    year, candidates, note = resolve_year(question)
    rows = pq.search(expand(question), academic_year=year, limit=30)
    rows = _relevant(rows, terms_of(question))[:limit]
    return {"question": question, "academic_year": year,
            "year_candidates": candidates, "year_note": note, "pages": rows}


def build_answer(result: dict) -> str:
    pages = result["pages"]
    out = []
    if result["year_note"]:
        out.append(f"*{result['year_note']}*\n")
    if not pages:
        if result["year_candidates"]:
            out.append("Academic years held: " + ", ".join(result["year_candidates"]))
        else:
            out.append("Nothing on the official KJSCE pages I hold answers that.")
        return "\n".join(out)

    out.append(f"**{len(pages)} official page(s):**\n")
    for p in pages:
        out.append("- " + md_link(p["title"], p["source_url"]))
        meta = []
        if p.get("academic_years"):
            meta.append("Academic year " + ", ".join(p["academic_years"]))
        if p.get("page_section"):
            meta.append(p["page_section"])
        if meta:
            out.append(f"  {' · '.join(meta)}")
        for f in pq.facts_of(p, limit=4):
            head = f"{f['heading']}: " if f["heading"] else ""
            out.append(f"    - {head}{f['fact']}")
    out.append("\nSource: " + md_link("KJSCE official site", DOCUMENTS_PAGE))
    return "\n".join(out)


def answer_page_question(question: str, debug: bool = False) -> dict:
    result = retrieve(question)
    payload = {
        "answer": build_answer(result),
        "pages": [{"doc_id": p["doc_id"], "title": p["title"],
                   "url": p["source_url"], "academic_years": p.get("academic_years"),
                   "section": p.get("page_section")} for p in result["pages"]],
        "found": bool(result["pages"]),
    }
    if debug:
        payload["debug"] = {"academic_year": result["academic_year"],
                            "year_candidates": result["year_candidates"],
                            "expanded": expand(question),
                            "terms": terms_of(question)}
    return payload

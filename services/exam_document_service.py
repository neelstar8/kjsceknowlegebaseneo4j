"""Question -> Neo4j -> official Examination documents, with clickable links.

Deterministic end to end, for the same reason services/pyq_service.py is: the
answer to "show me the examination calendars" *is* a list of official documents
retrieval already found. Sending it through the model adds latency and can only
mangle a URL. No Ollama call is made from this module.

Every URL is rendered as a Markdown link at the point the answer is built, so
the existing KJ GPT link-handling rule holds whether or not a model ever sees it.

Scope: only nodes with source_type='examination_calendar'. This never reaches
attendance, internship, faculty, admission or placement knowledge, and it is not
the PYQ question-paper path -- these are calendars and schedules, not papers.
"""
import re

from graph import exam_queries as q

# The Examination > Examination Download Forms section of the official documents
# page publishes nothing: the endpoint returns the literal body "No Data Found.".
# A student who asks for it deserves that answer rather than a nearest guess.
DOWNLOAD_FORMS_FINDING = (
    "The official documents page has an **Examination Download Forms** section, but it "
    "currently publishes no documents at all - the college's own page returns "
    "\"No Data Found.\" for it. The Examination section's published documents are the "
    "academic and examination calendars listed below."
)

DOCUMENTS_PAGE = "https://kjsce.somaiya.edu/en/documents/"


def md_link(text: str, url: str) -> str:
    """A Markdown link whose destination survives a real renderer.

    Three of the official examination URLs contain literal parentheses, e.g.
    .../AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf. Written the plain way,
    a CommonMark parser ends the destination at the first unescaped ')', so the
    link silently resolves to ".../AEC_SY_TY_LY_(B.Tech" and 404s. Wrapping the
    destination in angle brackets is the CommonMark-sanctioned fix and keeps the
    URL byte-identical to what Neo4j holds.
    """
    needs_wrap = any(c in url for c in "() <>")
    return f"[{text}](<{url}>)" if needs_wrap else f"[{text}]({url})"

_LEVELS = [("FY", [r"\bfy\b", r"\bfirst year\b", r"\b1st year\b"]),
           ("SY", [r"\bsy\b", r"\bsecond year\b", r"\b2nd year\b"]),
           ("TY", [r"\bty\b", r"\bthird year\b", r"\b3rd year\b"]),
           ("LY", [r"\bly\b", r"\blast year\b", r"\bfinal year\b", r"\b4th year\b"])]

_PROGRAMMES = [("B.Tech", [r"\bb[\s.\-]?tech\b", r"\bbtech\b", r"\bundergraduate\b", r"\bug\b"]),
               ("M.Tech", [r"\bm[\s.\-]?tech\b", r"\bmtech\b", r"\bpostgraduate\b", r"\bpg\b"])]

# "download forms" must be checked before the generic document intent, or the
# word "forms" alone would just list calendars and quietly answer the wrong thing.
_FORMS_PATTERNS = [r"download form", r"examination form", r"exam form", r"\bforms?\b"]


def extract_filters(question: str) -> dict:
    text = re.sub(r"\s+", " ", (question or "").lower()).strip()

    year = None
    # 2026-27, 2026-2027, 2026/27 -- normalised to the stored "2026-27" form.
    m = re.search(r"\b(20\d{2})\s*[-/–]\s*(20)?(\d{2})\b", text)
    if m:
        year = f"{m.group(1)}-{m.group(3)}"
    else:
        m = re.search(r"\b(20\d{2})\b", text)
        if m:
            year = None if m.group(1) else None
            # A bare year could mean either half of an academic year; resolved
            # against what the graph actually holds, in retrieve().
            year = f"__bare__{m.group(1)}"

    programme = next((p for p, pats in _PROGRAMMES
                      if any(re.search(x, text) for x in pats)), None)
    level = next((l for l, pats in _LEVELS
                  if any(re.search(x, text) for x in pats)), None)
    wants_forms = any(re.search(p, text) for p in _FORMS_PATTERNS)
    wants_dates = bool(re.search(r"\bdate|when|schedule|timetable|ese\b|ise\b|mse\b|exam period", text))

    return {"academic_year": year, "programme": programme, "level": level,
            "wants_forms": wants_forms, "wants_dates": wants_dates}


def _resolve_year(year: str | None) -> str | None:
    """Turn a bare '2026' into the academic year the graph actually stores."""
    if not year or not year.startswith("__bare__"):
        return year
    bare = year.removeprefix("__bare__")
    held = [r["academic_year"] for r in q.academic_years()]
    matches = [y for y in held if y.startswith(bare) or y.endswith(bare[-2:])]
    return matches[0] if len(matches) == 1 else None


def retrieve(question: str) -> dict:
    f = extract_filters(question)
    academic_year = _resolve_year(f["academic_year"])
    rows = q.find_documents(academic_year=academic_year,
                            programme=f["programme"], level=f["level"])
    return {"filters": {**f, "academic_year": academic_year}, "documents": rows}


def _describe(f: dict) -> str:
    bits = [b for b in (f.get("academic_year"), f.get("programme"), f.get("level")) if b]
    return f" for {', '.join(bits)}" if bits else ""


def build_answer(result: dict) -> str:
    """Markdown, with every official URL as a clickable link."""
    f, docs = result["filters"], result["documents"]
    lines = []

    if f["wants_forms"]:
        lines += [DOWNLOAD_FORMS_FINDING, ""]

    if not docs:
        lines.append(
            f"I don't hold an examination document{_describe(f)} in the KJ GPT knowledge base."
            if not f["wants_forms"] else "")
        held = q.academic_years()
        if held:
            years = ", ".join(f"{r['academic_year']} ({r['documents']})" for r in held)
            lines.append(f"\nExamination documents I do hold, by academic year: {years}.")
        return "\n".join(x for x in lines if x is not None).strip()

    lines.append(f"**{len(docs)} official examination document(s)"
                 f"{_describe(f)}:**\n")
    for d in docs:
        lines.append("- " + md_link(d["title"], d["source_url"]))
        meta = []
        if d.get("academic_year"):
            meta.append(f"Academic year {d['academic_year']}")
        if d.get("level_note"):
            meta.append(d["level_note"])
        if d.get("document_status") in ("proposed", "tentative", "revised"):
            meta.append(f"marked {d['document_status']}")
        if meta:
            lines.append(f"  {' · '.join(meta)}")

        if f["wants_dates"]:
            for ev in q.events_of(d):
                lines.append(f"    - {ev['term']} — {ev['event']}: {ev['schedule']}")
    lines.append("\nSource: " + md_link("KJSCE official documents page", DOCUMENTS_PAGE)
                 + " (Examination section).")
    return "\n".join(lines).strip()


def answer_exam_document_question(question: str, debug: bool = False) -> dict:
    result = retrieve(question)
    payload = {
        "answer": build_answer(result),
        "documents": [
            {"doc_id": d["doc_id"], "title": d["title"], "url": d["source_url"],
             "academic_year": d["academic_year"], "programmes": d["programmes"],
             "levels": d["levels"], "document_status": d["document_status"],
             "events": q.events_of(d) if result["filters"]["wants_dates"] else []}
            for d in result["documents"]
        ],
        "found": bool(result["documents"]),
    }
    if debug:
        payload["debug"] = {"filters": result["filters"],
                            "doc_ids": [d["doc_id"] for d in result["documents"]]}
    return payload

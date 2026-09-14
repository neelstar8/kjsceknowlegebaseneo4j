"""Question -> Neo4j -> official Academics resources, with clickable links.

Deterministic retrieval, exactly like services/exam_document_service.py: no model
call is made here. The caller may pass the returned text to Qwen for a single
final answer-generation call, which is the one Ollama call in the pipeline.

Precision is the point. The question is classified into one or more resource
intents (calendar / timetable / syllabus / roll call / strategic plan /
development plan / software); only those `source_type`s are queried. A question
about the syllabus therefore cannot return calendars, and a question about the
strategic plan cannot return every academic PDF. Multi-intent questions ("show
me the 2026-27 calendar and where the syllabus is") return evidence for each
intent, separately headed.

Every URL is rendered as a Markdown link at build time, so the existing KJ GPT
link rule holds whether or not a model ever sees the text.
"""
import re

from graph import academics_queries as q

DOCUMENTS_PAGE = "https://kjsce.somaiya.edu/en/documents/"


def md_link(text: str, url: str) -> str:
    """Markdown link whose destination survives a real renderer.

    Several official URLs contain literal parentheses, e.g.
    .../AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026-27.pdf. Written plainly, a
    CommonMark parser ends the destination at the first unescaped ')' and the
    link 404s. Angle brackets are the sanctioned fix and keep the URL byte-exact.
    """
    return f"[{text}](<{url}>)" if any(c in url for c in "() <>") else f"[{text}]({url})"


# Intent -> the source_types it may retrieve. Order matters only for display.
INTENTS = [
    ("strategic_plan", [q.STRATEGIC],
     [r"strategic plan", r"2025[\s\-–]*2030", r"\bstrategy\b", r"strategic goal"]),
    ("development_plan", [q.PLAN],
     [r"8\s*point", r"eight\s*point", r"development plan"]),
    ("software", [q.SOFTWARE],
     [r"\bmatlab\b", r"\bsoftware\b", r"download softwares?"]),
    ("syllabus", [q.INDEXES["syllabus"]],
     [r"\bsyllabus\b", r"\bsyllabi\b", r"\bcurriculum\b", r"course content"]),
    ("timetable", [q.INDEXES["timetable"]],
     [r"time\s*table", r"timetable", r"class schedule", r"lecture schedule"]),
    ("roll_call", [q.INDEXES["roll_call"]],
     [r"roll\s*call", r"roll\s*list", r"attendance sheet"]),
    ("calendar", [q.CALENDAR],
     [r"\bcalendars?\b", r"\baec\b", r"academic year", r"\bterms?\b", r"\bsemesters?\b",
      r"\bese\b", r"\bmse\b", r"\bise\b", r"exam date", r"\bholiday", r"\bvacation",
      r"\bresults?\b", r"\binternships?\b", r"convocation"]),
]

_PROGRAMMES = [("M.Tech", [r"\bm[\s.\-]?tech\b", r"\bmtech\b", r"\bpg\b", r"postgraduate"]),
               ("B.Tech", [r"\bb[\s.\-]?tech\b", r"\bbtech\b", r"\bug\b", r"undergraduate"])]
_LEVELS = [("FY", [r"\bfy\b", r"first year", r"1st year", r"f\.?\s?y\.?\s?b"]),
           ("SY", [r"\bsy\b", r"second year", r"2nd year"]),
           ("TY", [r"\bty\b", r"third year", r"3rd year"]),
           ("LY", [r"\bly\b", r"last year", r"final year", r"4th year"])]


def classify(question: str) -> dict:
    text = re.sub(r"\s+", " ", (question or "").lower()).strip()

    intents = [name for name, _types, pats in INTENTS
               if any(re.search(p, text) for p in pats)]
    # "academic documents" with no other signal = show everything we hold.
    broad = bool(re.search(r"academic (documents?|resources?)|what.*available", text))
    if not intents and broad:
        intents = ["all"]
    if not intents:
        intents = ["all"]

    year = None
    m = re.search(r"\b(20\d{2})\s*[-/–]\s*(?:20)?(\d{2})\b", text)
    if m:
        year = f"{m.group(1)}-{m.group(2)}"
    programme = next((p for p, pats in _PROGRAMMES if any(re.search(x, text) for x in pats)), None)
    level = next((l for l, pats in _LEVELS if any(re.search(x, text) for x in pats)), None)

    wants_dates = bool(re.search(r"\bdate|when\b|schedule|deadline|\bese\b|\bmse\b|\bise\b|"
                                 r"holiday|vacation|result|start|begin|end\b", text))
    branch = None
    mb = re.search(r"\bfor ([a-z &]+?) (?:branch|department|engineering)\b", text)
    if mb:
        branch = mb.group(1).strip()
    return {"intents": intents, "academic_year": year, "programme": programme,
            "level": level, "wants_dates": wants_dates, "branch": branch}


def retrieve(question: str) -> dict:
    f = classify(question)
    blocks = []
    if "all" in f["intents"]:
        blocks.append(("all", q.all_academic_documents()))
    else:
        for name, types, _pats in INTENTS:
            if name not in f["intents"]:
                continue
            kw = {}
            if name == "calendar":
                # calendars_only keeps the parent-link arm from pulling in the
                # timetable/syllabus/plan documents, which carry no events.
                kw = {"academic_year": f["academic_year"], "programme": f["programme"],
                      "level": f["level"], "calendars_only": True,
                      "include_parent_linked": True}
            blocks.append((name, q.find(types, **kw)))
    return {"filters": f, "blocks": blocks}


HEADINGS = {"all": "Academic documents", "calendar": "Academic calendars",
            "timetable": "Class timetable", "syllabus": "Syllabus",
            "roll_call": "Roll call lists", "strategic_plan": "Strategic Plan 2025-2030",
            "development_plan": "8 Point Development Plan", "software": "Software"}


def _doc_line(d):
    line = "- " + md_link(d["title"], d["source_url"])
    bits = []
    if d.get("academic_year"):
        bits.append(f"Academic year {d['academic_year']}")
    if d.get("level_note"):
        bits.append(d["level_note"])
    if d.get("document_status") in ("proposed", "tentative", "revised"):
        bits.append(f"marked {d['document_status']}")
    return line, (f"  {' · '.join(bits)}" if bits else None)


def build_answer(result: dict) -> str:
    f = result["filters"]
    out = []
    found_any = False

    for name, docs in result["blocks"]:
        if not docs:
            scope = " ".join(x for x in (f.get("academic_year"), f.get("programme"),
                                         f.get("level")) if x)
            out.append(f"**{HEADINGS.get(name, name)}** — nothing matching "
                       f"{scope or 'that'} is in the KJ GPT knowledge base.")
            years = q.academic_years()
            if years and name == "calendar":
                out.append("Academic calendars held, by year: "
                           + ", ".join(f"{y['academic_year']} ({y['documents']})"
                                       for y in years if y["academic_year"]) + ".")
            out.append("")
            continue

        found_any = True
        out.append(f"**{HEADINGS.get(name, name)}** ({len(docs)}):\n")
        for d in docs:
            line, meta = _doc_line(d)
            out.append(line)
            if meta:
                out.append(meta)

            if d["source_type"] == q.STRATEGIC:
                out.append(f"  Period: {d.get('plan_period')}")
                for g in q.goals_of(d):
                    out.append(f"    {g['number']}. **{g['name']}** — {g['development_agenda']}")
            elif d["source_type"] == q.PLAN:
                out.append(f"  Purpose: {d.get('plan_purpose')} "
                           f"({d.get('parameter_count')} parameters in {len(q.sections_of(d))} sections)")
                for s in q.sections_of(d):
                    out.append(f"    {s['number']}. **{s['name']}** "
                               f"(parameters {s['parameter_range']}): "
                               + "; ".join(s["parameters"]))
            elif d["source_type"] == q.SOFTWARE:
                out.append(f"  {d.get('access_note')}")
            elif d.get("branch_names"):
                branches = q.branches_of(d)
                wanted = f.get("branch")
                if wanted:
                    branches = [b for b in branches
                                if wanted.replace(" ", "") in b["branch"].lower().replace(" ", "")] or branches
                out.append(f"  Per-branch folders ({len(branches)}):")
                for b in branches:
                    out.append("    - " + md_link(b["branch"], b["url"]))
            elif f["wants_dates"] and d.get("event_names"):
                for ev in q.events_of(d):
                    out.append(f"    - {ev['term']} — {ev['event']}: {ev['schedule']}")
        out.append("")

    if found_any:
        out.append("Source: " + md_link("KJSCE official documents page", DOCUMENTS_PAGE)
                   + " (Academics section).")
    return "\n".join(out).strip()


def answer_academic_question(question: str, debug: bool = False) -> dict:
    result = retrieve(question)
    docs = [d for _n, ds in result["blocks"] for d in ds]
    payload = {
        "answer": build_answer(result),
        "documents": [{"doc_id": d["doc_id"], "title": d["title"], "url": d["source_url"],
                       "source_type": d["source_type"], "academic_year": d.get("academic_year"),
                       "programmes": d.get("programmes"), "levels": d.get("levels")}
                      for d in docs],
        "found": bool(docs),
    }
    if debug:
        payload["debug"] = {"filters": result["filters"],
                            "blocks": {n: [d["doc_id"] for d in ds]
                                       for n, ds in result["blocks"]}}
    return payload

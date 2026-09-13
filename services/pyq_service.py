"""Turns a student's question about question papers into Drive links.

    question -> deterministic filter extraction -> Neo4j -> links

Retrieval is deterministic for the same reason the faculty router is: Qwen
never writes Cypher. The vocabulary it matches against is read out of the
graph itself (:Subject aliases), so it grows as the registry grows.

The answer is deterministic too, and that is the important performance
decision. A PYQ answer *is* a list of links that retrieval has already found;
sending it through an 8B model to be retyped adds seconds and can only lose
fidelity. The LLM path is opt-in, for conversational phrasing only.
"""
import re

import graph.pyq_queries as q
from llm.qwen import ask_qwen
from llm.system_prompt import KJGPT_PYQ_SYSTEM_PROMPT

MAX_RESULTS = 50

# The corpus KJGPT is allowed to answer from. The ESE Drive folder reaches back
# to 2013, but only 2019 onwards was mapped, so this is belt-and-braces: even if
# an older paper ever reached the graph it would not be handed to a student.
MIN_YEAR = 2019
MAX_YEAR = 2025
# Only the LLM path is capped -- see build_context(). The deterministic
# answer always lists every match.
MAX_LLM_PAPERS = 15

# Words that carry the request, not the subject.
#
# Connector words ("of", "for", "the") are deliberately NOT stripped: aliases
# like "analysis of algorithms" and "cryptography and system security" need
# them to match. No alias is an English connector, so leaving them costs
# nothing -- except "is", which CASE_SENSITIVE_ALIASES handles separately.
QUESTION_NOISE = [
    "give me", "show me", "send me", "i want", "i need", "can you", "please",
    "get me", "find me", "do you have", "where is", "where can i find",
    "previous year", "past year", "question papers", "question paper",
    "papers", "paper", "pyqs", "pyq", "exams", "exam",
]

# Aliases that are also ordinary English words. Requiring the capitalised form
# stops "What is the OS paper" from being read as a request for Information
# Security. Without this guard, "is" matches almost every question asked.
CASE_SENSITIVE_ALIASES = {"is", "it", "as", "at", "in", "on", "or", "be", "do"}

# Connectors and quantifiers kept in the text for alias matching, but which do
# not count as the student having named a subject.
FILLER_WORDS = {
    "of", "for", "the", "a", "an", "all", "any", "some", "from", "in", "on",
    "at", "to", "me", "my", "and", "or", "is", "are", "do", "you", "have",
    "with", "about", "want", "need", "get", "give", "show", "send", "find",
    "please", "sir", "maam", "kjgpt", "previous", "year", "years", "past",
    "old", "last", "this", "recent", "latest", "s",
}

EXAM_PATTERNS = [
    ("ISE", [r"\bise\b", r"\bmse\b", r"\bmid[\s-]?sem\w*\b", r"\binternal\b",
             r"\bin[\s-]?sem\b"]),
    ("ESE", [r"\bese\b", r"\bend[\s-]?sem\w*\b", r"\bfinal\s+exam\b"]),
]

YEAR_OF_STUDY_PATTERNS = [
    ("MTECH", [r"\bm[\s.]?tech\b", r"\bmtech\b", r"\bmasters?\b"]),
    # "last year" is deliberately NOT here. To a student asking for a paper it
    # almost always means "the previous year's paper", not "Last Year" the
    # fourth-year cohort -- reading it as LY made "I need last year's DBMS
    # paper" return nothing, because DBMS is a second-year subject.
    ("LY", [r"\bly\b", r"\bfinal year\b", r"\bfourth year\b", r"\b4th year\b"]),
    ("TY", [r"\bty\b", r"\bthird year\b", r"\b3rd year\b"]),
    ("SY", [r"\bsy\b", r"\bsecond year\b", r"\b2nd year\b"]),
]

CATEGORY_PATTERNS = [
    ("honours", [r"\bhonou?rs\b"]),
    ("minor", [r"\bminor\b"]),
    ("open_elective", [r"\bopen elective\b", r"\boehm\b", r"\boet\b"]),
    ("dept_elective", [r"\bdept\w*\s+elective\b", r"\bdepartment elective\b"]),
]

ROMAN = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7,
         "viii": 8}

_index_cache: dict | None = None


def _build_index() -> dict:
    """Read the subject vocabulary out of the graph, once per process.

    Same approach as services/faculty_service._build_index(): the router never
    hard-codes a vocabulary it could read from the data.
    """
    pairs = []
    for row in q.all_subjects():
        key = row["subject_key"]
        names = set(row.get("aliases") or [])
        if row.get("name"):
            names.add(row["name"].lower())
        # Unresolved subjects have no registry entry, but a student may well
        # ask for "ITVC paper" -- so the key itself is always an alias.
        names.add(key.replace("_", " "))
        names.add(key)
        for alias in names:
            alias = alias.strip().lower()
            # A one-character alias (the 'c' slug that "C#.pdf" produces) would
            # match a stray letter in almost any question.
            if len(alias) > 1:
                pairs.append((alias, key))
    # Longest alias first, so "database management system" wins over "database".
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    return {"aliases": pairs}


def get_index(refresh: bool = False) -> dict:
    global _index_cache
    if _index_cache is None or refresh:
        _index_cache = _build_index()
    return _index_cache


def _first(text: str, table) -> str | None:
    for label, patterns in table:
        for pattern in patterns:
            if re.search(pattern, text):
                return label
    return None


def extract_filters(question: str) -> dict:
    """Pull structured filters out of a natural-language request.

    Deterministic and cheap -- no model call, so the whole lookup stays in the
    millisecond range.
    """
    raw = question or ""
    text = re.sub(r"[^\w\s#&-]", " ", raw.lower())
    text = re.sub(r"\s+", " ", text).strip()

    filters = {
        "subject_key": None, "exam_type": None, "year": None, "semester": None,
        "year_of_study": None, "category": None, "variant": None,
        "year_min": None, "year_max": None,
    }

    filters["exam_type"] = _first(text, EXAM_PATTERNS)
    filters["year_of_study"] = _first(text, YEAR_OF_STUDY_PATTERNS)
    filters["category"] = _first(text, CATEGORY_PATTERNS)
    if re.search(r"\bpwd\b", text):
        filters["variant"] = "pwd"

    # A span of several years -- "from 2019 to 2025", "between 2019 and 2025",
    # "2019-2025". Checked before the single-year forms, and only accepted when
    # the two years are more than one apart: "2023-2024" is an academic year,
    # not a request for a range.
    span = re.search(
        r"\b(20\d{2})\s*(?:-|–|/|to|until|through|and|upto|up to)\s*(20\d{2})\b",
        text)
    if span and int(span.group(2)) - int(span.group(1)) > 1:
        filters["year_min"] = int(span.group(1))
        filters["year_max"] = int(span.group(2))
    else:
        # Year: a bare 2024, or an academic span like 2023-24 / 23-24.
        m = re.search(r"\b(20\d{2})\s*[-/]\s*(?:20)?\d{2}\b", text) or \
            re.search(r"\b(20\d{2})\b", text)
        if m:
            filters["year"] = int(m.group(1))
        else:
            m = re.search(r"\b(\d{2})\s*[-/]\s*(\d{2})\b", text)
            if m and int(m.group(2)) == int(m.group(1)) + 1:
                filters["year"] = 2000 + int(m.group(1))

    # Semester, numeric or roman.
    m = re.search(r"\bsem(?:ester)?\s*(\d)\b", text) or \
        re.search(r"\b(\d)(?:st|nd|rd|th)?\s+sem(?:ester)?\b", text)
    if m:
        filters["semester"] = int(m.group(1))
    else:
        m = re.search(r"\bsem(?:ester)?\s+(i{1,3}|iv|vi{0,3}|viii)\b", text)
        if m:
            filters["semester"] = ROMAN.get(m.group(1))

    # Subject last, against text with the above signals and request words gone,
    # so "all ISE DBMS papers" cannot match "ise" or "paper" as a subject.
    subject_text = text
    for pattern in [p for _, ps in EXAM_PATTERNS for p in ps] + \
                   [p for _, ps in YEAR_OF_STUDY_PATTERNS for p in ps] + \
                   [p for _, ps in CATEGORY_PATTERNS for p in ps] + \
                   [r"\bsem(?:ester)?\s*\w+\b", r"\b\d{2,4}\b", r"\bpwd\b"]:
        subject_text = re.sub(pattern, " ", subject_text)
    for phrase in sorted(QUESTION_NOISE, key=len, reverse=True):
        subject_text = re.sub(rf"\b{re.escape(phrase)}\b", " ", subject_text)
    subject_text = re.sub(r"\s+", " ", subject_text).strip()

    for alias, key in get_index()["aliases"]:
        if alias in CASE_SENSITIVE_ALIASES:
            # Must appear capitalised in what the student actually typed.
            if not re.search(rf"\b{re.escape(alias.upper())}\b", raw):
                continue
        elif not re.search(rf"\b{re.escape(alias)}\b", subject_text):
            continue
        filters["subject_key"] = key
        break

    # What the student named that we could not map to a subject. Lets the
    # caller tell "organic chemistry" (a subject we don't hold) apart from
    # "give me all papers" (no subject named at all). Filler left behind by the
    # connectors we deliberately kept does not count as naming anything.
    leftover = [w for w in subject_text.split() if w not in FILLER_WORDS]
    filters["_unmatched_text"] = (
        "" if filters["subject_key"] else " ".join(leftover))
    return filters


def build_context(rows: list[dict], filters: dict,
                  limit: int | None = None) -> str:
    """Plain-text list of papers and links, ready to show or to hand to Qwen.

    `limit` truncates the list. Only the LLM path uses it: reformatting 50
    links took Qwen3 8B past a 120 s timeout, while the deterministic path
    renders the whole set in microseconds and is never truncated.
    """
    if not rows:
        return ""
    described = describe_filters(filters)
    shown = rows if limit is None else rows[:limit]
    lines = [f"{len(rows)} matching question paper(s){described}:"]
    for r in shown:
        bits = [r["title"]]
        if r.get("page_label"):
            bits.append(f"({r['page_label']})")
        lines.append(f"- {' '.join(bits)}\n  {r['drive_url']}")
    if len(shown) < len(rows):
        lines.append(f"... and {len(rows) - len(shown)} more not listed here.")
    return "\n".join(lines)


def describe_filters(filters: dict) -> str:
    parts = []
    if filters.get("subject_key"):
        parts.append(filters["subject_key"].upper())
    if filters.get("exam_type"):
        parts.append(filters["exam_type"])
    if filters.get("year"):
        parts.append(str(filters["year"]))
    if filters.get("year_min") or filters.get("year_max"):
        parts.append(f"{filters.get('year_min') or MIN_YEAR}"
                     f"-{filters.get('year_max') or MAX_YEAR}")
    if filters.get("semester"):
        parts.append(f"sem {filters['semester']}")
    if filters.get("year_of_study"):
        parts.append(filters["year_of_study"])
    if filters.get("category") and filters["category"] != "core":
        parts.append(filters["category"].replace("_", " "))
    if filters.get("variant"):
        parts.append(filters["variant"].upper())
    return f" for {', '.join(parts)}" if parts else ""


def retrieve(question: str, limit: int = MAX_RESULTS) -> dict:
    filters = extract_filters(question)

    # An unfiltered question would dump the whole corpus; that is a miss, not a
    # match, and should be reported as one.
    if not any(filters[k] for k in
               ("subject_key", "year", "semester", "year_of_study",
                "category", "variant", "exam_type", "year_min", "year_max")):
        reason = "unknown_subject" if filters["_unmatched_text"] else "no_filters"
        return {"filters": filters, "rows": [], "context": "", "reason": reason}

    # Both ISE and ESE are ingested, so an unstated exam type means BOTH.
    # "all OS papers" has to return every OS paper; only an explicit "ISE" or
    # "ESE" in the question narrows it.
    # Underscore-prefixed keys are diagnostics for the caller, not query filters.
    query_filters = {k: v for k, v in filters.items() if not k.startswith("_")}
    # A span the student asked for narrows the corpus window; it can never
    # widen it, so a request for "2015 to 2025" still yields 2019 onwards.
    asked_min = query_filters.pop("year_min", None)
    asked_max = query_filters.pop("year_max", None)

    rows = q.find_pyq(limit=limit,
                      year_min=max(MIN_YEAR, asked_min or MIN_YEAR),
                      year_max=min(MAX_YEAR, asked_max or MAX_YEAR),
                      **query_filters)
    reason = None if rows else "no_match"
    return {"filters": filters, "rows": rows,
            "context": build_context(rows, filters), "reason": reason}


def answer_pyq_question(question: str, debug: bool = False,
                        use_llm: bool = False) -> dict:
    """Answer one PYQ question.

    use_llm=False (the default) returns the deterministic list. It is instant
    and cannot mangle a URL. use_llm=True sends the same context to Qwen with
    thinking off, for conversational phrasing.
    """
    trace = {"question": question}
    result = retrieve(question)
    trace["filters"] = result["filters"]
    trace["result_count"] = len(result["rows"])
    trace["context"] = result["context"]
    trace["reason"] = result["reason"]

    if not result["rows"]:
        if result["reason"] == "unknown_subject":
            named = result["filters"]["_unmatched_text"]
            answer = (f"I don't have any papers for \"{named}\" in the KJGPT "
                      "knowledge base.")
        elif result["reason"] == "no_filters":
            answer = ("Tell me which paper you want -- for example "
                      "\"DBMS 2024 ISE paper\" or \"all OS papers\".")
        else:
            answer = ("I couldn't find a matching question paper in the KJGPT "
                      "knowledge base.")
        trace["answer"] = answer
        return trace if debug else {"answer": answer, "papers": []}

    if use_llm:
        answer = ask_qwen(
            KJGPT_PYQ_SYSTEM_PROMPT,
            "PAPERS FOUND:\n"
            + build_context(result["rows"], result["filters"],
                            limit=MAX_LLM_PAPERS)
            + f"\n\nSTUDENT ASKED:\n{question}",
            think=False,
            timeout=180,
        )
    else:
        answer = result["context"]

    trace["answer"] = answer
    if debug:
        return trace
    return {"answer": answer, "papers": [
        {"title": r["title"], "drive_url": r["drive_url"],
         "subject": r["subject"], "exam_type": r["exam_type"],
         "academic_year": r["academic_year"], "semester": r["semester"]}
        for r in result["rows"]]}

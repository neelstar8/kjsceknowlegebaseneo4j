"""Turns raw Google Drive file records into PYQ + PYQFile records.

Two hard rules, inherited from normalization/faculty_normalizer.py:

  1. Nothing is invented. An abbreviation that is not in the curated registry
     comes out as subject_status="unresolved" -- never as a plausible guess.
  2. Parsing is deterministic. No LLM, no fuzzy matching. The corpus contains
     'Futter.pdf', and a fuzzy matcher would resolve that confidently and
     wrongly; an exact matcher reports it and waits for a human.

Parsing is token-bag based, not positional, because the same facts appear in
different orders across years:

    TY V OS.PDF                    ISE_COA_SY.pdf
    SY_ISE_ITVC.pdf                DSM_QUESTION PAPER_withoutCOs.pdf
    OS.pdf                         SVU_SEM_III_OOPM_2021-22_without_CO.pdf

The folder path is treated as at least as authoritative as the file name --
for the 24-25 files ('OS.pdf') it is the only source of context there is.
"""
import json
import os
import re

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
SUBJECTS_FILE = os.path.join(DATA_DIR, "pyq_subjects.json")
OVERRIDES_FILE = os.path.join(DATA_DIR, "pyq_overrides.json")

# ---------------------------------------------------------------- vocabularies

INGESTIBLE_MIME_TYPES = {"application/pdf", "image/jpeg", "image/png"}
ARCHIVE_MIME_TYPES = {
    "application/zip", "application/x-zip-compressed",
    "application/x-rar-compressed", "application/x-7z-compressed",
    "application/gzip", "application/x-tar",
}

EXAM_ISE_TOKENS = [
    "internal semester examination", "internal semester exam",
    "mid semester", "mid-semester", "mid sem", "mid-sem",
    "midsem", "insem", "in-sem", "ise", "mse", "internal",
]
EXAM_ESE_TOKENS = [
    "end semester examination", "end semester exam", "end semester",
    "end-semester", "end sem", "end-sem", "endsem", "semester end",
    "university exam", "final exam", "ese",
]

# Words the uploaders add that carry no metadata. Stripped before subject
# matching so they can never be mistaken for a subject abbreviation.
#
# Removal is longest-phrase-first, which is why the compound entries matter:
# "of question paper" has to win over "question paper", or a stray "of" is
# left behind and ends up inside the subject slug.
NOISE_PHRASES = [
    "without bt co", "without co and bt", "without_bt_co", "without co",
    "without_co", "withoutcos", "withoutco", "without cos", "with co",
    "without co bt mapping", "bt mapping", "mapping",
    "with blooms and toxonomy", "blooms and toxonomy", "blooms", "toxonomy",
    "taxonomy", "taxo",
    "template for question paper", "of question paper", "template for",
    "template", "question paper", "question", "paper", "qp", "pdf", "docx",
    "q paper", "for pwd students", "for students", "students", "student",
    "svu", "drive download", "and syllabus", "rev", "sa",
    "deptelec", "dept elec", "open elective", "elective", "abled",
]

# Standalone letters/fragments left over once real words are gone. Only ever
# applied to the residue, never to the original name.
RESIDUE_TOKENS = ["q", "s", "de", "o", "e", "for", "of", "the", "and"]

# Category prefixes. These describe the *track* a subject belongs to, not the
# subject, so they are recorded separately and removed before subject matching.
CATEGORY_PATTERNS = [
    ("honours", [r"\bhonours\b", r"\bhonors\b", r"\bh\b"]),
    ("minor", [r"\bminor\b", r"\bm\b"]),
    # OEHM = open elective (humanities/management), OET = open elective
    # (technical). Both are tracks, not subjects.
    ("open_elective", [r"\boehm\b", r"\boet\b", r"\boe\b",
                       r"\bopen elective\b"]),
    ("dept_elective", [r"\bdeptelec\b", r"\bdept elec\w*\b",
                       r"\bdepartment elective\b"]),
]

VARIANT_PATTERNS = [("pwd", [r"\bpwd\b", r"\bpwds\b"])]

# Branch and exam-admin words that appear in ESE file names where a subject
# would otherwise be read. Every one of these is checked against the registry
# as a non-alias, and all are stripped whole-word only -- '\bcomp\b' cannot
# fire inside "computer networks", which is why the abbreviation is listed and
# the full word deliberately is not.
ADMIN_NOISE_PHRASES = [
    "comp", "extc", "etrx", "mech", "excp", "idc", "phd", "ph d",
    "b tech", "btech", "first year",
    "exams", "exam", "kt", "k t",
]

YEAR_OF_STUDY_PATTERNS = [
    ("MTECH", [r"\bm\s*\.?\s*tech\b", r"\bmtech\b", r"\bme\b"]),
    ("LY", [r"\bly\b", r"\blast year\b", r"\bfinal year\b", r"\bbe\b"]),
    ("TY", [r"\bty\b", r"\bthird year\b"]),
    ("SY", [r"\bsy\b", r"\bsecond year\b"]),
]

ROMAN_TO_INT = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5,
                "vi": 6, "vii": 7, "viii": 8}
INT_TO_ROMAN = {v: k.upper() for k, v in ROMAN_TO_INT.items()}

# year_of_study + term -> semester. The one genuinely derivable fact in the
# whole corpus, and it is confirmed by the files that state both
# ("TY V OS.PDF" in a 23-24 odd folder).
SEMESTER_TABLE = {
    ("SY", "odd"): 3, ("SY", "even"): 4,
    ("TY", "odd"): 5, ("TY", "even"): 6,
    ("LY", "odd"): 7, ("LY", "even"): 8,
    ("MTECH", "odd"): 1, ("MTECH", "even"): 2,
}

# The inverse of SEMESTER_TABLE for B.Tech. M.Tech sems 1-2 collide with
# B.Tech's own numbering, so they are deliberately absent -- an M.Tech file has
# to say "M Tech" in its path to be read as one.
SEMESTER_TO_YEAR_OF_STUDY = {3: "SY", 4: "SY", 5: "TY", 6: "TY",
                             7: "LY", 8: "LY"}

# Month names encode the term (July-Nov = odd, Jan-May = even) and are
# stripped before subject matching so they cannot end up inside a subject slug.
MONTH_WORDS = [
    "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december",
    "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sept", "sep",
    "oct", "nov", "dec", "to",
]

# Underscore counts as a word character, so \b will not fire on
# '..._116U01C301.pdf' -- explicit alphanumeric lookarounds instead.
SUBJECT_CODE_RE = re.compile(
    r"(?<![A-Za-z0-9])\d{3}U\d{2}[A-Z]\d{3}(?![A-Za-z0-9])", re.I)
PAGE_LABEL_RE = re.compile(r"\b(\d+)\s*(?:pg|pgs|page|pages|part)\b", re.I)

# Ranges are listed before bare months, because "JANUARY - JUNE 2024" must be
# read as the even term rather than matching a stray month word. The ESE tree
# names its terms this way at every level ('Nov-Dec', 'May-June',
# 'JULY- DECEMBER -2024'), so the range forms carry most of the weight there.
MONTH_TERM = [
    ("odd", [r"\bjul\w*\s*[-–\s]\s*nov\w*", r"\bjuly\s*to\s*nov",
             r"\baug\w*\s*[-–\s]\s*dec\w*",
             r"\bjul\w*\s*[-–]?\s*dec\w*", r"\bnov\w*\s*[-–\s]\s*dec\w*",
             r"\boct\w*\s*[-–\s]\s*nov\w*",
             r"\bsept?\w*\b", r"\boct\w*\b"]),
    ("even", [r"\bjan\w*\s*[-–\s]\s*may\w*", r"\bfeb\w*\s*[-–\s]\s*jun\w*",
              r"\bjan\w*\s*[-–]?\s*jun\w*", r"\bjan\w*\s*[-–]?\s*apr\w*",
              r"\bmay\s*[-–\s]\s*jun\w*", r"\bapr\w*\s*[-–\s]\s*may\b",
              r"\bmar\w*\b", r"\bapr\w*\b"]),
]

# Branch folders in the ESE tree. The ISE collection is single-branch and says
# so in config; this corpus splits by branch in the path instead.
BRANCH_PATTERNS = [
    ("Computer Engineering", [r"\bcomp\b", r"\bcomputer\b", r"\bcmpn\b"]),
    ("Information Technology", [r"\bi\s*\.?\s*t\b", r"\binformation technology\b"]),
    ("Electronics and Telecommunication", [r"\bextc\b"]),
    ("Electronics Engineering", [r"\betrx\b", r"\bexcp\b"]),
    ("Mechanical Engineering", [r"\bmech\b"]),
    ("First Year", [r"\bfirst year\b", r"\bfe\b"]),
    ("Interdisciplinary", [r"\bidc\b"]),
    ("PhD", [r"\bphd\b", r"\bph\s*\.?\s*d\b"]),
]


# ------------------------------------------------------------------- registry

def load_subjects(path: str = SUBJECTS_FILE) -> list[dict]:
    """Only the 'subjects' block is loaded. 'candidates' is documentation."""
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("subjects", [])


def load_overrides(path: str = OVERRIDES_FILE) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {k: v for k, v in data.items() if not k.startswith("_")}


def build_alias_index(subjects: list[dict]) -> list[tuple[str, dict]]:
    """(alias, subject) pairs, longest alias first so 'data structures' wins
    over a bare 's' style collision before the short form is ever tried."""
    pairs = [(a.lower().strip(), s) for s in subjects for a in s["aliases"]]
    return sorted(pairs, key=lambda p: len(p[0]), reverse=True)


# --------------------------------------------------------------- text helpers

def normalize_text(value: str) -> str:
    """Lowercase, punctuation to spaces, whitespace collapsed."""
    value = (value or "").lower()
    value = re.sub(r"\.(pdf|jpe?g|png|zip)$", " ", value)
    value = re.sub(r"[_\-.,()\[\]/&+]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def strip_phrases(text: str, phrases: list[str]) -> str:
    """Remove whole-word phrases, longest first, leaving a space behind."""
    for phrase in sorted(phrases, key=len, reverse=True):
        text = re.sub(rf"\b{re.escape(phrase)}\b", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _match_any(text: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            return m.group(0).strip()
    return None


# ----------------------------------------------------------------- resolvers

def resolve_exam_type(file_name: str, folder_names: list[str]) -> dict:
    """Nearest-first: file name, then each folder from the leaf up to the root.

    Returns {"exam_type", "original_exam_label", "exam_type_source", "reason"}.
    An ESE marker at a nearer level beats an ISE marker at a farther one, so a
    file explicitly named ESE inside an ISE-titled tree is still classified ESE.
    """
    levels = [("file_name", file_name)]
    # folder_names is root-first; walk it leaf-first so nearer context wins.
    for i, name in enumerate(reversed(folder_names)):
        source = "collection_root" if i == len(folder_names) - 1 else "folder_path"
        levels.append((source, name))

    for source, raw in levels:
        text = normalize_text(raw)
        ise = _match_any(text, [rf"\b{re.escape(t)}\b" for t in EXAM_ISE_TOKENS])
        ese = _match_any(text, [rf"\b{re.escape(t)}\b" for t in EXAM_ESE_TOKENS])
        if ise and ese:
            return {"exam_type": None, "original_exam_label": None,
                    "exam_type_source": source, "reason": "exam_type_ambiguous"}
        if ese:
            return {"exam_type": "ESE", "original_exam_label": ese,
                    "exam_type_source": source, "reason": None}
        if ise:
            return {"exam_type": "ISE", "original_exam_label": ise,
                    "exam_type_source": source, "reason": None}

    return {"exam_type": None, "original_exam_label": None,
            "exam_type_source": None, "reason": "exam_type_unknown"}


def resolve_academic_year(text: str) -> str | None:
    """'23-24', '2021-22', '2021_2022', '2022-2023' -> '2023-24' style."""
    m = re.search(r"\b(20\d{2})\s*[-–\s]\s*(20\d{2}|\d{2})\b", text)
    if m:
        start = int(m.group(1))
        return f"{start}-{str(start + 1)[2:]}"
    m = re.search(r"\b(\d{2})\s*[-–\s]\s*(\d{2})\b", text)
    if m:
        start, end = int(m.group(1)), int(m.group(2))
        # Only consecutive two-digit pairs are academic years; '116U01' style
        # codes and page ranges are not.
        if end == start + 1 and 15 <= start <= 40:
            return f"20{start:02d}-{end:02d}"
    return None


def resolve_calendar_year(text: str) -> int | None:
    """A standalone four-digit year, as the ESE tree's '2024' folders use.

    Deliberately separate from resolve_academic_year: that one needs a span
    ('23-24') and would never fire on a bare year. Bounded to the plausible
    range so a subject code or a page count cannot be read as a year.
    """
    for m in re.finditer(r"(?<!\d)(20[0-3]\d)(?!\d)", text):
        year = int(m.group(1))
        if 2000 <= year <= 2035:
            return year
    return None


def academic_year_from(exam_year: int | None, term: str | None) -> str | None:
    """Inverse of exam_year_from. An odd-term exam opens the academic year, an
    even-term one closes it, so 'JULY-DEC 2024' is 2024-25 but 'JAN-JUNE 2024'
    is 2023-24."""
    if not exam_year or not term:
        return None
    start = exam_year if term == "odd" else exam_year - 1
    return f"{start}-{str(start + 1)[2:]}"


def resolve_branch(text: str) -> str | None:
    for branch, patterns in BRANCH_PATTERNS:
        if _match_any(text, patterns):
            return branch
    return None


def despace_initials(text: str) -> str:
    """'sem vi comp d b m s' -> 'sem vi comp dbms'.

    This corpus spells abbreviations out letter by letter ('D B M S', 'C S S',
    'S E'), which no alias in the registry would ever match. Runs of two or
    more single letters are glued back together; anything else is untouched, so
    ordinary words cannot be corrupted. Used only as a fallback when the text
    as written resolved nothing.
    """
    return re.sub(r"\b(?:[a-z]\s+){1,7}[a-z]\s*$",
                  lambda m: m.group(0).replace(" ", ""), text)


def resolve_term(text: str) -> str | None:
    if re.search(r"\bodd\b", text):
        return "odd"
    if re.search(r"\beven\b", text):
        return "even"
    for term, patterns in MONTH_TERM:
        if _match_any(text, patterns):
            return term
    return None


def exam_year_from(academic_year: str | None, term: str | None) -> int | None:
    """Odd semester exams sit in the first calendar year, even in the second."""
    if not academic_year or not term:
        return None
    start = int(academic_year[:4])
    return start if term == "odd" else start + 1


def candidate_years(academic_year: str | None,
                    exam_year: int | None) -> set[int]:
    """Every calendar year a paper could plausibly belong to.

    An academic year spans two calendar years and the term is often missing,
    so '2018-19' is genuinely either 2018 or 2019 until a term says otherwise.
    """
    years: set[int] = set()
    if exam_year:
        years.add(int(exam_year))
    if academic_year:
        start = int(academic_year[:4])
        years.update({start, start + 1})
    return years


def year_in_window(academic_year: str | None, exam_year: int | None,
                   min_year: int | None, max_year: int | None):
    """(in_window, reason) for a [min_year, max_year] calendar-year filter.

    Admits a paper when ANY plausible year falls inside the window, so an
    undated-term '2018-19' file still qualifies for a 2019+ window on its 2019
    reading. A paper with no year information at all is never silently
    admitted -- it is reported so a human can look at it.
    """
    if min_year is None and max_year is None:
        return True, None
    years = candidate_years(academic_year, exam_year)
    if not years:
        return False, "year_unknown"
    lo = min_year if min_year is not None else min(years)
    hi = max_year if max_year is not None else max(years)
    if any(lo <= y <= hi for y in years):
        return True, None
    return False, "year_out_of_range"


def resolve_year_of_study(text: str) -> str | None:
    for label, patterns in YEAR_OF_STUDY_PATTERNS:
        if _match_any(text, patterns):
            return label
    return None


def resolve_roman_semester(text: str) -> int | None:
    """An explicit roman numeral standing alone, as in 'TY V OS' or 'SEM III'."""
    m = re.search(r"\bsem(?:ester)?\s+([ivx]+)\b", text)
    if not m:
        m = re.search(r"\b(i{1,3}|iv|vi{0,3}|viii)\b", text)
    if not m:
        return None
    return ROMAN_TO_INT.get(m.group(1).lower())


def resolve_category(text: str) -> tuple[str, str | None]:
    """(category, matched token). 'core' when no track prefix is present."""
    for category, patterns in CATEGORY_PATTERNS:
        hit = _match_any(text, patterns)
        if hit:
            return category, hit
    return "core", None


def resolve_variant(text: str) -> str:
    return "pwd" if _match_any(text, VARIANT_PATTERNS[0][1]) else "regular"


def resolve_subjects(text: str, alias_index) -> tuple[list[dict], str]:
    """Every distinct subject whose alias appears as whole words in `text`.

    Matched spans are blanked out as we go, so a short alias cannot re-match
    inside a longer one that already won. Returns (subjects, leftover_text).
    """
    found, seen = [], set()
    remaining = text
    for alias, subject in alias_index:
        pattern = rf"\b{re.escape(alias)}\b"
        if not re.search(pattern, remaining):
            continue
        remaining = re.sub(pattern, " ", remaining)
        remaining = re.sub(r"\s+", " ", remaining).strip()
        if subject["subject_key"] not in seen:
            seen.add(subject["subject_key"])
            found.append(subject)
    return found, remaining


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (value or "").lower()).strip("_")


def bundle_subject_key(branch: str | None) -> str:
    """Identity slot for a semester bundle.

    Deliberately prefixed so it can never collide with a real subject_key and
    never be returned by a subject query looking for 'os' or 'dbms'.
    """
    return f"_bundle_{slugify(branch) or 'unknown'}"


def build_pyq_id(subject_key, exam_type, academic_year, term, semester,
                 category, variant) -> str:
    """Deterministic: the same parsed metadata always yields the same id, which
    is what makes re-running the ingest an update rather than a duplicate."""
    return "|".join([
        subject_key or "unknown",
        exam_type or "UNKNOWN",
        academic_year or "unknown",
        term or "unknown",
        f"sem{semester}" if semester else "sem_unknown",
        category or "core",
        variant or "regular",
    ])


def build_title(subject_name, exam_type, semester, academic_year,
                category, variant) -> str:
    # An unresolved subject arrives as the raw filename token ("itvc"). Shown
    # to a student it should read as the abbreviation they typed, not a slug.
    if subject_name and subject_name.islower() and " " not in subject_name:
        subject_name = subject_name.upper()
    parts = [subject_name or "Unknown subject"]
    detail = [exam_type or "Unknown exam"]
    if semester:
        detail.append(f"Sem {INT_TO_ROMAN.get(semester, semester)}")
    if academic_year:
        detail.append(academic_year)
    if category and category != "core":
        detail.append(category.replace("_", " ").title())
    if variant == "pwd":
        detail.append("PwD")
    return f"{parts[0]} — {', '.join(detail)}"


# ------------------------------------------------------------------ the parse

def classify_file(raw: dict) -> str | None:
    """Reasons a file is excluded before any parsing is attempted."""
    path = (raw.get("folder_path") or "").lower()
    if any(seg.strip().startswith("syllabus")
           for seg in path.split("/")):
        return "excluded_syllabus"
    mime = raw.get("mime_type") or ""
    if mime in ARCHIVE_MIME_TYPES:
        return "excluded_archive"
    if mime not in INGESTIBLE_MIME_TYPES:
        return "excluded_mime"
    return None


def to_file_record(raw: dict, collection: str) -> dict:
    """The PYQFile side. Pure Drive facts -- never any parsed interpretation."""
    return {
        "drive_file_id": raw["drive_file_id"],
        "drive_url": raw.get("drive_url"),
        "file_name": raw.get("file_name"),
        "mime_type": raw.get("mime_type"),
        "file_size": raw.get("file_size"),
        "parent_folder_id": raw.get("parent_folder_id"),
        "parent_folder_name": raw.get("parent_folder_name"),
        "folder_path": raw.get("folder_path"),
        "drive_created_time": raw.get("drive_created_time"),
        "drive_modified_time": raw.get("drive_modified_time"),
        "source": "google_drive",
        "collection": collection,
    }


def _subject_text_from(text: str, consumed: list[str]) -> str:
    """Strip everything already accounted for, leaving only the subject."""
    text = strip_phrases(text, consumed)
    text = re.sub(r"\b\d{3}u\d{2}[a-z]\d{3}\b", " ", text)
    # 'semiv', 'semvii' -- 'sem' glued to a roman numeral with no separator.
    text = re.sub(r"\bsem(i{1,3}|iv|vi{0,3}|viii)\b", " ", text)
    text = re.sub(r"\b(i{1,3}|iv|vi{0,3}|viii)\b", " ", text)
    # 'nov2020', 'march2021' -- month glued to a year.
    text = re.sub(
        r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s*\d{2,4}\b",
        " ", text)
    text = re.sub(r"\b\d{2,4}\b", " ", text)
    text = PAGE_LABEL_RE.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_pyq(raw: dict, alias_index, *, branch: str,
                  collection: str, overrides: dict | None = None,
                  default_exam_type: str | None = None) -> dict:
    """Parse one Drive file into {file, papers, reasons}.

    `papers` may hold more than one entry when a single physical file contains
    several identifiable papers, and may be empty when the file is excluded or
    cannot be classified. The file record is produced either way, so a rejected
    file is still fully reported.
    """
    overrides = overrides or {}
    reasons: list[str] = []
    file_record = to_file_record(raw, collection)

    excluded = classify_file(raw)
    if excluded:
        return {"file": file_record, "papers": [], "reasons": [excluded]}

    file_name = raw.get("file_name") or ""
    folder_names = [p for p in (raw.get("folder_path") or "").split("/") if p]

    exam = resolve_exam_type(file_name, folder_names)
    # Nothing in the ESE tree names the exam type -- not the files, not the
    # folders, not even its root. The operator asserts it per collection
    # instead, exactly as the ISE root asserts it by being named for it. Only
    # 'unknown' defers to that default; a contradictory tree is still rejected.
    if exam["exam_type"] is None and default_exam_type and \
            exam["reason"] == "exam_type_unknown":
        exam = {"exam_type": default_exam_type, "original_exam_label": None,
                "exam_type_source": "collection_default", "reason": None}
    # ISE and ESE are both first-class now. Only a file we cannot classify at
    # all (no marker anywhere, or contradictory markers) is rejected here.
    if exam["exam_type"] is None:
        return {"file": file_record, "papers": [],
                "reasons": [exam["reason"]], "exam": exam}

    name_text = normalize_text(file_name)
    # 'sem vi comp d b m s' -> 'sem vi comp dbms'. Done here, before anything
    # else reads the text: the 'minor' category pattern matches a standalone
    # 'm' and would otherwise eat the M out of D B M S. Anchored to the end of
    # the name, so an interior run like the 'v h' of 'TY V H-BCT' is untouched.
    despaced_name = despace_initials(name_text)
    path_text = normalize_text(" ".join(folder_names))
    both_text = f"{name_text} {path_text}"

    subject_code_match = SUBJECT_CODE_RE.search(file_name)
    subject_code = subject_code_match.group(0).upper() if subject_code_match else None

    page_match = PAGE_LABEL_RE.search(file_name)
    page_label = page_match.group(0).strip() if page_match else None
    part_index = int(page_match.group(1)) if page_match else None

    # Folder first: for the 24-25 files the path is the only context there is.
    academic_year = (resolve_academic_year(path_text)
                     or resolve_academic_year(name_text))
    term = resolve_term(path_text) or resolve_term(name_text)
    # The ESE tree dates itself with a bare year folder ('2024') and a term
    # folder ('JANUARY - JUNE 2024') instead of an academic span, so rebuild the
    # span from the two. Only reached when no '23-24' style span was found.
    if not academic_year:
        academic_year = academic_year_from(
            resolve_calendar_year(path_text) or resolve_calendar_year(name_text),
            term)
    year_of_study = (resolve_year_of_study(path_text)
                     or resolve_year_of_study(name_text))
    # A branch named in the path beats the collection-wide default.
    detected_branch = resolve_branch(path_text)

    semester = SEMESTER_TABLE.get((year_of_study, term))
    explicit_semester = resolve_roman_semester(name_text)
    if explicit_semester and semester and explicit_semester != semester:
        reasons.append("semester_mismatch")
        semester = explicit_semester
    elif explicit_semester and not semester:
        semester = explicit_semester

    # ESE names the semester and leaves the cohort implicit ('COMP- SEM- VIII'),
    # which is the ISE corpus's relationship the other way round.
    if semester and not year_of_study:
        year_of_study = SEMESTER_TO_YEAR_OF_STUDY.get(semester)

    if not academic_year:
        reasons.append("academic_year_unknown")
    if not semester:
        reasons.append("semester_unknown")

    category, category_token = resolve_category(despaced_name)
    variant = resolve_variant(both_text)

    # Strip everything already accounted for, so only the subject is left.
    consumed = list(NOISE_PHRASES) + ADMIN_NOISE_PHRASES + \
        EXAM_ISE_TOKENS + EXAM_ESE_TOKENS + [
        "sy", "ty", "ly", "mtech", "m tech", "sem", "semester",
        "odd", "even", "pwd", "pwds", "without", "co", "cos", "bt",
    ] + MONTH_WORDS
    if category_token:
        consumed.append(category_token)
    subject_text = _subject_text_from(name_text, consumed)

    # Residue words are stripped only AFTER matching: aliases like "analysis of
    # algorithms" and "computer organization and architecture" need their
    # connecting words intact to match at all.
    matched, leftover = resolve_subjects(subject_text, alias_index)
    if not matched and despaced_name != name_text:
        alt = _subject_text_from(despaced_name, consumed)
        alt_matched, alt_leftover = resolve_subjects(alt, alias_index)
        if alt_matched:
            matched, leftover = alt_matched, alt_leftover
            reasons.append("despaced_initials")
    leftover = strip_phrases(leftover, RESIDUE_TOKENS)

    override = overrides.get(raw["drive_file_id"]) or {}
    if override.get("papers"):
        reasons.append("override_applied")

    papers = []
    if override.get("papers"):
        for spec in override["papers"]:
            papers.append(_build_paper(
                spec.get("subject_key"), spec.get("subject_name"),
                spec.get("subject_raw") or file_name, "resolved",
                spec.get("subject_code") or subject_code,
                exam, spec.get("academic_year") or academic_year, term,
                spec.get("semester") or semester, year_of_study,
                spec.get("branch") or detected_branch or branch,
                spec.get("course_category") or category,
                spec.get("variant") or variant,
                spec.get("section_label"), page_label, part_index,
            ))
    elif matched:
        if len(matched) > 1:
            reasons.append("multi_paper_file")
        for subject in matched:
            papers.append(_build_paper(
                subject["subject_key"], subject["name"], subject["aliases"][0],
                "resolved", subject_code or subject.get("code"),
                exam, academic_year, term, semester, year_of_study,
                detected_branch or branch, category, variant,
                subject["name"] if len(matched) > 1 else None,
                page_label, part_index,
            ))
    elif explicit_semester and not leftover:
        # Nothing subject-like is left and the FILE ITSELF names a whole
        # semester -- 'COMP- SEM- VIII..pdf'. A semester merely inherited from
        # the folder is not enough, or an ISE file that simply omits its
        # subject ('ISE-QP without co.pdf') would be misread as a bundle.
        # That is a bundle of every paper sat that
        # semester, not a paper about a subject called "comp sem viii". It is
        # recorded at semester level and carries no FOR_SUBJECT edge, so a
        # subject query can never reach it. Inspecting the PDF may later split
        # it into real subject papers; until then this is the honest record.
        reasons.append("semester_bundle")
        papers.append(_build_paper(
            bundle_subject_key(detected_branch or branch), None,
            file_name, "unresolved", subject_code, exam, academic_year, term,
            semester, year_of_study, detected_branch or branch, category,
            variant, None, page_label, part_index, is_bundle=True,
        ))
    else:
        reasons.append("unresolved_subject")
        raw_token = leftover or subject_text or file_name
        papers.append(_build_paper(
            slugify(raw_token) or "unknown", None, raw_token, "unresolved",
            subject_code, exam, academic_year, term, semester, year_of_study,
            detected_branch or branch, category, variant, None,
            page_label, part_index,
        ))

    return {"file": file_record, "papers": papers, "reasons": reasons,
            "exam": exam}


def _build_paper(subject_key, subject_name, subject_raw, status, subject_code,
                 exam, academic_year, term, semester, year_of_study, branch,
                 category, variant, section_label, page_label, part_index,
                 branch_source="collection_default", is_bundle=False):
    program = "M.Tech" if year_of_study == "MTECH" else "B.Tech"
    display_name = subject_name or subject_raw
    if is_bundle:
        display_name = f"{branch or 'All branches'} (all subjects)"
    return {
        "pyq_id": build_pyq_id(subject_key, exam["exam_type"], academic_year,
                               term, semester, category, variant),
        "subject": display_name,
        "subject_key": subject_key,
        "subject_raw": subject_raw,
        "subject_code": subject_code,
        "subject_status": status,
        "subject_name_canonical": subject_name,
        "exam_type": exam["exam_type"],
        "original_exam_label": exam["original_exam_label"],
        "exam_type_source": exam["exam_type_source"],
        "academic_year": academic_year,
        "exam_year": exam_year_from(academic_year, term),
        "exam_term": term,
        "semester": semester,
        "semester_roman": INT_TO_ROMAN.get(semester) if semester else None,
        "year_of_study": year_of_study,
        "program": program if year_of_study else None,
        "branch": branch,
        "branch_source": branch_source,
        "is_bundle": is_bundle,
        "course_category": category,
        "variant": variant,
        "title": build_title(display_name, exam["exam_type"], semester,
                             academic_year, category, variant),
        "edge": {"section_label": section_label, "page_label": page_label,
                 "part_index": part_index},
    }


# Neo4j properties must be primitives or arrays of primitives, and an empty
# value must never overwrite a good one -- same contract as the faculty layer.
NESTED_FIELDS = ("edge", "subject_name_canonical")


def to_neo4j_properties(paper: dict) -> dict:
    return {k: v for k, v in paper.items()
            if k not in NESTED_FIELDS and v is not None and v != "" and v != []}

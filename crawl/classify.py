"""Routing a crawled document to a source_type and an existing parent policy.

Deliberately a lookup table, not a model. The rule is: if a document does not match
a known pattern, it is *not* guessed at -- it becomes REVIEW and a human decides.
An unrouted document costs one review; a wrongly routed one silently answers student
questions out of the wrong section.

Every parent here is a `:Policy` node that already exists in the graph. Nothing in
this module invents a parent, which is the same refusal `exam_ingestion.py` and
`academics_ingestion.py` already enforce at write time.
"""
from __future__ import annotations

import re
import urllib.parse as up

from crawl.site_urls import filename_of

# (source_type, parent policy_id, matcher) -- first match wins, so order matters.
ROUTES: list[tuple[str, str, re.Pattern]] = [
    ("ranking_report", "qms_iqac",
     re.compile(r"(?i)\b(nirf|ariia|arifa|national institutional ranking|"
                r"atal ranking)\b")),

    ("accreditation_document", "qms_iqac",
     re.compile(r"(?i)\b(naac|nba|accreditation|iqac|aqar|ssr)\b")),

    ("mandatory_disclosure", "governance_statutory_bodies",
     re.compile(r"(?i)\bmandatory\s+disclosure\b")),

    ("admission_document", "admission_process",
     re.compile(r"(?i)\b(admission|prospectus|brochure|eligibility criteria|"
                r"cut\s*off|fee\s*structure)\b")),

    ("placement_document", "training_placement_policy",
     re.compile(r"(?i)\b(placement|recruiter|training and placement|internship)\b")),

    ("library_document", "library_policy",
     re.compile(r"(?i)\b(library|knowledge resource|e-?resources?|book bank)\b")),

    ("scholarship_document", "scholarship_freeship",
     re.compile(r"(?i)\b(scholarship|freeship|financial aid)\b")),

    ("hostel_document", "hostel_facility",
     re.compile(r"(?i)\bhostel\b")),

    ("research_document", "research_development_policy",
     re.compile(r"(?i)\b(research|consultancy|patent|publication|r\s*&\s*d)\b")),

    ("examination_document", "exam_structure_current",
     re.compile(r"(?i)\b(examination|exam\s*cell|revaluation|result|hall\s*ticket)\b")),

    ("academic_document", "teaching_learning_process",
     re.compile(r"(?i)\b(academic|curriculum|syllabus|time\s*table|calendar|"
                r"roll\s*call|aec)\b")),

    ("development_plan", "teaching_learning_process",
     re.compile(r"(?i)\b(development plan|strategic plan|eight point|8\s*point)\b")),
]

# Many documents have a title that says nothing on its own -- "Overall",
# "Team Members 2023-24", "Download Form" -- while the URL path states exactly what
# they are. These patterns run against the path only, after the title-based table
# above has failed, because the path is the site's own filing system.
PATH_ROUTES: list[tuple[str, str, re.Pattern]] = [
    ("ranking_report", "qms_iqac",
     re.compile(r"(?i)/(nirf|ariia)|affiliation.{0,3}&.{0,3}accredition/.*"
                r"(engg|engineering|overall|innovation|sdg)")),

    ("accreditation_document", "qms_iqac",
     re.compile(r"(?i)/(affiliation|accredition|accreditation|naac|nba)")),

    ("alumni_document", "industry_institute_interaction",
     re.compile(r"(?i)/alumni/")),

    ("library_document", "library_policy",
     re.compile(r"(?i)/library/")),

    ("transcript_document", "student_section_certificates",
     re.compile(r"(?i)/transcripts?/")),

    ("admission_document", "admission_process",
     re.compile(r"(?i)/(admission|admissions)[_+\-0-9]*/")),

    ("placement_document", "training_placement_policy",
     re.compile(r"(?i)/(placement|placements|internship)/")),

    ("examination_document", "exam_structure_current",
     re.compile(r"(?i)/(exam|examination)[_+\-0-9]*/")),

    ("academic_document", "teaching_learning_process",
     re.compile(r"(?i)/(academics|academic)/")),

    ("research_document", "research_development_policy",
     re.compile(r"(?i)/(research|consultancy|patents?)/")),
]


def classify_document(*, title: str | None, url: str,
                      discovered_via: list | None = None) -> dict:
    """Return {source_type, parent_policy_id, matched_on} or a review verdict.

    Matching runs over the title, the filename and the documents-page section the
    link was found under -- the section is often the most reliable signal, because
    the site groups by purpose even when a filename does not say so.
    """
    section_hints = " ".join(
        f"{v.get('department','')} {v.get('category','')}"
        for v in (discovered_via or []) if isinstance(v, dict))
    haystack = f"{title or ''} {filename_of(url)} {section_hints}"

    for source_type, parent, pattern in ROUTES:
        m = pattern.search(haystack)
        if m:
            return {"source_type": source_type, "parent_policy_id": parent,
                    "matched_on": m.group(0), "matched_by": "title"}

    # Fall back to the URL path, which is the site's own filing system and is often
    # far more specific than a link's visible text.
    path = up.unquote(up.urlsplit(url).path)
    for source_type, parent, pattern in PATH_ROUTES:
        m = pattern.search(path)
        if m:
            return {"source_type": source_type, "parent_policy_id": parent,
                    "matched_on": m.group(0), "matched_by": "url_path"}

    return {"source_type": None, "parent_policy_id": None, "matched_on": None,
            "reason": "no routing rule matched; will not guess a section"}


def ranking_metadata(title: str | None, url: str) -> dict:
    """The only facts read out of a ranking report, per the document-level-only rule.

    NIRF and ARIIA submissions are statistical tables; mining them is out of scope.
    The year and category are taken from the title, which states both explicitly.
    """
    text = f"{title or ''} {filename_of(url)}"
    out: dict[str, object] = {}

    body = re.search(r"(?i)\b(nirf|ariia)\b", text)
    if body:
        out["ranking_body"] = body.group(1).upper()

    year = re.search(r"\b(20\d{2})\b", text)
    if year:
        out["report_year"] = int(year.group(1))

    category = re.search(r"(?i)\b(engineering|innovation|overall|management|"
                         r"pharmacy|architecture)\b", text)
    if category:
        out["ranking_category"] = category.group(1).title()

    out["extraction_method"] = (
        "document-level only: title and cover confirmed; statistical tables not mined")
    return out

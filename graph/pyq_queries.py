"""Deterministic, parameterized Cypher for the PYQ graph.

Same house rules as graph/faculty_queries.py: no query is ever built by string
interpolation, and none is LLM-generated. The eventual LLM layer's job is to
turn a student's sentence into the *filters* below, never into Cypher.

Every search returns the Drive URL alongside the paper, because a link is the
entire point of this subgraph.
"""
from graph.neo4j_driver import run_query

# One filter query covering every question shape in scope. Each filter is
# skipped when its parameter is null, so "all DBMS papers", "all ISE papers"
# and "DBMS 2024 ISE" are the same query with different parameters.
#
# The year filter deliberately matches three ways: a student saying "2024" may
# mean calendar 2024 (exam_year) or academic 2024-25, and both readings should
# find the paper rather than silently returning nothing.
FIND_PYQ = """
MATCH (p:PYQ)-[r:STORED_IN]->(f:PYQFile)
WHERE ($subject_key   IS NULL OR p.subject_key = $subject_key)
  AND ($exam_type     IS NULL OR p.exam_type = $exam_type)
  AND ($semester      IS NULL OR p.semester = $semester)
  AND ($year_of_study IS NULL OR p.year_of_study = $year_of_study)
  AND ($category      IS NULL OR p.course_category = $category)
  AND ($variant       IS NULL OR p.variant = $variant)
  AND ($year          IS NULL
       OR p.exam_year = $year
       OR p.academic_year STARTS WITH toString($year)
       OR p.academic_year ENDS WITH right(toString($year), 2))
RETURN p.pyq_id        AS pyq_id,
       p.title         AS title,
       p.subject       AS subject,
       p.subject_key   AS subject_key,
       p.subject_status AS subject_status,
       p.exam_type     AS exam_type,
       p.academic_year AS academic_year,
       p.exam_year     AS exam_year,
       p.semester      AS semester,
       p.year_of_study AS year_of_study,
       p.course_category AS course_category,
       p.variant       AS variant,
       f.drive_url     AS drive_url,
       f.file_name     AS file_name,
       r.page_label    AS page_label
ORDER BY p.exam_year DESC, p.subject, p.variant, r.part_index
LIMIT $limit
"""

FIND_BY_SUBJECT_TEXT = """
MATCH (s:Subject)
WHERE toLower(s.name) CONTAINS toLower($text)
   OR any(a IN coalesce(s.aliases, []) WHERE toLower(a) = toLower($text))
RETURN s.subject_key AS subject_key, s.name AS name
LIMIT $limit
"""

ALL_SUBJECTS = """
MATCH (s:Subject)<-[:FOR_SUBJECT]-(p:PYQ)
RETURN s.subject_key AS subject_key, s.name AS name,
       coalesce(s.aliases, []) AS aliases, count(p) AS paper_count
ORDER BY s.name
"""

DISTINCT_FILTER_VALUES = """
MATCH (p:PYQ)
RETURN collect(DISTINCT p.exam_type)     AS exam_types,
       collect(DISTINCT p.academic_year) AS academic_years,
       collect(DISTINCT p.exam_year)     AS exam_years,
       collect(DISTINCT p.semester)      AS semesters,
       collect(DISTINCT p.year_of_study) AS years_of_study
"""

UNRESOLVED_SUBJECTS = """
MATCH (p:PYQ)-[:STORED_IN]->(f:PYQFile)
WHERE p.subject_status = 'unresolved'
RETURN p.subject_raw AS subject_raw, count(DISTINCT p) AS papers,
       collect(DISTINCT f.file_name)[0..5] AS example_files
ORDER BY papers DESC, subject_raw
"""

MULTI_PAPER_FILES = """
MATCH (f:PYQFile)<-[:STORED_IN]-(p:PYQ)
WITH f, collect(p.title) AS titles, count(p) AS papers
WHERE papers > 1
RETURN f.file_name AS file_name, f.drive_url AS drive_url,
       papers, titles
ORDER BY papers DESC, file_name
"""

MULTI_FILE_PAPERS = """
MATCH (p:PYQ)-[:STORED_IN]->(f:PYQFile)
WITH p, collect(f.file_name) AS files, count(f) AS file_count
WHERE file_count > 1
RETURN p.pyq_id AS pyq_id, p.title AS title, file_count, files
ORDER BY file_count DESC, title
"""


def find_pyq(subject_key: str | None = None, exam_type: str | None = "ISE",
             year: int | None = None, semester: int | None = None,
             year_of_study: str | None = None, category: str | None = None,
             variant: str | None = None, limit: int = 50) -> list[dict]:
    """The single entry point the future query layer calls.

    exam_type defaults to "ISE" rather than None so a caller that forgets to
    set it cannot accidentally hand a student an ESE paper once phase 2 lands.
    """
    return run_query(FIND_PYQ, {
        "subject_key": subject_key, "exam_type": exam_type, "year": year,
        "semester": semester, "year_of_study": year_of_study,
        "category": category, "variant": variant, "limit": limit,
    })


def resolve_subject_text(text: str, limit: int = 5) -> list[dict]:
    """Map a student's wording ('database management') to a subject_key."""
    return run_query(FIND_BY_SUBJECT_TEXT, {"text": text, "limit": limit})


def all_subjects() -> list[dict]:
    """The vocabulary, read out of the graph -- the pattern
    services/faculty_service._build_index() already uses for faculty."""
    return run_query(ALL_SUBJECTS)


def filter_values() -> dict:
    rows = run_query(DISTINCT_FILTER_VALUES)
    return rows[0] if rows else {}


def unresolved_subjects() -> list[dict]:
    return run_query(UNRESOLVED_SUBJECTS)


def multi_paper_files() -> list[dict]:
    return run_query(MULTI_PAPER_FILES)


def multi_file_papers() -> list[dict]:
    return run_query(MULTI_FILE_PAPERS)

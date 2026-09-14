"""Read side for the official Examination documents.

Scoped by `source_type = 'examination_calendar'` throughout, so an examination
question can never surface an Attendance, Internship, Faculty, Admission or
Placement node -- and never a PYQ question paper, which is a different system
entirely (see graph/pyq_queries.py).
"""
from graph.neo4j_driver import run_query

SOURCE_TYPE = "examination_calendar"

# Everything the answer layer needs about one document. Event arrays come back
# whole; the caller zips them if the question is about dates.
_FIELDS = """
    d.doc_id AS doc_id, d.title AS title, d.source_url AS source_url,
    d.academic_year AS academic_year, d.programmes AS programmes,
    d.levels AS levels, d.level_note AS level_note, d.terms AS terms,
    d.document_type AS document_type, d.document_status AS document_status,
    d.document_date AS document_date, d.issuing_authority AS issuing_authority,
    d.pages AS pages, d.content_note AS content_note,
    d.institution_name_in_source AS institution_name_in_source,
    d.event_terms AS event_terms, d.event_names AS event_names,
    d.event_schedules AS event_schedules, d.event_count AS event_count
"""

ALL_DOCUMENTS = f"""
MATCH (d:PolicyDocument {{source_type: $source_type}})
RETURN {_FIELDS}
ORDER BY d.academic_year DESC, d.title
"""

# Filters are all optional; a NULL filter matches everything. `any()` over the
# stored arrays is what lets one document answer for several programmes/levels,
# which matters because several of these PDFs carry more than one calendar.
FILTERED = f"""
MATCH (d:PolicyDocument {{source_type: $source_type}})
WHERE ($academic_year IS NULL OR d.academic_year = $academic_year)
  AND ($programme     IS NULL OR any(p IN d.programmes WHERE toLower(p) = toLower($programme)))
  AND ($level         IS NULL OR any(l IN d.levels     WHERE toLower(l) = toLower($level)))
  AND ($text          IS NULL OR toLower(d.title) CONTAINS toLower($text)
                              OR toLower(coalesce(d.events_text,'')) CONTAINS toLower($text))
RETURN {_FIELDS}
ORDER BY d.academic_year DESC, d.title
"""

BY_ID = f"""
MATCH (d:PolicyDocument {{doc_id: $doc_id, source_type: $source_type}})
RETURN {_FIELDS}
"""

PARENT = """
MATCH (p:Policy)-[r:REFERENCES]->(d:PolicyDocument {source_type: $source_type})
RETURN p.policy_id AS policy_id, p.name AS policy_name,
       p.status AS policy_status, count(d) AS documents
"""

YEARS = """
MATCH (d:PolicyDocument {source_type: $source_type})
RETURN d.academic_year AS academic_year, count(*) AS documents
ORDER BY academic_year DESC
"""


def all_documents() -> list[dict]:
    return run_query(ALL_DOCUMENTS, {"source_type": SOURCE_TYPE})


def find_documents(*, academic_year: str | None = None, programme: str | None = None,
                   level: str | None = None, text: str | None = None) -> list[dict]:
    return run_query(FILTERED, {
        "source_type": SOURCE_TYPE, "academic_year": academic_year,
        "programme": programme, "level": level, "text": text,
    })


def document_by_id(doc_id: str) -> dict | None:
    rows = run_query(BY_ID, {"doc_id": doc_id, "source_type": SOURCE_TYPE})
    return rows[0] if rows else None


def parent_policy() -> list[dict]:
    return run_query(PARENT, {"source_type": SOURCE_TYPE})


def academic_years() -> list[dict]:
    return run_query(YEARS, {"source_type": SOURCE_TYPE})


def events_of(row: dict) -> list[dict]:
    """Re-pair the parallel event arrays into rows."""
    terms = row.get("event_terms") or []
    names = row.get("event_names") or []
    scheds = row.get("event_schedules") or []
    return [{"term": terms[i] if i < len(terms) else None,
             "event": names[i] if i < len(names) else None,
             "schedule": scheds[i] if i < len(scheds) else None}
            for i in range(len(names))]

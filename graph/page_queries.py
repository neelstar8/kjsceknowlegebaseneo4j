"""Retrieval over knowledge extracted from official KJSCE webpages.

Students do not use the site's wording. They type "how much attendance do I need",
not "Attendance Requirement"; "FY BTech calendar", not "Academic and Examination
Calendar First Year Bachelor of Technology". So matching is fulltext over the
page's own headings, facts and table rows, with a term-coverage floor borrowed from
services/policy_service.py to stop a Lucene OR query answering anything plausibly.

Year handling is the other half. A page that names 2024-25 must never answer as
2026-27, so `academic_years` is stored per page and filtered on explicitly. When a
student names a bare year, the caller resolves it against the years the graph
actually holds rather than guessing.
"""
from graph.neo4j_driver import run_query

PAGE_FULLTEXT = "page_content_text"

ENSURE_INDEX = f"""
CREATE FULLTEXT INDEX {PAGE_FULLTEXT} IF NOT EXISTS
FOR (d:PolicyDocument)
ON EACH [d.title, d.headings_text, d.facts_text, d.table_rows_text, d.summary]
"""

_FIELDS = """
    d.doc_id AS doc_id, d.title AS title, d.source_url AS source_url,
    d.alternate_source_url AS alternate_source_url,
    d.source_type AS source_type, d.document_type AS document_type,
    d.page_section AS page_section, d.summary AS summary,
    d.headings AS headings, d.academic_years AS academic_years,
    d.latest_academic_year AS latest_academic_year,
    d.fact_headings AS fact_headings, d.fact_texts AS fact_texts,
    d.table_captions AS table_captions, d.fact_count AS fact_count,
    d.table_count AS table_count, d.alias_urls AS alias_urls
"""

SEARCH = f"""
CALL db.index.fulltext.queryNodes($index, $query) YIELD node AS d, score
WHERE d.source_type = 'webpage'
  AND ($academic_year IS NULL OR $academic_year IN d.academic_years)
  AND ($doc_type IS NULL OR d.document_type = $doc_type)
RETURN {_FIELDS}, score
ORDER BY score DESC
LIMIT $limit
"""

BY_TYPE = f"""
MATCH (d:PolicyDocument {{source_type:'webpage'}})
WHERE ($doc_type IS NULL OR d.document_type = $doc_type)
  AND ($academic_year IS NULL OR $academic_year IN d.academic_years)
RETURN {_FIELDS}
ORDER BY coalesce(d.latest_academic_year,'') DESC, d.title
LIMIT $limit
"""

YEARS_HELD = """
MATCH (d:PolicyDocument) WHERE d.academic_years IS NOT NULL
UNWIND d.academic_years AS y
RETURN y AS academic_year, count(*) AS documents
ORDER BY academic_year DESC
"""


def ensure_index() -> None:
    run_query(ENSURE_INDEX)


def search(query: str, *, academic_year=None, doc_type=None, limit=10) -> list[dict]:
    return run_query(SEARCH, {"index": PAGE_FULLTEXT, "query": query,
                              "academic_year": academic_year,
                              "doc_type": doc_type, "limit": limit})


def by_type(doc_type=None, *, academic_year=None, limit=25) -> list[dict]:
    return run_query(BY_TYPE, {"doc_type": doc_type,
                               "academic_year": academic_year, "limit": limit})


def years_held() -> list[dict]:
    return run_query(YEARS_HELD)


def facts_of(row: dict, limit: int = 8) -> list[dict]:
    heads = row.get("fact_headings") or []
    texts = row.get("fact_texts") or []
    return [{"heading": heads[i] if i < len(heads) else "", "fact": texts[i]}
            for i in range(min(len(texts), limit))]

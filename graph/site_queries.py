"""Read side for documents discovered by the site crawl.

Every query is scoped by `source_type`, so a question about placements cannot reach
admission documents, and none of them can reach faculty, PYQ or provision data.
"""
from graph.neo4j_driver import run_query

_FIELDS = """
    d.doc_id AS doc_id, d.title AS title, d.source_url AS source_url,
    d.alternate_source_url AS alternate_source_url,
    d.source_type AS source_type, d.pages AS pages,
    d.report_year AS report_year, d.ranking_body AS ranking_body,
    d.ranking_category AS ranking_category,
    d.extraction_method AS extraction_method,
    d.needs_visual_read AS needs_visual_read
"""

FIND = f"""
MATCH (d:PolicyDocument) WHERE d.source_type IN $types
  AND ($year IS NULL OR d.report_year = $year
       OR ($year IS NOT NULL AND d.title CONTAINS toString($year)))
RETURN {_FIELDS}
ORDER BY coalesce(d.report_year, 0) DESC, d.title
"""

BY_PARENT = f"""
MATCH (p:Policy {{policy_id: $policy_id}})-[:REFERENCES]->(d:PolicyDocument)
WHERE d.discovered_by = 'site_crawl'
RETURN {_FIELDS}
ORDER BY d.source_type, d.title
"""

FAMILIES = """
MATCH (d:PolicyDocument) WHERE d.discovered_by = 'site_crawl'
RETURN d.source_type AS source_type, count(*) AS documents
ORDER BY documents DESC
"""


def find(types: list[str], *, year: int | None = None) -> list[dict]:
    return run_query(FIND, {"types": types, "year": year})


def by_parent(policy_id: str) -> list[dict]:
    return run_query(BY_PARENT, {"policy_id": policy_id})


def families() -> list[dict]:
    return run_query(FAMILIES)

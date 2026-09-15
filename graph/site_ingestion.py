"""Writing crawl-discovered documents into the existing graph.

Same shape as `graph/exam_ingestion.py` and `graph/academics_ingestion.py`, because
this is the same kind of thing: an official PDF hung off a policy that already
exists. No new labels, no new relationship types, no new constraints.

    (:Policy {policy_id: <existing parent>})-[:REFERENCES]->(:PolicyDocument)

Three things this module adds over its two predecessors, all of them because a
site-wide crawl is riskier than a hand-curated section:

  * `ingest_batch_id` on every node it creates, so one bad run can be reverted
    precisely without touching anything a previous run wrote.
  * `record_alternate_url()` is applied to documents the crawl re-found under a
    second URL, rather than creating a second node -- the case proven by the
    Strategic Plan appearing under both /About/ and /documents/.
  * It refuses to write a document whose parent policy is not already present, the
    same refusal both predecessors enforce.
"""
from __future__ import annotations

from graph.neo4j_driver import run_query

#: Every source_type this module is allowed to write. A value outside this list is a
#: routing bug, not a new category, so the ingest fails rather than inventing one.
SOURCE_TYPES = [
    "ranking_report", "accreditation_document", "mandatory_disclosure",
    "admission_document", "placement_document", "library_document",
    "scholarship_document", "hostel_document", "research_document",
    "examination_document", "academic_document", "development_plan",
]

RELATION = "official_site_document"

UPSERT_DOCUMENT = """
MERGE (d:PolicyDocument {doc_id: $doc_id})
ON CREATE SET d.first_seen_at = $now, d._created = true,
              d.ingest_batch_id = $batch_id
SET d += $props, d.last_seen_at = $now
WITH d, coalesce(d._created, false) AS created
REMOVE d._created
RETURN created
"""

LINK_TO_PARENT = """
MATCH (p:Policy {policy_id: $policy_id})
MATCH (d:PolicyDocument {doc_id: $doc_id})
MERGE (p)-[r:REFERENCES]->(d)
ON CREATE SET r.created_at = $now, r.ingest_batch_id = $batch_id
SET r.relation = $relation
RETURN count(r) AS linked
"""

RECORD_ALTERNATE_URL = """
MATCH (d:PolicyDocument {doc_id: $doc_id})
SET d.alternate_source_url = $alternate_source_url,
    d.also_published_under = $also_published_under,
    d.last_seen_at = $now
RETURN d.doc_id AS doc_id, d.source_url AS source_url,
       d.alternate_source_url AS alternate_source_url
"""

COUNTS = """
MATCH (d:PolicyDocument) WHERE d.source_type IN $source_types
WITH count(d) AS site_documents
MATCH (:Policy)-[r:REFERENCES {relation: $relation}]->(:PolicyDocument)
RETURN site_documents, count(r) AS site_links
"""

BATCH_ROLLBACK_PREVIEW = """
MATCH (d:PolicyDocument {ingest_batch_id: $batch_id})
RETURN count(d) AS nodes, collect(d.doc_id)[..25] AS sample
"""


def parent_exists(policy_id: str) -> bool:
    rows = run_query("MATCH (p:Policy {policy_id: $policy_id}) RETURN count(p) AS c",
                     {"policy_id": policy_id})
    return bool(rows and rows[0]["c"])


def document_props(doc: dict) -> dict:
    """Only primitives and arrays of primitives; nulls dropped so a sparse re-run
    never blanks a richer existing value."""
    props = {k: v for k, v in doc.items() if k != "doc_id"}
    return {k: v for k, v in props.items() if v is not None}


def upsert_document(doc_id: str, props: dict, now: str, batch_id: str) -> bool:
    rows = run_query(UPSERT_DOCUMENT, {"doc_id": doc_id, "props": props,
                                       "now": now, "batch_id": batch_id})
    return bool(rows and rows[0]["created"])


def link_document(doc_id: str, policy_id: str, now: str, batch_id: str) -> int:
    rows = run_query(LINK_TO_PARENT, {"policy_id": policy_id, "doc_id": doc_id,
                                      "now": now, "batch_id": batch_id,
                                      "relation": RELATION})
    return rows[0]["linked"] if rows else 0


def record_alternate_url(doc_id: str, alternate_source_url: str, now: str,
                         also_published_under: str = "official KJSCE site crawl") -> dict:
    rows = run_query(RECORD_ALTERNATE_URL, {
        "doc_id": doc_id, "alternate_source_url": alternate_source_url,
        "also_published_under": also_published_under, "now": now})
    return rows[0] if rows else {}


def counts() -> dict:
    rows = run_query(COUNTS, {"source_types": SOURCE_TYPES, "relation": RELATION})
    return rows[0] if rows else {}


def rollback_preview(batch_id: str) -> dict:
    """What a rollback of this batch would remove. Read-only."""
    rows = run_query(BATCH_ROLLBACK_PREVIEW, {"batch_id": batch_id})
    return rows[0] if rows else {"nodes": 0, "sample": []}

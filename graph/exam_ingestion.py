"""Upserts the official Examination documents (academic & examination calendars).

Graph shape -- no new labels, no new relationship types, no schema change:

    (:Policy {policy_id: 'exam_structure_current'})-[:REFERENCES]->(:PolicyDocument)

`PolicyDocument` is the label the handbook pipeline already uses for "a PDF we
fetched", and `doc_id` is already unique-constrained, so re-running this updates
rather than duplicates. The documents are distinguished from handbook chapters by
`source_type = 'examination_calendar'`, the same way the existing corpus already
distinguishes 'handbook_chapter' from 'official_site_supplement'.

Why REFERENCES and not DOCUMENTED_IN: in this graph `DOCUMENTED_IN` asserts that
a policy's *text lives in* that PDF, and carries the page range where it can be
read. A calendar does not contain the examination policy -- it is a separate
official document the examination area publishes. REFERENCES (already used by
Policy for Scheme, Committee, Programme, Portal, ...) says "the examination
knowledge area points at this document" without making the stronger claim.

Why the calendars are not PolicyProvisions: none of these 16 PDFs states a rule,
ordinance, eligibility condition or penalty. They are schedules. Turning a dated
schedule into a permanent provision would make "ESE is 18 November to 8 December"
look like standing policy, which it is not -- it is one term of one year. Dates
are therefore held on the document that published them, as parallel arrays, the
same shape `flatten_numbers()` uses in the handbook ingest because Neo4j cannot
store a list of maps on a property.
"""
from graph.neo4j_driver import run_query

# The existing Examination knowledge node the documents hang from.
EXAM_POLICY_ID = "exam_structure_current"

SOURCE_TYPE = "examination_calendar"

# List properties are written through `SET d += $props`, so the shape of the
# document node is whatever the knowledge file says plus these bookkeeping
# fields. Nothing is deleted.
UPSERT_DOCUMENT = """
MERGE (d:PolicyDocument {doc_id: $doc_id})
ON CREATE SET d.first_seen_at = $now, d._created = true
SET d += $props, d.last_seen_at = $now
WITH d, coalesce(d._created, false) AS created
REMOVE d._created
RETURN created
"""

LINK_TO_EXAM_POLICY = """
MATCH (p:Policy {policy_id: $policy_id})
MATCH (d:PolicyDocument {doc_id: $doc_id})
MERGE (p)-[r:REFERENCES]->(d)
ON CREATE SET r.created_at = $now
SET r.relation = 'official_examination_document'
RETURN count(r) AS linked
"""

COUNTS = """
MATCH (d:PolicyDocument {source_type: $source_type})
WITH count(d) AS exam_documents
MATCH (:Policy {policy_id: $policy_id})-[r:REFERENCES]->(:PolicyDocument {source_type: $source_type})
RETURN exam_documents, count(r) AS exam_document_links
"""


def flatten_events(events: list[dict]) -> dict:
    """Events become three parallel arrays plus one searchable string.

    Parallel arrays because Neo4j cannot hold a list of maps on a property --
    the same reason graph/policy_ingestion.py flattens numbers. The joined
    `events_text` exists so a question like "when is the ESE in the 2026-27
    calendar" can match on text without re-reading the PDF.
    """
    if not events:
        return {"event_terms": [], "event_names": [], "event_schedules": [],
                "events_text": "", "event_count": 0}
    return {
        "event_terms": [e["term"] for e in events],
        "event_names": [e["event"] for e in events],
        "event_schedules": [e["schedule"] for e in events],
        "events_text": " | ".join(f"{e['term']}: {e['event']} - {e['schedule']}"
                                  for e in events),
        "event_count": len(events),
    }


def document_props(doc: dict, meta: dict) -> dict:
    """Everything the knowledge file says about one PDF, flattened for Neo4j."""
    props = {k: v for k, v in doc.items() if k not in ("events", "doc_id")}
    props.update(flatten_events(doc.get("events") or []))
    props.update({
        "source_type": SOURCE_TYPE,
        "institution": meta["institution"],
        "source_page": meta["source_page"],
        "source_section": meta["source_section"],
        "knowledge_version": meta["knowledge_version"],
    })
    # Drop nulls: a missing issuing authority should be an absent property,
    # not a property whose value is None.
    return {k: v for k, v in props.items() if v is not None}


def upsert_document(doc_id: str, props: dict, now: str) -> bool:
    rows = run_query(UPSERT_DOCUMENT, {"doc_id": doc_id, "props": props, "now": now})
    return bool(rows and rows[0]["created"])


def link_document(doc_id: str, now: str, policy_id: str = EXAM_POLICY_ID) -> int:
    rows = run_query(LINK_TO_EXAM_POLICY,
                     {"policy_id": policy_id, "doc_id": doc_id, "now": now})
    return rows[0]["linked"] if rows else 0


def exam_policy_exists(policy_id: str = EXAM_POLICY_ID) -> bool:
    rows = run_query("MATCH (p:Policy {policy_id: $policy_id}) RETURN count(p) AS c",
                     {"policy_id": policy_id})
    return bool(rows and rows[0]["c"])


def counts(policy_id: str = EXAM_POLICY_ID) -> dict:
    rows = run_query(COUNTS, {"source_type": SOURCE_TYPE, "policy_id": policy_id})
    return rows[0] if rows else {}

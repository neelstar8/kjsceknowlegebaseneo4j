"""Upserts the official Academics documents from the KJSCE documents page.

Graph shape -- no new labels, no new relationship types, no schema change:

    (:Policy {policy_id: 'teaching_learning_process'})-[:REFERENCES]->(:PolicyDocument)

This mirrors graph/exam_ingestion.py exactly. `PolicyDocument` is the label the
handbook pipeline already uses for "a PDF we fetched" and `doc_id` is already
unique-constrained, which is what makes the ingest rerunnable. Academics
documents are told apart from handbook chapters and examination calendars by
`source_type`, the same discriminator the existing corpus already uses:

    academic_calendar        the six AEC / schedule documents
    class_timetable_index    the Class Time Table link hub
    syllabus_index           the Syllabus link hub
    roll_call_index          the Roll Call List link hub
    academic_development_plan  the 8 Point Development Plan
    strategic_plan           the KJSSE Strategic Plan 2025-2030
    software_resource        the MATLAB portal (an external page, not a PDF)

Why `teaching_learning_process` is the parent: it is the existing academic
policy in the graph (current, 13 provisions, in the academic_quality_policy
category). Inventing an empty "Academics" node purely to hold PDFs is what this
ingest must not do, exactly as the examination ingest hangs its documents from
the existing `exam_structure_current` policy.

Why REFERENCES and not DOCUMENTED_IN: `DOCUMENTED_IN` asserts that a policy's
*text lives in* that PDF and carries the page range where it can be read. A
calendar, a timetable index or a strategic plan does not contain the teaching-
learning policy, so the weaker, already-existing REFERENCES edge is the honest one.

Why no PolicyProvisions: none of these resources states a rule, ordinance,
penalty or eligibility condition. Calendar dates belong to the calendar that
published them; strategic-plan goals are institutional intentions; the 8 Point
Plan's 43 entries are measurement parameters. Turning any of them into a
provision would make them read as standing student rules, which they are not.

Why list-valued properties rather than child nodes: Neo4j cannot store a list of
maps on a property, so events, branch links, plan sections and strategic goals
are held as parallel arrays plus one searchable string each -- the same shape
`flatten_numbers()` uses in the handbook ingest and `flatten_events()` uses for
examination calendars. This keeps the schema untouched. Per-goal nodes would be
a purely additive change later if retrieval ever needs them.
"""
from graph.neo4j_driver import run_query

ACADEMIC_PARENT_ID = "teaching_learning_process"

SOURCE_TYPES = [
    "academic_calendar", "class_timetable_index", "syllabus_index",
    "roll_call_index", "academic_development_plan", "strategic_plan",
    "software_resource",
]

# Keys that are structure in the knowledge file, not node properties: each has a
# flattened array form written alongside it.
NON_PROPERTY_KEYS = {"events", "branch_links", "sections", "goals"}

UPSERT_DOCUMENT = """
MERGE (d:PolicyDocument {doc_id: $doc_id})
ON CREATE SET d.first_seen_at = $now, d._created = true
SET d += $props, d.last_seen_at = $now
WITH d, coalesce(d._created, false) AS created
REMOVE d._created
RETURN created
"""

LINK_TO_PARENT = """
MATCH (p:Policy {policy_id: $policy_id})
MATCH (d:PolicyDocument {doc_id: $doc_id})
MERGE (p)-[r:REFERENCES]->(d)
ON CREATE SET r.created_at = $now
SET r.relation = 'official_academic_document'
RETURN count(r) AS linked
"""

# The Academics section republishes one examination calendar under a second URL.
# The node is reused; the alternate URL is recorded on it rather than cloned.
RECORD_ALTERNATE_URL = """
MATCH (d:PolicyDocument {doc_id: $doc_id})
SET d.alternate_source_url = $alternate_source_url,
    d.also_published_under = 'Academics > Academic and Examination Calendar',
    d.last_seen_at = $now
RETURN d.doc_id AS doc_id, d.source_url AS source_url
"""

COUNTS = """
MATCH (d:PolicyDocument) WHERE d.source_type IN $source_types
WITH count(d) AS academics_documents
MATCH (:Policy {policy_id: $policy_id})-[r:REFERENCES]->(d2:PolicyDocument)
RETURN academics_documents, count(r) AS academics_links
"""


def _flatten(doc: dict) -> dict:
    """Turn the list-of-maps structures into parallel arrays Neo4j can store."""
    out = {}
    for branch in (doc.get("branch_links") or []):
        pass  # branch arrays are already written by the builder
    sections = doc.get("sections") or []
    if sections:
        out["section_details"] = [
            f"{s['number']}. {s['name']} (parameters {s['parameter_range']}): "
            + "; ".join(s["parameters"]) for s in sections]
    goals = doc.get("goals") or []
    if goals:
        out["goal_details"] = [
            f"{g['number']}. {g['name']}: {g['development_agenda']}" for g in goals]
    return out


def document_props(doc: dict, meta: dict) -> dict:
    props = {k: v for k, v in doc.items()
             if k not in NON_PROPERTY_KEYS and k != "doc_id"}
    props.update(_flatten(doc))
    props.update({
        "institution": meta["institution"],
        "source_page": meta["source_page"],
        "source_section": meta["source_section"],
        "knowledge_version": meta["knowledge_version"],
    })
    return {k: v for k, v in props.items() if v is not None}


def upsert_document(doc_id: str, props: dict, now: str) -> bool:
    rows = run_query(UPSERT_DOCUMENT, {"doc_id": doc_id, "props": props, "now": now})
    return bool(rows and rows[0]["created"])


def link_document(doc_id: str, now: str, policy_id: str = ACADEMIC_PARENT_ID) -> int:
    rows = run_query(LINK_TO_PARENT,
                     {"policy_id": policy_id, "doc_id": doc_id, "now": now})
    return rows[0]["linked"] if rows else 0


def record_alternate_url(doc_id: str, alternate_source_url: str, now: str) -> dict:
    rows = run_query(RECORD_ALTERNATE_URL, {
        "doc_id": doc_id, "alternate_source_url": alternate_source_url, "now": now})
    return rows[0] if rows else {}


def parent_exists(policy_id: str = ACADEMIC_PARENT_ID) -> bool:
    rows = run_query("MATCH (p:Policy {policy_id: $policy_id}) RETURN count(p) AS c",
                     {"policy_id": policy_id})
    return bool(rows and rows[0]["c"])


def document_exists(doc_id: str) -> bool:
    rows = run_query("MATCH (d:PolicyDocument {doc_id: $doc_id}) RETURN count(d) AS c",
                     {"doc_id": doc_id})
    return bool(rows and rows[0]["c"])


def counts(policy_id: str = ACADEMIC_PARENT_ID) -> dict:
    rows = run_query(COUNTS, {"source_types": SOURCE_TYPES, "policy_id": policy_id})
    return rows[0] if rows else {}

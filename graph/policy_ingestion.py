"""Upserts KJSIT Institute Policy Handbook knowledge into Neo4j.

Graph shape:

    (:PolicyHandbook)-[:HAS_CATEGORY]->(:PolicyCategory)
    (:Policy)-[:BELONGS_TO]->(:PolicyCategory)
    (:Policy)-[:DOCUMENTED_IN {page_start, page_end, section}]->(:PolicyDocument)
    (:Policy)-[:DEFINES|SPECIFIES]->(:PolicyProvision)
    (:PolicyProvision)-[:SOURCED_FROM {page, section, subsection}]->(:PolicyDocument)
    (:Policy)-[:APPLIES_TO]->(:StudentCategory|:Programme|:Department)
    (:Policy)-[:INVOLVES]->(:Department|:Committee)
    (:PolicyProvision)-[:REQUIRES]->(:Form)
    (:PolicyProvision)-[:USES]->(:Portal)
    (:Role)-[:RESPONSIBLE_FOR]->(:Policy|:PolicyProvision)
    (:Committee)-[:APPROVES]->(:PolicyProvision)
    (:PolicyProvision)-[:HAS_CONSEQUENCE|HAS_EXCEPTION]->(:PolicyProvision)
    (:Policy)-[:REFERENCES]->(:Policy|:ExternalOrganization)
    (:Policy)-[:SUPERSEDED_BY]->(:Policy)

Three levels, on purpose:

  PolicyDocument  the physical PDF that was fetched -- one row per file, with
                  its URL, page count and checksum. Never holds page text.
  Policy          the logical policy (a handbook chapter or a numbered section
                  inside one). What a student names when they ask a question.
  PolicyProvision one atomic normative statement -- a rule, a fee, a deadline,
                  a penalty. This is the unit that carries page-level
                  provenance, because "75% attendance" is only trustworthy if
                  the graph can say which page of which PDF said so.

Identity is deterministic everywhere (`policy_id`, `provision_id`,
`doc_id`, `*_key`) and unique-constrained, so re-running the ingest updates
rather than duplicates. This module never deletes anything.

Institution scope: every node carries `institution`. The handbook is a KJSIT
(formerly KJSIEIT) document; nothing here may be read as applying to KJSSE.
"""
from graph.neo4j_driver import run_query

# Entity labels that are addressed by a single `entity_key` property. Keeping
# them in one allow-list means the upsert can stay generic without ever letting
# a typo in the knowledge file invent a new label.
ENTITY_LABELS = [
    "Department", "Committee", "Role", "Programme", "StudentCategory",
    "Form", "Portal", "Facility", "ExternalOrganization", "Scheme",
]

CONSTRAINTS = [
    "CREATE CONSTRAINT policy_handbook_key_unique IF NOT EXISTS "
    "FOR (h:PolicyHandbook) REQUIRE h.handbook_key IS UNIQUE",
    "CREATE CONSTRAINT policy_category_key_unique IF NOT EXISTS "
    "FOR (c:PolicyCategory) REQUIRE c.category_key IS UNIQUE",
    "CREATE CONSTRAINT policy_document_id_unique IF NOT EXISTS "
    "FOR (d:PolicyDocument) REQUIRE d.doc_id IS UNIQUE",
    "CREATE CONSTRAINT policy_id_unique IF NOT EXISTS "
    "FOR (p:Policy) REQUIRE p.policy_id IS UNIQUE",
    "CREATE CONSTRAINT policy_provision_id_unique IF NOT EXISTS "
    "FOR (v:PolicyProvision) REQUIRE v.provision_id IS UNIQUE",
] + [
    f"CREATE CONSTRAINT {label.lower()}_entity_key_unique IF NOT EXISTS "
    f"FOR (e:{label}) REQUIRE e.entity_key IS UNIQUE"
    for label in ENTITY_LABELS
]

INDEXES = [
    "CREATE INDEX policy_category_key IF NOT EXISTS FOR (p:Policy) ON (p.category_key)",
    "CREATE INDEX policy_status IF NOT EXISTS FOR (p:Policy) ON (p.status)",
    "CREATE INDEX policy_institution IF NOT EXISTS FOR (p:Policy) ON (p.institution)",
    "CREATE INDEX policy_provision_kind IF NOT EXISTS FOR (v:PolicyProvision) ON (v.kind)",
    "CREATE INDEX policy_provision_policy IF NOT EXISTS FOR (v:PolicyProvision) ON (v.policy_id)",
    "CREATE INDEX policy_provision_topic IF NOT EXISTS FOR (v:PolicyProvision) ON (v.topic)",
    "CREATE FULLTEXT INDEX policy_provision_text IF NOT EXISTS "
    "FOR (v:PolicyProvision) ON EACH [v.text, v.topic]",
    "CREATE FULLTEXT INDEX policy_name_text IF NOT EXISTS "
    "FOR (p:Policy) ON EACH [p.name, p.aliases_text]",
]

HANDBOOK_QUERY = """
MERGE (h:PolicyHandbook {handbook_key: $handbook_key})
  ON CREATE SET h.first_seen_at = $now
SET h += $props, h.ingested_at = $now
RETURN h.handbook_key AS key
"""

CATEGORY_QUERY = """
MERGE (c:PolicyCategory {category_key: $category_key})
  ON CREATE SET c._created = true, c.first_seen_at = $now
SET c += $props, c.ingested_at = $now
WITH c, coalesce(c._created, false) AS created
REMOVE c._created
WITH c, created
MATCH (h:PolicyHandbook {handbook_key: $handbook_key})
MERGE (h)-[:HAS_CATEGORY]->(c)
RETURN created
"""

DOCUMENT_QUERY = """
MERGE (d:PolicyDocument {doc_id: $doc_id})
  ON CREATE SET d._created = true, d.first_seen_at = $now
SET d += $props, d.last_seen_at = $now
WITH d, coalesce(d._created, false) AS created
REMOVE d._created
RETURN created
"""

POLICY_QUERY = """
MERGE (p:Policy {policy_id: $policy_id})
  ON CREATE SET p._created = true, p.first_seen_at = $now
SET p += $props, p.ingested_at = $now
WITH p, coalesce(p._created, false) AS created
REMOVE p._created
WITH p, created
MATCH (c:PolicyCategory {category_key: $category_key})
MERGE (p)-[:BELONGS_TO]->(c)
WITH p, created
MATCH (d:PolicyDocument {doc_id: $doc_id})
MERGE (p)-[r:DOCUMENTED_IN]->(d)
SET r += $doc_edge
RETURN created
"""

# DEFINES vs SPECIFIES is a pure function of the provision kind, so the
# knowledge file never has to state the edge type and can never contradict it.
PROVISION_QUERY = """
MERGE (v:PolicyProvision {provision_id: $provision_id})
  ON CREATE SET v._created = true, v.first_seen_at = $now
SET v += $props, v.ingested_at = $now
WITH v, coalesce(v._created, false) AS created
REMOVE v._created
WITH v, created
MATCH (p:Policy {policy_id: $policy_id})
FOREACH (_ IN CASE WHEN $edge = 'DEFINES' THEN [1] ELSE [] END |
    MERGE (p)-[:DEFINES]->(v))
FOREACH (_ IN CASE WHEN $edge = 'SPECIFIES' THEN [1] ELSE [] END |
    MERGE (p)-[:SPECIFIES]->(v))
WITH v, created
MATCH (d:PolicyDocument {doc_id: $doc_id})
MERGE (v)-[s:SOURCED_FROM]->(d)
SET s += $source_edge
RETURN created
"""

ENTITY_QUERY = """
MERGE (e:%(label)s {entity_key: $entity_key})
  ON CREATE SET e._created = true, e.first_seen_at = $now
SET e += $props, e.ingested_at = $now
WITH e, coalesce(e._created, false) AS created
REMOVE e._created
RETURN created
"""

# Relationship type and both endpoint labels are validated by the caller against
# fixed allow-lists before they ever reach this string, so no user-controlled
# text is interpolated into Cypher.
LINK_QUERY = """
MATCH (a:%(from_label)s {%(from_key)s: $from_id})
MATCH (b:%(to_label)s {%(to_key)s: $to_id})
MERGE (a)-[r:%(rel)s]->(b)
SET r += $props
RETURN count(r) AS linked
"""

KEY_PROPERTY = {
    "PolicyHandbook": "handbook_key",
    "PolicyCategory": "category_key",
    "PolicyDocument": "doc_id",
    "Policy": "policy_id",
    "PolicyProvision": "provision_id",
}
for _label in ENTITY_LABELS:
    KEY_PROPERTY[_label] = "entity_key"

RELATIONSHIP_TYPES = {
    "APPLIES_TO", "INVOLVES", "REQUIRES", "USES", "RESPONSIBLE_FOR",
    "APPROVES", "HAS_CONSEQUENCE", "HAS_EXCEPTION", "REFERENCES",
    "SUPERSEDED_BY", "HAS_MEMBER_ROLE", "PROVIDES", "ESCALATES_TO",
}

DEFINES_KINDS = {
    "rule", "requirement", "definition", "eligibility", "fee", "penalty",
    "exception", "responsibility", "contact", "numeric",
}
SPECIFIES_KINDS = {"procedure", "timeline", "process"}

COUNT_QUERIES = {
    "policy_handbook": "MATCH (n:PolicyHandbook) RETURN count(n) AS count",
    "policy_category": "MATCH (n:PolicyCategory) RETURN count(n) AS count",
    "policy_document": "MATCH (n:PolicyDocument) RETURN count(n) AS count",
    "policy": "MATCH (n:Policy) RETURN count(n) AS count",
    "policy_provision": "MATCH (n:PolicyProvision) RETURN count(n) AS count",
    "faculty_member": "MATCH (n:FacultyMember) RETURN count(n) AS count",
    "pyq": "MATCH (n:PYQ) RETURN count(n) AS count",
}


def edge_for_kind(kind: str) -> str:
    """Rules are DEFINED by a policy; procedures are SPECIFIED by it."""
    if kind in SPECIFIES_KINDS:
        return "SPECIFIES"
    if kind in DEFINES_KINDS:
        return "DEFINES"
    raise ValueError(f"unknown provision kind: {kind!r}")


def strip_empty(props: dict) -> dict:
    """Drop empty values so a sparse record never nulls out good data.

    Same contract as graph/faculty_ingestion.py and graph/pyq_ingestion.py.
    """
    return {k: v for k, v in props.items()
            if v is not None and v != "" and v != [] and v != {}}


def ensure_schema():
    """Create constraints and indexes. Safe to call on every run."""
    for statement in CONSTRAINTS + INDEXES:
        run_query(statement)


def upsert_handbook(*, handbook_key, props, now):
    run_query(HANDBOOK_QUERY, {"handbook_key": handbook_key,
                               "props": strip_empty(props), "now": now})


def upsert_category(*, category_key, handbook_key, props, now) -> bool:
    rows = run_query(CATEGORY_QUERY, {
        "category_key": category_key, "handbook_key": handbook_key,
        "props": strip_empty(props), "now": now})
    return bool(rows and rows[0]["created"])


def upsert_document(*, doc_id, props, now) -> bool:
    rows = run_query(DOCUMENT_QUERY, {"doc_id": doc_id,
                                      "props": strip_empty(props), "now": now})
    return bool(rows and rows[0]["created"])


def upsert_policy(*, policy_id, category_key, doc_id, props, doc_edge, now) -> bool:
    rows = run_query(POLICY_QUERY, {
        "policy_id": policy_id, "category_key": category_key, "doc_id": doc_id,
        "props": strip_empty(props), "doc_edge": strip_empty(doc_edge), "now": now})
    return bool(rows and rows[0]["created"])


def upsert_provision(*, provision_id, policy_id, doc_id, kind, props,
                     source_edge, now) -> bool:
    rows = run_query(PROVISION_QUERY, {
        "provision_id": provision_id, "policy_id": policy_id, "doc_id": doc_id,
        "edge": edge_for_kind(kind), "props": strip_empty(props),
        "source_edge": strip_empty(source_edge), "now": now})
    return bool(rows and rows[0]["created"])


def upsert_entity(*, label, entity_key, props, now) -> bool:
    if label not in ENTITY_LABELS:
        raise ValueError(f"unknown entity label: {label!r}")
    rows = run_query(ENTITY_QUERY % {"label": label},
                     {"entity_key": entity_key, "props": strip_empty(props),
                      "now": now})
    return bool(rows and rows[0]["created"])


def link(*, from_label, from_id, rel, to_label, to_id, props=None) -> int:
    """Create one relationship. Labels and type are allow-listed, not free text."""
    if rel not in RELATIONSHIP_TYPES:
        raise ValueError(f"unknown relationship type: {rel!r}")
    for label in (from_label, to_label):
        if label not in KEY_PROPERTY:
            raise ValueError(f"unknown node label: {label!r}")
    query = LINK_QUERY % {
        "from_label": from_label, "from_key": KEY_PROPERTY[from_label],
        "to_label": to_label, "to_key": KEY_PROPERTY[to_label], "rel": rel,
    }
    rows = run_query(query, {"from_id": from_id, "to_id": to_id,
                             "props": strip_empty(props or {})})
    return rows[0]["linked"] if rows else 0


def counts() -> dict:
    return {name: run_query(q)[0]["count"] for name, q in COUNT_QUERIES.items()}

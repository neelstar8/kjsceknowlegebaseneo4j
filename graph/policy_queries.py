"""Parameterized Cypher for policy retrieval. The LLM never writes Cypher.

Same contract as graph/faculty_queries.py and graph/pyq_queries.py: every
query here takes parameters, returns dicts, and is safe to call with whatever
a student typed.

Two retrieval shapes, because policy questions come in two shapes:

  by topic    "what is the attendance requirement" -> provisions, ranked, each
              carrying its own page and section so the answer can cite them.
  by policy   "what is the library policy" -> one policy with its provisions.

Superseded policies are excluded by default. The handbook contains a 2018
edition whose examination rules no longer apply; answering a current student
from it would be worse than saying nothing.
"""
from graph.neo4j_driver import run_query

# One system prompt for the whole Policy knowledge domain, read off the
# singleton :PolicyHandbook root rather than duplicated onto every Policy or
# PolicyProvision node.
HANDBOOK_SYSTEM_PROMPT_QUERY = """
MATCH (h:PolicyHandbook)
RETURN h.system_prompt AS system_prompt
LIMIT 1
"""

VOCABULARY_QUERY = """
MATCH (p:Policy)
RETURN p.policy_id AS policy_id, p.name AS name, p.aliases AS aliases,
       p.status AS status, p.category_key AS category_key
ORDER BY p.name
"""

ENTITY_VOCABULARY_QUERY = """
MATCH (e)
WHERE e:Committee OR e:Department OR e:Role OR e:Form OR e:Portal
   OR e:Scheme OR e:Facility OR e:StudentCategory OR e:Programme
   OR e:ExternalOrganization
RETURN labels(e)[0] AS label, e.entity_key AS entity_key, e.name AS name
ORDER BY e.name
"""

TOPIC_VOCABULARY_QUERY = """
MATCH (v:PolicyProvision)
WHERE v.topic IS NOT NULL
RETURN DISTINCT v.topic AS topic
ORDER BY topic
"""

# Fulltext over provision text and topic. `status` filtering happens on the
# owning policy, not the provision, so a superseded edition drops out whole.
SEARCH_PROVISIONS_QUERY = """
CALL db.index.fulltext.queryNodes('policy_provision_text', $search)
YIELD node AS v, score
MATCH (p:Policy)-[]->(v)
WHERE ($include_superseded OR p.status <> 'superseded')
  AND ($kinds IS NULL OR v.kind IN $kinds)
MATCH (v)-[s:SOURCED_FROM]->(d:PolicyDocument)
RETURN v.provision_id AS provision_id, v.text AS text, v.kind AS kind,
       v.topic AS topic, v.source_page AS page, v.source_section AS section,
       v.number_values AS number_values, v.number_units AS number_units,
       v.number_labels AS number_labels, v.ambiguity AS ambiguity,
       v.superseded_note AS superseded_note,
       p.policy_id AS policy_id, p.name AS policy_name, p.status AS policy_status,
       d.title AS document_title, d.source_url AS source_url,
       d.filename AS filename, score
ORDER BY score DESC
LIMIT $limit
"""

POLICY_BY_ID_QUERY = """
MATCH (p:Policy {policy_id: $policy_id})-[:BELONGS_TO]->(c:PolicyCategory)
MATCH (p)-[doc:DOCUMENTED_IN]->(d:PolicyDocument)
OPTIONAL MATCH (p)-[:SUPERSEDED_BY]->(newer:Policy)
RETURN p.policy_id AS policy_id, p.name AS name, p.purpose AS purpose,
       p.scope AS scope, p.status AS status, p.institution AS institution,
       p.version_note AS version_note, p.completeness_note AS completeness_note,
       p.source_note AS source_note,
       c.name AS category, d.title AS document_title, d.source_url AS source_url,
       d.filename AS filename, d.pages AS document_pages,
       doc.section AS section, doc.page_start AS page_start,
       doc.page_end AS page_end, newer.policy_id AS superseded_by,
       newer.name AS superseded_by_name
"""

PROVISIONS_FOR_POLICY_QUERY = """
MATCH (p:Policy {policy_id: $policy_id})-[]->(v:PolicyProvision)
WHERE $kinds IS NULL OR v.kind IN $kinds
RETURN v.provision_id AS provision_id, v.kind AS kind, v.topic AS topic,
       v.text AS text, v.source_page AS page, v.source_section AS section,
       v.number_values AS number_values, v.number_units AS number_units,
       v.number_labels AS number_labels, v.ambiguity AS ambiguity,
       v.superseded_note AS superseded_note
ORDER BY v.source_page, v.provision_id
"""

# "What documents do I need for X" / "which portal do I use".
PROVISION_REQUIREMENTS_QUERY = """
MATCH (v:PolicyProvision {provision_id: $provision_id})
OPTIONAL MATCH (v)-[:REQUIRES]->(f:Form)
OPTIONAL MATCH (v)-[:USES]->(portal:Portal)
OPTIONAL MATCH (role)-[:RESPONSIBLE_FOR]->(v)
OPTIONAL MATCH (approver)-[:APPROVES]->(v)
OPTIONAL MATCH (v)-[:HAS_CONSEQUENCE]->(pen:PolicyProvision)
OPTIONAL MATCH (v)-[:HAS_EXCEPTION]->(exc:PolicyProvision)
RETURN collect(DISTINCT CASE WHEN f IS NULL THEN NULL
                             ELSE {name: f.name, url: f.url} END) AS forms,
       collect(DISTINCT portal.name) AS portals,
       collect(DISTINCT role.name) AS responsible,
       collect(DISTINCT approver.name) AS approvers,
       collect(DISTINCT pen.text) AS consequences,
       collect(DISTINCT exc.text) AS exceptions
"""

POLICIES_FOR_ENTITY_QUERY = """
MATCH (e {entity_key: $entity_key})
MATCH (p:Policy)-[r]->(e)
WHERE type(r) IN ['APPLIES_TO', 'INVOLVES', 'REFERENCES']
  AND ($include_superseded OR p.status <> 'superseded')
RETURN DISTINCT p.policy_id AS policy_id, p.name AS name, type(r) AS relationship,
       p.status AS status
ORDER BY p.name
"""

CATEGORY_TREE_QUERY = """
MATCH (h:PolicyHandbook)-[:HAS_CATEGORY]->(c:PolicyCategory)
OPTIONAL MATCH (p:Policy)-[:BELONGS_TO]->(c)
RETURN c.category_key AS category_key, c.name AS category,
       c.display_order AS display_order,
       collect({policy_id: p.policy_id, name: p.name, status: p.status}) AS policies
ORDER BY c.display_order
"""

NUMERIC_LOOKUP_QUERY = """
MATCH (p:Policy)-[]->(v:PolicyProvision)
WHERE v.number_values IS NOT NULL
  AND ($include_superseded OR p.status <> 'superseded')
  AND any(label IN v.number_labels WHERE toLower(label) CONTAINS toLower($label))
RETURN v.provision_id AS provision_id, v.topic AS topic, v.text AS text,
       v.number_values AS number_values, v.number_units AS number_units,
       v.number_labels AS number_labels, v.source_page AS page,
       v.source_section AS section, p.name AS policy_name,
       p.policy_id AS policy_id
ORDER BY v.provision_id
LIMIT $limit
"""


def handbook_system_prompt() -> str | None:
    rows = run_query(HANDBOOK_SYSTEM_PROMPT_QUERY)
    return rows[0]["system_prompt"] if rows else None


def policy_vocabulary() -> list[dict]:
    return run_query(VOCABULARY_QUERY)


def entity_vocabulary() -> list[dict]:
    return run_query(ENTITY_VOCABULARY_QUERY)


def topic_vocabulary() -> list[str]:
    return [row["topic"] for row in run_query(TOPIC_VOCABULARY_QUERY)]


def search_provisions(search: str, *, limit: int = 12, kinds: list[str] | None = None,
                      include_superseded: bool = False) -> list[dict]:
    return run_query(SEARCH_PROVISIONS_QUERY, {
        "search": search, "limit": limit, "kinds": kinds,
        "include_superseded": include_superseded})


def policy_by_id(policy_id: str) -> dict | None:
    rows = run_query(POLICY_BY_ID_QUERY, {"policy_id": policy_id})
    return rows[0] if rows else None


def provisions_for_policy(policy_id: str, kinds: list[str] | None = None) -> list[dict]:
    return run_query(PROVISIONS_FOR_POLICY_QUERY,
                     {"policy_id": policy_id, "kinds": kinds})


def provision_requirements(provision_id: str) -> dict:
    rows = run_query(PROVISION_REQUIREMENTS_QUERY, {"provision_id": provision_id})
    return rows[0] if rows else {}


def policies_for_entity(entity_key: str, include_superseded: bool = False) -> list[dict]:
    return run_query(POLICIES_FOR_ENTITY_QUERY,
                     {"entity_key": entity_key,
                      "include_superseded": include_superseded})


def category_tree() -> list[dict]:
    return run_query(CATEGORY_TREE_QUERY)


def numeric_lookup(label: str, *, limit: int = 10,
                   include_superseded: bool = False) -> list[dict]:
    return run_query(NUMERIC_LOOKUP_QUERY, {
        "label": label, "limit": limit, "include_superseded": include_superseded})

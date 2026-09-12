"""Upserts normalized faculty records into Neo4j.

Graph shape for this stage -- deliberately flat:

    (:Faculty {name: "Faculty"})-[:HAS_MEMBER]->(:FacultyMember {...})

Exactly one :Faculty root. No Department/Subject/Publication/Institution
nodes yet; every attribute lives as a property on the FacultyMember. The
graph gets normalized in a later stage.

Identity is the official faculty_id from the directory's view-member URL,
which is stable across runs, so re-running updates rather than duplicates.
"""
from graph.neo4j_driver import run_query

ROOT_FACULTY_NAME = "Faculty"

CONSTRAINT_QUERY = """
CREATE CONSTRAINT faculty_member_faculty_id_unique IF NOT EXISTS
FOR (v:FacultyMember) REQUIRE v.faculty_id IS UNIQUE
"""

ROOT_QUERY = """
MERGE (f:Faculty {name: $root_name})
RETURN f
"""

# Note: MERGE on faculty_id then `SET v += $properties`. Because the caller
# strips empty values out of $properties, keys the source has nothing to say
# about are left untouched rather than nulled out.
UPSERT_QUERY = """
MATCH (f:Faculty {name: $root_name})
MERGE (v:FacultyMember {faculty_id: $faculty_id})
ON CREATE SET v._created = true
SET v += $properties
MERGE (f)-[:HAS_MEMBER]->(v)
WITH v, coalesce(v._created, false) AS created
REMOVE v._created
RETURN created
"""

GET_EXISTING_QUERY = """
MATCH (v:FacultyMember)
WHERE v.faculty_id IN $ids
RETURN v.faculty_id AS faculty_id, properties(v) AS props
"""

COUNT_QUERY = "MATCH (v:FacultyMember) RETURN count(v) AS count"


def ensure_schema():
    """Create the uniqueness constraint (Neo4j 5/2025+ syntax)."""
    run_query(CONSTRAINT_QUERY)
    run_query(ROOT_QUERY, {"root_name": ROOT_FACULTY_NAME})


def fetch_existing(ids: list[str]) -> dict[str, dict]:
    if not ids:
        return {}
    rows = run_query(GET_EXISTING_QUERY, {"ids": ids})
    return {r["faculty_id"]: r["props"] for r in rows}


def merge_properties(existing: dict, incoming: dict) -> dict:
    """Decide what to actually write, without destroying good data.

    Rules:
      * Keys absent from `incoming` are never touched (the caller has already
        stripped empty values), so a sparse directory record cannot blank out
        a richly filled-in node.
      * Scalars: the fresh official value wins -- that is the point of
        re-running the pipeline when a designation or email changes. The one
        exception is when the existing value is a strict expansion of the new
        one ("Computer Engineering" vs the directory's terser "Computer"):
        that is the same fact stated more fully, so the richer form is kept.
      * Lists: keep whichever is longer. Profile sections are sometimes
        rendered partially, and silently shrinking a list is far more likely
        to be data loss than a genuine update.
    """
    if not existing:
        return dict(incoming)

    out = {}
    for key, new_value in incoming.items():
        old_value = existing.get(key)
        if isinstance(new_value, list) and isinstance(old_value, list):
            out[key] = old_value if len(old_value) > len(new_value) else new_value
        elif (
            isinstance(new_value, str)
            and isinstance(old_value, str)
            and len(old_value) > len(new_value)
            and new_value.lower() in old_value.lower()
        ):
            out[key] = old_value
        else:
            out[key] = new_value
    return out


def upsert_faculty_member(faculty_id: str, properties: dict) -> bool:
    """Returns True if the node was created, False if it was updated."""
    rows = run_query(
        UPSERT_QUERY,
        {
            "root_name": ROOT_FACULTY_NAME,
            "faculty_id": faculty_id,
            "properties": properties,
        },
    )
    return bool(rows and rows[0]["created"])


def count_faculty_members() -> int:
    return run_query(COUNT_QUERY)[0]["count"]

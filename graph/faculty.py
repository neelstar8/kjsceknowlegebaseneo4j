"""Faculty-specific Cypher queries. All queries here are deterministic and
parameterized -- no string interpolation, no LLM-generated Cypher."""
from graph.neo4j_driver import run_query

UPSERT_FACULTY_MEMBER_QUERY = """
MERGE (f:Faculty {name: "Faculty"})
MERGE (v:FacultyMember {name: $name})
SET v += $properties
MERGE (f)-[:HAS_MEMBER]->(v)
RETURN v
"""

GET_FACULTY_MEMBER_QUERY = """
MATCH (f:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
WHERE toLower(v.name) = toLower($name)
RETURN v
"""

GET_ALL_FACULTY_QUERY = """
MATCH (f:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
RETURN v
"""


def upsert_faculty_member(name: str, properties: dict):
    return run_query(
        UPSERT_FACULTY_MEMBER_QUERY,
        {"name": name, "properties": properties},
    )


def get_faculty_member(name: str):
    """Returns the FacultyMember node properties dict, or None if not found."""
    records = run_query(GET_FACULTY_MEMBER_QUERY, {"name": name})
    if not records:
        return None
    return records[0]["v"]


def get_all_faculty_members():
    records = run_query(GET_ALL_FACULTY_QUERY)
    return [r["v"] for r in records]

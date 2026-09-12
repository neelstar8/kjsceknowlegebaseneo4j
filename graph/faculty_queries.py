"""Deterministic, parameterized Cypher for the faculty graph.

Everything here queries the flat stage-1 shape only:
    (:Faculty {name:"Faculty"})-[:HAS_MEMBER]->(:FacultyMember)
No Department/Subject/Publication nodes exist yet, so "find by department"
means matching a property, not traversing a relationship.

No query is ever built by string interpolation, and none is LLM-generated.
"""
from graph.neo4j_driver import run_query

COUNT_FACULTY = "MATCH (v:FacultyMember) RETURN count(v) AS count"

FIND_BY_NAME = """
MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
WHERE toLower(v.name) CONTAINS toLower($name)
   OR any(alias IN coalesce(v.name_variations, [])
          WHERE toLower(alias) CONTAINS toLower($name))
RETURN v
ORDER BY v.name
LIMIT $limit
"""

FIND_BY_FACULTY_ID = """
MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember {faculty_id: $faculty_id})
RETURN v
"""

FIND_BY_DEPARTMENT = """
MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
WHERE toLower(coalesce(v.department, '')) CONTAINS toLower($department)
RETURN v
ORDER BY v.name
LIMIT $limit
"""

FIND_BY_DESIGNATION = """
MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
WHERE toLower(coalesce(v.designation, '')) CONTAINS toLower($designation)
RETURN v
ORDER BY v.name
LIMIT $limit
"""

FIND_BY_SCHOOL = """
MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
WHERE toLower(coalesce(v.school, '')) CONTAINS toLower($school)
RETURN v
ORDER BY v.name
LIMIT $limit
"""

FIND_BY_RESEARCH_INTEREST = """
MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
WHERE any(topic IN coalesce(v.research_interests, [])
          WHERE toLower(topic) CONTAINS toLower($topic))
   OR any(topic IN coalesce(v.research_specialization, [])
          WHERE toLower(topic) CONTAINS toLower($topic))
RETURN v
ORDER BY v.name
LIMIT $limit
"""

FIND_BY_SUBJECT = """
MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
WHERE any(s IN coalesce(v.subjects_taught, [])
          WHERE toLower(s) CONTAINS toLower($subject))
RETURN v
ORDER BY v.name
LIMIT $limit
"""

WITH_GOOGLE_SCHOLAR = """
MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
WHERE v.google_scholar_url IS NOT NULL
RETURN v
ORDER BY v.name
LIMIT $limit
"""

WITH_PUBLICATIONS = """
MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
WHERE size(coalesce(v.publications, [])) > 0
   OR size(coalesce(v.selected_publications, [])) > 0
RETURN v
ORDER BY v.name
LIMIT $limit
"""

LIST_WITH_DEPARTMENTS = """
MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
RETURN v.name AS name, v.designation AS designation,
       v.department AS department, v.school AS school
ORDER BY v.name
LIMIT $limit
"""


ALL_NAMES = """
MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
RETURN v.faculty_id AS faculty_id, v.name AS name,
       coalesce(v.name_variations, []) AS name_variations
ORDER BY v.name
"""

DISTINCT_RESEARCH_TOPICS = """
MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
UNWIND coalesce(v.research_interests, []) +
       coalesce(v.research_specialization, []) AS topic
RETURN DISTINCT topic
"""

DISTINCT_SUBJECTS = """
MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
UNWIND coalesce(v.subjects_taught, []) AS subject
RETURN DISTINCT subject
"""


def run_all_names():
    return run_query(ALL_NAMES)


def distinct_research_topics() -> list[str]:
    return [r["topic"] for r in run_query(DISTINCT_RESEARCH_TOPICS) if r["topic"]]


def distinct_subjects() -> list[str]:
    return [r["subject"] for r in run_query(DISTINCT_SUBJECTS) if r["subject"]]


def _nodes(query, params):
    return [r["v"] for r in run_query(query, params)]


def count_faculty() -> int:
    return run_query(COUNT_FACULTY)[0]["count"]


def find_by_name(name: str, limit: int = 10):
    return _nodes(FIND_BY_NAME, {"name": name, "limit": limit})


def find_by_faculty_id(faculty_id: str):
    nodes = _nodes(FIND_BY_FACULTY_ID, {"faculty_id": faculty_id})
    return nodes[0] if nodes else None


def find_by_department(department: str, limit: int = 50):
    return _nodes(FIND_BY_DEPARTMENT, {"department": department, "limit": limit})


def find_by_designation(designation: str, limit: int = 50):
    return _nodes(FIND_BY_DESIGNATION, {"designation": designation, "limit": limit})


def find_by_school(school: str, limit: int = 50):
    return _nodes(FIND_BY_SCHOOL, {"school": school, "limit": limit})


def find_by_research_interest(topic: str, limit: int = 50):
    return _nodes(FIND_BY_RESEARCH_INTEREST, {"topic": topic, "limit": limit})


def find_by_subject(subject: str, limit: int = 50):
    return _nodes(FIND_BY_SUBJECT, {"subject": subject, "limit": limit})


def find_with_google_scholar(limit: int = 50):
    return _nodes(WITH_GOOGLE_SCHOLAR, {"limit": limit})


def find_with_publications(limit: int = 50):
    return _nodes(WITH_PUBLICATIONS, {"limit": limit})


def list_with_departments(limit: int = 100):
    return run_query(LIST_WITH_DEPARTMENTS, {"limit": limit})

"""Runs the stage-1 verification queries against the faculty graph.

These only exercise the flat shape that exists today:
    (:Faculty {name:"Faculty"})-[:HAS_MEMBER]->(:FacultyMember)
There are deliberately no Subject / Department / Publication nodes yet, so
"faculty in Computer Engineering" is a property match, not a traversal.

Usage:
    python -m scripts.test_faculty_queries
"""
from graph.neo4j_driver import close_driver, run_query, verify_connection

QUERIES = [
    (
        "1. Find Vaibhav Vasani",
        """
        MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
        WHERE toLower(v.name) CONTAINS 'vasani'
        RETURN v.faculty_id AS faculty_id, v.name AS name,
               v.designation AS designation, v.department AS department
        """,
        {},
    ),
    (
        "2. All faculty in Computer Engineering",
        """
        MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
        WHERE toLower(coalesce(v.department, '')) CONTAINS 'computer'
        RETURN v.name AS name, v.designation AS designation,
               v.department AS department
        ORDER BY v.name LIMIT 25
        """,
        {},
    ),
    (
        "3. All Assistant Professors",
        """
        MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
        WHERE toLower(coalesce(v.designation, '')) = 'assistant professor'
        RETURN count(v) AS assistant_professors
        """,
        {},
    ),
    (
        "4. Research interests containing Machine Learning",
        """
        MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
        WHERE any(t IN coalesce(v.research_interests, [])
                  WHERE toLower(t) CONTAINS 'machine learning')
        RETURN v.name AS name, v.department AS department,
               v.research_interests AS research_interests
        ORDER BY v.name LIMIT 15
        """,
        {},
    ),
    (
        "5. Names containing 'Sharma'",
        """
        MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
        WHERE toLower(v.name) CONTAINS 'sharma'
        RETURN v.name AS name, v.designation AS designation,
               v.department AS department
        ORDER BY v.name
        """,
        {},
    ),
    (
        "6. Count faculty",
        "MATCH (v:FacultyMember) RETURN count(v) AS total_faculty",
        {},
    ),
    (
        "7. Faculty with their departments (first 15 of 100)",
        """
        MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
        RETURN v.name AS name, v.designation AS designation,
               v.department AS department
        ORDER BY v.name LIMIT 15
        """,
        {},
    ),
    (
        "8. Faculty with a Google Scholar profile",
        """
        MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
        WHERE v.google_scholar_url IS NOT NULL
        RETURN count(v) AS with_google_scholar
        """,
        {},
    ),
    (
        "9. Faculty who have publications listed",
        """
        MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
        WHERE size(coalesce(v.publications, [])) > 0
           OR size(coalesce(v.selected_publications, [])) > 0
        RETURN count(v) AS with_publications
        """,
        {},
    ),
    (
        "10. Faculty with research interest $topic",
        """
        MATCH (:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
        WHERE any(t IN coalesce(v.research_interests, []) +
                       coalesce(v.research_specialization, [])
                  WHERE toLower(t) CONTAINS toLower($topic))
        RETURN v.name AS name, v.department AS department
        ORDER BY v.name LIMIT 15
        """,
        {"topic": "Data Science"},
    ),
    (
        "11. Graph shape sanity check",
        """
        MATCH (f:Faculty)
        OPTIONAL MATCH (f)-[:HAS_MEMBER]->(v:FacultyMember)
        RETURN count(DISTINCT f) AS faculty_root_nodes,
               count(DISTINCT v) AS linked_members
        """,
        {},
    ),
]


def main():
    verify_connection()
    for title, cypher, params in QUERIES:
        print("=" * 70)
        print(title)
        print("=" * 70)
        rows = run_query(cypher, params)
        if not rows:
            print("  (no results)")
        for row in rows:
            printable = {
                k: (v if not isinstance(v, list) else ", ".join(map(str, v))[:110])
                for k, v in row.items()
            }
            print("  " + " | ".join(f"{k}={v}" for k, v in printable.items()))
        print()
    close_driver()


if __name__ == "__main__":
    main()

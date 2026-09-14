"""Upserts PYQ records into Neo4j. Metadata and Drive links only -- no PDF bytes.

Graph shape:

    (:PYQ)-[:STORED_IN {page_label, part_index, section_label}]->(:PYQFile)
    (:PYQ)-[:FOR_SUBJECT]->(:Subject)

Two nodes rather than one because the physical Drive file and the logical
question paper are many-to-many in both directions in this corpus: one PDF can
hold several papers, and one paper can be split across several files
('ML 1 pg.jpg' + 'ML 2 pg.jpg'). Collapsing them would either duplicate the
physical file or lose a page.

Identity:
    PYQFile  -> drive_file_id, assigned by Google and stable forever.
    PYQ      -> pyq_id, a pure function of the parsed metadata.
Both are unique-constrained, so re-running the ingest updates rather than
duplicates. This module never deletes anything.
"""
from graph.neo4j_driver import run_query

CONSTRAINTS = [
    """
    CREATE CONSTRAINT pyq_file_drive_id_unique IF NOT EXISTS
    FOR (f:PYQFile) REQUIRE f.drive_file_id IS UNIQUE
    """,
    """
    CREATE CONSTRAINT pyq_id_unique IF NOT EXISTS
    FOR (p:PYQ) REQUIRE p.pyq_id IS UNIQUE
    """,
    """
    CREATE CONSTRAINT subject_key_unique IF NOT EXISTS
    FOR (s:Subject) REQUIRE s.subject_key IS UNIQUE
    """,
]

INDEXES = [
    "CREATE INDEX pyq_subject_key IF NOT EXISTS FOR (p:PYQ) ON (p.subject_key)",
    "CREATE INDEX pyq_exam_type IF NOT EXISTS FOR (p:PYQ) ON (p.exam_type)",
    "CREATE INDEX pyq_exam_year IF NOT EXISTS FOR (p:PYQ) ON (p.exam_year)",
    "CREATE INDEX pyq_academic_year IF NOT EXISTS FOR (p:PYQ) ON (p.academic_year)",
    "CREATE INDEX pyq_semester IF NOT EXISTS FOR (p:PYQ) ON (p.semester)",
]

# One statement per (paper, file) pair. `SET x += $props` with empty values
# already stripped by the caller, so a sparse parse never nulls out good data --
# the same contract graph/faculty_ingestion.py uses.
UPSERT_QUERY = """
MERGE (f:PYQFile {drive_file_id: $drive_file_id})
  ON CREATE SET f.first_seen_at = $now
SET f += $file_props, f.last_seen_at = $now

MERGE (s:Subject {subject_key: $subject_key})
  ON CREATE SET s.name = $subject_name, s.created_at = $now
SET s.name = coalesce($subject_name, s.name),
    s.aliases = CASE WHEN $aliases IS NULL THEN s.aliases ELSE $aliases END,
    s.code = coalesce($subject_code, s.code),
    s.status = $subject_status

MERGE (p:PYQ {pyq_id: $pyq_id})
  ON CREATE SET p._created = true, p.first_seen_at = $now
SET p += $pyq_props, p.ingested_at = $now

MERGE (p)-[r:STORED_IN]->(f)
SET r += $edge_props
MERGE (p)-[:FOR_SUBJECT]->(s)

WITH p, coalesce(p._created, false) AS created
REMOVE p._created
RETURN created
"""

# A semester bundle holds every subject sat that semester and names none of
# them. It gets the PYQ and PYQFile nodes so its Drive link stays reachable by
# semester/year/exam-type queries, but deliberately no :Subject and no
# FOR_SUBJECT edge -- a subject query must never be able to reach it, because
# nothing in the metadata establishes which subjects are inside.
UPSERT_BUNDLE_QUERY = """
MERGE (f:PYQFile {drive_file_id: $drive_file_id})
  ON CREATE SET f.first_seen_at = $now
SET f += $file_props, f.last_seen_at = $now

MERGE (p:PYQ {pyq_id: $pyq_id})
  ON CREATE SET p._created = true, p.first_seen_at = $now
SET p += $pyq_props, p.ingested_at = $now

MERGE (p)-[r:STORED_IN]->(f)
SET r += $edge_props

WITH p, coalesce(p._created, false) AS created
REMOVE p._created
RETURN created
"""

COUNT_QUERIES = {
    "pyq": "MATCH (p:PYQ) RETURN count(p) AS count",
    "pyq_file": "MATCH (f:PYQFile) RETURN count(f) AS count",
    "subject": "MATCH (s:Subject) RETURN count(s) AS count",
    "stored_in": "MATCH (:PYQ)-[r:STORED_IN]->(:PYQFile) RETURN count(r) AS count",
    "for_subject": "MATCH (:PYQ)-[r:FOR_SUBJECT]->(:Subject) RETURN count(r) AS count",
    "faculty_member": "MATCH (v:FacultyMember) RETURN count(v) AS count",
}

STALE_QUERY = """
MATCH (f:PYQFile)
WHERE f.collection = $collection AND (f.last_seen_at IS NULL OR f.last_seen_at < $run_started)
RETURN f.drive_file_id AS drive_file_id, f.file_name AS file_name,
       f.folder_path AS folder_path, f.last_seen_at AS last_seen_at
ORDER BY f.file_name
"""

NON_ISE_QUERY = "MATCH (p:PYQ) WHERE p.exam_type <> 'ISE' RETURN count(p) AS count"


def ensure_schema():
    """Create constraints and indexes. Safe to call on every run."""
    for statement in CONSTRAINTS + INDEXES:
        run_query(statement)


def upsert_pyq(*, pyq_id, pyq_props, file_props, edge_props, subject_key,
               subject_name, subject_code, subject_status, aliases, now,
               is_bundle: bool = False) -> bool:
    """Write one paper and the file it lives in. True if the PYQ was created."""
    if is_bundle:
        rows = run_query(UPSERT_BUNDLE_QUERY, {
            "pyq_id": pyq_id,
            "pyq_props": pyq_props,
            "drive_file_id": file_props["drive_file_id"],
            "file_props": file_props,
            "edge_props": edge_props,
            "now": now,
        })
        return bool(rows and rows[0]["created"])
    rows = run_query(UPSERT_QUERY, {
        "pyq_id": pyq_id,
        "pyq_props": pyq_props,
        "drive_file_id": file_props["drive_file_id"],
        "file_props": file_props,
        "edge_props": edge_props,
        "subject_key": subject_key,
        "subject_name": subject_name,
        "subject_code": subject_code,
        "subject_status": subject_status,
        "aliases": aliases,
        "now": now,
    })
    return bool(rows and rows[0]["created"])


def counts() -> dict:
    return {name: run_query(q)[0]["count"] for name, q in COUNT_QUERIES.items()}


def stale_files(collection: str, run_started: str) -> list[dict]:
    """Files in the graph that this run did not see in Drive any more.

    Reported, never deleted -- a transient Drive permission problem must not
    be able to erase the knowledge base.
    """
    return run_query(STALE_QUERY, {"collection": collection,
                                   "run_started": run_started})


def non_ise_count() -> int:
    return run_query(NON_ISE_QUERY)[0]["count"]

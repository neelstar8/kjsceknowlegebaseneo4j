"""Verification queries for the PYQ subgraph.

Checks the things that would actually hurt if they broke:
  * the five student question shapes each return a usable Drive link
  * the faculty subgraph is untouched
  * no PDF content leaked into the graph
  * no ESE paper was ingested in this phase
  * physical files are never duplicated, and split papers stay unified

Usage:
    .venv/bin/python -m scripts.test_pyq_queries
"""
from graph.neo4j_driver import close_driver, run_query, verify_connection
from graph.pyq_ingestion import counts, non_ise_count
import graph.pyq_queries as q

EXPECTED_FACULTY_MEMBERS = 613

# Properties that would mean paper *content* had been stored rather than a
# pointer to it. The whole design depends on this staying empty.
FORBIDDEN_PROPS = ["content", "text", "body", "binary", "base64", "pages_text",
                   "raw_pdf", "extracted_text"]

CONTENT_LEAK_QUERY = """
MATCH (n) WHERE n:PYQ OR n:PYQFile
WITH n, [k IN keys(n) WHERE k IN $forbidden] AS bad
WHERE size(bad) > 0
RETURN labels(n) AS labels, bad LIMIT 5
"""

DUP_FILE_QUERY = """
MATCH (f:PYQFile)
WITH f.drive_file_id AS id, count(*) AS c
WHERE c > 1
RETURN id, c
"""

MISSING_URL_QUERY = """
MATCH (f:PYQFile)
WHERE f.drive_url IS NULL OR NOT f.drive_url STARTS WITH 'https://drive.google.com/'
RETURN f.file_name AS file_name, f.drive_url AS drive_url LIMIT 5
"""

ORPHAN_QUERY = """
MATCH (p:PYQ) WHERE NOT (p)-[:STORED_IN]->(:PYQFile)
RETURN p.pyq_id AS pyq_id LIMIT 5
"""


def main():
    verify_connection()
    failures, notes = [], []

    def check(label, ok, detail=""):
        print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"  -- {detail}" if detail else ""))
        if not ok:
            failures.append(label)

    c = counts()
    print(f"\nGraph: PYQ={c['pyq']} PYQFile={c['pyq_file']} Subject={c['subject']} "
          f"STORED_IN={c['stored_in']} FOR_SUBJECT={c['for_subject']}")

    print("\n-- the five student question shapes --")
    for label, kwargs in [
        ("all DBMS papers", {"subject_key": "dbms", "limit": 100}),
        ("DBMS paper 2024", {"subject_key": "dbms", "year": 2024}),
        ("DBMS 2024 ISE paper", {"subject_key": "dbms", "year": 2024,
                                 "exam_type": "ISE"}),
        ("all ISE papers", {"exam_type": "ISE", "limit": 1000}),
        ("all ISE DBMS papers", {"subject_key": "dbms", "exam_type": "ISE",
                                 "limit": 100}),
    ]:
        rows = q.find_pyq(**kwargs)
        usable = [r for r in rows
                  if (r.get("drive_url") or "").startswith("https://drive.google.com/")]
        check(f'"{label}"', bool(rows) and len(usable) == len(rows),
              f"{len(rows)} result(s), {len(usable)} with a usable link")

    print("\n-- integrity --")
    check("faculty subgraph untouched", c["faculty_member"] == EXPECTED_FACULTY_MEMBERS,
          f"FacultyMember={c['faculty_member']} (expected {EXPECTED_FACULTY_MEMBERS})")

    leaks = run_query(CONTENT_LEAK_QUERY, {"forbidden": FORBIDDEN_PROPS})
    check("no paper content stored in the graph", not leaks, str(leaks[:2]))

    check("no ESE papers ingested in this phase", non_ise_count() == 0,
          f"non-ISE PYQ nodes = {non_ise_count()}")

    dups = run_query(DUP_FILE_QUERY)
    check("no duplicated physical Drive files", not dups, str(dups[:3]))

    bad_urls = run_query(MISSING_URL_QUERY)
    check("every PYQFile has a Google Drive URL", not bad_urls, str(bad_urls[:2]))

    orphans = run_query(ORPHAN_QUERY)
    check("every PYQ points at a file", not orphans, str(orphans[:3]))

    print("\n-- many-to-many cases --")
    multi_files = q.multi_paper_files()
    check("multi-paper PDFs kept as one file node", bool(multi_files),
          f"{len(multi_files)} file(s) holding several papers")
    for row in multi_files[:3]:
        print(f"        {row['file_name']} -> {row['papers']} papers")

    split = q.multi_file_papers()
    check("split papers kept as one PYQ", bool(split),
          f"{len(split)} paper(s) spanning several files")
    for row in split[:3]:
        print(f"        {row['title']} -> {row['files']}")

    print("\n-- review queue (informational, not failures) --")
    unresolved = q.unresolved_subjects()
    print(f"  {sum(r['papers'] for r in unresolved)} paper(s) with an unresolved "
          f"subject, {len(unresolved)} distinct token(s)")
    for row in unresolved[:5]:
        print(f"        {row['subject_raw']!r} x{row['papers']}  e.g. "
              f"{row['example_files'][0]}")
    print("  -> data/pyq_unknown_report.json lists every one with its Drive link")

    fv = q.filter_values()
    print(f"\n  academic years: {sorted(x for x in fv['academic_years'] if x)}")
    print(f"  semesters:      {sorted(x for x in fv['semesters'] if x)}")
    print(f"  subjects with papers: {len(q.all_subjects())}")

    print()
    if failures:
        print(f"FAILED: {len(failures)} check(s) -- {failures}")
        close_driver()
        return 1
    print("All PYQ graph checks passed.")
    close_driver()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

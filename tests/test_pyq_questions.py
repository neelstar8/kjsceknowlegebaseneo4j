"""End-to-end PYQ question test: 32 student questions -> Drive links.

Checks both that retrieval finds the right papers and that every link handed
back is a real Google Drive URL. Deterministic path by default, so the whole
suite runs in well under a second:

    .venv/bin/python -m tests.test_pyq_questions
    .venv/bin/python -m tests.test_pyq_questions --llm     # Qwen phrasing too
    .venv/bin/python -m tests.test_pyq_questions --verbose # print every link
"""
import argparse
import time

from graph.neo4j_driver import close_driver, verify_connection
from services.pyq_service import answer_pyq_question, extract_filters, retrieve

DRIVE_PREFIX = "https://drive.google.com/"

# (question, expectation)
#   ("min", n)      -> at least n papers, every one with a usable link
#   ("subject", k)  -> at least one paper, and every result is subject k
#   ("empty", why)  -> no papers, for the stated reason
QUESTIONS = [
    # --- the five shapes from the brief ---------------------------------
    ("Give me all DBMS papers",                    ("subject", "dbms")),
    ("Give me DBMS paper 2024",                    ("subject", "dbms")),
    ("Give me DBMS 2024 ISE paper",                ("subject", "dbms")),
    ("Give me all ISE papers",                     ("min", 50)),
    ("Give me all ISE DBMS papers",                ("subject", "dbms")),

    # --- abbreviation vs full name --------------------------------------
    ("give me OS paper",                           ("subject", "os")),
    ("operating system previous year papers",      ("subject", "os")),
    ("database management system paper",           ("subject", "dbms")),
    ("give me rdbms paper",                        ("subject", "dbms")),
    ("Give me all Computer Networks papers",       ("subject", "cn")),
    ("CN 2023 paper",                              ("subject", "cn")),
    ("artificial intelligence papers",             ("subject", "ai")),
    ("machine learning paper",                     ("subject", "ml")),
    ("soft computing question paper",              ("subject", "sc")),
    ("analysis of algorithms 2025",                ("subject", "aoa")),
    ("give me NLP papers",                         ("subject", "nlp")),
    ("cryptography and system security paper",     ("subject", "css")),
    ("web programming paper",                      ("subject", "wp")),
    ("Flutter paper",                              ("subject", "mad")),

    # --- filters other than subject --------------------------------------
    ("Give me COA paper sem 3",                    ("subject", "coa")),
    ("give me TY papers",                          ("min", 5)),
    ("SY DBMS paper",                              ("subject", "dbms")),
    ("give me all honours papers",                 ("min", 3)),
    ("minor AI paper",                             ("subject", "ai")),
    ("PwD DS paper",                               ("subject", "ds")),
    ("give me DS paper 2021-22",                   ("subject", "ds")),
    ("give me sem 8 papers",                       ("min", 2)),
    ("give me M.Tech papers",                      ("min", 2)),
    ("papers from 2020-21",                        ("min", 5)),

    # --- subjects whose abbreviation is not yet resolved ------------------
    #     the paper must STILL be reachable by link
    ("give me ITVC paper",                         ("min", 1)),
    ("give me BCT paper",                          ("min", 1)),

    # --- honest misses ----------------------------------------------------
    ("give me ESE DBMS paper",                     ("empty", "ese_not_ingested")),
    ("give me organic chemistry paper",            ("empty", "unknown_subject")),
    ("give me all papers",                         ("empty", "no_filters")),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm", action="store_true",
                        help="also run the Qwen phrasing path")
    parser.add_argument("--verbose", action="store_true",
                        help="print every returned link")
    args = parser.parse_args()

    verify_connection()
    failures = []
    started = time.perf_counter()

    for question, (kind, expected) in QUESTIONS:
        result = retrieve(question)
        rows, filters = result["rows"], result["filters"]

        bad_links = [r for r in rows
                     if not (r.get("drive_url") or "").startswith(DRIVE_PREFIX)]
        problems = []

        if kind == "empty":
            if rows:
                problems.append(f"expected no results, got {len(rows)}")
            if result["reason"] != expected:
                problems.append(f"reason {result['reason']!r}, "
                                f"expected {expected!r}")
        else:
            if not rows:
                problems.append(f"no results (filters={filters})")
            if kind == "min" and len(rows) < expected:
                problems.append(f"{len(rows)} results, expected >= {expected}")
            if kind == "subject":
                if filters["subject_key"] != expected:
                    problems.append(f"subject_key {filters['subject_key']!r}, "
                                    f"expected {expected!r}")
                off = {r["subject_key"] for r in rows} - {expected}
                if off:
                    problems.append(f"returned other subjects: {off}")
        if bad_links:
            problems.append(f"{len(bad_links)} unusable link(s)")

        status = "FAIL" if problems else "ok  "
        print(f"  {status} {question:46} {len(rows):>3} paper(s)")
        if args.verbose and rows:
            for r in rows[:3]:
                print(f"          {r['title']}")
                print(f"          {r['drive_url']}")
            if len(rows) > 3:
                print(f"          ... and {len(rows) - 3} more")
        for p in problems:
            print(f"          -> {p}")
            failures.append(f"{question}: {p}")

    elapsed = time.perf_counter() - started
    print(f"\n{len(QUESTIONS)} questions in {elapsed:.2f}s "
          f"({elapsed / len(QUESTIONS) * 1000:.0f} ms each, no model call)")

    if args.llm:
        print("\n-- Qwen phrasing path (think=False) --")
        for question in ["Give me DBMS 2024 ISE paper", "give me all OS papers"]:
            t0 = time.perf_counter()
            out = answer_pyq_question(question, use_llm=True)
            print(f"\n  Q: {question}   [{time.perf_counter() - t0:.1f}s]")
            print("  " + out["answer"].replace("\n", "\n  "))

    print()
    if failures:
        print(f"FAILED: {len(failures)} problem(s)")
        close_driver()
        return 1
    print(f"All {len(QUESTIONS)} PYQ questions answered correctly, "
          "every link is a valid Google Drive URL.")
    close_driver()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

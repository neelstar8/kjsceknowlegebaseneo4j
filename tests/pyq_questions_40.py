"""The PYQ question bank: 40 student-style requests for question papers.

Kept separate from the runner so the same list can be reused by
tests/run_pyq_live.py (full pipeline, real Qwen3 calls) and by
tests/test_pyq_questions.py (fast deterministic assertions).

Each entry is (category, question). Categories exist so the summary can show
where any failure clusters.
"""

PYQ_QUESTIONS = [
    # --- the five shapes from the original brief ------------------------
    ("core",        "Give me all DBMS papers"),
    ("core",        "Give me DBMS paper 2024"),
    ("core",        "Give me DBMS 2024 ISE paper"),
    ("core",        "Give me all ISE papers"),
    ("core",        "Give me all ISE DBMS papers"),

    # --- abbreviation vs full subject name ------------------------------
    ("naming",      "give me OS paper"),
    ("naming",      "operating system previous year papers"),
    ("naming",      "database management system question paper"),
    ("naming",      "give me rdbms paper"),
    ("naming",      "Give me all Computer Networks papers"),
    ("naming",      "artificial intelligence papers"),
    ("naming",      "give me machine learning paper"),
    ("naming",      "soft computing question paper"),
    ("naming",      "analysis of algorithms paper"),
    ("naming",      "cryptography and system security paper"),
    ("naming",      "Flutter paper"),

    # --- year and semester filters --------------------------------------
    ("filters",     "CN 2023 paper"),
    ("filters",     "give me DS paper 2021-22"),
    ("filters",     "papers from 2020-21"),
    ("filters",     "Give me COA paper sem 3"),
    ("filters",     "give me sem 8 papers"),
    ("filters",     "AI paper sem 6"),
    ("filters",     "give me OOPM paper 2025"),

    # --- year of study and track ----------------------------------------
    ("track",       "give me TY papers"),
    ("track",       "SY DBMS paper"),
    ("track",       "give me M.Tech papers"),
    ("track",       "give me all honours papers"),
    ("track",       "minor AI paper"),
    ("track",       "PwD DS paper"),
    ("track",       "open elective papers"),

    # --- subjects whose abbreviation is not yet resolved -----------------
    #     the link must still come back
    ("unresolved",  "give me ITVC paper"),
    ("unresolved",  "give me BCT paper"),
    ("unresolved",  "give me DM paper"),

    # --- the multi-paper PDF: four papers inside one Drive file ----------
    ("multi",       "give me PSOT paper 2021-22"),
    ("multi",       "give me TACD paper"),

    # --- conversational phrasing ----------------------------------------
    ("phrasing",    "can you send me the operating systems paper please"),
    ("phrasing",    "I need last year's DBMS question paper"),
    ("phrasing",    "do you have any computer graphics papers"),

    # --- honest misses ---------------------------------------------------
    ("miss",        "give me ESE DBMS paper"),
    ("miss",        "give me organic chemistry paper"),
]

assert len(PYQ_QUESTIONS) == 40, f"expected 40 questions, got {len(PYQ_QUESTIONS)}"

"""20 student requests, chosen to exercise Drive-link retrieval.

Where tests/pyq_questions_40.py is a broad sweep of phrasing, this list is
aimed at the thing a student actually receives: the link. It walks the seven
question shapes from the ISE+ESE brief (A-G) and then pushes on the rules that
decide WHICH links come back --

    * an unqualified request must return BOTH exam types
    * "ISE ..." / "ESE ..." must narrow to one
    * only 2019-2025 is ever reachable
    * every returned link is the file's own Drive URL, never a folder
    * a subject query must never reach an unresolved semester bundle

Each entry is (category, question, note). `note` says what the answer is
supposed to demonstrate, so the generated report explains itself.
"""

PYQ_QUESTIONS_20 = [
    # --- A-G: the shapes the brief names explicitly ----------------------
    ("A. default rule", "Give me all OS papers",
     "No exam type named -> must return BOTH ISE and ESE."),
    ("B. exam filter", "Give me ISE OS papers",
     "Explicit ISE -> ISE only, a strict subset of A."),
    ("C. exam filter", "Give me ESE OS papers",
     "Explicit ESE -> ESE only."),
    ("D. default rule", "Give me all DBMS papers from 2022",
     "Year named, exam type not -> both types, 2022 only."),
    ("E. exam + year", "Give me ESE DBMS 2024 paper",
     "Narrowest shape: one subject, one type, one year."),
    ("F. exam only", "Give me all ESE papers",
     "Every mapped ESE paper, 2019-2025."),
    ("G. year range", "Give me all papers from 2019 to 2025",
     "Both exam types across the whole allowed window."),

    # --- the link itself -------------------------------------------------
    ("link", "give me Computer Networks paper",
     "Every row must carry a file-level /file/d/<id>/view URL."),
    ("link", "give me PSOT paper 2021-22",
     "A paper split across two PDFs returns both links, not one."),
    ("link", "give me TACD paper",
     "Subject shares a PDF with others; the link is that one file."),

    # --- year window -----------------------------------------------------
    ("year window", "give me OS papers from 2018",
     "Outside the window -> honest miss, never a 2013-2018 paper."),
    ("year window", "give me DBMS paper 2019",
     "First year of the window; boundary must be inclusive."),
    ("year window", "give me papers from 2025",
     "Last year of the window; boundary must be inclusive."),

    # --- subject resolution ----------------------------------------------
    ("subject", "give me rdbms paper",
     "Alias of DBMS -> same subject, same links."),
    ("subject", "operating system previous year papers",
     "Full name instead of the abbreviation."),
    ("subject", "give me ITVC paper",
     "Unresolved subject, but the link must still be reachable."),

    # --- bundles ----------------------------------------------------------
    ("bundle", "give me ESE sem 5 papers",
     "Semester-level request MAY return unresolved semester bundles."),
    ("bundle", "give me ESE Machine Learning papers",
     "Subject-level request must NEVER return a bundle."),

    # --- honest misses ----------------------------------------------------
    ("miss", "give me organic chemistry paper",
     "Subject not in the knowledge base -> say so, invent nothing."),
    ("miss", "give me all papers",
     "No filter at all -> ask for narrowing rather than dumping the corpus."),
]

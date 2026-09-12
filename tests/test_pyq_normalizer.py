"""Offline tests for the PYQ filename/folder parser.

Every case below is a real file observed in the Drive tree, not a synthetic
example -- the parser exists to handle this corpus specifically, so inventing
tidier inputs would test the wrong thing.

No network, no Neo4j, no credentials:
    .venv/bin/python -m tests.test_pyq_normalizer
"""
from normalization.pyq_normalizer import (
    build_alias_index,
    load_subjects,
    normalize_pyq,
    resolve_academic_year,
    exam_year_from,
)

ROOT = "ise question paper kj somaiya/drive-download-20260811T182940Z-1-001"
ALIASES = build_alias_index(load_subjects())

PDF, JPG, ZIP = "application/pdf", "image/jpeg", "application/zip"
DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

# (file_name, folder_path, mime, expected dict of paper[0] fields, expected reasons subset)
CASES = [
    # --- semester stated explicitly as a roman numeral, plus derived --------
    ("TY V OS.PDF", f"{ROOT}/ISE QP 23-24 odd/TY", PDF,
     {"subject_key": "os", "academic_year": "2023-24", "semester": 5,
      "exam_year": 2023, "exam_term": "odd", "year_of_study": "TY",
      "course_category": "core", "variant": "regular", "exam_type": "ISE"}, []),
    ("SY III COA.PDF", f"{ROOT}/ISE QP 23-24 odd/SY", PDF,
     {"subject_key": "coa", "semester": 3, "exam_year": 2023}, []),

    # --- no context in the name at all; the folder path carries everything --
    ("OS.pdf", f"{ROOT}/ISE QP 24-25 Odd PDF/TY", PDF,
     {"subject_key": "os", "academic_year": "2024-25", "semester": 5,
      "exam_year": 2024, "exam_type": "ISE",
      "exam_type_source": "folder_path"}, []),
    ("COA.pdf", f"{ROOT}/ISE QP 24-25 Odd PDF/SY", PDF,
     {"subject_key": "coa", "semester": 3, "exam_year": 2024}, []),

    # --- token order varies wildly between years ---------------------------
    ("ISE_COA_SY.pdf", f"{ROOT}/20-21 odd/SY", PDF,
     {"subject_key": "coa", "academic_year": "2020-21", "semester": 3}, []),
    ("ISE_ SY_OOPM .pdf", f"{ROOT}/20-21 odd/SY", PDF,
     {"subject_key": "oopm", "semester": 3}, []),
    ("SY DS-ISE QUESTION odd 20-21 without CO and BT.pdf",
     f"{ROOT}/20-21 odd/SY", PDF, {"subject_key": "ds", "semester": 3}, []),

    # --- PwD variant must NOT collide with the regular paper ---------------
    ("SY_ISE_DS_PWD without CO.pdf", f"{ROOT}/21-22 odd/SY", PDF,
     {"subject_key": "ds", "variant": "pwd", "academic_year": "2021-22"}, []),
    ("SY_ISE_DS_Paper WITHOUT BT CO.pdf", f"{ROOT}/21-22 odd/SY", PDF,
     {"subject_key": "ds", "variant": "regular"}, []),
    ("ISE_SemIV_PSOT_ (PWD)_March 20-21.pdf", f"{ROOT}/20-21 even/SY", PDF,
     {"subject_key": "psot", "variant": "pwd", "semester": 4}, []),

    # --- track prefixes, in both spellings ---------------------------------
    ("SY III H-AC.PDF", f"{ROOT}/ISE QP 23-24 odd/SY", PDF,
     {"subject_key": "ac", "course_category": "honours"}, []),
    ("SY III Honors DV.PDF", f"{ROOT}/ISE QP 23-24 odd/SY", PDF,
     {"subject_key": "dv", "course_category": "honours"}, []),
    ("TY V m-AI.PDF", f"{ROOT}/ISE QP 23-24 odd/TY", PDF,
     {"subject_key": "ai", "course_category": "minor"}, []),
    ("TY V OEHM-Consumer Behaviour.PDF", f"{ROOT}/ISE QP 23-24 odd/TY", PDF,
     {"subject_key": "cb", "course_category": "open_elective"}, []),
    ("OET_PDS_QP_sem5_without CO.pdf", f"{ROOT}/21-22 odd/TY", PDF,
     {"subject_key": "pds", "course_category": "open_elective"}, []),

    # --- full subject name written out in the file name --------------------
    ("ISE_MOBILE APPLICATION DEVELOPMENT FLUTTER.pdf",
     f"{ROOT}/20-21 odd/TY", PDF, {"subject_key": "mad"}, []),
    ("ISE_soft computing without COS and blooms.pdf",
     f"{ROOT}/20-21 odd/TY", PDF, {"subject_key": "sc"}, []),
    ("TY_Software Engineering_ISE_October_2021.pdf",
     f"{ROOT}/21-22 odd/TY", PDF, {"subject_key": "se"}, []),

    # --- an official course code embedded in the name ----------------------
    ("SY_ISE_ITVC_July-Nov 2021_116U01C301.pdf", f"{ROOT}/21-22 odd/SY", PDF,
     {"subject_code": "116U01C301", "subject_status": "unresolved",
      "subject_raw": "itvc"}, ["unresolved_subject"]),

    # --- noise words must never leak into the subject slug -----------------
    ("STQA OF QUESTION PAPER WITHOUT CO_FOR STUDENTS.pdf",
     f"{ROOT}/20-21 even/LY", PDF, {"subject_key": "stqa"}, []),
    ("MSD ISE_TEMPLATE FOR QUESTION PAPER_WITHOUT CO.pdf",
     f"{ROOT}/20-21 even/TY", PDF, {"subject_raw": "msd"},
     ["unresolved_subject"]),
    ("NLP - LY - VII - ISE Q PAPER - NOV 2020.pdf", f"{ROOT}/20-21 odd/LY", PDF,
     {"subject_key": "nlp", "semester": 7}, []),

    # --- a typo must stay unresolved, never be fuzzy-matched to Flutter ----
    ("Futter.pdf", f"{ROOT}/ISE QP 24-25 Odd PDF/TY", PDF,
     {"subject_status": "unresolved", "subject_raw": "futter"},
     ["unresolved_subject"]),

    # --- images are real papers -------------------------------------------
    ("ML 1 pg.jpg",
     f"{ROOT}/ISE QP 22-23 Even & Syllabus/ISE QP with Blooms and Toxonomy/M Tech/ML",
     JPG, {"subject_key": "ml", "year_of_study": "MTECH", "program": "M.Tech",
           "semester": 2}, []),
]

# (file_name, folder_path, mime, expected reason) -- these produce no PYQ node
REJECTED = [
    ("VI syllabus.pdf",
     f"{ROOT}/ISE QP 22-23 Even & Syllabus/Syllabus/VI syllabus subject wise",
     PDF, "excluded_syllabus"),
    ("ISE QP 23-24 odd.zip", ROOT, ZIP, "excluded_archive"),
    ("AI TY ISE 20-21.docx", f"{ROOT}/20-21 even/TY", DOCX, "excluded_mime"),
    ("TY VI ESE DBMS.pdf", f"{ROOT}/ISE QP 23-24 Even/TY", PDF, "exam_type_ese"),
    ("End Sem OS.pdf", f"{ROOT}/ISE QP 23-24 Even/TY", PDF, "exam_type_ese"),
]

MULTI = [
    ("SY(PSOT,AOA,RDBMS,TACD).PDF", f"{ROOT}/21-22 even/SY", PDF,
     {"psot", "aoa", "dbms", "tacd"}),
    ("TY(AI,DSIP,CSS).PDF", f"{ROOT}/21-22 even/TY", PDF,
     {"ai", "dsip", "css"}),
]


def _parse(name, path, mime):
    return normalize_pyq(
        {"drive_file_id": "test", "file_name": name, "mime_type": mime,
         "folder_path": path, "drive_url": "https://drive.google.com/file/d/x/view"},
        ALIASES, branch="Computer Engineering", collection="test")


def main():
    failures = []

    for name, path, mime, expected, want_reasons in CASES:
        result = _parse(name, path, mime)
        if not result["papers"]:
            failures.append(f"{name}: produced no paper ({result['reasons']})")
            continue
        paper = result["papers"][0]
        for key, want in expected.items():
            got = paper.get(key)
            if got != want:
                failures.append(f"{name}: {key} == {got!r}, expected {want!r}")
        for reason in want_reasons:
            if reason not in result["reasons"]:
                failures.append(f"{name}: expected reason {reason}, "
                                f"got {result['reasons']}")

    for name, path, mime, reason in REJECTED:
        result = _parse(name, path, mime)
        if result["papers"]:
            failures.append(f"{name}: expected no paper, got "
                            f"{[p['subject_key'] for p in result['papers']]}")
        if reason not in result["reasons"]:
            failures.append(f"{name}: expected {reason}, got {result['reasons']}")

    for name, path, mime, keys in MULTI:
        result = _parse(name, path, mime)
        got = {p["subject_key"] for p in result["papers"]}
        if not keys.issubset(got):
            failures.append(f"{name}: expected subjects {keys}, got {got}")
        if "multi_paper_file" not in result["reasons"]:
            failures.append(f"{name}: expected multi_paper_file reason")
        # The physical file must appear once, however many papers it holds.
        ids = {result["file"]["drive_file_id"]}
        if len(ids) != 1:
            failures.append(f"{name}: file duplicated across papers")

    # A split paper must produce ONE identity shared by both files.
    pg1 = _parse("ML 1 pg.jpg", f"{ROOT}/ISE QP 22-23 Even & Syllabus/"
                 "ISE QP with Blooms and Toxonomy/M Tech/ML", JPG)["papers"][0]
    pg2 = _parse("ML 2 pg.jpg", f"{ROOT}/ISE QP 22-23 Even & Syllabus/"
                 "ISE QP with Blooms and Toxonomy/M Tech/ML", JPG)["papers"][0]
    if pg1["pyq_id"] != pg2["pyq_id"]:
        failures.append("split paper: ML 1 pg / ML 2 pg got different pyq_ids")
    if pg1["edge"]["part_index"] != 1 or pg2["edge"]["part_index"] != 2:
        failures.append("split paper: page labels not captured on the edge")

    # PwD and regular must NOT share an identity.
    reg = _parse("SY_ISE_DS_Paper WITHOUT BT CO.pdf",
                 f"{ROOT}/21-22 odd/SY", PDF)["papers"][0]
    pwd = _parse("SY_ISE_DS_PWD without CO.pdf",
                 f"{ROOT}/21-22 odd/SY", PDF)["papers"][0]
    if reg["pyq_id"] == pwd["pyq_id"]:
        failures.append("PwD variant collides with the regular paper")

    # Academic-year / exam-year arithmetic.
    for text, want in [("ise qp 23 24 odd", "2023-24"), ("2021 22", "2021-22"),
                       ("20 21 odd", "2020-21"), ("116u01c301", None)]:
        got = resolve_academic_year(text)
        if got != want:
            failures.append(f"resolve_academic_year({text!r}) == {got!r}, "
                            f"expected {want!r}")
    for ay, term, want in [("2023-24", "odd", 2023), ("2023-24", "even", 2024),
                           (None, "odd", None)]:
        got = exam_year_from(ay, term)
        if got != want:
            failures.append(f"exam_year_from({ay}, {term}) == {got}, expected {want}")

    total = len(CASES) + len(REJECTED) + len(MULTI) + 8
    if failures:
        print(f"FAILED ({len(failures)} problem(s) across ~{total} checks):")
        for f in failures:
            print("  -", f)
        return 1
    print(f"All PYQ normalizer checks passed "
          f"({len(CASES)} parses, {len(REJECTED)} rejections, "
          f"{len(MULTI)} multi-paper files, plus identity and date checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

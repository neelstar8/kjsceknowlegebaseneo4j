"""Phase 7: realistic KJ GPT policy questions, end to end against the graph.

Every question either resolves to sourced provisions or is answered honestly
as "not in the documents I hold". The ones marked expect_found=False are the
point of the file: they are questions a student will genuinely ask that this
corpus cannot answer, and the system must say so rather than invent a number.

    .venv/bin/python -m tests.test_policy_questions
    .venv/bin/python -m tests.test_policy_questions --verbose
"""
import argparse
import sys
import time

from graph.neo4j_driver import close_driver, verify_connection
from services.policy_service import answer_policy_question

# (question, expect_found, a phrase that must appear when found)
QUESTIONS = [
    # --- the user's named test questions ---
    ("What is the examination policy?", True, "CBCGS"),
    ("What are the examination rules?", True, "examination"),
    ("What is the procedure for revaluation?", True, "revaluation"),
    ("What is the attendance requirement?", True, "75"),
    ("What are the library rules?", True, "library"),
    ("What is the placement policy?", True, "placement"),
    ("What is the student welfare policy?", True, "cells"),
    ("What is the IT policy?", True, "SVVNetID"),

    # --- who / what / what-if shapes ---
    ("Who approves new programs of study?", True, "Governing Body"),
    ("Who is responsible for the examination hall?", True, "Supervisor"),
    ("What documents are required for admission?", True, "medical fitness"),
    ("What documents do I need for a leaving certificate?", True, "no dues"),
    ("What happens if my attendance is below 75 percent?", True, "defaulter"),
    ("What happens if I am caught copying in an exam?", True, "unfair means"),
    ("What happens if I lose a library book?", True, "replace"),
    ("What happens if I back out of a placement process?", True, "action"),

    # --- numbers a student actually asks for ---
    ("How many books can I borrow from the library?", True, "6"),
    ("What are the library timings?", True, "8.00"),
    ("How much is the revaluation fee?", True, "500"),
    ("What is the ATKT rule?", True, "heads"),
    ("How many grace marks can I get for sports?", True, "10"),
    ("What is the minimum attendance for grant of term?", True, "75"),
    ("What is the minimum percentage to pass?", True, "40"),
    ("How long does a bonafide certificate take?", True, "one day"),
    ("What is the hostel timing?", True, "9.00"),
    ("How much is the alumni library membership deposit?", True, "1,500"),
    ("What is the faculty development grant amount?", True, "15,000"),
    ("What is the M.Tech eligibility?", True, "50%"),

    # --- procedures ---
    ("How do I apply for a scholarship?", True, "Student Section"),
    ("How do I get a new ID card if I lost it?", True, "FIR"),
    ("How do I apply for railway concession?", True, "concession"),
    ("How do I file a grievance?", True, "Grievance"),
    ("How do I report ragging?", True, "Anti-Ragging"),
    ("How do I join a club or cell?", True, "interview"),
    ("What is the procedure for hostel admission?", True, "request letter"),
    ("How do I complain about sexual harassment?", True, "CWDC"),

    # --- policy areas ---
    ("What is the anti plagiarism policy?", True, "Plagiarism"),
    ("What is the disciplinary policy?", True, "discipline"),
    ("What is the dress code?", True, "sleeveless"),
    ("What are the lab rules?", True, "ID card"),
    ("What is the infrastructure policy?", True, "Estate"),
    ("What is the consultancy policy?", True, "Consultancy"),
    ("What is the leave policy for staff?", True, "Casual Leave"),
    ("What is the PhD study leave policy?", True, "study leave"),
    ("What is the retirement age?", True, "60"),
    ("What is the fee collection policy?", True, "My Account"),

    # --- gaps: the corpus has no answer, and says so in the graph rather than
    # --- staying silent. These must surface the recorded gap, never a number.
    ("What is the attendance condonation procedure?", True,
     "No attendance condonation"),
    ("Can I get medical exemption from attendance?", True,
     "medical exemption"),
    ("How many internship credits do I need to graduate?", True,
     "NO internship policy"),
    ("What is the library fine per day for students?", True,
     "NOT SPECIFIED IN SOURCE"),
    ("What is the holiday list?", True, "University Circulars"),

    ("What is the fee refund policy if I leave mid-year?", True,
     "NOT SPECIFIED IN SOURCE"),
    ("What is the academic calendar for 2026-27?", True,
     "NOT SPECIFIED IN SOURCE"),

    # --- nothing in the corpus is even close; the system must decline ---
    ("What is Vaibhav Vasani's favorite food?", False, ""),
    ("What is the cafeteria menu?", False, ""),
    ("Who won the cricket match yesterday?", False, ""),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    verify_connection()
    passed = failed = 0
    misses = []
    started = time.time()

    for question, expect_found, phrase in QUESTIONS:
        t0 = time.perf_counter()
        result = answer_policy_question(question)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        found = result["found"]
        ok = found == expect_found
        if ok and expect_found and phrase:
            ok = phrase.lower() in result["answer"].lower()
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1
            misses.append((question, expect_found, found, phrase))
        label = "answered" if found else "honest miss"
        print(f"  [{status}] {elapsed_ms:6.1f}ms  {label:<12} {question}")
        if args.verbose:
            print("      " + result["answer"].replace("\n", "\n      ")[:1200])
            print()

    total_ms = (time.time() - started) * 1000
    print(f"\n  {passed}/{len(QUESTIONS)} passed in {total_ms:.0f}ms "
          f"({total_ms / len(QUESTIONS):.0f}ms average)")
    if misses:
        print("\n  failures:")
        for question, expect_found, found, phrase in misses:
            print(f"    {question}\n      expected found={expect_found}, got {found}"
                  + (f", required phrase {phrase!r}" if phrase else ""))
    close_driver()
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

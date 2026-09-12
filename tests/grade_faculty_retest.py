"""Applies the manual verdicts to faculty_retest_results.jsonl and prints the summary.

Every verdict below was assigned by checking the answer against the exact
`neo4j_context` string that was sent to Qwen for that question. Read-only.
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "faculty_retest_results.jsonl"
GRADED = ROOT / "faculty_retest_graded.jsonl"

VERDICTS = {
    1: ("PASS", "All three degrees returned verbatim from Education."),
    2: ("PASS", "Returned the exact cv_url."),
    3: ("PASS", "Returned the exact vidwan_url."),
    4: ("PASS", "Returned the Qualifications list."),
    5: ("PASS", "Returned the exact google_scholar_url."),
    6: ("MISSING_DATA_CORRECTLY_HANDLED",
        "No vidwan_url in context; said so. Minor: then volunteered profile URL + CV link."),
    7: ("PASS", "All three professional_experience entries, correct dates."),
    8: ("PASS", "All seven subjects_taught listed."),
    9: ("PASS", "Correct official_email, nothing else."),
    10: ("PASS", "PhD IITB 2009 read correctly out of the Education string."),
    11: ("WRONG_FIELD",
         "cv_url is absent. Instead of saying so, Qwen assembled a CV from the whole profile dump."),
    12: ("MISSING_DATA_CORRECTLY_HANDLED", "No education in context; said so plainly."),
    13: ("PASS", "Correct official_email."),
    14: ("PASS", "Correct designation."),
    15: ("MISSING_DATA_CORRECTLY_HANDLED",
         "No google_scholar_url in context; said so. Minor: pointed to external search."),
    16: ("PASS", "All three awards, verbatim."),
    17: ("PASS", "Image Processing, correct."),
    18: ("PASS", "PhD NMIMS 2020, correct."),
    19: ("PASS", "Correct linkedin_url."),
    20: ("PASS", "Correct orcid_url."),
    21: ("PASS", "16+ years matches total_teaching_experience."),
    22: ("PASS", "Patent title, application no. and inventors all match the context."),
    23: ("PASS", "Publications listed are all present in the 16.7k-char context."),
    24: ("FAIL",
         "Education IS in the context at char 805, but Qwen said it is not mentioned and "
         "told the student to contact the college. 12.6k-char context."),
    25: ("FAIL",
         "vidwan_url IS in the context at char 670, but Qwen said no link is included and "
         "guessed at what 'Vidwan' might mean."),
    26: ("PASS", "Both specialisation areas returned."),
    27: ("PASS", "Correct cv_url."),
    28: ("PASS", "Correct office_address."),
    29: ("PASS", "Correct phone; correctly noted no mobile number is listed."),
    30: ("PASS", "Correct department."),
    31: ("PASS", "Both books with correct publishers and years."),
    32: ("MISSING_DATA_CORRECTLY_HANDLED", "No orcid_url in context; single clean sentence."),
    33: ("MISSING_DATA_CORRECTLY_HANDLED", "No linkedin_url in context; said so."),
    34: ("PASS", "Three prior employers, correctly excluding the current KJSSE role."),
    35: ("MISSING_DATA_CORRECTLY_HANDLED",
         "No subjects_taught; said so and cited the expertise line, which is in the Introduction."),
    36: ("PASS", "'Twenty seven years' and every other detail traceable to the context."),
    37: ("FAIL",
         "visiting_hours IS in the context at char 450, but Qwen claimed the data contains no "
         "reference to Rajesh Pansare at all. 14.8k-char context."),
    38: ("PASS",
         "research_interests is absent, but every claim comes from the Introduction and "
         "publication titles in the context."),
    39: ("MISSING_DATA_CORRECTLY_HANDLED", "No qualifications in context; said so."),
    40: ("PASS", "Specialisation list matches research_specialization."),
}


def strip_think(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text or "", flags=re.S).strip()


def main():
    rows = [json.loads(line) for line in RESULTS.read_text().splitlines() if line.strip()]

    with GRADED.open("w") as fh:
        for r in rows:
            verdict, note = VERDICTS[r["question_number"]]
            r["answer_clean"] = strip_think(r.get("answer") or "")
            r["verdict"] = verdict
            r["verdict_note"] = note
            r["context_chars"] = len(r.get("neo4j_context") or "")
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    counts = Counter(r["verdict"] for r in rows)
    times = [r["response_time_ms"] for r in rows]

    print(f"Total questions: {len(rows)}\n")
    for label in ("PASS", "MISSING_DATA_CORRECTLY_HANDLED", "FAIL", "HALLUCINATION",
                  "WRONG_FACULTY", "WRONG_FIELD", "IRRELEVANT_RESPONSE", "ERROR"):
        print(f"{label}: {counts.get(label, 0)}")

    print(f"\nAverage response time: {sum(times) // len(times)} ms")
    print(f"Median / min / max: {sorted(times)[len(times) // 2]} / {min(times)} / {max(times)} ms")
    print(f"Correct faculty retrieved: {sum(1 for r in rows if r['retrieved_faculty'] == r['expected_faculty'])}/{len(rows)}")
    print(f"\nGraded results: {GRADED}")


if __name__ == "__main__":
    main()

"""Read-only retest of the current Neo4j retrieval + Qwen3 8B faculty pipeline.

Runs 40 realistic student-style questions one at a time through the live
`answer_faculty_question` service, appending each result to a JSONL file
immediately so a crash never loses completed work.

Nothing here writes to Neo4j.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from graph.neo4j_driver import run_query, verify_connection  # noqa: E402
from llm.qwen import verify_ollama  # noqa: E402
from services.faculty_service import answer_faculty_question  # noqa: E402

RESULTS_PATH = Path(__file__).resolve().parents[1] / "faculty_retest_results.jsonl"

# (question, expected faculty name or None, the node property the question asks for)
QUESTIONS = [
    ("what is the education of smita sankhe", "Dr. Smita Ramesh Sankhe", "education"),
    ("give me cv of kirti mishra", "Ms. Kirti Dilip Mishra", "cv_url"),
    ("give me vidwan profile link of kirti mishra", "Ms. Kirti Dilip Mishra", "vidwan_url"),
    ("what is qualification of smita sankhe", "Dr. Smita Ramesh Sankhe", "qualifications"),
    ("smita sankhe google scholar", "Dr. Smita Ramesh Sankhe", "google_scholar_url"),
    ("give me smita sankhe vidwan profile", "Dr. Smita Ramesh Sankhe", "vidwan_url"),
    ("what is kirti mishra experience", "Ms. Kirti Dilip Mishra", "professional_experience"),
    ("what subjects does kirti mishra teach", "Ms. Kirti Dilip Mishra", "subjects_taught"),
    ("kirti mishra email id", "Ms. Kirti Dilip Mishra", "official_email"),
    ("where did ramesh karandikar do his phd", "Dr. Ramesh Gopal Karandikar", "education"),
    ("give me cv of ramesh karandikar", "Dr. Ramesh Gopal Karandikar", "cv_url"),
    ("what is the education of minendra surve", "Dr. Minendra Laxman Surve", "education"),
    ("minendra surve email", "Dr. Minendra Laxman Surve", "official_email"),
    ("what is prasanna raut current designation", "Dr. Prasanna Pramod Raut", "designation"),
    ("give me google scholar of prasanna shete", "Dr. Prasanna Jaichand Shete", "google_scholar_url"),
    ("what awards has ashwini dalvi received", "Dr. Ashwini Anant Dalvi", "awards"),
    ("bhakti palkar research area", "Dr. Bhakti Nilesh Palkar", "research_interests"),
    ("what is bhakti palkar highest qualification", "Dr. Bhakti Nilesh Palkar", "qualifications"),
    ("give me linkedin of vaibhav vasani", "Dr. Vaibhav Prakash Vasani", "linkedin_url"),
    ("vaibhav vasani orcid", "Dr. Vaibhav Prakash Vasani", "orcid_url"),
    ("how many years of experience does vaibhav vasani have", "Dr. Vaibhav Prakash Vasani", "total_teaching_experience"),
    ("what patents does deepak sharma have", "Dr. Deepak Hemandas Sharma", "patents"),
    ("give me publications of sonali patil", "Dr. Sonali Atulkumar Patil", "publications"),
    ("where did sujata pathak study", "Dr. Sujata Prasad Pathak", "education"),
    ("sujata pathak vidwan link", "Dr. Sujata Prasad Pathak", "vidwan_url"),
    ("what is ankita nagmote research specialization", "Dr. Ankita Salil Nagmote", "research_specialization"),
    ("give me cv of ankita nagmote", "Dr. Ankita Salil Nagmote", "cv_url"),
    ("what is the office address of jyoti joglekar", "Dr. Jyoti Vishnu Joglekar", "office_address"),
    ("phone number of grishma sharma", "Dr. Grishma Jaideep Sharma", "phone"),
    ("which department is mansi kambli from", "Dr. Mansi Manoj Kambli", "department"),
    ("what books has mansi kambli written", "Dr. Mansi Manoj Kambli", "books"),
    ("give me the orcid of smita sankhe", "Dr. Smita Ramesh Sankhe", "orcid_url"),
    ("what is linkedin of kirti mishra", "Ms. Kirti Dilip Mishra", "linkedin_url"),
    ("where did rina bora work before joining kj somaiya", "Dr. Rina Kamalkumar Bora", "professional_experience"),
    ("shruti javkar subjects taught", "Dr. Shruti Nilesh Javkar", "subjects_taught"),
    ("who is dr shailesh nikam", "Dr. Shailesh Ravindra Nikam", None),
    ("what are the visiting hours of rajesh pansare", "Dr. Rajesh Balasaheb Pansare", "visiting_hours"),
    ("what is pankaj mishra research interest", "Dr. Pankaj Prakash Mishra", "research_interests"),
    ("abhishek mishra qualification", "Mr. Abhishek Mishra", "qualifications"),
    ("what is siddappa bhusnoor specialization", "Dr. Siddappa Sharnappa Bhusnoor", "research_specialization"),
]


def ground_truth(name: str | None, field: str | None):
    """Read-only lookup of the single property the question asks about."""
    if not name or not field:
        return None
    rows = run_query(
        "MATCH (f:FacultyMember {name: $name}) RETURN f[$field] AS value",
        {"name": name, "field": field},
    )
    return rows[0]["value"] if rows else None


def main():
    verify_connection()
    verify_ollama()

    RESULTS_PATH.write_text("")
    total = len(QUESTIONS)

    for i, (question, expected_name, field) in enumerate(QUESTIONS, start=1):
        print(f"[{i}/{total}] Running: {question}", flush=True)
        started = time.perf_counter()
        record = {
            "question_number": i,
            "question": question,
            "expected_faculty": expected_name,
            "expected_field": field,
        }
        try:
            trace = answer_faculty_question(question, debug=True)
            elapsed = int((time.perf_counter() - started) * 1000)
            record.update({
                "strategy": trace.get("strategy"),
                "retrieved_faculty": trace.get("match"),
                "result_count": trace.get("result_count"),
                "neo4j_context": trace.get("context"),
                "field_value_in_neo4j": ground_truth(expected_name, field),
                "answer": trace.get("answer"),
                "response_time_ms": elapsed,
                "status": "success",
                "error": None,
            })
            print(f"[{i}/{total}] Completed ({elapsed} ms)", flush=True)
        except Exception as e:  # noqa: BLE001 - a failure must not stop the run
            elapsed = int((time.perf_counter() - started) * 1000)
            record.update({
                "strategy": None,
                "retrieved_faculty": None,
                "result_count": 0,
                "neo4j_context": None,
                "field_value_in_neo4j": None,
                "answer": None,
                "response_time_ms": elapsed,
                "status": "error",
                "error": f"{type(e).__name__}: {e}",
            })
            print(f"[{i}/{total}] ERROR: {type(e).__name__}: {e}", flush=True)

        with RESULTS_PATH.open("a") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            fh.flush()

    print(f"\nAll {total} questions completed. Results: {RESULTS_PATH}", flush=True)


if __name__ == "__main__":
    main()

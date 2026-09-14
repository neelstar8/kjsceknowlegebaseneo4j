"""Batch test: 30 student-style questions about Dr. Vaibhav Prakash Vasani.

Run with:
    python -m tests.batch_30_questions

For each question, times the full pipeline (Neo4j retrieval + Qwen3 8B answer)
and prints question, response time, and answer. Writes a summary table at the
end. A few questions are deliberately out-of-scope to confirm no hallucination.
"""
import time

from graph.neo4j_driver import verify_connection, close_driver
from llm.qwen import verify_ollama
from llm.system_prompt import KJGPT_FACULTY_SYSTEM_PROMPT
from services.faculty_service import answer_faculty_question

STUDENT_QUESTIONS = [
    "Who is Vaibhav Vasani sir?",
    "Which department is Vaibhav Vasani sir from?",
    "What is Vaibhav Vasani sir's designation?",
    "Is Vaibhav Vasani sir a professor or assistant professor?",
    "What is his official email id?",
    "Where can I find his faculty profile page?",
    "What subjects does he teach in computer engineering?",
    "Does he teach Data Structures?",
    "Does he teach any AI or ML related subject?",
    "What are his educational qualifications?",
    "Does he have a PhD?",
    "Where did he complete his PhD from?",
    "What is his highest degree and in which year did he complete it?",
    "How many years of teaching experience does he have?",
    "When did he join Somaiya?",
    "Where did he work before joining K J Somaiya School of Engineering?",
    "What are his research interests?",
    "What is he specialized in research-wise?",
    "What tools and technologies does he know?",
    "What programming languages does he know?",
    "Is he good in Python?",
    "What responsibilities does he handle in the department?",
    "Is he the coordinator of any club or cell?",
    "What awards has he received?",
    "Has he won any hackathon?",
    "Can you list a few of his research publications?",
    "What is his Google Scholar profile link?",
    "What is his LinkedIn profile link?",
    "Is he a member of ACM or any professional body?",
    "What is Vaibhav Vasani sir's favorite cricket team?",
]

assert len(STUDENT_QUESTIONS) == 30, f"expected 30 questions, got {len(STUDENT_QUESTIONS)}"


def main():
    print("Checking Neo4j connection...")
    verify_connection()
    print("Neo4j OK.\n")

    print("Checking Ollama + Qwen3...")
    verify_ollama()
    print("Ollama OK.\n")

    print("=" * 70)
    print("SYSTEM PROMPT USED FOR EVERY QUESTION")
    print("=" * 70)
    print(KJGPT_FACULTY_SYSTEM_PROMPT)
    print("=" * 70)
    print()

    results = []
    for i, question in enumerate(STUDENT_QUESTIONS, start=1):
        start = time.perf_counter()
        trace = answer_faculty_question(question, debug=False)
        elapsed = time.perf_counter() - start

        answer = trace["answer"]
        results.append((i, question, elapsed, answer))

        print(f"[{i:02d}/30] ({elapsed:.2f}s) Q: {question}")
        print(f"        A: {answer}")
        print("-" * 70)

    close_driver()

    total_time = sum(r[2] for r in results)
    avg_time = total_time / len(results)
    fastest = min(results, key=lambda r: r[2])
    slowest = max(results, key=lambda r: r[2])

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Questions asked:      {len(results)}")
    print(f"Total time:           {total_time:.2f}s")
    print(f"Average response time: {avg_time:.2f}s")
    print(f"Fastest: [{fastest[0]:02d}] {fastest[2]:.2f}s - {fastest[1]}")
    print(f"Slowest: [{slowest[0]:02d}] {slowest[2]:.2f}s - {slowest[1]}")
    print()
    print(f"{'#':<4}{'Time (s)':<10}Question")
    print("-" * 70)
    for i, question, elapsed, _ in results:
        print(f"{i:<4}{elapsed:<10.2f}{question}")


if __name__ == "__main__":
    main()

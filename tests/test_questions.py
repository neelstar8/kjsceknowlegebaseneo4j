"""Manual test/debug script for the KJGPT prototype.

Run with:
    python -m tests.test_questions

Prints the full pipeline trace (question -> Cypher -> Neo4j result -> context
-> Qwen answer) for a fixed list of test questions, including one question
whose answer is NOT in the knowledge base (to verify no hallucination).
"""
from graph.neo4j_driver import verify_connection, close_driver
from llm.qwen import verify_ollama
from services.faculty_service import answer_faculty_question

TEST_QUESTIONS = [
    "Who is Vaibhav V. Vasani?",
    "What is Vaibhav V. Vasani's designation?",
    "Which department does he belong to?",
    "What subjects does he teach?",
    "What are his qualifications?",
    "What are his research interests?",
    "Tell me everything available about Vaibhav V. Vasani.",
    "What is Vaibhav V. Vasani's favorite food?",  # not in DB -- must not hallucinate
]


def print_section(title, content):
    print("-" * 34)
    print(title)
    print("-" * 34)
    print(content)
    print()


def main():
    print("Checking Neo4j connection...")
    verify_connection()
    print("Neo4j OK.\n")

    print("Checking Ollama + Qwen3...")
    verify_ollama()
    print("Ollama OK.\n")

    for question in TEST_QUESTIONS:
        trace = answer_faculty_question(question, debug=True)
        print_section("USER QUESTION", trace["question"])
        print_section("NEO4J QUERY", trace.get("query") or "(no query run)")
        print_section("NEO4J RESULT", trace.get("result"))
        print_section("CONTEXT SENT TO QWEN3", trace.get("context"))
        print_section("QWEN3 ANSWER", trace.get("answer"))
        print("=" * 60)
        print()

    close_driver()


if __name__ == "__main__":
    main()

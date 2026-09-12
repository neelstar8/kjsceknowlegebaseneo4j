"""End-to-end check of the faculty RAG path:

    question -> deterministic Neo4j retrieval -> context -> Qwen3 8B -> answer

Qwen is only ever given retrieved context; it never generates Cypher and is
instructed to answer strictly from that context.

Usage:
    python -m scripts.test_faculty_rag
    python -m scripts.test_faculty_rag "Who is Vaibhav Vasani?"
"""
import sys

from graph.neo4j_driver import close_driver, verify_connection
from llm.qwen import verify_ollama
from services.faculty_service import answer_faculty_question

DEFAULT_QUESTIONS = [
    "Who is Vaibhav Vasani?",
    "Who teaches in the Computer Engineering department?",
    "Which faculty members are Assistant Professors?",
    "Which faculty members have Machine Learning as a research interest?",
    "Tell me about Dr. Abhishek Ghosh.",
    "What is the phone number of the Vice Chancellor's dog?",
]


def main():
    questions = sys.argv[1:] or DEFAULT_QUESTIONS

    verify_connection()
    verify_ollama()

    for question in questions:
        print("=" * 74)
        print("Q:", question)
        print("-" * 74)
        trace = answer_faculty_question(question, debug=True)
        print(f"[retrieval: strategy={trace['strategy']} "
              f"match={trace['match']!r} results={trace['result_count']}]")
        print()
        print(trace["answer"])
        print()

    close_driver()


if __name__ == "__main__":
    main()

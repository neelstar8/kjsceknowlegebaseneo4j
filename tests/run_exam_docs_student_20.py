"""20 student-persona questions against the Examination document knowledge.

Writes tests/../EXAM_DOCS_STUDENT_TEST_LIVE.md incrementally -- one row per
completed question, while the run is in progress -- so the file can be watched
live. Same rhythm as POLICY_LLM_LIVE_TEST.md.

Each question is run twice:
  RETRIEVAL  services.exam_document_service (deterministic, no model call).
             This is what the production route returns.
  LLM        the same retrieved text handed to Qwen under the Policy-domain
             system prompt stored on :PolicyHandbook -- the prompt carrying the
             LINK HANDLING rule -- to show what a student actually reads.

    .venv/bin/python -m tests.run_exam_docs_student_20
"""
import time
from datetime import datetime

from graph.neo4j_driver import close_driver, verify_connection
from graph.policy_queries import handbook_system_prompt
from llm.qwen import ask_qwen, verify_ollama
from services.exam_document_service import answer_exam_document_question

OUT = "EXAM_DOCS_STUDENT_TEST_LIVE.md"

# A student asking real things, including the questions this corpus must refuse
# or qualify rather than answer smoothly.
QUESTIONS = [
    ("What examination documents do you have?", "broad listing"),
    ("Show me all the examination calendars.", "broad listing"),
    ("Where do I download examination forms?", "empty section - must say so"),
    ("What's the academic and examination calendar for 2026-27?", "specific year"),
    ("Give me the 2023-24 exam calendar.", "specific year"),
    ("Is there an exam calendar for B.Tech?", "programme filter"),
    ("I'm an M.Tech student, which calendars apply to me?", "programme filter"),
    ("When is the ESE in the 2026-27 calendar?", "dated event lookup"),
    ("When is the mid-semester exam in 2026-27?", "dated event lookup"),
    ("When do results come out for 2026-27?", "dated event lookup"),
    ("Is the 2026-27 calendar final or just proposed?", "must flag proposed/tentative"),
    ("When are the Diwali holidays in 2026-27?", "dated event lookup"),
    ("Is there a calendar for direct second year (DSY) students?", "DSY edge case"),
    ("When is the supplementary exam for SY B.Tech 2021-22?", "supplementary window"),
    ("Do you have an exam calendar for 2019-20?", "year we do NOT hold - must refuse"),
    ("What's the exam calendar for 2030-31?", "year we do NOT hold - must refuse"),
    ("Were exams online during covid? What was the paper pattern?", "2020-21 mode details"),
    ("I'm FY B.Tech 2021-22, my even semester dates changed - which calendar is right?",
     "revised vs new-batch ambiguity"),
    ("When does internship happen according to the 2026-27 calendar?", "internship rows in calendar"),
    ("Give me previous year question papers for DBMS.", "must NOT return calendars - wrong system"),
]


def header(n):
    return (
        "# KJ GPT - Examination Documents: 20 Student Questions (LIVE)\n\n"
        f"**Started:** {datetime.now().isoformat(timespec='seconds')}  \n"
        "**Retrieval:** `services.exam_document_service` - deterministic, Neo4j only, no model call.  \n"
        "**LLM:** `qwen3:8b` via Ollama, using the Policy-domain system prompt stored on "
        "`(:PolicyHandbook).system_prompt` (the one carrying the LINK HANDLING rule).  \n"
        "**Data/code/prompts:** untouched - testing only.\n\n"
        "## Progress\n\n"
        f"- Completed: 0 / {n}\n- Status: RUNNING\n\n---\n\n"
    )


def main():
    verify_connection()
    verify_ollama()
    system_prompt = handbook_system_prompt()

    body = []
    n = len(QUESTIONS)

    def flush(done, status="RUNNING", elapsed=None):
        head = (
            "# KJ GPT - Examination Documents: 20 Student Questions (LIVE)\n\n"
            f"**Started:** {START}  \n"
            "**Retrieval:** `services.exam_document_service` - deterministic, Neo4j only, no model call.  \n"
            "**LLM:** `qwen3:8b` via Ollama, using the Policy-domain system prompt stored on "
            "`(:PolicyHandbook).system_prompt` (the one carrying the LINK HANDLING rule).  \n"
            "**Data/code/prompts:** untouched - testing only.\n\n"
            "## Progress\n\n"
            f"- Completed: **{done} / {n}**\n"
            f"- Status: **{status}**\n"
        )
        if elapsed is not None:
            head += f"- Elapsed: {elapsed:.0f}s\n"
        head += "\n---\n\n"
        with open(OUT, "w", encoding="utf-8") as fh:
            fh.write(head + "".join(body))

    START = datetime.now().isoformat(timespec="seconds")
    flush(0)
    t_run = time.time()

    for i, (q, intent) in enumerate(QUESTIONS, 1):
        t0 = time.time()
        det = answer_exam_document_question(q, debug=True)
        t_det = (time.time() - t0) * 1000

        context = det["answer"]
        t1 = time.time()
        try:
            llm = ask_qwen(
                system_prompt,
                f"RETRIEVED POLICY PROVISIONS:\n{context}\n\nSTUDENT QUESTION:\n{q}",
                think=False, timeout=240,
            )
            err = None
        except Exception as e:  # keep the run going; record the failure
            llm, err = "", repr(e)
        t_llm = time.time() - t1

        n_docs = len(det["documents"])
        links = context.count("](http")
        llm_links = llm.count("](http")
        bad = "example.com" in llm

        body.append(
            f"## Q{i}. {q}\n\n"
            f"*What this probes:* {intent}\n\n"
            f"| | |\n|---|---|\n"
            f"| Documents retrieved | {n_docs} |\n"
            f"| Retrieval time | {t_det:.1f} ms |\n"
            f"| LLM time | {t_llm:.1f} s |\n"
            f"| Markdown links in retrieval | {links} |\n"
            f"| Markdown links in LLM answer | {llm_links} |\n"
            f"| Fabricated example.com link | {'YES - BAD' if bad else 'no'} |\n"
            f"| Filters | `{det['debug']['filters']}` |\n\n"
            f"**KJ GPT answer (LLM):**\n\n{llm if not err else '`ERROR: ' + err + '`'}\n\n"
            f"<details><summary>Deterministic retrieval passed to the model</summary>\n\n"
            f"```\n{context}\n```\n\n</details>\n\n---\n\n"
        )
        flush(i, elapsed=time.time() - t_run)
        print(f"[{i:>2}/{n}] {t_det:>7.1f}ms retrieval | {t_llm:>5.1f}s llm | "
              f"{n_docs:>2} docs | {llm_links} links | {q[:52]}")

    flush(n, status="COMPLETE", elapsed=time.time() - t_run)
    close_driver()
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()

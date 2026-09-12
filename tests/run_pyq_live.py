"""Live 40-question run of the PYQ pipeline, with real Qwen3 8B calls.

Pipeline exercised end to end:
    student question
      -> deterministic filter extraction (no model)
      -> Neo4j PYQ search
      -> Drive links
      -> Qwen3 8B phrasing (think=False)

Every question is timed twice -- once for the deterministic path and once for
the Qwen phrasing path -- so the cost of involving the model is visible per
question rather than asserted.

Writes incrementally after every question, so a long run can be watched live
and survives being interrupted:
    data/pyq_live_test.md        human-readable: question, times, answer, links
    data/pyq_live_results.jsonl  one JSON object per question

Run with:
    python -m tests.run_pyq_live
    python -m tests.run_pyq_live --no-llm      # deterministic timings only
    python -m tests.run_pyq_live --limit 5
"""
import argparse
import json
import os
import time
from datetime import datetime, timezone

from graph.neo4j_driver import close_driver, verify_connection
from llm.qwen import OLLAMA_MODEL, verify_ollama
from services.pyq_service import MAX_LLM_PAPERS, build_context, retrieve
from llm.qwen import ask_qwen
from llm.system_prompt import KJGPT_PYQ_SYSTEM_PROMPT
from tests.pyq_questions_40 import PYQ_QUESTIONS

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_PATH = os.path.join(REPO_ROOT, "data", "pyq_live_test.md")
JSONL_PATH = os.path.join(REPO_ROOT, "data", "pyq_live_results.jsonl")

DRIVE_PREFIX = "https://drive.google.com/"


def render_markdown(records, meta):
    lines = [
        "# KJGPT PYQ — live 40-question run",
        "",
        f"- Started: {meta['started']}",
        f"- Model: `{meta['model']}` (thinking off)" if meta["llm"]
        else "- Model: not called (`--no-llm`)",
        f"- Papers in graph: {meta['paper_count']}",
        f"- Progress: **{meta['done']}/{meta['total']}** "
        f"({meta['completed']} completed, {meta['failed']} failed)",
        "",
        "`retrieval` is question -> filters -> Neo4j -> links, with no model call.",
        "`qwen` is the extra time to have Qwen3 8B reword that same list.",
        "",
        "## Summary",
        "",
        "| # | Category | Question | Papers | Retrieval | Qwen | Status |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in records:
        q = r["question"].replace("|", "\\|")
        qwen = f"{r['qwen_s']:.1f}s" if r.get("qwen_s") is not None else "—"
        ret = f"{r['retrieval_ms']:.0f}ms" if r.get("retrieval_ms") is not None else "—"
        lines.append(f"| {r['n']} | {r['category']} | {q} | "
                     f"{r.get('paper_count', '—')} | {ret} | {qwen} | {r['status']} |")

    lines += ["", "## Detail", ""]
    for r in records:
        lines.append(f"### {r['n']}. {r['question']}")
        lines.append("")
        lines.append(f"- Category: `{r['category']}`  ·  Status: **{r['status']}**")
        if r.get("filters"):
            shown = {k: v for k, v in r["filters"].items()
                     if v and not k.startswith("_")}
            lines.append(f"- Filters extracted: `{shown or '{}'}`")
        if r.get("retrieval_ms") is not None:
            lines.append(f"- Retrieval: {r['retrieval_ms']:.0f} ms · "
                         f"{r.get('paper_count', 0)} paper(s)")
        if r.get("qwen_s") is not None:
            lines.append(f"- Qwen3 8B: {r['qwen_s']:.1f} s")
        if r.get("error"):
            lines.append(f"- Error: `{r['error']}`")
        lines.append("")
        if r.get("papers"):
            lines.append("Papers found:")
            lines.append("")
            for p in r["papers"]:
                lines.append(f"- {p['title']}  \n  {p['drive_url']}")
            lines.append("")
        if r.get("answer"):
            lines.append("Answer:")
            lines.append("")
            lines.append("```")
            lines.append(r["answer"])
            lines.append("```")
            lines.append("")
    return "\n".join(lines) + "\n"


def flush(records, meta):
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write(render_markdown(records, meta))
    with open(JSONL_PATH, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-llm", action="store_true",
                        help="skip the Qwen phrasing pass")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    use_llm = not args.no_llm

    print("Verifying Neo4j...")
    verify_connection()
    if use_llm:
        print("Verifying Ollama...")
        verify_ollama()
    print("Connected.\n")

    from graph.pyq_ingestion import counts
    questions = PYQ_QUESTIONS[:args.limit] if args.limit else PYQ_QUESTIONS

    meta = {
        "started": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": OLLAMA_MODEL, "llm": use_llm,
        "paper_count": counts()["pyq"],
        "total": len(questions), "done": 0, "completed": 0, "failed": 0,
    }
    records = []
    run_started = time.perf_counter()

    for n, (category, question) in enumerate(questions, 1):
        record = {"n": n, "category": category, "question": question,
                  "status": "Running"}
        records.append(record)
        meta["done"] = n
        flush(records, meta)
        print(f"[{n}/{len(questions)}] {question}")

        try:
            t0 = time.perf_counter()
            result = retrieve(question)
            record["retrieval_ms"] = (time.perf_counter() - t0) * 1000
            record["filters"] = result["filters"]
            record["reason"] = result["reason"]
            record["paper_count"] = len(result["rows"])
            record["papers"] = [{"title": r["title"], "drive_url": r["drive_url"]}
                                for r in result["rows"]]
            bad = [p for p in record["papers"]
                   if not p["drive_url"].startswith(DRIVE_PREFIX)]
            record["bad_links"] = len(bad)

            if result["rows"] and use_llm:
                t1 = time.perf_counter()
                record["answer"] = ask_qwen(
                    KJGPT_PYQ_SYSTEM_PROMPT,
                    "PAPERS FOUND:\n"
                    + build_context(result["rows"], result["filters"],
                                    limit=MAX_LLM_PAPERS)
                    + f"\n\nSTUDENT ASKED:\n{question}",
                    think=False,
                    timeout=180,
                )
                record["qwen_s"] = time.perf_counter() - t1
            else:
                record["answer"] = result["context"] or f"(no papers: {result['reason']})"

            record["status"] = "Completed"
            meta["completed"] += 1
            print(f"        {record['paper_count']} paper(s) · "
                  f"retrieval {record['retrieval_ms']:.0f} ms"
                  + (f" · qwen {record['qwen_s']:.1f} s"
                     if record.get("qwen_s") else ""))
        except Exception as e:
            record["status"] = "Failed"
            record["error"] = f"{type(e).__name__}: {e}"
            meta["failed"] += 1
            print(f"        FAILED: {record['error']}")

        flush(records, meta)

    elapsed = time.perf_counter() - run_started
    ret_times = [r["retrieval_ms"] for r in records if r.get("retrieval_ms")]
    qwen_times = [r["qwen_s"] for r in records if r.get("qwen_s")]
    bad_total = sum(r.get("bad_links", 0) for r in records)
    no_result = [r for r in records
                 if r["status"] == "Completed" and r.get("paper_count") == 0]

    print(f"\n{'=' * 60}")
    print(f"Completed: {meta['completed']}   Failed: {meta['failed']}")
    print(f"Total wall time: {elapsed:.1f}s")
    if ret_times:
        print(f"Retrieval: avg {sum(ret_times)/len(ret_times):.0f} ms, "
              f"max {max(ret_times):.0f} ms")
    if qwen_times:
        print(f"Qwen3 8B:  avg {sum(qwen_times)/len(qwen_times):.1f} s, "
              f"max {max(qwen_times):.1f} s")
    print(f"Unusable links: {bad_total}")
    print(f"Questions returning no paper: {len(no_result)} "
          f"({', '.join(r['question'] for r in no_result) or 'none'})")
    print(f"\n-> {os.path.relpath(MD_PATH, REPO_ROOT)}")
    print(f"-> {os.path.relpath(JSONL_PATH, REPO_ROOT)}")

    close_driver()
    return 0 if meta["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Runs the 20 link-retrieval questions and writes a readable report.

    question
      -> deterministic filter extraction (no model)
      -> Neo4j PYQ search
      -> Drive links
      -> Qwen3 8B phrasing (think=False, optional)

The report is about the LINKS. Every returned row is checked to be a
file-level Drive URL rather than a folder, and inside the 2019-2025 window,
and the checks are shown per question so a failure is visible where it
happened rather than only in a total at the end.

Writes after every question, so a long run can be watched live and survives
being interrupted:
    data/pyq_links_20.md

Run with:
    .venv/bin/python -m tests.run_pyq_links_20
    .venv/bin/python -m tests.run_pyq_links_20 --no-llm
    .venv/bin/python -m tests.run_pyq_links_20 --limit 5
"""
import argparse
import os
import time
from datetime import datetime, timezone

from graph.neo4j_driver import close_driver, run_query, verify_connection
from llm.qwen import OLLAMA_MODEL, ask_qwen, verify_ollama
from llm.system_prompt import KJGPT_PYQ_SYSTEM_PROMPT
from services.pyq_service import (
    MAX_LLM_PAPERS,
    MAX_YEAR,
    MIN_YEAR,
    build_context,
    retrieve,
)
from tests.pyq_questions_20 import PYQ_QUESTIONS_20

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_PATH = os.path.join(REPO_ROOT, "data", "pyq_links_20.md")

# A student must be sent to the paper, never to the folder it sits in.
FILE_URL_PREFIX = "https://drive.google.com/file/d/"
DRIVE_PREFIX = "https://drive.google.com/"

# Questions that are supposed to come back empty. Their emptiness is the pass,
# so the summary must not read them as failures.
EXPECTED_EMPTY = {"miss", "year window"}


def link_checks(rows, category, blocked=False) -> list[tuple[str, bool, str]]:
    """(label, ok, detail) for the things that make a link usable."""
    checks = []
    if not rows:
        if blocked:
            checks.append(("returned nothing", True,
                           "ESE not ingested yet -- cannot be judged"))
        else:
            checks.append(("returned nothing", category in EXPECTED_EMPTY,
                           "expected for this category"
                           if category in EXPECTED_EMPTY
                           else "expected at least one paper"))
        return checks

    bad_url = [r for r in rows
               if not (r.get("drive_url") or "").startswith(DRIVE_PREFIX)]
    checks.append(("every link is a Google Drive URL", not bad_url,
                   f"{len(rows) - len(bad_url)}/{len(rows)}"))

    folder_links = [r for r in rows
                    if "/drive/folders/" in (r.get("drive_url") or "")]
    checks.append(("no link points at a folder", not folder_links,
                   f"{len(folder_links)} folder link(s)"))

    file_links = [r for r in rows
                  if (r.get("drive_url") or "").startswith(FILE_URL_PREFIX)]
    checks.append(("links are file-level /file/d/<id>", len(file_links) == len(rows),
                   f"{len(file_links)}/{len(rows)}"))

    out_of_range = [r for r in rows
                    if r.get("exam_year") is not None
                    and not (MIN_YEAR <= r["exam_year"] <= MAX_YEAR)]
    checks.append((f"every paper is {MIN_YEAR}-{MAX_YEAR}", not out_of_range,
                   f"{len(out_of_range)} outside"))

    unique = {r.get("drive_url") for r in rows}
    checks.append(("no duplicate link in one answer", len(unique) == len(rows),
                   f"{len(unique)} unique of {len(rows)}"))

    return checks


def _esc(text) -> str:
    """Keep a question or title from breaking the markdown table."""
    return str(text).replace("|", "\\|").replace("\n", " ")


def render(records, meta) -> str:
    passed = sum(1 for r in records if r["status"] == "PASS")
    failed = sum(1 for r in records if r["status"] == "FAIL")
    blocked = sum(1 for r in records if r["status"] == "BLOCKED")
    lines = [
        "# KJGPT PYQ — 20-question Drive-link run",
        "",
        f"- Started: `{meta['started']}`",
        f"- Model: `{meta['model']}` (thinking off)" if meta["llm"]
        else "- Model: not called (`--no-llm`)",
        f"- Papers in graph: **{meta['pyq']}** "
        f"(ISE {meta['ise']}, ESE {meta['ese']})",
        f"- Year window enforced: **{MIN_YEAR}-{MAX_YEAR}**",
        f"- Progress: **{meta['done']}/{meta['total']}** — "
        f"{passed} passed, {failed} failed, {blocked} blocked",
        "",
        "`retrieval` is question → filters → Neo4j → links, with no model call. "
        "`qwen` is the extra time for Qwen3 8B to reword that same list; it "
        "never invents or edits a URL.",
        "",
    ]
    if meta["ese"] == 0:
        lines += [
            "> **Note** — no ESE papers are in the graph yet: ingesting them "
            "needs `service_account.json`, which is missing. ESE questions "
            "below therefore return an honest empty answer. Every ISE result "
            "and every link check is real.",
            "",
        ]

    lines += [
        "## Summary",
        "",
        "| # | Category | Question | Papers | Types | Retrieval | Qwen | Result |",
        "|---|---|---|---|---:|---|---:|---:|",
    ]
    for r in records:
        lines.append(
            f"| {r['n']} | {r['category']} | {_esc(r['question'])} | "
            f"{r['count']} | {r['types'] or '—'} | {r['retrieval_ms']}ms | "
            f"{r['qwen_s']} | {r['status']} |")

    lines += ["", "## Detail", ""]
    for r in records:
        lines += [
            f"### {r['n']}. {_esc(r['question'])}",
            "",
            f"*{r['note']}*",
            "",
            f"- Category: `{r['category']}` · Result: **{r['status']}**",
            f"- Filters: `{r['filters']}`",
            f"- Papers: **{r['count']}** · Retrieval: {r['retrieval_ms']}ms"
            + (f" · Qwen: {r['qwen_s']}" if r["qwen_s"] != "—" else ""),
            "",
        ]
        if r["checks"]:
            lines += ["| Link check | Result | Detail |", "|---|---|---|"]
            for label, ok, detail in r["checks"]:
                lines.append(f"| {label} | {'PASS' if ok else 'FAIL'} | {detail} |")
            lines.append("")

        if r["rows"]:
            lines += ["**Papers returned**", "",
                      "| # | Title | Exam | Year | Sem | Drive link |",
                      "|---|---|---|---:|---:|---|"]
            for i, row in enumerate(r["rows"], 1):
                title = _esc(row.get("title"))
                if row.get("page_label"):
                    title += f" ({row['page_label']})"
                lines.append(
                    f"| {i} | {title} | {row.get('exam_type') or '—'} | "
                    f"{row.get('exam_year') or '—'} | {row.get('semester') or '—'} | "
                    f"[open]({row.get('drive_url')}) |")
            lines.append("")
            lines += ["<details><summary>Raw URLs</summary>", ""]
            lines += [f"{i}. `{row.get('drive_url')}`"
                      for i, row in enumerate(r["rows"], 1)]
            lines += ["", "</details>", ""]
        else:
            lines += [f"**No papers returned** — reason: `{r['reason']}`", ""]

        if r.get("answer"):
            lines += ["**Qwen3 8B answer**", "", "```text", r["answer"].strip(),
                      "```", ""]
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def graph_counts() -> dict:
    rows = run_query(
        "MATCH (p:PYQ) RETURN coalesce(p.exam_type,'?') AS t, count(*) AS c")
    by_type = {r["t"]: r["c"] for r in rows}
    return {"pyq": sum(by_type.values()),
            "ise": by_type.get("ISE", 0), "ese": by_type.get("ESE", 0)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-llm", action="store_true",
                        help="skip the Qwen phrasing pass")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--out", default=MD_PATH)
    args = parser.parse_args()

    questions = PYQ_QUESTIONS_20[: args.limit] if args.limit else PYQ_QUESTIONS_20
    use_llm = not args.no_llm

    print("Verifying Neo4j...")
    verify_connection()
    if use_llm:
        print("Verifying Ollama...")
        verify_ollama()

    counts = graph_counts()
    meta = {"started": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "model": OLLAMA_MODEL, "llm": use_llm, "total": len(questions),
            "done": 0, **counts}
    print(f"Graph: PYQ={counts['pyq']} (ISE {counts['ise']}, ESE {counts['ese']})\n")

    records = []
    for n, (category, question, note) in enumerate(questions, 1):
        t0 = time.perf_counter()
        result = retrieve(question)
        retrieval_ms = int((time.perf_counter() - t0) * 1000)

        rows = result["rows"]
        # An ESE question cannot pass or fail while there is no ESE data to
        # query. Reporting that as a failure would hide the real defects.
        blocked = (not rows
                   and result["filters"].get("exam_type") == "ESE"
                   and counts["ese"] == 0)
        checks = link_checks(rows, category, blocked=blocked)
        ok = all(c[1] for c in checks)
        status = "BLOCKED" if blocked else ("PASS" if ok else "FAIL")

        answer, qwen_s = None, "—"
        if use_llm and rows:
            t1 = time.perf_counter()
            try:
                answer = ask_qwen(
                    KJGPT_PYQ_SYSTEM_PROMPT,
                    "PAPERS FOUND:\n"
                    + build_context(rows, result["filters"],
                                    limit=MAX_LLM_PAPERS)
                    + f"\n\nSTUDENT ASKED:\n{question}",
                    think=False, timeout=180)
                qwen_s = f"{time.perf_counter() - t1:.1f}s"
            except Exception as e:
                answer = f"[Qwen call failed: {type(e).__name__}: {e}]"
                qwen_s = "error"

        filters = {k: v for k, v in result["filters"].items()
                   if v and not k.startswith("_")}
        records.append({
            "n": n, "category": category, "question": question, "note": note,
            "filters": filters or "none", "count": len(rows),
            "types": ",".join(sorted({r["exam_type"] for r in rows})),
            "retrieval_ms": retrieval_ms, "qwen_s": qwen_s,
            "rows": rows, "reason": result["reason"], "answer": answer,
            "ok": ok, "status": status, "checks": checks,
        })
        meta["done"] = n
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(render(records, meta))

        print(f"  {n:>2}/{len(questions)}  {status:<7}"
              f"{len(rows):>3} paper(s)  {retrieval_ms:>4}ms  "
              f"qwen={qwen_s:>6}  {question[:44]}")

    passed = sum(1 for r in records if r["status"] == "PASS")
    failed = sum(1 for r in records if r["status"] == "FAIL")
    blocked = sum(1 for r in records if r["status"] == "BLOCKED")
    print(f"\n{passed} passed, {failed} failed, {blocked} blocked "
          f"(of {len(records)})")
    print(f"-> {os.path.relpath(args.out)}")
    close_driver()
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Parses the already-completed data/faculty_batch_test_30.md and (re)appends
the Batch Test Analysis section, using the fixed analysis logic. Does not call
Neo4j or Qwen again -- all 30 questions already ran successfully.
"""
import re

import tests.run_faculty_batch_30 as batch

MD_PATH = batch.OUT_PATH


def parse():
    with open(MD_PATH) as f:
        text = f.read()

    # Drop any previously appended (and possibly crashed/partial) analysis section.
    text = text.split("\n# Batch Test Analysis")[0]

    blocks = re.split(r"\n## Test (\d+)\n", text)[1:]
    it = iter(blocks)
    for num_str, body in zip(it, it):
        i = int(num_str)
        r = batch.records[i]

        def field(name, body=body):
            m = re.search(rf"{re.escape(name)}:\n(.*?)(?:\n\n|\Z)", body, re.S)
            return m.group(1).strip() if m else None

        r["category"] = field("Category")
        r["question"] = field("Question")
        status_raw = field("Status") or ""
        r["status"] = "Completed" if "Completed" in status_raw else (
            "Failed" if "Failed" in status_raw else "Pending")
        r["strategy"] = field("Retrieval Strategy")
        r["match"] = field("Neo4j Match")
        rc = field("Neo4j Result Count")
        r["result_count"] = int(rc) if rc and rc.isdigit() else 0
        ctx_m = re.search(r"Neo4j Retrieved Context \(sent to Qwen3\):\n```\n(.*?)\n```", body, re.S)
        ctx = ctx_m.group(1) if ctx_m else None
        r["context"] = None if ctx in (None, "(none - no matching node in graph)") else ctx
        r["answer"] = field("Qwen3 Final Answer")
        rt = field("Response Time (seconds)")
        r["elapsed"] = float(rt) if rt and rt not in ("N/A",) else None
        r["error"] = field("Error")

    return text  # the cleaned, pre-analysis markdown body


def main():
    cleaned = parse()
    with open(MD_PATH, "w") as f:
        f.write(cleaned)
    batch.append_analysis()
    print(f"Re-wrote analysis section in {MD_PATH}")

    completed = sum(1 for r in batch.records.values() if r["status"] == "Completed")
    failed = sum(1 for r in batch.records.values() if r["status"] == "Failed")
    print(f"Parsed {len(batch.records)} tests -> completed={completed} failed={failed}")


if __name__ == "__main__":
    main()

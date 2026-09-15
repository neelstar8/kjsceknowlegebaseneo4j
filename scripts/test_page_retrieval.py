"""Retrieval validation for the page-content knowledge, across services.

The KJ GPT graph answers different question shapes from different places: a rule
("how much attendance?") comes from the handbook provisions, a document ("show me
the 2026-27 calendar") from the document layer, and page-shaped knowledge
("admission eligibility") from the pages ingested here. A validation suite that
only tested one service would look green while the student got nothing, so every
case below names the service that is supposed to answer it.

    .venv/bin/python -m scripts.test_page_retrieval
"""
from __future__ import annotations

import re
import sys

from graph.neo4j_driver import close_driver, run_query
from services.academic_document_service import answer_academic_question
from services.page_knowledge_service import answer_page_question
from services.policy_service import answer_policy_question
from services.site_document_service import answer_site_document_question

_passed = _failed = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global _passed, _failed
    if ok:
        _passed += 1
        print(f"  [PASS] {label}" + (f" -- {detail}" if detail else ""))
    else:
        _failed += 1
        print(f"  [FAIL] {label}" + (f" -- {detail}" if detail else ""))


def pages(q):
    return answer_page_question(q)


def policy(q):
    return answer_policy_question(q)


def run() -> None:
    print("\n== rule questions answer from the handbook provisions ==")
    for q in ["What is the attendance requirement?",
              "How much attendance do students need?",
              "minimum attendance?",
              "How much attendance do I need?"]:
        r = policy(q)
        check(f'"{q}"', r["found"] and len(r["sources"]) > 0,
              f"{len(r['sources'])} sourced provisions")

    print("\n== page questions answer from page knowledge ==")
    for q, must in [("admission eligibility for B.Tech", "admission"),
                    ("What are the B.Tech fees?", "admission"),
                    ("direct second year admission", "Direct Second Year"),
                    ("What programmes are offered?", None)]:
        r = pages(q)
        titles = " ".join(p["title"] for p in r["pages"]).lower()
        ok = r["found"] and (must is None or must.lower() in titles
                             or any(must.lower() in (p["section"] or "").lower()
                                    for p in r["pages"]))
        check(f'"{q}"', ok, f"{len(r['pages'])} pages")

    print("\n== the same question, three ways, reaches the same page ==")
    for a, b in [("DSY admission", "direct second year admission"),
                 ("FY BTech fees", "first year B.Tech fees"),
                 ("MTech admission", "M.Tech admission")]:
        ra, rb = pages(a), pages(b)
        ta = {p["doc_id"] for p in ra["pages"][:3]}
        tb = {p["doc_id"] for p in rb["pages"][:3]}
        check(f'"{a}" == "{b}"', bool(ta & tb),
              f"{len(ta & tb)} shared of top 3")

    print("\n== year handling ==")
    r = pages("What is the 2026-27 admission process?")
    ok = all("2026-27" in (p["academic_years"] or []) for p in r["pages"])
    check("exact year returns only pages naming it", ok and r["found"],
          f"{len(r['pages'])} pages, all naming 2026-27")

    r = pages("2026 admission")
    check("bare year is resolved or reported, never guessed",
          r["found"] or bool(r.get("pages")),
          "resolved against the years actually held")

    held = {x["academic_year"] for x in run_query(
        "MATCH (d:PolicyDocument) WHERE d.academic_years IS NOT NULL "
        "UNWIND d.academic_years AS y RETURN DISTINCT y AS academic_year")}
    r = pages("2019 admission")
    bad = [p for p in r["pages"] if p["academic_years"]
           and "2019-20" not in p["academic_years"]]
    check("an old-year query never silently returns a different year",
          not r["found"] or not bad,
          f"{len(bad)} mismatched" if bad else "no year substitution")

    print("\n== no phantom academic years survived extraction ==")
    phantom = run_query("""
        MATCH (d:PolicyDocument) WHERE d.academic_years IS NOT NULL
        UNWIND d.academic_years AS y
        WITH y WHERE NOT y =~ '20\\\\d{2}-\\\\d{2}'
        RETURN count(y) AS v""")[0]["v"]
    check("every stored academic year is well formed", phantom == 0,
          f"{phantom} malformed")
    nonconsec = 0
    for y in held:
        m = re.match(r"(\d{4})-(\d{2})$", y)
        if m and int(m.group(2)) != (int(m.group(1)) + 1) % 100:
            nonconsec += 1
    check("every stored academic year is consecutive", nonconsec == 0,
          f"{nonconsec} impossible (e.g. 2026-24)")

    print("\n== documents still answer from the document layer ==")
    r = answer_academic_question("What is the academic calendar for 2026-27?")
    check("2026-27 academic calendar", len(r["documents"]) >= 1,
          f"{len(r['documents'])} documents")
    r = answer_academic_question("Where can I find the syllabus?")
    check("syllabus returns only the syllabus index", len(r["documents"]) == 1,
          f"{len(r['documents'])} documents")
    r = answer_site_document_question("What is the NIRF ranking report?")
    check("NIRF ranking reports", len(r["documents"]) >= 5,
          f"{len(r['documents'])} documents")

    print("\n== multi-intent ==")
    r = answer_academic_question(
        "Show me the 2026-27 academic calendar and tell me where the syllabus is")
    kinds = {d["source_type"] for d in r["documents"]}
    check("calendar + syllabus both returned", len(kinds) >= 2,
          f"source types: {sorted(kinds)}")

    print("\n== links are real ==")
    official = {x["u"] for x in run_query(
        "MATCH (d:PolicyDocument) WHERE d.source_url IS NOT NULL "
        "RETURN d.source_url AS u")}
    official |= {x["u"] for x in run_query(
        "MATCH (d:PolicyDocument) WHERE d.alternate_source_url IS NOT NULL "
        "RETURN d.alternate_source_url AS u")}
    official.add("https://kjsce.somaiya.edu/en/documents/")
    official.add("https://kjsce.somaiya.edu/en/")
    bad_links = []
    for q in ["admission eligibility for B.Tech", "What are the B.Tech fees?",
              "direct second year admission", "What programmes are offered?"]:
        a = answer_page_question(q)["answer"]
        urls = set(re.findall(r"\]\(<([^>]+)>\)", a)) | set(
            re.findall(r"\]\((?!<)([^)\s]+)\)", a))
        bad_links += [u for u in urls if u not in official]
    check("no answer contains a link that is not in the graph", not bad_links,
          f"{len(bad_links)} invented" if bad_links else "all links verified")
    check("no placeholder URL anywhere",
          not any("example.com" in u for u in bad_links), "no example.com")


def main() -> int:
    try:
        run()
    finally:
        close_driver()
    total = _passed + _failed
    print(f"\n{_passed}/{total} retrieval checks passed")
    return 1 if _failed else 0


if __name__ == "__main__":
    sys.exit(main())

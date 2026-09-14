"""Phase 6: validate the policy graph in place. Run after scripts.ingest_policies.

Checks the things that would make the graph quietly wrong rather than
obviously broken: duplicates, orphans, provisions with no source, a policy in
the wrong category, a node claiming the wrong institution, a superseded policy
reachable from a normal query, and content that should never be in Neo4j.

    .venv/bin/python -m scripts.test_policy_queries
"""
import json
import sys

from graph import policy_queries as pq
from graph.neo4j_driver import close_driver, run_query, verify_connection

FAILURES = []
CHECKS = 0


def check(name, condition, detail=""):
    global CHECKS
    CHECKS += 1
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}" + (f"  -- {detail}" if detail else ""))
    if not condition:
        FAILURES.append(f"{name}: {detail}")


def scalar(query, params=None):
    rows = run_query(query, params or {})
    return list(rows[0].values())[0] if rows else None


def main():
    verify_connection()
    knowledge = json.load(open("data/policy_knowledge.json", encoding="utf-8"))
    expected_policies = len(knowledge["policies"])
    expected_provisions = sum(len(p["provisions"]) for p in knowledge["policies"])

    print("\n== counts ==")
    check("all policies ingested",
          scalar("MATCH (p:Policy) RETURN count(p)") == expected_policies,
          f"graph has {scalar('MATCH (p:Policy) RETURN count(p)')}, "
          f"file has {expected_policies}")
    check("all provisions ingested",
          scalar("MATCH (v:PolicyProvision) RETURN count(v)") == expected_provisions,
          f"graph has {scalar('MATCH (v:PolicyProvision) RETURN count(v)')}, "
          f"file has {expected_provisions}")
    check("four handbook categories",
          scalar("MATCH (c:PolicyCategory) RETURN count(c)") == 4)
    check("exactly one handbook root",
          scalar("MATCH (h:PolicyHandbook) RETURN count(h)") == 1)

    print("\n== no duplicates ==")
    for label, key in (("Policy", "policy_id"), ("PolicyProvision", "provision_id"),
                       ("PolicyDocument", "doc_id"), ("PolicyCategory", "category_key")):
        dupes = scalar(f"MATCH (n:{label}) WITH n.{key} AS k, count(*) AS c "
                       f"WHERE c > 1 RETURN count(k)")
        check(f"no duplicate {label}.{key}", dupes == 0, f"{dupes} duplicated")
    dupe_rels = scalar("""
        MATCH (a)-[r]->(b) WITH a, type(r) AS t, b, count(*) AS c
        WHERE c > 1 RETURN count(*)""")
    check("no duplicated relationships", dupe_rels == 0, f"{dupe_rels} duplicated")

    print("\n== source traceability ==")
    no_source = scalar("""
        MATCH (v:PolicyProvision) WHERE NOT (v)-[:SOURCED_FROM]->(:PolicyDocument)
        RETURN count(v)""")
    check("every provision points at a document", no_source == 0,
          f"{no_source} provisions have no SOURCED_FROM")
    no_page = scalar("MATCH (v:PolicyProvision) WHERE v.source_page IS NULL "
                     "RETURN count(v)")
    check("every provision has a page number", no_page == 0,
          f"{no_page} provisions have no page")
    no_section = scalar("MATCH (v:PolicyProvision) WHERE v.source_section IS NULL "
                        "RETURN count(v)")
    check("every provision has a section", no_section == 0)
    no_url = scalar("MATCH (d:PolicyDocument) WHERE d.source_url IS NULL "
                    "RETURN count(d)")
    check("every document has a source URL", no_url == 0)

    print("\n== structure ==")
    orphan_policies = scalar("""
        MATCH (p:Policy) WHERE NOT (p)-[:BELONGS_TO]->(:PolicyCategory)
        RETURN count(p)""")
    check("every policy belongs to a category", orphan_policies == 0)
    undocumented = scalar("""
        MATCH (p:Policy) WHERE NOT (p)-[:DOCUMENTED_IN]->(:PolicyDocument)
        RETURN count(p)""")
    check("every policy points at its document", undocumented == 0)
    detached = scalar("""
        MATCH (v:PolicyProvision)
        WHERE NOT (:Policy)-[:DEFINES|SPECIFIES]->(v) RETURN count(v)""")
    check("every provision hangs off a policy", detached == 0)
    both_edges = scalar("""
        MATCH (p:Policy)-[:DEFINES]->(v:PolicyProvision)<-[:SPECIFIES]-(p)
        RETURN count(v)""")
    check("no provision is both DEFINED and SPECIFIED", both_edges == 0)
    procedures_specified = scalar("""
        MATCH (p:Policy)-[:DEFINES]->(v:PolicyProvision)
        WHERE v.kind IN ['procedure', 'timeline', 'process'] RETURN count(v)""")
    check("procedures use SPECIFIES, not DEFINES", procedures_specified == 0,
          f"{procedures_specified} miscategorised")

    print("\n== institution scope ==")
    wrong_institution = scalar("""
        MATCH (n) WHERE (n:Policy OR n:PolicyProvision OR n:PolicyDocument)
        AND n.institution <> 'KJSIT' RETURN count(n)""")
    check("no node claims an institution other than KJSIT", wrong_institution == 0,
          f"{wrong_institution} nodes")
    kjsse = scalar("""
        MATCH (v:PolicyProvision) WHERE toLower(v.text) CONTAINS 'kjsse'
        RETURN count(v)""")
    check("nothing in the graph mentions KJSSE", kjsse == 0,
          f"{kjsse} provisions mention KJSSE")

    print("\n== versioning ==")
    superseded = scalar("MATCH (p:Policy {status:'superseded'}) RETURN count(p)")
    check("superseded policies are retained as history", superseded > 0,
          f"{superseded} superseded policies")
    unlinked_superseded = scalar("""
        MATCH (p:Policy {status:'superseded'})
        WHERE NOT (p)-[:SUPERSEDED_BY]->(:Policy) RETURN count(p)""")
    check("every superseded policy names its replacement", unlinked_superseded == 0,
          f"{unlinked_superseded} unlinked")
    default_hits = pq.search_provisions("ATKT heads of passing", limit=20)
    check("default search excludes superseded editions",
          all(r["policy_status"] != "superseded" for r in default_hits),
          f"{sum(1 for r in default_hits if r['policy_status'] == 'superseded')} leaked")
    opt_in = pq.search_provisions("ATKT heads of passing", limit=20,
                                  include_superseded=True)
    check("superseded editions are reachable on request",
          any(r["policy_status"] == "superseded" for r in opt_in))

    print("\n== no document content in the graph ==")
    # The same rule the PYQ system follows: metadata and links, never the file.
    longest = scalar("MATCH (v:PolicyProvision) RETURN max(size(v.text))")
    check("no provision is a page dump", longest < 4000, f"longest is {longest} chars")
    total_chars = scalar("MATCH (v:PolicyProvision) RETURN sum(size(v.text))")
    check("total provision text is a summary, not the corpus",
          total_chars < 400_000,
          f"{total_chars} chars vs ~676,000 chars of extracted source text")
    pdf_bytes = scalar("""
        MATCH (n) WHERE any(k IN keys(n) WHERE k IN ['pdf','content','raw','bytes'])
        RETURN count(n)""")
    check("no node carries file bytes", pdf_bytes == 0)

    print("\n== other systems untouched ==")
    check("FacultyMember still 613",
          scalar("MATCH (v:FacultyMember) RETURN count(v)") == 613)
    check("PYQ still 164", scalar("MATCH (p:PYQ) RETURN count(p)") == 164)
    check("Subject still 81", scalar("MATCH (s:Subject) RETURN count(s)") == 81)
    cross = scalar("""
        MATCH (p:Policy)--(n)
        WHERE n:FacultyMember OR n:PYQ OR n:PYQFile OR n:Subject RETURN count(*)""")
    check("policy graph does not entangle the faculty or PYQ graphs", cross == 0)

    print("\n== gaps are represented, not hidden ==")
    flagged = scalar("MATCH (v:PolicyProvision) WHERE v.ambiguity IS NOT NULL "
                     "RETURN count(v)")
    check("ambiguous provisions are flagged in the graph", flagged >= 20,
          f"{flagged} flagged")
    not_specified = scalar("""
        MATCH (v:PolicyProvision)
        WHERE toUpper(v.text) CONTAINS 'NOT SPECIFIED IN SOURCE' RETURN count(v)""")
    check("known gaps are recorded as provisions", not_specified > 0,
          f"{not_specified} provisions record an explicit gap")

    print(f"\n{CHECKS - len(FAILURES)}/{CHECKS} checks passed")
    if FAILURES:
        print("\nFAILURES:")
        for failure in FAILURES:
            print(f"  - {failure}")
    close_driver()
    sys.exit(1 if FAILURES else 0)


if __name__ == "__main__":
    main()

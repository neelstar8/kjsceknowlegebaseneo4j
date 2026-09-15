"""Decide, for every crawled resource, what the graph should do with it.

    crawl manifest + live Neo4j  ->  data/crawl/site_reconciliation.json

Read-only against the graph. It writes no nodes; it produces a reviewable decision
per resource so the ingest stage has nothing left to guess. Run it as often as you
like -- it recomputes from scratch each time.

    .venv/bin/python -m scripts.reconcile_site
    .venv/bin/python -m scripts.reconcile_site --show NEW
"""
from __future__ import annotations

import argparse
import json
import os
from collections import Counter

from crawl.manifest import Manifest, Status
from crawl.site_urls import HostClass, canonical_url, filename_of
from graph.neo4j_driver import close_driver, verify_connection
from graph.site_reconcile import Decision, load_index

OUT = "data/crawl/site_reconciliation.json"

#: A crawled resource is only a candidate for the graph once it has been read.
CANDIDATE_STATUSES = {Status.EXTRACTED, Status.RECORDED, Status.SKIPPED_PII,
                      Status.NEEDS_REVIEW}


def decide(row: dict, index) -> dict:
    """Route one crawled resource through the dedup ladder."""
    status = row.get("status")
    url = row.get("canonical_url", "")
    title = row.get("title") or filename_of(url)

    base = {"resource_id": row.get("resource_id"), "canonical_url": url,
            "title": title, "kind": row.get("kind"),
            "host_class": row.get("host_class"), "status": status}

    if status == Status.SKIPPED_PII:
        return {**base, "decision": Decision.SKIPPED_PII,
                "evidence": row.get("pii_reason", "")}

    if status == Status.NEEDS_REVIEW:
        return {**base, "decision": Decision.REVIEW,
                "evidence": row.get("review_reason", "")}

    if row.get("host_class") == HostClass.REFERENCE:
        # The link is real and official; the content is out of engineering-college
        # scope. Kept in the manifest so a student can still be pointed at it.
        return {**base, "decision": Decision.REFERENCE_ONLY,
                "evidence": "non-KJ host: recorded as a reference link only"}

    if row.get("kind") == "page":
        # Pages are link sources, not documents. They become graph content only if a
        # later stage extracts a rule from them; the crawl itself creates nothing.
        return {**base, "decision": Decision.REFERENCE_ONLY,
                "evidence": "site page: harvested for links, not a document"}

    rung, matched, evidence = index.match(
        raw_url=row.get("raw_url") or url,
        canonical=url,
        sha256=row.get("sha256"),
        title=title,
        pages=row.get("pages"),
        size=row.get("bytes"),
    )

    if rung == "none":
        return {**base, "decision": Decision.NEW, "matched_on": None,
                "evidence": "no existing document matches",
                "pages": row.get("pages"), "sha256": row.get("sha256"),
                "needs_visual_read": row.get("needs_visual_read", False)}

    if rung == "title_size":
        return {**base, "decision": Decision.REVIEW, "matched_on": rung,
                "matched_doc_id": matched["doc_id"] if matched else None,
                "evidence": evidence}

    return {**base, "decision": Decision.REUSE, "matched_on": rung,
            "matched_doc_id": matched["doc_id"] if matched else None,
            "evidence": evidence,
            "alternate_url_to_record": (
                url if matched and url != matched.get("source_url") else None)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--show", default=None,
                    help="print every row with this decision, e.g. NEW or REVIEW")
    args = ap.parse_args()

    man = (Manifest(args.manifest) if args.manifest else Manifest()).load()
    verify_connection()
    try:
        index = load_index(canonical_url)
        rows = [r for r in man.rows.values() if r.get("status") in CANDIDATE_STATUSES]
        decisions = [decide(r, index) for r in rows]
    finally:
        close_driver()

    tally = Counter(d["decision"] for d in decisions)
    by_rung = Counter(d.get("matched_on") for d in decisions if d.get("matched_on"))

    print(f"\n  existing documents in graph : {len(index.documents)}")
    print(f"  crawled resources considered : {len(decisions)}\n")
    for decision, n in tally.most_common():
        print(f"    {decision:<16} {n}")
    if by_rung:
        print("\n  reuse matched on:")
        for rung, n in by_rung.most_common():
            print(f"    {rung:<16} {n}")

    if args.show:
        want = args.show.upper()
        print(f"\n  --- {want} ---")
        for d in decisions:
            if d["decision"] == want:
                print(f"    {(d['title'] or '')[:58]:<60} {d['canonical_url'][-52:]}")
                if d.get("evidence"):
                    print(f"      {d['evidence'][:110]}")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    payload = {"summary": dict(tally), "matched_on": dict(by_rung),
               "existing_documents": len(index.documents),
               "decisions": decisions}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()

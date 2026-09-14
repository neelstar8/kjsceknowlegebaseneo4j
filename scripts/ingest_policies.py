"""Stage 4: write the validated policy knowledge into Neo4j.

    data/policy_knowledge.json -> Neo4j -> data/policy_ingestion_report.json

Idempotent. Every node is MERGEd on a deterministic id and every relationship
is MERGEd, so running this twice inserts nothing the second time. Nothing is
ever deleted, and no existing :Faculty, :FacultyMember, :PYQ, :PYQFile or
:Subject node is touched -- the only thing shared with those systems is the
driver in graph/neo4j_driver.py.

    .venv/bin/python -m scripts.ingest_policies --dry-run   # prints, writes nothing
    .venv/bin/python -m scripts.ingest_policies
"""
import argparse
import json
import os
from datetime import datetime, timezone

from graph import policy_ingestion as gi
from graph.neo4j_driver import close_driver, verify_connection

IN_PATH = "data/policy_knowledge.json"
REPORT_PATH = "data/policy_ingestion_report.json"
VALIDATION_PATH = "data/policy_validation_report.json"

# Which entity field on a provision becomes which relationship.
PROVISION_ENTITY_EDGES = [
    ("requires_forms", "Form", "REQUIRES", "forward"),
    ("uses_portals", "Portal", "USES", "forward"),
]
# ["Label", "key"] fields. `reverse` means the entity is the source of the edge.
PROVISION_PAIR_EDGES = [
    ("responsible", "RESPONSIBLE_FOR", "reverse"),
    ("approved_by", "APPROVES", "reverse"),
    ("escalates_to", "ESCALATES_TO", "forward"),
]
PROVISION_SINGLE_EDGES = [
    ("scheme", "Scheme", "PROVIDES", "reverse"),
    ("references_org", "ExternalOrganization", "REFERENCES", "forward"),
    ("applies_to_category", "StudentCategory", "APPLIES_TO", "forward"),
    ("involves_committee", "Committee", "INVOLVES", "forward"),
]
# Policy-level fields: which relationship each maps to.
POLICY_EDGES = {"applies_to": "APPLIES_TO", "involves": "INVOLVES",
                "references": "REFERENCES"}
PROVISION_LINKS = [("consequence_of", "HAS_CONSEQUENCE"),
                   ("exception_to", "HAS_EXCEPTION")]

# Provision keys that are structure, not node properties.
NON_PROPERTY_KEYS = {
    "pid", "kind", "page", "section", "subsection", "doc_id_override",
    "requires_forms", "uses_portals", "responsible", "approved_by",
    "escalates_to", "scheme", "references_org", "applies_to_category",
    "involves_committee", "consequence_of", "exception_to", "numbers",
}
POLICY_NON_PROPERTY_KEYS = {
    "policy_id", "category_key", "doc_id", "provisions", "applies_to",
    "involves", "references", "page_start", "page_end", "section",
    "superseded_by", "aliases",
}


def _now():
    return datetime.now(timezone.utc).isoformat()


def flatten_numbers(numbers: list[dict]) -> dict:
    """Numbers become parallel arrays, so Cypher can filter on them.

    Neo4j cannot store a list of maps on a property, and a student question
    like "what is the minimum attendance" is answered by the number, not by
    the sentence around it -- so the values are kept addressable rather than
    buried in prose.
    """
    if not numbers:
        return {}
    return {
        "number_values": [float(n["value"]) for n in numbers],
        "number_units": [str(n["unit"]) for n in numbers],
        "number_labels": [str(n.get("of", "")) for n in numbers],
    }


def ingest(knowledge: dict, dry_run: bool = False) -> dict:
    now = _now()
    meta = knowledge["meta"]
    counts = {"created": {}, "updated": {}, "relationships": 0}
    created = {k: 0 for k in ("category", "document", "policy", "provision", "entity")}
    seen = {k: 0 for k in created}

    def note(kind, was_created):
        seen[kind] += 1
        if was_created:
            created[kind] += 1

    if dry_run:
        print("DRY RUN - no writes")
    else:
        gi.ensure_schema()
        gi.upsert_handbook(handbook_key=meta["handbook_key"], now=now, props={
            "name": "KJSIT Institute Policy Handbook",
            "handbook_url": meta["handbook_url"],
            "institution": meta["institution"],
            "institution_name_in_sources": meta["institution_name_in_sources"],
            "institution_note": meta["institution_note"],
            "first_publication": meta["first_publication"],
            "second_publication": meta["second_publication"],
            "last_update": meta["last_update"],
            "knowledge_version": meta["knowledge_version"],
            # One prompt for the whole Policy knowledge domain, held on its
            # singleton root node rather than duplicated onto every Policy or
            # PolicyProvision -- see services/policy_service.py's LLM path.
            "system_prompt": meta.get("system_prompt"),
        })

    for category in knowledge["categories"]:
        props = {k: v for k, v in category.items() if k != "category_key"}
        props["institution"] = meta["institution"]
        if dry_run:
            print(f"  category  {category['category_key']}")
            note("category", False)
            continue
        note("category", gi.upsert_category(category_key=category["category_key"],
                                            handbook_key=meta["handbook_key"],
                                            props=props, now=now))

    for doc in knowledge["documents"]:
        props = {k: v for k, v in doc.items() if k != "doc_id"}
        props["handbook_url"] = meta["handbook_url"]
        if dry_run:
            print(f"  document  {doc['doc_id']} ({doc.get('pages')}p)")
            note("document", False)
            continue
        note("document", gi.upsert_document(doc_id=doc["doc_id"], props=props, now=now))

    for entity in knowledge["entities"]:
        props = {k: v for k, v in entity.items()
                 if k not in ("label", "entity_key")}
        props["institution"] = meta["institution"]
        if dry_run:
            note("entity", False)
            continue
        note("entity", gi.upsert_entity(label=entity["label"],
                                        entity_key=entity["entity_key"],
                                        props=props, now=now))

    relationships = 0
    for policy in knowledge["policies"]:
        pid = policy["policy_id"]
        props = {k: v for k, v in policy.items() if k not in POLICY_NON_PROPERTY_KEYS}
        props["category_key"] = policy["category_key"]
        props["aliases"] = policy.get("aliases", [])
        # Fulltext indexes cannot search inside a list, so the aliases are also
        # kept as one searchable string.
        props["aliases_text"] = " | ".join(policy.get("aliases", []))
        props["source_url"] = next(
            (d["source_url"] for d in knowledge["documents"]
             if d["doc_id"] == policy["doc_id"]), None)
        props["handbook_url"] = meta["handbook_url"]
        doc_edge = {"page_start": policy.get("page_start"),
                    "page_end": policy.get("page_end"),
                    "section": policy.get("section")}
        if dry_run:
            print(f"  policy    {pid:<34} {len(policy['provisions'])} provisions")
            note("policy", False)
        else:
            note("policy", gi.upsert_policy(policy_id=pid,
                                            category_key=policy["category_key"],
                                            doc_id=policy["doc_id"], props=props,
                                            doc_edge=doc_edge, now=now))
            for field, rel in POLICY_EDGES.items():
                for label, key in policy.get(field, []):
                    relationships += gi.link(from_label="Policy", from_id=pid,
                                             rel=rel, to_label=label, to_id=key)

        for prov in policy["provisions"]:
            vid = prov["pid"]
            doc_id = prov.get("doc_id_override", policy["doc_id"])
            vprops = {k: v for k, v in prov.items() if k not in NON_PROPERTY_KEYS}
            vprops.update({
                "kind": prov["kind"], "policy_id": pid, "doc_id": doc_id,
                "source_page": prov.get("page"), "source_section": prov.get("section"),
                "source_url": next((d["source_url"] for d in knowledge["documents"]
                                    if d["doc_id"] == doc_id), None),
                "institution": meta["institution"],
            })
            vprops.update(flatten_numbers(prov.get("numbers")))
            source_edge = {"page": prov.get("page"), "section": prov.get("section"),
                           "subsection": prov.get("subsection")}
            if dry_run:
                note("provision", False)
                continue
            note("provision", gi.upsert_provision(
                provision_id=vid, policy_id=pid, doc_id=doc_id, kind=prov["kind"],
                props=vprops, source_edge=source_edge, now=now))

            for field, label, rel, direction in PROVISION_ENTITY_EDGES:
                for key in prov.get(field, []):
                    relationships += _link_directed(vid, rel, label, key, direction)
            for field, rel, direction in PROVISION_PAIR_EDGES:
                if prov.get(field):
                    label, key = prov[field]
                    relationships += _link_directed(vid, rel, label, key, direction)
            for field, label, rel, direction in PROVISION_SINGLE_EDGES:
                if prov.get(field):
                    relationships += _link_directed(vid, rel, label,
                                                    prov[field], direction)

        if not dry_run:
            for prov in policy["provisions"]:
                for field, rel in PROVISION_LINKS:
                    if prov.get(field):
                        relationships += gi.link(
                            from_label="PolicyProvision", from_id=prov[field],
                            rel=rel, to_label="PolicyProvision", to_id=prov["pid"])

    # Policy-to-policy edges run last, in their own pass. A policy can be
    # superseded by one that appears later in the file, and MERGE on a MATCH
    # that finds nothing silently does nothing -- so on a fresh graph the
    # first-pass version of this dropped an edge and only a second run fixed it.
    if not dry_run:
        for policy in knowledge["policies"]:
            if policy.get("superseded_by"):
                linked = gi.link(from_label="Policy", from_id=policy["policy_id"],
                                 rel="SUPERSEDED_BY", to_label="Policy",
                                 to_id=policy["superseded_by"])
                if not linked:
                    raise RuntimeError(
                        f"SUPERSEDED_BY {policy['policy_id']} -> "
                        f"{policy['superseded_by']} matched no nodes")
                relationships += linked

    counts = {"seen": seen, "created": created, "relationships": relationships,
              "run_at": now, "dry_run": dry_run}
    if not dry_run:
        counts["graph_counts"] = gi.counts()
    return counts


def _link_directed(provision_id, rel, label, key, direction):
    if direction == "forward":
        return gi.link(from_label="PolicyProvision", from_id=provision_id,
                       rel=rel, to_label=label, to_id=key)
    return gi.link(from_label=label, from_id=key, rel=rel,
                   to_label="PolicyProvision", to_id=provision_id)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="in_path", default=IN_PATH)
    ap.add_argument("--report", default=REPORT_PATH)
    ap.add_argument("--validation", default=VALIDATION_PATH)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skip-validation-check", action="store_true")
    args = ap.parse_args()

    if not args.skip_validation_check and os.path.exists(args.validation):
        report = json.load(open(args.validation, encoding="utf-8"))
        if report.get("blocking"):
            raise SystemExit(
                f"{args.validation} reports {report['severe']} severe errors. "
                "Fix them and re-run scripts.validate_policies first.")

    knowledge = json.load(open(args.in_path, encoding="utf-8"))
    if not args.dry_run:
        verify_connection()
    try:
        result = ingest(knowledge, dry_run=args.dry_run)
    finally:
        close_driver()

    print("\n  node type    seen  created")
    for key in result["seen"]:
        print(f"  {key:<12} {result['seen'][key]:>4}  {result['created'][key]:>7}")
    print(f"  relationships merged: {result['relationships']}")
    if "graph_counts" in result:
        print("\n  graph totals:")
        for key, value in result["graph_counts"].items():
            print(f"    {key:<20} {value}")
    if not args.dry_run:
        os.makedirs(os.path.dirname(args.report), exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)
        print(f"\nWrote {args.report}")


if __name__ == "__main__":
    main()

"""Stage 3: validate data/policy_knowledge.json before anything touches Neo4j.

    data/policy_knowledge.json -> data/policy_validation_report.json

Blocks the ingest on severe errors, the same contract scripts/validate_pyq.py
uses. Severe means the graph would be wrong or unbuildable: a duplicate id, a
dangling reference, a provision with no page, a policy pointing at a document
that was never fetched.

Warnings are reported and do not block: a provision with no numbers, a policy
with no aliases, an entity nothing links to.

    .venv/bin/python -m scripts.validate_policies
"""
import argparse
import json
import os
from collections import Counter, defaultdict

from graph.policy_ingestion import (DEFINES_KINDS, ENTITY_LABELS,
                                    SPECIFIES_KINDS)

IN_PATH = "data/policy_knowledge.json"
DISCOVERY_PATH = "data/policy_discovery.json"
REPORT_PATH = "data/policy_validation_report.json"

VALID_KINDS = DEFINES_KINDS | SPECIFIES_KINDS
# Entity references written as {"label": "key"} pairs inside a provision.
ENTITY_REF_FIELDS = {
    "requires_forms": "Form",
    "uses_portals": "Portal",
}
# Entity references written as ["Label", "key"] pairs.
PAIR_REF_FIELDS = ["responsible", "approved_by", "escalates_to"]


def validate(knowledge: dict, discovery: dict | None) -> dict:
    errors, warnings = [], []
    stats = Counter()

    doc_ids = {d["doc_id"] for d in knowledge["documents"]}
    category_keys = {c["category_key"] for c in knowledge["categories"]}
    entity_keys = defaultdict(set)
    for entity in knowledge["entities"]:
        label = entity["label"]
        if label not in ENTITY_LABELS:
            errors.append(f"entity {entity['entity_key']}: unknown label {label!r}")
        entity_keys[label].add(entity["entity_key"])
    all_entity_keys = {k for keys in entity_keys.values() for k in keys}

    for name, values in (("document", [d["doc_id"] for d in knowledge["documents"]]),
                         ("category", [c["category_key"] for c in knowledge["categories"]]),
                         ("entity", [e["entity_key"] for e in knowledge["entities"]]),
                         ("policy", [p["policy_id"] for p in knowledge["policies"]])):
        for key, count in Counter(values).items():
            if count > 1:
                errors.append(f"duplicate {name} id: {key} appears {count} times")

    # Every document named in the knowledge file must have actually been
    # fetched, unless it is explicitly an off-handbook supplement.
    if discovery:
        fetched = {d.get("filename") for d in discovery["documents"]
                   if d.get("status") == "FETCHED"}
        for doc in knowledge["documents"]:
            if doc.get("source_type") == "official_site_supplement":
                stats["documents_off_handbook"] += 1
                continue
            if doc["filename"] not in fetched:
                errors.append(f"document {doc['doc_id']}: filename "
                              f"{doc['filename']!r} was not fetched by discovery")

    provision_ids = []
    policy_ids = {p["policy_id"] for p in knowledge["policies"]}

    for policy in knowledge["policies"]:
        pid = policy["policy_id"]
        stats["policies"] += 1
        if policy["category_key"] not in category_keys:
            errors.append(f"policy {pid}: unknown category {policy['category_key']!r}")
        if policy["doc_id"] not in doc_ids:
            errors.append(f"policy {pid}: unknown doc_id {policy['doc_id']!r}")
        if policy.get("superseded_by") and policy["superseded_by"] not in policy_ids:
            errors.append(f"policy {pid}: superseded_by names unknown policy "
                          f"{policy['superseded_by']!r}")
        if not policy.get("aliases"):
            warnings.append(f"policy {pid}: no aliases, retrieval will only match the name")
        if policy.get("institution") != "KJSIT":
            errors.append(f"policy {pid}: institution is {policy.get('institution')!r}, "
                          "expected 'KJSIT' - this corpus is KJSIT only")

        for field in ("applies_to", "involves", "references"):
            for ref in policy.get(field, []):
                if len(ref) != 2:
                    errors.append(f"policy {pid}: malformed {field} entry {ref!r}")
                    continue
                label, key = ref
                if label not in ENTITY_LABELS:
                    errors.append(f"policy {pid}: {field} uses unknown label {label!r}")
                elif key not in entity_keys[label]:
                    errors.append(f"policy {pid}: {field} names unknown "
                                  f"{label} {key!r}")

        local_provisions = set()
        for prov in policy["provisions"]:
            vid = prov["pid"]
            provision_ids.append(vid)
            stats["provisions"] += 1
            stats[f"kind_{prov['kind']}"] += 1
            local_provisions.add(vid)
            if prov["kind"] not in VALID_KINDS:
                errors.append(f"provision {vid}: unknown kind {prov['kind']!r}")
            if not prov.get("page"):
                errors.append(f"provision {vid}: no page number - source "
                              "traceability would be lost")
            if not prov.get("section"):
                errors.append(f"provision {vid}: no section heading")
            if not prov.get("text", "").strip():
                errors.append(f"provision {vid}: empty text")
            if prov.get("doc_id_override") and prov["doc_id_override"] not in doc_ids:
                errors.append(f"provision {vid}: doc_id_override names unknown "
                              f"document {prov['doc_id_override']!r}")
            if prov.get("numbers"):
                stats["provisions_with_numbers"] += 1
                for number in prov["numbers"]:
                    if "value" not in number or "unit" not in number:
                        errors.append(f"provision {vid}: number entry missing "
                                      f"value or unit: {number!r}")
            if prov.get("ambiguity"):
                stats["provisions_flagged_ambiguous"] += 1
            if prov.get("superseded_note"):
                stats["provisions_flagged_superseded"] += 1

            for field, label in ENTITY_REF_FIELDS.items():
                for key in prov.get(field, []):
                    if key not in entity_keys[label]:
                        errors.append(f"provision {vid}: {field} names unknown "
                                      f"{label} {key!r}")
            for field in PAIR_REF_FIELDS:
                ref = prov.get(field)
                if not ref:
                    continue
                label, key = ref
                if label not in ENTITY_LABELS:
                    errors.append(f"provision {vid}: {field} uses unknown label {label!r}")
                elif key not in entity_keys[label]:
                    errors.append(f"provision {vid}: {field} names unknown {label} {key!r}")
            for field, label in (("scheme", "Scheme"), ("references_org", "ExternalOrganization"),
                                 ("applies_to_category", "StudentCategory"),
                                 ("involves_committee", "Committee")):
                key = prov.get(field)
                if key and key not in entity_keys[label]:
                    errors.append(f"provision {vid}: {field} names unknown {label} {key!r}")

        # Provision-to-provision links must stay inside the same policy, so a
        # penalty can never end up hanging off an unrelated rule.
        for prov in policy["provisions"]:
            for field in ("consequence_of", "exception_to"):
                target = prov.get(field)
                if target and target not in local_provisions:
                    errors.append(f"provision {prov['pid']}: {field} names "
                                  f"{target!r}, which is not a provision of {pid}")

    for key, count in Counter(provision_ids).items():
        if count > 1:
            errors.append(f"duplicate provision id: {key} appears {count} times")

    linked_entities = set()
    for policy in knowledge["policies"]:
        for field in ("applies_to", "involves", "references"):
            for label, key in policy.get(field, []):
                linked_entities.add(key)
        for prov in policy["provisions"]:
            for field in ENTITY_REF_FIELDS:
                linked_entities.update(prov.get(field, []))
            for field in PAIR_REF_FIELDS:
                if prov.get(field):
                    linked_entities.add(prov[field][1])
            for field in ("scheme", "references_org", "applies_to_category",
                          "involves_committee"):
                if prov.get(field):
                    linked_entities.add(prov[field])
    orphans = sorted(all_entity_keys - linked_entities)
    for key in orphans:
        warnings.append(f"entity {key}: nothing links to it (it will be an "
                        "isolated node reachable only by name)")
    stats["orphan_entities"] = len(orphans)

    return {
        "errors": errors,
        "warnings": warnings,
        "stats": dict(sorted(stats.items())),
        "severe": len(errors),
        "blocking": bool(errors),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="in_path", default=IN_PATH)
    ap.add_argument("--discovery", default=DISCOVERY_PATH)
    ap.add_argument("--report", default=REPORT_PATH)
    args = ap.parse_args()

    knowledge = json.load(open(args.in_path, encoding="utf-8"))
    discovery = (json.load(open(args.discovery, encoding="utf-8"))
                 if os.path.exists(args.discovery) else None)
    if discovery is None:
        print(f"NOTE: {args.discovery} not found; skipping the fetched-document check.")

    report = validate(knowledge, discovery)
    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)

    for key, value in report["stats"].items():
        print(f"  {key:<34} {value}")
    print(f"\n  errors   {len(report['errors'])}")
    print(f"  warnings {len(report['warnings'])}")
    for err in report["errors"][:40]:
        print(f"    ERROR   {err}")
    for warn in report["warnings"][:10]:
        print(f"    warning {warn}")
    if len(report["warnings"]) > 10:
        print(f"    ... and {len(report['warnings']) - 10} more warnings")
    print(f"\nWrote {args.report}")
    if report["blocking"]:
        raise SystemExit("Validation failed. Ingest is blocked.")


if __name__ == "__main__":
    main()

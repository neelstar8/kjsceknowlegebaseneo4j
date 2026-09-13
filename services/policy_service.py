"""Question -> Neo4j -> sourced policy answer. Deterministic retrieval.

Routing matches the question against vocabularies read out of the graph
itself - policy names, aliases and entity names - the same pattern
services/faculty_service._build_index() and services/pyq_service use, so the
router grows automatically as the knowledge base grows.

Two things this module will not do, both deliberate:

  It will not answer from a superseded policy. The corpus holds a 2018 edition
  whose examination rules were replaced when the institute became autonomous.
  Those provisions stay in the graph as version history and are reachable, but
  only when the caller explicitly asks for them.

  It will not answer at all when retrieval finds nothing. A policy question
  with no supporting provision gets "not in the policy documents I hold",
  named back to the student, plus what to ask for instead. Every fact it does
  return carries its document, page and section.
"""
import re
from functools import lru_cache

from graph import policy_queries as q

# Aliases that are ordinary English words match nearly every question, so they
# only count when the question is otherwise about that topic. Same guard
# services/pyq_service.py needed for the 'IS' (Information Security) alias.
STOPWORD_ALIASES = {"about institute", "discipline", "quality policy", "mission",
                    "vision", "insurance", "forms", "committees", "internship"}
MIN_ALIAS_LENGTH = 4


@lru_cache(maxsize=1)
def _index():
    """Policy names, aliases and entity names, read from the graph."""
    policies = q.policy_vocabulary()
    entities = q.entity_vocabulary()
    alias_to_policy = {}
    for policy in policies:
        terms = [policy["name"]] + (policy["aliases"] or [])
        for term in terms:
            key = term.lower().strip()
            if len(key) < MIN_ALIAS_LENGTH:
                continue
            # First policy to claim an alias keeps it; the knowledge file is
            # ordered so the current policy is authored before the superseded
            # one on the same topic.
            alias_to_policy.setdefault(key, policy)
    entity_terms = {}
    for entity in entities:
        if entity["name"]:
            entity_terms.setdefault(entity["name"].lower().strip(), entity)
    return {"policies": policies, "alias_to_policy": alias_to_policy,
            "entity_terms": entity_terms}


def reset_index():
    """Drop the cached vocabulary. Call after a re-ingest."""
    _index.cache_clear()


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def match_policy(question: str) -> dict | None:
    """Longest alias wins, so 'examination policy' beats 'policy'."""
    normalized = _normalize(question)
    best = None
    for alias, policy in _index()["alias_to_policy"].items():
        if alias in STOPWORD_ALIASES and alias not in normalized:
            continue
        if alias in normalized and (best is None or len(alias) > len(best[0])):
            best = (alias, policy)
    return {"alias": best[0], **best[1]} if best else None


def match_entities(question: str) -> list[dict]:
    normalized = _normalize(question)
    found = []
    for term, entity in _index()["entity_terms"].items():
        if len(term) >= MIN_ALIAS_LENGTH and term in normalized:
            found.append(entity)
    return found


SKIP_WORDS = {"what", "the", "is", "are", "for", "how", "can", "and", "you",
              "does", "who", "with", "from", "that", "this", "any", "all",
              "get", "there", "when", "where", "which", "will", "was", "why",
              "tell", "give", "about", "much", "many", "have", "has", "not",
              "kjsit", "kjsieit", "college", "institute", "please", "need",
              "should", "must", "would", "could", "they", "their", "our"}
# Words so common in this corpus that matching one proves nothing about
# relevance. A hit has to land on something more specific than "policy".
WEAK_TERMS = {"policy", "policies", "rule", "rules", "student", "students",
              "procedure", "institute", "year", "years", "marks", "exam"}
# A provision has to match at least this many distinct question terms to count.
# Without this the Lucene OR query returns a plausible-looking answer to
# literally any question -- which is the one failure mode this system must not
# have, because a sourced-looking wrong answer is worse than no answer.
MIN_TERM_COVERAGE = 2
# Fulltext hits to score before filtering. Wide, because the ranking that
# matters is the term-coverage one below, not Lucene's.
CANDIDATE_POOL = 60


def _content_terms(question: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9\-]{2,}", question)
    return [w.lower() for w in words if w.lower() not in SKIP_WORDS]


def _fulltext_query(question: str) -> str:
    """Turn the question into a Lucene OR query over the meaningful words."""
    terms = _content_terms(question)
    return " OR ".join(terms) if terms else question


def _stem(term: str) -> str:
    """Prefix stem, so 'percentage' reaches 'percent' and 'timings' reaches 'timing'.

    Five characters is short enough to survive the inflections this corpus
    actually uses and long enough that unrelated words do not collide.
    """
    return term[:5] if len(term) >= 6 else term


def _haystack(row: dict) -> str:
    """Everything about a provision a question could legitimately be asking about.

    number_labels belongs here: "minimum marks for a pass" is the structured
    part of the provision, and a student asking for the minimum pass mark is
    asking about exactly that, not about the sentence wrapped around it.
    """
    parts = [row.get("text", ""), row.get("topic", ""), row.get("policy_name", ""),
             row.get("section", ""), row.get("ambiguity", "")]
    parts.extend(row.get("number_labels") or [])
    parts.extend(row.get("number_units") or [])
    return " ".join(p for p in parts if p).lower()


def _matches(stem: str, haystack: str) -> bool:
    """A word in the haystack must START with the stem.

    Plain substring matching is what made 'fine' match inside 'define' and
    'day' match inside 'today', which pulled the library vision statement to
    the top of a question about library fines.
    """
    return re.search(r"\b" + re.escape(stem), haystack) is not None


def _coverage(row: dict, terms: list[str]) -> tuple[int, int, bool]:
    """(terms matched, strong terms matched, whether a strong term is topical)."""
    haystack = _haystack(row)
    # The provision's own topic only. Including the policy name here made every
    # provision of the Higher Studies policy "on topic" for any question
    # containing the word "study", which buried the actual answer.
    topical = (row.get("topic") or "").lower()
    matched = {t for t in terms if _matches(_stem(t), haystack)}
    strong = {t for t in matched if t not in WEAK_TERMS}
    on_topic = any(_matches(_stem(t), topical) for t in strong)
    return len(matched), len(strong), on_topic


def _relevant(rows: list[dict], terms: list[str]) -> list[dict]:
    """Drop hits that share too little with the question to be an answer.

    Two ways to survive, because a fixed floor gets both cases wrong:

      two matched terms, at least one of them distinctive -- the ordinary case;
      one distinctive term, but it is what the provision is *about* -- so
      "what happens if my attendance is low" still reaches the provision whose
      topic is 'attendance defaulter consequence'.

    A single distinctive term buried in the body is not enough. That is what
    stops "favourite food" from being answered out of the rule that bans food
    in the examination hall.
    """
    if not terms:
        return []
    required = min(MIN_TERM_COVERAGE, len(terms))
    kept = []
    for row in rows:
        matched, strong, on_topic = _coverage(row, terms)
        if strong < 1:
            continue
        if matched >= required or on_topic:
            row["_matched_terms"] = matched
            row["_on_topic"] = on_topic
            kept.append(row)
    kept.sort(key=lambda r: (r["_on_topic"], r["_matched_terms"]), reverse=True)
    return kept


def _attach_forms(provisions: list[dict]) -> list[dict]:
    """Fold each provision's REQUIRES->Form links onto the row for build_answer.

    provision_requirements() already existed for this; nothing in the answer
    path called it, so form links found their way into the graph but never
    into a student-facing answer.
    """
    for row in provisions:
        reqs = q.provision_requirements(row["provision_id"])
        row["_forms"] = reqs.get("forms") or []
    return provisions


def retrieve(question: str, *, include_superseded: bool = False,
             limit: int = 8) -> dict:
    """Route the question and pull the supporting provisions."""
    policy = match_policy(question)
    entities = match_entities(question)
    terms = _content_terms(question)
    provisions = _relevant(
        q.search_provisions(_fulltext_query(question), limit=CANDIDATE_POOL,
                            include_superseded=include_superseded),
        terms)

    # Naming a policy is a preference, not an override. Putting every provision
    # of the named policy ahead of everything else meant "what is the library
    # fine" was answered with the library's vision statement, while the
    # provision that actually records the fine gap sat in a sibling policy and
    # never made the cut.
    # "What is the IT policy?" carries no distinctive term at all -- IT is two
    # letters and "policy" is in every provision here. Naming the policy is the
    # whole question, so answer it with that policy.
    if policy and not [t for t in terms if t not in WEAK_TERMS]:
        rows = q.provisions_for_policy(policy["policy_id"])
        for row in rows:
            row.update(policy_id=policy["policy_id"], policy_name=policy["name"],
                       policy_status=policy["status"])
        return {"question": question, "matched_policy": policy,
                "matched_entities": entities,
                "provisions": _attach_forms(rows[:limit])}

    if policy:
        known = {row["provision_id"] for row in provisions}
        extra = [row for row in q.provisions_for_policy(policy["policy_id"])
                 if row["provision_id"] not in known]
        for row in extra:
            row.update(policy_id=policy["policy_id"], policy_name=policy["name"],
                       policy_status=policy["status"], score=0.0)
        provisions = provisions + _relevant(extra, terms)
        for row in provisions:
            row["_own"] = row["policy_id"] == policy["policy_id"]
        provisions.sort(key=lambda r: (r["_on_topic"], r["_matched_terms"],
                                       r.get("_own", False), r.get("score") or 0.0),
                        reverse=True)
    return {"question": question, "matched_policy": policy,
            "matched_entities": entities,
            "provisions": _attach_forms(provisions[:limit])}


def _format_numbers(row: dict) -> str:
    values = row.get("number_values") or []
    if not values:
        return ""
    units = row.get("number_units") or []
    labels = row.get("number_labels") or []
    parts = []
    for i, value in enumerate(values):
        value_text = f"{value:g}"
        unit = units[i] if i < len(units) else ""
        label = labels[i] if i < len(labels) else ""
        parts.append(f"{value_text} {unit}".strip() + (f" ({label})" if label else ""))
    return "; ".join(parts)


def build_answer(result: dict) -> str:
    """Plain text with a citation under every fact. No model involved."""
    provisions = result["provisions"]
    if not provisions:
        return _no_answer(result)

    lines = []
    policy = result.get("matched_policy")
    if policy:
        detail = q.policy_by_id(policy["policy_id"])
        if detail:
            lines.append(f"{detail['name']} ({detail['category']})")
            if detail.get("purpose"):
                lines.append(f"Purpose: {detail['purpose']}")
            if detail.get("scope"):
                lines.append(f"Scope: {detail['scope']}")
            if detail.get("status") == "superseded" and detail.get("superseded_by_name"):
                lines.append(f"NOTE: This policy is SUPERSEDED by "
                             f"{detail['superseded_by_name']}.")
            if detail.get("version_note"):
                lines.append(f"VERSION WARNING: {detail['version_note']}")
            if detail.get("completeness_note"):
                lines.append(f"NOTE: {detail['completeness_note']}")
            if detail.get("source_note"):
                lines.append(f"NOTE: {detail['source_note']}")
            lines.append("")

    for row in provisions:
        lines.append(f"- {row['text']}")
        numbers = _format_numbers(row)
        if numbers:
            lines.append(f"  Key figures: {numbers}")
        if row.get("ambiguity"):
            lines.append(f"  FLAGGED: {row['ambiguity']}")
        if row.get("superseded_note"):
            lines.append(f"  VERSION: {row['superseded_note']}")
        lines.append(f"  Source: {row.get('document_title') or row.get('policy_name')}"
                     f", page {row.get('page')}, section {row.get('section')}")
        for form in row.get("_forms") or []:
            if form.get("url"):
                lines.append(f"  Form: {form['name']} - {form['url']}")
            elif form.get("name"):
                lines.append(f"  Form: {form['name']}")
        lines.append("")
    lines.append("Institution: K J Somaiya Institute of Technology (KJSIT), "
                 "formerly KJSIEIT. These policies are KJSIT's own and are not "
                 "stated to apply to any other Somaiya institute.")
    return "\n".join(lines).strip()


def _no_answer(result: dict) -> str:
    lines = ["I don't have that in the KJSIT Institute Policy Handbook documents "
             "I hold, so I won't guess."]
    if result.get("matched_policy"):
        policy = result["matched_policy"]
        lines.append(f"I do hold the '{policy['name']}' policy, but nothing in it "
                     "answers this question.")
    categories = q.category_tree()
    lines.append("")
    lines.append("What I do hold, by handbook category:")
    for category in categories:
        names = [p["name"] for p in category["policies"] if p["policy_id"]]
        lines.append(f"  {category['category']}: {len(names)} policies")
    return "\n".join(lines)


def answer_policy_question(question: str, *, debug: bool = False,
                           include_superseded: bool = False) -> dict:
    result = retrieve(question, include_superseded=include_superseded)
    answer = build_answer(result)
    payload = {
        "answer": answer,
        "matched_policy": (result["matched_policy"] or {}).get("policy_id"),
        "sources": [
            {"policy": row.get("policy_name"), "document": row.get("document_title"),
             "page": row.get("page"), "section": row.get("section"),
             "url": row.get("source_url"), "status": row.get("policy_status")}
            for row in result["provisions"]
        ],
        "forms": [
            form for row in result["provisions"] for form in (row.get("_forms") or [])
        ],
        "found": bool(result["provisions"]),
    }
    if debug:
        payload["debug"] = {
            "fulltext_query": _fulltext_query(question),
            "matched_entities": [e["entity_key"] for e in result["matched_entities"]],
            "provision_ids": [r["provision_id"] for r in result["provisions"]],
        }
    return payload

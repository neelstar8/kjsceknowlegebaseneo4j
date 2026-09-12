"""Ties Neo4j retrieval + Qwen together for faculty questions.

Flow:
  user question -> deterministic routing -> Neo4j -> context -> Qwen -> answer

Retrieval stays deterministic: Qwen never writes Cypher. The router matches
the question against vocabularies (names, departments, designations, research
topics) read out of the graph itself, so it grows automatically as the
directory grows.
"""
import re

from graph import faculty_queries as q
from llm.qwen import ask_qwen
from llm.system_prompt import KJGPT_SYSTEM_PROMPT

MAX_LIST_RESULTS = 40

# Words that are part of a title/honorific, never a distinguishing name token.
TITLE_TOKENS = {"dr", "prof", "mr", "mrs", "ms", "adv", "ca", "cs", "er", "shri"}

DESIGNATION_TERMS = [
    "assistant professor",
    "associate professor",
    "distinguished professor",
    "visiting faculty",
    "adjunct faculty",
    "professor of practice",
    "professor",
    "lecturer",
    "librarian",
    "principal",
    "director",
    "dean",
]

_index_cache: dict | None = None


def _build_index() -> dict:
    """Read the vocabularies the router matches against, once per process."""
    rows = q.list_with_departments(limit=10000)
    people = q.run_all_names()

    departments, schools = set(), set()
    for r in rows:
        if r.get("department"):
            departments.add(r["department"])
        if r.get("school"):
            schools.add(r["school"])

    topics = set(q.distinct_research_topics())
    subjects = set(q.distinct_subjects())

    return {
        "people": people,
        "departments": sorted(departments, key=len, reverse=True),
        "schools": sorted(schools, key=len, reverse=True),
        "topics": sorted(topics, key=len, reverse=True),
        "subjects": sorted(subjects, key=len, reverse=True),
    }


def get_index(refresh: bool = False) -> dict:
    global _index_cache
    if _index_cache is None or refresh:
        _index_cache = _build_index()
    return _index_cache


def _name_tokens(name: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z]+", (name or "").lower())
    return [t for t in tokens if t not in TITLE_TOKENS and len(t) >= 3]


def detect_faculty_name(question: str) -> str | None:
    """Return the faculty_id of the person the question is about, or None.

    Requires either a multi-token name match (e.g. "vaibhav vasani") or a
    single distinctive token that belongs to exactly one member, so a common
    first name shared by many members does not silently pick one at random.
    """
    q_lower = question.lower()
    q_tokens = set(re.findall(r"[a-zA-Z]+", q_lower))

    scored = []
    for person in get_index()["people"]:
        tokens = _name_tokens(person["name"])
        if not tokens:
            continue
        hits = [t for t in tokens if t in q_tokens]
        if hits:
            scored.append((len(hits), person, hits))

    if not scored:
        return None

    best = max(s[0] for s in scored)
    winners = [s for s in scored if s[0] == best]

    if best >= 2:
        return winners[0][1]["faculty_id"]
    if best == 1 and len(winners) == 1:
        # A single token, but it identifies exactly one person in the whole
        # directory -- e.g. an unusual surname.
        return winners[0][1]["faculty_id"]
    return None


def _first_match(question: str, vocabulary: list[str]) -> str | None:
    q_lower = question.lower()
    for term in vocabulary:
        if term and term.lower() in q_lower:
            return term
    return None


FIELD_LABELS = {
    "title": "Title",
    "designation": "Designation",
    "department": "Department",
    "school": "School",
    "institution": "Institution",
    "campus": "Campus",
    "member_type": "Member Type",
    "location": "Location",
    "official_email": "Email",
    "phone": "Phone",
    "landline": "Landline",
    "extension": "Extension",
    "office_address": "Office Address",
    "visiting_hours": "Timings for Visitors",
    "profile_url": "Faculty Profile URL",
    "faculty_profile_url": "Faculty Profile URL",
    "introduction": "Introduction",
    "linkedin_url": "LinkedIn",
    "google_scholar_url": "Google Scholar",
    "vidwan_url": "Vidwan Profile",
    "orcid_url": "ORCID",
    "scopus_url": "Scopus",
    "scopus_id": "Scopus ID",
    "web_of_science_id": "Web of Science ID",
    "researchgate_url": "ResearchGate",
    "cv_url": "Curriculum Vitae",
    "education": "Education",
    "qualifications": "Qualifications",
    "current_position": "Current Position",
    "joined_somaiya": "Joined Somaiya",
    "total_teaching_experience": "Total Teaching Experience",
    "experience": "Experience",
    "subjects_taught": "Subjects Taught",
    "courses_taught": "Courses Taught",
    "research_interests": "Research Interests",
    "research_specialization": "Research Specialisation",
    "research_specialisation": "Research Specialisation",
    "areas_of_expertise": "Areas of Expertise",
    "expertise": "Expertise",
    "roles_and_responsibilities": "Roles and Responsibilities",
    "professional_experience": "Professional Experience",
    "projects": "Projects",
    "publications": "Publications",
    "selected_publications": "Selected Publications",
    "proceedings": "Conference Proceedings",
    "books": "Books",
    "book_chapters": "Book Chapters",
    "patents": "Patents / IPR",
    "mdp_fdp": "MDP / FDP",
    "awards": "Awards",
    "professional_memberships": "Professional Memberships",
    "certifications": "Certifications",
    "sources": "Sources",
    "last_verified": "Last Verified",
}


def build_context(faculty_node: dict) -> str:
    """Convert one FacultyMember node's properties into clean text context."""
    lines = [f"Faculty Member: {faculty_node.get('name', 'Unknown')}"]
    for key, label in FIELD_LABELS.items():
        value = faculty_node.get(key)
        if value in (None, "", [], "TODO_VERIFY"):
            continue
        if isinstance(value, list):
            value = "; ".join(str(v) for v in value)
        lines.append(f"{label}: {value}")
    return "\n".join(lines)


def build_list_context(nodes: list[dict], heading: str) -> str:
    """Compact context for 'which faculty ...' questions over many people."""
    lines = [f"{heading} ({len(nodes)} matching faculty members):"]
    for n in nodes:
        parts = [n.get("name", "Unknown")]
        if n.get("designation"):
            parts.append(n["designation"])
        if n.get("department"):
            parts.append(f"Department: {n['department']}")
        if n.get("school"):
            parts.append(n["school"])
        lines.append("- " + " | ".join(parts))
    return "\n".join(lines)


def retrieve(question: str) -> dict:
    """Deterministically pick a retrieval strategy and run it.

    Returns {"strategy", "context", "nodes", "match"} or a context of None
    when nothing in the knowledge base matches.
    """
    index = get_index()

    faculty_id = detect_faculty_name(question)
    if faculty_id:
        node = q.find_by_faculty_id(faculty_id)
        if node:
            return {
                "strategy": "person",
                "match": node.get("name"),
                "nodes": [node],
                "context": build_context(node),
            }

    subject = _first_match(question, index["subjects"])
    topic = _first_match(question, index["topics"])
    department = _first_match(question, index["departments"])
    designation = _first_match(question, DESIGNATION_TERMS)
    school = _first_match(question, index["schools"])

    # More specific signals win over more generic ones.
    if topic and ("research" in question.lower() or "interest" in question.lower()):
        nodes = q.find_by_research_interest(topic, limit=MAX_LIST_RESULTS)
        heading = f"Faculty members with research interest matching '{topic}'"
        strategy = "research_interest"
    elif subject and ("teach" in question.lower() or "subject" in question.lower()
                      or "course" in question.lower()):
        nodes = q.find_by_subject(subject, limit=MAX_LIST_RESULTS)
        heading = f"Faculty members teaching '{subject}'"
        strategy = "subject"
    elif department:
        nodes = q.find_by_department(department, limit=MAX_LIST_RESULTS)
        heading = f"Faculty members in the {department} department"
        strategy = "department"
    elif designation:
        nodes = q.find_by_designation(designation, limit=MAX_LIST_RESULTS)
        heading = f"Faculty members with designation '{designation}'"
        strategy = "designation"
    elif school:
        nodes = q.find_by_school(school, limit=MAX_LIST_RESULTS)
        heading = f"Faculty members at {school}"
        strategy = "school"
    elif topic:
        nodes = q.find_by_research_interest(topic, limit=MAX_LIST_RESULTS)
        heading = f"Faculty members with research interest matching '{topic}'"
        strategy = "research_interest"
    elif subject:
        nodes = q.find_by_subject(subject, limit=MAX_LIST_RESULTS)
        heading = f"Faculty members teaching '{subject}'"
        strategy = "subject"
    else:
        return {"strategy": "none", "match": None, "nodes": [], "context": None}

    if not nodes:
        return {"strategy": strategy, "match": None, "nodes": [], "context": None}

    return {
        "strategy": strategy,
        "match": heading,
        "nodes": nodes,
        "context": build_list_context(nodes, heading),
    }


def answer_faculty_question(question: str, debug: bool = False) -> dict:
    """Run the full retrieval -> context -> Qwen flow for one question."""
    trace = {"question": question}

    result = retrieve(question)
    trace["strategy"] = result["strategy"]
    trace["match"] = result["match"]
    trace["result_count"] = len(result["nodes"])
    trace["context"] = result["context"]

    if not result["context"]:
        answer = (
            "I couldn't find anything matching that question in the current "
            "KJGPT knowledge base, which currently covers the official Somaiya "
            "faculty directory."
        )
        trace["answer"] = answer
        return trace if debug else {"answer": answer}

    user_prompt = (
        f"KNOWLEDGE BASE CONTEXT:\n{result['context']}\n\n"
        f"USER QUESTION:\n{question}"
    )
    answer = ask_qwen(KJGPT_SYSTEM_PROMPT, user_prompt)
    trace["answer"] = answer

    return trace if debug else {"answer": answer}

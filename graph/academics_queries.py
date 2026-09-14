"""Read side for the official Academics documents.

Every query is scoped by `source_type`, so an academic question can never
surface Faculty, Internship, Attendance, Admission or Placement knowledge, and
never a PYQ question paper. Examination calendars live under their own
`examination_calendar` type and are only returned when the caller asks for them.
"""
from graph.neo4j_driver import run_query

CALENDAR = "academic_calendar"
INDEXES = {"timetable": "class_timetable_index",
           "syllabus": "syllabus_index",
           "roll_call": "roll_call_index"}
PLAN = "academic_development_plan"
STRATEGIC = "strategic_plan"
SOFTWARE = "software_resource"

ALL_TYPES = [CALENDAR, *INDEXES.values(), PLAN, STRATEGIC, SOFTWARE]

_DOC = """
    d.doc_id AS doc_id, d.title AS title, d.source_url AS source_url,
    d.alternate_source_url AS alternate_source_url,
    d.source_type AS source_type, d.academics_subcategory AS subcategory,
    d.resource_kind AS resource_kind, d.document_type AS document_type,
    d.academic_year AS academic_year, d.programmes AS programmes,
    d.levels AS levels, d.level_note AS level_note, d.terms AS terms,
    d.document_status AS document_status, d.document_date AS document_date,
    d.issuing_authority AS issuing_authority, d.pages AS pages,
    d.content_note AS content_note,
    d.event_terms AS event_terms, d.event_names AS event_names,
    d.event_schedules AS event_schedules, d.event_count AS event_count,
    d.branch_names AS branch_names, d.branch_urls AS branch_urls,
    d.goal_numbers AS goal_numbers, d.goal_names AS goal_names,
    d.goal_agendas AS goal_agendas, d.plan_period AS plan_period,
    d.section_numbers AS section_numbers, d.section_names AS section_names,
    d.section_parameters AS section_parameters,
    d.section_parameter_ranges AS section_parameter_ranges,
    d.parameter_count AS parameter_count, d.plan_purpose AS plan_purpose,
    d.software AS software, d.provider AS provider, d.audience AS audience,
    d.access_note AS access_note, d.fetch_status AS fetch_status
"""

# A document counts as Academics if it carries an Academics source_type OR is
# linked from the academic parent. The second arm matters for the one calendar
# the Academics section republishes from the Examination section: it is a single
# reused node whose source_type stays 'examination_calendar', and a student
# asking for the 2026-27 academic calendar should still be given it.
BY_TYPES = f"""
MATCH (d:PolicyDocument)
WHERE (d.source_type IN $types
       OR ($include_parent_linked
           AND (:Policy {{policy_id:'teaching_learning_process'}})-[:REFERENCES]->(d)))
  AND ($academic_year IS NULL OR d.academic_year = $academic_year)
  AND ($programme IS NULL OR any(p IN d.programmes WHERE toLower(p) = toLower($programme)))
  AND ($level IS NULL OR any(l IN d.levels WHERE toLower(l) = toLower($level)))
  AND ($calendars_only = false OR d.event_count IS NOT NULL)
RETURN {_DOC}
ORDER BY coalesce(d.academic_year,'') DESC, d.title
"""

ALL_ACADEMIC = f"""
MATCH (d:PolicyDocument) WHERE d.source_type IN $types
RETURN {_DOC}
ORDER BY d.source_type, coalesce(d.academic_year,'') DESC, d.title
"""

YEARS = """
MATCH (d:PolicyDocument {source_type: $calendar})
RETURN d.academic_year AS academic_year, count(*) AS documents
ORDER BY academic_year DESC
"""

PARENT = """
MATCH (p:Policy)-[r:REFERENCES {relation:'official_academic_document'}]->(d:PolicyDocument)
RETURN p.policy_id AS policy_id, p.name AS policy_name, count(d) AS documents
"""


def find(types: list[str], *, academic_year=None, programme=None, level=None,
         calendars_only: bool = False, include_parent_linked: bool = False) -> list[dict]:
    """`include_parent_linked` widens the match to anything hanging off the
    academic parent, which is how the reused examination calendar is reached.
    Only the calendar intent sets it; every other intent stays strictly typed."""
    return run_query(BY_TYPES, {"types": types, "academic_year": academic_year,
                                "programme": programme, "level": level,
                                "calendars_only": calendars_only,
                                "include_parent_linked": include_parent_linked})


def all_academic_documents() -> list[dict]:
    return run_query(ALL_ACADEMIC, {"types": ALL_TYPES})


def academic_years() -> list[dict]:
    return run_query(YEARS, {"calendar": CALENDAR})


def parent() -> list[dict]:
    return run_query(PARENT)


def events_of(row) -> list[dict]:
    names = row.get("event_names") or []
    terms = row.get("event_terms") or []
    scheds = row.get("event_schedules") or []
    return [{"term": terms[i] if i < len(terms) else None, "event": names[i],
             "schedule": scheds[i] if i < len(scheds) else None}
            for i in range(len(names))]


def branches_of(row) -> list[dict]:
    names = row.get("branch_names") or []
    urls = row.get("branch_urls") or []
    return [{"branch": names[i], "url": urls[i] if i < len(urls) else None}
            for i in range(len(names))]


def goals_of(row) -> list[dict]:
    nums = row.get("goal_numbers") or []
    names = row.get("goal_names") or []
    agendas = row.get("goal_agendas") or []
    return [{"number": nums[i] if i < len(nums) else None, "name": names[i],
             "development_agenda": agendas[i] if i < len(agendas) else None}
            for i in range(len(names))]


def sections_of(row) -> list[dict]:
    nums = row.get("section_numbers") or []
    names = row.get("section_names") or []
    params = row.get("section_parameters") or []
    rng = row.get("section_parameter_ranges") or []
    return [{"number": nums[i] if i < len(nums) else None, "name": names[i],
             "parameter_range": rng[i] if i < len(rng) else None,
             "parameters": (params[i].split(" ; ") if i < len(params) else [])}
            for i in range(len(names))]

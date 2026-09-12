"""Turns raw scraped Somaiya records into one common FacultyMember schema.

Two hard rules:

  1. Nothing is invented. If the official source does not state a field, it
     comes out as None / "" / [] -- never a guess.
  2. Parsing is deterministic. The site already labels every block
     ("Education", "Research Papers", ...), so no LLM is involved here.

The site uses several literal placeholders for "empty" ("No Information
Available", "NA", "-"). Those are normalized to nothing.
"""
import re

# Strings the site renders when a section has no content.
PLACEHOLDERS = {
    "",
    "-",
    "--",
    "na",
    "n/a",
    "nil",
    "none",
    "not available",
    "no information available",
    "no information available.",
    "no data available",
    "information not available",
}

TITLE_PREFIXES = ["Dr.", "Prof.", "Mr.", "Mrs.", "Ms.", "Adv.", "CA", "CS", "Er."]

# Panel heading on the profile page -> field on the normalized record.
SECTION_MAP = {
    "introduction": "introduction",
    "education": "education",
    "professional experience": "professional_experience",
    "courses/subjects teaching": "subjects_taught",
    "courses / subjects teaching": "subjects_taught",
    "research specialisation": "research_specialization",
    "research specialization": "research_specialization",
    "consultancy expertise": "areas_of_expertise",
    "consultancy projects": "projects",
    "achievements, recognitions & awards": "awards",
    "achievements, recognitions and awards": "awards",
    "mdp / fdp": "mdp_fdp",
    "mdp/fdp": "mdp_fdp",
    "research papers": "publications",
    "proceedings": "proceedings",
    "books": "books",
    "book chapters": "book_chapters",
    "ipr": "patents",
    "roles and responsibilities": "roles_and_responsibilities",
    "administrative responsibilities": "roles_and_responsibilities",
    "memberships": "professional_memberships",
    "professional memberships": "professional_memberships",
}

# Sidebar link label -> dedicated profile field. Anything unmatched is kept
# under other_profiles so no official link is silently dropped.
LINK_MAP = {
    "google scholar profile": "google_scholar_url",
    "google scholar": "google_scholar_url",
    "vidwan profile": "vidwan_url",
    "vidwan": "vidwan_url",
    "orcid profile": "orcid_url",
    "orcid": "orcid_url",
    "scopus profile": "scopus_url",
    "scopus": "scopus_url",
    "web of science profile": "web_of_science_url",
    "publons profile": "web_of_science_url",
    "researchgate profile": "researchgate_url",
    "researchgate": "researchgate_url",
    "linkedin profile": "linkedin_url",
    "linkedin": "linkedin_url",
    "curriculum vitae": "cv_url",
}

# Sidebar links that are site chrome, not the person's profile.
LINK_IGNORE = {"faculty login", "back to directory", ""}

LIST_FIELDS = [
    "education",
    "professional_experience",
    "subjects_taught",
    "courses_taught",
    "research_specialization",
    "research_interests",
    "areas_of_expertise",
    "projects",
    "awards",
    "mdp_fdp",
    "publications",
    "proceedings",
    "books",
    "book_chapters",
    "patents",
    "roles_and_responsibilities",
    "professional_memberships",
    "certifications",
    "skills",
    "qualifications",
    "name_variations",
    "sources",
]

SCALAR_FIELDS = [
    "faculty_id",
    "name",
    "title",
    "designation",
    "department",
    "school",
    "faculty",
    "institution",
    "sub_institute",
    "campus",
    "official_email",
    "phone",
    "landline",
    "extension",
    "profile_url",
    "photo_url",
    "member_type",
    "office_address",
    "visiting_hours",
    "joining_date",
    "experience",
    "introduction",
    "additional_information",
    "google_scholar_url",
    "vidwan_url",
    "orcid_url",
    "scopus_url",
    "scopus_id",
    "web_of_science_url",
    "web_of_science_id",
    "researchgate_url",
    "linkedin_url",
    "cv_url",
    "last_verified",
]


def is_placeholder(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().lower().strip(".") in {p.strip(".") for p in PLACEHOLDERS}


def clean_scalar(value: str | None) -> str | None:
    """Returns a trimmed string, or None if the source said nothing."""
    if value is None:
        return None
    value = re.sub(r"\s+", " ", value).strip()
    if is_placeholder(value):
        return None
    return value


def clean_list(values) -> list[str]:
    """Drops placeholders/duplicates while preserving source order."""
    if not values:
        return []
    if isinstance(values, str):
        values = [values]
    out, seen = [], set()
    for v in values:
        cleaned = clean_scalar(v)
        if cleaned is None:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(cleaned)
    return out


def split_title(name: str) -> tuple[str | None, str]:
    """Splits "Dr. Vaibhav Prakash Vasani" -> ("Dr.", "Vaibhav Prakash Vasani")."""
    name = re.sub(r"\s+", " ", (name or "")).strip()
    for prefix in TITLE_PREFIXES:
        if name.lower().startswith(prefix.lower() + " "):
            return prefix, name[len(prefix):].strip()
        if name.lower().startswith(prefix.lower().rstrip(".") + " "):
            return prefix, name[len(prefix.rstrip(".")):].strip()
    return None, name


def build_name_variations(full_name: str, bare_name: str) -> list[str]:
    """Only mechanical variations of the official name -- nothing invented."""
    variations = {full_name, bare_name}
    parts = bare_name.split()
    if len(parts) >= 3:
        # First + last, dropping middle names.
        variations.add(f"{parts[0]} {parts[-1]}")
    return sorted(v for v in variations if v)


def _split_contact_details(text: str | None) -> tuple[str | None, str | None]:
    """"Landline No. : NA Extension No. : 9107" -> (landline, extension)."""
    if not text:
        return None, None
    landline = extension = None
    m = re.search(r"Landline\s*No\.?\s*:?\s*(.*?)(?=Extension|$)", text, re.I)
    if m:
        landline = clean_scalar(m.group(1))
    m = re.search(r"Extension\s*No\.?\s*:?\s*(.*)$", text, re.I)
    if m:
        extension = clean_scalar(m.group(1))
    return landline, extension


def _role_line_parts(role_line: str | None) -> tuple[str | None, str | None]:
    """"Assistant Professor at K J Somaiya School of Engineering"."""
    if not role_line:
        return None, None
    m = re.match(r"(.*?)\s+at\s+(.*)$", role_line.strip(), re.I)
    if m:
        return clean_scalar(m.group(1)), clean_scalar(m.group(2))
    return clean_scalar(role_line), None


def _extract_scopus_id(url: str | None) -> str | None:
    if not url:
        return None
    m = re.search(r"authorId=(\d+)", url) or re.search(r"authorID=(\d+)", url)
    return m.group(1) if m else None


def normalize_faculty(raw_faculty: dict, last_verified: str) -> dict:
    """Convert one raw record into the common schema.

    `raw_faculty` is a discovery record:
        {source_id, name, profile_url, raw_data, profile (optional)}
    where `profile` is the output of scraper.parse_profile.
    """
    raw_card = raw_faculty.get("raw_data") or {}
    profile = raw_faculty.get("profile") or {}
    sections = profile.get("sections") or {}
    sidebar = profile.get("sidebar") or {}
    links = profile.get("links") or {}

    # ---- identity ----------------------------------------------------
    full_name = clean_scalar(profile.get("full_name")) or clean_scalar(
        raw_faculty.get("name")
    ) or clean_scalar(raw_card.get("name")) or ""
    title, bare_name = split_title(full_name)

    record: dict = {
        "faculty_id": raw_faculty.get("source_id"),
        "name": full_name,
        "name_variations": build_name_variations(full_name, bare_name),
        "title": title,
    }

    # ---- role / affiliation -----------------------------------------
    role_designation, role_institute = _role_line_parts(profile.get("role_line"))
    record["designation"] = role_designation or clean_scalar(
        raw_card.get("designation")
    )
    institute = (
        clean_scalar(sidebar.get("institute"))
        or role_institute
        or clean_scalar(raw_card.get("institute"))
    )
    record["school"] = institute
    # The directory is organised by institute/school; the parent body is the
    # university. Both are recorded verbatim rather than inferred.
    record["institution"] = institute
    record["sub_institute"] = clean_scalar(raw_card.get("institute")) if (
        clean_scalar(raw_card.get("institute")) != institute
    ) else None
    record["faculty"] = None  # Not exposed by the directory or profile pages.
    record["department"] = clean_scalar(sidebar.get("department"))
    record["campus"] = clean_scalar(raw_card.get("campus"))
    record["member_type"] = clean_scalar(
        profile.get("member_type") or raw_card.get("member_type")
    )

    # ---- contact ------------------------------------------------------
    record["official_email"] = clean_scalar(
        sidebar.get("email") or raw_card.get("email")
    )
    landline, extension = _split_contact_details(sidebar.get("contact_details"))
    record["landline"] = landline
    record["extension"] = extension
    record["phone"] = clean_scalar(raw_card.get("phone")) or landline
    record["office_address"] = clean_scalar(
        sidebar.get("office_address") or raw_card.get("office_address")
    )
    record["visiting_hours"] = clean_scalar(
        sidebar.get("timings") or raw_card.get("timings")
    )
    record["profile_url"] = raw_faculty.get("profile_url")
    record["photo_url"] = clean_scalar(
        profile.get("photo_url") or raw_card.get("photo_url")
    )

    # ---- profile sections --------------------------------------------
    for field in LIST_FIELDS:
        record.setdefault(field, [])
    for heading, block in sections.items():
        field = SECTION_MAP.get(heading.strip().lower())
        if field is None:
            continue
        items = clean_list(block.get("items"))
        if field == "introduction":
            record["introduction"] = clean_scalar(block.get("text"))
        else:
            record[field] = items

    # Courses/subjects: the site has a single list; expose it under both the
    # teaching-oriented names rather than inventing a second list.
    record["courses_taught"] = list(record["subjects_taught"])
    # The site offers no separate "research interests" block; specialisation is
    # the closest official equivalent and is reused verbatim, not invented.
    record["research_interests"] = list(record["research_specialization"])
    record["qualifications"] = list(record["education"])
    record.setdefault("introduction", None)

    # ---- academic profile links --------------------------------------
    other_profiles = {}
    for label, url in links.items():
        key = label.strip().lower()
        if key in LINK_IGNORE:
            continue
        field = LINK_MAP.get(key)
        if field:
            record.setdefault(field, url)
        else:
            other_profiles[label.strip()] = url
    for field in (
        "google_scholar_url",
        "vidwan_url",
        "orcid_url",
        "scopus_url",
        "web_of_science_url",
        "researchgate_url",
        "linkedin_url",
        "cv_url",
    ):
        record.setdefault(field, None)
    record["other_profiles"] = other_profiles
    record["scopus_id"] = _extract_scopus_id(record.get("scopus_url"))
    record["web_of_science_id"] = None  # Not published on the profile page.

    record["professional_profiles"] = {
        k: v
        for k, v in {
            "google_scholar": record["google_scholar_url"],
            "vidwan": record["vidwan_url"],
            "orcid": record["orcid_url"],
            "scopus": record["scopus_url"],
            "web_of_science": record["web_of_science_url"],
            "researchgate": record["researchgate_url"],
            "linkedin": record["linkedin_url"],
            "cv": record["cv_url"],
            **other_profiles,
        }.items()
        if v
    }

    # ---- fields the official source simply does not provide ----------
    record["joining_date"] = None
    record["experience"] = None
    record["additional_information"] = None
    record["certifications"] = []
    record["skills"] = []

    # ---- provenance ---------------------------------------------------
    sources = ["https://www.somaiya.edu/en/contact-us/faculty-directory/"]
    if record["profile_url"]:
        sources.append(record["profile_url"])
    fetched = raw_faculty.get("profile_url_fetched")
    if fetched and fetched not in sources:
        sources.append(fetched)
    record["sources"] = sources
    record["last_verified"] = last_verified
    record["profile_fetched"] = bool(profile)

    return record


# Nested values are fine in JSON but Neo4j properties must be primitives or
# arrays of primitives, so the graph layer uses this flattened view.
NESTED_FIELDS = ("other_profiles", "professional_profiles")


def to_neo4j_properties(record: dict) -> dict:
    """Flatten a normalized record into Neo4j-storable properties.

    Empty values are dropped entirely so a sparse directory record never
    overwrites richer existing data with nulls.
    """
    props = {}
    for key, value in record.items():
        if key in NESTED_FIELDS:
            continue
        if value is None or value == "" or value == []:
            continue
        props[key] = value
    return props

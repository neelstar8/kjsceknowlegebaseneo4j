"""Looks inside a semester-bundle PDF to find which subjects it actually holds.

Only reached for files whose name and folder path establish a semester but no
subject -- 'COMP- SEM- VIII..pdf'. Those bundle one paper per subject sat that
semester, and nothing outside the PDF says which.

What this module is NOT: it does not extract, chunk, embed, summarise or store
paper text. It reads the pages, decides which registry subject each one
evidences, and returns page ranges. The text itself is dropped when the
function returns; only {subject_key, page_start, page_end} ever leaves here,
and only that reaches Neo4j.

Two rules carried over from normalization/pyq_normalizer.py:

  1. Nothing is invented. A page resolves to a subject only if a curated alias
     or a subject code appears in its header. Anything less leaves the bundle
     exactly as it was -- a semester-level record with an unresolved subject.
  2. Deterministic. Exact alias matching, no fuzzy scoring, no model call.

A bundle that cannot be split confidently must stay a bundle: a wrong subject
link is far worse than an unresolved one, because it hands a student the wrong
paper while looking authoritative.
"""
import re

# A question paper states its subject in the masthead. Matching the whole page
# would let a passing mention in a question body ("...compare with DBMS...")
# masquerade as the paper's own subject.
HEADER_CHARS = 700

# Lines that mark a genuine subject declaration. A hit here is worth far more
# than a bare alias floating in the header.
SUBJECT_LABEL_RE = re.compile(
    r"\b(?:subject|course|paper)\s*(?:name|title|code)?\s*[:\-]\s*(.{3,80})",
    re.I)

SUBJECT_CODE_RE = re.compile(
    r"(?<![A-Za-z0-9])\d{3}U\d{2}[A-Z]\d{3}(?![A-Za-z0-9])", re.I)

# Below this share of pages resolved, the split is not trustworthy and the
# whole bundle is left alone.
MIN_PAGE_COVERAGE = 0.30


def page_texts(pdf_bytes: bytes, max_pages: int = 400) -> list[str]:
    """Per-page text. Returns [] rather than raising on an unreadable PDF."""
    try:
        import io

        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(pdf_bytes))
        return [(page.extract_text() or "")
                for page in reader.pages[:max_pages]]
    except Exception:
        # A scanned or corrupt bundle simply cannot be split. That is a normal
        # outcome here, not an error worth failing the run over.
        return []


def _normalize(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[_\-.,()\[\]/&+:]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def subject_on_page(text: str, alias_index, code_index: dict | None = None):
    """The one subject this page evidences, or None.

    Ambiguity is resolved by refusing to answer: if the header names two
    different subjects with equal standing, the page is left unresolved.
    """
    header = text[:HEADER_CHARS]
    code_index = code_index or {}

    # A subject code is unambiguous -- prefer it over any name match.
    for match in SUBJECT_CODE_RE.finditer(header):
        subject = code_index.get(match.group(0).upper())
        if subject:
            return subject["subject_key"], f"code:{match.group(0).upper()}"

    # A "Subject: ..." line is the paper declaring its own subject.
    labelled = SUBJECT_LABEL_RE.search(header)
    if labelled:
        found = _match_aliases(_normalize(labelled.group(1)), alias_index)
        if len(found) == 1:
            key, alias = found[0]
            return key, f"label:{alias}"

    found = _match_aliases(_normalize(header), alias_index)
    if len(found) == 1:
        key, alias = found[0]
        return key, f"header:{alias}"
    return None


def _match_aliases(text: str, alias_index) -> list[tuple[str, str]]:
    """Distinct subjects whose alias appears as whole words, longest first."""
    found, seen, remaining = [], set(), text
    for alias, subject in alias_index:
        # One- and two-character aliases are far too weak inside prose; the
        # file-name parser can trust 'os' because a file name is all signal,
        # but a page of text is not.
        if len(alias) < 3:
            continue
        pattern = rf"\b{re.escape(alias)}\b"
        if not re.search(pattern, remaining):
            continue
        remaining = re.sub(pattern, " ", remaining)
        if subject["subject_key"] not in seen:
            seen.add(subject["subject_key"])
            found.append((subject["subject_key"], alias))
    return found


def extract_subject_pages(pdf_bytes: bytes, alias_index,
                          subjects: list[dict] | None = None) -> list[dict]:
    """Split a bundle into [{subject_key, page_start, page_end, evidence}].

    Returns [] whenever the split cannot be trusted -- an unreadable PDF, too
    few pages resolved, or only one subject found (which would mean the file
    was never really a bundle and the caller should not start guessing).
    Page numbers are 1-based and inclusive, matching what a reader sees.
    """
    pages = page_texts(pdf_bytes)
    if not pages:
        return []

    code_index = {s["code"].upper(): s
                  for s in (subjects or []) if s.get("code")}

    resolved = [subject_on_page(t, alias_index, code_index) for t in pages]
    hits = [r for r in resolved if r]
    if len(hits) < max(1, MIN_PAGE_COVERAGE * len(pages)):
        return []
    if len({key for key, _ in hits}) < 2:
        return []

    # A paper runs from its own title page to the page before the next one, so
    # unresolved pages inherit the subject of the last resolved page.
    spans, current = [], None
    for i, hit in enumerate(resolved):
        if hit and (current is None or hit[0] != current["subject_key"]):
            current = {"subject_key": hit[0], "page_start": i + 1,
                       "page_end": i + 1, "evidence": hit[1]}
            spans.append(current)
        elif current is not None:
            current["page_end"] = i + 1
    return spans

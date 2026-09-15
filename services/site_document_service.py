"""Question -> Neo4j -> official site documents, with clickable links.

Deterministic, like services/exam_document_service.py and
services/academic_document_service.py: regex intent classification, one filtered
Cypher read, a Markdown answer built in Python. No model call happens here, so the
official URLs cannot be altered on the way out. The caller may pass the result to a
single Ollama call for final phrasing.

Scoped by `source_type` throughout, so a placement question cannot return admission
documents and none of them can reach faculty, PYQ or provision data.
"""
from __future__ import annotations

import re

from graph import site_queries as q

DOCUMENTS_PAGE = "https://kjsce.somaiya.edu/en/documents/"


def md_link(text: str, url: str) -> str:
    """Angle-bracket the destination when it contains characters that would end a
    CommonMark link early. Several official URLs contain `(`, `)` or `&`."""
    return f"[{text}](<{url}>)" if any(c in url for c in "() <>") else f"[{text}]({url})"


INTENTS: list[tuple[str, list[str], list[str]]] = [
    ("ranking", ["ranking_report"],
     [r"\bnirf\b", r"\bariia\b", r"\brank(ing|ed)?\b", r"\bposition\b"]),
    ("accreditation", ["accreditation_document"],
     [r"\bnaac\b", r"\bnba\b", r"\baccredit", r"\biqac\b", r"\bgrade\b", r"\bugc\b"]),
    ("placement", ["placement_document"],
     [r"\bplacement", r"\brecruit", r"\bpackage\b", r"\bsalary\b", r"\binternship\b"]),
    ("admission", ["admission_document"],
     [r"\badmission", r"\bbrochure\b", r"\bprospectus\b", r"\beligibilit",
      r"\bcut\s*off\b", r"\bannexure\b", r"\bdsy\b", r"\blateral\b"]),
    ("alumni", ["alumni_document"],
     [r"\balumni\b", r"\balumnus\b", r"\bannual report\b", r"\bteam members\b"]),
    ("library", ["library_document"],
     [r"\blibrary\b", r"\bjournal", r"\bmagazine", r"\bbook bank\b"]),
    ("transcript", ["transcript_document"],
     [r"\btranscript", r"\bcertificate\b", r"\bmarksheet\b"]),
    ("mandatory_disclosure", ["mandatory_disclosure"],
     [r"\bmandatory disclosure\b", r"\bdisclosure\b"]),
]

ALL_TYPES = [t for _n, types, _p in INTENTS for t in types]

HEADINGS = {
    "ranking": "Ranking reports (NIRF / ARIIA)",
    "accreditation": "Accreditation documents",
    "placement": "Placement and internship documents",
    "admission": "Admission documents",
    "alumni": "Alumni documents",
    "library": "Library documents",
    "transcript": "Transcript documents",
    "mandatory_disclosure": "Mandatory disclosure",
    "all": "Official site documents",
}


def classify(question: str) -> dict:
    text = re.sub(r"\s+", " ", (question or "").lower()).strip()
    intents = [name for name, _types, pats in INTENTS
               if any(re.search(p, text) for p in pats)]
    year = None
    m = re.search(r"\b(20\d{2})\b", text)
    if m:
        year = int(m.group(1))
    return {"intents": intents or ["all"], "year": year}


def retrieve(question: str) -> dict:
    f = classify(question)
    blocks = []
    if "all" in f["intents"]:
        blocks.append(("all", q.find(ALL_TYPES, year=f["year"])))
    else:
        for name, types, _pats in INTENTS:
            if name in f["intents"]:
                blocks.append((name, q.find(types, year=f["year"])))
    return {"filters": f, "blocks": blocks}


def build_answer(result: dict) -> str:
    f = result["filters"]
    out, found = [], False
    for name, docs in result["blocks"]:
        if not docs:
            scope = f" for {f['year']}" if f.get("year") else ""
            out.append(f"**{HEADINGS.get(name, name)}** — nothing{scope} is in the "
                       "KJ GPT knowledge base.")
            out.append("")
            continue
        found = True
        out.append(f"**{HEADINGS.get(name, name)}** ({len(docs)}):\n")
        for d in docs:
            out.append("- " + md_link(d["title"] or d["doc_id"], d["source_url"]))
            bits = []
            if d.get("report_year"):
                bits.append(f"Year {d['report_year']}")
            if d.get("ranking_category"):
                bits.append(d["ranking_category"])
            if d.get("pages"):
                bits.append(f"{d['pages']} pages")
            if d.get("extraction_method"):
                bits.append(d["extraction_method"])
            if bits:
                out.append(f"  {' · '.join(bits)}")
        out.append("")
    if found:
        out.append("Source: " + md_link("KJSCE official documents page", DOCUMENTS_PAGE))
    return "\n".join(out).strip()


def answer_site_document_question(question: str, debug: bool = False) -> dict:
    result = retrieve(question)
    docs = [d for _n, ds in result["blocks"] for d in ds]
    payload = {
        "answer": build_answer(result),
        "documents": [{"doc_id": d["doc_id"], "title": d["title"],
                       "url": d["source_url"], "source_type": d["source_type"]}
                      for d in docs],
        "found": bool(docs),
    }
    if debug:
        payload["debug"] = {"filters": result["filters"],
                            "blocks": {n: [d["doc_id"] for d in ds]
                                       for n, ds in result["blocks"]}}
    return payload

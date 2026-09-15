"""Deciding what the crawl found that the graph does not already have.

This is the guard that keeps a site-wide crawl from doubling the knowledge base.
The graph already holds 42 documents gathered by hand; the crawl re-finds most of
them, often under a different URL. Every candidate therefore runs a dedup ladder
before anything is written, and the first rung that matches wins:

    1  exact source_url            already the document's own URL
    2  alternate_source_url        already recorded as a second URL for it
    3  canonical URL               same URL modulo escaping, params and case
    4  sha256                      same bytes under a different name
    5  title + page count + size   probably the same document -- FLAG, never merge
    6  nothing matched             genuinely new

Rung 4 is the one that earns its keep. The AEC 2026-27 calendar is published as both
`…_2026_27.pdf` and `…_2026-27.pdf`, and the 8 Point and Strategic plans appear under
both `/About/` and `/documents/`. No amount of URL normalisation catches those -- only
the bytes do. Rung 5 deliberately refuses to decide: a wrong auto-merge silently
destroys a distinct document, which is worse than asking.

Read-only. Nothing in this module writes to the graph.
"""
from __future__ import annotations

import re

from graph.neo4j_driver import run_query

EXISTING_DOCUMENTS = """
MATCH (d:PolicyDocument)
RETURN d.doc_id AS doc_id, d.source_url AS source_url,
       d.alternate_source_url AS alternate_source_url, d.sha256 AS sha256,
       d.title AS title, d.pages AS pages, d.file_size_bytes AS file_size_bytes,
       d.source_type AS source_type
"""

EXISTING_ENTITY_URLS = """
MATCH (n) WHERE (n:Form OR n:Portal) AND n.url IS NOT NULL
RETURN labels(n)[0] AS label, n.entity_key AS entity_key, n.name AS name, n.url AS url
"""


class Decision:
    REUSE = "REUSE"                  # already in the graph; record the alternate URL
    NEW = "NEW"                      # genuinely new, safe to create
    REFERENCE_ONLY = "REFERENCE_ONLY"  # non-KJ host: link kept outside the graph
    SKIPPED_PII = "SKIPPED_PII"
    REVIEW = "REVIEW"                # a human decides; never auto-ingested


def _norm_title(title: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


class GraphIndex:
    """One snapshot of what the graph already knows, folded into lookup tables.

    Loaded once per run rather than queried per candidate -- the whole corpus is a
    few hundred rows, so a single read is cheaper and gives every candidate a
    consistent view.
    """

    def __init__(self) -> None:
        self.by_url: dict[str, dict] = {}
        self.by_canonical: dict[str, dict] = {}
        self.by_sha: dict[str, dict] = {}
        self.by_title: dict[str, list[dict]] = {}
        self.documents: list[dict] = []
        self.entity_urls: dict[str, dict] = {}

    def load(self, canonicalise) -> "GraphIndex":
        self.documents = run_query(EXISTING_DOCUMENTS)
        for row in self.documents:
            for key in ("source_url", "alternate_source_url"):
                url = row.get(key)
                if url:
                    self.by_url[url] = row
                    canon = canonicalise(url)
                    if canon:
                        self.by_canonical[canon] = row
            if row.get("sha256"):
                self.by_sha[row["sha256"]] = row
            self.by_title.setdefault(_norm_title(row.get("title")), []).append(row)

        for row in run_query(EXISTING_ENTITY_URLS):
            if row.get("url"):
                self.entity_urls[row["url"]] = row
                canon = canonicalise(row["url"])
                if canon:
                    self.entity_urls.setdefault(canon, row)
        return self

    # ------------------------------------------------------------------ ladder
    def match(self, *, raw_url: str, canonical: str, sha256: str | None,
              title: str | None, pages: int | None,
              size: int | None) -> tuple[str, dict | None, str]:
        """Run the ladder. Returns (rung, matched_row, evidence)."""
        if raw_url and raw_url in self.by_url:
            return "exact_url", self.by_url[raw_url], f"source_url == {raw_url}"

        if canonical and canonical in self.by_canonical:
            row = self.by_canonical[canonical]
            return "canonical_url", row, f"canonical URL matches {row['doc_id']}"

        if canonical and canonical in self.entity_urls:
            row = self.entity_urls[canonical]
            return ("entity_url", None,
                    f"already a :{row['label']} entity ({row.get('entity_key')})")

        if sha256 and sha256 in self.by_sha:
            row = self.by_sha[sha256]
            return "sha256", row, (f"identical bytes to {row['doc_id']} "
                                   f"(sha256 {sha256[:16]}…)")

        if title:
            for row in self.by_title.get(_norm_title(title), []):
                same_pages = pages and row.get("pages") and pages == row["pages"]
                near_size = (size and row.get("file_size_bytes")
                             and abs(size - row["file_size_bytes"]) <= max(
                                 1024, int(0.01 * size)))
                if same_pages or near_size:
                    return ("title_size", row,
                            f"same title and {'page count' if same_pages else 'size'} "
                            f"as {row['doc_id']} — needs review, not auto-merged")

        return "none", None, ""


def load_index(canonicalise) -> GraphIndex:
    return GraphIndex().load(canonicalise)

# Full KJSCE Site Crawl → Neo4j Knowledge Base

## Context

KJ GPT's Neo4j graph currently holds knowledge from four hand-run ingestions: the KJSIT policy
handbook, the faculty directory, PYQ question papers, and — built most recently — the Examination
and Academics document sections of <https://kjsce.somaiya.edu/en/documents/>. Each was discovered
and curated manually, one section at a time.

That approach does not scale to the rest of the site, and it has no memory: there is no record of
what has been seen, no way to resume, and no automatic check for whether a newly found document is
something the graph already has. Meanwhile the documents page is only **40 of the site's ~450
addressable resources** — the other sections (admission, placement, library, exam cell, internship
cell, programmes, PhD) have never been crawled at all.

This project builds a **resumable, deduplicating crawler** that discovers everything in scope on the
official site, reads the documents properly, reconciles each find against the live graph, and ingests
only what is genuinely new — reusing the existing `:PolicyDocument` architecture rather than adding a
parallel one.

**Outcome:** one manifest-driven pipeline that can be stopped and resumed, a measurable coverage
percentage, and a graph that answers student questions with exact official links and intact
provenance.

---

## Verified findings (measured this session, not assumed)

### The site

| Fact | Value |
|---|---|
| `robots.txt` | Permissive — 3 `Disallow` entries only (2 faculty query-param URLs, 1 alumni subdomain) |
| `sitemap.xml` | **366 URLs**, all on `kjsce.somaiya.edu`, **0 PDFs**, 149 carrying query params |
| Distinct top-level sections | 51 |
| Documents page | Content is **AJAX**, not static HTML |

Largest sitemap clusters: `/view-publication` 94, `/programme` 91, `/admission` 44,
`/view-announcement` 35, `/view-member` 12, `/placement` 9, `/library` 8, `/view-events` 7,
`/blog` 6, `/notices` 5, plus ~40 singleton pages (`/documents`, `/exam-cell`, `/internship-cell`,
`/phd`, `/mandatory-disclosure`, `/ranking`, `/transcripts`, `/academic-programme`, …).

### The documents page

Content loads via `POST https://kjsce.somaiya.edu/arigel_general/get_document` with
`page_no / department_id / category_id / institute_id=16 / dept_name / cat_name / lang`.
15 (department, category) pairs exist across 4 departments; **3 return the literal body
`No Data Found.`**. Enumerating all 15 yields **40 unique resources — 39 PDFs + 1 external page**.

**29 of those 40 are already in Neo4j** (Examination 16, Academics 11, Internship forms 2).
The **11 remaining are all Administrative**: the 8 Point Development Plan and KJSSE Strategic Plan
*republished under a different path*, 7 NIRF reports (2020–2024), and 2 ARIIA reports.

### Documents live on other hosts

PDFs are **not** in the sitemap. Sampling 8 key pages found 80 unique document links spread across
five hosts: `kjsce-files.somaiya.edu`, `kjsse-files.somaiya.edu`, `kjsce-old.somaiya.edu`,
`svu-files.somaiya.edu`, `svv-files.somaiya.edu.in`, `svu-admissions.somaiya.edu`.
`/en/phd/` alone links **77** documents, 61 of them on `svu-files`.

### URL normalisation traps (measured)

Of the 366 sitemap URLs, **149 carry query parameters**. Param keys: `type` (105), `id` (93),
`vthmstablink` (40), `cat_id` (4).

1. **`&amp;` in `<loc>` is correct XML escaping.** The raw sitemap contains
   `…/view-publication/966?type=research&amp;id=160120`. A crawler that does not XML-unescape will
   request a parameter literally named `amp;id` and get the wrong page. (My own first pass counted
   `amp;id` as a distinct key — proof the trap bites.)
2. **Query params here are semantically significant — do not strip them.** Stripping all params
   would collapse 149 URLs onto 106 paths, merging 8 distinct `/admission/btech?vthmstablink=…`
   tab pages into one and 10 `/admission/direct-second-year` pages into one. Rule: **keep params,
   normalise their order and casing, and let the content hash collapse genuine duplicates** rather
   than guessing which params matter.

### Two hazards found by inspection

1. **Student PII.** Linked PDFs include *"Provisionally Admitted Students List July 2026 COMP"* and
   *"Provisionally Selected Phd candidates IT"* — named individuals.
2. **The host drops connections under burst.** A modest sequence of requests triggered
   `ConnectionResetError(54)`. Conservative pacing and backoff are mandatory, not optional.

---

## Approved scope

| Decision | Choice |
|---|---|
| **Pages** | All 366 sitemap URLs — core student-facing **+** `/programme` (91) **+** `/view-publication` (94) **+** announcements/events/blogs |
| **Hosts** | Download and deep-read only `kjsce-files`, `kjsse-files`, `kjsce-old`. `svu-files`, `svv-files`, `svu-admissions` and any other host: **record title + exact URL as a reference, never download or extract** |
| **Student PII** | **Excluded entirely.** Detect merit/admitted/selected/candidate lists, record in the manifest as skipped-with-reason + URL, never download or store names or roll numbers |
| **NIRF / ARIIA** | **Document-level only** — title, year, category, issuing body, exact URL. Read only enough to confirm identity and reporting year; do not mine statistical tables |

**Institution scope:** KJSCE / KJSSE / KJSIT are one engineering college throughout. `institution`
stays `KJSIT` for graph consistency (the existing validator requires it); the name printed on each
source goes in `institution_name_in_source`. No institution branches.

**Backend scope:** Neo4j only. No embeddings, no vector search, no second retrieval system.

---

## Existing code to reuse

Discovery confirmed the repo already has most of the building blocks. The plan reuses, not rebuilds:

| Need | Reuse |
|---|---|
| Neo4j access | `graph/neo4j_driver.py` — `run_query`, `verify_connection`, `close_driver` |
| Idempotent upsert | The `_created` sentinel `MERGE … ON CREATE SET … SET x += $props` pattern in every `graph/*_ingestion.py` |
| Document ingestion template | `graph/exam_ingestion.py`, `graph/academics_ingestion.py` — closest models |
| Same doc, second URL | `graph/academics_ingestion.record_alternate_url()` |
| Nested data → properties | `flatten_events()` / `_flatten()` / `flatten_numbers()` + read-side `events_of` / `branches_of` re-pair helpers |
| Safe relationship writes | `graph/policy_ingestion.link()` — allow-listed rel types and labels |
| Don't clobber good data | `graph/policy_ingestion.strip_empty()`, `graph/faculty_ingestion.merge_properties()` |
| HTTP retry/backoff | `scraper/somaiya_faculty.py::_request()` (delay 1.0s, timeout 30, 4 retries, base 2.0, retries 5xx/429) |
| Cycle-safe enumeration | `drive/client.py::walk_folder()` `visited` set; `_execute()` jittered backoff |
| PDF download + scanned detection | `scripts/discover_policies.py::fetch_document()`, `scanned_pages()`, `_image_areas()` (nested Form XObjects) |
| Deterministic retrieval + Markdown | `services/exam_document_service.py`, `services/academic_document_service.py`, `md_link()` |
| Staged pipeline convention | discover → normalize → validate → ingest, JSON artifact per stage, `--dry-run` everywhere |
| Test style | Standalone `main()` scripts, hand-rolled PASS/FAIL, non-zero exit; `scripts/test_policy_queries.py` is the integrity model |

### Parents already exist for almost every content family

The graph holds **38 non-superseded `:Policy` nodes**. Each is a ready-made anchor, so new documents
hang off existing knowledge instead of needing invented parents — the same discipline the Examination
and Academics ingests already follow:

| Content family | Existing parent `policy_id` | Already carries |
|---|---|---|
| Examination documents | `exam_structure_current` | 16 docs |
| Academic documents | `teaching_learning_process` | 13 docs |
| Placement / internship | `training_placement_policy` | 21 provisions, 0 docs |
| Library | `library_policy`, `library_services` | 36 provisions |
| Admission | `admission_process` | 8 provisions |
| Programmes / departments | `programs_and_departments` | 6 provisions |
| Research, publications | `research_development_policy` | 9 provisions |
| NIRF / ARIIA / accreditation | `qms_iqac` | 4 provisions |
| Student bodies, cells, clubs | `student_welfare_policies` | 17 provisions |
| Scholarships | `scholarship_freeship` | 9 provisions |
| Fees | `fee_collection` | 7 provisions |
| Hostel | `hostel_facility` | 5 provisions |

### Gaps this project must fill

No URL canonicaliser anywhere. sha256 is computed at discovery but **never used for dedup**. No disk
cache with skip-if-exists. No PDF link-annotation (`/Annots` `/URI`) extraction. Two inconsistent
scraper implementations. No checkpoint/resume — today's model is full-recompute.

---

---

## Coverage math — how "95%" becomes a real number

The denominator cannot be guessed up front, because discovery itself grows it. So the crawl is
**two-phase**, and coverage is only meaningful after phase A finishes.

**Phase A — Discovery (cheap, no downloads).** Walk the sitemap, the AJAX document endpoint, and
every in-scope page's links until the frontier is empty. Nothing is downloaded; only URLs, titles and
link context are recorded. When the frontier empties, the manifest is **frozen** and its in-scope row
count becomes the denominator. Phase A is re-runnable and will re-open the frontier if the site adds
pages.

**Phase B — Processing.** Fetch, hash, read and ingest each in-scope resource, moving it through the
status machine. Coverage is computed from the frozen manifest:

```
coverage = (DONE + SKIPPED_BY_POLICY + REFERENCE_ONLY) / TOTAL_IN_SCOPE
```

All three numerator terms are *terminal, intentional* states, so a PII document that we deliberately
refused counts as processed — it is not an incomplete item. `FAILED` and `PENDING` never count.

**Reported alongside the percentage, always:** the exact counts per status, and the full list of
everything not yet `DONE` with its reason. Stopping at ~95% is allowed only against this frozen
denominator, never against an estimate.

### Estimated size (order of magnitude only — the manifest is the truth)

| | |
|---|---|
| Sitemap pages | **366** (exact) |
| Documents-page resources | **40** (exact; 29 already ingested, 11 pending) |
| Document links per page | **10.0** unique across 8 sampled pages (skewed — `/phd` alone had 77) |
| Projected unique documents site-wide | **~250–650**, depending on what share of pages carry documents |
| Of those, on KJ hosts needing deep read | roughly a third; the rest are reference-only by the host rule |
| Projected total requests | ~400 pages + ~200 document downloads, at ~1.5 s spacing ≈ **45–60 min** of wall-clock fetching, spread across resumable runs |

---

## Pipeline architecture

Five stages, extending the repo's existing **discover → normalize → validate → ingest** convention
with a crawl stage in front. Every stage reads the previous stage's JSON artifact and never re-fetches
the network; every script takes `--dry-run` and `--resume`.

```
  0  crawl/fetcher.py        shared HTTP layer  (rate limit, backoff, disk cache, conditional GET)
        │
  1  scripts/crawl_site.py --discover      sitemap + AJAX + link-following → FROZEN manifest
        │                                   data/site_crawl_manifest.json
  2  scripts/crawl_site.py --process       download, hash, extract → data/site_resources.json
        │                                   (PDF text, page count, scanned pages, embedded links)
  3  scripts/reconcile_site.py             match every resource against the LIVE graph → decisions
        │                                   data/site_reconciliation.json
  4  scripts/validate_site.py              block on any unsafe/incomplete decision
        │                                   data/site_validation_report.json
  5  scripts/ingest_site_documents.py      idempotent MERGE → data/site_ingestion_report.json
```

Stages 1–2 touch the network. Stages 3–5 are offline and re-runnable, exactly like the existing PYQ
and policy pipelines.

### Stage 0 — the shared fetch layer (`crawl/fetcher.py`, new)

Consolidates the two inconsistent scrapers. Built on `scraper/somaiya_faculty.py::_request()`'s
proven shape, with the gaps closed:

- `canonical_url(url, base=None) -> str` — the missing canonicaliser: XML/HTML-unescape (fixes the
  `&amp;id` trap), resolve relative against base, lowercase scheme+host, strip fragments, drop
  session-ish params (`utm_*`, `PHPSESSID`), **keep meaningful params**, sort param order, normalise
  percent-encoding. Returns the key used everywhere downstream.
- `get(url, *, kind)` — rate-limited (≥1.5 s spacing, single-threaded), 4 retries, exponential
  backoff **with jitter** (borrowed from `drive/client.py::_execute`), 30 s timeout, retries 5xx/429
  **and `ConnectionResetError`** (observed on this host).
- Disk cache at `data/crawl_cache/<sha256(canonical_url)>` storing body + `ETag`/`Last-Modified`.
  Re-runs send `If-None-Match`/`If-Modified-Since` and skip unchanged content — closing the
  "re-downloads every run" gap in `discover_policies.py`.
- `sha256` of every fetched body, recorded and **actually used** for dedup (today it is computed and
  discarded).

### Stage 1 — discovery

Three sources merge into one manifest, deduplicated by `canonical_url`:

1. **Sitemap** — 366 URLs, XML-unescaped.
2. **AJAX document endpoint** — enumerate all `get_document(dept, deptId, cat, catId)` pairs parsed
   from the documents page; records the `No Data Found.` sections as an observed fact, as the
   Academics ingest already does.
3. **Link-following** — from each in-scope page: HTML `<a href>` plus, for PDFs, **embedded
   `/Annots` `/URI` link annotations** (the technique that found 41 per-branch Drive folders behind
   the Syllabus index; there is no existing helper for this, so it becomes
   `crawl/pdf_links.py::embedded_links(reader)`).

Loop avoidance: a `visited` set keyed on `canonical_url`, the `walk_folder` pattern. Depth cap 4 from
any seed. Frontier empties → manifest frozen.

### Stage 2 — processing and extraction

Per resource, by class:

| Class | Treatment |
|---|---|
| HTML page on `kjsce.somaiya.edu` | Fetch, extract main content + links. Page text is **not** stored in Neo4j — it feeds entity extraction only |
| PDF on `kjsce-files` / `kjsse-files` / `kjsce-old` | Download, `%PDF` check, sha256, full `pypdf` text per page, `scanned_pages()` detection |
| PDF flagged scanned | Extract page rasters from DCTDecode streams and **read visually**, the method used for the 19 image-only Academics/Examination pages. Not OCR-by-default — only where text extraction found nothing |
| Document on any non-KJ host | **Reference only** — title + exact URL recorded, never downloaded |
| Detected PII list | **Skipped** — URL + reason recorded, never fetched |
| NIRF / ARIIA | Downloaded, first pages read only to confirm identity + reporting year. Tables not mined |

**PII detection** is deterministic, on filename/anchor text, and errs toward skipping:
`/(provisionally\s+)?(admitted|selected|merit|shortlist|candidate)s?\b.*\b(list|students?|candidates?)/i`
plus `roll\s*no`, `seat\s*no`. Any hit → `SKIPPED_PII`. Ambiguous hits are skipped, not read.

### The manifest — one row per resource, the single source of truth

`data/site_crawl_manifest.json`, written atomically (temp file + rename) after every N rows so a
crash never corrupts it:

```jsonc
{
  "canonical_url": "…",          // primary key
  "raw_urls": ["…"],             // every spelling seen, incl. the &amp; form
  "discovered_from": ["…"],      // parent page(s) — provenance of the link itself
  "anchor_text": "…",
  "kind": "page | pdf | external",
  "host_class": "kj | other_somaiya | external",
  "in_scope": true,
  "scope_reason": "sitemap | documents_ajax | followed_link | out_of_scope:<why>",

  "status": "PENDING",           // status machine below
  "http_status": 200,
  "etag": "…", "last_modified": "…",
  "sha256": "…", "bytes": 123456, "cache_path": "data/crawl_cache/…",
  "pages": 12, "scanned_pages": [1,2], "text_chars": 29920,
  "embedded_links": ["…"],

  "dedup": {"decision": "NEW|REUSE|REFERENCE_ONLY|SKIPPED_PII|REVIEW",
            "matched_doc_id": "…", "matched_on": "sha256|url|canonical_url|title+size",
            "evidence": "…"},

  "neo4j": {"doc_id": "…", "source_type": "…", "parent_policy_id": "…",
            "ingested_at": "…", "ingest_batch_id": "…"},

  "attempts": 0, "last_error": null,
  "first_seen_at": "…", "last_touched_at": "…"
}
```

**Status machine** — terminal states in bold:

```
PENDING ──► FETCHING ──► FETCHED ──► EXTRACTED ──► RECONCILED ──► **DONE**
   │            │                                       └────────► **REUSED**
   │            └─► FAILED ─(attempts<4)─► PENDING
   │                   └─(attempts=4)──► **FAILED_PERMANENT**
   ├─► **REFERENCE_ONLY**      (non-KJ host — recording the link IS the processing)
   ├─► **SKIPPED_PII**         (student list — refused by policy)
   └─► **OUT_OF_SCOPE**        (excluded by the scope rules; kept for auditability)
```

`--resume` is simply: load the manifest, select everything not in a terminal state, continue. Because
every write is an idempotent `MERGE` keyed on `doc_id`, re-processing a row that was already ingested
is harmless. A row that fails 4 times becomes `FAILED_PERMANENT` and is listed in the report rather
than retried forever.

### Stage 3 — reconciliation against the live graph (the heart of this project)

Before anything is created, each resource runs a **dedup ladder**, stopping at the first hit:

| # | Signal | Action |
|---|---|---|
| 1 | Exact `source_url` already on a `:PolicyDocument` / `:Form` / `:Portal` | **REUSE** — nothing to do |
| 2 | `alternate_source_url` already matches | **REUSE** |
| 3 | `canonical_url` matches an existing canonicalised URL | **REUSE**, record alternate URL |
| 4 | **sha256 matches an existing document** | **REUSE + `record_alternate_url()`** — the exact case already proven: the AEC 2026-27 PDF published under both `…2026-27.pdf` and `…2026_27.pdf`, and the two plan PDFs republished under `/documents/` vs `/About/` |
| 5 | Normalised title + page count + byte size match | **FLAG for review** — likely duplicate, never auto-merged |
| 6 | Nothing matches | **NEW** — assign `doc_id`, choose `source_type` + parent |

Entity reconciliation follows the same discipline: before creating any `:Department`, `:Programme`,
`:Subject`, `:Committee`, `:Form`, `:Portal` or `:FacultyMember`, look it up by its existing
`entity_key` / `subject_key` / `faculty_id` constraint. **Never create a second node for an existing
entity under a different spelling** — `faculty_ingestion.merge_properties()` is the model for
enriching rather than overwriting.

The output is an explicit decision per resource (`REUSE` / `NEW` / `REFERENCE_ONLY` / `SKIPPED_PII`
/ `REVIEW`), each with its evidence. **A human-reviewable file, not an automatic write.**

### Stage 4–5 — validate, then ingest

Validation blocks the ingest (the `blocking` convention from `scripts/validate_policies.py`) on:
duplicate `doc_id`/`source_url` in the input, any resource with decision `REVIEW`, any node carrying
forbidden content keys (`pdf`, `content`, `raw`, `bytes`, `text`), any `institution` other than
`KJSIT`, any parent `policy_id` not already in the graph.

Ingestion reuses `graph/exam_ingestion.py` / `graph/academics_ingestion.py` verbatim in shape:
`MERGE` on `doc_id`, `SET d += $props`, `MERGE (parent)-[:REFERENCES {relation:…}]->(d)`, refuse to
run if the parent is missing.

---

## Neo4j mapping

**No new labels. No new relationship types. No new constraints.** Everything lands on
`:PolicyDocument` discriminated by `source_type`, hung off an existing `:Policy` parent by
`REFERENCES` — the pattern already carrying 29 documents.

New `source_type` values (the only additions, all following existing naming):

`admission_document`, `placement_document`, `internship_document`, `library_document`,
`ranking_report` (NIRF/ARIIA), `mandatory_disclosure`, `programme_page`, `notice`,
`reference_link` (non-KJ-host, link-only).

Facts extracted from documents attach as **properties and parallel arrays** on the document
(`flatten_*` + read-side re-pair), not as new node types — the decision already taken for 138 calendar
events, 41 branch links, 8 strategic goals and 43 plan parameters.

**A page or document only becomes a `:PolicyProvision` if it states an actual rule** — a requirement,
eligibility condition, penalty or deadline — and then it carries `source_page` + `source_section`
provenance, matching the existing three-tier `PolicyDocument → Policy → PolicyProvision` model.
Calendars, notices, reports and brochures do **not** become provisions. This is the same line drawn
in the Examination and Academics ingests, and it is what keeps dated schedules from being answered as
standing policy.

### Temporal handling

Every document keeps `academic_year`, `document_date` and `document_status` (as printed —
`proposed` / `tentative` / `revised` / `issued`). Newer documents **never overwrite** older ones;
where a source explicitly supersedes another, the existing `SUPERSEDED_BY` edge is used and the
superseded node is retained and excluded from default retrieval — the mechanism already protecting
the 2018 handbook edition. Historical calendars stay queryable but are never presented as current.

---

## Files

**New**
| Path | Purpose |
|---|---|
| `crawl/__init__.py`, `crawl/fetcher.py` | Shared HTTP: canonicalisation, rate limit, jittered backoff, disk cache, conditional GET, sha256 |
| `crawl/manifest.py` | Manifest load/save/update, status machine, coverage computation |
| `crawl/pdf_links.py` | `/Annots` `/URI` extraction + rect→anchor-text mapping |
| `crawl/classify.py` | Deterministic resource classification, PII detection, `source_type`/parent routing |
| `scripts/crawl_site.py` | Stages 1–2, `--discover` / `--process` / `--resume` / `--limit` / `--dry-run` |
| `scripts/reconcile_site.py` | Stage 3 — the dedup ladder against the live graph |
| `scripts/validate_site.py` | Stage 4 |
| `scripts/ingest_site_documents.py` | Stage 5 |
| `graph/site_ingestion.py` | Upsert + parent linking, modelled on `exam_ingestion.py` |
| `graph/site_queries.py` | Scoped reads for the new `source_type` values |
| `services/site_document_service.py` | Deterministic retrieval + `md_link`, modelled on the exam/academics services |
| `scripts/test_site_crawl.py` | Graph-integrity assertions, modelled on `test_policy_queries.py` |
| `data/site_crawl_manifest.json` + 4 stage artifacts | Checkpoint + reports |
| `FULL_KJSCE_SITE_CRAWL_PLAN.md`, `SITE_CRAWL_REPORT.md` | Plan + final report |

**Modified (minimally)**
- `main.py` — add `/site/ask` + debug, mirroring `/exam/documents/ask`.
- `requirements.txt` — no new dependencies expected; `requests`, `bs4`, `lxml`, `pypdf` already cover it.

**Not touched:** every existing `graph/`, `services/`, `scripts/` and `data/` file for faculty, PYQ,
policy, exam and academics.

---

## Verification

**Data-safety assertions** (`scripts/test_site_crawl.py`, run before and after every ingest):
baseline counts must hold — FacultyMember 613, PYQ 164, PYQFile 162, Subject 81, PolicyProvision 432,
Policy 41, and the 42 pre-existing `:PolicyDocument` nodes must still have 42 distinct `doc_id` and
42 distinct `source_url`. Plus: no duplicate `doc_id`/`source_url` graph-wide; no orphan documents;
no node carrying `pdf`/`content`/`raw`/`bytes`/`text`; every document has a `source_url`; every new
document reaches an existing `:Policy` parent; no `institution` other than `KJSIT`.

**Retrieval validation** — the 10 single-intent questions plus the multi-intent example, asserting
*which* documents come back, not just that something does:

- attendance requirement · internship requirement · 2026-27 academic calendar · syllabus location ·
  examination calendar · who teaches Computer Engineering · official internship form · examination
  forms · strategic plan · software for students
- multi-intent: *"Show me the 2026-27 academic calendar and the syllabus"* → evidence for **both**,
  separately headed

Precision assertions: a syllabus question returns no calendars; a strategic-plan question returns no
unrelated PDFs; every emitted URL exists in the graph (the 109-link, 0-invented check already used
for Academics); links containing parentheses render via `md_link`'s angle-bracket form.

**Rollback.** Every new node carries `ingest_batch_id` and `first_seen_at`, so one run is reversible
with a single scoped `MATCH (d:PolicyDocument {ingest_batch_id: $id}) DETACH DELETE d`. Reused nodes
are never deleted — only the `alternate_source_url` property they gained would be removed. A dry-run
and a full baseline count snapshot precede every real write.

---

## What changes after approval

1. Nothing in Neo4j on day one — stages 1–2 only build the manifest and read documents.
2. The frozen manifest arrives first, with the real denominator and the full in-scope list, for your
   review before any write.
3. Ingestion happens in reviewable batches per content family (admission, placement, library, …),
   each with a dry-run, a reconciliation file you can inspect, and a before/after count check.
4. You can stop at any batch boundary; `--resume` continues from the checkpoint.

## Open risks

- **Denominator grows during discovery.** Mitigated by freezing the manifest before computing
  coverage, and re-opening it explicitly if the site changes.
- **`/programme` (91) and `/view-publication` (94) are page-shaped, not document-shaped.** They may
  yield few PDFs and much prose. If prose does not state rules, it produces no provisions by design —
  which may make those 185 pages low-yield. Worth a checkpoint after the first 10.
- **Connection resets under load** — already observed. Single-threaded, ≥1.5 s spacing, jittered
  backoff; the crawl is resumable precisely because interruptions are expected.
- **Scanned PDFs need visual reads**, which are slow and cannot be batched. Detected in stage 2 and
  queued so they do not block the text-extractable majority.

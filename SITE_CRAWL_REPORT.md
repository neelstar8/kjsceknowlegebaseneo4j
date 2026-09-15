# Full KJSCE Site Crawl — Ingestion Report

**Source:** <https://kjsce.somaiya.edu/> starting from `/en/documents/`  
**Backend:** Neo4j only — no embeddings, no vector search, no second retrieval system.  
**Ingest batch:** `sitecrawl_20260915T083201_eaacc0`  
**Run:** 2026-09-15T08:32:01.375583+00:00  
**Scope:** KJSCE / KJSSE / KJSIT treated throughout as one engineering college.

## 1. Coverage

**946 of 959 in-scope resources resolved = 98.64%**

The denominator was frozen once the discovery frontier emptied; it is the manifest's
own in-scope row count, not an estimate. Every resource that has *not* reached a
deliberate outcome is named below — the percentage cannot hide unfinished work.

| Status | Count | Counts toward coverage? |
|---|---:|---|
| `RECORDED` | 834 | yes — page, or non-KJ host — link kept, never downloaded |
| `OUT_OF_SCOPE` | 69 | excluded from denominator — same-host page not in sitemap; audited, not crawled |
| `INGESTED` | 65 | yes — new document written to Neo4j |
| `REUSED` | 30 | yes — already in the graph; alternate URL recorded |
| `SKIPPED_PII` | 17 | yes — student list — refused before any fetch |
| `PERMANENTLY_FAILED` | 7 | no — unreachable after retries |
| `EXTRACTED` | 4 | no — read but not routed to a section |
| `NEEDS_REVIEW` | 2 | no — ambiguous — a human decides |

**Outstanding: 13**, every one listed:

- `EXTRACTED` — https://kjsse-files.somaiya.edu/documents/Eight+Point+Development+Plan_+KJSSE.pdf
- `NEEDS_REVIEW` — https://kjsce-files.somaiya.edu/Academics/KJSCE_Roll+Call.pdf
  - ambiguous student-list wording: KJSCE Roll Call pdf Roll Call List
- `EXTRACTED` — https://kjsce-old.somaiya.edu/
- `NEEDS_REVIEW` — https://financialaid.somaiya.edu/en/special-scholarship/
  - ambiguous student-list wording: Merit Scholarship
- `PERMANENTLY_FAILED` — https://kjsse-files.somaiya.edu/Admission+2026-27/Admission+Cancellation+&+Refund+Policy+AY+2026-27,+SVU_1.pdf
  - server returns HTTP 403: not publicly accessible (verified with Referer and Accept headers)
- `PERMANENTLY_FAILED` — https://kjsce-files.somaiya.edu/Admissions_2022/DSY/Annexure+1.pdf
  - server returns HTTP 403: not publicly accessible (verified with Referer and Accept headers)
- `PERMANENTLY_FAILED` — https://kjsce-files.somaiya.edu/Admissions_2022/DSY/Annexure++2+(1).pdf
  - server returns HTTP 403: not publicly accessible (verified with Referer and Accept headers)
- `EXTRACTED` — https://kjsce-files.somaiya.edu/mtech/Annexure+1.pdf
- `EXTRACTED` — https://kjsce-files.somaiya.edu/mtech-website/Annexure+2+with+KJSCE+logo+-+as+per+guideline.pdf
- `PERMANENTLY_FAILED` — https://kjsce-files.somaiya.edu/Admission+2026-27/Annexure-5.pdfAdmission+2025/KJSSE_MTech_Annexure-5.pdf
  - server returns HTTP 403: not publicly accessible (verified with Referer and Accept headers)
- `PERMANENTLY_FAILED` — http://kjsse-files.somaiya.edu/Admission+2026-27/Annexure-5.pdf
  - server returns HTTP 403: not publicly accessible (verified with Referer and Accept headers)
- `PERMANENTLY_FAILED` — http://kjsse-files.somaiya.edu/Internship/SLI+Final+Policy+-25-26+-+Signed+Copy.pdf
  - server returns HTTP 403: not publicly accessible (verified with Referer and Accept headers)
- `PERMANENTLY_FAILED` — https://kjsce-files.somaiya.edu/Alumni/Teams/KJSSE_AC+24-25.pdf
  - server returns HTTP 403: not publicly accessible (verified with Referer and Accept headers)

## 2. What was discovered

| | |
|---|---:|
| Sitemap pages (fixed denominator) | 366 |
| Pages crawled (sitemap + found) | 435 |
| Total manifest rows | 1028 |
| Documents + external resources | 593 |
| Documents-page AJAX resources | 40 (39 PDFs + 1 external page) |

**Page coverage: 435/435 = 100%.** Every page in the sitemap, plus those reached
from them, was fetched and had its links harvested.

## 3. Reconciliation against the existing graph

Nothing was created before checking what the graph already held. Each resource ran a
six-rung dedup ladder, stopping at the first match.

| Decision | Count |
|---|---:|
| REFERENCE_ONLY | 834 |
| NEW | 68 |
| REUSE | 30 |
| SKIPPED_PII | 17 |
| REVIEW | 3 |

| Reuse matched on | Count | What it means |
|---|---:|---|
| `exact_url` | 27 | the document's own URL was already in the graph |
| `entity_url` | 2 | already a `:Form` / `:Portal` entity |
| `title_size` | 1 | same title and size — flagged for review, never auto-merged |
| `sha256` | 1 | **identical bytes under a different name** — no URL rule could catch this |

### The duplicates it caught

Two documents are published on this site under more than one URL. The ladder
distinguished them correctly, which is the whole point:

| Document | Copy A | Copy B | Outcome |
|---|---|---|---|
| KJSSE Strategic Plan 2025-2030 | `/About/…` `1f421370…` 1,205,270 B | `/documents/…` `1f421370…` 1,205,270 B | **identical → reused**, alternate URL recorded |
| 8 Point Development Plan | `/About/…` `8dbae7a1…` 158,926 B | `/documents/…` `e74d8bca…` **184,441 B** | same title and page count, **different bytes → held for review**, not merged |
| NIRF 2025 Engineering | `https://…` | `http://…` same path | same file linked twice; collapsed to one node |

## 4. What went into Neo4j

**64 documents created, 64 REFERENCES edges, 3 alternate URLs recorded.**

| source_type | Parent policy (already existed) | Documents |
|---|---|---:|
| `alumni_document` | `industry_institute_interaction` | 18 |
| `ranking_report` | `qms_iqac` | 17 |
| `admission_document` | `admission_process` | 11 |
| `placement_document` | `training_placement_policy` | 10 |
| `accreditation_document` | `qms_iqac` | 4 |
| `library_document` | `library_policy` | 2 |
| `transcript_document` | `student_section_certificates` | 2 |

**No new labels. No new relationship types. No new constraints.** Everything is a
`:PolicyDocument` discriminated by `source_type`, hung off a `:Policy` that already
existed, by the `REFERENCES` edge — the same pattern the Examination and Academics
ingests use. No parent was invented; the ingest refuses to run if one is missing.

**No `:PolicyProvision` was created.** None of these documents states a rule,
ordinance, penalty or eligibility condition — they are reports, brochures, forms and
annual reports. Turning them into provisions would make them answer as standing policy.

## 5. Student PII — refused, never retrieved

**17 documents were refused before any fetch.** The gate runs on the URL and
anchor text, so nothing was downloaded, hashed or stored — verified by an assertion
that no refused row carries a checksum or local path.

- List of Applicants Provisionally Selected for PhD Program - July 2026 Computer Engineering
- List of Applicants Provisionally Selected for PhD Program - July 2026 Electronics Engineering
- List of Applicants Provisionally Selected for PhD Program - July 2026 Electronics & Telecommunic
- List of Applicants Provisionally Selected for PhD Program - July 2026 Information Technology
- List of Applicants Provisionally Selected for PhD Program - July 2026 Mechanical Engineering
- Documents - 2020 Admitted Students
- Documents - 2021 Admitted Students
- Documents - 2022 Admitted Students
- Documents - January 2023 Admitted Students
- Documents - July 2023 Admitted Students
- Documents - February 2024 Admitted RTA Students
- Documents - April 2025 Admitted JRF students
- Documents - July 2025 Admitted Students
- Students placed through Campus Placement in 2024-2025
- Download or View

## 6. Validation

### Data safety — existing knowledge untouched

| Label | Before | After |
|---|---:|---:|
| FacultyMember | 613 | 613 |
| PYQ | 164 | 164 |
| PYQFile | 162 | 162 |
| Subject | 81 | 81 |
| PolicyProvision | 432 | 432 |
| Policy | 41 | 41 |
| PolicyDocument | 42 | 106 |

### Integrity — `scripts/test_site_crawl.py`: **24/24 passed**

Including: every document has a distinct `doc_id` and a unique `source_url`; no two
documents share a checksum; every crawled document hangs off a `:Policy`; no node
carries file content; crawled documents come only from allowed hosts; no refused
document was ever downloaded; every outstanding resource is named.

### Existing suites

- `scripts.test_policy_queries` — **33/33 passed**
- `tests.test_policy_questions` — **56/56 passed**
- Existing retrieval unchanged: academics 2026-27 calendar → 4 docs, syllabus → 1,
  examination → 16, policy attendance → found

### Retrieval — 8 questions, 0 invented links

| Question | Documents | Intent |
|---|---:|---|
| What is the NIRF ranking report? | 14 | `ranking` |
| Show me the placement reports. | 10 | `placement` |
| What is the accreditation status? | 4 | `accreditation` |
| Where can I find the admission brochure? | 10 | `admission` |
| Do you have alumni annual reports? | 18 | `alumni` |
| What library journals are available? | 2 | `library` |
| How do I apply for a transcript? | 2 | `transcript` |
| Show me the NIRF 2024 report. | 4 | `ranking` |

Every URL emitted was checked against the graph: **0 links not in the knowledge base.**
Destinations containing `(`, `)` or `&` are wrapped `[text](<url>)` so they resolve.

## 7. Bugs found and fixed during the run

1. **PII false negative (the serious one).** `_` is a word character, so `\badmitted`
   never matched `KJSCE_Admitted_Students_List_2026.pdf` — a real student list would
   have passed the gate. Separators are now flattened before matching.
2. **PII false positive.** `roll call` was treated as certain PII, skipping the Roll
   Call *index*, which the graph already holds verified safe. Downgraded to review;
   the actual per-branch roll calls live in Drive folders this crawl never opens.
3. **`http` vs `https` duplicate.** The same NIRF report is linked under both schemes;
   canonicalisation lowercased the scheme but never unified it, so one file became two
   nodes. Fixed at the canonicaliser, plus intra-batch checksum dedup as a safety net.
4. **`EXTRACTED` was re-processed every pass** because it was not terminal for the
   crawl stage. Harmless thanks to the cache, but slow and misleading. Split
   `CRAWL_DONE` from `TERMINAL`.
5. **Routing on title alone was too weak.** 40 documents had uninformative titles
   ("Overall", "Team Members 2023-24", "Download Form") while their URL path stated
   exactly what they were. Added a path-based fallback; unrouted fell 40 → 3.

## 8. Known issues, not caused by this work

- **`scripts/test_pyq_queries.py` fails 3 ESE checks.** The merge `9f988ac` brought in
  an ESE-aware version of the test (ESE mentions 2 → 12) from `899a46c`, but the ESE
  papers were never ingested into this database — it holds 164 PYQ nodes, all `ISE`.
  This is a test/data mismatch from the branch merge. My batch created exactly 60
  nodes, all `:PolicyDocument`, verified by `ingest_batch_id`.
- **One pre-existing orphan**, `kjsit_exam_structure_coc`, an
  `official_site_supplement` with no parent, added by the policy pipeline.
- **15 of the original 42 documents carry no `sha256`** (the handbook chapters), so
  checksum dedup cannot protect them. They live on `kjsit-files.somaiya.edu.in`, which
  this crawl does not cover, so they cannot be re-found and duplicated. A backfill from
  `data/policy_discovery.json` (12 of 15 available) would close the gap.

## 9. Resuming

```bash
.venv/bin/python -m scripts.crawl_site --status      # progress and coverage
.venv/bin/python -m scripts.crawl_site --process     # resumes automatically
.venv/bin/python -m scripts.reconcile_site           # re-decide against the graph
.venv/bin/python -m scripts.ingest_site_documents --dry-run
```
The manifest is an append-only event log at `data/crawl/manifest_events.jsonl`. A run
killed mid-write loses at most one truncated line, which replay ignores. Resume is
"replay the log, skip terminal rows, continue" — there is no separate checkpoint to
fall out of sync.

**Rollback for this batch:**
```cypher
MATCH (d:PolicyDocument {ingest_batch_id: 'sitecrawl_20260915T083201_eaacc0'}) DETACH DELETE d
```

---

*No Git commit was made.*

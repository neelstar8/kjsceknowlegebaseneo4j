# KJSCE Site Page-Content Ingestion Report

**Source:** official KJSCE site pages already discovered by the previous crawl  
**Ingest batch:** `pages_20260915T122102_9bffc0`  
**Run:** 2026-09-15T12:21:02.666138+00:00  
**Resumed from:** the existing crawl manifest — **no page was re-fetched**; all 366 were already in the local cache.  
**Scope:** KJSCE / KJSSE / KJSIT treated as one engineering college throughout.

## 1–8. Page accounting

| | |
|---|---:|
| Page resources discovered (previous crawl) | 366 |
| Already processed for links | 366 |
| **Remaining for content ingestion** | **366** |
| — pages with real content | 301 |
| — **distinct content bodies** | **245** |
| — collapsed as identical content (client-side tab URLs) | 56 |
| — soft 404 (HTTP 200, error body) | 12 |
| — thin / navigation only | 53 |
| **Newly ingested as knowledge** | **158** |
| Faculty-owned, deliberately skipped | 84 |
| Not substantive after cleaning | 3 |
| Unrouted | 0 |
| Reused instead of created | 0 |
| PII refused (unchanged from previous run) | 17 |

**Why 366 pages became 158 nodes.** 56 are the same page served under different
`?vthmstablink=` URLs — proven identical by content hash, so they are recorded as
alternate URLs on one node rather than 56 nodes. 84 belong to the faculty pipeline.
65 are error pages or pure navigation. What remains is the knowledge.

## 9–12. Entities and relationships

| | Before | After | Change |
|---|---:|---:|---|
| PolicyDocument | 106 | 264 | +158 |
| FacultyMember | 613 | 613 | unchanged |
| PolicyProvision | 432 | 432 | unchanged |
| Policy | 41 | 41 | unchanged |
| PYQ | 164 | 164 | unchanged |
| PYQFile | 162 | 162 | unchanged |
| Subject | 81 | 81 | unchanged |

**No new labels and no new relationship types were created.** Pages are
`:PolicyDocument {source_type:'webpage'}` hung off an existing `:Policy` by the
existing `REFERENCES` edge — the same shape the examination, academics and document
layers already use.

| Parent policy (already existed) | Pages attached |
|---|---:|
| `programs_and_departments` | 81 |
| `governance_statutory_bodies` | 40 |
| `student_welfare_policies` | 8 |
| `library_policy` | 7 |
| `training_placement_policy` | 7 |
| `admission_process` | 4 |
| `about_institute` | 3 |
| `exam_structure_current` | 3 |
| `research_development_policy` | 3 |
| `student_section_certificates` | 1 |
| `teaching_learning_process` | 1 |

**Relationships created:** 158 `REFERENCES` edges, all to parents that already existed.  
**Entities reused:** every parent policy; no `:Policy`, `:Programme`, `:Department`, `:Subject` or `:FacultyMember` node was created or modified.

## 13–14. Documents and alternate URLs

- Pages carrying alternate URLs: **16**, covering **52** further URLs.
- No document was re-downloaded: links already ingested by the document layer were
  matched by URL and reused.
- Content-fingerprint duplicates within the graph: **0**

## 15–16. What carried knowledge, and what did not

**Pages with meaningful new knowledge, by kind:**

| Kind | Pages |
|---|---:|
| `programme_page` | 81 |
| `notice_page` | 40 |
| `student_life_page` | 8 |
| `library_page` | 7 |
| `placement_page` | 7 |
| `admission_page` | 4 |
| `institution_page` | 3 |
| `research_page` | 3 |
| `examination_page` | 3 |
| `academic_page` | 1 |
| `certificate_page` | 1 |

Extracted across them: **405 fact statements** and **108 tables** (admission rounds, fee structures, important dates), each kept with the heading it appeared under so it can be cited.

**Pages deliberately not ingested:**

- **84 faculty-owned pages** (`/view-member`, `/view-publication`). 11 of 12 member ids on those pages are already in `FacultyMember` (613 records). Ingesting them would create a second, disagreeing copy of faculty data, so they are recorded and skipped.
- **12 soft 404s** — pages returning an error body under HTTP 200, mostly `/programme/certificate-*`, i.e. broken links on the site itself.
- **53 thin pages** — navigation shells with under 200 characters of content once menus, the contact modal and the footer are removed.

## 17. Current vs historical

Every page records the academic years it actually names, and retrieval filters on them. A 2024-25 page can never answer as 2026-27.

| Academic year | Documents |
|---|---:|
| 2026-27 | 39 |
| 2025-26 | 2 |
| 2024-25 | 4 |
| 2023-24 | 2 |
| 2022-23 | 2 |
| 2021-22 | 4 |
| 2020-21 | 1 |
| 2019-20 | 2 |
| 2015-16 | 1 |

**A phantom-year bug was caught and fixed here.** The first pass stored `2026-24` and
`2026-25` on the M.Tech admission page, because two unrelated numbers sitting next to
each other in a fee table matched the academic-year pattern. Years are now required to
be consecutive, and a validation check asserts no impossible year exists. A phantom
year is worse than a missing one: it makes a page look authoritative for a year it
never mentions.

## 18. Retrieval validation — `scripts/test_page_retrieval.py`: **22/22 passed**

| Question shape | Result |
|---|---|
| Rule wording — "What is the attendance requirement?" | 8 sourced provisions |
| Casual — "How much attendance do I need?" | same 8 provisions |
| Terse — "minimum attendance?" | same 8 provisions |
| Page content — "admission eligibility for B.Tech" | 6 pages, admission first |
| Abbreviation — "DSY admission" | same top 3 as "direct second year admission" |
| Abbreviation — "FY BTech fees" | same top 3 as "first year B.Tech fees" |
| Year-qualified — "2026-27 admission process" | 3 pages, **all** naming 2026-27 |
| Ambiguous year — "2026 admission" | resolved against years actually held |
| Old year — "2019 admission" | no year substitution |
| Multi-intent — calendar + syllabus | both source types returned |
| Link integrity | every URL verified present in the graph |

Routing is the point: rule questions answer from the handbook provisions, page
questions from page knowledge, document questions from the document layer. "attendance requirement" correctly returns **zero** page hits — the rule lives in the provisions, and a page search that answered it would be guessing.

## 19. LLM answer validation — one Ollama call per question

| Question | Evidence from | Correct | Invented links |
|---|---|---|---|
| What is the attendance requirement? | policy provisions | 75% stated | 0 |
| Eligibility criteria for B.Tech admission? | page knowledge | HSC + subject criteria | 0 |
| What is the 2026-27 B.Tech admission process? | page knowledge | year-qualified correctly | 0 |

The pipeline remains **one** Ollama call: query → deterministic Neo4j retrieval → single call. No second model call was added.

## 20–22. Outstanding, and the checkpoint

**Coverage: 946/959 = 98.64%** against the frozen denominator.

| Status | Count |
|---|---:|
| `RECORDED` | 624 |
| `INGESTED` | 275 |
| `OUT_OF_SCOPE` | 69 |
| `REUSED` | 30 |
| `SKIPPED_PII` | 17 |
| `PERMANENTLY_FAILED` | 7 |
| `EXTRACTED` | 4 |
| `NEEDS_REVIEW` | 2 |

**Outstanding: 13**, unchanged by this run and each named:

- `EXTRACTED` — https://kjsse-files.somaiya.edu/documents/Eight+Point+Development+Plan_+KJSSE.pdf
- `NEEDS_REVIEW` — https://kjsce-files.somaiya.edu/Academics/KJSCE_Roll+Call.pdf
- `EXTRACTED` — https://kjsce-old.somaiya.edu/
- `NEEDS_REVIEW` — https://financialaid.somaiya.edu/en/special-scholarship/
- `PERMANENTLY_FAILED` — https://kjsse-files.somaiya.edu/Admission+2026-27/Admission+Cancellation+&+Refund+Policy+AY+2026-27,+SVU_1.pdf
- `PERMANENTLY_FAILED` — https://kjsce-files.somaiya.edu/Admissions_2022/DSY/Annexure+1.pdf
- `PERMANENTLY_FAILED` — https://kjsce-files.somaiya.edu/Admissions_2022/DSY/Annexure++2+(1).pdf
- `EXTRACTED` — https://kjsce-files.somaiya.edu/mtech/Annexure+1.pdf
- `EXTRACTED` — https://kjsce-files.somaiya.edu/mtech-website/Annexure+2+with+KJSCE+logo+-+as+per+guideline.pdf
- `PERMANENTLY_FAILED` — https://kjsce-files.somaiya.edu/Admission+2026-27/Annexure-5.pdfAdmission+2025/KJSSE_MTech_Annexure-5.pdf
- `PERMANENTLY_FAILED` — http://kjsse-files.somaiya.edu/Admission+2026-27/Annexure-5.pdf
- `PERMANENTLY_FAILED` — http://kjsse-files.somaiya.edu/Internship/SLI+Final+Policy+-25-26+-+Signed+Copy.pdf
- `PERMANENTLY_FAILED` — https://kjsce-files.somaiya.edu/Alumni/Teams/KJSSE_AC+24-25.pdf

**Resume:**

```bash
.venv/bin/python -m scripts.crawl_site --status            # coverage
.venv/bin/python -m scripts.ingest_page_content --dry-run  # re-plan pages
.venv/bin/python -m scripts.ingest_page_content            # refreshes its own pages
```
The manifest is the append-only event log at `data/crawl/manifest_events.jsonl`. Page rows carry `ingested_by='page_content'`, so a re-run **refreshes** them rather than skipping — which is how the phantom-year fix reached pages already written.

**Rollback:**
```cypher
MATCH (d:PolicyDocument {ingest_batch_id: 'pages_20260915T122102_9bffc0'}) DETACH DELETE d
```

---

*No Git commit was made.*

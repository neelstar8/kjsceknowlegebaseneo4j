# Examination Document Ingestion Report

**Source:** <https://kjsce.somaiya.edu/en/documents/> — Examination › Examination Calendar  
**Backend:** Neo4j only. No embeddings, no vector search, no RAG chunks, no new retrieval architecture.  
**Run:** 2026-09-14T13:14:09.544533+00:00

## 1–2. Discovery count vs expected

| | |
|---|---|
| Expected (stated in the task) | 16 |
| Discovered on the official page | **16** |
| Downloaded successfully | **16 / 16** |
| Fully analysed from actual PDF content | **16 / 16** |
| Ingested into Neo4j | **16 / 16** |
| Distinct `doc_id` in Neo4j | 16 |
| Distinct `source_url` in Neo4j | 16 |

The count was **verified, not assumed**. The Examination section's links are not in the page's 
static HTML — they are loaded by a `get_document()` AJAX call. Calling that endpoint directly
(`POST https://kjsce.somaiya.edu/arigel_general/get_document`, `department_id=10&category_id=94`)
returned exactly 16 unique PDF links. Requesting page 2 returned the same set, so there is no
pagination hiding further documents.

## 3. Every PDF

### 1. Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27

- **URL:** <https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** proposed
- **Academic year:** 2026-27 · **terms:** First/Odd, Second/Even
- **Programme:** B.Tech, M.Tech · **level:** SY/TY/LY (B.Tech) and FY/SY (M.Tech)
- **Document date:** 2026-09-01
- **Issuing authority:** Dr. Suresh Ukarande, Director, KJSSE; Dr. J H Nirmal, Associate Dean Academics Programmes
- **Institution as printed on the PDF:** K J Somaiya School of Engineering
- **Pages:** 3 · **text layer:** scanned_images_read_visually · **sha256:** `39eefe465aa3a9c5…`
- **What it actually contains:** Title page plus two calendar tables. Page 2 is headed 'Proposed' (First Term/Odd Semester, SY/TY/LY B.Tech); page 3 is headed 'Proposed/Tentative' (Second Term/Even Semester, SY/TY/LY B.Tech and FY/SY M.Tech). The document does not present these dates as final.
- **Extracted examination events:** 30
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_aec_2026_27_sytyly_btech_fysy_mtech"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

### 2. Academic and Examination Calendar 2022-23- SY, TY, LY and FY

- **URL:** <https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_KJSCE__Academic+and+Examination+Calendar+AEC-2022-23.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** issued
- **Academic year:** 2022-23 · **terms:** First/Odd, Second/Even
- **Programme:** B.Tech, M.Tech · **level:** Separate templates for SY B.Tech, SY M.Tech, TY B.Tech, LY B.Tech (KJSCE 2018) and FY B.Tech
- **Institution as printed on the PDF:** KJSCE / Somaiya Vidyavihar University
- **Pages:** 5 · **text layer:** text · **sha256:** `7ec9f72b363ad8bb…`
- **What it actually contains:** One PDF containing FIVE separate programme calendars on five pages: SY B.Tech (SVU 2020), SY M.Tech (SVU 2020), TY B.Tech (SVU 2020), LY B.Tech (KJSCE 2018) and FY B.Tech (SVU 2020). The SY M.Tech even-term rows are blank in the source. Issued on the Somaiya Vidyavihar University AEC template.
- **Extracted examination events:** 17
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_aec_2022_23_all_years"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

### 3. Academic and Examination (AEC) Calendar 2023-24

- **URL:** <https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_+Uniform+AEC_SVU+KJSCE++2023-24.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** tentative
- **Academic year:** 2023-24 · **terms:** First/Odd, Second/Even
- **Programme:** B.Tech, M.Tech · **level:** FY/SY/TY/LY, all programmes (UG and PG)
- **Document date:** 2023-07-12
- **Institution as printed on the PDF:** KJSCE / Somaiya Vidyavihar University
- **Pages:** 2 · **text layer:** text · **sha256:** `eab464ec7e7abea9…`
- **What it actually contains:** Headed 'Tentative Uniform/Common Academic and Examination Calendar (AEC)'. A single common calendar covering all years and programmes, giving separate FY and SY/TY/LY dates in the same rows.
- **Extracted examination events:** 17
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_aec_2023_24_uniform"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

### 4. Odd Term/Semester UG and PG FY -SVU 2020-21

- **URL:** <https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar_FY+BTECH+and+MTECH.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** tentative
- **Academic year:** 2020-21 · **terms:** First/Odd
- **Programme:** B.Tech, M.Tech · **level:** FY B.Tech Semester I and FY M.Tech Semester I
- **Document date:** 2020-11-11
- **Issuing authority:** Examination In-Charge, KJSCE
- **Institution as printed on the PDF:** K J Somaiya College of Engineering (Constituent College of Somaiya Vidyavihar University)
- **Pages:** 2 · **text layer:** text · **sha256:** `3ac0cc5f58d83774…`
- **What it actually contains:** Covers TWO programmes in one PDF: FY B.Tech Sem I and FY M.Tech Sem I. Unlike the other calendars this one is a COVID-period schedule that also records examination MODE (online, Google Docs with video proctoring) and question-paper pattern per assessment. Schedules are given as weeks/months, not exact dates, and the column is headed 'Tentative Schedule'.
- **Extracted examination events:** 10
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_cal_2020_21_odd_fy_btech_mtech"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

### 5. TY-LY  Academic and Examination Calendar 2021-22

- **URL:** <https://kjsce-files.somaiya.edu/Exam/Calendar/TY-LY+_+Academic+and+Examination+Calendar+2021-22.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** issued
- **Academic year:** 2021-22 · **terms:** Odd, Even
- **Programme:** B.Tech · **level:** TY/LY B.Tech
- **Document date:** 2021-05-12
- **Issuing authority:** Principal
- **Institution as printed on the PDF:** K J Somaiya College of Engineering (Autonomous College Affiliated to University of Mumbai)
- **Pages:** 1 · **text layer:** text · **sha256:** `751e562abcf0c9a2…`
- **What it actually contains:** Single-page TY/LY B.Tech calendar. This is the only document in the set whose letterhead still describes the college as affiliated to the University of Mumbai.
- **Extracted examination events:** 8
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_aec_2021_22_ty_ly_btech"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

### 6. SY M.TECH (SVU-2020)_ Academic and Examination Calendar 21-22

- **URL:** <https://kjsce-files.somaiya.edu/Exam/Calendar/SY+M.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** issued
- **Academic year:** 2021-22 · **terms:** Odd, Even
- **Programme:** M.Tech · **level:** SY M.Tech (SVU 2020)
- **Document date:** 2021-05-10
- **Issuing authority:** Principal
- **Institution as printed on the PDF:** K J Somaiya College of Engineering (A constituent college of Somaiya Vidyavihar University)
- **Pages:** 1 · **text layer:** text · **sha256:** `9c87add7a9eabab9…`
- **What it actually contains:** Single-page SY M.Tech calendar. The Even Term rows for ISE, dispersal and conduct of examinations are left blank ('--') in the source and are therefore not recorded.
- **Extracted examination events:** 5
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_aec_2021_22_sy_mtech"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

### 7. SY B.TECH (SVU-2020)_ Academic and Examination Calendar 21-22

- **URL:** <https://kjsce-files.somaiya.edu/Exam/Calendar/SY+B.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** issued
- **Academic year:** 2021-22 · **terms:** Odd, Even
- **Programme:** B.Tech · **level:** SY B.Tech (SVU 2020)
- **Document date:** 2021-05-10
- **Issuing authority:** Principal
- **Institution as printed on the PDF:** K J Somaiya College of Engineering (A constituent college of Somaiya Vidyavihar University)
- **Pages:** 1 · **text layer:** text · **sha256:** `3f8bbc65111e3c94…`
- **What it actually contains:** Single-page SY B.Tech calendar; the only 2021-22 single-year calendar that also names a Supplementary Exam window.
- **Extracted examination events:** 9
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_aec_2021_22_sy_btech"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

### 8. Odd Term/Semester UG and PG SY/TY/LY 2020-21

- **URL:** <https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar+-+UG-SY-TY+and+PG+SEM+III.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** issued
- **Academic year:** 2020-21 · **terms:** First/Odd
- **Programme:** B.Tech, M.Tech · **level:** SY/TY/LY B.Tech Semesters III, V and VII and M.Tech Sem III (regular); plus FY/SY/TY/LY B.Tech Semesters I-VI and M.Tech Sem I (backlog/KT)
- **Document date:** 2020-11-20
- **Issuing authority:** Examination In-Charge, KJSCE
- **Institution as printed on the PDF:** K J Somaiya College of Engineering (Constituent College of Somaiya Vidyavihar University)
- **Pages:** 1 · **text layer:** text · **sha256:** `704f351d21ae5fe3…`
- **What it actually contains:** Covers TWO distinct examination sets in one PDF: regular examinations for SY/TY/LY B.Tech Sem III/V/VII and M.Tech Sem III, and separately the BACKLOG (KT) examinations for FY/SY/TY/LY B.Tech Sem I-VI and M.Tech Sem I. A COVID-period schedule that records mode and paper pattern; several practical exams were deferred depending on the pandemic situation.
- **Extracted examination events:** 7
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_cal_2020_21_odd_sy_ty_ly"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

### 9. FY B.TECH -Academic and Examination calendar

- **URL:** <https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+B.TECH_+Academic+and+Examination+Calendar+20-21.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** issued
- **Academic year:** 2020-21 · **terms:** Odd, Even
- **Programme:** B.Tech · **level:** FY B.Tech, for students admitted to college till October 2020
- **Document date:** 2020-12-04
- **Issuing authority:** Principal
- **Institution as printed on the PDF:** K J Somaiya College of Engineering / Somaiya Vidyavihar University
- **Pages:** 1 · **text layer:** text · **sha256:** `9ee0bfb89a846551…`
- **What it actually contains:** FY B.Tech calendar explicitly scoped in its own title to students admitted to the college till October 2020.
- **Extracted examination events:** 8
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_aec_2020_21_fy_btech"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

### 10. FY.M.TECH -Academic and Examination calendar

- **URL:** <https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+M.TECH_+Academic+and+Examination+Calendar+20-21.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** issued
- **Academic year:** 2020-21 · **terms:** Odd, Even
- **Programme:** M.Tech · **level:** FY M.Tech
- **Document date:** 2020-12-04
- **Issuing authority:** Principal
- **Institution as printed on the PDF:** K J Somaiya College of Engineering / Somaiya Vidyavihar University
- **Pages:** 1 · **text layer:** text · **sha256:** `1bf8a8cce4275fd8…`
- **What it actually contains:** FY M.Tech calendar for 2020-21; its odd term starts in November 2020, later than the FY B.Tech odd term of the same year.
- **Extracted examination events:** 8
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_aec_2020_21_fy_mtech"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

### 11. SY/TY/LY B. Tech/M. Tech Academic and Examination Calendar

- **URL:** <https://kjsce-files.somaiya.edu/Exam/Calendar/SY-LY+_+Academic+and+Examination+Calendar_Modified.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** issued
- **Academic year:** 2020-21 · **terms:** Odd, Even
- **Programme:** B.Tech, M.Tech · **level:** SY/TY/LY B.Tech and M.Tech
- **Document date:** 2020-12-04
- **Issuing authority:** Principal
- **Institution as printed on the PDF:** K J Somaiya College of Engineering (A constituent college of Somaiya Vidyavihar University)
- **Pages:** 1 · **text layer:** text · **sha256:** `0e451ecf59e9c64f…`
- **What it actually contains:** Single combined calendar for SY/TY/LY across both B.Tech and M.Tech for 2020-21.
- **Extracted examination events:** 8
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_aec_2020_21_sy_ty_ly"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

### 12. Academic and Examination Calendar for FY FY M TECH 2021-22

- **URL:** <https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+M.TECH_+Academic+and+Examination+Calendar+21-22.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** issued
- **Academic year:** 2021-22 · **terms:** Odd, Even
- **Programme:** M.Tech · **level:** FY M.Tech
- **Document date:** 2021-10-01
- **Issuing authority:** Principal
- **Institution as printed on the PDF:** K J Somaiya College of Engineering / Somaiya Vidyavihar University
- **Pages:** 1 · **text layer:** text · **sha256:** `675d620922a97055…`
- **What it actually contains:** FY M.Tech 2021-22 calendar. Its dates are identical to the FY B.Tech 2021-22 calendar issued the same day.
- **Extracted examination events:** 8
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_aec_2021_22_fy_mtech"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

### 13. Academic and Examination Calendar for FY B TECH  2021-22

- **URL:** <https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+B.TECH_+Academic+and+Examination+Calendar.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** issued
- **Academic year:** 2021-22 · **terms:** Odd, Even
- **Programme:** B.Tech · **level:** FY B.Tech
- **Document date:** 2021-10-01
- **Issuing authority:** Principal
- **Institution as printed on the PDF:** K J Somaiya College of Engineering / Somaiya Vidyavihar University
- **Pages:** 1 · **text layer:** text · **sha256:** `bffbbdc378afb5c1…`
- **What it actually contains:** FY B.Tech 2021-22 calendar, issued 1 October 2021. Its even-term dates were later revised - see the 'regular students' revision and the separate calendar for students newly admitted from November 2021, both dated 14 January 2022.
- **Extracted examination events:** 8
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_aec_2021_22_fy_btech"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

### 14. Revised Academic and Examination Calendar for DSY SEM III

- **URL:** <https://kjsce-files.somaiya.edu/Exam/SVU_Notices/Revised+Academic+and+Examination+Calendar+DSY+2021-22.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** revised
- **Academic year:** 2021-22 · **terms:** Even
- **Programme:** B.Tech · **level:** SY B.Tech (SVU 2020) Sem IV, and Sem III for Direct Second Year (DSY) admitted students only
- **Document date:** 2022-01-02
- **Issuing authority:** Asst Controller of Exam; Controller of Examinations
- **Institution as printed on the PDF:** K J Somaiya College of Engineering (A constituent college of Somaiya Vidyavihar University)
- **Pages:** 1 · **text layer:** scanned_images_read_visually · **sha256:** `309935209c73947d…`
- **What it actually contains:** The listed title names only the DSY SEM III revision, but the PDF actually contains TWO tables: the SY B.Tech (SVU 2020) SEM IV Even Term calendar, and a separate 'Revised Academic and examination Calendar for SEM III - DSY' that applies only to Direct Second Year admitted students.
- **Extracted examination events:** 10
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_aec_2021_22_sy_btech_sem4_dsy_sem3"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

### 15. Academic and Examination Calendar for Newly admitted  Batch ( 26 Nov and onwards)  to FY BTECH -2021

- **URL:** <https://kjsce-files.somaiya.edu/Exam/SVU_Notices/FOR+NEW+BATCH__21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** issued
- **Academic year:** 2021-22 · **terms:** Odd, Even
- **Programme:** B.Tech · **level:** FY B.Tech, newly admitted students only (admitted November 2021 and onwards)
- **Document date:** 2022-01-14
- **Issuing authority:** ACE/EIC; Principal
- **Institution as printed on the PDF:** K J Somaiya College of Engineering / Somaiya Vidyavihar University
- **Pages:** 1 · **text layer:** text · **sha256:** `ce9e476c76ffcbad…`
- **What it actually contains:** Applies ONLY to FY B.Tech students admitted in November 2021 and onwards - a later intake than the regular 2021-22 FY batch, so its odd term begins in January 2022. The document carries the note: 'In unforeseen circumstances the schedule is subject to change'.
- **Extracted examination events:** 9
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_aec_2021_22_fy_btech_new_batch"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

### 16. Revised Academic Calendar for FY BTECH Even Semester 2021-22

- **URL:** <https://kjsce-files.somaiya.edu/Exam/SVU_Notices/REVISED+EVEN+SEM_21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf>
- **Document type:** academic_and_examination_calendar · **status as printed:** revised
- **Academic year:** 2021-22 · **terms:** Odd, Even
- **Programme:** B.Tech · **level:** FY B.Tech, regular students (2021-22)
- **Document date:** 2022-01-14
- **Issuing authority:** ACE/EIC; Principal
- **Institution as printed on the PDF:** K J Somaiya College of Engineering / Somaiya Vidyavihar University
- **Pages:** 1 · **text layer:** text · **sha256:** `022a49582d294522…`
- **What it actually contains:** Revises the even-semester schedule for REGULAR FY B.Tech students of 2021-22. The odd term dates repeat the 1 October 2021 calendar; the even term section is explicitly headed 'Revised Schedule for Even Semester (2021-22)'. Carries the note: 'In unforeseen circumstances the schedule is subject to change'. Its supplementary window ends 12 September 2022, whereas the newly-admitted batch calendar issued the same day ends 16 September 2022.
- **Extracted examination events:** 9
- **Neo4j node:** `(:PolicyDocument {doc_id: "exam_aec_2021_22_fy_btech_revised_even"})`
- **Relationship:** `(:Policy {policy_id:"exam_structure_current"})-[:REFERENCES]->` this node
- **Ingestion status:** ingested and linked ✅ (first run: updated)

## 4. Documents that contained meaningful data

All **16 of 16** carry real, extractable examination content — 
**171 examination events** in total, every one read from the 
PDF itself rather than inferred from a filename.

Several PDFs carry more than one calendar, which is modelled rather than flattened:

- **Academic and Examination Calendar 2022-23- SY, TY, LY and FY** — One PDF containing FIVE separate programme calendars on five pages: SY B.Tech (SVU 2020), SY M.Tech (SVU 2020), TY B.Tech (SVU 2020), LY B.Tech (KJSCE 2018) and FY B.Tech (SVU 2020). The SY M.Tech even-term rows are blank in the source. Issued on the Somaiya Vidyavihar University AEC template.
- **Odd Term/Semester UG and PG FY -SVU 2020-21** — Covers TWO programmes in one PDF: FY B.Tech Sem I and FY M.Tech Sem I. Unlike the other calendars this one is a COVID-period schedule that also records examination MODE (online, Google Docs with video proctoring) and question-paper pattern per assessment. Schedules are given as weeks/months, not exact dates, and the column is headed 'Tentative Schedule'.
- **Odd Term/Semester UG and PG SY/TY/LY 2020-21** — Covers TWO distinct examination sets in one PDF: regular examinations for SY/TY/LY B.Tech Sem III/V/VII and M.Tech Sem III, and separately the BACKLOG (KT) examinations for FY/SY/TY/LY B.Tech Sem I-VI and M.Tech Sem I. A COVID-period schedule that records mode and paper pattern; several practical exams were deferred depending on the pandemic situation.
- **Revised Academic and Examination Calendar for DSY SEM III** — The listed title names only the DSY SEM III revision, but the PDF actually contains TWO tables: the SY B.Tech (SVU 2020) SEM IV Even Term calendar, and a separate 'Revised Academic and examination Calendar for SEM III - DSY' that applies only to Direct Second Year admitted students.

## 5. Documents / sections that were empty

**No PDF was empty.** One *section* was:

- **Examination > Examination Download Forms** (`department_id=10, category_id=30`) — The official endpoint returns the literal body 'No Data Found.' - the section publishes no documents at all. Recorded as an observed fact; no content invented.

This is recorded as an observed fact and surfaced in answers; nothing was invented to fill it.

## 6. Existing Examination Policy status

**Status: it already existed — Structure Decision A.** No placeholder policy node was invented.

Found in the graph before any change, and left completely untouched:

| policy_id | status | provisions |
|---|---|---|
| `exam_structure_current` | current | 32 |
| `examination_policy_cbcgs` | current_but_incomplete | 15 |
| `examination_policy_2018` | superseded | 15 |
| `exam_ordinances_2018` | superseded | 7 |

`exam_structure_current` (the current Examination policy, 32 provisions) is used as the parent 
the documents hang from. Its own provisions, text and relationships were not modified.

**No date from any calendar was turned into a PolicyProvision.** These 16 PDFs are schedules, 
not rules — none states an ordinance, eligibility condition or penalty. Verified: 
`0` provisions are SOURCED_FROM any examination document.

## 7. Neo4j structure used

```
(:Policy {policy_id: 'exam_structure_current'})   ← already existed, untouched
      │
      └─[:REFERENCES {relation: 'official_examination_document'}]─→
              (:PolicyDocument {source_type: 'examination_calendar'})   × 16
```

**No new labels. No new relationship types. No new constraints. No schema change.**

- `PolicyDocument` is the label the handbook pipeline already uses for a fetched PDF, and 
  `doc_id` was already unique-constrained — which is what makes the ingest idempotent.
- `source_type='examination_calendar'` is the discriminator, alongside the existing 
  `handbook_chapter`, `handbook_full_edition` and `official_site_supplement` values.
- `REFERENCES` (not `DOCUMENTED_IN`): in this graph `DOCUMENTED_IN` asserts a policy's *text 
  lives in* that PDF and carries the page range. A calendar does not contain the examination 
  policy, so the weaker, already-existing `REFERENCES` edge is the honest one.
- Events are stored as the parallel arrays `event_terms` / `event_names` / `event_schedules` 
  plus a searchable `events_text` — the same shape `flatten_numbers()` uses in the handbook 
  ingest, because Neo4j cannot hold a list of maps on a property.

## 8. Validation queries and results

| Check | Result |
|---|---|
| Exam documents present | **16** |
| REFERENCES edges from the Examination policy | **16** |
| Distinct doc_id (no duplicates) | **16** |
| Distinct source_url (no duplicates) | **16** |
| URLs on the official kjsce-files host | **16** |
| Examination Policy nodes (unchanged, not duplicated) | **4** |
| Provisions created from calendars (must be 0) | **0** |
| Node labels exam docs touch (must be Policy only) | **1** |
| FacultyMember (untouched) | **613** |
| PYQ (untouched) | **164** |
| Subject (untouched) | **81** |
| PolicyProvision (untouched) | **432** |

Byte-for-byte URL comparison between the official page and Neo4j: **exact match, 16/16**.

Existing suites after ingestion:

- `scripts.test_policy_queries` — **33/33 passed**
- `tests.test_policy_questions` — **56/56 passed**
- `tests.test_pyq_normalizer`, `tests.test_pyq_pdf_subjects` — **passed**

Idempotence: a second identical run reported `created: 0, updated: 16, REFERENCES merged: 16` 
and node counts did not move.

### Retrieval test — the seven required questions

All answered from Neo4j, deterministically, with every official URL rendered as a clickable 
Markdown link. None returned Attendance, Internship, Faculty, Admission, Placement or PYQ content.

| # | Question | Documents returned |
|---|---|---|
| 1 | What examination documents are available? | 16 |
| 2 | Show me the examination calendars. | 16 |
| 3 | Where can I find the examination download forms? | 16 + states the section is empty |
| 4 | What examination calendar is available for 2026-27? | 1 |
| 5 | Show me the academic and examination calendar for 2023-24. | 1 |
| 6 | What examination documents are available for B.Tech? | 13 |
| 7 | What are the examination dates mentioned in the 2026-27 calendar? | 1 + 30 dated events |

## 9. Ambiguities and missing information

Recorded rather than resolved by guessing:

- **The 2026-27 calendar is not final.** Page 2 is headed *Proposed*, page 3 *Proposed/Tentative*. 
  Stored as `document_status: proposed` so it is never presented as a settled schedule.
- **The 2023-24 calendar is headed *Tentative Uniform/Common*.** Stored as `tentative`.
- **SY M.Tech 2021-22** leaves its Even Term ISE, dispersal and examination rows blank (`--`) in 
  the source. Those rows are absent from the graph rather than filled in.
- **The 2022-23 PDF's FY B.Tech template has internally inconsistent dates** as printed 
  (ISE "5 December – 10 December 2023" sits before a dispersal of "21st January 2023"). 
  Transcribed exactly as printed; not silently corrected.
- **Two 2021-22 FY B.Tech calendars were issued on the same day (14 Jan 2022)** — one for regular 
  students, one for students admitted from November 2021 — with different supplementary windows 
  (12 vs 16 September 2022). Kept as two separate documents; not merged.
- **No calendar is assumed to apply to the current academic year.** Each document carries only 
  the academic year printed on it.
- **Some schedules are weeks/months, not dates** (the 2020-21 COVID-period calendars). Stored 
  verbatim as text, e.g. "December first week".
- **Issuing authority is absent from the 2022-23 and 2023-24 PDFs** — the property is omitted 
  rather than guessed.

## 10. Documents that could not be accessed or read

**None.** All 16 downloaded with HTTP 200 and a valid `%PDF` header.

Two were image-only scans with no text layer, and were **read visually rather than skipped**:

| Document | Pages | How it was read |
|---|---|---|
| Academic and Examination Calendar … 2026-27 | 3 | All 3 pages are full-page JPEG scans (0 chars extractable). Page rasters were extracted from the PDF's DCTDecode streams and read as images. |
| Revised Academic and Examination Calendar for DSY SEM III | 1 | Single full-page JPEG scan (0 chars extractable). Read the same way — which is how the second, untitled SEM IV table on that page was found. |

---

*No Git commit was made. No knowledge outside the Examination area was modified.*

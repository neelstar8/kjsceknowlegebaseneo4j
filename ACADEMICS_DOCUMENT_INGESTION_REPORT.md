# Academics Document Ingestion Report

**Source:** <https://kjsce.somaiya.edu/en/documents/> — Academics section (`department_id=15`)  
**Backend:** Neo4j only. No embeddings, no vector search, no RAG chunks, no new retrieval architecture.  
**Run:** 2026-09-14T14:34:56.618230+00:00  
**Scope:** KJSCE / KJSSE / KJSIT treated throughout as one engineering college. No institution branches created.

## 1–7. Discovery and outcome

| | |
|---|---|
| Resources discovered under Academics | **13** |
| — PDFs | **12** |
| — external web resources | **1** (MATLAB portal) |
| PDFs downloaded | **12 / 12** |
| PDFs fully analysed from actual content | **12 / 12** |
| Documents ingested | **13** (12 new nodes + 1 existing node reused) |
| Skipped | **0** |
| Calendar events extracted | **138** |
| Per-branch Drive folders mapped | **41** |
| Strategic goals / plan sections / parameters | **8 / 8 / 43** |

Nothing was skipped. The one resource not fully readable is the MATLAB portal, which is an
external MathWorks page that returns HTTP 403 to automated fetches; it is recorded as a link
with its audience, and no content is invented for it.

### How Academics is implemented (discovered, not assumed)

The Academics entries are **not** in the page's static HTML. The left menu fires
`get_document('Academics','15',<subcategory>,<id>)`, which POSTs to
`https://kjsce.somaiya.edu/arigel_general/get_document`. Calling that endpoint directly
enumerated the complete section. Seven subcategories exist:

| Subcategory | category_id | Items returned |
|---|---|---|
| Academic and Examination Calendar | `183` | 7 |
| 8 POINT DEVELOPMENT PLAN | `198` | 0 — AJAX endpoint returns 'No Data Found.'; the PDF is linked from the site's About navigation |
| KJSSE Strategic Plan (2025-2030) | `199` | 0 — AJAX endpoint returns 'No Data Found.'; the PDF is linked from the site's About navigation |
| Roll Call List | `49` | 1 |
| Class Time Table | `47` | 1 |
| Syllabus | `48` | 1 |
| Download Softwares | `163` | 1 |

Two subcategories (**8 Point Development Plan**, **KJSSE Strategic Plan**) return the literal
body `No Data Found.` from the documents endpoint. Their PDFs are published on the same official
site but linked from the **About** navigation instead. Both were located, downloaded and read in full.

### Entries that expand into further documents

Three entries are **link hubs, not documents**. Class Time Table, Syllabus and Roll Call List are
one-page index PDFs whose branch names are hyperlinks. Their embedded PDF link annotations were
extracted and each link mapped to its branch by reading the text inside the link rectangle:

| Hub | Branch folders |
|---|---|
| Class Time Table | **13** Google Drive folders |
| Syllabus | **15** Google Drive folders |
| Roll Call List | **13** Google Drive folders |

The actual timetables, syllabi and roll call lists live inside those Drive folders. This report
does not claim any subject, credit, module, day/time or room detail, because none appears in the
PDFs themselves.

## 8. Every resource in detail

### Academic & Examination Calendar AEC-KJSSE 2024-25

- **URL:** <https://kjsce-files.somaiya.edu/Academics/AEC+KJSCE+2024-25.pdf>
- **Type:** pdf · `source_type` = `academic_calendar` · subcategory: Academic and Examination Calendar
- **Academic year:** 2024-25
- **Programme:** B.Tech, M.Tech
- **Student year / level:** FY, SY, TY, LY — FY/SY/TY/LY, all programmes (UG and PG)
- **Terms / semesters:** First/Odd, Second/Even
- **Status as printed:** tentative
- **Document date:** 2024-07-25
- **Issuing authority:** Dr. S K Ukarande, Principal
- **Institution as printed:** K J Somaiya College of Engineering, Somaiya Vidyavihar University
- **Pages:** 3 · text layer: scanned_images_read_visually
- **sha256:** `cc7af30f3cf2dd43…`
- **What it actually contains:** Two calendar tables. The odd-term table is laid out in TWO COLUMNS giving different dates for FY and for SY/TY/LY; the even-term table gives a single set of dates for all levels and is headed 'Proposed/Tentative'.
- **Extracted:** 27 dated academic/examination events
- **Neo4j node:** `(:PolicyDocument {doc_id: "acad_aec_2024_25"})`
- **Relationship:** `(:Policy {policy_id:"teaching_learning_process"})-[:REFERENCES {relation:'official_academic_document'}]->` this node
- **Entities reused:** the existing `:Policy` parent and the existing `:PolicyDocument` label — no new entity type was created for this document
- **Ingestion status:** ingested and linked ✅

### Academic & Examination Calendar AEC-KJSSE 2025-26

- **URL:** <https://kjsce-files.somaiya.edu/Academics/AEC-Academic+Year-+2025-26.pdf>
- **Type:** pdf · `source_type` = `academic_calendar` · subcategory: Academic and Examination Calendar
- **Academic year:** 2025-26
- **Programme:** B.Tech, M.Tech
- **Student year / level:** FY, SY, TY, LY — FY/SY/TY/LY (B.Tech and M.Tech)
- **Terms / semesters:** First/Odd, Second/Even
- **Status as printed:** proposed
- **Document date:** 2025-05-20
- **Issuing authority:** Dr. Suresh Ukarande, Director KJSSE; Dr. Sonali Patil, Associate Dean Academics Programmes
- **Institution as printed:** K J Somaiya School of Engineering, Somaiya Vidyavihar University
- **Pages:** 3 · text layer: scanned_images_read_visually
- **sha256:** `4d3736ca33319599…`
- **What it actually contains:** A single unified calendar covering FY through LY for both B.Tech and M.Tech. The odd-term page is headed 'Proposed' and the even-term page 'Proposed/Tentative'. Note this differs from the separate FY B.Tech 2025-26 calendar issued later on 24 July 2025.
- **Extracted:** 27 dated academic/examination events
- **Neo4j node:** `(:PolicyDocument {doc_id: "acad_aec_2025_26"})`
- **Relationship:** `(:Policy {policy_id:"teaching_learning_process"})-[:REFERENCES {relation:'official_academic_document'}]->` this node
- **Entities reused:** the existing `:Policy` parent and the existing `:PolicyDocument` label — no new entity type was created for this document
- **Ingestion status:** ingested and linked ✅

### F Y B.Tech. Academic and Exam Calendar 2025-26

- **URL:** <https://kjsce-files.somaiya.edu/Academics/F.Y.+B+Tech_Academic+Calender_2025-2026.pdf>
- **Type:** pdf · `source_type` = `academic_calendar` · subcategory: Academic and Examination Calendar
- **Academic year:** 2025-26
- **Programme:** B.Tech
- **Student year / level:** FY — FY (B.Tech) only
- **Terms / semesters:** First/Odd, Second/Even
- **Status as printed:** issued
- **Document date:** 2025-07-24
- **Issuing authority:** Dr. Suresh Ukarande, Director KJSSE; Dr. Sonali Patil, Associate Dean Academics Programmes
- **Institution as printed:** K J Somaiya School of Engineering, Somaiya Vidyavihar University
- **Pages:** 3 · text layer: scanned_images_read_visually
- **sha256:** `4ec24b4d6a86e446…`
- **What it actually contains:** FY B.Tech-specific calendar for 2025-26. Its ODD term differs from the unified 2025-26 calendar (classes start 4 August rather than 14 July, MSE 6-10 October rather than ISE 15-19 September, ESE 2 weeks rather than 3). Its EVEN term is identical to the unified one.
- **Extracted:** 20 dated academic/examination events
- **Neo4j node:** `(:PolicyDocument {doc_id: "acad_aec_2025_26_fy_btech"})`
- **Relationship:** `(:Policy {policy_id:"teaching_learning_process"})-[:REFERENCES {relation:'official_academic_document'}]->` this node
- **Entities reused:** the existing `:Policy` parent and the existing `:PolicyDocument` label — no new entity type was created for this document
- **Ingestion status:** ingested and linked ✅

### F Y B.Tech. Academic and Exam Calendar 2026-27

- **URL:** <https://kjsce-files.somaiya.edu/Academics/AEC_FYB_Tech+_2026_27.pdf>
- **Type:** pdf · `source_type` = `academic_calendar` · subcategory: Academic and Examination Calendar
- **Academic year:** 2026-27
- **Programme:** B.Tech
- **Student year / level:** FY — FY (B.Tech) only
- **Terms / semesters:** First/Odd, Second/Even
- **Status as printed:** issued
- **Document date:** 2026-09-01
- **Issuing authority:** Dr. Suresh Ukarande, Director KJSSE; Dr. J H Nirmal, Associate Dean Academics Programmes
- **Institution as printed:** K J Somaiya School of Engineering (formerly K J Somaiya College of Engineering), Somaiya Vidyavihar University
- **Pages:** 3 · text layer: scanned_images_read_visually
- **sha256:** `ec14313328b38314…`
- **What it actually contains:** FY B.Tech-specific calendar for 2026-27. Its ODD term differs materially from the SY/TY/LY 2026-27 calendar (classes 17 August rather than 13 July, MSE 26-30 October rather than 7-12 September, ESE 2 weeks rather than 3). Its EVEN term matches the SY/TY/LY even term.
- **Extracted:** 25 dated academic/examination events
- **Neo4j node:** `(:PolicyDocument {doc_id: "acad_aec_2026_27_fy_btech"})`
- **Relationship:** `(:Policy {policy_id:"teaching_learning_process"})-[:REFERENCES {relation:'official_academic_document'}]->` this node
- **Entities reused:** the existing `:Policy` parent and the existing `:PolicyDocument` label — no new entity type was created for this document
- **Ingestion status:** ingested and linked ✅

### M. Tech. Academic and Exam Calendar 2026-27

- **URL:** <https://kjsse-files.somaiya.edu/Academics/AEC_2026-27_FY+(M.Tech)_Final.pdf>
- **Type:** pdf · `source_type` = `academic_calendar` · subcategory: Academic and Examination Calendar
- **Academic year:** 2026-27
- **Programme:** M.Tech
- **Student year / level:** FY, SY — FY M.Tech calendar, plus the Second Year M.Tech (Batch 2026-28) Semester III and IV schedule
- **Terms / semesters:** First/Odd, Semester III, Semester IV
- **Status as printed:** proposed
- **Document date:** 2026-07-30
- **Issuing authority:** Dr. Suresh Ukarande, Director KJSSE; Associate Dean Academic Programmes
- **Institution as printed:** K J Somaiya School of Engineering (formerly K J Somaiya College of Engineering), Somaiya Vidyavihar University
- **Pages:** 3 · text layer: scanned_images_read_visually
- **sha256:** `77b5984e38522269…`
- **What it actually contains:** Despite its single title, this PDF contains TWO different documents. Page 2 is the 'Proposed' FY M.Tech AEC for 2026-27 First Term/Odd Semester (dated 30/07/2026). Page 3 is a separate 'Schedule of Second Year M.Tech, Batch 2026-28, Semester III and IV' (dated 31/07/2026) covering dissertation milestones for all PG programmes. There is no FY M.Tech even-term table in this PDF.
- **Extracted:** 26 dated academic/examination events
- **Neo4j node:** `(:PolicyDocument {doc_id: "acad_aec_2026_27_mtech"})`
- **Relationship:** `(:Policy {policy_id:"teaching_learning_process"})-[:REFERENCES {relation:'official_academic_document'}]->` this node
- **Entities reused:** the existing `:Policy` parent and the existing `:PolicyDocument` label — no new entity type was created for this document
- **Ingestion status:** ingested and linked ✅

### Schedule of SY M.Tech

- **URL:** <https://kjsse-files.somaiya.edu/Academics/Schedule+of+SY+_M.Tech+2025-27+Batch+(Sem-III+%26+IV).pdf>
- **Type:** pdf · `source_type` = `academic_calendar` · subcategory: Academic and Examination Calendar
- **Academic year:** 2026-27
- **Programme:** M.Tech
- **Student year / level:** SY — Second Year M.Tech, Batch 2025-27, Semester III and IV (all PG programmes)
- **Terms / semesters:** Semester III, Semester IV
- **Status as printed:** issued
- **Document date:** 2026-07-31
- **Issuing authority:** Dr. Suresh Ukarande, Director KJSSE; Associate Dean Academic Programmes
- **Institution as printed:** K J Somaiya School of Engineering (formerly K J Somaiya College of Engineering), Somaiya Vidyavihar University
- **Pages:** 1 · text layer: scanned_images_read_visually
- **sha256:** `c449636489f8791a…`
- **What it actually contains:** Dissertation and milestone schedule for Second Year M.Tech of the 2025-27 batch. It is a different batch from the 2026-28 schedule carried inside the M.Tech 2026-27 calendar PDF, so the two must not be merged. Its Semester IV progress seminar refers to AEC 2026-27.
- **Extracted:** 13 dated academic/examination events
- **Neo4j node:** `(:PolicyDocument {doc_id: "acad_schedule_sy_mtech"})`
- **Relationship:** `(:Policy {policy_id:"teaching_learning_process"})-[:REFERENCES {relation:'official_academic_document'}]->` this node
- **Entities reused:** the existing `:Policy` parent and the existing `:PolicyDocument` label — no new entity type was created for this document
- **Ingestion status:** ingested and linked ✅

### Class Time Table

- **URL:** <https://kjsce-files.somaiya.edu/Academics/KJSCE_Class_TT.pdf>
- **Type:** pdf · `source_type` = `class_timetable_index` · subcategory: Class Time Table
- **Pages:** 1 · text layer: text_plus_embedded_link_annotations
- **sha256:** `48086b4c94bea87c…`
- **What it actually contains:** Index PDF listing FY B.Tech (all branches) plus each branch, with an embedded Google Drive folder link per branch. It is a link hub, not a timetable itself: the actual class timetables live in the linked Drive folders. No day/time/room/faculty detail appears in this PDF, so none is recorded.
- **Extracted:** 13 per-branch Google Drive folder links
- **Neo4j node:** `(:PolicyDocument {doc_id: "acad_class_timetable"})`
- **Relationship:** `(:Policy {policy_id:"teaching_learning_process"})-[:REFERENCES {relation:'official_academic_document'}]->` this node
- **Entities reused:** the existing `:Policy` parent and the existing `:PolicyDocument` label — no new entity type was created for this document
- **Ingestion status:** ingested and linked ✅

### Syllabus

- **URL:** <https://kjsce-files.somaiya.edu/Download/KJSCE_syllabus.pdf>
- **Type:** pdf · `source_type` = `syllabus_index` · subcategory: Syllabus
- **Pages:** 1 · text layer: text_plus_embedded_link_annotations
- **sha256:** `6bb8e5fc5e119fbf…`
- **What it actually contains:** Index PDF listing the FY Curriculum (all programmes), each B.Tech branch and All Minor Programmes, with an embedded Google Drive folder link per entry. It is a link hub, not a syllabus: no subject, subject code, credit, module or course-outcome detail appears in this PDF, and no curriculum scheme or regulation year is stated, so none is recorded.
- **Extracted:** 15 per-branch Google Drive folder links
- **Neo4j node:** `(:PolicyDocument {doc_id: "acad_syllabus"})`
- **Relationship:** `(:Policy {policy_id:"teaching_learning_process"})-[:REFERENCES {relation:'official_academic_document'}]->` this node
- **Entities reused:** the existing `:Policy` parent and the existing `:PolicyDocument` label — no new entity type was created for this document
- **Ingestion status:** ingested and linked ✅

### Roll Call List

- **URL:** <https://kjsce-files.somaiya.edu/Academics/KJSCE_Roll+Call.pdf>
- **Type:** pdf · `source_type` = `roll_call_index` · subcategory: Roll Call List
- **Pages:** 1 · text layer: text_plus_embedded_link_annotations
- **sha256:** `12960ef6802a10f3…`
- **What it actually contains:** Index PDF listing FY B.Tech (all branches) and each department, with an embedded Google Drive folder link per entry. It is a link hub and contains NO individual student names or roll numbers - only branch/department labels - so no personal data enters the graph.
- **Extracted:** 13 per-branch Google Drive folder links
- **Neo4j node:** `(:PolicyDocument {doc_id: "acad_roll_call"})`
- **Relationship:** `(:Policy {policy_id:"teaching_learning_process"})-[:REFERENCES {relation:'official_academic_document'}]->` this node
- **Entities reused:** the existing `:Policy` parent and the existing `:PolicyDocument` label — no new entity type was created for this document
- **Ingestion status:** ingested and linked ✅

### 8 POINT DEVELOPMENT PLAN

- **URL:** <https://kjsse-files.somaiya.edu/About/Eight+Point+Development+Plan_+KJSSE.pdf>
- **Type:** pdf · `source_type` = `academic_development_plan` · subcategory: 8 POINT DEVELOPMENT PLAN
- **Issuing authority:** Dr. Suresh K. Ukarande, Director
- **Institution as printed:** K J Somaiya School of Engineering
- **Pages:** 4 · text layer: text
- **sha256:** `8dbae7a134d8d315…`
- **What it actually contains:** A measurement framework, not a set of student rules. Eight numbered sections (I-VIII) define 43 numbered parameters the institute tracks for rankings, ratings and global impact, each with a 'Details' note describing how it is to be counted. It sets no obligation on students and states no targets or deadlines.
- **Extracted:** 8 sections / 43 numbered parameters
- **Neo4j node:** `(:PolicyDocument {doc_id: "acad_8_point_plan"})`
- **Relationship:** `(:Policy {policy_id:"teaching_learning_process"})-[:REFERENCES {relation:'official_academic_document'}]->` this node
- **Entities reused:** the existing `:Policy` parent and the existing `:PolicyDocument` label — no new entity type was created for this document
- **Ingestion status:** ingested and linked ✅

### KJSSE Strategic Plan (2025-2030)

- **URL:** <https://kjsse-files.somaiya.edu/About/KJSSE+Strategic+Plan+2025-2030+by+Dr.+S+K+Ukarande+.r.pdf>
- **Type:** pdf · `source_type` = `strategic_plan` · subcategory: KJSSE Strategic Plan (2025-2030)
- **Issuing authority:** Dr. S K Ukarande, Director KJSSE and Dean, Faculty of Engineering and Technology, Somaiya Vidyavihar University
- **Institution as printed:** K J Somaiya School of Engineering (formerly K J Somaiya College of Engineering), a constituent of Somaiya Vidyavihar University
- **Pages:** 12 · text layer: text
- **sha256:** `1f421370a5b10b3e…`
- **What it actually contains:** A five-year institutional roadmap headed 'STRATEGIC PLAN AGENDA, IMPLEMENTATION YEARS: 2025-2030'. Eight agenda items each carry a Development Agenda statement and a set of Action Items bucketed into three timelines: Immediately Actionable (1 Year), Planned Strengthening (1-3 Years) and Progressive Implementation (2-5 Years). These are institutional intentions and commitments, NOT current student rules or requirements.
- **Extracted:** 8 strategic goals with development agendas, across 3 action timelines
- **Neo4j node:** `(:PolicyDocument {doc_id: "acad_strategic_plan_2025_2030"})`
- **Relationship:** `(:Policy {policy_id:"teaching_learning_process"})-[:REFERENCES {relation:'official_academic_document'}]->` this node
- **Entities reused:** the existing `:Policy` parent and the existing `:PolicyDocument` label — no new entity type was created for this document
- **Ingestion status:** ingested and linked ✅

### Matlab for students/faculty and staff members

- **URL:** <https://www.mathworks.com/academia/tah-portal/kj-somaiya-college-of-engineering-925175.html>
- **Type:** external_webpage · `source_type` = `software_resource` · subcategory: Download Softwares
- **What it actually contains:** Listed under Academics > Download Softwares as 'Matlab for students/faculty and staff members.' The link is a MathWorks Academic Tah-Portal page for K J Somaiya College of Engineering, i.e. a campus-wide MATLAB licence portal hosted by MathWorks, not a file on the college site.
- **Neo4j node:** `(:PolicyDocument {doc_id: "acad_matlab"})`
- **Relationship:** `(:Policy {policy_id:"teaching_learning_process"})-[:REFERENCES {relation:'official_academic_document'}]->` this node
- **Entities reused:** the existing `:Policy` parent and the existing `:PolicyDocument` label — no new entity type was created for this document
- **Ingestion status:** ingested and linked ✅

### Reused document (duplicate, not re-created)

- **Academics title:** Academic & Examination Calendar AEC-KJSSE 2026-27 (SY/TY/LY)
- **Academics URL:** <https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026-27.pdf>
- **Already in the graph as:** `exam_aec_2026_27_sytyly_btech_fysy_mtech` (ingested from the Examination section)
- **Proof they are the same file:** identical sha256 `39eefe465aa3a9c51f470b7b67b59bfc…`
- **Action:** the existing node was reused. The Academics URL is stored on it as
  `alternate_source_url`, and the node is now linked from the Academics parent as well, so it
  is reachable from both areas. **No duplicate document node was created.**

## 9–11. Existing nodes, and whether a new parent was needed

**Existing Academic/Examination nodes found before any change:**

| policy_id | status | provisions | role here |
|---|---|---|---|
| `exam_structure_current` | current | 32 | parent of the Examination documents (untouched) |
| `examination_policy_2018` | superseded | 15 | untouched |
| `examination_policy_cbcgs` | current_but_incomplete | 15 | untouched |
| `teaching_learning_process` | current | 13 | **parent used for Academics documents** |
| `exam_ordinances_2018` | superseded | 7 | untouched |

**Did an Academic Policy node already exist? Yes.** `teaching_learning_process` (current, 13
provisions, in the `academic_quality_policy` category) is the existing academic policy in the
graph. It is kept exactly as it was and used as the anchor the Academics documents hang from —
the same pattern the Examination ingest uses with `exam_structure_current`.

**Was a new Academic parent or category required? No.** No parent node, no PolicyCategory and no
placeholder policy was created. Creating an empty node merely to hold PDFs is precisely what was
avoided.

**Were the documents turned into policy?** No. None of these resources states a rule, ordinance,
penalty or eligibility condition, so **zero PolicyProvisions** were created. Calendar dates stay
on the calendar that published them; strategic-plan goals are recorded as institutional
intentions with their 2025-2030 scope, not as student requirements; the 8 Point Plan's 43 entries
are recorded as measurement parameters.

## 12. Neo4j structure used

```
(:Policy {policy_id: 'teaching_learning_process'})      ← already existed, untouched
      │
      └─[:REFERENCES {relation: 'official_academic_document'}]─→
              (:PolicyDocument)   × 13
                   ├─ source_type = 'academic_calendar'          × 6
                   ├─ source_type = 'class_timetable_index'      × 1   (13 branch Drive links)
                   ├─ source_type = 'syllabus_index'             × 1   (15 branch Drive links)
                   ├─ source_type = 'roll_call_index'            × 1   (13 branch Drive links)
                   ├─ source_type = 'academic_development_plan'  × 1   (8 sections / 43 parameters)
                   ├─ source_type = 'strategic_plan'             × 1   (8 goals)
                   ├─ source_type = 'software_resource'          × 1   (external MATLAB portal)
                   └─ source_type = 'examination_calendar'       × 1   (REUSED, also linked from Examination)
```

**Labels used:** `PolicyDocument`, `Policy` — both already in the schema.  
**Relationship used:** `REFERENCES` — already in the schema.  
**New labels: none. New relationship types: none. New constraints: none. Schema unchanged.**

Design decisions worth recording:

- **`REFERENCES`, not `DOCUMENTED_IN`.** In this graph `DOCUMENTED_IN` asserts a policy's *text
  lives in* that PDF and carries a page range. A calendar or strategic plan does not contain the
  teaching-learning policy, so the weaker existing edge is the honest one.
- **`source_type` as the discriminator**, alongside the existing `handbook_chapter`,
  `handbook_full_edition`, `official_site_supplement` and `examination_calendar` values.
- **List-valued properties instead of child nodes.** Events, branch links, plan sections and
  strategic goals are stored as parallel arrays plus a searchable string — the same shape
  `flatten_numbers()` uses in the handbook ingest. This keeps the schema untouched. Promoting
  strategic goals to their own nodes would be a purely additive change later if wanted.
- **No personal data.** The Roll Call List PDF contains only branch/department labels and Drive
  links — no student names or roll numbers — and carries `contains_personal_data: false`.

## 13. Duplicate safety

| Check | Result |
|---|---|
| Total :PolicyDocument nodes | **42** |
| Distinct doc_id | **42** |
| Distinct source_url | **42** |
| Academics-typed documents | **12** |
| Documents linked from the academic parent | **14** |
| Nodes sharing the 2026-27 calendar's checksum (must be 1) | **1** |
| Policy nodes (unchanged) | **41** |
| PolicyProvision (unchanged) | **432** |
| Provisions created from Academics documents (must be 0) | **0** |
| FacultyMember (unchanged) | **613** |
| PYQ (unchanged) | **164** |
| Subject (unchanged) | **81** |
| Node labels Academics docs connect to (must be 1 = Policy) | **1** |

**Idempotence:** a second identical run reported `created: 0, updated: 12, reused: 1,
REFERENCES merged: 13`, and no node count moved.

## 14. Retrieval validation

All queries run against `services/academic_document_service` — deterministic Neo4j retrieval,
no model call. Answers are then passed to **one** Ollama call for final generation.

| # | Question | Documents returned | Intent block(s) |
|---|---|---|---|
| 1 | What academic documents are available? | 12 | `all` |
| 2 | Show me the academic calendars. | 7 | `calendar` |
| 3 | What is the academic calendar for 2026-27? | 4 | `calendar` |
| 4 | Show me the FY B.Tech academic calendar for 2026-27. | 2 | `calendar` |
| 5 | What academic calendar is available for M.Tech 2026-27? | 3 | `calendar` |
| 6 | What was the academic calendar for 2025-26? | 2 | `calendar` |
| 7 | Where can I find the class timetable? | 1 | `timetable` |
| 8 | Where can I find the syllabus? | 1 | `syllabus` |
| 9 | What information is available about the 2025-2030 strategic plan? | 1 | `strategic_plan` |
| 10 | What is the 8 Point Development Plan? | 1 | `development_plan` |
| 11 | Is MATLAB available for students? | 1 | `software` |
| 12 | What academic documents are available for B.Tech? | 12 | `all` |
| 13 | What is the syllabus for Computer Engineering branch? | 1 | `syllabus` |
| 14 | Show me the official academic calendar link for 2026-27. | 4 | `calendar` |
| 15 | Show me the 2026-27 academic calendar and tell me where I can find the syllabus. | 5 | `syllabus+calendar` |

**Precision checks that matter:**

- *"Where can I find the syllabus?"* returns **only** the syllabus index — no calendars.
- *"What is the 2025-2030 strategic plan?"* returns **only** the strategic plan and its 8 goals.
- *"FY B.Tech academic calendar 2026-27"* returns the FY B.Tech 2026-27 calendar; it does not
  return 2024-25, 2025-26 or the M.Tech-only calendars.
- The **multi-intent** question returns evidence for *both* intents, separately headed.
- No query returned Faculty, Internship, Attendance, Admission, Placement or PYQ content:
  every query is scoped by `source_type`, and Academics documents connect only to `:Policy`.

**Link rendering:** every URL is emitted as a Markdown link at build time. Destinations
containing literal parentheses (three of the official URLs do) are wrapped as `[text](<url>)`,
the CommonMark form, so they resolve instead of breaking at the first `)`.

## 15. Ambiguities, and documents that could not be fully read

- **The 2026-27 SY/TY/LY calendar is published twice**, under URLs differing only by `2026-27`
  vs `2026_27`. Proven identical by checksum; one node, two URLs.
- **Not every "2026-27 calendar" is the same calendar.** FY B.Tech, FY M.Tech and SY/TY/LY have
  materially different dates (FY B.Tech classes start 17 Aug 2026 and its ESE runs 2 weeks;
  SY/TY/LY start 13 Jul 2026 with a 3-week ESE; FY M.Tech starts 3 Aug 2026). They are kept as
  separate documents and never merged.
- **One PDF holds two documents.** *M. Tech. Academic and Exam Calendar 2026-27* contains the FY
  M.Tech odd-term AEC (dated 30/07/2026) **and** a separate *Schedule of Second Year M.Tech, Batch
  2026-28, Semester III & IV* (dated 31/07/2026). It has **no FY M.Tech even-term table**.
- **Two different SY M.Tech batches.** The 2026-28 batch schedule sits inside the M.Tech calendar
  PDF; the 2025-27 batch has its own PDF. Different batches, kept separate.
- **Status wording is preserved.** 2024-25 and 2025-26 even-term pages are headed
  *Proposed/Tentative*; the FY M.Tech 2026-27 page is headed *Proposed*. Recorded as
  `document_status`, so nothing is presented as final that the source does not call final.
- **The 2024-25 odd-term table has two columns** (FY vs SY/TY/LY) with different dates; both are
  recorded as separate events rather than collapsed.
- **No syllabus content could be extracted.** The Syllabus entry is an index of Drive folders. No
  subject, subject code, credits, teaching hours, prerequisites, course outcomes, modules or
  assessment structure appears in it, and **no curriculum scheme or regulation year is stated**,
  so none is recorded. The same applies to timetable day/time/room/faculty detail.
- **MATLAB portal not readable.** <https://www.mathworks.com/academia/tah-portal/...> returns
  HTTP 403 to automated requests. Recorded as an external MathWorks campus-licence portal for
  students, faculty and staff, with `content_verified: false`. Nothing about eligibility, version
  or installation steps is claimed.
- **No Drive folder was opened.** The per-branch folders are recorded as official links only; the
  graph makes no claim about their contents.

## 16. Important modelling decisions

1. **Reuse over re-create** for the duplicated 2026-27 calendar.
2. **Existing parent, no new node** — `teaching_learning_process`.
3. **No PolicyProvisions from calendars or plans** — dates and goals are not standing rules.
4. **Arrays over child nodes** to keep the schema untouched.
5. **Link hubs modelled as hubs**, with per-branch links preserved, rather than pretending the
   index PDFs are timetables/syllabi.
6. **One college.** `institution` is `KJSIT` for graph consistency while the name printed on each
   document is kept in `institution_name_in_source`; several documents say
   *"K J Somaiya School of Engineering (formerly K J Somaiya College of Engineering)"*, which is
   the source's own confirmation that these names denote one institution.

---

*No Git commit was made. Faculty, Internship, Attendance, Admission, ISE/ESE/PYQ, Placement and
all unrelated policies were not modified.*

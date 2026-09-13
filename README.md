# KJGPT Prototype — Graph Knowledge Base + Qwen3

The full Somaiya faculty directory ingested into Neo4j, retrieved with deterministic
Cypher queries, and turned into natural-language answers by Qwen3 8B running locally
via Ollama.

Stage 1 (done): every faculty member from the official directory as a flat
`FacultyMember` node. Stage 2 (later) will normalize departments, subjects and
publications into their own nodes.

```
User question
     |
Deterministic faculty-name detection
     |
Neo4j query (parameterized, no LLM-generated Cypher)
     |
FacultyMember node -> plain-text context
     |
System prompt + context + question -> Qwen3 8B (Ollama)
     |
Final answer
```

## 1. Start Neo4j Desktop

Open Neo4j Desktop, find the **KJGPT** instance, and make sure its status is
**RUNNING** (click Start if it isn't).

## 2. Create/start the database

Neo4j Desktop showed "Databases (0)" for this instance, meaning no database had been
created inside the DBMS yet besides the built-in `system` database. The default
database name is `neo4j`. If it doesn't already exist, open the instance's **Query**
pane in Neo4j Desktop / Neo4j Browser and run:

```cypher
CREATE DATABASE neo4j IF NOT EXISTS;
```

(If your Neo4j Desktop version auto-creates a default `neo4j` database when the
instance is started, this step is a no-op.)

## 3. Find your connection URI

Neo4j Desktop shows this on the instance card / connection details panel. For this
project it is:

```
neo4j://127.0.0.1:7687
```

## 4. Configure `.env`

A `.env` file already exists at the project root with:

```
NEO4J_URI=neo4j://127.0.0.1:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<your password>
NEO4J_DATABASE=neo4j

OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=qwen3:8b
```

Fill in `NEO4J_PASSWORD` with the password you set when creating the instance in
Neo4j Desktop. **Never commit this file** — it's already listed in `.gitignore`.

## 5. Check Ollama

```bash
ollama --version
ollama list
```

`qwen3:8b` must appear in the list. If it doesn't, pull it with:

```bash
ollama pull qwen3:8b
```

Ollama's local API server must also be reachable (it usually starts automatically
with the Ollama app, or run `ollama serve`):

```bash
curl http://127.0.0.1:11434/api/tags
```

## 6. Install dependencies

A virtualenv is already set up in `.venv`. To recreate it from scratch:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Dependencies: `neo4j`, `python-dotenv`, `fastapi`, `uvicorn`, `requests`. No
LangChain, no vector DB, no embeddings — deliberately, for this experiment.

## 7. Ingest the faculty directory

The pipeline is four independent stages, so Neo4j never depends on the scraper
running:

```
Somaiya directory  ->  data/faculty_directory_raw.json   (scripts/discover_faculty.py)
                   ->  data/faculty_normalized.json      (scripts/normalize_faculty.py)
                   ->  data/faculty_validation_report.json (scripts/validate_faculty.py)
                   ->  Neo4j                             (scripts/ingest_faculty.py)
```

```bash
.venv/bin/python -m scripts.discover_faculty      # ~11 min, rate limited
.venv/bin/python -m scripts.normalize_faculty
.venv/bin/python -m scripts.validate_faculty
.venv/bin/python -m scripts.ingest_faculty
```

Every stage takes `--limit N` / `--in` / `--out`, so you can rehearse on 10 records
before committing to the whole directory:

```bash
.venv/bin/python -m scripts.discover_faculty --limit 10 --out data/raw10.json
```

Ingestion is idempotent: nodes are merged on the official `faculty_id`, so re-runs
update rather than duplicate. Empty source values never overwrite existing data.

The original single-member seed is still available via
`.venv/bin/python -m graph.seed_vaibhav`.

### How the directory is actually read

The directory page is dynamically loaded, so there is no faculty data in its HTML.
The underlying request it makes is:

```
POST https://www.somaiya.edu/arigel_general/faculty_ajax_new/<offset>
     page_no=<offset>&sortBy=&keywords=&gender=&campus_check=&institute_check=
     &sub_institute_check=&dept_check=&desig_check=&lang=en
```

It returns an **HTML fragment** (not JSON) with 10 cards per request; `page_no` is a
row offset (0, 10, 20, ...), and the pagination block reports the total record count.
Individual profiles at `/en/view-member/<id>/` are fully server-rendered with labeled
accordion panels, so **all extraction is deterministic — no LLM is used for parsing**.

## 8. Inspect the graph

In Neo4j Browser (or the Neo4j Desktop query pane), run:

```cypher
MATCH (n) RETURN n;
```

There is exactly one `Faculty` root node, with a `HAS_MEMBER` edge to every
`FacultyMember`:

```cypher
MATCH (f:Faculty)-[:HAS_MEMBER]->(v:FacultyMember)
RETURN f, v LIMIT 20;

MATCH (v:FacultyMember) RETURN count(v);
```

Or run the full set of verification queries:

```bash
.venv/bin/python -m scripts.test_faculty_queries
```

## 9. Run the application

As an API:

```bash
.venv/bin/uvicorn main:app --reload
```

Then:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What subjects does Vaibhav Vasani teach?"}'
```

Or the debug endpoint (shows the Cypher query, raw Neo4j result, and context sent
to Qwen3 — development only, not meant for a production UI):

```bash
curl -X POST http://127.0.0.1:8000/ask/debug \
  -H "Content-Type: application/json" \
  -d '{"question": "What subjects does Vaibhav Vasani teach?"}'
```

## 10. Run the test questions

```bash
.venv/bin/python -m tests.test_questions
```

This runs 8 fixed test questions (including one that is **not** in the knowledge
base — "What is Vaibhav Vasani's favorite food?") and prints the full pipeline
trace for each: question, Cypher query, Neo4j result, context sent to Qwen3, and
Qwen3's final answer. It also verifies the Neo4j and Ollama connections first.

## How information flows

1. `services/faculty_service.retrieve` deterministically routes the question. It
   matches against vocabularies read out of the graph itself (names, departments,
   research topics, subjects), so it grows automatically as the directory grows.
2. `graph/faculty_queries` runs a parameterized Cypher query against Neo4j.
   Qwen never generates Cypher.
3. `services/faculty_service.build_context` converts the node's properties into
   clean, labeled plain text.
4. That context, plus the reusable system prompt (`llm/system_prompt.py`), plus the
   user's question, is sent to Qwen3 8B via `llm/qwen.ask_qwen`.
5. The system prompt instructs Qwen3 to treat the context as the sole source of
   truth and to say so explicitly when the answer isn't in it — verified this
   works correctly (see report below).

## Project layout

```
graph/
    neo4j_driver.py      # driver, connection verification, run_query()
    faculty.py           # original single-member Cypher helpers
    faculty_queries.py   # directory-scale Cypher (parameterized, deterministic)
    faculty_ingestion.py # constraint, upsert, non-destructive merge logic
    seed_vaibhav.py      # original seed script (MERGE-based, idempotent)
scraper/
    somaiya_faculty.py   # directory AJAX endpoint + profile page parsing
normalization/
    faculty_normalizer.py # raw site records -> one common schema
scripts/
    discover_faculty.py  normalize_faculty.py  validate_faculty.py
    ingest_faculty.py    test_faculty_queries.py  test_faculty_rag.py
llm/
    qwen.py             # Ollama HTTP client, knows nothing about Neo4j
    system_prompt.py    # reusable KJGPT system prompt (not faculty-specific)
services/
    faculty_service.py  # retrieval -> context -> Qwen orchestration, debug trace
data/
    vaibhav_vasani.json            # original hand-verified seed record
    faculty_directory_raw.json     # raw snapshot of the source
    faculty_normalized.json        # common schema
    faculty_validation_report.json # pre-insert validation
    faculty_ingestion_report.json  # post-insert data quality report
    faculty_errors.json            # per-record failures, never fatal
tests/
    test_questions.py   # runs the 8 test questions with full debug trace
main.py                 # FastAPI app: /ask and /ask/debug
```

## Known limitations (by design)

- **Flat graph.** Department, school, subject and publication are properties on
  `FacultyMember`, not their own nodes. Normalizing them is the next stage.
- **Sparse source data.** Many profiles — largely visiting faculty — are genuinely
  empty on the official site ("No Information Available"). Those are stored as
  empty rather than filled in with guesses. Nothing in this pipeline invents data.
- **Routing is vocabulary matching, not NLP.** Good enough for "who teaches X" /
  "faculty in Y department" questions; it does not handle multi-hop or comparative
  questions yet.

---

# PYQ Knowledge Base (ISE/MSE + ESE)

Previous-year question papers stay in Google Drive. KJGPT stores **only metadata
and the Drive link**, so a student asking for a paper gets a URL they click to open
the real PDF in Drive.

No chunking, no embeddings, no vector DB, no OCR, **no PDF bytes in Neo4j** — this is
link resolution, not RAG. `scripts/test_pyq_queries.py` asserts that the graph carries
no paper content.

Phase 1 covers **ISE/MSE only**. ESE papers are detected, classified, and deliberately
not ingested; they are logged to `data/pyq_ese_report.json` so their coverage is known
in advance.

## Graph shape

```
(:PYQ)-[:STORED_IN {page_label, part_index, section_label}]->(:PYQFile)
(:PYQ)-[:FOR_SUBJECT]->(:Subject)
```

Two nodes, because in this corpus the physical file and the logical paper are
many-to-many **in both directions**:

- `SY(PSOT,AOA,RDBMS,TACD).PDF` is one Drive file holding **four** papers. Four `PYQ`
  nodes point at one `PYQFile` — the file is never duplicated.
- `ML 1 pg.jpg` + `ML 2 pg.jpg` is **one** paper split across two files. One `PYQ`
  node with two `STORED_IN` edges, each carrying its page label.

Identity: `PYQFile.drive_file_id` (assigned by Google, stable forever) and
`PYQ.pyq_id`, a deterministic function of the parsed metadata —
`{subject}|{exam_type}|{academic_year}|{term}|sem{n}|{category}|{variant}`. Both are
unique-constrained, so **re-running the ingest updates rather than duplicates**.

`:Faculty`, `:FacultyMember` and `:HAS_MEMBER` are untouched. The only thing shared
with the faculty system is the Neo4j driver in `graph/neo4j_driver.py` — no second
connection.

## 1. Google Drive access

A read-only service account, so the credential physically cannot modify the source
Drive:

1. In the Google Cloud console: create a project, enable the **Drive API**, create a
   **service account**, download its JSON key.
2. Save the key as `service_account.json` in the project root (already gitignored).
3. Share the Drive folder with the service account's `client_email` — **Viewer** is
   enough.

`.env` additions:

```
GOOGLE_SERVICE_ACCOUNT_FILE=./service_account.json
PYQ_DRIVE_ROOT_FOLDER_ID=1oBE_-p1E64JOl28luRsiw_KGyjUs-Q-J
PYQ_COLLECTION_NAME=ise_question_paper_kj_somaiya
PYQ_DEFAULT_BRANCH=Computer Engineering
PYQ_ALLOWED_EXAM_TYPES=ISE
```

`branch` is a collection-level assumption (the Drive tree has no branch level
anywhere), recorded on every node as `branch_source="collection_default"` so it stays
auditable. `program` (B.Tech vs M.Tech) **is** derived from the folder level.

## 2. Run the pipeline

Same four independent stages as the faculty pipeline, so Neo4j never depends on Drive
being reachable:

```
Google Drive  ->  data/pyq_drive_raw.json      (scripts/discover_pyq.py)
              ->  data/pyq_normalized.json     (scripts/normalize_pyq.py)
              ->  data/pyq_validation_report.json (scripts/validate_pyq.py)
              ->  Neo4j                        (scripts/ingest_pyq.py)
```

```bash
.venv/bin/python -m scripts.discover_pyq          # recursive, cycle-safe Drive walk
.venv/bin/python -m scripts.normalize_pyq         # offline; re-run freely
.venv/bin/python -m scripts.validate_pyq          # blocks ingest on severe errors
.venv/bin/python -m scripts.ingest_pyq --dry-run  # prints writes, touches nothing
.venv/bin/python -m scripts.ingest_pyq
```

Every stage takes `--in` / `--out` / `--limit`. `--report-stale` lists `PYQFile` nodes
this run no longer saw in Drive; it **reports only and never deletes**.

Stage 1 does zero parsing, so once you have the raw dump every later re-parse is free
and offline — the same reason `faculty_directory_raw.json` exists.

## 3. How a filename is read

Parsing is **token-bag based, not positional**, because the same facts appear in
different orders across years — `TY V OS.PDF`, `ISE_COA_SY.pdf`, `OS.pdf`,
`SVU_SEM_III_OOPM_2021-22_without_CO.pdf`. The folder path is at least as
authoritative as the file name; for the 24-25 files (`OS.pdf`) it is the only context
that exists.

| Field | Source |
|---|---|
| `academic_year` | folder (`23-24`) or filename (`2021-22`) → `"2023-24"` |
| `exam_term` | `odd`/`even` in the folder; `July-Nov`→odd, `Jan-May`→even |
| `exam_year` | odd → start year, even → start+1. Drive's `modifiedTime` is upload time, **not** exam time, so it is never used for this |
| `semester` | SY odd=3 even=4, TY odd=5 even=6, LY odd=7 even=8, M.Tech I/II. An explicit roman numeral in the name wins and any mismatch is logged |
| `course_category` | `H-`/`Honors`/`Honours`, `M-`, `OEHM-`/`OET-`, `DeptElec` |
| `variant` | `PWD`/`PwD` → `pwd`, else `regular` — without this the PwD paper would collide with the regular one |
| `subject_code` | `116U01C301`-style codes when present |

`exam_type` resolves **nearest-first**: file name, then each folder from the leaf up
to the root. An explicit `ESE` at a nearer level beats an `ISE` further out. Most
24-25 files carry no exam token at all, but the collection root is literally named
*"ise question paper kj somaiya"* — that is inheritance from an explicit ancestor,
not a guess, and `exam_type_source` records exactly where it came from:

```cypher
MATCH (p:PYQ) RETURN p.exam_type_source, count(*);
```

## 4. Subject normalization

Filenames use abbreviations (`OS`, `CN`, `COA`, `AOA`, `H-DA`, `OEHM-IMGT`), so
`data/pyq_subjects.json` is a curated registry mapping aliases to a canonical
`subject_key`. Matching is **exact, whole-word, longest-alias-first — never fuzzy**,
because the corpus contains `Futter.pdf` and a fuzzy matcher would resolve that
confidently and wrongly.

Every expansion in the registry is corroborated either by a real subject string
already in the faculty graph (`FacultyMember.subjects_taught`) or by the filename
expanding its own abbreviation. **Nothing is guessed.**

An abbreviation that could not be corroborated ingests as
`subject_status="unresolved"` with `subject_raw` set — the paper is still reachable by
link — and is listed in `data/pyq_unknown_report.json` and in the `candidates` block of
`data/pyq_subjects.json` with the evidence for and against. To adopt one: move it into
`subjects`, give it a `name`, re-run normalize + ingest, and the paper moves to its
proper `subject_key` in place.

```cypher
MATCH (p:PYQ) WHERE p.subject_status = 'unresolved'
RETURN p.subject_raw, count(*) ORDER BY count(*) DESC;
```

## 5. Multiple papers in one PDF

Since paper *content* is never read, multi-paper files are found two ways:

1. **Filename** — two or more *known* subject aliases in one name
   (`SY(PSOT,AOA,RDBMS,TACD).PDF`) produce N `PYQ` nodes sharing one `PYQFile`.
2. **`data/pyq_overrides.json`** — keyed by `drive_file_id`, applied after parsing and
   always wins. This is the escape hatch for anything a filename cannot express, with
   no code change and no re-discovery:

```json
{ "1AbC...": { "papers": [
    {"subject_key": "dbms", "semester": 4, "section_label": "pages 1-3"},
    {"subject_key": "os",   "semester": 4, "section_label": "pages 4-6"}]}}
```

Known limitation: a PDF named `DBMS.pdf` that silently contains three papers cannot be
detected in this phase. It surfaces as one PYQ pointing at the right link — the student
still reaches the paper. A later content-analysis pipeline can populate the overrides
file automatically; nothing in the data model changes.

Two distinct files that parse to the same `pyq_id` are merged into one paper so both
links stay reachable. When page labels explain it (`ML 1 pg` / `ML 2 pg`) that is
expected; otherwise it is flagged in `data/pyq_collisions.json` for review.

## 6. Verify

```bash
.venv/bin/python -m tests.test_pyq_normalizer   # offline, no credentials needed
.venv/bin/python -m scripts.test_pyq_queries    # against the live graph
.venv/bin/python -m scripts.ingest_pyq          # run twice -> inserted=0
```

`tests/test_pyq_normalizer.py` asserts against real filenames from the tree, including
the PwD pair, both Honours spellings, the embedded course code, the `Futter` typo
staying unresolved, syllabus/zip/ESE rejection, and the split-paper identity.

`scripts/test_pyq_queries.py` checks the student question shapes, that
`FacultyMember` is still 613, that no content leaked into the graph, that an unqualified
request returns both exam types while a qualified one does not, that nothing outside
2019-2025 is reachable, that no semester bundle is reachable by subject, and that no
physical file was duplicated.

## 7. The ESE collection

ESE is a second collection through the same four stages, plus one extra stage. It writes
its own `data/pyq_ese_*.json` files, so the ISE data is never touched. Existing ISE nodes
cannot collide with it because `pyq_id` includes `exam_type`.

```bash
.venv/bin/python -m scripts.discover_pyq \
    --folder 1WyOcP9LbQBgA7LWsK6nZeZ2YWfk-asHr \
    --out data/pyq_ese_drive_raw.json

.venv/bin/python -m scripts.normalize_pyq --tag ese \
    --in data/pyq_ese_drive_raw.json \
    --collection ese_question_paper_kj_somaiya \
    --exam-types ESE --default-exam-type ESE \
    --min-year 2019 --max-year 2025

# stage 2.5 -- opens semester-bundle PDFs to find the subjects inside
.venv/bin/python -m scripts.inspect_pyq_bundles --in data/pyq_ese_normalized.json

.venv/bin/python -m scripts.validate_pyq --in data/pyq_ese_normalized.json \
    --report data/pyq_ese_validation_report.json
.venv/bin/python -m scripts.ingest_pyq --in data/pyq_ese_normalized.json \
    --report data/pyq_ese_ingestion_report.json
```

Three things about this corpus differ from the ISE one, and the pipeline handles each:

**Nothing names the exam type.** Not the files, not the folders, not the root. The ISE
root is literally called *"ise question paper kj somaiya"*, which is where its ISE marker
comes from; this tree has no equivalent. `--default-exam-type ESE` asserts it for the
collection, and the resulting nodes record `exam_type_source: "collection_default"` so
the provenance stays honest. A file that *does* name ESE or ISE still wins over the
default, and a contradictory tree is still rejected.

**Dates are split across folders.** `2024/JANUARY - JUNE 2024/...` gives a bare calendar
year plus a month range instead of the `23-24` span the ISE tree uses. The two are
recombined: an odd term opens the academic year, an even term closes it, so
*JAN-JUNE 2024* is `2023-24` and *JULY-DEC 2024* is `2024-25`.

**Granularity is mixed.** Some files are one paper (`SEM V COMP OS.pdf`); others bundle a
whole semester (`COMP- SEM- VIII..pdf`) and name no subject at all. See below.

### Semester bundles

A file whose own name states a semester but no subject is a **bundle** — every paper sat
that semester, in one PDF. It gets `is_bundle: true`, a `_bundle_<branch>` identity, and
**no `FOR_SUBJECT` edge**, so a subject query can never reach it.

`scripts/inspect_pyq_bundles.py` then opens each bundle and reads its pages. Where a page
header carries a curated alias or a subject code, that subject is established and the
bundle is replaced by real subject-level papers with their page ranges on the
`STORED_IN` edge. Where it cannot be established, the bundle stays exactly as it was.

The splitter refuses rather than guesses: an unreadable or scanned PDF, a header naming
two subjects, fewer than 30% of pages resolved, or only one subject found all leave the
bundle intact. A wrong subject link is worse than an unresolved one, because it hands a
student the wrong paper while looking authoritative. **No ISE data is ever used to infer
an ESE subject.** Nothing downloaded is retained — the bytes are read in memory and
dropped, and only `{subject_key, page_start, page_end}` survives.

So: `"ESE OS papers"` returns only papers whose subject was actually established, while
`"all ESE papers"` and `"ESE 2024 papers"` also return unresolved bundles.

### The two folders are nested

The ESE folder sits *inside* the ISE root. A future ISE re-walk must therefore exclude it,
or it would sweep ESE files into the ISE collection:

```bash
.venv/bin/python -m scripts.discover_pyq \
    --exclude-folder 1WyOcP9LbQBgA7LWsK6nZeZ2YWfk-asHr
```

## Files

```
drive/client.py                  # read-only service account, cycle-safe recursive walk
normalization/pyq_normalizer.py  # token-bag parsing; deterministic, no LLM
graph/pyq_ingestion.py           # constraints, indexes, idempotent upsert, stale report
graph/pyq_queries.py             # parameterized search; Qwen never writes Cypher
normalization/pyq_pdf_subjects.py # reads bundle pages to establish subjects
scripts/discover_pyq.py  normalize_pyq.py  validate_pyq.py  ingest_pyq.py
scripts/inspect_pyq_bundles.py   # stage 2.5, splits semester bundles
services/pyq_service.py          # question -> filters -> links; deterministic
scripts/test_pyq_queries.py      # live-graph verification
tests/test_pyq_normalizer.py     # offline parser tests on real filenames
tests/test_pyq_questions.py      # 34 student questions end to end
data/pyq_subjects.json           # curated alias registry + uncorroborated candidates
data/pyq_overrides.json          # manual multi-paper / correction hook
data/pyq_unknown_report.json     # everything needing a human look
data/pyq_ese_report.json         # ESE papers, held for phase 2
data/pyq_collisions.json         # distinct files that parsed to the same paper
```

## 8. Asking for a paper

```bash
curl -X POST http://127.0.0.1:8000/pyq/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Give me DBMS 2024 ISE paper"}'
```

Returns `{"answer": "...", "papers": [{title, drive_url, subject, exam_type,
academic_year, semester}]}`. A UI should link the `papers` array directly rather than
parsing URLs back out of `answer`. `/pyq/ask/debug` additionally shows the extracted
filters.

**Retrieval and the answer are both deterministic, and that is the performance
decision.** A PYQ answer *is* the list of links retrieval already found, so passing it
through an 8B model only adds latency and risk:

| path | latency | |
|---|---|---|
| deterministic (default) | **~2 ms** | exact links, never drops a row |
| `use_llm: true` | 11-18 s | observed silently omitting one of two matching papers |

Qwen never writes Cypher here either. `extract_filters()` pulls `{subject, exam_type,
year, semester, year_of_study, category, variant}` out of the question by matching
against the `(:Subject).aliases` vocabulary **read from the graph**, the same pattern
`services/faculty_service._build_index()` uses. Add a subject to the registry and the
router picks it up on the next run with no code change.

Two guards worth knowing about:

- Aliases that are ordinary English words must appear capitalised. Without this,
  `is` (Information Security) matches nearly every question asked — *"What **is** the
  OS paper"* would return security papers.
- Connector words are deliberately **not** stripped from the question, because
  aliases like `analysis of algorithms` need them to match.

Misses are answered honestly and distinctly: an ESE request says ESE is not loaded
yet, a subject we don't hold is named back to the student, and a question with no
filters at all asks for one rather than dumping the corpus.

```bash
.venv/bin/python -m tests.test_pyq_questions            # 34 questions, ~2 ms each
.venv/bin/python -m tests.test_pyq_questions --verbose  # print every link
.venv/bin/python -m tests.test_pyq_questions --llm      # compare the Qwen path
```

Note on years: *"DBMS paper 2024"* returns both the 2024-25 and the 2023-24 paper on
purpose — `2024` may mean calendar 2024 (an even-semester exam sits in the second half
of 2023-24) or academic 2024-25, and both readings are matched rather than guessed.

## Not in this phase

Nothing in the retrieval path is model-driven, which is deliberate. If you later want
free-form questions the pattern matcher cannot handle ("compare the DBMS papers from
the last three years"), the place to add a model is filter *extraction* —
`extract_filters()` — not answer generation, and not Cypher. `/ask` and `/ask/debug`
are unchanged.

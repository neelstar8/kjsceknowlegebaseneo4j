# KJ GPT - Examination Documents: 20 Student Questions (LIVE)

**Started:** 2026-09-14T18:52:56  
**Retrieval:** `services.exam_document_service` - deterministic, Neo4j only, no model call.  
**LLM:** `qwen3:8b` via Ollama, using the Policy-domain system prompt stored on `(:PolicyHandbook).system_prompt` (the one carrying the LINK HANDLING rule).  
**Data/code/prompts:** untouched - testing only.

## Progress

- Completed: **20 / 20**
- Status: **COMPLETE**
- Elapsed: 293s

---

## Q1. What examination documents do you have?

*What this probes:* broad listing

| | |
|---|---|
| Documents retrieved | 16 |
| Retrieval time | 68.5 ms |
| LLM time | 35.4 s |
| Markdown links in retrieval | 17 |
| Markdown links in LLM answer | 1 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': None, 'programme': None, 'level': None, 'wants_forms': False, 'wants_dates': False}` |

**KJ GPT answer (LLM):**

The K J Somaiya Institute of Technology (KJSIT) provides several academic and examination calendars for different academic years and programs. These include:

- **Academic and Examination Calendar SY/TY/LY (B.Tech) FY/SY (M.Tech) 2026-27**  
- **Academic and Examination (AEC) Calendar 2023-24**  
- **Academic and Examination Calendar 2022-23**  
- **Academic and Examination Calendar for FY B.Tech 2021-22**  
- **Academic and Examination Calendar for FY M.Tech 2021-22**  
- **Academic and Examination Calendar for Newly Admitted Batch (26 Nov and onwards) to FY B.Tech - 2021**  
- **Revised Academic Calendar for FY B.Tech Even Semester 2021-22**  
- **Revised Academic and Examination Calendar for DSY SEM III**  
- **SY B.Tech (SVU-2020) Academic and Examination Calendar 21-22**  
- **SY M.Tech (SVU-2020) Academic and Examination Calendar 21-22**  
- **TY-LY Academic and Examination Calendar 2021-22**  
- **FY B.Tech - Academic and Examination Calendar**  
- **FY M.Tech - Academic and Examination Calendar**  
- **Odd Term/Semester UG and PG FY - SVU 2020-21**  
- **Odd Term/Semester UG and PG SY/TY/LY 2020-21**  
- **SY/TY/LY B.Tech/M.Tech Academic and Examination Calendar**

These calendars are available on the [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/).

<details><summary>Deterministic retrieval passed to the model</summary>

```
**16 official examination document(s):**

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed
- [Academic and Examination (AEC) Calendar 2023-24](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_+Uniform+AEC_SVU+KJSCE++2023-24.pdf)
  Academic year 2023-24 · FY/SY/TY/LY, all programmes (UG and PG) · marked tentative
- [Academic and Examination Calendar 2022-23- SY, TY, LY and FY](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_KJSCE__Academic+and+Examination+Calendar+AEC-2022-23.pdf)
  Academic year 2022-23 · Separate templates for SY B.Tech, SY M.Tech, TY B.Tech, LY B.Tech (KJSCE 2018) and FY B.Tech
- [Academic and Examination Calendar for FY B TECH  2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+B.TECH_+Academic+and+Examination+Calendar.pdf)
  Academic year 2021-22 · FY B.Tech
- [Academic and Examination Calendar for FY FY M TECH 2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+M.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY M.Tech
- [Academic and Examination Calendar for Newly admitted  Batch ( 26 Nov and onwards)  to FY BTECH -2021](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/FOR+NEW+BATCH__21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY B.Tech, newly admitted students only (admitted November 2021 and onwards)
- [Revised Academic Calendar for FY BTECH Even Semester 2021-22](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/REVISED+EVEN+SEM_21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY B.Tech, regular students (2021-22) · marked revised
- [Revised Academic and Examination Calendar for DSY SEM III](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/Revised+Academic+and+Examination+Calendar+DSY+2021-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020) Sem IV, and Sem III for Direct Second Year (DSY) admitted students only · marked revised
- [SY B.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+B.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020)
- [SY M.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+M.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · SY M.Tech (SVU 2020)
- [TY-LY  Academic and Examination Calendar 2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/TY-LY+_+Academic+and+Examination+Calendar+2021-22.pdf)
  Academic year 2021-22 · TY/LY B.Tech
- [FY B.TECH -Academic and Examination calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+B.TECH_+Academic+and+Examination+Calendar+20-21.pdf)
  Academic year 2020-21 · FY B.Tech, for students admitted to college till October 2020
- [FY.M.TECH -Academic and Examination calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+M.TECH_+Academic+and+Examination+Calendar+20-21.pdf)
  Academic year 2020-21 · FY M.Tech
- [Odd Term/Semester UG and PG FY -SVU 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar_FY+BTECH+and+MTECH.pdf)
  Academic year 2020-21 · FY B.Tech Semester I and FY M.Tech Semester I · marked tentative
- [Odd Term/Semester UG and PG SY/TY/LY 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar+-+UG-SY-TY+and+PG+SEM+III.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech Semesters III, V and VII and M.Tech Sem III (regular); plus FY/SY/TY/LY B.Tech Semesters I-VI and M.Tech Sem I (backlog/KT)
- [SY/TY/LY B. Tech/M. Tech Academic and Examination Calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/SY-LY+_+Academic+and+Examination+Calendar_Modified.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech and M.Tech

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q2. Show me all the examination calendars.

*What this probes:* broad listing

| | |
|---|---|
| Documents retrieved | 16 |
| Retrieval time | 39.8 ms |
| LLM time | 94.2 s |
| Markdown links in retrieval | 17 |
| Markdown links in LLM answer | 17 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': None, 'programme': None, 'level': None, 'wants_forms': False, 'wants_dates': False}` |

**KJ GPT answer (LLM):**

Here are the available examination calendars for the K J Somaiya Institute of Technology (KJSIT):

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)  
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed

- [Academic and Examination (AEC) Calendar 2023-24](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_+Uniform+AEC_SVU+KJSCE++2023-24.pdf)  
  Academic year 2023-24 · FY/SY/TY/LY, all programmes (UG and PG) · marked tentative

- [Academic and Examination Calendar 2022-23- SY, TY, LY and FY](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_KJSCE__Academic+and+Examination+Calendar+AEC-2022-23.pdf)  
  Academic year 2022-23 · Separate templates for SY B.Tech, SY M.Tech, TY B.Tech, LY B.Tech (KJSCE 2018) and FY B.Tech

- [Academic and Examination Calendar for FY B TECH  2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+B.TECH_+Academic+and+Examination+Calendar.pdf)  
  Academic year 2021-22 · FY B.Tech

- [Academic and Examination Calendar for FY FY M TECH 2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+M.TECH_+Academic+and+Examination+Calendar+21-22.pdf)  
  Academic year 2021-22 · FY M.Tech

- [Academic and Examination Calendar for Newly admitted  Batch ( 26 Nov and onwards)  to FY BTECH -2021](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/FOR+NEW+BATCH__21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)  
  Academic year 2021-22 · FY B.Tech, newly admitted students only (admitted November 2021 and onwards)

- [Revised Academic Calendar for FY BTECH Even Semester 2021-22](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/REVISED+EVEN+SEM_21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)  
  Academic year 2021-22 · FY B.Tech, regular students (2021-22) · marked revised

- [Revised Academic and Examination Calendar for DSY SEM III](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/Revised+Academic+and+Examination+Calendar+DSY+2021-22.pdf)  
  Academic year 2021-22 · SY B.Tech (SVU 2020) Sem IV, and Sem III for Direct Second Year (DSY) admitted students only · marked revised

- [SY B.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+B.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)  
  Academic year 2021-22 · SY B.Tech (SVU 2020)

- [SY M.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+M.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)  
  Academic year 2021-22 · SY M.Tech (SVU 2020)

- [TY-LY  Academic and Examination Calendar 2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/TY-LY+_+Academic+and+Examination+Calendar+2021-22.pdf)  
  Academic year 2021-22 · TY/LY B.Tech

- [FY B.TECH -Academic and Examination calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+B.TECH_+Academic+and+Examination+Calendar+20-21.pdf)  
  Academic year 2020-21 · FY B.Tech, for students admitted to college till October 2020

- [FY.M.TECH -Academic and Examination calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+M.TECH_+Academic+and+Examination+Calendar+20-21.pdf)  
  Academic year 2020-21 · FY M.Tech

- [Odd Term/Semester UG and PG FY -SVU 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar_FY+BTECH+and+MTECH.pdf)  
  Academic year 2020-21 · FY B.Tech Semester I and FY M.Tech Semester I · marked tentative

- [Odd Term/Semester UG and PG SY/TY/LY 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar+-+UG-SY-TY+and+PG+SEM+III.pdf)  
  Academic year 2020-21 · SY/TY/LY B.Tech Semesters III, V and VII and M.Tech Sem III (regular); plus FY/SY/TY/LY B.Tech Semesters I-VI and M.Tech Sem I (backlog/KT)

- [SY/TY/LY B. Tech/M. Tech Academic and Examination Calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/SY-LY+_+Academic+and+Examination+Calendar_Modified.pdf)  
  Academic year 2020-21 · SY/TY/LY B.Tech and M.Tech

These calendars are available on the [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) under the Examination section.

<details><summary>Deterministic retrieval passed to the model</summary>

```
**16 official examination document(s):**

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed
- [Academic and Examination (AEC) Calendar 2023-24](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_+Uniform+AEC_SVU+KJSCE++2023-24.pdf)
  Academic year 2023-24 · FY/SY/TY/LY, all programmes (UG and PG) · marked tentative
- [Academic and Examination Calendar 2022-23- SY, TY, LY and FY](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_KJSCE__Academic+and+Examination+Calendar+AEC-2022-23.pdf)
  Academic year 2022-23 · Separate templates for SY B.Tech, SY M.Tech, TY B.Tech, LY B.Tech (KJSCE 2018) and FY B.Tech
- [Academic and Examination Calendar for FY B TECH  2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+B.TECH_+Academic+and+Examination+Calendar.pdf)
  Academic year 2021-22 · FY B.Tech
- [Academic and Examination Calendar for FY FY M TECH 2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+M.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY M.Tech
- [Academic and Examination Calendar for Newly admitted  Batch ( 26 Nov and onwards)  to FY BTECH -2021](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/FOR+NEW+BATCH__21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY B.Tech, newly admitted students only (admitted November 2021 and onwards)
- [Revised Academic Calendar for FY BTECH Even Semester 2021-22](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/REVISED+EVEN+SEM_21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY B.Tech, regular students (2021-22) · marked revised
- [Revised Academic and Examination Calendar for DSY SEM III](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/Revised+Academic+and+Examination+Calendar+DSY+2021-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020) Sem IV, and Sem III for Direct Second Year (DSY) admitted students only · marked revised
- [SY B.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+B.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020)
- [SY M.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+M.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · SY M.Tech (SVU 2020)
- [TY-LY  Academic and Examination Calendar 2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/TY-LY+_+Academic+and+Examination+Calendar+2021-22.pdf)
  Academic year 2021-22 · TY/LY B.Tech
- [FY B.TECH -Academic and Examination calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+B.TECH_+Academic+and+Examination+Calendar+20-21.pdf)
  Academic year 2020-21 · FY B.Tech, for students admitted to college till October 2020
- [FY.M.TECH -Academic and Examination calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+M.TECH_+Academic+and+Examination+Calendar+20-21.pdf)
  Academic year 2020-21 · FY M.Tech
- [Odd Term/Semester UG and PG FY -SVU 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar_FY+BTECH+and+MTECH.pdf)
  Academic year 2020-21 · FY B.Tech Semester I and FY M.Tech Semester I · marked tentative
- [Odd Term/Semester UG and PG SY/TY/LY 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar+-+UG-SY-TY+and+PG+SEM+III.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech Semesters III, V and VII and M.Tech Sem III (regular); plus FY/SY/TY/LY B.Tech Semesters I-VI and M.Tech Sem I (backlog/KT)
- [SY/TY/LY B. Tech/M. Tech Academic and Examination Calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/SY-LY+_+Academic+and+Examination+Calendar_Modified.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech and M.Tech

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q3. Where do I download examination forms?

*What this probes:* empty section - must say so

| | |
|---|---|
| Documents retrieved | 16 |
| Retrieval time | 32.2 ms |
| LLM time | 19.9 s |
| Markdown links in retrieval | 17 |
| Markdown links in LLM answer | 1 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': None, 'programme': None, 'level': None, 'wants_forms': True, 'wants_dates': False}` |

**KJ GPT answer (LLM):**

The official Examination Download Forms section on the KJSCE documents page currently publishes no documents, and the college's own page returns "No Data Found." for it. However, you can find the relevant academic and examination calendars for various academic years and programs by visiting the [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) and navigating to the Examination section. The calendars provided there include details about the academic schedule and examination dates for different programs and years.

<details><summary>Deterministic retrieval passed to the model</summary>

```
The official documents page has an **Examination Download Forms** section, but it currently publishes no documents at all - the college's own page returns "No Data Found." for it. The Examination section's published documents are the academic and examination calendars listed below.

**16 official examination document(s):**

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed
- [Academic and Examination (AEC) Calendar 2023-24](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_+Uniform+AEC_SVU+KJSCE++2023-24.pdf)
  Academic year 2023-24 · FY/SY/TY/LY, all programmes (UG and PG) · marked tentative
- [Academic and Examination Calendar 2022-23- SY, TY, LY and FY](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_KJSCE__Academic+and+Examination+Calendar+AEC-2022-23.pdf)
  Academic year 2022-23 · Separate templates for SY B.Tech, SY M.Tech, TY B.Tech, LY B.Tech (KJSCE 2018) and FY B.Tech
- [Academic and Examination Calendar for FY B TECH  2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+B.TECH_+Academic+and+Examination+Calendar.pdf)
  Academic year 2021-22 · FY B.Tech
- [Academic and Examination Calendar for FY FY M TECH 2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+M.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY M.Tech
- [Academic and Examination Calendar for Newly admitted  Batch ( 26 Nov and onwards)  to FY BTECH -2021](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/FOR+NEW+BATCH__21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY B.Tech, newly admitted students only (admitted November 2021 and onwards)
- [Revised Academic Calendar for FY BTECH Even Semester 2021-22](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/REVISED+EVEN+SEM_21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY B.Tech, regular students (2021-22) · marked revised
- [Revised Academic and Examination Calendar for DSY SEM III](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/Revised+Academic+and+Examination+Calendar+DSY+2021-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020) Sem IV, and Sem III for Direct Second Year (DSY) admitted students only · marked revised
- [SY B.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+B.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020)
- [SY M.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+M.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · SY M.Tech (SVU 2020)
- [TY-LY  Academic and Examination Calendar 2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/TY-LY+_+Academic+and+Examination+Calendar+2021-22.pdf)
  Academic year 2021-22 · TY/LY B.Tech
- [FY B.TECH -Academic and Examination calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+B.TECH_+Academic+and+Examination+Calendar+20-21.pdf)
  Academic year 2020-21 · FY B.Tech, for students admitted to college till October 2020
- [FY.M.TECH -Academic and Examination calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+M.TECH_+Academic+and+Examination+Calendar+20-21.pdf)
  Academic year 2020-21 · FY M.Tech
- [Odd Term/Semester UG and PG FY -SVU 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar_FY+BTECH+and+MTECH.pdf)
  Academic year 2020-21 · FY B.Tech Semester I and FY M.Tech Semester I · marked tentative
- [Odd Term/Semester UG and PG SY/TY/LY 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar+-+UG-SY-TY+and+PG+SEM+III.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech Semesters III, V and VII and M.Tech Sem III (regular); plus FY/SY/TY/LY B.Tech Semesters I-VI and M.Tech Sem I (backlog/KT)
- [SY/TY/LY B. Tech/M. Tech Academic and Examination Calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/SY-LY+_+Academic+and+Examination+Calendar_Modified.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech and M.Tech

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q4. What's the academic and examination calendar for 2026-27?

*What this probes:* specific year

| | |
|---|---|
| Documents retrieved | 1 |
| Retrieval time | 199.4 ms |
| LLM time | 8.3 s |
| Markdown links in retrieval | 2 |
| Markdown links in LLM answer | 1 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': '2026-27', 'programme': None, 'level': None, 'wants_forms': False, 'wants_dates': False}` |

**KJ GPT answer (LLM):**

The academic and examination calendar for the academic year 2026-27 for B.Tech (SY/TY/LY) and M.Tech (FY/SY) is outlined in the document titled [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf). This document provides the proposed schedule for academic and examination activities.

<details><summary>Deterministic retrieval passed to the model</summary>

```
**1 official examination document(s) for 2026-27:**

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q5. Give me the 2023-24 exam calendar.

*What this probes:* specific year

| | |
|---|---|
| Documents retrieved | 1 |
| Retrieval time | 32.3 ms |
| LLM time | 6.6 s |
| Markdown links in retrieval | 2 |
| Markdown links in LLM answer | 1 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': '2023-24', 'programme': None, 'level': None, 'wants_forms': False, 'wants_dates': False}` |

**KJ GPT answer (LLM):**

The 2023-24 exam calendar for KJSIT is available in the [Academic and Examination (AEC) Calendar 2023-24](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_+Uniform+AEC_SVU+KJSCE++2023-24.pdf). This document outlines the tentative schedule for FY/SY/TY/LY, all programmes (UG and PG).

<details><summary>Deterministic retrieval passed to the model</summary>

```
**1 official examination document(s) for 2023-24:**

- [Academic and Examination (AEC) Calendar 2023-24](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_+Uniform+AEC_SVU+KJSCE++2023-24.pdf)
  Academic year 2023-24 · FY/SY/TY/LY, all programmes (UG and PG) · marked tentative

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q6. Is there an exam calendar for B.Tech?

*What this probes:* programme filter

| | |
|---|---|
| Documents retrieved | 13 |
| Retrieval time | 21.5 ms |
| LLM time | 12.3 s |
| Markdown links in retrieval | 14 |
| Markdown links in LLM answer | 1 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': None, 'programme': 'B.Tech', 'level': None, 'wants_forms': False, 'wants_dates': False}` |

**KJ GPT answer (LLM):**

Yes, there are several exam calendars available for B.Tech students at KJSIT, covering different academic years and semesters. These include calendars for FY (First Year), SY (Second Year), TY (Third Year), LY (Fourth Year), and revised or special admission batches. You can find these calendars on the [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) under the Examination section.

<details><summary>Deterministic retrieval passed to the model</summary>

```
**13 official examination document(s) for B.Tech:**

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed
- [Academic and Examination (AEC) Calendar 2023-24](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_+Uniform+AEC_SVU+KJSCE++2023-24.pdf)
  Academic year 2023-24 · FY/SY/TY/LY, all programmes (UG and PG) · marked tentative
- [Academic and Examination Calendar 2022-23- SY, TY, LY and FY](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_KJSCE__Academic+and+Examination+Calendar+AEC-2022-23.pdf)
  Academic year 2022-23 · Separate templates for SY B.Tech, SY M.Tech, TY B.Tech, LY B.Tech (KJSCE 2018) and FY B.Tech
- [Academic and Examination Calendar for FY B TECH  2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+B.TECH_+Academic+and+Examination+Calendar.pdf)
  Academic year 2021-22 · FY B.Tech
- [Academic and Examination Calendar for Newly admitted  Batch ( 26 Nov and onwards)  to FY BTECH -2021](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/FOR+NEW+BATCH__21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY B.Tech, newly admitted students only (admitted November 2021 and onwards)
- [Revised Academic Calendar for FY BTECH Even Semester 2021-22](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/REVISED+EVEN+SEM_21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY B.Tech, regular students (2021-22) · marked revised
- [Revised Academic and Examination Calendar for DSY SEM III](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/Revised+Academic+and+Examination+Calendar+DSY+2021-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020) Sem IV, and Sem III for Direct Second Year (DSY) admitted students only · marked revised
- [SY B.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+B.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020)
- [TY-LY  Academic and Examination Calendar 2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/TY-LY+_+Academic+and+Examination+Calendar+2021-22.pdf)
  Academic year 2021-22 · TY/LY B.Tech
- [FY B.TECH -Academic and Examination calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+B.TECH_+Academic+and+Examination+Calendar+20-21.pdf)
  Academic year 2020-21 · FY B.Tech, for students admitted to college till October 2020
- [Odd Term/Semester UG and PG FY -SVU 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar_FY+BTECH+and+MTECH.pdf)
  Academic year 2020-21 · FY B.Tech Semester I and FY M.Tech Semester I · marked tentative
- [Odd Term/Semester UG and PG SY/TY/LY 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar+-+UG-SY-TY+and+PG+SEM+III.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech Semesters III, V and VII and M.Tech Sem III (regular); plus FY/SY/TY/LY B.Tech Semesters I-VI and M.Tech Sem I (backlog/KT)
- [SY/TY/LY B. Tech/M. Tech Academic and Examination Calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/SY-LY+_+Academic+and+Examination+Calendar_Modified.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech and M.Tech

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q7. I'm an M.Tech student, which calendars apply to me?

*What this probes:* programme filter

| | |
|---|---|
| Documents retrieved | 9 |
| Retrieval time | 26.0 ms |
| LLM time | 26.6 s |
| Markdown links in retrieval | 10 |
| Markdown links in LLM answer | 3 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': None, 'programme': 'M.Tech', 'level': None, 'wants_forms': False, 'wants_dates': False}` |

**KJ GPT answer (LLM):**

As an M.Tech student, the following academic calendars apply to you depending on your academic year:

- If you are in your **first year (FY)**, the **[FY M.Tech - Academic and Examination calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+M.TECH_+Academic+and+Examination+Calendar+20-21.pdf)** for the academic year 2020-21 applies. However, please note that this is a historical document and you should confirm with the academic office for the most current calendar.
- If you are in your **second year (SY)**, the **[SY M.Tech (SVU-2020) - Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+M.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)** for the academic year 2021-22 applies. Again, confirm with the academic office for the most recent version.
- For the academic year **2026-27**, the **[Academic and Examination Calendar SY/TY/LY (B.Tech) FY/SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)** is marked as proposed and may apply to you if you are in your second year (SY) or later.

For the most accurate and up-to-date information, please consult the academic office or the official examination section.

<details><summary>Deterministic retrieval passed to the model</summary>

```
**9 official examination document(s) for M.Tech:**

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed
- [Academic and Examination (AEC) Calendar 2023-24](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_+Uniform+AEC_SVU+KJSCE++2023-24.pdf)
  Academic year 2023-24 · FY/SY/TY/LY, all programmes (UG and PG) · marked tentative
- [Academic and Examination Calendar 2022-23- SY, TY, LY and FY](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_KJSCE__Academic+and+Examination+Calendar+AEC-2022-23.pdf)
  Academic year 2022-23 · Separate templates for SY B.Tech, SY M.Tech, TY B.Tech, LY B.Tech (KJSCE 2018) and FY B.Tech
- [Academic and Examination Calendar for FY FY M TECH 2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+M.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY M.Tech
- [SY M.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+M.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · SY M.Tech (SVU 2020)
- [FY.M.TECH -Academic and Examination calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+M.TECH_+Academic+and+Examination+Calendar+20-21.pdf)
  Academic year 2020-21 · FY M.Tech
- [Odd Term/Semester UG and PG FY -SVU 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar_FY+BTECH+and+MTECH.pdf)
  Academic year 2020-21 · FY B.Tech Semester I and FY M.Tech Semester I · marked tentative
- [Odd Term/Semester UG and PG SY/TY/LY 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar+-+UG-SY-TY+and+PG+SEM+III.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech Semesters III, V and VII and M.Tech Sem III (regular); plus FY/SY/TY/LY B.Tech Semesters I-VI and M.Tech Sem I (backlog/KT)
- [SY/TY/LY B. Tech/M. Tech Academic and Examination Calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/SY-LY+_+Academic+and+Examination+Calendar_Modified.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech and M.Tech

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q8. When is the ESE in the 2026-27 calendar?

*What this probes:* dated event lookup

| | |
|---|---|
| Documents retrieved | 1 |
| Retrieval time | 24.0 ms |
| LLM time | 15.7 s |
| Markdown links in retrieval | 2 |
| Markdown links in LLM answer | 1 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': '2026-27', 'programme': None, 'level': None, 'wants_forms': False, 'wants_dates': True}` |

**KJ GPT answer (LLM):**

The ESE (End Semester Examination) for the 2026-27 academic year is scheduled as follows:

- For the First/Odd term: 18 November 2026 to 8 December 2026 (a period of 3 weeks).
- For the Second/Even term: 3 May 2027 to 21 May 2027 (a period of 3 weeks).

These dates are outlined in the [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf).

<details><summary>Deterministic retrieval passed to the model</summary>

```
**1 official examination document(s) for 2026-27:**

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed
    - First/Odd — Commencement of Classes (SY to LY): 13 July 2026
    - First/Odd — Mid-Semester Examination (MSE): 7 September 2026 to 12 September 2026
    - First/Odd — Display of Attendance and Defaulter List up to August: 3 September 2026
    - First/Odd — Display of Attendance and Defaulter List up to September: 5 October 2026
    - First/Odd — One week Diwali Holidays for Students: 9 November to 13 November 2026
    - First/Odd — Last instructional day of First/Odd term: 4 November 2026
    - First/Odd — Submission of Theory CA, LAB/TUT CA, Term-work Marksheets: 6 November 2026
    - First/Odd — Execution of Regular ESE Examinations (Seminars + Projects + Semester Long Internships + Practical + Oral + Theory): 18 November to 8 December 2026 (3 weeks)
    - First/Odd — Internship (Wherever is applicable): 10 December 2026 to 3 January 2027
    - First/Odd — One week Christmas Holidays for Students: 24 December 2026 to 1 January 2027
    - First/Odd — Date of Declaration of Regular Examinations Results: On or before 8 January 2027
    - First/Odd — Open day: From 11 to 15 January 2027 (exact schedule notified in first week of January 2027)
    - First/Odd — Proposed Date of Declaration of results after open day of semester I, III, V and VII: On or before 30 January 2027
    - Second/Even — Commencement of Classes: 4 January 2027
    - Second/Even — Institute Level Faculty Meeting (ILFM): 4 January 2027
    - Second/Even — Mid-Semester Examination (MSE)/Test: 1 March to 6 March 2027
    - Second/Even — Last instructional day: 23 April 2027
    - Second/Even — Display of Final Attendance and Defaulter List: 26 April 2027
    - Second/Even — Submission of Theory CA, LAB/TUT CA, Term-work Marksheets: 26 April 2027
    - Second/Even — Execution of Regular ESE Examinations (Seminars + Projects + Semester Long Internships + Practical + Oral + Theory): 3 May to 21 May 2027
    - Second/Even — Internship (Wherever Applicable): 24 May 2027 to 30 June 2027
    - Second/Even — Date of Declaration of Regular Examinations Results: On or before 10 June 2027
    - Second/Even — Open day: 11 June 2027
    - Second/Even — Date of Declaration of results after open day of semester II, IV, VI, VIII: On or before 22 June 2027
    - Second/Even — Execution of Supplementary ESE Examinations: 24 June 2027 to 8 July 2027
    - Second/Even — Date of Declaration of Supplementary Examinations Results: On or before 22 July 2027
    - Second/Even — Open day of Supplementary Exam: 23 July 2027
    - Second/Even — Date of Declaration of results after open day of Supplementary Exam (semester II, IV, VI, VIII): On or before 4 August 2027
    - Second/Even — Commencement of Next Academic Year 2027-28: 1 July 2027
    - Second/Even — Convocation 2027: 18 September 2027

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q9. When is the mid-semester exam in 2026-27?

*What this probes:* dated event lookup

| | |
|---|---|
| Documents retrieved | 1 |
| Retrieval time | 29.7 ms |
| LLM time | 2.6 s |
| Markdown links in retrieval | 2 |
| Markdown links in LLM answer | 0 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': '2026-27', 'programme': None, 'level': None, 'wants_forms': False, 'wants_dates': True}` |

**KJ GPT answer (LLM):**

The mid-semester examination (MSE) for the 2026-27 academic year is scheduled from 7 September 2026 to 12 September 2026.

<details><summary>Deterministic retrieval passed to the model</summary>

```
**1 official examination document(s) for 2026-27:**

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed
    - First/Odd — Commencement of Classes (SY to LY): 13 July 2026
    - First/Odd — Mid-Semester Examination (MSE): 7 September 2026 to 12 September 2026
    - First/Odd — Display of Attendance and Defaulter List up to August: 3 September 2026
    - First/Odd — Display of Attendance and Defaulter List up to September: 5 October 2026
    - First/Odd — One week Diwali Holidays for Students: 9 November to 13 November 2026
    - First/Odd — Last instructional day of First/Odd term: 4 November 2026
    - First/Odd — Submission of Theory CA, LAB/TUT CA, Term-work Marksheets: 6 November 2026
    - First/Odd — Execution of Regular ESE Examinations (Seminars + Projects + Semester Long Internships + Practical + Oral + Theory): 18 November to 8 December 2026 (3 weeks)
    - First/Odd — Internship (Wherever is applicable): 10 December 2026 to 3 January 2027
    - First/Odd — One week Christmas Holidays for Students: 24 December 2026 to 1 January 2027
    - First/Odd — Date of Declaration of Regular Examinations Results: On or before 8 January 2027
    - First/Odd — Open day: From 11 to 15 January 2027 (exact schedule notified in first week of January 2027)
    - First/Odd — Proposed Date of Declaration of results after open day of semester I, III, V and VII: On or before 30 January 2027
    - Second/Even — Commencement of Classes: 4 January 2027
    - Second/Even — Institute Level Faculty Meeting (ILFM): 4 January 2027
    - Second/Even — Mid-Semester Examination (MSE)/Test: 1 March to 6 March 2027
    - Second/Even — Last instructional day: 23 April 2027
    - Second/Even — Display of Final Attendance and Defaulter List: 26 April 2027
    - Second/Even — Submission of Theory CA, LAB/TUT CA, Term-work Marksheets: 26 April 2027
    - Second/Even — Execution of Regular ESE Examinations (Seminars + Projects + Semester Long Internships + Practical + Oral + Theory): 3 May to 21 May 2027
    - Second/Even — Internship (Wherever Applicable): 24 May 2027 to 30 June 2027
    - Second/Even — Date of Declaration of Regular Examinations Results: On or before 10 June 2027
    - Second/Even — Open day: 11 June 2027
    - Second/Even — Date of Declaration of results after open day of semester II, IV, VI, VIII: On or before 22 June 2027
    - Second/Even — Execution of Supplementary ESE Examinations: 24 June 2027 to 8 July 2027
    - Second/Even — Date of Declaration of Supplementary Examinations Results: On or before 22 July 2027
    - Second/Even — Open day of Supplementary Exam: 23 July 2027
    - Second/Even — Date of Declaration of results after open day of Supplementary Exam (semester II, IV, VI, VIII): On or before 4 August 2027
    - Second/Even — Commencement of Next Academic Year 2027-28: 1 July 2027
    - Second/Even — Convocation 2027: 18 September 2027

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q10. When do results come out for 2026-27?

*What this probes:* dated event lookup

| | |
|---|---|
| Documents retrieved | 1 |
| Retrieval time | 724.0 ms |
| LLM time | 3.6 s |
| Markdown links in retrieval | 2 |
| Markdown links in LLM answer | 0 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': '2026-27', 'programme': None, 'level': None, 'wants_forms': False, 'wants_dates': True}` |

**KJ GPT answer (LLM):**

For the academic year 2026-27, the results for the First/Odd term are declared on or before 8 January 2027. For the Second/Even term, the results are declared on or before 10 June 2027.

<details><summary>Deterministic retrieval passed to the model</summary>

```
**1 official examination document(s) for 2026-27:**

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed
    - First/Odd — Commencement of Classes (SY to LY): 13 July 2026
    - First/Odd — Mid-Semester Examination (MSE): 7 September 2026 to 12 September 2026
    - First/Odd — Display of Attendance and Defaulter List up to August: 3 September 2026
    - First/Odd — Display of Attendance and Defaulter List up to September: 5 October 2026
    - First/Odd — One week Diwali Holidays for Students: 9 November to 13 November 2026
    - First/Odd — Last instructional day of First/Odd term: 4 November 2026
    - First/Odd — Submission of Theory CA, LAB/TUT CA, Term-work Marksheets: 6 November 2026
    - First/Odd — Execution of Regular ESE Examinations (Seminars + Projects + Semester Long Internships + Practical + Oral + Theory): 18 November to 8 December 2026 (3 weeks)
    - First/Odd — Internship (Wherever is applicable): 10 December 2026 to 3 January 2027
    - First/Odd — One week Christmas Holidays for Students: 24 December 2026 to 1 January 2027
    - First/Odd — Date of Declaration of Regular Examinations Results: On or before 8 January 2027
    - First/Odd — Open day: From 11 to 15 January 2027 (exact schedule notified in first week of January 2027)
    - First/Odd — Proposed Date of Declaration of results after open day of semester I, III, V and VII: On or before 30 January 2027
    - Second/Even — Commencement of Classes: 4 January 2027
    - Second/Even — Institute Level Faculty Meeting (ILFM): 4 January 2027
    - Second/Even — Mid-Semester Examination (MSE)/Test: 1 March to 6 March 2027
    - Second/Even — Last instructional day: 23 April 2027
    - Second/Even — Display of Final Attendance and Defaulter List: 26 April 2027
    - Second/Even — Submission of Theory CA, LAB/TUT CA, Term-work Marksheets: 26 April 2027
    - Second/Even — Execution of Regular ESE Examinations (Seminars + Projects + Semester Long Internships + Practical + Oral + Theory): 3 May to 21 May 2027
    - Second/Even — Internship (Wherever Applicable): 24 May 2027 to 30 June 2027
    - Second/Even — Date of Declaration of Regular Examinations Results: On or before 10 June 2027
    - Second/Even — Open day: 11 June 2027
    - Second/Even — Date of Declaration of results after open day of semester II, IV, VI, VIII: On or before 22 June 2027
    - Second/Even — Execution of Supplementary ESE Examinations: 24 June 2027 to 8 July 2027
    - Second/Even — Date of Declaration of Supplementary Examinations Results: On or before 22 July 2027
    - Second/Even — Open day of Supplementary Exam: 23 July 2027
    - Second/Even — Date of Declaration of results after open day of Supplementary Exam (semester II, IV, VI, VIII): On or before 4 August 2027
    - Second/Even — Commencement of Next Academic Year 2027-28: 1 July 2027
    - Second/Even — Convocation 2027: 18 September 2027

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q11. Is the 2026-27 calendar final or just proposed?

*What this probes:* must flag proposed/tentative

| | |
|---|---|
| Documents retrieved | 1 |
| Retrieval time | 23.1 ms |
| LLM time | 3.8 s |
| Markdown links in retrieval | 2 |
| Markdown links in LLM answer | 0 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': '2026-27', 'programme': None, 'level': None, 'wants_forms': False, 'wants_dates': False}` |

**KJ GPT answer (LLM):**

The 2026-27 Academic and Examination Calendar for B.Tech and M.Tech is marked as "proposed" in the document, indicating that it is not yet the final version. The exact status of whether it becomes final or any updates to it would be communicated by the institute.

<details><summary>Deterministic retrieval passed to the model</summary>

```
**1 official examination document(s) for 2026-27:**

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q12. When are the Diwali holidays in 2026-27?

*What this probes:* dated event lookup

| | |
|---|---|
| Documents retrieved | 1 |
| Retrieval time | 6.7 ms |
| LLM time | 7.0 s |
| Markdown links in retrieval | 2 |
| Markdown links in LLM answer | 0 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': '2026-27', 'programme': None, 'level': None, 'wants_forms': False, 'wants_dates': True}` |

**KJ GPT answer (LLM):**

The Diwali holidays for the 2026-27 academic year are from 9 November to 13 November 2026.

<details><summary>Deterministic retrieval passed to the model</summary>

```
**1 official examination document(s) for 2026-27:**

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed
    - First/Odd — Commencement of Classes (SY to LY): 13 July 2026
    - First/Odd — Mid-Semester Examination (MSE): 7 September 2026 to 12 September 2026
    - First/Odd — Display of Attendance and Defaulter List up to August: 3 September 2026
    - First/Odd — Display of Attendance and Defaulter List up to September: 5 October 2026
    - First/Odd — One week Diwali Holidays for Students: 9 November to 13 November 2026
    - First/Odd — Last instructional day of First/Odd term: 4 November 2026
    - First/Odd — Submission of Theory CA, LAB/TUT CA, Term-work Marksheets: 6 November 2026
    - First/Odd — Execution of Regular ESE Examinations (Seminars + Projects + Semester Long Internships + Practical + Oral + Theory): 18 November to 8 December 2026 (3 weeks)
    - First/Odd — Internship (Wherever is applicable): 10 December 2026 to 3 January 2027
    - First/Odd — One week Christmas Holidays for Students: 24 December 2026 to 1 January 2027
    - First/Odd — Date of Declaration of Regular Examinations Results: On or before 8 January 2027
    - First/Odd — Open day: From 11 to 15 January 2027 (exact schedule notified in first week of January 2027)
    - First/Odd — Proposed Date of Declaration of results after open day of semester I, III, V and VII: On or before 30 January 2027
    - Second/Even — Commencement of Classes: 4 January 2027
    - Second/Even — Institute Level Faculty Meeting (ILFM): 4 January 2027
    - Second/Even — Mid-Semester Examination (MSE)/Test: 1 March to 6 March 2027
    - Second/Even — Last instructional day: 23 April 2027
    - Second/Even — Display of Final Attendance and Defaulter List: 26 April 2027
    - Second/Even — Submission of Theory CA, LAB/TUT CA, Term-work Marksheets: 26 April 2027
    - Second/Even — Execution of Regular ESE Examinations (Seminars + Projects + Semester Long Internships + Practical + Oral + Theory): 3 May to 21 May 2027
    - Second/Even — Internship (Wherever Applicable): 24 May 2027 to 30 June 2027
    - Second/Even — Date of Declaration of Regular Examinations Results: On or before 10 June 2027
    - Second/Even — Open day: 11 June 2027
    - Second/Even — Date of Declaration of results after open day of semester II, IV, VI, VIII: On or before 22 June 2027
    - Second/Even — Execution of Supplementary ESE Examinations: 24 June 2027 to 8 July 2027
    - Second/Even — Date of Declaration of Supplementary Examinations Results: On or before 22 July 2027
    - Second/Even — Open day of Supplementary Exam: 23 July 2027
    - Second/Even — Date of Declaration of results after open day of Supplementary Exam (semester II, IV, VI, VIII): On or before 4 August 2027
    - Second/Even — Commencement of Next Academic Year 2027-28: 1 July 2027
    - Second/Even — Convocation 2027: 18 September 2027

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q13. Is there a calendar for direct second year (DSY) students?

*What this probes:* DSY edge case

| | |
|---|---|
| Documents retrieved | 8 |
| Retrieval time | 569.6 ms |
| LLM time | 11.4 s |
| Markdown links in retrieval | 9 |
| Markdown links in LLM answer | 1 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': None, 'programme': None, 'level': 'SY', 'wants_forms': False, 'wants_dates': False}` |

**KJ GPT answer (LLM):**

Yes, there is a calendar specifically for Direct Second Year (DSY) students. The **Revised Academic and Examination Calendar for DSY SEM III** applies to the academic year 2021-22 and covers the Sem III for DSY admitted students only. You can access it here: [Revised Academic and Examination Calendar for DSY SEM III](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/Revised+Academic+and+Examination+Calendar+DSY+2021-22.pdf).

<details><summary>Deterministic retrieval passed to the model</summary>

```
**8 official examination document(s) for SY:**

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed
- [Academic and Examination (AEC) Calendar 2023-24](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_+Uniform+AEC_SVU+KJSCE++2023-24.pdf)
  Academic year 2023-24 · FY/SY/TY/LY, all programmes (UG and PG) · marked tentative
- [Academic and Examination Calendar 2022-23- SY, TY, LY and FY](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_KJSCE__Academic+and+Examination+Calendar+AEC-2022-23.pdf)
  Academic year 2022-23 · Separate templates for SY B.Tech, SY M.Tech, TY B.Tech, LY B.Tech (KJSCE 2018) and FY B.Tech
- [Revised Academic and Examination Calendar for DSY SEM III](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/Revised+Academic+and+Examination+Calendar+DSY+2021-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020) Sem IV, and Sem III for Direct Second Year (DSY) admitted students only · marked revised
- [SY B.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+B.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020)
- [SY M.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+M.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · SY M.Tech (SVU 2020)
- [Odd Term/Semester UG and PG SY/TY/LY 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar+-+UG-SY-TY+and+PG+SEM+III.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech Semesters III, V and VII and M.Tech Sem III (regular); plus FY/SY/TY/LY B.Tech Semesters I-VI and M.Tech Sem I (backlog/KT)
- [SY/TY/LY B. Tech/M. Tech Academic and Examination Calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/SY-LY+_+Academic+and+Examination+Calendar_Modified.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech and M.Tech

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q14. When is the supplementary exam for SY B.Tech 2021-22?

*What this probes:* supplementary window

| | |
|---|---|
| Documents retrieved | 2 |
| Retrieval time | 349.5 ms |
| LLM time | 6.0 s |
| Markdown links in retrieval | 3 |
| Markdown links in LLM answer | 0 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': '2021-22', 'programme': 'B.Tech', 'level': 'SY', 'wants_forms': False, 'wants_dates': True}` |

**KJ GPT answer (LLM):**

The supplementary exam for SY B.Tech 2021-22 is scheduled for the last week of July 2022.

<details><summary>Deterministic retrieval passed to the model</summary>

```
**2 official examination document(s) for 2021-22, B.Tech, SY:**

- [Revised Academic and Examination Calendar for DSY SEM III](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/Revised+Academic+and+Examination+Calendar+DSY+2021-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020) Sem IV, and Sem III for Direct Second Year (DSY) admitted students only · marked revised
    - Even — Commencement of classes of Even term (SEM IV): 10 January 2022
    - Even — In-Semester Examination (ISE) (SEM IV): 7 to 11 March 2022
    - Even — Dispersal of Classes of even term (SEM IV): 6 May 2022
    - Even — Conduct of Examinations (Oral + Theory) (SEM IV): 9 May 2022 to 12 June 2022
    - Even — Supplementary Exam (SEM IV): Last week of July 2022
    - Even — Commencement of classes for Mathematics of SEM III (DSY only): 10 January 2022 till 15 April 2022 (time slot decided by course faculty)
    - Even — Theory and Practical classes for SEM III, all other courses (DSY only): 1 June 2022 to 23 July 2022
    - Even — Conduct of ISE SEM III (DSY only): 27 June to 2 July 2022
    - Even — Conduct of Examinations (Oral/Practical) SEM III (DSY only): 25 July to 30 July 2022
    - Even — Conduct of Examinations (Theory) SEM III (DSY only): 1 August to 13 August 2022
- [SY B.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+B.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020)
    - Odd — Commencement of classes: 9 August 2021
    - Odd — In-Semester Examination (ISE): 4 to 8 October 2021
    - Odd — Dispersal of Classes of odd term: 3 December 2021
    - Odd — Conduct of Examinations (Oral + Theory): 6 December to 31 December 2021
    - Even — Commencement of classes of Even term: 10 January 2022
    - Even — In-Semester Examination (ISE): 7 to 11 March 2022
    - Even — Dispersal of Classes of even term: 6 May 2022
    - Even — Conduct of Examinations (Oral + Theory): 9 May 2022 to 12 June 2022
    - Even — Supplementary Exam: Last week of July 2022

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q15. Do you have an exam calendar for 2019-20?

*What this probes:* year we do NOT hold - must refuse

| | |
|---|---|
| Documents retrieved | 0 |
| Retrieval time | 215.9 ms |
| LLM time | 2.3 s |
| Markdown links in retrieval | 0 |
| Markdown links in LLM answer | 0 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': '2019-20', 'programme': None, 'level': None, 'wants_forms': False, 'wants_dates': False}` |

**KJ GPT answer (LLM):**

I do not have an examination document for the academic year 2019-20 in the KJ GPT knowledge base.

<details><summary>Deterministic retrieval passed to the model</summary>

```
I don't hold an examination document for 2019-20 in the KJ GPT knowledge base.

Examination documents I do hold, by academic year: 2026-27 (1), 2023-24 (1), 2022-23 (1), 2021-22 (8), 2020-21 (5).
```

</details>

---

## Q16. What's the exam calendar for 2030-31?

*What this probes:* year we do NOT hold - must refuse

| | |
|---|---|
| Documents retrieved | 0 |
| Retrieval time | 31.5 ms |
| LLM time | 2.1 s |
| Markdown links in retrieval | 0 |
| Markdown links in LLM answer | 0 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': '2030-31', 'programme': None, 'level': None, 'wants_forms': False, 'wants_dates': False}` |

**KJ GPT answer (LLM):**

The available KJSIT policy information does not specify an exam calendar for the academic year 2030-31.

<details><summary>Deterministic retrieval passed to the model</summary>

```
I don't hold an examination document for 2030-31 in the KJ GPT knowledge base.

Examination documents I do hold, by academic year: 2026-27 (1), 2023-24 (1), 2022-23 (1), 2021-22 (8), 2020-21 (5).
```

</details>

---

## Q17. Were exams online during covid? What was the paper pattern?

*What this probes:* 2020-21 mode details

| | |
|---|---|
| Documents retrieved | 16 |
| Retrieval time | 10.6 ms |
| LLM time | 10.5 s |
| Markdown links in retrieval | 17 |
| Markdown links in LLM answer | 0 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': None, 'programme': None, 'level': None, 'wants_forms': False, 'wants_dates': False}` |

**KJ GPT answer (LLM):**

The available KJSIT policy information does not specify whether exams were conducted online during the pandemic or provide details about the paper pattern used during that period.

<details><summary>Deterministic retrieval passed to the model</summary>

```
**16 official examination document(s):**

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed
- [Academic and Examination (AEC) Calendar 2023-24](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_+Uniform+AEC_SVU+KJSCE++2023-24.pdf)
  Academic year 2023-24 · FY/SY/TY/LY, all programmes (UG and PG) · marked tentative
- [Academic and Examination Calendar 2022-23- SY, TY, LY and FY](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_KJSCE__Academic+and+Examination+Calendar+AEC-2022-23.pdf)
  Academic year 2022-23 · Separate templates for SY B.Tech, SY M.Tech, TY B.Tech, LY B.Tech (KJSCE 2018) and FY B.Tech
- [Academic and Examination Calendar for FY B TECH  2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+B.TECH_+Academic+and+Examination+Calendar.pdf)
  Academic year 2021-22 · FY B.Tech
- [Academic and Examination Calendar for FY FY M TECH 2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+M.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY M.Tech
- [Academic and Examination Calendar for Newly admitted  Batch ( 26 Nov and onwards)  to FY BTECH -2021](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/FOR+NEW+BATCH__21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY B.Tech, newly admitted students only (admitted November 2021 and onwards)
- [Revised Academic Calendar for FY BTECH Even Semester 2021-22](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/REVISED+EVEN+SEM_21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY B.Tech, regular students (2021-22) · marked revised
- [Revised Academic and Examination Calendar for DSY SEM III](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/Revised+Academic+and+Examination+Calendar+DSY+2021-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020) Sem IV, and Sem III for Direct Second Year (DSY) admitted students only · marked revised
- [SY B.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+B.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020)
- [SY M.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+M.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · SY M.Tech (SVU 2020)
- [TY-LY  Academic and Examination Calendar 2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/TY-LY+_+Academic+and+Examination+Calendar+2021-22.pdf)
  Academic year 2021-22 · TY/LY B.Tech
- [FY B.TECH -Academic and Examination calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+B.TECH_+Academic+and+Examination+Calendar+20-21.pdf)
  Academic year 2020-21 · FY B.Tech, for students admitted to college till October 2020
- [FY.M.TECH -Academic and Examination calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+M.TECH_+Academic+and+Examination+Calendar+20-21.pdf)
  Academic year 2020-21 · FY M.Tech
- [Odd Term/Semester UG and PG FY -SVU 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar_FY+BTECH+and+MTECH.pdf)
  Academic year 2020-21 · FY B.Tech Semester I and FY M.Tech Semester I · marked tentative
- [Odd Term/Semester UG and PG SY/TY/LY 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar+-+UG-SY-TY+and+PG+SEM+III.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech Semesters III, V and VII and M.Tech Sem III (regular); plus FY/SY/TY/LY B.Tech Semesters I-VI and M.Tech Sem I (backlog/KT)
- [SY/TY/LY B. Tech/M. Tech Academic and Examination Calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/SY-LY+_+Academic+and+Examination+Calendar_Modified.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech and M.Tech

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q18. I'm FY B.Tech 2021-22, my even semester dates changed - which calendar is right?

*What this probes:* revised vs new-batch ambiguity

| | |
|---|---|
| Documents retrieved | 3 |
| Retrieval time | 26.9 ms |
| LLM time | 14.4 s |
| Markdown links in retrieval | 4 |
| Markdown links in LLM answer | 1 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': '2021-22', 'programme': 'B.Tech', 'level': 'FY', 'wants_forms': False, 'wants_dates': True}` |

**KJ GPT answer (LLM):**

For the FY B.Tech 2021-22 even semester, the revised calendar is the correct one. The **Revised Academic Calendar for FY BTECH Even Semester 2021-22** reflects the updated dates for commencement of classes, In-Semester Examinations (ISE), dispersal of classes, and the conduct of examinations. You can refer to the calendar here: [Revised Even Semester Calendar](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/REVISED+EVEN+SEM_21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf).

<details><summary>Deterministic retrieval passed to the model</summary>

```
**3 official examination document(s) for 2021-22, B.Tech, FY:**

- [Academic and Examination Calendar for FY B TECH  2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+B.TECH_+Academic+and+Examination+Calendar.pdf)
  Academic year 2021-22 · FY B.Tech
    - Odd — Commencement of classes: 11 October 2021
    - Odd — In-Semester Examination (ISE): 20 December to 23 December 2021
    - Odd — Dispersal of Classes of odd term: 4 February 2022
    - Odd — Conduct of Examinations (Oral + Theory): 7 February 2022 to 28 February 2022
    - Even — Commencement of classes of Even term: 7 March 2022
    - Even — In-Semester Examination (ISE): 2 May 2022 to 7 May 2022
    - Even — Dispersal of Classes of even term: 30 June 2022
    - Even — Conduct of Examinations (Oral + Theory): 4 July to 23 July 2022
- [Academic and Examination Calendar for Newly admitted  Batch ( 26 Nov and onwards)  to FY BTECH -2021](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/FOR+NEW+BATCH__21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY B.Tech, newly admitted students only (admitted November 2021 and onwards)
    - Odd — Commencement of classes: 10 January 2022
    - Odd — In-Semester Examination (ISE): 5, 12 and 26 February 2022
    - Odd — Dispersal of Classes of odd term: 19 March 2022
    - Odd — Conduct of Examinations (Oral + Theory): 21 March 2022 to 2 April 2022
    - Even — Commencement of classes of Even term: 28 March 2022
    - Even — In-Semester Examination (ISE): 23 May 2022 to 28 May 2022
    - Even — Dispersal of Classes of even term: 15 July 2022
    - Even — Conduct of Examinations (Oral + Theory): 18 July to 6 August 2022
    - Even — Supplementary Exam of semester II: 5 September 2022 to 16 September 2022
- [Revised Academic Calendar for FY BTECH Even Semester 2021-22](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/REVISED+EVEN+SEM_21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY B.Tech, regular students (2021-22) · marked revised
    - Odd — Commencement of classes: 11 October 2021
    - Odd — In-Semester Examination (ISE): 20 December to 23 December 2021
    - Odd — Dispersal of Classes of odd term: 4 February 2022
    - Odd — Conduct of Examinations (Oral + Theory): 7 February 2022 to 28 February 2022
    - Even — Commencement of classes of Even term (revised): 28 March 2022
    - Even — In-Semester Examination (ISE) (revised): 23 May 2022 to 28 May 2022
    - Even — Dispersal of Classes of even term (revised): 15 July 2022
    - Even — Conduct of Examinations (Oral + Theory) (revised): 18 July to 6 August 2022
    - Even — Supplementary Exam of semester II: 5 September 2022 to 12 September 2022

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q19. When does internship happen according to the 2026-27 calendar?

*What this probes:* internship rows in calendar

| | |
|---|---|
| Documents retrieved | 1 |
| Retrieval time | 20.4 ms |
| LLM time | 5.8 s |
| Markdown links in retrieval | 2 |
| Markdown links in LLM answer | 0 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': '2026-27', 'programme': None, 'level': None, 'wants_forms': False, 'wants_dates': True}` |

**KJ GPT answer (LLM):**

According to the 2026-27 academic calendar, internships for the First/Odd term are scheduled from 10 December 2026 to 3 January 2027. For the Second/Even term, internships are scheduled from 24 May 2027 to 30 June 2027.

<details><summary>Deterministic retrieval passed to the model</summary>

```
**1 official examination document(s) for 2026-27:**

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed
    - First/Odd — Commencement of Classes (SY to LY): 13 July 2026
    - First/Odd — Mid-Semester Examination (MSE): 7 September 2026 to 12 September 2026
    - First/Odd — Display of Attendance and Defaulter List up to August: 3 September 2026
    - First/Odd — Display of Attendance and Defaulter List up to September: 5 October 2026
    - First/Odd — One week Diwali Holidays for Students: 9 November to 13 November 2026
    - First/Odd — Last instructional day of First/Odd term: 4 November 2026
    - First/Odd — Submission of Theory CA, LAB/TUT CA, Term-work Marksheets: 6 November 2026
    - First/Odd — Execution of Regular ESE Examinations (Seminars + Projects + Semester Long Internships + Practical + Oral + Theory): 18 November to 8 December 2026 (3 weeks)
    - First/Odd — Internship (Wherever is applicable): 10 December 2026 to 3 January 2027
    - First/Odd — One week Christmas Holidays for Students: 24 December 2026 to 1 January 2027
    - First/Odd — Date of Declaration of Regular Examinations Results: On or before 8 January 2027
    - First/Odd — Open day: From 11 to 15 January 2027 (exact schedule notified in first week of January 2027)
    - First/Odd — Proposed Date of Declaration of results after open day of semester I, III, V and VII: On or before 30 January 2027
    - Second/Even — Commencement of Classes: 4 January 2027
    - Second/Even — Institute Level Faculty Meeting (ILFM): 4 January 2027
    - Second/Even — Mid-Semester Examination (MSE)/Test: 1 March to 6 March 2027
    - Second/Even — Last instructional day: 23 April 2027
    - Second/Even — Display of Final Attendance and Defaulter List: 26 April 2027
    - Second/Even — Submission of Theory CA, LAB/TUT CA, Term-work Marksheets: 26 April 2027
    - Second/Even — Execution of Regular ESE Examinations (Seminars + Projects + Semester Long Internships + Practical + Oral + Theory): 3 May to 21 May 2027
    - Second/Even — Internship (Wherever Applicable): 24 May 2027 to 30 June 2027
    - Second/Even — Date of Declaration of Regular Examinations Results: On or before 10 June 2027
    - Second/Even — Open day: 11 June 2027
    - Second/Even — Date of Declaration of results after open day of semester II, IV, VI, VIII: On or before 22 June 2027
    - Second/Even — Execution of Supplementary ESE Examinations: 24 June 2027 to 8 July 2027
    - Second/Even — Date of Declaration of Supplementary Examinations Results: On or before 22 July 2027
    - Second/Even — Open day of Supplementary Exam: 23 July 2027
    - Second/Even — Date of Declaration of results after open day of Supplementary Exam (semester II, IV, VI, VIII): On or before 4 August 2027
    - Second/Even — Commencement of Next Academic Year 2027-28: 1 July 2027
    - Second/Even — Convocation 2027: 18 September 2027

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---

## Q20. Give me previous year question papers for DBMS.

*What this probes:* must NOT return calendars - wrong system

| | |
|---|---|
| Documents retrieved | 16 |
| Retrieval time | 113.3 ms |
| LLM time | 1.7 s |
| Markdown links in retrieval | 17 |
| Markdown links in LLM answer | 0 |
| Fabricated example.com link | no |
| Filters | `{'academic_year': None, 'programme': None, 'level': None, 'wants_forms': False, 'wants_dates': False}` |

**KJ GPT answer (LLM):**

The available KJSIT policy information does not specify an answer to that question.

<details><summary>Deterministic retrieval passed to the model</summary>

```
**16 official examination document(s):**

- [Academic and Examination Calendar SY TY LY (B.Tech) FY SY (M.Tech) 2026-27](https://kjsce-files.somaiya.edu/Academics/AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf)
  Academic year 2026-27 · SY/TY/LY (B.Tech) and FY/SY (M.Tech) · marked proposed
- [Academic and Examination (AEC) Calendar 2023-24](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_+Uniform+AEC_SVU+KJSCE++2023-24.pdf)
  Academic year 2023-24 · FY/SY/TY/LY, all programmes (UG and PG) · marked tentative
- [Academic and Examination Calendar 2022-23- SY, TY, LY and FY](https://kjsce-files.somaiya.edu/Exam/Calendar/526_COE_KJSCE__Academic+and+Examination+Calendar+AEC-2022-23.pdf)
  Academic year 2022-23 · Separate templates for SY B.Tech, SY M.Tech, TY B.Tech, LY B.Tech (KJSCE 2018) and FY B.Tech
- [Academic and Examination Calendar for FY B TECH  2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+B.TECH_+Academic+and+Examination+Calendar.pdf)
  Academic year 2021-22 · FY B.Tech
- [Academic and Examination Calendar for FY FY M TECH 2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/21-22_FY+M.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY M.Tech
- [Academic and Examination Calendar for Newly admitted  Batch ( 26 Nov and onwards)  to FY BTECH -2021](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/FOR+NEW+BATCH__21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY B.Tech, newly admitted students only (admitted November 2021 and onwards)
- [Revised Academic Calendar for FY BTECH Even Semester 2021-22](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/REVISED+EVEN+SEM_21-22_FY+B.TECH_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · FY B.Tech, regular students (2021-22) · marked revised
- [Revised Academic and Examination Calendar for DSY SEM III](https://kjsce-files.somaiya.edu/Exam/SVU_Notices/Revised+Academic+and+Examination+Calendar+DSY+2021-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020) Sem IV, and Sem III for Direct Second Year (DSY) admitted students only · marked revised
- [SY B.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+B.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · SY B.Tech (SVU 2020)
- [SY M.TECH (SVU-2020)_ Academic and Examination Calendar 21-22](https://kjsce-files.somaiya.edu/Exam/Calendar/SY+M.TECH+(SVU-2020)_+Academic+and+Examination+Calendar+21-22.pdf)
  Academic year 2021-22 · SY M.Tech (SVU 2020)
- [TY-LY  Academic and Examination Calendar 2021-22](https://kjsce-files.somaiya.edu/Exam/Calendar/TY-LY+_+Academic+and+Examination+Calendar+2021-22.pdf)
  Academic year 2021-22 · TY/LY B.Tech
- [FY B.TECH -Academic and Examination calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+B.TECH_+Academic+and+Examination+Calendar+20-21.pdf)
  Academic year 2020-21 · FY B.Tech, for students admitted to college till October 2020
- [FY.M.TECH -Academic and Examination calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/85COE_FY+M.TECH_+Academic+and+Examination+Calendar+20-21.pdf)
  Academic year 2020-21 · FY M.Tech
- [Odd Term/Semester UG and PG FY -SVU 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar_FY+BTECH+and+MTECH.pdf)
  Academic year 2020-21 · FY B.Tech Semester I and FY M.Tech Semester I · marked tentative
- [Odd Term/Semester UG and PG SY/TY/LY 2020-21](https://kjsce-files.somaiya.edu/Exam/Calendar/Examination+Calendar+-+UG-SY-TY+and+PG+SEM+III.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech Semesters III, V and VII and M.Tech Sem III (regular); plus FY/SY/TY/LY B.Tech Semesters I-VI and M.Tech Sem I (backlog/KT)
- [SY/TY/LY B. Tech/M. Tech Academic and Examination Calendar](https://kjsce-files.somaiya.edu/Exam/Calendar/SY-LY+_+Academic+and+Examination+Calendar_Modified.pdf)
  Academic year 2020-21 · SY/TY/LY B.Tech and M.Tech

Source: [KJSCE official documents page](https://kjsce.somaiya.edu/en/documents/) (Examination section).
```

</details>

---


---

## Verdict

| Result | Count |
|---|---|
| PASS | **18** |
| PASS* | **1** |
| PARTIAL | **1** |

| Q | Verdict | Notes |
|---|---|---|
| 1 | PASS | Listed all 16 with the official documents-page link. |
| 2 | PASS* | All 16 listed with links. *Renderer caveat below. |
| 3 | PASS | Stated the Download Forms section publishes nothing and returns 'No Data Found.' - no invention. |
| 4 | PASS | Returned only the 2026-27 AEC. |
| 5 | PASS | Returned only the 2023-24 AEC. |
| 6 | PASS | 13 B.Tech documents, correctly excluding M.Tech-only calendars. |
| 7 | PASS | 9 M.Tech-relevant documents. |
| 8 | PASS | Odd 18 Nov-8 Dec 2026, Even 3 May-21 May 2027 - exact match to the scanned PDF. |
| 9 | PASS | Odd 7-12 Sep 2026, Even 1-6 Mar 2027 - exact. |
| 10 | PASS | On or before 8 Jan 2027 / 10 Jun 2027 - exact. |
| 11 | PASS | Correctly reported the calendar as 'proposed', not final. |
| 12 | PASS | 9-13 Nov 2026 - exact. |
| 13 | PASS | Found the DSY SEM III calendar - the one buried in a scanned PDF. |
| 14 | PASS | Last week of July 2022 - exact. |
| 15 | PASS | Refused: no 2019-20 document held. |
| 16 | PASS | Refused: no 2030-31 document held. |
| 17 | PASS | Reported online mode and paper pattern from the 2020-21 COVID calendars. |
| 18 | PARTIAL | Picked the revised regular-student calendar and linked it correctly, but did not mention that a second calendar issued the same day covers students admitted from Nov 2021. The student did not say which batch they are in. |
| 19 | PASS | 10 Dec 2026-3 Jan 2027 and 24 May-30 Jun 2027 - exact. |
| 20 | PASS | Refused. Retrieval over-returned 16 calendars, but the grounding rules stopped the model presenting calendars as question papers. |

### Link integrity

- **0** fabricated links across 20 answers (no `example.com`, no invented URL).
- **0** bare URLs - every URL the model emitted was inside a Markdown link.
- **28** Markdown links emitted; every destination byte-identical to the URL stored in Neo4j.

### One real bug found and fixed during this test

Three of the sixteen official URLs contain literal parentheses, e.g.
`.../AEC_SY_TY_LY_(B.Tech)_FY_SY_(M.Tech)_2026_27.pdf`. Written the plain Markdown way,
`[title](https://...(B.Tech)...pdf)`, a CommonMark renderer ends the destination at the first
unescaped `)` - so the link resolved to `.../AEC_SY_TY_LY_(B.Tech` and would 404 for the student.
The URL stored in Neo4j was always correct; only the rendering was broken.

Fixed in `services/exam_document_service.md_link()`: a destination containing `(`, `)`, space or
angle brackets is wrapped as `[title](<url>)`, which is the CommonMark form. After the fix all
**17/17** links in the deterministic answer resolve to the exact official URL.

### Known remaining weakness

On a re-test the model copied the corrected `(<...>)` form on 3 of 4 questions. On
*"Show me all the examination calendars"* - a single answer containing 17 links - Qwen3 8B
dropped the angle brackets on the three parenthesised URLs, re-breaking them. The deterministic
route (`POST /exam/documents/ask`, what production serves) is unaffected and always correct;
this only affects an LLM-reworded long list. Adding the angle-bracket case to the LINK HANDLING
rule in the stored prompt would likely close it, but that edits a shared prompt and was not done
as part of a test run.

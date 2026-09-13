# KJGPT PYQ — 20-question Drive-link run

- Started: `2026-09-13T06:28:34+00:00`
- Model: `qwen3:8b` (thinking off)
- Papers in graph: **164** (ISE 164, ESE 0)
- Year window enforced: **2019-2025**
- Progress: **20/20** — 15 passed, 0 failed, 5 blocked

`retrieval` is question → filters → Neo4j → links, with no model call. `qwen` is the extra time for Qwen3 8B to reword that same list; it never invents or edits a URL.

> **Note** — no ESE papers are in the graph yet: ingesting them needs `service_account.json`, which is missing. ESE questions below therefore return an honest empty answer. Every ISE result and every link check is real.

## Summary

| # | Category | Question | Papers | Types | Retrieval | Qwen | Result |
|---|---|---|---|---:|---|---:|---:|
| 1 | A. default rule | Give me all OS papers | 5 | ISE | 23ms | 20.0s | PASS |
| 2 | B. exam filter | Give me ISE OS papers | 5 | ISE | 58ms | 19.0s | PASS |
| 3 | C. exam filter | Give me ESE OS papers | 0 | — | 93ms | — | BLOCKED |
| 4 | D. default rule | Give me all DBMS papers from 2022 | 1 | ISE | 6ms | 5.2s | PASS |
| 5 | E. exam + year | Give me ESE DBMS 2024 paper | 0 | — | 39ms | — | BLOCKED |
| 6 | F. exam only | Give me all ESE papers | 0 | — | 6ms | — | BLOCKED |
| 7 | G. year range | Give me all papers from 2019 to 2025 | 50 | ISE | 11ms | 61.9s | PASS |
| 8 | link | give me Computer Networks paper | 4 | ISE | 70ms | 16.3s | PASS |
| 9 | link | give me PSOT paper 2021-22 | 3 | ISE | 40ms | 5.6s | PASS |
| 10 | link | give me TACD paper | 3 | ISE | 48ms | 13.9s | PASS |
| 11 | year window | give me OS papers from 2018 | 0 | — | 262ms | — | PASS |
| 12 | year window | give me DBMS paper 2019 | 0 | — | 4ms | — | PASS |
| 13 | year window | give me papers from 2025 | 45 | ISE | 19ms | 59.4s | PASS |
| 14 | subject | give me rdbms paper | 5 | ISE | 72ms | 19.4s | PASS |
| 15 | subject | operating system previous year papers | 5 | ISE | 107ms | 17.8s | PASS |
| 16 | subject | give me ITVC paper | 4 | ISE | 57ms | 15.1s | PASS |
| 17 | bundle | give me ESE sem 5 papers | 0 | — | 1222ms | — | BLOCKED |
| 18 | bundle | give me ESE Machine Learning papers | 0 | — | 10ms | — | BLOCKED |
| 19 | miss | give me organic chemistry paper | 0 | — | 0ms | — | PASS |
| 20 | miss | give me all papers | 0 | — | 0ms | — | PASS |

## Detail

### 1. Give me all OS papers

*No exam type named -> must return BOTH ISE and ESE.*

- Category: `A. default rule` · Result: **PASS**
- Filters: `{'subject_key': 'os'}`
- Papers: **5** · Retrieval: 23ms · Qwen: 20.0s

| Link check | Result | Detail |
|---|---|---|
| every link is a Google Drive URL | PASS | 5/5 |
| no link points at a folder | PASS | 0 folder link(s) |
| links are file-level /file/d/<id> | PASS | 5/5 |
| every paper is 2019-2025 | PASS | 0 outside |
| no duplicate link in one answer | PASS | 5 unique of 5 |

**Papers returned**

| # | Title | Exam | Year | Sem | Drive link |
|---|---|---|---:|---:|---|
| 1 | Operating Systems — ISE, Sem IV, 2024-25 | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/1nvwBQjFgEpnEsXat2rPRWtstOeasUmIJ/view?usp=drivesdk) |
| 2 | Operating Systems — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk) |
| 3 | Operating Systems — ISE, Sem V, 2024-25, Minor | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk) |
| 4 | Operating Systems — ISE, Sem V, 2023-24 | ISE | 2023 | 5 | [open](https://drive.google.com/file/d/1XGYyCyVJWWpeqKWmoMCRjargjs9kqqUd/view?usp=drivesdk) |
| 5 | Operating Systems — ISE, Sem V, 2023-24, Minor | ISE | 2023 | 5 | [open](https://drive.google.com/file/d/18_GHVAMFUg5l8kdg12fSIe4lImGa5xA3/view?usp=drivesdk) |

<details><summary>Raw URLs</summary>

1. `https://drive.google.com/file/d/1nvwBQjFgEpnEsXat2rPRWtstOeasUmIJ/view?usp=drivesdk`
2. `https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk`
3. `https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk`
4. `https://drive.google.com/file/d/1XGYyCyVJWWpeqKWmoMCRjargjs9kqqUd/view?usp=drivesdk`
5. `https://drive.google.com/file/d/18_GHVAMFUg5l8kdg12fSIe4lImGa5xA3/view?usp=drivesdk`

</details>

**Qwen3 8B answer**

```text
- Operating Systems — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1nvwBQjFgEpnEsXat2rPRWtstOeasUmIJ/view?usp=drivesdk  
- Operating Systems — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk  
- Operating Systems — ISE, Sem V, 2024-25, Minor  
  https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk  
- Operating Systems — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1XGYyCyVJWWpeqKWmoMCRjargjs9kqqUd/view?usp=drivesdk  
- Operating Systems — ISE, Sem V, 2023-24, Minor  
  https://drive.google.com/file/d/18_GHVAMFUg5l8kdg12fSIe4lImGa5xA3/view?usp=drivesdk
```

---

### 2. Give me ISE OS papers

*Explicit ISE -> ISE only, a strict subset of A.*

- Category: `B. exam filter` · Result: **PASS**
- Filters: `{'subject_key': 'os', 'exam_type': 'ISE'}`
- Papers: **5** · Retrieval: 58ms · Qwen: 19.0s

| Link check | Result | Detail |
|---|---|---|
| every link is a Google Drive URL | PASS | 5/5 |
| no link points at a folder | PASS | 0 folder link(s) |
| links are file-level /file/d/<id> | PASS | 5/5 |
| every paper is 2019-2025 | PASS | 0 outside |
| no duplicate link in one answer | PASS | 5 unique of 5 |

**Papers returned**

| # | Title | Exam | Year | Sem | Drive link |
|---|---|---|---:|---:|---|
| 1 | Operating Systems — ISE, Sem IV, 2024-25 | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/1nvwBQjFgEpnEsXat2rPRWtstOeasUmIJ/view?usp=drivesdk) |
| 2 | Operating Systems — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk) |
| 3 | Operating Systems — ISE, Sem V, 2024-25, Minor | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk) |
| 4 | Operating Systems — ISE, Sem V, 2023-24 | ISE | 2023 | 5 | [open](https://drive.google.com/file/d/1XGYyCyVJWWpeqKWmoMCRjargjs9kqqUd/view?usp=drivesdk) |
| 5 | Operating Systems — ISE, Sem V, 2023-24, Minor | ISE | 2023 | 5 | [open](https://drive.google.com/file/d/18_GHVAMFUg5l8kdg12fSIe4lImGa5xA3/view?usp=drivesdk) |

<details><summary>Raw URLs</summary>

1. `https://drive.google.com/file/d/1nvwBQjFgEpnEsXat2rPRWtstOeasUmIJ/view?usp=drivesdk`
2. `https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk`
3. `https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk`
4. `https://drive.google.com/file/d/1XGYyCyVJWWpeqKWmoMCRjargjs9kqqUd/view?usp=drivesdk`
5. `https://drive.google.com/file/d/18_GHVAMFUg5l8kdg12fSIe4lImGa5xA3/view?usp=drivesdk`

</details>

**Qwen3 8B answer**

```text
- Operating Systems — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1nvwBQjFgEpnEsXat2rPRWtstOeasUmIJ/view?usp=drivesdk  
- Operating Systems — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk  
- Operating Systems — ISE, Sem V, 2024-25, Minor  
  https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk  
- Operating Systems — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1XGYyCyVJWWpeqKWmoMCRjargjs9kqqUd/view?usp=drivesdk  
- Operating Systems — ISE, Sem V, 2023-24, Minor  
  https://drive.google.com/file/d/18_GHVAMFUg5l8kdg12fSIe4lImGa5xA3/view?usp=drivesdk
```

---

### 3. Give me ESE OS papers

*Explicit ESE -> ESE only.*

- Category: `C. exam filter` · Result: **BLOCKED**
- Filters: `{'subject_key': 'os', 'exam_type': 'ESE'}`
- Papers: **0** · Retrieval: 93ms

| Link check | Result | Detail |
|---|---|---|
| returned nothing | PASS | ESE not ingested yet -- cannot be judged |

**No papers returned** — reason: `no_match`

---

### 4. Give me all DBMS papers from 2022

*Year named, exam type not -> both types, 2022 only.*

- Category: `D. default rule` · Result: **PASS**
- Filters: `{'subject_key': 'dbms', 'year': 2022}`
- Papers: **1** · Retrieval: 6ms · Qwen: 5.2s

| Link check | Result | Detail |
|---|---|---|
| every link is a Google Drive URL | PASS | 1/1 |
| no link points at a folder | PASS | 0 folder link(s) |
| links are file-level /file/d/<id> | PASS | 1/1 |
| every paper is 2019-2025 | PASS | 0 outside |
| no duplicate link in one answer | PASS | 1 unique of 1 |

**Papers returned**

| # | Title | Exam | Year | Sem | Drive link |
|---|---|---|---:|---:|---|
| 1 | Database Management System — ISE, Sem IV, 2021-22 | ISE | 2022 | 4 | [open](https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk) |

<details><summary>Raw URLs</summary>

1. `https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk`

</details>

**Qwen3 8B answer**

```text
1 matching question paper(s) for DBMS, 2022:
- Database Management System — ISE, Sem IV, 2021-22
  https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk
```

---

### 5. Give me ESE DBMS 2024 paper

*Narrowest shape: one subject, one type, one year.*

- Category: `E. exam + year` · Result: **BLOCKED**
- Filters: `{'subject_key': 'dbms', 'exam_type': 'ESE', 'year': 2024}`
- Papers: **0** · Retrieval: 39ms

| Link check | Result | Detail |
|---|---|---|
| returned nothing | PASS | ESE not ingested yet -- cannot be judged |

**No papers returned** — reason: `no_match`

---

### 6. Give me all ESE papers

*Every mapped ESE paper, 2019-2025.*

- Category: `F. exam only` · Result: **BLOCKED**
- Filters: `{'exam_type': 'ESE'}`
- Papers: **0** · Retrieval: 6ms

| Link check | Result | Detail |
|---|---|---|
| returned nothing | PASS | ESE not ingested yet -- cannot be judged |

**No papers returned** — reason: `no_match`

---

### 7. Give me all papers from 2019 to 2025

*Both exam types across the whole allowed window.*

- Category: `G. year range` · Result: **PASS**
- Filters: `{'year_min': 2019, 'year_max': 2025}`
- Papers: **50** · Retrieval: 11ms · Qwen: 61.9s

| Link check | Result | Detail |
|---|---|---|
| every link is a Google Drive URL | PASS | 50/50 |
| no link points at a folder | PASS | 0 folder link(s) |
| links are file-level /file/d/<id> | PASS | 50/50 |
| every paper is 2019-2025 | PASS | 0 outside |
| no duplicate link in one answer | PASS | 50 unique of 50 |

**Papers returned**

| # | Title | Exam | Year | Sem | Drive link |
|---|---|---|---:|---:|---|
| 1 | Analysis of Algorithms — ISE, Sem IV, 2024-25 | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/1zfkQGgPBUp81cqW-HLGzWsqIqDCcKcTh/view?usp=drivesdk) |
| 2 | Applied Cryptography — ISE, Sem IV, 2024-25, Honours | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/1XiYynz9lMTs8abrWw0lyeJXKUDm3TUTh/view?usp=drivesdk) |
| 3 | Applied Cryptography — ISE, Sem VI, 2024-25 | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1loFGIh56qKC3ZOAJDeietJ-gR0kGgbp7/view?usp=drivesdk) |
| 4 | Artificial Intelligence — ISE, Sem VI, 2024-25 | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1djTOaEfjT43TP26QJTzE4M5ypBWSEkFI/view?usp=drivesdk) |
| 5 | Cloud Computing — ISE, Sem VI, 2024-25 | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1q_ItzuW7iJcz1o98BlcX1H-OyDPeDmiV/view?usp=drivesdk) |
| 6 | Database Management System — ISE, Sem IV, 2024-25 | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/1LzMSNrHgqFj_4_2VQ45iqxe1Q5b30_mp/view?usp=drivesdk) |
| 7 | Digital Signal and Image Processing — ISE, Sem VI, 2024-25 | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1FlICjdxr_xphPKJ4vWVzVJv9QoR3woxW/view?usp=drivesdk) |
| 8 | German — ISE, Sem VI, 2024-25, Open Elective | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1_I6sg3SeRQjgZM4o_ValkyCPhIw6U9B3/view?usp=drivesdk) |
| 9 | Information Security — ISE, Sem VI, 2024-25 | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1jGjfmjNB_O7yNd4npYJ_UZmarL6bDi7J/view?usp=drivesdk) |
| 10 | Natural Language Processing — ISE, Sem VIII, 2024-25 | ISE | 2025 | 8 | [open](https://drive.google.com/file/d/1R4_wQP0i96f1Psq46myyfkHVcYqjt1VX/view?usp=drivesdk) |
| 11 | Operating Systems — ISE, Sem IV, 2024-25 | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/1nvwBQjFgEpnEsXat2rPRWtstOeasUmIJ/view?usp=drivesdk) |
| 12 | Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2024-25 | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/1LFmiF68LjxVstlJhUjSQxHXg3ooY9Ja7/view?usp=drivesdk) |
| 13 | AADA — ISE, Sem VIII, 2024-25 | ISE | 2025 | 8 | [open](https://drive.google.com/file/d/129Rz3r4gqWcRrkl0zpBV9wMb2TINX2uS/view?usp=drivesdk) |
| 14 | ADM — ISE, Sem VI, 2024-25, Honours | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1SCRFmBTSvH7eLLICTua5OXdKxwxelG70/view?usp=drivesdk) |
| 15 | AMLT — ISE, Sem VI, 2024-25, Open Elective | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1n_tezzisr_cnEtWnzz_x4d5GB0id4hZm/view?usp=drivesdk) |
| 16 | IDS — ISE, Sem IV, 2024-25, Honours | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/14cCFjXcSosmRm14kc76iSdkox7w329H_/view?usp=drivesdk) |
| 17 | IOE — ISE, Sem VIII, 2024-25 | ISE | 2025 | 8 | [open](https://drive.google.com/file/d/1rKjRTN5Sjau0M0jhwMewmkB2dPvcQJ8O/view?usp=drivesdk) |
| 18 | VAPT — ISE, Sem VI, 2024-25, Honours | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1nAAuXCOjRdeRJwpAyHBP0wxVaZaMW1wK/view?usp=drivesdk) |
| 19 | Analysis of Algorithms — ISE, Sem IV, 2023-24 | ISE | 2024 | 4 | [open](https://drive.google.com/file/d/1es15Evap777oz4GSV4FjfHEnhVctESMe/view?usp=drivesdk) |
| 20 | Computer Graphics — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/13cWmT80KIZB7TDXTUm4yB7xOPmsBy1Ea/view?usp=drivesdk) |
| 21 | Computer Organization and Architecture — ISE, Sem III, 2024-25 | ISE | 2024 | 3 | [open](https://drive.google.com/file/d/12h39hSO32TTi4ZlCbz6iXtAEJ67IHu2w/view?usp=drivesdk) |
| 22 | Data Analytics — ISE, Sem V, 2024-25, Honours | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/15nW5d2D5y5PJSzRJHXWfMnKebF9QiVhP/view?usp=drivesdk) |
| 23 | Data Structures — ISE, Sem III, 2024-25 | ISE | 2024 | 3 | [open](https://drive.google.com/file/d/1CInufaTvXi8HMs4Bfll5o1DefG3uTdlt/view?usp=drivesdk) |
| 24 | Data Structures — ISE, Sem VII, 2024-25 | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1ujXpfqYUdtRvIxsrVfwPrlnvhDy1R_lb/view?usp=drivesdk) |
| 25 | Database Management System — ISE, Sem IV, 2023-24 | ISE | 2024 | 4 | [open](https://drive.google.com/file/d/1PHe3j7OCb63hnFQf4MIguMNoDyAkrf3f/view?usp=drivesdk) |
| 26 | Machine Learning — ISE, 2023-24 | ISE | 2024 | — | [open](https://drive.google.com/file/d/1oGH0iPsEkLTTIsBTGjtzEkKYzou0klxh/view?usp=drivesdk) |
| 27 | Object Oriented Programming Methodology — ISE, Sem III, 2024-25 | ISE | 2024 | 3 | [open](https://drive.google.com/file/d/122cc57KTEy97xYZmDznGcneLwTZem8AV/view?usp=drivesdk) |
| 28 | Object Oriented Programming Methodology — ISE, Sem IV, 2023-24, Minor | ISE | 2024 | 4 | [open](https://drive.google.com/file/d/1CLtG6wUXMT8YdAjqgXELgdgeYP0DeLaO/view?usp=drivesdk) |
| 29 | Operating Systems — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk) |
| 30 | Operating Systems — ISE, Sem V, 2024-25, Minor | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk) |
| 31 | Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2023-24 | ISE | 2024 | 4 | [open](https://drive.google.com/file/d/1P8WD2PDrJ5mRyLgNdbgkZRIp47hPg9uk/view?usp=drivesdk) |
| 32 | Soft Computing — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/1y96qSCajVf4AJa8-XEqOGLkEuYNbzR6s/view?usp=drivesdk) |
| 33 | Supply Chain Management — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/1Lo-YYH5BoDnopypRMNKKMAoR9nXPvG1L/view?usp=drivesdk) |
| 34 | Theory of Automata and Compiler Design — ISE, Sem IV, 2023-24 | ISE | 2024 | 4 | [open](https://drive.google.com/file/d/1bqzzNVLOGcEYIw-uzpGpxVkBncwdDSYF/view?usp=drivesdk) |
| 35 | User Experience Design — ISE, Sem VII, 2024-25 | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1dtwCbJcDn5m5gjQxZpc_Adr11HxkQQ3T/view?usp=drivesdk) |
| 36 | Web Programming — ISE, Sem VII, 2024-25, Minor | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/19tFxqsuJNXWFAwz-dMuIbna8RAXxjt_K/view?usp=drivesdk) |
| 37 | ADS — ISE, Sem IV, 2023-24, Honours | ISE | 2024 | 4 | [open](https://drive.google.com/file/d/1h_A7iLrSiQUBSeVpU8SwKgsGa_ualnNb/view?usp=drivesdk) |
| 38 | AML — ISE, Sem VII, 2024-25, Honours | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1BEjIWBcUE2uD1LmPxtXjB4AVbYids_Gj/view?usp=drivesdk) |
| 39 | APM — ISE, Sem VII, 2024-25 | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1FJmeo2rAMC_PaKt5aNbdsAjnaYJWLjH9/view?usp=drivesdk) |
| 40 | BCT — ISE, Sem VII, 2024-25 | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1qyHUhixRZY3xkCcwVMR6sSNNIHF1qvDx/view?usp=drivesdk) |
| 41 | BCT — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/1dPEZrRsNekZ5k5HazrQ6QutPYD8SCsbt/view?usp=drivesdk) |
| 42 | C# — ISE, Sem VII, 2024-25 | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1TPJ4M5hdaWQaA4I9zkyCdMYfbkg8NRfE/view?usp=drivesdk) |
| 43 | CSFC — ISE, Sem IV, 2023-24, Honours | ISE | 2024 | 4 | [open](https://drive.google.com/file/d/1XWlrsMKIj-KOWZ7EKp9_Iy6SoYakPk8V/view?usp=drivesdk) |
| 44 | CSM — ISE, Sem VII, 2024-25 | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/14SCvLh5s5GwyaPJknvvEzXxOtkCSfrhB/view?usp=drivesdk) |
| 45 | DL — ISE, Sem VII, 2024-25, Minor | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1gruFNmOp2y7tM9GYRa9eS07r_ew0AsKm/view?usp=drivesdk) |
| 46 | DSM — ISE, Sem III, 2024-25 | ISE | 2024 | 3 | [open](https://drive.google.com/file/d/1KsiZGSTwRCl1dEtoD1MUZPG9xSlk5q_1/view?usp=drivesdk) |
| 47 | EEFM — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/1bW486S2-QZvu9x5oBkEfOHNZyKVib23c/view?usp=drivesdk) |
| 48 | FUTTER — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/1sgpB-n4ZpajoLUCfHOSqI9a4L7CwMrJd/view?usp=drivesdk) |
| 49 | IMCT — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/1MBA0y_Fpm4nxDbrB7QPbWXbAwrUIqxa6/view?usp=drivesdk) |
| 50 | ITVC — ISE, Sem III, 2024-25 | ISE | 2024 | 3 | [open](https://drive.google.com/file/d/1SezKMUGyrPn6-aUdPhnWjgnLyan-IXwE/view?usp=drivesdk) |

<details><summary>Raw URLs</summary>

1. `https://drive.google.com/file/d/1zfkQGgPBUp81cqW-HLGzWsqIqDCcKcTh/view?usp=drivesdk`
2. `https://drive.google.com/file/d/1XiYynz9lMTs8abrWw0lyeJXKUDm3TUTh/view?usp=drivesdk`
3. `https://drive.google.com/file/d/1loFGIh56qKC3ZOAJDeietJ-gR0kGgbp7/view?usp=drivesdk`
4. `https://drive.google.com/file/d/1djTOaEfjT43TP26QJTzE4M5ypBWSEkFI/view?usp=drivesdk`
5. `https://drive.google.com/file/d/1q_ItzuW7iJcz1o98BlcX1H-OyDPeDmiV/view?usp=drivesdk`
6. `https://drive.google.com/file/d/1LzMSNrHgqFj_4_2VQ45iqxe1Q5b30_mp/view?usp=drivesdk`
7. `https://drive.google.com/file/d/1FlICjdxr_xphPKJ4vWVzVJv9QoR3woxW/view?usp=drivesdk`
8. `https://drive.google.com/file/d/1_I6sg3SeRQjgZM4o_ValkyCPhIw6U9B3/view?usp=drivesdk`
9. `https://drive.google.com/file/d/1jGjfmjNB_O7yNd4npYJ_UZmarL6bDi7J/view?usp=drivesdk`
10. `https://drive.google.com/file/d/1R4_wQP0i96f1Psq46myyfkHVcYqjt1VX/view?usp=drivesdk`
11. `https://drive.google.com/file/d/1nvwBQjFgEpnEsXat2rPRWtstOeasUmIJ/view?usp=drivesdk`
12. `https://drive.google.com/file/d/1LFmiF68LjxVstlJhUjSQxHXg3ooY9Ja7/view?usp=drivesdk`
13. `https://drive.google.com/file/d/129Rz3r4gqWcRrkl0zpBV9wMb2TINX2uS/view?usp=drivesdk`
14. `https://drive.google.com/file/d/1SCRFmBTSvH7eLLICTua5OXdKxwxelG70/view?usp=drivesdk`
15. `https://drive.google.com/file/d/1n_tezzisr_cnEtWnzz_x4d5GB0id4hZm/view?usp=drivesdk`
16. `https://drive.google.com/file/d/14cCFjXcSosmRm14kc76iSdkox7w329H_/view?usp=drivesdk`
17. `https://drive.google.com/file/d/1rKjRTN5Sjau0M0jhwMewmkB2dPvcQJ8O/view?usp=drivesdk`
18. `https://drive.google.com/file/d/1nAAuXCOjRdeRJwpAyHBP0wxVaZaMW1wK/view?usp=drivesdk`
19. `https://drive.google.com/file/d/1es15Evap777oz4GSV4FjfHEnhVctESMe/view?usp=drivesdk`
20. `https://drive.google.com/file/d/13cWmT80KIZB7TDXTUm4yB7xOPmsBy1Ea/view?usp=drivesdk`
21. `https://drive.google.com/file/d/12h39hSO32TTi4ZlCbz6iXtAEJ67IHu2w/view?usp=drivesdk`
22. `https://drive.google.com/file/d/15nW5d2D5y5PJSzRJHXWfMnKebF9QiVhP/view?usp=drivesdk`
23. `https://drive.google.com/file/d/1CInufaTvXi8HMs4Bfll5o1DefG3uTdlt/view?usp=drivesdk`
24. `https://drive.google.com/file/d/1ujXpfqYUdtRvIxsrVfwPrlnvhDy1R_lb/view?usp=drivesdk`
25. `https://drive.google.com/file/d/1PHe3j7OCb63hnFQf4MIguMNoDyAkrf3f/view?usp=drivesdk`
26. `https://drive.google.com/file/d/1oGH0iPsEkLTTIsBTGjtzEkKYzou0klxh/view?usp=drivesdk`
27. `https://drive.google.com/file/d/122cc57KTEy97xYZmDznGcneLwTZem8AV/view?usp=drivesdk`
28. `https://drive.google.com/file/d/1CLtG6wUXMT8YdAjqgXELgdgeYP0DeLaO/view?usp=drivesdk`
29. `https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk`
30. `https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk`
31. `https://drive.google.com/file/d/1P8WD2PDrJ5mRyLgNdbgkZRIp47hPg9uk/view?usp=drivesdk`
32. `https://drive.google.com/file/d/1y96qSCajVf4AJa8-XEqOGLkEuYNbzR6s/view?usp=drivesdk`
33. `https://drive.google.com/file/d/1Lo-YYH5BoDnopypRMNKKMAoR9nXPvG1L/view?usp=drivesdk`
34. `https://drive.google.com/file/d/1bqzzNVLOGcEYIw-uzpGpxVkBncwdDSYF/view?usp=drivesdk`
35. `https://drive.google.com/file/d/1dtwCbJcDn5m5gjQxZpc_Adr11HxkQQ3T/view?usp=drivesdk`
36. `https://drive.google.com/file/d/19tFxqsuJNXWFAwz-dMuIbna8RAXxjt_K/view?usp=drivesdk`
37. `https://drive.google.com/file/d/1h_A7iLrSiQUBSeVpU8SwKgsGa_ualnNb/view?usp=drivesdk`
38. `https://drive.google.com/file/d/1BEjIWBcUE2uD1LmPxtXjB4AVbYids_Gj/view?usp=drivesdk`
39. `https://drive.google.com/file/d/1FJmeo2rAMC_PaKt5aNbdsAjnaYJWLjH9/view?usp=drivesdk`
40. `https://drive.google.com/file/d/1qyHUhixRZY3xkCcwVMR6sSNNIHF1qvDx/view?usp=drivesdk`
41. `https://drive.google.com/file/d/1dPEZrRsNekZ5k5HazrQ6QutPYD8SCsbt/view?usp=drivesdk`
42. `https://drive.google.com/file/d/1TPJ4M5hdaWQaA4I9zkyCdMYfbkg8NRfE/view?usp=drivesdk`
43. `https://drive.google.com/file/d/1XWlrsMKIj-KOWZ7EKp9_Iy6SoYakPk8V/view?usp=drivesdk`
44. `https://drive.google.com/file/d/14SCvLh5s5GwyaPJknvvEzXxOtkCSfrhB/view?usp=drivesdk`
45. `https://drive.google.com/file/d/1gruFNmOp2y7tM9GYRa9eS07r_ew0AsKm/view?usp=drivesdk`
46. `https://drive.google.com/file/d/1KsiZGSTwRCl1dEtoD1MUZPG9xSlk5q_1/view?usp=drivesdk`
47. `https://drive.google.com/file/d/1bW486S2-QZvu9x5oBkEfOHNZyKVib23c/view?usp=drivesdk`
48. `https://drive.google.com/file/d/1sgpB-n4ZpajoLUCfHOSqI9a4L7CwMrJd/view?usp=drivesdk`
49. `https://drive.google.com/file/d/1MBA0y_Fpm4nxDbrB7QPbWXbAwrUIqxa6/view?usp=drivesdk`
50. `https://drive.google.com/file/d/1SezKMUGyrPn6-aUdPhnWjgnLyan-IXwE/view?usp=drivesdk`

</details>

**Qwen3 8B answer**

```text
- Analysis of Algorithms — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1zfkQGgPBUp81cqW-HLGzWsqIqDCcKcTh/view?usp=drivesdk  
- Applied Cryptography — ISE, Sem IV, 2024-25, Honours  
  https://drive.google.com/file/d/1XiYynz9lMTs8abrWw0lyeJXKUDm3TUTh/view?usp=drivesdk  
- Applied Cryptography — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1loFGIh56qKC3ZOAJDeietJ-gR0kGgbp7/view?usp=drivesdk  
- Artificial Intelligence — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1djTOaEfjT43TP26QJTzE4M5ypBWSEkFI/view?usp=drivesdk  
- Cloud Computing — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1q_ItzuW7iJcz1o98BlcX1H-OyDPeDmiV/view?usp=drivesdk  
- Database Management System — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1LzMSNrHgqFj_4_2VQ45iqxe1Q5b30_mp/view?usp=drivesdk  
- Digital Signal and Image Processing — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1FlICjdxr_xphPKJ4vWVzVJv9QoR3woxW/view?usp=drivesdk  
- German — ISE, Sem VI, 2024-25, Open Elective  
  https://drive.google.com/file/d/1_I6sg3SeRQjgZM4o_ValkyCPhIw6U9B3/view?usp=drivesdk  
- Information Security — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1jGjfmjNB_O7yNd4npYJ_UZmarL6bDi7J/view?usp=drivesdk  
- Natural Language Processing — ISE, Sem VIII, 2024-25  
  https://drive.google.com/file/d/1R4_wQP0i96f1Psq46myyfkHVcYqjt1VX/view?usp=drivesdk  
- Operating Systems — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1nvwBQjFgEpnEsXat2rPRWtstOeasUmIJ/view?usp=drivesdk  
- Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1LFmiF68LjxVstlJhUjSQxHXg3ooY9Ja7/view?usp=drivesdk  
- AADA — ISE, Sem VIII, 2024-25  
  https://drive.google.com/file/d/129Rz3r4gqWcRrkl0zpBV9wMb2TINX2uS/view?usp=drivesdk  
- ADM — ISE, Sem VI, 2024-25, Honours  
  https://drive.google.com/file/d/1SCRFmBTSvH7eLLICTua5OXdKxwxelG70/view?usp=drivesdk  
- AMLT — ISE, Sem VI, 2024-25, Open Elective  
  https://drive.google.com/file/d/1n_tezzisr_cnEtWnzz_x4d5GB0id4hZm/view?usp=drivesdk  
... and 35 more not listed here.
```

---

### 8. give me Computer Networks paper

*Every row must carry a file-level /file/d/<id>/view URL.*

- Category: `link` · Result: **PASS**
- Filters: `{'subject_key': 'cn'}`
- Papers: **4** · Retrieval: 70ms · Qwen: 16.3s

| Link check | Result | Detail |
|---|---|---|
| every link is a Google Drive URL | PASS | 4/4 |
| no link points at a folder | PASS | 0 folder link(s) |
| links are file-level /file/d/<id> | PASS | 4/4 |
| every paper is 2019-2025 | PASS | 0 outside |
| no duplicate link in one answer | PASS | 4 unique of 4 |

**Papers returned**

| # | Title | Exam | Year | Sem | Drive link |
|---|---|---|---:|---:|---|
| 1 | Computer Networks — ISE, Sem V, 2023-24 | ISE | 2023 | 5 | [open](https://drive.google.com/file/d/1DfjeKjMKXLoJmVuR2b7kV_bpjb3hBxAG/view?usp=drivesdk) |
| 2 | Computer Networks — ISE, Sem V, 2021-22, PwD | ISE | 2021 | 5 | [open](https://drive.google.com/file/d/1h5DHpnsY9XQZJF5zNvpP5-eDGzNN_apJ/view?usp=drivesdk) |
| 3 | Computer Networks — ISE, Sem V, 2021-22 | ISE | 2021 | 5 | [open](https://drive.google.com/file/d/15cNzpvYB2Qj0I0XmjQT2gN6XzQtF-exm/view?usp=drivesdk) |
| 4 | Computer Networks — ISE, Sem V, 2020-21 | ISE | 2020 | 5 | [open](https://drive.google.com/file/d/18V2oz1BVg-qVK7km1G22Z3JCSflvWs3A/view?usp=drivesdk) |

<details><summary>Raw URLs</summary>

1. `https://drive.google.com/file/d/1DfjeKjMKXLoJmVuR2b7kV_bpjb3hBxAG/view?usp=drivesdk`
2. `https://drive.google.com/file/d/1h5DHpnsY9XQZJF5zNvpP5-eDGzNN_apJ/view?usp=drivesdk`
3. `https://drive.google.com/file/d/15cNzpvYB2Qj0I0XmjQT2gN6XzQtF-exm/view?usp=drivesdk`
4. `https://drive.google.com/file/d/18V2oz1BVg-qVK7km1G22Z3JCSflvWs3A/view?usp=drivesdk`

</details>

**Qwen3 8B answer**

```text
- Computer Networks — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1DfjeKjMKXLoJmVuR2b7kV_bpjb3hBxAG/view?usp=drivesdk  
- Computer Networks — ISE, Sem V, 2021-22, PwD  
  https://drive.google.com/file/d/1h5DHpnsY9XQZJF5zNvpP5-eDGzNN_apJ/view?usp=drivesdk  
- Computer Networks — ISE, Sem V, 2021-22  
  https://drive.google.com/file/d/15cNzpvYB2Qj0I0XmjQT2gN6XzQtF-exm/view?usp=drivesdk  
- Computer Networks — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/18V2oz1BVg-qVK7km1G22Z3JCSflvWs3A/view?usp=drivesdk
```

---

### 9. give me PSOT paper 2021-22

*A paper split across two PDFs returns both links, not one.*

- Category: `link` · Result: **PASS**
- Filters: `{'subject_key': 'psot', 'year': 2021}`
- Papers: **3** · Retrieval: 40ms · Qwen: 5.6s

| Link check | Result | Detail |
|---|---|---|
| every link is a Google Drive URL | PASS | 3/3 |
| no link points at a folder | PASS | 0 folder link(s) |
| links are file-level /file/d/<id> | PASS | 3/3 |
| every paper is 2019-2025 | PASS | 0 outside |
| no duplicate link in one answer | PASS | 3 unique of 3 |

**Papers returned**

| # | Title | Exam | Year | Sem | Drive link |
|---|---|---|---:|---:|---|
| 1 | Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2021-22 | ISE | 2022 | 4 | [open](https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk) |
| 2 | Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2020-21, PwD | ISE | 2021 | 4 | [open](https://drive.google.com/file/d/1B4jWAF8awXQR10EwC7ihxMU5A7cjofgx/view?usp=drivesdk) |
| 3 | Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2020-21 | ISE | 2021 | 4 | [open](https://drive.google.com/file/d/1IW2puX_65JCtpZ-RlbU8C1nI6YwSc0rR/view?usp=drivesdk) |

<details><summary>Raw URLs</summary>

1. `https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk`
2. `https://drive.google.com/file/d/1B4jWAF8awXQR10EwC7ihxMU5A7cjofgx/view?usp=drivesdk`
3. `https://drive.google.com/file/d/1IW2puX_65JCtpZ-RlbU8C1nI6YwSc0rR/view?usp=drivesdk`

</details>

**Qwen3 8B answer**

```text
- Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2021-22  
  https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk
```

---

### 10. give me TACD paper

*Subject shares a PDF with others; the link is that one file.*

- Category: `link` · Result: **PASS**
- Filters: `{'subject_key': 'tacd'}`
- Papers: **3** · Retrieval: 48ms · Qwen: 13.9s

| Link check | Result | Detail |
|---|---|---|
| every link is a Google Drive URL | PASS | 3/3 |
| no link points at a folder | PASS | 0 folder link(s) |
| links are file-level /file/d/<id> | PASS | 3/3 |
| every paper is 2019-2025 | PASS | 0 outside |
| no duplicate link in one answer | PASS | 3 unique of 3 |

**Papers returned**

| # | Title | Exam | Year | Sem | Drive link |
|---|---|---|---:|---:|---|
| 1 | Theory of Automata and Compiler Design — ISE, Sem IV, 2023-24 | ISE | 2024 | 4 | [open](https://drive.google.com/file/d/1bqzzNVLOGcEYIw-uzpGpxVkBncwdDSYF/view?usp=drivesdk) |
| 2 | Theory of Automata and Compiler Design — ISE, Sem IV, 2021-22 | ISE | 2022 | 4 | [open](https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk) |
| 3 | Theory of Automata and Compiler Design — ISE, Sem IV, 2020-21 | ISE | 2021 | 4 | [open](https://drive.google.com/file/d/1BbUD5_NDbijmYQi3IoQitJuqHSoUzHpf/view?usp=drivesdk) |

<details><summary>Raw URLs</summary>

1. `https://drive.google.com/file/d/1bqzzNVLOGcEYIw-uzpGpxVkBncwdDSYF/view?usp=drivesdk`
2. `https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk`
3. `https://drive.google.com/file/d/1BbUD5_NDbijmYQi3IoQitJuqHSoUzHpf/view?usp=drivesdk`

</details>

**Qwen3 8B answer**

```text
- Theory of Automata and Compiler Design — ISE, Sem IV, 2023-24  
  https://drive.google.com/file/d/1bqzzNVLOGcEYIw-uzpGpxVkBncwdDSYF/view?usp=drivesdk  
- Theory of Automata and Compiler Design — ISE, Sem IV, 2021-22  
  https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk  
- Theory of Automata and Compiler Design — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/1BbUD5_NDbijmYQi3IoQitJuqHSoUzHpf/view?usp=drivesdk
```

---

### 11. give me OS papers from 2018

*Outside the window -> honest miss, never a 2013-2018 paper.*

- Category: `year window` · Result: **PASS**
- Filters: `{'subject_key': 'os', 'year': 2018}`
- Papers: **0** · Retrieval: 262ms

| Link check | Result | Detail |
|---|---|---|
| returned nothing | PASS | expected for this category |

**No papers returned** — reason: `no_match`

---

### 12. give me DBMS paper 2019

*First year of the window; boundary must be inclusive.*

- Category: `year window` · Result: **PASS**
- Filters: `{'subject_key': 'dbms', 'year': 2019}`
- Papers: **0** · Retrieval: 4ms

| Link check | Result | Detail |
|---|---|---|
| returned nothing | PASS | expected for this category |

**No papers returned** — reason: `no_match`

---

### 13. give me papers from 2025

*Last year of the window; boundary must be inclusive.*

- Category: `year window` · Result: **PASS**
- Filters: `{'year': 2025}`
- Papers: **45** · Retrieval: 19ms · Qwen: 59.4s

| Link check | Result | Detail |
|---|---|---|
| every link is a Google Drive URL | PASS | 45/45 |
| no link points at a folder | PASS | 0 folder link(s) |
| links are file-level /file/d/<id> | PASS | 45/45 |
| every paper is 2019-2025 | PASS | 0 outside |
| no duplicate link in one answer | PASS | 45 unique of 45 |

**Papers returned**

| # | Title | Exam | Year | Sem | Drive link |
|---|---|---|---:|---:|---|
| 1 | Analysis of Algorithms — ISE, Sem IV, 2024-25 | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/1zfkQGgPBUp81cqW-HLGzWsqIqDCcKcTh/view?usp=drivesdk) |
| 2 | Applied Cryptography — ISE, Sem VI, 2024-25 | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1loFGIh56qKC3ZOAJDeietJ-gR0kGgbp7/view?usp=drivesdk) |
| 3 | Applied Cryptography — ISE, Sem IV, 2024-25, Honours | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/1XiYynz9lMTs8abrWw0lyeJXKUDm3TUTh/view?usp=drivesdk) |
| 4 | Artificial Intelligence — ISE, Sem VI, 2024-25 | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1djTOaEfjT43TP26QJTzE4M5ypBWSEkFI/view?usp=drivesdk) |
| 5 | Cloud Computing — ISE, Sem VI, 2024-25 | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1q_ItzuW7iJcz1o98BlcX1H-OyDPeDmiV/view?usp=drivesdk) |
| 6 | Database Management System — ISE, Sem IV, 2024-25 | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/1LzMSNrHgqFj_4_2VQ45iqxe1Q5b30_mp/view?usp=drivesdk) |
| 7 | Digital Signal and Image Processing — ISE, Sem VI, 2024-25 | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1FlICjdxr_xphPKJ4vWVzVJv9QoR3woxW/view?usp=drivesdk) |
| 8 | German — ISE, Sem VI, 2024-25, Open Elective | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1_I6sg3SeRQjgZM4o_ValkyCPhIw6U9B3/view?usp=drivesdk) |
| 9 | Information Security — ISE, Sem VI, 2024-25 | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1jGjfmjNB_O7yNd4npYJ_UZmarL6bDi7J/view?usp=drivesdk) |
| 10 | Natural Language Processing — ISE, Sem VIII, 2024-25 | ISE | 2025 | 8 | [open](https://drive.google.com/file/d/1R4_wQP0i96f1Psq46myyfkHVcYqjt1VX/view?usp=drivesdk) |
| 11 | Operating Systems — ISE, Sem IV, 2024-25 | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/1nvwBQjFgEpnEsXat2rPRWtstOeasUmIJ/view?usp=drivesdk) |
| 12 | Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2024-25 | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/1LFmiF68LjxVstlJhUjSQxHXg3ooY9Ja7/view?usp=drivesdk) |
| 13 | AADA — ISE, Sem VIII, 2024-25 | ISE | 2025 | 8 | [open](https://drive.google.com/file/d/129Rz3r4gqWcRrkl0zpBV9wMb2TINX2uS/view?usp=drivesdk) |
| 14 | ADM — ISE, Sem VI, 2024-25, Honours | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1SCRFmBTSvH7eLLICTua5OXdKxwxelG70/view?usp=drivesdk) |
| 15 | AMLT — ISE, Sem VI, 2024-25, Open Elective | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1n_tezzisr_cnEtWnzz_x4d5GB0id4hZm/view?usp=drivesdk) |
| 16 | IDS — ISE, Sem IV, 2024-25, Honours | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/14cCFjXcSosmRm14kc76iSdkox7w329H_/view?usp=drivesdk) |
| 17 | IOE — ISE, Sem VIII, 2024-25 | ISE | 2025 | 8 | [open](https://drive.google.com/file/d/1rKjRTN5Sjau0M0jhwMewmkB2dPvcQJ8O/view?usp=drivesdk) |
| 18 | VAPT — ISE, Sem VI, 2024-25, Honours | ISE | 2025 | 6 | [open](https://drive.google.com/file/d/1nAAuXCOjRdeRJwpAyHBP0wxVaZaMW1wK/view?usp=drivesdk) |
| 19 | Computer Graphics — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/13cWmT80KIZB7TDXTUm4yB7xOPmsBy1Ea/view?usp=drivesdk) |
| 20 | Computer Organization and Architecture — ISE, Sem III, 2024-25 | ISE | 2024 | 3 | [open](https://drive.google.com/file/d/12h39hSO32TTi4ZlCbz6iXtAEJ67IHu2w/view?usp=drivesdk) |
| 21 | Data Analytics — ISE, Sem V, 2024-25, Honours | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/15nW5d2D5y5PJSzRJHXWfMnKebF9QiVhP/view?usp=drivesdk) |
| 22 | Data Structures — ISE, Sem III, 2024-25 | ISE | 2024 | 3 | [open](https://drive.google.com/file/d/1CInufaTvXi8HMs4Bfll5o1DefG3uTdlt/view?usp=drivesdk) |
| 23 | Data Structures — ISE, Sem VII, 2024-25 | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1ujXpfqYUdtRvIxsrVfwPrlnvhDy1R_lb/view?usp=drivesdk) |
| 24 | Object Oriented Programming Methodology — ISE, Sem III, 2024-25 | ISE | 2024 | 3 | [open](https://drive.google.com/file/d/122cc57KTEy97xYZmDznGcneLwTZem8AV/view?usp=drivesdk) |
| 25 | Operating Systems — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk) |
| 26 | Operating Systems — ISE, Sem V, 2024-25, Minor | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk) |
| 27 | Soft Computing — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/1y96qSCajVf4AJa8-XEqOGLkEuYNbzR6s/view?usp=drivesdk) |
| 28 | Supply Chain Management — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/1Lo-YYH5BoDnopypRMNKKMAoR9nXPvG1L/view?usp=drivesdk) |
| 29 | User Experience Design — ISE, Sem VII, 2024-25 | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1dtwCbJcDn5m5gjQxZpc_Adr11HxkQQ3T/view?usp=drivesdk) |
| 30 | Web Programming — ISE, Sem VII, 2024-25, Minor | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/19tFxqsuJNXWFAwz-dMuIbna8RAXxjt_K/view?usp=drivesdk) |
| 31 | AML — ISE, Sem VII, 2024-25, Honours | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1BEjIWBcUE2uD1LmPxtXjB4AVbYids_Gj/view?usp=drivesdk) |
| 32 | APM — ISE, Sem VII, 2024-25 | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1FJmeo2rAMC_PaKt5aNbdsAjnaYJWLjH9/view?usp=drivesdk) |
| 33 | BCT — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/1dPEZrRsNekZ5k5HazrQ6QutPYD8SCsbt/view?usp=drivesdk) |
| 34 | BCT — ISE, Sem VII, 2024-25 | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1qyHUhixRZY3xkCcwVMR6sSNNIHF1qvDx/view?usp=drivesdk) |
| 35 | C# — ISE, Sem VII, 2024-25 | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1TPJ4M5hdaWQaA4I9zkyCdMYfbkg8NRfE/view?usp=drivesdk) |
| 36 | CSM — ISE, Sem VII, 2024-25 | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/14SCvLh5s5GwyaPJknvvEzXxOtkCSfrhB/view?usp=drivesdk) |
| 37 | DL — ISE, Sem VII, 2024-25, Minor | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1gruFNmOp2y7tM9GYRa9eS07r_ew0AsKm/view?usp=drivesdk) |
| 38 | DSM — ISE, Sem III, 2024-25 | ISE | 2024 | 3 | [open](https://drive.google.com/file/d/1KsiZGSTwRCl1dEtoD1MUZPG9xSlk5q_1/view?usp=drivesdk) |
| 39 | EEFM — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/1bW486S2-QZvu9x5oBkEfOHNZyKVib23c/view?usp=drivesdk) |
| 40 | FUTTER — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/1sgpB-n4ZpajoLUCfHOSqI9a4L7CwMrJd/view?usp=drivesdk) |
| 41 | IMCT — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/1MBA0y_Fpm4nxDbrB7QPbWXbAwrUIqxa6/view?usp=drivesdk) |
| 42 | ITVC — ISE, Sem III, 2024-25 | ISE | 2024 | 3 | [open](https://drive.google.com/file/d/1SezKMUGyrPn6-aUdPhnWjgnLyan-IXwE/view?usp=drivesdk) |
| 43 | RL — ISE, Sem VII, 2024-25 | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1wZnV6ljujkdq2JGiGzA8gYisJy6EFbKu/view?usp=drivesdk) |
| 44 | SADT — ISE, Sem VII, 2024-25 | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1937JtJl8g6aD2uEHTCY2Ko5kVBGPKNuU/view?usp=drivesdk) |
| 45 | SEC — ISE, Sem VII, 2024-25, Honours | ISE | 2024 | 7 | [open](https://drive.google.com/file/d/1HIVY7Sc_LCPtVRS5gizOCO8dclGVKgRc/view?usp=drivesdk) |

<details><summary>Raw URLs</summary>

1. `https://drive.google.com/file/d/1zfkQGgPBUp81cqW-HLGzWsqIqDCcKcTh/view?usp=drivesdk`
2. `https://drive.google.com/file/d/1loFGIh56qKC3ZOAJDeietJ-gR0kGgbp7/view?usp=drivesdk`
3. `https://drive.google.com/file/d/1XiYynz9lMTs8abrWw0lyeJXKUDm3TUTh/view?usp=drivesdk`
4. `https://drive.google.com/file/d/1djTOaEfjT43TP26QJTzE4M5ypBWSEkFI/view?usp=drivesdk`
5. `https://drive.google.com/file/d/1q_ItzuW7iJcz1o98BlcX1H-OyDPeDmiV/view?usp=drivesdk`
6. `https://drive.google.com/file/d/1LzMSNrHgqFj_4_2VQ45iqxe1Q5b30_mp/view?usp=drivesdk`
7. `https://drive.google.com/file/d/1FlICjdxr_xphPKJ4vWVzVJv9QoR3woxW/view?usp=drivesdk`
8. `https://drive.google.com/file/d/1_I6sg3SeRQjgZM4o_ValkyCPhIw6U9B3/view?usp=drivesdk`
9. `https://drive.google.com/file/d/1jGjfmjNB_O7yNd4npYJ_UZmarL6bDi7J/view?usp=drivesdk`
10. `https://drive.google.com/file/d/1R4_wQP0i96f1Psq46myyfkHVcYqjt1VX/view?usp=drivesdk`
11. `https://drive.google.com/file/d/1nvwBQjFgEpnEsXat2rPRWtstOeasUmIJ/view?usp=drivesdk`
12. `https://drive.google.com/file/d/1LFmiF68LjxVstlJhUjSQxHXg3ooY9Ja7/view?usp=drivesdk`
13. `https://drive.google.com/file/d/129Rz3r4gqWcRrkl0zpBV9wMb2TINX2uS/view?usp=drivesdk`
14. `https://drive.google.com/file/d/1SCRFmBTSvH7eLLICTua5OXdKxwxelG70/view?usp=drivesdk`
15. `https://drive.google.com/file/d/1n_tezzisr_cnEtWnzz_x4d5GB0id4hZm/view?usp=drivesdk`
16. `https://drive.google.com/file/d/14cCFjXcSosmRm14kc76iSdkox7w329H_/view?usp=drivesdk`
17. `https://drive.google.com/file/d/1rKjRTN5Sjau0M0jhwMewmkB2dPvcQJ8O/view?usp=drivesdk`
18. `https://drive.google.com/file/d/1nAAuXCOjRdeRJwpAyHBP0wxVaZaMW1wK/view?usp=drivesdk`
19. `https://drive.google.com/file/d/13cWmT80KIZB7TDXTUm4yB7xOPmsBy1Ea/view?usp=drivesdk`
20. `https://drive.google.com/file/d/12h39hSO32TTi4ZlCbz6iXtAEJ67IHu2w/view?usp=drivesdk`
21. `https://drive.google.com/file/d/15nW5d2D5y5PJSzRJHXWfMnKebF9QiVhP/view?usp=drivesdk`
22. `https://drive.google.com/file/d/1CInufaTvXi8HMs4Bfll5o1DefG3uTdlt/view?usp=drivesdk`
23. `https://drive.google.com/file/d/1ujXpfqYUdtRvIxsrVfwPrlnvhDy1R_lb/view?usp=drivesdk`
24. `https://drive.google.com/file/d/122cc57KTEy97xYZmDznGcneLwTZem8AV/view?usp=drivesdk`
25. `https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk`
26. `https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk`
27. `https://drive.google.com/file/d/1y96qSCajVf4AJa8-XEqOGLkEuYNbzR6s/view?usp=drivesdk`
28. `https://drive.google.com/file/d/1Lo-YYH5BoDnopypRMNKKMAoR9nXPvG1L/view?usp=drivesdk`
29. `https://drive.google.com/file/d/1dtwCbJcDn5m5gjQxZpc_Adr11HxkQQ3T/view?usp=drivesdk`
30. `https://drive.google.com/file/d/19tFxqsuJNXWFAwz-dMuIbna8RAXxjt_K/view?usp=drivesdk`
31. `https://drive.google.com/file/d/1BEjIWBcUE2uD1LmPxtXjB4AVbYids_Gj/view?usp=drivesdk`
32. `https://drive.google.com/file/d/1FJmeo2rAMC_PaKt5aNbdsAjnaYJWLjH9/view?usp=drivesdk`
33. `https://drive.google.com/file/d/1dPEZrRsNekZ5k5HazrQ6QutPYD8SCsbt/view?usp=drivesdk`
34. `https://drive.google.com/file/d/1qyHUhixRZY3xkCcwVMR6sSNNIHF1qvDx/view?usp=drivesdk`
35. `https://drive.google.com/file/d/1TPJ4M5hdaWQaA4I9zkyCdMYfbkg8NRfE/view?usp=drivesdk`
36. `https://drive.google.com/file/d/14SCvLh5s5GwyaPJknvvEzXxOtkCSfrhB/view?usp=drivesdk`
37. `https://drive.google.com/file/d/1gruFNmOp2y7tM9GYRa9eS07r_ew0AsKm/view?usp=drivesdk`
38. `https://drive.google.com/file/d/1KsiZGSTwRCl1dEtoD1MUZPG9xSlk5q_1/view?usp=drivesdk`
39. `https://drive.google.com/file/d/1bW486S2-QZvu9x5oBkEfOHNZyKVib23c/view?usp=drivesdk`
40. `https://drive.google.com/file/d/1sgpB-n4ZpajoLUCfHOSqI9a4L7CwMrJd/view?usp=drivesdk`
41. `https://drive.google.com/file/d/1MBA0y_Fpm4nxDbrB7QPbWXbAwrUIqxa6/view?usp=drivesdk`
42. `https://drive.google.com/file/d/1SezKMUGyrPn6-aUdPhnWjgnLyan-IXwE/view?usp=drivesdk`
43. `https://drive.google.com/file/d/1wZnV6ljujkdq2JGiGzA8gYisJy6EFbKu/view?usp=drivesdk`
44. `https://drive.google.com/file/d/1937JtJl8g6aD2uEHTCY2Ko5kVBGPKNuU/view?usp=drivesdk`
45. `https://drive.google.com/file/d/1HIVY7Sc_LCPtVRS5gizOCO8dclGVKgRc/view?usp=drivesdk`

</details>

**Qwen3 8B answer**

```text
- Analysis of Algorithms — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1zfkQGgPBUp81cqW-HLGzWsqIqDCcKcTh/view?usp=drivesdk  
- Applied Cryptography — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1loFGIh56qKC3ZOAJDeietJ-gR0kGgbp7/view?usp=drivesdk  
- Applied Cryptography — ISE, Sem IV, 2024-25, Honours  
  https://drive.google.com/file/d/1XiYynz9lMTs8abrWw0lyeJXKUDm3TUTh/view?usp=drivesdk  
- Artificial Intelligence — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1djTOaEfjT43TP26QJTzE4M5ypBWSEkFI/view?usp=drivesdk  
- Cloud Computing — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1q_ItzuW7iJcz1o98BlcX1H-OyDPeDmiV/view?usp=drivesdk  
- Database Management System — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1LzMSNrHgqFj_4_2VQ45iqxe1Q5b30_mp/view?usp=drivesdk  
- Digital Signal and Image Processing — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1FlICjdxr_xphPKJ4vWVzVJv9QoR3woxW/view?usp=drivesdk  
- German — ISE, Sem VI, 2024-25, Open Elective  
  https://drive.google.com/file/d/1_I6sg3SeRQjgZM4o_ValkyCPhIw6U9B3/view?usp=drivesdk  
- Information Security — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1jGjfmjNB_O7yNd4npYJ_UZmarL6bDi7J/view?usp=drivesdk  
- Natural Language Processing — ISE, Sem VIII, 2024-25  
  https://drive.google.com/file/d/1R4_wQP0i96f1Psq46myyfkHVcYqjt1VX/view?usp=drivesdk  
- Operating Systems — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1nvwBQjFgEpnEsXat2rPRWtstOeasUmIJ/view?usp=drivesdk  
- Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1LFmiF68LjxVstlJhUjSQxHXg3ooY9Ja7/view?usp=drivesdk  
- AADA — ISE, Sem VIII, 2024-25  
  https://drive.google.com/file/d/129Rz3r4gqWcRrkl0zpBV9wMb2TINX2uS/view?usp=drivesdk  
- ADM — ISE, Sem VI, 2024-25, Honours  
  https://drive.google.com/file/d/1SCRFmBTSvH7eLLICTua5OXdKxwxelG70/view?usp=drivesdk  
- AMLT — ISE, Sem VI, 2024-25, Open Elective  
  https://drive.google.com/file/d/1n_tezzisr_cnEtWnzz_x4d5GB0id4hZm/view?usp=drivesdk  
... and 30 more not listed here.
```

---

### 14. give me rdbms paper

*Alias of DBMS -> same subject, same links.*

- Category: `subject` · Result: **PASS**
- Filters: `{'subject_key': 'dbms'}`
- Papers: **5** · Retrieval: 72ms · Qwen: 19.4s

| Link check | Result | Detail |
|---|---|---|
| every link is a Google Drive URL | PASS | 5/5 |
| no link points at a folder | PASS | 0 folder link(s) |
| links are file-level /file/d/<id> | PASS | 5/5 |
| every paper is 2019-2025 | PASS | 0 outside |
| no duplicate link in one answer | PASS | 5 unique of 5 |

**Papers returned**

| # | Title | Exam | Year | Sem | Drive link |
|---|---|---|---:|---:|---|
| 1 | Database Management System — ISE, Sem IV, 2024-25 | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/1LzMSNrHgqFj_4_2VQ45iqxe1Q5b30_mp/view?usp=drivesdk) |
| 2 | Database Management System — ISE, Sem IV, 2023-24 | ISE | 2024 | 4 | [open](https://drive.google.com/file/d/1PHe3j7OCb63hnFQf4MIguMNoDyAkrf3f/view?usp=drivesdk) |
| 3 | Database Management System — ISE, Sem IV, 2021-22 | ISE | 2022 | 4 | [open](https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk) |
| 4 | Database Management System — ISE, Sem IV, 2020-21 | ISE | 2021 | 4 | [open](https://drive.google.com/file/d/1oSz_qUiPfy13AhYW_Wn8mzwwfTjeZgGa/view?usp=drivesdk) |
| 5 | Database Management System — ISE, Sem IV, 2020-21 | ISE | 2021 | 4 | [open](https://drive.google.com/file/d/1KOgOhX4Tgjw3JVQHTzbGk7jJzA-0e5wc/view?usp=drivesdk) |

<details><summary>Raw URLs</summary>

1. `https://drive.google.com/file/d/1LzMSNrHgqFj_4_2VQ45iqxe1Q5b30_mp/view?usp=drivesdk`
2. `https://drive.google.com/file/d/1PHe3j7OCb63hnFQf4MIguMNoDyAkrf3f/view?usp=drivesdk`
3. `https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk`
4. `https://drive.google.com/file/d/1oSz_qUiPfy13AhYW_Wn8mzwwfTjeZgGa/view?usp=drivesdk`
5. `https://drive.google.com/file/d/1KOgOhX4Tgjw3JVQHTzbGk7jJzA-0e5wc/view?usp=drivesdk`

</details>

**Qwen3 8B answer**

```text
- Database Management System — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1LzMSNrHgqFj_4_2VQ45iqxe1Q5b30_mp/view?usp=drivesdk  
- Database Management System — ISE, Sem IV, 2023-24  
  https://drive.google.com/file/d/1PHe3j7OCb63hnFQf4MIguMNoDyAkrf3f/view?usp=drivesdk  
- Database Management System — ISE, Sem IV, 2021-22  
  https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk  
- Database Management System — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/1oSz_qUiPfy13AhYW_Wn8mzwwfTjeZgGa/view?usp=drivesdk  
- Database Management System — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/1KOgOhX4Tgjw3JVQHTzbGk7jJzA-0e5wc/view?usp=drivesdk
```

---

### 15. operating system previous year papers

*Full name instead of the abbreviation.*

- Category: `subject` · Result: **PASS**
- Filters: `{'subject_key': 'os'}`
- Papers: **5** · Retrieval: 107ms · Qwen: 17.8s

| Link check | Result | Detail |
|---|---|---|
| every link is a Google Drive URL | PASS | 5/5 |
| no link points at a folder | PASS | 0 folder link(s) |
| links are file-level /file/d/<id> | PASS | 5/5 |
| every paper is 2019-2025 | PASS | 0 outside |
| no duplicate link in one answer | PASS | 5 unique of 5 |

**Papers returned**

| # | Title | Exam | Year | Sem | Drive link |
|---|---|---|---:|---:|---|
| 1 | Operating Systems — ISE, Sem IV, 2024-25 | ISE | 2025 | 4 | [open](https://drive.google.com/file/d/1nvwBQjFgEpnEsXat2rPRWtstOeasUmIJ/view?usp=drivesdk) |
| 2 | Operating Systems — ISE, Sem V, 2024-25 | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk) |
| 3 | Operating Systems — ISE, Sem V, 2024-25, Minor | ISE | 2024 | 5 | [open](https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk) |
| 4 | Operating Systems — ISE, Sem V, 2023-24 | ISE | 2023 | 5 | [open](https://drive.google.com/file/d/1XGYyCyVJWWpeqKWmoMCRjargjs9kqqUd/view?usp=drivesdk) |
| 5 | Operating Systems — ISE, Sem V, 2023-24, Minor | ISE | 2023 | 5 | [open](https://drive.google.com/file/d/18_GHVAMFUg5l8kdg12fSIe4lImGa5xA3/view?usp=drivesdk) |

<details><summary>Raw URLs</summary>

1. `https://drive.google.com/file/d/1nvwBQjFgEpnEsXat2rPRWtstOeasUmIJ/view?usp=drivesdk`
2. `https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk`
3. `https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk`
4. `https://drive.google.com/file/d/1XGYyCyVJWWpeqKWmoMCRjargjs9kqqUd/view?usp=drivesdk`
5. `https://drive.google.com/file/d/18_GHVAMFUg5l8kdg12fSIe4lImGa5xA3/view?usp=drivesdk`

</details>

**Qwen3 8B answer**

```text
- Operating Systems — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1nvwBQjFgEpnEsXat2rPRWtstOeasUmIJ/view?usp=drivesdk  
- Operating Systems — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk  
- Operating Systems — ISE, Sem V, 2024-25, Minor  
  https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk  
- Operating Systems — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1XGYyCyVJWWpeqKWmoMCRjargjs9kqqUd/view?usp=drivesdk  
- Operating Systems — ISE, Sem V, 2023-24, Minor  
  https://drive.google.com/file/d/18_GHVAMFUg5l8kdg12fSIe4lImGa5xA3/view?usp=drivesdk
```

---

### 16. give me ITVC paper

*Unresolved subject, but the link must still be reachable.*

- Category: `subject` · Result: **PASS**
- Filters: `{'subject_key': 'itvc'}`
- Papers: **4** · Retrieval: 57ms · Qwen: 15.1s

| Link check | Result | Detail |
|---|---|---|
| every link is a Google Drive URL | PASS | 4/4 |
| no link points at a folder | PASS | 0 folder link(s) |
| links are file-level /file/d/<id> | PASS | 4/4 |
| every paper is 2019-2025 | PASS | 0 outside |
| no duplicate link in one answer | PASS | 4 unique of 4 |

**Papers returned**

| # | Title | Exam | Year | Sem | Drive link |
|---|---|---|---:|---:|---|
| 1 | ITVC — ISE, Sem III, 2024-25 | ISE | 2024 | 3 | [open](https://drive.google.com/file/d/1SezKMUGyrPn6-aUdPhnWjgnLyan-IXwE/view?usp=drivesdk) |
| 2 | ITVC — ISE, Sem III, 2023-24 | ISE | 2023 | 3 | [open](https://drive.google.com/file/d/1FS3NNR8OR5A4pCeK0Muy8TBDSDdBgCXD/view?usp=drivesdk) |
| 3 | ITVC — ISE, Sem III, 2021-22 | ISE | 2021 | 3 | [open](https://drive.google.com/file/d/1qIvy4qCYs-dQ4ZCYSTBsky-Mw8pYDpZh/view?usp=drivesdk) |
| 4 | ITVC — ISE, Sem III, 2020-21 | ISE | 2020 | 3 | [open](https://drive.google.com/file/d/1GvUsH3oZ8wTPNPc2cxPtWBh3ol5fda7I/view?usp=drivesdk) |

<details><summary>Raw URLs</summary>

1. `https://drive.google.com/file/d/1SezKMUGyrPn6-aUdPhnWjgnLyan-IXwE/view?usp=drivesdk`
2. `https://drive.google.com/file/d/1FS3NNR8OR5A4pCeK0Muy8TBDSDdBgCXD/view?usp=drivesdk`
3. `https://drive.google.com/file/d/1qIvy4qCYs-dQ4ZCYSTBsky-Mw8pYDpZh/view?usp=drivesdk`
4. `https://drive.google.com/file/d/1GvUsH3oZ8wTPNPc2cxPtWBh3ol5fda7I/view?usp=drivesdk`

</details>

**Qwen3 8B answer**

```text
- ITVC — ISE, Sem III, 2024-25  
  https://drive.google.com/file/d/1SezKMUGyrPn6-aUdPhnWjgnLyan-IXwE/view?usp=drivesdk  
- ITVC — ISE, Sem III, 2023-24  
  https://drive.google.com/file/d/1FS3NNR8OR5A4pCeK0Muy8TBDSDdBgCXD/view?usp=drivesdk  
- ITVC — ISE, Sem III, 2021-22  
  https://drive.google.com/file/d/1qIvy4qCYs-dQ4ZCYSTBsky-Mw8pYDpZh/view?usp=drivesdk  
- ITVC — ISE, Sem III, 2020-21  
  https://drive.google.com/file/d/1GvUsH3oZ8wTPNPc2cxPtWBh3ol5fda7I/view?usp=drivesdk
```

---

### 17. give me ESE sem 5 papers

*Semester-level request MAY return unresolved semester bundles.*

- Category: `bundle` · Result: **BLOCKED**
- Filters: `{'exam_type': 'ESE', 'semester': 5}`
- Papers: **0** · Retrieval: 1222ms

| Link check | Result | Detail |
|---|---|---|
| returned nothing | PASS | ESE not ingested yet -- cannot be judged |

**No papers returned** — reason: `no_match`

---

### 18. give me ESE Machine Learning papers

*Subject-level request must NEVER return a bundle.*

- Category: `bundle` · Result: **BLOCKED**
- Filters: `{'subject_key': 'ml', 'exam_type': 'ESE'}`
- Papers: **0** · Retrieval: 10ms

| Link check | Result | Detail |
|---|---|---|
| returned nothing | PASS | ESE not ingested yet -- cannot be judged |

**No papers returned** — reason: `no_match`

---

### 19. give me organic chemistry paper

*Subject not in the knowledge base -> say so, invent nothing.*

- Category: `miss` · Result: **PASS**
- Filters: `none`
- Papers: **0** · Retrieval: 0ms

| Link check | Result | Detail |
|---|---|---|
| returned nothing | PASS | expected for this category |

**No papers returned** — reason: `unknown_subject`

---

### 20. give me all papers

*No filter at all -> ask for narrowing rather than dumping the corpus.*

- Category: `miss` · Result: **PASS**
- Filters: `none`
- Papers: **0** · Retrieval: 0ms

| Link check | Result | Detail |
|---|---|---|
| returned nothing | PASS | expected for this category |

**No papers returned** — reason: `no_filters`

---

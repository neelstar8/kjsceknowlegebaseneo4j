# KJGPT PYQ — live 40-question run

- Started: 2026-09-12T04:59:19+00:00
- Model: `qwen3:8b` (thinking off)
- Papers in graph: 164
- Progress: **40/40** (40 completed, 0 failed)

`retrieval` is question -> filters -> Neo4j -> links, with no model call.
`qwen` is the extra time to have Qwen3 8B reword that same list.

## Summary

| # | Category | Question | Papers | Retrieval | Qwen | Status |
|---|---|---|---|---|---|---|
| 1 | core | Give me all DBMS papers | 5 | 20ms | 17.3s | Completed |
| 2 | core | Give me DBMS paper 2024 | 2 | 53ms | 7.3s | Completed |
| 3 | core | Give me DBMS 2024 ISE paper | 2 | 14ms | 4.2s | Completed |
| 4 | core | Give me all ISE papers | 50 | 30ms | 55.3s | Completed |
| 5 | core | Give me all ISE DBMS papers | 5 | 36ms | 17.2s | Completed |
| 6 | naming | give me OS paper | 5 | 37ms | 16.6s | Completed |
| 7 | naming | operating system previous year papers | 5 | 45ms | 15.9s | Completed |
| 8 | naming | database management system question paper | 5 | 39ms | 16.2s | Completed |
| 9 | naming | give me rdbms paper | 5 | 57ms | 16.3s | Completed |
| 10 | naming | Give me all Computer Networks papers | 4 | 57ms | 13.4s | Completed |
| 11 | naming | artificial intelligence papers | 4 | 31ms | 13.4s | Completed |
| 12 | naming | give me machine learning paper | 5 | 41ms | 16.7s | Completed |
| 13 | naming | soft computing question paper | 5 | 31ms | 16.5s | Completed |
| 14 | naming | analysis of algorithms paper | 5 | 46ms | 16.4s | Completed |
| 15 | naming | cryptography and system security paper | 3 | 33ms | 10.4s | Completed |
| 16 | naming | Flutter paper | 4 | 23ms | 14.4s | Completed |
| 17 | filters | CN 2023 paper | 1 | 227ms | 4.2s | Completed |
| 18 | filters | give me DS paper 2021-22 | 3 | 40ms | 7.3s | Completed |
| 19 | filters | papers from 2020-21 | 47 | 70ms | 58.2s | Completed |
| 20 | filters | Give me COA paper sem 3 | 3 | 64ms | 10.6s | Completed |
| 21 | filters | give me sem 8 papers | 11 | 37ms | 38.6s | Completed |
| 22 | filters | AI paper sem 6 | 3 | 54ms | 9.7s | Completed |
| 23 | filters | give me OOPM paper 2025 | 1 | 40ms | 4.3s | Completed |
| 24 | track | give me TY papers | 50 | 56ms | 63.0s | Completed |
| 25 | track | SY DBMS paper | 5 | 47ms | 17.9s | Completed |
| 26 | track | give me M.Tech papers | 7 | 43ms | 24.3s | Completed |
| 27 | track | give me all honours papers | 15 | 44ms | 59.5s | Completed |
| 28 | track | minor AI paper | 1 | 19ms | 11.6s | Completed |
| 29 | track | PwD DS paper | 1 | 31ms | 4.8s | Completed |
| 30 | track | open elective papers | 15 | 87ms | 61.1s | Completed |
| 31 | unresolved | give me ITVC paper | 4 | 83ms | 15.4s | Completed |
| 32 | unresolved | give me BCT paper | 5 | 27ms | 17.1s | Completed |
| 33 | unresolved | give me DM paper | 3 | 37ms | 10.0s | Completed |
| 34 | multi | give me PSOT paper 2021-22 | 3 | 37ms | 3.8s | Completed |
| 35 | multi | give me TACD paper | 3 | 59ms | 10.7s | Completed |
| 36 | phrasing | can you send me the operating systems paper please | 5 | 69ms | 16.3s | Completed |
| 37 | phrasing | I need last year's DBMS question paper | 5 | 43ms | 7.1s | Completed |
| 38 | phrasing | do you have any computer graphics papers | 2 | 46ms | 7.3s | Completed |
| 39 | miss | give me ESE DBMS paper | 0 | 25ms | — | Completed |
| 40 | miss | give me organic chemistry paper | 0 | 0ms | — | Completed |

## Detail

### 1. Give me all DBMS papers

- Category: `core`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'dbms'}`
- Retrieval: 20 ms · 5 paper(s)
- Qwen3 8B: 17.3 s

Papers found:

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

Answer:

```
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

### 2. Give me DBMS paper 2024

- Category: `core`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'dbms', 'year': 2024}`
- Retrieval: 53 ms · 2 paper(s)
- Qwen3 8B: 7.3 s

Papers found:

- Database Management System — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1LzMSNrHgqFj_4_2VQ45iqxe1Q5b30_mp/view?usp=drivesdk
- Database Management System — ISE, Sem IV, 2023-24  
  https://drive.google.com/file/d/1PHe3j7OCb63hnFQf4MIguMNoDyAkrf3f/view?usp=drivesdk

Answer:

```
- Database Management System — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1LzMSNrHgqFj_4_2VQ45iqxe1Q5b30_mp/view?usp=drivesdk  
- Database Management System — ISE, Sem IV, 2023-24  
  https://drive.google.com/file/d/1PHe3j7OCb63hnFQf4MIguMNoDyAkrf3f/view?usp=drivesdk
```

### 3. Give me DBMS 2024 ISE paper

- Category: `core`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'dbms', 'exam_type': 'ISE', 'year': 2024}`
- Retrieval: 14 ms · 2 paper(s)
- Qwen3 8B: 4.2 s

Papers found:

- Database Management System — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1LzMSNrHgqFj_4_2VQ45iqxe1Q5b30_mp/view?usp=drivesdk
- Database Management System — ISE, Sem IV, 2023-24  
  https://drive.google.com/file/d/1PHe3j7OCb63hnFQf4MIguMNoDyAkrf3f/view?usp=drivesdk

Answer:

```
- Database Management System — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1LzMSNrHgqFj_4_2VQ45iqxe1Q5b30_mp/view?usp=drivesdk
```

### 4. Give me all ISE papers

- Category: `core`  ·  Status: **Completed**
- Filters extracted: `{'exam_type': 'ISE'}`
- Retrieval: 30 ms · 50 paper(s)
- Qwen3 8B: 55.3 s

Papers found:

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
- IDS — ISE, Sem IV, 2024-25, Honours  
  https://drive.google.com/file/d/14cCFjXcSosmRm14kc76iSdkox7w329H_/view?usp=drivesdk
- IOE — ISE, Sem VIII, 2024-25  
  https://drive.google.com/file/d/1rKjRTN5Sjau0M0jhwMewmkB2dPvcQJ8O/view?usp=drivesdk
- VAPT — ISE, Sem VI, 2024-25, Honours  
  https://drive.google.com/file/d/1nAAuXCOjRdeRJwpAyHBP0wxVaZaMW1wK/view?usp=drivesdk
- Analysis of Algorithms — ISE, Sem IV, 2023-24  
  https://drive.google.com/file/d/1es15Evap777oz4GSV4FjfHEnhVctESMe/view?usp=drivesdk
- Computer Graphics — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/13cWmT80KIZB7TDXTUm4yB7xOPmsBy1Ea/view?usp=drivesdk
- Computer Organization and Architecture — ISE, Sem III, 2024-25  
  https://drive.google.com/file/d/12h39hSO32TTi4ZlCbz6iXtAEJ67IHu2w/view?usp=drivesdk
- Data Analytics — ISE, Sem V, 2024-25, Honours  
  https://drive.google.com/file/d/15nW5d2D5y5PJSzRJHXWfMnKebF9QiVhP/view?usp=drivesdk
- Data Structures — ISE, Sem III, 2024-25  
  https://drive.google.com/file/d/1CInufaTvXi8HMs4Bfll5o1DefG3uTdlt/view?usp=drivesdk
- Data Structures — ISE, Sem VII, 2024-25  
  https://drive.google.com/file/d/1ujXpfqYUdtRvIxsrVfwPrlnvhDy1R_lb/view?usp=drivesdk
- Database Management System — ISE, Sem IV, 2023-24  
  https://drive.google.com/file/d/1PHe3j7OCb63hnFQf4MIguMNoDyAkrf3f/view?usp=drivesdk
- Machine Learning — ISE, 2023-24  
  https://drive.google.com/file/d/1oGH0iPsEkLTTIsBTGjtzEkKYzou0klxh/view?usp=drivesdk
- Object Oriented Programming Methodology — ISE, Sem III, 2024-25  
  https://drive.google.com/file/d/122cc57KTEy97xYZmDznGcneLwTZem8AV/view?usp=drivesdk
- Object Oriented Programming Methodology — ISE, Sem IV, 2023-24, Minor  
  https://drive.google.com/file/d/1CLtG6wUXMT8YdAjqgXELgdgeYP0DeLaO/view?usp=drivesdk
- Operating Systems — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk
- Operating Systems — ISE, Sem V, 2024-25, Minor  
  https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk
- Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2023-24  
  https://drive.google.com/file/d/1P8WD2PDrJ5mRyLgNdbgkZRIp47hPg9uk/view?usp=drivesdk
- Soft Computing — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1y96qSCajVf4AJa8-XEqOGLkEuYNbzR6s/view?usp=drivesdk
- Supply Chain Management — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1Lo-YYH5BoDnopypRMNKKMAoR9nXPvG1L/view?usp=drivesdk
- Theory of Automata and Compiler Design — ISE, Sem IV, 2023-24  
  https://drive.google.com/file/d/1bqzzNVLOGcEYIw-uzpGpxVkBncwdDSYF/view?usp=drivesdk
- User Experience Design — ISE, Sem VII, 2024-25  
  https://drive.google.com/file/d/1dtwCbJcDn5m5gjQxZpc_Adr11HxkQQ3T/view?usp=drivesdk
- Web Programming — ISE, Sem VII, 2024-25, Minor  
  https://drive.google.com/file/d/19tFxqsuJNXWFAwz-dMuIbna8RAXxjt_K/view?usp=drivesdk
- ADS — ISE, Sem IV, 2023-24, Honours  
  https://drive.google.com/file/d/1h_A7iLrSiQUBSeVpU8SwKgsGa_ualnNb/view?usp=drivesdk
- AML — ISE, Sem VII, 2024-25, Honours  
  https://drive.google.com/file/d/1BEjIWBcUE2uD1LmPxtXjB4AVbYids_Gj/view?usp=drivesdk
- APM — ISE, Sem VII, 2024-25  
  https://drive.google.com/file/d/1FJmeo2rAMC_PaKt5aNbdsAjnaYJWLjH9/view?usp=drivesdk
- BCT — ISE, Sem VII, 2024-25  
  https://drive.google.com/file/d/1qyHUhixRZY3xkCcwVMR6sSNNIHF1qvDx/view?usp=drivesdk
- BCT — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1dPEZrRsNekZ5k5HazrQ6QutPYD8SCsbt/view?usp=drivesdk
- C# — ISE, Sem VII, 2024-25  
  https://drive.google.com/file/d/1TPJ4M5hdaWQaA4I9zkyCdMYfbkg8NRfE/view?usp=drivesdk
- CSFC — ISE, Sem IV, 2023-24, Honours  
  https://drive.google.com/file/d/1XWlrsMKIj-KOWZ7EKp9_Iy6SoYakPk8V/view?usp=drivesdk
- CSM — ISE, Sem VII, 2024-25  
  https://drive.google.com/file/d/14SCvLh5s5GwyaPJknvvEzXxOtkCSfrhB/view?usp=drivesdk
- DL — ISE, Sem VII, 2024-25, Minor  
  https://drive.google.com/file/d/1gruFNmOp2y7tM9GYRa9eS07r_ew0AsKm/view?usp=drivesdk
- DSM — ISE, Sem III, 2024-25  
  https://drive.google.com/file/d/1KsiZGSTwRCl1dEtoD1MUZPG9xSlk5q_1/view?usp=drivesdk
- EEFM — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1bW486S2-QZvu9x5oBkEfOHNZyKVib23c/view?usp=drivesdk
- FUTTER — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1sgpB-n4ZpajoLUCfHOSqI9a4L7CwMrJd/view?usp=drivesdk
- IMCT — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1MBA0y_Fpm4nxDbrB7QPbWXbAwrUIqxa6/view?usp=drivesdk
- ITVC — ISE, Sem III, 2024-25  
  https://drive.google.com/file/d/1SezKMUGyrPn6-aUdPhnWjgnLyan-IXwE/view?usp=drivesdk

Answer:

```
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

### 5. Give me all ISE DBMS papers

- Category: `core`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'dbms', 'exam_type': 'ISE'}`
- Retrieval: 36 ms · 5 paper(s)
- Qwen3 8B: 17.2 s

Papers found:

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

Answer:

```
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

### 6. give me OS paper

- Category: `naming`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'os'}`
- Retrieval: 37 ms · 5 paper(s)
- Qwen3 8B: 16.6 s

Papers found:

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

Answer:

```
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

### 7. operating system previous year papers

- Category: `naming`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'os'}`
- Retrieval: 45 ms · 5 paper(s)
- Qwen3 8B: 15.9 s

Papers found:

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

Answer:

```
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

### 8. database management system question paper

- Category: `naming`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'dbms'}`
- Retrieval: 39 ms · 5 paper(s)
- Qwen3 8B: 16.2 s

Papers found:

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

Answer:

```
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

### 9. give me rdbms paper

- Category: `naming`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'dbms'}`
- Retrieval: 57 ms · 5 paper(s)
- Qwen3 8B: 16.3 s

Papers found:

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

Answer:

```
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

### 10. Give me all Computer Networks papers

- Category: `naming`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'cn'}`
- Retrieval: 57 ms · 4 paper(s)
- Qwen3 8B: 13.4 s

Papers found:

- Computer Networks — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1DfjeKjMKXLoJmVuR2b7kV_bpjb3hBxAG/view?usp=drivesdk
- Computer Networks — ISE, Sem V, 2021-22, PwD  
  https://drive.google.com/file/d/1h5DHpnsY9XQZJF5zNvpP5-eDGzNN_apJ/view?usp=drivesdk
- Computer Networks — ISE, Sem V, 2021-22  
  https://drive.google.com/file/d/15cNzpvYB2Qj0I0XmjQT2gN6XzQtF-exm/view?usp=drivesdk
- Computer Networks — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/18V2oz1BVg-qVK7km1G22Z3JCSflvWs3A/view?usp=drivesdk

Answer:

```
- Computer Networks — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1DfjeKjMKXLoJmVuR2b7kV_bpjb3hBxAG/view?usp=drivesdk  
- Computer Networks — ISE, Sem V, 2021-22, PwD  
  https://drive.google.com/file/d/1h5DHpnsY9XQZJF5zNvpP5-eDGzNN_apJ/view?usp=drivesdk  
- Computer Networks — ISE, Sem V, 2021-22  
  https://drive.google.com/file/d/15cNzpvYB2Qj0I0XmjQT2gN6XzQtF-exm/view?usp=drivesdk  
- Computer Networks — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/18V2oz1BVg-qVK7km1G22Z3JCSflvWs3A/view?usp=drivesdk
```

### 11. artificial intelligence papers

- Category: `naming`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'ai'}`
- Retrieval: 31 ms · 4 paper(s)
- Qwen3 8B: 13.4 s

Papers found:

- Artificial Intelligence — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1djTOaEfjT43TP26QJTzE4M5ypBWSEkFI/view?usp=drivesdk
- Artificial Intelligence — ISE, Sem V, 2023-24, Minor  
  https://drive.google.com/file/d/1KKp2Ls832sOuf7ON376yLeHlXOgvFG9S/view?usp=drivesdk
- Artificial Intelligence — ISE, Sem VI, 2021-22  
  https://drive.google.com/file/d/1qIK8vZDECtcsBmTLaMudDPa3mmnkwji8/view?usp=drivesdk
- Artificial Intelligence — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1ZR1g_-25Ji9ju3htsgJLlpWpHTyEzpTd/view?usp=drivesdk

Answer:

```
- Artificial Intelligence — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1djTOaEfjT43TP26QJTzE4M5ypBWSEkFI/view?usp=drivesdk  
- Artificial Intelligence — ISE, Sem V, 2023-24, Minor  
  https://drive.google.com/file/d/1KKp2Ls832sOuf7ON376yLeHlXOgvFG9S/view?usp=drivesdk  
- Artificial Intelligence — ISE, Sem VI, 2021-22  
  https://drive.google.com/file/d/1qIK8vZDECtcsBmTLaMudDPa3mmnkwji8/view?usp=drivesdk  
- Artificial Intelligence — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1ZR1g_-25Ji9ju3htsgJLlpWpHTyEzpTd/view?usp=drivesdk
```

### 12. give me machine learning paper

- Category: `naming`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'ml'}`
- Retrieval: 41 ms · 5 paper(s)
- Qwen3 8B: 16.7 s

Papers found:

- Machine Learning — ISE, 2023-24  
  https://drive.google.com/file/d/1oGH0iPsEkLTTIsBTGjtzEkKYzou0klxh/view?usp=drivesdk
- Machine Learning — ISE, Sem II, 2022-23  
  https://drive.google.com/file/d/1kuz4fD9aKcf7wv7Ag2SYyl-h5L4O-npD/view?usp=drivesdk
- Machine Learning — ISE, Sem II, 2022-23  
  https://drive.google.com/file/d/1D1L1chnStdvCI2owuyh4mkOKwXtk9u1K/view?usp=drivesdk
- Machine Learning — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1jbfMu6GxXxczWbKDl1yBUE9XSiKUTG-G/view?usp=drivesdk
- Machine Learning — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/12_A2LbfS1UgRfZ1FKSNNsp_ai2IsJzlO/view?usp=drivesdk

Answer:

```
- Machine Learning — ISE, 2023-24  
  https://drive.google.com/file/d/1oGH0iPsEkLTTIsBTGjtzEkKYzou0klxh/view?usp=drivesdk  
- Machine Learning — ISE, Sem II, 2022-23 (1 pg)  
  https://drive.google.com/file/d/1kuz4fD9aKcf7wv7Ag2SYyl-h5L4O-npD/view?usp=drivesdk  
- Machine Learning — ISE, Sem II, 2022-23 (2 pg)  
  https://drive.google.com/file/d/1D1L1chnStdvCI2owuyh4mkOKwXtk9u1K/view?usp=drivesdk  
- Machine Learning — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1jbfMu6GxXxczWbKDl1yBUE9XSiKUTG-G/view?usp=drivesdk  
- Machine Learning — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/12_A2LbfS1UgRfZ1FKSNNsp_ai2IsJzlO/view?usp=drivesdk
```

### 13. soft computing question paper

- Category: `naming`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'sc'}`
- Retrieval: 31 ms · 5 paper(s)
- Qwen3 8B: 16.5 s

Papers found:

- Soft Computing — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1y96qSCajVf4AJa8-XEqOGLkEuYNbzR6s/view?usp=drivesdk
- Soft Computing — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1g3GyqXdrHd3xyou0Y-nWOcfjEsD1NsZR/view?usp=drivesdk
- Soft Computing — ISE, Sem V, 2021-22  
  https://drive.google.com/file/d/1jvHTr7QeWmvvcvQEkUNAWmQ-OMwXiZTq/view?usp=drivesdk
- Soft Computing — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/1hBY4kqWMaKkWpFH4MeXPn7pab5zFKVZK/view?usp=drivesdk
- Soft Computing — ISE, Sem VII, 2020-21  
  https://drive.google.com/file/d/1zl33DTIc160TY8MzLaOKQPMQucGLdmRd/view?usp=drivesdk

Answer:

```
- Soft Computing — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1y96qSCajVf4AJa8-XEqOGLkEuYNbzR6s/view?usp=drivesdk  
- Soft Computing — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1g3GyqXdrHd3xyou0Y-nWOcfjEsD1NsZR/view?usp=drivesdk  
- Soft Computing — ISE, Sem V, 2021-22  
  https://drive.google.com/file/d/1jvHTr7QeWmvvcvQEkUNAWmQ-OMwXiZTq/view?usp=drivesdk  
- Soft Computing — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/1hBY4kqWMaKkWpFH4MeXPn7pab5zFKVZK/view?usp=drivesdk  
- Soft Computing — ISE, Sem VII, 2020-21  
  https://drive.google.com/file/d/1zl33DTIc160TY8MzLaOKQPMQucGLdmRd/view?usp=drivesdk
```

### 14. analysis of algorithms paper

- Category: `naming`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'aoa'}`
- Retrieval: 46 ms · 5 paper(s)
- Qwen3 8B: 16.4 s

Papers found:

- Analysis of Algorithms — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1zfkQGgPBUp81cqW-HLGzWsqIqDCcKcTh/view?usp=drivesdk
- Analysis of Algorithms — ISE, Sem IV, 2023-24  
  https://drive.google.com/file/d/1es15Evap777oz4GSV4FjfHEnhVctESMe/view?usp=drivesdk
- Analysis of Algorithms — ISE, Sem IV, 2021-22  
  https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk
- Analysis of Algorithms — ISE, Sem IV, 2020-21, PwD  
  https://drive.google.com/file/d/1sdAh2Y_dQ9sbf6X3ait54o4G426W9GOX/view?usp=drivesdk
- Analysis of Algorithms — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/18UgEqHuP5Z8haQpjYil_pX7dN7tMiQ10/view?usp=drivesdk

Answer:

```
- Analysis of Algorithms — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1zfkQGgPBUp81cqW-HLGzWsqIqDCcKcTh/view?usp=drivesdk  
- Analysis of Algorithms — ISE, Sem IV, 2023-24  
  https://drive.google.com/file/d/1es15Evap777oz4GSV4FjfHEnhVctESMe/view?usp=drivesdk  
- Analysis of Algorithms — ISE, Sem IV, 2021-22  
  https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk  
- Analysis of Algorithms — ISE, Sem IV, 2020-21, PwD  
  https://drive.google.com/file/d/1sdAh2Y_dQ9sbf6X3ait54o4G426W9GOX/view?usp=drivesdk  
- Analysis of Algorithms — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/18UgEqHuP5Z8haQpjYil_pX7dN7tMiQ10/view?usp=drivesdk
```

### 15. cryptography and system security paper

- Category: `naming`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'css'}`
- Retrieval: 33 ms · 3 paper(s)
- Qwen3 8B: 10.4 s

Papers found:

- Cryptography and System Security — ISE, Sem VI, 2021-22  
  https://drive.google.com/file/d/1qIK8vZDECtcsBmTLaMudDPa3mmnkwji8/view?usp=drivesdk
- Cryptography and System Security — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1QWO7s-BWm28K4t3cMzu9i6u7aWAjhBnx/view?usp=drivesdk
- Cryptography and System Security — ISE, Sem VII, 2020-21  
  https://drive.google.com/file/d/1RD4pyCHMg5t-OMlOoKFstWdGSFp5Xq-J/view?usp=drivesdk

Answer:

```
- Cryptography and System Security — ISE, Sem VI, 2021-22  
  https://drive.google.com/file/d/1qIK8vZDECtcsBmTLaMudDPa3mmnkwji8/view?usp=drivesdk  
- Cryptography and System Security — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1QWO7s-BWm28K4t3cMzu9i6u7aWAjhBnx/view?usp=drivesdk  
- Cryptography and System Security — ISE, Sem VII, 2020-21  
  https://drive.google.com/file/d/1RD4pyCHMg5t-OMlOoKFstWdGSFp5Xq-J/view?usp=drivesdk
```

### 16. Flutter paper

- Category: `naming`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'mad'}`
- Retrieval: 23 ms · 4 paper(s)
- Qwen3 8B: 14.4 s

Papers found:

- Mobile Application Development — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1SUAOP7YrhfJDpxP3p_RrZommu8Cz8wCr/view?usp=drivesdk
- Mobile Application Development — ISE, Sem V, 2021-22, Open Elective, PwD  
  https://drive.google.com/file/d/1ddGln35yFFywr7uoBtwFPoI9CCJ4rS_u/view?usp=drivesdk
- Mobile Application Development — ISE, Sem V, 2021-22, Open Elective  
  https://drive.google.com/file/d/1T99R7_p2nWUXdXyEqj6JJXzfKGZOE_wy/view?usp=drivesdk
- Mobile Application Development — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/1BD8SbE19O0W_JB8p31Kq0_6dl5NrpJTK/view?usp=drivesdk

Answer:

```
- Mobile Application Development — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1SUAOP7YrhfJDpxP3p_RrZommu8Cz8wCr/view?usp=drivesdk  
- Mobile Application Development — ISE, Sem V, 2021-22, Open Elective, PwD  
  https://drive.google.com/file/d/1ddGln35yFFywr7uoBtwFPoI9CCJ4rS_u/view?usp=drivesdk  
- Mobile Application Development — ISE, Sem V, 2021-22, Open Elective  
  https://drive.google.com/file/d/1T99R7_p2nWUXdXyEqj6JJXzfKGZOE_wy/view?usp=drivesdk  
- Mobile Application Development — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/1BD8SbE19O0W_JB8p31Kq0_6dl5NrpJTK/view?usp=drivesdk
```

### 17. CN 2023 paper

- Category: `filters`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'cn', 'year': 2023}`
- Retrieval: 227 ms · 1 paper(s)
- Qwen3 8B: 4.2 s

Papers found:

- Computer Networks — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1DfjeKjMKXLoJmVuR2b7kV_bpjb3hBxAG/view?usp=drivesdk

Answer:

```
Computer Networks — ISE, Sem V, 2023-24  
https://drive.google.com/file/d/1DfjeKjMKXLoJmVuR2b7kV_bpjb3hBxAG/view?usp=drivesdk
```

### 18. give me DS paper 2021-22

- Category: `filters`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'ds', 'year': 2021}`
- Retrieval: 40 ms · 3 paper(s)
- Qwen3 8B: 7.3 s

Papers found:

- Data Structures — ISE, Sem III, 2021-22, PwD  
  https://drive.google.com/file/d/1Gr-q0QW6AWI-9X4v5ChKz4ioybOMv21H/view?usp=drivesdk
- Data Structures — ISE, Sem III, 2021-22  
  https://drive.google.com/file/d/1HIK03AC3nhDPUcec1a6ypsDrV-QzwM-W/view?usp=drivesdk
- Data Structures — ISE, Sem III, 2020-21  
  https://drive.google.com/file/d/1rCkwX_jSjo0lprV1rIBC2S9oEoTItlxg/view?usp=drivesdk

Answer:

```
- Data Structures — ISE, Sem III, 2021-22, PwD  
  https://drive.google.com/file/d/1Gr-q0QW6AWI-9X4v5ChKz4ioybOMv21H/view?usp=drivesdk  
- Data Structures — ISE, Sem III, 2021-22  
  https://drive.google.com/file/d/1HIK03AC3nhDPUcec1a6ypsDrV-QzwM-W/view?usp=drivesdk
```

### 19. papers from 2020-21

- Category: `filters`  ·  Status: **Completed**
- Filters extracted: `{'year': 2020}`
- Retrieval: 70 ms · 47 paper(s)
- Qwen3 8B: 58.2 s

Papers found:

- Advanced Internet Technologies — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1x7SkjiNx8-i9ig0DVPZQayzxhYdysYQF/view?usp=drivesdk
- Analysis of Algorithms — ISE, Sem IV, 2020-21, PwD  
  https://drive.google.com/file/d/1sdAh2Y_dQ9sbf6X3ait54o4G426W9GOX/view?usp=drivesdk
- Analysis of Algorithms — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/18UgEqHuP5Z8haQpjYil_pX7dN7tMiQ10/view?usp=drivesdk
- Artificial Intelligence — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1ZR1g_-25Ji9ju3htsgJLlpWpHTyEzpTd/view?usp=drivesdk
- Big Data Analytics — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1deMJq92fEGTWeDUJdLE-4gsFgoLrny18/view?usp=drivesdk
- Cryptography and System Security — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1QWO7s-BWm28K4t3cMzu9i6u7aWAjhBnx/view?usp=drivesdk
- Data Mining and Business Intelligence — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1qgDCCETnEKZ_BUDJk-5CBdNzMYbNY-SE/view?usp=drivesdk
- Database Management System — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/1oSz_qUiPfy13AhYW_Wn8mzwwfTjeZgGa/view?usp=drivesdk
- Database Management System — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/1KOgOhX4Tgjw3JVQHTzbGk7jJzA-0e5wc/view?usp=drivesdk
- Digital Signal and Image Processing — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1gda-ziy3ALRnz6erEYu70vc_qfP8jqsv/view?usp=drivesdk
- Machine Learning — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1jbfMu6GxXxczWbKDl1yBUE9XSiKUTG-G/view?usp=drivesdk
- Machine Learning — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/12_A2LbfS1UgRfZ1FKSNNsp_ai2IsJzlO/view?usp=drivesdk
- Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2020-21, PwD  
  https://drive.google.com/file/d/1B4jWAF8awXQR10EwC7ihxMU5A7cjofgx/view?usp=drivesdk
- Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/1IW2puX_65JCtpZ-RlbU8C1nI6YwSc0rR/view?usp=drivesdk
- Software Testing and Quality Assurance — ISE, Sem VIII, 2020-21, PwD  
  https://drive.google.com/file/d/1LbL_ltLvQTetLgBVuMtho0J7Byd_bivD/view?usp=drivesdk
- Software Testing and Quality Assurance — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1WWdry-JOd4czEZkgG2APYMkTx41hdmj6/view?usp=drivesdk
- Theory of Automata and Compiler Design — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/1BbUD5_NDbijmYQi3IoQitJuqHSoUzHpf/view?usp=drivesdk
- AITISE — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/10sFZWM1mgFuR-ADxR92aOMEsx1fbjGIU/view?usp=drivesdk
- aml programming — ISE, Sem VI, 2020-21, Open Elective  
  https://drive.google.com/file/d/1VW-8JINUZAv0lFz3MCmJAB3hjTYB7I6l/view?usp=drivesdk
- aml theory — ISE, Sem VI, 2020-21, Open Elective  
  https://drive.google.com/file/d/10GCDoO62ozXVvMMnFC4-8XbXHi802tyw/view?usp=drivesdk
- DCC — ISE, Sem VIII, 2020-21, PwD  
  https://drive.google.com/file/d/1u8wcoU6zn51osEUMOTdkL1Cg3iXfkjoW/view?usp=drivesdk
- DCC — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1Qd9xOhBr7wD35k_irLKKPofUNgbLF0Ho/view?usp=drivesdk
- MSD — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1oIgmjvDFgPAJEkmkgGjti6wXQiQ_MVvb/view?usp=drivesdk
- SMAC — ISE, Sem VI, 2020-21, Open Elective  
  https://drive.google.com/file/d/1FHZnk1eBHj1zzCer0OkxsQEF3-SymPBm/view?usp=drivesdk
- Augmented and Virtual Reality — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/194wkvhdP56cbFczxqyZl3z88gWXnC1Ua/view?usp=drivesdk
- Computer Graphics and Virtual Reality Systems — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/1kh-HL3w4Bvnj_n9WmnMUVOqLdB494ntq/view?usp=drivesdk
- Computer Networks — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/18V2oz1BVg-qVK7km1G22Z3JCSflvWs3A/view?usp=drivesdk
- Computer Organization and Architecture — ISE, Sem III, 2020-21  
  https://drive.google.com/file/d/1HJCPvBmkMeSrFlQjG7uZ8mkMVhOE6Xam/view?usp=drivesdk
- Cryptography and System Security — ISE, Sem VII, 2020-21  
  https://drive.google.com/file/d/1RD4pyCHMg5t-OMlOoKFstWdGSFp5Xq-J/view?usp=drivesdk
- Data Structures — ISE, Sem III, 2020-21  
  https://drive.google.com/file/d/1rCkwX_jSjo0lprV1rIBC2S9oEoTItlxg/view?usp=drivesdk
- Data Warehousing and Mining — ISE, Sem VII, 2020-21  
  https://drive.google.com/file/d/1sheEQ7p_ZhonIV-jAXVjc6fb1IpSIuDo/view?usp=drivesdk
- Mobile Application Development — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/1BD8SbE19O0W_JB8p31Kq0_6dl5NrpJTK/view?usp=drivesdk
- Mobile Application Development (iOS) — ISE, Sem V, 2020-21, Open Elective  
  https://drive.google.com/file/d/1y0CMoWbj48Mg4GwDm3zE3zkiFP0cOYrN/view?usp=drivesdk
- Natural Language Processing — ISE, Sem VII, 2020-21  
  https://drive.google.com/file/d/1G9s9eT0z0RrXfVQQcXfqmSHE0jhBimQO/view?usp=drivesdk
- Object Oriented Programming Methodology — ISE, Sem III, 2020-21  
  https://drive.google.com/file/d/1SkH1XaMiDRI83wKWHxhhREXboaEyUhDx/view?usp=drivesdk
- Open Source Software Systems — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/1zrGw3UQAOh80UU5uHCXwcvy_kODq2T4c/view?usp=drivesdk
- Python for Data Science — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/1X_R17znF6r-4Xkbm8PlpYXfDYVfjlN6P/view?usp=drivesdk
- Soft Computing — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/1hBY4kqWMaKkWpFH4MeXPn7pab5zFKVZK/view?usp=drivesdk
- Soft Computing — ISE, Sem VII, 2020-21  
  https://drive.google.com/file/d/1zl33DTIc160TY8MzLaOKQPMQucGLdmRd/view?usp=drivesdk
- Software Engineering — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/1j-g5mXZFyw8tNp5kJIkalIF4M4rguz1z/view?usp=drivesdk
- Software Project Management — ISE, Sem VII, 2020-21  
  https://drive.google.com/file/d/1aF5WDPTaqvjnhGKfbf868yNrC_HK1o4n/view?usp=drivesdk
- ADBDWH — ISE, Sem V, 2020-21  
  https://drive.google.com/file/d/1DVzUAKGfP2xnWLK9bB965jNSbgLkuvWU/view?usp=drivesdk
- c# net — ISE, Sem VII, 2020-21  
  https://drive.google.com/file/d/1FQz6UKQIN2zgR1FRcPfVZTPL65UlcM2q/view?usp=drivesdk
- CSM — ISE, Sem VII, 2020-21  
  https://drive.google.com/file/d/1kJVeFXG6A3q3xixq70EGUJ9n4hmYZBH6/view?usp=drivesdk
- DSM — ISE, Sem III, 2020-21  
  https://drive.google.com/file/d/1hC69geck1MotrWw-25P-lO_chkh4RsvM/view?usp=drivesdk
- HMI — ISE, Sem VII, 2020-21  
  https://drive.google.com/file/d/1gzDXXX-oApwDWjMrIQJOelKlC7O7BQQ5/view?usp=drivesdk
- ITVC — ISE, Sem III, 2020-21  
  https://drive.google.com/file/d/1GvUsH3oZ8wTPNPc2cxPtWBh3ol5fda7I/view?usp=drivesdk

Answer:

```
47 matching question paper(s) for 2020-21:
- Advanced Internet Technologies — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1x7SkjiNx8-i9ig0DVPZQayzxhYdysYQF/view?usp=drivesdk  
- Analysis of Algorithms — ISE, Sem IV, 2020-21, PwD  
  https://drive.google.com/file/d/1sdAh2Y_dQ9sbf6X3ait54o4G426W9GOX/view?usp=drivesdk  
- Analysis of Algorithms — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/18UgEqHuP5Z8haQpjYil_pX7dN7tMiQ10/view?usp=drivesdk  
- Artificial Intelligence — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1ZR1g_-25Ji9ju3htsgJLlpWpHTyEzpTd/view?usp=drivesdk  
- Big Data Analytics — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1deMJq92fEGTWeDUJdLE-4gsFgoLrny18/view?usp=drivesdk  
- Cryptography and System Security — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1QWO7s-BWm28K4t3cMzu9i6u7aWAjhBnx/view?usp=drivesdk  
- Data Mining and Business Intelligence — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1qgDCCETnEKZ_BUDJk-5CBdNzMYbNY-SE/view?usp=drivesdk  
- Database Management System — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/1oSz_qUiPfy13AhYW_Wn8mzwwfTjeZgGa/view?usp=drivesdk  
- Database Management System — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/1KOgOhX4Tgjw3JVQHTzbGk7jJzA-0e5wc/view?usp=drivesdk  
- Digital Signal and Image Processing — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1gda-ziy3ALRnz6erEYu70vc_qfP8jqsv/view?usp=drivesdk  
- Machine Learning — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1jbfMu6GxXxczWbKDl1yBUE9XSiKUTG-G/view?usp=drivesdk  
- Machine Learning — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/12_A2LbfS1UgRfZ1FKSNNsp_ai2IsJzlO/view?usp=drivesdk  
- Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2020-21, PwD  
  https://drive.google.com/file/d/1B4jWAF8awXQR10EwC7ihxMU5A7cjofgx/view?usp=drivesdk  
- Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/1IW2puX_65JCtpZ-RlbU8C1nI6YwSc0rR/view?usp=drivesdk  
- Software Testing and Quality Assurance — ISE, Sem VIII, 2020-21, PwD  
  https://drive.google.com/file/d/1LbL_ltLvQTetLgBVuMtho0J7Byd_bivD/view?usp=drivesdk  
... and 32 more not listed here.
```

### 20. Give me COA paper sem 3

- Category: `filters`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'coa', 'semester': 3}`
- Retrieval: 64 ms · 3 paper(s)
- Qwen3 8B: 10.6 s

Papers found:

- Computer Organization and Architecture — ISE, Sem III, 2024-25  
  https://drive.google.com/file/d/12h39hSO32TTi4ZlCbz6iXtAEJ67IHu2w/view?usp=drivesdk
- Computer Organization and Architecture — ISE, Sem III, 2023-24  
  https://drive.google.com/file/d/1egH5USMx78-KAnzCYrab9sBLCyv2SODq/view?usp=drivesdk
- Computer Organization and Architecture — ISE, Sem III, 2020-21  
  https://drive.google.com/file/d/1HJCPvBmkMeSrFlQjG7uZ8mkMVhOE6Xam/view?usp=drivesdk

Answer:

```
- Computer Organization and Architecture — ISE, Sem III, 2024-25  
  https://drive.google.com/file/d/12h39hSO32TTi4ZlCbz6iXtAEJ67IHu2w/view?usp=drivesdk  
- Computer Organization and Architecture — ISE, Sem III, 2023-24  
  https://drive.google.com/file/d/1egH5USMx78-KAnzCYrab9sBLCyv2SODq/view?usp=drivesdk  
- Computer Organization and Architecture — ISE, Sem III, 2020-21  
  https://drive.google.com/file/d/1HJCPvBmkMeSrFlQjG7uZ8mkMVhOE6Xam/view?usp=drivesdk
```

### 21. give me sem 8 papers

- Category: `filters`  ·  Status: **Completed**
- Filters extracted: `{'semester': 8}`
- Retrieval: 37 ms · 11 paper(s)
- Qwen3 8B: 38.6 s

Papers found:

- Natural Language Processing — ISE, Sem VIII, 2024-25  
  https://drive.google.com/file/d/1R4_wQP0i96f1Psq46myyfkHVcYqjt1VX/view?usp=drivesdk
- AADA — ISE, Sem VIII, 2024-25  
  https://drive.google.com/file/d/129Rz3r4gqWcRrkl0zpBV9wMb2TINX2uS/view?usp=drivesdk
- IOE — ISE, Sem VIII, 2024-25  
  https://drive.google.com/file/d/1rKjRTN5Sjau0M0jhwMewmkB2dPvcQJ8O/view?usp=drivesdk
- Advanced Internet Technologies — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1x7SkjiNx8-i9ig0DVPZQayzxhYdysYQF/view?usp=drivesdk
- Big Data Analytics — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1deMJq92fEGTWeDUJdLE-4gsFgoLrny18/view?usp=drivesdk
- Machine Learning — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1jbfMu6GxXxczWbKDl1yBUE9XSiKUTG-G/view?usp=drivesdk
- Software Testing and Quality Assurance — ISE, Sem VIII, 2020-21, PwD  
  https://drive.google.com/file/d/1LbL_ltLvQTetLgBVuMtho0J7Byd_bivD/view?usp=drivesdk
- Software Testing and Quality Assurance — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1WWdry-JOd4czEZkgG2APYMkTx41hdmj6/view?usp=drivesdk
- AITISE — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/10sFZWM1mgFuR-ADxR92aOMEsx1fbjGIU/view?usp=drivesdk
- DCC — ISE, Sem VIII, 2020-21, PwD  
  https://drive.google.com/file/d/1u8wcoU6zn51osEUMOTdkL1Cg3iXfkjoW/view?usp=drivesdk
- DCC — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1Qd9xOhBr7wD35k_irLKKPofUNgbLF0Ho/view?usp=drivesdk

Answer:

```
- Natural Language Processing — ISE, Sem VIII, 2024-25  
  https://drive.google.com/file/d/1R4_wQP0i96f1Psq46myyfkHVcYqjt1VX/view?usp=drivesdk  
- AADA — ISE, Sem VIII, 2024-25  
  https://drive.google.com/file/d/129Rz3r4gqWcRrkl0zpBV9wMb2TINX2uS/view?usp=drivesdk  
- IOE — ISE, Sem VIII, 2024-25  
  https://drive.google.com/file/d/1rKjRTN5Sjau0M0jhwMewmkB2dPvcQJ8O/view?usp=drivesdk  
- Advanced Internet Technologies — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1x7SkjiNx8-i9ig0DVPZQayzxhYdysYQF/view?usp=drivesdk  
- Big Data Analytics — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1deMJq92fEGTWeDUJdLE-4gsFgoLrny18/view?usp=drivesdk  
- Machine Learning — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1jbfMu6GxXxczWbKDl1yBUE9XSiKUTG-G/view?usp=drivesdk  
- Software Testing and Quality Assurance — ISE, Sem VIII, 2020-21, PwD  
  https://drive.google.com/file/d/1LbL_ltLvQTetLgBVuMtho0J7Byd_bivD/view?usp=drivesdk  
- Software Testing and Quality Assurance — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1WWdry-JOd4czEZkgG2APYMkTx41hdmj6/view?usp=drivesdk  
- AITISE — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/10sFZWM1mgFuR-ADxR92aOMEsx1fbjGIU/view?usp=drivesdk  
- DCC — ISE, Sem VIII, 2020-21, PwD  
  https://drive.google.com/file/d/1u8wcoU6zn51osEUMOTdkL1Cg3iXfkjoW/view?usp=drivesdk  
- DCC — ISE, Sem VIII, 2020-21  
  https://drive.google.com/file/d/1Qd9xOhBr7wD35k_irLKKPofUNgbLF0Ho/view?usp=drivesdk
```

### 22. AI paper sem 6

- Category: `filters`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'ai', 'semester': 6}`
- Retrieval: 54 ms · 3 paper(s)
- Qwen3 8B: 9.7 s

Papers found:

- Artificial Intelligence — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1djTOaEfjT43TP26QJTzE4M5ypBWSEkFI/view?usp=drivesdk
- Artificial Intelligence — ISE, Sem VI, 2021-22  
  https://drive.google.com/file/d/1qIK8vZDECtcsBmTLaMudDPa3mmnkwji8/view?usp=drivesdk
- Artificial Intelligence — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1ZR1g_-25Ji9ju3htsgJLlpWpHTyEzpTd/view?usp=drivesdk

Answer:

```
Artificial Intelligence — ISE, Sem VI, 2024-25  
https://drive.google.com/file/d/1djTOaEfjT43TP26QJTzE4M5ypBWSEkFI/view?usp=drivesdk  

Artificial Intelligence — ISE, Sem VI, 2021-22  
https://drive.google.com/file/d/1qIK8vZDECtcsBmTLaMudDPa3mmnkwji8/view?usp=drivesdk  

Artificial Intelligence — ISE, Sem VI, 2020-21  
https://drive.google.com/file/d/1ZR1g_-25Ji9ju3htsgJLlpWpHTyEzpTd/view?usp=drivesdk
```

### 23. give me OOPM paper 2025

- Category: `filters`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'oopm', 'year': 2025}`
- Retrieval: 40 ms · 1 paper(s)
- Qwen3 8B: 4.3 s

Papers found:

- Object Oriented Programming Methodology — ISE, Sem III, 2024-25  
  https://drive.google.com/file/d/122cc57KTEy97xYZmDznGcneLwTZem8AV/view?usp=drivesdk

Answer:

```
- Object Oriented Programming Methodology — ISE, Sem III, 2024-25  
  https://drive.google.com/file/d/122cc57KTEy97xYZmDznGcneLwTZem8AV/view?usp=drivesdk
```

### 24. give me TY papers

- Category: `track`  ·  Status: **Completed**
- Filters extracted: `{'year_of_study': 'TY'}`
- Retrieval: 56 ms · 50 paper(s)
- Qwen3 8B: 63.0 s

Papers found:

- Applied Cryptography — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1loFGIh56qKC3ZOAJDeietJ-gR0kGgbp7/view?usp=drivesdk
- Artificial Intelligence — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1djTOaEfjT43TP26QJTzE4M5ypBWSEkFI/view?usp=drivesdk
- Cloud Computing — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1q_ItzuW7iJcz1o98BlcX1H-OyDPeDmiV/view?usp=drivesdk
- Digital Signal and Image Processing — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1FlICjdxr_xphPKJ4vWVzVJv9QoR3woxW/view?usp=drivesdk
- German — ISE, Sem VI, 2024-25, Open Elective  
  https://drive.google.com/file/d/1_I6sg3SeRQjgZM4o_ValkyCPhIw6U9B3/view?usp=drivesdk
- Information Security — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1jGjfmjNB_O7yNd4npYJ_UZmarL6bDi7J/view?usp=drivesdk
- ADM — ISE, Sem VI, 2024-25, Honours  
  https://drive.google.com/file/d/1SCRFmBTSvH7eLLICTua5OXdKxwxelG70/view?usp=drivesdk
- AMLT — ISE, Sem VI, 2024-25, Open Elective  
  https://drive.google.com/file/d/1n_tezzisr_cnEtWnzz_x4d5GB0id4hZm/view?usp=drivesdk
- VAPT — ISE, Sem VI, 2024-25, Honours  
  https://drive.google.com/file/d/1nAAuXCOjRdeRJwpAyHBP0wxVaZaMW1wK/view?usp=drivesdk
- Computer Graphics — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/13cWmT80KIZB7TDXTUm4yB7xOPmsBy1Ea/view?usp=drivesdk
- Data Analytics — ISE, Sem V, 2024-25, Honours  
  https://drive.google.com/file/d/15nW5d2D5y5PJSzRJHXWfMnKebF9QiVhP/view?usp=drivesdk
- Operating Systems — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk
- Operating Systems — ISE, Sem V, 2024-25, Minor  
  https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk
- Soft Computing — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1y96qSCajVf4AJa8-XEqOGLkEuYNbzR6s/view?usp=drivesdk
- Supply Chain Management — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1Lo-YYH5BoDnopypRMNKKMAoR9nXPvG1L/view?usp=drivesdk
- BCT — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1dPEZrRsNekZ5k5HazrQ6QutPYD8SCsbt/view?usp=drivesdk
- EEFM — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1bW486S2-QZvu9x5oBkEfOHNZyKVib23c/view?usp=drivesdk
- FUTTER — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1sgpB-n4ZpajoLUCfHOSqI9a4L7CwMrJd/view?usp=drivesdk
- IMCT — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1MBA0y_Fpm4nxDbrB7QPbWXbAwrUIqxa6/view?usp=drivesdk
- Artificial Intelligence — ISE, Sem V, 2023-24, Minor  
  https://drive.google.com/file/d/1KKp2Ls832sOuf7ON376yLeHlXOgvFG9S/view?usp=drivesdk
- Computer Graphics — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/18eL5wt5kXQSOxFVFNH78hs1yzK2CVtuG/view?usp=drivesdk
- Computer Networks — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1DfjeKjMKXLoJmVuR2b7kV_bpjb3hBxAG/view?usp=drivesdk
- Consumer Behaviour — ISE, Sem V, 2023-24, Open Elective  
  https://drive.google.com/file/d/19A9RVJ_D_WFZQCKHEWD0w_lBW1z_B1P3/view?usp=drivesdk
- Data Analytics — ISE, Sem V, 2023-24, Honours  
  https://drive.google.com/file/d/1WGC-zf_HPJGI8MuAvJ__erhaUuRbhEAL/view?usp=drivesdk
- Mobile Application Development — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1SUAOP7YrhfJDpxP3p_RrZommu8Cz8wCr/view?usp=drivesdk
- Operating Systems — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1XGYyCyVJWWpeqKWmoMCRjargjs9kqqUd/view?usp=drivesdk
- Operating Systems — ISE, Sem V, 2023-24, Minor  
  https://drive.google.com/file/d/18_GHVAMFUg5l8kdg12fSIe4lImGa5xA3/view?usp=drivesdk
- Soft Computing — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1g3GyqXdrHd3xyou0Y-nWOcfjEsD1NsZR/view?usp=drivesdk
- Software Engineering — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/1cXPFgJxqlSrt2eC8ML5yRojZJihiFVNT/view?usp=drivesdk
- BCT — ISE, Sem V, 2023-24, Honours  
  https://drive.google.com/file/d/1kow94wBJIcIfC05qvysDmseB5vhUmF9g/view?usp=drivesdk
- IMGT — ISE, Sem V, 2023-24, Open Elective  
  https://drive.google.com/file/d/1xU0U1kaYagVLUvfV0lVwaRF27kXgtyRS/view?usp=drivesdk
- Artificial Intelligence — ISE, Sem VI, 2021-22  
  https://drive.google.com/file/d/1qIK8vZDECtcsBmTLaMudDPa3mmnkwji8/view?usp=drivesdk
- Cryptography and System Security — ISE, Sem VI, 2021-22  
  https://drive.google.com/file/d/1qIK8vZDECtcsBmTLaMudDPa3mmnkwji8/view?usp=drivesdk
- Digital Signal and Image Processing — ISE, Sem VI, 2021-22  
  https://drive.google.com/file/d/1qIK8vZDECtcsBmTLaMudDPa3mmnkwji8/view?usp=drivesdk
- Artificial Intelligence — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1ZR1g_-25Ji9ju3htsgJLlpWpHTyEzpTd/view?usp=drivesdk
- Augmented and Virtual Reality — ISE, Sem V, 2021-22  
  https://drive.google.com/file/d/19pEvqswXJWe7i0B5xiNqde6jUJXTRQcY/view?usp=drivesdk
- Computer Graphics and Virtual Reality Systems — ISE, Sem V, 2021-22  
  https://drive.google.com/file/d/1XwcitxbeBbUOaKu6A9RACJ4xRcWWU46Z/view?usp=drivesdk
- Computer Graphics and Virtual Reality Systems — ISE, Sem V, 2021-22  
  https://drive.google.com/file/d/1wr1z_pEXdQaf3bJnIyUH17soMytxf1mx/view?usp=drivesdk
- Computer Networks — ISE, Sem V, 2021-22, PwD  
  https://drive.google.com/file/d/1h5DHpnsY9XQZJF5zNvpP5-eDGzNN_apJ/view?usp=drivesdk
- Computer Networks — ISE, Sem V, 2021-22  
  https://drive.google.com/file/d/15cNzpvYB2Qj0I0XmjQT2gN6XzQtF-exm/view?usp=drivesdk
- Consumer Behaviour — ISE, Sem V, 2021-22, Open Elective  
  https://drive.google.com/file/d/1l3rjYcSqLWMbxe6ozxkGKRK7_VV-OW1E/view?usp=drivesdk
- Cryptography and System Security — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1QWO7s-BWm28K4t3cMzu9i6u7aWAjhBnx/view?usp=drivesdk
- Data Mining and Business Intelligence — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1qgDCCETnEKZ_BUDJk-5CBdNzMYbNY-SE/view?usp=drivesdk
- Digital Signal and Image Processing — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/1gda-ziy3ALRnz6erEYu70vc_qfP8jqsv/view?usp=drivesdk
- Goods and Services Marketing — ISE, Sem V, 2021-22, Open Elective  
  https://drive.google.com/file/d/1Kngp9nmFTwotKtUkE88BXv5OqfejjV-P/view?usp=drivesdk
- Machine Learning — ISE, Sem VI, 2020-21  
  https://drive.google.com/file/d/12_A2LbfS1UgRfZ1FKSNNsp_ai2IsJzlO/view?usp=drivesdk
- Microprocessor — ISE, Sem V, 2021-22, Dept Elective  
  https://drive.google.com/file/d/1eukRh9kLwY5rG7-I6E3WcHRhguyV0clF/view?usp=drivesdk
- Mobile Application Development — ISE, Sem V, 2021-22, Open Elective, PwD  
  https://drive.google.com/file/d/1ddGln35yFFywr7uoBtwFPoI9CCJ4rS_u/view?usp=drivesdk
- Mobile Application Development — ISE, Sem V, 2021-22, Open Elective  
  https://drive.google.com/file/d/1T99R7_p2nWUXdXyEqj6JJXzfKGZOE_wy/view?usp=drivesdk
- Open Source Software Systems — ISE, Sem V, 2021-22  
  https://drive.google.com/file/d/1wpbEADof423PkshtcauGYbFWd0J9wwHk/view?usp=drivesdk

Answer:

```
- Applied Cryptography — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1loFGIh56qKC3ZOAJDeietJ-gR0kGgbp7/view?usp=drivesdk  
- Artificial Intelligence — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1djTOaEfjT43TP26QJTzE4M5ypBWSEkFI/view?usp=drivesdk  
- Cloud Computing — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1q_ItzuW7iJcz1o98BlcX1H-OyDPeDmiV/view?usp=drivesdk  
- Digital Signal and Image Processing — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1FlICjdxr_xphPKJ4vWVzVJv9QoR3woxW/view?usp=drivesdk  
- German — ISE, Sem VI, 2024-25, Open Elective  
  https://drive.google.com/file/d/1_I6sg3SeRQjgZM4o_ValkyCPhIw6U9B3/view?usp=drivesdk  
- Information Security — ISE, Sem VI, 2024-25  
  https://drive.google.com/file/d/1jGjfmjNB_O7yNd4npYJ_UZmarL6bDi7J/view?usp=drivesdk  
- ADM — ISE, Sem VI, 2024-25, Honours  
  https://drive.google.com/file/d/1SCRFmBTSvH7eLLICTua5OXdKxwxelG70/view?usp=drivesdk  
- AMLT — ISE, Sem VI, 2024-25, Open Elective  
  https://drive.google.com/file/d/1n_tezzisr_cnEtWnzz_x4d5GB0id4hZm/view?usp=drivesdk  
- VAPT — ISE, Sem VI, 2024-25, Honours  
  https://drive.google.com/file/d/1nAAuXCOjRdeRJwpAyHBP0wxVaZaMW1wK/view?usp=drivesdk  
- Computer Graphics — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/13cWmT80KIZB7TDXTUm4yB7xOPmsBy1Ea/view?usp=drivesdk  
- Data Analytics — ISE, Sem V, 2024-25, Honours  
  https://drive.google.com/file/d/15nW5d2D5y5PJSzRJHXWfMnKebF9QiVhP/view?usp=drivesdk  
- Operating Systems — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/11GRvDDmy4iXbKIhku0PsU0wDuD8_OdAT/view?usp=drivesdk  
- Operating Systems — ISE, Sem V, 2024-25, Minor  
  https://drive.google.com/file/d/12-3RzQvQ3OPlTcQXvRngSpXcLGbnbxGx/view?usp=drivesdk  
- Soft Computing — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1y96qSCajVf4AJa8-XEqOGLkEuYNbzR6s/view?usp=drivesdk  
- Supply Chain Management — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1Lo-YYH5BoDnopypRMNKKMAoR9nXPvG1L/view?usp=drivesdk  
... and 35 more not listed here.
```

### 25. SY DBMS paper

- Category: `track`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'dbms', 'year_of_study': 'SY'}`
- Retrieval: 47 ms · 5 paper(s)
- Qwen3 8B: 17.9 s

Papers found:

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

Answer:

```
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

### 26. give me M.Tech papers

- Category: `track`  ·  Status: **Completed**
- Filters extracted: `{'year_of_study': 'MTECH'}`
- Retrieval: 43 ms · 7 paper(s)
- Qwen3 8B: 24.3 s

Papers found:

- Advanced Internet Technologies — ISE, Sem II, 2022-23  
  https://drive.google.com/file/d/1IU0SNd9Lz444mzJHqJNorEip8wdZWPfK/view?usp=drivesdk
- Machine Learning — ISE, Sem II, 2022-23  
  https://drive.google.com/file/d/1kuz4fD9aKcf7wv7Ag2SYyl-h5L4O-npD/view?usp=drivesdk
- Machine Learning — ISE, Sem II, 2022-23  
  https://drive.google.com/file/d/1D1L1chnStdvCI2owuyh4mkOKwXtk9u1K/view?usp=drivesdk
- Big Data Analytics — ISE, Sem II, 2021-22, Minor  
  https://drive.google.com/file/d/1NIcFI1v4LGy6uCvNsSJtYL_fP9OITlM0/view?usp=drivesdk
- Natural Language Processing — ISE, Sem II, 2021-22, Minor  
  https://drive.google.com/file/d/1H5YyeHkDCfb3hd3RiXrY7N5R2YqJG6Q4/view?usp=drivesdk
- User Experience Design — ISE, Sem II, 2021-22, Minor  
  https://drive.google.com/file/d/1-oYJOBXy2u8ohvyE4cgrqINyI9oyId38/view?usp=drivesdk
- BCT — ISE, Sem II, 2021-22, Minor  
  https://drive.google.com/file/d/1SLvJTa7pQ_6qRh9J1lE3uFi3hngHX6Cm/view?usp=drivesdk

Answer:

```
- Advanced Internet Technologies — ISE, Sem II, 2022-23  
  https://drive.google.com/file/d/1IU0SNd9Lz444mzJHqJNorEip8wdZWPfK/view?usp=drivesdk  
- Machine Learning — ISE, Sem II, 2022-23 (1 pg)  
  https://drive.google.com/file/d/1kuz4fD9aKcf7wv7Ag2SYyl-h5L4O-npD/view?usp=drivesdk  
- Machine Learning — ISE, Sem II, 2022-23 (2 pg)  
  https://drive.google.com/file/d/1D1L1chnStdvCI2owuyh4mkOKwXtk9u1K/view?usp=drivesdk  
- Big Data Analytics — ISE, Sem II, 2021-22, Minor  
  https://drive.google.com/file/d/1NIcFI1v4LGy6uCvNsSJtYL_fP9OITlM0/view?usp=drivesdk  
- Natural Language Processing — ISE, Sem II, 2021-22, Minor  
  https://drive.google.com/file/d/1H5YyeHkDCfb3hd3RiXrY7N5R2YqJG6Q4/view?usp=drivesdk  
- User Experience Design — ISE, Sem II, 2021-22, Minor  
  https://drive.google.com/file/d/1-oYJOBXy2u8ohvyE4cgrqINyI9oyId38/view?usp=drivesdk  
- BCT — ISE, Sem II, 2021-22, Minor  
  https://drive.google.com/file/d/1SLvJTa7pQ_6qRh9J1lE3uFi3hngHX6Cm/view?usp=drivesdk
```

### 27. give me all honours papers

- Category: `track`  ·  Status: **Completed**
- Filters extracted: `{'category': 'honours'}`
- Retrieval: 44 ms · 15 paper(s)
- Qwen3 8B: 59.5 s

Papers found:

- Applied Cryptography — ISE, Sem IV, 2024-25, Honours  
  https://drive.google.com/file/d/1XiYynz9lMTs8abrWw0lyeJXKUDm3TUTh/view?usp=drivesdk
- ADM — ISE, Sem VI, 2024-25, Honours  
  https://drive.google.com/file/d/1SCRFmBTSvH7eLLICTua5OXdKxwxelG70/view?usp=drivesdk
- IDS — ISE, Sem IV, 2024-25, Honours  
  https://drive.google.com/file/d/14cCFjXcSosmRm14kc76iSdkox7w329H_/view?usp=drivesdk
- VAPT — ISE, Sem VI, 2024-25, Honours  
  https://drive.google.com/file/d/1nAAuXCOjRdeRJwpAyHBP0wxVaZaMW1wK/view?usp=drivesdk
- Data Analytics — ISE, Sem V, 2024-25, Honours  
  https://drive.google.com/file/d/15nW5d2D5y5PJSzRJHXWfMnKebF9QiVhP/view?usp=drivesdk
- ADS — ISE, Sem IV, 2023-24, Honours  
  https://drive.google.com/file/d/1h_A7iLrSiQUBSeVpU8SwKgsGa_ualnNb/view?usp=drivesdk
- AML — ISE, Sem VII, 2024-25, Honours  
  https://drive.google.com/file/d/1BEjIWBcUE2uD1LmPxtXjB4AVbYids_Gj/view?usp=drivesdk
- CSFC — ISE, Sem IV, 2023-24, Honours  
  https://drive.google.com/file/d/1XWlrsMKIj-KOWZ7EKp9_Iy6SoYakPk8V/view?usp=drivesdk
- SEC — ISE, Sem VII, 2024-25, Honours  
  https://drive.google.com/file/d/1HIVY7Sc_LCPtVRS5gizOCO8dclGVKgRc/view?usp=drivesdk
- Applied Cryptography — ISE, Sem III, 2023-24, Honours  
  https://drive.google.com/file/d/1DJhdMBnsyImraUkY1hiceKIPDKUQLgjk/view?usp=drivesdk
- Data Analytics — ISE, Sem V, 2023-24, Honours  
  https://drive.google.com/file/d/1WGC-zf_HPJGI8MuAvJ__erhaUuRbhEAL/view?usp=drivesdk
- Data Visualization — ISE, Sem III, 2023-24, Honours  
  https://drive.google.com/file/d/1dNi5oZ9FfIMZIeuihMh2AW4MgIf-mM1z/view?usp=drivesdk
- BCT — ISE, Sem V, 2023-24, Honours  
  https://drive.google.com/file/d/1kow94wBJIcIfC05qvysDmseB5vhUmF9g/view?usp=drivesdk
- Applied Cryptography — ISE, Sem III, 2021-22, Honours  
  https://drive.google.com/file/d/18LTYnUvrNEZ-QTi-pruHvQWIOJfWyuS_/view?usp=drivesdk
- Data Visualization — ISE, Sem III, 2021-22, Honours  
  https://drive.google.com/file/d/1PEbjdVvQHIpLyvCObJ0ogFBxWYlfXc6u/view?usp=drivesdk

Answer:

```
- Applied Cryptography — ISE, Sem IV, 2024-25, Honours  
  https://drive.google.com/file/d/1XiYynz9lMTs8abrWw0lyeJXKUDm3TUTh/view?usp=drivesdk  
- ADM — ISE, Sem VI, 2024-25, Honours  
  https://drive.google.com/file/d/1SCRFmBTSvH7eLLICTua5OXdKxwxelG70/view?usp=drivesdk  
- IDS — ISE, Sem IV, 2024-25, Honours  
  https://drive.google.com/file/d/14cCFjXcSosmRm14kc76iSdkox7w329H_/view?usp=drivesdk  
- VAPT — ISE, Sem VI, 2024-25, Honours  
  https://drive.google.com/file/d/1nAAuXCOjRdeRJwpAyHBP0wxVaZaMW1wK/view?usp=drivesdk  
- Data Analytics — ISE, Sem V, 2024-25, Honours  
  https://drive.google.com/file/d/15nW5d2D5y5PJSzRJHXWfMnKebF9QiVhP/view?usp=drivesdk  
- ADS — ISE, Sem IV, 2023-24, Honours  
  https://drive.google.com/file/d/1h_A7iLrSiQUBSeVpU8SwKgsGa_ualnNb/view?usp=drivesdk  
- AML — ISE, Sem VII, 2024-25, Honours  
  https://drive.google.com/file/d/1BEjIWBcUE2uD1LmPxtXjB4AVbYids_Gj/view?usp=drivesdk  
- CSFC — ISE, Sem IV, 2023-24, Honours  
  https://drive.google.com/file/d/1XWlrsMKIj-KOWZ7EKp9_Iy6SoYakPk8V/view?usp=drivesdk  
- SEC — ISE, Sem VII, 2024-25, Honours  
  https://drive.google.com/file/d/1HIVY7Sc_LCPtVRS5gizOCO8dclGVKgRc/view?usp=drivesdk  
- Applied Cryptography — ISE, Sem III, 2023-24, Honours  
  https://drive.google.com/file/d/1DJhdMBnsyImraUkY1hiceKIPDKUQLgjk/view?usp=drivesdk  
- Data Analytics — ISE, Sem V, 2023-24, Honours  
  https://drive.google.com/file/d/1WGC-zf_HPJGI8MuAvJ__erhaUuRbhEAL/view?usp=drivesdk  
- Data Visualization — ISE, Sem III, 2023-24, Honours  
  https://drive.google.com/file/d/1dNi5oZ9FfIMZIeuihMh2AW4MgIf-mM1z/view?usp=drivesdk  
- BCT — ISE, Sem V, 2023-24, Honours  
  https://drive.google.com/file/d/1kow94wBJIcIfC05qvysDmseB5vhUmF9g/view?usp=drivesdk  
- Applied Cryptography — ISE, Sem III, 2021-22, Honours  
  https://drive.google.com/file/d/18LTYnUvrNEZ-QTi-pruHvQWIOJfWyuS_/view?usp=drivesdk  
- Data Visualization — ISE, Sem III, 2021-22, Honours  
  https://drive.google.com/file/d/1PEbjdVvQHIpLyvCObJ0ogFBxWYlfXc6u/view?usp=drivesdk
```

### 28. minor AI paper

- Category: `track`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'ai', 'category': 'minor'}`
- Retrieval: 19 ms · 1 paper(s)
- Qwen3 8B: 11.6 s

Papers found:

- Artificial Intelligence — ISE, Sem V, 2023-24, Minor  
  https://drive.google.com/file/d/1KKp2Ls832sOuf7ON376yLeHlXOgvFG9S/view?usp=drivesdk

Answer:

```
Artificial Intelligence — ISE, Sem V, 2023-24, Minor  
https://drive.google.com/file/d/1KKp2Ls832sOuf7ON376yLeHlXOgvFG9S/view?usp=drivesdk
```

### 29. PwD DS paper

- Category: `track`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'ds', 'variant': 'pwd'}`
- Retrieval: 31 ms · 1 paper(s)
- Qwen3 8B: 4.8 s

Papers found:

- Data Structures — ISE, Sem III, 2021-22, PwD  
  https://drive.google.com/file/d/1Gr-q0QW6AWI-9X4v5ChKz4ioybOMv21H/view?usp=drivesdk

Answer:

```
Data Structures — ISE, Sem III, 2021-22, PwD  
https://drive.google.com/file/d/1Gr-q0QW6AWI-9X4v5ChKz4ioybOMv21H/view?usp=drivesdk
```

### 30. open elective papers

- Category: `track`  ·  Status: **Completed**
- Filters extracted: `{'category': 'open_elective'}`
- Retrieval: 87 ms · 15 paper(s)
- Qwen3 8B: 61.1 s

Papers found:

- German — ISE, Sem VI, 2024-25, Open Elective  
  https://drive.google.com/file/d/1_I6sg3SeRQjgZM4o_ValkyCPhIw6U9B3/view?usp=drivesdk
- AMLT — ISE, Sem VI, 2024-25, Open Elective  
  https://drive.google.com/file/d/1n_tezzisr_cnEtWnzz_x4d5GB0id4hZm/view?usp=drivesdk
- Consumer Behaviour — ISE, Sem V, 2023-24, Open Elective  
  https://drive.google.com/file/d/19A9RVJ_D_WFZQCKHEWD0w_lBW1z_B1P3/view?usp=drivesdk
- IMGT — ISE, Sem V, 2023-24, Open Elective  
  https://drive.google.com/file/d/1xU0U1kaYagVLUvfV0lVwaRF27kXgtyRS/view?usp=drivesdk
- Consumer Behaviour — ISE, Sem V, 2021-22, Open Elective  
  https://drive.google.com/file/d/1l3rjYcSqLWMbxe6ozxkGKRK7_VV-OW1E/view?usp=drivesdk
- Development of Religious Thought — ISE, Sem VII, 2021-22, Open Elective  
  https://drive.google.com/file/d/19jpbKv0DK637qdjyI4owUDt3uVT-Eoid/view?usp=drivesdk
- Goods and Services Marketing — ISE, Sem V, 2021-22, Open Elective  
  https://drive.google.com/file/d/1Kngp9nmFTwotKtUkE88BXv5OqfejjV-P/view?usp=drivesdk
- Human Values and Jainism — ISE, Sem VII, 2021-22, Open Elective  
  https://drive.google.com/file/d/1rLNztMieadoBftIDa19WBC2-2lTJyYgy/view?usp=drivesdk
- Mobile Application Development — ISE, Sem V, 2021-22, Open Elective, PwD  
  https://drive.google.com/file/d/1ddGln35yFFywr7uoBtwFPoI9CCJ4rS_u/view?usp=drivesdk
- Mobile Application Development — ISE, Sem V, 2021-22, Open Elective  
  https://drive.google.com/file/d/1T99R7_p2nWUXdXyEqj6JJXzfKGZOE_wy/view?usp=drivesdk
- Python for Data Science — ISE, Sem V, 2021-22, Open Elective  
  https://drive.google.com/file/d/1y_SygnOVrMf0IHM_D6mLgxVka5AhQiHd/view?usp=drivesdk
- aml programming — ISE, Sem VI, 2020-21, Open Elective  
  https://drive.google.com/file/d/1VW-8JINUZAv0lFz3MCmJAB3hjTYB7I6l/view?usp=drivesdk
- aml theory — ISE, Sem VI, 2020-21, Open Elective  
  https://drive.google.com/file/d/10GCDoO62ozXVvMMnFC4-8XbXHi802tyw/view?usp=drivesdk
- SMAC — ISE, Sem VI, 2020-21, Open Elective  
  https://drive.google.com/file/d/1FHZnk1eBHj1zzCer0OkxsQEF3-SymPBm/view?usp=drivesdk
- Mobile Application Development (iOS) — ISE, Sem V, 2020-21, Open Elective  
  https://drive.google.com/file/d/1y0CMoWbj48Mg4GwDm3zE3zkiFP0cOYrN/view?usp=drivesdk

Answer:

```
- German — ISE, Sem VI, 2024-25, Open Elective  
  https://drive.google.com/file/d/1_I6sg3SeRQjgZM4o_ValkyCPhIw6U9B3/view?usp=drivesdk  
- AMLT — ISE, Sem VI, 2024-25, Open Elective  
  https://drive.google.com/file/d/1n_tezzisr_cnEtWnzz_x4d5GB0id4hZm/view?usp=drivesdk  
- Consumer Behaviour — ISE, Sem V, 2023-24, Open Elective  
  https://drive.google.com/file/d/19A9RVJ_D_WFZQCKHEWD0w_lBW1z_B1P3/view?usp=drivesdk  
- IMGT — ISE, Sem V, 2023-24, Open Elective  
  https://drive.google.com/file/d/1xU0U1kaYagVLUvfV0lVwaRF27kXgtyRS/view?usp=drivesdk  
- Consumer Behaviour — ISE, Sem V, 2021-22, Open Elective  
  https://drive.google.com/file/d/1l3rjYcSqLWMbxe6ozxkGKRK7_VV-OW1E/view?usp=drivesdk  
- Development of Religious Thought — ISE, Sem VII, 2021-22, Open Elective  
  https://drive.google.com/file/d/19jpbKv0DK637qdjyI4owUDt3uVT-Eoid/view?usp=drivesdk  
- Goods and Services Marketing — ISE, Sem V, 2021-22, Open Elective  
  https://drive.google.com/file/d/1Kngp9nmFTwotKtUkE88BXv5OqfejjV-P/view?usp=drivesdk  
- Human Values and Jainism — ISE, Sem VII, 2021-22, Open Elective  
  https://drive.google.com/file/d/1rLNztMieadoBftIDa19WBC2-2lTJyYgy/view?usp=drivesdk  
- Mobile Application Development — ISE, Sem V, 2021-22, Open Elective, PwD  
  https://drive.google.com/file/d/1ddGln35yFFywr7uoBtwFPoI9CCJ4rS_u/view?usp=drivesdk  
- Mobile Application Development — ISE, Sem V, 2021-22, Open Elective  
  https://drive.google.com/file/d/1T99R7_p2nWUXdXyEqj6JJXzfKGZOE_wy/view?usp=drivesdk  
- Python for Data Science — ISE, Sem V, 2021-22, Open Elective  
  https://drive.google.com/file/d/1y_SygnOVrMf0IHM_D6mLgxVka5AhQiHd/view?usp=drivesdk  
- aml programming — ISE, Sem VI, 2020-21, Open Elective  
  https://drive.google.com/file/d/1VW-8JINUZAv0lFz3MCmJAB3hjTYB7I6l/view?usp=drivesdk  
- aml theory — ISE, Sem VI, 2020-21, Open Elective  
  https://drive.google.com/file/d/10GCDoO62ozXVvMMnFC4-8XbXHi802tyw/view?usp=drivesdk  
- SMAC — ISE, Sem VI, 2020-21, Open Elective  
  https://drive.google.com/file/d/1FHZnk1eBHj1zzCer0OkxsQEF3-SymPBm/view?usp=drivesdk  
- Mobile Application Development (iOS) — ISE, Sem V, 2020-21, Open Elective  
  https://drive.google.com/file/d/1y0CMoWbj48Mg4GwDm3zE3zkiFP0cOYrN/view?usp=drivesdk
```

### 31. give me ITVC paper

- Category: `unresolved`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'itvc'}`
- Retrieval: 83 ms · 4 paper(s)
- Qwen3 8B: 15.4 s

Papers found:

- ITVC — ISE, Sem III, 2024-25  
  https://drive.google.com/file/d/1SezKMUGyrPn6-aUdPhnWjgnLyan-IXwE/view?usp=drivesdk
- ITVC — ISE, Sem III, 2023-24  
  https://drive.google.com/file/d/1FS3NNR8OR5A4pCeK0Muy8TBDSDdBgCXD/view?usp=drivesdk
- ITVC — ISE, Sem III, 2021-22  
  https://drive.google.com/file/d/1qIvy4qCYs-dQ4ZCYSTBsky-Mw8pYDpZh/view?usp=drivesdk
- ITVC — ISE, Sem III, 2020-21  
  https://drive.google.com/file/d/1GvUsH3oZ8wTPNPc2cxPtWBh3ol5fda7I/view?usp=drivesdk

Answer:

```
- ITVC — ISE, Sem III, 2024-25  
  https://drive.google.com/file/d/1SezKMUGyrPn6-aUdPhnWjgnLyan-IXwE/view?usp=drivesdk  
- ITVC — ISE, Sem III, 2023-24  
  https://drive.google.com/file/d/1FS3NNR8OR5A4pCeK0Muy8TBDSDdBgCXD/view?usp=drivesdk  
- ITVC — ISE, Sem III, 2021-22  
  https://drive.google.com/file/d/1qIvy4qCYs-dQ4ZCYSTBsky-Mw8pYDpZh/view?usp=drivesdk  
- ITVC — ISE, Sem III, 2020-21  
  https://drive.google.com/file/d/1GvUsH3oZ8wTPNPc2cxPtWBh3ol5fda7I/view?usp=drivesdk
```

### 32. give me BCT paper

- Category: `unresolved`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'bct'}`
- Retrieval: 27 ms · 5 paper(s)
- Qwen3 8B: 17.1 s

Papers found:

- BCT — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1dPEZrRsNekZ5k5HazrQ6QutPYD8SCsbt/view?usp=drivesdk
- BCT — ISE, Sem VII, 2024-25  
  https://drive.google.com/file/d/1qyHUhixRZY3xkCcwVMR6sSNNIHF1qvDx/view?usp=drivesdk
- BCT — ISE, Sem V, 2023-24, Honours  
  https://drive.google.com/file/d/1kow94wBJIcIfC05qvysDmseB5vhUmF9g/view?usp=drivesdk
- BCT — ISE, Sem II, 2021-22, Minor  
  https://drive.google.com/file/d/1SLvJTa7pQ_6qRh9J1lE3uFi3hngHX6Cm/view?usp=drivesdk
- BCT — ISE, Sem VII, 2021-22  
  https://drive.google.com/file/d/1nIF-KFrAGgQI-EfrQiF7qe6097AD_OkL/view?usp=drivesdk

Answer:

```
- BCT — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/1dPEZrRsNekZ5k5HazrQ6QutPYD8SCsbt/view?usp=drivesdk  
- BCT — ISE, Sem VII, 2024-25  
  https://drive.google.com/file/d/1qyHUhixRZY3xkCcwVMR6sSNNIHF1qvDx/view?usp=drivesdk  
- BCT — ISE, Sem V, 2023-24, Honours  
  https://drive.google.com/file/d/1kow94wBJIcIfC05qvysDmseB5vhUmF9g/view?usp=drivesdk  
- BCT — ISE, Sem II, 2021-22, Minor  
  https://drive.google.com/file/d/1SLvJTa7pQ_6qRh9J1lE3uFi3hngHX6Cm/view?usp=drivesdk  
- BCT — ISE, Sem VII, 2021-22  
  https://drive.google.com/file/d/1nIF-KFrAGgQI-EfrQiF7qe6097AD_OkL/view?usp=drivesdk
```

### 33. give me DM paper

- Category: `unresolved`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'dm'}`
- Retrieval: 37 ms · 3 paper(s)
- Qwen3 8B: 10.0 s

Papers found:

- DM — ISE, Sem III, 2023-24  
  https://drive.google.com/file/d/1aiiD6VMHfBrcCvixVXcAXy5ZaLtKnvFd/view?usp=drivesdk
- DM — ISE, Sem III, 2021-22, PwD  
  https://drive.google.com/file/d/1d_pCihKLTuNMeCIMOPL0ysGg1s6s1Rwx/view?usp=drivesdk
- DM — ISE, Sem III, 2021-22  
  https://drive.google.com/file/d/1kHOXiW2ZbF5xkKZdy1xTpjSVCEyT64NT/view?usp=drivesdk

Answer:

```
- DM — ISE, Sem III, 2023-24  
  https://drive.google.com/file/d/1aiiD6VMHfBrcCvixVXcAXy5ZaLtKnvFd/view?usp=drivesdk  
- DM — ISE, Sem III, 2021-22, PwD  
  https://drive.google.com/file/d/1d_pCihKLTuNMeCIMOPL0ysGg1s6s1Rwx/view?usp=drivesdk  
- DM — ISE, Sem III, 2021-22  
  https://drive.google.com/file/d/1kHOXiW2ZbF5xkKZdy1xTpjSVCEyT64NT/view?usp=drivesdk
```

### 34. give me PSOT paper 2021-22

- Category: `multi`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'psot', 'year': 2021}`
- Retrieval: 37 ms · 3 paper(s)
- Qwen3 8B: 3.8 s

Papers found:

- Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2021-22  
  https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk
- Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2020-21, PwD  
  https://drive.google.com/file/d/1B4jWAF8awXQR10EwC7ihxMU5A7cjofgx/view?usp=drivesdk
- Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/1IW2puX_65JCtpZ-RlbU8C1nI6YwSc0rR/view?usp=drivesdk

Answer:

```
- Probability, Statistics and Optimization Techniques — ISE, Sem IV, 2021-22  
  https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk
```

### 35. give me TACD paper

- Category: `multi`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'tacd'}`
- Retrieval: 59 ms · 3 paper(s)
- Qwen3 8B: 10.7 s

Papers found:

- Theory of Automata and Compiler Design — ISE, Sem IV, 2023-24  
  https://drive.google.com/file/d/1bqzzNVLOGcEYIw-uzpGpxVkBncwdDSYF/view?usp=drivesdk
- Theory of Automata and Compiler Design — ISE, Sem IV, 2021-22  
  https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk
- Theory of Automata and Compiler Design — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/1BbUD5_NDbijmYQi3IoQitJuqHSoUzHpf/view?usp=drivesdk

Answer:

```
- Theory of Automata and Compiler Design — ISE, Sem IV, 2023-24  
  https://drive.google.com/file/d/1bqzzNVLOGcEYIw-uzpGpxVkBncwdDSYF/view?usp=drivesdk  
- Theory of Automata and Compiler Design — ISE, Sem IV, 2021-22  
  https://drive.google.com/file/d/1xo4l5NFN5bwp-EPo1Fq7dcVoCUdziQcx/view?usp=drivesdk  
- Theory of Automata and Compiler Design — ISE, Sem IV, 2020-21  
  https://drive.google.com/file/d/1BbUD5_NDbijmYQi3IoQitJuqHSoUzHpf/view?usp=drivesdk
```

### 36. can you send me the operating systems paper please

- Category: `phrasing`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'os'}`
- Retrieval: 69 ms · 5 paper(s)
- Qwen3 8B: 16.3 s

Papers found:

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

Answer:

```
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

### 37. I need last year's DBMS question paper

- Category: `phrasing`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'dbms'}`
- Retrieval: 43 ms · 5 paper(s)
- Qwen3 8B: 7.1 s

Papers found:

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

Answer:

```
- Database Management System — ISE, Sem IV, 2023-24  
  https://drive.google.com/file/d/1PHe3j7OCb63hnFQf4MIguMNoDyAkrf3f/view?usp=drivesdk  
- Database Management System — ISE, Sem IV, 2024-25  
  https://drive.google.com/file/d/1LzMSNrHgqFj_4_2VQ45iqxe1Q5b30_mp/view?usp=drivesdk
```

### 38. do you have any computer graphics papers

- Category: `phrasing`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'cg'}`
- Retrieval: 46 ms · 2 paper(s)
- Qwen3 8B: 7.3 s

Papers found:

- Computer Graphics — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/13cWmT80KIZB7TDXTUm4yB7xOPmsBy1Ea/view?usp=drivesdk
- Computer Graphics — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/18eL5wt5kXQSOxFVFNH78hs1yzK2CVtuG/view?usp=drivesdk

Answer:

```
- Computer Graphics — ISE, Sem V, 2024-25  
  https://drive.google.com/file/d/13cWmT80KIZB7TDXTUm4yB7xOPmsBy1Ea/view?usp=drivesdk  
- Computer Graphics — ISE, Sem V, 2023-24  
  https://drive.google.com/file/d/18eL5wt5kXQSOxFVFNH78hs1yzK2CVtuG/view?usp=drivesdk
```

### 39. give me ESE DBMS paper

- Category: `miss`  ·  Status: **Completed**
- Filters extracted: `{'subject_key': 'dbms', 'exam_type': 'ESE'}`
- Retrieval: 25 ms · 0 paper(s)

Answer:

```
(no papers: ese_not_ingested)
```

### 40. give me organic chemistry paper

- Category: `miss`  ·  Status: **Completed**
- Filters extracted: `{}`
- Retrieval: 0 ms · 0 paper(s)

Answer:

```
(no papers: unknown_subject)
```


# DOCUMENT.md — `data/mcqs/`

## What lives here

The MCQ bank for Quiz mode — one JSON file per lecture plus the topic taxonomy.
**Not embedded**: loaded into memory at app startup and filtered exactly by
lecture / topic / difficulty.

## Current state (Curated — 2026-06-10)

The live bank is a **500-question curated selection** (one `lecture-NN-<slug>.json`
per lecture, 50 questions each) drawn from the full 4,337-question bank, which now
lives **losslessly in `data/mcqs-archive/`** (all 20 original files, moved
unchanged — see that folder's DOCUMENT.md for restore instructions). Passes the
`validate_mcqs.py` gate ("10 file(s) valid").

Every curated question was copied **byte-for-byte** from the archive (IDs
preserved, content untouched; verified by span-level integrity check). Set-2
questions (IDs ≥ `LNN-Q501`, perspective-shifted) are mixed into the per-lecture
files alongside set-1 (direct-recall) questions — the validator and quiz loader
are filename-agnostic, so no code change was needed.

**Selection criteria** (applied per lecture, ~50 each):
- Difficulty mix exactly easy 20% / medium 40% / hard 30% / very-hard 10%
  (10/20/15/5 per lecture).
- Recall (set-1) vs perspective-shifted (set-2) ≈ 60/40 (actual 292/208 overall;
  per-lecture varies ±25% where topic spread or de-dup constraints won).
- Topic spread across each lecture's taxonomy topics, weighted toward
  exam-emphasized material (refactoring, code smells, testing, CI/CD, clean
  code/architecture, version control, technical debt/decision-making).
- No near-duplicate stems within the curated set (Jaccard > 0.6 on normalized
  stem word sets rejected).
- Preference for questions with substantive, quotable explanations.
- L01 includes `Q029`/`Q030` (verified-correct after the 2026-06-10 Capers Jones
  correction).

| Lecture | Curated | set-1 | set-2 |
|---------|---------|-------|-------|
| L01 | 50 | 30 | 20 |
| L02 | 50 | 30 | 20 |
| L03 | 50 | 31 | 19 |
| L04 | 50 | 22 | 28 |
| L05 | 50 | 31 | 19 |
| L06 | 50 | 30 | 20 |
| L07 | 50 | 30 | 20 |
| L09 | 50 | 23 | 27 |
| L10 | 50 | 35 | 15 |
| L11 | 50 | 30 | 20 |
| **Total** | **500** | **292** | **208** |

### Full-bank history (now archived)

The full bank shipped as **two parallel sets** totalling **4,337 questions**
(set-1 `lecture-*.json` 2,337 direct-recall; set-2 `lecture-*-v2.json` 2,000
perspective-shifted across 10 archetypes, IDs offset at `LNN-Q501`). Per-lecture
counts: L01 279, L02 472, L03 472, L04 491, L05 504, L06 550, L07 541, L09 325,
L10 369, L11 334. All 20 files were moved byte-identically to
`data/mcqs-archive/` on 2026-06-10.

`_taxonomy.md` — controlled 16-topic `topic` vocabulary + lecture→topic map +
difficulty scale; feeds the (bank-derived) UI filter chips. Applies to both sets.

Lectures 8 and 12 have no materials, so there is **no** `lecture-08-*` /
`lecture-12-*` file in either set (out of scope, by user decision).

## Schema & quality rules (from architecture §4)

- **File shape:** `{ lecture_id, lecture_num, lecture_title, generated_from[],
  schema_version, questions[] }`.
- **Question shape:** stable `id` (`L04-Q001`), `lecture_id`, `topic` (from the
  closed taxonomy), `difficulty` (`easy|medium|hard|very-hard`), `stem`, exactly 4
  `options`, one correct `answer`, `explanation` (defeats every distractor, ends in
  a citation), `source` (`{deck, page}`), optional `tags`.
- **Quality gates** (`validate_mcqs.py`): valid schema, 4 options, exactly one
  answer, no duplicate stems within/across lectures, citation present,
  difficulty/topic in vocabulary.
- **Answer hygiene:** `answer` + `explanation` are withheld by `/api/quiz` and only
  revealed by `/api/quiz/check`.

## How it connects

`quiz.py` loads `data/mcqs/*.json` (env `MCQ_ROOT`) at startup into an in-memory
index, pre-bucketed by `lecture_id` and `difficulty` — the glob now picks up the
10 curated per-lecture files (`data/mcqs-archive/` is outside the glob and is
**not** loaded). `validate_mcqs.py` gates the bank at build time. `_taxonomy.md`
is the shared source for both the quiz topic filter and the search topic filter.
Mounted read-only at `/data/mcqs`. The app must be restarted/re-ingested for the
curated bank to take effect (handled by the backend engineer).

## Content corrections

- **2026-06-10 — L01 Capers Jones figures (10× fix).** The Introduction deck's
  "Agile Approach" table (PDF p.18, slide footer 17/28; Jones 1996, IEEE Computer)
  gives monthly requirements-change rates of **1.0 / 1.5 / 2.0 / 2.0 / 3.5 %** —
  the bank previously taught 10/15/20/35 %. Corrected in set-1
  `lecture-01-...json` (Q029 explanation; Q030/Q031/Q032 options + explanations)
  and set-2 `lecture-01-...-v2.json` (Q562 options + explanation; Q614
  explanation). Counts unchanged (149 + 130); gate re-run green
  ("20 file(s) valid"). These corrected files now live in `data/mcqs-archive/`;
  the corrected `Q029`/`Q030` were carried into the curated bank.

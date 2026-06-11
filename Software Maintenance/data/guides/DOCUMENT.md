# DOCUMENT.md — `data/guides/`

## What lives here

The per-lecture study-guide markdown — the **embedded search corpus** for Lookup
mode. One file per lecture, kebab-case and zero-padded, plus an overview/appendix
and five `9N-*` exam-preparation guides (three exam guides + two lab deep-dives).

## Current state (Shipped 2026-06-09; deepened in place 2026-06-10; exam guides added 2026-06-10; lab deep-dives added 2026-06-11)

Landed: **`00-overview.md` + 10 per-lecture guides + 3 exam guides + 2 lab
deep-dive guides** (~274k words across the lecture guides, ~3.4k in the overview,
~44k across the exam guides, ~30.4k across the lab deep-dives — **16 content
files, ~352k words total**), fully cited. Each lecture guide keeps the original
9 core H2 sections and adds deep-dive H2 sections on top (9–19 H2s per guide).
Present:

| File                                   | Purpose                                                      |
|----------------------------------------|--------------------------------------------------------------|
| `00-overview.md`                       | Course map + bibliography (`[Raj13]`, `[Fowler99]`, …) + change-process phase diagram. |
| `lecture-01-introduction-version-control.md` | L01 — intro & version control / Git |
| `lecture-02-software-change-concept-location.md` | L02 — software change, concept location, JHotDraw |
| `lecture-03-impact-analysis-processes-ci.md` | L03 — impact analysis, processes, CI |
| `lecture-04-refactoring-maintainable-code.md` | L04 — refactoring & maintainable code |
| `lecture-05-actualization-clean-architecture.md` | L05 — actualization, clean architecture, OO principles |
| `lecture-06-clean-code-design-patterns.md` | L06 — clean code & design patterns |
| `lecture-07-software-testing.md` | L07 — software testing |
| `lecture-09-bdd-verification.md` | L09 — BDD / verification |
| `lecture-10-conclusion-worked-example.md` | L10 — conclusion + Drawlets worked example |
| `lecture-11-technical-debt.md` | L11 — technical debt |
| `90-exam-what-to-expect.md` | Exam logistics & strategy (~3.3k words) — format, question list, how to prepare |
| `91-exam-model-answers.md` | Exam model answers (~15k words) — one H2 per exam question: copy-paste answer + justification add-ons + adapt-to-your-lab + key terms |
| `92-exam-copy-paste-library.md` | Exam copy-paste library (~25.5k words) — catalogs of reusable definitions, examples, comparisons and citations |
| `93-lab-deep-dives-1.md` | Lab deep-dives 1 (17,245 words) — Lectures 1–3 labs (Intro, Git, Change Request, Concept Location, Impact Analysis, CI): one H2 per lab with 7 fixed H3s (assignment, walkthrough, justifications, copy-paste reflection, likely exam questions, pitfalls, theory links) |
| `94-lab-deep-dives-2.md` | Lab deep-dives 2 (13,200 words) — Lectures 4–9 labs (Refactoring, Actualization, Testing, BDD), same H2-per-lab structure, exam-heaviest labs covered deepest |

Lectures 8 and 12 have no source materials, so there is **no** `lecture-08-*.md` /
`lecture-12-*.md` (out of scope, by user decision). These 16 files are embedded into
the `software_maintenance` ChromaDB collection (**2,130 chunks**, re-ingested
2026-06-11) by `ingest.py`.

The five `9N-*` guides (90/91/92 exam series + 93/94 lab deep-dives) are **not tied
to a lecture**: their filenames do not match `lecture-NN-*`, so the ingest identity
rule falls back to slug-derived deck titles ("Lab Deep Dives 1", "Lab Deep Dives 2",
…) and their Lookup result cards carry **no lecture badge** (by design).

## Content corrections

- **2026-06-10 — `91-exam-model-answers.md` Q5 retrievability (App Tester P2).**
  The section under the verbatim H2 `## Why did you structure it that way?` never
  surfaced for its own query: the chunker strips heading lines, so the embedded
  chunk text is the body only, and the pronoun-heavy H2 gave the embedder no
  signal. Fix: the "Copy-paste answer" body now **opens by naming its subject
  explicitly** ("Why did I structure my CI pipeline that way? Because every
  structural choice in the pipeline — the pull-request trigger, the Maven
  build-and-test stages, and the merge gate — follows a CI principle. …"). The H2
  line itself is byte-identical (plan §7 requirement), the paragraph stays within
  the 450-token chunk budget (one chunk, not split), and no other section was
  touched. Verified live post-re-ingest: the chunk ranks #1 for its own query.

## Conventions (from architecture §3)

- **Section structure.** Each guide is H1 + H2/H3: the original 9 core H2 sections
  (Overview, Learning Objectives, Key Concepts, JHotDraw Connection, Worked Example,
  Definitions, Common Pitfalls, Exam Focus, Source Map) are preserved, with added
  deep-dive H2 sections per lecture (9–19 H2s per guide). `##` H2 headings are the
  primary chunk boundary, so each section must stand alone.
- **Citations everywhere.** Every non-obvious claim ends with `(Deck p.X)`; readings
  use literature keys defined once in `00-overview.md`.
- **Numeric, zero-padded names.** `lecture-04-refactoring.md`, etc.

## How it connects

`ingest.py` globs `data/guides/*.md` (numerically sorted), runs `chunk_markdown`
(size-bounded: H2 → H3 → paragraph-window → sentence cascade, ≤~450 tokens per
chunk), embeds with bge-small, and writes the `software_maintenance` ChromaDB
collection. Mounted read-only at `/data/guides` in the `ingest` container.

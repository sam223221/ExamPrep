# AI Exam Prep — Study Package Design

**Date:** 2026-05-22
**Author:** PM (Claude Code)
**Status:** Draft → User Review
**Project root:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI`

---

## 1. Goal

Convert the existing AI exam-prep folder (10 lecture PDFs, 11 labs, supporting datasets and templates) into a complete, exam-ready study package consisting of:

1. **10 textbook-quality lecture study PDFs** — one per lecture, covering every concept, formula, and worked example from the source slides, written for self-study by someone preparing for the final exam.
2. **1 master index PDF** — full table of contents, cross-reference graph, glossary, and a recommended study order.
3. **Solved versions of every lab** — saved as `*_solution.{py|ipynb}` alongside the original templates, with inline `# KNOB:` comments documenting every tunable variable and a header docstring containing the original problem statement and a "how to adapt for variants" guide.
4. **Verification artifacts** — proof that every solution runs and every PDF renders.

The user (Sam) must be able to (a) open any lecture PDF and learn the topic from scratch, and (b) open any solved lab and answer a new variant of the exam question by changing only the `# KNOB:` values, without studying the implementation internals.

## 2. Scope

### In scope

- Read every lecture PDF in `AI/` page-by-page and extract a comprehensive textbook chapter per lecture.
- Read every lab handout PDF and template file, solve the lab, document tunable parameters.
- Build a shared glossary and cross-reference map across all lectures.
- Generate PDFs from markdown via WeasyPrint (with documented fallbacks).
- Run multi-reviewer loops on every artifact until reviewers are satisfied.
- Stress-test every lab with 3 "exam agent" variants that must succeed using only docstring + KNOB comments.
- Verifier pass: execute every solution, confirm every PDF renders.

### Out of scope

- Modifying original lecture PDFs or lab template files (they stay untouched).
- Generating an additional walkthrough PDF per lab (problem statement is embedded in solution file instead).
- Re-recording lectures, producing videos, or audio summaries.
- Building a quiz/flashcard app.
- Translating content to another language.
- Maintaining the study package once exams are over.

### User-facing acceptance criteria

- Opening any `study/lectures/L{N}-*.pdf` provides a self-contained chapter that covers every slide of the source PDF without needing to re-open the original.
- Opening any `*_solution.{py|ipynb}` shows: (a) the full problem statement, (b) the relevant lecture reference, (c) every adjustable variable explicitly tagged with `# KNOB:`, (d) a "how to adapt for variant questions" block.
- Running any `*_solution.py` from the command line, or running every cell of any `*_solution.ipynb`, completes without error and produces the expected output.
- A naive reader who only reads the header docstring + KNOB comments of a lab can solve a previously-unseen variant of that lab's exam question by changing KNOB values.

## 3. Project Source Inventory

Confirmed by the exploration pass on 2026-05-22:

### Lectures (10 PDFs at root)

| File | Topic |
|---|---|
| Lecture2-Introduction to Agents.pdf | Agents |
| Lecture3-Uninformed Search.pdf | Uninformed Search (BFS, DFS) |
| Lecture5-Local Search.pdf | Local Search (hill climbing, simulated annealing, GA) |
| Lecture6-Adversarial Search.pdf | Adversarial Search (minimax, alpha-beta) |
| Lecture7-Constraint Satisfaction Problem.pdf | CSPs |
| Lecture9-Bayesian Networks.pdf | Bayesian Networks |
| Lecture9-Hidden Markov Models.pdf | HMMs |
| Lecture10-Introduction to Machine Learning.pdf | ML overview |
| Lecture11-Regression.pdf | Regression |
| Lecture12-Clustering.pdf | Clustering |

### Labs (11 total — 8 algorithm labs in folders, 3 ML labs as notebooks)

| Lab | Location | Type | Templates |
|---|---|---|---|
| Lab 1 — Agents | `Lab1-Agents/` + `Lab 1.pdf` | `.py` files | `reflex_vacuum_agent.py`, `reflex_agent_with_state.py`, `table_driven_agent.py`, `Enums.py` |
| Lab 2 — Search | `Lab 2/` | `.py` | `Search.py` |
| Lab 4 — Genetic Algorithms | `handout_lab_4/` | `.py` | `ga.py`, `Number.py`, `Queen.py`, `queens_fitness.py` |
| Lab 5 — Alpha-Beta / Tic-Tac-Toe | `handout/handout/` | `.py` | `alpha_beta.py`, `tictactoe_template.py` |
| Lab 6 — CSP | `lab6/` | `.py` | `constraints_template.py`, `Colors.py`, `States.py` |
| Lab 7 — Bayesian Networks | `Lab7/handout/` | `.py` | `bn.py`, `Variable.py`, `Runner.py` |
| Lab 8 — HMM | `Lab 8/handout/` | `.py` | `hidden_markov_models.py` |
| ML Lab 1 — Classification | `lab1_classification_handout.ipynb` (root) | `.ipynb` | TODO-driven cells |
| ML Lab 2 — Regression | `lab2_regression_handout.ipynb` (root) | `.ipynb` | TODO-driven cells |
| ML Lab 3 — Clustering | `lab3_clustering_handout.ipynb` (root) | `.ipynb` | TODO-driven cells |

Lab numbering note: there are TWO independent "Lab 1" series (the algorithm-lab "Lab 1 — Agents" and the ML-notebook "ML Lab 1 — Classification"). They are treated as separate labs throughout.

## 4. Output Structure

```
AI/
├── (originals — UNTOUCHED)
├── docs/
│   └── superpowers/specs/
│       └── 2026-05-22-ai-exam-prep-study-package-design.md   # this file
├── study/
│   ├── _shared/
│   │   ├── glossary.md
│   │   ├── cross-references.md
│   │   ├── style.css
│   │   └── html-template.html
│   ├── _review/                          # per-artifact review reports
│   │   ├── L02/round1/reviewer{1-4}.md, revise-summary.md
│   │   ├── L02/round2/...
│   │   ├── ...
│   │   └── labs/Lab4-GA/round1/...
│   ├── _exam/                            # per-lab exam-agent runs
│   │   └── Lab4-GA/
│   │       ├── variants.md
│   │       ├── examiner1-attempt.md
│   │       ├── examiner2-attempt.md
│   │       └── examiner3-attempt.md
│   ├── _verification-report.md
│   ├── lectures/
│   │   ├── L02-Agents.md  L02-Agents.pdf
│   │   ├── L03-Uninformed-Search.md  L03-Uninformed-Search.pdf
│   │   ├── L05-Local-Search.md  L05-Local-Search.pdf
│   │   ├── L06-Adversarial-Search.md  L06-Adversarial-Search.pdf
│   │   ├── L07-CSP.md  L07-CSP.pdf
│   │   ├── L09a-Bayesian-Networks.md  L09a-Bayesian-Networks.pdf
│   │   ├── L09b-HMM.md  L09b-HMM.pdf
│   │   ├── L10-Intro-to-ML.md  L10-Intro-to-ML.pdf
│   │   ├── L11-Regression.md  L11-Regression.pdf
│   │   └── L12-Clustering.md  L12-Clustering.pdf
│   ├── extracted_figures/
│   │   ├── L02/, L03/, ... L12/         # PNGs lifted from lecture PDFs
│   ├── 00-master-index.md  00-master-index.pdf
│   └── render.py
└── (solution files alongside each lab template, e.g.):
    Lab1-Agents/reflex_vacuum_agent_solution.py
    Lab 2/Search_solution.py
    handout/handout/alpha_beta_solution.py
    handout/handout/tictactoe_template_solution.py
    handout_lab_4/ga_solution.py
    lab6/constraints_template_solution.py
    Lab7/handout/bn_solution.py  (and Runner_solution.py if needed)
    Lab 8/handout/hidden_markov_models_solution.py
    lab1_classification_solution.ipynb
    lab2_regression_solution.ipynb
    lab3_clustering_solution.ipynb
```

Originals are never modified. Every new file is either under `study/`, `docs/`, or named with `_solution` suffix beside the original template.

## 5. Orchestration — Approach B (glossary-first, then parallel) with review loops and exam agents

### 5.1 Waves

```
Wave 0  Glossary Skimmer                              serial, ~15 min
Wave 1  Lecture Extractor x10  ─┐
        Lab Solver x11          ├─ each with its own review loop, all parallel
                                │  Wave 1 ends when all 21 artifacts are LOCKED
                                ┘
Wave 2  Index Builder → its own review loop → PDF Renderer → Verifier
```

### 5.2 Wave 0 — Glossary Skimmer (1 agent, serial, ~15 min)

**Input:** all 10 lecture PDFs.

**Output:**
- `study/_shared/glossary.md` — canonical name for every concept introduced in any lecture, with a one-paragraph definition and the lecture(s) where it appears.
- `study/_shared/cross-references.md` — a directed graph of "concept introduced in L{X} is reused in L{Y}" relations, used by extractors to insert correct cross-links.

**Method:** shallow read (table of contents + section headers + first/last slide of each section). Not a full read — that's what Lecture Extractors are for.

### 5.3 Wave 1 — Lecture Extractor (10 agents, parallel, ~20–30 min each)

Each Lecture Extractor handles ONE lecture PDF. It is briefed with:
- The PDF path.
- The shared glossary and cross-references.
- The lecture-chapter template (see §6).
- An explicit instruction to read the entire PDF page-by-page, not skim.

**Output:** `study/lectures/L{N}-{Topic}.md` plus PNGs in `study/extracted_figures/L{N}/`.

Then the **lecture review loop** (§7) runs until the chapter is LOCKED.

### 5.4 Wave 1 — Lab Solver (11 agents, parallel, ~20–40 min each)

Each Lab Solver handles ONE lab. It is briefed with:
- All template files for that lab (paths).
- The lab handout PDF path.
- The relevant lecture(s) for context (lookup via `cross-references.md`).
- The shared glossary.
- The solution-file template (see §6.2).
- The KNOB convention (see §6.3).
- The variant bank curated for this lab (used later by exam agents — see §8.3).

**Output:** `*_solution.{py|ipynb}` files alongside originals.

Then the **lab review loop** (§8.1) runs, followed by the **exam-agent gate** (§8.2), until the lab is LOCKED.

### 5.5 Wave 2 — Index, Render, Verify

- **Index Builder** (1 agent, ~10 min): reads every locked lecture `.md`, writes `study/00-master-index.md` containing:
  - A full table of contents (every lecture, every major section, every concept) with links into the lecture `.md`s.
  - The complete `_shared/glossary.md` flattened into a single reference.
  - An **Analogies Index** — a one-page table that lists every concept and the one-line analogy used for it, grouped by lecture. This is what you flip to first when reviewing: read the analogy, then jump to the deep section if the analogy doesn't land.
  - A **Cross-reference graph** — a Mermaid diagram showing which lecture introduces a concept and which lectures reuse it.
  - A **Recommended study order** — suggested reading sequence with estimated time per chapter.
  - Then runs its own 4-reviewer loop (using the same template) until APPROVED.
- **PDF Renderer** (1 agent, ~10 min): writes `study/render.py`, installs WeasyPrint dependencies, renders every `.md` to a `.pdf` in the same directory.
- **Verifier** (1 agent, ~15 min): executes every `*_solution.py` and `*_solution.ipynb`, confirms every expected PDF exists, validates every cross-reference link. Writes `study/_verification-report.md`. If anything fails, dispatches targeted fixers and re-verifies.

## 6. Content Conventions

### 6.1 Lecture-chapter template (Markdown)

```markdown
# Lecture {N}: {Topic}

> **Reading time:** ~{X} min  |  **Prereqs:** {links to prior lectures}
> **Glossary terms introduced:** {list}

## 1. Overview & Motivation
Why this topic matters; what problem it solves; where it sits in the course.

## 2. The Big Picture — Analogies
A "mental model" section BEFORE any formalism. For each major concept in
this lecture, give a concrete, everyday analogy that captures the essence:

- **{Concept A} is like ...** — analogy in 2–4 sentences, plus a "where the
  analogy breaks down" caveat (every analogy has limits; calling them out
  prevents mis-learning).
- **{Concept B} is like ...** — etc.

Examples of the kind of analogies expected:
- A* search ↔ "GPS navigation that estimates remaining distance"
- Hidden Markov Model ↔ "you watch someone's umbrella every morning to
  guess if it's raining inside their house"
- Bayesian Network ↔ "a gossip graph where each person's mood depends on
  the moods of the people upstream from them"
- K-means clustering ↔ "asking N party-hosts to each claim the nearest
  guests, then repeatedly re-arranging until nobody wants to switch"
- Alpha-beta pruning ↔ "you stop reading a bad chess line the moment you
  realise it's worse than one you've already considered"

Prefer analogies grounded in everyday physical experience over analogies
that depend on other technical concepts.

## 3. Core Concepts
### 3.1 {Concept A}
Definition. Formal statement. Worked micro-example. Cross-link back to the
analogy in §2 ("recall the GPS-navigation analogy: the heuristic `h(n)` is
the GPS's distance estimate").
### 3.2 {Concept B}
...

## 4. Algorithms / Methods
Pseudocode (preserved from slides where given), complexity analysis,
when to use which method, comparison table.

## 5. Worked Examples
Every example from the lecture slides, fully expanded with all steps.

## 6. Common Pitfalls / Exam Traps
Frequently-tested mistakes, ambiguous notation, and edge cases.

## 7. Connections to Other Lectures
Cross-refs using canonical glossary terms, linking to the relevant section
in the other lecture's `.md`. Where useful, point out that "the analogy
from §2 also applies to {related concept in lecture Y}".

## 8. Cheat-Sheet Summary
One-page bullet/formula recap suitable for last-minute review. Each concept
on the cheat sheet carries a one-line analogy reminder in italics.

---
_Source: Lecture {N} slides {X}–{Y}._
```

**Conventions:**
- Math in LaTeX: `$inline$`, `$$display$$`. Pre-rendered to KaTeX HTML/SVG before WeasyPrint (WeasyPrint does not execute JS).
- **Figures from the source PDF are FIRST-CLASS content, not a fallback.** See §6.1.1 below for the full figure protocol.
- Code blocks: triple-fenced with language tag, runnable where applicable.
- Cross-refs: `[See L11 §3 — Polynomial Regression](L11-Regression.md#3-algorithms--methods)`. Verifier validates every link.
- Every section ends with `[Lecture {N}, slides {X}–{Y}]` so the reader can flip back to the source.

### 6.1.1 Figure extraction protocol (mandatory)

Every Lecture Extractor agent must:

1. **Enumerate every image, diagram, chart, table-as-image, and screenshot in the source PDF.** Use `PyMuPDF` (the `fitz` library) which reliably lists embedded images. Required dependency, pinned in `study/requirements.txt`:
   ```
   PyMuPDF==1.24.9
   Pillow==10.4.0
   ```
2. **Extract every image** to `study/extracted_figures/L{N}/fig{NN}-{short-slug}.png`. Filename uses zero-padded sequence number (`fig01`, `fig02`, ...) and a short kebab-case slug derived from nearby caption text. If a "figure" is actually a math equation rendered as an image, extract it anyway — Reviewer #2 will decide whether to keep it or re-typeset.
3. **Catalog every figure** in `study/extracted_figures/L{N}/figures.md` with:
   - filename
   - source page number in the PDF
   - the surrounding slide text / caption (for context)
   - the agent's relevance verdict: **USE** / **REWORK** / **SKIP**
     - **USE:** figure is referenced in the chapter as-is.
     - **REWORK:** figure is useful but unclear / low-res / cluttered — agent supplements with a Mermaid diagram or describes it in prose alongside.
     - **SKIP:** figure is decorative (institutional logos, slide-template ornaments, photos of the lecturer, irrelevant clip-art).
   - rationale (1–2 sentences) for the verdict
4. **Embed every USE and REWORK figure** in the chapter `.md` at the appropriate section, with markdown image syntax and a caption:
   ```markdown
   ![Caption explaining the figure and what to look at](../extracted_figures/L{N}/fig07-search-tree.png)
   _Figure 7: a search tree where dotted arrows are pruned by alpha-beta. (Lecture {N}, slide 23.)_
   ```
5. **For REWORK figures**, also add either a Mermaid diagram or a prose description alongside, so the reader has a backup if the extracted image is unclear.
6. **Never silently drop a figure.** If a figure is genuinely SKIP-worthy, the rationale in `figures.md` must justify it.

Whole-PDF-page screenshots (rendering an entire slide as PNG) are a permitted fallback when image-level extraction fails — handled by `fitz.Page.get_pixmap()`. Tag any such fallback in `figures.md` as `EXTRACTION_METHOD: page-render`.

### 6.2 Solution-file header template

Each `*_solution.{py|ipynb}` opens with:

```python
"""
LAB N: <Title>
==============

PROBLEM STATEMENT (from Lab N.pdf):
-----------------------------------
<full extracted problem statement, verbatim where possible>

MENTAL MODEL (one-line analogy):
--------------------------------
{This lab is like ...} — a short concrete analogy reminding you what
problem this code is really solving. Pulled from / consistent with the
analogy used in the corresponding lecture chapter §2.

REFERENCES:
-----------
- Lecture {X} §{Y}: {Topic} — see study/lectures/L{X}-...md
- Related glossary terms: {list}

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
1. To solve <variant A>: set KNOB_X = ..., KNOB_Y = ...
2. To solve <variant B>: set KNOB_Z = ...
3. To change the problem size: ...
4. To trade accuracy for speed: ...

OUTPUTS WHEN RUN:
-----------------
<one-line description of what the script prints/produces>

ENTRY POINT: yes | no
---------------------
- "yes" if running this file directly (`python <file>`) demonstrates the lab.
- "no" if this file is a helper module imported by another solution file.
  When "no", state which file is the entry point.
"""
```

For `.ipynb` files, the same header lives in the first markdown cell. Notebooks are always entry points (Verifier executes them whole).

**Multi-file labs:** when a lab has several template files that form one system (e.g. Lab 1 has three reflex-agent files, Lab 5 has `alpha_beta.py` + `tictactoe_template.py`), the Lab Solver designates **one** file as the entry point and the rest as modules. The entry-point file imports from the modules and contains an `if __name__ == "__main__":` block that exercises the system end-to-end.

### 6.3 KNOB convention

Every tunable parameter — anything whose value changes the behaviour or output — is tagged with a `# KNOB:` block immediately above its definition:

```python
# KNOB: N_QUEENS (default=4, allowed=any positive int >= 4)
#   What it does: board size for the N-Queens problem.
#   Effect: search space grows roughly as N!. N=4 finishes instantly;
#           N=12 may take seconds; N>=20 is hard with naive GA.
#   Exam variants: 4-queens (default), 8-queens (set 8), 12-queens (set 12).
N_QUEENS = 4

# KNOB: POPULATION_SIZE (default=100, range=10–10000)
#   What it does: size of the GA population each generation.
#   Effect: larger = better exploration, slower per generation.
#   Exam variants: tune to 50 for "speed-sensitive" framing, 500 for
#                  "find best solution" framing.
POPULATION_SIZE = 100
```

KNOB rules every Lab Solver follows:
- Replace every `raise NotImplementedError(...)` with a working implementation.
- Tag every parameter that affects results. Reviewer #2 (KNOB Coverage) actively hunts for magic numbers buried in function bodies.
- Comments inside function bodies explain WHY, never WHAT.
- Function signatures from the template are preserved exactly (Reviewer #1 enforces this).
- Notebooks: each TODO cell gets a code solution + a preceding markdown cell explaining the approach.
- The solver runs the solution at least once before marking it done.

## 7. Lecture Review Loop

For each lecture chapter, before it is LOCKED:

```
Lecture Extractor produces v1
         │
         ▼
4 parallel Critical Reviewers (distinct lenses)
         │
   any reviewer reports P0 or P1?
         ├─ yes ─► Reviser agent (reads all 4 reports + current draft)
         │              │ produces v2
         │              └─► back to 4 reviewers
         └─ all 4 APPROVED with zero P0/P1 ─► LOCKED, proceeds to render
```

### 7.1 The 4 reviewers

| # | Role | Hunts For |
|---|---|---|
| 1 | **Concept Completeness (incl. Figures)** | Cross-checks every slide in the source PDF against the `.md`. Flags any concept, definition, or topic-bullet missing or under-covered. Specifically: does the chapter cover **every** slide section, **every** named concept, **every** formula shown? **Also audits figures**: opens `study/extracted_figures/L{N}/figures.md`, confirms every USE / REWORK figure is actually embedded in the chapter at a sensible location, every SKIP verdict is justified, and no informative figure from the source PDF was missed. Flags figures that are present in the catalogue but not used in the chapter, or referenced in the chapter but missing from the catalogue. |
| 2 | **Mathematical Rigor** | Verifies every formula matches the source. Catches missing derivation steps, wrong indices, ambiguous notation, dropped assumptions, mismatched variable names. |
| 3 | **Pedagogical Clarity (incl. Analogies)** | Reads as a confused student. Flags hand-waving, unjustified leaps, undefined terms, missing intuition, examples that don't illustrate the concept. **Also enforces analogies**: every major concept must have at least one concrete everyday analogy in §2, each cross-linked from its formal definition in §3, with a "where the analogy breaks down" caveat. Reviewer flags weak or missing analogies and may demand replacement analogies. |
| 4 | **Exam Readiness** | Reads as someone writing the exam. Flags missing worked examples, ignored edge cases, inaccurate cheat-sheet, thin common-pitfalls section. |

### 7.2 Reviewer brief

Every reviewer is briefed with:
- The original lecture PDF path.
- The current `.md` draft path.
- Their specific lens (one of the 4 above).
- An explicit instruction to be **harsh**: false positives are cheap, missed concepts are expensive.
- Output format: `study/_review/L{N}/round{R}/reviewer{1-4}.md` with sections:
  - **VERDICT:** `APPROVED` or `NEEDS_REVISION`
  - **P0 — MUST FIX (blocks approval):** concrete bullet list with line references
  - **P1 — SHOULD FIX (requested, not blocking):** bullet list
  - **P2 — NICE TO HAVE:** bullet list
  - **EVIDENCE:** which slides / which sections of `.md` were inspected

### 7.3 Reviser brief

When at least one reviewer returns `NEEDS_REVISION`, a single Reviser agent is dispatched with:
- The current `.md` draft.
- All 4 reviewer reports from this round (even APPROVED ones — they may contain P2 items).
- An instruction to address every P0 and P1, and to consider every P2.
- Output: revised `.md` + a `revise-summary.md` listing what was changed and which reviewer comment each change addresses.

### 7.4 Approval rule

A lecture is LOCKED only when, in a single round, **all 4 reviewers** return `VERDICT: APPROVED` **with zero P0 and zero P1** items. P2 items are recorded but never block.

### 7.5 Loop bound

Soft target: ≤5 rounds per lecture. If round 5 still has P0/P1, the PM is paged with a summary and decides: continue, accept with caveat (and document it), or escalate.

## 8. Lab Review Loop + Exam Agents

For each lab, two gates must pass: the 4-reviewer gate, and the 3-exam-agent gate.

```
Lab Solver produces v1
        │
        ▼
4 parallel Critical Reviewers
        │
        ├─ revisions needed ──► Reviser ──► back to 4 reviewers
        │
        ▼ (all 4 APPROVED, zero P0/P1)
3 parallel Exam Agents — each given a DIFFERENT variant question
        │
        │ Each examiner:
        │  • Reads ONLY the docstring header + KNOB blocks + signatures
        │  • Is forbidden from reading function bodies, helper modules,
        │    or the lab handout PDF
        │  • Must modify KNOBs (or call signatures, if exposed) to solve
        │  • Reports: SOLVED (answer + KNOB diff) / STUCK (with what was unclear)
        │
   all 3 SOLVED?
        ├─ no ─► Reviser improves the docstring and/or KNOB documentation
        │       (rarely the implementation) ─► back to 4 reviewers
        │       ─► back to a FRESH batch of 3 exam agents
        │
        └─ yes ─► LOCKED
```

### 8.1 The 4 lab reviewers

| # | Role | Hunts For |
|---|---|---|
| 1 | **Correctness** | Runs the code (or every cell of the notebook). Verifies the original lab problem is solved. Catches off-by-one, wrong loop conditions, broken edge cases, wrong outputs, broken signatures. |
| 2 | **KNOB Coverage** | Audits every parameter. Is each `# KNOB:` block complete (default + range + effect + variants)? Are there hidden magic numbers in function bodies that should have been promoted to KNOBs? |
| 3 | **Pedagogical Clarity** | Are comments useful? Is the header docstring clear? Could a student understand WHY without reading deep into the code? |
| 4 | **Variant Adaptability** | Reads the lab handout PDF + the curated variant bank for this lab. Predicts plausible exam variants and checks whether current KNOBs + docstring are enough to solve them without rewriting any function. |

Reviewer brief, reviser brief, approval rule, and loop bound are identical in structure to §7.2–§7.5, with reports written to `study/_review/labs/{LabName}/round{R}/`.

### 8.2 The 3 exam agents

Each exam agent is briefed independently with:
- The path to the locked `*_solution.{py|ipynb}` file.
- Their assigned variant question (one of three from the variant bank).
- Hard constraints:
  - **Readable:** the docstring header, KNOB comment blocks, function signatures (the `def ...:` line), and any **data files** the lab consumes (CSVs, JSON datasets, images used as inputs).
  - **Forbidden:** function bodies, class bodies, helper modules' source code, the lab handout PDF, the lecture PDFs, the lecture `.md` files, the solution code of other labs.
  - You **must** declare the exact KNOB changes you plan to make BEFORE running.
  - You **must** run the modified solution and report the final answer.
  - If you cannot solve the variant within the constraints, report `STUCK` and explain precisely what was unclear (which KNOB was missing, which variant the docstring didn't anticipate, etc.).
- Output: `study/_exam/{LabName}/examiner{1-3}-attempt.md` containing:
  - `VARIANT:` the variant they were given (verbatim)
  - `KNOB CHANGES:` diff of values they touched
  - `RUN OUTPUT:` captured stdout
  - `ANSWER:` their final answer
  - `VERDICT:` `SOLVED` or `STUCK`
  - `STUCK REASON:` (if applicable) what was missing from the documentation

### 8.3 Variant banks (initial; Lab Solvers may extend)

| Lab | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|
| 1 — Agents | Add a new sensor type to the environment | Different room layout (3-room) | Stateless vs stateful reflex comparison |
| 2 — Search | 8-puzzle instead of the given problem | Switch heuristic (Manhattan ↔ Euclidean) | New start/goal pair on the same map |
| 4 — GA (Queens) | 8-queens instead of 4-queens | Change mutation rate, observe convergence | Different fitness function (penalize column conflicts more) |
| 5 — Alpha-Beta / TicTacToe | Change tree-depth limit | Different evaluator function | Reorder move generation to test pruning |
| 6 — CSP | Different map (e.g. Iceland regions) | Add a 5th color | Change constraint set (adjacency vs distance) |
| 7 — BN | Different evidence values | Query a different node | Add a new variable to the network |
| 8 — HMM | Different observation sequence | Different transition matrix | Compute filtered vs smoothed posterior |
| ML 1 — Classification | Different `max_depth` | Random Forest with different `n_estimators` | Different feature subset |
| ML 2 — Regression | Higher polynomial degree | Drop a feature, observe degradation | Predict for a new input row |
| ML 3 — Clustering | Different K | Different feature pairs | Different initialization (k-means++ vs random) |

Variant banks are stored at `study/_exam/{LabName}/variants.md` and may be expanded by the Lab Solver if it identifies obvious additional variants from the handout.

### 8.4 Approval rule

A lab is LOCKED only when, in a single sequence, all 4 reviewers `APPROVED` with zero P0/P1 **AND** all 3 exam agents reported `SOLVED`.

If any exam agent reports `STUCK`, the Reviser is dispatched with the stuck-reason and asked to improve the documentation (rarely the implementation). The 4-reviewer loop then re-runs, followed by a **fresh** batch of 3 exam agents on the same variants.

## 9. Security & Data Considerations

- No external network calls except `pip install`. All datasets are already local (synthetic, baked into notebooks).
- No user data, no PII, no secrets handled.
- Solutions write to disk only under `AI/study/`, `AI/docs/`, and beside originals (named `*_solution.*`). No deletes, no overwrites of originals.
- WeasyPrint and dependencies are pinned to specific versions in a `requirements.txt` under `study/`.
- Verifier executes notebooks via `jupyter nbconvert --execute`; notebooks run synthetic data only.

## 10. Rendering Pipeline

`study/render.py` (written by PDF Renderer agent):

1. Reads every `study/lectures/*.md` and `study/00-master-index.md`.
2. For each, pre-processes math: extracts `$...$` and `$$...$$`, renders to inline HTML/MathML via the **primary** path `pip install pylatexenc` + `markdown-katex` extension. If those fail, fall back to the `pyppeteer` + headless-Chrome rendering of KaTeX, then final fallback to plain `\(...\)` text (math still readable, just not typeset).
3. Converts to HTML via `markdown` + `pymdown-extensions` (tables, fenced code, footnotes, attr_list, def_list, arithmatex for math passthrough).
4. Wraps in `_shared/html-template.html` with `_shared/style.css`. The stylesheet sets `img { max-width: 100%; height: auto; page-break-inside: avoid; }` so extracted slide figures scale to the printable area without overflow and don't split awkwardly across pages. Figure captions use `figure` / `figcaption` styling and stay attached to their image.
5. Runs WeasyPrint to produce a PDF beside each `.md`. WeasyPrint handles PNG natively via standard `<img>` tags — no additional configuration needed for embedded figures.

Exact pinned requirements (Renderer agent writes `study/requirements.txt`, shared by Lecture Extractors for figure extraction and by the Verifier for notebook execution):
```
weasyprint==62.3
markdown==3.6
pymdown-extensions==10.9
markdown-katex==202406.1035
Pygments==2.18.0
jupyter==1.0.0
nbconvert==7.16.4
PyMuPDF==1.24.9
Pillow==10.4.0
```

Wave 0 (Glossary Skimmer) installs this file first so every downstream agent can rely on the same toolchain.

**Fallback chain** (declared upfront, not improvised):
- If WeasyPrint fails to install (known GTK runtime issue on Windows): fall back to `pdfkit` + `wkhtmltopdf`.
- If `wkhtmltopdf` is also unavailable: emit styled HTML, instruct user to Print → PDF in their browser. Renderer agent reports which path was taken.

## 11. Verification

Verifier agent runs last and produces `study/_verification-report.md`:

1. **Solution execution:** for every lab, run the designated **entry-point file** declared in that lab's `_solution.py` docstring under the heading `ENTRY POINT:`. If a lab has multiple solution files (e.g. Lab 1 — Agents has three separate reflex agents), every solution file declares whether it is an entry point or a module; Verifier runs every entry point. For every `*_solution.ipynb`, run `jupyter nbconvert --to notebook --execute --inplace=false` and confirm zero cells errored.
2. **PDF presence:** confirm every expected PDF exists and is > 50 KB.
3. **Cross-reference resolution:** parse every `.md` for `[...](...)` links into other `.md` files, confirm targets exist and anchor (where present) resolves.
4. **KNOB sanity:** for each `*_solution.py` and the code cells of each `*_solution.ipynb`, parse for `# KNOB:` comments and confirm at least one is present (every lab has at least one tunable).
5. **Function signature preservation:** for each `*_solution.py`, parse top-level `def` and `class` declarations; confirm every name from the original template still exists with a matching signature (parameter names and order preserved; default values may change).
6. **Figure integrity:** for each lecture `.md`, parse every `![...](../extracted_figures/...)` reference and confirm the file exists and is > 1 KB (catches broken paths and zero-byte extraction failures). Confirm `study/extracted_figures/L{N}/figures.md` exists and lists at least one `USE` or `REWORK` figure for every lecture whose source PDF contains figures (effectively all of them — Reviewer #1 already ensures coverage; this check is a final safety net).

Failure handling: any item that fails triggers the PM to dispatch a targeted fixer for that single artifact, then Verifier re-runs the failing checks only. Loop until clean.

## 12. PM Loop Controller (the orchestration brain)

The PM (me, this Claude Code session) is the loop controller. The PM's responsibilities:

1. Dispatch Glossary Skimmer; wait; absorb output.
2. Dispatch all 10 Lecture Extractors and all 11 Lab Solvers in **parallel** (single message, multiple `Agent` tool calls).
3. For each artifact, when the implementer reports back, dispatch the 4 reviewers in **parallel**.
4. When reviewer reports return, decide: LOCKED (all APPROVED, zero P0/P1) or REVISE.
5. If REVISE: dispatch Reviser with all 4 reports + current draft; loop to step 3.
6. For LOCKED lab artifacts: dispatch the 3 Exam Agents in **parallel**. If any STUCK, dispatch Reviser with the stuck-reason, loop to step 3 (back to reviewers).
7. When all 21 artifacts are LOCKED: dispatch Index Builder; run its own review loop; then Renderer; then Verifier.
8. On any Verifier failure: dispatch targeted fixer; re-verify.
9. On project completion: write a final `study/00-DONE.md` summarising what shipped and any open P2 items.

The PM never reads or writes lecture/lab content itself. Every concrete action is delegated.

## 13. Cost & Time Estimate

| | Optimistic | Likely | Pessimistic |
|---|---|---|---|
| Rounds per lecture | 2 | 3 | 5 |
| Rounds per lab (reviewer gate) | 2 | 3 | 5 |
| Exam-agent retries per lab | 0 | 1 | 2 |
| Total agent invocations | ~250 | ~400 | ~700 |
| Wall-clock time | ~2 hr | ~3–4 hr | ~6+ hr |

The user has explicitly requested taking as much time as needed. Pessimistic ceiling is acceptable.

## 14. Hard Exit Criteria

A lecture is "done" only when:
- All 4 reviewers `VERDICT: APPROVED` with zero P0 and zero P1 in the same round.
- Verifier confirms PDF rendered and is > 50 KB.
- Every cross-reference link from this lecture resolves.
- §2 "The Big Picture — Analogies" exists and contains an analogy for every major concept introduced in the lecture (enforced by Reviewer #3).
- Every informative figure from the source PDF is either embedded (USE / REWORK) or has a justified SKIP verdict in `study/extracted_figures/L{N}/figures.md` (enforced by Reviewer #1).
- All embedded figure files exist and are non-empty (enforced by Verifier).

A lab is "done" only when:
- All 4 reviewers `VERDICT: APPROVED` with zero P0 and zero P1.
- All 3 exam agents reported `SOLVED` on their distinct variant in the most recent batch.
- Verifier ran the solution end-to-end without error.
- Verifier confirmed the original template's public function signatures are preserved.
- The "MENTAL MODEL (one-line analogy)" line in the docstring header exists and is consistent with the analogy used in the corresponding lecture chapter.

The whole project is done only when every lecture, every lab, AND the master index pass their respective gates, AND the Verifier report is fully green.

## 15. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| WeasyPrint won't install on Windows (GTK runtime issue) | Documented fallback chain to `pdfkit` then to HTML-only (§10). Renderer agent reports which path was taken. |
| PyMuPDF image-level extraction misses a figure that is a slide-level composite (text + shapes + images on one slide) | Fallback: render the whole slide page as PNG via `fitz.Page.get_pixmap(dpi=200)`. Tagged `EXTRACTION_METHOD: page-render` in `figures.md`. Catches every visual the source PDF shows, even when slides aren't structured as discrete embedded image objects. |
| Extracted figure is low-resolution or visually unclear | Extractor verdict = `REWORK`: figure is still embedded, and a Mermaid diagram or prose description is added alongside as a clearer backup. Reviewer #3 (Pedagogical Clarity) judges whether the pair is enough; if not, P0 to redraw. |
| Reviewer loop never converges | Soft bound of 5 rounds; PM is paged and decides to accept-with-caveat (documented in `study/00-DONE.md`) or escalate. |
| Exam agent rules ("don't read function bodies") are honour-system | Briefing emphasises this and the agent must produce its KNOB diff BEFORE running. Reviewer #4 (Variant Adaptability) acts as a second line of defence by predicting whether KNOBs are sufficient. |
| Parallel agent volume hits rate limits | Wave 1 dispatches all 21 implementers in parallel; reviewer batches are 4-parallel per artifact. If rate-limited, PM throttles by dispatching artifacts in groups of 5 instead of all 21 at once. |
| Notebook execution fails on user's machine due to missing packages | Each `*_solution.ipynb` opens with a setup cell pinning required packages. Verifier runs in the user's environment and reports missing packages explicitly. |
| Original templates use specific function signatures that conflict with KNOB-as-global convention | KNOBs are module-level globals AND mirrored as default kwargs where the template exposes a function. Best of both. |

## 16. Open Questions (none blocking)

None — all clarifying questions were resolved in the brainstorming phase. Variant banks (§8.3) are seeded with reasonable defaults; Lab Solvers may extend them.

## 17. Next Step

After user approval of this spec, invoke `superpowers:writing-plans` to produce the executable implementation plan: ordered task list, per-agent briefing templates, parallelism specification, and review-loop state machine.

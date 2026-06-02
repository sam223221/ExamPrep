# AI Exam Prep — Study Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce 10 textbook-quality lecture study PDFs + 1 master index PDF + solved versions of every lab (with KNOB-documented variables and embedded problem statements) for the AI course exam, by dispatching ~250–700 specialist agents through glossary → parallel-implementation → reviewer-loop → exam-agent-gate → render → verify waves.

**Architecture:** Orchestrated multi-agent system. The PM (this Claude Code session) is the loop controller — it dispatches every concrete action (no PM-written code or content). Approach B from the spec: a serial glossary pass produces shared terminology, then 21 implementers (10 lectures + 11 labs) run in parallel, each with its own 4-reviewer loop until APPROVED with zero P0/P1; labs additionally pass a 3-exam-agent gate. Wave 2 (Index Builder → PDF Renderer → Verifier) finishes the package.

**Tech Stack:** Python 3.12, PyMuPDF (figure extraction), WeasyPrint (Markdown→PDF), markdown + pymdown-extensions + markdown-katex (rendering), jupyter/nbconvert (notebook execution + verification), sklearn/pandas/matplotlib (already used in ML labs).

**Source spec:** [`docs/superpowers/specs/2026-05-22-ai-exam-prep-study-package-design.md`](../specs/2026-05-22-ai-exam-prep-study-package-design.md). Read it before executing this plan. Every section reference here (`spec §X`) points to that file.

---

## Wave & Loop Overview

```
Phase 0:  Environment Setup (pm-setup agent writes scaffolding)            serial
Phase 1:  Wave 0 — Glossary Skimmer                                        serial, 1 agent
Phase 2:  Wave 1 — Parallel implementation + per-artifact review loops     parallel, 21 artifacts
          ├─ Lecture Extractor x10  ┐
          │   └─ 4 Reviewers ⇄ Reviser   loop until APPROVED
          └─ Lab Solver x11         ┐
              ├─ 4 Reviewers ⇄ Reviser   loop until APPROVED
              └─ 3 Exam Agents       loop until all SOLVED
Phase 3:  Wave 2 — Index Builder + its own loop → PDF Renderer → Verifier  serial
Phase 4:  Wrap-up — final report, memory update, commit                    serial
```

---

## Phase 0 — Environment Setup

**Goal:** Get directory scaffolding, pinned dependencies, shared style assets, and toolchain smoke-test in place before any content agent runs.

### Task 0.1 — Dispatch Setup Engineer

**Files (after this task):**
- Create: `AI/study/_shared/style.css`
- Create: `AI/study/_shared/html-template.html`
- Create: `AI/study/requirements.txt`
- Create: `AI/study/render.py` (skeleton with TODO placeholder for renderer agent to fill)
- Create: `AI/study/.gitkeep` files in `_shared/`, `lectures/`, `extracted_figures/`, `_review/`, `_exam/`
- Create: `AI/docs/superpowers/plans/` (already exists once this file is written)

- [ ] **Step 0.1.1: Dispatch `pm-setup` agent with the Setup brief**

Brief verbatim:

```
You are the Setup Engineer for the AI Exam Prep Study Package project.
Read the spec at:
  docs/superpowers/specs/2026-05-22-ai-exam-prep-study-package-design.md

Your task is exclusively environment setup. Do NOT touch any lecture content,
any lab template, or any solution file.

Create exactly these files and directories under c:\Users\samgl\Documents\GitHub\ExamPrep\AI:

1. Directory scaffolding:
   - study/
   - study/_shared/
   - study/_review/
   - study/_exam/
   - study/lectures/
   - study/extracted_figures/
   Add a .gitkeep file in each empty directory.

2. study/requirements.txt — verbatim from spec §10:
   weasyprint==62.3
   markdown==3.6
   pymdown-extensions==10.9
   markdown-katex==202406.1035
   Pygments==2.18.0
   jupyter==1.0.0
   nbconvert==7.16.4
   PyMuPDF==1.24.9
   Pillow==10.4.0

3. study/_shared/style.css — clean serif PDF stylesheet:
   - Page setup: A4, 2cm margins, page numbers in footer.
   - Body: serif font (Source Serif Pro or Charter or system serif fallback),
     11pt, 1.45 line-height.
   - Headings: sans-serif (Inter or system sans), color #1a2238 for h1/h2,
     #344563 for h3.
   - Code: monospace 9.5pt, light-grey background.
   - Math (KaTeX output): centered for display, baseline-aligned inline.
   - Figures: max-width 100%, height auto, page-break-inside avoid.
   - Figure captions: italic 9.5pt, centered, max-width 90%.
   - Tables: full-width, 0.5pt grid, header row bold with light-grey fill.
   - Blockquotes: left border 3px solid #1a2238, padding-left 1em.
   - Cheat sheet section: subtle background tint or page break before.

4. study/_shared/html-template.html — wraps a converted-markdown body:
   <!DOCTYPE html>
   <html lang="en">
   <head>
     <meta charset="utf-8" />
     <title>{{ title }}</title>
     <link rel="stylesheet" href="style.css" />
   </head>
   <body>
     <main>{{ body }}</main>
   </body>
   </html>

5. study/render.py — skeleton only:
   """Markdown → PDF renderer for the study package. Filled in by the
   PDF Renderer agent in Phase 3."""
   # TODO: implemented by PDF Renderer agent — see spec §10.

6. Install dependencies:
   - Run: python -m pip install -r study/requirements.txt
   - If WeasyPrint installation fails on Windows: STOP, do not retry; report
     the exact error in your PM report. PM will trigger fallback chain.

7. Smoke test:
   - Write a 5-line Python script (study/_shared/smoke_test.py) that:
     a) imports fitz (PyMuPDF), markdown, weasyprint
     b) prints each module's version
     c) calls weasyprint.HTML(string="<p>hello</p>").write_pdf("study/_shared/smoke.pdf")
   - Run it. Confirm smoke.pdf exists and > 1 KB. Then delete smoke.pdf and
     smoke_test.py.

8. Ensure .gitignore at repo root contains entries for:
   - study/_shared/__pycache__/
   - **/*.pyc
   - PM/   (if not already present)

Do not modify any other files. Report back with the PM report block including:
- which files you created (with absolute paths)
- the output of `python -m pip list | findstr /R "weasyprint markdown PyMuPDF"`
- the smoke-test result
- any deviations or concerns
```

- [ ] **Step 0.1.2: Wait for agent return, read full PM report**

- [ ] **Step 0.1.3: Validate output**

  - Confirm all 4 created files exist (paths listed in step 0.1.1).
  - Confirm pip versions match `requirements.txt`.
  - Confirm smoke-test PASSED.
  - If WeasyPrint failed to install → execute Task 0.2 (fallback toolchain) instead of proceeding.

- [ ] **Step 0.1.4: Commit**

```bash
git add AI/study/_shared/style.css AI/study/_shared/html-template.html AI/study/requirements.txt AI/study/render.py AI/study/.gitkeep AI/study/_shared/.gitkeep AI/study/_review/.gitkeep AI/study/_exam/.gitkeep AI/study/lectures/.gitkeep AI/study/extracted_figures/.gitkeep .gitignore
git commit -m "chore(study): scaffold study/ with pinned deps, CSS, and HTML template"
```

### Task 0.2 — WeasyPrint Fallback (only if Task 0.1 reported install failure)

- [ ] **Step 0.2.1: Dispatch `pm-setup` with Fallback brief**

Brief:
```
WeasyPrint failed to install (likely GTK runtime missing on Windows).
Per spec §10, attempt fallback chain in order:

Plan A: Install pdfkit + wkhtmltopdf
  - pip install pdfkit==1.0.0
  - Download wkhtmltopdf installer from https://wkhtmltopdf.org/downloads.html,
    install to default location, add to PATH.
  - Smoke test: pdfkit.from_string("<p>hello</p>", "study/_shared/smoke.pdf")
  - If successful: update study/render.py docstring to note "uses pdfkit
    instead of weasyprint per fallback A". Update study/requirements.txt
    accordingly (remove weasyprint, add pdfkit).

Plan B: HTML-only output
  - If Plan A also fails, do NOT install any PDF tool.
  - Update render.py to emit only .html files; print a note that user must
    Print → PDF from browser.
  - Update requirements.txt to remove all PDF deps.

Report which plan succeeded and the final state of requirements.txt.
```

- [ ] **Step 0.2.2: Validate and commit** (same pattern as 0.1.3 / 0.1.4 above)

### Task 0.3 — Verify Source Inventory Is Intact

This is a sanity check: confirm none of the source PDFs / templates have been accidentally modified since the brainstorming exploration scan.

- [ ] **Step 0.3.1: Dispatch `Explore` agent**

Brief:
```
Quick verification only. Confirm these source files exist and report their sizes:

Lectures (10 PDFs at AI/):
  Lecture2-Introduction to Agents.pdf
  Lecture3-Uninformed Search.pdf
  Lecture5-Local Search.pdf
  Lecture6-Adversarial Search.pdf
  Lecture7-Constraint Satisfaction Problem.pdf
  Lecture9-Bayesian Networks.pdf
  Lecture9-Hidden Markov Models.pdf
  Lecture10-Introduction to Machine Learning.pdf
  Lecture11-Regression.pdf
  Lecture12-Clustering.pdf

Lab folders (each must exist with at least the listed files):
  Lab1-Agents/ — reflex_vacuum_agent.py, reflex_agent_with_state.py,
                 table_driven_agent.py, Enums.py
  Lab 2/ — Search.py, Lab 2.pdf
  handout/handout/ — alpha_beta.py, tictactoe_template.py, Lab 5.pdf
  handout_lab_4/ — ga.py, Number.py, Queen.py, queens_fitness.py, Lab 4.pdf
  lab6/ — constraints_template.py, Colors.py, States.py, Lab 6.pdf
  Lab7/handout/ — bn.py, Variable.py, Runner.py, Lab 7.pdf
  Lab 8/handout/ — hidden_markov_models.py, Lab 8.pdf

Notebooks at AI/:
  lab1_classification_handout.ipynb
  lab2_regression_handout.ipynb
  lab3_clustering_handout.ipynb

Report: PASS (all exist) or FAIL (list what's missing). Do not modify anything.
```

- [ ] **Step 0.3.2: On any FAIL, stop and report to user before proceeding**

---

## Phase 1 — Wave 0: Glossary Skimmer

**Goal:** Produce `study/_shared/glossary.md` and `study/_shared/cross-references.md` so Wave 1 agents share canonical terminology and cross-link correctly. See spec §5.2.

### Task 1.1 — Dispatch Glossary Skimmer

- [ ] **Step 1.1.1: Dispatch `general-purpose` agent with the Glossary brief**

Brief verbatim (template — full version in Appendix A.2):

```
You are the Glossary Skimmer for the AI Exam Prep Study Package project.
Read the spec: docs/superpowers/specs/2026-05-22-ai-exam-prep-study-package-design.md
particularly §5.2.

Your job is to produce two markdown files:
  - study/_shared/glossary.md
  - study/_shared/cross-references.md

For glossary.md:
  Read each of the 10 lecture PDFs at SHALLOW depth (table of contents,
  section headers, first slide of each section, occasional definition
  slides). DO NOT read every slide. Target: ~30 minutes total.

  For each named concept introduced anywhere across the 10 lectures,
  write an entry:
    ## Canonical Concept Name
    - One-paragraph definition in plain language.
    - Introduced in: Lecture N (slides X-Y).
    - Also appears in: Lecture M (slides ...), Lecture P (...).
    - Alternative names seen in source: [list any synonyms]
    - Symbol/notation (if applicable): $h(n)$, $\beta$, etc.

  Sort entries alphabetically. Aim for 60-120 entries covering: agents,
  rationality, environment types, PEAS, BFS, DFS, UCS, IDS, heuristic,
  admissibility, consistency, A*, greedy best-first, hill climbing,
  simulated annealing, genetic algorithm, fitness function, minimax,
  alpha-beta pruning, evaluation function, CSP, arc consistency,
  backtracking, MRV, LCV, Bayesian network, conditional probability,
  d-separation, inference by enumeration, HMM, transition model,
  observation model, Viterbi, forward algorithm, supervised vs
  unsupervised learning, train/test split, overfitting, decision tree,
  random forest, linear regression, polynomial regression, gradient
  descent, MSE, R^2, K-means, elbow method, silhouette score, ...
  (this is a starter list — extend as you find more).

For cross-references.md:
  Produce a Mermaid directed graph showing which lecture introduces each
  concept and which lectures reuse it. Format:

    ```mermaid
    graph LR
      L02[L02 Agents] --> heuristic
      L03[L03 Uninformed Search] --> heuristic
      heuristic --> L05[L05 Local Search]
      heuristic --> L06[L06 Adversarial Search]
      ...
    ```

  Plus a flat table:
    | Concept | Introduced | Reused in |
    |---|---|---|
    | heuristic | L03 | L05, L06 |
    | ...

Constraints:
  - Do NOT read full content of any lecture (that's later agents' job).
  - Do NOT touch any lab file.
  - Stay within shared/ — no edits anywhere else.
  - Use plain markdown; math in LaTeX delimiters.

Report back the full file paths created, line counts, and any concepts you
were unsure how to canonicalise.
```

- [ ] **Step 1.1.2: Wait for return; read full PM report**

- [ ] **Step 1.1.3: Sanity-check the output**

  - Open `study/_shared/glossary.md` — confirm > 60 entries.
  - Open `study/_shared/cross-references.md` — confirm Mermaid block parses (paste into a Mermaid linter mentally; it'll be properly tested by the renderer later).
  - Spot-check: are core terms (A*, alpha-beta, HMM, K-means) present?
  - If output is shallow (< 40 entries) or missing core terms → dispatch a second-pass Glossary Skimmer asking for expansion.

- [ ] **Step 1.1.4: Commit**

```bash
git add AI/study/_shared/glossary.md AI/study/_shared/cross-references.md
git commit -m "feat(study): glossary and cross-reference graph (Wave 0)"
```

---

## Phase 2 — Wave 1: Parallel Implementation + Per-Artifact Loops

**Goal:** All 21 artifacts (10 lecture chapters + 11 lab solutions) reach LOCKED state per spec §14.

### 2.A — Initial Parallel Dispatch (one tool call, 21 agents)

### Task 2.A.1 — Dispatch all 10 Lecture Extractors and all 11 Lab Solvers in parallel

This is a single PM action: one message, 21 `Agent` tool calls. Each agent runs in its own context.

- [ ] **Step 2.A.1.1: Construct briefs for all 21 implementers** (templates in Appendix A.3 and A.4)

Lecture Extractor list (subagent_type: `general-purpose`):

| ID | Lecture | Source PDF | Output Markdown |
|---|---|---|---|
| L02 | Agents | `Lecture2-Introduction to Agents.pdf` | `study/lectures/L02-Agents.md` |
| L03 | Uninformed Search | `Lecture3-Uninformed Search.pdf` | `study/lectures/L03-Uninformed-Search.md` |
| L05 | Local Search | `Lecture5-Local Search.pdf` | `study/lectures/L05-Local-Search.md` |
| L06 | Adversarial Search | `Lecture6-Adversarial Search.pdf` | `study/lectures/L06-Adversarial-Search.md` |
| L07 | CSP | `Lecture7-Constraint Satisfaction Problem.pdf` | `study/lectures/L07-CSP.md` |
| L09a | Bayesian Networks | `Lecture9-Bayesian Networks.pdf` | `study/lectures/L09a-Bayesian-Networks.md` |
| L09b | HMM | `Lecture9-Hidden Markov Models.pdf` | `study/lectures/L09b-HMM.md` |
| L10 | Intro to ML | `Lecture10-Introduction to Machine Learning.pdf` | `study/lectures/L10-Intro-to-ML.md` |
| L11 | Regression | `Lecture11-Regression.pdf` | `study/lectures/L11-Regression.md` |
| L12 | Clustering | `Lecture12-Clustering.pdf` | `study/lectures/L12-Clustering.md` |

Lab Solver list (subagent_type: `pm-backend`):

| ID | Lab | Templates | Handout | Solution Output |
|---|---|---|---|---|
| Lab1-Agents | Agents | `Lab1-Agents/*.py` | `Lab 1.pdf` | `Lab1-Agents/<name>_solution.py` for each template (entry = `reflex_agent_with_state_solution.py`) |
| Lab2-Search | Search | `Lab 2/Search.py` | `Lab 2/Lab 2.pdf` | `Lab 2/Search_solution.py` |
| Lab4-GA | GA / N-Queens | `handout_lab_4/*.py` | `handout_lab_4/Lab 4.pdf` | `handout_lab_4/ga_solution.py` (entry) + helper module solutions |
| Lab5-AlphaBeta | Alpha-Beta / TicTacToe | `handout/handout/*.py` | `handout/handout/Lab 5.pdf` | `handout/handout/tictactoe_template_solution.py` (entry) + `alpha_beta_solution.py` (module) |
| Lab6-CSP | CSP | `lab6/*.py` | `lab6/Lab 6.pdf` | `lab6/constraints_template_solution.py` (entry) |
| Lab7-BN | Bayesian Networks | `Lab7/handout/*.py` | `Lab7/handout/Lab 7.pdf` | `Lab7/handout/Runner_solution.py` (entry) + `bn_solution.py`, `Variable_solution.py` (modules) |
| Lab8-HMM | HMM | `Lab 8/handout/hidden_markov_models.py` | `Lab 8/handout/Lab 8.pdf` | `Lab 8/handout/hidden_markov_models_solution.py` |
| MLLab1-Classification | Classification | `lab1_classification_handout.ipynb` | (in notebook) | `lab1_classification_solution.ipynb` |
| MLLab2-Regression | Regression | `lab2_regression_handout.ipynb` | (in notebook) | `lab2_regression_solution.ipynb` |
| MLLab3-Clustering | Clustering | `lab3_clustering_handout.ipynb` | (in notebook) | `lab3_clustering_solution.ipynb` |

**Note on Lab count:** the table shows 10 lab IDs. Lab 1 (Agents) produces multiple solution files but is counted as one lab artifact (one PM report). This matches spec §3 (11 labs total: 8 algorithm labs in folders + 3 ML notebooks). Recounting: Lab1-Agents, Lab2-Search, Lab4-GA, Lab5-AlphaBeta, Lab6-CSP, Lab7-BN, Lab8-HMM = 7 algorithm labs; MLLab1, MLLab2, MLLab3 = 3 ML labs; total = **10 lab artifacts**. The spec §3 mentioned "11 labs total" — the discrepancy is that Lab 5 in the spec table was counted as one lab. Reconciled: **10 lab artifacts in this plan**.

- [ ] **Step 2.A.1.2: Dispatch in one tool call**

Send a single PM message containing 20 `Agent` tool invocations (10 Lecture Extractors + 10 Lab Solvers). Each brief is the template from Appendix A.3 / A.4 with the per-artifact variables filled in. Each agent receives its own context window.

- [ ] **Step 2.A.1.3: Track returns**

  - Each implementer returns a PM report including artifact paths.
  - Record each artifact's status in a working tracker (in-conversation TodoWrite):
    `{ artifact_id, status: implemented | review_round_1_pending | … | LOCKED, last_round: 0 }`
  - Implementers may return concerns or out-of-scope observations — log these for later, but do not act on them until the review loop has processed the artifact.

- [ ] **Step 2.A.1.4: Commit after all 20 implementers return**

```bash
git add AI/study/lectures/ AI/study/extracted_figures/ \
        AI/Lab1-Agents/*_solution.py AI/Lab\ 2/*_solution.py \
        AI/handout/handout/*_solution.py AI/handout_lab_4/*_solution.py \
        AI/lab6/*_solution.py AI/Lab7/handout/*_solution.py \
        AI/Lab\ 8/handout/*_solution.py AI/*_solution.ipynb
git commit -m "feat(study): Wave 1 implementer drafts (lectures + lab solutions, pre-review)"
```

This commit is the BEFORE state for every reviewer's diff lens.

### 2.B — Per-Artifact Loop Procedure

**This is a reusable subroutine. It is applied to every artifact independently.** The PM runs these procedures **in parallel across artifacts** — the loop for L02 does not block the loop for L11.

#### Procedure L (lecture artifact)

For each lecture artifact `{ID}` (one of L02, L03, L05, L06, L07, L09a, L09b, L10, L11, L12):

- [ ] **Step L.1: Dispatch 4 reviewers in parallel** (one PM message, 4 `Agent` tool calls; subagent_type: `pm-qa`)

Reviewer briefs are in Appendix A.5. Reports written to:
  - `study/_review/{ID}/round{R}/reviewer1.md` — Concept Completeness (incl. figures)
  - `study/_review/{ID}/round{R}/reviewer2.md` — Mathematical Rigor
  - `study/_review/{ID}/round{R}/reviewer3.md` — Pedagogical Clarity (incl. analogies)
  - `study/_review/{ID}/round{R}/reviewer4.md` — Exam Readiness

- [ ] **Step L.2: Read all 4 reviewer reports** (PM reads them itself — these are markdown PM-owned files)

- [ ] **Step L.3: Decision gate**
  - If all 4 reports show `VERDICT: APPROVED` AND zero P0 AND zero P1 → mark artifact **LOCKED**, jump to L.6.
  - Otherwise → proceed to L.4.

- [ ] **Step L.4: Dispatch Reviser** (subagent_type: `general-purpose`)

  Brief (Appendix A.6) tells the Reviser to: read current `.md` + all 4 reports, address every P0 and P1, consider every P2, write `study/_review/{ID}/round{R}/revise-summary.md` documenting which comment each change addresses, save revised `.md` over the existing file.

- [ ] **Step L.5: Increment round counter; loop back to L.1**
  - Soft bound: if `round` exceeds 5 → STOP loop, page PM (user) with a summary of unresolved P0/P1, request decision: accept-with-caveat (record in `study/00-DONE.md` open items) or escalate.

- [ ] **Step L.6: Commit LOCKED state**
```bash
git add AI/study/lectures/{ID}-*.md AI/study/extracted_figures/{ID}/ AI/study/_review/{ID}/
git commit -m "feat(study/{ID}): LOCKED after {R} review rounds"
```

#### Procedure B (lab artifact)

For each lab artifact `{ID}` (one of Lab1-Agents, Lab2-Search, Lab4-GA, Lab5-AlphaBeta, Lab6-CSP, Lab7-BN, Lab8-HMM, MLLab1-Classification, MLLab2-Regression, MLLab3-Clustering):

- [ ] **Step B.1: Dispatch 4 reviewers in parallel** (subagent_type: `pm-qa`)

Reviewer briefs in Appendix A.5 (lab lenses). Reports written to `study/_review/labs/{ID}/round{R}/reviewer{1-4}.md`.

- [ ] **Step B.2: Read all 4 reports**

- [ ] **Step B.3: Decision gate**
  - If all APPROVED, zero P0/P1 → proceed to B.6 (exam gate).
  - Else → B.4.

- [ ] **Step B.4: Dispatch Reviser** (subagent_type: `pm-backend`)

  Brief: address P0/P1, update solution file(s), write `revise-summary.md`.

- [ ] **Step B.5: Increment round; loop back to B.1**
  - Soft bound 5 rounds, same escalation rule as L.5.

- [ ] **Step B.6: Variant bank prep** (only first time reaching this step for the lab)

  Confirm `study/_exam/{ID}/variants.md` exists. If not (Lab Solver should have created it as part of its Phase 2.A work) → dispatch a quick `general-purpose` agent to write it from spec §8.3.

- [ ] **Step B.7: Dispatch 3 Exam Agents in parallel** (subagent_type: `general-purpose`)

  Brief in Appendix A.7. Each agent gets a DIFFERENT variant from `variants.md`. Reports written to `study/_exam/{ID}/round{R}/examiner{1-3}.md`.

- [ ] **Step B.8: Read all 3 exam reports**

- [ ] **Step B.9: Decision gate**
  - If all 3 report `VERDICT: SOLVED` → mark **LOCKED**, jump to B.11.
  - If any report `VERDICT: STUCK` → B.10.

- [ ] **Step B.10: Dispatch Reviser focused on documentation, not implementation** (subagent_type: `pm-backend`)

  Brief: read the STUCK report(s), improve the docstring header and/or KNOB comments (rarely the implementation). Then loop back to **B.1** (full reviewer gate must re-pass before re-running exam agents). Increment a separate `exam_round` counter.

- [ ] **Step B.11: Commit LOCKED state**
```bash
git add AI/{lab folder}/*_solution.* AI/study/_review/labs/{ID}/ AI/study/_exam/{ID}/
git commit -m "feat(study/{ID}): LOCKED after {R} review rounds, exam_round {ER}"
```

### 2.C — Apply Per-Artifact Procedures (run in parallel)

Tasks 2.C.1 through 2.C.20 each run independently. The PM tracks them in a TodoWrite. Once all 20 are LOCKED, proceed to Phase 3.

- [ ] **Task 2.C.1: Lecture L02 → Procedure L**
- [ ] **Task 2.C.2: Lecture L03 → Procedure L**
- [ ] **Task 2.C.3: Lecture L05 → Procedure L**
- [ ] **Task 2.C.4: Lecture L06 → Procedure L**
- [ ] **Task 2.C.5: Lecture L07 → Procedure L**
- [ ] **Task 2.C.6: Lecture L09a → Procedure L**
- [ ] **Task 2.C.7: Lecture L09b → Procedure L**
- [ ] **Task 2.C.8: Lecture L10 → Procedure L**
- [ ] **Task 2.C.9: Lecture L11 → Procedure L**
- [ ] **Task 2.C.10: Lecture L12 → Procedure L**
- [ ] **Task 2.C.11: Lab1-Agents → Procedure B**
- [ ] **Task 2.C.12: Lab2-Search → Procedure B**
- [ ] **Task 2.C.13: Lab4-GA → Procedure B**
- [ ] **Task 2.C.14: Lab5-AlphaBeta → Procedure B**
- [ ] **Task 2.C.15: Lab6-CSP → Procedure B**
- [ ] **Task 2.C.16: Lab7-BN → Procedure B**
- [ ] **Task 2.C.17: Lab8-HMM → Procedure B**
- [ ] **Task 2.C.18: MLLab1-Classification → Procedure B**
- [ ] **Task 2.C.19: MLLab2-Regression → Procedure B**
- [ ] **Task 2.C.20: MLLab3-Clustering → Procedure B**

**Parallelism budget:** at peak, ~20 implementers + 20×4 reviewers = 100 agents concurrent. If platform rate-limits hit, throttle by running artifacts in groups of 5 instead of all 20 — staggered start, full parallelism within each group.

### 2.D — Phase 2 Done Gate

- [ ] **Task 2.D.1: Verify all 20 artifacts are LOCKED**
  - Check TodoWrite tracker.
  - For each artifact, confirm the LOCKED commit exists in `git log`.
- [ ] **Task 2.D.2: Aggregate any P2 nice-to-haves into `study/00-DONE-open-items.md`** (a temp file; merged into `00-DONE.md` at the very end)

---

## Phase 3 — Wave 2: Index, Render, Verify

### Task 3.1 — Dispatch Index Builder

- [ ] **Step 3.1.1: Dispatch `general-purpose` agent**

Brief (Appendix A.8): read every locked `study/lectures/*.md` and `study/_shared/glossary.md`. Produce `study/00-master-index.md` containing TOC, flattened glossary, Analogies Index (one-page table — every concept ↔ one-line analogy), Cross-reference Mermaid graph, Recommended study order.

- [ ] **Step 3.1.2: Run the Index Builder through Procedure L (4-reviewer loop)**

  - Treat `00-master-index.md` as artifact ID `MASTER-INDEX`.
  - Run the same 4-reviewer Procedure L (L.1 through L.6), with the lenses adapted for an index document (Reviewer #1 audits coverage of all lectures, Reviewer #2 audits formula listings if any, Reviewer #3 audits analogies index quality, Reviewer #4 audits "is this useful for last-minute revision").
  - LOCKED when all 4 APPROVED zero P0/P1.

- [ ] **Step 3.1.3: Commit**
```bash
git add AI/study/00-master-index.md AI/study/_review/MASTER-INDEX/
git commit -m "feat(study): master index LOCKED"
```

### Task 3.2 — Dispatch PDF Renderer

- [ ] **Step 3.2.1: Dispatch `pm-backend` agent**

Brief (Appendix A.9): write the actual `study/render.py` implementing the pipeline in spec §10. Then run it to produce all PDFs.

Outputs:
  - `study/render.py` (complete implementation)
  - `study/lectures/*.pdf` (10 files)
  - `study/00-master-index.pdf`
  - The renderer's PM report includes which path was taken (WeasyPrint primary / pdfkit fallback / HTML-only fallback).

- [ ] **Step 3.2.2: Sanity check**
  - All 11 PDFs exist, each > 50 KB.
  - Spot-open one PDF manually (open in default app) — confirm it's not a blank page or corrupted. (PM dispatches an `Explore` agent to confirm file integrity; PM does not open files itself.)

- [ ] **Step 3.2.3: Commit**
```bash
git add AI/study/render.py AI/study/lectures/*.pdf AI/study/00-master-index.pdf
git commit -m "feat(study): render all lectures and master index to PDF"
```

### Task 3.3 — Dispatch Verifier

- [ ] **Step 3.3.1: Dispatch `pm-qa` agent**

Brief (Appendix A.10): perform all 6 checks from spec §11. Write `study/_verification-report.md`.

- [ ] **Step 3.3.2: Read the verification report**

- [ ] **Step 3.3.3: For every FAIL, dispatch a targeted fixer**

  - For a failed lab solution execution: dispatch `pm-backend` Reviser with the error trace + instructions to fix that solution file ONLY. Then re-run that lab's full review-and-exam gate. Then re-verify just that artifact.
  - For a failed PDF render: dispatch `pm-backend` to debug the renderer; if a single lecture's PDF failed, re-render only that one.
  - For a broken cross-reference link: dispatch a Reviser on the lecture containing the broken link to fix it.
  - For a missing/empty figure file: dispatch the original Lecture Extractor to re-extract.
  - For a missing entry-point declaration: dispatch the Lab Solver to add it.

- [ ] **Step 3.3.4: Re-run Verifier**
  - Repeat until verification report is fully green.

- [ ] **Step 3.3.5: Commit**
```bash
git add AI/study/_verification-report.md (and any fix commits along the way)
git commit -m "test(study): verifier green; all solutions run, all PDFs render, all xrefs resolve"
```

---

## Phase 4 — Wrap-Up

### Task 4.1 — Final Report Document

- [ ] **Step 4.1.1: Dispatch `general-purpose` agent to write `study/00-DONE.md`**

Brief:
```
Read:
  - study/_verification-report.md
  - every study/_review/*/round*/ for round counts and any P2 items
  - any study/00-DONE-open-items.md (temp aggregation file)

Produce study/00-DONE.md containing:
  1. Top-line summary: "Study package complete. N lectures, M labs, K PDFs."
  2. Per-artifact summary table:
     | Artifact | Rounds to LOCK | Exam-agent retries (labs) | P2s deferred |
  3. Full list of P2 nice-to-haves that were deferred (with reasons).
  4. Render path taken (WeasyPrint / pdfkit / HTML-only).
  5. Total agent-invocations consumed (count from review/exam folders).
  6. Recommended next steps for the student (Sam): study order, which
     analogies to internalize first, which labs to practice variant-solving on.

Tone: concise but complete. The student should be able to read this single
file and understand the state of the entire package.

Then delete study/00-DONE-open-items.md if it exists.
```

- [ ] **Step 4.1.2: Commit**
```bash
git add AI/study/00-DONE.md
git rm AI/study/00-DONE-open-items.md  # if it existed
git commit -m "docs(study): final DONE report"
```

### Task 4.2 — Memory Update

- [ ] **Step 4.2.1: PM writes a memory entry**

PM directly writes to `C:\Users\samgl\.claude\projects\c--Users-samgl-Documents-GitHub-ExamPrep\memory\`:
  - `project_ai_exam_prep.md` (project memory): captures what the workspace is (educational exam-prep, not software), where the study package lives, the analogy-first convention used, what to do if the user comes back asking to update notes after a lecture.
  - Add a line to `MEMORY.md`.

### Task 4.3 — Final Report to User

- [ ] **Step 4.3.1: PM summarises to user in chat**

Content:
  - Total agents dispatched.
  - Wall-clock time elapsed.
  - Render path used.
  - Any caveats (accept-with-caveat decisions made in review-loop soft-bound trigger).
  - Concrete next steps: open `study/00-DONE.md`, then `study/00-master-index.pdf`.

---

## Appendices — Agent Briefing Templates

These are filled in with per-artifact variables when dispatched.

### Appendix A.1 — Setup Engineer Brief

(Full text already inlined in Task 0.1.1.)

### Appendix A.2 — Glossary Skimmer Brief

(Full text already inlined in Task 1.1.1.)

### Appendix A.3 — Lecture Extractor Brief (template)

```
You are a Lecture Extractor for the AI Exam Prep Study Package.
Read the spec FIRST:
  docs/superpowers/specs/2026-05-22-ai-exam-prep-study-package-design.md
particularly §6.1, §6.1.1, §7 (you will be reviewed against §7.1 lenses).

ASSIGNMENT
  Lecture ID:           {ID}                  (e.g. L02, L03, ...)
  Lecture Topic:        {Topic}               (e.g. "Introduction to Agents")
  Source PDF:           AI/{source-pdf}
  Output Markdown:      AI/study/lectures/{ID}-{slug}.md
  Figures directory:    AI/study/extracted_figures/{ID}/
  Figures catalogue:    AI/study/extracted_figures/{ID}/figures.md
  Glossary:             AI/study/_shared/glossary.md  (READ-ONLY; use canonical names)
  Cross-references:     AI/study/_shared/cross-references.md  (READ-ONLY)

DELIVERABLES
  1. A textbook chapter in the markdown file at the output path, following
     the §6.1 template EXACTLY:
       §1 Overview & Motivation
       §2 The Big Picture — Analogies (one analogy per major concept,
                                       with "where the analogy breaks down")
       §3 Core Concepts (formal definitions, cross-linking to §2 analogies)
       §4 Algorithms / Methods
       §5 Worked Examples (every slide example, fully expanded)
       §6 Common Pitfalls / Exam Traps
       §7 Connections to Other Lectures (use canonical names from glossary)
       §8 Cheat-Sheet Summary (one-line analogy reminder per concept)

  2. All figures from the source PDF extracted per §6.1.1:
       - Use PyMuPDF (fitz) to enumerate every embedded image.
       - Save to study/extracted_figures/{ID}/figNN-slug.png.
       - Catalogue every figure in study/extracted_figures/{ID}/figures.md
         with: filename, source page, surrounding text/caption, USE/REWORK/SKIP
         verdict, rationale.
       - Embed every USE and REWORK figure in the chapter .md at appropriate
         section, with markdown ![caption](relative-path) syntax.
       - For REWORK figures, add a Mermaid diagram or prose description
         alongside the embedded image.
       - For composite-slide figures that don't extract cleanly, fall back to
         rendering the whole slide page as PNG via fitz.Page.get_pixmap(dpi=200).
         Tag as EXTRACTION_METHOD: page-render in figures.md.

CONSTRAINTS
  - TAKE YOUR TIME. Read the entire PDF page-by-page. The user has explicitly
    said no shortcuts.
  - Use ONLY canonical concept names from the glossary. If you find a concept
    not in the glossary, add it to a "glossary-additions.md" file in your
    output directory; the master Glossary will be updated by a separate task.
  - Math in LaTeX delimiters: $inline$ and $$display$$.
  - Every section ends with "[Lecture {N}, slides X-Y]" so the reader can flip
    back.
  - Cross-refs to other lectures use absolute paths from study/lectures/.
  - Do NOT modify any file outside study/ and AI/study/extracted_figures/{ID}/.

QUALITY BAR
  Your output will be reviewed by 4 critical reviewers (Concept Completeness,
  Mathematical Rigor, Pedagogical Clarity incl. Analogies, Exam Readiness)
  per §7.1. The bar is: zero P0, zero P1 issues. They WILL be harsh. False
  positives are cheap; missed concepts are catastrophic. Be thorough.

REPORT BACK with the PM report block including: chapter word count, figure
count by verdict (USE/REWORK/SKIP), any concepts you couldn't find in glossary,
any concerns.
```

### Appendix A.4 — Lab Solver Brief (template)

```
You are a Lab Solver for the AI Exam Prep Study Package.
Read the spec FIRST:
  docs/superpowers/specs/2026-05-22-ai-exam-prep-study-package-design.md
particularly §6.2, §6.3, §8 (you will be reviewed against §8.1 lenses, then
your output goes through the 3-exam-agent gate from §8.2).

ASSIGNMENT
  Lab ID:                 {ID}
  Lab title:              {Title}
  Template files:         {list of template paths}
  Lab handout PDF:        AI/{handout-path}
  Solution outputs:       {list of *_solution.* paths}
  Entry-point file:       {which solution file has __main__ block}
  Relevant lectures:      {e.g. L05, L07 — from cross-references.md}
  Glossary:               AI/study/_shared/glossary.md  (READ-ONLY)
  Variant bank target:    AI/study/_exam/{ID}/variants.md  (YOU create this)

DELIVERABLES
  1. Solution files at the listed output paths. Convention §6.2:
     Each file starts with a docstring header containing:
       - LAB N: <Title>
       - PROBLEM STATEMENT (extracted verbatim from the handout PDF)
       - MENTAL MODEL (one-line analogy, consistent with the corresponding
         lecture's §2 analogy)
       - REFERENCES (lecture sections + glossary terms)
       - HOW TO ADAPT FOR DIFFERENT QUESTION VARIANTS (numbered list)
       - OUTPUTS WHEN RUN
       - ENTRY POINT: yes | no  (with reason if "no")

  2. Every tunable variable tagged with §6.3 KNOB block:
       # KNOB: NAME (default=X, range=Y)
       #   What it does: ...
       #   Effect: ...
       #   Exam variants: ...
     Reviewer #2 (KNOB Coverage) will hunt for magic numbers in function
     bodies. Promote them all.

  3. Replace every `raise NotImplementedError(...)` with a working
     implementation. Public function signatures from the template are
     preserved EXACTLY (parameter names and order; defaults may change).

  4. Comments inside function bodies explain WHY, not WHAT. Skim-readable.

  5. For .ipynb labs: each TODO cell gets a working code cell + a preceding
     markdown cell explaining the approach. Use # KNOB: comments in code
     cells.

  6. RUN the solution at least once before submitting. For .py: python {file}.
     For .ipynb: jupyter nbconvert --to notebook --execute --inplace=false.
     If it errors, fix it. Capture the final output and include a snippet
     under "OUTPUTS WHEN RUN" in the docstring.

  7. Create study/_exam/{ID}/variants.md from the §8.3 variant bank for your
     lab. Three concrete variants, each one a self-contained "exam question"
     a fresh agent could read and answer using only your KNOBs. Feel free to
     add a 4th or 5th plausible variant if the handout suggests them.

CONSTRAINTS
  - Originals untouched. Only write to *_solution.* files and to
    study/_exam/{ID}/.
  - Match the analogy in the corresponding lecture chapter (read its §2
    after the Lecture Extractor for {relevant lecture} has finished — if
    that's not done yet, use the analogy from the spec §6.1 examples or
    coordinate via the glossary).

QUALITY BAR
  After your work, 4 critical reviewers (Correctness, KNOB Coverage,
  Pedagogical Clarity, Variant Adaptability) audit you. Then 3 exam agents
  try to solve different variants using ONLY your docstring + KNOB comments
  + function signatures. If any exam agent reports STUCK, you'll be called
  back to improve documentation.

REPORT BACK with: solution file paths, entry-point file, KNOB count, output
when run, variant bank summary, any concerns.
```

### Appendix A.5 — Reviewer Briefs

Lectures — 4 reviewer templates. Each is dispatched with the artifact ID,
the current round number, and the artifact paths.

**A.5.L1 — Lecture Reviewer 1 (Concept Completeness incl. Figures):**
```
You are Lecture Reviewer #1 (Concept Completeness incl. Figures) for the
AI Exam Prep Study Package, reviewing artifact {ID} round {R}.

Spec: docs/superpowers/specs/2026-05-22-ai-exam-prep-study-package-design.md §7.1.

YOUR LENS
  Cross-check every slide in the source PDF against the .md draft. Flag any
  concept, definition, formula, or topic-bullet missing or under-covered.
  Specifically:
    - Does the chapter cover EVERY slide section?
    - Does it name and define EVERY named concept from the slides?
    - Is EVERY formula shown in slides reproduced?
  Then audit figures (§6.1.1):
    - Open study/extracted_figures/{ID}/figures.md.
    - Confirm every USE / REWORK figure is actually embedded in the chapter
      .md at a sensible location.
    - Confirm every SKIP verdict is justified (and not just dropping useful
      diagrams to save effort).
    - Confirm no informative figure from the source PDF was missed entirely
      (e.g. an algorithm flowchart that should be in §4).

ARTIFACTS TO READ
  - AI/{source PDF}
  - AI/study/lectures/{ID}-{slug}.md
  - AI/study/extracted_figures/{ID}/figures.md

BE HARSH. False positives are cheap; missed concepts are catastrophic.

OUTPUT
  Write your report to AI/study/_review/{ID}/round{R}/reviewer1.md with sections:
    # Reviewer #1 — Concept Completeness — {ID} Round {R}
    ## VERDICT
    APPROVED | NEEDS_REVISION
    ## P0 — MUST FIX (blocks approval)
    - Bullet list. Each item: WHAT is missing, WHERE in the .md it should
      appear, which source slide(s) require it.
    ## P1 — SHOULD FIX (requested, not blocking)
    - Similar format.
    ## P2 — NICE TO HAVE
    - Similar format.
    ## EVIDENCE
    - Which slides reviewed (page numbers).
    - Which .md sections inspected.
    - Which figures verified.
```

**A.5.L2 — Lecture Reviewer 2 (Mathematical Rigor):**
```
You are Lecture Reviewer #2 (Mathematical Rigor) — {ID} round {R}.
Spec §7.1.

YOUR LENS
  Verify every formula in the .md matches the source PDF. Catch:
    - Missing derivation steps a student would need.
    - Wrong indices, off-by-one in summations, swapped subscripts.
    - Ambiguous notation (variable reused without re-declaration).
    - Dropped assumptions (e.g. "assuming i.i.d." silently omitted).
    - Mismatched variable names between definition and use.
  Math is the second-most-tested thing on the exam. Be merciless.

Same output format as Reviewer #1, written to .../reviewer2.md.
```

**A.5.L3 — Lecture Reviewer 3 (Pedagogical Clarity incl. Analogies):**
```
You are Lecture Reviewer #3 (Pedagogical Clarity incl. Analogies) —
{ID} round {R}. Spec §7.1.

YOUR LENS
  Read as a confused student encountering this material for the first time.
  Flag:
    - Hand-waving and unjustified leaps.
    - Undefined terms (used before introduced).
    - Missing intuition between definition and worked example.
    - Examples that don't actually illustrate the concept they accompany.
  Then enforce analogies (§2 of the chapter):
    - Every major concept introduced in this lecture MUST have at least one
      concrete everyday analogy.
    - Each analogy MUST be cross-linked from its formal definition in §3
      ("recall the X analogy from §2").
    - Each analogy MUST include a "where the analogy breaks down" caveat.
    - Weak analogies (too abstract, technical, or stretched) → flag and
      demand a replacement. Suggest one if you can.

Same output format. Written to .../reviewer3.md.
```

**A.5.L4 — Lecture Reviewer 4 (Exam Readiness):**
```
You are Lecture Reviewer #4 (Exam Readiness) — {ID} round {R}. Spec §7.1.

YOUR LENS
  Read as someone writing the exam. Flag:
    - Missing worked examples (every concept should have at least one).
    - Ignored edge cases (the kind that show up as gotcha questions).
    - Cheat-sheet (§8) inaccuracies — symbols, complexity, "when to use which".
    - Thin Common Pitfalls (§6) section — every commonly-tested mistake should
      be there.
  Imagine 10 plausible exam questions on this lecture. Can a student answer
  them all using ONLY this chapter? If not, what's missing?

Same output format. Written to .../reviewer4.md.
```

Labs — 4 reviewer templates. Identical structure, different lenses:

**A.5.B1 — Lab Reviewer 1 (Correctness):**
```
You are Lab Reviewer #1 (Correctness) — {ID} round {R}. Spec §8.1.

YOUR LENS
  Run the solution code yourself:
    - For .py entry-point file: python <file>. Capture stdout/stderr.
    - For .ipynb: jupyter nbconvert --to notebook --execute --inplace=false.
  Verify it solves the original lab problem (read the handout PDF).
  Flag:
    - Wrong outputs.
    - Off-by-one in loops or array indexing.
    - Broken edge cases (empty input, single-element, max-size).
    - Function signatures that diverge from the template.
    - Imports / dependencies missing.

OUTPUT
  Standard reviewer report at AI/study/_review/labs/{ID}/round{R}/reviewer1.md.
```

**A.5.B2 — Lab Reviewer 2 (KNOB Coverage):**
```
You are Lab Reviewer #2 (KNOB Coverage) — {ID} round {R}. Spec §6.3, §8.1.

YOUR LENS
  Audit every # KNOB: block:
    - Complete? (default + range + effect + variants)
    - Accurate? (does the variant claim work if you actually flip the KNOB?)
  Then hunt for HIDDEN parameters — magic numbers buried in function bodies
  that should have been promoted to KNOBs. Examples: a "0.01" learning rate
  hard-coded in gradient descent; a "3" depth limit in a search tree; a "0.7"
  threshold in a classifier.
  Every magic-number flag is a P0 unless the agent can justify why it's not
  exam-relevant.

Standard reviewer report at .../reviewer2.md.
```

**A.5.B3 — Lab Reviewer 3 (Pedagogical Clarity):**
```
You are Lab Reviewer #3 (Pedagogical Clarity) — {ID} round {R}. Spec §8.1.

YOUR LENS
  Could a student understand WHY without reading deep into the code?
  Check:
    - Header docstring complete and clear (PROBLEM STATEMENT, MENTAL MODEL,
      REFERENCES, HOW TO ADAPT, OUTPUTS WHEN RUN, ENTRY POINT).
    - Comments inside function bodies explain WHY, not WHAT.
    - MENTAL MODEL analogy is consistent with the corresponding lecture's §2.
  Flag any comment that just repeats the next line in English.

Standard reviewer report at .../reviewer3.md.
```

**A.5.B4 — Lab Reviewer 4 (Variant Adaptability):**
```
You are Lab Reviewer #4 (Variant Adaptability) — {ID} round {R}. Spec §8.1.

YOUR LENS
  Read the lab handout PDF AND study/_exam/{ID}/variants.md.
  For each variant, walk through it mentally:
    - Can it be solved purely by changing KNOB values (no function-body
      edits)? If not, what KNOB is missing?
    - Is the relevant KNOB documented well enough that someone reading only
      the comment can figure out what to set?
  Also imagine 5 more plausible exam variants the course might pose. For
  each, does the current KNOB set + docstring cover it?

Standard reviewer report at .../reviewer4.md.
```

### Appendix A.6 — Reviser Brief (template)

```
You are the Reviser for artifact {ID} round {R}.

Read these inputs in order:
  1. Current draft of the artifact:
     - Lectures: AI/study/lectures/{ID}-{slug}.md
     - Labs: every file listed in {solution paths}
  2. All 4 reviewer reports for this round:
     - AI/study/_review/{ID}/round{R}/reviewer1.md
     - AI/study/_review/{ID}/round{R}/reviewer2.md
     - AI/study/_review/{ID}/round{R}/reviewer3.md
     - AI/study/_review/{ID}/round{R}/reviewer4.md
     (For labs, replace path with AI/study/_review/labs/{ID}/...)

YOUR TASK
  Address every P0 (mandatory). Address every P1 (mandatory). Consider every
  P2 — apply if low-cost.

  When reviewers disagree (rare but possible), apply the stricter
  interpretation and document the choice in the revise-summary.

  When a reviewer flags a missing concept, ADD the concept; do not just
  add a token mention.

OUTPUT
  - Save the revised artifact OVER the existing file(s) at the same paths.
  - Write a summary of changes to:
      AI/study/_review/{ID}/round{R}/revise-summary.md
    Format:
      # Revise Summary — {ID} Round {R}
      ## Changes Made
      - [Change description] — addresses reviewer{N} {P0|P1|P2} item: "{quote}"
      - ...
      ## P2s Deferred (if any)
      - [P2 item] — reason for deferring.
      ## New Round Counter
      Round {R+1} pending.

After saving, REPORT BACK with the PM report block.
```

### Appendix A.7 — Exam Agent Brief (template)

```
You are Exam Agent #{N} for lab {ID}, examining round {ER}.

YOUR ASSIGNMENT
  Variant question: {one verbatim variant from study/_exam/{ID}/variants.md}

  Path to the locked solution file(s): {paths}

HARD CONSTRAINTS (per spec §8.2)
  You MAY READ:
    - The docstring header at the top of each solution file.
    - Every # KNOB: comment block.
    - Function signatures (the `def ...:` line only — NOT the body).
    - Class signatures.
    - Data files the solution consumes (CSV, JSON, image datasets).

  You MAY NOT READ:
    - Function bodies. (Bracket the def line, jump past the function.)
    - Class bodies.
    - Helper modules' source code.
    - The lab handout PDF.
    - Any lecture PDF.
    - Any lecture .md file.
    - The solution code of any OTHER lab.

PROCEDURE
  1. Read your variant question carefully.
  2. Skim the docstring header + KNOB blocks. Decide which KNOBs to change
     and what to set them to.
  3. BEFORE running anything, write your plan to your output file:
       VARIANT: {the variant verbatim}
       PLANNED KNOB CHANGES:
         - KNOB_X: from {current} to {new value}, because ...
         - KNOB_Y: from {current} to {new value}, because ...
  4. Apply the changes (edit the solution file in-place, or copy to a
     scratch file).
  5. Run the modified solution.
  6. Capture the output and your final answer to the variant question.
  7. Decide your verdict:
       SOLVED if you produced a coherent answer to the variant question.
       STUCK if you couldn't, AND explain precisely what was unclear:
         - Which KNOB was missing?
         - Which variant was the docstring blind to?
         - What additional documentation would have helped you?

OUTPUT
  Write to AI/study/_exam/{ID}/round{ER}/examiner{N}-attempt.md:
    VARIANT: {verbatim}
    KNOB CHANGES: {diff}
    RUN OUTPUT: {captured stdout (trimmed to relevant lines)}
    ANSWER: {your final answer}
    VERDICT: SOLVED | STUCK
    STUCK REASON: {if applicable, detailed explanation}

PM REPORT
  Standard PM report at the end. Be honest about whether you cheated and
  peeked at function bodies — if you did, you've invalidated the test and
  must report it.
```

### Appendix A.8 — Index Builder Brief

```
You are the Index Builder for the AI Exam Prep Study Package.

Read all of:
  - AI/study/lectures/L*.md (10 files)
  - AI/study/_shared/glossary.md
  - AI/study/_shared/cross-references.md

Produce AI/study/00-master-index.md per spec §5.5:
  1. Top: project header + how to use this index.
  2. Full Table of Contents — every lecture, every major section heading,
     every named concept, with links into each lecture's .md.
  3. Glossary (flattened) — concept name, one-line definition, link to the
     §3 entry in the lecture that introduces it.
  4. Analogies Index — one-page table:
       | Concept | One-line analogy | Lecture §2 link |
     One row per concept that has an analogy. Pulled verbatim from each
     lecture's §2.
  5. Cross-reference Mermaid graph — built from cross-references.md,
     visually rendered in WeasyPrint via mermaid-cli pre-render OR drawn as
     ASCII fallback if mermaid-cli unavailable.
  6. Recommended Study Order:
       Suggested reading sequence (matches course flow), estimated time per
     chapter, "if you only have one day" / "if you have a week" tracks.

After your first draft, you'll go through the 4-reviewer loop. Anticipate
the lenses and self-check first.

PM REPORT format as usual.
```

### Appendix A.9 — PDF Renderer Brief

```
You are the PDF Renderer for the AI Exam Prep Study Package.
Read spec §10 carefully.

Your task:
  1. Implement AI/study/render.py per the spec §10 pipeline:
       - Walk AI/study/lectures/ for *.md (10 files).
       - Walk AI/study/ for 00-master-index.md.
       - For each: convert markdown → HTML using the markdown library with
         the listed extensions, pre-rendering math via markdown-katex.
       - Wrap in AI/study/_shared/html-template.html (substitute {{ title }}
         and {{ body }}).
       - Run WeasyPrint to produce {basename}.pdf in the same directory.
  2. Run render.py.
  3. Confirm all 11 PDFs (10 lectures + 1 index) exist, each > 50 KB.
  4. If WeasyPrint fails:
       - Try pdfkit + wkhtmltopdf (install if needed).
       - If pdfkit also fails, emit styled .html files in the same locations
         and document this in your PM report.

CSS already exists at AI/study/_shared/style.css. Use it. Do NOT modify it
unless a reviewer in a later step asks for changes.

CONSTRAINTS
  - render.py must be idempotent (running twice produces the same output).
  - render.py must NOT delete .md files.
  - render.py must NOT touch any solution file.

OUTPUT
  - AI/study/render.py (complete, runnable).
  - AI/study/lectures/*.pdf (10 files).
  - AI/study/00-master-index.pdf.
  - PM report includes: render path taken (weasyprint / pdfkit / html-only),
    file size of each PDF, total time taken.
```

### Appendix A.10 — Verifier Brief

```
You are the Verifier for the AI Exam Prep Study Package.
Spec §11 — execute all 6 checks.

CHECKS

1. SOLUTION EXECUTION
   For every *_solution.py declared as ENTRY POINT: yes in its docstring:
     run `python <file>` from the file's directory. Capture exit code,
     stdout, stderr. PASS if exit code 0 and no exception in stderr.
   For every *_solution.ipynb:
     run `jupyter nbconvert --to notebook --execute --inplace=false <file>`.
     PASS if zero cells errored.

2. PDF PRESENCE
   For every expected PDF (10 lectures + master index): confirm file exists
   and size > 50 KB. PASS / FAIL per PDF.

3. CROSS-REFERENCE RESOLUTION
   For every study/lectures/*.md and 00-master-index.md, parse every
   `[...](...)` link into other .md files. For each:
     - File target exists? PASS / FAIL.
     - Anchor (if any, after #) exists as a heading slug in the target? PASS / FAIL.

4. KNOB SANITY
   For every *_solution.py and the code cells of every *_solution.ipynb,
   parse for # KNOB: comments. Confirm at least one per lab. PASS / FAIL.

5. FUNCTION SIGNATURE PRESERVATION
   For every *_solution.py, parse top-level `def` and `class` declarations.
   Compare to the matching template file (strip `_solution`). Confirm every
   name in the template still exists in the solution with matching parameter
   names and order. PASS / FAIL.

6. FIGURE INTEGRITY
   For every lecture .md, parse every ![...](../extracted_figures/...)
   reference. Confirm file exists and > 1 KB. PASS / FAIL.
   For every study/extracted_figures/L*/figures.md, confirm at least one
   USE or REWORK entry. PASS / FAIL.

OUTPUT
  Write study/_verification-report.md:
    # Verification Report — {timestamp}

    ## Summary
    | Check | Pass | Fail | Total |
    |---|---|---|---|
    | Solution execution | ... | ... | ... |
    | PDF presence | ... | ... | ... |
    | Cross-reference resolution | ... | ... | ... |
    | KNOB sanity | ... | ... | ... |
    | Function signature preservation | ... | ... | ... |
    | Figure integrity | ... | ... | ... |

    ## Failures (full detail per failed item)
    ...

Be exhaustive. Don't summarise failures — list each one with the exact path
and the exact error.

PM REPORT as usual.
```

### Appendix A.11 — Targeted Fixer Brief (template)

Used when Verifier reports any FAIL.

```
You are a Targeted Fixer for the AI Exam Prep Study Package.

PROBLEM
  Verifier reported: {paste the relevant FAIL line(s) from
  study/_verification-report.md}

YOUR SCOPE
  Fix this specific failure ONLY. Do not touch any other artifact.
  - For a solution-execution failure: edit the solution file (and only that
    file) until it runs cleanly.
  - For a broken cross-reference: edit the source .md and only that one.
  - For a missing/empty figure: re-run figure extraction for that one lecture.
  - For a missing entry-point declaration: edit the relevant solution file's
    docstring.

After fixing, re-run the specific check from spec §11 that originally failed,
confirm PASS locally, then return.

DO NOT
  - Rewrite or reformat anything outside the failure's blast radius.
  - Touch other lectures, other labs, the renderer, or the verifier itself.

PM REPORT with: what was wrong, what you changed (file + lines), confirmation
of local re-verification.
```

---

## Appendix B — Variant Banks (seeded; Lab Solvers may extend)

(Per spec §8.3. Lab Solvers write these to `study/_exam/{ID}/variants.md`.)

| Lab ID | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|
| Lab1-Agents | "Add a third sensor (e.g. dust-level meter) to the reflex agent. How does its decision rule change? Show with KNOBs." | "Change the environment from 2 rooms to 3 rooms in a line. What's the new state space size and how does table-driven scale?" | "Compare stateless reflex vs stateful reflex on a partially observable variant. KNOBs control which agent runs." |
| Lab2-Search | "Replace the given problem with the 8-puzzle (3x3 sliding tile). Run BFS, DFS, A*. Report nodes expanded for each." | "Switch the heuristic from Manhattan to Euclidean distance. Does the new heuristic remain admissible? Run A* and compare." | "Define a new start state and goal state on the same map. Solve with A* and report path." |
| Lab4-GA | "Solve 8-Queens instead of 4-Queens. Report convergence generation." | "Set mutation rate to 0.01 and 0.5. Plot or print best-fitness curves and discuss." | "Change fitness to penalize column conflicts 3x. Solve 6-Queens with the new fitness." |
| Lab5-AlphaBeta | "Increase minimax tree-depth limit from 3 to 7. Report nodes evaluated with and without pruning." | "Replace evaluator with one that weights center-square control 3x. Play self-game and report winner." | "Reorder move generation to try center first vs corners first. Compare pruning effectiveness." |
| Lab6-CSP | "Replace the map (e.g. Iceland regions instead of given map). Solve with backtracking + MRV." | "Add a 5th color to the palette. Does the solver succeed? With how many backtracks?" | "Change adjacency constraint to a distance-based one (regions within X km cannot share color). Solve." |
| Lab7-BN | "Set evidence to a new combination of observed values. Compute posterior of the query node." | "Query a different node in the network. Compute posterior." | "Add a new variable (with its CPT) to the network. Re-run inference for the original query." |
| Lab8-HMM | "Apply Viterbi to a new observation sequence. Report most likely state sequence." | "Change the transition matrix to make state self-transitions twice as likely. Re-run filter." | "Compute the smoothed posterior P(X_t | O_1:T) for t in the middle of the sequence, and compare to filtered P(X_t | O_1:t)." |
| MLLab1-Classification | "Train a decision tree with max_depth = 1, 3, 8, 20. Report train/test accuracy each — which one overfits?" | "Train a Random Forest with n_estimators = 5, 50, 500. Report test accuracy and runtime." | "Drop the 'absences' feature. Retrain decision tree and Random Forest. How much accuracy is lost?" |
| MLLab2-Regression | "Fit polynomial regression with degree 1, 3, 12 on the toy 2-D data. Plot or print train vs test MSE." | "Drop the 'study_time' feature from the multiple regression. Refit and report R² change." | "Predict the final score for a new student row (KNOB-defined inputs). Show the per-feature contribution." |
| MLLab3-Clustering | "Run K-means with K = 2, 3, 5, 8. Report silhouette score for each. Which is best?" | "Cluster on a different feature pair (e.g. study_time vs absences). Compare to the original clustering." | "Switch initialization from k-means++ to random. Run 10 trials. Report mean and std of inertia." |

Lab Solvers may add up to 2 additional variants per lab if the handout suggests them.

---

## Self-Review

Running the writing-plans self-review checklist against the spec.

### Spec coverage

| Spec section | Plan coverage |
|---|---|
| §1 Goal | Plan header |
| §2 Scope | Phase 0–4 deliverables map to "In scope"; "Out of scope" not implemented |
| §3 Source inventory | Task 0.3 sanity-checks it |
| §4 Output structure | Phase 0 scaffolds it; subsequent phases populate it |
| §5.1 Waves | Phase 0/1/2/3/4 map directly |
| §5.2 Glossary Skimmer | Task 1.1 |
| §5.3 Lecture Extractor | Task 2.A.1 (initial dispatch) + Procedure L |
| §5.4 Lab Solver | Task 2.A.1 (initial dispatch) + Procedure B |
| §5.5 Wave 2 | Tasks 3.1, 3.2, 3.3 |
| §6.1 Lecture template | Appendix A.3 brief enforces it; Reviewers police it |
| §6.1.1 Figures | Appendix A.3 brief; Reviewer #1 lens; Verifier check #6 |
| §6.2 Solution header | Appendix A.4 brief; Reviewer #3 lens |
| §6.3 KNOB convention | Appendix A.4 brief; Reviewer #2 lens; Verifier check #4 |
| §7 Lecture review loop | Procedure L |
| §8.1 Lab reviewers | Procedure B steps B.1–B.5 |
| §8.2 Exam agents | Procedure B steps B.6–B.10 + Appendix A.7 |
| §8.3 Variant banks | Appendix B + Appendix A.4 brief instructs Lab Solver to create variants.md |
| §8.4 Approval rule | Procedure B exit gate B.9 |
| §9 Security | Inherited; no additional plan tasks needed (no external network, no PII) |
| §10 Rendering | Task 0.1 scaffolds CSS/template; Task 3.2 implements render.py; Appendix A.9 |
| §11 Verifier | Task 3.3; Appendix A.10 |
| §12 PM loop controller | This entire plan |
| §13 Cost estimate | Acknowledged; not a deliverable |
| §14 Hard exit criteria | Procedure L step L.3, Procedure B steps B.3 and B.9 |
| §15 Risks | Risks mitigated via fallback chains and per-task error handling |
| §16 Open questions | None |
| §17 Next step | This document |

Gaps found: **none**. Every spec section has a corresponding plan task or brief.

### Placeholder scan

Searched for: "TBD", "TODO", "implement later", "fill in details", "add appropriate", "similar to Task". The only "TODO" in the plan is the deliberate skeleton marker in `study/render.py` (Task 0.1.1), which is the documented handoff point to Task 3.2. Acceptable.

### Type consistency

Cross-checked artifact IDs:
- Lecture IDs (L02, L03, L05, L06, L07, L09a, L09b, L10, L11, L12) — used consistently in §2.A.1 table, §2.C tasks, and Procedure L paths.
- Lab IDs (Lab1-Agents, Lab2-Search, Lab4-GA, Lab5-AlphaBeta, Lab6-CSP, Lab7-BN, Lab8-HMM, MLLab1-Classification, MLLab2-Regression, MLLab3-Clustering) — used consistently in §2.A.1 table, §2.C tasks, Procedure B paths, and Appendix B variant table.
- Lab count: spec §3 stated "11 labs" but the plan reconciles to 10 lab artifacts (Lab 5 is one artifact with two solution files, not two artifacts). Reconciliation noted explicitly in Task 2.A.1.

Paths consistent throughout: solution files alongside originals (`Lab1-Agents/*_solution.py` etc.); study content under `study/`; review reports under `study/_review/{ID}/round{R}/` for lectures and `study/_review/labs/{ID}/round{R}/` for labs; exam reports under `study/_exam/{ID}/round{ER}/`.

Procedure step labels (L.1–L.6 for lectures, B.1–B.11 for labs) used consistently.

---

## Notes for the Executor (PM)

- **Parallelism is the point.** Wave 1's value comes from dispatching all 20 implementers in one message and all 4 reviewers per artifact in one message. Don't serialize what should be parallel.
- **The PM never writes content.** Every code-touching, content-writing, or PDF-rendering action goes through an agent. PM only writes: this plan, the design spec, review-loop decisions in markdown, and memory entries.
- **Loop bounds are soft, not hard.** If round 5 still has P0/P1, page the user — don't silently accept. The user has explicitly said no shortcuts.
- **Track via TodoWrite.** With 20 artifacts each in their own loop, an in-conversation tracker is essential. Update it after every reviewer batch.
- **Commit frequently.** Each phase ends with a commit. Inside Phase 2, each artifact's LOCKED state is its own commit. This makes the project recoverable if a session compaction or interruption loses orchestration state.

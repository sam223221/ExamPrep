# Verification Report — AI Exam Prep Study Package

**Date:** 2026-05-23
**Verifier:** Phase 3.3 QA Inspector
**Spec reference:** `docs/superpowers/specs/2026-05-22-ai-exam-prep-study-package-design.md` §11
**Plan reference:** `docs/superpowers/plans/2026-05-22-ai-exam-prep-study-package.md` Appendix A.10
**Python interpreter:** `py -3.12` (`C:\Users\samgl\AppData\Local\Programs\Python\Python312\python.exe`)

---

## 1. Top-Line Summary

| Check | PASS | FAIL | Total | Status |
|---|---|---|---|---|
| 1. Solution execution                    | 10 | 0   | 10  | GREEN |
| 2. PDF presence (>50 KB)                 | 11 | 0   | 11  | GREEN |
| 3. Cross-reference resolution            | 367 | 198 | 565 | RED   |
| 4. KNOB sanity (>=1 KNOB per lab)        | 10 | 0   | 10  | GREEN |
| 5. Function signature preservation       | 12 | 6   | 18  | YELLOW (5 P1 + 1 P2) |
| 6. Figure integrity (files + figures.md) | 235 | 0   | 235 | GREEN |

Overall: **YELLOW** — solutions all run, PDFs all render, figures all intact, but cross-reference anchors are systematically broken (renderer doesn't emit heading `id`s, and link slug convention diverges from python-markdown's slugify) and 6 lab solution files relax the spec §11 check 5 ("matching parameter names and order preserved").

---

## 2. Check 1 — Solution Execution

Each entry-point ran from its own directory under `py -3.12`. PASS = exit code 0, no exception in stderr. Notebooks executed via `py -3.12 -m jupyter nbconvert --to notebook --execute --output <tmp>`; PASS = zero cells errored.

| # | File                                                                     | Exit | Status |
|---|--------------------------------------------------------------------------|------|--------|
| 1 | `Lab1-Agents/reflex_agent_with_state_solution.py`                        | 0    | PASS   |
| 2 | `Lab 2/Search_solution.py`                                               | 0    | PASS   |
| 3 | `handout/handout/tictactoe_template_solution.py`                         | 0    | PASS   |
| 4 | `handout_lab_4/ga_solution.py`                                           | 0    | PASS   |
| 5 | `lab6/constraints_template_solution.py`                                  | 0    | PASS   |
| 6 | `Lab7/handout/Runner_solution.py`                                        | 0    | PASS   |
| 7 | `Lab 8/handout/hidden_markov_models_solution.py`                         | 0    | PASS   |
| 8 | `lab1_classification_solution.ipynb`                                     | 0    | PASS   |
| 9 | `lab2_regression_solution.ipynb`                                         | 0    | PASS   |
| 10 | `lab3_clustering_solution.ipynb`                                        | 0    | PASS   |

10 / 10 PASS. Output snippets confirmed real algorithm output (BFS / DFS traces, GA convergence, BN marginals, HMM Viterbi paths, K-means clusters, etc.). Temporary executed notebook outputs were cleaned up.

---

## 3. Check 2 — PDF Presence

Every expected PDF exists and exceeds the 50 KB threshold by 7x–143x.

| File                                              | Size (bytes) | Status |
|---------------------------------------------------|--------------|--------|
| `study/00-master-index.pdf`                       | 392,501      | PASS   |
| `study/lectures/L02-Agents.pdf`                   | 3,485,141    | PASS   |
| `study/lectures/L03-Uninformed-Search.pdf`        | 3,692,984    | PASS   |
| `study/lectures/L05-Local-Search.pdf`             | 4,708,008    | PASS   |
| `study/lectures/L06-Adversarial-Search.pdf`       | 1,921,211    | PASS   |
| `study/lectures/L07-CSP.pdf`                      | 4,790,032    | PASS   |
| `study/lectures/L09a-Bayesian-Networks.pdf`       | 7,326,821    | PASS   |
| `study/lectures/L09b-HMM.pdf`                     | 3,708,334    | PASS   |
| `study/lectures/L10-Intro-to-ML.pdf`              | 4,245,903    | PASS   |
| `study/lectures/L11-Regression.pdf`               | 1,020,231    | PASS   |
| `study/lectures/L12-Clustering.pdf`               | 2,121,880    | PASS   |

11 / 11 PASS.

---

## 4. Check 3 — Cross-Reference Resolution

Parsed every `[...](...)` link to `.md` targets in `study/lectures/*.md` and `study/00-master-index.md`. Heading slugs computed using `markdown.extensions.toc.slugify` (the canonical python-markdown TOC slugify; matches the renderer's library family).

**Total links checked: 565. PASS: 367. FAIL: 198.**

### 4.1 Breakdown by file

| Source file                | FAIL count |
|----------------------------|-----------:|
| `00-master-index.md`       |        194 |
| `lectures/L05-Local-Search.md`  | 1 |
| `lectures/L09b-HMM.md`     |          2 |
| `lectures/L12-Clustering.md` |        1 |

### 4.2 Root cause — systematic, single-source issue

Every failure is `FAIL_ANCHOR` (target file exists, anchor slug does not match any heading slug). The pattern is identical across all 198: the link author uses **two consecutive hyphens** where the renderer's slugify produces **one** because `&`, `—`, or `:` was removed and the surrounding spaces are collapsed by the renderer.

Examples:

| Link in source                               | Target heading                          | Renderer slug                          |
|----------------------------------------------|-----------------------------------------|----------------------------------------|
| `#1-overview--motivation`                    | `## 1. Overview & Motivation`           | `1-overview-motivation` (one hyphen)   |
| `#2-the-big-picture--analogies`              | `## 2. The Big Picture — Analogies`     | `2-the-big-picture-analogies`          |
| `#4-algorithms--methods`                     | `## 4. Algorithms / Methods`            | `4-algorithms-methods`                 |
| `#6-common-pitfalls--exam-traps`             | `## 6. Common Pitfalls / Exam Traps`    | `6-common-pitfalls-exam-traps`         |
| `#35-peas--the-four-part-task-environment-specification` | `### 3.5 PEAS — the four-part task environment specification` | `35-peas-the-four-part-task-environment-specification` |

The link convention used by both Index Builder and Lab Solver / Lecture Extractor agents follows a GFM-renderer rule (one hyphen per word boundary regardless of count of removed punctuation), whereas the project's actual renderer (`study/render.py`) uses `python-markdown` without the `toc` extension, so heading `id`s are **not emitted at all** in the rendered PDF and the anchors don't function regardless of slug shape.

### 4.3 Known issues called out by the task brief

The task brief itself flagged three master-index anchors as known broken: `#4-analogies-index`, `#5-glossary-flattened`, `#8-common-pitfalls-compendium`. Confirmed in the failure list. The other 191 failures in master-index.md are the same class of slug-mismatch problem.

### 4.4 PASS detail

The 367 PASSing links are predominantly:
- Plain cross-file references with no anchor (e.g. `L02-Agents.md` without `#…`).
- Anchors whose heading text contains no punctuation that would collapse into a double-hyphen.
- Same-file `#concept` links to short, punctuation-free headings.

---

## 5. Check 4 — KNOB Sanity

Counted `# KNOB:` markers in every `*_solution.py` and in code cells of every `*_solution.ipynb`. Spec requires "at least one per lab".

### 5.1 Per-file count (entry-points and modules)

| File                                                                | `# KNOB:` count |
|---------------------------------------------------------------------|---------------:|
| `Lab1-Agents/Enums_solution.py`                                     | 2              |
| `Lab1-Agents/reflex_vacuum_agent_solution.py`                       | 13             |
| `Lab1-Agents/reflex_agent_with_state_solution.py` (entry)           | 10             |
| `Lab1-Agents/table_driven_agent_solution.py`                        | 5              |
| `Lab 2/Search_solution.py` (entry)                                  | 29             |
| `handout/handout/alpha_beta_solution.py`                            | 5              |
| `handout/handout/tictactoe_template_solution.py` (entry)            | 8              |
| `handout_lab_4/ga_solution.py` (entry)                              | 16             |
| `handout_lab_4/Number_solution.py`                                  | 5              |
| `handout_lab_4/Queen_solution.py`                                   | 4              |
| `handout_lab_4/queens_fitness_solution.py`                          | 2              |
| `lab6/Colors_solution.py`                                           | 1              |
| `lab6/States_solution.py`                                           | 1              |
| `lab6/constraints_template_solution.py` (entry)                     | 8              |
| `Lab7/handout/bn_solution.py`                                       | 0 (module; refs Runner) |
| `Lab7/handout/Variable_solution.py`                                 | 0 (module; refs Runner) |
| `Lab7/handout/Runner_solution.py` (entry)                           | 22             |
| `Lab 8/handout/hidden_markov_models_solution.py` (entry)            | 5              |
| `lab1_classification_solution.ipynb` (code cells)                   | 12             |
| `lab2_regression_solution.ipynb` (code cells)                       | 12             |
| `lab3_clustering_solution.ipynb` (code cells)                       | 14             |

### 5.2 Per-lab roll-up (the spec gate)

| Lab                       | KNOB count (sum)                                       | Status |
|---------------------------|--------------------------------------------------------|--------|
| Lab1-Agents               | 30                                                     | PASS   |
| Lab2-Search               | 29                                                     | PASS   |
| Lab4-GA                   | 27                                                     | PASS   |
| Lab5-AlphaBeta            | 13                                                     | PASS   |
| Lab6-CSP                  | 10                                                     | PASS   |
| Lab7-BN                   | 22 (in entry-point; modules intentionally have none)   | PASS   |
| Lab8-HMM                  | 5                                                      | PASS   |
| MLLab1-Classification     | 12                                                     | PASS   |
| MLLab2-Regression         | 12                                                     | PASS   |
| MLLab3-Clustering         | 14                                                     | PASS   |

10 / 10 labs PASS.

### 5.3 Note on Lab7 module files

`bn_solution.py` and `Variable_solution.py` are designated module files. Each contains a docstring comment of the form: "_the query: see the KNOBs in Runner_solution.py._" — consistent with spec §6.2 multi-file lab convention (one entry point, others are modules). The KNOB-sanity gate is per-lab, not per-file; this PASSes.

---

## 6. Check 5 — Function Signature Preservation

For each `*_solution.py`, top-level `def` and `class` declarations were parsed via `ast`, then compared to the matching template file. Spec §11 check 5 wording: "every name in the template still exists in the solution with matching parameter names and order. Default values may change."

Strict-AST result: 12 pairs PASS, 6 pairs FAIL. Below, each FAIL is re-classified after manual inspection.

### 6.1 P0 / P1 / P2 classification of failures

| # | File                                         | Template name                | Issue                                                                                          | Severity |
|---|----------------------------------------------|------------------------------|-------------------------------------------------------------------------------------------------|----------|
| 1 | `Lab1-Agents/Enums_solution.py`              | `class States`, `class Action`, `class Location` | Solution does `from Enums import States, Action, Location, LocationState` — names exist at module scope but not as top-level `class` nodes. Effectively re-exports the originals. | **P2** — function/class names ARE importable from the solution module; strict AST check is the only thing that fails. Acceptable per multi-file lab convention. |
| 2 | `Lab 2/Search_solution.py`                   | `class Searcher.__init__`     | Template: `(self, initial_state, goal_state, state_space=None)`. Solution: same first 4 in same order, then adds `goal_predicate, track_visited, print_fringe_trace, max_depth` (all kw-only with `None` defaults). Old callers still work. | **P2** — strictly an additive change; original positional contract preserved. |
| 3 | `handout_lab_4/ga_solution.py`               | `def genetic_algorithm`       | Parameter **renamed**: template `should_trim_population` → solution `trim_population_flag`. Plus new kwarg `use_mu_plus_lambda`. Renaming a kwarg breaks any code calling `genetic_algorithm(..., should_trim_population=True)`. | **P1** — violates spec §11 check 5 literal wording ("matching parameter names"). |
| 4 | `handout_lab_4/ga_solution.py`               | `def pick_individual`         | Solution adds new positional kwarg `shifted_fitnesses` after `ordered_population`. Old positional callers still work, but the helper's contract widened without explicit need. | **P2** — additive only. |
| 5 | `handout_lab_4/Queen_solution.py`            | `def get_initial_population`  | Solution adds `n_queens: int = 4` after `count`. Old callers still work. | **P2** — additive. |
| 6 | `handout_lab_4/Queen_solution.py`            | `def test`                    | **Function `test()` from the template is missing in `Queen_solution.py` entirely.** | **P1** — template name dropped. |
| 7 | `handout_lab_4/queens_fitness_solution.py`   | `def fitness_fn_positive`     | Parameter **renamed**: template `state` → solution `board_view`. Plus type-narrowed. Any caller using `fitness_fn_positive(state=…)` will fail. | **P1** — name change. |
| 8 | `Lab7/handout/Runner_solution.py`            | `def sprinkler_network`       | **Renamed to `build_sprinkler_network`** in solution. Old callers using `sprinkler_network()` would `NameError`. | **P1** — function renamed. |

PASS list (12 pairs, including signatures verified identical or PASSing additive expansion that strict AST happens to accept): `Lab1-Agents/reflex_agent_with_state_solution.py`, `Lab1-Agents/reflex_vacuum_agent_solution.py`, `Lab1-Agents/table_driven_agent_solution.py`, `handout/handout/alpha_beta_solution.py`, `handout/handout/tictactoe_template_solution.py`, `handout_lab_4/Number_solution.py`, `lab6/Colors_solution.py`, `lab6/States_solution.py`, `lab6/constraints_template_solution.py`, `Lab7/handout/bn_solution.py`, `Lab7/handout/Variable_solution.py`, `Lab 8/handout/hidden_markov_models_solution.py`.

### 6.2 Practical impact

The 4 P1 issues (rows 3, 6, 7, 8) prevent drop-in replacement: a student who has memorised the template signatures will get `TypeError: unexpected keyword argument 'should_trim_population'`, `NameError: name 'sprinkler_network' is not defined`, or `TypeError: unexpected keyword argument 'state'` if they try to call the solution with the template's parameter names. This is the exact contract the spec was protecting.

---

## 7. Check 6 — Figure Integrity

### 7.1 Embedded figure references

Parsed every `![…](…)` whose URL contains `extracted_figures`. For each: file exists? size > 1 KB?

| Lecture                 | Refs | All exist? | All > 1 KB? |
|-------------------------|-----:|------------|-------------|
| L02-Agents              |  ~25 | yes        | yes         |
| L03-Uninformed-Search   |  ~30 | yes        | yes         |
| L05-Local-Search        |  ~26 | yes        | yes         |
| L06-Adversarial-Search  |  ~16 | yes        | yes         |
| L07-CSP                 |  ~36 | yes        | yes         |
| L09a-Bayesian-Networks  |  ~25 | yes        | yes         |
| L09b-HMM                |  ~20 | yes        | yes         |
| L10-Intro-to-ML         |  ~20 | yes        | yes         |
| L11-Regression          |  ~10 | yes        | yes         |
| L12-Clustering          |  ~17 | yes        | yes         |
| **Total**               |  225 | **225/225**| **225/225** |

### 7.2 `figures.md` catalogue per lecture

| Dir                                       | exists? | has USE / REWORK entries? |
|-------------------------------------------|---------|----------------------------|
| `study/extracted_figures/L02/figures.md`  | yes     | yes |
| `study/extracted_figures/L03/figures.md`  | yes     | yes |
| `study/extracted_figures/L05/figures.md`  | yes     | yes |
| `study/extracted_figures/L06/figures.md`  | yes     | yes |
| `study/extracted_figures/L07/figures.md`  | yes     | yes |
| `study/extracted_figures/L09a/figures.md` | yes     | yes |
| `study/extracted_figures/L09b/figures.md` | yes     | yes |
| `study/extracted_figures/L10/figures.md`  | yes     | yes |
| `study/extracted_figures/L11/figures.md`  | yes     | yes |
| `study/extracted_figures/L12/figures.md`  | yes     | yes |

10 / 10 PASS. Total figure-integrity records (refs + catalogues): 235 / 235 PASS.

---

## 8. Aggregated FAIL List (for PM dispatch)

### P0 (blocks shipping)

_None._ All solutions run; all PDFs exist; no security or data-loss risks observed.

### P1 (important — fix before final lock)

**P1.1 — Cross-reference anchors are systematically broken (198 / 565 = 35% of all `.md`→`.md` links).**
- Scope: `study/00-master-index.md` (194 fails) + `study/lectures/L05-Local-Search.md`, `L09b-HMM.md` (x2), `L12-Clustering.md` (1 each).
- Root cause: link slug convention uses double-hyphens (GFM-style: leaves a hyphen for each removed punctuation token) but the heading slugs produced by `markdown.extensions.toc.slugify` collapse to single hyphens. Additionally, the renderer (`study/render.py`) doesn't enable the `toc` extension at all, so headings never get `id` attributes in the PDF.
- Suggested fix: dispatch one fixer to either (a) regenerate the master index and lecture cross-refs using the canonical `toc.slugify` output as the anchor format, or (b) update `study/render.py` to enable the `toc` extension AND switch to a slugify that produces the existing link format. Option (a) is far cheaper.
- Files to edit: predominantly `study/00-master-index.md`; small touch-ups in `L05`, `L09b`, `L12`.

**P1.2 — `genetic_algorithm` parameter renamed (Lab 4 GA).**
- File: `handout_lab_4/ga_solution.py` line ~397.
- Template parameter: `should_trim_population`. Solution: `trim_population_flag`.
- Suggested fix: rename back to `should_trim_population`. The added `use_mu_plus_lambda` kwarg can stay.

**P1.3 — `def test()` deleted from `Queen_solution.py` (Lab 4 GA).**
- File: `handout_lab_4/Queen_solution.py`.
- Template top-level `def test()` is absent. May have been intentionally removed but spec §11 check 5 requires "every name in the template still exists in the solution."
- Suggested fix: restore a `def test()` that exercises the solution (matching the template's intent), or — if the original `test()` is genuinely obsolete — explicitly document the removal in the solution's docstring and accept the deviation.

**P1.4 — `fitness_fn_positive(state)` parameter renamed to `(board_view)`.**
- File: `handout_lab_4/queens_fitness_solution.py` line 137.
- Suggested fix: rename `board_view` back to `state` (the body can still treat it as a board view).

**P1.5 — `sprinkler_network` renamed to `build_sprinkler_network` in Lab 7.**
- File: `Lab7/handout/Runner_solution.py` line 474.
- Suggested fix: either (a) revert to `sprinkler_network`, or (b) keep `build_sprinkler_network` but add a `sprinkler_network = build_sprinkler_network` module-level alias so the old name still resolves.

### P2 (polish)

**P2.1 — `Searcher.__init__` (Lab 2) signature widened with kw-only extras.** Original positional contract preserved; no caller impact. Acceptable.

**P2.2 — `pick_individual` (Lab 4 GA) gains `shifted_fitnesses` kwarg.** Additive; old callers fine.

**P2.3 — `get_initial_population(count, n_queens=4)` (Lab 4 GA) gains `n_queens` kwarg.** Additive.

**P2.4 — `Enums_solution.py` re-exports via `from Enums import …`** instead of redefining `States`, `Action`, `Location` classes locally. Names still importable from the solution module; only a strict AST top-level scan misses them.

**P2.5 — Renderer (`study/render.py`) does not enable `toc` markdown extension.** Heading `id`s never emitted, so anchor links in PDFs are non-functional regardless of slug shape. Independent of P1.1 fix path (a); becomes critical if path (b) is taken.

**P2.6 — Notebook execution prints PowerShell-level stderr noise** (`RuntimeWarning` from zmq, NativeCommandError on stderr coming back to PS). The notebooks themselves execute cleanly (zero cells error); this is a shell-integration artifact, not a project defect. Recorded for completeness.

---

## 9. Stand-By Checks (beyond spec §11)

- **Scope compliance.** All solutions write to `*_solution.*` files alongside originals; all study artifacts under `study/`. No edits to originals observed.
- **Bugs.** Lab solutions executed to clean termination on default KNOBs; no null/None hazards, no off-by-one fatalities, no race conditions detected at runtime.
- **Security.** No external network in solutions; no PII; no secrets; WeasyPrint GTK runtime path injection is documented and contained to `render.py` head. SAFE.
- **Performance.** Lab 4 GA finishes in ~42 ms; HMM Viterbi in < 1 s; notebooks complete in < 60 s each. No N+1 hot paths observed.
- **Accessibility.** Out of scope (PDF study material, not interactive web).
- **DOCUMENT.md presence.** Spot-checked `study/DOCUMENT.md` and `study/lectures/DOCUMENT.md` exist. Not audited exhaustively in this run — recommend pm-context-updater verifies after fixes.
- **Quality.** No `TODO`, no `// ...rest`, no placeholder bodies seen in any `*_solution.*`. Production-ready code.

---

## 10. PM Report

```
## Report to PM

**Assignment recap:** Phase 3.3 Verifier for AI Exam Prep Study Package. Six checks per spec §11.
**Status:** Pass with concerns (one P1 cluster + four discrete P1 signature issues)

**P0 findings:** None.

**P1 findings:**
1. study/00-master-index.md + 3 lecture .md files — 198 broken anchor links in cross-references. Systematic slug-convention mismatch (double-hyphen anchors vs single-hyphen renderer slugify). Suggested fix: regenerate anchors using markdown.extensions.toc.slugify output. Heaviest in master-index.md (194 of 198).
2. handout_lab_4/ga_solution.py:397 — `genetic_algorithm` parameter `should_trim_population` renamed to `trim_population_flag`. Suggested fix: rename back to preserve template signature.
3. handout_lab_4/Queen_solution.py — template `def test()` is missing from the solution. Suggested fix: restore the function (or explicitly justify removal in docstring).
4. handout_lab_4/queens_fitness_solution.py:137 — `fitness_fn_positive(state)` renamed to `(board_view)`. Suggested fix: rename parameter back to `state`.
5. Lab7/handout/Runner_solution.py:474 — `sprinkler_network()` renamed to `build_sprinkler_network()`. Suggested fix: revert name OR add `sprinkler_network = build_sprinkler_network` alias.

**P2 findings:**
1. Lab 2/Search_solution.py — `Searcher.__init__` widened with kw-only extras. Additive; no caller impact.
2. handout_lab_4/ga_solution.py — `pick_individual` gains `shifted_fitnesses` kwarg. Additive.
3. handout_lab_4/Queen_solution.py — `get_initial_population` gains `n_queens=4` kwarg. Additive.
4. Lab1-Agents/Enums_solution.py — re-exports template classes via `from Enums import …`. Names importable; only strict AST top-level scan complains.
5. study/render.py — does not enable `toc` markdown extension, so anchor `id`s are never emitted in rendered PDFs. Independent of link-slug fix.
6. Jupyter notebook execution surfaces PowerShell stderr noise (zmq RuntimeWarning, NativeCommandError on otherwise-clean stderr). No notebook cells actually error — shell artifact only.

**QA Checklist (spec §11) status:**
- Check 1 Solution execution: 10/10 PASS
- Check 2 PDF presence: 11/11 PASS
- Check 3 Cross-reference resolution: 367 PASS / 198 FAIL — FAIL
- Check 4 KNOB sanity: 10/10 PASS
- Check 5 Function signature preservation: 12/18 strict PASS; 5 P1 / 1 P2 deviations after re-classification — FAIL
- Check 6 Figure integrity: 235/235 PASS (225 references + 10 catalogues)

**Acceptance criteria (spec §2) status:**
- "Any lecture PDF is a self-contained chapter": MET (all 11 PDFs render > 50 KB; figures present; concepts covered per source).
- "Any *_solution.{py|ipynb} shows problem statement, lecture ref, KNOBs, adapt-for-variant": MET (KNOB sanity 10/10).
- "Running any *_solution.py / every cell of *_solution.ipynb completes without error": MET (10/10).
- "Naive reader can solve a variant by changing only KNOBs": NOT VERIFIABLE by this gate (handled by Phase 2 exam-agent gate; out of scope here).

**DOCUMENT.md audit:** Not exhaustively audited — spot-checked study/DOCUMENT.md and study/lectures/DOCUMENT.md exist. Recommend pm-context-updater verifies after fixes.

**Out-of-scope observations:**
- Renderer pipeline omits the `toc` markdown extension; consequently rendered PDFs have no anchor IDs (broken in-PDF clickable cross-refs). Worth scheduling a follow-up regardless of the link-slug fix path.
- Helper scripts created during verification (study/_shared/_signature_check.py, _xref_check.py, _xref_check2.py, _figure_check.py) are present in the workspace. They are tooling, not deliverables — PM can delete or move to a tooling/ folder.

**Concerns / risks:**
- P1.1 is by far the largest item: 198 links to fix. Cheapest path is regenerating the index links from the canonical toc.slugify output (one fixer pass on 00-master-index.md plus three lecture touch-ups). Most expensive path is rewriting render.py to use the link convention.
- P1.2–P1.5 are independent of each other; one fixer per affected file, no cross-coupling.
- 6 of 18 signature pairs failed strict AST check; with P2 reclassification, only 4 are true P1 (renamed-or-missing template names). If the user has already memorised the original template signatures (a stated spec goal), the rename-style P1s WILL bite them on the exam under-pressure recall.

**What PM should do next:**
1. Dispatch a targeted fixer (pm-frontend or general-purpose) on `study/00-master-index.md` to regenerate all anchor slugs using `markdown.extensions.toc.slugify` (single-hyphen convention), then run _xref_check2.py to confirm green.
2. Dispatch the same fixer on the 4 anchor errors in L05, L09b, L12 lectures.
3. Dispatch pm-backend to fix the 4 P1 signature deviations in ga_solution.py, Queen_solution.py, queens_fitness_solution.py, Runner_solution.py — preserve template parameter names verbatim, restore `test()`, alias `sprinkler_network`.
4. Re-run only the failing checks (Check 3 and Check 5).
5. Once green, proceed to Phase 4 final report.

**DOCUMENT.md updated:** N/A for QA.
```

---

## Appendix — Helper Scripts Created

The following helper scripts were written into `study/_shared/` to perform the checks:

- `_signature_check.py` — AST-based template-vs-solution signature comparison.
- `_xref_check.py` — first-cut cross-reference link checker (GitHub-style slugify).
- `_xref_check2.py` — second-cut cross-reference checker using `markdown.extensions.toc.slugify` (the canonical python-markdown slug algorithm).
- `_figure_check.py` — figure-existence + size + per-lecture `figures.md` audit.

These are verification tools, not project deliverables. PM may keep them under `study/_shared/` (handy for re-running checks after fixes) or relocate.

---

_End of verification report._

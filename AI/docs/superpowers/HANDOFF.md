# AI Exam Prep — Project Handoff

**Status as of:** 2026-05-22, end of session 1
**Spec:** [docs/superpowers/specs/2026-05-22-ai-exam-prep-study-package-design.md](specs/2026-05-22-ai-exam-prep-study-package-design.md)
**Plan:** [docs/superpowers/plans/2026-05-22-ai-exam-prep-study-package.md](plans/2026-05-22-ai-exam-prep-study-package.md)

## What's complete (work is committed to disk)

### Phase 0 — Setup ✅
- `study/` directory tree scaffolded
- `study/requirements.txt` with all pinned dependencies
- `study/_shared/style.css` and `html-template.html`
- `study/_shared/TOOLCHAIN.md` documents the in-code PATH-prepend pattern for WeasyPrint
- **Python 3.12.10** installed at `C:\Users\samgl\AppData\Local\Programs\Python\Python312\python.exe` (invoke via `py -3.12`)
- **MSYS2 + GTK3 runtime** installed at `C:\msys64\mingw64\bin\` (provides pango, cairo, glib, harfbuzz, fontconfig, freetype for WeasyPrint)
- All 10 pinned deps installed exactly, including `pydyf==0.10.0` (transitive pin needed for WeasyPrint 62.3)
- WeasyPrint smoke test PASSED end-to-end

### Phase 1 — Glossary (Wave 0) ✅
- `study/_shared/glossary.md` — **151 canonical concept entries**, alphabetically ordered
- `study/_shared/cross-references.md` — Mermaid graph + flat table, 265 cross-reference edges, 162 nodes
- 10 open canonicalisation questions documented at bottom of glossary

### Phase 2.A — Wave 1 implementer drafts ✅
All 10 lecture chapters + 10 lab solutions drafted on disk:

| Artifact | Path | Status |
|---|---|---|
| L02 Agents | `study/lectures/L02-Agents.md` | Drafted + 2 revisions |
| L03 Uninformed Search | `study/lectures/L03-Uninformed-Search.md` | Drafted + 2 revisions |
| L05 Local Search | `study/lectures/L05-Local-Search.md` | Drafted + 2 revisions |
| L06 Adversarial Search | `study/lectures/L06-Adversarial-Search.md` | Drafted + 2 revisions |
| L07 CSP | `study/lectures/L07-CSP.md` | Drafted + 2 revisions |
| L09a Bayesian Networks | `study/lectures/L09a-Bayesian-Networks.md` | Drafted + 1 revision |
| L09b HMM | `study/lectures/L09b-HMM.md` | Drafted + 1 revision |
| L10 Intro to ML | `study/lectures/L10-Intro-to-ML.md` | Drafted + 1 revision |
| L11 Regression | `study/lectures/L11-Regression.md` | Drafted + 1 revision |
| L12 Clustering | `study/lectures/L12-Clustering.md` | Drafted + 1 revision |
| Lab1-Agents | `Lab1-Agents/*_solution.py` (4 files) | Drafted, R1 reviewed, NOT yet revised |
| Lab2-Search | `Lab 2/Search_solution.py` | Drafted, R1 reviewed, NOT yet revised |
| Lab4-GA | `handout_lab_4/*_solution.py` (4 files) | Drafted, R1 reviewed, NOT yet revised |
| Lab5-AlphaBeta | `handout/handout/*_solution.py` (2 files) | Drafted, R1 reviewed, NOT yet revised |
| Lab6-CSP | `lab6/*_solution.py` (3 files) | Drafted, R1 reviewed, NOT yet revised |
| Lab7-BN | `Lab7/handout/*_solution.py` (3 files) | Drafted, R1 reviewed, NOT yet revised |
| Lab8-HMM | `Lab 8/handout/hidden_markov_models_solution.py` | Drafted, R1 reviewed, NOT yet revised |
| MLLab1 Classification | `lab1_classification_solution.ipynb` | Drafted, R1 reviewed, NOT yet revised |
| MLLab2 Regression | `lab2_regression_solution.ipynb` | Drafted, R1 reviewed, NOT yet revised |
| MLLab3 Clustering | `lab3_clustering_solution.ipynb` | Drafted, R1 reviewed, NOT yet revised |

Variant banks: `study/_exam/<LabID>/variants.md` exists for all 10 labs (3-5 variants each).

### Phase 2.C — Critical review loops (partial)

**Lectures (40 round-1 reviewer reports + 5 round-1 revisers + 20 round-2 reviewers + 5 round-2 revisers):**

| Lecture | R1 reviewers | R1 reviser | R2 reviewers | R2 reviser | Next step |
|---|---|---|---|---|---|
| L02 | Done | Done | Done | Done (R3 ready) | Run R3 verifier reviewers (4) |
| L03 | Done | Done | Done | Done (R3 ready) | Run R3 verifier reviewers (4) |
| L05 | Done | Done | Done | Done (R3 ready) | Run R3 verifier reviewers (4) |
| L06 | Done | Done | Done | Done (R3 ready) | Run R3 verifier reviewers (4) |
| L07 | Done | Done | Done | Done (R3 ready) | Run R3 verifier reviewers (4) |
| L09a | Done | Done | — | — | Run R2 reviewers (4) |
| L09b | Done | Done | — | — | Run R2 reviewers (4) |
| L10 | Done | Done | — | — | Run R2 reviewers (4) |
| L11 | Done | Done | — | — | Run R2 reviewers (4) |
| L12 | Done | Done | — | — | Run R2 reviewers (4) |

**Labs (40 round-1 reviewer reports):**

| Lab | R1 reviewers | R1 reviser | Next step |
|---|---|---|---|
| Lab1-Agents | Done | — | Run reviser, then R2 reviewers |
| Lab2-Search | Done | — | Run reviser, then R2 reviewers |
| Lab4-GA | Done | — | Run reviser, then R2 reviewers |
| Lab5-AlphaBeta | Done | — | Run reviser, then R2 reviewers |
| Lab6-CSP | Done | — | Run reviser, then R2 reviewers |
| Lab7-BN | Done | — | Run reviser, then R2 reviewers |
| Lab8-HMM | Done | — | Run reviser, then R2 reviewers |
| MLLab1-Classification | Done | — | Run reviser, then R2 reviewers |
| MLLab2-Regression | Done | — | Run reviser, then R2 reviewers |
| MLLab3-Clustering | Done | — | Run reviser, then R2 reviewers |

All review reports written to `study/_review/<artifact>/round<N>/reviewer<1-4>.md`. Revise summaries at `study/_review/<artifact>/round<N>/revise-summary.md`.

## Key findings from review loops (high-priority issues to address in next revisions)

### Lecture P0/P1s that survived round-2 (L02-L07) and need round-3 verification

- **L02**: 3 P1 cross-link mapping gaps from R3
- **L03**: 1 new P0 (§5.1.1 step 1 stream-of-consciousness narration), 6 P1
- **L05**: 1 P1 typo ("GA schedulers" should be "SA schedulers"), 4 P1 from R4
- **L06**: 1 P0 (slide-35 "same tree" claim is factually wrong — was over-corrected in round 2; needs to say "same topology, different leaf values")
- **L07**: 5 P0 from R1 (figures fig01/02/06/09/10 wrong, K4 over-correction), 1 P0 from R4 (§5.6 worklist init lists non-adjacent arcs)

### Lecture P0s found in L09a-L12 round 1 (revisions done; need round 2 verification)

- **L09a**: 4 USE figures not embedded; missing slide 31-33 anthrax narrative; 5+ missing §2 analogies; circular §3.10 derivation
- **L09b**: 5 broken cross-ref anchors; sum-vs-max analogy missing breakdown caveat; backward variable/smoothing missing
- **L10**: §4.5 vs §5.6 numerical contradiction (best Gini threshold "85-90 vs 1/3 2/4" wrong; actual is "97, 3/3 vs 0/4")
- **L11**: t-multiplier direction wrong; p-value definition quotes slide's classical fallacy; analogies bullet 4 ("fuss") undefined; bullet 5 ("mirage") inverts meaning
- **L12**: K-means iteration table off-by-one vs slides 9-10; DBSCAN core-point definition ambiguous; agglomerative trace doesn't declare linkage

### Lab P0s from round 1 (highest priority — all 10 labs failed)

Per lab, the most damaging findings:

- **Lab1-Agents**: `range(1, steps)` off-by-one (NUM_STEPS=20 produces 19 ticks); MENTAL MODEL drifts from L02; Variants 1+2 unsolvable by KNOB edits alone
- **Lab2-Search**: Variants.md has wrong expected answers (V1 7-step is actually 5; V2 DFS expansions wrong); secret undocumented `_track_visited` KNOB; no Depth-Limited/IDS/UCS hooks despite L03 covering them; vacuum Left/Right semantics contradict L03
- **Lab4-GA**: KNOB name mismatches between variants.md and code (`POPULATION_SIZE` vs `POPULATION_SIZE_QUEENS` etc.); one-child crossover vs lecture's two-child; mutation flips "exactly one bit" vs lecture's per-bit-with-prob-m
- **Lab5-AlphaBeta**: TTT docstring falsely claims KNOB propagation from Nim module; `balanced-first` move ordering computes wrong quantity; Variant 4 has no public API; Variant 2 degenerate at default depth
- **Lab6-CSP**: MRV is a no-op without FC; LCV is a no-op on uniform domains; `_forward_check` only works for `≠` constraints; FC snapshot leak on success path; Variant 5 has no controlling KNOB
- **Lab7-BN**: `get_conditional_probability` is not exact inference by enumeration (approximation; sprinkler P(S|W) gives 0.4737 vs true 0.4298); B1 variant requires source edit
- **Lab8-HMM**: Default emissions use template values, not slide values (chapter R1 promised slide values); `MODE` KNOB has no validation (typos silently no-op)
- **MLLab1**: Random Forest test_acc 0.688 LOSES to best single tree (depth-3) at 0.703 — entire narrative wrong; `TREE_MAX_DEPTH` KNOB blurb says 0.78-0.82 but actual is 0.703; `RF_RANDOM_STATE` referenced in variants.md but doesn't exist
- **MLLab2**: T4 header forecasts grade 7 (≈7.7), actual is grade 10 (9.70); `variants.md` references `TOY_RANDOM_SEED`/`TOY_N_TRAIN`/`TOY_NOISE_STD` KNOBs that don't exist; Variant 1 demands 6 R² rows but verify cell hardcodes 3 subplots
- **MLLab3**: Scratch K-means iter 10 NOT converged (actually converges at iter 14) — narrative attributes gap to init scheme but real reason is iteration count; T4 silhouette-argmax recommends K=2 but rest of notebook is built on K=3; T3 vs T4 silhouettes on different feature sets

## What remains to complete the spec

### Immediate next steps (session 2)
1. Dispatch round-3 verifier reviewers for L02-L07 (20 agents) — see specific P0 lists above
2. Dispatch round-2 verifier reviewers for L09a-L12 (20 agents)
3. Dispatch revisers for all 10 labs (10 agents) — each reads its 4 round-1 reports
4. Dispatch round-2 reviewers for all 10 labs (40 agents) after revisions
5. Iterate revision rounds until all artifacts LOCKED (all 4 reviewers APPROVED, zero P0/P1)
6. Dispatch 3 exam agents per lab (30 agents) — verifies KNOB-only solvability of variants
7. Phase 3: Index Builder + its own review loop, PDF Renderer, Verifier
8. Phase 4: Write `study/00-DONE.md`, update memory

Estimated remaining: ~150-300 more agent invocations across multiple conversation sessions.

### How to resume

1. Read this HANDOFF.md
2. Read the spec and plan referenced at top
3. Glance at the most-recent `study/_review/<artifact>/round<N>/` directories to see latest review state
4. Pick up at "Immediate next steps" #1

The PM convention is: dispatch agents in batches, each batch in a single tool-message with multiple parallel `Agent` calls. Use `pm-qa` subagent_type for reviewers, `general-purpose` for revisers and other content work, `pm-backend` for code-heavy revisers.

## Files inventory (created this session)

```
AI/
├── docs/superpowers/
│   ├── specs/2026-05-22-ai-exam-prep-study-package-design.md
│   ├── plans/2026-05-22-ai-exam-prep-study-package.md
│   └── HANDOFF.md (this file)
├── study/
│   ├── _shared/
│   │   ├── TOOLCHAIN.md
│   │   ├── glossary.md (151 entries)
│   │   ├── cross-references.md
│   │   ├── style.css
│   │   └── html-template.html
│   ├── lectures/ (10 .md chapters, all revised at least once)
│   ├── extracted_figures/L02..L12/ (figure PNGs + figures.md catalogues)
│   ├── _review/<lecture>/round1/, /round2/, sometimes /round1/revise-summary.md
│   ├── _review/labs/<lab>/round1/ (4 reviewer reports each)
│   ├── _exam/<lab>/variants.md (10 variant banks)
│   ├── requirements.txt
│   └── render.py (skeleton — to be filled by Phase 3 Renderer agent)
├── (originals — UNTOUCHED)
└── (10 labs' _solution files alongside originals — drafted, R1 reviewed, awaiting revision)
```

## What did NOT happen

- No PDFs rendered yet (render.py is still a skeleton)
- No `study/00-master-index.md` yet
- No `study/00-DONE.md` yet
- No `study/_verification-report.md` yet
- No exam-agent dispatches yet
- No commits — all changes still in working tree

## Toolchain reminders

- Always use `py -3.12` (system default is 3.14 which doesn't have wheels for our pins)
- For WeasyPrint to work, prepend `C:\msys64\mingw64\bin` to PATH (either in-code per `study/_shared/TOOLCHAIN.md`, or `$env:PATH = 'C:\msys64\mingw64\bin;' + $env:PATH` in shell)
- Persistent env var `WEASYPRINT_DLL_DIRECTORIES` is set in user environment but WeasyPrint 62.3 ignores it (only honours PATH)

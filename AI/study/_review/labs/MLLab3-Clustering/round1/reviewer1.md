# Lab Reviewer #1 (Correctness) — MLLab3-Clustering, Round 1

**Notebook reviewed:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab3_clustering_solution.ipynb`
**Execution command:** `py -3.12 -m jupyter nbconvert --to notebook --execute --inplace=false lab3_clustering_solution.ipynb`
**Executed artefact:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab3_clustering_solution.executed.ipynb` (811 KB written, 0 errors raised in any cell).
**Lens:** ruthless correctness — every cell executes; every numeric claim verified against an independent reimplementation; every algorithmic claim cross-checked against the L12 lecture deck and the handout (`lab3_clustering_handout.ipynb`).

---

## 0. Executive verdict

**Status: Pass with concerns.** The notebook runs cleanly end-to-end. The headline numerical results (inertias, silhouettes, cluster sizes, grade spread) are all reproducible and match an independent sklearn re-run to the last decimal. K-means, the elbow method, the silhouette score, and the from-scratch Lloyd loop are implemented correctly *in algorithmic substance*.

What pushes this off "Pass" is a **subtle but real bug in the scratch K-means convergence story** (T6) and a **pedagogical mis-attribution** of the sklearn-vs-scratch inertia gap, plus a small handful of cell-ordering and labelling rough edges. None of these break code; all of them will cost the student exam points if a marker probes the explanation.

---

## 1. Cell-by-cell execution check

Ran `nbconvert --execute` with the default KNOBs (`K_T1=3`, `K_PRIMARY=3`, `FEATURE_PAIR_T1=('study_hours_per_week','prior_math_grade')`, `INIT_SCHEME='k-means++'`, `N_INIT=10`, `RANDOM_STATE=42`).

| Cell id | Status | Key output |
|---------|--------|-----------|
| `global-knobs` | OK | KNOBs banner prints |
| `cell-imports` | OK | "Setup complete." |
| `cell-warmup` | OK | 3-blob figure |
| `cell-dataset` | OK | Shape `(360, 9)`, head() displays |
| `cell-feature-look` | OK | describe() + 3 scatter panels |
| `cell-t1-intuition` | OK | Means `[-0., -0.]`, stds `[1., 1.]` |
| `cell-t1-solve` | OK | Fit silent |
| `cell-t1-verify` | OK | Sizes `{0:145, 1:120, 2:95}`, **inertia 168.9** |
| `cell-t2-solve` | OK | Fit silent |
| `cell-t2-verify` | OK | Sizes `{0:82, 1:133, 2:145}`, **inertia 1010.8**, heatmap |
| `cell-t2-reveal` | OK | Mean grades `{0:0.63, 1:9.96, 2:5.44}`, **spread 9.33** |
| `cell-t3-solve` | OK | Fit silent |
| `cell-t3-verify` | OK | Inertia/silhouette table: k=2→288.1/0.493, k=3→168.9/0.450, k=5→111.0/0.398 |
| `cell-t4-solve` | OK | Full sweep, **recommended K=2** |
| `cell-t4-plot` | OK | Elbow + silhouette panels |
| `cell-t5-solve` | OK | Predicts cluster 1 |
| `cell-t5-reveal` | OK | "Dedicated achievers", typical grade 9.96 |
| `cell-t6-prep` | OK | Initial centroids printed |
| `cell-t6-solve` | OK | Loop runs |
| `cell-t6-verify` | OK | **Scratch 170.1 vs sklearn 168.9, diff 1.2** |
| `cell-banner` | OK | Summary banner |

Zero exceptions raised. Zero warnings (sklearn 1.x is silent at `n_init=10`, scratch path doesn't warn).

---

## 2. Independent numerical verification

I re-implemented the dataset generator and ran sklearn fits in a fresh Python session with the same seeds. **Every reported number matched to the last printed digit:**

| Quantity | Solution prints | My reimpl | Match |
|----------|---------------|-----------|-------|
| T1 inertia (2-feat, k=3) | 168.9 | 168.886 | ✓ |
| T2 inertia (6-feat, k=3) | 1010.8 | 1010.750 | ✓ |
| T2 cluster sizes | {0:82, 1:133, 2:145} | identical | ✓ |
| T3 silhouette k=2 / k=3 / k=5 | 0.493 / 0.450 / 0.398 | identical | ✓ |
| T4 silhouettes k=2..10 | 0.328, 0.278, 0.277, 0.264, 0.253, 0.204, 0.222, 0.190, 0.163 | identical | ✓ |
| T4 inertias k=1..10 | 2160, 1289.5, 1010.8, 854.2, 752.4, 672.7, 644.1, 614.3, 588.9, 565.3 | identical | ✓ |
| Grade spread (max − min mean grade) | 9.33 | 9.33 | ✓ |

I also separately verified that the K=1 inertia (2160.0) is exactly `N × p = 360 × 6` (because `StandardScaler` uses `ddof=0`, so per-feature variance is exactly 1.0). That sanity-check passes — the elbow's left anchor is mathematically sound.

---

## 3. P0 — none

No correctness defects severe enough to block shipping.

---

## 4. P1 — important issues

### P1-A. Scratch K-means is **not converged at iter 10**, and the solution attributes the residual gap to the wrong cause

**Where:** `cell-t6-solve` (`for it in range(SCRATCH_ITERS)` with `SCRATCH_ITERS=10`) and the explanatory markdown in `section-t6-explain`.

**What I found:**

Running the same scratch loop with `SCRATCH_ITERS=50` and an early-stop on label-stability, convergence happens at **iteration 14**, not iteration 10. The full inertia trajectory is:

```
iter  9: 170.1033   <-- solution stops here, reports this as 'final'
iter 10: 169.6366
iter 11: 169.2746
iter 12: 168.9327
iter 13: 168.8965
iter 14: 168.8859   <-- true convergence; matches sklearn to 4 decimals
```

So sklearn's reported 168.886 is **exactly** what the scratch loop reaches at convergence on this initialisation. The seed-0 Forgy init on this 2-feature data lands in the same global optimum as k-means++. There is no init-quality penalty.

The markdown in `section-t6-explain` claims:
> *"the small gap is because sklearn uses `init='k-means++'` with `N_INIT` restarts while our scratch version does one run from Forgy random init."*

This is **false on this dataset with this seed**. The gap of 1.2 is entirely the "I stopped before convergence" gap. If a marker asks "why is your inertia 1.2 higher than sklearn's?" the correct answer is "I only ran 10 iterations and the algorithm needed 14 here" — not the init-scheme story the solution rehearses.

**Severity:** P1. The algorithm runs and produces a plausible-looking convergence curve, but (i) the headline "matches sklearn within a couple of points" understates how close the scratch implementation actually is, and (ii) the explanation will mislead a student who reads the markdown as exam preparation.

**Compounding subtlety:** the inertia is recorded **before** the centroid update inside each iteration. That means `inertia_history[-1]` reports the inertia of the *previous* iteration's centroids evaluated against the new assignment. After convergence this is identical to the post-update inertia, but during the transient (where this code stops!) it's one update stale. Recompute the true final inertia after the loop, or move the `inertia_history.append(...)` line to after the update step.

**Suggested fix (for the engineer, not for QA to apply):**
1. Bump `SCRATCH_ITERS` to e.g. 20 (still cheap), or add an early-stop on label stability.
2. Either move the inertia bookkeeping below the update, or after the loop add a final post-update inertia computation and append it to the history.
3. Rewrite the markdown explanation to say "*the gap on this seed shrinks to zero once we run to convergence; init-scheme matters more on adversarial data or with `N_INIT=1`*."

### P1-B. T4 silhouette-argmax says K=2 but the entire rest of the notebook is built around K=3

**Where:** `cell-t4-solve` prints "Recommended K by silhouette-argmax: K = 2". `cell-t4-plot` puts the red dashed line at K=2. Yet T2, T5, T6, the cluster heatmap, the grade reveal, and the "Dedicated achievers / Moderate middle / Light effort" naming all rely on K=3.

**Why this matters:** The lab's pedagogical climax is "K-Means rediscovered the three baked archetypes." A student reading the solution top-to-bottom sees:
- T2: K=3 gives a 9.33-grade-point spread → "K-means works!"
- T4: silhouette says K=2 → "the algorithm itself disagrees."
- No reconciliation paragraph.

The handout's own cell-28 markdown anticipates this ("The elbow isn't crisp on a real dataset … silhouette peaks at one of those two values. Both curves are saying: two or three natural groups. We baked in three archetypes, so k=3 is defensible, but k=2 would also be a reasonable simplification. **K-Means *suggests*, you *choose*.**"). The solution **drops this nuance** — there is no equivalent paragraph in `section-t4-explain` or after `cell-t4-plot`.

**Severity:** P1. The numbers are right; the narrative is missing a critical "and here's how to choose between them" sentence. As-is, an exam marker reading the solution alone might conclude the recommended K is 2 and mark a K=3 student answer wrong.

**Suggested fix:** Add a markdown cell after `cell-t4-plot` that (a) acknowledges silhouette and elbow disagree, (b) reminds the student the silhouette score numerically prefers fewer, well-separated clusters and so will often pick K=2 even when the underlying truth is K=3, (c) points out the grade-spread evidence from T2 is the *external* validity check that confirms K=3 is meaningful.

### P1-C. T4 silhouette computed on the 6-feature data, T3 silhouette on the 2-feature data — comparison printed in the same column without a guard

**Where:** `cell-t3-verify` prints silhouettes computed on `X2_scaled` (range 0.398–0.493). `cell-t4-solve` prints silhouettes computed on `X6_scaled` (range 0.163–0.328). A student skimming the two outputs will see "k=3 silhouette = 0.450 in T3, but 0.278 in T4 — which is right?" and have no anchor for the discrepancy.

**Severity:** P1 (clarity / risk of student confusion in revision). The numbers are individually correct, but the inconsistency is not flagged in the surrounding markdown. The header docstring acknowledges T4 uses 6 features ("inertia + silhouette over a wider K range" with no axis spec), and `axes[0].set_title('Elbow curve — inertia vs k (on 6-feature data)')` does say so on the plot itself. But the printed table headers in both T3 and T4 just say "silhouette" with no feature-set qualifier.

**Suggested fix:** Print "(2-feature)" / "(6-feature)" in the table headers, or add a one-line markdown bridge between T3 and T4 that explicitly notes the change in input dimension.

### P1-D. T4 includes K=1 in the elbow plot but the `n_init` parameter for that fit is `1` (overridden to silence sklearn), while the others use `N_INIT=10`

**Where:** `cell-t4-solve` lines:
```
km1 = KMeans(n_clusters=1, n_init=1, random_state=RANDOM_STATE).fit(X6_scaled)
```
vs the k≥2 branch which uses `n_init=N_INIT` (default 10).

**Why this matters:** Strictly, the K=1 fit can use `n_init=1` because there's no centroid to initialise (the one centroid is always the global mean — there is no local-optimum trap). So functionally this is fine. But the explanation in the docstring of the cell doesn't say so, and a careful reader will wonder whether the K=1 inertia is comparable to the K≥2 inertias on the elbow plot. (It is, exactly. But the cell doesn't tell you that.)

**Severity:** P1 for documentation; the math is fine.

**Suggested fix:** Add an inline comment to the K=1 branch: `# n_init=1 is fine here: the K=1 minimum is unique (it's the global mean).`

### P1-E. `np.argmin` in `snap_to_danish` returns the *first* match on ties, but `DANISH_SCALE` has a tie at score = -1.5 (midway between -3 and 0), at 1.0 (midway between 0 and 2), etc.

**Where:** `cell-dataset`, function `snap_to_danish`.

**Why this matters:** Real scores from the generator are rounded to two decimals and clipped to `[-3, 12]`. The probability of a score landing exactly on a tie midpoint is essentially zero, **but** the function is also used by the handout, so consistency matters for any exam-variant where N is small and rounding produces ties. The default behaviour (round to lower grade on tie) is asymmetric — exam-style "round half up" / "Danish scale" tradition would round to the higher grade.

**Severity:** P1 if you care about exam-style grade-snapping fidelity. P2 if you treat it as "the generator's convention is what it is."

**Suggested fix:** Out of scope for this lab (would require re-baking the dataset). Worth noting in the lecture/handout glossary.

---

## 5. P2 — polish, suggestions

### P2-A. Cell-banner has UTF-8 encoding artefacts

`cell-banner` prints `LAB ML 3 — CLUSTERING — SOLUTION COMPLETE`. In the executed notebook's text output, the em-dash renders as `�` (replacement character) in `iopub` text. This is a Windows console / Jupyter `text/plain` encoding issue, not a Python bug — but the surrogate appears in the executed notebook JSON. Consider replacing em-dashes with hyphens in print-only strings.

### P2-B. `cell-t6-prep` initial-centroid `print` shows scaled coordinates with no axis labels

```
[[ 0.575  0.215]
 [-0.6   -2.415]
 [-1.037 -1.1  ]]
```

A student reading this won't know what feature each column is. Add the column names: `print('Initial centroids (scaled, columns =', two_feats, '):')`.

### P2-C. `section-t2-explain` says **"the cluster means differ by more than half the Danish scale"** but the actual spread is 9.33 grade points on a scale running from −3 to 12 (range 15). That's 62% of the scale, not just "more than half" — the prose understates the result.

P2 wording only.

### P2-D. `cell-t1-intuition` uses `StandardScaler().fit_transform(X_demo_raw)` then reports `stds = [1, 1]`. With `ddof=1` numpy std this would actually print `[1.001..., 1.001...]`. The print uses `.std(axis=0)` which is `ddof=0` (numpy default), so it prints exactly `[1, 1]`. Fine, but worth a one-line comment that StandardScaler and numpy `std` agree on `ddof=0`.

### P2-E. `section-t6-explain` says **"Implements the same algorithm sklearn uses internally"** — strictly, sklearn uses Elkan's accelerated K-means (triangle-inequality pruning) by default since v1.0, not naive Lloyd. The result is identical to within floating-point on this data, but the claim "the same algorithm" is technically wrong. Better wording: *"implements Lloyd's K-means, the textbook version of what sklearn does under the hood."*

### P2-F. `cell-t4-solve` builds `inertia_curve` and `silhouette_curve` as DataFrames with k as index; both are then `display()`-ed. The integer-keyed K=1 row appears in both. A keen-eyed student will notice `silhouette` column at K=1 is `NaN` and may worry. The cell already says "(NaN at K=1)" in the print — good — but the elbow plot also draws a line through K=1 down to K=2 which optically suggests K=1 is "on the curve." Up to design taste; mention only.

### P2-G. Cell ordering: `cell-t5-reveal` re-computes `summary` from `df`/`labels_t2`, but the same `summary` was already computed in `cell-t2-reveal`. Re-running is harmless (idempotent), but DRY violation. Either factor into a helper or trust the prior cell. P2.

### P2-H. `MY_PROFILE` defaults to a profile that lands in the "Dedicated achievers" cluster every time. The narrative banner triumphantly announces "you look most like a Dedicated achiever" with no caveat. For a student running the notebook unchanged, this is a *false* result about themselves. Suggest a more neutral default, or a more neutral printed banner ("the placeholder profile lands in the …").

---

## 6. Standing-check summary

| Standing check | Result |
|---|---|
| 1. Scope compliance (handout T1–T6) | Pass. Solution adds an explicit T4 cell pair (elbow + silhouette) which the handout's narrative promises but never implements — this is the right scope expansion. |
| 2. Bugs (null/oob/race) | One real subtlety: scratch K-means records inertia pre-update and stops one iteration before convergence (see P1-A). No nulls, no off-by-ones in array indexing, no race risks (single-threaded). |
| 3. Security | N/A — local educational notebook, no inputs from network, no secrets, no SQL. |
| 4. Performance | Fine. The slow path is the K_GRID_T4 sweep (10 KMeans fits × `N_INIT=10` restarts on N=360, p=6). Sub-second. The vectorised distance matrix in scratch K-means is `O(N × K × p)` per iter — fine. |
| 5. Accessibility | N/A for a Jupyter notebook (no DOM, no ARIA). Plot colour palette is colour-blind friendly enough (teal/orange/purple/blue) — no red-green confusion. |
| 6. Convention adherence | Follows the `# KNOB:` block style established by the lab series. Variable naming matches handout (`kmeans2`, `kmeans6`, `labels_t1`, `labels_t2`, `centers_raw_t1`, etc.) — handout-required variables all present, so a student grading against the handout's "Required variables after your code runs" lists will be satisfied. |
| 7. `DOCUMENT.md` presence | N/A — solution lives at repo root next to the handout, same as MLLab1 and MLLab2. No directory-level docs convention for the lab notebooks. |
| 8. Tests | No formal pytest. The notebook's own sanity-check cells (`cell-t1-verify`, `cell-t2-verify`, `cell-t3-verify`, `cell-t6-verify`) function as inline tests; all pass. |
| 9. Quality (TODO, placeholders) | No `TODO`, no `# ...rest`, no `pass`-as-placeholder. Production-ready in the lab-solution sense. Handout-side `raise NotImplementedError` markers are correctly *not* present in the solution. |

---

## 7. Conventions cross-check vs other ML labs

I quickly compared the solution's structure against the in-flight `MLLab1-Classification` review folder layout. The naming and KNOB-block conventions are consistent with the prior labs.

---

## 8. Lecture/handout alignment

Cross-checked against `study/lectures/L12-Clustering.md`:
- §3 (Core Concepts: centroid, intra/inter-cluster distance, inertia) — solution uses correct terminology.
- §4 (Lloyd's iteration: assign + update) — scratch K-means in T6 matches.
- §6 (Pitfalls: random init traps, unscaled features, picking K) — addressed via `INIT_SCHEME` KNOB, `StandardScaler` reasoning, and the T4 elbow/silhouette pair.
- Lecture line 532 explicitly notes the deck **omits** K-means++, elbow, silhouette — the solution's header acknowledges this correctly.

The solution's claim that the elbow method and silhouette score are "not in L12, introduced by this lab" matches the lecture's own glossary note. Good.

---

## Report to PM

**Assignment recap:** MLLab3-Clustering — Lab Reviewer #1 (Correctness), Round 1. Reviewed against the explicit handout task list (T1, T2, T3, T5, T6) plus the implicit T4 (elbow + silhouette).

**Status:** Pass with concerns.

**P0 findings:** None.

**P1 findings:**

1. **`cell-t6-solve` + `section-t6-explain` — scratch K-means stops one iteration before convergence and the markdown misattributes the residual gap to init-scheme differences.** Scratch reports inertia 170.1; true converged inertia on this seed is 168.886, identical to sklearn. The gap is "I stopped early," not "init scheme matters." Compounded by recording inertia *before* the per-iteration centroid update. *Fix:* either run more iterations (bump `SCRATCH_ITERS` to 20 or add early-stop on label stability) **and** rewrite the explanation, or move the `inertia_history.append(...)` line to after the centroid update.

2. **`cell-t4-solve` recommends K=2 by silhouette-argmax but the rest of the notebook teaches K=3 with no reconciling paragraph.** *Fix:* add a markdown cell after `cell-t4-plot` that explicitly addresses the silhouette-vs-elbow disagreement and points to the T2 grade-spread as the external validity argument for K=3 (the handout's cell-28 already has the right wording — port it across).

3. **T3 vs T4 silhouettes are computed on different feature sets (2 vs 6) and the table headers don't say so.** *Fix:* annotate the table column / add a one-line bridge in markdown.

4. **K=1 sklearn fit in `cell-t4-solve` uses `n_init=1` while other Ks use `N_INIT=10`, without comment.** Mathematically correct (K=1 has a unique optimum); cosmetically confusing. *Fix:* one-line inline comment.

5. **`snap_to_danish` ties resolve toward the lower grade.** Generator-side convention; flagging for awareness, no fix needed unless variant labs run with tiny N.

**P2 findings:**

A. Cell-banner em-dash encoded as `�` in executed notebook text output.
B. `cell-t6-prep` prints initial centroids without column names.
C. "more than half the Danish scale" understates the 9.33/15 ≈ 62% spread.
D. `cell-t1-intuition` could add a one-line ddof note.
E. "the same algorithm sklearn uses" → sklearn uses Elkan, not naive Lloyd; wording.
F. Elbow plot draws through K=1; intentional but could mislead.
G. `cell-t5-reveal` recomputes `summary` already built in `cell-t2-reveal` (DRY).
H. Default `MY_PROFILE` always lands in "Dedicated achievers"; banner triumphantly addresses the student personally, which is misleading for an unmodified placeholder run.

**QA Checklist (§7) status:**
- Bug-free against scope above: Concerns (P1-A scratch convergence).
- Security items: N/A.
- Performance acceptable: Pass.
- Accessibility: N/A.
- DOCUMENT.md present: N/A for lab notebooks.
- Conventions from `PM/conventions.md`: Pass (handout-required variable names all present).

**Acceptance criteria (§1) status:**
- T1 (K=3 on 2 features, save labels + raw-unit centroids): Met. Inertia 168.9.
- T2 (K=3 on 6 features, describe by centroid, reveal grades): Met. Spread 9.33.
- T3 (refit at K=2/3/5, dict keyed by k, inertia/silhouette): Met. Sizes and metrics match expectations.
- T4 (elbow + silhouette over K=1..10, recommend K with evidence): Met *numerically*; **narrative weak** (P1-B).
- T5 (predict cluster for `MY_PROFILE`): Met.
- T6 (scratch K-means within a few inertia points of sklearn): **Met as printed** (diff 1.2), but the convergence story is wrong (P1-A).

**DOCUMENT.md audit:** N/A — lab notebooks live at repo root with no `DOCUMENT.md` convention.

**Out-of-scope observations:**
- The same `snap_to_danish` and dataset-generator code is duplicated across Lab 2 and Lab 3. A shared `study/_shared/student_data.py` would dry this up, but that's a series-level refactor, not a Lab 3 issue.
- The handout cell-28 has the "K-Means *suggests*, you *choose*" reconciliation prose that the solution should have re-used verbatim. Cheap fix the engineer should apply.

**Concerns / risks:**
- The scratch K-means explanation (P1-A) is the biggest exam-risk item. A student who memorises the solution's explanation and is asked "why did your inertia not exactly match sklearn?" will give a wrong answer. The actual reason is iteration count, not init scheme — Forgy init with this seed lands at the global optimum on this data.
- The silhouette-argmax = 2 result (P1-B) sets up an answer-shape inconsistency the solution doesn't resolve. A student answering "what K should we use?" by quoting the printed recommendation gets a different answer than the lab-narrative implies. Marker exposure.

**What PM should do next:** Dispatch the implementing engineer (whoever wrote the solution) to address P1-A and P1-B at minimum — both are markdown-and-one-loop-bound fixes (<15 minutes of work). Re-run QA after those land; the other P1s are nice-to-haves. Do **not** ship to App Tester until P1-A and P1-B are addressed: App Tester will read the notebook's own narrative as ground truth and produce a misleading run report.

**DOCUMENT.md updated:** N/A for QA.

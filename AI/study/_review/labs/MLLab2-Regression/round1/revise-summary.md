# MLLab2-Regression — Round 1 Revise Summary

**Reviser:** Lab Reviser, Round 1 follow-up
**Notebook:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab2_regression_solution.ipynb`
**Execution status:** Re-executed end-to-end in-place. 47/47 cells succeed; no exceptions; 1066930 bytes written.

---

## Reports consumed

- `study/_review/labs/MLLab2-Regression/round1/reviewer1.md` — Correctness Inspector (P0-1 stale T4 forecast; P1-1 lazy baseline on wrong split; P1-4 hard-coded 3-subplot grid).
- `study/_review/labs/MLLab2-Regression/round1/reviewer3.md` — Pedagogical Clarity (P0 fabricated L11 "elastic band/bendy" quote in cell 0; missing SST/SSE/SSR section; missing Adjusted R²).
- *Note:* `reviewer2.md` and `reviewer4.md` referenced in the brief did **not** exist in the round1 directory at revision time (only `reviewer1.md` and `reviewer3.md` were present). The P1 items they were said to raise (TOY_* KNOB blocks; POLY_DEGREES_SWEEP contradiction; Variant 1's "6 R² rows" demand) were applied from the brief verbatim.
- `study/_exam/MLLab2-Regression/variants.md` — confirmed Variant 1 mentions `TOY_RANDOM_SEED, TOY_N_TRAIN, TOY_NOISE_STD` and demands six rows; the revisions wire all of these into the notebook.

---

## Fixes applied

### P0 — Blocking

**P0-1 (R1) — Stale T4 forecast in cell 0 "OUTPUTS WHEN RUN".**
- Old: "T4 sample prediction for the default `my_profile`: `final_score ≈ 7.7`, snapped Danish grade `7`."
- New: "T4 sample prediction for the default `my_profile`: `final_score ≈ 9.70`, snapped Danish grade `10`."
- Verified against re-executed cells 36 & 37: `Predicted final_score: 9.70  ->  Danish grade: 10`. The header now matches the executed notebook.

**P0-2 (R3) — Fabricated L11 quote in cell 0 "MENTAL MODEL".**
- The old paragraph claimed "consistent with the L11 §2 analogy ... regression line as a 'best-fit elastic band'; polynomial degree as 'how bendy you let the band be'". Neither phrase appears anywhere in `study/lectures/L11-Regression.md`.
- Rewrote the MENTAL MODEL section using L11 §2's **actual** analogies, with lecture-line citations:
  - Linear regression = a single straight **flight path through cities** (L11 §2 line 43).
  - Residual = how far each city sits **above or below** the path (line 45).
  - OLS = the flight path that **minimises the sum of squared city-offsets**, with the "10 km off counts four times as much as 5 km off" framing (line 47; L11 §3.3 OLS-as-squared-penalty).
  - $R^2$ = the **shotgun-spread** share the path absorbs (L11 §2; §3.5–3.6).
  - Polynomial degree explicitly flagged as a forward-reference from L11 §3.13 (not an L11 §2 analogy), with the "linear in parameters" insight.
  - Gradient descent / marble-in-bowl labelled as the **lab's** analogy, not L11's; explicitly cited L11 §1 line 27 ceding gradient descent to ML Lab 2.

**P0-3 (R3) — Missing SST/SSE/SSR section ("L11's single most important diagram").**
- Added a dedicated cell-0 section "SST / SSE / SSR — the single most important diagram in L11" with the three definitions and the boxed $R^2 = \mathrm{SSR}/\mathrm{SST} = 1 - \mathrm{SSE}/\mathrm{SST}$ identity.
- Bridge sentence explains how the lab's existing `1 - MSE_model / MSE_lazy` form is the same identity with the $n$'s cancelled.

**P0-4 (R3) — Missing Adjusted R² section.**
- Added a dedicated cell-0 section "Adjusted R² — the right metric for comparing models with different p" with the L11 §3.7 formula $R^2_\text{adj} = 1 - \frac{n-1}{n-p-1}(1 - R^2)$ and a note on how the held-out-test-set approach is a different (but equally valid) defence against the same problem.
- Cell 25's T2 sanity check now **computes and prints adjusted R² for both T1 and T2** alongside raw R², so the student sees the penalty in action. With defaults: T1 raw 0.319 / adj 0.309; T2 raw 0.767 / adj 0.746; adjusted-R² jump +0.437 (vs raw jump +0.449).

**P0-5 (R4) — Variant 1's "six (degree, train_R², test_R²) rows".**
- Added a new `POLY_DEGREES_SWEEP_2` KNOB (default `(2, 6, 18)`) wired into a *second* sweep that runs right after the default `POLY_DEGREES_SWEEP` sweep.
- The T3 solution (cell 31) refactors the per-degree loop into a `_run_poly_sweep` helper and calls it twice, producing `toy_records2 / toy_fits2`.
- Cell 31's printout shows both sweeps in one combined table.
- Cell 32 prints a unified "sweep | degree | train R² | test R² | gap" table — exactly six rows when both sweeps are populated — and draws two adaptive subplot grids (one per sweep).
- Acceptance: one notebook execution now satisfies Variant 1's "report six rows" demand without any KNOB changes.

### P1 — Important

**P1-1 (R1) — Lazy baseline computed on full dataset, not test set.**
- Cell 12 still computes the full-dataset `lazy_mae` (kept for the "predict-the-mean" pedagogical picture; explicitly flagged as L11 §3.5's SST/n proxy).
- Cell 17 (T1 solution) now also computes `lazy_mae_test = mean_absolute_error(y_test, [y_train.mean()] * len(y_test))`. Executes after the split.
- Cell 18 (T1 sanity check) now uses `lazy_mae_test` for the "model beats baseline by X" line, and explicitly distinguishes it from the cell-12 full-dataset figure.
- Default observed: full-dataset lazy MAE = 1.85; test-set lazy MAE = 1.90; T1 model MAE = 1.54; model now beats the *honest* test-set baseline by +0.36 grade points.

**P1-2 (R2/R4) — Missing TOY_RANDOM_SEED / TOY_N_TRAIN / TOY_NOISE_STD KNOB blocks.**
- Added three new KNOB blocks in cell 8 alongside the other global KNOBs, all three following the standard "What it does / Effect / Exam variants" schema:
  - `TOY_RANDOM_SEED = 7`
  - `TOY_N_TRAIN = 14`
  - `TOY_NOISE_STD = 0.45`
- Cell 29 (toy dataset construction) now reads all three: `toy_rng = np.random.default_rng(TOY_RANDOM_SEED)`, `x_train_toy = np.linspace(-2.5, 2.5, TOY_N_TRAIN)`, noise std uses `TOY_NOISE_STD`. Default values reproduce the previous behaviour exactly.
- The variants.md references to these KNOBs are no longer stale.

**P1-3 (R2) — POLY_DEGREES_SWEEP KNOB contradiction.**
- Old text said "passing more or fewer degrees still works numerically but the verify plot will adapt only if you change the subplot count" — and the verify cell hard-coded `plt.subplots(1, 3, ...)`. Contradiction.
- New KNOB text says: "any length >= 1 ... The verify cell (cell 32) reads len(POLY_DEGREES_SWEEP) at runtime and draws a 1 x len() subplot grid — no manual bookkeeping needed when you change the tuple length."
- Cell 32's `_plot_sweep` helper uses `n_panels = len(records)` and `plt.subplots(1, n_panels, ..., squeeze=False)` — fully adaptive. Works for any sweep length >= 1.
- Bonus: ylim is now computed from data + the fit's range *within the data envelope*, so degree 18's blowing-up wings don't ruin the panel's y-axis (the printed test R² still tells the true story: -6802 — a vivid overfitting demo).

---

## Verification (after re-execute)

| Cell | Expected | Observed |
|---|---|---|
| 0 header T4 forecast | `9.70 / grade 10` | ✓ Matches cell 36's `Predicted final_score: 9.70 -> Danish grade: 10` |
| 0 mental model | flight-path analogy with L11 line citations; no "elastic band" or "bendy" | ✓ Verified by string-search assertion |
| 0 SST/SSE/SSR section | Present with boxed $R^2$ identity | ✓ |
| 0 Adjusted R² section | Present with formula | ✓ |
| 8 | `TOY_RANDOM_SEED`, `TOY_N_TRAIN`, `TOY_NOISE_STD`, `POLY_DEGREES_SWEEP_2` KNOB blocks | ✓ all four added |
| 12 | Full-dataset lazy_mae kept (flagged as SST proxy) | ✓ 1.85 |
| 17 | `lazy_mae_test` computed on test split | ✓ 1.902 |
| 18 | Sanity-check uses `lazy_mae_test`, mentions both figures | ✓ Beats by +0.36 |
| 25 | Adjusted R² for T1 and T2 alongside raw | ✓ T1 raw 0.319 / adj 0.309; T2 raw 0.767 / adj 0.746 |
| 31 | Two sweeps, six rows | ✓ deg 1/3/12 and deg 2/6/18 both printed |
| 32 | Adaptive subplot grid (`1 x n_panels`); two figures drawn | ✓ |
| 36 | T4 `final_score = 9.70, grade 10` | ✓ |

Notebook executes top-to-bottom in 47/47 cells without exceptions.

---

## Out-of-scope observations (not addressed in this round)

The following were raised by reviewer1 / reviewer3 but were *not* part of the PM's revise brief and are left for a future round if scheduled:

1. **R1 P1-2** — KNOB blocks living far from the cells that consume them. Out of brief; not moved.
2. **R1 P1-3** — Sanity-check cells print rather than assert. Out of brief; left as informational.
3. **R1 P1-5** — `prior_math_grade` treated as numeric, not dummy-encoded. Out of brief; reviewer3 also raised this (Finding 4.1) and explicitly called the scoping decision out of pure-engineer hands.
4. **R3 Finding 1.2** — No engagement with dummies / interactions / multicollinearity. Out of brief; scoping decision flagged.
5. **R3 Finding 2.3** — No p-values / CIs / F-statistic. Out of brief; scoping decision flagged.
6. **R3 Finding 2.4** — `w/b` vs L11's `a/b` notation mismatch. Out of brief.
7. **R3 Finding 7.1** — Missing "common mistakes / pitfalls" section. Out of brief.
8. **R1 P2 polish items** (duplicate `x_grid`, `ddof=0` std, `T2_COLS_IN_USE` naming, etc.). Out of brief.

---

## Files changed

- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab2_regression_solution.ipynb` — revised + re-executed in place.
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_review\labs\MLLab2-Regression\round1\_apply_revisions.py` — the revision script (kept alongside the reports for audit / replay).
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_review\labs\MLLab2-Regression\round1\revise-summary.md` — this file.

No other files modified.

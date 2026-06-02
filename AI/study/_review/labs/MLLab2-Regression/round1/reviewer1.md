# MLLab2-Regression — Round 1 — Reviewer #1 (Correctness)

**Reviewer:** Lab Reviewer #1 — Correctness Inspector
**Notebook:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab2_regression_solution.ipynb`
**Execution command:** `py -3.12 -m jupyter nbconvert --to notebook --execute --output lab2_regression_solution_executed.ipynb lab2_regression_solution.ipynb`
**Result:** Notebook executed end-to-end without exceptions; 47 cells in, 47 cells out, `938817 bytes` written.
**Mandate:** Be harsh. Verify linear, multiple, polynomial fits + gradient descent.

---

## Executive verdict

**Status:** PASS WITH CONCERNS.

The five tasks (T1 simple linear, T2 multiple linear, T3 polynomial sweep with overfitting, T4 personal-row prediction, T5 hand-rolled gradient descent) all compute correct, sanity-check-window-compliant numbers. There are no functional bugs in the math. However, the solution is shipped with one **stale documented number** that the cell-0 header advertises as a guarantee, several **methodological asymmetries** that a strict examiner would flag, and a handful of **silent-failure modes** that would let a wrong variant slip through unnoticed. None of these would prevent the variant-gate from reporting `SOLVED`, but the bar for "Correctness reviewer" is higher than "doesn't crash."

---

## P0 — Blocking correctness findings

### P0-1. Cell 0 header advertises T4 numbers that disagree with the executed notebook

- **Location:** `lab2_regression_solution.ipynb`, cell 0 (markdown), section "OUTPUTS WHEN RUN", lines reading:
  > T4 sample prediction for the default `my_profile`: `final_score ≈ 7.7`, snapped Danish grade `7`.
- **Observed at execution:** cell 36 prints `Predicted final_score: 9.70   ->  Danish grade: 10`, and cell 37 reaffirms `Predicted Danish grade: 10`.
- **Magnitude of error:** ≈2 grade points of `final_score` (7.7 vs 9.70) — large enough to **snap to a different Danish grade** (7 vs 10). This is not a tolerance issue; it is a documented sample-output that is simply wrong.
- **Root cause (likely):** the default `my_profile` was tuned upward (study_hours_per_week=12.0, attendance_rate_pct=90.0, prior_math_grade=10, exercises_completed=9) at some point after the header was written, and the header was not refreshed. The KNOB block over `my_profile` lists those same values, so the implementation is internally consistent; only the cell-0 "OUTPUTS WHEN RUN" prose is stale.
- **Impact on graders/students:** any examiner who reads cell 0 to learn "what should the default produce" will mark the solution as broken on first run. For an exam-bank document this is a P0.
- **Suggested fix:** edit cell 0 to say `final_score ≈ 9.70`, snapped Danish grade `10`. While there, double-check the other forecast numbers — T1, T2, T3, T5 forecasts match the executed output exactly.

---

## P1 — Important issues

### P1-1. Lazy-baseline MAE and T1 test-MAE are not on the same data

- **Location:** cell 12 (lazy baseline) computes `lazy_mae = mean_absolute_error(df['final_score'], [lazy_prediction] * len(df))` on the **full 360-row dataset**. Cell 17 / 18 compares this directly to `mae_t1`, which is computed on the **72-row test split only**.
- **Symptom:** cell 18 prints `Lazy baseline MAE was 1.85. Your model beats the baseline by 0.31 grade points.` The 0.31 improvement number is meaningful only if both numbers are on comparable populations. The correct baseline for a held-out evaluation is `mean_absolute_error(y_test, [y_train.mean()] * len(y_test))` — i.e. the mean of the **training** target predicted for every **test** student.
- **Why this matters:** a stricter examiner running variant 5 (`TEST_SPLIT_RATIO=0.5`) will see the lazy baseline stay glued at 1.85 (it never moves with the split) while `mae_t1` drifts; the printed "beats baseline by X" delta becomes increasingly fictional. For a correctness review this is a known classification/regression pitfall the lab itself teaches about (cell 11: "if our real model can't beat this, we haven't learned anything").
- **Suggested fix:** in cell 12 also stash `lazy_mae_test = mean_absolute_error(y_test, [y_train.mean()] * len(y_test))` (after the split is defined) or move the lazy calculation to live next to the T1/T2 splits. Update cell 18's `improvement = lazy_mae - mae_t1` line to use the test-set lazy.

### P1-2. KNOB declarations live at the end of the dataset cell, far from the cells that consume them

- **Location:** cell 8. After `df = make_student_grade_data()` returns, the cell continues with four `# KNOB:` blocks defining `TEST_SPLIT_RATIO`, `SPLIT_RANDOM_STATE`, `POLY_DEGREES_SWEEP`, and `T2_FEATURE_SUBSET`. T1 lives in cell 17, T2 in cell 24, T3 in cell 31.
- **Why this matters:** the variant gate explicitly allows examiners to read only the `# KNOB:` comment blocks. A KNOB that governs T3 sitting inside the dataset cell forces the examiner to scroll past 60+ lines of data-generation code to reach the comment block. For an exam-prep notebook with variant-bank intent this is fragile organisation.
- **Suggested fix:** move `POLY_DEGREES_SWEEP` into cell 31 (T3), `T2_FEATURE_SUBSET` into cell 24 (T2), and keep `TEST_SPLIT_RATIO` / `SPLIT_RANDOM_STATE` at the top of cell 17 (T1) since they're shared T1↔T2. (Cell 17 already declares `T1_FEATURE` correctly, so the precedent is set.)

### P1-3. Sanity-check cells never assert — only print

- **Location:** cells 18, 25, 32, 43. Each one prints "MAE = X (expected ~Y, anything in A–B is fine)" but never raises if the value falls outside `[A, B]`.
- **Why this matters:** the variant-gate spec (cell 0 header: "every cell must succeed without raising") relies on `nbconvert --execute` exit status. If a variant change accidentally pushes `r2_t2` to 0.40 (massively broken), every cell still runs without raising and the gate reports `SOLVED`. A correctness reviewer must call this out: the printed tolerances are advisory, not enforced.
- **Suggested fix:** add `assert 0.25 <= r2_t1 <= 0.40, f"T1 R² out of band: {r2_t1:.3f}"` (and analogous lines for MAE/MSE and for T2/T3/T5) to the sanity-check cells. The default values will still pass; only an actually broken variant trips the assertion.

### P1-4. Polynomial T3 sanity-check plot silently truncates if `POLY_DEGREES_SWEEP` is not length-3

- **Location:** cell 32 creates `fig, axes = plt.subplots(1, 3, ...)` and then `for ax, (d, tr, te) in zip(axes, toy_records)`.
- **Why this matters:** `POLY_DEGREES_SWEEP`'s KNOB block says "passing more or fewer degrees still works numerically but the verify plot will adapt only if you change the subplot count." That note is honest, but it means a variant like `(1, 2, 3, 6, 12)` would silently plot only the first three. The numerical `toy_records` would be complete; the plot would be misleading.
- **Suggested fix:** make the subplot grid dynamic: `n = len(POLY_DEGREES_SWEEP); fig, axes = plt.subplots(1, n, figsize=(5*n, 4.4), sharey=True)`. Cheap fix; eliminates a silent failure mode for variant 1.

### P1-5. `prior_math_grade` is modelled as a continuous numeric despite being an ordinal scale with non-equal spacing

- **Location:** cell 8 (dataset construction) and cells 17/24 (T1/T2 fits). The Danish scale `{-3, 0, 2, 4, 7, 10, 12}` is ordinal with steps of `{3, 2, 2, 3, 3, 2}` — non-uniform. The model treats `prior_math_grade` as if a unit change has constant effect, but the dataset's hidden generative formula `0.35 * prior_math` does the same — so the model and the data agree.
- **Why this matters for correctness:** the agreement is by construction, not by design. A variant that asks "is treating an ordinal feature as numeric appropriate?" would expect the solution to acknowledge this. L11 explicitly covers dummy variables, but the solution never mentions the choice. For a correctness reviewer this is a pedagogical gap, not a bug.
- **Suggested fix:** a one-sentence note in the cell-21 (T2 concept) or cell-27 (post-T2 commentary) markdown saying "we're treating `prior_math_grade` as numeric for simplicity; lecture L11 §3 shows the dummy-variable encoding that would be more rigorous for an ordinal scale with unequal steps."

### P1-6. Variant 3 acceptance criteria in `variants.md` are not independently verified by this solution

- **Location:** `study/_exam/MLLab2-Regression/variants.md`, Variant 3 acceptance bullet ("a predicted `final_score` in roughly the `0 to +2` range … a snapped Danish grade of `02` … `study_hours_per_week` as the dominant negative contributor (~-1.7 grade points)").
- **Status:** the solution notebook does **not** include a smoke test of the Variant 3 my_profile values to confirm those acceptance numbers. Reviewer-1 did not re-run with Variant 3 applied (out of scope for round-1 correctness pass) so cannot affirm the numbers in `variants.md` are still accurate against today's `model_t2`. If model_t2's coefficients have drifted (e.g. a re-seed of the dataset), the Variant 3 acceptance text is at risk of going stale the same way the cell-0 T4 forecast already has.
- **Suggested fix:** the exam-bank maintainer should add a small verification script (separate from the lab) that loads the notebook, applies each variant's KNOB changes, and prints the resulting numbers, so `variants.md` cannot silently drift.

---

## P2 — Polish / suggestions

### P2-1. `x_grid` is defined twice

- Cell 29 defines `x_grid = np.linspace(-2.55, 2.55, 300)`, cell 32 redefines `x_grid = np.linspace(-2.6, 2.6, 300)`. Different ranges (-2.55 vs -2.6) but visually indistinguishable. Pick one.

### P2-2. Standardised coefficient uses `np.std(ddof=0)` implicitly

- Cell 26: `X6_train.std(axis=0)` is numpy default `ddof=0` (population std). The "grade points per 1σ" interpretation is more conventional with `ddof=1` (sample std). With n_train=288 the numerical difference is ≈0.17% — invisible on a bar chart but worth a comment if a sharp student asks.

### P2-3. T2_COLS_IN_USE name shadows convention

- Cell 24 ends by stashing `T2_COLS_IN_USE = t2_cols`. The variable is `UPPER_SNAKE_CASE` (suggesting "constant") yet is reassigned per run. Either keep it lowercase `t2_cols_in_use` or document that it is a "session constant that mutates with KNOB changes." Minor naming nit.

### P2-4. Cell-32 hardcoded `ax.set_ylim(0, 5)` may clip a divergent degree-12 fit

- For very small toy random seeds the degree-12 prediction can swing outside `[0, 5]`. With the default seed (`toy_rng = np.random.default_rng(7)`) this doesn't happen, but variant 1's `(2, 6, 18)` sweep ran from cell 32 in an unmodified subplot grid (see P1-4) might clip. Either remove the ylim or compute it from the data.

### P2-5. Demo line in cell 14 prints `y = 0.30 * study_hours + 2.63`

- Sample of 50 rows from the dataset. The "intuition picture" with red residual segments is informative, but the printed equation differs from T1's learned `0.427 * study_hours + 1.755`. A student comparing the two might briefly worry. A one-liner "this is a small random sample, not the train split — your T1 numbers will differ" would forestall confusion.

### P2-6. Sanity-check messaging in cell 25 calls T2's improvement "a jump of +0.449"

- That's a correct calculation of `r2_t2 - r2_t1`. But the words "using more features pays off" is editorialising — a stricter regression reviewer would note that more features always non-decrease training R² and the test-set jump (which is what's reported here) is the honest signal. This is a teaching point worth one sentence.

### P2-7. Cell-43 sklearn MSE horizontal-dashed reference is recomputed inline

- The expression `((sk.predict(x_gd.reshape(-1, 1)) - y_gd) ** 2).mean()` is duplicated effort given that `sk` is already fit. Cache `sk_mse = ((sk.predict(x_gd.reshape(-1, 1)) - y_gd) ** 2).mean()` in cell 40 and reuse. Cosmetic.

---

## Per-task correctness verdicts

| Task | Expected | Observed | Verdict |
|------|----------|----------|---------|
| **T1 — simple linear regression** | MAE ~1.54 (1.35–1.70), MSE ~3.5 (3.0–4.3), R² ~0.319 (0.25–0.40) | MAE = 1.541, MSE = 3.458, R² = 0.319 | **Correct.** Learned line `0.427 * study_hours_per_week + 1.755` is sensible (positive slope, intercept near grade `2`). Predicts on test split only — honest. |
| **T2 — multiple linear regression** | MAE ~0.85 (0.70–1.05), MSE ~1.20 (0.90–1.60), R² ~0.767 (0.70–0.82) | MAE = 0.838, MSE = 1.181, R² = 0.767 | **Correct.** Coefficient ranking (`study_hours_per_week` > `prior_math_grade` > `exercises_completed` > others) matches the hidden generative formula's coefficients. Standardised-coefficient bar chart is correct in direction and approximate magnitude. |
| **T3 — polynomial sweep** | deg 1: train≈0.2–0.4 / test≈0.2–0.4 (underfit); deg 3: train≈0.85–0.90 / test≈0.85–0.90 (good); deg 12: train≈1.0 / test≈0.3–0.6 (overfit) | deg 1: train=0.215 / test=0.368; deg 3: train=0.882 / test=0.867; deg 12: train=0.999 / test=0.486 | **Correct.** Note: at degree 1 test R² (0.368) is *higher* than train R² (0.215). This is a known small-sample artifact for the toy 14-train/40-test layout — the train sample happens to sit slightly off the line. Not a bug; could be one sentence in the "what to notice" markdown for completeness. |
| **T4 — predict your own grade** | header forecast: `final_score ≈ 7.7`, grade `7` | `final_score = 9.70`, grade `10` | **Computation correct, documentation stale** (see P0-1). Feature-contribution chart sign and ordering look correct vs the trained coefficients. |
| **T5 — gradient descent from scratch** | `|Δw| < 0.05, |Δb| < 0.05` after 100 epochs vs sklearn closed-form | `|Δw| = 0.0000, |Δb| = 0.0001` after 100 epochs (`w = 1.3757, b = 5.1546` vs sklearn `1.3758, 5.1547`) | **Correct.** Gradient formulas `dw = (2/n) Σ error·x`, `db = (2/n) Σ error` are textbook. `lr = 0.05` on standardised inputs is well within stable range. Loss curve drops monotonically from 31.80 → 3.34. |

---

## Linear / Multiple / Polynomial / Gradient-Descent — focused checks (per the brief)

### Linear (T1)
- Five-step recipe followed: build `X1` 2-D, train/test split, fit `LinearRegression`, predict on test, score with MAE/MSE/R². ✓
- `X1 = df[[T1_FEATURE]].values` correctly produces shape `(n, 1)` (not `(n,)`). ✓
- `random_state=42` honored. ✓
- Numerical answers inside sanity-check window. ✓
- Methodological concern: lazy baseline computed on wrong population (P1-1).

### Multiple (T2)
- `X6 = df[t2_cols].values` shape `(360, 6)` for `T2_FEATURE_SUBSET='all'`. ✓
- Same `random_state=42` and `test_size=TEST_SPLIT_RATIO=0.2` as T1, so y_train and y_test are identical to T1's — comparison fair. ✓
- Coefficients: `[0.452, 0.026, 0.311, 0.174, 0.177, 0.179]` (study_hours, attendance, prior_math, sleep, exercises, prog_years). The dataset's hidden generative formula uses `(0.45, 0.025, 0.35, *(quadratic)*, 0.18, 0.30)` — five out of six are within 10% of truth. The seventh (`prior_programming_years`) recovers 0.179 vs truth 0.30 — that's the expected attenuation when prior_math_grade absorbs some of the explained variance via the ordinal-as-numeric encoding. **Not a bug**, just realistic OLS shrinkage on a 288-row train set. ✓
- Subset KNOB validation (`'all' / 'drop_study_hours' / explicit list`) is well-guarded with `raise ValueError` on unknown columns. ✓

### Polynomial (T3)
- `PolynomialFeatures(degree=d, include_bias=False)` used correctly — model still owns its intercept. ✓
- `fit_transform` on train + `transform` on test (not `fit_transform` on test) — correct. ✓
- Train/test R² gap order: degree 1 ≈ -0.15 (slightly negative, underfit small-sample anomaly), degree 3 ≈ +0.02 (good fit, near-zero gap), degree 12 ≈ +0.51 (overfit). ✓ All three degrees in the same `toy_fits` dict for the verify-plot. ✓
- Concerns: P1-4 (silent truncation if sweep length ≠ 3) and P2-4 (ylim clip risk).

### Gradient descent (T5)
- Input standardised before the loop (`x_gd = (x_gd_raw - x_mean) / x_std`). ✓ Without this, the natural-scale gradients on `study_hours_per_week ∈ [0.5, 20]` would push `lr=0.05` into divergence territory.
- Gradient formulas: `dw = (2/n) * (error * x_gd).sum()`, `db = (2/n) * error.sum()`. ✓ Textbook OLS gradient with the `2` constant retained (cosmetic — absorbing it into `lr` would be equivalent).
- Update rule: `w = w - lr * dw`, `b = b - lr * db`. ✓ Sign is correct (subtract gradient, not add).
- Loss recorded with pre-update error — matches the documented convention in the comment.
- Convergence: `|Δw|=0.0000, |Δb|=0.0001` against sklearn's closed-form on the same standardised data. Far better than the `<0.05` acceptance tolerance.
- Loss-curve red-dashed reference matches `sk` MSE — sanity confirmed visually.

---

## Standing-check audit (per QA Inspector protocol)

| Check | Result |
|-------|--------|
| Scope compliance (Plan §1) | ✓ Solution implements exactly T1–T5 per handout. No scope creep into California housing (that lives in homework markdown only). |
| Bugs / null hazards / off-by-ones | None found in the math. Methodological flaw flagged at P1-1. |
| Security (Plan §6) | N/A — pure-numeric synthetic dataset, no inputs, no I/O, no secrets. |
| Performance | All operations vectorised. 360 rows × 6 columns × 100 GD epochs is trivial. No N+1, no unbounded queries. ✓ |
| Accessibility | N/A — Jupyter notebook, no semantic HTML / ARIA surface. Color palette in `COLORS` dict mixes teal/red, which can fail red-green colorblind diagnostics in the residual-vs-fit and contribution charts. P2-suggestion, not enforced here. |
| Convention adherence | `PM/conventions.md` not present in repo; checked against the variants.md spec instead. All KNOB blocks present and structured per spec. ✓ |
| DOCUMENT.md presence | The notebook is in the AI root (`c:\Users\samgl\Documents\GitHub\ExamPrep\AI`); no DOCUMENT.md convention is enforced in this project. N/A for the lab. |
| Tests | Sanity-check cells exist for T1, T2, T3, T5; T4 has no sanity check (it's a "fill in your habits" demo). All sanity checks are print-only (no assertions) — see P1-3. |
| Quality | No `TODO` markers, no `// ...rest`, no `raise NotImplementedError` left over. Five-step recipe + KNOB blocks + tight comments. Production-ready as exam material. ✓ |

---

## Out-of-scope observations (worth noting, not blocking)

1. **Cell 0 markdown is doubling as a spec sheet.** It carries problem statement, mental model, references, variant adaptation guide, expected outputs, and entry-point declaration. For a lab solution it's verbose; for an exam-bank artifact it's appropriate. The risk is exactly the kind of drift seen at P0-1: a long header is not refreshed when implementation tweaks change the answer.
2. **The `display(...)` call in cells 9 and 26** uses Jupyter's implicit `display` from IPython without an explicit import. Runs fine in nbconvert (IPython kernel injects it) but a static linter would flag it. Tolerable.
3. **`prior_programming_years` recovers ~60% of the true coefficient** (`0.179` learned vs `0.30` truth, see Multiple-task section above). A pedagogically curious student might ask "why?" — the answer is feature correlation, not a bug.
4. **Variant 5 (TEST_SPLIT_RATIO=0.5) interacts with the lazy-baseline asymmetry (P1-1)** — that's the one place the methodological flaw is visible to an examiner.

---

## What the PM should do next

1. **Fix P0-1 immediately.** Edit cell 0's "OUTPUTS WHEN RUN" so the T4 sample says `final_score ≈ 9.70` and Danish grade `10`. Then re-run nbconvert to confirm the executed notebook agrees with the header.
2. **Decide on P1-1 / P1-3.** Either (a) fix the lazy-baseline-on-test-set asymmetry and add assertions to sanity checks (recommended for an exam-bank artifact) or (b) explicitly document that the baseline is a "full-dataset reference" and not an apples-to-apples comparison.
3. **Optional but recommended:** address P1-4 by making the T3 verify-plot subplot count dynamic, then a Variant-1 examiner can swap `POLY_DEGREES_SWEEP` to any length safely.
4. **Re-QA after fixes.** Round 2 should be quick: re-run nbconvert, re-check cell-0 forecast vs cell-36 output, confirm assertions don't trip.
5. **Then proceed to Reviewer #2 (Pedagogy / Style)** for the next dimension of review.

---

**Final stance:** The math is correct. The bookkeeping around the math is slipshod in two places (stale forecast at P0-1, asymmetric baseline at P1-1) and silent-failure-prone in two more (no asserts at P1-3, fixed-3 subplot at P1-4). Fix P0-1 before any further review; the P1 batch can be addressed in a single follow-up engineering pass.

— Lab Reviewer #1 (Correctness), Round 1, MLLab2-Regression

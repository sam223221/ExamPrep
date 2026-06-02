# MLLab2-Regression — Exam Variant Bank

This file is the curated list of exam-style variants for the Regression
notebook (`lab2_regression_solution.ipynb`). Each variant is a
self-contained "exam question" that an examining agent (or a student)
must answer using **only**:

- the header markdown cell of `lab2_regression_solution.ipynb`,
- the `# KNOB:` comment blocks inside the solution code cells,
- the visible variable names declared by each TODO cell
  (`X1`, `X6`, `model_t1`, `model_t2`, `toy_records`, `toy_fits`,
  `my_profile`, `loss_history`, etc.),
- the function signatures that ship with the notebook
  (`make_student_grade_data`, `snap_to_danish`).

No reading the function bodies of `make_student_grade_data`, no peeking
at the hidden generative formula inside it, no reading the L11 lecture
PDF, no reading the lab handout PDF.

The exam-agent gate (spec §8.2) runs **three** of these variants in
parallel against the locked solution; all three must report `SOLVED`.

Seeded from plan Appendix B (MLLab2-Regression row); extended to be
self-contained exam questions with explicit acceptance criteria.

---

## Variant 1 — Polynomial degree sweep on the toy 2-D data

**Question.** The default T3 solution sweeps polynomial degrees
`[1, 3, 12]` on the toy 1-D dataset (14 train points + 40 test points)
and prints / plots train and test R² for each. Change the KNOB(s) so
that the sweep now uses degrees **`[1, 3, 12]`** in the order
`underfit → goodfit → overfit` — i.e. confirm that the default is
already an underfit→goodfit→overfit sequence — and then **re-run with
degrees `[2, 6, 18]`** to show the same pattern at a different scale.

Report:

1. Train R² and Test R² for each of the six total degrees (three from
   the default `[1, 3, 12]` sweep, three from the new `[2, 6, 18]`
   sweep).
2. Which degree in `[2, 6, 18]` plays each role (underfit, good fit,
   overfit) and why.
3. The train-test R² gap for the most overfit model in each sweep.

**Expected KNOB changes.**

- `POLY_DEGREES_SWEEP` from the default tuple `(1, 3, 12)` to
  `(2, 6, 18)` for the second sweep.
- Keep `TOY_RANDOM_SEED`, `TOY_N_TRAIN`, `TOY_NOISE_STD` at their
  defaults so the comparison is apples-to-apples; the only knob the
  variant actually requires is `POLY_DEGREES_SWEEP`.

**Acceptance.** Six (degree, train_R², test_R², gap) rows reported.
The student/agent must identify which degree in `[2, 6, 18]` is the
overfit (degree 18: train R² ≈ 1.0, big test-train gap) and which is
the goodfit (typically degree 6, close to the truth's intrinsic
flexibility). Brief justification using KNOB-block vocabulary
("the gap is the overfitting signal").

---

## Variant 2 — Drop the `study_time` feature from the multiple regression

**Question.** The T2 solution fits a multiple linear regression using
**all six** features in `FEATURE_COLS`. Drop `study_hours_per_week`
(the lab's "study time" feature — the strongest single predictor) and
refit the multiple regression on the remaining five features. Report:

1. New test MAE, MSE, and R² (call them `mae_t2_dropped`,
   `mse_t2_dropped`, `r2_t2_dropped` or similar).
2. R² **change**: `Δ R² = r2_t2_dropped − r2_t2`. Expected to be
   strongly negative (around −0.30 to −0.40 — `study_hours_per_week`
   is the dominant signal and removing it costs a lot).
3. Which feature became the **largest standardised coefficient** after
   dropping study time? (Hint: it will be a feature that previously sat
   second-strongest on the bar chart — `prior_math_grade`.)

**Expected KNOB changes.**

- `T2_FEATURE_SUBSET` from `"all"` to `"drop_study_hours"` (or
  equivalently, set it to the explicit list of the remaining five
  feature column names). The KNOB block must document both forms.
- All other KNOBs (test split, random state) untouched so the
  comparison is fair.

**Acceptance.** Three numbers (MAE, MSE, R² for the 5-feature model),
the signed Δ R², and one sentence interpreting why dropping study time
hurts. The agent/student should reference the KNOB documentation
explaining that the dropped feature was the strongest signal in the
correlation heatmap.

---

## Variant 3 — Predict for a new student row (KNOB-defined inputs)

**Question.** A new student walks in with the following habits. Using
the T2 model (six-feature linear regression), predict their
`final_score` and the snapped Danish grade. Then show the per-feature
contribution chart and report which two habits push the prediction up
the most and which one pulls it down the most.

**The new student's row** (override every entry in `my_profile`):

| Feature | Value |
|---|---|
| `study_hours_per_week` | `4.0` |
| `attendance_rate_pct` | `60.0` |
| `prior_math_grade` | `2` |
| `sleep_hours` | `6.0` |
| `exercises_completed` | `3` |
| `prior_programming_years` | `0.5` |

Report:

1. The predicted continuous `final_score` (one number, two decimals).
2. The snapped Danish grade (one of `-3, 00, 02, 4, 7, 10, 12`).
3. The single largest *negative* contributor (feature name + signed
   grade-point contribution).
4. Any features whose contribution is roughly **zero** (i.e. this
   student is close to the class average on that habit).

Note: with the values given above, this student is below the class
average on **every** feature, so all six contributions will be
negative. That itself is the lesson — a profile uniformly below
average gets a uniformly-negative bar chart.

**Expected KNOB changes.**

- Replace every value in `my_profile` per the table above. The KNOB
  block over `my_profile` documents the allowed range for each entry.
- No other KNOBs need to change.

**Acceptance.** A predicted `final_score` in roughly the `0 to +2`
range (this student's profile is well below the class average on the
strongest signals), a snapped Danish grade of `02` (or possibly `00`
under rounding tolerance), and a correct identification of
`study_hours_per_week` as the dominant negative contributor (~-1.7
grade points) with `prior_math_grade` next (~-0.9), and
`prior_programming_years` / `sleep_hours` close to zero contribution.

---

## Optional extras (not part of the gate, useful for self-practice)

### Variant 4 — Learning-rate sensitivity in gradient descent (T5 bonus)

**Question.** The default T5 gradient-descent loop uses `lr = 0.05`
and converges in 100 epochs to within `|Δw|, |Δb| < 0.05` of sklearn's
closed-form answer. Re-run the loop with **`lr = 0.005`** (10× smaller)
and **`lr = 0.5`** (10× larger). Report:

1. Final `(w, b)` and `|Δw|, |Δb|` for each setting.
2. Which run, if any, has diverged or is still climbing at epoch 100?
3. What this says about the learning-rate / epochs tradeoff.

**Expected KNOB changes.**

- `GD_LEARNING_RATE` from `0.05` to `0.005`, then to `0.5`.
- Optionally bump `GD_N_EPOCHS` to give the slow setting a fair shot.

**Acceptance.** Two `(w, b)` pairs plus one sentence each on why the
small lr is too cautious and the large lr risks instability.

### Variant 5 — Train/test split ratio

**Question.** The default split is `test_size=0.2` (288 train / 72
test). Re-run T2 with `test_size=0.5` (180 train / 180 test) and
report the new test R². Does the model still beat the lazy baseline?

**Expected KNOB changes.** `TEST_SPLIT_RATIO` from `0.2` to `0.5`,
keeping `random_state=42`.

**Acceptance.** New R² (expected: lower but still well above 0), plus
a sentence on why halving the training set hurts R² but doesn't
collapse the model.

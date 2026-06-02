# Lab Reviewer #1 (Correctness) — MLLab1-Classification, Round 1

**Reviewer role:** Correctness inspector
**Notebook under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab1_classification_solution.ipynb`
**Handout reference:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab1_classification_handout.ipynb`
**Execution command run (PM-supplied command had `--inplace=false`, which is invalid `nbconvert` syntax; substituted equivalent):**

```
py -3.12 -m jupyter nbconvert --to notebook --execute \
  --output lab1_classification_solution_review_check.ipynb \
  lab1_classification_solution.ipynb
```

**Execution result:** Notebook converted and written (1019334 bytes). **Cell errors: 0.** Verified via grep for `"output_type": "error"`, `"ename":`, and `"traceback":` in the executed notebook — all returned zero matches. Single non-fatal `RuntimeWarning` from `zmq/_future.py` about Proactor event loop (Windows-only, harmless, unrelated to lab content).

---

## Status: **Pass with concerns**

The notebook is logically correct, fully reproducible end-to-end, all six tasks (T1–T6) are implemented, and there are no cell errors. The decision-tree and random-forest outputs are *internally consistent* with the synthetic data. However, several pedagogical / interpretive concerns are flagged below: the unbounded single tree's test accuracy is barely above class baseline (0.594 vs. 0.516), and the Random Forest does **not** in fact beat the best single tree (RF=0.688 vs. depth-3 tree=0.703), which contradicts the narrative the notebook prints at T5.

---

## P0 findings (block ship)

**None.**

---

## P1 findings (important — should fix before next round)

### P1-1. RF comparison baseline is misleading (T5 narrative vs. T4 evidence contradicts itself)
- **Location:** `lab1_classification_solution.ipynb`, cell after the `# KNOB: RF_N_ESTIMATORS` block (T5), and surrounding markdown `"The Random Forest usually matches or improves on the single tree by averaging out individual-tree mistakes."`
- **Evidence (from executed run):**
  - T3 unbounded tree: `tree_acc = 0.594`
  - T4 depth sweep: best test acc `= 0.703` at `max_depth = 3`
  - T5 Random Forest: `rf_acc = 0.688`
  - T5 prints `Gain over tree: +0.094` — true relative to the unbounded `tree_acc`, but **the Random Forest is actually 1.5 percentage points worse than the best regularised single tree from T4 (0.688 < 0.703).**
- **Why this matters:** The lab's pedagogical claim is "many trees voting are usually more stable / better than one tree." The seed-42 evidence on this dataset directly contradicts that claim once you compare apples to apples (best regularised tree vs. forest). A diligent student who actually looks at the printed numbers will be confused or — worse — internalise the wrong conclusion.
- **Suggested fix:** Either (a) compare `rf_acc` against the *best* depth from the T4 sweep, with a sentence acknowledging "on this small/noisy dataset, a single well-regularised tree can occasionally tie or beat the forest"; or (b) bump `N_STUDENTS` to ~800–1000 in the solution so the RF advantage stabilises and matches the narrative; or (c) keep N=320 but explicitly add a disclaimer to the markdown that "with only 64 test rows and a noisy boundary, the forest gain is within sampling noise."

### P1-2. Unbounded single tree test accuracy (0.594) is essentially the majority-class baseline
- **Location:** T3 cell output (`Decision Tree (max_depth=None)`).
- **Evidence:** Test set class balance is 31 / 33 (Need support / Pass), so guessing "Pass" always = 33/64 = 0.516. The unbounded tree scores 0.594 — only ~5 percentage points above the trivial baseline, with train accuracy 1.000 and a train–test gap of +0.406.
- **Why this matters:** Pedagogically intentional (T3 → T4 wants to motivate overfitting), so this is **not a bug**. But the markdown after T3 reads `"The notebook should print a sensible test accuracy"` — students may interpret 0.594 as broken rather than as the intended overfitting demo. The solution's own narrative below the cell does not call out that the test accuracy is intentionally bad here.
- **Suggested fix:** Add an explicit one-liner under the T3 output: *"This unbounded-depth tree is the worst test-accuracy run you will see in this notebook on purpose — T4 will show why."*

### P1-3. Depth-1 and depth-2 yield identical test accuracy — under-explained
- **Location:** T4 depth-sweep table (executed output of the `# KNOB: DEPTH_GRID` cell).
- **Evidence:**
  ```
  max_depth  train_acc  test_acc   gap  leaves
          1      0.695     0.641 0.055       2
          2      0.695     0.641 0.055       4
  ```
  Both rows are identical in train and test accuracy, despite depth-2 having twice the leaves. Plausible — the second-level splits refine training partitions in a way that doesn't flip any of the 64 test predictions — but to a student this looks like a copy-paste bug.
- **Why this matters:** Eroded trust in the notebook's correctness when nothing is wrong.
- **Suggested fix:** Either add `min_samples_leaf` or a different `random_state` for the sweep so depth-2 differs meaningfully from depth-1, **or** add one sentence in the markdown that this "stuck" pattern is real and explains why (second-level splits land inside the same predicted-class region of the test set).

### P1-4. Depth-sweep test-accuracy curve is non-monotonic in a way that confuses the "underfit → balance → overfit" story
- **Location:** T4 depth-sweep output.
- **Evidence:** Test accuracies progress `1: 0.641, 2: 0.641, 3: 0.703, 4: 0.594, 5: 0.656, 6: 0.625, 8: 0.656, None: 0.594`. The drop from depth 3 (0.703) to depth 4 (0.594) is sharper than the drop from depth 8 to None, and depth-5 then recovers. The teaching narrative in the surrounding markdown says *"Deep trees drive training accuracy very high while test accuracy stops improving"* — implying a smooth plateau. The reality is jagged.
- **Why this matters:** The accompanying plot includes annotations "Underfit risk" (at depth 1) and "Overfit risk" (at depth None), but the real shape is U-with-zigzag, not a clean U. Pedagogically, this is the right learning, but the solution does not call it out.
- **Suggested fix:** Add a sentence to the "What you should notice" block: *"Notice the curve is jagged, not smooth — with only 64 test rows, single-sample noise dominates ~1.5 pp swings."* This sets correct expectations for the plot.

### P1-5. `--inplace=false` in the documented re-execution command is invalid `nbconvert` syntax
- **Location:** Top markdown of `lab1_classification_solution.ipynb`, line 4–5: `Re-execute end-to-end with: ` `py -3.12 -m jupyter nbconvert --to notebook --execute --inplace=false --output lab1_classification_solution.ipynb lab1_classification_solution.ipynb`
- **Evidence:** Running that command verbatim errors with `argument --inplace: ignored explicit argument 'false'`. `--inplace` in `nbconvert` is a boolean *flag*, not a key-value option.
- **Why this matters:** A student following the documented command will hit an immediate error and may lose trust in the notebook.
- **Suggested fix:** Drop `--inplace=false` entirely. The `--output <name>` flag already controls where the result is written, so the command is well-formed without `--inplace`. Replacement:
  ```
  py -3.12 -m jupyter nbconvert --to notebook --execute \
    --output lab1_classification_solution.ipynb lab1_classification_solution.ipynb
  ```

### P1-6. Solution silently adds `n_jobs=-1` to RandomForestClassifier — handout/spec did not request it
- **Location:** T5 RF instantiation cell.
- **Evidence:** Handout T5 hint says `Use RandomForestClassifier(n_estimators=200, random_state=42)`. Solution uses `RandomForestClassifier(n_estimators=RF_N_ESTIMATORS, max_depth=RF_MAX_DEPTH, random_state=RANDOM_STATE, n_jobs=-1)`.
- **Why this matters:** Non-deterministic in subtle ways on some platforms (parallel trees can produce slightly different bootstrap orderings depending on the threading backend in older sklearn versions). On current sklearn the result is bitwise reproducible, so this is borderline P2, but a strict spec-conformance review flags it.
- **Suggested fix:** Either drop `n_jobs=-1`, or add a comment justifying it (`n_jobs=-1 is safe under sklearn ≥ 0.24 with `random_state` set`).

---

## P2 findings (polish / nice-to-have)

### P2-1. RF reports `predicted Pass probability = 0.990` from a model whose held-out accuracy is 0.688
- **Location:** T6 final output.
- **Why this matters:** A 99% confidence from a 69% accuracy model is the textbook setup for the "calibration ≠ accuracy" misconception. The "Common beginner mistake" markdown at the end touches on it ("Treating one probability as truth…") but does not explicitly say "the model thinks it is 99% confident, but it is only 69% accurate overall — these are different things."
- **Suggested fix:** One added sentence in the wrap-up about probability calibration.

### P2-2. Feature-importance ordering differs from the data-generating coefficients — worth a callout
- **Location:** T5 importance output.
- **Evidence:** Generator's logit coefficients: `+0.47 * study_time_hours, -1.15 * past_failures, -0.08 * absences, +1.05 * did_lab, -0.30 * (sleep - 7.1)**2`. RF importance ranking: `study_time_hours (0.394) > sleep_hours (0.257) > absences (0.151) > past_failures (0.118) > did_lab (0.080)`.
  - `study_time_hours` ranking first is plausible (large variance × moderate coefficient ≈ large contribution to score).
  - But `sleep_hours` (a quadratic term centred at 7.1, contribution rarely exceeds ~0.3 in absolute value) ranking *above* `past_failures` (coefficient −1.15) and `did_lab` (coefficient +1.05) is suspicious. With random_state=42 and 200 trees this is reproducible, so it is not a bug — but it is also not the ranking a thoughtful student would predict from the generator.
- **Why this matters:** Pedagogical surprise that goes unexplained.
- **Suggested fix:** Add one paragraph in the T5 narrative or wrap-up: *"Tree-based importance is biased toward continuous, high-cardinality features (study_time_hours, sleep_hours) over low-cardinality categorical features (did_lab, past_failures). This is a known artefact of impurity-based feature importance — see permutation importance as a less-biased alternative."*

### P2-3. Two helper label columns (`pass_label`, `did_lab_label`) are in `df` but never explicitly excluded from a potential `df.corr()` accidental leak
- **Location:** T1 generator.
- **Why this matters:** The correlation heatmap explicitly lists the six numeric columns by name (no leak), so this is purely defensive. A copy-pasting student who writes `df.corr()` without a column list would still be safe because pandas drops string columns automatically. No fix required; flagged only because a reviewer should mention it.

### P2-4. T3 print line says `"Need-support prob: 0.010"` — minor formatting nit
- **Location:** T6 final stdout: `Need-support prob:     0.010`.
- **Why this matters:** Hyphenation inconsistent with the rest of the notebook which uses `"Need support"` (no hyphen) everywhere else (class names, labels, axis tick labels).
- **Suggested fix:** Use `"Need support prob:"` for consistency.

### P2-5. Markdown wrap-up table lists `RF_MAX_DEPTH` and `DEPTH_GRID` as KNOBs but there is no exam variant referencing `RF_MAX_DEPTH`
- **Location:** Wrap-up cheat-sheet table.
- **Why this matters:** Minor — variants.md (not read in this review) may already cover it. Flagging for completeness.

---

## QA Checklist (Plan §7) status

| Item | Status | Note |
|---|---|---|
| 1. Notebook executes end-to-end with 0 cell errors | **Pass** | Verified via `nbconvert --execute`; zero `error` / `ename` / `traceback` entries in executed output. |
| 2. T1 (dataset generation + X/y split) correct | **Pass** | Shape (320, 8) with 5-col `X` and 1-col `y`. Class balance 166/154 (51.9% / 48.1%) — reasonable. |
| 3. T2 (stratified split) correct | **Pass** | Train 256, test 64. Proportions 0.48/0.52 train vs 0.484/0.516 test — stratification working. |
| 4. T3 (single decision tree) trains and reports sensible metrics | **Pass with concerns** | Trains; reports depth=13, leaves=71, train=1.000, test=0.594. Numbers are internally consistent but pedagogical framing weak — see P1-2. |
| 5. T4 (depth sweep) shows under/over-fit story | **Pass with concerns** | Curve has the expected shape macroscopically (best at depth 3, overfit at None), but non-monotonic in the middle — see P1-3, P1-4. |
| 6. T5 (random forest) trains, accuracy comparable to/above tree | **Fail** | RF (0.688) beats the unbounded tree (0.594) but **loses to the best-depth tree (0.703)**. Markdown narrative claims "matches or improves on the single tree" — contradicted by the printed numbers. See P1-1. |
| 7. T6 (custom profile prediction) produces a class + probability | **Pass** | Predicted "Pass" with probability 0.990 for the default profile. Mechanically correct. Calibration concern is P2-1. |
| 8. Random forest feature importances printed | **Pass** | All 5 features present, sum to ≈1.0. Ordering documented but worth a pedagogical callout — P2-2. |
| 9. Reproducibility (random_state pinned) | **Pass** | `RANDOM_STATE = 42` flows into `make_student_success_data`, `train_test_split`, `DecisionTreeClassifier`, and `RandomForestClassifier`. |
| 10. KNOB documentation present and accurate | **Pass** | Every KNOB has a docstring-style block documenting default, range, effect, and exam-variant usage. Conforms to spec §8.1. |

---

## Acceptance criteria (Plan §1) status

(Inferred from the solution notebook's own preamble — no separate Feature Plan was provided to the reviewer.)

| Criterion | Status |
|---|---|
| T1: generator called, `df` / `feature_cols` / `target_col` / `X` / `y` populated | **Met** |
| T2: stratified train/test split, 20% held out | **Met** |
| T3: DecisionTreeClassifier fit + accuracy + classification report printed | **Met** |
| T4: depth sweep across `[1, 2, 3, 4, 5, 6, 8, None]` reporting train/test accuracy | **Met** |
| T5: RandomForestClassifier(200) fit + accuracy + feature importances | **Met** |
| T6: one-row DataFrame from `MY_PROFILE` → `predict` + `predict_proba` | **Met** |
| Zero `raise NotImplementedError` after execution | **Met** |
| End-to-end re-execution succeeds | **Met** (with corrected nbconvert command — see P1-5) |

---

## DOCUMENT.md audit

**N/A** — this lab is a single Jupyter notebook (no directory of source files). No `DOCUMENT.md` requirement applies at the notebook level.

---

## Out-of-scope observations

1. **`lab1_classification_solution_review_check.ipynb`** is now present in the working directory as a by-product of my execution (then deleted). PM should ensure this transient file is not committed.
2. The handout's T4 plotting cell hardcodes `depth_labels = ['1', '2', '3', '4', '5', '6', '8', 'None']`, so if a student also edits `depths`, the labels will silently misalign. The solution fixes this dynamically (good). The **handout** could be improved but is out of scope for this review.
3. The handout's T6 doesn't reindex `my_profile_df` by `feature_cols`; the solution does. Good defensive coding by the solution, but worth noting that students copying the handout cell will have an order-dependent bug that the solution silently masks.

---

## Concerns / risks

- **Primary risk:** P1-1 — the RF-vs-tree comparison narrative contradicts the printed evidence on the chosen seed. This is the single most likely thing to confuse exam students.
- **Secondary risk:** P1-5 — the documented execution command is broken. Any reader who runs it verbatim will hit an immediate error.
- **Tertiary:** the notebook's metrics are noisy because the test set is only 64 rows. A bigger `N_STUDENTS` would stabilise the depth sweep and the RF/tree comparison without changing the lab's pedagogical aim.

---

## What PM should do next

1. **Dispatch fixer agent** to address P1-1, P1-5, and at least one of {P1-2, P1-3, P1-4} as a single combined edit (all are narrative / KNOB tweaks, no new code paths). Recommended approach:
   - Either bump `N_STUDENTS` to 800 (stabilises everything, no narrative changes needed) **or** keep N=320 and add the disclaimer paragraphs called out above.
   - Drop `--inplace=false` from the top-of-notebook re-execute command.
2. **Re-QA (round 2)** after the fix to confirm RF accuracy now meets or beats the best single tree (or that the narrative no longer claims it does).
3. **Then proceed to App Tester / Code Reviewer** as normal.

## DOCUMENT.md updated

N/A for QA / Lab Reviewer.

---

**Report submitted by:** Lab Reviewer #1 (Correctness)
**Date:** 2026-05-22
**Round:** 1

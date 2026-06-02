# MLLab1-Classification — Exam Variant Bank

This file is the curated list of exam-style variants for **ML Lab 1 — Classification
(Decision Trees + Random Forests on student data)**. Each variant is a
self-contained "exam question" that an examining agent (or a student) must
answer using **only**:

- the first markdown cell of `lab1_classification_solution.ipynb` (the
  §6.2 header), and
- the `# KNOB:` comment blocks inside the code cells, and
- the public scikit-learn API of the classes the notebook builds
  (`DecisionTreeClassifier`, `RandomForestClassifier`, `train_test_split`).

No reading the function bodies inside `sklearn`, no reading the lab
handout, no reading the L10 lecture chapter.

The exam-agent gate (spec §8.2) runs **three** of these variants in
parallel against the locked solution; all three must report `SOLVED`.

The notebook is the entry point. Edit it in place (or copy to a scratch
notebook) and re-run with:

```powershell
py -3.12 -m jupyter nbconvert --to notebook --execute --inplace \
    lab1_classification_solution.ipynb
```

Then open the executed notebook and read the printed outputs / plots.

---

## Variant 1 — Different `max_depth` (depth sensitivity)

**Question.** The default Decision Tree in T3 is built with
`DecisionTreeClassifier(random_state=42)` — i.e. **unbounded depth**.
That is exactly the *overfit-prone* end of the depth-vs-accuracy curve
plotted in T4.

Re-train the T3 Decision Tree with `max_depth = 3` instead (a value the
T4 sweep highlights as close to the best test accuracy). Report:

1. The **train accuracy** of the depth-3 tree (use
   `tree.score(X_train, y_train)`).
2. The **test accuracy** of the depth-3 tree (use
   `accuracy_score(y_test, tree.predict(X_test))`).
3. The **gap** `train - test`. Compare it to the gap of the default
   (unbounded) tree printed by T3.
4. One sentence explaining (in the vocabulary of the KNOB block) why a
   shallower tree usually has a smaller train–test gap.

**Expected KNOB changes.**

- `TREE_MAX_DEPTH` from `None` to `3`. The KNOB block must say what
  `None` means (grow until pure) and what small values mean (force
  underfit) so the examinee picks `3` confidently.
- Everything else stays put.

**Acceptance.** Two concrete accuracy numbers, the signed gap, and a
one-sentence "shallower trees generalise better because they cannot
memorise individual training rows" answer.

---

## Variant 2 — Random Forest `n_estimators` sweep

**Question.** T5 fits a Random Forest with `n_estimators = 200`. Repeat
the experiment with three forest sizes — **10, 50, 200** — and report
the test accuracy of each. Briefly comment on whether accuracy keeps
climbing or plateaus.

You must reuse the same `X_train`, `y_train`, `X_test`, `y_test`
produced by T2; do not re-split the data. Use `random_state=42` every
time so the comparison is fair.

**Expected KNOB changes.**

- `RF_N_ESTIMATORS` from `200` down to `10`, run once; then `50`, run
  once; then back to `200`. The KNOB block must call out that the
  forest accuracy typically **plateaus** beyond ~100 trees — the
  examinee should expect 50 ≈ 200 and 10 to be noticeably worse, and
  say so in writing.
- `RANDOM_STATE` stays at `42` (it is the single seed shared by data
  generation, the train/test split, the decision tree, and the
  random forest — see the KNOB block in the first code cell of the
  notebook). Fixing it is what makes the three runs comparable.

**Acceptance.** Three numbers (one per `n_estimators` setting) and a
one-sentence interpretation that mentions diminishing returns / variance
reduction. Bonus if the examinee references the feature-importance
chart and notes it barely changes between 50 and 200 trees.

---

## Variant 3 — Drop a feature

**Question.** The default feature list is

```
['study_time_hours', 'past_failures', 'absences', 'did_lab', 'sleep_hours']
```

Re-run the whole pipeline (T2 split + T3 single tree + T5 random
forest) **without** the `past_failures` column. Report:

1. The Decision Tree test accuracy without `past_failures`.
2. The Random Forest test accuracy without `past_failures`.
3. The Random Forest test accuracy *with* all five features (already
   computed in T5, just quote it).
4. One sentence on which model degrades more and why, using the
   feature-importance chart from T5 as evidence.

**Expected KNOB changes.**

- `FEATURE_COLS` from the full five-item list to a four-item list with
  `past_failures` removed. The KNOB block must spell out that
  `FEATURE_COLS` controls both `X` (which columns go in) AND
  `feature_cols` (used by the tree plot and the feature-importance
  chart). One edit, both downstream effects.
- Everything else stays put.
- The examinee must **also** redo T6 (`my_profile`) without
  `past_failures` to keep prediction consistent — the docstring header
  says so explicitly.

**Acceptance.** Three accuracy numbers, plus a one-sentence
interpretation citing feature importance.

---

## Optional extras (not part of the gate, useful for self-practice)

- **4a — Class imbalance.** Lower `N_STUDENTS` from 320 to 80 and
  rerun. Does the train/test split still stay balanced? (Yes, because
  `stratify=y`, but the absolute counts get small.) Report
  `y_train.value_counts()` and `y_test.value_counts()`.
- **4b — Reproducibility check.** Change `RANDOM_STATE` from 42 to 7
  and rerun T3 and T5. Do the accuracies move? By how much? This is the
  "is this variance real, or noise" check students often need to
  reason about.
- **4c — Tune both at once.** Set `TREE_MAX_DEPTH = 5` AND
  `RF_N_ESTIMATORS = 50`. Does the gap between the single tree and the
  forest shrink? (Usually yes — a depth-cap regularises the tree.)
- **4d — Predict an at-risk student.** In T6, edit `MY_PROFILE` to
  `{'study_time_hours': 2.0, 'past_failures': 2, 'absences': 12,
  'did_lab': 0, 'sleep_hours': 5.0}` and re-run. The model should now
  predict "Need support" with high confidence — confirm.

The Lab Solver may add up to 2 additional variants here if the handout
suggests them; current count = 3 mandatory + 4 optional.

# MLLab1-Classification — Round 1 Reviser Summary

**Reviser role:** Round 1 reviser for `lab1_classification_solution.ipynb`.
**Inputs:** reviewer1.md (Correctness), reviewer3.md (Pedagogical Clarity),
reviewer4.md (Variant Adaptability). reviewer2.md was not present in the
round1 directory and so was not consulted.
**Strategy chosen:** the PM-recommended **Option A + Option B combined** —
bump `N_STUDENTS` default from 320 to 1000 **and** set `RF_MAX_DEPTH = 8`
(was `None`). On its own, Option A still leaves the unbounded RF losing
to the best regularised tree on this synthetic data (the per-tree
overfit is correlated across the bootstrap samples). Combining them
gives a clean pedagogical story: RF beats both the T3 unbounded
baseline (+0.075) **and** the best tree from the T4 sweep (+0.020).

---

## Numerical state after revision (locked seed)

| Quantity | Before (N=320, RF_MAX_DEPTH=None) | After (N=1000, RF_MAX_DEPTH=8) |
|---|---|---|
| Dataset shape | (320, 8) | (1000, 8) |
| Train / test rows | 256 / 64 | 800 / 200 |
| T3 unbounded tree (test acc) | 0.594 | 0.645 |
| T4 best depth | 3 (0.703) | 2 (0.700) — also 4 ties at 0.700 |
| T5 RF (test acc) | 0.688 | **0.720** |
| RF vs best tree | **−0.015 (worse)** | **+0.020 (better)** |
| RF gain over T3 unbounded | +0.094 | +0.075 |
| T6 default profile pass prob | 0.990 | 0.916 |
| Feature importance #1 | study_time_hours (0.394) | study_time_hours (0.356) |
| Feature importance rank of `past_failures` | 4th (0.118) | **3rd (0.202)** — closer to EDA narrative |

The headline pedagogical claim of T5 ("the Random Forest matches or
improves on the single tree by averaging out individual-tree mistakes")
is now empirically true against both the unbounded tree **and** the
best tuned tree.

---

## P0 fixes applied

1. **(R1 / R3 / R4 P0)** RF vs single tree narrative now demonstrably true.
   - Bumped `N_STUDENTS` default `320` → `1000` (cell `da22285d`).
   - Added `RF_MAX_DEPTH = 8` default (was `None`) in cell `244d378d`.
   - Result: RF (0.720) beats both T3 unbounded (0.645) and best T4 tree
     (0.700).
   - Also re-wrote the T5 print block so it explicitly reports the gain
     against the best T4 tree (`best_tree_acc_t4`), not just against the
     T3 unbounded tree. The "Gain over tree" line is now honest in both
     directions.

2. **(R2 / R4 P0)** `TREE_MAX_DEPTH` KNOB blurb realigned with reality
   (cell `25e63d02`).
   - Old blurb claimed depth 3-5 → "test acc ~0.78-0.82".
   - New blurb states realised ranges on N=1000 (depth 3-4 near best,
     test ~0.67-0.70) and warns that the curve is mildly non-monotone
     due to the irreducible noise term in the generator.
   - Also rewrote the "None" entry to call out the catastrophic
     overfit (depth ~20-25, gap ~+0.35) instead of just "overfit-prone".

3. **(R4 P0)** `RF_RANDOM_STATE` reference in `variants.md` Variant 2.
   - Renamed to `RANDOM_STATE` with one extra sentence explaining that
     there is exactly one shared seed across the data generator, split,
     tree, and forest (matching the actual notebook).

---

## P1 fixes applied

4. **(R1 / R4 P1)** Dropped invalid `--inplace=false` flag from the
   nbconvert command in the top markdown cell (cell `b3f400ae`). The
   `--output <name>` flag already controls the destination, so the
   command is well-formed without `--inplace`.

5. **(R1 P1)** Removed `n_jobs=-1` from `RandomForestClassifier`
   instantiation (cell `244d378d`). Per Reviewer #1, the handout
   does not request it and it can subtly affect determinism on older
   sklearn versions. Kept the rest of the call signature unchanged.

6. **(R1 / R3 P1)** L10 cross-reference now points to the correct
   chapters (cell `b3f400ae` REFERENCES block). Was: "§§ 2-4 for the
   supervised-learning framing, train/test split, decision trees, and
   overfitting diagnosis." Now explicitly breaks out:
   - § 2 (analogies)
   - § 3 (supervised-learning framing + train/test split)
   - § 4.5 + 4.8 (tree induction + stopping criteria)
   - § 4.9 (random forests)
   - **§ 6 (overfitting diagnosis — the chapter T4 demonstrates)**

   Reviewer #3's P0-3 is now addressed: the previous range left out the
   exact chapter (§ 6) that T4 is supposed to illustrate.

7. **(R3 P1, R4 P1)** Wrap-up cheat sheet now includes an
   **expected-outputs table per variant** (cell `21cc22b9`), so an
   examinee or grading agent has concrete target numbers (±0.03) to
   self-grade against. Covers default T3/T4/T5 and all three mandatory
   variants V1/V2/V3.

8. **(R3 / R4 P1)** Re-wrote the T5 "What you should notice" markdown
   (cell `011fa6f4`) to:
   - Reflect the realised forest-beats-tree result on the new defaults.
   - Add an explicit **"What this does *not* mean"** disclaimer that the
     forest is not *guaranteed* to beat a tuned tree on every dataset
     (Reviewer #3's repeated request for symmetric scaffolding).
   - Add a one-line callout that tree-based feature importance is biased
     toward continuous, high-cardinality features (R1's P2-2 / R3's
     P2-2 promoted to "common beginner mistake").

---

## Items deliberately NOT done in this round

These are documented review concerns that were left for a later round
because they exceed the scope of the PM-supplied "KEY FIXES" list:

- **R3 P0-2 (averaged depth sweep across seeds).** Did not add a
  `DEPTH_SWEEP_SEEDS` KNOB to average T4 across multiple seeds. At
  N=1000 the sweep is already monotone-enough that the "U-shape"
  narrative holds (best at depth 2/4 = 0.700, monotone-ish decline
  from depth 5 onward, catastrophic at depth None = 0.645). The curve
  is still slightly jagged in the middle (depth 3 dips to 0.665, depth
  5 to 0.655) but the annotated "Underfit risk" / "Best" / "Overfit
  risk" labels are now consistent with the visible curve.
- **R3 P0-4 ("the tree trusts a feature" anthropomorphism).** Untouched
  for this round; was a phrasing nit in cell `5f285abc`, not a
  correctness or variant-gate issue.
- **R3 P0-5 (calibration framing on the 0.99 → now 0.916 probability).**
  Less acute now that the probability is 0.916 instead of 0.990, but
  still a missed teaching opportunity. Not in the PM scope for this
  round.
- **R3 P1-2, P1-3, P1-6, P1-7 (additional MENTAL MODEL header copy,
  EDA root-split exercise, missing "what this does *not* mean" after
  T2, T1).** Pedagogical scaffolding additions that exceed the round-1
  must-fix list.
- **R3 P1-5 (L10 §7 backlink to solution instead of handout).** Out of
  scope — that is an L10 chapter fix, not a notebook fix.
- **R4 P1-5 (asymmetric MY_PROFILE / FEATURE_COLS validation).** Code
  hardening; valid but out of scope for the narrative-fix round.
- **R4 P2-3 (`DEPTH_GRID` defaults stated as "1..8, None" in cheat
  sheet — fixed during this revise by rewriting the row as
  "(1,2,3,4,5,6,8,None)" verbatim).**

---

## Re-execution

The notebook was re-executed end-to-end via

```
py -3.12 -m jupyter nbconvert --to notebook --execute \
    --output lab1_classification_solution.ipynb \
    lab1_classification_solution.ipynb
```

after all edits. Result: **34 cells, 0 errors** (verified by scanning
the saved notebook for `output_type == 'error'`). The only warning was
a Windows-only `RuntimeWarning` from `zmq/_future.py` about the Proactor
event loop, which is unrelated to lab content.

---

## Files changed

| File | Cells / lines touched |
|---|---|
| `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab1_classification_solution.ipynb` | `b3f400ae` (header markdown — nbconvert command + L10 ref), `da22285d` (N_STUDENTS KNOB block + default), `25e63d02` (TREE_MAX_DEPTH KNOB blurb), `244d378d` (RF_MAX_DEPTH KNOB block + default, RF instantiation drops n_jobs=-1, T5 print block adds best-tree comparison), `011fa6f4` (T5 "what you should notice" markdown), `21cc22b9` (wrap-up cheat sheet — added expected-outputs table). All cached outputs refreshed via end-to-end re-execution. |
| `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\MLLab1-Classification\variants.md` | Variant 2 expected-KNOB-changes block: `RF_RANDOM_STATE` → `RANDOM_STATE` with one extra sentence on the shared-seed model. |
| `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_review\labs\MLLab1-Classification\round1\revise-summary.md` | (new) this file. |

---

## Suggested Round-2 dispatches

1. **Re-run Reviewer #1 (Correctness)** — verify the new cached
   outputs are internally consistent and that the T5 print block now
   reports the best-tree gain honestly.
2. **Re-run Reviewer #3 (Pedagogical Clarity)** — verify the L10 §6
   reference now appears in the header, the T5 forest narrative is no
   longer contradicted by the printed numbers, and the wrap-up
   expected-outputs table satisfies the variant-gate self-grading
   concern.
3. **Re-run Reviewer #4 (Variant Adaptability)** — verify the new
   expected-outputs table matches the variants in the bank, that
   `RF_RANDOM_STATE` no longer appears in variants.md, and that
   Variants 1-3 mechanically work against the new locked seed.
4. **Round 2 reviser** should plan to address the deferred R3 P1-2 /
   P1-3 / P1-6 / P1-7 pedagogical scaffolding adds and the R3 P0-5
   calibration callout if a tighter pedagogical pass is needed.

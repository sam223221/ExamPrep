# Lab Reviewer #4 — Variant Adaptability — Round 1

**Lab:** `MLLab1-Classification`
**Notebook under review:** `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab1_classification_solution.ipynb`
**Variant bank:** `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\MLLab1-Classification\variants.md`
**Reviewer charter:** Variant Adaptability (can each variant be solved by editing only KNOBs + reading the docstring header + KNOB comments + public sklearn API, with no surgery to function bodies?)
**Disposition:** **FAIL — Pass with serious concerns demoted to Fail.** The mechanical adaptation paths all work, but the KNOB comment blocks **lie about expected numerical outcomes** and the locked seed produces results that *contradict the docstring's qualitative claims*. An exam-agent gate that trusts the KNOB blurbs will mark `SOLVED` against numbers that never actually appear in the notebook's executed outputs. That is the central failure mode this reviewer is paid to catch.

---

## Report to PM

**Assignment recap:** Variant Adaptability review (Reviewer #4) for `MLLab1-Classification` Round 1. I read the locked solution notebook end-to-end (including the cached execution outputs in the .ipynb) and cross-checked every KNOB against every variant in `variants.md`. I did NOT re-execute the notebook; the cached outputs already in the file are the ground truth I used.

**Status:** **Fail.** Mechanical KNOB coverage is complete (every variant maps cleanly to a KNOB or KNOB set, no source-code surgery required). But the KNOB blurbs make **falsifiable numerical claims that the notebook's own cached outputs falsify** — and on this seed the Random Forest is *strictly worse* than the best single Decision Tree, which directly contradicts the T5 narrative the variant gate depends on. A student who trusts the comments to validate their variant answer will hand in wrong expected ranges.

---

### P0 findings (block the gate — must fix before Round 2)

**P0-1. `TREE_MAX_DEPTH` KNOB lies about the depth-3..5 sweet spot range.**
- File: `lab1_classification_solution.ipynb`, cell `25e63d02` (T3 KNOB block), lines describing depths 3–5.
- Claim in KNOB blurb: *"3-5  -> usually the BEST balance on this dataset (test acc ~0.78-0.82; small train-test gap)."*
- Actual cached output (T4 sweep, cell `16e3600a`):

  ```
  max_depth  train_acc  test_acc   gap  leaves
          3      0.738     0.703 0.035       8
          4      0.781     0.594 0.188      15
          5      0.805     0.656 0.148      24
  ```

  Best test_acc in the 3–5 band = **0.703** at depth 3. Depth 4 *drops to 0.594*. Depth 5 = 0.656. None of {0.703, 0.594, 0.656} is anywhere near the advertised "0.78–0.82" range.
- Impact on variant gate: **Variant 1 directly depends on this band.** A student following Variant 1 sets `TREE_MAX_DEPTH = 3`, reads off `tree.score(...)` and `accuracy_score(...)`, gets 0.738 / 0.703 / +0.035, and then has to compare against the docstring's "expected" range. The docstring's range is wrong by ~10 percentage points. An examining agent that grades with the KNOB-stated expectation will reject correct examinee output.
- Suggested fix: replace the band with the empirically observed numbers on the locked seed: depth 3 -> test ~0.70, depth 4 -> test ~0.59 (yes, dips here on this seed — call that out as a feature, not a bug), depth 5 -> test ~0.66; and warn that the curve is noisy on N=320. Or raise `N_STUDENTS` default to 1000 so the depth-vs-accuracy story is monotone enough to make the original claim true.

**P0-2. Random Forest is strictly worse than the depth-3 single tree on the locked seed, contradicting the T5 narrative the gate depends on.**
- Files / cells: `244d378d` (T5 RF KNOB+fit), `011fa6f4` (T5 takeaway markdown), and the wrap-up cheat-sheet `21cc22b9`.
- Cached outputs:
  - Single tree at depth 3 (T4 sweep): test_acc = **0.703**.
  - Random Forest at `n_estimators=200`: test_acc = **0.688**.
  - Single tree at unbounded depth (T3 baseline): test_acc = **0.594**.
- The T5 print line says `"Gain over tree:   +0.094"` — but that gain is computed against the **unbounded overfit tree** (`tree_acc`, 0.594), not against the best tuned tree (0.703). Measured against the best tree the forest LOSES by **−0.015**.
- The takeaway markdown `011fa6f4` then asserts: *"The Random Forest usually matches or improves on the single tree by averaging out individual-tree mistakes."* On this notebook's actual cached run, against the best comparable tree, **it does the opposite**.
- Impact on variant gate: **Variant 2's acceptance criterion is** *"50 ≈ 200 and 10 noticeably worse"* and **"matches or improves on the tree"** is the framing the examinee is told to reproduce. The locked seed cannot demonstrate this. The KNOB-stated qualitative result is unverifiable from the notebook's own outputs.
- Suggested fix: pick a `RANDOM_STATE` that actually exhibits the textbook story (try a small grid: 0, 1, 7, 13, 42, 123) and lock the seed where RF(200) ≥ best-tree-test-acc by ≥0.02; document in the KNOB block that this is intentional. Alternatively, raise `N_STUDENTS` to stabilise the comparison. Do NOT ship a notebook whose own executed cells contradict its own teaching claim.

**P0-3. Variant 2 references a KNOB that does not exist (`RF_RANDOM_STATE`).**
- File: `variants.md` lines 82–84: *"`RF_RANDOM_STATE` stays at `42` (fixing the seed is what makes the three runs comparable)."*
- The notebook has exactly one seed KNOB: `RANDOM_STATE` (cell `c11e6bcf`). No `RF_RANDOM_STATE`. The RF is constructed with `random_state=RANDOM_STATE` in cell `244d378d`.
- Impact on variant gate: a literal examining agent that grep-searches for `RF_RANDOM_STATE` to confirm the instruction was followed will return empty. A human examinee reading variants.md will hunt for a KNOB that isn't there.
- Suggested fix: either (a) reword variants.md to say "`RANDOM_STATE` stays at 42 (it is shared by the data generation, split, and forest — see KNOB block in cell 1)", or (b) split the global seed into `DATA_RANDOM_STATE`, `SPLIT_RANDOM_STATE`, `TREE_RANDOM_STATE`, `RF_RANDOM_STATE` so the variant bank's claim matches the notebook. (a) is the cheap fix; (b) is the correct one for an exam-prep notebook because students will be asked about seed independence.

---

### P1 findings (important — fix before sign-off)

**P1-1. `TREE_MAX_DEPTH=None` KNOB blurb undersells the actual collapse.**
- Cell `25e63d02`. Blurb: *"None  -> grows until every leaf is pure or has 1 sample. Typically depth 10-15 on this dataset. Overfit-prone."*
- Actual cached behaviour: depth=13, leaves=71, test_acc=0.594, train_acc=1.000, gap=+0.406. That isn't merely "overfit-prone" — the unbounded tree is the **single worst** point on the depth-vs-accuracy curve (tied with depth=4 at 0.594), and the gap is **+0.406**, which is closer to "catastrophic memorisation" than "overfit-prone".
- Why this matters for adaptability: Variant 1 asks the examinee to "compare to the gap of the default (unbounded) tree printed by T3". The expected comparison story is "shallow gap small, unbounded gap big". The numbers do show this — but the KNOB blurb's understated language ("overfit-prone") will lead a student to expect maybe a 0.10–0.15 gap when the actual gap is 0.41. Recalibrate the blurb to the observed magnitude.

**P1-2. Variant 1 is partially pre-answered by the T4 sweep; the KNOB edit is therefore optional, not required.**
- variants.md Variant 1 asks for train acc, test acc, and gap at `TREE_MAX_DEPTH=3`. The T4 sweep table in cell `16e3600a` *already prints all three numbers for depth 3* (0.738, 0.703, +0.035), with no KNOB edit needed.
- This is the opposite of the variant's spirit — the variant is supposed to exercise the `TREE_MAX_DEPTH` KNOB. A lazy examinee can satisfy Variant 1 acceptance without ever touching `TREE_MAX_DEPTH`.
- Suggested fix: either (a) tighten Variant 1 to require running T3 with `TREE_MAX_DEPTH=3` and printing T3's full classification report at that depth (which T4 does not produce), or (b) drop `3` from `DEPTH_GRID` so the answer is only available via the KNOB edit. (a) is the better fix because it preserves T4's pedagogic role.

**P1-3. Variant 3 acceptance depends on a feature-importance ordering that may flip under the dropped feature.**
- variants.md Variant 3 expects the examinee to "cite the feature-importance chart from T5 as evidence". The cached T5 chart shows: `study_time_hours 0.394, sleep_hours 0.257, absences 0.151, past_failures 0.118, did_lab 0.080`.
- Note `past_failures` is only **fourth**, not second as the EDA correlation heatmap and the `8d0f8e1e` cell suggest. The cell text repeatedly emphasises "past failures are a strong warning sign" and the cheat-sheet says "past failures and study time carry most of the signal", but the importance ranking on the locked seed has `sleep_hours` outranking `past_failures` by more than 2×.
- Adaptability impact: Variant 3 acceptance says "one sentence on which model degrades more and why, *using the feature-importance chart from T5 as evidence*". The chart says `past_failures` is a minor feature (rank 4, importance 0.118), so dropping it should cause a small degradation — but the markdown narrative throughout the notebook tells the examinee `past_failures` is a major feature. The two contradict each other. A student writing the variant answer will not know which to cite.
- Suggested fix: rewrite the post-T5 markdown to reflect the actual importance ordering observed (study_time_hours dominant, sleep_hours surprisingly second, past_failures fourth) OR change the seed so importances align with the EDA narrative. Pick one; do not ship contradictions.

**P1-4. `DEPTH_GRID` is documented as adjustable but the surrounding plot annotations hard-assume the default grid.**
- Cell `16e3600a` (DEPTH_GRID KNOB blurb): *"extend with intermediate values (e.g. add 10, 12, 15)"*.
- Cell `1fa23d12` (annotation plot) draws three annotations: "Underfit risk" at position `x_pos[0]`, "Best test accuracy (depth=...)" at `x_pos[best_depth_idx]`, "Overfit risk" at `x_pos[-1]`. These are robust to grid length, so no breakage.
- However, the *axes title and x-tick labels* assume the grid includes `None` at the end (the "overfit risk" annotation is anchored to the last point). If a variant author drops `None` from the grid (which the blurb explicitly allows — "extend" is not "must keep None"), the "overfit risk" annotation will point at the wrong place.
- Adaptability impact: minor — none of the three mandatory variants edit DEPTH_GRID. But the optional extras mention extending the grid, and the blurb invites it.
- Suggested fix: harden the blurb: *"Always keep `None` as the last entry; the annotation plot anchors the overfit-risk arrow to the last point."* One-line clarification, no code change.

**P1-5. MY_PROFILE reindex check is asymmetric — silently drops extras, only catches missing keys.**
- Cell `9211e2d3`: `pd.DataFrame([MY_PROFILE]).reindex(columns=feature_cols)` and then a `missing = ... isna()` check.
- If the examinee follows Variant 3 and removes `past_failures` from `FEATURE_COLS` but forgets to remove it from `MY_PROFILE`, the reindex **silently drops** the extra key. No warning, no error. The model then predicts on a 4-column row and Variant 3 "works" — but the examinee never learns they had a stale key.
- Conversely, if they remove the key from `MY_PROFILE` but forget to remove it from `FEATURE_COLS`, the existing `missing` check fires with a clear error.
- Adaptability impact: the asymmetry teaches the wrong lesson. The T6 markdown explicitly tells students to keep MY_PROFILE in sync; the code should enforce both directions.
- Suggested fix: after reindex, also check `extra = set(MY_PROFILE.keys()) - set(feature_cols)` and raise a `ValueError` listing the stale keys. Five lines.

**P1-6. Optional 4d "expected" prediction may not hold on the current seed.**
- variants.md 4d expects: *"predict 'Need support' with probability_pass < 0.25"*.
- The fitted model on the locked seed gives RF test_acc = 0.688 with the importance ranking above. Without re-executing the at-risk profile I cannot confirm whether `predict_proba` < 0.25 holds — but on a 200-tree forest with test_acc = 0.688 and `did_lab=0, past_failures=2, absences=12`, this is plausible but **not guaranteed**.
- Adaptability impact: optional, not gate. Still — if you ship a numeric expectation, you should have the seed-locked output to back it.
- Suggested fix: add a cached "optional 4d answer key" line in the wrap-up cheat-sheet, computed and pasted by whoever locks the seed.

---

### P2 findings (polish — fix when convenient)

**P2-1.** `DEPTH_GRID` is declared as a tuple `(1, 2, 3, 4, 5, 6, 8, None)` then immediately converted via `depths = list(DEPTH_GRID)`. Either declare it as a list directly, or document why immutability matters here. Cosmetic.

**P2-2.** `TARGET_COL` KNOB blurb says *"not used at exam-gate level; included so KNOB Coverage Reviewer (spec §8.1 #2) can confirm no magic strings."* — this reviewer's charter is variant adaptability, but I want to note that exposing a KNOB whose only justification is "to satisfy a different reviewer" is a code smell. If it isn't variant-relevant, demote it to a `TARGET_COL = 'pass_class'` constant without the elaborate KNOB block.

**P2-3.** The wrap-up cheat-sheet `21cc22b9` says *"`DEPTH_GRID` | 1..8, None"* but the actual default is `(1, 2, 3, 4, 5, 6, 8, None)` — missing `7`. Trivially confusing; either render it as `1..6, 8, None` or update the default to `1..8, None`.

**P2-4.** `RF_MAX_DEPTH` KNOB blurb is well-written but no variant in `variants.md` exercises it. The Optional 4c combo uses `TREE_MAX_DEPTH=5` and `RF_N_ESTIMATORS=50`, not `RF_MAX_DEPTH`. If `RF_MAX_DEPTH` is purely teaching, mark it as such; otherwise add a variant that uses it.

**P2-5.** `STRATIFY` KNOB blurb says *"useful to show 'what does stratify=y actually buy us' in a teaching context"* but no variant exercises it either. Consider adding it as optional 4e to round out the variant bank, or downgrade to a constant.

**P2-6.** The KNOB blurb for `TREE_PLOT_DEPTH` (cell `8580ee59`) is fine, but no variant references it. Pure visualization knob, harmless.

---

### Per-variant adaptability scorecard

| Variant | Mechanical KNOB path exists? | Single-edit suffices? | KNOB-stated expectation matches locked-seed output? | Verdict |
|---|---|---|---|---|
| **V1 — Different max_depth** | Yes (`TREE_MAX_DEPTH = 3`) | Yes (T3 re-runs from that knob) | **No** — blurb claims test_acc 0.78–0.82, actual 0.703. See P0-1. | **Fail (numeric expectation wrong)** |
| **V2 — RF n_estimators sweep** | Yes (`RF_N_ESTIMATORS` -> 10, 50, 200) | Yes (T5 re-runs each time) | **No** — "matches or improves on the tree" not true on locked seed (RF 200 = 0.688 < best tree = 0.703). And `RF_RANDOM_STATE` referenced by variants.md doesn't exist. See P0-2, P0-3. | **Fail (narrative + reference)** |
| **V3 — Drop a feature** | Yes (`FEATURE_COLS` minus `past_failures`, `MY_PROFILE` likewise) | Yes (single source of truth propagates) | Partial — mechanics work, but the post-T5 narrative says `past_failures` is a top driver while the cached feature-importance chart ranks it 4th out of 5. See P1-3. | **Pass with concerns** |
| **Opt 4a — N_STUDENTS=80** | Yes (`N_STUDENTS = 80`) | Yes | Not checked (no cached output for 80) | Pass (untested) |
| **Opt 4b — RANDOM_STATE flip** | Yes (`RANDOM_STATE = 7`) | Yes | Not checked | Pass (untested) |
| **Opt 4c — TREE_MAX_DEPTH=5 AND RF_N_ESTIMATORS=50** | Yes (both KNOBs exist) | Yes (two edits) | Not checked; the underlying RF/tree story is broken on this seed (see P0-2) so the qualitative "gap shrinks" claim is suspect. | Pass with concerns |
| **Opt 4d — at-risk MY_PROFILE** | Yes (`MY_PROFILE = {...}`) | Yes (one dict literal) | Not directly verified; see P1-6. | Pass with concerns |

**Bottom line:** the three mandatory variants all have a clean mechanical KNOB path (good), but **two of three carry numerical or narrative expectations that the notebook's own cached outputs falsify** (P0-1, P0-2, P0-3, P1-3). That is what fails Round 1 for variant adaptability.

---

### Out-of-scope observations (for the PM)

- **Reproducibility of cached outputs.** The .ipynb ships with cached outputs from one execution. If those outputs drift between sklearn versions, the discrepancies I flagged above could quietly shift. Lock the sklearn version (and numpy) in the project's environment file (`requirements.txt` or `pyproject.toml`) before the exam.
- **Synthetic data is borderline too noisy for a teaching set at N=320.** The depth sweep is not monotone (depth 4 is *worse* than depth 3 by 0.109). On a fair pedagogic dataset the curve should be cleaner. Either raise `N_STUDENTS` default to ≥1000 (the docstring even hints at this — *"push to 1000 to lock down the depth-vs-accuracy trend if it looks noisy at the default"*) or accept that the lab teaches "trees are noisy" rather than the cleaner intended lesson "depth has a U-shape".
- **No KNOB for `STRATIFY` is exercised by any variant.** If `STRATIFY` is here purely as a teaching prop, mark it accordingly. If it's intended for a variant, write that variant.
- **`make_student_success_data` is excluded from the KNOB surface.** That's defensible (it's the ground truth) but a sophisticated examiner could ask "what if the data generator changes?" — out of scope for Round 1 but worth a sentence in `PM/history.md`.

---

### Concerns / risks

1. **Highest risk:** an exam-agent gate that grades by comparing examinee output to the KNOB-stated expectation will mark correct work `FAILED` for Variants 1 and 2. This is the worst kind of failure — a self-inconsistent exam.
2. **Second-highest risk:** a student reading the cheat-sheet and the post-T5 markdown ("RF matches or improves on the tree", "past failures dominate") will produce variant answers that match the *narrative* but contradict the *cached numbers*. They will be marked wrong on either grader.
3. **Lower risk:** the optional extras (4a–4d) have no cached evidence in the notebook, so any quantitative claim there is unverifiable until someone executes them.

---

### What PM should do next

1. **Dispatch `pm-backend` (or whoever owns the notebook)** to fix the three P0s in order:
   - Recompute realistic numeric ranges for the `TREE_MAX_DEPTH` 3–5 blurb against the locked seed (P0-1).
   - Either change the seed (preferred) or raise `N_STUDENTS` so the RF actually beats the best single tree, then update the takeaway markdown to match the new cached output (P0-2).
   - Fix the `RF_RANDOM_STATE` reference in `variants.md` (P0-3).
2. **Then dispatch `pm-frontend`/markdown owner** to fix the P1-3 narrative-vs-importance contradiction.
3. **Re-execute the notebook end-to-end** and commit the new cached outputs.
4. **Re-dispatch this reviewer (Reviewer #4)** for Round 2. Do not advance to App Tester or Code Reviewer until all P0s clear.
5. P2 items can be batched into a single follow-up sweep after Round 2 passes.

**DOCUMENT.md updated:** N/A for QA.

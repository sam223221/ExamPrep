# MLLab1-Classification — Reviewer #3 (Pedagogical Clarity), Round 1

**Reviewer role:** Lab Reviewer #3 — Pedagogical Clarity (incl. analogies). Harsh.
**Spec anchor:** First markdown cell of `lab1_classification_solution.ipynb` = the §6.2 header
(MENTAL MODEL / PROBLEM STATEMENT / REFERENCES / HOW TO ADAPT / OUTPUTS / ENTRY POINT). Cross-reference: **MENTAL MODEL ↔ L10**.
**Artifacts reviewed (absolute paths):**

- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab1_classification_solution.ipynb`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L10-Intro-to-ML.md`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\MLLab1-Classification\variants.md` (variant gate)

**Verdict at a glance:** **Fail.** The MENTAL MODEL header is well-written and the analogy
(*"20 questions"* and *"many slightly-different experts taking a majority vote"*) is the same one
L10 uses in §2 and §4.9 — that part is good. **But the actual numerical output of the executed
solution flatly contradicts every pedagogical promise the prose makes.** A student who runs this
notebook end-to-end and reads the surrounding markdown will conclude that the lecture's three
headline lessons (overfit-deep-trees, sweet-spot-medium-depth, forest-beats-tree) are *not*
demonstrated by the supplied data, and yet the markdown insists they are. This is the worst
pedagogical failure mode: the *vocabulary* matches the lecture but the *evidence printed on the
page* refutes it, and the prose pretends the evidence is fine.

---

## P0 findings (the printed evidence contradicts the lesson)

### P0-1. The "Random Forest beats the single tree" claim is **false on the default run**, but every markdown cell that mentions it assumes it is true

**Locations:**
- `lab1_classification_solution.ipynb` cell `244d378d` (T5 trainer) — prints
  `Random Forest test acc = 0.688`, `Single-tree acc = 0.594`, `Gain = +0.094` — that comparison is
  **rigged against the wrong baseline**.
- The T4 depth sweep (cell `16e3600a`, printed) shows the **best single tree (`max_depth=3`) reaches
  test acc = 0.703**, i.e. **higher than the random forest's 0.688**.
- T6 wrap-up markdown (cell `011fa6f4`) — "The Random Forest usually matches or improves on the
  single tree by averaging out individual-tree mistakes."
- T5 intro markdown (cell `653e7ce8`) — "**A stronger team of trees**".
- T5 approach markdown (cell `db77d59c`) — frames the experiment as "compare its test accuracy with
  the single-tree baseline `tree_acc`".

**Pedagogical damage.** A careful student reads the depth-sweep table, notices that
`max_depth=3` already gives 0.703 test accuracy, then reads the next section that calls the
forest "stronger" and claims a `+0.094` gain — and immediately sees the cheat: the gain is
measured against the **unbounded overfit tree** (0.594), not against the **best** single tree
(0.703). The honest report would be "Random Forest 0.688 is **worse than the best regularised
single tree** (depth-3, 0.703) on this seed/sample." The lecture (L10 §4.9) does not promise the
forest will always beat the best single tree; it promises **variance reduction**. The notebook
collapses that nuance into a triumphal headline that the numbers do not support.

**Suggested fix.** Pick one:
(a) In T5, baseline the forest against `max(test_accs)` from the T4 sweep, not against the
unbounded T3 tree, and report the (possibly negative) gap honestly. Then add a sentence:
"on this small synthetic dataset the forest's variance reduction does not beat a well-tuned
single tree — the lecture's *general* statement is about variance, not a guarantee."
(b) Change `RANDOM_STATE` or `N_STUDENTS` until the default run actually shows the lesson.
(a) is the honest pedagogical fix; (b) is the cheap one.

---

### P0-2. The depth sweep does **not** show the U-shape the lecture (L10 §6.1 Fig 17) promises — but the annotated plot pretends it does

**Locations:**
- T4 sweep table (cell `16e3600a` output):
  ```
  max_depth  train_acc  test_acc   gap  leaves
          1      0.695     0.641 0.055       2
          2      0.695     0.641 0.055       4
          3      0.738     0.703 0.035       8
          4      0.781     0.594 0.188      15
          5      0.805     0.656 0.148      24
          6      0.867     0.625 0.242      35
          8      0.938     0.656 0.281      54
       None      1.000     0.594 0.406      71
  ```
- T4 plot (cell `1fa23d12`) — annotates "Underfit risk" at depth 1, "Best test accuracy (depth=3)",
  and "Overfit risk" at depth `None`.
- T4 wrap-up markdown (cell `43ee40e5`): "Shallow trees miss useful structure and **underfit**.";
  "A middle depth (typically 3–5 on this dataset) gives the best balance"; "Deep trees drive
  training accuracy very high while test accuracy stops improving — the **overfit** regime."

**Why this is broken pedagogy.**
1. The **depth-1 underfit story is false**: depth-1 has *higher* test accuracy (0.641) than depth-4
   (0.594), depth-6 (0.625) and depth-`None` (0.594). The "Underfit risk" arrow points at the
   second-best test point in the whole table. A student who computes "which arrow corresponds to a
   worse model?" answers "depth=None or depth=4", not "depth=1".
2. The **U-shape is non-monotone garbage**: test accuracy jumps 0.641 → 0.641 → 0.703 → **0.594** →
   0.656 → 0.625 → 0.656 → 0.594. That is not a U; that is noise. L10 Fig 17 (slide 56) shows a
   smooth U; this plot does not. A student staring at the chapter's clean U-curve and then at this
   notebook's saw-tooth will assume one of the two is lying.
3. The **5–6 depth range is supposed to be "the best balance" per the markdown**, but the printed
   numbers say depth-3 wins and the depth-4 result is actually the *worst* in the table (tied with
   `None`). The annotation in the markdown ("typically 3–5") is true for the population average
   over seeds; on the *one seed the notebook prints*, the claim is wrong for depths 4 and 5.

**Pedagogical damage — severe.** This is exactly the lecture's `L10 §6.5` exam-trap bullet
"Confusing train and test error". The notebook's job is to make the U visible. With `N_STUDENTS=320`
and `RANDOM_STATE=42` the U is invisible because the test set has only 64 rows, so accuracy is
quantised in steps of `1/64 ≈ 0.0156` and one record's label swing dominates the depth signal. The
solution should either (a) raise `N_STUDENTS` until the U emerges, (b) average over multiple seeds
in the sweep and plot mean ± std, or (c) honestly relabel the section "the U-shape is real but
hard to see at this sample size — here is what the curve looks like averaged over 30 seeds".

**Suggested fix.** Add a KNOB `DEPTH_SWEEP_SEEDS = 30` (or similar) and average the train/test
accuracies across seeds before plotting. The current single-seed plot is *anti-pedagogical*: it
teaches the student to ignore evidence and trust the prose.

---

### P0-3. The MENTAL MODEL header promises the §6.2 cross-reference is to **L10 §§ 2–4**, but the actual mapping to L10 §6 (overfitting) is the part the notebook fails to demonstrate

**Location:** First markdown cell `b3f400ae`, "REFERENCES" block — "Lecture L10 §§ 2–4 for the
supervised-learning framing, train/test split, decision trees, **and overfitting diagnosis**."

**Why this is wrong.** L10 §6 is the overfitting chapter, not §§ 2–4. §2 has the *analogies*, §3
has the framing, §4 has the algorithms. The notebook's own T4 cell explicitly demonstrates
overfitting; the prompt's "MENTAL MODEL ↔ L10" anchor is **§6.2** ("Two distinct causes of
overfitting"), not §§ 2–4. So the reference is off by three sections from the very chapter the
prompt nominates. A student following the breadcrumb to "study L10 §§ 2–4 to understand T4" will
land in the algorithms section and find no discussion of overfit / underfit at all.

**Suggested fix.** Change "§§ 2–4" to "§§ 2 (analogies), 3.1 + 3.3 (framing), 4.5 + 4.8 (tree
induction + stopping criteria), **6 (overfitting diagnosis)**, and 4.9 (random forests)". Five
section pointers, one per task. The current single-range pointer is misleading.

---

### P0-4. The MENTAL MODEL analogy in the header is L10's, but the rendered §5 markdown silently swaps to a different (weaker) gloss

**Locations:**
- Cell `b3f400ae` (MENTAL MODEL): "A decision tree is 20 questions; a random forest is asking many
  slightly-different experts and taking a majority vote." — matches L10 §2.
- Cell `653e7ce8` (Section 5 intro): "A random forest trains many trees, each on a bootstrap sample
  of the rows and a random subset of the features at each split, and lets them vote. The expert
  analogy: **many slightly-different experts, majority vote**."

**Problem.** The header analogy is *experts*, then the section intro restates *experts* — but
between them, cell `5f285abc` (post-T3 commentary) abandons the analogy entirely and switches to
"The root split is the feature the tree trusts most." That phrase replaces L10's "20 questions"
mental model with an anthropomorphic "trust" mental model that the lecture does not use. L10 §2
explicitly says decision trees are *greedy* — "at each step it picks the locally-best split, never
looking ahead" — not "the tree trusts a feature". A student exposed to both phrasings has to
reconcile two different models of *what a tree node is*. The lecture never uses "trust"; the
notebook should not either.

**Suggested fix.** Replace "The root split is the feature the tree trusts most" with "The root
split is the feature that maximally reduces impurity at the top — the first 'question' in the
20-questions analogy". Keep one analogy throughout.

---

### P0-5. The Random Forest at `random_state=42, N_STUDENTS=320` returns **0.99 pass probability** for the default `MY_PROFILE` — and the markdown after T6 ignores that this is *implausibly* certain

**Locations:**
- Cell `9211e2d3` output: `Pass probability: 0.990`, `Need-support prob: 0.010`.
- Cell `61408de9` wrap-up markdown: "the prediction is not destiny", "a model trained on synthetic
  data is useful for **learning concepts**, not for making real academic decisions" — true but
  toothless. The actual issue is that the model is **0.990 confident** on a feature vector that
  sits comfortably inside the training distribution, despite the forest's headline test accuracy
  being only **0.688**.

**Why this matters pedagogically.** A model with 68.8% accuracy assigning 99.0% probability to a
single input is a textbook *calibration failure*. L10 does not formally cover calibration, but
this is exactly the moment to plant the seed — "the forest's vote share is not the same thing as
a calibrated probability". Instead, the notebook prints the number with three decimal places and
calls it a day. A student will internalise "high probability = correct" and walk away with a
false sense of security in tree-ensemble outputs.

The lecture (L10 §6.5) is explicit about this kind of trap: "Treating one probability as truth
instead of asking what data generated the model and whether the features are even realistic." The
notebook's own wrap-up bullet uses similar words but does not connect them to the **0.990** that
just printed three lines above.

**Suggested fix.** Either (a) explicitly call out that 99% is the vote share of 200 trees, not a
calibrated posterior — "if 198 of 200 trees vote Pass, `predict_proba` returns 0.99, but
test accuracy is only 0.69, so the *certainty* is overstated"; or (b) demonstrate a calibration
diagnostic (e.g. compare `predict_proba` distribution on the test set to actual outcomes) in a
small extra cell. Right now the notebook ships a 0.99 prediction and a "the prediction is not
destiny" disclaimer that does not name the actual failure.

---

## P1 findings (important pedagogical issues)

### P1-1. KNOB blocks make claims that the executed output contradicts

**Locations:**
- `TREE_MAX_DEPTH` KNOB comment (cell `25e63d02`):
  > "3-5 -> usually the BEST balance on this dataset (test acc ~0.78-0.82; small train-test gap)."

  The actual depth-3 test accuracy printed is **0.703**, not "~0.78-0.82". Depth-5 is **0.656**.
  Neither value is in the promised range. The KNOB block is the **only thing a variant-gate
  examinee is allowed to read** (per `study/_exam/MLLab1-Classification/variants.md` lines 7–15) —
  if the KNOB lies about the expected range, the examinee cannot self-check.

- `RF_N_ESTIMATORS` KNOB (cell `244d378d`):
  > "10 -> noticeably noisier accuracy; the forest is small enough that one bad bootstrap sample
  > can dominate."

  This is testable. With `RF_N_ESTIMATORS=10` and `random_state=42` the forest on this exact split
  may well land at 0.66 or 0.72; the KNOB does not give a numerical band the way `TREE_MAX_DEPTH`
  does. Either commit to ranges for both or for neither — inconsistent KNOB documentation reads
  as "we tested some and not others".

- `TREE_MAX_DEPTH` KNOB:
  > "None -> grows until every leaf is pure or has 1 sample. Typically depth 10-15 on this dataset.
  > Overfit-prone."

  Actual depth grown at `None`: **13**. OK, this one is honest.

**Pedagogical damage.** Variant 1 (depth sensitivity) asks the examinee to "set `max_depth = 3`,
report train, test, gap, one sentence". The KNOB tells them to expect test ~0.78–0.82. They run
it, see 0.703, and either (a) suspect their environment is wrong, or (b) realise the KNOB is
ghost-typed and stop trusting any KNOB comment. Both outcomes are bad for the variant gate.

**Suggested fix.** Either run the solution end-to-end first, then update the KNOB ranges to
match the actual realised numbers (preserving the *qualitative* claim "depth-3 is near the best
balance"), or weaken the ranges to "expect 0.65–0.80 depending on seed/sample size; the *gap*
should shrink, that is the headline".

---

### P1-2. The MENTAL MODEL block's "20 questions" analogy is correctly aligned with L10 §2, but the analogy's *failure mode* from L10 is not transferred to the notebook

L10 §2.6 ends the 20-questions analogy with "*Where it breaks down:* a vanilla decision tree is
*greedy*: at each step it picks the locally-best split, never looking ahead. That is why two
different decision trees can fit the same data (slide 23) and why post-pruning exists."

The notebook's MENTAL MODEL header gives the analogy but omits the breaks-down note. So a student
reading the notebook alone learns "decision tree = 20 questions" without learning *why the analogy
fails* — which is the half that motivates the entire `max_depth` sweep in T4. The notebook then
*shows* the consequence of greediness (the unbounded tree at depth 13 overfits to test acc 0.594)
without ever connecting that observation back to "greedy ≠ optimal".

**Suggested fix.** Add one paragraph after the analogy in the MENTAL MODEL block:
> *Where the analogy breaks down:* a human playing 20 questions is **strategic** — they pick the
> next question to halve the remaining possibilities. A decision tree is **greedy** — it picks the
> locally-best split with no look-ahead, which is exactly why an unbounded tree memorises the
> training data and why T4 sweeps `max_depth` instead of trusting "fully grown".

---

### P1-3. The "20 questions" / "many doctors voting" pair in L10 §2 is presented as analogies #6 and #7; the notebook header presents only #6 and #7 and skips #8 (overfitting = "memorising past papers")

The handout's MENTAL MODEL block is one line about trees + one line about forests. L10 §2.8 has a
dedicated analogy for overfitting ("a student who memorises every past-paper answer scores 100% on
those exact papers and fails the moment the question is rephrased"). The whole purpose of T4 is to
**demonstrate** that analogy. The notebook never names it.

**Pedagogical damage.** The student reaches T4, sees a noisy curve (P0-2), reads "deep trees drive
training accuracy very high while test accuracy stops improving — the **overfit** regime", and has
no mnemonic to hook the abstract "overfit" word onto. The lecture's "memorising past papers"
analogy is a one-line mnemonic that would solve this. It is missing.

**Suggested fix.** Add to the MENTAL MODEL header:
> **Overfitting = memorising past papers.** A tree grown to depth 13 with 71 leaves on 256
> training rows has effectively memorised a verdict per ~3.6 students. T4 makes this concrete:
> the unbounded tree hits 100% train accuracy and ~59% test accuracy. That gap is the model
> failing the exam it studied for.

---

### P1-4. The HOW TO ADAPT block's "Variant 1" advice contradicts the printed numbers (followup to P1-1)

The MENTAL MODEL header's HOW TO ADAPT section says:
> "Variant 1 — Different `max_depth`. Set `TREE_MAX_DEPTH = 3` (instead of `None`). Re-run T3
> (which honours `TREE_MAX_DEPTH`); the T4 sweep already covers many depths."

This is fine procedurally, but it omits the punchline. The variants doc (line 58–60) wants
"two concrete accuracy numbers, the signed gap, and a one-sentence 'shallower trees generalise
better because they cannot memorise individual training rows' answer." The notebook's header
should preview the *expected qualitative result* — "expect train acc to drop from 1.000 to ~0.74,
test acc to rise from 0.594 to ~0.70, gap to fall from +0.406 to ~+0.04". Without that anchor, an
examinee who lands on the locked solution and reads only the header has no way to know whether
their post-edit numbers are sensible.

**Suggested fix.** Append one bullet under Variant 1:
> "Expect, on the default seed: train acc ≈ 0.74, test acc ≈ 0.70, gap ≈ +0.04 (vs unbounded's
> train=1.000, test=0.594, gap=+0.406). The gap is the headline."

Do the same for Variants 2 and 3.

---

### P1-5. The "MENTAL MODEL ↔ L10" anchoring is asymmetric — the notebook references the lecture, but the lecture does **not** point back to the lab

L10 §7 "Connections to Other Lectures" mentions ML Lab 1 in passing:
> "used directly in **ML Lab 1 — Classification** (`lab1_classification_handout.ipynb`)"

But the back-reference is to the **handout**, not the **solution**. A student studying L10 cold
who wants to see the lecture applied has nowhere to go — the handout has `raise
NotImplementedError`s; the solution is the place to read the worked code. The lecture should
explicitly say "after reading §6 (overfitting) and §4.9 (random forests), the worked
end-to-end example is `lab1_classification_solution.ipynb` cells T3–T5".

**Pedagogical damage.** The lab and lecture sit in disjoint reading paths. L10's §7 mentions
the lab as an *application* but the lab's MENTAL MODEL header points to L10 §§ 2–4, missing §6
(P0-3) — so the bidirectional pointer chain is broken on both sides.

**Suggested fix.** This is an L10 fix, not a notebook fix. Reviewer #3 flags it; the engineer
should patch L10's §7 Lab handoff to add a section-by-section map.

---

### P1-6. Mid-T1 commentary cell (`188b711f`) is the only place that gives the EDA pedagogy, but the bullets are weak

Current text:
> "Students who study more and miss fewer classes tend to sit closer to the 'Pass' region."
> "Past failures are a strong warning sign, but they are not the whole story by themselves."
> "`did_lab` helps, but it does not magically override every other feature."

These are correct but **anti-pedagogical** — they tell the student what to see, instead of asking
them to see it. The whole EDA panel just rendered three plots (count, scatter, heatmap); the
commentary should be "for each plot, what is the one observation a student should make and what
is the one observation that would be a misread?". Right now the cell reads as a flat summary.

**Pedagogical damage.** The EDA section is supposed to motivate feature engineering and impurity
measures (which features will the tree split on first?). Without an explicit "predict the root
split from the heatmap" exercise, the student does not exercise the L10 §4.4 impurity intuition
before T3 prints the answer.

**Suggested fix.** Restructure as:
> **From the count plot:** is the class distribution close enough to 50/50 that accuracy is a
> reasonable metric? (Yes, ~52/48.)
>
> **From the scatter plot:** can you spot a single linear boundary that separates Pass from Need
> Support? (No — there is significant overlap; that is why the tree's *staircase* boundary will
> outperform a single threshold.)
>
> **From the heatmap:** which feature has the largest absolute correlation with `pass_class`? Use
> that as your **prediction** for the root split of the tree T3 will fit. (Answer revealed in T3.)

---

### P1-7. The "What this does *not* mean" markdown blocks are pedagogically valuable but inconsistent — three sections have them, three do not

Present (good):
- After T3 (cell `5f285abc`): "**What to look for in the next tree plot**" — but no
  "what this does *not* mean".
- After T4 (cell `43ee40e5`): "**What this does *not* mean** — The deepest tree is not
  automatically 'best'..." — good.
- After T5 (cell `011fa6f4`): "**Common beginner mistake** — Assuming the forest is 'better' in
  every way." — good.
- After T6 (cell `61408de9`): "**What this does *not* mean**" and "**Common beginner mistake**" —
  both present. Good.

Absent (bad):
- After T1 EDA (cell `188b711f`): has "Common beginner mistake" but **no** "What this does *not*
  mean".
- After T3 (cell `5f285abc`): has "What you should notice" but **no** "What this does *not* mean".
- T2 (the split): **no commentary cell at all** after the printed table. The lecture (L10 §3.3)
  treats train/test split as the conceptual hinge of supervised learning — the lab gives it one
  KNOB and one print, no reflection.

**Pedagogical damage.** Asymmetric scaffolding teaches the student "these tasks have caveats, those
do not", which is false. T2 is exactly where the misconception "accuracy on the training set tells
me how well my model works" lives (L10 §6.5 first bullet).

**Suggested fix.** Add a small commentary cell after T2 along the lines of:
> **What this does *not* mean.** The train/test split is not a guarantee that test accuracy
> reflects deployment accuracy. It only guarantees that **the model has not seen these specific
> rows** during fit. If your training and test data both come from a synthetic generator (as here),
> they share the *same* distribution; on real data they often do not, and accuracy on a held-out
> split can still be optimistic.

Add a "what this does *not* mean" to the EDA and T3 commentary too, for symmetry.

---

### P1-8. The "Wrap-Up Cheat Sheet" KNOB table at the bottom is the right idea but does not surface the **expected outputs** for the variants

Cell `21cc22b9` has a nice KNOB-recap table. But there is no companion table that says
"if you set `TREE_MAX_DEPTH=3`, expect these numbers" — i.e. the cheat-sheet for variant gating
is missing.

**Pedagogical damage.** The variant gate (per `variants.md`) expects an examinee to *self-grade*
("did I get the right answer?"). The notebook does not give them a target. L10's §8 cheat sheet
includes recall hooks for every analogy; the lab's cheat sheet recalls every KNOB but no
expected metric.

**Suggested fix.** Add a second table or a follow-up cell:
> **Expected numbers for the gate variants (random_state=42, N_STUDENTS=320):**
>
> | Variant | KNOB change | Train acc | Test acc | Gap |
> |---|---|---|---|---|
> | Default (T3) | none | 1.000 | 0.594 | +0.406 |
> | V1 depth=3 | `TREE_MAX_DEPTH=3` | ≈ 0.738 | ≈ 0.703 | ≈ +0.035 |
> | V2 RF=10 | `RF_N_ESTIMATORS=10` | n/a | ≈ 0.65–0.70 | n/a |
> | V2 RF=50 | `RF_N_ESTIMATORS=50` | n/a | ≈ 0.68–0.71 | n/a |
> | V3 drop past_failures | `FEATURE_COLS=[...]` | depends | ≈ −0.03 to −0.05 vs full | — |

---

## P2 findings (polish, suggestions)

### P2-1. The MENTAL MODEL header's analogy text uses "majority vote" but L10 §4.9 calls it "majority-vote (classification)"

L10 §4.9 distinguishes regression (average) from classification (majority-vote). The notebook
silently picks the classification variant without noting why. One line — "we use **majority vote**
because this is classification; for regression we would average" — would close the loop with
L11 (Regression) where the same ensemble idea reappears with averaging.

---

### P2-2. The `make_student_success_data` generator's coefficients are documented as "not KNOBs" but the docstring buries the *direction* each coefficient should be

> "0.47 * study_time, -1.15 * failures, ..."

A student reading the generator code can extract the signs but the docstring does not say
"positive coefficients raise pass probability; negative coefficients lower it." This is the
underlying *ground truth* the classifiers must learn — explicitly listing it in the docstring would
let the student check feature importance (T5) against the *true* feature ranking. The lecture
(L10 §3.2) describes a supervised model as "an equation relating input to output" — the generator
*is* that equation, and the lab should expose it.

**Suggested fix.** After the function body, add a small comment:
> "Ground-truth ranking (by absolute coefficient): past_failures (−1.15) > did_lab (+1.05) >
> study_time_hours (+0.47) > sleep_hours (curvature −0.30) > absences (−0.08). A correctly-fit
> tree or forest should put these in roughly this order in its feature_importances_ chart."

The current default RF feature ranking is:
```
study_time_hours    0.394
sleep_hours         0.257
absences            0.151
past_failures       0.118
did_lab             0.080
```

— which is **roughly inverted** from the generator's coefficient ranking (past_failures and
did_lab are the two largest absolute coefficients but rank 4th and 5th in importance). That is a
genuinely interesting pedagogical artifact (impurity-based importance ≠ effect-size importance),
and the lab is silent on it.

---

### P2-3. The T1 EDA plot at cell `8d0f8e1e` is gorgeous but mixes two palettes within five lines of code

`palette = {'Pass': COLORS['orange'], 'Need support': COLORS['teal']}` for the failure-rate bar
and violin, then `cmap='crest'` for the heatmap (which uses a teal-gradient ramp). The visual story
is "orange = pass, teal = need support" everywhere except the heatmap, where teal-gradient is
strength-of-correlation. A student tracking colour as a signal will be briefly confused. Minor.

---

### P2-4. The T3 classification report uses `target_names=['Need support', 'Pass']` but the confusion matrix uses index labels `['Actual: Need support', 'Actual: Pass']`

Two different label formats for the same two classes within five lines of output. Pick one.

---

### P2-5. The reference list in the MENTAL MODEL block points to "study/_shared/cross-references.md" but does not name a specific anchor

L10 has its own §7 with explicit anchors. The notebook reference is "see L10 ↔ L11 ↔ L12 ML
cluster" — a vague pointer. Reviewer #3 prefers either an exact section name ("see L10 §7 Lab
handoff") or no pointer at all. Vague-but-confident references degrade trust in the rest of the
references.

---

### P2-6. The cell `5c8caa04` (T6 approach) mentions `predict_proba(...)[:, 1]` "for the probability of the *positive* (pass) class" — but does not explain *why* column 1

L10 §3.3 defines class probabilities, but never says "the probability of class 1 is at index 1 of
the predict_proba output because sklearn orders classes by `np.sort(np.unique(y))`". This is a
common sklearn footgun (especially if labels are strings). One line would close the gap.

---

### P2-7. The wrap-up cheat sheet table does not align with the lecture's §8 cheat sheet structure

L10 §8 is a one-page recap structured around analogies. The lab's cheat sheet is structured around
KNOBs. Both are valid, but a student studying L10's cheat sheet and then the lab's cheat sheet has
to switch mental models. Aligning the lab's wrap-up to also include the lecture's analogies (one
italic per row) would close the loop. Optional.

---

### P2-8. The phrase "exam-relevant intuition" appears once (cell `bde53242`) but the notebook does not link to the exam variants file

That cell calls T4 "the heart of the exam-relevant intuition". An examinee reading this with the
gate in mind would benefit from an explicit pointer:
> "exam-relevant intuition — see `study/_exam/MLLab1-Classification/variants.md` for the three
> gate questions you should be able to answer after T4 and T5."

---

### P2-9. The `MY_PROFILE` default values are described as "mid-engagement student likely to pass" — but the result is **99% Pass**, which is not "likely", it's "near-certain"

Cell `9211e2d3` calls the default profile "mid-engagement student likely to pass". 99.0% is
*not* "likely"; it is "near-certain". Either describe the profile as "high-engagement, easy case"
or change the values to actually be borderline (e.g. study=5.5, absences=4) so the student sees
a more interesting probability and the "the prediction is not destiny" lesson lands.

---

## Lecture-alignment audit (does the lab teach what L10 §2–§6 promise?)

| L10 concept | L10 section | Notebook coverage | Verdict |
|---|---|---|---|
| Supervised learning framing (input → output) | §3.2 | T1 sets up `X`, `y` cleanly | OK |
| Classification, formally | §3.3 | T1 + T2 | OK |
| Train/test split + stratification | §3.3 | T2 with `STRATIFY` KNOB | OK |
| Decision tree as "20 questions" analogy | §2.6 | MENTAL MODEL header cites it | OK (but P0-4 swaps analogy mid-stream) |
| Hunt's algorithm / impurity | §4.2–§4.5 | Implicit (sklearn does it) — never named | Missed teaching opportunity, see P1-6 |
| `max_depth` as pre-pruning knob | §4.8 + §6.3 | T3 + T4 + KNOB `TREE_MAX_DEPTH` | OK procedurally, **BROKEN** evidentially (P0-2) |
| Underfitting vs overfitting U-curve | §6.1 (Fig 17) | T4 plot annotates U | **BROKEN** — evidence does not show a U (P0-2) |
| Two causes of overfitting (noise + insufficient examples) | §6.2 | Not addressed | Missing — could be a one-line comment after T4 |
| Pre-pruning hyperparameters (max_depth, min_samples_leaf, min_samples_split) | §6.3 | Only `max_depth` exposed | Acceptable for scope; mention the others in a comment |
| Bagging + random subspace = random forest | §4.9 | T5 + analogy in header | OK (analogy) but **BROKEN** evidentially (P0-1) |
| Forest as variance-reducer (not always more accurate than the best regularised tree) | §4.9 implicit | T5 markdown says forest "improves on the single tree" | **WRONG** on this seed (P0-1) |
| Feature importance | §4.9 background | T5 prints + plots | OK procedurally, but inverted vs ground-truth coefficient ranking (P2-2) — interesting, never named |
| Calibration of probability outputs | not in L10 | T6 emits 0.99 | Missed teaching opportunity (P0-5) |
| Common exam mistakes (train vs test confusion) | §6.5 | T4 wrap-up implicitly addresses | OK |
| Memorising-past-papers analogy for overfitting | §2.8 | **Missing from the header** | Missing (P1-3) |

**Net verdict.** The lab *names* the L10 vocabulary but the *executed numerical output* fails to
demonstrate three of the lecture's five headline lessons (overfit U-curve, "deep trees overfit",
"forest beats tree"). The prose pretends the demonstrations are clean; they are not. This is the
specific pedagogical failure mode the harsh-reviewer brief calls out: the lesson is *named* but
not *shown*.

---

## Concerns / Risks

1. **The variant gate may pass for the wrong reason.** An examinee who runs Variant 1 will get
   train≈0.74, test≈0.70, gap≈0.04 — but the KNOB block (P1-1) tells them to expect test ≈ 0.78.
   They will record their answer with a 0.07 discrepancy and either lose confidence or write a
   defence ("my seed was different") that the locked solution does not reward. The gate's
   self-grading rubric is opaque to the examinee.
2. **The default printed numbers undermine the lecture.** A diligent student does what every good
   student does — they actually *read* the numerical output. The numerical output of this notebook
   says "the unbounded tree is no worse than the depth-3 tree", "the forest is worse than the
   depth-3 tree", and "depth=1 is a perfectly fine model". Every one of those conclusions
   contradicts the lecture, and the lab does not reconcile.
3. **The "MENTAL MODEL ↔ L10" cross-reference is broken in both directions** (P0-3 + P1-5). A
   student following the breadcrumb from the notebook header to L10 §§ 2–4 will not find
   overfitting; a student following the breadcrumb from L10 §7 to the lab will land in the
   handout, not the solution. Bidirectional pointer hygiene is a Round-1 must-fix.
4. **No DOCUMENT.md presence anywhere.** I cannot verify whether this notebook was the last
   touchpoint, whether the engineer left a working set of "expected outputs", or whether a future
   engineer should regenerate the depth-sweep. Reviewer #3 cannot verify directory documentation
   from a single notebook, but the absence is worth a P1 flag from another reviewer.
5. **The reviewer brief said "MENTAL MODEL ↔ L10".** I read that as L10 §2 (analogies) and §6
   (overfitting). The lab cites §§ 2–4. The mismatch suggests the engineer working the MENTAL
   MODEL header did not actually open L10 §6 — and §6 is exactly where the lab's T4 task lives.
   Round 2 should require the engineer to re-walk the MENTAL MODEL block with L10 open at §6.

---

## What PM should do next

1. **Fix the four P0 evidence-contradicts-prose items first** (P0-1 through P0-4). These are not
   wording fixes — P0-1 and P0-2 require either averaging across seeds or re-baselining the forest
   vs the best single tree. The engineer should re-run the notebook end-to-end after each change
   and confirm the printed numbers now support the surrounding prose.
2. **Then fix P0-5** (calibration framing on the 0.99 prediction) and **P1-1 through P1-4** (KNOB
   ranges, "where the analogy breaks down" missing, missing overfitting analogy, missing variant
   targets).
3. **Then re-dispatch Reviewer #3.** The lecture-alignment audit table above is the rubric: every
   `BROKEN` row must move to `OK` before this lab is fit to ship to the variant gate.
4. **Do not proceed to App Tester** until P0-2 is fixed — a tester walking the depth-sweep will
   see the saw-tooth and either flag it or (worse) not flag it. Either way Reviewer #3 has done
   the work for them.
5. **Out of band:** L10 §7 should be patched to point at the *solution* notebook (not the handout)
   and to map specific tasks to specific L10 sections (P1-5). Recommend dispatching the L10
   chapter author in parallel with the lab engineer.

---

## Report to PM

**Assignment recap:** MLLab1-Classification, Round 1, Reviewer #3 — Pedagogical Clarity incl.
MENTAL MODEL ↔ L10 alignment. Source notebook (29 cells, executed end-to-end), L10 chapter
(742 lines), and variants gate (147 lines) all read fully. Reviewed against the §6.2 header
(first markdown cell) as the spec anchor.

**Status:** **Fail.** The lab's vocabulary is L10-aligned; the lab's *evidence* is not.

**P0 findings:**
1. `lab1_classification_solution.ipynb` cell `244d378d` + cell `011fa6f4` markdown — "Random Forest
   beats single tree" claim is false on the default run. Forest (0.688) < best single tree (0.703).
   The reported `+0.094` gain is rigged against the unbounded overfit tree, not the best
   regularised tree. **Suggested fix:** re-baseline forest vs `max(test_accs)` from T4 sweep.
2. `lab1_classification_solution.ipynb` cell `16e3600a` + `1fa23d12` + `43ee40e5` — Depth sweep
   does not show a U-shape; depth-1 ties with depth-3 on test accuracy; depth-4 is the *worst* in
   the table. The annotated plot pretends a clean U exists. **Suggested fix:** add
   `DEPTH_SWEEP_SEEDS` KNOB and average across seeds before plotting.
3. `lab1_classification_solution.ipynb` cell `b3f400ae` REFERENCES block — points to L10 §§ 2–4 for
   "overfitting diagnosis", but L10's overfitting chapter is **§6**. Off by three sections.
   **Suggested fix:** rewrite as "L10 §§ 2 (analogies), 3 (framing), 4.5 + 4.8 (induction +
   stopping), 4.9 (forests), **6 (overfitting)**".
4. `lab1_classification_solution.ipynb` cell `5f285abc` — "the tree trusts a feature" replaces
   L10's "20 questions / greedy" mental model with an anthropomorphic "trust" model the lecture
   never uses. **Suggested fix:** restate as "the root split is the question that most reduces
   impurity at the top".
5. `lab1_classification_solution.ipynb` cell `9211e2d3` output `0.990` + cell `61408de9` markdown
   — model with 68.8% test accuracy emits 99.0% probability for a single input. The wrap-up bullet
   "the prediction is not destiny" does not name calibration. **Suggested fix:** add a sentence
   distinguishing forest vote share from calibrated probability.

**P1 findings:**
1. `TREE_MAX_DEPTH` KNOB comment promises "test acc ~0.78-0.82" at depth 3-5; realised numbers are
   0.703 (depth-3), 0.594 (depth-4), 0.656 (depth-5). KNOBs are the only source the variant gate
   examinee may read — they must be accurate.
2. MENTAL MODEL header's "20 questions" analogy is missing L10 §2.6's *where it breaks down*
   ("greedy ≠ strategic") — the half that motivates T4.
3. MENTAL MODEL header omits L10 §2.8's overfitting analogy ("memorising past papers"). T4's whole
   point is to demonstrate that analogy; it never names it.
4. HOW TO ADAPT block's per-variant guidance does not preview the *expected qualitative result*
   (train/test/gap numbers). An examinee has no anchor for self-grading.
5. L10 §7 "Lab handoff" points at the handout, not the solution, and gives no section-by-section
   map. Bidirectional pointer chain is broken.
6. EDA commentary cell `188b711f` summarises plots instead of asking the student to predict
   features (root-split prediction exercise missing).
7. "What this does *not* mean" / "Common beginner mistake" blocks are present in 3 of 6 task
   sections; T2 has no commentary cell at all. Asymmetric scaffolding.
8. Wrap-up cheat sheet has KNOB recap but no *expected output recap* for the gate variants.

**P2 findings:** 9 items detailed in §"P2 findings" above — analogy direction, ground-truth
coefficient ranking vs feature importance, palette mixing, label-format inconsistency, vague
cross-reference anchors, `predict_proba[:, 1]` ordering footgun, cheat-sheet structural alignment
with L10 §8, exam-variants pointer, "mid-engagement" vs "near-certain" mislabel of the default
profile.

**QA Checklist (§7) status:** No project Feature Plan §7. Treating the reviewer brief's
"Pedagogical Clarity (MENTAL MODEL ↔ L10)" as the rubric:

| Criterion | Status | Note |
|---|---|---|
| MENTAL MODEL header present | Pass | Cell `b3f400ae` |
| MENTAL MODEL analogies match L10 §2 | Pass with concerns | "20 questions" and "many doctors" are quoted; "memorising past papers" missing (P1-3) |
| Each L10 §2 analogy's *where it breaks down* carried over | Fail | Notebook header has none of the break-down notes |
| Cross-reference to L10 sections accurate | **Fail** | P0-3, off by three sections |
| Cross-reference is bidirectional | Fail | P1-5, L10 §7 points to handout not solution |
| Executed numerical evidence supports the prose | **Fail** | P0-1, P0-2 |
| Per-task scaffolding (what to notice / what this does not mean) | Pass with concerns | Asymmetric, P1-7 |
| KNOB documentation is accurate | Fail | P1-1, ranges are off |
| Variant gate self-grading anchors present | Fail | P1-4, P1-8 |
| Probability outputs framed honestly | Fail | P0-5 |

**Acceptance criteria (§1) status:** N/A — no Feature Plan §1. Treating "the notebook teaches what
the prompt's MENTAL MODEL ↔ L10 anchor promises" as the implicit acceptance criterion:
**Not met.** The lab names L10's vocabulary but the executed evidence contradicts it.

**DOCUMENT.md audit:** N/A for Reviewer #3 — no project directories touched.

**Out-of-scope observations:**
- Reviewer #2 (correctness) should flag: the depth-4 result being the worst in the sweep (P0-2) is
  not just a pedagogy issue — it suggests `random_state=42, N_STUDENTS=320` is a pathological
  configuration. A robust fix is to bump `N_STUDENTS` until the sweep stabilises.
- L10 author should patch §7 Lab handoff (P1-5).
- Variants doc author should add expected-output anchors so the gate is self-graded (P1-4, P1-8).
- The `make_student_success_data` coefficients (P2-2) inverted-vs-feature-importance result is
  genuinely pedagogically interesting and should be promoted to a half-page sidebar somewhere.

**Concerns / risks:**
- The lab will likely *pass* the variant gate (because the gate checks "did the examinee edit the
  KNOB and run the notebook?", not "did the numbers match the KNOB's promised range?"). So the
  gate is a weak signal. The pedagogical failure is real and the gate will not catch it.
- The single-seed depth-sweep curve will be remembered by students; the lecture's clean U-curve
  will be remembered as theoretical. The notebook is teaching the wrong empirical lesson.
- Round 2 reviewer is at risk of receiving a "looks polished, prose reads well" version that
  Reviewer #1 (KNOB coverage) and Reviewer #2 (correctness) approve while Reviewer #3 fails.
  Do not let "three of four reviewers passed" obscure the headline issue.

**What PM should do next:** dispatch the lab engineer to fix P0-1 through P0-5 (estimated 1–2
hours: re-baselining T5 against `max(test_accs)`, adding `DEPTH_SWEEP_SEEDS` and averaging,
patching the L10 §§ 2–4 reference to include §6, replacing "trusts" with "asks about", and
naming the calibration gap on the 0.99 probability). Then fix P1-1 (KNOB ranges), P1-2 +
P1-3 (analogy break-down + memorising-past-papers), P1-4 + P1-8 (per-variant expected outputs),
and P1-6 + P1-7 (EDA exercises + symmetric scaffolding). Re-run Reviewer #3 against the
lecture-alignment audit table; every `BROKEN` row must move to `OK`. Do not proceed to App
Tester until P0-2 is fixed. In parallel, dispatch the L10 chapter author to patch §7 Lab
handoff (P1-5).

**DOCUMENT.md updated:** N/A for QA / Reviewer #3.

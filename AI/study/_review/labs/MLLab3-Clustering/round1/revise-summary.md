# MLLab3-Clustering — Round 1 Revise Summary

**Notebook:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab3_clustering_solution.ipynb`
**Variants:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\MLLab3-Clustering\variants.md`
**Reports addressed:** reviewer1.md, reviewer2.md, reviewer3.md, reviewer4.md

---

## P0 fixes applied

### Fix 1 — Scratch K-means convergence story (R1 P1-A, R4 P0)

**Cells touched:** `cell-t6-prep`, `cell-t6-solve`, `cell-t6-verify`, `section-t6-explain`.

- **`SCRATCH_ITERS` bumped 10 -> 20.** Lloyd's algorithm converges at iter ~14
  on this 2-feature data with `SCRATCH_SEED=0`; the old default stopped 4
  iterations early. New default gives a comfortable convergence margin.
- **Inertia bookkeeping moved AFTER the centroid update.** The recorded
  `inertia_history[-1]` now reflects the post-update centroids (the ones the
  next assign step will use), not the pre-update ones.
- **Inertia re-derived from updated centroids** rather than reused from the
  pre-update distance matrix, so the recorded value is internally consistent
  with `centroids_scratch` at loop exit.
- **`section-t6-explain` rewritten** to (a) drop the false "init-scheme" story
  ("the gap is because sklearn uses k-means++ ..."), (b) explain the gap was
  actually iteration count, (c) cross-reference L12 §4.1 ("K-means is local
  search in disguise") and L05's random-restart hill climbing analogy, (d)
  correctly attribute sklearn's algorithm to Elkan's accelerated variant.

**Result.** Scratch inertia at iter 20 = **168.886**, identical to sklearn's
168.886 (diff 0.000). The "matches sklearn within a couple of points" headline
is no longer needed — they now agree to the third decimal.

### Fix 2 — T6 K-knob ownership (R4 P0)

**Cells touched:** `cell-t6-prep`, `cell-t6-solve`, `cell-t6-verify`, the
`K_PRIMARY` KNOB docstring in `cell-global-knobs`, the `K_T1` docstring, the
HOW TO ADAPT §1 in `sol-header`.

T6 now uses **`K_T1`** (the 2-feature K knob) instead of `K_PRIMARY`, because
T6 operates on `X2_scaled` (the 2-feature data). Previously, Variant 1
(`K_PRIMARY=4`) produced a 2-feature K=4 scratch fit alongside a 2-feature K=3
T1 plot — internally inconsistent and unflagged.

Convention now stated explicitly: **T6 ↔ K_T1 (2-feature), T2/T5 ↔ K_PRIMARY
(6-feature)**. The `K_PRIMARY` docstring now spells out which cells it does and
does *not* drive. The `K_T1` docstring now mentions T6. The HOW TO ADAPT §1
rewritten in the same shape, and the false "elbow plot reads from K_PRIMARY"
claim removed.

### Fix 3 — K=2 vs K=3 reconciliation (R1 P1-B)

**New cell:** `section-t4-reconcile` (markdown, inserted after `cell-t4-plot`).

Explains the apparent contradiction between T4's `Recommended K = 2` and the
rest of the notebook's K=3 narrative, per L12 §6 pitfall #3 *"choosing K by
eyeballing"*. The reconciliation:

- Silhouette numerically prefers K=2 because the moderate-middle archetype
  blurs the boundary at K=3, costing the metric on inter-cluster separation.
- K=3 is justified by **external validity**: the T2 grade-spread of 9.33 grade
  points (62% of the Danish scale) is unambiguous evidence that three clusters
  recover real structure.
- L12 line: *"K is an input — pick it"*. Elbow and silhouette are
  practitioner heuristics, not verdicts. Right exam answer: *"K=3, defensible
  by elbow + external grade-spread; silhouette numerically prefers K=2
  because ..."* — not *"silhouette said K=2 so we use K=2."*

### Fix 4 — Variants V1 false claim about T4 (R4 P0, R2 P1)

**File touched:** `variants.md`.

Variant 1's KNOB checklist no longer claims `K_PRIMARY` affects the T4 elbow
read-out. Replaced with an explicit clarification that `recommended_k` is
silhouette-argmax over `K_GRID_T4` and is **independent of `K_PRIMARY`**. The
recommendation is to be used as a *control* in the K=4 comparison, not as a
consequence of the KNOB flip. Also added notes on (a) cluster naming falling
back to "study-hours tier N" when K_PRIMARY != 3, (b) cluster IDs not being
stable across K.

### Fix 5 — Variants V2 conflation of T3 and T4 (R4 P0)

**File touched:** `variants.md`.

Removed the misleading "T3 k=2/3/5 sweep elbow" phrasing. Replaced with a
clarification that:

- T3 is the side-by-side inertia/silhouette table on 2-feature data
  (`X2_scaled`); it does pick up FEATURE_PAIR_T1.
- T4 is the elbow + silhouette curves on **6-feature data** (`X6_scaled`);
  it does **not** pick up FEATURE_PAIR_T1. Plots, recommendation, and T2/T5
  are identical to the default run under Variant 2.

The stretch variant (`sleep_hours × prior_programming_years`) now explicitly
states that the visually chaotic T1 plot is expected, not a bug.

### Fix 6 — Local-minimum trap demonstration (R3 P0)

**New cells:** `section-local-min` (markdown) and `cell-local-min-demo`
(code), inserted between `cell-t2-reveal` and `section-t3-explain`.

The demo hard-codes `INIT_SCHEME='random'` + `N_INIT=1` and sweeps
`RANDOM_STATE` across 8 seeds. To make the trap *visible* (the 6-feature K=3
fit's basin is so large that even single-shot random init reliably finds the
global optimum), the demo deliberately **over-clusters at K=5 on the
2-feature data**. Result: inertia ranges from **109.85 (best) to 128.92
(worst)** across seeds — 5/8 seeds stuck in a meaningfully worse basin. The
demo bar-chart visually anchors the L12 §6 #1 lesson; the markdown
cross-references L05 Local Search §3 (random-restart hill climbing).

---

## P1/P2 fixes also folded in

- `cell-t6-prep` initial-centroid print now includes column names (R1 P2-B).
- `cell-t6-verify` now prints which comparison path was taken (cached vs fresh
  sklearn fit) (R2 P2 #5).
- Stale `K_T1` "expected sizes sanity-check" docstring removed; replaced with
  accurate note about T6's dependence (R4 P1, R2 P2 #2).
- `K_PRIMARY` docstring now lists exactly which cells it drives and which it
  does not (R2 P2 #1).

---

## Verification

- Re-executed end-to-end via `py -3.12 -m jupyter nbconvert --to notebook
  --execute --inplace lab3_clustering_solution.ipynb`. Zero errors. 37 cells.
- Headline numbers under defaults (RANDOM_STATE=42, K_T1=3, K_PRIMARY=3,
  k-means++, N_INIT=10):
  - T1 inertia (2-feat, k=3): **168.9** — unchanged.
  - T2 inertia (6-feat, k=3): **1010.8** — unchanged.
  - T2 grade-spread: **9.33** points — unchanged.
  - T4 recommended K: **2** (silhouette-argmax) — unchanged; now reconciled
    with the K=3 narrative.
  - T6 scratch inertia at iter 20: **168.886**; sklearn's: **168.886**;
    diff: **0.000** (previously: 170.1 vs 168.9, diff 1.2).
  - Local-min demo: K=5 on 2-feature, range **109.85 -> 128.92** (delta
    19.07), 5/8 seeds in a worse basin.

---

## Items intentionally NOT addressed in this revision (lower-severity P1/P2)

These are documented in the round-1 reports and remain outstanding; they're
non-blocking and can be addressed in a follow-up round if needed:

- R1 P1-C: T3 silhouettes on 2-feature data vs T4 on 6-feature data — table
  headers don't say which.
- R1 P1-D: T4 K=1 branch uses `n_init=1` without inline comment.
- R1 P1-E: `snap_to_danish` rounds ties downward (Danish-scale convention is
  asymmetric).
- R1 P2-A: `cell-banner` em-dash is mojibake on Windows console.
- R1 P2-H: Default `MY_PROFILE` always lands in "Dedicated achievers".
- R2 P2 #3-#7: misc KNOB-docstring polish.
- R3 P0-1, P0-3, P1-1..P1-7, P2: pedagogical breadth (multi-analogy MENTAL
  MODEL, three-family taxonomy, SSE-vs-inertia naming, hierarchical/DBSCAN
  comparison) — this would roughly double the notebook's markdown footprint
  and is a Round-2 scope question.
- R4 P1 #5: nine declared KNOBs without variant coverage (stretch variants).
- R4 P2 #3: `cell-t5-reveal` uses `rank(method='first')`, fragile to ties.

The P0 round-1 trio (T6 convergence story + K-knob ownership; K=2/K=3
reconciliation; local-min trap demo; variants V1/V2 false claims) is closed.

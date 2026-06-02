# MLLab3-Clustering — Variant Bank

Three self-contained exam-style variants for `lab3_clustering_solution.ipynb`,
each solvable by editing only the KNOB cells (no function bodies).

Each variant ends with a checklist of KNOBs the examiner must touch. Variants
follow Appendix B's spec §8.3 seed for this lab (`Different K` / `Different
feature pairs` / `Different initialization (k-means++ vs random)`).

---

## Variant 1 — K sweep: refit at K = 4

> *Refit K-means on the 6-feature student data with `K = 4` instead of the
> default 3. Report the new cluster sizes, the inertia, the mean
> `final_grade` per cluster, and whether the new clustering recovers the
> three baked archetypes any better than `K = 3` did.*

**Why this variant exists.** L12 emphasises that K-means cannot *choose* its
own `K`. The student must observe that asking for one more cluster than the
data has produces an over-split — typically the "Dedicated achievers" group
breaks into two near-identical sub-clusters whose mean grades barely differ,
while the silhouette score drops.

**KNOB changes to make (before running):**

- [ ] `K_PRIMARY = 4` (affects **T2 fit only** — i.e. T2 verify, T2 reveal,
      and T5 self-classification, which predicts on the T2 model)
- [ ] Leave `K_T1` alone (T1 *and* the T6 scratch loop both fit on the
      2-feature data and read from `K_T1`; touch `K_T1` only if the question
      asks about the 2-feature fit)
- [ ] Leave everything else at defaults

**What to report:**

- New cluster sizes (4 numbers) and inertia
- Mean `final_grade` per cluster
- Pairwise grade-spread between the two highest-study clusters (expect <1
  grade point — that's the over-split signal)
- Standalone observation: the T4 `recommended_k` printout is the
  silhouette-argmax over `K_GRID_T4` and is **independent of `K_PRIMARY`** —
  it will be the same as the default run. Use it as a *control*: compare
  your K=4 fit's quality against the recommendation, don't expect the
  recommendation to change because you flipped `K_PRIMARY`.

**Note on cluster naming.** With K_PRIMARY != 3, T5's human-readable cluster
names (`Light effort` / `Moderate middle` / `Dedicated achievers`) fall back to
generic `study-hours tier 1..K` labels — by design, because the three-archetype
narrative only fits K=3.

**Note on cluster IDs.** sklearn's cluster IDs (0, 1, 2, 3) are arbitrary and
not stable across K. "Cluster 0 at K=4" has no relationship to "Cluster 0 at
K=3". To compare across K, align clusters by mean study hours (or another
informative feature) — don't compare ID-to-ID.

---

## Variant 2 — Feature pair: use attendance vs exercises instead

> *Repeat T1 (the 2-feature fit, K=3) using `attendance_rate_pct` and
> `exercises_completed` instead of the default `(study_hours_per_week,
> prior_math_grade)`. Plot the resulting clusters. Did K-means still find
> three visually clean groups? How does the inertia compare?*

**Why this variant exists.** Feature choice can make or break a clustering.
`(attendance, exercises)` are both *behavioural* features that should still
separate the three archetypes — but the separation is on different axes, so
the centroid layout looks completely different. The student must understand
that K-means is feature-agnostic and that the "right" pair depends on what
question you're answering.

**KNOB changes to make (before running):**

- [ ] `FEATURE_PAIR_T1 = ('attendance_rate_pct', 'exercises_completed')`
- [ ] Leave `K_T1 = 3`
- [ ] Leave everything else at defaults

**What to report:**

- New T1 inertia (will differ from the default ~169 because the units have
  changed — that's why we scale)
- A short qualitative description: are the three clusters still visible?
  Along which axis are they most separated?
- T3 inertia-and-silhouette table at k=2/3/5 on the new feature pair — does
  k=3 still produce the best-looking partition in the side-by-side scatter?

**What does NOT change in this variant.** The T4 elbow + silhouette curves
fit on the **6-feature data** (`X6_scaled`), not on `FEATURE_PAIR_T1`. So the
T4 plots, the recommended K, and the T2/T5 results are identical to the
default run. The variant only touches the 2-feature artefacts: T1 (intuition,
solve, verify), T3 (solve, verify), and T6 (scratch loop on the new pair).

**Stretch:** try
`FEATURE_PAIR_T1 = ('sleep_hours', 'prior_programming_years')` — these two
features barely separate the archetypes, so K-means produces a visually
chaotic partition. The T1 plot will look unstructured and the T3 k-sweep
panels will look almost identical to each other; that is **the expected
result, not a bug**. The right takeaway: K-means faithfully clustered the
(uninformative) features. Useful to demonstrate the limits of clustering and
the "garbage in, garbage out" principle.

---

## Variant 3 — Initialisation scheme: random vs k-means++

> *Switch from `k-means++` initialisation to `'random'` initialisation
> (drop `N_INIT` to 1 to make the difference visible). Report whether the
> T2 inertia and silhouette change, and explain in one sentence why
> k-means++ usually wins.*

**Why this variant exists.** K-means is a Lloyd-step algorithm that finds
**local** optima. The initial centroid placement determines which basin of
attraction it lands in. `k-means++` spreads its initial seeds far apart on
purpose; pure `random` (Forgy) can occasionally start two seeds in the same
cluster, leading to a sub-optimal final partition. With `N_INIT > 1` sklearn
mostly papers over this by trying multiple starts and keeping the best —
the variant deliberately sets `N_INIT = 1` to expose the failure mode.

**KNOB changes to make (before running):**

- [ ] `INIT_SCHEME = 'random'`
- [ ] `N_INIT = 1`
- [ ] Optionally try several values of `RANDOM_STATE` (e.g. 0, 1, 7, 42) to
      see how variable the result is

**What to report:**

- New T2 inertia. Compare against the **default run's printed T2 inertia**
  (re-run the notebook once on defaults first and record the number — the
  exact baseline value depends on sklearn version and the dataset seed, so
  use the intra-session reading rather than a hard-coded constant).
  `'random'` with `N_INIT=1` should be at-best-equal, occasionally a few
  points worse.
- New silhouette at K=3 (from the T3 sanity-check table) — typically also
  flat or worse.
- One-sentence answer: why does k-means++ usually win? (Hint: read the
  K-means++ glossary entry — it spreads initial seeds proportional to
  squared distance from previous picks, so two seeds rarely start in the
  same true cluster.)
- The new **local-minimum trap demo cell** (3b in the notebook) sweeps
  `RANDOM_STATE` under `'random' + N_INIT=1` and prints inertia per seed.
  Use it as a textbook demonstration that K-means is local search (L12 §6
  pitfall #1). Some seeds will be visibly worse than others — that is the
  trap.

**Stretch:** set `INIT_SCHEME = 'random'` but bring `N_INIT` back to 10.
Inertia should match k-means++ closely — demonstrating that restart count
can mostly compensate for poor initialisation at the cost of more compute.

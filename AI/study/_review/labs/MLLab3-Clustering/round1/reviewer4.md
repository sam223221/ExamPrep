# Lab Reviewer #4 — Variant Adaptability (HARSH)
## Lab: MLLab3-Clustering — Round 1

**Reviewer scope:** I only judge whether the three variants in
`study/_exam/MLLab3-Clustering/variants.md` actually work when the student does
exactly what the variant instructs. I trace every KNOB the variant touches
through the notebook and flag any cell whose code does not match the variant's
promised behaviour, every documentation claim that is wrong or stale, and every
silent failure mode an examiner could exploit.

**Files inspected:**

- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab3_clustering_solution.ipynb`
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\MLLab3-Clustering\variants.md`

**Verdict up front:** **FAIL.** None of the three variants is wholly broken,
but every one carries at least one documentation claim that is provably wrong
when traced against the notebook, and Variant 1 contains a structural bug
where the "primary K" knob silently leaks into a cell that fits on the
2-feature data — producing a result the variant doc neither warns about nor
explains. The notebook is adaptable in spirit but the variant pack and the
KNOB docstrings lie about the scope of several knobs.

---

## Findings (severity-tagged)

### P0 — Variant 1: T6 from-scratch loop silently fits `K_PRIMARY` on 2-feature data

`cell-t6-prep` and `cell-t6-solve` build `centroids_scratch` from `X2_scaled`
(the 2-feature data) but loop with `K_PRIMARY` as the cluster count:

```python
init_idx = rng_scratch.choice(len(X2_scaled), size=K_PRIMARY, replace=False)
centroids_scratch = X2_scaled[init_idx].copy()
...
for c in range(K_PRIMARY):
    if (labels_scratch == c).any():
        centroids_scratch[c] = X2_scaled[labels_scratch == c].mean(axis=0)
```

`cell-t6-verify` then compares against a sklearn fit at `K_PRIMARY` on
**`X2_scaled`** (2-feature data), not the 6-feature data K_PRIMARY is supposed
to govern:

```python
sk_inertia = KMeans(n_clusters=K_PRIMARY, ...).fit(X2_scaled).inertia_
```

Variant 1's KNOB checklist says "`K_PRIMARY = 4` (affects T2 fit, T4 elbow
recommendation read-out, **T5 self-classification, T6 scratch loop**)". The
student following Variant 1 will set `K_PRIMARY=4` but **leave `K_T1=3`**, on
the explicit instruction "Leave `K_T1` alone (the 2-feature plot is a different
exercise; touch it only if the question asks about T1)". The result is an
internally inconsistent notebook: T1 plots 3 clusters on the 2-feature data,
T6 plots 4 clusters on the *same* 2-feature data with no commentary, and the
variant's promised "report whether the new clustering recovers the three baked
archetypes any better than K=3 did" — the variant is framed around 6-feature
behaviour — gets contaminated by a 2-feature scratch fit at K=4 on a feature
pair that only has two clean splits.

Either T6 should fit on 6 features (matching K_PRIMARY semantics), or T6's
cluster count should come from `K_T1` (matching its 2-feature data choice), or
the variant doc must explicitly warn the student that running T6 under
Variant 1 produces a 2-feature K=4 fit that nobody asked for. Currently none
of those three things is true.

**Suggested fix:** Decide which dataset T6 belongs to. If T6 is "scratch
K-means on the 2-feature scatter" (which the plot's intent suggests), then
T6 must use `K_T1`, not `K_PRIMARY`. Otherwise rewrite T6 to operate on
`X6_scaled`.

---

### P0 — Variant 1: KNOB checklist claims K_PRIMARY affects T4 "elbow recommendation read-out"; it does not

Variant 1 lists "T4 elbow recommendation read-out" as a downstream of
`K_PRIMARY`. Trace through the notebook:

- `cell-t4-solve` iterates `K_GRID_T4 = list(range(1, 11))`.
- `recommended_k = int(silhouette_curve['silhouette'].idxmax())`.

`K_PRIMARY` appears nowhere in the T4 cells. The recommended_k printout is the
silhouette-argmax across the *grid*, completely independent of K_PRIMARY. The
variant's "Did the silhouette recommendation move?" question is **only**
answerable by the underlying dataset structure — flipping K_PRIMARY from 3 to
4 cannot move `recommended_k` because K_PRIMARY does not feed the silhouette
computation.

A student reading the variant brief will reasonably expect that "set
K_PRIMARY=4 and re-run" causes the T4 read-out to change in some
deterministic way. It will not. The variant question silently relies on the
data-generation seed happening to produce a silhouette argmax that the student
can compare against — but the variant brief frames it as a consequence of the
KNOB flip, which it is not.

**Suggested fix:** Either remove "T4 elbow recommendation read-out" from the
list of things K_PRIMARY affects, or reword the question so the student
reports the standalone recommended_k as a control alongside the K_PRIMARY=4
clustering, not as a consequence of it.

---

### P0 — Variant 2: variant doc conflates T3 and T4; T4 elbow does NOT pick up FEATURE_PAIR_T1

Variant 2's "What to report" includes:

> Side-by-side observation: does the T3 k=2/3/5 sweep still look like a clean
> elbow at k=3 with this feature pair?

There are two problems here:

1. **T3 is not an elbow plot.** `cell-t3-verify` prints an inertia/silhouette
   table and lays out k=2/3/5 cluster scatters side-by-side. The actual elbow
   curve is in T4 (`cell-t4-plot`). Calling T3's k-sweep an "elbow" misleads
   the student into looking at the wrong figure.
2. **T4 elbow ignores FEATURE_PAIR_T1.** `cell-t4-solve` fits every K on
   `X6_scaled` (the 6-feature data). Changing FEATURE_PAIR_T1 cannot alter the
   T4 elbow or silhouette curve at all. Same for the recommended_k printout.

The notebook's `sol-header` HOW TO ADAPT §2 also misleads on this point: it
lists "The 2-D scatter, the side-by-side k-sweep plot, and the from-scratch
loop all pick up the new pair" — true — but omits that the T4 elbow does
**not**. A student inspecting the elbow under Variant 2 will see an identical
curve to the default and wonder what they did wrong.

**Suggested fix:** Either (a) reword Variant 2 to ask about T3's inertia table
only and explicitly note that T4 is on 6 features and won't move, or (b) add
a parallel KNOB `FEATURE_SET_T2T4` so the 6-feature path is itself swappable,
unblocking a richer family of feature-related variants.

---

### P1 — Stale documentation in `K_T1` KNOB block ("sanity-check 'expected sizes' line only matches at K=3")

The `K_T1` KNOB docstring in `cell-global-knobs` says:

> Exam variants: 2 / 3 (default) / 4 / 5. The sanity-check 'expected sizes'
> line only matches at K=3.

There is **no expected-sizes sanity-check line anywhere in the notebook**.
`cell-t1-verify` prints `Cluster sizes:` and `Inertia: ...` but does not
compare against any baked expectation. The "only matches at K=3" claim refers
to a sanity check that does not exist. Either the check was removed and the
docstring was not updated, or the check was never written. Students who skim
the KNOB docstrings looking for variant guidance will be confused.

**Suggested fix:** Either add the sanity-check (a `print` line comparing
observed sizes against expected `[126, 144, 90]` or similar derived from the
archetype mixing proportions when K_T1=3), or delete the stale promise from
the docstring.

---

### P1 — Variant 3 silently leaks past `INIT_SCHEME` into the T4 K=1 fit, but the K=1 fit hard-codes `n_init=1` without `init=INIT_SCHEME`

In `cell-t4-solve`:

```python
if k == 1:
    km1 = KMeans(n_clusters=1, n_init=1, random_state=RANDOM_STATE).fit(X6_scaled)
```

This is technically harmless (sklearn KMeans defaults to `init='k-means++'`
but at K=1 there's only one centroid to place, so the init scheme does not
matter). However it breaks the otherwise-uniform "every fit honours
INIT_SCHEME" contract that the variant brief and the KNOB docstring promise.
A reviewer or student looking at the cell will be unable to tell at a glance
whether the K=1 row of the elbow is consistent with the rest. More
importantly, it's an inconsistency that will bite if anyone ever extends
INIT_SCHEME beyond the two sklearn-supported values (e.g. via a callable
custom init).

**Suggested fix:** Pass `init=INIT_SCHEME` to the K=1 fit too, or refactor so
the K=1 branch shares the same KMeans constructor block as the rest of the
loop.

---

### P1 — Variant 3's `K=1` row in the silhouette table prints NaN; variant brief never warns the examiner that the argmax may degenerate

If the variant student also widens `K_GRID_T4` (it's a documented KNOB they
might touch), and the random-init silhouette curve ends up monotone decreasing
or NaN-heavy, `recommended_k = int(silhouette_curve['silhouette'].idxmax())`
will return whichever K happens to be max (possibly K=2 by default, since K=1
is NaN). The variant brief does not warn that with bad init, the argmax can
shift to a degenerate K. A harsh examiner could exploit this by asking "what
K does silhouette recommend now?" expecting the student to report the silly
answer (e.g. K=2) and discuss why.

This is a documentation omission, not a code bug — but it leaves the student
unprepared for an obvious follow-up question.

**Suggested fix:** Add a sentence to Variant 3 noting that the silhouette
argmax can shift to K=2 with `INIT_SCHEME='random' / N_INIT=1`, and ask the
student to explain why.

---

### P1 — Variant 1 says "Leave K_T1 alone" but the notebook's own header doc says K_T1 is the T1-specific override

`sol-header` HOW TO ADAPT §1 says:

> "Refit with a different K" (e.g. K=4, K=7) — change `K_PRIMARY` in the T2
> cell. The grade-reveal cell, the heatmap, the T5 self-cluster, the T6
> from-scratch loop, and the elbow plot all read from this KNOB.

Two issues:

1. The header doc claims "the elbow plot" reads from K_PRIMARY. It does not
   (see the P0 finding above). Stale.
2. The header doc claims "the T6 from-scratch loop" reads from K_PRIMARY.
   This is technically true, but as the P0 finding shows, T6 also operates on
   the 2-feature data, which is K_T1's territory. The header doc does not
   warn that this creates a K_PRIMARY-vs-K_T1 inconsistency. So a student
   following the header's guidance to "just change K_PRIMARY for any K
   variant" walks into the same trap Variant 1 walks them into.

**Suggested fix:** Rewrite the header doc and Variant 1 together so they tell
the same story about which K-knob owns which fit, and resolve the T6 owner
question (see P0).

---

### P1 — No variant exercises `K_GRID_T3`, `K_GRID_T4`, `MAX_ITER`, `N_STUDENTS`, or `DATA_SEED` — adaptability surface is half-untested

The notebook exposes nine top-level KNOBs (`RANDOM_STATE`, `K_T1`,
`K_PRIMARY`, `FEATURE_PAIR_T1`, `K_GRID_T3`, `K_GRID_T4`, `INIT_SCHEME`,
`N_INIT`, `MAX_ITER`) plus two dataset KNOBs (`N_STUDENTS`, `DATA_SEED`) plus
`SCRATCH_ITERS`, `SCRATCH_SEED`, `MY_PROFILE`. The variants file exercises
**three** of them. That leaves nine declared KNOBs with no corresponding
variant, including some with non-trivial cross-cell effects (`K_GRID_T3`
changes T3's side-by-side plot; `MAX_ITER=1` produces a distinctively
mid-converged result that the docstring promises as "educational").

Per the variants spec, Appendix B §8.3 names exactly three seeds (different
K, different feature pairs, different init). So strictly the variant pack
covers the *prescribed* surface — but the notebook's own KNOB inventory
promises more. Either prune the unused KNOBs (and their docstrings) or add a
"stretch variants" section.

**Suggested fix:** Either trim the KNOBs that no variant exercises down to a
minimal set, or extend variants.md with a §4 "stretch" block covering
`K_GRID_T3`, `MAX_ITER=1`, and a `DATA_SEED` re-roll to confirm the elbow is
robust to data resampling.

---

### P1 — Variant 2 stretch (`sleep_hours`, `prior_programming_years`) crashes the cluster-name fallback in T5

When `FEATURE_PAIR_T1` changes, T5 is technically unaffected because T5 uses
the 6-feature `kmeans6`. So the stretch is safe in that respect.

However, the variant doc does not warn that the 2-feature stretch produces a
visually "arbitrary partition" (the variant doc's own phrase) on T1 — meaning
the T1 centroids printout, the T1 scatter, and the T3 k-sweep plots will all
look chaotic and may not pass a casual "does this look reasonable?" sanity
check. A harsh examiner will ask: "your T1 plot looks meaningless — is your
K-means broken?" and the student needs to be ready with "no, the *features*
are uninformative" as the answer. Variant 2's stretch hints at this in one
sentence; it should be made explicit so the student doesn't second-guess
their code.

**Suggested fix:** Expand the stretch block in Variant 2 from one sentence to
a short paragraph explicitly stating that the visual result will look
unstructured, that this is expected, and that the right takeaway is "K-means
faithfully clustered the (uninformative) features".

---

### P2 — Variant 3's "expected inertia ~1010.8" baseline is unverified and brittle

Variant 3 says:

> Compare against the default's ~1010.8 — `'random'` with `N_INIT=1` should be
> at-best-equal, occasionally a few points worse.

The 1010.8 number is a specific empirical claim. It depends on
`RANDOM_STATE=42`, `DATA_SEED=42`, `N_STUDENTS=360`, the exact archetype
mixing proportions, and the sklearn version (since `n_init` semantics changed
in 1.4). Any change to any of those flips the baseline and the variant brief
silently becomes wrong. If the lab is graded against the variant brief's
literal number, the student is one sklearn-upgrade away from a "your inertia
doesn't match" deduction.

**Suggested fix:** Either (a) change "~1010.8" to "the default's printed
inertia value" so the comparison is intra-session, or (b) pin sklearn in the
environment and add a regression test that asserts the baseline number.

---

### P2 — Variant 1's "report cluster sizes" implicitly requires the student to know labels are not stable across K

When the student flips `K_PRIMARY=4` and re-runs T2, the *label IDs* (0, 1, 2,
3) are arbitrary — sklearn doesn't promise that "cluster 0" at K=4 has any
relationship to "cluster 0" at K=3. The variant brief asks for "cluster
sizes" and "mean final_grade per cluster" but does not warn that the IDs are
not comparable to the K=3 IDs. A harsh examiner could ask "did cluster 0
shrink or split?" and the student, naively comparing IDs, will give a wrong
answer.

This is a known K-means pedagogical pitfall and would be a fair exam
follow-up; the variant brief should pre-empt it.

**Suggested fix:** Add a sentence to Variant 1's "What to report" block:
"Note that cluster IDs are arbitrary; align clusters across K by their mean
study hours (or another feature) before comparing."

---

### P2 — `MY_PROFILE` cluster-naming fallback is order-dependent in a subtle way

In `cell-t5-reveal`:

```python
study_ranks = centers_df_t2['study_hours_per_week'].rank(method='first').astype(int)
if len(centers_df_t2) == 3:
    name_by_rank = {1: 'Light effort', 2: 'Moderate middle', 3: 'Dedicated achievers'}
else:
    name_by_rank = {r: f'study-hours tier {r}' for r in study_ranks.unique()}
```

`rank(method='first')` breaks ties by the order of appearance in the
DataFrame. For K_PRIMARY=4 (Variant 1), if two cluster centroids happen to
have identical study_hours_per_week to two decimal places, the tier ordering
depends on KMeans label assignment order — which is itself sklearn-version
sensitive. The variant doc does not flag this; the failure mode is "the tier
labels reshuffle on a different sklearn version even though the clustering is
identical".

Realistically, with 360 students and 6 features, exact ties are vanishingly
unlikely. But the fallback is still fragile and ought to use
`rank(method='dense')` or sort the centroids deterministically before
relabelling.

**Suggested fix:** Replace `rank(method='first')` with `rank(method='dense')`
or sort by `study_hours_per_week` ascending and reassign tier IDs from the
sort order.

---

### P2 — No variant exercises K_PRIMARY=2 or K_PRIMARY=5; Variant 1 only covers the K=4 over-split

The KNOB docstring promises "Exam variants: 2 / 3 (default) / 4 / 5". Only
K=4 is exercised in variants.md. K=2 is genuinely interesting (it collapses
"moderate middle" into either light or dedicated, and the silhouette can
spike). K=5 demonstrates further over-splitting. The variant pack should at
least mention these alternatives in Variant 1's "stretch" tail.

**Suggested fix:** Add a stretch tail to Variant 1: "try K_PRIMARY=2 and
report whether silhouette spikes (it often does, because K=2 collapses two
archetypes into a single 'meh' cluster against the 'achievers')."

---

## Trace summary — what each variant actually affects

| Variant | KNOB(s) flipped | Cells whose output truly changes | Cells the variant doc *claims* change but don't | Risk |
|---|---|---|---|---|
| 1 (K=4) | `K_PRIMARY=4` | T2 fit (cell-t2-solve, cell-t2-verify, cell-t2-reveal), T5 (cell-t5-solve, cell-t5-reveal), T6 (cell-t6-prep, cell-t6-solve, cell-t6-verify) | T4 elbow read-out (variant claims it changes; it doesn't) | T6 fits 2-feature data with K_PRIMARY=4 silently |
| 2 (FEATURE_PAIR) | `FEATURE_PAIR_T1=...` | T1 intuition cell, T1 solve/verify, T3 solve/verify, T6 (because T6 uses X2_scaled) | T4 elbow ("T3 k-sweep elbow") — variant conflates T3 with T4; T4 never changes | Student inspects T4 elbow expecting movement, finds none |
| 3 (random init) | `INIT_SCHEME='random'`, `N_INIT=1` | T1, T2, T3, T4 (K>=2 rows) | None significant | K=1 T4 row hardcodes `init='k-means++'` implicitly via default; minor consistency issue |

---

## Coverage gap against Appendix B §8.3

Spec §8.3 names three variant axes: different K / different feature pairs /
different init. Variants 1/2/3 nominally cover all three. However:

- "Different K" is covered with K=4 only; the docstring promises K=2 and K=5
  as accepted variants but no variant exercises them.
- "Different feature pairs" only changes the 2-feature artifacts; the 6-feature
  T2/T4 path has no variant lever, leaving half the notebook unswappable.
- "Different init" is exercised with `INIT_SCHEME='random' + N_INIT=1`, the
  worst case. There's no variant that just changes `INIT_SCHEME` while
  leaving `N_INIT=10`, which is the "in practice does this matter?" question
  the L12 lecture material asks.

This is technically compliant but minimally so.

---

## What the harsh examiner will catch

1. The Variant 1 student reports cluster sizes and inertia for T2 (correct),
   then runs T6 and gets a 2-feature K=4 result they have no framing for.
   "Why does your scratch implementation use a different K than your sklearn
   T1?" — student has no answer.
2. The Variant 2 student looks at the T4 elbow plot, sees it identical to
   default, concludes they did the variant wrong, and starts second-guessing
   `FEATURE_PAIR_T1` instead of writing up the (correct) Variant 2 answer.
3. The Variant 3 student reports an inertia ≠ 1010.8 and panics, when in fact
   the baseline was version-fragile.
4. Any student trying K=2 or K=5 (off-script but inside the KNOB docstring's
   promise) finds T5's cluster names are no longer "Light/Moderate/Dedicated"
   but `study-hours tier {n}` — fine, but the variant pack offers no
   guidance on whether to keep or rewrite the T5 narrative.

---

## Report to PM

**Assignment recap:** Lab Reviewer #4 (Variant Adaptability) for
MLLab3-Clustering Round 1. Reviewed the three variants in
`study\_exam\MLLab3-Clustering\variants.md` against
`lab3_clustering_solution.ipynb` to verify each variant produces a coherent,
internally consistent re-run when the prescribed KNOBs are flipped.

**Status:** FAIL.

**P0 findings:**

1. **T6 scratch loop fits K_PRIMARY on 2-feature data** (`cell-t6-prep`,
   `cell-t6-solve`, `cell-t6-verify` in
   `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab3_clustering_solution.ipynb`).
   Under Variant 1 this produces a 2-feature K=4 fit while T1 keeps K=3 on
   the same data — internally inconsistent. Suggested fix: switch T6 to use
   `K_T1` or move T6 onto the 6-feature data and use `K_PRIMARY` honestly.
2. **Variant 1 falsely claims K_PRIMARY drives the T4 elbow read-out.**
   `cell-t4-solve` does not reference `K_PRIMARY` anywhere; `recommended_k`
   is silhouette-argmax over `K_GRID_T4`. The variant brief frames the T4
   readout as a consequence of the KNOB flip. Suggested fix: rewrite the
   "KNOB changes to make" block in Variant 1 and the corresponding sentence
   in `sol-header` HOW TO ADAPT §1.
3. **Variant 2 conflates T3 with T4 and claims T4 elbow picks up
   FEATURE_PAIR_T1.** T4 fits on `X6_scaled` and is invariant to
   `FEATURE_PAIR_T1`. Suggested fix: rewrite Variant 2's "Side-by-side
   observation" bullet; alternately add a `FEATURE_SET_T2T4` knob so the
   6-feature path is itself swappable.

**P1 findings:**

1. Stale docstring in `K_T1` KNOB references a "sanity-check 'expected
   sizes' line" that does not exist in the notebook.
2. Variant 3's T4 K=1 fit hardcodes the default sklearn init, bypassing
   `INIT_SCHEME` — minor consistency issue.
3. Variant 3 does not warn the student that `recommended_k` can degenerate
   under bad init — an obvious follow-up question for a harsh examiner.
4. `sol-header` HOW TO ADAPT §1 claims K_PRIMARY drives the elbow plot
   (false) and the T6 scratch loop (true but with the silent 2-feature
   bug from P0 #1).
5. Nine declared KNOBs are not exercised by any variant — `K_GRID_T3`,
   `K_GRID_T4`, `MAX_ITER`, `N_STUDENTS`, `DATA_SEED`, `SCRATCH_ITERS`,
   `SCRATCH_SEED`, `MY_PROFILE`, plus K_T1 (no variant changes it
   independently). Either trim or add stretch variants.
6. Variant 2's `sleep_hours` × `prior_programming_years` stretch produces a
   visually chaotic T1 plot that an unwarned student will misread as a bug.

**P2 findings:**

1. Variant 3's "~1010.8" baseline is unverified and sklearn-version
   sensitive.
2. Variant 1 doesn't warn about cluster-ID instability across K — students
   will incorrectly compare cluster 0 at K=4 with cluster 0 at K=3.
3. `cell-t5-reveal` uses `rank(method='first')` for tier ordering; fragile
   to tied centroid values.
4. Variant 1 only exercises K=4; K=2 and K=5 are promised by the KNOB
   docstring but never tested.

**Variant coverage status:**

- Variant 1 (K sweep, K=4) — runs but produces an unflagged T6
  inconsistency; T4 claim is false. **Fail.**
- Variant 2 (FEATURE_PAIR_T1) — runs but variant brief conflates T3/T4 and
  T4 is genuinely unaffected. **Pass with concerns.**
- Variant 3 (random init, N_INIT=1) — runs; brittle baseline number and
  silent K=1 init inconsistency. **Pass with concerns.**

**Adaptability surface assessment:** The notebook exposes ~14 KNOBs but only
three see variant coverage. Documentation in `sol-header` HOW TO ADAPT and
in individual KNOB docstrings makes promises that the variant pack and (in
some cases) the cell code do not back up. The "flip a KNOB and re-run"
contract is honoured only for the simple cases; cross-cell coupling
(K_PRIMARY vs K_T1, FEATURE_PAIR_T1 vs the 6-feature path) is documented
loosely and tested narrowly.

**Out-of-scope observations:**

- `cell-t4-solve` recreates a KMeans constructor in two slightly different
  shapes (K=1 branch vs K>=2 branch). Easy refactor.
- The grade-reveal cell builds `reveal = df.copy()` twice (once in
  `cell-t2-reveal`, once in `cell-t5-reveal`) — minor redundancy.
- The notebook has no test/regression assertions; would benefit from at
  least one `assert` per task confirming sensible cluster sizes against the
  baked archetype proportions.

**Concerns / risks:**

- Variant 1 is the most likely to mislead a student because the K=4
  re-fit on T6 produces output that *looks correct* (the loop converges
  and matches sklearn at the same 2-feature K=4) but is the wrong K for
  the variant question being asked.
- If the lab is graded by automated comparison against a frozen expected
  output, Variant 3's "~1010.8" claim is a regression-test landmine.
- The notebook's coupling between K_PRIMARY (semantically "main K, 6
  features") and the T6 cell (which uses 2-feature data) is the kind of
  bug that survives because both cells "work" independently. Until
  someone draws a dependency graph of KNOB-to-cell, more such cases may
  be hiding.

**What PM should do next:** Send the notebook back to the implementation
engineer with the three P0 findings as mandatory fixes. Specifically: (a)
resolve T6's K-knob ownership, (b) correct Variant 1's claim about T4, (c)
correct Variant 2's claim about T4 and the T3/T4 conflation. After those
land, dispatch QA to re-verify the variant pack end-to-end before this lab
goes to App Tester. The P1 docstring/consistency fixes can ride along in
the same patch.

**DOCUMENT.md updated:** N/A for QA / lab review.

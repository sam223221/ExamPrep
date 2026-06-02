# Lab Reviewer #2 — KNOB Coverage — MLLab3-Clustering — Round 1

**Reviewer focus:** Does every critical KNOB declared in
`lab3_clustering_solution.ipynb` actually drive the cells it claims to drive,
and is every variant in `variants.md` solvable by KNOB-flipping alone?

**Critical KNOBs in scope:** `K_T1`, `K_PRIMARY`, `K_GRID_T3`, `FEATURE_PAIR_T1`,
`INIT_SCHEME`, `N_INIT`, `MAX_ITER`, `MY_PROFILE`.

**Mode:** harsh — fail-fast on any KNOB whose self-description does not match
its reach in the code, or any variant whose checklist KNOBs do not fully cover
the requested behaviour change.

---

## Per-KNOB Audit

### K_T1 (default = 3)

| Aspect | Finding |
|---|---|
| Declared scope | "number of clusters in T1 (2-feature fit)" |
| Actual code reach | `kmeans2 = KMeans(n_clusters=K_T1, ...)` in `cell-t1-solve`; `for i in range(K_T1)` in `cell-t1-verify`; T1 plot title `f'k={K_T1}'`. |
| Match? | YES — narrow, accurate. |
| Hidden coupling | None. K_T1 does **not** propagate to T3 (`K_GRID_T3` is independent), to T6 (`K_PRIMARY`), or to T4 (`K_GRID_T4`). The KNOB intro text correctly distinguishes K_T1 vs K_PRIMARY. |
| Variant solvability | Adequate. No variant in the bank touches K_T1 alone, but the variant docs flag that it can be changed for a "T1 with k=4" follow-up. |
| Verdict | **PASS** |

### K_PRIMARY (default = 3)

| Aspect | Finding |
|---|---|
| Declared scope | "main K used by T2 (all 6 features), T5 (self-classification), and T6 (from-scratch)" |
| Actual code reach | `kmeans6 = KMeans(n_clusters=K_PRIMARY, ...)` in `cell-t2-solve`; T5 prediction is via `kmeans6.predict(...)` so inherits K_PRIMARY transitively; T6 prep uses `size=K_PRIMARY` and `for c in range(K_PRIMARY)`; T6 verify uses `if K_PRIMARY in kmeans_by_k` then falls back to a fresh fit at K_PRIMARY. |
| Match? | YES on T2, T5, T6. |
| Hidden coupling | **The KNOB intro markdown (`cell-knobs-intro`) bullet 1 says K_PRIMARY also affects "the elbow plot" — this is FALSE.** The elbow + silhouette sweep is driven exclusively by `K_GRID_T4`; `recommended_k` is `silhouette_curve['silhouette'].idxmax()`, never compared against K_PRIMARY. The T4 plot has no visual marker tied to K_PRIMARY. See P2 finding below. |
| Hidden coupling #2 | T5 cluster-name dictionary in `cell-t5-reveal` only emits the human-readable names ("Light effort" / "Moderate middle" / "Dedicated achievers") when `len(centers_df_t2) == 3`. For K_PRIMARY != 3 (e.g. Variant 1's K=4) it falls back to `f'study-hours tier {r}'`. Working as intended but not flagged in the KNOB header. |
| Hidden coupling #3 | T6 scratch loop compares against `kmeans_by_k[K_PRIMARY]` if available, else fits a fresh sklearn model. For K_PRIMARY=4 (not in default K_GRID_T3=[2,3,5]) the fallback path is taken silently. Functions correctly but the silent fallback is undocumented. |
| Variant solvability | Variant 1 (K=4) — solvable by flipping K_PRIMARY=4 alone, with caveats above. |
| Verdict | **PASS WITH CONCERNS** (P2 documentation drift) |

### K_GRID_T3 (default = [2, 3, 5])

| Aspect | Finding |
|---|---|
| Declared scope | "three K values T3 lays out side-by-side on the 2-D fit" |
| Actual code reach | `for k in K_GRID_T3:` in `cell-t3-solve`; iteration over `kmeans_by_k` in `cell-t3-verify`. |
| Match? | YES. |
| Robustness | `cell-t3-verify` defensively guards silhouette with `if k >= 2:` but **does not guard the KMeans fit itself against k=1**. `KMeans(n_clusters=1)` does run (sklearn accepts it) so that's safe, but the doc says "Any three positive ints >= 2 work" while the guard implies the author considered k=1. Mildly inconsistent. |
| Variant solvability | No variant in the bank touches K_GRID_T3 directly. Variant docs mention `[2, 3, 4]` / `[3, 5, 8]` as legal options. Covered. |
| Verdict | **PASS** |

### FEATURE_PAIR_T1 (default = ('study_hours_per_week', 'prior_math_grade'))

| Aspect | Finding |
|---|---|
| Declared scope | "T1 / T3 / T6 use" |
| Actual code reach | `cell-t1-intuition` reads it for the before/after scaling demo; `cell-t1-solve` builds `two_feats`, `X2_raw`, `scaler2`, `X2_scaled` from it; `cell-t3-solve` re-uses `X2_scaled`; `cell-t3-verify` re-uses `scaler2.inverse_transform(...)` and `two_feats` axis labels; `cell-t6-prep` re-uses `X2_scaled`. |
| Match? | YES — propagation is clean because T3 and T6 both consume the cached `X2_scaled`, not re-derive from FEATURE_PAIR_T1. The KNOB doesn't need to be re-read in later cells. |
| Variant solvability | Variant 2 — solvable by flipping FEATURE_PAIR_T1 alone. T2's 6-feature view does not depend on it (as expected — T2 always uses all 6). |
| Subtle risk | If a student flips FEATURE_PAIR_T1 but only re-runs T1 (skipping T3 + T6), the downstream cells still operate on the OLD `X2_scaled`. This is the standard "re-run from this cell down" failure mode that all KNOB notebooks share; the sol-header warns about it ("flipping a KNOB and re-running from that cell onward"). Acceptable. |
| Verdict | **PASS** |

### INIT_SCHEME (default = 'k-means++')

| Aspect | Finding |
|---|---|
| Declared scope | "T1, T2, and T3 KMeans calls all read it" |
| Actual code reach | Used in T1 (`cell-t1-solve`), T2 (`cell-t2-solve`), T3 (`cell-t3-solve`), **and T4 (`cell-t4-solve`)** — the latter is undocumented in the KNOB header but is the correct behaviour. |
| Match? | YES — actual reach is *broader* than documented (T4 also picks it up). Documentation under-states; not a defect. |
| Not reached | The warm-up demo (`cell-warmup`) hardcodes `init` (uses default `'k-means++'` implicitly). T6 scratch uses Forgy/random by construction (correct — it is a from-scratch demo, not an INIT_SCHEME consumer). T4's k=1 branch uses default init (irrelevant for k=1). All intentional. |
| Variant solvability | Variant 3 — solvable by flipping INIT_SCHEME='random' + N_INIT=1. T2 (k=3, 6-feature) inertia visibly changes; T1/T3/T4 all also change as a bonus. Covered. |
| Verdict | **PASS** (documentation slightly understates scope; harmless) |

### N_INIT (default = 10)

| Aspect | Finding |
|---|---|
| Declared scope | "number of independent restarts" — applies to all four sklearn fits (T1/T2/T3/T4). |
| Actual code reach | T1, T2, T3, T4 all use `n_init=N_INIT`. T4's k=1 branch hardcodes `n_init=1` (correct — restarting a 1-cluster fit is meaningless). Warm-up demo hardcodes `n_init=10`. T6 scratch has no concept of restarts (single Forgy run). |
| Match? | YES. |
| Variant solvability | Variant 3 requires N_INIT=1 — covered. Variant 3 stretch (`N_INIT=10` with random init) also covered. |
| Hidden caveat | When INIT_SCHEME='k-means++', N_INIT effectively only varies the seed of the k-means++ probabilistic init; for this dataset the result is essentially deterministic, so dropping N_INIT to 1 with k-means++ leaves inertia unchanged. The doc text correctly notes "random init is more sensitive to N_INIT" but a student might expect N_INIT=1 with k-means++ to also degrade — it usually won't on this data. Not a defect, but worth noting. |
| Verdict | **PASS** |

### MAX_ITER (default = 300)

| Aspect | Finding |
|---|---|
| Declared scope | "hard cap on assign/update iterations per restart" |
| Actual code reach | T1, T2, T3, T4 fits. **NOT** in T4's k=1 branch (irrelevant). **NOT** in T6 (scratch uses `SCRATCH_ITERS`, declared as a separate KNOB — appropriate). **NOT** in warm-up (intentional). |
| Match? | YES. |
| Variant solvability | No variant in the bank exercises MAX_ITER. Doc lists `1 / 300 / 3000` as variants but no exam-question is written for them. The KNOB exists as a *demonstration lever* (set to 1 to show under-converged centroids). Acceptable. |
| Subtle risk | If `MAX_ITER = 1` and `INIT_SCHEME = 'k-means++'`, the result is still close to converged because k-means++ seeds near-final centroid positions on well-separated data. To see the "under-converged" effect, one must also set `INIT_SCHEME = 'random'` and `N_INIT = 1`. This compound dependency is not documented in MAX_ITER's KNOB block. Minor. |
| Verdict | **PASS** (with a P2 note on cross-KNOB interaction not being spelled out) |

### MY_PROFILE (default = balanced moderate student)

| Aspect | Finding |
|---|---|
| Declared scope | "the habit vector predicted by kmeans6" |
| Actual code reach | `cell-t5-solve` reads it: `my_x = np.array([[MY_PROFILE[c] for c in FEATURE_COLS]])`. Then `scaler6.transform` + `kmeans6.predict`. Plus `cell-t5-reveal` builds `my_series = pd.Series(MY_PROFILE, name='you')` for the side-by-side compare table. |
| Match? | YES. |
| Robustness gap | **MY_PROFILE must contain ALL six FEATURE_COLS keys, in any order**. A missing key (e.g. dropping `prior_programming_years`) raises `KeyError` at the list comprehension. A misspelled key likewise fails. This footgun is not flagged in the KNOB's "What it does" block. P2. |
| Robustness gap #2 | Extra keys in MY_PROFILE are silently ignored by the list comprehension (because it iterates FEATURE_COLS) but they DO appear in the `compare` table via `pd.Series(MY_PROFILE)`. So a student who adds `'caffeine_mg': 200` to MY_PROFILE will see a spurious row in the compare DataFrame with NaN in the `centroid` column. Not common, but possible. P2. |
| Variant solvability | No bank variant exercises MY_PROFILE directly, but the lab's task T5 explicitly invites the student to fill in their own habits. The KNOB pattern works. |
| Verdict | **PASS WITH CONCERNS** (footguns undocumented) |

---

## Variant-by-Variant Coverage Check

### Variant 1 — `K_PRIMARY = 4`

- [x] KNOB checklist (`K_PRIMARY = 4`) is sufficient to drive T2 + T5 + T6 to k=4.
- [x] "Cluster sizes (4 numbers)" — produced by `cell-t2-verify`.
- [x] "Inertia" — produced.
- [x] "Mean `final_grade` per cluster" — produced by `cell-t2-reveal` summary table.
- [ ] **"Did the silhouette recommendation move?"** — The variant text implies
      this question is answerable from the K_PRIMARY=4 run. In fact `recommended_k`
      is computed **independently** of K_PRIMARY (it is the argmax of
      `silhouette_curve` over `K_GRID_T4 = range(1, 11)`). The recommendation
      therefore does not change between the default run and the K=4 run. The
      variant phrasing is misleading — see P1 finding below.
- [x] "Pairwise grade-spread between the two highest-study clusters" — readable
      off the summary table but not pre-computed; reasonable student exercise.

**Coverage:** Solvable with the listed KNOB flip; one report item phrased
ambiguously.

### Variant 2 — `FEATURE_PAIR_T1 = ('attendance_rate_pct', 'exercises_completed')`

- [x] KNOB checklist is sufficient.
- [x] New T1 inertia produced.
- [x] T1 scatter + T3 k=2/3/5 sweep both reflect the new pair (verified via
      `two_feats`, `X2_raw`, `X2_scaled` derivation chain).
- [x] T6 scratch also runs on the new pair (uses `X2_scaled`).
- [x] Stretch (`sleep_hours, prior_programming_years`) likewise covered.

**Coverage:** Clean.

### Variant 3 — `INIT_SCHEME = 'random'` + `N_INIT = 1`

- [x] KNOB checklist is sufficient.
- [x] T1, T2, T3, T4 fits all pick up both KNOBs.
- [x] T6 scratch is correctly *unaffected* (it is the from-scratch demonstration
      of random init by construction).
- [x] Stretch (`INIT_SCHEME='random' + N_INIT=10`) covered — restart count
      compensates for poor init.
- [x] Reproducibility: variant docs invite varying `RANDOM_STATE`, which is a
      separate KNOB and works as advertised.

**Coverage:** Clean.

---

## Findings

### P0 — Blocks shipping

None.

### P1 — Important issues

1. **Variant 1 phrasing misleads about silhouette recommendation**
   (`variants.md` lines 39 + 27). The variant lists `K_PRIMARY = 4` as the sole
   KNOB and asks "Did the silhouette recommendation move?" — but `recommended_k`
   in the notebook is derived from the T4 sweep over `K_GRID_T4`, not from
   K_PRIMARY. Flipping only K_PRIMARY does not change the printout. Either
   reword the question ("Compare the default silhouette recommendation against
   the K=4 fit you just ran") or include `K_GRID_T4` in the checklist with a
   note that the recommendation is a function of the sweep.
   *Suggested fix:* add a sentence to the variant: "The `recommended_k`
   printout reflects the silhouette argmax over `K_GRID_T4` and is independent
   of `K_PRIMARY`. Compare your K=4 cluster quality against the recommendation,
   don't expect the recommendation itself to change."

### P2 — Polish / suggestions

1. **KNOB intro markdown (`cell-knobs-intro`) overstates K_PRIMARY's reach.**
   Bullet 1 lists "the elbow plot" among the cells K_PRIMARY drives. The
   elbow/silhouette sweep is governed solely by `K_GRID_T4`. Strike "the elbow
   plot" from that bullet, or clarify that K_PRIMARY only feeds the T4 *read-out*
   (it doesn't — `recommended_k` is independent of K_PRIMARY).

2. **sol-header `OUTPUTS WHEN RUN` claim about T1 sanity-check is stale.**
   The header text says "the sanity-check 'expected sizes' line only matches at
   K=3" but `cell-t1-verify` does not print an expected-sizes assertion; it
   just prints the actual sizes. Either remove the claim or add the missing
   assertion.

3. **MY_PROFILE footguns undocumented.** The KNOB block does not warn that:
   (a) all six `FEATURE_COLS` keys are required, missing key → KeyError;
   (b) extra keys leak into the compare table as NaN-centroid rows.
   Add a one-line "must contain exactly the six FEATURE_COLS keys" note.

4. **K_GRID_T3 robustness comment is inconsistent.** The KNOB doc says "Any
   three positive ints >= 2 work" but `cell-t3-verify` defensively guards
   silhouette with `if k >= 2:`. Either drop the guard (since k>=2 is
   guaranteed) or document that k=1 is technically permitted with silhouette
   reported as "n/a".

5. **T6 silent fallback to a fresh sklearn fit when `K_PRIMARY ∉ K_GRID_T3`.**
   For Variant 1 (K=4), the comparison-vs-sklearn line refits a fresh model
   instead of pulling from `kmeans_by_k`. This is correct behaviour but the
   silence may confuse a student debugging an inertia mismatch. Add a `print`
   indicating which path was taken.

6. **MAX_ITER demonstration depends on compound KNOB state.** The KNOB doc
   suggests `MAX_ITER=1` shows "what K-means looks like after a single Lloyd
   step" — but with `INIT_SCHEME='k-means++'` (default) the centroids are
   already near-final at iteration 1 on this well-separated data. To see the
   educational effect, the student must also set `INIT_SCHEME='random'` and
   `N_INIT=1`. Document this compound requirement.

7. **Cluster-name fallback only triggers at K!=3.** Variant 1 (K=4) loses the
   human-readable cluster names ("Light effort" etc.) and shows
   "study-hours tier 1/2/3/4" instead. This is intentional and reasonable but
   not previewed in the variant doc — students may expect the achiever cluster
   to be labelled in plain English.

---

## KNOB Coverage Matrix (final)

| KNOB | Documented scope matches code? | Variant-bank coverage |
|---|---|---|
| K_T1 | YES | covered as a documented variant option |
| K_PRIMARY | MOSTLY (P2 #1 — overstates "elbow plot") | Variant 1 (with P1 #1 caveat) |
| K_GRID_T3 | YES (P2 #4 — minor doc inconsistency) | covered as variant option |
| FEATURE_PAIR_T1 | YES | Variant 2 |
| INIT_SCHEME | YES (actual reach is broader than docs claim — harmless) | Variant 3 |
| N_INIT | YES | Variant 3 |
| MAX_ITER | YES (P2 #6 — compound dependency hidden) | no bank variant, doc-listed only |
| MY_PROFILE | YES (P2 #3 — footguns undocumented) | exercised by T5 task |

---

## Report to PM

**Assignment recap:** Lab Reviewer #2 — KNOB Coverage audit on
`lab3_clustering_solution.ipynb` round 1, against
`study/_exam/MLLab3-Clustering/variants.md`.

**Status:** Pass with concerns

**P0 findings:** None.

**P1 findings:**

1. `study/_exam/MLLab3-Clustering/variants.md:39` (and the implicit checklist
   at line 27) — Variant 1 asks "Did the silhouette recommendation move?" as if
   flipping `K_PRIMARY=4` should affect `recommended_k`. It cannot: in
   `lab3_clustering_solution.ipynb` `cell-t4-solve` `recommended_k` is the
   silhouette-argmax over `K_GRID_T4`, independent of `K_PRIMARY`. Suggested
   fix: reword the question to compare cluster-quality of K=4 against the
   independent recommendation, OR add `K_GRID_T4` to the checklist with an
   explanation that the recommendation is sweep-driven.

**P2 findings:**

1. `lab3_clustering_solution.ipynb` `cell-knobs-intro` bullet 1 — strike "the
   elbow plot" from the list of cells K_PRIMARY drives. The elbow/silhouette
   sweep is `K_GRID_T4`-driven.
2. `lab3_clustering_solution.ipynb` `cell-sol-header` — the "expected sizes
   sanity-check" claim is stale; T1 verify cell does not assert sizes.
3. `lab3_clustering_solution.ipynb` `cell-global-knobs` MY_PROFILE block — add
   a one-line note that all six `FEATURE_COLS` keys are required (missing →
   KeyError) and extra keys appear as NaN-centroid rows in the compare table.
4. `lab3_clustering_solution.ipynb` `cell-t3-verify` — the `if k >= 2:` guard
   conflicts with the KNOB doc's claim that K_GRID_T3 entries must be >= 2.
   Either drop the guard or relax the doc.
5. `lab3_clustering_solution.ipynb` `cell-t6-verify` — silent fallback to a
   fresh sklearn fit when `K_PRIMARY ∉ K_GRID_T3`; add a `print` line so the
   student sees which comparison path was taken.
6. `lab3_clustering_solution.ipynb` `cell-global-knobs` MAX_ITER block —
   document that the "single Lloyd step" demonstration requires also setting
   `INIT_SCHEME='random'` and `N_INIT=1` to be visually instructive.
7. `study/_exam/MLLab3-Clustering/variants.md` Variant 1 — flag that cluster
   names will fall back to "study-hours tier 1/2/3/4" when K_PRIMARY != 3.

**QA Checklist (§7) status:** N/A — no formal Feature Plan QA checklist was
issued for this lab; this review covers KNOB coverage and variant solvability
only.

**Acceptance criteria (§1) status:**

- Critical KNOBs each documented with a scoped purpose: MET
- Variants 1–3 solvable by KNOB-flipping alone: MET (Variant 1 with the
  phrasing caveat in P1 #1)
- KNOB descriptions consistent with code behaviour: MOSTLY MET (see P2 #1, #2,
  #4, #6)

**DOCUMENT.md audit:** Not applicable to this lab (study/lab notebook, not a
service directory).

**Out-of-scope observations:**

- `cell-warmup` is hardcoded (random_state=0, n_init=10, k=3) and does not read
  any global KNOB. Intentional (it is a fixed pedagogical demo) but worth a
  one-line comment so a student doesn't try to flip KNOBs and re-run only the
  warm-up.
- `DATA_SEED` and `N_STUDENTS` are KNOBs declared inside `cell-dataset`, not
  hoisted to the global KNOB block. They behave as documented but are out of
  the eight critical KNOBs this review focuses on.
- `SCRATCH_ITERS` and `SCRATCH_SEED` likewise local to T6.

**Concerns / risks:**

- The P1 finding above is the one item that could cause a student to submit a
  technically-incorrect Variant 1 answer ("the recommendation moved") because
  they trusted the variant prompt. Worth fixing before round 2.
- KNOB documentation drift between the sol-header markdown, the KNOB cell
  docstrings, and the actual code paths is the dominant P2 theme. None of the
  drifts break execution, but they erode the "trust the doc, flip a KNOB"
  contract.

**What PM should do next:**

1. Dispatch `pm-frontend` (or whichever owns the notebook) to apply the P1 +
   P2 fixes listed above — they are all documentation/text edits, no algorithm
   changes.
2. Re-dispatch this reviewer for round 2 once edits land.
3. Then proceed to App Tester for end-to-end variant execution.

**DOCUMENT.md updated:** N/A for QA.

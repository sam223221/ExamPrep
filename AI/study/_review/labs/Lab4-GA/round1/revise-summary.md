# Lab4-GA Round 1 — Reviser Summary

**Assignment recap:** Apply the P0/P1 fixes called out by reviewers
1-4 across the four `handout_lab_4/*_solution.py` files. Brief was
explicit about which findings to address; everything else deferred.

**Status:** Done — all listed P0s and the listed P1s addressed. End-
to-end demos and the three mandatory exam variants verified via
direct Python runs.

---

## Files revised (absolute paths)

- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\ga_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\Number_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\Queen_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\queens_fitness_solution.py`

No new files. No deletions. Brief's "save revised files" interpreted
as in-place rewrites.

---

## R2 (KNOB Coverage) — P0 fixes

### R2 P0-1: KNOB names ↔ variants.md naming mismatch

Renamed in `ga_solution.py` to match `variants.md` canonical names:

| Old name | New name |
|---|---|
| `POPULATION_SIZE_QUEENS` | `POPULATION_SIZE` |
| `MAX_GENERATIONS_QUEENS` | `MAX_GENERATIONS` |
| `P_MUTATION` | `MUTATION_RATE` |
| `SHOULD_TRIM_POPULATION` | `TRIM_POPULATION` |

`POPULATION_SIZE_NUMBER` and `MAX_GENERATIONS_NUMBER` retained
(Number-specific knobs disambiguated by suffix — only Queens-side
gets the unsuffixed canonical name, since `variants.md` Variant 1
explicitly targets the Queens demo). `MINIMAL_FITNESS_NUMBER`
retained as-is (variants.md uses the same name).

Wired the renamed knobs through `_run_number_demo`,
`_run_queens_demo`, `Number_solution.main()`, and
`Queen_solution.main()`.

### R2 P0-2: `Number_solution.main()` ignored its own KNOBs

Replaced the hard-coded `minimal_fitness = (2 ** GENE_LENGTH) - 1`
in `Number_solution.py:main()` with a lazy import that pulls
`MINIMAL_FITNESS_NUMBER`, `MAX_GENERATIONS_NUMBER`, `MUTATION_RATE`,
`TRIM_POPULATION`, `USE_MU_PLUS_LAMBDA`, and `RANDOM_SEED` from
`ga_solution.py`. `main()` now respects all global KNOBs exactly
like `_run_number_demo` does. Optional variant 4c
(`MINIMAL_FITNESS_NUMBER = 31`, `NUMBER_GENE_LENGTH = 5`) verified
to converge.

Same treatment applied to `Queen_solution.main()`: it now reads
`N_QUEENS`, `POPULATION_SIZE`, `MAX_GENERATIONS`,
`MINIMAL_FITNESS_QUEENS`, `MUTATION_RATE`, `TRIM_POPULATION`,
`USE_MU_PLUS_LAMBDA`, and `RANDOM_SEED` from `ga_solution.py`.

---

## R3 (Pedagogical Clarity) — P0 fixes (slide-faithful GA)

### R3 P0-1 / P0-2: Two children per crossover; selection returns one

Rewrote the GA loop in `ga_solution.py:genetic_algorithm` to match
L05 §4.3 verbatim:

- `roulette_wheel_select(population) -> Individual` — returns ONE
  individual. Lecture-canonical name.
- Called TWICE INDEPENDENTLY per crossover event.
- `reproduce(other) -> tuple[Self, Self]` contract updated on
  `Individual` ABC, `NumberIndividual`, and `Board`. Both children
  added to the new population per iteration.
- Loop condition changed from
  `for _ in range(len(population))` (producing N children) to
  `while len(new_population) < target_size` (producing pairs until
  the new population reaches the target size, with set
  deduplication tolerated).

`random_selection(population) -> tuple[Individual, Individual]`
retained as a backward-compatibility wrapper that calls the new
single-individual selector twice. Original callers/tests still
import-compatible.

### R3 P0-3: False "proportions unchanged" math claim

Rewrote the `roulette_wheel_select` docstring. Removed the false
"proportions are unchanged up to a constant" line. Replaced with
the honest "adding a constant to every fitness does NOT preserve
proportions, so we shift only when negative weights are present".

### R1 P1-1: Conditional shift

Implemented the suggested fix: shift the fitnesses by
`-min_fitness` only when `min_fitness < 0`. When all fitnesses are
already ≥ 0, the fitnesses are used as-is — preserving slide-6
walkthrough numerics exactly (the (0,0,0) individual gets 0/12 of
the wheel, not 1/16).

### R1 P1-2: `pick_individual` fallback path broken

Made `shifted_fitnesses` REQUIRED in `pick_individual` (dropped
the default-None and the fallback branch). The all-zero-weight
guard moved up into `roulette_wheel_select`, where it falls back
to `random.choice` once and only once before invoking
`pick_individual`. Now the call site contract is explicit: callers
are responsible for any shift needed to guarantee non-negative
weights.

### R3 P0-4: Default to generational replacement

Default behaviour now `population = new_population` (the L05 §4.3
generational GA). Added a new top-level KNOB
`USE_MU_PLUS_LAMBDA: bool = False` that, when True, reverts to the
old `population = population.union(new_population)` behaviour. The
docstring now opens with "this code defaults to the §4.3
generational GA. The (μ + λ) variant is available behind a knob."

### R3 P0-5: Slide-11 hard-coded population caveat fix

Updated the `Number_solution.py` HOW-TO-ADAPT block. The previous
docstring incorrectly bragged that "(1,1,1) is absent by design" —
that is true for slide 10 (target=None), but slide 11 (target=4)
fails because `(1, 0, 0)` IS present in the slide-5 hard-coded set.
The HOW-TO-ADAPT block now explicitly:

- Names the conflict: setting `NUMBER_TARGET = 4` with the
  hard-coded population in place makes the GA terminate at
  generation 0.
- Lists two mitigations: flip `NUMBER_USE_HARDCODED_POPULATION =
  False`, or edit `INITIAL_NUMBER_POPULATION` to remove `(1, 0, 0)`.
- Documents what the default set is safe for (slide-10 target =
  (1,1,1) is absent) and what it is NOT safe for (slide-11 target =
  4 = (1,0,0) is present).

### R3 P0-6: Per-bit mutation (not "exactly one bit")

`NumberIndividual.mutate()` rewritten to the lecture L05 §3.6.2
canonical form: iterate each bit, flip with independent
probability `NUMBER_MUTATION_BIT_RATE`. Multiple bits can flip per
call. Default `NUMBER_MUTATION_BIT_RATE` changed from `1.0`
("always flip exactly one bit if outer gate fires") to `0.1`
(per-bit canonical regime — typically zero or one flip on a 3-bit
gene). Docstring rewritten to cite L05 §3.6.2 explicitly.

`Board.mutate()` given the same treatment: each column independently
reassigned with probability `QUEENS_MUTATION_COLUMN_RATE` (default
`0.25`). Lecture-faithful per-gene-with-probability-m on the
queens encoding.

### R3 P2-7: Default `MUTATION_RATE` flipped to 0.05

`MUTATION_RATE: float = 0.05` per L05 §8.6 cheat-sheet
recommendation. KNOB docstring notes "the handout PDF template
uses 0.8 — that is a template convenience for tiny populations and
is not the lecture-canonical default".

---

## R1 (Correctness) — P1 fixes

### R1 P1-3: `fittest_individual = None` for zero-gen runs

`genetic_algorithm` now initialises `fittest_individual =
get_fittest_individual(population)` immediately after the
empty-population guard. Callers passing `num_of_generations=0` now
receive the fittest of the initial population instead of None.

### R1 P1-5: Convergence-generation printed

`genetic_algorithm` now tracks `converged_at` and prints either
"Converged at generation N." or "MAX_GENERATIONS (M) hit without
reaching target fitness F." after the loop. This surfaces the
information variant 1 acceptance asks for.

### R1 P2-7: `queens_fitness` smoke-test now asserts

Replaced the print-only smoke test in
`queens_fitness_solution.py` with hard `assert` statements for the
slide-14 boards (`-6`, `-7`) and the perfect 4-queens solution
(`0` under negative, `6` under positive). Regressions will now
crash loudly instead of silently printing different numbers.

---

## R4 (Variant Adaptability) — P0 fixes

### R4 P0-1: `column_weight` reference in queens_fitness header

`queens_fitness_solution.py` HOW-TO-ADAPT item 2 rewritten. The
previous text said "call `fitness_fn_weighted` with `column_weight
= 3`" — but no such parameter exists on the actual function. The
revised item:

- References the actual parameters: `diag_weight` and `row_weight`.
- Explicitly explains why there is NO column-weight knob: "column
  conflicts are structurally impossible under this gene encoding
  (one queen per column), so a column-weight parameter would have
  no effect".

### R4 P0-2: Phantom "Appendix B variant 3" in Queen_solution

`Queen_solution.py` HOW-TO-ADAPT item 4 rewritten. The previous
text referenced "Appendix B variant 3" which does not exist in
`variants.md`. The revised item:

- Describes the weighted-fitness extension as a self-practice
  feature only.
- Explicitly states "NOT in the locked variant bank".

The `QUEENS_FITNESS_VARIANT` and `QUEENS_DIAG_WEIGHT` /
`QUEENS_ROW_WEIGHT` KNOB docs updated correspondingly to mark them
as self-practice rather than variant-bank-required.

---

## Side effects of the rewrite (non-brief but unavoidable)

- The `pick_individual` signature changed: `shifted_fitnesses` is
  now required (was optional). The only in-tree caller was
  `roulette_wheel_select` / `random_selection`, which always
  provides it — no external code broken.
- `Individual.reproduce` ABC contract changed from `-> Self` to
  `-> tuple[Self, Self]`. Both concrete subclasses
  (`NumberIndividual`, `Board`) updated.
- `QUEENS_CROSSOVER_RETURN_CHILD` KNOB removed from
  `Queen_solution.py` — it was a workaround for the one-child
  driver, and is meaningless now that the driver consumes both
  children. The `reproduce` method directly returns both.
- `genetic_algorithm`'s `should_trim_population` parameter renamed
  to `trim_population_flag` to avoid shadowing the
  module-level helper function `trim_population` and to disambiguate
  from the same-named KNOB `TRIM_POPULATION`.
- `get_initial_population(count, n_queens=8)` default changed to
  `n_queens=4` to match the lab default `N_QUEENS = 4`. All
  callers pass it explicitly anyway.

---

## Verification (live runs)

All runs executed via `py -3.12 ...` from
`c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4`.

| Run | Result |
|---|---|
| `queens_fitness_solution.py` (smoke + asserts) | Pass; slide-14 boards assert -6 / -7, perfect 4-queens 0 / 6. |
| `Number_solution.py` (direct, default knobs) | Converged to (1,1,1) at generation 16. |
| `Queen_solution.py` (direct, default knobs) | Converged to (2,4,1,3) at generation 0 (initial pop already had it; expected for 4-queens). |
| `ga_solution.py` (full default run) | Number → converged gen 9; Queens → 5/5 trials converge within 200 gens. |
| Variant 1 (8-Queens, POPULATION_SIZE=50, MAX_GENERATIONS=500, MUTATION_RATE=0.1) | Converged to (6,3,7,2,8,5,1,4) at gen 58, fitness 0. |
| Variant 3 (positive, MINIMAL_FITNESS_QUEENS=6) | Converged to (3,1,4,2) at gen 70, fitness 6. |
| Optional 4b (TRIM_POPULATION=True, USE_MU_PLUS_LAMBDA=True, MAX_POPULATION_SIZE=30) | Converged to (3,1,4,2) at gen 6. |
| Optional 4c (5-bit Number, MINIMAL_FITNESS_NUMBER=31) | Converged to (1,1,1,1,1) at gen 6. |

One observation: on the default queens run (`POPULATION_SIZE=4`,
`MUTATION_RATE=0.05`, `MAX_GENERATIONS=100`), about 1-in-5 runs
plateau and hit MAX_GENERATIONS without converging — exactly the
"premature convergence" regime variant 1's acceptance criterion
calls out. The acceptance criterion explicitly allows "explain via
KNOB inspection why convergence plateaued"; the GA's printout now
makes the plateau visible by emitting "MAX_GENERATIONS (N) hit
without reaching target fitness F." Bumping `POPULATION_SIZE` to
~20 or `MUTATION_RATE` to ~0.15 reliably hits 0 within 200
generations.

---

## Out-of-scope observations (not addressed)

These reviewer findings were NOT addressed because the brief did
not list them:

- R1 P1-4 (MAX_GENERATIONS_NUMBER KNOB comment "pre-empts" variant
  4c) — KNOB doc softened slightly during the rewrite, but the
  variant-bank text itself was not touched.
- R1 P2-1 through P2-8 (cosmetic polish).
- R2 P1-1 through P1-10 (most addressed transitively; some
  knob-proliferation concerns remain — e.g.
  `NUMBER_MUTATION_BIT_RATE` and `QUEENS_MUTATION_COLUMN_RATE` are
  still separate knobs from `MUTATION_RATE`, by design).
- R3 P1-1 through P1-9, all P2s (most addressed transitively
  during the broader rewrite; some, like P1-3 "slide-42 worked
  example smoke test", are explicit future work).
- R4 P1-1 through P1-7, all P2s (renames addressed; some doc
  cross-references e.g. variant 1's "30 → 200" wording would need a
  `variants.md` edit, which was not in scope — the source-side
  defaults are now reasonable for either reading).
- The `variants.md` file itself was NOT edited. The brief offered
  "either rename to match variants.md OR update variants.md"; the
  rename-source path was taken, which keeps `variants.md` as the
  canonical contract.

---

## Concerns / risks

1. **Default `MUTATION_RATE = 0.05` makes default 4-queens runs
   stochastic.** With population 4 and 100 generations, ~20% of
   runs plateau. Variant 1 acceptance permits this (the "explain
   via KNOB inspection" fallback). If a future gate wants
   deterministic-convergence-on-defaults, bump
   `MAX_GENERATIONS = 200` and `POPULATION_SIZE = 20`.

2. **`reproduce` contract change is breaking.** Any external code
   importing the original `Number.py`/`Queen.py` `reproduce(other)
   -> Self` signature will break. This is the intended slide-faithful
   alignment, but worth flagging if the grader runs original
   template tests.

3. **`pick_individual` signature change is breaking.** Any
   external caller relying on the optional `shifted_fitnesses`
   parameter will need to provide it. In-tree callers updated;
   external callers (none known) will not be.

4. **No automated test suite.** The smoke-test in
   `queens_fitness_solution.py` now asserts, but the GA loop has
   no test pinning the slide-42 worked example. Reviewer R3 P1-3
   recommended adding one; the brief did not require it.

---

## What PM should do next

1. Re-dispatch QA Inspector (round 2) against the patched solution
   set.
2. If QA passes, run the exam-agent gate against the three
   mandatory variants in `variants.md`. All KNOB names now match
   the canonical short forms (`POPULATION_SIZE`, `MUTATION_RATE`,
   `MAX_GENERATIONS`, `TRIM_POPULATION`) per the variant bank's
   spec.
3. If the gate flags anything related to the default
   `MUTATION_RATE = 0.05` causing plateaus, the simplest fix is to
   amend `variants.md` Variant 1's recipe to also nudge
   `MUTATION_RATE` to 0.1 (already mentioned in the
   ga_solution.py HOW-TO-ADAPT block). Source-side defaults stay
   lecture-canonical.

**DOCUMENT.md updated:** N/A — study repo, no DOCUMENT.md in
`handout_lab_4/`.

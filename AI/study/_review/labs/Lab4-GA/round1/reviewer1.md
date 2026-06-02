# Lab4-GA Round 1 — Reviewer #1 (Correctness)

**Assignment recap:** Lab 4 — Genetic Algorithm (Number exercise + N-Queens homework). Reviewing the locked solution against the slide-shipped templates in `handout_lab_4/ga.py`, `Number.py`, `Queen.py`, `queens_fitness.py`, the Lab 4.pdf handout (slides 1–18), and `study/_exam/Lab4-GA/variants.md`.

**Files reviewed (absolute paths):**
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\ga_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\Number_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\Queen_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\queens_fitness_solution.py`

**Verification I performed (live, not just by reading):**
- `py -3.12 ga_solution.py` — three independent runs, all converged.
  - Number demo: every run converged to `(1, 1, 1)` with fitness 7 within 1–3 generations.
  - N-Queens demo: every run converged to a fitness 0 board (`(3, 1, 4, 2)` twice, `(2, 4, 1, 3)` once) within 5–20 generations and well under 1 second.
- `py -3.12 queens_fitness_solution.py` — slide-14 boards score `(5,6,2,3,5,8,6,1) → -6` and `(7,3,6,6,4,6,8,1) → -7`, matching the slide labels exactly. The perfect 4-queens board `(2,4,1,3)` scores 0 negative / 6 positive / 0 weighted-3x — all internally consistent.
- Manual edge tests: gene-length-1 reproduce/mutate behave; positive-fitness variant returns the correct `n*(n-1)/2 = 6` for `(2,4,1,3)`; empty-population path is guarded by `genetic_algorithm`.

---

## VERDICT: **PASS WITH CONCERNS**

The solution is functionally correct. Both demos converge reliably and the slide-14 fitness reference values match to the digit. The roulette-wheel + shift-by-`(-min + 1)` trick is the right generalisation for the negative-fitness queens variant — it strictly preserves selection pressure on the positive Number landscape (because the shift becomes "+1" uniformly) while remaining well-defined on the negative landscape (because every shifted weight is ≥ 1, so the worst individual is *not* dead-weight, which matches the slide-6 spirit where every individual has a non-zero slot). Mutation, crossover, hashing, equality, and the union-then-trim policy all line up with the slide-2 pseudocode line-for-line.

However: there are three concerns worth flagging before this is locked, and one is *almost* a P0 in the sense that it changes the GA's behaviour relative to the slide-shipped template even though it doesn't break convergence. Read the P1 block carefully.

---

## P0 — MUST FIX (blocks shipping)

**None.** I could not find a correctness bug that prevents either demo from converging or that misreports a slide-stated fitness value.

---

## P1 — SHOULD FIX (correctness-adjacent, behaviour-altering, or contract drift)

### P1-1. `random_selection` uses `(-min + 1)` shift even when fitnesses are already strictly positive — silently changes selection proportions from the slide-6 walkthrough.

**File:** `ga_solution.py` lines 469–480.

The slide-6 walkthrough table is the canonical roulette example: the four individuals have fitness `6, 4, 2, 0` with total `12`, so the `(1,1,0)` individual gets `6/12 = 50 %` of the wheel and `(0,0,0)` gets `0/12 = 0 %`. **That is a slide-stated property of the exercise** — slide 6 explicitly draws the `(0,0,0)` slot as having *zero* width.

The solution shifts *every* fitness by `(-min + 1)`. For the slide-6 population the min is 0, so the shift is `+1`, and the weights become `7, 5, 3, 1` with total `16`. Now `(1,1,0)` gets `7/16 = 43.75 %` and `(0,0,0)` gets `1/16 = 6.25 %`. The all-zero individual is no longer a dead chromosome — it can be picked, can become a parent, and the slide-6 numbers in any exam handout-walkthrough rendering will not reproduce.

The docstring on lines 462–469 *claims* "the SLIDE-FAITHFUL behaviour is preserved when all fitnesses are already ≥ 0 (the shift becomes '+1' and proportions are unchanged up to a constant)". **That last clause is false.** Multiplying all weights by a constant preserves proportions; **adding** a constant does not. With weights `6,4,2,0` proportions are `6:4:2:0`; after adding 1 they are `7:5:3:1`, which is a strictly different distribution (the worst individual's share rose from 0 to 1/16; the best individual's share fell from 1/2 to 7/16).

**Why this is P1 not P0:** convergence is not affected (every demo run hit the optimum well within the generation budget). The slide-6 *table* is illustrative, not load-bearing for the algorithm. But the docstring asserts a property the code does not have, and the exam variants in `study/_exam/Lab4-GA/variants.md` may ask students to reproduce slide-6 numbers; if so, this solution will produce different proportions and any student-comparison will not match.

**Suggested fix.** Either (a) only shift when `min_fitness < 0` (then the slide-6 case truly is unchanged), or (b) drop the "+1" component when `min_fitness >= 0` so the shift is a pure floor-to-zero rather than a strict-positivity guarantee. The cleanest version:

```python
shift = max(0, -min_fitness)
shifted = [f + shift for f in fitnesses]
# Guard for the all-equal-fitness-0 case so we don't divide by zero:
if sum(shifted) == 0:
    shifted = [1.0] * len(shifted)
```

Document the conditional shift in the docstring so the "(1,1,0) gets 50 %" walkthrough is reproducible.

---

### P1-2. `pick_individual` fallback path (when `shifted_fitnesses is None`) is broken for any negative-fitness population — silently degrades to uniform selection.

**File:** `ga_solution.py` lines 483–520.

The fallback path on lines 499–508 recomputes weights as `[ind.get_fitness() for ind in ordered_population]` — i.e. *raw* fitness, no shift. For the negative-fitness queens variant every weight is ≤ 0, so the `if total_fitness_sum <= 0: return random.choice(...)` branch fires and we get *uniform* selection. That is silently worse than roulette-wheel and breaks the "fitness-proportionate" property the GA is supposed to demonstrate.

**The current callers in `random_selection` always pass `shifted_fitnesses`, so the bug is unreachable from the entry-point demos.** But:
- The function is module-public (no leading underscore).
- The docstring explicitly invites callers to omit `shifted_fitnesses` ("The argument is optional so callers that do not need the shift … can omit it and the function still works").
- An exam variant that asks students to "compute the roulette wheel by hand using `pick_individual`" on a negative-fitness population will silently get the wrong answer.

**Why P1 not P0:** unreachable from the GA loop today. But the public contract is wrong, and the docstring claim is wrong, so this will bite future use.

**Suggested fix.** Either (a) shift inside the fallback path the same way `random_selection` does, or (b) make `shifted_fitnesses` required (drop the default-None and the fallback branch entirely; callers already always provide it).

---

### P1-3. `genetic_algorithm` returns `fittest_individual = None` when `num_of_generations <= 0`, even though `population` is non-empty.

**File:** `ga_solution.py` lines 384–429.

`fittest_individual` is initialised to `None` on line 388 and only assigned inside the `for generation in range(num_of_generations):` loop on line 420. If a caller passes `num_of_generations=0` (perfectly legal — "how does the GA do with no generations of work?" is a sensible exam question), the loop body never executes and the function returns `None` despite the input population being well-formed.

The Number original `Number.py` and the Queen template `Queen.py` both implicitly assume `num_of_generations >= 1`. But the slide-2 pseudocode framing — "For generation in (0..N): …" — does not forbid N=0, and a zero-generation run *should* return the fittest of the initial population.

**Suggested fix.** Initialise `fittest_individual = get_fittest_individual(population)` immediately after the `if not population: return None` guard. Then the loop body's reassignment overrides it, and the zero-generation case still returns a sensible result.

Also: the `print(f"Final generation {generation}:")` on line 426 reads `generation` from the loop variable. When the loop body never executes, `generation` is bound on line 387 to 0 — that line is currently dead code unless `num_of_generations >= 1`, but it would print `Final generation 0:` confusingly. Combined with the above fix, also guard the "Final generation" print behind `if generation > 0 or num_of_generations > 0` (or similar).

---

### P1-4. `MAX_GENERATIONS_NUMBER` default is 30, but `ga_solution.py`'s `_run_number_demo` is the only caller and it converges in 1–3 generations — the 30 is dead weight; meanwhile the exam variant for "5-bit number" (`study/_exam/Lab4-GA/variants.md` optional 4c) explicitly tests whether 30 still suffices.

**File:** `ga_solution.py` line 171.

Not a bug, but the KNOB comment on lines 169–170 says: *"30 is far more than enough for 3-bit; bump if you enlarged the gene length (5-bit may need ~60, 8-bit ~120)."* I checked: with `NUMBER_GENE_LENGTH = 5` and the default population of 4, the GA *can* converge inside 30 generations but the optional-4c variant expects students to *fail* convergence at the default and then bump. The KNOB comment pre-empts the variant by telling the student the answer.

**Suggested fix.** Either soften the KNOB comment ("may need bumping for larger gene lengths") or rephrase the variant to ask about a less-pre-empted parameter. This is a soft contract issue between the solution and the variant bank, not a code bug.

---

### P1-5. `_run_queens_demo` does not print the generation at which convergence happened — variant 1 explicitly asks for this.

**File:** `ga_solution.py` lines 585–613; variant 1 acceptance criterion in `study/_exam/Lab4-GA/variants.md` line 28.

Variant 1 says: *"Report … 3. The generation at which it converged (or whether MAX_GENERATIONS was hit first)."*

The current demo prints the fittest individual and elapsed milliseconds but does not surface the convergence generation. A student running this verbatim and pasting the output cannot answer the variant-1 acceptance question.

**Why P1:** the slide-shipped `ga.py` doesn't print this either, so this is the solution inheriting a template gap rather than introducing a new one. But the variant bank assumes the solution surfaces it.

**Suggested fix.** Have `genetic_algorithm` also return the generation index it stopped at (or expose the inner `generation` via a mutable container the caller supplies), and have `_run_queens_demo` print it.

---

## P2 — POLISH / MINOR

### P2-1. `pick_individual` parameter `total_fitness_sum` is silently overwritten when `shifted_fitnesses is None`.

**File:** `ga_solution.py` lines 499–503. If a caller passes a meaningful `total_fitness_sum` but forgets `shifted_fitnesses`, line 503 throws their value away. Not a bug — just a confusing signature.

### P2-2. `genetic_algorithm` `generation` variable shadow.

**File:** `ga_solution.py` lines 387, 390. `generation: int = 0` on line 387 is shadowed by the `for generation in range(...)` loop variable on line 390. The outer binding is only meaningful if the loop body never executes (see P1-3). Rename one of them or remove the outer one once P1-3 is addressed.

### P2-3. `print_population` calls `get_fittest_individual` even for the "too large to print" summary, which re-traverses the population.

**File:** `ga_solution.py` lines 441–445. After the GA loop already computed `fittest_individual` on line 420, the next-generation print recomputes the same `max(population)` inside `print_population`. Tiny perf hit; for the 100-element 8-queens variant it doubles per-generation traversal cost. Cache the fittest on the GA loop side and pass it in.

### P2-4. `NumberIndividual.mutate` when `NUMBER_MUTATION_BIT_RATE < 1.0` returns a clone of self — pointless allocation.

**File:** `Number_solution.py` lines 234–235. Returning `self` directly would be safe because individuals are immutable value objects (the docstring says so on line 226). The new instance is added to the set on line 410 of `ga_solution.py` and immediately collapses into the existing entry via `__hash__`/`__eq__`, but the allocation still happens. Cosmetic.

### P2-5. `Board.mutate` does not exclude the current row when picking a new row — possibility of "mutation" that doesn't change the gene.

**File:** `Queen_solution.py` lines 252–254. With probability `1/n` the random new row equals the existing one, producing a no-op mutation. The docstring on lines 248–250 acknowledges this is intentional ("We do NOT exclude the current row — the slides don't either"), but it does make convergence speed slightly worse on small boards. Not a bug.

### P2-6. `Number_solution.NumberIndividual.__eq__` returns `NotImplemented` for non-`NumberIndividual` comparisons; `Queen_solution.Board.__eq__` does the same. Good. But neither defines `__ne__` — that's fine in Python 3 (auto-derived from `__eq__`) but worth a comment.

### P2-7. Slide-14 example boards are not used as a doctest / unit test.

**File:** `queens_fitness_solution.py` lines 196–204. The `_smoke_test` exercises the slide-14 boards manually but only when the file is run as `__main__`. There's no assertion; a future refactor that breaks `fitness_fn_negative` would not fail any test — it would just print different numbers. Convert to `assert neg == -6, …` and `assert neg == -7, …` so a regression actually crashes.

### P2-8. The N-Queens demo at the default `N_QUEENS = 4` runs with `POPULATION_SIZE_QUEENS = 4`, but the slide-shipped `Queen.py.main()` passes `8` to `get_initial_population`. The semantic confusion ("is 8 the population size or the board size?") is resolved in the docstring on lines 209–215, but the *default* picked here diverges from the slide-shipped default. An exam variant that asks "reproduce slide-shipped behaviour" needs the student to change a KNOB.

Not a bug — documented — but the divergence costs a KNOB-change for any "reproduce slide defaults" variant.

---

## QA Checklist (§7 of Plan) status

The Lab4-GA plan was not located in `PM/` (`PM/` folder doesn't exist for this project — this is a study repo, not a feature repo), so I'm running against the generic standing checks plus the variant bank:

- **Scope compliance (Plan §1):** N/A — no Plan §1. The solution stays within what slides 1–18 ask for plus the documented exam-variant knobs.
- **Bugs (standing check):** No P0 bugs found. P1-1, P1-2, P1-3 are correctness-adjacent concerns documented above.
- **Security (Plan §6):** N/A — no user input, no I/O, no network. Pure-function exercise.
- **Performance:** Acceptable. 4-queens converges in <100 ms; per-generation O(n² · pop) is the queens-fitness inner loop, fine for slide-scale inputs. The `print_population` redundant `max(...)` (P2-3) is the only obvious inefficiency.
- **Accessibility:** N/A — no UI.
- **Convention adherence:** No `PM/conventions.md` available to check against. Type hints, docstrings, and naming are consistent with the slide-shipped template.
- **DOCUMENT.md presence:** No `DOCUMENT.md` exists in `handout_lab_4/`. Per the standing check this is a P1, but this is a study repo and the project never asked for one. **Flagging as N/A** rather than P1 — the global rule presupposes a feature-development context that does not apply here.
- **Tests:** No automated test suite exists for the lab. The `__main__` blocks in `Number_solution.py`, `Queen_solution.py`, and `queens_fitness_solution.py` are smoke tests but contain no assertions (see P2-7).
- **Quality:** No `TODO`, no `// ...rest`, no placeholders. Every `_solution.py` is production-grade — the source originals all had `raise NotImplementedError("…")` stubs and those are all filled in. ✔

## Acceptance criteria (§1) status

Using the variant bank `study/_exam/Lab4-GA/variants.md` as the acceptance proxy:

- **Variant 1 (8-Queens):** KNOBs `N_QUEENS`, `MAX_GENERATIONS_QUEENS`, `POPULATION_SIZE_QUEENS` are all exposed and well-documented. ✔ (Code path verified; convergence generation not auto-printed — see P1-5.)
- **Variant 2 (Mutation-rate tuning):** `P_MUTATION` is exposed; `RANDOM_SEED` is exposed. ✔
- **Variant 3 (Positive fitness):** `QUEENS_FITNESS_VARIANT = "positive"` is exposed; `MINIMAL_FITNESS_QUEENS` is exposed and documented to need lifting to `n*(n-1)/2`. ✔ (Verified live: `Board((2,4,1,3))` under positive variant returns 6.0 = n*(n-1)/2 = 6.)

## DOCUMENT.md audit

- `handout_lab_4/` — **no DOCUMENT.md**. Flagged as N/A per the QA Checklist analysis above (study repo, not feature repo).

## Out-of-scope observations

- The original `Queen.py` has a buggy `create_random` that always seeds with `(1,2,3,4,5,6,7,8)` before overwriting — works only because every index is overwritten, but ships as fragile. The solution fixed this (line 302 of `Queen_solution.py`).
- The original `queens_fitness.py` `fitness_fn_positive` has a documented bug (off-by-one in the inner `range(1, col + 1)` loop — should be `range(col)` for non-conflict counting). The solution sidesteps this by deriving the positive count from the negative count (`Queen_solution`/`queens_fitness_solution.py` line 148: `total_pairs - conflicts`). Good catch.
- The original `Queen.py` imports `from Lab4.ga` and `from Lab4.queens_fitness` — i.e. expects a `Lab4` package wrapping. The solution dropped the package prefix and imports directly. Documented difference, not a bug, but means the original `Queen.py` cannot be run as-is from the handout directory; the solution can.

## Concerns / risks

- **P1-1 is the one I'd push back on if I were the gate reviewer.** The docstring promises "proportions are unchanged up to a constant" and that is mathematically false for an additive shift. If the exam-agent gate is comparing slide-6 roulette percentages against the solution's behaviour, this will diverge.
- **P1-2 is a latent footgun.** Today's callers are safe; tomorrow's may not be.
- The solution layers a lot of KNOBs on top of the slide-shipped algorithm. That's fine for an exam-variant-bank-driven study repo, but the `random_selection` shift logic gets harder to reason about as a consequence — and that's exactly where the P1-1 bug lives. The KNOB-explosion strategy traded simplicity for variant-coverage in a way that obscured a verifiable algebraic claim.

## What PM should do next

1. **Fix P1-1** by making the shift conditional on `min_fitness < 0` (or document the docstring's claim as wrong and let the proportions drift). This is the only one that affects a slide-faithful walkthrough.
2. **Fix P1-2** by either shifting in the fallback path or making `shifted_fitnesses` required.
3. **Fix P1-3** by initialising `fittest_individual = get_fittest_individual(population)` before the loop.
4. (Optional) **Address P1-4 and P1-5** if the variant-bank gate is strict about pre-emption and convergence-generation reporting.
5. Re-dispatch QA against the patched solution; the demo runs themselves do not regress (already verified live three times).
6. Then proceed to App Tester (or, since this is a non-UI study repo, to the exam-agent gate directly).

**DOCUMENT.md updated:** N/A for QA.

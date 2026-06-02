# Lab4-GA — Exam Variant Bank

This file is the curated list of exam-style variants for the GA / N-Queens
lab. Each variant is a self-contained "exam question" that an examining
agent (or a student) must answer using **only**:

- the header docstring of `ga_solution.py`,
- the `# KNOB:` comment blocks in `ga_solution.py`,
  `Number_solution.py`, `Queen_solution.py`,
  `queens_fitness_solution.py`,
- the function signatures (`def` lines) of those files.

No reading the function bodies, no reading the lab handout PDF, no reading
the L05 lecture.

The exam-agent gate (spec §8.2) runs **three** of these variants in
parallel against the locked solution; all three must report `SOLVED`.

---

## Variant 1 — N-Queens scaling (8-Queens)

**Question.** The default solution solves the 4-Queens problem. Change
the KNOBs so the same script solves the **8-Queens** problem instead.
Run the modified solution and report:

1. The fittest individual found (the gene tuple).
2. Its fitness value (should reach 0 if a full solution is found, since
   the negative-conflicts fitness is maximised at 0).
3. The generation at which it converged (or whether
   `MAX_GENERATIONS` was hit first).

**Expected KNOB changes.**

- `N_QUEENS` from 4 to 8.
- `MAX_GENERATIONS` may need bumping (e.g. from 30 to 200 or 500) so the
  larger search space has time to converge — exam variant relies on the
  KNOB documentation saying so.
- `POPULATION_SIZE` may need bumping (e.g. from 4 to 50–100) so a wider
  search front explores the larger landscape.
- `MUTATION_RATE` is fine at the default but documentation should
  describe its effect.

**Acceptance.** Reports a concrete gene tuple of length 8 with fitness
0 (no conflicts) OR explains via KNOB inspection why convergence
plateaued and reports the best fitness reached.

---

## Variant 2 — Mutation-rate tuning

**Question.** With `N_QUEENS = 6`, compare two runs of the solver:

- Run A: `MUTATION_RATE = 0.01` (very low; the GA relies mostly on
  crossover).
- Run B: `MUTATION_RATE = 0.5` (high; near-random walk).

Report the best fitness reached by each run within the same
`MAX_GENERATIONS`. Briefly comment on why one converges faster or gets
trapped at a local optimum.

**Expected KNOB changes.**

- `N_QUEENS` from 4 to 6.
- `MUTATION_RATE` first to 0.01, then re-run with 0.5.
- Optionally bump `MAX_GENERATIONS` to give the low-mutation run a fair
  shot.
- Use `RANDOM_SEED` to pin a seed for reproducible comparison.

**Acceptance.** Two best-fitness numbers (one per setting) plus a
sentence explaining low vs high mutation tradeoff using vocabulary from
the KNOB blocks ("exploration", "premature convergence", "near-random
walk").

---

## Variant 3 — Alternative (positive) fitness function

**Question.** The default uses the *negative-conflicts* fitness (zero is
perfect, lower is worse). The `queens_fitness_solution` module exposes
**both** the negative and positive variants. Switch the solver to use
the positive-non-conflicting-pairs variant and re-run 4-Queens. Report
the fittest individual and its fitness, and explain (one sentence) why
the *target* (`MINIMAL_FITNESS_QUEENS`) changes when the fitness
direction flips.

**Expected KNOB changes.**

- `QUEENS_FITNESS_VARIANT` from `"negative"` to `"positive"`.
- `MINIMAL_FITNESS_QUEENS` from `0` (the negative-fitness optimum) to
  `n*(n-1)/2` for an n-queens board (= 6 for n=4) — the positive
  fitness maximum equals the number of distinct pairs of queens.

**Acceptance.** Reports a concrete gene tuple, the positive fitness it
achieved, and one sentence linking the new target to `n*(n-1)/2`.

---

## Optional extras (not part of the gate, useful for self-practice)

- **4a.** Increase `POPULATION_SIZE` from 4 to 100 and `N_QUEENS` to 8.
  Does convergence happen in fewer generations? Why? (Bigger
  population = broader sampling per generation = fewer generations but
  more work per generation.)
- **4b.** Trim the population each generation by setting
  `TRIM_POPULATION = True` and `MAX_POPULATION_SIZE = 30`. Does the
  solver still converge? How does it affect generation count?
- **4c.** Swap the 3-bit Number problem for a 5-bit one
  (`NUMBER_GENE_LENGTH = 5`, `MINIMAL_FITNESS_NUMBER = 31`) — does the
  same `MAX_GENERATIONS_NUMBER` still suffice? Why or why not?

The Lab Solver may add up to 2 additional variants here if the handout
suggests them; current count = 3 mandatory + 3 optional.

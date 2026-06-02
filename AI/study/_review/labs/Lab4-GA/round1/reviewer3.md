# Lab4-GA Round 1 — Reviewer #3 (Pedagogical Clarity)

**Assignment recap:** Review `handout_lab_4/*_solution.py` for pedagogical clarity against `study/lectures/L05-Local-Search.md`. Be harsh — this is a study aid for an exam student, not production code, and pedagogical defects are first-class bugs.

**Status:** **Fail** (Pass with concerns is too charitable — the divergence between the solution and the lecture's GA pseudocode is severe enough to mislead a student studying from both side-by-side, and the docstring marketing is so heavy that the actual lessons are buried.)

---

## P0 findings (correctness/pedagogy bugs that will actively MISLEAD a student studying this lab next to L05)

### P0-1 — The GA loop produces ONE child per crossover; the lecture is explicit that the canonical GA produces TWO

**Location:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout_lab_4\ga_solution.py:402-410` and the entire `random_selection` / `reproduce` contract.

**The lecture says** (L05 §3.6.2, §4.3, §5.7, §8.3):

- `SINGLE-POINT-CROSSOVER(p1, p2)` returns `(child1, child2)`.
- The pseudocode in §4.3 is explicit: `(child1, child2) ← single_point_crossover(parent1, parent2)` then `mutate` each, then `append child1, child2 to new_population`.
- The §8.3 cheat-sheet stanza is identical: select two parents, produce TWO children, mutate each.
- §5.7 slide-43 worked example shows BOTH offspring being produced and BOTH being mutated.
- §3.6 selection note: *"To produce one pair of parents for one crossover event, spin the wheel twice independently. This is the single most common GA implementation bug."*

**The solution does** something fundamentally different: it iterates `for _ in range(len(population))` and in each iteration calls `mother.reproduce(father)` which returns ONE child (`return type(self)(child_gene)` in `NumberIndividual.reproduce`, and one of `left_child`/`right_child` in `Board.reproduce`). The "other child" is thrown away.

**Why this is P0, not P2:** a student running through the slide-43 worked example by hand and then reading this code will conclude they have a bug — they don't, the code is just implementing a *different* algorithm. The docstring at `Queen_solution.py:25-29` even acknowledges the gap *("the GA driver consumes one child per parent pair, so this Board.reproduce returns one of the two possible children at random")* but doesn't reconcile it. The honest thing would be to either:
  - (a) Change `reproduce` to return a tuple of two children and rewrite the driver loop to consume both, matching the lecture verbatim, OR
  - (b) Put a screaming-loud DEVIATION FROM LECTURE box at the top of `ga_solution.py` explaining "we run the loop `len(population)` times so each iteration produces one child; the lecture runs `len(population)/2` times and each iteration produces two — algebraically equivalent in expected output, but if you trace by hand from the slide-42 / slide-43 example you must use the lecture loop, not this code".

**Suggested fix:** rewrite the driver loop to match §4.3 verbatim (two children per pair, halve the loop count). The "one child" framing is a *worse* GA because it discards information for no reason — and it disagrees with the lecture cheat-sheet that students will revise from.

---

### P0-2 — `random_selection` returns BOTH parents in one call; the lecture is explicit that selections are TWO INDEPENDENT spins of the wheel, and emphasises this as the most-common-bug warning

**Location:** `ga_solution.py:455-480`. The function returns `(mother, father)` — sampled by two calls to `pick_individual`, so technically independent — but the name `random_selection` returning a pair (rather than the lecture's `roulette_wheel_select` returning ONE individual) directly contradicts the lecture's framing.

**The lecture says** (L05 §3.6, §4.3, §8.3):

- §3.6: *"To produce one pair of parents for one crossover event, spin the wheel twice independently — once for Parent 1 and once for Parent 2. This is the single most common GA implementation bug: spinning once and reusing the parent."*
- §4.3 pseudocode: `parent1 ← roulette_wheel_select(population, fitness)` then `parent2 ← roulette_wheel_select(population, fitness)` — two separate named calls.
- §8.3: "roulette-select parents (spin twice)".

**Why this is P0:** the lecture goes out of its way to call out exactly the bug pattern this function's *signature* normalises. A student who memorises this code's API as "the correct shape of selection" will write `mother, father = select(pop)` on the exam and get docked, because the canonical answer is "call selection twice independently". The current implementation is *behaviourally* correct (two independent `pick_individual` calls) but *pedagogically* it teaches the wrong API.

**Bonus pedagogical sin:** the lecture function is named `roulette_wheel_select`. The solution calls it `random_selection`, which is a *weaker* name that does not telegraph the roulette-wheel mechanism. Slide 6 of the handout PDF is literally titled "Fitness ratio" and the lecture glossary entry is "roulette-wheel selection". Strip the word from the function name and the connection to slide 6 vanishes.

**Suggested fix:** rename to `roulette_wheel_select(population) -> Individual` (singular), make it return ONE parent, and call it twice in the driver. The docstring then writes itself: "this is the §3.6.1 procedure; call it twice independently per generation".

---

### P0-3 — `pick_individual` argues for the fitness-shift trick incorrectly; the math claim "proportions are unchanged up to a constant" is FALSE

**Location:** `ga_solution.py:469-475` docstring of `random_selection`:

> *"With this shift the SLIDE-FAITHFUL behaviour is preserved when all fitnesses are already ≥ 0 (the shift becomes "+1" and proportions are unchanged up to a constant)."*

**The lecture says** (L05 §3.6.1 worked example with chromosome fitnesses `1, 2, 3, 1, 3, 5, 1, 2`):
- Chromosome 6's slice is `(10, 15]`, width 5 out of total 18 → P[pick] = 5/18 ≈ 0.278.

If you apply the shift `f → f - min + 1 = f + 0` (since min is 1) ... no, wait, min is 1, so shift is `f - 1 + 1 = f`. OK, slide example is unaffected.

But the docstring's general claim *"proportions are unchanged up to a constant"* is **mathematically wrong**. Roulette-wheel proportions are `f_i / Σ f_i`. Adding a constant `k` to every fitness gives `(f_i + k) / (Σ f_i + N·k)`. These are NOT proportional to the original `f_i / Σ f_i` unless `k = 0`. With `k = 1` and the example `[1, 2, 3, 1, 3, 5, 1, 2]` (min=1, so shift adds +1 to each): new weights `[2, 3, 4, 2, 4, 6, 2, 3]`, new total = 26, P[pick chrom 6] = 6/26 ≈ 0.231 — NOT 5/18 ≈ 0.278.

**Why this is P0:** a student trying to reconcile their slide-42 hand trace ($R \in (10, 15] \Rightarrow$ chromosome 6) with this code will be silently working with a different distribution because of the `+1` shift. The function will *almost certainly* still pick chromosome 6 in expectation, but the docstring's reassurance that "proportions are unchanged" is a lie that hides the discrepancy.

**Suggested fix:** delete the false claim. The honest version is: *"Adding a constant `+1` to every fitness produces a strictly different distribution (it pulls all selection probabilities toward uniform). We accept this small distortion because it preserves the *ranking* and makes negative fitnesses safe; we deviate from the slide-42 example by an arithmetic constant. Do not use this implementation to reproduce the slide-42 numerical answer — use the cumulative-sum formulation in §3.6.1 of the lecture for that."*

---

### P0-4 — `genetic_algorithm` does `population ← population ∪ new_population` instead of `population ← new_population`; this is a (μ + λ) variant, NOT the (μ, λ) generational GA the lecture describes

**Location:** `ga_solution.py:415` — `population = population.union(new_population)`.

**The lecture says** (L05 §3.6 "Replacement" paragraph, §4.3, §8.3):

- §3.6: *"After repeating selection + crossover + mutation until you have $N$ offspring, this set of $N$ offspring **is the new generation**. The old population is then discarded (generational GA, the lecture form) or merged with the offspring and truncated by fitness (steady-state GA)."*
- §4.3 pseudocode line: `population ← new_population` (just assign, do not union).
- §8.3 stanza: `population ← children` (same).

**The solution does:**

```python
population = population.union(new_population)   # line 415
if should_trim_population: population = trim_population(...)  # line 417-418
```

The solution's own docstring (lines 380-383) labels this *"closer to the textbook '(μ + λ)' variant"*. Cool — but the LECTURE explicitly distinguishes generational GA (the lecture form) from steady-state (merge + truncate), and the solution silently picks the non-lecture variant **by default** (`SHOULD_TRIM_POPULATION = False`).

The combination of "union, do not trim" means the population GROWS UNBOUNDEDLY across generations — for the queens demo with population size 4 over 100 generations, the working set could swell to hundreds of unique boards before set deduplication helps. That's not just a deviation; it's a *different time-complexity profile* than the lecture's $O(NF)$ per generation. Per the lecture's complexity calculation in §4.3, the per-generation cost should be $O(NF)$ with constant N. Here it's $O((\text{accumulated unique set})·F)$ — strictly larger and growing.

**Why this is P0:** if a student is asked on the exam "what is the per-generation cost of a GA?", they should answer $O(NF)$. If they revise from this code they'll be looking at a quadratic-ish curve and wondering why their answer is being marked wrong.

**Suggested fix:** flip the default. Make `population = new_population` the default (matching §4.3) and gate the union behaviour behind a knob like `USE_MU_PLUS_LAMBDA = False`. Then update the docstring to *open* with "this code defaults to the §4.3 generational GA. The (μ + λ) variant is available behind a knob."

---

### P0-5 — `_run_number_demo` uses the **hard-coded slide-5 population** which CONTAINS the perfect chromosome (1, 1, 1) ... no wait, it doesn't. But the docstring claim about slide-11 is wrong.

**Location:** `Number_solution.py:46-66` and `Number_solution.py:145-150`.

The docstring at `Number_solution.py:55-57` claims:

> *"4. To make the perfect individual unavailable in the start state (slide 11 caveat: 'make sure the perfect individual is not in the initial population'): leave the hard-coded population as-is — (1,1,1) is absent from it by design."*

OK — for the slide-10 target `(1, 1, 1)`, the hard-coded population `{(1,1,0), (0,0,0), (0,1,0), (1,0,0)}` does indeed lack `(1,1,1)`. Fine for slide 10.

But for **slide 11** (NUMBER_TARGET=4 → target gene `(1, 0, 0)`), the hard-coded population *contains* `(1, 0, 0)` — the perfect chromosome IS in the initial population. So setting `NUMBER_TARGET = 4` *without also changing the initial population* will make the GA terminate at generation 0 because the perfect individual already exists. The docstring claim "(1,1,1) is absent from it by design" is technically true but is the **wrong** absence to brag about — what slide 11 cares about is `(1, 0, 0)`'s absence, and `(1, 0, 0)` is PRESENT.

**Why this is P0:** the entire point of slide 11's caveat is to make the GA actually demonstrate convergence. A student following this docstring will set `NUMBER_TARGET = 4`, run the demo, see "Fittest Individual: Gene: (1, 0, 0) - Fitness: 7" at generation 0, and think they've reproduced slide 11 successfully. They have not — they've shown that a population which already contains the answer is "solved" in zero generations, which proves nothing.

**Suggested fix:** add an explicit guard: when `NUMBER_TARGET` is set and the hard-coded population contains the perfect chromosome, either (a) print a loud warning, (b) auto-swap in a sanitised population that excludes the target, or (c) at minimum fix the docstring to actually warn about this rather than pretending the hard-coded set is safe.

---

### P0-6 — Mutation in `NumberIndividual` is **always exactly one bit flip**, NOT the lecture's per-gene-with-probability-m

**Location:** `Number_solution.py:220-239`.

**The lecture says** (L05 §3.6 "Mutation", §3.6.2, §5.7 slide-44, §8.3):

- §3.6.2 pseudocode: `MUTATE(chromosome, m): for i in 1..length(chromosome): if random() < m: chromosome[i] ← flip(chromosome[i])`. **Every** bit gets an independent coin flip; multiple bits can mutate at once.
- §5.7 slide-44 worked example: Offspring 1 → ONE bit flips; Offspring 2 → ONE bit flips. The lecture is showing that **with low $m$**, typically one (or zero) bit flips per chromosome, but in principle multiple can.

**The solution does:** `idx = random.randint(0, len(self.gene) - 1); flipped = 1 - self.gene[idx]` — picks exactly ONE bit and flips it. There is no per-bit probability check. The outer `P_MUTATION` gate decides whether mutation happens *at all*; if it does, exactly one bit flips.

**Why this is P0:** a student reading §3.6.2's pseudocode and this code side-by-side will see a structurally different operator. The per-bit-with-probability-m formulation is what the slide-44 worked example *exemplifies* (it just happens that one bit flipped in each offspring at $m \approx 0.1$). The "always exactly one bit" formulation is what the **handout PDF slides** seem to specify, but the lecture L05 *deliberately* presents the per-bit version because that's the formulation that generalises.

The KNOB `NUMBER_MUTATION_BIT_RATE` exists but means something completely different from $m$: it's the probability that mutation happens AT ALL given that the outer `P_MUTATION` gate fired. The docstring at line 123-124 says *"this gives effective bit-flip rate `p_mutation * NUMBER_MUTATION_BIT_RATE / GENE_LENGTH per bit`"* — that formula is wrong even for the implementation: if the outer gate fires (prob `p_mutation`) AND the inner gate fires (prob `NUMBER_MUTATION_BIT_RATE`), then **one specific bit** flips with probability `1/GENE_LENGTH` (it's uniformly chosen). The "per-bit flip probability" is `p_mutation * NUMBER_MUTATION_BIT_RATE / GENE_LENGTH` only in expectation over many calls — but the actual per-call behaviour is "either no flip or exactly one flip", which is a fundamentally different distribution from the lecture's "each bit independently".

**Suggested fix:** add a true per-bit mutation mode controlled by a `NUMBER_MUTATION_MODE` knob (`"single_bit"` for the handout-PDF version, `"per_bit"` for the L05 lecture version), and default to `"per_bit"` to match the lecture. Document the difference explicitly.

---

## P1 findings (important pedagogical or correctness defects, but not algorithm-rewriting)

### P1-1 — The crossover function takes `randint(1, n-1)` and the docstring says "internal cut" — but the lecture's slide-43 cut is "after position 3" (cut point 3 in a 10-bit string) and the lecture pseudocode is `cut ← random integer in [1, L-1]` (which includes both 1 and L-1 inclusive). Verify the off-by-one.

**Location:** `Number_solution.py:258` and `Queen_solution.py:267`.

Python's `random.randint(a, b)` is **inclusive on both ends**. The lecture's `random integer in [1, L-1]` is also inclusive on both ends (mathematician's convention). So `random.randint(1, n - 1)` is correct.

But the docstring at `Number_solution.py:253-254` muddles it:

> *"WHY randint over [1, n-1]: a cut at position 0 would copy `other` verbatim, and a cut at position n would copy `self`."*

For an n=3 gene `(a, b, c)`:
- cut=1 → `self[:1] + other[1:]` = `(a, other_b, other_c)`. ✓ child differs from self.
- cut=2 → `self[:2] + other[2:]` = `(a, b, other_c)`. ✓ child differs from self.
- cut=0 → `self[:0] + other[0:]` = `() + (other_a, other_b, other_c)` = full copy of `other`. The docstring says this is "copying `other` verbatim" — true.
- cut=n=3 → `self[:3] + other[3:]` = `(a, b, c) + ()` = full copy of `self`. The docstring says this is "copying `self`" — true.

OK, the math checks out. **But** the slide-43 example has cut after position 3, meaning Parent 1's prefix is bits 1-3 and suffix is bits 4-10 — i.e. cut=3, and the relevant prefix slice is `[:3]`. With `random.randint(1, n-1)` and n=10, the range is `[1, 9]` inclusive, so cut=3 is reachable. Fine.

**The actual issue:** the docstring should *also* call out that cut=n-1 produces a child that differs from `self` only in the last bit (almost-identity), and cut=1 produces a child that differs from `self` in all but the first bit. These edge-of-range cuts are *technically* valid crossovers but produce minimally-recombined children. The lecture is silent on whether this is fine; some textbooks restrict to `[2, L-2]` for "interesting" cuts. The solution should mention it.

**Suggested fix:** expand the docstring to mention that cut=1 and cut=n-1 produce minimal-recombination children and that this is intentional per the lecture's `[1, L-1]` range.

---

### P1-2 — The lecture's slide-13 hill-climbing `<` vs `≤` discussion is not relevant to GA, but the lab solution should at least mention how GA's *termination condition* maps to the lecture

**Location:** `ga_solution.py:422-423` (`if minimal_fitness <= fittest_individual.get_fitness(): break`) and `ga_solution.py:359-364` docstring.

The lecture's GA termination (L05 §4.3, §8.3) is:
- *"if best fitness in population is 'good enough': return best"* → `>=` target check.
- *"max generations"* → loop cap.

The solution implements exactly this: `<=` from the algorithm's perspective is the same as `>=` from the fitness's perspective. But the docstring never says "this is the §4.3 termination condition" — it just describes the mechanics. A student needs the **link**, not the mechanics.

**Suggested fix:** add a sentence to the `genetic_algorithm` docstring: *"Termination matches L05 §4.3 — stop when best fitness ≥ target OR when `num_of_generations` is exhausted. Neither condition guarantees a globally-optimal answer (no formal completeness claim per the lecture's §4.4 table)."*

---

### P1-3 — None of the solution files explicitly walk through the slide-42 worked example

**Location:** All four `*_solution.py` files.

The lecture spends a full sub-section (§5.7) on the slide-41/42/43/44 worked example: 8 chromosomes with fitnesses `[1, 2, 3, 1, 3, 5, 1, 2]`, $R = 7 \Rightarrow$ chromosome 4, $R = 12 \Rightarrow$ chromosome 6, single-point crossover at cut=3, mutation at bit 6 and bit 3.

A pedagogically excellent solution would include this as a **test case** in a `_smoke_test` block or `if __name__ == "__main__"` demo — pin `RANDOM_SEED`, prefab the population, force the cumulative-sum walk, and print "Selected chromosome: 4 (matches slide-42 expected output)". This is exam-prep gold and is *missing*.

**Suggested fix:** add a `_lecture_smoke_test()` function to `ga_solution.py` that reproduces the slide-42 trace (or fails loudly if the implementation has drifted). This is the single highest-leverage pedagogical addition possible.

---

### P1-4 — The `MENTAL MODEL` blocks are **cute but vague** and don't pull their weight

**Location:** Top of every `*_solution.py` file.

`ga_solution.py:39-46`: *"A GA is *evolution in a bottle*: you stage a tiny ecosystem of candidate solutions ..."* — fine.

`Number_solution.py:29-35`: *"This module is *evolution on the dimmer switch*: each individual is a 3-light dimmer state ..."* — strained. A 3-bit number is not naturally a "3-light dimmer"; it's a binary-encoded integer. The lecture's slide-31 framing ("integer → binary using place values $512, 256, \dots, 1$") is more useful and more transferable. The dimmer analogy adds no insight that isn't already in the §2.D animal-breeding analogy from the lecture.

`Queen_solution.py:42-49`: *"This module is a *chessboard breeding farm*: each Board is a candidate queen-arrangement ..."* — better, but again duplicates the lecture's §2.D analogy without adding insight.

`queens_fitness_solution.py:24-29`: *"This module is the *scoreboard*. It does not play the GA — it tells the GA how good a candidate chessboard is."* — actually useful. Keep this one.

**Suggested fix:** delete the weak analogies; keep the scoreboard one. The lecture's §2.D / §2.E analogies are already strong; the lab files should *cite* them, not invent new ones that compete for student attention.

---

### P1-5 — KNOB docstrings are **excessively long and bury the lecture connection**

**Location:** All four files, but especially `ga_solution.py:117-306` (190 lines of KNOB block before the algorithm even starts).

A student opening `ga_solution.py` to study the GA algorithm has to scroll past 190 lines of KNOB documentation before reaching line 358's `def genetic_algorithm`. This is the opposite of progressive disclosure: the most important thing (the GA loop) is the most-buried thing.

The KNOBs are individually well-documented — explaining what each one does, its range, its effect, and which exam variant uses it. That's good. But pedagogically, the structure should be:

1. **§3.6/§4.3 algorithm-level overview** (the canonical GA loop).
2. **The actual `genetic_algorithm` function** — minimal, slide-faithful.
3. **Knobs and variants** *below the algorithm*, framed as "ways to deviate from the slide-faithful baseline".

Currently it's reversed: knobs first, algorithm last, and the algorithm has to thread through `PRINT_GENERATIONS`, `CROSSOVER_RATE`, `SHOULD_TRIM_POPULATION`, `MAX_POPULATION_SIZE` checks that are extraneous to the lecture's pseudocode. A student who wants to compare line-by-line against §4.3 has to mentally strip these out.

**Suggested fix:** restructure each file. Top → docstring with PROBLEM STATEMENT + MENTAL MODEL + REFERENCES. Middle → core algorithm/class (the lecture-faithful version). Bottom → KNOBs, variants, exam-prep section.

---

### P1-6 — `pick_individual` has a divide-by-zero / all-zero-fitness fallback that returns `random.choice` — the lecture never mentions this case

**Location:** `ga_solution.py:507-508`.

```python
if total_fitness_sum <= 0:
    return random.choice(ordered_population)
```

This is defensive coding (good!) but pedagogically untied. The lecture's §3.6.1 procedure assumes fitnesses are positive; what happens with all-zero fitness is undefined. The fallback to `random.choice` is reasonable but the docstring should connect to the lecture: *"the lecture's §3.6.1 procedure assumes Σf > 0; if all fitnesses are zero (e.g. a degenerate Number gene `(0, 0, 0)` population) the cumulative-sum walk has no information to use, and uniform random selection is the principled fallback."*

**Suggested fix:** add the link to the lecture in the docstring.

---

### P1-7 — `Queen_solution.py:230` `get_fitness` routes through `_score` but does not check the slide-14 example values

**Location:** `Queen_solution.py:230` (`get_fitness` returns `_score(self.gene)`) and `queens_fitness_solution.py:196-204` (smoke test for slide-14 boards).

The smoke test in `queens_fitness_solution.py` correctly hits the slide-14 examples (`(5, 6, 2, 3, 5, 8, 6, 1)` → -6; `(7, 3, 6, 6, 4, 6, 8, 1)` → -7; `(2, 4, 1, 3)` → 0). Good.

But the comment on lines 199-201 says these match "the slide labels 'Fitness: -6' and 'Fitness: -7'". I don't have the handout PDF to verify, and the lecture's §5.5 fig08 (the local-max board) is different from these two boards. The lecture L05 does not specifically validate that these particular boards have those particular fitness values — the lecture's worked example is the slide-41/42 GA (oil-drilling), not the slide-14 n-queens boards.

The slide-14 boards' captions ("-6" and "-7") need to be confirmed against the actual handout PDF. If the captions are right, the smoke test is good. If they're wrong, the smoke test is a silent fail-safe that gives a false sense of correctness.

**Suggested fix:** add a hard `assert fitness_fn_negative((5, 6, 2, 3, 5, 8, 6, 1)) == -6, "Slide-14 left board should score -6"` etc. The smoke test currently *prints* but never *asserts* — so it cannot fail. A test that cannot fail is a test that has no pedagogical value.

---

### P1-8 — The `Self` type annotation usage requires Python 3.11+, but the `type Population = set["Individual"]` syntax requires Python 3.12+, and neither file says so

**Location:** `ga_solution.py:113` (`from typing import Self`) and `ga_solution.py:313` (`type Population = set["Individual"]`).

The PEP-695 `type` statement is Python 3.12+. The docstring at line 84 mentions `py -3.12 ga_solution.py` which implies 3.12 is required. But the top of the file has no explicit version banner. A student on Python 3.10 will get a confusing `SyntaxError`.

**Suggested fix:** add a `# Requires Python 3.12+` banner at the top.

---

### P1-9 — `_run_queens_demo` in `ga_solution.py` and `main` in `Queen_solution.py` are nearly-but-not-quite duplicates

**Location:** `ga_solution.py:585-613` and `Queen_solution.py:326-360`.

Both functions:
1. Build initial population via `get_initial_population`.
2. Time the GA.
3. Print fittest + elapsed.

The differences are cosmetic (one uses `time.perf_counter_ns()` directly, the other wraps it; the prefix print line differs). A pedagogically clean solution would have ONE driver and call it from both entry points.

**Why this is P1 not P0:** it doesn't mislead a student about the algorithm, but it makes "which file is the canonical entry point?" ambiguous — the `ENTRY POINT: yes/no` markers help, but the duplication still adds noise.

**Suggested fix:** delete `Queen_solution.py:326-360` and have `Queen_solution.py:__main__` call `_run_queens_demo()` from `ga_solution.py`.

---

### P1-10 — `Number_solution.py:323` hard-codes the `minimal_fitness` calculation as `(2 ** NUMBER_GENE_LENGTH) - 1` but this is wrong for the slide-11 variant

**Location:** `Number_solution.py:319-324`.

```python
def main():
    minimal_fitness = (2 ** NUMBER_GENE_LENGTH) - 1
```

The docstring at line 321-322 says *"For the slide-11 variant it is the same number because we flipped the formula to peak at (2**LEN - 1) when value == target."* OK, mathematically that's true — the `get_fitness` peaks at `max_value` when `value == NUMBER_TARGET`.

But this main is only called from `if __name__ == "__main__"` block. The `_run_number_demo` in `ga_solution.py` correctly uses `MINIMAL_FITNESS_NUMBER if not None else (2 ** NUMBER_GENE_LENGTH) - 1`. So the two entry points have **different** termination logic — `Number_solution.py:main` ignores the `MINIMAL_FITNESS_NUMBER` KNOB entirely. A student running `python Number_solution.py` with `MINIMAL_FITNESS_NUMBER = 4` set will be surprised when the GA doesn't terminate at fitness 4.

**Suggested fix:** make `Number_solution.py:main` respect the same KNOB as `_run_number_demo`.

---

## P2 findings (polish, suggestions, things that would be nice but the lab still functions without them)

### P2-1 — Variable naming `mother` / `father` is cute but anthropomorphic

**Location:** `ga_solution.py:403`.

The lecture uses `parent1` / `parent2` consistently. `mother` / `father` is a folksy choice that doesn't carry over to other GA literature (where you'd also see `papa` / `mama` or just `a` / `b`). For a student who'll later read AIMA or a research paper, `parent1` / `parent2` is more useful.

### P2-2 — No reference to the lecture's §6 "Common Pitfalls" anywhere in the solution

The lecture spends 100+ lines on pitfalls (sign convention, completeness claims, plateau handling, mutation-rate vs crossover-rate confusion, genotype vs phenotype). The lab solution KNOBs implicitly touch on most of these, but never *name* them. A "PITFALLS THIS LAB AVOIDS / DEMONSTRATES" list at the top of `ga_solution.py` would be high-value cross-reference.

### P2-3 — `Number_solution.py:200-218` `get_fitness` could cite the lecture's slide-31 binary-encoding example

The decoding `value += bit * (2 ** position)` is exactly the lecture's slide-31 binary-encoding (`512, 256, …, 1` place values). The comment at lines 206-209 mentions "decimal value of the individual" but doesn't link to slide 31. A one-line `# matches L05 §5.6 slide-31 binary place-value encoding` would help.

### P2-4 — The `INITIAL_NUMBER_POPULATION` tuple-of-tuples is documented as the "slide-5 set" but the lecture L05 doesn't have a slide 5 with `{(1,1,0), (0,0,0), (0,1,0), (1,0,0)}`

The lecture L05's slide 5 is **the 8-puzzle**, not the 3-bit Number GA. The Number GA slides start at slide 10 (per the docstring at `ga_solution.py:11`). So *"slide-5 set"* refers to the **handout PDF's** slide 5, NOT the lecture L05 slide 5. The docstring should disambiguate.

**Suggested fix:** rename mentions of "slide 5" to "handout slide 5" (or "Lab 4.pdf slide 5") wherever the GA-specific slide 5 is meant, vs "L05 slide 5" wherever the 8-puzzle is meant.

### P2-5 — `Queen_solution.py:135-151` `QUEENS_DIAG_WEIGHT` / `QUEENS_ROW_WEIGHT` introduce a weighting concept the LECTURE L05 never mentions

The lecture's slide-14 n-queens local-max board uses a unit-weight fitness. The "weighted" variant is from "Appendix B" of an unspecified plan document. Including it is fine for variant coverage, but the docstring should be honest: this is **not in the lecture** — it's an Appendix-B-only extension. Currently the line *"Lecture L05 §3 / §4 — Genetic Algorithm (fitness function role)"* at `queens_fitness_solution.py:33` suggests the weighted variant is lecture-supported.

### P2-6 — `__repr__` returns `f"Gene: {self.gene} - Fitness: {self.get_fitness()}"` — pedagogically OK, but `Fitness` is computed lazily on every repr

For the print-heavy `PRINT_GENERATIONS = True` path, this means `get_fitness` is called multiple times per individual per generation. For the queens fitness function this is $O(n^2)$ per call. Not a correctness bug, but in a tight 8-queens run with hundreds of population members, the print loop becomes a hot path. A `Fitness: <cached>` would help. (P2 because it's a performance hint, not a learning hint.)

### P2-7 — The KNOB block on `P_MUTATION` (`ga_solution.py:245-260`) recommends 0.01–0.1, contradicting the slide-shipped default of 0.8 elsewhere

The lecture's §3.6 says *"the mutation rate is small — typically 0.001–0.1"* and §8.6 cheat-sheet says default 0.05. The solution KNOB at line 246 sets `P_MUTATION = 0.8` because *"the template's `default_p_mutation = 0.8` is what we preserve"*. The docstring at lines 253-254 then concedes *"the classic GA literature recommends 0.01–0.1 for bitstrings"* but keeps the slide-shipped 0.8 anyway.

This is **inverted**: the *lecture-canonical* default should be 0.05 (per §8.6), and "0.8 to match the template" should be an OVERRIDE knob. A student studying the lecture and running this code with default knobs will see drastically more mutation than the lecture recommends, which materially changes convergence behaviour and would lead the student to mis-report mutation-rate sensitivity.

**Suggested fix:** flip the default to 0.05. Keep 0.8 documented as "matches the handout-PDF template's default" but don't make it the default.

---

## QA Checklist (§7) status

The Feature Plan didn't ship a §7 QA Checklist; the brief is *"BE HARSH against pedagogical clarity"*. I'm marking standard items:

- [ ] **Scope compliance** — Pass with concerns. The solution stays in scope (GA for 3-bit number + n-queens) but the KNOB explosion goes beyond what the lab asks for. Pass.
- [ ] **Bugs** — Fail. See P0-3 (false math claim), P0-4 (population unbounded growth), P0-5 (slide-11 perfect-individual present), P0-6 (mutation operator semantically different).
- [ ] **Security** — N/A (no inputs from untrusted sources; no DB; no auth).
- [ ] **Performance** — Pass with concerns. P1-7 (smoke test never asserts), P2-6 (lazy `__repr__` fitness recomputation).
- [ ] **Accessibility** — N/A.
- [ ] **Convention adherence** — Pass. PEP-695 type aliases, abstract base class with `@abstractmethod`, hashable equatable individuals.
- [ ] **DOCUMENT.md presence** — Not checked (out of scope for a pedagogical-clarity review). Would be an audit item for a different reviewer.
- [ ] **Tests** — Fail. The "smoke test" in `queens_fitness_solution.py` does not assert; the slide-42 worked example is not reproducible from the code; the slide-44 mutation example is not pinned. See P1-3, P1-7.
- [ ] **Quality** — Fail on pedagogy. The KNOB-first structure (P1-5) inverts progressive disclosure. The (μ + λ) default (P0-4) silently differs from the lecture. The one-child crossover (P0-1) silently differs from the lecture.

---

## Acceptance criteria (§1) status

Inferred acceptance criteria from the docstrings:

- "Runs both demos by default and converges" — **Met**. Both demos converge for the default knobs.
- "Slide-faithful to L05 lecture" — **Not met**. See P0-1, P0-2, P0-4, P0-6.
- "Supports exam variants 1, 2, 3" — **Met**. Knobs exist for board size, mutation rate, fitness direction.
- "Reproduces slide-42 worked example" — **Not met**. The `+1` fitness shift (P0-3) breaks the proportionality; no test pins the slide-42 outcome.

---

## DOCUMENT.md audit

Not in scope for pedagogical-clarity review.

---

## Out-of-scope observations

- The non-`_solution.py` files (`ga.py`, `Number.py`, `Queen.py`, `queens_fitness.py`) — the original template files — should also be checked for whether the solution adds *MORE* than the template required (it clearly does, by ~200 lines of KNOB block). The grading rubric for this lab is likely "complete the four functions"; the solution as written is way over-engineered relative to that. For an exam-prep aid, the over-engineering is mostly a feature (lots of knobs = lots of variant coverage), but it should be *layered* (minimal slide-faithful version first, then knobs).

- The `queens_fitness.py` original template uses `column_weight` for weighting (per the `Queen_solution.py:46-50` docstring comment) — the solution's `fitness_fn_weighted` uses `diag_weight` and `row_weight` instead. This means the solution is **not a drop-in replacement** for the template if the lab grader runs the original tests. P2 if the lab is exam-only; P0 if it's also graded against the template's signature.

- The `random_selection` returns `tuple[Individual, Individual]` but the lecture-canonical `roulette_wheel_select` returns `Individual`. A student copying this signature to an exam will not match the canonical API. See P0-2.

---

## Concerns / risks

1. **The student studying from this code will internalise three lecture-divergent patterns** (one-child crossover, paired selection, union-then-trim) as "correct GA". On the exam they will write these and get docked because the marked solution follows §4.3. This is the biggest risk.

2. **The mutation operator's "exactly one bit" semantics** (P0-6) is the second-biggest risk because the lecture's mutation is per-bit, and a student writing per-bit mutation on the exam will write *correct* code that the marker will mark, but if they're studying from this lab they may write the "always one bit" version instead and lose marks.

3. **The KNOB-heavy structure** (P1-5) means a student who needs to "read the GA loop in 30 seconds before the exam" can't, because they have to skip past 190 lines of knob documentation first. The lab fails as a quick-revision aid.

4. **No reproducible test against the lecture's slide-42 worked example** (P1-3) means there is *no mechanical way* to verify the code matches the lecture. Every claim of "slide-faithful" is unverified.

5. **The roulette-wheel `+1` shift** (P0-3) makes the slide-42 numerical answer unreproducible from this code. A student trying to walk through slide 42 with this code will get *almost* the same answer but with measurably different probabilities, and the docstring tells them this is fine when it isn't.

---

## What PM should do next

**Fix the P0s before re-QA.** Specifically:

1. **P0-1 + P0-2:** rewrite `genetic_algorithm` and `random_selection` to match §4.3 verbatim (two children per crossover, selection returns one parent, called twice independently). The current code is a different GA wearing a slide-faithful docstring.

2. **P0-3:** delete the false "proportions unchanged up to a constant" claim. Document the shift honestly.

3. **P0-4:** flip `population = population.union(new_population)` to `population = new_population`. Move the (μ + λ) variant to a knob.

4. **P0-5:** fix the slide-11 hard-coded-population docstring (or change the hard-coded set to exclude `(1, 0, 0)`).

5. **P0-6:** implement true per-bit mutation. The current "always one bit" semantics is the **handout PDF's** rule, NOT the lecture's. Add a knob to switch between them; default to lecture per-bit.

**Then re-QA before App Tester runs.** The App Tester will not catch any of these because the code's runtime behaviour (does it converge? does it return a board with 0 conflicts?) is fine. These are all *pedagogical* defects that only surface when the student studies this code beside the L05 notes.

After P0s: address P1-3 (the slide-42 reproducibility test) — this is the single highest-leverage pedagogical addition, and it will *prove* the P0 fixes worked.

**Recommend:** dispatch `pm-frontend` (or whichever engineer owns this lab — likely `pm-backend` since it's algorithm code) with this report and a tight scope: "fix the six P0s, add the slide-42 smoke test, do not add new features". Then re-dispatch `pm-qa` (me) for round 2.

---

## DOCUMENT.md updated

N/A for QA.

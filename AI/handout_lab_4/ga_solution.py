"""
LAB 4: Genetic Algorithm — driver + entry point
================================================

PROBLEM STATEMENT (from Lab 4.pdf):
-----------------------------------
The Local-Search / Genetic Algorithm lab has two exercises and a
homework.

Exercise (slides 4-10): "A trivial problem is to determine the
greatest 3-bit binary number. We will be trying to solve this trivial
problem by using the GA. ... Complete `get_fitness`, `reproduce`,
`mutate` in NumberIndividual (Number.py) and `random_selection` in
ga.py." (Number_solution.py covers the per-individual functions; this
file covers selection + the GA loop.)

Slide 11 follow-up: "Specific 3-bit binary number — modify the
fitness function to specify how close the individual is to the
number 4". Exposed here via Number_solution's `NUMBER_TARGET` knob.

Homework (slides 12-18): "Place n-queens on a chessboard in
non-conflicting positions. Modify your GA program given the following
problem and code (queens_fitness.py)." Implemented in
Queen_solution.py. The GA driver is the same as for the Number
problem — that is the whole point of the abstract Individual class:
one algorithm, multiple problem encodings.

Algorithm pseudocode (L05 §4.3 — slide-faithful):
    Start with a random valid population of size N.
    For generation in (0 ... MAX_GENERATIONS):
        new_population = empty
        Repeat N/2 times:
            parent1 = roulette_wheel_select(population)   # spin once
            parent2 = roulette_wheel_select(population)   # spin again
            (child1, child2) = single_point_crossover(parent1, parent2)
            mutate child1 (per-bit with prob m)
            mutate child2 (per-bit with prob m)
            append child1, child2 to new_population
        population = new_population            # generational replacement
        If best fitness >= target → stop and return best
    Return the fittest individual ever seen.

Two-children-per-crossover and two-independent-spins-of-the-wheel are
the lecture-canonical form (L05 §3.6, §4.3, §8.3). This module
implements that. A (μ + λ) "union with previous generation, then
trim" variant is available behind the `USE_MU_PLUS_LAMBDA` knob.

MENTAL MODEL (one-line analogy):
--------------------------------
A GA is *evolution in a bottle*: you stage a tiny ecosystem of
candidate solutions, let "survival of the fittest" do its work
(parents proportional to fitness), allow couples to *cross over*
ideas (genetic recombination), and inject the occasional *mutation*
(random tweak) so the gene pool does not stagnate — same engine
whether the bottle holds 3-bit numbers or 8-queens chessboards.

REFERENCES:
-----------
- Lecture L05 §3 / §4 / §6 — Genetic Algorithm (population,
  selection, crossover, mutation, fitness landscape, premature
  convergence).
- Glossary: Genetic algorithm, Population, Chromosome, Fitness
  function, Roulette-wheel selection, Crossover, Mutation,
  Elitism, Local search, Local maximum.
- See `study/lectures/L05-Local-Search.md` (once locked).

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
Every knob below is exam-tunable. The three exam variants in
`study/_exam/Lab4-GA/variants.md` are solved as follows:

  - Variant 1 (8-Queens instead of 4-Queens): bump `N_QUEENS` to 8;
    bump `MAX_GENERATIONS` to ~500; bump `POPULATION_SIZE` to
    ~50-100. Consider lowering `MUTATION_RATE` to ~0.1 for the
    larger board. No code edits.

  - Variant 2 (mutation-rate tuning): set `MUTATION_RATE` to 0.01,
    then re-run with 0.5. Pin `RANDOM_SEED` for reproducibility.

  - Variant 3 (positive fitness): set
    `QUEENS_FITNESS_VARIANT = "positive"` in Queen_solution.py; set
    `MINIMAL_FITNESS_QUEENS` here to `N_QUEENS*(N_QUEENS-1)//2`.

Beyond the variant bank, two general adaptations:

  - To run only the 3-bit Number demo (skip n-queens), set
    `RUN_NUMBER_DEMO = True` and `RUN_QUEENS_DEMO = False`.
  - To pin a random seed (so a re-run reproduces the exact same
    convergence trace), set `RANDOM_SEED` to any int.

OUTPUTS WHEN RUN:
-----------------
`py -3.12 ga_solution.py` runs (by default) BOTH demos:

  1. "===== Lab 4 — Exercise (3-bit Number) =====" then per-
     generation populations, then "Fittest Individual: Gene: (1, 1, 1)
     - Fitness: 7" and the generation at which it converged.
  2. "===== Lab 4 — Homework (N-Queens) =====" then per-generation
     populations (or a "Population too large to print" summary if
     POPULATION_SIZE > 10), then "Fittest Individual: Gene:
     (...) - fitness: 0" (i.e. a conflict-free 4-queens layout), the
     generation at which it converged, and elapsed milliseconds.

The script's exit code is 0 on success. Either demo printing a
non-zero fitness from the Number target or a non-zero fitness from
queens-negative is still "success" — the GA may genuinely not
converge inside MAX_GENERATIONS, which is itself a valid lesson
(see L05 §6 "Common Pitfalls" on premature convergence). For exam
variants that NEED convergence, raise MAX_GENERATIONS.

ENTRY POINT: yes
----------------
This is the single entry point for Lab 4. The other three
*_solution.py files are helper modules:
  • `queens_fitness_solution.py` — the scoring functions.
  • `Number_solution.py` — the 3-bit-number Individual subclass.
  • `Queen_solution.py` — the N-Queens Board (Individual) subclass.

Requires Python 3.12+ (uses PEP-695 `type` aliases and PEP-673 `Self`).
"""

import random
from abc import ABC, abstractmethod
from typing import Self


# --------------------------------------------------------------------
# Top-level KNOBs — the highest-leverage parameters for exam variants.
# --------------------------------------------------------------------

# KNOB: RANDOM_SEED (default=None, allowed=None or any int)
#   What it does: seed for Python's `random` module. When set,
#       every run reproduces the same sequence of selections,
#       mutations, and crossover points. Re-applied at the start of
#       each demo function so in-process A/B comparisons are
#       apples-to-apples.
#   Effect: None → genuine pseudo-random per run (different
#       convergence paths). int → fully deterministic; convergence
#       comparisons across knob settings become apples-to-apples.
#   Exam variants: pin to an int (e.g. 42) when answering
#       "compare mutation rate 0.01 vs 0.5" so both runs start
#       from the same seed.
RANDOM_SEED: int | None = None

# KNOB: RUN_NUMBER_DEMO (default=True)
#   What it does: include the slide-10 "highest 3-bit number"
#       exercise in the entry-point run.
#   Effect: turn off to focus on the n-queens homework only.
#   Exam variants: leave True for full-lab demonstrations; flip to
#       False when only the homework matters.
RUN_NUMBER_DEMO: bool = True

# KNOB: RUN_QUEENS_DEMO (default=True)
#   What it does: include the slide-13+ n-queens homework in the
#       entry-point run.
#   Effect: turn off to verify the Number exercise in isolation.
#   Exam variants: True for any variant in variants.md;
#       False if a question is specifically about the Number
#       exercise (slide 10 or slide 11).
RUN_QUEENS_DEMO: bool = True


# --------------------------------------------------------------------
# Number-problem KNOBs (the slide-10 / slide-11 exercise)
# --------------------------------------------------------------------

# KNOB: POPULATION_SIZE_NUMBER (default=4, range=2..32)
#   What it does: size of the initial population for the 3-bit
#       number demo (when NUMBER_USE_HARDCODED_POPULATION is False).
#   Effect: tiny populations (4 = slide default) suffice for 3-bit
#       (search space of only 8 elements). Bigger populations
#       wasted on tiny gene length.
#   Exam variants: bump if you also bumped NUMBER_GENE_LENGTH;
#       capped at 2**NUMBER_GENE_LENGTH (you cannot have more
#       unique individuals than the gene allows).
POPULATION_SIZE_NUMBER: int = 4

# KNOB: MAX_GENERATIONS_NUMBER (default=30, range=1..10000)
#   What it does: hard cap on generations for the Number demo.
#       The GA may stop earlier when MINIMAL_FITNESS_NUMBER is hit.
#   Effect: 30 is far more than enough for 3-bit; may need bumping
#       for larger gene lengths.
#   Exam variants: optional 4c (5-bit Number) may need bumping.
MAX_GENERATIONS_NUMBER: int = 30

# KNOB: MINIMAL_FITNESS_NUMBER (default=None → auto, allowed=any int)
#   What it does: target fitness that triggers early termination
#       for the Number demo. When None (the default), this file
#       auto-computes it as `2**NUMBER_GENE_LENGTH - 1` (the
#       maximum possible value of an n-bit gene). Override to stop
#       earlier (e.g. accept any fitness >= 6).
#   Effect: None → optimal-fitness target; int → custom target
#       allowing partial-credit answers for the slide-11 "target a
#       specific number" variant where the perfect individual is
#       absent from the initial population.
#   Exam variants: set to 4 to ask "reach value 4" (cooperates
#       with NUMBER_TARGET=4 in Number_solution). See also
#       `NUMBER_TARGET` in Number_solution.py for the slide-11
#       follow-up "specific 3-bit binary number" variant.
MINIMAL_FITNESS_NUMBER: int | None = None


# --------------------------------------------------------------------
# N-Queens KNOBs (the slide-13+ homework)
# --------------------------------------------------------------------

# KNOB: N_QUEENS (default=4, range=4..N)
#   What it does: board size for the N-Queens problem. Each gene
#       has length N_QUEENS and each row value is in [1, N_QUEENS].
#   Effect: search space grows roughly as N**N. N=4 finishes
#       in well under a second; N=8 takes a few seconds with a
#       larger population; N=12 may take tens of seconds and
#       benefits from population trimming.
#   Exam variants: variant 1 in variants.md — set 8 for the
#       canonical 8-queens framing. Set 6 for the variant-2
#       mutation-rate study.
N_QUEENS: int = 4

# KNOB: POPULATION_SIZE (default=4, range=4..1000)
#   What it does: size of the initial population for the queens
#       demo.
#   Effect: larger population → better diversity per generation but
#       slower per-generation cost. Under generational replacement
#       (default) the population stays at this size every
#       generation. Under (μ + λ) the working set grows unless
#       `TRIM_POPULATION` is on.
#   Exam variants: keep at 4 for 4-queens; bump to ~50-100 for
#       8-queens (variant 1) so the wider search space has
#       sufficient sampling each generation. (Same name as in
#       variants.md.)
POPULATION_SIZE: int = 4

# KNOB: MAX_GENERATIONS (default=100, range=1..100000)
#   What it does: hard cap on generations for the queens demo.
#       The GA may stop earlier when MINIMAL_FITNESS_QUEENS is hit.
#   Effect: 4-queens converges within 10-50 generations; 8-queens
#       commonly needs 200-1000 depending on population and seed.
#   Exam variants: variant 1 (8-queens) typically wants 200-500;
#       variant 2 (low mutation rate) may need 500+ to give the
#       slow-mutation run a fair chance. (Same name as in
#       variants.md.)
MAX_GENERATIONS: int = 100

# KNOB: MINIMAL_FITNESS_QUEENS (default=0.0, allowed=any number)
#   What it does: target fitness that triggers early termination
#       for the queens demo. For the default "negative" fitness
#       this is 0 (no conflicts). For the "positive" variant it
#       should be N_QUEENS*(N_QUEENS-1)//2 (the maximum possible
#       non-conflicting pair count).
#   Effect: stop when "good enough" instead of running every
#       generation. Set to a slightly worse value (e.g. -1 for
#       negative fitness) to accept near-perfect solutions on
#       large boards where 0 may be impractical (e.g. 6-queens
#       does have solutions, but 2-queens and 3-queens DO NOT).
#   Exam variants: variant 3 (positive fitness) → set to
#       N_QUEENS*(N_QUEENS-1)//2 (e.g. 6 for n=4). Set to -1 to
#       accept "off by one conflict" solutions in a "speed-
#       sensitive" framing.
MINIMAL_FITNESS_QUEENS: float = 0.0

# KNOB: MUTATION_RATE (default=0.05, range=0.0..1.0)
#   What it does: probability that a freshly produced child is
#       mutated. The lecture L05 §3.6 and §8.6 cheat-sheet
#       recommend a small mutation rate, typically 0.001-0.1; the
#       canonical default is 0.05. The handout PDF template uses
#       0.8 — that is a template convenience for tiny populations
#       and is not the lecture-canonical default.
#   Effect: low values (e.g. 0.01) — GA leans on crossover and may
#       converge slowly or get trapped in local optima (premature
#       convergence). High values (e.g. 0.5+) — GA explores
#       aggressively but loses beneficial substructures, becoming
#       a near-random walk.
#   Exam variants: variant 2 — sweep through 0.01 and 0.5 and
#       report best-fitness curves. (Same name as in variants.md.)
MUTATION_RATE: float = 0.05

# KNOB: CROSSOVER_RATE (default=1.0, range=0.0..1.0)
#   What it does: probability that crossover is applied to a
#       parent pair instead of cloning the two parents. The
#       slide-shipped GA implicitly assumes 1.0 (every pair
#       crosses), so the default keeps that behaviour.
#   Effect: lowering this preserves more genetic material from
#       parents verbatim and is sometimes useful when crossover is
#       destructive on small genes; raising it has no effect (max
#       is 1.0).
#   Exam variants: leave at 1.0 unless a variant explicitly asks
#       "what if crossover is rare". Some textbook formulations
#       set this to 0.7-0.95; included here for completeness.
CROSSOVER_RATE: float = 1.0

# KNOB: USE_MU_PLUS_LAMBDA (default=False)
#   What it does: when True, the new generation is UNIONed with
#       the old (textbook (μ + λ) variant). When False (the
#       lecture default), the old population is discarded and the
#       new generation replaces it (textbook generational GA, L05
#       §4.3).
#   Effect: (μ + λ) preserves high-fitness ancestors across
#       generations but causes the working set to grow unless
#       `TRIM_POPULATION` is also on. Generational replacement
#       keeps per-generation cost O(N·F) — matches the lecture's
#       complexity analysis.
#   Exam variants: leave False for slide-faithful behaviour. Flip
#       True when a question explicitly mentions "preserve old
#       population" or "(μ + λ)".
USE_MU_PLUS_LAMBDA: bool = False

# KNOB: TRIM_POPULATION (default=False)
#   What it does: after building the new generation (and optionally
#       unioning with the old), trim the result back down to
#       MAX_POPULATION_SIZE by keeping the top individuals by
#       fitness. Most useful in combination with
#       USE_MU_PLUS_LAMBDA=True (where the working set would
#       otherwise grow unboundedly).
#   Effect: caps memory and per-generation cost; introduces a mild
#       form of elitism (best individuals always survive). Off by
#       default to match the lecture's pure generational GA.
#   Exam variants: optional 4b — True with MAX_POPULATION_SIZE=30.
#       (Same name as in variants.md.)
TRIM_POPULATION: bool = False

# KNOB: MAX_POPULATION_SIZE (default=100, range=10..100000)
#   What it does: the cap used by `trim_population` when
#       TRIM_POPULATION is True. No effect when TRIM_POPULATION is
#       False (read this first — the knob is a sub-knob of
#       TRIM_POPULATION).
#   Effect: smaller cap → tighter selection pressure; larger cap →
#       closer to "no trimming at all".
#   Exam variants: set to ~30 for tight-budget variants;
#       leave at 100 for the slide-shipped default.
MAX_POPULATION_SIZE: int = 100

# KNOB: PRINT_GENERATIONS (default=True)
#   What it does: switch the per-generation population print on/off.
#       Useful when running large populations; the GA still prints
#       a "Population too large to print" summary line when the
#       set exceeds 10 individuals.
#   Effect: turn off to silence per-generation noise and only
#       print the final fittest individual.
#   Exam variants: turn off when collecting only convergence-
#       generation numbers across many parameter sweeps.
PRINT_GENERATIONS: bool = True


# --------------------------------------------------------------------
# Type aliases (PEP-695 style, matching the original template)
# --------------------------------------------------------------------

type Population = set["Individual"]


# --------------------------------------------------------------------
# Abstract base class — identical surface area to the original
# `ga.py` Individual.
# --------------------------------------------------------------------

class Individual(ABC):
    """Abstract candidate solution.

    Subclasses must implement `get_fitness`, `mutate`, and
    `reproduce`. They must also be hashable (the GA stores them in
    a `set`) and totally ordered (`max(population)` uses `__lt__`).
    The default `__lt__` here orders by fitness, so subclasses
    rarely need to override it.

    NOTE on `reproduce` contract: the lecture L05 §3.6.2 / §4.3
    canonical form is single-point crossover returning a TUPLE of
    TWO children. Subclasses must respect that contract — see
    NumberIndividual.reproduce / Board.reproduce.
    """

    @abstractmethod
    def get_fitness(self) -> float:
        """Return the fitness of the individual. Higher = better."""
        ...

    @abstractmethod
    def mutate(self) -> Self:
        """Return a (possibly) mutated copy. Should not modify self."""
        ...

    @abstractmethod
    def reproduce(self, other: Self) -> tuple[Self, Self]:
        """Return (child1, child2) produced by crossover with `other`."""
        ...

    def __lt__(self, other: Self) -> bool:
        return self.get_fitness() < other.get_fitness()

    def __repr__(self):
        return f"Fitness: {self.get_fitness()}"


# --------------------------------------------------------------------
# Driver — the actual GA loop. Algorithmically faithful to L05 §4.3.
# --------------------------------------------------------------------

def genetic_algorithm(
    population: Population,
    minimal_fitness: float,
    num_of_generations: int = 30,
    should_trim_population: bool = False,
    p_mutation: float = 0.05,
    use_mu_plus_lambda: bool = False,
) -> "Individual | None":
    """Run the GA on a starting population.

    Returns the fittest individual seen by the time the loop stops
    (or None if `population` was empty). The lecture L05 §4.3
    pseudocode is followed step-by-step:
      1. For each generation, print the population (subject to
         PRINT_GENERATIONS).
      2. Build a new population by repeatedly:
            parent1 = roulette_wheel_select(population)
            parent2 = roulette_wheel_select(population)
            (child1, child2) = parent1.reproduce(parent2)
            mutate each child with probability p_mutation
            add both children to new_population
         until the new population has reached the target size.
      3. Replace the old population (generational GA, the lecture
         default) or union-then-trim it (μ + λ variant, gated by
         `use_mu_plus_lambda`).
      4. Stop if best fitness >= minimal_fitness.

    Termination matches L05 §4.3 — stop when best fitness reaches
    the target OR when num_of_generations is exhausted. Neither
    condition guarantees a globally-optimal answer (no formal
    completeness claim, per L05 §4.4).

    WHY two children per crossover: the lecture §3.6.2 and §4.3
    pseudocode explicitly return `(child1, child2)` from
    single-point crossover. Discarding one child throws away
    information from the parents' joint genome.

    WHY two independent spins of the wheel: the lecture §3.6
    explicitly calls this out as "the single most common GA
    implementation bug: spinning once and reusing the parent". We
    call `roulette_wheel_select` twice independently per pair.
    """
    if not population:
        return None

    # Initialise the fittest individual from the input population
    # so that callers passing num_of_generations=0 still get a
    # sensible answer (the fittest of the initial population).
    fittest_individual: Individual = get_fittest_individual(population)
    target_size: int = len(population)

    generation: int = 0
    converged_at: int | None = None

    for generation in range(num_of_generations):
        if PRINT_GENERATIONS:
            print(f"Generation {generation}:")
            print_population(population)

        new_population: Population = set()

        # WHY iterate until we have target_size children: the
        # lecture loops "N/2 times, producing 2 children each" to
        # build a generation of size N. We iterate until we have
        # at least N — the set may deduplicate identical children,
        # so we keep generating pairs until the count is reached.
        while len(new_population) < target_size:
            parent1 = roulette_wheel_select(population)
            parent2 = roulette_wheel_select(population)

            if random.uniform(0, 1) < CROSSOVER_RATE:
                child1, child2 = parent1.reproduce(parent2)
            else:
                # No crossover: clone the parents.
                child1, child2 = parent1, parent2

            if random.uniform(0, 1) < p_mutation:
                child1 = child1.mutate()
            if random.uniform(0, 1) < p_mutation:
                child2 = child2.mutate()

            new_population.add(child1)
            new_population.add(child2)

        # Replacement step. L05 §4.3 default is generational
        # (discard old population). (μ + λ) merges and is available
        # behind the knob.
        if use_mu_plus_lambda:
            population = population.union(new_population)
        else:
            population = new_population

        if should_trim_population:
            population = trim_population(population, MAX_POPULATION_SIZE)

        fittest_individual = get_fittest_individual(population)

        if minimal_fitness <= fittest_individual.get_fitness():
            converged_at = generation
            break

    if PRINT_GENERATIONS:
        print(f"Final generation {generation}:")
        print_population(population)

    if converged_at is not None:
        print(f"Converged at generation {converged_at}.")
    else:
        print(
            f"MAX_GENERATIONS ({num_of_generations}) hit without "
            f"reaching target fitness {minimal_fitness}."
        )

    return fittest_individual


def print_population(population: Population) -> None:
    """Print the population, or a summary if it is large.

    The slides print a 4-element population in full (slide 6 table)
    so we keep that behaviour for small sets. For larger
    populations we degrade gracefully to a one-line summary so the
    8-queens-with-100-individuals variant does not flood the
    terminal.
    """
    if len(population) > 10:
        print(
            f"Population too large to print {len(population)}, "
            f"fittest individual: {get_fittest_individual(population)}"
        )
        return
    for individual in population:
        print(individual)


# --------------------------------------------------------------------
# Selection — the implementation of slide 6's "Fitness ratio" table.
# Lecture-canonical name: `roulette_wheel_select`, returns ONE
# individual. Call it twice independently to form a parent pair.
# --------------------------------------------------------------------

def roulette_wheel_select(population: Population) -> Individual:
    """Pick ONE parent proportional to fitness (roulette wheel).

    Call this function TWICE INDEPENDENTLY per crossover event to
    produce a parent pair — per L05 §3.6, "spinning once and
    reusing the parent" is the single most common GA implementation
    bug.

    WHY a conditional shift: the n-queens "negative" fitness
    variant returns <= 0 values, but roulette-wheel selection
    needs non-negative weights. When the minimum fitness is < 0 we
    shift every fitness by `-min_fitness` so the worst individual
    has weight 0 (and all others strictly positive). When all
    fitnesses are already >= 0 we do NOT shift — the slide-6
    walkthrough numbers (`(0,0,0)` has 0/12 of the wheel) are
    preserved exactly.

    NOTE on shift semantics: adding a constant to every fitness
    does NOT preserve proportions (unlike multiplication). The
    older "+1" shift used here previously inflated the worst
    individual's selection probability from 0 to 1/N. We avoid
    that distortion by shifting only when negative weights are
    present.
    """
    ordered_population = sorted(population, reverse=True)  # best first
    fitnesses = [ind.get_fitness() for ind in ordered_population]

    min_fitness = min(fitnesses)
    if min_fitness < 0:
        # Shift only when we must. Worst individual gets weight 0.
        shifted = [f - min_fitness for f in fitnesses]
    else:
        # Slide-6 faithful: positive fitnesses are used as-is.
        shifted = list(fitnesses)

    fit_sum = sum(shifted)

    # Degenerate case: all weights are zero (e.g. an all-(0,0,0)
    # Number population, or all individuals tied at the worst
    # negative fitness). Fall back to uniform selection — the
    # lecture's §3.6.1 cumulative walk is undefined when Σf = 0.
    if fit_sum <= 0:
        return random.choice(ordered_population)

    return pick_individual(fit_sum, ordered_population, shifted)


# Kept as an alias for backward compatibility with any caller that
# imports `random_selection`. The lecture-canonical name is
# `roulette_wheel_select`.
def random_selection(population: Population) -> tuple[Individual, Individual]:
    """Backward-compatibility wrapper: returns (parent1, parent2).

    Prefer `roulette_wheel_select(population)` called twice for new
    code, matching the lecture L05 §3.6 / §4.3 API. This wrapper
    exists so older callers do not break.
    """
    return roulette_wheel_select(population), roulette_wheel_select(population)


def pick_individual(
    total_fitness_sum: float,
    ordered_population: list[Individual],
    shifted_fitnesses: list[float],
) -> Individual:
    """Walk a cumulative-fitness list with a uniform random draw.

    `shifted_fitnesses` is REQUIRED — the caller (roulette wheel
    selection) is responsible for any shift needed to guarantee
    non-negative weights. This keeps the proportionality contract
    explicit at the call site rather than buried behind a fallback.

    The lecture's §3.6.1 procedure assumes Σf > 0 and proceeds:
      pick = uniform(0, total)
      walk the cumulative sum until it crosses `pick`
      return that individual.
    """
    pick = random.uniform(0, total_fitness_sum)
    running = 0.0
    for ind, w in zip(ordered_population, shifted_fitnesses):
        running += w
        if running >= pick:
            return ind
    # WHY a final fallback: floating-point rounding can leave
    # `running` epsilon short of `total_fitness_sum` even after the
    # full sweep. Falling back to the last individual matches the
    # slide-shipped template behaviour `return ordered_population[-1]`.
    return ordered_population[-1]


# --------------------------------------------------------------------
# Population helpers
# --------------------------------------------------------------------

def get_fittest_individual(from_population: Population) -> Individual:
    """Return the individual with the highest fitness.

    Relies on Individual.__lt__ ordering by `get_fitness()`, so
    `max(population)` is the fittest.
    """
    return max(from_population)


def trim_population(population: Population, desired_length: int) -> Population:
    """Reduce population to the top `desired_length` by fitness.

    WHY a sort-and-slice: the population is a small set; a sort is
    O(n log n) and trivial for slide-scale problems. For very
    large populations a partial sort (heapq.nlargest) would be
    faster, but we keep the simple version to match the slide-
    shipped template line-for-line.
    """
    if len(population) <= desired_length:
        return population
    population_list = sorted(population, reverse=True)
    population_list = population_list[:desired_length]
    return set(population_list)


# --------------------------------------------------------------------
# Entry-point demos
# --------------------------------------------------------------------

def _run_number_demo() -> None:
    """Slide 10 — highest 3-bit binary number."""
    # Imported lazily so the file can be inspected by an exam
    # agent that only wants to read this file's docstring without
    # triggering Number_solution's import chain.
    from Number_solution import (
        NumberIndividual,
        NUMBER_GENE_LENGTH,
        build_initial_population,
    )

    # Re-seed at the start of each demo so in-process A/B
    # comparisons (e.g. variant 2's two mutation-rate runs) start
    # from the same RNG state.
    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED)

    print("===== Lab 4 — Exercise (3-bit Number) =====")
    target = (
        MINIMAL_FITNESS_NUMBER
        if MINIMAL_FITNESS_NUMBER is not None
        else (2 ** NUMBER_GENE_LENGTH) - 1
    )
    population: set[NumberIndividual] = build_initial_population()
    fittest = genetic_algorithm(
        population,
        minimal_fitness=target,
        num_of_generations=MAX_GENERATIONS_NUMBER,
        should_trim_population=TRIM_POPULATION,
        p_mutation=MUTATION_RATE,
        use_mu_plus_lambda=USE_MU_PLUS_LAMBDA,
    )
    print(f"Fittest Individual: {fittest}")
    print()


def _run_queens_demo() -> None:
    """Slide 13+ — N-Queens homework."""
    import time
    from Queen_solution import Board, get_initial_population

    # Re-seed at the start of each demo (see _run_number_demo).
    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED)

    print(f"===== Lab 4 — Homework (N-Queens, N = {N_QUEENS}) =====")
    initial_population: set[Board] = get_initial_population(
        POPULATION_SIZE, N_QUEENS
    )
    start_time = time.perf_counter_ns()
    fittest = genetic_algorithm(
        initial_population,
        minimal_fitness=MINIMAL_FITNESS_QUEENS,
        num_of_generations=MAX_GENERATIONS,
        should_trim_population=TRIM_POPULATION,
        p_mutation=MUTATION_RATE,
        use_mu_plus_lambda=USE_MU_PLUS_LAMBDA,
    )
    end_time = time.perf_counter_ns()

    if fittest is not None:
        print(
            f"Fittest Individual: {fittest} - "
            f"fitness: {fittest.get_fitness()}"
        )
    else:
        print("No fittest individual produced (population was empty).")
    elapsed_ms = (end_time - start_time) / 10 ** 6
    print(f"total elapsed time: {elapsed_ms:.3f} ms")
    print()


def main() -> None:
    """Lab-4 entry point. Runs both demos by default."""
    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED)

    if RUN_NUMBER_DEMO:
        _run_number_demo()
    if RUN_QUEENS_DEMO:
        _run_queens_demo()


if __name__ == "__main__":
    main()

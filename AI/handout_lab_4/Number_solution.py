"""
LAB 4: Genetic Algorithm — 3-bit binary number (in-class exercise)
==================================================================

PROBLEM STATEMENT (from Lab 4.pdf, slides 5-10):
------------------------------------------------
"A trivial problem is to determine the greatest 3-bit binary number.
We will be trying to solve this trivial problem by using the GA."

  - Representation: an individual is a tuple of bits, e.g. (1, 0, 0).
  - Initial population: a small random set of bit tuples, e.g.
        {(1,0,0), (0,1,0), (0,1,0), (0,0,0)}.
  - Fitness function: returns the integer value of the bit tuple
        (0..7 for a 3-bit gene). The GA maximises this; the goal is
        (1, 1, 1).
  - Selection: roulette (fitness-proportionate). Implemented in
        `ga_solution.py`.
  - Crossover: single-point. Bits before the cut come from the
        first parent; bits at and after the cut come from the second.
        Produces TWO children (the second uses the complementary
        prefix/suffix split) — matching the lecture L05 §3.6.2.
  - Mutation: per-bit-with-probability-m (L05 §3.6 canonical
        formulation). Each bit independently flips with the given
        probability; multiple bits can mutate per call.

Slide 10 ("Exercise — Highest 3-bit binary number") asks the
student to fill in `get_fitness`, `reproduce`, `mutate`, and the
`random_selection` function from `ga.py`. The matching slide-11
follow-up ("Specific 3-bit binary number") asks the student to
change the fitness so that the GA targets the value 4 — that
variant is exposed here via the `NUMBER_TARGET` KNOB.

MENTAL MODEL (one-line analogy):
--------------------------------
Each individual is an n-bit integer (slide 31 binary place-value
encoding: bit 0 → 1, bit 1 → 2, bit 2 → 4, ...). The GA evolves
toward the largest representable value (slide 10) or the gene
closest to a chosen target (slide 11).

REFERENCES:
-----------
- Lecture L05 §3 / §4 — Genetic Algorithm (chromosome, fitness,
  crossover, mutation). L05 §5.6 slide-31 — binary place-value
  encoding.
- Glossary: Chromosome, Crossover, Mutation, Fitness function,
  Population, Genetic algorithm, Roulette-wheel selection.
- See `study/lectures/L05-Local-Search.md` (once locked).

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
1. To change the gene length (e.g. solve "highest 5-bit number"):
   bump `NUMBER_GENE_LENGTH` to 5 and `MINIMAL_FITNESS_NUMBER` to 31.
   The slides' 3-bit framing is just a default — the code itself is
   already n-bit.
2. To target a specific value (slide 11 "Specific 3-bit binary
   number" variant — target 4): set `NUMBER_TARGET = 4`. The
   fitness becomes `7 - |value - 4|` (closer to 4 is better) so the
   GA still has something to maximise. IMPORTANT: the hard-coded
   slide-5 population CONTAINS `(1, 0, 0)` (which decodes to 4), so
   if you set `NUMBER_TARGET = 4` while leaving
   `NUMBER_USE_HARDCODED_POPULATION = True`, the GA terminates at
   generation 0 — the perfect individual is already present. The
   slide-11 caveat is "make sure the perfect individual is NOT in
   the initial population". To honour that caveat, either:
     (a) flip `NUMBER_USE_HARDCODED_POPULATION = False` and use a
         random pool, OR
     (b) edit `INITIAL_NUMBER_POPULATION` below to remove
         `(1, 0, 0)`.
3. To start from a hand-crafted population (slide-5 example):
   set `NUMBER_USE_HARDCODED_POPULATION = True` and leave the
   `INITIAL_NUMBER_POPULATION` constant as-is. To start from a
   random set instead, set `NUMBER_USE_HARDCODED_POPULATION = False`
   and tune `POPULATION_SIZE_NUMBER` in `ga_solution.py`.
4. The default hard-coded population `{(1,1,0), (0,0,0), (0,1,0),
   (1,0,0)}` deliberately omits `(1, 1, 1)` so that for the default
   slide-10 target (`NUMBER_TARGET = None` → "highest 3-bit number"
   = `(1, 1, 1)`) the GA cannot terminate at generation 0. For
   slide-11 targets you may need to remove additional tuples — see
   point 2 above.

OUTPUTS WHEN RUN:
-----------------
Running this file directly (`py -3.12 Number_solution.py`) runs the
3-bit-number GA using the same global KNOBs as `ga_solution.py`. It
prints each generation's population, prefixed by "Generation N:",
and finishes with "Fittest Individual: ...". For the default
settings it converges to `(1, 1, 1)` (fitness 7) within a handful of
generations.

ENTRY POINT: no
---------------
This module is a helper imported by `ga_solution.py`. The Lab 4
entry point is `ga_solution.py` (it runs both the Number demo and
the N-Queens homework in one go). Running this file directly is
supported (its `__main__` block exercises only the Number demo) but
the canonical entry is `ga_solution.py`.
"""

import random
from typing import Self

from ga_solution import Individual, genetic_algorithm


# KNOB: NUMBER_GENE_LENGTH (default=3, range=1..16)
#   What it does: bit-width of each candidate number.
#   Effect: search space is 2**NUMBER_GENE_LENGTH. Length 3 is the
#       slide default (highest 3-bit number). Length 5 gives 32
#       possible individuals, 8 gives 256, etc.
#   Exam variants: bump to 5 or 8 for "highest n-bit number"
#       restatements of the in-class exercise (optional 4c).
NUMBER_GENE_LENGTH: int = 3

# KNOB: NUMBER_TARGET (default=None, allowed=None or int in [0, 2**LEN-1])
#   What it does: switches between two fitness rules.
#     • None  — fitness is the integer value of the gene. The GA
#               searches for the *largest* representable number.
#               This is the slide-10 default ("highest 3-bit").
#     • int v — fitness is `(2**LEN - 1) - |value - v|`. The GA
#               searches for the gene whose value is *closest* to
#               v. This is the slide-11 follow-up ("specific 3-bit
#               binary number — target 4").
#   Effect: the algorithm itself is identical; only the fitness
#       landscape changes. With a numeric target the fitness is
#       still strictly maximised and the GA's `>=` stop condition
#       still triggers when the perfect individual appears.
#   Exam variants: variant "target 4" → set to 4 AND ensure the
#       initial population does not already contain `(1, 0, 0)`
#       (see the HOW-TO-ADAPT note above). Variant "target 19 on
#       a 5-bit gene" → set GENE_LENGTH=5 and NUMBER_TARGET=19.
NUMBER_TARGET: int | None = None

# KNOB: NUMBER_MUTATION_BIT_RATE (default=0.1, range=0.0..1.0)
#   What it does: per-bit independent flip probability. Each bit
#       of the gene flips independently with this probability,
#       matching L05 §3.6.2 canonical mutation:
#           for i in 1..length(chromosome):
#               if random() < m: chromosome[i] = flip(chromosome[i])
#   Effect: With this rate at ~0.1 on a 3-bit gene the typical
#       call flips zero or one bit, occasionally two — exactly the
#       lecture's worked-example regime. Setting it to a high
#       value (e.g. 0.5) randomises the gene almost completely;
#       setting it to 0 disables internal mutation (only the outer
#       MUTATION_RATE gate fires the operator, but the per-bit
#       check then never flips anything).
#   Exam variants: leave at 0.1 for any standard exam question.
#       The OUTER per-individual gate is `MUTATION_RATE` in
#       ga_solution.py — that decides "does this child get
#       mutate() called at all"; this KNOB decides "given mutation
#       fires, how many bits actually flip".
NUMBER_MUTATION_BIT_RATE: float = 0.1

# KNOB: INITIAL_NUMBER_POPULATION (default=slide-5 set)
#   What it does: the starting population for the Number demo when
#       `NUMBER_USE_HARDCODED_POPULATION` is True. The default is the
#       four-individual set from slide 5 of the handout.
#   Effect: starting from a hand-crafted population lets you
#       reproduce the slide-6 → slide-9 walkthrough exactly; the
#       results in the slides assume this specific seed set.
#       For the slide-10 target `(1, 1, 1)` this set is safe
#       (the target is absent). For the slide-11 target 4 = `(1,
#       0, 0)`, the set is UNSAFE — `(1, 0, 0)` is present.
#   Exam variants: edit the tuples here to reproduce a different
#       slide variant or to remove a target that would otherwise be
#       already present (e.g. for target 4 remove `(1, 0, 0)`).
INITIAL_NUMBER_POPULATION: tuple[tuple[int, ...], ...] = (
    (1, 1, 0),
    (0, 0, 0),
    (0, 1, 0),
    (1, 0, 0),
)

# KNOB: NUMBER_USE_HARDCODED_POPULATION (default=True)
#   What it does: choose between the slide-shipped population
#       (`INITIAL_NUMBER_POPULATION` above) and a random one.
#   Effect: True reproduces the textbook walkthrough; False uses
#       `POPULATION_SIZE_NUMBER` (from ga_solution.py) random
#       individuals — the more honest GA setup but harder to
#       reason about by hand.
#   Exam variants: leave True for slide-faithful reproductions;
#       flip to False when the variant asks "what happens if you
#       start from a random pool", OR when the slide-11 target
#       you choose would otherwise be already present in the
#       hard-coded set.
NUMBER_USE_HARDCODED_POPULATION: bool = True


class NumberIndividual(Individual):
    """A candidate solution for the 3-bit-number exercise.

    The gene is a tuple of bits, e.g. (1, 0, 0). Two genes are equal
    iff their tuples are equal; the GA uses this to deduplicate the
    population via Python's `set` semantics (see `__hash__` below).
    """

    def __init__(self, gene: tuple):
        self.gene = gene

    def get_fitness(self) -> float:
        """Compute fitness from the gene.

        WHY two branches: the lab actually contains TWO 3-bit
        problems, on consecutive slides:
          • slide 10 ("Highest 3-bit binary number") — fitness is
            the integer value of the bitstring; the GA hunts for
            (1, 1, 1).
          • slide 11 ("Specific 3-bit binary number") — fitness is
            "closeness to a target number"; the GA hunts for
            whichever bitstring equals the target.
        Both variants must use the same `genetic_algorithm` driver,
        which maximises fitness. We therefore express the
        slide-11 variant as `(max possible value) - |value - target|`
        so it also stays maximisation-friendly.
        """
        # Decode the bit tuple. enumerate(reversed(gene)) yields
        # (position, bit) with position = 0 for the least-significant
        # bit, matching L05 §5.6 slide-31 binary place-value encoding.
        value = 0
        for position, bit in enumerate(reversed(self.gene)):
            value += bit * (2 ** position)

        if NUMBER_TARGET is None:
            return value  # slide 10 — maximise value

        # Slide-11 variant: fitness peaks at (2**L - 1) and decreases
        # linearly with |value - target|. Stays non-negative, so the
        # roulette-wheel selection in ga_solution.py works without a
        # shift.
        max_value = (2 ** len(self.gene)) - 1
        return max_value - abs(value - NUMBER_TARGET)

    def mutate(self) -> Self:
        """Per-bit mutation: each bit flips independently with
        probability NUMBER_MUTATION_BIT_RATE.

        Returns a *new* individual.

        WHY return a new instance (not mutate self): individuals are
        hashable (they live in a `set`); mutating in place would
        change an element's hash while it is still indexed by the
        old hash, corrupting the set. The GA expects an immutable-
        looking value object.

        WHY per-bit (vs "exactly one bit"): the L05 §3.6.2 canonical
        formulation flips each bit independently with probability
        m. Multiple bits can flip per call; with low m typically
        zero or one will. The slide-44 worked example happens to
        flip one bit, but the operator is structurally per-bit.
        """
        new_gene_list = []
        any_change = False
        for bit in self.gene:
            if random.random() < NUMBER_MUTATION_BIT_RATE:
                new_gene_list.append(1 - bit)
                any_change = True
            else:
                new_gene_list.append(bit)
        if not any_change:
            # Return self-equivalent (the set will deduplicate).
            return type(self)(self.gene)
        return type(self)(tuple(new_gene_list))

    def reproduce(self, other: Self) -> tuple[Self, Self]:
        """Single-point crossover with `other`. Returns TWO children.

        WHY two children: L05 §3.6.2 / §4.3 canonical single-point
        crossover returns `(child1, child2)`. child1 takes self's
        prefix + other's suffix; child2 takes other's prefix +
        self's suffix.

        WHY randint over [1, n-1]: a cut at position 0 would copy
        `other` verbatim, and a cut at position n would copy
        `self`. Neither is a meaningful crossover, so the slides
        implicitly assume an internal cut point. Note that cut=1
        and cut=n-1 produce minimally-recombined children that
        differ from one parent only in the last (or first) bit —
        this is intentional per the lecture's `[1, L-1]` range.
        """
        n = len(self.gene)
        if n < 2:
            return type(self)(self.gene), type(self)(other.gene)
        crossover_point = random.randint(1, n - 1)
        child1_gene = self.gene[:crossover_point] + other.gene[crossover_point:]
        child2_gene = other.gene[:crossover_point] + self.gene[crossover_point:]
        return type(self)(child1_gene), type(self)(child2_gene)

    def __hash__(self):
        return hash(self.gene)

    def __eq__(self, other) -> bool:
        # WHY override: needed for set-based deduplication; relying
        # on object identity would treat two (1, 1, 1) tuples as
        # different individuals.
        if not isinstance(other, NumberIndividual):
            return NotImplemented
        return self.gene == other.gene

    @classmethod
    def create_random(cls, length_of_gene: int) -> Self:
        return cls(tuple(random.randint(0, 1) for _ in range(length_of_gene)))

    def __repr__(self) -> str:
        return f"Gene: {self.gene} - Fitness: {self.get_fitness()}"


def get_initial_population(n: int, count: int) -> set[NumberIndividual]:
    """Build `count` unique random individuals of bit-length `n`.

    WHY a while-loop with a set: the lab specifies *unique*
    individuals (set semantics in `ga_solution.py`). If `count`
    approaches 2**n the loop becomes slow, so we explicitly guard
    against `count > 2**n` and return early.
    """
    if count > 2 ** n:
        raise ValueError(
            "Count must be at most 2**n; otherwise not enough unique "
            "individuals can be generated."
        )

    out: set[NumberIndividual] = set()
    while len(out) < count:
        out.add(NumberIndividual.create_random(n))
    return out


def build_initial_population() -> set[NumberIndividual]:
    """Choose between the hard-coded slide-5 seed and a random pool.

    Centralising the choice here lets `ga_solution.py` simply call
    `build_initial_population()` without knowing which KNOBs were
    flipped.
    """
    # Lazy-import the global POPULATION_SIZE_NUMBER so a flip in
    # `ga_solution.py` takes effect here without a re-import.
    from ga_solution import POPULATION_SIZE_NUMBER

    if NUMBER_USE_HARDCODED_POPULATION:
        return {NumberIndividual(tuple(g)) for g in INITIAL_NUMBER_POPULATION}
    return get_initial_population(
        NUMBER_GENE_LENGTH, POPULATION_SIZE_NUMBER
    )


def main():
    """Slide-10 exercise: run the GA on the 3-bit-number problem.

    Reads all knobs from `ga_solution.py` (the canonical
    configuration source) so that running this file directly
    behaves identically to running `ga_solution.py` with
    `RUN_QUEENS_DEMO = False`.
    """
    # Lazy-import the globals so a flip in `ga_solution.py`
    # propagates here even when this file is executed directly.
    from ga_solution import (
        MAX_GENERATIONS_NUMBER,
        MINIMAL_FITNESS_NUMBER,
        MUTATION_RATE,
        TRIM_POPULATION,
        USE_MU_PLUS_LAMBDA,
        RANDOM_SEED,
    )

    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED)

    target = (
        MINIMAL_FITNESS_NUMBER
        if MINIMAL_FITNESS_NUMBER is not None
        else (2 ** NUMBER_GENE_LENGTH) - 1
    )
    initial_population = build_initial_population()
    fittest = genetic_algorithm(
        initial_population,
        minimal_fitness=target,
        num_of_generations=MAX_GENERATIONS_NUMBER,
        should_trim_population=TRIM_POPULATION,
        p_mutation=MUTATION_RATE,
        use_mu_plus_lambda=USE_MU_PLUS_LAMBDA,
    )
    print(f"Fittest Individual: {fittest}")


if __name__ == "__main__":
    main()

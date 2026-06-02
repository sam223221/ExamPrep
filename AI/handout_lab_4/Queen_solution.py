"""
LAB 4: Genetic Algorithm — N-Queens (homework)
==============================================

PROBLEM STATEMENT (from Lab 4.pdf, slides 12-18):
-------------------------------------------------
"Modify your GA program given the following problem and code
(queens_fitness.py): Place n-queens on a chessboard in non-conflicting
positions."

  - Representation: a tuple of n integers; index = column,
    value = row of the queen in that column. Slide 13 gives the
    example `(3, 4, 2, 6, 1, 7, 8, 5)` for n=8.
  - Fitness: from `queens_fitness.py` — number of *non-conflicting*
    queen pairs (positive, max = n(n-1)/2) OR minus the number of
    conflicting pairs (negative, max = 0). The slides use both;
    the GA in `ga_solution.py` maximises, so we use the negative
    variant by default and stop at 0.
  - Selection: roulette (fitness-proportionate) — implemented in
    `ga_solution.py`. To support the negative fitness, the
    selection routine shifts fitness by `-min_fitness` when the
    minimum is negative.
  - Crossover: single-point. Slides 15 ("crossover example") and 16
    ("full example") illustrate single-point crossover; the
    homework brief says "two new children are produced from the
    crossover" — `Board.reproduce` returns BOTH children as a
    tuple, matching the lecture L05 §3.6.2 canonical form.
  - Mutation: with probability `QUEENS_MUTATION_COLUMN_RATE` per
    column, reassign that column's row to a new random value in
    [1, n] (lecture-canonical per-column independent flip).
  - Initial population: random tuples of length n with values in
    [1, n].

The homework asks for:
  • `get_fitness()` — uses queens_fitness.
  • `reproduce()` — single-point crossover.
  • `mutate()` — one column → new row in [1, n].
  • `get_initial_population()` — `count` random boards.
  • Wire `genetic_algorithm(...)` correctly in `main()`.
This file implements all five.

MENTAL MODEL (one-line analogy):
--------------------------------
Each Board is a candidate queen-arrangement (one queen per column),
the fitness scoreboard penalises queens that can attack each other,
and the GA evolves toward a non-attacking layout.

REFERENCES:
-----------
- Lecture L05 §3 / §4 — Genetic Algorithm (the canonical n-queens
  example is the standard slide motivation for GAs).
- Glossary: Genetic algorithm, Fitness function, Crossover,
  Mutation, Chromosome, Population, Roulette-wheel selection,
  Local search.
- See `study/lectures/L05-Local-Search.md` (once locked).

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
1. To solve k-queens for any k >= 4 (variant 1 in
   `study/_exam/Lab4-GA/variants.md`): set `N_QUEENS = k` in
   `ga_solution.py`. The Board class respects N_QUEENS for every
   constructor, mutation, and initial-population call.
2. To tune mutation rate (variant 2): change `MUTATION_RATE` in
   `ga_solution.py`. To distinguish between "this individual got
   chosen for mutation" and "given that, what's the inner
   per-column probability", also expose
   `QUEENS_MUTATION_COLUMN_RATE` here (defaults to 0.25 — close to
   the lecture's per-gene-with-prob-m formulation).
3. To switch fitness direction (variant 3): set
   `QUEENS_FITNESS_VARIANT = "positive"` here AND set
   `MINIMAL_FITNESS_QUEENS` in `ga_solution.py` to the new
   per-board maximum (= n*(n-1)//2). The Board class will route to
   `fitness_fn_positive` automatically.
4. To experiment with weighted conflicts (not in the locked variant
   bank — useful for self-practice): set
   `QUEENS_FITNESS_VARIANT = "weighted"` and tune `QUEENS_DIAG_WEIGHT`
   / `QUEENS_ROW_WEIGHT`. By construction columns cannot conflict
   under this gene encoding (one queen per column), so there is no
   column-weight knob — only diagonal and row weights are
   meaningful.
5. To enable elitism (preserve the best individual across
   generations): not implemented directly. The closest approximation
   is the combination `USE_MU_PLUS_LAMBDA = True` and
   `TRIM_POPULATION = True` in `ga_solution.py`.

OUTPUTS WHEN RUN:
-----------------
Running this file directly (`py -3.12 Queen_solution.py`) runs the
N-Queens GA at the defaults (`N_QUEENS = 4`, single-point
crossover, negative fitness, `MAX_GENERATIONS = 100`). On a
4-queens problem the GA reliably converges within ~10-50
generations to a tuple whose fitness is 0 (no conflicts). It also
prints elapsed wall-clock milliseconds.

ENTRY POINT: no
---------------
This module is a helper imported by `ga_solution.py`. The Lab 4
entry point is `ga_solution.py` (it runs both the Number demo and
the N-Queens homework). Running this file directly is supported
(the `__main__` block exercises only the N-Queens demo).
"""

import random
from typing import Self

from ga_solution import Individual, genetic_algorithm
from queens_fitness_solution import (
    fitness_fn_negative,
    fitness_fn_positive,
    fitness_fn_weighted,
)


# KNOB: QUEENS_FITNESS_VARIANT (default="negative",
#       allowed={"negative", "positive", "weighted"})
#   What it does: chooses which fitness function in
#       `queens_fitness_solution.py` to use.
#     • "negative" — return -conflicts. Maximum is 0. Default.
#     • "positive" — return non-conflicting pairs. Maximum is
#                    n*(n-1)//2.
#     • "weighted" — return -(weighted conflicts), using the
#                    `QUEENS_DIAG_WEIGHT` and `QUEENS_ROW_WEIGHT`
#                    knobs as multipliers.
#   Effect: changes the fitness landscape; the GA still maximises.
#       When you switch to "positive", you must also lift
#       MINIMAL_FITNESS_QUEENS in `ga_solution.py` so the early-
#       termination condition matches the new optimum.
#   Exam variants: "positive" is variant 3 in variants.md.
#       "weighted" is a self-practice extension only — it is NOT in
#       the locked variant bank.
QUEENS_FITNESS_VARIANT: str = "negative"

# KNOB: QUEENS_DIAG_WEIGHT (default=1, range=1..N)
#   What it does: multiplier applied to diagonal conflicts when
#       QUEENS_FITNESS_VARIANT == "weighted". Ignored otherwise.
#   Effect: see `queens_fitness_solution.DEFAULT_DIAG_WEIGHT`. With
#       weight=1 this fully matches the default "negative" variant.
#   Exam variants: not exercised by the locked variant bank;
#       self-practice only.
QUEENS_DIAG_WEIGHT: int = 1

# KNOB: QUEENS_ROW_WEIGHT (default=1, range=1..N)
#   What it does: multiplier applied to row conflicts under the
#       "weighted" fitness. Ignored otherwise.
#   Effect: weight=1 reproduces default scoring; higher weights
#       force the GA to spread queens vertically first.
#   Exam variants: not exercised by the locked variant bank;
#       self-practice only.
QUEENS_ROW_WEIGHT: int = 1

# KNOB: QUEENS_MUTATION_COLUMN_RATE (default=0.25, range=0.0..1.0)
#   What it does: per-column probability that the column's row
#       value is reassigned to a fresh random value in [1, n].
#       Matches the lecture L05 §3.6.2 per-gene-with-probability-m
#       formulation. Each column is checked independently;
#       multiple columns can mutate per call.
#   Effect: low values (e.g. 0.1) — at most one or two columns
#       typically change per call. Higher values (e.g. 0.5+) — many
#       columns change, approaching random reseeding.
#   Exam variants: keep at 0.25 for standard runs. Use `MUTATION_RATE`
#       in ga_solution.py for the outer per-board mutation gate.
QUEENS_MUTATION_COLUMN_RATE: float = 0.25


type BoardView = tuple[int, ...]


def _score(board_view: BoardView) -> float:
    """Route a board's fitness through whichever variant is active.

    Centralised so `Board.get_fitness` stays small and so that
    flipping QUEENS_FITNESS_VARIANT at runtime is a single dispatch
    point — the rest of the module never names the underlying
    queens_fitness function directly.
    """
    if QUEENS_FITNESS_VARIANT == "negative":
        return float(fitness_fn_negative(board_view))
    if QUEENS_FITNESS_VARIANT == "positive":
        return float(fitness_fn_positive(board_view))
    if QUEENS_FITNESS_VARIANT == "weighted":
        return float(fitness_fn_weighted(
            board_view,
            diag_weight=QUEENS_DIAG_WEIGHT,
            row_weight=QUEENS_ROW_WEIGHT,
        ))
    raise ValueError(
        f"Unknown QUEENS_FITNESS_VARIANT: {QUEENS_FITNESS_VARIANT!r}. "
        f"Expected one of: 'negative', 'positive', 'weighted'."
    )


class Board(Individual):
    """A candidate n-queens arrangement.

    The gene is a tuple of length n; gene[col] is the row of the
    queen sitting in column `col`. Rows are 1-based to match the
    slide-14 example `(5, 6, 2, 3, 5, 8, 6, 1)`. The underlying
    `queens_fitness` module does not care about the offset — it
    only compares row values to each other.
    """

    def __init__(self, gene: BoardView):
        self.gene = gene

    def get_fitness(self) -> float:
        return _score(self.gene)

    def mutate(self) -> Self:
        """Per-column mutation: each column's row is independently
        reassigned to a fresh random row in [1, n] with probability
        QUEENS_MUTATION_COLUMN_RATE.

        WHY per-column (vs "exactly one column"): the lecture L05
        §3.6.2 canonical mutation is per-gene-with-probability-m
        (each gene independently flips). For the queens problem
        each "gene" is one column's row assignment; per-column
        independent reassignment is the direct translation.

        We do NOT exclude the current row — the slides don't
        either, and excluding it would skew the row distribution.
        """
        n = len(self.gene)
        new_gene_list = []
        any_change = False
        for row in self.gene:
            if random.random() < QUEENS_MUTATION_COLUMN_RATE:
                new_row = random.randint(1, n)
                new_gene_list.append(new_row)
                if new_row != row:
                    any_change = True
            else:
                new_gene_list.append(row)
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

        WHY randint over [1, n-1]: same reasoning as
        NumberIndividual.reproduce — an internal cut so the
        children differ from both parents.
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
        if not isinstance(other, Board):
            return NotImplemented
        return self.gene == other.gene

    @classmethod
    def create_random(cls, n_queens: int) -> Self:
        """Generate a random n-queens gene with rows in [1, n].

        WHY randint(1, n): the slide-14 example uses 1-based rows
        (e.g. row 5 in column a). queens_fitness only compares
        row values to each other so the offset is harmless either
        way; we choose 1-based to keep the displayed gene tuples
        legible alongside the slide.
        """
        gene = tuple(random.randint(1, n_queens) for _ in range(n_queens))
        return cls(gene)

    def __repr__(self) -> str:
        return f"Gene: {self.gene} - Fitness: {self.get_fitness()}"


def get_initial_population(count: int, n_queens: int = 4) -> set[Board]:
    """Build `count` random boards of size n_queens.

    WHY a while-loop with a set: the original handout doc-string
    says "Note since it uses a set it disregards duplicate elements"
    — duplicates are not added to the result, but we keep drawing
    until we hit the requested count.

    Note on capacity: n_queens of size n has n**n possible boards,
    so collisions are negligible for any realistic count <= 200.

    Default `n_queens=4` matches the lab default `N_QUEENS = 4` in
    ga_solution.py. Callers in ga_solution.py always pass it
    explicitly.
    """
    out: set[Board] = set()
    while len(out) < count:
        out.add(Board.create_random(n_queens))
    return out


def test() -> None:
    """Smoke-test stub ported forward from the template Queen.py.

    The original template (`Queen.py`) defines:

        def test():
            print(Board((1, 2, 3, 4, 5, 6, 7, 8)).get_fitness())

    Purpose: a one-liner that constructs a Board with a known gene
    (the slide-13 example `(1, 2, 3, 4, 5, 6, 7, 8)` — main diagonal,
    every pair conflicts on the row+1 diagonal) and prints its
    fitness. Used by the lab handout as a "does it import / does
    `get_fitness` not crash" sanity check.

    Behaviour preserved exactly so any rubric / IDE-marker that
    looks up `Queen_solution.test` finds the same callable shape.
    """
    print(Board((1, 2, 3, 4, 5, 6, 7, 8)).get_fitness())


def main():
    """Run the N-Queens GA using the global KNOBs in `ga_solution.py`.

    Reads its configuration from the canonical KNOB block so that
    running this file directly behaves identically to running
    `ga_solution.py` with `RUN_NUMBER_DEMO = False`.

    Wired exactly as the slide-17 "Call the genetic algorithm
    function correctly in the main function" homework asks.
    """
    import time

    # Lazy-import the globals so a flip in `ga_solution.py`
    # propagates here even when this file is executed directly.
    from ga_solution import (
        N_QUEENS,
        POPULATION_SIZE,
        MAX_GENERATIONS,
        MINIMAL_FITNESS_QUEENS,
        MUTATION_RATE,
        TRIM_POPULATION,
        USE_MU_PLUS_LAMBDA,
        RANDOM_SEED,
    )

    if RANDOM_SEED is not None:
        random.seed(RANDOM_SEED)

    print(f"===== Lab 4 — Homework (N-Queens, N = {N_QUEENS}) =====")
    initial_population = get_initial_population(POPULATION_SIZE, N_QUEENS)

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

    if fittest is None:
        print("No fittest individual produced (population was empty).")
    else:
        print(f"Fittest Individual: {fittest} - "
              f"fitness: {fittest.get_fitness()}")
    elapsed_time = (end_time - start_time) / 10 ** 6
    print(f"total elapsed time: {elapsed_time:.3f} ms")
    return fittest


if __name__ == "__main__":
    main()

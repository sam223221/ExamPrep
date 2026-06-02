"""
LAB 4: Genetic Algorithm / N-Queens — Fitness module
====================================================

PROBLEM STATEMENT (from Lab 4.pdf, Hint slide):
-----------------------------------------------
"Use the queens_fitness module for the homework to calculate the
fitness levels." The handout ships two precomputed fitness functions
that score a board (a tuple where index = column and value = row of
the queen in that column):

- `fitness_fn_negative(board)`  — returns *minus* the number of
  conflicting pairs. Zero is perfect; more negative is worse. We
  *maximise* this and stop at 0.
- `fitness_fn_positive(board)`  — returns the number of
  non-conflicting pairs. For an n-queens board the maximum is
  C(n, 2) = n*(n-1)/2.

Both fitness functions count attacks the same way: two queens
conflict if they share a row, share a column (impossible by
construction in this representation — one per column), or share a
diagonal (`|dx| == |dy|`).

MENTAL MODEL (one-line analogy):
--------------------------------
This module is the *scoreboard*. It does not play the GA — it tells
the GA how good a candidate chessboard is. The GA maximises whatever
number this scoreboard prints; the only difference between the two
variants is which direction is "good" (toward 0 vs toward `n*(n-1)/2`).

REFERENCES:
-----------
- Lecture L05 §3 / §4 — Genetic Algorithm (fitness function role).
- Glossary: Fitness function, Genetic algorithm, N-queens.
- See `study/lectures/L05-Local-Search.md` (once locked).

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
1. To switch direction (variant 3 in
   `study/_exam/Lab4-GA/variants.md`): leave this module alone and
   flip `QUEENS_FITNESS_VARIANT` in `Queen_solution.py` to
   `"positive"` — the Board class will route to
   `fitness_fn_positive` instead. You must also lift
   `MINIMAL_FITNESS_QUEENS` (in `ga_solution.py`) from 0 to
   `n*(n-1)//2`.
2. To penalise diagonal conflicts more heavily: call
   `fitness_fn_weighted` with `diag_weight = 3` from the Board's
   `get_fitness()` (set `QUEENS_FITNESS_VARIANT = "weighted"` and
   `QUEENS_DIAG_WEIGHT = 3` in `Queen_solution.py`). Note: there is
   no column-weight knob — column conflicts are structurally
   impossible under this gene encoding (one queen per column), so a
   column-weight parameter would have no effect. Only `diag_weight`
   and `row_weight` are meaningful.
3. To make the GA *minimise* a positive cost instead of maximising a
   negative one, return `+conflicts` and flip the comparison in
   `genetic_algorithm` (`>=` → `<=`). The solution opts to maximise
   throughout because that is what the lab's `ga_solution.py`
   expects.
4. To penalise row conflicts independently of diagonal conflicts:
   pass `row_weight = 2` to `fitness_fn_weighted` — useful for exam
   questions about "what if horizontal attacks were considered
   worse than diagonal attacks".

OUTPUTS WHEN RUN:
-----------------
Running this file directly prints fitness scores for two example
boards from slide 14 of the handout
(`(5,6,2,3,5,8,6,1)` and `(7,3,6,6,4,6,8,1)`), under all three
fitness variants — useful for sanity-checking before the GA is
invoked.

ENTRY POINT: no
---------------
This module is a helper imported by `Queen_solution.py`. The Lab 4
entry point is `ga_solution.py`.
"""

from typing import Iterable


# KNOB: DEFAULT_DIAG_WEIGHT (default=1, range=1..N)
#   What it does: multiplier applied to diagonal conflicts inside
#       fitness_fn_weighted. Diagonals are by far the most common
#       conflict in this representation (one-queen-per-column already
#       eliminates column attacks), so this knob primarily controls
#       the *severity* assigned to a diagonal clash.
#   Effect: A higher weight makes the GA spend more selection
#       pressure on resolving diagonals first; with weight=1 it
#       matches the slide-shipped `fitness_fn_negative` behaviour
#       exactly.
#   Exam variants: variant "penalise diagonals 3x" — set to 3 in
#       a fresh call; the solver does not change its API.
DEFAULT_DIAG_WEIGHT: int = 1

# KNOB: DEFAULT_ROW_WEIGHT (default=1, range=1..N)
#   What it does: multiplier applied to row conflicts (queens on the
#       same horizontal line). Independent of the diagonal weight.
#   Effect: With row weight = 1 we exactly recover the
#       slide-shipped scoring rule. Row weight > 1 makes the GA
#       prioritise spreading queens vertically.
#   Exam variants: variant "rows are forbidden but diagonals are
#       allowed" — set row weight to a very large number; the GA
#       will converge to a board with no horizontal collisions even
#       if diagonals remain.
DEFAULT_ROW_WEIGHT: int = 1


def fitness_fn_negative(board_view: tuple[int, ...]) -> int:
    """Return *minus* the number of conflicting queen pairs.

    Two queens at (col_i, row_i) and (col_j, row_j) conflict iff:
      • row_i == row_j  (same row), OR
      • |col_i - col_j| == |row_i - row_j|  (same diagonal).
    Columns can never collide in this representation because the
    gene assigns exactly one queen per column index.

    The GA in ga_solution.py *maximises* this value, so a perfect
    n-queens solution scores 0 and worse boards score negative
    numbers. This matches the slide-shipped `fitness_fn_negative`
    line for line.
    """
    # WHY: enumerate pairs once (i < j) instead of comparing every
    # ordered pair — saves a factor of 2 and avoids self-comparisons.
    n = len(board_view)
    conflicts = 0
    for column, row in enumerate(board_view):
        for other_column in range(column + 1, n):
            dx = abs(column - other_column)
            dy = abs(row - board_view[other_column])
            # dx == dy: on a diagonal. dy == 0: on the same row.
            # dx == 0 is impossible because other_column != column.
            if dx == dy or dy == 0:
                conflicts += 1
    return -conflicts


def fitness_fn_positive(state: tuple[int, ...]) -> int:
    """Return the number of *non-conflicting* queen pairs.

    Parameter name matches the original `queens_fitness.py` template
    (`def fitness_fn_positive(state)`), preserving the signature any
    handout marker / IDE rename might rely on.

    Mirror of `fitness_fn_negative`: max equals C(n, 2) = n*(n-1)/2
    for an n-queens board (every pair is friendly), and decreases as
    conflicts appear. The GA still maximises, but the "perfect"
    target shifts from 0 to n*(n-1)/2.
    """
    n = len(state)
    # WHY: derive non-conflict count from conflict count rather than
    # re-iterate pairs. Total pairs = n*(n-1)/2; non-conflicts = total
    # minus conflicts. This keeps the two variants algebraically
    # consistent and avoids the buggy double-counting present in the
    # slide-shipped `fitness_fn_positive` template.
    conflicts = -fitness_fn_negative(state)
    total_pairs = n * (n - 1) // 2
    return total_pairs - conflicts


def fitness_fn_weighted(
    board_view: tuple[int, ...],
    diag_weight: int = DEFAULT_DIAG_WEIGHT,
    row_weight: int = DEFAULT_ROW_WEIGHT,
) -> int:
    """Return -(weighted sum of conflicts).

    Allows exam variants to penalise different conflict types
    differently. With both weights = 1 (the defaults) this reduces to
    `fitness_fn_negative` and the GA's stop condition (>= 0) still
    works.
    """
    n = len(board_view)
    cost = 0
    for column, row in enumerate(board_view):
        for other_column in range(column + 1, n):
            dx = abs(column - other_column)
            dy = abs(row - board_view[other_column])
            if dy == 0:
                cost += row_weight
            elif dx == dy:
                cost += diag_weight
    return -cost


def _smoke_test(boards: Iterable[tuple[int, ...]]) -> None:
    """Print every variant's score for each board. Used by __main__
    only — not called from the GA.
    """
    for board in boards:
        n = len(board)
        max_pos = n * (n - 1) // 2
        neg = fitness_fn_negative(board)
        pos = fitness_fn_positive(board)
        weighted_3 = fitness_fn_weighted(board, diag_weight=3)
        print(
            f"board={board!r:30s} "
            f"negative={neg:>4d}  "
            f"positive={pos:>4d}/{max_pos:<4d}  "
            f"diag3x={weighted_3:>4d}"
        )


if __name__ == "__main__":
    # The two boards from slide 14 of Lab 4.pdf — both score
    # negative under the default weights, matching the slide labels
    # "Fitness: -6" and "Fitness: -7". Hard-assert so a regression
    # actually crashes (not just prints different numbers).
    slide14_left = (5, 6, 2, 3, 5, 8, 6, 1)
    slide14_right = (7, 3, 6, 6, 4, 6, 8, 1)
    perfect_4 = (2, 4, 1, 3)

    assert fitness_fn_negative(slide14_left) == -6, (
        f"Slide-14 left board {slide14_left} should score -6, got "
        f"{fitness_fn_negative(slide14_left)}"
    )
    assert fitness_fn_negative(slide14_right) == -7, (
        f"Slide-14 right board {slide14_right} should score -7, got "
        f"{fitness_fn_negative(slide14_right)}"
    )
    assert fitness_fn_negative(perfect_4) == 0, (
        f"Perfect 4-queens board {perfect_4} should score 0, got "
        f"{fitness_fn_negative(perfect_4)}"
    )
    assert fitness_fn_positive(perfect_4) == 6, (
        f"Perfect 4-queens board {perfect_4} should score 6 under "
        f"the positive variant (= 4*3/2), got "
        f"{fitness_fn_positive(perfect_4)}"
    )

    _smoke_test([slide14_left, slide14_right, perfect_4])

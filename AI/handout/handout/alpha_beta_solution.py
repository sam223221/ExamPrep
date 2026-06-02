"""
LAB 5 (module): Alpha-Beta Pruning on Nim
=========================================

PROBLEM STATEMENT (from Lab 5.pdf, slides 9-12 — "Homework Nim"):
-----------------------------------------------------------------
Implement the game of Nim with alpha-beta search.

Nim rules (slide 10):
  * A single pile of N tokens sits between two opponents.
  * At each move the current player must split ONE pile into two NON-EMPTY
    piles of DIFFERENT sizes. So a pile of 6 may become [5,1] or [4,2] but
    NOT [3,3]; a pile of 7 may become [6,1], [5,2] or [4,3].
  * The first player who can no longer move loses (i.e. when every pile has
    size 1 or 2 — none of those can be split into two unequal positive
    parts).

The handout (slide 12) asks the student to:
  1. Rewrite Nim using `alpha_beta_decision`.
  2. Test it with starting piles of 7, 15, and 20.
  3. Note that with 7 tokens MIN (the human, who moves first) is certain to
     lose against a perfect MAX opponent.

In this template:
  * The USER moves first (so the USER is the MIN player here, matching the
    slide's "MIN should start the game" remark).
  * The COMPUTER (MAX) responds with the optimal alpha-beta move.
  * `utility_of` returns +1 if the COMPUTER wins, -1 if the USER wins
    (slide-11 convention).

MENTAL MODEL (one-line analogy):
--------------------------------
Alpha-beta pruning is like reading a chess book: the moment you realise a
candidate line is worse than something you have already considered, you
stop reading it — you do not need to know exactly HOW bad it is, only that
it is worse than your current best.

REFERENCES:
-----------
- Lecture 6 (Adversarial Search) — see study/lectures/L06-Adversarial-Search.md
  * §3 minimax, §3 alpha-beta pruning, §3 alpha cutoff, §3 beta cutoff.
- Lecture 6 slides 20-35 (alpha-beta derivation).
- Glossary terms (study/_shared/glossary.md): "Alpha-beta pruning",
  "Alpha cutoff", "Beta cutoff", "Minimax", "Utility function",
  "Successor function", "Terminal test", "Branching factor".

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
1. To change the starting pile size (variant: "test with 15 and 20"):
     set START_PILE = 15  (or 20, or any positive integer >= 3).

2. To make the COMPUTER play MIN instead of MAX (slide 12 step 3):
     set COMPUTER_PLAYS_MAX = False.
     `utility_of` then flips its sign: it returns +1 when MIN wins.

3. To toggle whether alpha-beta pruning is actually used (e.g. when an
   exam variant asks "compare nodes evaluated with and without pruning"):
     set USE_ALPHA_BETA_PRUNING = False to fall back to plain minimax.

4. To count the number of game-tree nodes the solver evaluates (useful for
   variant: "report nodes evaluated with and without pruning"):
     set COUNT_NODES = True. The script prints the count after each call
     to `alpha_beta_decision` / `minmax_decision`.

5. To switch the move-ordering heuristic (variant: "compare pruning
   effectiveness with different move orderings"):
     set MOVE_ORDERING ∈ {"natural", "balanced-first", "skewed-first"}.

6. To inspect the root utility programmatically without driving the
   interactive REPL (variant 4 — "is COMPUTER guaranteed to win from
   [15]?"):
     `from alpha_beta_solution import root_utility`
     `root_utility([15], to_move="MIN")`  # USER (MIN) opens, slide-10.
     Sign convention: +1 = COMPUTER wins (with default COMPUTER_PLAYS_MAX
     = True); flip COMPUTER_PLAYS_MAX to invert.

OUTPUTS WHEN RUN:
-----------------
This module is independent of `tictactoe_template_solution.py`. Each file
has its own copy of the alpha-beta engine and its own KNOB block; editing
a KNOB in this file affects ONLY the Nim game (and vice versa). Running
this file directly drives the Nim REPL described on slide 12.

ENTRY POINT: yes — but optional. Running `py -3.12 alpha_beta_solution.py`
plays one Nim game (interactive). The canonical lab entry point that is
exercised by the Verifier is `tictactoe_template_solution.py` (it
demonstrates the Tic-Tac-Toe exercise from slides 4-8 end-to-end without
requiring any keyboard input).
"""

from collections.abc import Iterable
from typing import Callable

# ============================================================================
# KNOBs — exam-tunable parameters (Lecture 6 / Lab 5)
# ============================================================================

# KNOB: START_PILE (default=7, allowed=any int >= 3)
#   What it does: number of tokens in the single starting pile of Nim.
#   Effect: search-tree depth grows roughly linearly with the pile size,
#           branching factor grows roughly as N/2. With N=7 the game is
#           trivial; N=15 produces a deeper tree where pruning matters;
#           N=20 begins to show the alpha-beta speed-up clearly.
#   Exam variants: 7 (slide 11 default), 15 and 20 (slide 12 homework).
START_PILE = 7

# KNOB: COMPUTER_PLAYS_MAX (default=True, allowed={True, False})
#   What it does: whether the computer (alpha_beta_decision) plays the MAX
#           side of the game tree.
#   Effect: with the default True the computer maximises utility_of and the
#           user is MIN (matching the slide-11 figure where MIN moves
#           first). With False the script swaps roles and `utility_of`
#           returns +1 when MIN wins (slide-12 homework step 3).
#   Exam variants: True (slides 9-11), False (slide 12 step 3 — "play the
#           MIN position").
COMPUTER_PLAYS_MAX = True

# KNOB: USE_ALPHA_BETA_PRUNING (default=True, allowed={True, False})
#   What it does: enable/disable the alpha-beta cutoff checks inside
#           `alpha_beta_decision`.
#   Effect: when False the algorithm becomes plain minimax — it returns the
#           SAME move but evaluates every leaf. Useful to demonstrate that
#           alpha-beta is a SPEED optimisation, not a correctness change
#           (Lecture 6 §3, "best-case O(b^{d/2})").
#   Exam variants: report nodes evaluated with True vs False; verify that
#           the chosen move is identical either way.
USE_ALPHA_BETA_PRUNING = True

# KNOB: COUNT_NODES (default=True, allowed={True, False})
#   What it does: instrument the recursion to count every (state, depth)
#           visited during one alpha_beta_decision call.
#   Effect: enables a print line "[alpha-beta] evaluated N states" after
#           each top-level decision. Used in variant-1 of variants.md
#           ("report nodes evaluated with and without pruning").
#   Exam variants: True for the variant-1 measurement; False for clean
#           transcripts.
COUNT_NODES = True

# KNOB: MOVE_ORDERING (default="natural", allowed={"natural",
#                                                  "balanced-first",
#                                                  "skewed-first"})
#   What it does: order the children returned by `successors_of` before
#           alpha-beta inspects them. Ordering is by the spread of the
#           NEW pair (not the whole post-split state).
#   Effect: alpha-beta's pruning quality depends heavily on move ordering
#           — perfect ordering achieves O(b^{d/2}), random ordering tends
#           toward O(b^{3d/4}). "balanced-first" tries splits whose two
#           halves are closest in size first (e.g. [3,4] before [1,6]).
#           "skewed-first" reverses that. Unknown values raise ValueError.
#   Exam variants: tied to variants.md variant 3 ("compare pruning
#           effectiveness with different move orderings"). Note: this
#           Nim file does NOT have a MAX_DEPTH KNOB (the slide-12 game
#           is small enough that full-depth search is feasible); use the
#           Tic-Tac-Toe file for depth-cut experiments.
MOVE_ORDERING = "natural"


# ============================================================================
# Game type aliases
# ============================================================================

type Piles = list[int]


# ============================================================================
# Counters (driven by COUNT_NODES)
# ============================================================================

# Module-level counter that exam variant scripts can read directly.
nodes_evaluated: int = 0

# Bounds-of-the-recursion sentinel.
_INFINITY: float = float('inf')


def reset_node_counter() -> None:
    """Reset the global counter before a new top-level decision."""
    global nodes_evaluated
    nodes_evaluated = 0


# ============================================================================
# Alpha-beta decision (handout's template, instrumented)
# ============================================================================

def max_value(state_option: Piles, alpha: float, beta: float) -> float:
    """MAX side of the alpha-beta recursion.

    Exposed at module level so exam variants (e.g. variants.md variant 4)
    can call it directly to inspect the root utility from a given Nim
    state. Returns the minimax value as a `float` (the bounds `-inf` /
    `+inf` propagate through intermediate calls; at terminal states the
    value coincides with `utility_of`, an int).
    """
    global nodes_evaluated
    if COUNT_NODES:
        nodes_evaluated += 1

    if is_terminal(state_option):
        return utility_of(state_option)

    expected_value = -_INFINITY
    for successor in successors_of(state_option):
        expected_value = max(expected_value, min_value(successor, alpha, beta))
        # The beta cutoff: if MAX can already guarantee >= beta, the
        # MIN parent will never let the game reach this branch.
        if USE_ALPHA_BETA_PRUNING and expected_value >= beta:
            return expected_value
        alpha = max(alpha, expected_value)
    return expected_value


def min_value(state_option: Piles, alpha: float, beta: float) -> float:
    """MIN side of the alpha-beta recursion. See `max_value` for notes
    on the module-level exposure."""
    global nodes_evaluated
    if COUNT_NODES:
        nodes_evaluated += 1

    if is_terminal(state_option):
        return utility_of(state_option)

    v = _INFINITY
    for successor in successors_of(state_option):
        v = min(v, max_value(successor, alpha, beta))
        # The alpha cutoff (Lecture 6 slide 22): if MIN can already
        # guarantee <= alpha, the MAX ancestor will never choose us.
        if USE_ALPHA_BETA_PRUNING and v <= alpha:
            return v
        beta = min(beta, v)
    return v


def root_utility(state: Piles, *, to_move: str = "MIN") -> float:
    """Inspect the minimax value of `state` assuming optimal play.

    `to_move` selects which side acts at the root:
      * "MIN" (default, slide-10 convention: USER opens Nim).
      * "MAX" (the COMPUTER acts first — e.g. when COMPUTER_PLAYS_MAX is
        False, so the COMPUTER plays MIN but you still want to ask "what
        is the value here if I were MAX?").

    Useful for variants.md variant 4 ("is COMPUTER guaranteed to win from
    [15]?") — you can call `root_utility([15])` and inspect the sign
    without driving the interactive REPL.
    """
    if to_move not in {"MIN", "MAX"}:
        raise ValueError(
            f"to_move must be 'MIN' or 'MAX', got {to_move!r}"
        )
    if to_move == "MIN":
        return min_value(state, -_INFINITY, _INFINITY)
    return max_value(state, -_INFINITY, _INFINITY)


def alpha_beta_decision(state: Piles) -> Piles:
    """
    Return the SUCCESSOR STATE that the computer should move to.

    Implementation note: this is the "handout-style root" — it calls
    `min_value` independently for each top-level successor via `argmax`,
    so the alpha bound is NOT threaded across top-level siblings. The
    inner `max_value` / `min_value` are textbook alpha-beta (Lecture 6 §3).
    """
    state = argmax(
        successors_of(state),
        lambda a: min_value(a, -_INFINITY, _INFINITY)
    )
    return state


# ============================================================================
# is_terminal / utility_of / successors_of — the three TODOs in the handout
# ============================================================================

def is_terminal(state: Piles) -> bool:
    """
    A Nim state is terminal when no legal split exists — that is, every
    pile has size 1 or 2 (a pile of 1 has no split; a pile of 2 can only
    split into [1,1] which is forbidden because the parts must be
    different).
    """
    # WHY all(...): the game ends when NO pile can be split, not just when
    # ONE cannot. A single pile of >=3 keeps the game alive even if
    # everything else is dust.
    return all(pile <= 2 for pile in state)


def utility_of(state: Piles) -> int:
    """
    Sign convention (slide 11):
      * The USER (MIN) makes the first move from the starting [N] pile.
      * Each successful split adds exactly one pile, so len(state) tells
        us how many splits have happened so far:
          len == 1 → no splits yet      → USER's turn  (USER = MIN)
          len == 2 → 1 split done       → COMPUTER's turn (COMPUTER = MAX)
          len == 3 → 2 splits done      → USER's turn
          ...
      * At a TERMINAL state the player whose turn it is just lost
        (they cannot move). So:
          - terminal with odd len  → USER's turn → USER lost → +1.
          - terminal with even len → COMPUTER's turn → COMPUTER lost → -1.

    When COMPUTER_PLAYS_MAX is False we flip the sign (slide 12 step 3:
    "play the MIN position — utility_of should return +1 for MIN").
    """
    if not is_terminal(state):
        # Non-terminal states do not have a defined utility in the
        # zero-sum convention used by the slides.
        return 0
    # By default: computer = MAX, so computer wins when USER cannot move.
    base = +1 if (len(state) % 2 == 1) else -1
    return base if COMPUTER_PLAYS_MAX else -base


def successors_of(state: Piles) -> list[Piles]:
    """
    For every pile that is splittable (size >= 3) enumerate every
    unequal-split of that pile and substitute it back into the list.

    `state[:i] + new_pair + state[i+1:]` is the canonical immutable update
    — we never mutate the input state.
    """
    # Tag each successor with the NEW pair so move-ordering can rank by
    # the spread of the freshly-created split, not the spread of the
    # whole post-split state (which is dominated by unchanged piles).
    tagged: list[tuple[Piles, Piles]] = []
    for i, pile in enumerate(state):
        if pile <= 2:
            # piles of 1 or 2 cannot be legally split → skip.
            continue
        for split in split_pile_options(pile):
            new_state = state[:i] + split + state[i + 1:]
            tagged.append((new_state, split))

    # Move ordering — alpha-beta's pruning ratio depends on it
    # (Lecture 6 §4 "Best move first" remark). We sort by the spread of
    # the new pair only: "balanced-first" puts splits like [3,4] before
    # [1,6]; "skewed-first" reverses that.
    if MOVE_ORDERING == "balanced-first":
        tagged.sort(key=lambda item: _imbalance_score(item[1]))
    elif MOVE_ORDERING == "skewed-first":
        tagged.sort(key=lambda item: _imbalance_score(item[1]), reverse=True)
    elif MOVE_ORDERING != "natural":
        raise ValueError(
            f"Unknown MOVE_ORDERING={MOVE_ORDERING!r}; "
            "allowed values: 'natural', 'balanced-first', 'skewed-first'."
        )
    # "natural" → keep insertion order.

    return [s for s, _ in tagged]


def split_pile_options(pile: int) -> list[Piles]:
    """
    Enumerate every (j, pile-j) split with 1 <= j < pile-j.

    The strict inequality `j < k` is what enforces "different sizes" and
    also prevents duplicate pairs like [1,6] vs [6,1].

    Example: split_pile_options(7) → [[1,6], [2,5], [3,4]].
    """
    options: list[Piles] = []
    # WHY j only goes up to pile//2 (exclusive): once j == pile - j we'd
    # have an equal split (forbidden), and any j > pile//2 just repeats a
    # split we've already produced with the smaller-half first.
    for j in range(1, pile):
        k = pile - j
        if j < k:
            options.append([j, k])
    return options


# ----------------------------------------------------------------------------
# helpers used by MOVE_ORDERING
# ----------------------------------------------------------------------------

def _imbalance_score(pair: Piles) -> int:
    """
    Heuristic for ordering successors. `pair` is the freshly-created
    two-element split (NOT the whole post-split state). Lower score =
    more balanced. Used only for move ordering, never for evaluation.
    """
    return max(pair) - min(pair)


def argmax(iterable: Iterable, func: Callable[[Piles], int]):
    """Return the element of `iterable` that maximises `func(element)`."""
    return max(iterable, key=func)


# ============================================================================
# Game shell — Nim REPL (this file's __main__ entry)
# ============================================================================

def computer_select_pile(state: Piles) -> Piles:
    return alpha_beta_decision(state)


def user_select_pile(list_of_piles: Piles) -> Piles:
    """
    Interactive prompt for the human player. Untouched from the handout —
    only the surrounding game loop changes.
    """
    print("\n    Current piles: {}".format(list_of_piles))

    i = -1
    while i < 0 or i >= len(list_of_piles) or list_of_piles[i] < 3:
        print("What is the number of the pile you want to split?")
        print("The pile must have more than 2 stones")
        print(f"Choose a number between 1 and {len(list_of_piles)}")
        i = -1 + int(input())

    print("Selected pile {}".format(list_of_piles[i]))

    max_split = list_of_piles[i] - 1

    j = 0
    while j < 1 or j > max_split or j == list_of_piles[i] - j:
        print_str = f"Where should the first split be (from 1 to {max_split}"
        if list_of_piles[i] % 2 == 0:
            print_str += f", but not {list_of_piles[i] // 2}"

        print_str += ")?"
        print(print_str)

        j = int(input())

    k = list_of_piles[i] - j

    new_list_of_piles = list_of_piles[:i] + [j, k] + list_of_piles[i + 1:]

    print("    New piles: {}".format(new_list_of_piles))

    return new_list_of_piles


def main():
    """Run one interactive Nim game starting from a single pile of
    START_PILE tokens.

    Whoever plays MIN moves first (slide-10 convention "MIN should start
    the game"). By default COMPUTER_PLAYS_MAX is True, so the USER (MIN)
    opens. When COMPUTER_PLAYS_MAX is False the COMPUTER plays MIN and
    therefore moves first (slide-12 step 3).
    """
    state = [START_PILE]
    print(f"[alpha-beta] START_PILE={START_PILE}, "
          f"COMPUTER_PLAYS_MAX={COMPUTER_PLAYS_MAX}, "
          f"pruning={USE_ALPHA_BETA_PRUNING}, ordering={MOVE_ORDERING}")

    def _do_computer_move(s: Piles) -> Piles:
        reset_node_counter()
        s2 = computer_select_pile(s)
        if COUNT_NODES:
            print(f"[alpha-beta] evaluated {nodes_evaluated} states "
                  f"(pruning={USE_ALPHA_BETA_PRUNING}, "
                  f"ordering={MOVE_ORDERING})")
        print(f"The computer split a pile → {s2}")
        return s2

    # MIN always moves first. With COMPUTER_PLAYS_MAX=False the computer
    # is MIN, so it opens.
    computer_opens = not COMPUTER_PLAYS_MAX

    while not is_terminal(state):
        if computer_opens:
            state = _do_computer_move(state)
            computer_opens = False  # alternation continues USER→...
            if is_terminal(state):
                break
            state = user_select_pile(state)
        else:
            state = user_select_pile(state)
            if not is_terminal(state):
                state = _do_computer_move(state)

    print("    Final state is {}".format(state))


if __name__ == '__main__':
    main()

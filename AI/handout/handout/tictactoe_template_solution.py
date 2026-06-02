"""
LAB 5: Alpha-Beta Pruning with Tic-Tac-Toe
==========================================

PROBLEM STATEMENT (from Lab 5.pdf, slides 4-8):
-----------------------------------------------
Implement the minimax / alpha-beta search engine for Tic-Tac-Toe.

Slides 4-6 fix the representation:
  * The board is a list of 9 cells indexed 0-8, layout
        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8
  * The initial empty state is `[UNPLACED]*9`.
  * After X plays the centre the state is
        [UNPLACED, UNPLACED, UNPLACED, UNPLACED, X, UNPLACED, ...].
  * `utility_of(state)` returns +1 if X (MAX) has three in a row,
    -1 if O (MIN) does, and 0 for non-winning states (draws included).
  * `successors_of(state)` returns a list of pairs `(move, new_state)`
    where `move` is the cell index just filled.
  * `is_terminal(state)` returns True when someone has won or the board
    is full (draw).

Slide 8 lists the student TODOs. The handout template
`tictactoe_template.py` ships five `raise NotImplementedError` stubs that
must all be filled in:
  1. `is_terminal(state)`         (slide-8 TODO #1)
  2. `utility_of(state)`          (slide-8 TODO #2)
  3. `winner_of(state)`           (helper used by is_terminal/utility_of)
  4. `is_full_board(state)`       (helper used by is_terminal)
  5. `successors_of(state)`       (slide-8 TODO #3)
And then run the resulting game. The human plays O; the computer plays X
and goes first.

Slide 7 lists study questions (branching factor, depth, DFS vs BFS) that
inform the test plan but are not implemented here.

MENTAL MODEL (one-line analogy):
--------------------------------
Alpha-beta pruning is like reading a chess opening book: the moment you
realise the current line is worse than something you have already
considered, you stop reading it — you only need to know that this line is
worse than another, not exactly HOW bad it is.

(Consistent with the analogy used in Lecture 6 study/lectures/L06-Adversarial-Search.md §2
"Alpha-beta pruning ↔ you stop reading a bad chess line the moment you
realise it's worse than one you've already considered".)

REFERENCES:
-----------
- Lecture 6 (Adversarial Search) — study/lectures/L06-Adversarial-Search.md
  * §3 Game tree, §3 Minimax, §3 Alpha-beta pruning,
    §3 Alpha cutoff, §3 Beta cutoff, §4 Move ordering.
  * Slides 4-8 fix the Tic-Tac-Toe representation and the three TODO
    functions students must write.
- Slide 11 (Nim diagram) for the labelling convention MAX = +1, MIN = -1.
- Sister module: `alpha_beta_solution.py` — same alpha-beta engine on
  Nim, with the COUNT_NODES instrumentation we reuse here.
- Glossary terms (study/_shared/glossary.md):
  "Minimax", "Alpha-beta pruning", "Alpha cutoff", "Beta cutoff",
  "Utility function", "Successor function", "Terminal test",
  "Branching factor", "Evaluation function".

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
1. To change the search depth (variant: "increase minimax tree-depth from
   3 to 7, count nodes evaluated"):
     set MAX_DEPTH = 7. The default None means "search to terminal
     states" (which is feasible for Tic-Tac-Toe). With a finite MAX_DEPTH
     the engine consults EVALUATOR at the cutoff frontier instead of
     `utility_of`. Combine with COUNT_NODES = True to compare nodes
     evaluated with and without alpha-beta pruning.

2. To swap the evaluation heuristic (variant: "replace evaluator with one
   that weights centre-square control 3x"):
     set EVALUATOR = "center-weighted"  (or "lines",  "rows-cols-diags").
     Only relevant when MAX_DEPTH cuts off before terminal — at terminal
     leaves `utility_of` always wins.

3. To toggle alpha-beta pruning (variant: "report nodes evaluated with
   pruning on vs off"):
     set USE_ALPHA_BETA_PRUNING = False. The chosen move stays the same
     (alpha-beta is a speed optimisation, not a strategy change); only
     `nodes_evaluated` grows.

4. To reorder move generation (variant: "try centre first vs corners
   first; compare pruning effectiveness"):
     set MOVE_ORDERING ∈ {"natural", "center-first", "corners-first",
     "random"}.

5. To play interactively (slide-8 default "human vs computer"):
     set DEMO_MODE = "interactive". By default DEMO_MODE = "self-play"
     so that running `py -3.12 tictactoe_template_solution.py` is
     deterministic, prints the entire game, and finishes without keyboard
     input — the form the Verifier and the exam-agent gate require.

6. To start from a non-empty board (variant: "show alpha-beta from this
   mid-game position"):
     set STARTING_BOARD = <any list of 9 Symbols>. Defaults to all
     UNPLACED. The opponent will be inferred from how many X / O are
     already placed.

OUTPUTS WHEN RUN:
-----------------
With the defaults this script self-plays one full Tic-Tac-Toe game:

    py -3.12 tictactoe_template_solution.py

prints the board after every move, then the final board, who won (or
"draw"), and a summary of how many minimax nodes were evaluated. The
self-play result against a minimax opponent is always a draw (Tic-Tac-Toe
is a solved game), which exercises every code path:
  * `is_terminal` triggers on a board full of X and O (no winner).
  * `winner_of` returns None at the end.
  * `utility_of` is consulted at every leaf.
  * Alpha-beta pruning fires repeatedly on suboptimal branches.

ENTRY POINT: yes — this is the canonical Lab 5 entry point. The Verifier
runs `py -3.12 tictactoe_template_solution.py` from this directory and
checks that the exit code is 0 with no exception on stderr. The sibling
file `alpha_beta_solution.py` is also runnable but is treated as a
module: it serves the same alpha-beta engine for a Nim game and is
exercised separately.
"""

from enum import Enum
from typing import Self

# NOTE on the sister Nim module (`alpha_beta_solution.py`):
# ---------------------------------------------------------
# Both files contain a STANDALONE copy of the alpha-beta engine and a
# matching KNOB block. They do NOT share state — setting
# `USE_ALPHA_BETA_PRUNING = False` in `alpha_beta_solution.py` will NOT
# change the Tic-Tac-Toe behaviour, and vice versa. If you want to alter
# Tic-Tac-Toe pruning, edit THIS file. If you want to alter Nim pruning,
# edit `alpha_beta_solution.py`. The two are kept separate on purpose
# so that the Nim REPL and the TTT self-play can be driven independently.


# ============================================================================
# KNOBs — Tic-Tac-Toe-specific exam parameters
# ============================================================================

# KNOB: MAX_DEPTH (default=None, allowed=None or any int >= 1)
#   What it does: depth limit for the minimax recursion. None means
#           "search until terminal" (feasible for Tic-Tac-Toe because the
#           tree has at most 9! / something leaves and most branches are
#           shorter).
#   Effect: with a finite depth the recursion uses EVALUATOR at the
#           cut-off frontier instead of `utility_of`. Smaller depth →
#           faster but weaker play; larger depth → optimal play.
#   Exam variants: 1 (very weak), 3 (default in many course examples),
#           7 (close to perfect), None (exact minimax).
MAX_DEPTH: int | None = None

# KNOB: EVALUATOR (default="lines", allowed={"lines",
#                                             "center-weighted",
#                                             "rows-cols-diags"})
#   What it does: choose the heuristic that approximates utility at the
#           depth-cut frontier. NO effect unless MAX_DEPTH is finite — at
#           terminal leaves `utility_of` is always exact.
#   Effect:
#     - "lines"            L06 §3.4 / slide 30 heuristic:
#                          (X's open lines) - (O's open lines), where an
#                          "open line for X" has no O on it. Each
#                          qualifying line contributes +/-1.
#     - "center-weighted"  same open-line count as "lines", PLUS a
#                          (center_weight - 1) bonus for owning the
#                          centre square — used in variants.md variant 2.
#     - "rows-cols-diags"  alternative phrasing of the same open-line
#                          formula, named after its variable triple
#                          (rows + cols + diagonals).
#   Exam variants: variant 2 ("centre-square 3x"). Unknown values raise
#           ValueError.
EVALUATOR = "lines"

# KNOB: USE_ALPHA_BETA_PRUNING (default=True, allowed={True, False})
#   What it does: enable/disable alpha cutoffs and beta cutoffs.
#   Effect: same move, fewer states explored. Pair with COUNT_NODES to
#           reproduce the slide's "nodes evaluated with and without
#           pruning" measurement.
#   Exam variants: True/False sweep.
USE_ALPHA_BETA_PRUNING = True

# KNOB: COUNT_NODES (default=True, allowed={True, False})
#   What it does: instrument the recursion to count visited states.
#   Effect: prints "[alpha-beta] evaluated N states" after each computer
#           move. Used by every variant that compares search effort.
#   Exam variants: True for measurement transcripts; False otherwise.
COUNT_NODES = True

# KNOB: MOVE_ORDERING (default="center-first", allowed={"natural",
#                                                       "center-first",
#                                                       "corners-first",
#                                                       "random"})
#   What it does: order the children produced by `successors_of` BEFORE
#           the minmax recursion inspects them.
#   Effect: alpha-beta's pruning quality depends on how good the first
#           child is. "center-first" tries cell 4 (the centre) before the
#           rest, then the corners, then the edges — a textbook ordering
#           for Tic-Tac-Toe. "corners-first" reverses that. "natural"
#           keeps cell-index order (0,1,2,...) — note that cell 0 is a
#           corner, so "natural" is empirically WORSE than corners-first
#           for ply-1 pruning despite the name suggesting neutrality.
#           "random" shuffles deterministically using RANDOM_SEED so
#           transcripts stay reproducible across runs. Unknown values
#           raise ValueError.
#   Exam variants: variant 3 ("compare pruning effectiveness with
#           different move orderings").
MOVE_ORDERING = "center-first"

# KNOB: RANDOM_SEED (default=42, allowed=any int)
#   What it does: seed for the shuffled "random" move ordering.
#   Effect: reproducible transcripts; change to vary the shuffled order.
#           Only consulted when MOVE_ORDERING == "random".
RANDOM_SEED = 42

# KNOB: DEMO_MODE (default="self-play", allowed={"self-play",
#                                                 "interactive"})
#   What it does: select what `main()` does when this file is run.
#   Effect:
#     - "self-play"   computer plays both X and O against itself; output
#                     is deterministic, no input() calls (Verifier-safe).
#     - "interactive" original slide-8 behaviour: computer plays X,
#                     human plays O via stdin.
#   Exam variants: keep "self-play" for any automated examiner run;
#           switch to "interactive" only when you want to play.
DEMO_MODE = "self-play"

# KNOB: STARTING_BOARD (default=None, allowed=None or list[Symbols])
#   What it does: explicit initial board. None means an empty board (all
#           UNPLACED). Use this to inspect end-game positions from the
#           slides or set up "show alpha-beta on this position" variants.
#   Effect: if not None, must contain exactly 9 cells; X must be played
#           between 0 and 1 more times than O (X is MAX and moves first).
#   Exam variants: provide a board with one X already placed to ask "what
#           does O do next?".
STARTING_BOARD: "list[Symbols] | None" = None


# ============================================================================
# Symbols & type aliases — UNCHANGED from the handout template
# ============================================================================

class Symbols(Enum):
    X = "X"
    O = "O"
    UNPLACED = "i"

    def __str__(self):
        return self.value

    @classmethod
    def placed(cls) -> tuple[Self, Self]:
        return cls.X, cls.O


type Board = list[Symbols]


# Module-level counter for THIS lab's recursion. The Nim module
# (`alpha_beta_solution.py`) has its own independent counter — they never
# touch one another, so a Nim game and a Tic-Tac-Toe game can run in the
# same Python process without smearing counts.
nodes_evaluated: int = 0

_INFINITY: float = float('inf')


def _reset_local_counter() -> None:
    global nodes_evaluated
    nodes_evaluated = 0


# ============================================================================
# minmax_decision — derived from the handout template, instrumented with
# alpha-beta pruning, depth-limit + evaluator, and node counting.
# ============================================================================

def minmax_decision(state: Board) -> int:
    """
    Returns the index 0..8 of the next move for whichever side is to play.

    Implementation: alpha-beta on top of the minimax framework from
    Lecture 6 §3. Depth limit and evaluator are KNOB-driven so the same
    function services every exam variant.

    The function signature (state -> int) is preserved exactly from the
    handout template `tictactoe_template.py:minmax_decision`.
    """

    def max_value(state_option: Board, alpha: float, beta: float, depth: int) -> float:
        global nodes_evaluated
        if COUNT_NODES:
            nodes_evaluated += 1

        if is_terminal(state_option):
            return utility_of(state_option)
        if MAX_DEPTH is not None and depth >= MAX_DEPTH:
            # Cut-off frontier: fall back to the heuristic evaluator. At a
            # true terminal `utility_of` is exact; here we approximate.
            return _evaluate(state_option)

        expected_value: float = -_INFINITY
        for (_, s) in successors_of(state_option):
            expected_value = max(expected_value, min_value(s, alpha, beta, depth + 1))
            if USE_ALPHA_BETA_PRUNING and expected_value >= beta:
                return expected_value  # β-cutoff
            alpha = max(alpha, expected_value)
        return expected_value

    def min_value(state_option: Board, alpha: float, beta: float, depth: int) -> float:
        global nodes_evaluated
        if COUNT_NODES:
            nodes_evaluated += 1

        if is_terminal(state_option):
            return utility_of(state_option)
        if MAX_DEPTH is not None and depth >= MAX_DEPTH:
            return _evaluate(state_option)

        v: float = _INFINITY
        for (_, s) in successors_of(state_option):
            v = min(v, max_value(s, alpha, beta, depth + 1))
            if USE_ALPHA_BETA_PRUNING and v <= alpha:
                return v  # α-cutoff
            beta = min(beta, v)
        return v

    # Side to move: X is MAX (goes first); whoever has fewer marks is to
    # play next. With equal counts it's X's turn (slide 4 says X plays
    # first from the empty board).
    children = successors_of(state)
    if _to_move(state) is Symbols.X:
        action, _ = max(children, key=lambda a: min_value(a[1], -_INFINITY, _INFINITY, 1))
    else:
        action, _ = min(children, key=lambda a: max_value(a[1], -_INFINITY, _INFINITY, 1))
    return action


# ============================================================================
# is_terminal / utility_of / winner_of / is_full_board / successors_of —
# the five slide-8 TODOs (three named on slide 8 + two helpers that the
# handout template `tictactoe_template.py` also ships as
# `raise NotImplementedError` stubs).
# ============================================================================

def is_terminal(state: Board) -> bool:
    """
    A game state is terminal when someone has three in a row OR the board
    is completely filled (no UNPLACED cells left).
    """
    # WHY two checks: a win can occur on a non-full board (premature
    # three-in-a-row), and a full board with no winner is a draw — both
    # are terminal.
    return winner_of(state) is not None or is_full_board(state)


def utility_of(state: Board) -> int:
    """
    Slide-6 convention:
      +1 if X (MAX) has three in a row
      -1 if O (MIN) has three in a row
       0 otherwise (including draws and non-terminal states)
    """
    winner = winner_of(state)
    if winner == Symbols.X:
        return +1
    elif winner == Symbols.O:
        return -1
    else:
        # Both "draw" and "non-terminal" map to 0 — this matches the
        # slide-6 wording "or 0 otherwise". Under the default
        # MAX_DEPTH = None, the recursion guards every `utility_of` call
        # behind `is_terminal`, so in practice this branch is hit only at
        # draws. With a finite MAX_DEPTH the depth-cut frontier calls
        # `_evaluate` instead and `utility_of` is still only seen at
        # genuine terminals.
        return 0


# ---------- HELPER: check for a winner ----------

# Pre-computed once for efficiency (and so the KNOB-aware code below stays
# tidy). The 8 winning lines from the slides.
_WINNING_LINES: tuple[tuple[int, int, int], ...] = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),             # diagonals
)


def winner_of(state: Board):
    """
    Return Symbols.X or Symbols.O if either has all three cells of one
    of the 8 winning lines; return None otherwise.
    """
    # WHY iterate _WINNING_LINES once: each line check is O(1), total O(8).
    # This is also why we don't bother caching per-call results.
    for (a, b, c) in _WINNING_LINES:
        if state[a] != Symbols.UNPLACED and state[a] == state[b] == state[c]:
            return state[a]
    return None


# ---------- HELPER: check if board is full ----------

def is_full_board(state: Board) -> bool:
    """True iff no UNPLACED cell remains anywhere on the board."""
    return all(cell != Symbols.UNPLACED for cell in state)


# ============================================================================
# successors_of — the third slide-8 TODO
# ============================================================================

def successors_of(state: Board) -> list[tuple[int, Board]]:
    """
    Return every legal next state, paired with the cell index that produced
    it. Whose turn it is is inferred from how many cells are occupied:
    X (MAX) goes first, so when the count of placed cells is even it's
    X's turn (slide 4 figure).
    """
    open_count = sum(1 for cell in state if cell == Symbols.UNPLACED)
    # X starts (slide 4). After every X-move open_count drops by one
    # (becomes even). So odd open_count → next move belongs to X.
    player = Symbols.X if (open_count % 2 == 1) else Symbols.O

    successors: list[tuple[int, Board]] = []
    for move in range(9):
        if state[move] == Symbols.UNPLACED:
            successor = state[:]          # copy — never mutate `state`
            successor[move] = player
            successors.append((move, successor))

    return _apply_move_ordering(successors)


# ============================================================================
# Helpers used by KNOBs: move ordering, evaluator, side-to-move
# ============================================================================

_CENTER = 4
_CORNERS = (0, 2, 6, 8)
_EDGES = (1, 3, 5, 7)


def _apply_move_ordering(successors: list[tuple[int, Board]]) -> list[tuple[int, Board]]:
    if MOVE_ORDERING == "natural":
        return successors

    if MOVE_ORDERING == "center-first":
        # rank: centre (0) < corner (1) < edge (2)
        def rank(item):
            m = item[0]
            if m == _CENTER:
                return 0
            if m in _CORNERS:
                return 1
            return 2
        return sorted(successors, key=rank)

    if MOVE_ORDERING == "corners-first":
        def rank(item):
            m = item[0]
            if m in _CORNERS:
                return 0
            if m == _CENTER:
                return 1
            return 2
        return sorted(successors, key=rank)

    if MOVE_ORDERING == "random":
        import random
        rnd = random.Random(RANDOM_SEED)
        shuffled = list(successors)
        rnd.shuffle(shuffled)
        return shuffled

    raise ValueError(
        f"Unknown MOVE_ORDERING={MOVE_ORDERING!r}; "
        "allowed values: 'natural', 'center-first', 'corners-first', 'random'."
    )


def _to_move(state: Board) -> Symbols:
    """Whose turn it is, by the parity rule of `successors_of`."""
    open_count = sum(1 for cell in state if cell == Symbols.UNPLACED)
    return Symbols.X if (open_count % 2 == 1) else Symbols.O


def _evaluate(state: Board) -> int:
    """
    Heuristic for cut-off frontiers (only consulted when MAX_DEPTH limits
    the search before a terminal is reached). The three evaluators are
    all consistent in direction on most reachable states (positive when
    X is ahead, negative when O is ahead, zero in balanced positions);
    they differ in how strongly they reward centre control.
    """
    if EVALUATOR == "lines":
        return _score_lines(state, center_weight=1)
    if EVALUATOR == "center-weighted":
        return _score_lines(state, center_weight=3)
    if EVALUATOR == "rows-cols-diags":
        return _score_open_lines(state)
    raise ValueError(
        f"Unknown EVALUATOR={EVALUATOR!r}; "
        "allowed values: 'lines', 'center-weighted', 'rows-cols-diags'."
    )


def _score_lines(state: Board, *, center_weight: int) -> int:
    """
    L06 §3.4 / slide 30 heuristic:
        Eval(s) = (X's open lines) - (O's open lines)
    where an "open line for X" is a row/column/diagonal that has NO O on
    it (X might still complete it), and an "open line for O" is symmetric
    (no X on it). Each such line contributes exactly +1 (for X) or -1
    (for O). A completely empty line is open for BOTH and the two terms
    cancel; a line with one X is open for X but not for O.

    With `center_weight > 1`, owning the centre square scales the score
    accordingly — used by variants.md variant 2. The centre bonus is
    applied ON TOP of the open-line count and is what differentiates
    "center-weighted" from "lines".
    """
    score = 0
    for (a, b, c) in _WINNING_LINES:
        cells = (state[a], state[b], state[c])
        has_x = any(s == Symbols.X for s in cells)
        has_o = any(s == Symbols.O for s in cells)
        # Open-for-X: no O on the line (regardless of whether X is on it).
        if not has_o:
            score += 1
        # Open-for-O: no X on the line.
        if not has_x:
            score -= 1
    # Centre-square bonus. Does not affect terminal utility (terminal
    # states still come from `utility_of`).
    if state[_CENTER] == Symbols.X:
        score += (center_weight - 1)
    elif state[_CENTER] == Symbols.O:
        score -= (center_weight - 1)
    return score


def _score_open_lines(state: Board) -> int:
    """Alternative phrasing of the same open-line idea, named after the
    "rows-cols-diags" KNOB value. Counts winnable lines for each side.

    This is intentionally the same arithmetic as `_score_lines` with
    `center_weight=1` — kept as a separate function so the KNOB can pick
    a different evaluator name without touching `_score_lines`.
    """
    x_winnable = 0
    o_winnable = 0
    for (a, b, c) in _WINNING_LINES:
        cells = (state[a], state[b], state[c])
        if Symbols.O not in cells:
            x_winnable += 1
        if Symbols.X not in cells:
            o_winnable += 1
    return x_winnable - o_winnable


# ============================================================================
# Display
# ============================================================================

def display(state: list[Symbols]) -> None:
    print("-----")
    for i in range(0, 3):
        for c in range(i * 3, i * 3 + 3):
            print("|", end="")
            symbol = c if state[c] == Symbols.UNPLACED else state[c]
            print(symbol, end="")
        print("|")


# ============================================================================
# Game loops — driven by DEMO_MODE
# ============================================================================

def _starting_board() -> Board:
    """Build the initial board honouring STARTING_BOARD if set.

    Validates the KNOB-block contract: exactly 9 cells, every cell is a
    `Symbols` member, and X is played between 0 and 1 more times than O
    (X moves first, so legal positions have x_count == o_count or
    x_count == o_count + 1).
    """
    if STARTING_BOARD is None:
        return [Symbols.UNPLACED] * 9

    if len(STARTING_BOARD) != 9:
        raise ValueError(
            f"STARTING_BOARD must contain exactly 9 cells, "
            f"got {len(STARTING_BOARD)}."
        )
    bad = [c for c in STARTING_BOARD if not isinstance(c, Symbols)]
    if bad:
        raise ValueError(
            f"STARTING_BOARD cells must be `Symbols` members; "
            f"got non-Symbols entries: {bad!r}."
        )
    x_count = sum(1 for c in STARTING_BOARD if c == Symbols.X)
    o_count = sum(1 for c in STARTING_BOARD if c == Symbols.O)
    if not (x_count == o_count or x_count == o_count + 1):
        raise ValueError(
            f"STARTING_BOARD violates the X/O count rule "
            f"(x_count={x_count}, o_count={o_count}): X is MAX and "
            "moves first, so the legal range is x_count == o_count "
            "(O to move) or x_count == o_count + 1 (X to move)."
        )
    return list(STARTING_BOARD)


def _self_play() -> None:
    """
    Two perfect minimax agents play each other from STARTING_BOARD.

    Output:
      * the board after every move, indexed by move number;
      * a one-line "[alpha-beta] evaluated N states" trace per ply;
      * a final result line ("Game is over. ..." matching slide-8).

    Self-play between two minimax agents on Tic-Tac-Toe is guaranteed to
    end in a draw (the game is solved). The Verifier relies on this — it
    only checks for exit-code 0 and no exception.
    """
    board = _starting_board()
    ply = 0
    print("=== Lab 5 — Alpha-Beta Tic-Tac-Toe (self-play demo) ===")
    print(f"KNOBS: MAX_DEPTH={MAX_DEPTH}, EVALUATOR={EVALUATOR!r}, "
          f"USE_ALPHA_BETA_PRUNING={USE_ALPHA_BETA_PRUNING}, "
          f"MOVE_ORDERING={MOVE_ORDERING!r}")
    print()
    display(board)
    while not is_terminal(board):
        ply += 1
        side = _to_move(board)
        _reset_local_counter()
        move = minmax_decision(board)
        board[move] = side
        print(f"\nply {ply}: {side} plays cell {move}", end="")
        if COUNT_NODES:
            print(f"   [alpha-beta] evaluated {nodes_evaluated} states", end="")
        print()
        display(board)

    print()
    result = winner_of(board)
    if result is None:
        print("Game is over. No winner")
    else:
        print("Game is over. The winner is:", result)


def _interactive() -> None:
    """
    Original slide-8 game loop. The computer plays X (and goes first);
    the human plays O via stdin. KEPT FOR PEDAGOGY — not used by the
    Verifier or the exam agents.
    """
    board = _starting_board()
    while not is_terminal(board):
        _reset_local_counter()
        board[minmax_decision(board)] = Symbols.X
        if COUNT_NODES:
            print(f"[alpha-beta] evaluated {nodes_evaluated} states")
        if not is_terminal(board):
            display(board)
            board[int(input('Your move? '))] = Symbols.O
    display(board)

    result = winner_of(board)
    if result is None:
        print("Game is over. No winner")
    else:
        print("Game is over. The winner is:", result)


def main():
    if DEMO_MODE == "interactive":
        _interactive()
    else:
        _self_play()


if __name__ == '__main__':
    main()

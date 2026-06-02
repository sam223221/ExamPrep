# Lab 5 — Alpha-Beta Pruning — Exam Variant Bank

Source: Plan Appendix B (`docs/superpowers/plans/2026-05-22-ai-exam-prep-study-package-design.md`)
and Spec §8.3.

Each variant below is a self-contained exam question. A fresh exam agent
should be able to solve it using ONLY the solution's docstring header,
KNOB blocks, and function signatures — without reading any function body
or any lecture material.

Entry point for every variant:
`handout/handout/tictactoe_template_solution.py`
(imports the alpha-beta engine from `handout/handout/alpha_beta_solution.py`).

---

## Variant 1 — Tree-depth limit comparison (with and without pruning)

> **Question.** Set the minimax tree-depth limit to 3, then to 7. For
> each depth, report the number of states evaluated for the COMPUTER's
> first move from the empty board, both with alpha-beta pruning enabled
> and disabled. Confirm that the chosen move is identical in both cases
> (alpha-beta is a speed optimisation, not a strategy change).

How to solve via KNOBs only:

1. Open `tictactoe_template_solution.py`. **Edit KNOBs in THIS file —
   the sister Nim file `alpha_beta_solution.py` has its own independent
   copy and changing the Nim KNOBs will not affect the TTT measurement.**
2. Pin `MOVE_ORDERING = "natural"` for the measurement (the default
   `"center-first"` would conflate this variant with variant 3).
3. Set `MAX_DEPTH = 3`, run, record `nodes_evaluated` for ply 1 (X's
   opening move) with `USE_ALPHA_BETA_PRUNING = True`, then with `False`.
4. Set `MAX_DEPTH = 7`, repeat.
5. Tabulate: rows = (depth, pruning), columns = (move, nodes).
6. Required tabulation:

   | MAX_DEPTH | Pruning | Move | Nodes |
   |---|---|---|---|
   | 3 | on  | ? | ? |
   | 3 | off | ? | ? |
   | 7 | on  | ? | ? |
   | 7 | off | ? | ? |

Expected qualitative observation: nodes-with-pruning < nodes-without; the
ratio grows with depth (approaches the theoretical best-case
$b^{d/2}/b^d = b^{-d/2}$). The chosen move column is identical along each
row pair. Expect roughly 2–3× pruning ratio at depth 3 and 20–30× at
depth 7 (a sanity check, not an exact expectation).

Relevant KNOBs: `MAX_DEPTH`, `USE_ALPHA_BETA_PRUNING`, `COUNT_NODES`,
`MOVE_ORDERING`.

---

## Variant 2 — Centre-weighted evaluator

> **Question.** Replace the evaluator with one that weights centre-square
> control 3x. Play a self-game and report the winner (or "draw") along
> with the final board.

How to solve via KNOBs only:

1. In `tictactoe_template_solution.py` set
   `EVALUATOR = "center-weighted"`.
2. Set `MAX_DEPTH = 3`. The evaluator is only consulted at the depth-cut
   frontier, so MAX_DEPTH must be finite for the KNOB to have any
   observable effect. At `MAX_DEPTH = 2` the two evaluators are
   empirically indistinguishable (both pick the same moves);
   `MAX_DEPTH = 3` is the smallest depth at which the centre bonus
   changes the chosen line.
3. Run `py -3.12 tictactoe_template_solution.py`.
4. Compare the final board, the per-ply moves, and the winner against
   the run with `EVALUATOR = "lines"` and `MAX_DEPTH = 3`.

Required deliverables:
- Final board for `EVALUATOR = "lines"` at `MAX_DEPTH = 3`.
- Final board for `EVALUATOR = "center-weighted"` at `MAX_DEPTH = 3`.
- Statement of which side wins / whether it is a draw, in each case.
- Optional: one-sentence explanation of why centre-weighting matters in
  Tic-Tac-Toe (the centre participates in 4 of the 8 winning lines —
  more than any corner (3) or edge (2)).

Relevant KNOBs: `EVALUATOR`, `MAX_DEPTH`.

---

## Variant 3 — Move-ordering ablation

> **Question.** Reorder move generation to try the centre first vs the
> corners first, vs natural order. For each ordering, report the number
> of nodes alpha-beta evaluates on the COMPUTER's first move from the
> empty board (full-depth search). Comment on which ordering yields the
> tightest pruning and why.

How to solve via KNOBs only:

1. Keep `MAX_DEPTH = None`, `USE_ALPHA_BETA_PRUNING = True`,
   `COUNT_NODES = True`.
2. Sweep `MOVE_ORDERING` ∈ {"natural", "center-first", "corners-first"}.
3. For each setting, run the script. Note the very first
   "[alpha-beta] evaluated N states" line (ply 1).
4. Required tabulation:

   | MOVE_ORDERING | Nodes evaluated on ply 1 | First move |
   |---|---|---|
   | natural        | ? | ? |
   | center-first   | ? | ? |
   | corners-first  | ? | ? |

Expected qualitative observation: the centre is the strongest opening,
so inspecting it first lets alpha-beta establish tight bounds quickly
and prune the rest aggressively. Empirically `center-first` evaluates
~15 700 states, `corners-first` ~20 700, and `natural` ~30 700 — so
`natural` is the WORST of the three (despite the name suggesting
neutrality). Intuition: `natural` walks cell indices 0,1,2,..., which
puts a corner first (cell 0), then an edge (cell 1), then another
corner (cell 2), etc. The centre (cell 4) is only inspected fifth, so
alpha-beta has to refine its bounds through four weaker children before
it sees the strongest move.

Relevant KNOBs: `MOVE_ORDERING`, `USE_ALPHA_BETA_PRUNING`, `COUNT_NODES`.

---

## Variant 4 (extension — Nim, slide 12 homework)

Optional bonus variant pulled directly from the handout's slide-12
"Homework Nim" exercise. Useful evidence that the same alpha-beta engine
generalises across games.

> **Question.** Using the Nim entry point (`alpha_beta_solution.py`),
> play games starting with 15 and 20 tokens. For each starting pile,
> report whether the COMPUTER (MAX) is guaranteed to win against a
> perfect human (MIN) opener. Then flip the roles
> (`COMPUTER_PLAYS_MAX = False`) and rerun, confirming the sign of the
> root utility flips accordingly.

How to solve via KNOBs only:

1. In `alpha_beta_solution.py` set `START_PILE = 15`. Inspect the root
   utility by importing `root_utility` from the module — no interactive
   play required:

   ```python
   from alpha_beta_solution import root_utility
   root_utility([15], to_move="MIN")  # MIN opens (slide-10 convention)
   ```

   Sign convention: `+1` means COMPUTER (= MAX by default) wins; `-1`
   means USER wins.
2. Repeat with `START_PILE = 20` (i.e. call `root_utility([20])`).
3. Flip `COMPUTER_PLAYS_MAX = False`; rerun the same two cases — the
   sign of `root_utility` should flip because `utility_of` flips sign
   when the COMPUTER switches sides (slide-12 step 3).
4. (Optional) drive the interactive REPL via
   `py -3.12 alpha_beta_solution.py` to watch a full game; with
   COMPUTER_PLAYS_MAX=False the COMPUTER (now MIN) opens.

Relevant KNOBs: `START_PILE`, `COMPUTER_PLAYS_MAX`,
`USE_ALPHA_BETA_PRUNING`. Module-level helpers exposed for this variant:
`root_utility`, `max_value`, `min_value`.

---

## How exam agents are expected to behave

Per spec §8.2:
- They may read this `variants.md` and the solution-file docstrings.
- They may NOT read function bodies, the lab handout PDF, the lecture
  PDF, or the lecture markdown.
- They MUST declare their planned KNOB changes BEFORE running.
- They MUST report `VERDICT: SOLVED` or `VERDICT: STUCK` with reason.

Each examiner writes their attempt to
`study/_exam/Lab5-AlphaBeta/round{R}/examiner{N}-attempt.md` per the
format in plan Appendix A.7.

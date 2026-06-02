# Lab 2 - Search: Revise Summary (Round 1)

**Scope:** Apply all P0 findings from Reviewers #2, #3, #4 to
`Lab 2/Search_solution.py` and `study/_exam/Lab2-Search/variants.md`.
Reviewer #1 reported no P0 findings; its P1/P2 nits are addressed
opportunistically when they overlapped with the P0 work.

---

## Files changed

1. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 2\Search_solution.py`
   - Full rewrite of the KNOBs block, `Searcher` class, and the three demo
     drivers. All three default-demo outputs are preserved verbatim
     (verified by running `py -3.12 "Lab 2/Search_solution.py"`).
2. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab2-Search\variants.md`
   - Rewritten with verified expected answers for variants 1-5 (the three
     P0s plus the P1 incoherent-prose issue), and added variants 6 and 7
     covering the previously uncovered `KNOB_TRACK_VISITED=False` and
     `KNOB_EX2_GOAL_STATE=None` surfaces (R4 P1 findings 5, 6).

---

## R2 P0 fixes (KNOB coverage)

| R2 P0 | Fix applied |
|---|---|
| **P0-1** Vacuum statuses hardcoded `("Dirty","Clean")` | New `KNOB_EX2_STATUSES: tuple[str,...] = ("Dirty","Clean")`. Threaded through `build_vacuum_state_space(rooms, statuses)`; Suck uses `statuses[-1]` as the "clean" sentinel; the built-in "all clean" goal predicate also reads `statuses[-1]`. |
| **P0-2** River state arity `4` hardcoded | `build_river_state_space` now takes `item_count: int = 4`; `run_exercise_3()` passes `item_count=len(KNOB_EX3_INITIAL_STATE)`. The `range(1, 4)` literal is now `range(1, item_count)`. Adding a fifth item (chicken, fox, ...) is a KNOB change. |
| **P0-3** `global KNOB_PRINT_FRINGE_TRACE` mutation | Removed both `global` mutations from `run_exercise_2()` and `run_exercise_3()`. Replaced with per-exercise KNOBs `KNOB_EX1_PRINT_FRINGE_TRACE`, `KNOB_EX2_PRINT_FRINGE_TRACE`, `KNOB_EX3_PRINT_FRINGE_TRACE` (default: Ex1 True, Ex2/Ex3 False). `Searcher.__init__` accepts a `print_fringe_trace` parameter; demo drivers pass the appropriate per-exercise KNOB. No more `global`, no more `try/finally` dance. |
| **P0-4** Secret `_track_visited = False` reaching into a private attribute | Removed. `KNOB_EX1_TRACK_VISITED`, `KNOB_EX2_TRACK_VISITED`, `KNOB_EX3_TRACK_VISITED` are now explicit KNOBs in the top-of-file block (default: Ex1 False because the A..J tree is acyclic; Ex2/Ex3 None = inherit global True). `Searcher.__init__` accepts a `track_visited` parameter. |
| **P0-5** Goal-predicate hardcoded as nested class `AllCleanSearcher` | Deleted `AllCleanSearcher`. New per-exercise KNOBs `KNOB_EX1_GOAL_PREDICATE`, `KNOB_EX2_GOAL_PREDICATE`, `KNOB_EX3_GOAL_PREDICATE` (callable[[state], bool] \| None). `Searcher.__init__` accepts a `goal_predicate` parameter; `Searcher._is_goal` consults it before falling back to equality. The "any all clean" semantics for `KNOB_EX2_GOAL_STATE = None` is now provided by the module-level helper `_vacuum_all_clean_goal(statuses)`. |
| **P0-6** No depth limit / IDS / UCS hooks | Added `KNOB_MAX_DEPTH`, `KNOB_USE_IDS`, `KNOB_IDS_MAX_DEPTH`, `KNOB_STEP_COST_FN`. `KNOB_DEFAULT_STRATEGY` now accepts `"IDS"` and `"UCS"` in addition to `"BFS"`/`"DFS"`/`None`. `Searcher` gained `iterative_deepening_search()` (depth-limited DFS in a loop, distinguishes cutoff from failure) and `uniform_cost_search()` (heap-based, goal-test on pop per L03 sec 4.2.1). Verified end-to-end with a smoke test on the A..J tree. |

Also addressed (R2 P1 cleanups that lived in the same code paths):

- `KNOB_EX2_STATE_SPACE_OVERRIDE` and `KNOB_EX3_STATE_SPACE_OVERRIDE` now
  tested with `is not None` (R2 P1-9), so `{}` is honoured.
- `KNOB_MAX_EXPANSIONS` added (R2 P1-1) - separate from
  `KNOB_MAX_FRINGE_NODES`, fires when the loop iteration count exceeds
  the cap, catching the "cycle-free infinite chain" case.
- `KNOB_EX3_STATE_SPACE_OVERRIDE` (R2 P1-8) added for symmetry with Ex2.
- `StateSpace.successor` now raises `ValueError` when state space is
  unset (R2 out-of-scope item; Reviewer #1's P1-1 also flagged this).

---

## R3 P0 fixes (pedagogical clarity)

| R3 P0 | Fix applied |
|---|---|
| **P0-1** Vacuum Left/Right semantics contradict L03 sec 5.1 | Rewrote `build_vacuum_state_space`. Left now steps one room toward index 0 with no wrap-around (self-loop at `rooms[0]`); Right steps one room toward `rooms[-1]` with no wrap-around. The docstring now quotes L03 sec 5.1 verbatim and includes a worked successor table for `('A','Dirty','Dirty')` matching the handout hint. The 2-room behaviour is exactly L03's; the 3-room behaviour generalises L03's anchoring naturally (no cyclic A->B->C->A wrap). |
| **P0-2** MENTAL MODEL omits graph-vs-tree distinction | Added a new paragraph in the docstring header: "Tree search vs graph search. This file actually runs graph search (L03 sec 3.4) - i.e. tree search plus an explored set - whenever `KNOB_TRACK_VISITED` is True; `run_exercise_1()` flips it off (via `KNOB_EX1_TRACK_VISITED`) to demonstrate the pure tree-search behaviour the slides describe on the acyclic A..J tree." |
| **P0-3** `Node.expand` comment hand-waves the double-reversal | Rewrote `Node.expand`'s docstring as a student-facing explanation: the per-child `insert(s, successors, insert_as_first=True)` builds the children list in reverse; the caller's `insert_all` then either pushes that list onto the stack (DFS: leftmost child ends up on top, L03 sec 5.5 left-first convention) or onto the FIFO back (BFS: child order is reversed vs the dict, a deliberate template quirk). Concrete consequence ("BFS expands C before B after expanding A") spelled out. |

Also addressed (R3 P1 / P2 fixes that fell out of the P0 work):

- L03 paraphrase quote (R3 P1-1) replaced with a real L03 sec 3.4 / sec 2.6
  paraphrase, no longer in scare-quotes that misrepresent the lecture.
- `path()` (R3 P1-3) now has a docstring that states the leaf-to-root
  ordering contract explicitly.
- `StateSpace.successor` (R3 P1-4) has a proper docstring naming the
  L03 sec 3.2 successor function.
- `Searcher.__init__`, `_is_goal`, `tree_search`, `run` (R3 P1-5) all
  have docstrings now; `_is_goal` documents that it is overridable via
  `goal_predicate`.
- L03 scope note (R3 P1-6) added at the top of the docstring: BFS+DFS
  exercised by default, IDS/UCS reachable via new KNOBs.
- `insert` (R3 P1-8) docstring corrected: "list concatenation returns a
  new list" instead of the wrong "slicing creates a shallow copy".
- "Once extracted" stale phrasing (R3 P2-8) removed - L03 is now
  referenced as canonical.

---

## R4 P0 fixes (variant correctness)

All four R4 P0 findings target `variants.md` expected-answer sections.
The fix is a full rewrite of the file with verified expected outputs.

| R4 P0 | Fix applied (verified by running the solution under the variant's KNOBs) |
|---|---|
| **P0-1** Variant 1: "7-step plan / depth 6" wrong | Corrected to 5-action plan / depth 5. Verified path: `('A','D','D','D') -> ('A','C','D','D') -> ('B','C','D','D') -> ('B','C','C','D') -> ('C','C','C','D') -> ('C','C','C','C')`. |
| **P0-2** Variant 2: DFS expansion order `A,B,D,E,C,F,G` then J wrong | Corrected to 10 expansions `A,B,D,E,C,F,G,H,I,J` (J pops last and the goal-test fires). BFS unchanged at 8 expansions. Max fringe sizes (3 for DFS, 6 for BFS) re-verified. |
| **P0-3** Variant 3: "standard 7-step solution" from `('W','E','W','W')` wrong | Corrected to 3-step solution from `('W','E','W','W')`. Path: `('W','E','W','W') -> ('E','E','W','E') -> ('W','E','W','E') -> ('E','E','E','E')`. Explanation added: wolf already east shrinks the optimal plan by 4 moves. |
| **P0-4** Variant 4: "Up-Right" plan and non-KNOB-adaptability | Corrected to "Right, Right" (blank moves rightward twice; there is no Up move). Charter-compliance is now honestly addressed: the variant supplies a *hand-built minimal slice* of the 8-puzzle state space via `KNOB_EX1_STATE_SPACE` (3-state dict covering the optimal plan only); the variant explicitly notes that a full 8-puzzle would need a new generator function in `Search_solution.py`. |

Also addressed (R4 P1 / P2 fixes):

- Variant 5 (R4 P1-1) rewritten with a clean 5-action trace, no more
  internal contradiction; "depth 5, two fewer than the classic 7-step
  solution" matches the verified output.
- Variant 2 (R4 P1-3) now has an explicit note about the child-ordering
  quirk in `Node.expand()` and its effect on sibling traversal.
- Variant 4 (R4 P1-4) internal table/prose contradiction resolved -
  `KNOB_DEFAULT_STRATEGY` is `"BFS"` everywhere now, no more "DFS with
  depth limit" claim.
- New **Variant 6** added (R4 P1-5) exercising
  `KNOB_EX3_TRACK_VISITED = False` to demonstrate L03 sec 6 pitfall 5
  (DFS in cyclic graphs without the explored-set check).
- New **Variant 7** added (R4 P1-6) exercising
  `KNOB_EX2_GOAL_STATE = None` to demonstrate the built-in "any
  all-clean" goal predicate.
- (R4 P1-7's `KNOB_EX3_PASSENGERS_PER_TRIP = 2` variant was considered
  but deferred - the resulting puzzle is trivially solvable in 3 moves
  and the pedagogical content overlaps Variant 5. Easy to add later if
  needed.)
- Variant-bank top-of-file note (R4 out-of-scope item) about the
  `Node.expand` child-ordering quirk is included as a global preamble
  rather than buried in each variant.

---

## Verification

All seven variants were verified by running `Search_solution.py` with the
variant's KNOB block applied (via a one-off `importlib.reload` driver,
not committed to the repo). Outputs match each variant's "Expected
answer" section exactly:

| Variant | Verified depth / outcome |
|---|---|
| 1 (3-room vacuum, BFS) | depth 5; path 6 states (matches doc) |
| 2 DFS (A..J -> J) | 10 expansions A,B,D,E,C,F,G,H,I,J; max fringe 3; path A,C,G,J |
| 2 BFS (A..J -> J) | 8 expansions A,C,B,G,F,E,D,J; max fringe 6; path A,C,G,J |
| 2 DFS (A..J -> D) | 3 expansions; path A,B,D |
| 2 BFS (A..J -> D) | 7 expansions; path A,B,D |
| 3 (river from ('E','E','W','W')) | UNSAFE -> raises KeyError; nearby safe ('W','E','W','W') solves in depth 3 |
| 4 (8-puzzle slice) | depth 2; blank moves Right, Right |
| 5 (river, wolf-eats-goat only) | depth 5 |
| 6 (river, DFS, no visited) | aborts at expansion cap, prints "no solution" |
| 7 (vacuum, goal=None) | depth 3; equality default and "any all clean" coincide on this start |

Default-demo behaviour (running the file with no KNOB overrides) is
**byte-identical** to the pre-revision output for all three exercises -
verified by `py -3.12 "Lab 2/Search_solution.py"`.

---

## Out-of-scope observations

1. **`Self` typing requires Python 3.11+.** Not changed - the lab's
   `py -3.12` command is fine, and adding a fallback typing path is a
   distraction.
2. **Action labels** (Suck/Left/Right) are still implicit in the state
   transitions, not annotated on edges. R2 P1-4. Not addressed in this
   round - it would require adding an `action` field on `Node` plus a
   new return shape from the builders, which is a bigger surgery than
   the round 1 scope. The new `KNOB_STEP_COST_FN` is the closest
   adjacent change.
3. **Frontier dedup** (R3 P1-2) - the searcher still does not
   pre-check the fringe before pushing duplicates. Documented in
   `tree_search`'s docstring rather than implemented, because changing
   it would alter the fringe trace the handout literally asks for
   ("give the fringe after expanding each node"). Acceptable trade.
4. **No unit tests** locking in expected outputs. Variant verification
   was done ad-hoc via `importlib.reload`. A `pytest`-style
   regression suite would be a nice round 2 addition.
5. **Decorative banner headers** (R3 P2-1) - kept as-is. Cosmetic.

---

## What PM should do next

Per the standard PM workflow, this rev should now go to:

1. **Reviewers #1-#4 (round 2)** to confirm the P0 findings are
   actually closed (especially R4, where the expected-answer
   correctness is the entire deliverable).
2. **App Tester** if the team wants an end-to-end smoke check
   (`py -3.12 "Lab 2/Search_solution.py"` already runs cleanly).
3. **Code Reviewer** for the PR-style diff once all reviewers approve.

P1 findings not yet addressed: R2 P1-4 (action labels on edges),
R2 P1-5/P1-6 (frontier dedup, successor ordering KNOBs - cost more
than benefit for the lab's scope), R3 P2-6 (`Node.__repr__` terse
mode). Worth scheduling for a round 2 if time permits.

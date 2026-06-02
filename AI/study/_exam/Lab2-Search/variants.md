# Variant Bank - Lab 2: Uninformed Search

This file lists exam-style variant questions for `Lab 2/Search_solution.py`.
Each variant is self-contained: a fresh agent reading only the solution's
docstring header + KNOB comments + function signatures should be able to
answer it by changing KNOB values (no function-body edits).

**Important note on scope.** Spec sec 8.3 lists the canonical Lab-2 variant
bank as: (1) 8-puzzle, (2) Manhattan vs Euclidean heuristic, (3) new
start/goal pair. However, the actual Lab 2 handout (`Lab 2/Lab 2.pdf`)
covers ONLY uninformed BFS/DFS - there is no A* and no heuristic in the
lab. Variants 1-3 below faithfully realise the spec's intent (different
problem instance, swappable algorithm parameter, new start/goal) using the
algorithms the lab actually teaches; variants 4-6 exercise the KNOBs that
the spec implies but the original variant bank had not covered. Each
variant's "Expected answer" has been verified by running
`Search_solution.py` with the variant's KNOB block applied.

**Child-ordering quirk to be aware of.** `Node.expand()` prepends every
child to its working list (see `Search_solution.py:Node.expand` docstring).
This means when expanding A in the A..J tree, BFS pops C before B at depth
1, then expands G's children before F's, etc. The solution path is still
optimal in the BFS sense (J at minimal depth 3) but the sibling traversal
order is the **reverse** of the state-space dict's listing. Every printed
fringe trace and expansion order in this document reflects this quirk -
when reproducing a variant by hand, push children right-to-left, not
left-to-right.

---

## Variant 1 - Solve the 3-room vacuum world

**Question.** The original Exercise 2 has two rooms (A and B). Extend the
problem to three rooms (A, B, C) arranged in a line - Left moves one room
toward A (no-op at A), Right moves one room toward C (no-op at C). This
matches L03 sec 5.1's anchored semantics generalised to 3 rooms. Starting
from `('A', 'Dirty', 'Dirty', 'Dirty')` with the agent in room A, use
breadth-first search to find the shortest action sequence that ends with
every room clean and the agent in room C. Report the solution path and
its length.

**KNOB changes expected** (all in `Search_solution.py`):

| KNOB | Old | New |
|---|---|---|
| `KNOB_DEFAULT_STRATEGY` | `None` | `"BFS"` |
| `KNOB_RUN_EXERCISE_1` | `True` | `False` |
| `KNOB_RUN_EXERCISE_3` | `True` | `False` |
| `KNOB_EX2_ROOMS` | `("A", "B")` | `("A", "B", "C")` |
| `KNOB_EX2_INITIAL_STATE` | `("A", "Dirty", "Dirty")` | `("A", "Dirty", "Dirty", "Dirty")` |
| `KNOB_EX2_GOAL_STATE` | `("B", "Clean", "Clean")` | `("C", "Clean", "Clean", "Clean")` |

**Expected answer.** BFS finds a **5-action plan** (Suck-A, Right, Suck-B,
Right, Suck-C). The state path has 6 states; depth = 5.

```
('A','Dirty','Dirty','Dirty')   start
  -> ('A','Clean','Dirty','Dirty')    Suck
  -> ('B','Clean','Dirty','Dirty')    Right
  -> ('B','Clean','Clean','Dirty')    Suck
  -> ('C','Clean','Clean','Dirty')    Right
  -> ('C','Clean','Clean','Clean')    Suck  -- GOAL
```

**Sanity check.** With anchored Left/Right semantics (no wrap-around) the
agent must take exactly two Right moves to go A->B->C, plus one Suck per
room = 5 actions. A cyclic Left/Right interpretation would still produce
5 actions in this direction. The minimum is 5 because the agent visits
each of the 3 rooms (must reach C, the goal location) and cleans each
once.

**What this tests.** The agent must (a) infer that
`build_vacuum_state_space()` auto-handles N rooms from `KNOB_EX2_ROOMS`,
(b) match the arity of the initial/goal tuples to the new room count, and
(c) decide BFS is the right algorithm for "shortest" path. Also tests
understanding of L03 sec 5.1's L/R semantics generalised to 3 rooms.

---

## Variant 2 - DFS vs BFS on the same problem

**Question.** Run the *Exercise-1* abstract A..J state space with goal J
under BOTH depth-first and breadth-first search. For each, report (a) the
order in which nodes are expanded (popped from the fringe), (b) the
maximum size the fringe ever reaches, and (c) the final solution path.
Then state which algorithm would have done better had J been a leaf in
the LEFT subtree (e.g. node D instead of J).

**KNOB changes expected.**

| KNOB | Old | New |
|---|---|---|
| `KNOB_DEFAULT_STRATEGY` | `None` | `None` *(keep - runs both)* |
| `KNOB_EX1_PRINT_FRINGE_TRACE` | `True` | `True` *(keep - needed for the answer)* |
| `KNOB_RUN_EXERCISE_2` | `True` | `False` |
| `KNOB_RUN_EXERCISE_3` | `True` | `False` |

Then RE-RUN with `KNOB_EX1_GOAL_STATE = "D"` to answer the "had J been D"
sub-question.

**Expected answer.** For goal J (verified by running the solution):

  - **DFS** expansion order: `A, B, D, E, C, F, G, H, I, J` (10 pops; the
    last pop is J and the goal-test fires). Max fringe size **3**. Path
    `A -> C -> G -> J`.
  - **BFS** expansion order: `A, C, B, G, F, E, D, J` (8 pops; J pops at
    step 8). Max fringe size **6**. Path `A -> C -> G -> J`.

  (Note: both BFS and DFS return the same path here because `Node.expand`'s
  child-prepend quirk pushes children right-to-left, so the BFS sibling
  traversal explores C before B and DFS dives left-first.)

For goal D (re-run with `KNOB_EX1_GOAL_STATE = "D"`):

  - **DFS** expansion order: `A, B, D` (3 pops). Path `A -> B -> D`.
  - **BFS** expansion order: `A, C, B, G, F, E, D` (7 pops). Path `A -> B -> D`.

So for a goal in the LEFT subtree (D), **DFS wins decisively** - 3
expansions vs BFS's 7. This is the classic "DFS wins when the goal is
shallow on the side it explores first" result (L03 sec 5.5).

**What this tests.** Direct comparison of fringe behaviour; ability to
read the fringe-trace output produced by `KNOB_EX1_PRINT_FRINGE_TRACE =
True`. Awareness that the search tree's branching factor and the
algorithm's traversal order interact - DFS is not "always slower than
BFS" or vice versa, the answer depends on where the goal is.

---

## Variant 3 - A new start/goal in the river puzzle

**Question.** Suppose the farmer / wolf / goat / cabbage are already
arranged as `('E', 'E', 'W', 'W')` - the farmer and wolf are on the east
bank, the goat and cabbage are still on the west. Is this configuration
safe (i.e. does it violate any eat-rule)? If it is, use BFS to find the
shortest action sequence that lands everyone on the east bank. If it
isn't, explain why and propose the closest safe state from which a
solution exists.

**KNOB changes expected.**

| KNOB | Old | New |
|---|---|---|
| `KNOB_DEFAULT_STRATEGY` | `None` | `"BFS"` |
| `KNOB_RUN_EXERCISE_1` | `True` | `False` |
| `KNOB_RUN_EXERCISE_2` | `True` | `False` |
| `KNOB_EX3_INITIAL_STATE` | `('W','W','W','W')` | `('W','E','W','W')` *(see below)* |
| `KNOB_EX3_GOAL_STATE` | `('E','E','E','E')` | `('E','E','E','E')` *(keep)* |

**Expected answer.** `('E', 'E', 'W', 'W')` is **NOT safe**: the goat
(index 2) and cabbage (index 3) are both on the west bank, while the
farmer (index 0) is on the east. The eat-rule `(2, 3)` says "if goat
shares a bank with cabbage and the farmer is not there, goat eats
cabbage" - so this state is unsafe and `build_river_state_space()` does
not register it as a key in the state-space dict. Setting
`KNOB_EX3_INITIAL_STATE = ('E','E','W','W')` and running the searcher
would raise `KeyError('E','E','W','W')` from `StateSpace.successor` when
the search tries to expand the root node.

The closest safe state with the wolf already on the east bank is
`('W','E','W','W')` - farmer back on the west with goat and cabbage,
wolf alone on the east (wolf alone has no prey on its bank, safe).
From that state, BFS finds a **3-action plan** (depth 3):

```
('W','E','W','W')                start (farmer with goat+cabbage; wolf alone east)
  -> ('E','E','W','E')   farmer ferries cabbage east (wolf+cabbage on E, goat alone W)
  -> ('W','E','W','E')   farmer returns alone (wolf+cabbage east, goat alone west)
  -> ('E','E','E','E')   farmer ferries goat east  -- GOAL
```

Why so short? With the wolf already on the east bank in the start state,
the puzzle has skipped the first 4 moves of the canonical 7-step solution
(take goat over, return alone, take wolf, bring goat back). Only the last
3 moves are needed.

**What this tests.** Ability to predict that the eat-rules controlled by
`KNOB_EX3_EAT_RULES` will gate the state space. Reading the docstring of
`KNOB_EX3_EAT_RULES` should be enough to derive the unsafety without
inspecting `is_safe()`. Also tests recognition that the river puzzle is
not symmetric - starting from an intermediate state shrinks the optimal
plan.

---

## Variant 4 (stretch - spec sec 8.3 wording) - 8-puzzle with a hand-built slice

**Question.** Replace the abstract A..J state space with a small slice of
the 8-puzzle: states are 3x3 tile permutations represented as 9-tuples,
the blank is `0`, and the goal is `(1,2,3,4,5,6,7,8,0)`. Starting from
`(1,2,3,4,5,6,0,7,8)` (blank in the bottom-left), use BFS to find the
shortest plan that reaches the goal.

**KNOB changes expected.**

| KNOB | New |
|---|---|
| `KNOB_DEFAULT_STRATEGY` | `"BFS"` (uniform step cost = BFS is sound; A* is out of scope for this lab) |
| `KNOB_EX1_STATE_SPACE` | A dict supplying `(1,2,3,4,5,6,0,7,8)`, `(1,2,3,4,5,6,7,0,8)`, `(1,2,3,4,5,6,7,8,0)` (the three states the optimal plan visits) and their relevant neighbours. See "How to build the slice" below. |
| `KNOB_EX1_INITIAL_STATE` | `(1,2,3,4,5,6,0,7,8)` |
| `KNOB_EX1_GOAL_STATE` | `(1,2,3,4,5,6,7,8,0)` |
| `KNOB_MAX_FRINGE_NODES` | `200_000` (8-puzzle has 181,440 reachable states; safe even for the slice) |
| `KNOB_RUN_EXERCISE_2` | `False` |
| `KNOB_RUN_EXERCISE_3` | `False` |

**Charter compliance note.** The full 8-puzzle adjacency dict (181,440
entries) cannot be hand-written in the KNOB block. The variant bank
charter says "edit KNOBs only, no function-body edits"; this variant
honours the charter by accepting a *hand-built minimal slice* covering
the optimal plan, not the whole graph. A full 8-puzzle requires a
generator function (out of scope for this lab; would naturally live in
`Search_solution.py` as a new builder alongside
`build_vacuum_state_space`).

**How to build the slice (KNOB block only).**

```python
# The blank moves Right twice to reach the goal.
KNOB_EX1_STATE_SPACE = {
    (1,2,3,4,5,6,0,7,8): [(1,2,3,4,5,6,7,0,8)],   # blank moves Right
    (1,2,3,4,5,6,7,0,8): [(1,2,3,4,5,6,7,8,0)],   # blank moves Right again
    (1,2,3,4,5,6,7,8,0): [],                       # goal, no successors needed
}
```

**Expected answer.** From `(1,2,3,4,5,6,0,7,8)` (blank at index 6) the
goal `(1,2,3,4,5,6,7,8,0)` (blank at index 8) is reached in a 2-action
plan: **blank moves Right, then Right again** - i.e. the blank traverses
the bottom row from left to right. Solution path has 3 states; depth 2.

```
(1,2,3,4,5,6,0,7,8)  -> (1,2,3,4,5,6,7,0,8)  -> (1,2,3,4,5,6,7,8,0)
```

**What this tests.** The KNOB block can repurpose Exercise 1's
state-space dict for any small graph problem. The honest constraint -
that a *full* 8-puzzle solver would need a generator function rather
than a literal dict - is itself a useful lesson about the limits of the
"all variants via KNOBs" promise.

---

## Variant 5 (bonus) - Removing a constraint changes the solution length

**Question.** In the river-crossing puzzle, *what happens to the BFS
solution length if you remove the goat-eats-cabbage rule but keep the
wolf-eats-goat rule?* Run the experiment and explain the result.

**KNOB changes expected.**

| KNOB | Old | New |
|---|---|---|
| `KNOB_DEFAULT_STRATEGY` | `None` | `"BFS"` |
| `KNOB_RUN_EXERCISE_1` | `True` | `False` |
| `KNOB_RUN_EXERCISE_2` | `True` | `False` |
| `KNOB_EX3_EAT_RULES` | `((1, 2), (2, 3))` | `((1, 2),)` |

**Expected answer.** With only the wolf-eats-goat rule the puzzle has a
**5-action plan** (depth 5) - two fewer than the classic 7-step solution.
Verified path:

```
('W','W','W','W')               start
  -> ('E','W','E','W')   farmer takes goat to east
  -> ('W','W','E','W')   farmer returns alone (goat alone on east)
  -> ('E','W','E','E')   farmer takes cabbage to east (goat+cabbage together east, fine: no rule forbids it now)
  -> ('W','W','E','E')   farmer returns alone (wolf alone west; goat+cabbage alone east, fine)
  -> ('E','E','E','E')   farmer takes wolf to east   -- GOAL
```

Why depth 5? With both rules (the default), every "shuttle" pattern
needs the farmer to escort the goat across alone twice (once over, once
back to ferry the wolf). Removing the goat-eats-cabbage rule lets the
farmer leave goat+cabbage together on the east bank, so the goat does
not need to be ferried back - cutting two moves.

**What this tests.** Connection between the constraint set and the
length of the optimal plan; reading the `KNOB_EX3_EAT_RULES` docstring
carefully (indices into the state tuple).

---

## Variant 6 (bonus) - Tree search vs graph search on a cyclic graph

**Question.** On the river-crossing puzzle, what happens if you disable
visited-tracking and run DFS? Predict the outcome and check.

**KNOB changes expected.**

| KNOB | Old | New |
|---|---|---|
| `KNOB_DEFAULT_STRATEGY` | `None` | `"DFS"` |
| `KNOB_RUN_EXERCISE_1` | `True` | `False` |
| `KNOB_RUN_EXERCISE_2` | `True` | `False` |
| `KNOB_EX3_TRACK_VISITED` | `None` (inherits global True) | `False` (force pure tree search) |
| `KNOB_MAX_EXPANSIONS` | `None` | `1000` (insurance to abort the runaway search) |

**Expected answer.** Without cycle detection, DFS oscillates forever
along the river: the farmer ferries the goat across, then comes back,
then ferries the goat across again, and so on. The fringe stays bounded
in size (DFS's frontier is O(b*m)) so `KNOB_MAX_FRINGE_NODES` does not
fire; the only safety net is `KNOB_MAX_EXPANSIONS`. With the cap at
1000, the searcher prints `"Expansion count exceeded 1000 - aborting."`
and returns no solution.

This is L03 sec 6 pitfall 5 made concrete: **DFS in cyclic state spaces
without the explored-set check is not complete** - and indeed in this
puzzle it does not even terminate. Re-running with
`KNOB_EX3_TRACK_VISITED = True` recovers a valid (depth-7) solution.

**What this tests.** Understanding of the tree-vs-graph search
distinction (L03 sec 3.4). Demonstrates *why* every KNOB-driven
exercise default sets visited tracking to True.

---

## Variant 7 (bonus) - "Any all-clean" goal predicate

**Question.** On the default 2-room vacuum world, what is the shortest
plan to reach **any** state where both rooms are clean, regardless of
the agent's final position?

**KNOB changes expected.**

| KNOB | Old | New |
|---|---|---|
| `KNOB_DEFAULT_STRATEGY` | `None` | `"BFS"` |
| `KNOB_RUN_EXERCISE_1` | `True` | `False` |
| `KNOB_RUN_EXERCISE_3` | `True` | `False` |
| `KNOB_EX2_GOAL_STATE` | `("B", "Clean", "Clean")` | `None` |

**Expected answer.** With `KNOB_EX2_GOAL_STATE = None`, the searcher
falls back to the built-in "all rooms clean" predicate (every status
== `KNOB_EX2_STATUSES[-1]`). From `('A','Dirty','Dirty')`, BFS finds a
**3-action plan** (depth 3):

```
('A','Dirty','Dirty')  -> ('A','Clean','Dirty')  -> ('B','Clean','Dirty')  -> ('B','Clean','Clean')
```

Same length and same final state as the equality-with-`('B','Clean','Clean')`
default - on this 2-room problem the "any" relaxation doesn't help
because the agent is already in A and must move to B to reach B's dirt.
The relaxation matters on asymmetric starts (e.g. start in B with both
dirty -> agent stays in B and the plan ends in A or B depending on which
is reached first).

**What this tests.** The `KNOB_EX2_GOAL_STATE = None` -> built-in
"all-clean" predicate plumbing. Useful for studying how a goal *test*
differs from a goal *state* (L03 sec 3.2).

"""
LAB 2: Uninformed Search (BFS, DFS) - Tree Search Skeleton + Vacuum World + Farmer/Wolf/Goat/Cabbage
====================================================================================================

PROBLEM STATEMENT (from Lab 2.pdf):
-----------------------------------
Exercise 1 - Implement the tree-search primitives in Search.py: insert(),
insert_all(), and remove_first().

    "Successor nodes are inserted at front of the fringe (successor list) as a
     node is expanded.
       - What search is this? A breadth (FIFO) or depth-first search (LIFO)?
       - How does the fringe look for goal J?
     What is the effect of inserting successor nodes at the end of the fringe
     as a node is expanded?
       - What search is this?
       - For goal J, give the fringe (successor list) after expanding each
         node with this type of search."

Exercise 2 - Use the search program to solve the vacuum-world problem using
breadth-first search.

    "Hint: one way to represent the state space in Python is by a dictionary
     where the current state is a tuple (location, A status, B status) and a
     list holds successor states for each action. For example:
       ('A', 'Dirty', 'Dirty'): [('A', 'Clean', 'Dirty'),
                                  ('A', 'Dirty', 'Dirty'),
                                  ('B', 'Dirty', 'Dirty')]"

Homework - Modify the search program to solve the farmer/wolf/goat/cabbage
river-crossing problem.

    "A farmer has a goat, a cabbage and a wolf to move across a river with a
     boat that can only hold himself and one other passenger. If the goat and
     wolf are alone, the wolf will eat the goat. If the goat and cabbage are
     alone, the goat will eat the cabbage."
    State tuple is (farmer, wolf, goat, cabbage), each on 'W' (west) or 'E'
    (east). Goal: ('E', 'E', 'E', 'E'). The successor function must drop
    states that violate the eat-each-other constraints.

MENTAL MODEL (one-line analogy):
--------------------------------
BFS is like exploring a maze room-by-room with a torch and a notebook - you
finish sweeping the entire current floor before climbing any stairs.  DFS is
like the same explorer charging down the first corridor they see, doubling
back only when they hit a dead-end.  The only difference between the two
algorithms in this lab is whether new corridors get stapled to the FRONT of
the to-do list (LIFO -> DFS) or the BACK of it (FIFO -> BFS).  Everything else
- the map, the nodes, the path-reconstruction - stays exactly the same.
(L03 sec 3.4 / sec 2.6: "the order in which you pick is the search strategy".)

Tree search vs graph search.  This file actually runs **graph search**
(L03 sec 3.4) - i.e. tree search plus an explored set - whenever
KNOB_TRACK_VISITED is True; run_exercise_1() flips it off (via
KNOB_EX1_TRACK_VISITED) to demonstrate the pure tree-search behaviour the
slides describe on the acyclic A..J tree.  On the vacuum world and the
river puzzle the graph has cycles, so cycle detection is mandatory
(without it DFS oscillates A<->B forever, and BFS revisits exponentially).

REFERENCES:
-----------
- Lecture 3 sec 3-sec 4: Uninformed search - BFS, DFS, IDS, UCS.
  See study/lectures/L03-Uninformed-Search.md (canonical reference).
- Glossary terms used:
    Breadth-first search (BFS) - FIFO frontier, expands shallowest node.
    Depth-first search (DFS)  - LIFO frontier, expands deepest node.
    Frontier (fringe)         - set of generated-but-unexpanded nodes.
    Node                      - search-tree wrapper (state + parent + depth).
    Successor function        - maps a state to the list of next states.
    State space               - directed graph of all states (here: a dict).

L03 SCOPE NOTE:
---------------
L03 sec 1.2 names FOUR uninformed strategies: BFS, UCS, DFS, IDS.  This lab's
default demos exercise BFS and DFS (the two the handout actually asks for).
UCS and IDS are reachable via KNOBs:
  - Depth-limited DFS  : set KNOB_MAX_DEPTH = ell
  - Iterative deepening: set KNOB_USE_IDS = True  (drives the depth-limited
                         loop ell = 0, 1, 2, ... until a goal or definitive
                         failure)
  - Uniform-cost search: set KNOB_STEP_COST_FN = fn(state, succ) -> cost > 0
                         and KNOB_DEFAULT_STRATEGY = "UCS"
The default behaviour is unchanged when these KNOBs are at their defaults.

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
The point of this file is that every uninformed-search exam variant in the
spec sec 8.3 / handout's variant bank can be posed by changing one or more
KNOBs at the top of the script - no function body needs editing.

1. To switch BFS / DFS / IDS / UCS:
     KNOB_DEFAULT_STRATEGY = "BFS" | "DFS" | "IDS" | "UCS" | None
   When None, every demo runs both BFS and DFS side-by-side (the default).

2. To gate which exercises run:
     KNOB_RUN_EXERCISE_1 / 2 / 3 = True | False

3. To change the abstract tree (Exercise 1):
     KNOB_EX1_STATE_SPACE   = { state -> [successors] }
     KNOB_EX1_INITIAL_STATE
     KNOB_EX1_GOAL_STATE
     KNOB_EX1_GOAL_PREDICATE = callable(state) -> bool  (overrides equality)

4. To change the vacuum world (Exercise 2):
     KNOB_EX2_ROOMS         = ("A","B")    -- extend to 3 rooms by adding "C"
     KNOB_EX2_STATUSES      = ("Dirty","Clean")  -- e.g. ("Dirty","Clean","VeryDirty")
     KNOB_EX2_INITIAL_STATE, KNOB_EX2_GOAL_STATE
     KNOB_EX2_GOAL_PREDICATE = callable(state) -> bool  (e.g. "any clean")
     KNOB_EX2_STATE_SPACE_OVERRIDE = dict  (hand-crafted successors)

5. To change the river-crossing puzzle (Homework):
     KNOB_EX3_INITIAL_STATE / KNOB_EX3_GOAL_STATE -- arity sets item count
     KNOB_EX3_EAT_RULES = ((predator_idx, prey_idx), ...) -- indexed by tuple position
     KNOB_EX3_PASSENGERS_PER_TRIP -- boat capacity (excluding farmer)
     KNOB_EX3_GOAL_PREDICATE -- overrides equality goal test
     KNOB_EX3_STATE_SPACE_OVERRIDE -- hand-crafted successors

6. To control fringe-trace printing per exercise:
     KNOB_EX1_PRINT_FRINGE_TRACE = True   (handout's "show the fringe")
     KNOB_EX2_PRINT_FRINGE_TRACE = False  (vacuum trace is large/noisy)
     KNOB_EX3_PRINT_FRINGE_TRACE = False  (river trace is large/noisy)

7. To force visited-tracking on/off per exercise (overrides KNOB_TRACK_VISITED):
     KNOB_EX1_TRACK_VISITED = False  (Ex1 default - acyclic tree, see L03 sec 5.5)
     KNOB_EX2_TRACK_VISITED = None   (use global; cyclic, needs True)
     KNOB_EX3_TRACK_VISITED = None   (use global; cyclic, needs True)

ENTRY POINT: yes
----------------
Running this file directly demonstrates every exercise.  This file does NOT
modify the original Search.py; the original template stays intact for the
exam-prep workflow.

=================================================================
"""

from __future__ import annotations

from typing import Any, Callable, Self


# ===========================================================================
#                                K  N  O  B  S
# ===========================================================================
# All tunable parameters are declared up here so a fresh reader (or exam
# agent) can solve a variant by editing this block ONLY - no function-body
# changes required.

# KNOB: KNOB_DEFAULT_STRATEGY (default=None, allowed={None, "BFS", "DFS", "IDS", "UCS"})
#   What it does: forces every demonstration in __main__ to use a single
#       search strategy.  When None, each demo runs BOTH BFS and DFS so the
#       student can directly compare the fringes.
#   Effect: BFS = FIFO fringe; DFS = LIFO fringe; IDS = depth-limited DFS in
#       a loop ell=0,1,2,... (set KNOB_MAX_DEPTH = None for unbounded IDS);
#       UCS = priority queue keyed by g(n) using KNOB_STEP_COST_FN.
#   Exam variants: lock to "BFS" for the canonical Exercise-2 / Homework
#       walkthrough; lock to "DFS" to demonstrate depth-first wander;
#       lock to "IDS" for L03 sec 4.4; lock to "UCS" for L03 sec 4.2.
KNOB_DEFAULT_STRATEGY: str | None = None

# KNOB: KNOB_PRINT_FRINGE_TRACE (default=True, allowed={True, False})
#   What it does: GLOBAL default for the per-step "Fringe: [...]" debug
#       print inside Searcher.tree_search().  Each exercise has its own
#       KNOB_EXn_PRINT_FRINGE_TRACE that wins if set to True/False; if a
#       per-exercise KNOB is None it falls back to this global.
#   Effect: pure output noise control; does not change the algorithm.
#   Exam variants: set False to obtain a clean "solution path only" report.
KNOB_PRINT_FRINGE_TRACE: bool = True

# Per-exercise overrides for the fringe trace.  None = use the global.
# Defaults: Ex1 ON (the handout asks for it), Ex2/Ex3 OFF (their fringes
# explode and the trace becomes unreadable on the cyclic state spaces).
KNOB_EX1_PRINT_FRINGE_TRACE: bool | None = True
KNOB_EX2_PRINT_FRINGE_TRACE: bool | None = False
KNOB_EX3_PRINT_FRINGE_TRACE: bool | None = False

# KNOB: KNOB_MAX_FRINGE_NODES (default=10_000, range=>=1)
#   What it does: hard ceiling on the size of the frontier before the search
#       aborts.  Cheap insurance against runaway searches if a buggy
#       successor function pushes children faster than the fringe can drain.
#   Effect: larger limit = more memory, more chances to find a solution.
#       Note: a cycle-free infinite chain that keeps the fringe small never
#       trips this; use KNOB_MAX_EXPANSIONS for that case.
#   Exam variants: bump to 200_000 for 8-puzzle; 10_000 is plenty for all
#       three default exercises.
KNOB_MAX_FRINGE_NODES: int = 10_000

# KNOB: KNOB_MAX_EXPANSIONS (default=None, range=>=1 or None)
#   What it does: hard ceiling on the number of pop+expand iterations.
#       Catches "fringe stays small but algorithm never terminates" cases
#       (e.g. successor returning a fresh single state forever).  None
#       means unlimited.
KNOB_MAX_EXPANSIONS: int | None = None

# KNOB: KNOB_TRACK_VISITED (default=True, allowed={True, False})
#   What it does: GLOBAL default for visited-tracking.  When True the
#       searcher refuses to expand a state it has already expanded - this
#       turns the algorithm from "tree search" (slides' description) into
#       "graph search" (L03 sec 3.4).  Each exercise has its own
#       KNOB_EXn_TRACK_VISITED that wins if set; None falls back to this.
#   Effect: tree search on a graph WITH cycles never terminates without
#       this - DFS on the vacuum world, for instance, ping-pongs A<->B
#       forever.  BFS is also exponentially wasteful without it.  Tree
#       search on a graph WITHOUT cycles (Exercise 1's A..J tree) does
#       not need this and may even mask interesting fringe behaviour.
#   Exam variants: set True to match textbook BFS/DFS; set False to obtain
#       the literal "tree-search" behaviour the slides specify (and use a
#       very small KNOB_MAX_EXPANSIONS to demonstrate the explosion).
KNOB_TRACK_VISITED: bool = True

# Per-exercise overrides for visited tracking.  None = use the global.
# Ex1 is hard-defaulted to False because the A..J state space is an acyclic
# tree and the handout's hand-trace expects pure tree-search semantics.
KNOB_EX1_TRACK_VISITED: bool | None = False
KNOB_EX2_TRACK_VISITED: bool | None = None
KNOB_EX3_TRACK_VISITED: bool | None = None

# KNOB: KNOB_MAX_DEPTH (default=None, range=>=0 or None)
#   What it does: a depth cutoff for depth-limited DFS (L03 sec 4.4.0).  Any
#       node with depth > KNOB_MAX_DEPTH is not expanded.  None = no limit.
#   Effect: enables depth-limited search and is the building block for IDS
#       (KNOB_USE_IDS = True).  Has no effect on BFS / UCS pop order, only
#       on whether children get pushed.
#   Exam variants: KNOB_MAX_DEPTH = 4, KNOB_DEFAULT_STRATEGY = "DFS" gives
#       depth-limited DFS to depth 4.
KNOB_MAX_DEPTH: int | None = None

# KNOB: KNOB_USE_IDS (default=False)
#   What it does: when True, KNOB_DEFAULT_STRATEGY = "IDS" runs depth-limited
#       DFS in a loop ell = 0, 1, 2, ..., growing the depth bound by 1 each
#       iteration until a goal is found or a definitive "no solution"
#       failure is returned.  Each iteration uses KNOB_MAX_DEPTH = ell.
#   Effect: implements L03 sec 4.4's iterative deepening.  When
#       KNOB_DEFAULT_STRATEGY is "IDS" this is implicitly True.
KNOB_USE_IDS: bool = False

# KNOB: KNOB_IDS_MAX_DEPTH (default=64, range=>=0)
#   What it does: the largest depth limit IDS will try before giving up.
#       Default 64 is generous for the lab's exercises.
KNOB_IDS_MAX_DEPTH: int = 64

# KNOB: KNOB_STEP_COST_FN (default=None)
#   What it does: a function f(state, succ_state) -> non-negative float used
#       by UCS as the step cost.  None means "uniform cost = 1 per step"
#       (in which case UCS reduces to BFS - L03 sec 4.2).
#   Effect: only consulted when KNOB_DEFAULT_STRATEGY == "UCS"; ignored
#       otherwise.  The priority queue is keyed by g(n) = sum of step costs
#       from root to n.
#   Exam variants: a Romania-style map needs KNOB_STEP_COST_FN to lift the
#       road distances out of the dict; the lab's defaults don't need it.
KNOB_STEP_COST_FN: Callable[[Any, Any], float] | None = None

# KNOB: KNOB_RUN_EXERCISE_1 (default=True)
# KNOB: KNOB_RUN_EXERCISE_2 (default=True)
# KNOB: KNOB_RUN_EXERCISE_3 (default=True)
#   What they do: each toggles whether the corresponding demonstration is
#       printed when this file is run directly.
KNOB_RUN_EXERCISE_1: bool = True
KNOB_RUN_EXERCISE_2: bool = True
KNOB_RUN_EXERCISE_3: bool = True

# -------------------- Exercise 1 - Abstract tree A..J --------------------
# This is the canonical example from the slides: a small binary-ish tree with
# G branching to H, I, J.  The handout asks for the fringe after expanding
# each node, with goal J, under both BFS and DFS.

# KNOB: KNOB_EX1_STATE_SPACE (default=letters A..J from the handout)
#   What it does: defines the search graph as { state -> [successor states] }.
#       Leaves map to the empty list.  The searcher is type-agnostic.
#   Exam variants: replace with a Romania-style map; replace with the
#       8-puzzle adjacency dict to ask "DFS expansion order from this start
#       board"; etc.
KNOB_EX1_STATE_SPACE: dict[str, list[str]] = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F", "G"],
    "D": [],
    "E": [],
    "F": [],
    "G": ["H", "I", "J"],
    "H": [],
    "I": [],
    "J": [],
}

# KNOB: KNOB_EX1_INITIAL_STATE (default="A")
# KNOB: KNOB_EX1_GOAL_STATE    (default="J")
#   What they do: the start and target nodes for Exercise 1's tree search.
KNOB_EX1_INITIAL_STATE: str = "A"
KNOB_EX1_GOAL_STATE: str = "J"

# KNOB: KNOB_EX1_GOAL_PREDICATE (default=None)
#   What it does: when set, the searcher uses this callable instead of
#       equality with KNOB_EX1_GOAL_STATE.  None = default equality.
#   Exam variants: lambda s: s in ("F","G","J") for a multi-goal variant.
KNOB_EX1_GOAL_PREDICATE: Callable[[Any], bool] | None = None

# -------------------- Exercise 2 - Two-room vacuum world --------------------
# The classic AIMA two-room vacuum.  Rooms are A and B; each is either Dirty
# or Clean; the agent is in one room at a time.  The three actions are
# Suck, Left, Right.

# KNOB: KNOB_EX2_ROOMS (default=("A", "B"))
#   What it does: ordered tuple of room labels.  Must have at least one
#       room.  Left moves the agent one room to the left (no-op at
#       rooms[0]); Right moves one room to the right (no-op at rooms[-1]).
#       This matches L03 sec 5.1's anchored semantics ("L moves to A,
#       no-op if already in A").  No wrap-around.
#   Effect: extending to 3 rooms grows the state space from 8 to 24 nodes.
#   Exam variants: ("A","B","C") for the 3-room variant; ("A",) for a
#       degenerate single-room variant.
KNOB_EX2_ROOMS: tuple[str, ...] = ("A", "B")

# KNOB: KNOB_EX2_STATUSES (default=("Dirty", "Clean"))
#   What it does: ordered tuple of dirt levels.  The Suck action sets the
#       current room's status to statuses[-1] ("fully clean"); rooms in
#       other statuses are treated as "dirty" by the default goal-predicate.
#   Effect: a 3-level variant ("Dirty","Clean","VeryDirty") requires the
#       caller to also supply a custom KNOB_EX2_STATE_SPACE_OVERRIDE or
#       KNOB_EX2_SUCK_RULE (TODO if a future variant needs it).  Default
#       2-level semantics work out of the box.
KNOB_EX2_STATUSES: tuple[str, ...] = ("Dirty", "Clean")

# KNOB: KNOB_EX2_INITIAL_STATE (default=("A", "Dirty", "Dirty"))
#   What it does: the starting (location, *statuses) tuple.  Its arity must
#       match (1 + len(KNOB_EX2_ROOMS)).
KNOB_EX2_INITIAL_STATE: tuple = ("A", "Dirty", "Dirty")

# KNOB: KNOB_EX2_GOAL_STATE (default=("B", "Clean", "Clean"))
#   What it does: the (location, *statuses) tuple the agent must reach.
#       Set to None and pair with KNOB_EX2_GOAL_PREDICATE to mean "any
#       state with all rooms clean".  The default goal predicate (below)
#       treats None as "all rooms clean, regardless of agent position".
KNOB_EX2_GOAL_STATE: tuple | None = ("B", "Clean", "Clean")

# KNOB: KNOB_EX2_GOAL_PREDICATE (default=None)
#   What it does: when set, overrides equality with KNOB_EX2_GOAL_STATE.
#       If unset AND KNOB_EX2_GOAL_STATE is None, the searcher uses the
#       built-in "all rooms clean" predicate (status == KNOB_EX2_STATUSES[-1]
#       for every room).
KNOB_EX2_GOAL_PREDICATE: Callable[[Any], bool] | None = None

# KNOB: KNOB_EX2_STATE_SPACE_OVERRIDE (default=None)
#   What it does: lets a variant supply a hand-crafted state-space dict
#       (e.g. with a broken / one-way actuator).  When None, a complete
#       table is generated by build_vacuum_state_space() using Suck/Left/Right.
#       Tested with `is not None`, so an intentionally-empty dict {} is honoured.
KNOB_EX2_STATE_SPACE_OVERRIDE: dict | None = None

# -------------------- Homework - Farmer / Wolf / Goat / Cabbage ------------
# Classic river-crossing puzzle.  State is a 4-tuple of bank labels:
#   (farmer, wolf, goat, cabbage), each in {'W', 'E'}.
# Generalises to N items via len(KNOB_EX3_INITIAL_STATE); index 0 is always
# the agent / boat-pilot.

# KNOB: KNOB_EX3_BANKS (default=('W', 'E'))
KNOB_EX3_BANKS: tuple[str, str] = ("W", "E")

# KNOB: KNOB_EX3_INITIAL_STATE (default=('W', 'W', 'W', 'W'))
# KNOB: KNOB_EX3_GOAL_STATE    (default=('E', 'E', 'E', 'E'))
#   The arity of these tuples determines the item count.  Index 0 is the
#   farmer; indices 1..N-1 are the items.
KNOB_EX3_INITIAL_STATE: tuple = ("W", "W", "W", "W")
KNOB_EX3_GOAL_STATE: tuple = ("E", "E", "E", "E")

# KNOB: KNOB_EX3_EAT_RULES (default=( (1, 2), (2, 3) )  meaning wolf-eats-
#                          -goat and goat-eats-cabbage)
#   What it does: list of (predator_index, prey_index) pairs.  Indices are
#       positions into the state tuple (0=farmer, 1=wolf, 2=goat, 3=cabbage).
#       Whenever a predator shares a bank with its prey AND the farmer
#       (index 0) is NOT on that bank, the state is forbidden.
#   Effect: completely controls which states are "safe".
#   Exam variants: ((1,2),) keeps only wolf-eats-goat (5-step solution);
#       () drops all constraints (3-step trivial solution).
KNOB_EX3_EAT_RULES: tuple[tuple[int, int], ...] = ((1, 2), (2, 3))

# KNOB: KNOB_EX3_PASSENGERS_PER_TRIP (default=1, range=>=0)
#   What it does: the maximum number of non-farmer passengers the boat
#       carries per trip.  Handout fixes this at 1.
KNOB_EX3_PASSENGERS_PER_TRIP: int = 1

# KNOB: KNOB_EX3_GOAL_PREDICATE (default=None)
#   What it does: when set, overrides equality with KNOB_EX3_GOAL_STATE.
#   Exam variants: lambda s: all(b == "E" for b in s[1:]) to ask "everyone
#       except the farmer on east".
KNOB_EX3_GOAL_PREDICATE: Callable[[Any], bool] | None = None

# KNOB: KNOB_EX3_STATE_SPACE_OVERRIDE (default=None)
#   What it does: parallel of KNOB_EX2_STATE_SPACE_OVERRIDE for the river
#       puzzle.  When None, build_river_state_space() generates the full
#       table from the eat-rules and passenger cap.  Tested with `is not None`.
KNOB_EX3_STATE_SPACE_OVERRIDE: dict | None = None


# ===========================================================================
#                          C O R E   D A T A   T Y P E S
# ===========================================================================


class StateSpace:
    """A read-only dictionary mapping each state to its list of successors.

    The searcher only ever calls `.successor(state)`; the underlying
    representation is opaque.  This is what lets the same searcher solve
    Exercise 1 (states are letters), Exercise 2 (states are tuples), and the
    homework (states are 4-tuples) without modification.
    """

    def __init__(self, state_space: dict | None = None):
        self.state_space = state_space

    def successor(self, state: Any):
        """Return the list of successor states for `state`.

        L03 sec 3.2 defines the successor function as the core of a search
        problem.  When the state space has not been wired up at all, we
        raise a ValueError immediately - the original template merely
        printed a warning and then crashed with TypeError on the next line.
        """
        if self.state_space is None:
            raise ValueError(
                "StateSpace.successor called with no state_space set"
            )
        return self.state_space[state]


class Node:
    """A node in the search tree.

    A node bundles (a) the state it represents, (b) the parent node that
    generated it (so we can reconstruct the path), and (c) its depth.  The
    depth field is consulted by depth-limited DFS / IDS (L03 sec 4.4) when
    KNOB_MAX_DEPTH is set.
    """

    def __init__(self, state: Any, parent: Self | None = None, depth: int = 0):
        self.state = state
        self.parent_node = parent
        self.depth = depth

    def path(self) -> list[Self]:
        """Return the path from this node up to the root.

        Contract: the returned list is in **leaf-to-root** order, i.e. the
        first element is `self` and the last is the root.  Callers that
        want root-to-leaf order should `reversed(path)` (see `Searcher.run`).
        """
        current_node = self
        path = [self]
        while current_node.parent_node:
            current_node = current_node.parent_node
            path.append(current_node)
        return path

    def expand(self, state_space: StateSpace) -> list["Node"]:
        """Generate child nodes for every state-space successor of self.state.

        Implementation detail: each child is **prepended** to `successors`
        via the module-level `insert()` helper, so after the loop
        `successors` holds the children in **reverse** of the dict's listed
        order.  The caller (`tree_search`) then pushes that reversed list
        onto the fringe via `insert_all()`:

          - For DFS (insert_as_first=True), the fringe ends up with the
            leftmost (dict-order-first) child on TOP of the stack, popped
            next.  This is exactly L03 sec 5.5's "left-first DFS"
            convention: "DFS pushes children onto the LIFO stack in
            right-to-left order, so the leftmost child ends up on top of
            the stack and gets popped next."
          - For BFS (insert_as_first=False), the fringe receives the
            reversed list at the back, so the dict-order-first child
            ends up popped LAST among siblings, not first.  This is a
            **deliberate** quirk of the original template; for the A..J
            tree it means BFS expands `C` before `B` after expanding A.
            The resulting solution path A->C->G->J is still BFS-optimal
            (J is at minimal depth 3); only the sibling traversal order
            differs from a textbook BFS that pushes children in
            dict-order.

        L03 sec 6 pitfall 6 ("state vs node") applies here: every child
        Node wraps a fresh state but shares no identity with previously
        generated nodes.
        """
        successors: list[Node] = []
        children = state_space.successor(self.state)
        for child in children:
            s = Node(child, self, self.depth + 1)
            successors = insert(s, successors)
        return successors

    def display(self) -> None:
        print(self)

    def __repr__(self):
        return f"State: {self.state} - Depth: {self.depth}"


# ===========================================================================
#                F R I N G E   P R I M I T I V E S   (Exercise 1)
# ===========================================================================
# The three functions below are the entire difference between BFS and DFS in
# this implementation.  Note that we never mutate the input list - every
# function returns a fresh list.  That makes the searcher easier to debug:
# you can print the fringe before and after and they really are different
# objects, not aliases.


def insert(node: Node, queue: list[Node], insert_as_first: bool = True) -> list[Node]:
    """Return a NEW list with `node` inserted into `queue`.

    The choice between LIFO (insert_as_first=True => DFS) and FIFO
    (insert_as_first=False => BFS) is the only behavioural switch in this
    file.  Everything else - the state space, the goal test, the
    bookkeeping - is identical between the two algorithms.

    List concatenation (`+`) returns a new list, so the input `queue` is
    never mutated - this upholds the no-mutate contract spelled out in the
    original template's docstring.
    """
    if insert_as_first:
        return [node] + queue
    return queue + [node]


def insert_all(
    nodes_to_add: list[Node], queue: list[Node], insert_as_first: bool = True
) -> list[Node]:
    """Insert every node from `nodes_to_add` into `queue`, one at a time.

    Building the new list one insert() call at a time (rather than one
    list-concatenation) keeps the per-insertion ordering identical to what
    a hand-trace on the whiteboard would produce - useful for the exam
    question "give the fringe after expanding each node".
    """
    new_queue = queue
    for node in nodes_to_add:
        new_queue = insert(node, new_queue, insert_as_first)
    return new_queue


def remove_first(queue: list[Node]) -> Node:
    """Pop and return the first element of `queue` (the head).

    Always pops the head.  Whether that head is the "shallowest
    unexpanded node" (BFS) or the "deepest unexpanded node" (DFS) depends
    entirely on how `insert()` chose to splice new nodes in.  This is the
    elegance of the design: same removal rule, different insertion rules,
    two different algorithms.  This mutates `queue` (which is consistent
    with the template's docstring "removes the first element").
    """
    return queue.pop(0)


# ===========================================================================
#                              S E A R C H E R
# ===========================================================================


class Searcher:
    """Generic searcher parameterised by initial state, goal, and graph.

    The default _is_goal performs equality with self.goal_state.  Override
    by passing goal_predicate to __init__, or via the per-exercise
    KNOB_EXn_GOAL_PREDICATE plumbing in the demo drivers.

    BFS / DFS run through `tree_search(insert_as_first=...)`.  IDS / UCS
    use dedicated entry points (`iterative_deepening_search`,
    `uniform_cost_search`).
    """

    def __init__(
        self,
        initial_state,
        goal_state,
        state_space: StateSpace | None = None,
        goal_predicate: Callable[[Any], bool] | None = None,
        track_visited: bool | None = None,
        print_fringe_trace: bool | None = None,
        max_depth: int | None = None,
    ):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.state_space = state_space
        self.goal_predicate = goal_predicate
        # None on either of these means "use the global KNOB".
        self.track_visited = track_visited
        self.print_fringe_trace = print_fringe_trace
        self.max_depth = max_depth

    def _resolve_track_visited(self) -> bool:
        return KNOB_TRACK_VISITED if self.track_visited is None else self.track_visited

    def _resolve_print_fringe_trace(self) -> bool:
        return (
            KNOB_PRINT_FRINGE_TRACE
            if self.print_fringe_trace is None
            else self.print_fringe_trace
        )

    def _resolve_max_depth(self) -> int | None:
        return KNOB_MAX_DEPTH if self.max_depth is None else self.max_depth

    def _is_goal(self, state) -> bool:
        """Goal test.  L03 sec 3.2 defines this as a function, not equality."""
        if self.goal_predicate is not None:
            return self.goal_predicate(state)
        return state == self.goal_state

    def tree_search(self, insert_as_first: bool = True) -> list[Node] | None:
        """BFS / DFS / depth-limited DFS via FIFO or LIFO fringe.

        Returns None when the fringe empties before a goal is found
        (the original template's `while fringe is not None` was a subtle
        bug - a Python list is never None; it's only ever empty).  With
        KNOB_TRACK_VISITED disabled and a cyclic state space, the loop
        would still run forever - that is why visited-tracking exists
        (L03 sec 6 pitfall 5).

        When self.max_depth is not None, child nodes deeper than that
        limit are not pushed onto the fringe (depth-limited DFS, L03
        sec 4.4.0).  This is the building block of IDS.
        """
        track_visited = self._resolve_track_visited()
        print_trace = self._resolve_print_fringe_trace()
        max_depth = self._resolve_max_depth()
        visited: set = set()

        cutoff_hit = False  # for IDS to distinguish "no solution" from "go deeper"
        expansions = 0

        fringe: list[Node] = []
        initial_node = Node(self.initial_state)
        fringe = insert(initial_node, fringe, insert_as_first)
        while fringe:
            if len(fringe) > KNOB_MAX_FRINGE_NODES:
                print(f"Fringe exceeded {KNOB_MAX_FRINGE_NODES} nodes - aborting.")
                return None
            if (
                KNOB_MAX_EXPANSIONS is not None
                and expansions > KNOB_MAX_EXPANSIONS
            ):
                print(
                    f"Expansion count exceeded {KNOB_MAX_EXPANSIONS} - aborting."
                )
                return None
            node = remove_first(fringe)
            if self._is_goal(node.state):
                return node.path()
            # Cycle detection: only skip AFTER the goal test (so a goal that
            # happens to equal a visited state still wins) and BEFORE
            # expansion.  Note: L03 sec 3.4 also checks `s' not in frontier`
            # before pushing.  We don't dedup the fringe - duplicates may
            # sit there but are dropped harmlessly when popped (the
            # `visited` guard fires), so the solution path matches L03's
            # but the fringe trace may show transient duplicates.
            if track_visited:
                if node.state in visited:
                    continue
                visited.add(node.state)
            if max_depth is not None and node.depth >= max_depth:
                # Don't expand past the depth bound; remember that we hit
                # the bound so IDS can distinguish "cutoff" from "failure".
                cutoff_hit = True
                continue
            children = node.expand(self.state_space)
            fringe = insert_all(children, fringe, insert_as_first)
            expansions += 1
            if print_trace:
                print(f"Fringe: {fringe}")
        # Stash the cutoff flag where iterative_deepening_search can find it.
        self._last_run_hit_cutoff = cutoff_hit
        return None

    def iterative_deepening_search(self) -> list[Node] | None:
        """IDS (L03 sec 4.4): repeated depth-limited DFS, ell = 0, 1, 2, ...

        Stops at the first ell that returns a solution, or at
        KNOB_IDS_MAX_DEPTH (definitive failure if no cutoff was hit at
        that depth).
        """
        original_max_depth = self.max_depth
        try:
            for ell in range(0, KNOB_IDS_MAX_DEPTH + 1):
                self.max_depth = ell
                result = self.tree_search(insert_as_first=True)
                if result is not None:
                    return result
                if not getattr(self, "_last_run_hit_cutoff", False):
                    # No solution exists within the bound AND no node hit
                    # the depth cap - i.e. the search exhausted the
                    # reachable graph.  Going deeper won't help.
                    return None
        finally:
            self.max_depth = original_max_depth
        return None

    def uniform_cost_search(self) -> list[Node] | None:
        """UCS (L03 sec 4.2): priority queue keyed by g(n).

        Step cost is KNOB_STEP_COST_FN(state, succ) when set; otherwise
        every step costs 1 (in which case UCS reduces to BFS, L03 sec 4.2).
        Goal-test on POP (L03 sec 4.2.1) to preserve optimality.
        """
        import heapq

        step_cost = KNOB_STEP_COST_FN or (lambda _s, _t: 1.0)
        track_visited = self._resolve_track_visited()
        print_trace = self._resolve_print_fringe_trace()

        counter = 0  # tiebreaker for the heap
        visited: set = set()
        start = Node(self.initial_state)
        # Heap entry: (g, counter, node).  g is cumulative cost.
        heap: list = []
        heapq.heappush(heap, (0.0, counter, start))
        while heap:
            g, _, node = heapq.heappop(heap)
            if self._is_goal(node.state):
                return node.path()
            if track_visited:
                if node.state in visited:
                    continue
                visited.add(node.state)
            for child_state in self.state_space.successor(node.state):
                child = Node(child_state, node, node.depth + 1)
                counter += 1
                heapq.heappush(
                    heap, (g + step_cost(node.state, child_state), counter, child)
                )
            if print_trace:
                print(f"UCS heap size: {len(heap)}  g={g}")
        return None

    def run(self, insert_as_first: bool = True, strategy: str | None = None) -> list[Node] | None:
        """Dispatch the strategy and pretty-print the solution path."""
        # Choose the algorithm.
        if strategy is None:
            strategy = KNOB_DEFAULT_STRATEGY
        if strategy == "IDS" or KNOB_USE_IDS:
            path = self.iterative_deepening_search()
        elif strategy == "UCS":
            path = self.uniform_cost_search()
        else:
            # BFS / DFS / None all go through tree_search with the
            # appropriate insert_as_first.
            path = self.tree_search(insert_as_first)

        if path is None:
            print("No solution found.")
            return None
        print("Solution path:")
        # The path list is leaf-to-root; reversed() reads naturally for a
        # human ("start -> step 1 -> ... -> goal").
        for node in reversed(path):
            node.display()
        return path


# ===========================================================================
#               V A C U U M - W O R L D   B U I L D E R
# ===========================================================================


def build_vacuum_state_space(
    rooms: tuple[str, ...],
    statuses: tuple[str, ...] = ("Dirty", "Clean"),
) -> dict[tuple, list[tuple]]:
    """Generate the full transition table for the N-room vacuum world.

    For every reachable (location, *room_statuses) state we list the three
    standard successor states corresponding to the actions Suck, Left,
    Right.  Generating this table programmatically (rather than hand-typing
    it) is what lets KNOB_EX2_ROOMS scale from 2 rooms to 3, 4, ...

    Action semantics (L03 sec 5.1):
      - SUCK : the current room's status becomes statuses[-1] (the "clean"
               sentinel).  Position unchanged.  Emitted even if the room
               is already clean (matches the handout's hint, which lists
               ('A','Clean','Dirty') as a successor of ('A','Dirty','Dirty')).
      - LEFT : the agent moves one room toward index 0 (no wrap-around).
               At rooms[0] this is a self-loop, matching L03 sec 5.1:
               "L moves to A, no-op if already in A".
      - RIGHT: the agent moves one room toward index len(rooms)-1 (no
               wrap-around).  At rooms[-1] this is a self-loop, matching
               L03 sec 5.1: "R moves to B, no-op if already in B".

    Handout cross-check for the 2-room case:
      ('A','Dirty','Dirty') -> [
          ('A','Clean','Dirty'),   # Suck
          ('A','Dirty','Dirty'),   # Left  -> self-loop (already at rooms[0])
          ('B','Dirty','Dirty')    # Right -> step to rooms[1]
      ]
    """
    from itertools import product

    space: dict[tuple, list[tuple]] = {}

    for location in rooms:
        for status_combo in product(statuses, repeat=len(rooms)):
            state = (location,) + status_combo
            successors: list[tuple] = []

            # Action 1: SUCK - mark the current room as fully clean.
            new_statuses = list(status_combo)
            new_statuses[rooms.index(location)] = statuses[-1]
            successors.append((location,) + tuple(new_statuses))

            # Action 2: LEFT - step one room left, anchored at rooms[0].
            cur_idx = rooms.index(location)
            left_idx = cur_idx - 1 if cur_idx > 0 else cur_idx
            successors.append((rooms[left_idx],) + status_combo)

            # Action 3: RIGHT - step one room right, anchored at rooms[-1].
            right_idx = cur_idx + 1 if cur_idx < len(rooms) - 1 else cur_idx
            successors.append((rooms[right_idx],) + status_combo)

            space[state] = successors

    return space


def _vacuum_all_clean_goal(statuses: tuple[str, ...]) -> Callable[[Any], bool]:
    """Return a goal predicate "every room status equals statuses[-1]"."""
    clean_status = statuses[-1]
    return lambda state: all(s == clean_status for s in state[1:])


# ===========================================================================
#                H O M E W O R K   B U I L D E R
# ===========================================================================


def _swap_bank(banks: tuple[str, str], bank: str) -> str:
    """Helper: return the bank that isn't `bank`.

    Assumes a 2-element `banks` tuple - the river puzzle's two-bank model.
    Generalising to >2 banks would require a multi-way move generator.
    """
    return banks[0] if bank == banks[1] else banks[1]


def build_river_state_space(
    banks: tuple[str, str],
    eat_rules: tuple[tuple[int, int], ...],
    passengers_per_trip: int,
    item_count: int = 4,
) -> dict[tuple, list[tuple]]:
    """Generate every (farmer, *items) state and its safe successors.

    `item_count` is the arity of the state tuple (default 4 = farmer +
    wolf + goat + cabbage).  Variants with a 5th item (chicken, fox, ...)
    can pass item_count=5 and use eat_rules keyed by the new tuple
    positions.

    The procedure mirrors the homework's instructions verbatim:
      1. Enumerate every `item_count`-tuple over banks^item_count.
      2. For each safe state, list ALL syntactically valid moves (the
         farmer crosses alone, or with up to `passengers_per_trip` items
         currently on the same bank as the farmer).
      3. Filter out successor states that violate the eat rules.
    Splitting (2) and (3) keeps the code mappable onto the handout's
    instructions, which say "include successor states that violate the
    problem constraints; define successor_fn to return states that DO
    NOT violate them".
    """
    from itertools import combinations, product

    def is_safe(state: tuple) -> bool:
        # The farmer is at index 0; eat rules use absolute indices into the
        # state tuple, matching the docstring of KNOB_EX3_EAT_RULES.
        farmer_bank = state[0]
        for predator_idx, prey_idx in eat_rules:
            if (
                state[predator_idx] == state[prey_idx]
                and state[predator_idx] != farmer_bank
            ):
                return False
        return True

    space: dict[tuple, list[tuple]] = {}
    # All |banks|^item_count syntactic states.
    for state in product(banks, repeat=item_count):
        if not is_safe(state):
            # Unreachable states get no successors; including them as keys
            # would let a buggy search re-enter them.
            continue

        farmer_bank = state[0]
        # The farmer must always be in the boat; we then choose
        # 0..passengers_per_trip of the OTHER items on the farmer's bank
        # to come along.
        co_items_on_same_bank = [
            i for i in range(1, item_count) if state[i] == farmer_bank
        ]
        candidate_successors: list[tuple] = []
        for k in range(0, passengers_per_trip + 1):
            for chosen in combinations(co_items_on_same_bank, k):
                new_state = list(state)
                new_state[0] = _swap_bank(banks, farmer_bank)
                for idx in chosen:
                    new_state[idx] = _swap_bank(banks, farmer_bank)
                candidate_successors.append(tuple(new_state))

        # successor_fn (step 3 in the handout): drop unsafe successors.
        space[state] = [s for s in candidate_successors if is_safe(s)]

    return space


# ===========================================================================
#                       D E M O   D R I V E R S
# ===========================================================================


def _strategies_to_run() -> list[tuple[str, bool, str]]:
    """Return the list of (label, insert_as_first, strategy_tag) tuples.

    insert_as_first=True => LIFO => DFS.  False => FIFO => BFS.  The
    strategy_tag is passed to Searcher.run() to select IDS / UCS where
    appropriate; for BFS / DFS it is the same as the label root.
    """
    if KNOB_DEFAULT_STRATEGY == "BFS":
        return [("BFS (FIFO, insert at end)", False, "BFS")]
    if KNOB_DEFAULT_STRATEGY == "DFS":
        return [("DFS (LIFO, insert at front)", True, "DFS")]
    if KNOB_DEFAULT_STRATEGY == "IDS":
        return [("IDS (iterative deepening, L03 sec 4.4)", True, "IDS")]
    if KNOB_DEFAULT_STRATEGY == "UCS":
        return [("UCS (priority queue by g(n), L03 sec 4.2)", False, "UCS")]
    return [
        ("DFS (LIFO, insert at front)", True, "DFS"),
        ("BFS (FIFO, insert at end)", False, "BFS"),
    ]


def run_exercise_1() -> None:
    """Exercise 1 - A..J tree, goal J, both strategies."""
    print("=" * 70)
    print("EXERCISE 1 - Tree search on the abstract A..J state space")
    print("=" * 70)
    searcher = Searcher(
        KNOB_EX1_INITIAL_STATE,
        KNOB_EX1_GOAL_STATE,
        state_space=StateSpace(KNOB_EX1_STATE_SPACE),
        goal_predicate=KNOB_EX1_GOAL_PREDICATE,
        # The handout's A..J graph is acyclic, so visited-tracking would be
        # a no-op AND would mask the literal "tree-search" semantics the
        # slides describe.  KNOB_EX1_TRACK_VISITED defaults to False; do
        # NOT remove that override for the handout's hand-trace to be
        # reproducible - see L03 sec 5.5.
        track_visited=KNOB_EX1_TRACK_VISITED,
        print_fringe_trace=KNOB_EX1_PRINT_FRINGE_TRACE,
    )
    for label, insert_as_first, tag in _strategies_to_run():
        print(
            f"\n--- {label} from {KNOB_EX1_INITIAL_STATE!r} to "
            f"{KNOB_EX1_GOAL_STATE!r} ---"
        )
        searcher.run(insert_as_first=insert_as_first, strategy=tag)


def run_exercise_2() -> None:
    """Exercise 2 - vacuum world with BFS (default) or both strategies."""
    print("\n" + "=" * 70)
    print("EXERCISE 2 - Vacuum world")
    print("=" * 70)

    # KNOB_EX2_STATE_SPACE_OVERRIDE wins if supplied (tested with `is not None`
    # so an intentionally-empty dict is honoured).
    if KNOB_EX2_STATE_SPACE_OVERRIDE is not None:
        space_dict = KNOB_EX2_STATE_SPACE_OVERRIDE
    else:
        space_dict = build_vacuum_state_space(KNOB_EX2_ROOMS, KNOB_EX2_STATUSES)

    # Choose the goal predicate:
    #   - explicit KNOB_EX2_GOAL_PREDICATE wins
    #   - if goal_state is None, fall back to "all rooms clean"
    #   - otherwise default to equality (handled by Searcher._is_goal)
    goal_predicate: Callable[[Any], bool] | None = KNOB_EX2_GOAL_PREDICATE
    if goal_predicate is None and KNOB_EX2_GOAL_STATE is None:
        goal_predicate = _vacuum_all_clean_goal(KNOB_EX2_STATUSES)

    searcher = Searcher(
        KNOB_EX2_INITIAL_STATE,
        KNOB_EX2_GOAL_STATE,
        state_space=StateSpace(space_dict),
        goal_predicate=goal_predicate,
        # Vacuum world has cycles (Left/Right are inverses); without
        # visited-tracking even BFS revisits states exponentially.
        track_visited=KNOB_EX2_TRACK_VISITED,
        print_fringe_trace=KNOB_EX2_PRINT_FRINGE_TRACE,
    )

    for label, insert_as_first, tag in _strategies_to_run():
        # Only BFS is asked for in the handout; the DFS run is included
        # when KNOB_DEFAULT_STRATEGY is None purely for the pedagogical
        # comparison.
        print(
            f"\n--- {label}: {KNOB_EX2_INITIAL_STATE} -> "
            f"{KNOB_EX2_GOAL_STATE or 'any all-clean'} ---"
        )
        searcher.run(insert_as_first=insert_as_first, strategy=tag)


def run_exercise_3() -> None:
    """Homework - farmer/wolf/goat/cabbage river crossing."""
    print("\n" + "=" * 70)
    print("HOMEWORK - Farmer/Wolf/Goat/Cabbage river crossing")
    print("=" * 70)

    item_count = len(KNOB_EX3_INITIAL_STATE)
    if KNOB_EX3_STATE_SPACE_OVERRIDE is not None:
        space_dict = KNOB_EX3_STATE_SPACE_OVERRIDE
    else:
        space_dict = build_river_state_space(
            KNOB_EX3_BANKS,
            KNOB_EX3_EAT_RULES,
            KNOB_EX3_PASSENGERS_PER_TRIP,
            item_count=item_count,
        )

    searcher = Searcher(
        KNOB_EX3_INITIAL_STATE,
        KNOB_EX3_GOAL_STATE,
        state_space=StateSpace(space_dict),
        goal_predicate=KNOB_EX3_GOAL_PREDICATE,
        # River puzzle is cyclic (ferry back and forth); cycle detection
        # is mandatory or DFS oscillates forever.
        track_visited=KNOB_EX3_TRACK_VISITED,
        print_fringe_trace=KNOB_EX3_PRINT_FRINGE_TRACE,
    )

    for label, insert_as_first, tag in _strategies_to_run():
        print(
            f"\n--- {label}: {KNOB_EX3_INITIAL_STATE} -> "
            f"{KNOB_EX3_GOAL_STATE} ---"
        )
        searcher.run(insert_as_first=insert_as_first, strategy=tag)


# ===========================================================================
#                              E N T R Y   P O I N T
# ===========================================================================


if __name__ == "__main__":
    if KNOB_RUN_EXERCISE_1:
        run_exercise_1()
    if KNOB_RUN_EXERCISE_2:
        run_exercise_2()
    if KNOB_RUN_EXERCISE_3:
        run_exercise_3()

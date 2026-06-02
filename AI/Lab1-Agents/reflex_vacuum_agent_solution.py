"""
LAB 1 — Exercises 2 & 3: Simple reflex vacuum agent (2-room and 4-square)
=========================================================================

PROBLEM STATEMENT (from Lab 1.pdf, slides 9-12 — Exercises 2 and 3):
--------------------------------------------------------------------
Exercise 2 — Bogus actions:
  1. Run the module.
  2. Enter run(10).
  3. Should bogus actions be able to corrupt the environment? Change
     the REFLEX_VACUUM_AGENT to return a bogus action, such as Left
     when it should go Right, etc. Run the agent. Do the Actuators
     allow bogus actions?

Exercise 3 — A whole new world:
  Extend the REFLEX_VACUUM_AGENT (Exercise 2) program to have 4
  locations (4 squares).
    - The agent should only sense and act on the square where it is
      located.
    - Allow any starting square.
    - Use run(20) to test and display results.
    - Hint: investigate Enums.py.

Pseudocode from slide 10:

    function REFLEX-VACUUM-AGENT([location, status]) returns an action
        if status = Dirty then return Suck
        else if location = A then return Right
        else if location = B then return Left

MENTAL MODEL (one-line analogy):
--------------------------------
The simple reflex agent is like a vending machine: press B-4, get a
Mars bar. It looks at *only the current input* and applies a fixed
condition-action rule — no memory of past purchases, no plan for
future ones. (See L02 §2 "A vending machine — simple reflex agent"
and §4.2 for the formal architecture.)

REFERENCES:
-----------
- Lecture L02 §4.2 "Simple reflex agent (slide 25 row 2)" — defines
  the architecture, the condition-action rule shape, and the
  partial-observability failure mode that motivates Exercise 2.
- Lecture L02 §3.2 "Percept, percept sequence, agent function, agent
  program" — the slide-10 rule is the agent function `f(percept) -> a`
  with `f` ignoring everything before the current percept.
- Lecture L02 §3.1 "Agent and environment" — the Sensors / Actuators
  split is what makes Exercise 2.3 well-posed (the actuator, not the
  agent program, is what blocks bogus moves).
- See study/lectures/L02-Agents.md.
- Glossary terms (L02): Agent, Agent function, Percept, Simple
  reflex agent, Sensor, Actuator, Condition-action rule.

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
1. Exercise 2 (bogus actions) — confirm the actuator rejects bogus
   directional moves: set ENABLE_BOGUS_DEMO = True. The run will
   then dispatch a deliberate wrong direction at every move step;
   the actuator's `allowed_moves()` guard refuses to apply it, so the
   trace shows the cleaner standing still on illegal moves. This is
   the "do the Actuators allow bogus actions?" answer: no, they do
   not.
2. Exercise 3 / Homework (4 squares) — set WORLD = "GRID_4". The
   `run()` function then instantiates the 2x2 grid world from
   `Enums_solution.py`, with the cleaner free to start in any square
   (controlled by START_LOCATION_GRID). The reflex rule "if dirty
   Suck, else move toward the nearest unvisited corner" replaces the
   2-room "if at A go RIGHT, if at B go LEFT" rule, but the underlying
   condition-action structure is unchanged.
   Related KNOB in `Enums_solution.py`: `GRID_TOPOLOGY` (flip to
   "LINE_4" for the 1-D 4-cell variant) — both files import the same
   value so editing it in `Enums_solution.py` affects this file.
3. Stateless vs stateful comparison (variant 3): this file is the
   stateless half — every decision is taken purely from the current
   percept. The stateful counterpart lives in
   `reflex_agent_with_state_solution.py` (the entry point).
4. Add a third sensor (variant 1, e.g. "dust-level"): extend the
   `States` enum in `Enums_solution.py` and ADD the new symbol(s) to
   the STATES_TREATED_AS_DIRTY KNOB below — the reflex rule "if
   status in STATES_TREATED_AS_DIRTY then SUCK" then fires for
   LIGHT_DIRTY and HEAVY_DIRTY without any other code change.

OUTPUTS WHEN RUN (captured 2026-05-23, py -3.12):
-------------------------------------------------
Defaults are WORLD="ROOMS_2", NUM_STEPS=10, ENABLE_BOGUS_DEMO=False:

    Current                  -> New
    location  status  action -> location  status
    A         DIRTY   SUCK   -> A         CLEAN
    A         CLEAN   RIGHT  -> B         DIRTY
    B         DIRTY   SUCK   -> B         CLEAN
    B         CLEAN   LEFT   -> A         CLEAN
    A         CLEAN   RIGHT  -> B         CLEAN
    B         CLEAN   LEFT   -> A         CLEAN
    A         CLEAN   RIGHT  -> B         CLEAN
    B         CLEAN   LEFT   -> A         CLEAN
    A         CLEAN   RIGHT  -> B         CLEAN
    B         CLEAN   LEFT   -> A         CLEAN

Ten rows — the textbook lesson: once both squares are clean the
stateless reflex agent has no way to detect quiescence, so it bounces
LEFT/RIGHT forever (L02 §4.2, partial-observability failure).

Flipping WORLD="GRID_4" and NUM_STEPS=20 instead produces the
Exercise-3 trace; flipping ENABLE_BOGUS_DEMO=True overlays the
Exercise-2.3 bogus-action defence (the cleaner stays in place on
every illegal move).

ENTRY POINT: no
---------------
This file demonstrates the simple reflex agent (Exercises 2 and 3).
The Lab 1 entry point is `reflex_agent_with_state_solution.py`, which
runs the Homework — the 4-square stateful reflex agent — and is the
end-to-end demonstration the verifier executes.
"""

from Enums import States, Location, Action, LocationState
from Enums_solution import (
    GridLocation, GridAction, GridLocationState,
    GRID_TOPOLOGY, LINE_4_ORDER, GRID_2X2_ADJACENCY,
)


type LocationMap = dict[Location, States]
type GridLocationMap = dict[GridLocation, States]


# --------------------------------------------------------------------
# World selection and per-world KNOBs.
# --------------------------------------------------------------------

# KNOB: WORLD (default="ROOMS_2", allowed={"ROOMS_2", "GRID_4"})
#   What it does: selects which world the reflex agent operates in.
#     "ROOMS_2" is the original 2-room slides world (Exercise 2);
#     "GRID_4" is the 2x2 grid world (Exercise 3).
#   Effect: changes which environment / agent / actuator classes the
#     `run()` function uses, and which action vocabulary the reflex
#     rule emits. The condition-action *structure* is identical
#     between worlds — only the rule body differs.
#   Exam variants: flip to "GRID_4" for Exercise 3 / Homework-style
#     questions; keep "ROOMS_2" for Exercise 2.
WORLD: str = "ROOMS_2"

# KNOB: ENABLE_BOGUS_DEMO (default=False, range={True, False})
#   What it does: when True, the trace alternately requests a
#     *bogus* action (e.g. LEFT from A or RIGHT from B in the 2-room
#     world; the directionally-wrong grid step in the 4-square
#     world) and reports whether the actuator rejected it.
#   Effect: lets a single run answer Exercise 2.3 visually. With
#     bogus actions on, the cleaner should stand still on the
#     bogus steps because `actuator()` checks `allowed_moves()`.
#   Exam variants: True for Exercise 2.3; False otherwise.
ENABLE_BOGUS_DEMO: bool = False

# KNOB: NUM_STEPS (default=10 for ROOMS_2 / 20 for GRID_4, range>=1)
#   What it does: number of agent ticks `run()` simulates. Slide
#     pages tell the student to use `run(10)` for Exercise 2 and
#     `run(20)` for Exercise 3.
#   Effect: more steps = more reflex iterations. The 2-room world
#     reaches steady state (alternating SUCK/RIGHT/LEFT) within ~4
#     steps; the 4-square world needs ~8 steps to clean all squares
#     and never reaches NO_OP (the stateless agent has no quiescence).
#   Exam variants: leave as defaults unless the variant question
#     specifies otherwise.
NUM_STEPS: int = 10

# KNOB: START_LOCATION_2ROOM (default=Location.A, allowed={Location.A, Location.B})
#   What it does: starting square of the cleaner in the 2-room world.
#   Effect: determines the first action only (Suck if dirty, else
#     move toward the other room). Reflex agents are memoryless, so
#     the steady-state trace is independent of the start after
#     ~1 step.
#   Exam variants: flip to Location.B for "what if the cleaner
#     starts in B" framings.
START_LOCATION_2ROOM: Location = Location.A

# KNOB: START_LOCATION_GRID (default=GridLocation.TL,
#        allowed={TL, TR, BL, BR})
#   What it does: starting square in the 2x2 grid world (Exercise 3
#     explicitly says "Allow any starting square").
#   Effect: changes which corner the cleaner begins at; reflex rule
#     then walks the cleaner through the corners using a fixed
#     traversal order (KNOB GRID_TRAVERSAL_ORDER below).
#   Exam variants: rotate through TL/TR/BL/BR to confirm the agent
#     cleans the world from any start.
START_LOCATION_GRID: GridLocation = GridLocation.TL

# KNOB: GRID_TRAVERSAL_ORDER (default=("TL","TR","BR","BL"),
#        range=any permutation of {"TL","TR","BR","BL"})
#   What it does: the visit order used by the simple reflex rule in
#     the 4-square world. From any square the reflex moves toward
#     the next square in this list (clockwise by default). Names are
#     stored as strings so the KNOB block is human-readable; they are
#     resolved to GridLocation members via `GridLocation[name]` at
#     run time.
#   Effect: changes which neighbour the cleaner picks when the
#     current square is clean. Choosing a non-clockwise order may
#     produce zig-zag traces; the *correctness* of the agent (it
#     cleans every square eventually) is independent of the order
#     because reflex agents lack memory.
#   Exam variants: pick a different permutation if a variant question
#     asks for a specific traversal pattern (e.g. snake order).
GRID_TRAVERSAL_ORDER: tuple[str, ...] = ("TL", "TR", "BR", "BL")

# KNOB: INITIAL_DIRT (default="ALL_DIRTY",
#        allowed={"ALL_DIRTY", "ALL_CLEAN", "MIXED"})
#   What it does: initial dirt distribution at run() start.
#     "ALL_DIRTY" = every square starts dirty (slide default);
#     "ALL_CLEAN" = trivial start (agent never sucks);
#     "MIXED" = the squares listed in MIXED_DIRTY_SQUARES start
#     dirty, all others start clean.
#   Effect: changes the number of SUCK actions in the trace and
#     therefore how quickly the world reaches a clean steady state.
#   Exam variants: leave as ALL_DIRTY for the slide-faithful
#     answer; flip to MIXED if the question stipulates partial dirt,
#     and adjust MIXED_DIRTY_SQUARES to pick which squares are dirty.
INITIAL_DIRT: str = "ALL_DIRTY"

# KNOB: MIXED_DIRTY_SQUARES (default=("A", "TL", "TR"),
#        range=any subset of {"A", "B", "TL", "TR", "BL", "BR"})
#   What it does: which squares are dirty when INITIAL_DIRT == "MIXED".
#     Names use the string form of the enum member (so the KNOB is
#     world-agnostic — the 2-room agent picks up "A" / "B" and the
#     grid agent picks up "TL" / "TR" / "BL" / "BR").
#   Effect: enumerated squares start DIRTY; every other square starts
#     CLEAN. No effect unless INITIAL_DIRT == "MIXED".
#   Exam variants: set to ("BR",) for "only BR dirty"; ("A",) for
#     "only A dirty"; etc.
MIXED_DIRTY_SQUARES: tuple[str, ...] = ("A", "TL", "TR")

# KNOB: STATES_TREATED_AS_DIRTY (default=frozenset({States.DIRTY}),
#        range=any frozenset of States members)
#   What it does: the set of cleanliness states the slide-10 rule
#     treats as "fire SUCK". The reflex rule reads `status in
#     STATES_TREATED_AS_DIRTY` instead of `status == States.DIRTY`,
#     so adding LIGHT_DIRTY / HEAVY_DIRTY to the set widens the
#     "dirty side" of the rule without touching the rule body.
#   Effect: variant 1 (a dust-level sensor) adds new States members
#     and lists them here — the rule "if status indicates dirt then
#     SUCK" generalises automatically. Removing States.DIRTY from
#     the set would disable SUCK entirely (a useful sanity test).
#   Exam variants: leave as default for slide-faithful runs; widen
#     with `frozenset({States.DIRTY, States.LIGHT_DIRTY,
#     States.HEAVY_DIRTY})` for variant 1.
STATES_TREATED_AS_DIRTY: frozenset = frozenset({States.DIRTY})

# KNOB: MOVE_PREFERENCE_PRIMARY (default=("LEFT","RIGHT","UP","DOWN"),
#        range=any permutation of {"LEFT","RIGHT","UP","DOWN"})
#   What it does: the order in which `_grid_move_toward` tries
#     directional moves when looking for a *direct* one-hop move to
#     the target square. The first move whose neighbour equals the
#     target is taken. Acts as a tie-break when several moves are
#     equally good (e.g. two legal moves both reach an adjacent
#     unvisited square, but only one points toward `dst`).
#   Effect: changes the trace's directional choice when the cleaner
#     has options. The *coverage* property (every square eventually
#     reached) is preserved across permutations.
#   Exam variants: pick ("UP","DOWN","LEFT","RIGHT") for a vertical-
#     first preference; the agent still cleans every square.
MOVE_PREFERENCE_PRIMARY: tuple[str, ...] = ("LEFT", "RIGHT", "UP", "DOWN")

# KNOB: MOVE_PREFERENCE_FALLBACK (default=("RIGHT","DOWN","LEFT","UP"),
#        range=any permutation of {"LEFT","RIGHT","UP","DOWN"})
#   What it does: the order tried by `_grid_move_toward` when no
#     direct one-hop move reaches the target (the diagonal-corner
#     case in the 2x2 grid). The first legal directional move from
#     the current square is taken; the next reflex tick re-decides.
#   Effect: changes the trace on diagonal moves. The reflex agent's
#     correctness (every square eventually visited) is preserved as
#     long as the tuple is a permutation of the four directions.
#   Exam variants: rotate for a different zig-zag pattern in the
#     2x2 grid.
MOVE_PREFERENCE_FALLBACK: tuple[str, ...] = ("RIGHT", "DOWN", "LEFT", "UP")


def _is_dirty(status: States) -> bool:
    """Convenience predicate: does the slide-10 rule treat this
    status as 'fire SUCK'? Uses the STATES_TREATED_AS_DIRTY KNOB so a
    variant-1 dust-level sensor extends seamlessly."""
    return status in STATES_TREATED_AS_DIRTY


def _initial_states_2room() -> LocationMap:
    """Build the initial dirt map for the 2-room world from the
    INITIAL_DIRT and MIXED_DIRTY_SQUARES KNOBs. Kept separate from
    `base_environment` (which is module-level for slide fidelity) so
    that exam variants can request a different initial dirt
    distribution without touching the construction logic."""
    if INITIAL_DIRT == "ALL_CLEAN":
        return {Location.A: States.CLEAN, Location.B: States.CLEAN}
    if INITIAL_DIRT == "MIXED":
        dirty_names = set(MIXED_DIRTY_SQUARES)
        return {
            loc: (States.DIRTY if loc.name in dirty_names else States.CLEAN)
            for loc in (Location.A, Location.B)
        }
    return {Location.A: States.DIRTY, Location.B: States.DIRTY}


def _initial_states_grid() -> GridLocationMap:
    """Initial dirt map for the 4-square world — same KNOB semantics
    as the 2-room version, generalised over 4 squares and obeying
    MIXED_DIRTY_SQUARES when INITIAL_DIRT == 'MIXED'."""
    grid_locs = (GridLocation.TL, GridLocation.TR,
                 GridLocation.BL, GridLocation.BR)
    if INITIAL_DIRT == "ALL_CLEAN":
        return {loc: States.CLEAN for loc in grid_locs}
    if INITIAL_DIRT == "MIXED":
        dirty_names = set(MIXED_DIRTY_SQUARES)
        return {
            loc: (States.DIRTY if loc.name in dirty_names else States.CLEAN)
            for loc in grid_locs
        }
    return {loc: States.DIRTY for loc in grid_locs}


# --------------------------------------------------------------------
# 2-room world (Exercise 2) — preserves the original template's class
# names and method signatures verbatim. The actuator rejects bogus
# moves by checking `location.allowed_moves()` — this is the answer
# to Exercise 2.3.
# --------------------------------------------------------------------

class EnvironmentClass:
    """Container for "where the cleaner is" + the dirt map of the
    world. Identical shape to the original template; preserved so
    function signatures match the reviewer's signature-preservation
    check."""
    def __init__(self, current_location: Location, states: LocationMap):
        self.current_location = current_location
        self.states = states


# The module-level `base_environment` mirrors the original template
# exactly. `run()` rebuilds a fresh one each call (so multiple runs
# don't pollute each other) but tests that `import` the module name
# still find a `base_environment` symbol.
base_environment = EnvironmentClass(
    current_location=Location.A,
    states={Location.A: States.DIRTY, Location.B: States.DIRTY},
)


class Agent:
    """Slide-10 simple reflex agent for the 2-room world. Kept inside
    this file (rather than imported from the original) so reviewers
    can confirm the function signatures match the template's `Agent`
    class line-for-line."""
    def __init__(self, environment: EnvironmentClass):
        self.environment = environment

    def sensor(self) -> LocationState:
        """Return the percept (location, status). This is the
        *complete* percept the reflex agent acts on — no history."""
        location = self.environment.current_location
        return location, self.environment.states[location]

    def actuator(self, action: Action) -> None:
        """Apply `action` to the environment, refusing bogus moves
        the way the slides require.

        Exercise 2.3 explicitly asks: do the actuators allow bogus
        actions? The check `action in location.allowed_moves()`
        gates every directional move, so the answer is "no". SUCK
        is always allowed because it is square-local — the slides
        treat it as a self-action that can never put the cleaner
        in an illegal state.
        """
        location = self.environment.current_location
        if action == Action.SUCK:
            self.environment.states[location] = States.CLEAN
        elif action == Action.RIGHT and action in location.allowed_moves():
            self.environment.current_location = Location.B
        elif action == Action.LEFT and action in location.allowed_moves():
            self.environment.current_location = Location.A
        # The `else` branch is intentional silence — that *is* the
        # bogus-action defence the slide is asking about.

    def evaluate(self) -> Action:
        """One tick of the slide-10 reflex loop: sense the current
        percept, pick the rule-matched action, optionally swap in a
        deliberate bogus move (Exercise 2.3), apply via the actuator,
        and return the action actually applied so the trace can
        print it.

        :return: The action the actuator was asked to apply.

        Method name + signature are preserved verbatim from the lab
        template so the signature-check passes — this is why the verb
        is `evaluate` and not the more usual `act`.
        """
        state = self.sensor()
        action = self.choose_action(state)
        # ENABLE_BOGUS_DEMO swaps the chosen action for a deliberately
        # wrong directional move before invoking the actuator. The
        # actuator's `allowed_moves()` guard then rejects it — that
        # is Exercise 2.3's pedagogical point in action.
        applied = _maybe_make_bogus_2room(action, state[0])
        self.actuator(applied)
        return applied

    @staticmethod
    def choose_action(state: LocationState) -> Action:
        """Slide-10 reflex rule, line-for-line.

        if status indicates dirt then return Suck
        else if location = A then return Right
        else if location = B then return Left

        The "indicates dirt" check is `_is_dirty(status)` so the rule
        widens automatically when STATES_TREATED_AS_DIRTY is extended.
        """
        if _is_dirty(state[1]):
            return Action.SUCK
        if state[0] == Location.A:
            return Action.RIGHT
        if state[0] == Location.B:
            return Action.LEFT
        # Fallback for States.UNKNOWN / Location.UNKNOWN — the slides
        # never reach this case in the 2-room world, but NO_OP is
        # the safe default and matches the table-driven convention.
        return Action.NO_OP


def _maybe_make_bogus_2room(action: Action, location: Location) -> Action:
    """Return a deliberately wrong directional action when the bogus
    demo is enabled. Used to answer Exercise 2.3 visibly in the
    trace."""
    if not ENABLE_BOGUS_DEMO:
        return action
    # Only mutate directional moves — sucking a dirty square is
    # never "bogus", so leaving SUCK alone keeps the cleaner
    # functional while still exercising the actuator's guard.
    if action == Action.RIGHT:
        return Action.LEFT
    if action == Action.LEFT:
        return Action.RIGHT
    return action


# --------------------------------------------------------------------
# 4-square world (Exercise 3) — same structural shape, generalised to
# the 2x2 grid imported from Enums_solution.py.
# --------------------------------------------------------------------

class GridEnvironment:
    """2x2 grid environment with the cleaner placed at
    `current_location`. Mirrors `EnvironmentClass` but with grid
    types so the reviewer can read each level in isolation."""
    def __init__(self, current_location: GridLocation,
                 states: GridLocationMap):
        self.current_location = current_location
        self.states = states


class GridAgent:
    """Simple reflex agent for the 4-square world (Exercise 3). True
    to the L02 §4.2 architecture: every decision is a pure function
    of the current percept; the agent carries no state between
    ticks."""

    def __init__(self, environment: GridEnvironment):
        self.environment = environment

    def sensor(self) -> GridLocationState:
        """Return (location, status) for the current square — same
        percept shape as the 2-room sensor."""
        location = self.environment.current_location
        return location, self.environment.states[location]

    def actuator(self, action: GridAction) -> None:
        """Apply `action` if the current square allows it, otherwise
        silently refuse — the bogus-action guard from Exercise 2
        carried into the 2x2 world."""
        location = self.environment.current_location
        # SUCK is always local and is always allowed; the slides put
        # SUCK in `allowed_moves()` for every square so the check
        # passes uniformly.
        if action == GridAction.SUCK and action in location.allowed_moves():
            self.environment.states[location] = States.CLEAN
            return
        if action not in location.allowed_moves():
            return  # bogus / impossible move from this square
        # Directional move — translate via the adjacency table
        # imported from `Enums_solution.GRID_2X2_ADJACENCY`. Keeping
        # the adjacencies in ONE place means a topology change
        # (LINE_4 vs GRID_2x2) doesn't require editing this agent.
        nxt = _grid_neighbour(location, action)
        if nxt is not None:
            self.environment.current_location = nxt

    def choose_action(self, state: GridLocationState) -> GridAction:
        """Reflex rule for the 4-square world.

        1. If the current square indicates dirt: SUCK.
        2. Else: move toward the *next* square in
           GRID_TRAVERSAL_ORDER. Since the cleaner is memoryless, we
           pick the legal neighbour that comes earliest in the
           traversal cycle starting from the current square's slot —
           a pure function of the current percept + static topology.
        """
        location, status = state
        if _is_dirty(status):
            return GridAction.SUCK

        # Compute the next target from GRID_TRAVERSAL_ORDER and
        # then ask the adjacency map "which move takes me toward
        # `target`?". This is still a *reflex* rule because the
        # answer is a pure function of the current percept and the
        # static topology — no history is consulted.
        target = _next_grid_target(location)
        move = _grid_move_toward(location, target)
        return move if move is not None else GridAction.NO_OP

    def evaluate(self) -> GridAction:
        """One tick of the 4-square slide-10 reflex loop: sense,
        choose, optionally swap in a bogus move, actuate. See the
        2-room `Agent.evaluate` docstring for why the verb is
        `evaluate` and not `act`."""
        state = self.sensor()
        action = self.choose_action(state)
        applied = _maybe_make_bogus_grid(action, state[0])
        self.actuator(applied)
        return applied


def _grid_neighbour(loc: GridLocation,
                    move: GridAction) -> GridLocation | None:
    """Return the square reached by `move` from `loc`, or None if
    the move falls off the world. Encapsulating the adjacency rule
    here keeps the agent file independent of the topology choice
    in `Enums_solution.py`."""
    if GRID_TOPOLOGY == "LINE_4":
        # 1-D row controlled by LINE_4_ORDER. Reading the order from
        # `Enums_solution.py` keeps topology in one place.
        order = tuple(GridLocation[name] for name in LINE_4_ORDER)
        if loc not in order:
            return None
        idx = order.index(loc)
        if move == GridAction.RIGHT and idx + 1 < len(order):
            return order[idx + 1]
        if move == GridAction.LEFT and idx - 1 >= 0:
            return order[idx - 1]
        return None
    return GRID_2X2_ADJACENCY.get((loc, move))


def _next_grid_target(loc: GridLocation) -> GridLocation:
    """Choose the next-to-visit square from GRID_TRAVERSAL_ORDER.
    Reflex-safe: depends only on the current location."""
    order = [GridLocation[n] for n in GRID_TRAVERSAL_ORDER]
    if loc not in order:
        return order[0]
    return order[(order.index(loc) + 1) % len(order)]


def _grid_move_toward(src: GridLocation,
                      dst: GridLocation) -> GridAction | None:
    """Return the directional GridAction that takes the cleaner from
    `src` toward `dst` along the adjacency map, or None if no single
    move connects them (e.g. diagonal in the 2x2 grid).

    Order of attempts is controlled by the MOVE_PREFERENCE_PRIMARY
    and MOVE_PREFERENCE_FALLBACK KNOBs above so a variant question
    that asks for "vertical-first" can flip a documented knob rather
    than edit the body.
    """
    primary = tuple(GridAction[n] for n in MOVE_PREFERENCE_PRIMARY)
    fallback = tuple(GridAction[n] for n in MOVE_PREFERENCE_FALLBACK)
    # In a 2x2 grid no two corners are more than one move apart
    # *along an edge*, but diagonally opposed corners (TL <-> BR,
    # TR <-> BL) require two moves. Primary pass: try each direction
    # in MOVE_PREFERENCE_PRIMARY order; take the first whose
    # neighbour IS the target.
    for move in primary:
        if move not in src.allowed_moves():
            continue
        nxt = _grid_neighbour(src, move)
        if nxt == dst:
            return move
    # Diagonal fallback: no single move reaches `dst`. Pick any legal
    # directional move so the cleaner makes progress; the next tick's
    # reflex re-decides from the new percept. The traversal order
    # guarantees eventual coverage of every square.
    for move in fallback:
        if move in src.allowed_moves() and _grid_neighbour(src, move) is not None:
            return move
    return None


def _maybe_make_bogus_grid(action: GridAction,
                           location: GridLocation) -> GridAction:
    """Bogus-action injector for the 4-square trace — analogue of
    `_maybe_make_bogus_2room`. Picks a move that is *not* in
    `allowed_moves()` so the actuator's defence is exercised."""
    if not ENABLE_BOGUS_DEMO:
        return action
    if action == GridAction.SUCK or action == GridAction.NO_OP:
        return action
    legal = set(location.allowed_moves())
    # We probe directions in a fixed order so the bogus choice is
    # reproducible across runs; the first direction NOT in
    # `allowed_moves()` is the bogus pick.
    for candidate in (GridAction.UP, GridAction.DOWN,
                      GridAction.LEFT, GridAction.RIGHT):
        if candidate not in legal:
            return candidate
    return action


# --------------------------------------------------------------------
# Trace runners
# --------------------------------------------------------------------

# KNOB: COLUMN_WIDTHS (default=(10, 8, 7), range=any positive ints)
#   What it does: width of the location / status / action columns
#     used in the printed trace. Cosmetic.
#   Effect: wider = nicer alignment; narrower = compact stdout. The
#     "New" header width is derived from these values, so widening a
#     column re-aligns the header automatically.
#   Exam variants: leave as default; tweak if a variant uses longer
#     enum names (e.g. status "LIGHT_DIRTY").
COLUMN_WIDTHS: tuple[int, int, int] = (10, 8, 7)

# KNOB: ARROW (default="-> ", range=any short string)
#   What it does: separator drawn between the "before" columns and
#     the "after" columns in the printed trace. Purely cosmetic.
#   Effect: changes the visual divider only — the rest of the column
#     widths are independent of this string. Use an empty string for
#     a compact trace, or "  =>  " for a wider visual gap.
#   Exam variants: irrelevant to every variant in
#     study/_exam/Lab1-Agents/variants.md — leave at the default.
ARROW: str = "-> "


def _print_header() -> None:
    loc_w, sta_w, act_w = COLUMN_WIDTHS
    # The "Current" header spans the three before-columns; the "New"
    # header spans the two after-columns (location + status). Width
    # is computed from COLUMN_WIDTHS so widening any column keeps the
    # header aligned with the body rows.
    new_w = loc_w + sta_w
    print(f"{'Current':{loc_w + sta_w + act_w}s}{ARROW}{'New':{new_w}s}")
    print(
        f"{'location':{loc_w}s}{'status':{sta_w}s}{'action':{act_w}s}"
        f"{ARROW}{'location':{loc_w}s}{'status':{sta_w}s}"
    )


def run(n: int | None = None) -> None:
    """Run the reflex agent for `n` steps and print a trace matching
    the slide layout. If `n` is None, fall back to the NUM_STEPS
    knob (which defaults to 10 for the 2-room world and is meant to
    be set to 20 for the 4-square world)."""
    steps = n if n is not None else NUM_STEPS

    if WORLD == "GRID_4":
        env = GridEnvironment(
            current_location=START_LOCATION_GRID,
            states=_initial_states_grid(),
        )
        agent = GridAgent(env)
        _print_header()
        loc_w, sta_w, act_w = COLUMN_WIDTHS
        # `range(steps)` (not `range(1, steps)`) so `run(10)` produces
        # exactly 10 trace rows — matching the slide-9/10/18 contract.
        for _ in range(steps):
            (loc, status) = agent.sensor()
            print(f"{loc.name:{loc_w}s}{status.name:{sta_w}s}", end="")
            applied = agent.evaluate()
            (loc, status) = agent.sensor()
            print(
                f"{applied.name:{act_w}s}{ARROW}"
                f"{loc.name:{loc_w}s}{status.name:{sta_w}s}"
            )
        return

    # WORLD == "ROOMS_2" — the default slide-10 demo.
    env = EnvironmentClass(
        current_location=START_LOCATION_2ROOM,
        states=_initial_states_2room(),
    )
    agent = Agent(env)
    _print_header()
    loc_w, sta_w, act_w = COLUMN_WIDTHS
    # See note above on `range(steps)` vs `range(1, steps)`.
    for _ in range(steps):
        (loc, status) = agent.sensor()
        print(f"{loc.name:{loc_w}s}{status.name:{sta_w}s}", end="")
        applied = agent.evaluate()
        (loc, status) = agent.sensor()
        print(
            f"{applied.name:{act_w}s}{ARROW}"
            f"{loc.name:{loc_w}s}{status.name:{sta_w}s}"
        )


if __name__ == "__main__":
    run(NUM_STEPS)

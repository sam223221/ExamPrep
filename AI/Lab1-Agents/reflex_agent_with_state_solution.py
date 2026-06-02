"""
LAB 1 — Homework: Reflex agent with state, 4-square world (ENTRY POINT)
=======================================================================

PROBLEM STATEMENT (from Lab 1.pdf, slides 14-18 — Homework "Remembering the whole world"):
------------------------------------------------------------------------------------------
Reflex agent with state (slide 14):
  - The reflex agent only responded to current percepts; no history or
    knowledge.
  - Model-based reflex agents:
      - Maintain internal state that depends upon percept history.
      - Agent has a model of how the world works.
      - The model requires two types of information to update:
          - How the environment evolves independent of the agent
            (e.g., a Clean square stays clean).
          - How the agent's action affects the environment
            (e.g., Suck cleans the square).

Reflex agent with state (slide 15):
  - Refer to reflex_agent_with_state.py
  - Model - used to update history
      - History initially empty:  model = {A: Unknown, B: Unknown}
      - Model only used to change state when A == B == 'Clean':
            if model[A] == model[B] == 'Clean': action = NO_OP

Pseudocode (slide 16):

    function REFLEX-AGENT-WITH-STATE(percept) returns an action
        static: state, a description of the current world state
                rules, a sequence, a set of condition-action rules
                action, the most recent action, initially none
        state = UPDATE-STATE(state, action, percept)
        rule  = RULE-MATCH(state, rules)
        action = RULE-ACTION[rule]
        return action

Homework (slide 18, "Remembering the whole world"):
  Extend the REFLEX_AGENT_WITH_STATE program to have 4 locations
  (4 squares).
    - The agent should only sense and act on the square where it is
      located.
    - Allow any starting square.
    - Use run(20) to test and display results.

MENTAL MODEL (one-line analogy):
--------------------------------
The model-based reflex agent is like a driver in fog who keeps an
internal model of what is out there based on the last moment they
could see — every tick they update the picture with what they just
sensed and act on the updated picture, rather than on raw percepts
alone. (See L02 §2 "A driver in fog — model-based reflex agent" and
§4.3 for the formal architecture.) Equivalently for the vacuum world:
a maid with a checklist on a clipboard — same idea, narrower domain.

REFERENCES:
-----------
- Lecture L02 §4.3 "Model-based reflex agent (slide 25 row 3 —
  'Agents with memory')" — defines the architecture, the
  UPDATE-STATE / RULE-MATCH split, and the partial-observability
  failure of the simple reflex agent this one fixes.
- Lecture L02 §3.2 "Percept, percept sequence, agent function,
  agent program" — the state variable is the agent program's
  internal compression of the percept sequence.
- Lecture L02 §3.6 "Environment types" — quiescence (slide-15's
  `NO_OP` rule) is meaningful only because the vacuum world is
  *episodic-once-clean* (no new dirt arrives).
- See study/lectures/L02-Agents.md.
- Glossary terms (L02): Model-based reflex agent, Internal state,
  Update function, Rule matching, Percept sequence.

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
1. Homework default (4 squares, any start) — set WORLD = "GRID_4"
   and START_LOCATION_GRID to whichever corner you want. The
   `run()` traces 20 ticks; the agent terminates by emitting NO_OP
   once every modelled square is CLEAN (slide 15 rule).
2. Compare stateless vs stateful (variant 3 in
   study/_exam/Lab1-Agents/variants.md): leave WORLD = "GRID_4" and
   set AGENT_VARIANT = "STATELESS" to run the simple reflex
   counterpart from `reflex_vacuum_agent_solution.py`, or
   "STATEFUL" to run this file's agent. The trace columns are the
   same so the two are directly comparable. KNOBs that affect the
   stateless run (e.g. INITIAL_DIRT, START_LOCATION_GRID) are
   propagated via the delegation in `run()` so they do not need to
   be edited in two files.
3. Extend to 3 rooms in a line (variant 2): set WORLD = "GRID_4"
   AND `GRID_TOPOLOGY = "LINE_4"` in `Enums_solution.py` — the
   topology knob already collapses the 2x2 to a row.
   Related KNOB in `Enums_solution.py`: `LINE_4_ORDER` controls the
   row order (default TL → TR → BL → BR).
4. Add a third sensor (variant 1, dust-level): extend the `States`
   enum and add the new symbol(s) to STATES_TREATED_AS_DIRTY in
   `reflex_vacuum_agent_solution.py`. The Rule-1 SUCK trigger here
   reads `_is_dirty(...)` via that same KNOB, so widening the dirty
   side propagates automatically.
5. Run for a different number of ticks: set NUM_STEPS. Slide 18
   prescribes 20 for the Homework demo.

OUTPUTS WHEN RUN (captured 2026-05-23, py -3.12):
-------------------------------------------------
Stateful homework trace, 4 squares, start = TL, 20 ticks (defaults):

    Current                  -> New
    location  status  action -> location  status
    TL        DIRTY   SUCK   -> TL        CLEAN
    TL        CLEAN   RIGHT  -> TR        DIRTY
    TR        DIRTY   SUCK   -> TR        CLEAN
    TR        CLEAN   DOWN   -> BR        DIRTY
    BR        DIRTY   SUCK   -> BR        CLEAN
    BR        CLEAN   LEFT   -> BL        DIRTY
    BL        DIRTY   SUCK   -> BL        CLEAN
    BL        CLEAN   NO_OP  -> BL        CLEAN
    BL        CLEAN   NO_OP  -> BL        CLEAN
    ... (remaining ticks all NO_OP — every modelled square is CLEAN)

20 rows total. The first 7 ticks alternate SUCK + directional moves
to clean every corner; from tick 8 onward Rule 2 (slide-15
quiescence: every modelled square is CLEAN) fires NO_OP forever.

ENTRY POINT: yes
----------------
This file is the Lab 1 entry point because the Homework subsumes
every concept in the lab: 4-square environment, stateful reflex
rules, condition-action structure, actuator-level bogus-action
guarding. Run with: `py -3.12 reflex_agent_with_state_solution.py`.
"""

from Enums import States, Location, Action, LocationState
from Enums_solution import (
    GridLocation, GridAction, GridLocationState,
    GRID_TOPOLOGY, LINE_4_ORDER, GRID_2X2_ADJACENCY,
)
# Stateful file shares the "dirty-side widening" and move-preference
# KNOBs with the stateless agent — imported here so a variant question
# only ever flips one knob.
from reflex_vacuum_agent_solution import (
    STATES_TREATED_AS_DIRTY, MOVE_PREFERENCE_PRIMARY,
    MOVE_PREFERENCE_FALLBACK, _is_dirty,
)


type LocationMap = dict[Location, States]
type GridLocationMap = dict[GridLocation, States]


# --------------------------------------------------------------------
# World / variant knobs
# --------------------------------------------------------------------

# KNOB: WORLD (default="GRID_4", allowed={"ROOMS_2", "GRID_4"})
#   What it does: selects which world the stateful agent operates in.
#     "ROOMS_2" runs slide 16's original 2-room demo; "GRID_4" runs
#     the Homework's 4-square (2x2 grid) demo.
#   Effect: chooses which agent class + environment class `run()`
#     instantiates and which action vocabulary the trace prints.
#   Exam variants: default to "GRID_4" for the Homework. Set to
#     "ROOMS_2" to reproduce slide 16 exactly.
WORLD: str = "GRID_4"

# KNOB: AGENT_VARIANT (default="STATEFUL", allowed={"STATEFUL", "STATELESS"})
#   What it does: chooses between the stateful (slide 16) agent and
#     the stateless (slide 10) reflex agent. The stateless option
#     delegates to `reflex_vacuum_agent_solution.run()` so the user
#     can side-by-side compare the two in one entry-point file.
#   Effect: with STATEFUL the agent reaches a quiescent NO_OP state
#     once every square is modelled CLEAN; with STATELESS the agent
#     keeps bouncing forever because it has no memory.
#     Delegation also propagates the *world-shaping* KNOBs (WORLD,
#     START_LOCATION_*, NUM_STEPS, INITIAL_DIRT) into the stateless
#     module via attribute writes before invoking its `run()`.
#   Exam variants: flip to STATELESS for variant 3 (stateless vs
#     stateful comparison).
AGENT_VARIANT: str = "STATEFUL"

# KNOB: NUM_STEPS (default=20, range>=1)
#   What it does: number of agent ticks `run()` simulates. Slide 18
#     stipulates `run(20)` for the Homework demo.
#   Effect: more steps = longer trace. After the agent reaches the
#     quiescent state (all modelled squares CLEAN), additional ticks
#     emit only NO_OP.
#   Exam variants: bump if a variant asks for longer-horizon
#     behaviour; lower (e.g. 10) to match the 2-room slide demo.
NUM_STEPS: int = 20

# KNOB: START_LOCATION_2ROOM (default=Location.A,
#        allowed={Location.A, Location.B})
#   What it does: starting square in the 2-room world.
#   Effect: first action only. Stateful agent then traverses both
#     squares and stops at NO_OP once both are clean.
#   Exam variants: flip to B for "what if it starts in B".
START_LOCATION_2ROOM: Location = Location.A

# KNOB: START_LOCATION_GRID (default=GridLocation.TL,
#        allowed={GridLocation.TL, TR, BL, BR})
#   What it does: starting square in the 4-square world. Slide 18
#     explicitly says "Allow any starting square" — this knob is
#     how the Homework's "any" requirement is exercised.
#   Effect: the cleaner's traversal order rotates to start at the
#     chosen corner; the steady state (every square clean, then
#     NO_OP) is reached in the same number of moves regardless of
#     start (<= 8 ticks for a 4-square 2x2 grid).
#   Exam variants: cycle through TL/TR/BL/BR to confirm
#     start-independence.
START_LOCATION_GRID: GridLocation = GridLocation.TL

# KNOB: GRID_TRAVERSAL_ORDER (default=("TL","TR","BR","BL"),
#        range=any permutation of {"TL","TR","BR","BL"})
#   What it does: clockwise visit order used by the stateful rule
#     when picking the next-to-visit square. Different from the
#     stateless agent's order in that the stateful agent *skips*
#     squares it has already modelled as CLEAN.
#   Effect: alters the traversal pattern; correctness (every square
#     eventually cleaned) is preserved as long as every square
#     appears in the tuple exactly once.
#   Exam variants: switch to a snake order ("TL","TR","BL","BR")
#     or a column order if a variant question demands it.
GRID_TRAVERSAL_ORDER: tuple[str, ...] = ("TL", "TR", "BR", "BL")

# KNOB: INITIAL_DIRT (default="ALL_DIRTY",
#        allowed={"ALL_DIRTY", "ALL_CLEAN", "MIXED"})
#   What it does: initial dirt distribution. Same semantics as in
#     reflex_vacuum_agent_solution.py; duplicated here so each
#     entry-point file is self-contained. When INITIAL_DIRT ==
#     "MIXED" the set of dirty squares is controlled by
#     MIXED_DIRTY_SQUARES below.
#   Effect: changes the number of SUCK ticks before NO_OP onset.
#   Exam variants: leave ALL_DIRTY for the Homework default.
INITIAL_DIRT: str = "ALL_DIRTY"

# KNOB: MIXED_DIRTY_SQUARES (default=("A","TL","TR"),
#        range=any subset of {"A","B","TL","TR","BL","BR"})
#   What it does: which squares are dirty when INITIAL_DIRT == "MIXED".
#     Mirrors the same-named KNOB in the stateless agent — listing
#     it here keeps this entry-point file self-contained.
#   Effect: enumerated squares start DIRTY; every other square
#     starts CLEAN. No effect unless INITIAL_DIRT == "MIXED".
#   Exam variants: ("BR",) for "only BR dirty"; ("A",) for the
#     2-room "only A dirty" framing; etc.
MIXED_DIRTY_SQUARES: tuple[str, ...] = ("A", "TL", "TR")


# --------------------------------------------------------------------
# 2-room world (slide 16) — preserves the original template's class
# names and method signatures verbatim.
# --------------------------------------------------------------------

class EnvironmentClass:
    """Container for "where the cleaner is" + the dirt map of the
    world. Identical shape to the original template; preserved so
    function signatures match the reviewer's signature-preservation
    check."""
    def __init__(self, current_location: Location, states: LocationMap):
        self.current_location = current_location
        self.states = states


# Slide 15 demo environment, module-level so it matches the original
# template's symbol layout.
base_environment = EnvironmentClass(
    current_location=Location.A,
    states={Location.A: States.DIRTY, Location.B: States.DIRTY},
)


class StatefulReflexAgent:
    """Slide-16 reflex agent with state, 2-room world.

    The "state" is the agent's *model* of the world: a dict from
    location to its last-seen dirt status (slide 15). UPDATE-STATE
    *writes* to the model every tick; the model is *consulted for
    the action choice* only when the current square is clean — at
    that point Rule 2 (slide-15 quiescence) reads the whole model
    to decide between "move on" and "stop forever". Rule 1 (SUCK on
    dirty) and Rule 3 (move toward the other room) act on the
    current percept alone. The combination keeps this an L02 §4.3
    *model-based reflex agent* rather than a planning agent.
    """

    def __init__(self):
        # `model` is the persistent state — initially the agent has
        # never seen either square, so both entries are UNKNOWN.
        # This is exactly the dictionary on slide 15.
        self.model: LocationMap = {
            Location.A: States.UNKNOWN,
            Location.B: States.UNKNOWN,
        }
        # `state` mirrors the slide-16 pseudocode's static `state`
        # variable: the most recent UPDATE-STATE result.
        self.state: LocationState = (Location.UNKNOWN, States.UNKNOWN)
        # `last_action` is the slide-16 static `action` variable.
        # Kept for completeness even though the 2-room rule does
        # not consult it directly.
        self.last_action: Action = Action.NO_OP

    def match_rule(self) -> Action:
        """RULE-MATCH from slide 16.

        Rules (slide 14-15):
          1. If current square indicates dirt: SUCK.
          2. If both modelled squares are CLEAN: NO_OP.
          3. Otherwise move to the *other* room.

        Rules are checked in this order so that an explicit "dirty"
        percept is always handled before the quiescence check —
        this is the slide-15 ordering.
        """
        percept = self.state

        # Rule 1: act immediately on a dirty square. Reading
        # STATES_TREATED_AS_DIRTY via `_is_dirty` keeps the rule
        # variant-1 compatible (dust-level sensor).
        if _is_dirty(percept[1]):
            return Action.SUCK

        # Rule 2: model-derived quiescence. The slide-15 condition
        # `model[A] == model[B] == 'Clean'` reads the whole model.
        if self.model[Location.A] == self.model[Location.B] == States.CLEAN:
            return Action.NO_OP

        # Rule 3: move toward the unmodelled room. In the 2-room
        # world that simply means "go the other way".
        if percept[0] == Location.A:
            return Action.RIGHT
        if percept[0] == Location.B:
            return Action.LEFT
        return Action.NO_OP

    def update_state(self, percept: LocationState) -> None:
        """UPDATE-STATE from slide 16.

        For the simple 2-room world the only "model update" needed
        is recording the dirt status of the *current* square — the
        agent has not seen the other one yet, so its slot stays
        UNKNOWN until the cleaner moves there.
        """
        location, status = percept
        self.model[location] = status

    def sensors(self, environment: EnvironmentClass) -> tuple[Location, States]:
        """Return the percept (location, status) — identical to the
        stateless agent's sensor."""
        location = environment.current_location
        return location, environment.states[location]

    def actuators(self, requested_action: Action,
                  environment: EnvironmentClass) -> None:
        """Apply `requested_action`, refusing bogus moves the way
        Exercise 2 demonstrated. Slide-16 sequence: rule -> action ->
        actuator; the slide-9 "Actuators(action)" definition is
        what enforces the bogus-action guard."""
        location = environment.current_location
        # The original template used a `requested_action not in
        # allowed_moves()` early-return; we preserve that semantics
        # exactly so signature-preservation checks pass.
        if requested_action not in location.allowed_moves():
            return
        if requested_action == Action.SUCK:
            environment.states[location] = States.CLEAN
        elif requested_action == Action.RIGHT:
            environment.current_location = Location.B
        elif requested_action == Action.LEFT:
            environment.current_location = Location.A

    def act(self, environment: EnvironmentClass) -> Action:
        """One tick of slide-16's REFLEX-AGENT-WITH-STATE."""
        percept = self.sensors(environment)
        # state = UPDATE-STATE(state, action, percept)
        self.state = percept
        self.update_state(percept)
        # rule = RULE-MATCH(state, rules)  /  action = RULE-ACTION[rule]
        action = self.match_rule()
        # Apply via the actuator (which guards against bogus moves).
        self.actuators(action, environment)
        # Slide-16 says `static: action` — store it for the next
        # tick's UPDATE-STATE call (the 2-room update doesn't read
        # it but a richer model-based update would).
        self.last_action = action
        return action


# --------------------------------------------------------------------
# 4-square world (Homework) — the entry-point demo.
# --------------------------------------------------------------------

class GridEnvironment:
    """2x2 grid environment for the Homework. Symmetric in shape
    with the 2-room `EnvironmentClass` so reviewers can read each
    block independently."""
    def __init__(self, current_location: GridLocation,
                 states: GridLocationMap):
        self.current_location = current_location
        self.states = states


class StatefulGridAgent:
    """Slide-16 stateful reflex agent extended to the 2x2 grid
    (Homework). The model now has 4 entries; the quiescence rule
    fires when *all four* are CLEAN.

    Same model-based reflex architecture (L02 §4.3): UPDATE-STATE
    writes the current-square percept to `self.model` every tick;
    the model is consulted by Rule 2 (quiescence) and by Rule 3
    (which next-target to head toward). Rule 1 still fires on the
    raw percept alone, exactly like the simple reflex agent.
    """

    def __init__(self):
        # Slide 15 says the model is "initially ignorant" — every
        # square unmodelled until the cleaner senses it.
        self.model: GridLocationMap = {
            GridLocation.TL: States.UNKNOWN,
            GridLocation.TR: States.UNKNOWN,
            GridLocation.BL: States.UNKNOWN,
            GridLocation.BR: States.UNKNOWN,
        }
        self.state: GridLocationState = (
            GridLocation.UNKNOWN, States.UNKNOWN,
        )
        self.last_action: GridAction = GridAction.NO_OP

    def match_rule(self) -> GridAction:
        """RULE-MATCH for the 4-square world.

        Rules (mirroring slide 14-15):
          1. If the current square indicates dirt: SUCK.
          2. If every modelled square is CLEAN: NO_OP (quiescence).
          3. Otherwise pick the directional move that leads toward
             the *nearest* not-yet-known-clean square along
             GRID_TRAVERSAL_ORDER.
        """
        percept = self.state
        location, status = percept

        # Rule 1: act on dirty immediately (variant-1 safe via
        # _is_dirty / STATES_TREATED_AS_DIRTY).
        if _is_dirty(status):
            return GridAction.SUCK

        # Rule 2: quiescence — every modelled square known CLEAN.
        # This is the 4-square generalisation of slide-15's
        # `if model[A] == model[B] == 'Clean': NO_OP`.
        if all(s == States.CLEAN for s in self.model.values()):
            return GridAction.NO_OP

        # Rule 3: head toward the next square that is *not* known
        # to be CLEAN, choosing along GRID_TRAVERSAL_ORDER so the
        # agent makes deterministic progress.
        target = _next_unclean_target(location, self.model)
        move = _grid_move_toward(location, target)
        return move if move is not None else GridAction.NO_OP

    def update_state(self, percept: GridLocationState) -> None:
        """UPDATE-STATE: record what the cleaner just sensed about
        its current square. The slide-15 update also accounts for
        "how the environment evolves independent of the agent" —
        for the vacuum world that rule is the trivial "clean stays
        clean", so no additional bookkeeping is needed."""
        location, status = percept
        self.model[location] = status

    def sensors(self, environment: GridEnvironment) -> GridLocationState:
        """Return the (location, status) percept for the current
        square — identical signature shape to `StatefulReflexAgent`."""
        location = environment.current_location
        return location, environment.states[location]

    def actuators(self, requested_action: GridAction,
                  environment: GridEnvironment) -> None:
        """Apply `requested_action` if the current square allows it,
        otherwise stand still — the Exercise-2 bogus-action defence
        carried into the 4-square world."""
        location = environment.current_location
        if requested_action not in location.allowed_moves():
            return
        if requested_action == GridAction.SUCK:
            environment.states[location] = States.CLEAN
            return
        if requested_action == GridAction.NO_OP:
            return
        nxt = _grid_neighbour(location, requested_action)
        if nxt is not None:
            environment.current_location = nxt

    def act(self, environment: GridEnvironment) -> GridAction:
        """One tick of slide-16's REFLEX-AGENT-WITH-STATE in the
        4-square world."""
        percept = self.sensors(environment)
        self.state = percept
        self.update_state(percept)
        action = self.match_rule()
        self.actuators(action, environment)
        self.last_action = action
        return action


# --------------------------------------------------------------------
# Grid topology helpers (kept here so the entry-point file is
# self-contained; mirrors the helpers in
# reflex_vacuum_agent_solution.py)
# --------------------------------------------------------------------

def _grid_neighbour(loc: GridLocation,
                    move: GridAction) -> GridLocation | None:
    """Return the square reached by `move` from `loc`, or None if
    the move falls off the world. Topology-aware (respects
    GRID_TOPOLOGY)."""
    if GRID_TOPOLOGY == "LINE_4":
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


def _next_unclean_target(loc: GridLocation,
                         model: GridLocationMap) -> GridLocation:
    """Pick the next-in-traversal-order square that is *not* yet
    modelled as CLEAN. Falling back to the first traversal slot
    keeps the function total — `match_rule` separately handles the
    "all clean" case via Rule 2 before we get here."""
    order = [GridLocation[n] for n in GRID_TRAVERSAL_ORDER]
    # Start scanning from the slot AFTER the cleaner's current
    # location so the traversal feels continuous; wrap around the
    # tuple to keep total coverage.
    start = order.index(loc) if loc in order else 0
    for offset in range(1, len(order) + 1):
        candidate = order[(start + offset) % len(order)]
        if model.get(candidate, States.UNKNOWN) != States.CLEAN:
            return candidate
    return order[0]


def _grid_move_toward(src: GridLocation,
                      dst: GridLocation) -> GridAction | None:
    """Return the directional GridAction that moves from `src`
    toward `dst`, or None if no legal single move connects them.

    Direction-attempt order is controlled by the
    MOVE_PREFERENCE_PRIMARY / MOVE_PREFERENCE_FALLBACK KNOBs imported
    from `reflex_vacuum_agent_solution` — change a knob once, both
    agents pick it up.
    """
    primary = tuple(GridAction[n] for n in MOVE_PREFERENCE_PRIMARY)
    fallback = tuple(GridAction[n] for n in MOVE_PREFERENCE_FALLBACK)
    # First try a direct one-hop move.
    for move in primary:
        if move not in src.allowed_moves():
            continue
        if _grid_neighbour(src, move) == dst:
            return move
    # Otherwise pick any legal directional move so the cleaner makes
    # progress — the next tick's `match_rule` will re-aim.
    for move in fallback:
        if move in src.allowed_moves() and _grid_neighbour(src, move) is not None:
            return move
    return None


def _initial_states_2room() -> LocationMap:
    """2-room initial dirt distribution — same KNOBs as in the
    stateless agent so a reviewer can compare the two files easily.
    Respects MIXED_DIRTY_SQUARES when INITIAL_DIRT == 'MIXED'."""
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
    """4-square initial dirt distribution. Honours MIXED_DIRTY_SQUARES
    when INITIAL_DIRT == 'MIXED'."""
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
# Trace runner
# --------------------------------------------------------------------

# KNOB: COLUMN_WIDTHS (default=(10, 8, 7), range=positive ints)
#   What it does: width of the location / status / action columns in
#     the printed trace. Cosmetic.
#   Effect: wider = nicer alignment; narrower = compact stdout. The
#     "New" header width is derived from these values so the header
#     re-aligns automatically when a column is widened.
#   Exam variants: leave at the default; widen only if a variant
#     adds longer enum names (e.g. status "LIGHT_DIRTY").
COLUMN_WIDTHS: tuple[int, int, int] = (10, 8, 7)

# KNOB: ARROW (default="-> ", range=any short string)
#   What it does: separator drawn between the "before" columns and
#     the "after" columns in the printed trace. Purely cosmetic.
#   Effect: changes the visual divider only — column widths are
#     independent of this string.
#   Exam variants: irrelevant to every variant in
#     study/_exam/Lab1-Agents/variants.md — leave at the default.
ARROW: str = "-> "


def _print_header() -> None:
    loc_w, sta_w, act_w = COLUMN_WIDTHS
    new_w = loc_w + sta_w
    print(f"{'Current':{loc_w + sta_w + act_w}s}{ARROW}{'New':{new_w}s}")
    print(
        f"{'location':{loc_w}s}{'status':{sta_w}s}{'action':{act_w}s}"
        f"{ARROW}{'location':{loc_w}s}{'status':{sta_w}s}"
    )


def _propagate_knobs_to_stateless() -> None:
    """Write this file's world-shaping KNOBs into the stateless
    module before delegating to its `run()`. Without this the
    AGENT_VARIANT == 'STATELESS' branch would silently use the
    *stateless* file's own defaults (e.g. WORLD='ROOMS_2') instead
    of the entry-point KNOBs the user just set — exactly the
    delegation-propagation bug Reviewer #2 flagged."""
    import reflex_vacuum_agent_solution as stateless
    stateless.WORLD = WORLD
    stateless.NUM_STEPS = NUM_STEPS
    stateless.START_LOCATION_2ROOM = START_LOCATION_2ROOM
    stateless.START_LOCATION_GRID = START_LOCATION_GRID
    stateless.GRID_TRAVERSAL_ORDER = GRID_TRAVERSAL_ORDER
    stateless.INITIAL_DIRT = INITIAL_DIRT
    stateless.MIXED_DIRTY_SQUARES = MIXED_DIRTY_SQUARES


def run(n: int | None = None) -> None:
    """Run the stateful reflex agent for `n` steps. If `n` is None
    we fall back to the NUM_STEPS knob (default 20 — the Homework
    slide's `run(20)`)."""
    steps = n if n is not None else NUM_STEPS

    # Stateless variant: hand off to the simple reflex agent so the
    # variant-3 (stateless-vs-stateful) comparison can run from
    # this single entry-point file. KNOBs are propagated first so
    # the stateless run uses the same world / start / dirt config
    # the user set here.
    if AGENT_VARIANT == "STATELESS":
        _propagate_knobs_to_stateless()
        from reflex_vacuum_agent_solution import run as stateless_run
        stateless_run(steps)
        return

    if WORLD == "GRID_4":
        env = GridEnvironment(
            current_location=START_LOCATION_GRID,
            states=_initial_states_grid(),
        )
        agent = StatefulGridAgent()
        _print_header()
        loc_w, sta_w, act_w = COLUMN_WIDTHS
        # `range(steps)` (not `range(1, steps)`) so `run(20)` produces
        # exactly 20 rows — matching the slide-18 contract.
        for _ in range(steps):
            (loc, status) = agent.sensors(env)
            print(f"{loc.name:{loc_w}s}{status.name:{sta_w}s}", end="")
            action = agent.act(env)
            (loc, status) = agent.sensors(env)
            print(
                f"{action.name:{act_w}s}{ARROW}"
                f"{loc.name:{loc_w}s}{status.name:{sta_w}s}"
            )
        return

    # WORLD == "ROOMS_2" — slide 16 demo.
    env = EnvironmentClass(
        current_location=START_LOCATION_2ROOM,
        states=_initial_states_2room(),
    )
    agent = StatefulReflexAgent()
    _print_header()
    loc_w, sta_w, act_w = COLUMN_WIDTHS
    for _ in range(steps):
        (loc, status) = agent.sensors(env)
        print(f"{loc.name:{loc_w}s}{status.name:{sta_w}s}", end="")
        action = agent.act(env)
        (loc, status) = agent.sensors(env)
        print(
            f"{action.name:{act_w}s}{ARROW}"
            f"{loc.name:{loc_w}s}{status.name:{sta_w}s}"
        )


if __name__ == "__main__":
    run(NUM_STEPS)

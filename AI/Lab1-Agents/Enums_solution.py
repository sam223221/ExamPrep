"""
LAB 1: Agents (Reflex agents, vacuum world) — shared enums
==========================================================

PROBLEM STATEMENT (from Lab 1.pdf):
-----------------------------------
This module is the shared type vocabulary used by the four lab files in
Lab 1 (table-driven, simple reflex, stateful reflex, plus the 4-square
extensions in Exercise 3 / Homework). The Lab 1 hand-out itself contains
no exercise dedicated to `Enums.py`; it appears only as a "Hint:
investigate Enums.py" pointer in Exercise 3 and the Homework, where the
student must extend the world from 2 squares (A, B) to 4 squares (a 2x2
grid). To make every solution file work without editing the original
`Enums.py`, this `Enums_solution.py` re-exports the original enums and
ADDS one new enum (`GridLocation`, the 4-square layout) plus its
`allowed_moves()` rule. Everything else is unchanged.

MENTAL MODEL (one-line analogy):
--------------------------------
This file is the floor plan + the rulebook for "what doors open from
which room" that every agent in the lab shares — same map, same
allowed steps, no matter whether the brain reading the map is a
table-driven lookup (an infinite filing cabinet, L02 §2 / §4.1), a
simple-reflex vending machine (L02 §2 / §4.2), or a stateful driver-in-
fog with an internal model (L02 §2 / §4.3).

REFERENCES:
-----------
- Lecture L02 §3.1 "Agent and environment" — the formal agent /
  environment / sensors / actuators tuple this module realises.
- Lecture L02 §3.5 "PEAS" — the **E** (environment) and **A**
  (actuators) parts of the lab's vacuum world.
- See study/lectures/L02-Agents.md.
- Glossary terms (defined in L02): Agent, Environment, Actuator,
  Sensor, Percept, PEAS.

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
1. To switch the 4-square layout to a 1-D corridor of 4 cells: set
   GRID_TOPOLOGY = "LINE_4" — `GridLocation.allowed_moves()` then only
   exposes LEFT/RIGHT (no UP/DOWN). The row order is controlled by
   the LINE_4_ORDER KNOB (default TL → TR → BL → BR).
2. To grow the world to 3 rooms in a row (variant 2 in
   study/_exam/Lab1-Agents/variants.md): use the original 2-room
   `Location` enum as a template; add `Location.C`; update
   `Location.allowed_moves()` to expose LEFT at C and to expose RIGHT
   at B (B is now in the middle). The reflex rules in
   reflex_vacuum_agent_solution / reflex_agent_with_state_solution use
   `allowed_moves()`, so the controllers do not need to change.
3. To add a third sensor (e.g. "dust-level" — variant 1): extend
   `States` with `States.LIGHT_DIRTY` / `States.HEAVY_DIRTY`. The
   reflex agents already widen the "dirty side" via the
   `STATES_TREATED_AS_DIRTY` KNOB (declared in the agent files);
   just add the new symbols to that set and the slide-10 / slide-15
   rules keep firing unchanged.

OUTPUTS WHEN RUN (captured 2026-05-23, py -3.12):
-------------------------------------------------
Running this module directly (`py -3.12 Enums_solution.py`) executes
its `__main__` block, which prints a one-line sanity check of the
topology KNOB plus the moves allowed from every square. With the
defaults (GRID_TOPOLOGY = "GRID_2x2") the output is:

    GRID_TOPOLOGY = GRID_2x2
    LINE_4_ORDER  = ('TL', 'TR', 'BL', 'BR')
    Allowed moves per GridLocation:
      TL       -> ['RIGHT', 'DOWN', 'SUCK', 'NO_OP']
      TR       -> ['LEFT', 'DOWN', 'SUCK', 'NO_OP']
      BL       -> ['RIGHT', 'UP', 'SUCK', 'NO_OP']
      BR       -> ['LEFT', 'UP', 'SUCK', 'NO_OP']
      UNKNOWN  -> ['SUCK', 'NO_OP']

Flipping GRID_TOPOLOGY = "LINE_4" yields LEFT/RIGHT only and the row
order is LINE_4_ORDER.

ENTRY POINT: no
---------------
This module is a helper imported by the three agent solution files
(`table_driven_agent_solution.py`, `reflex_vacuum_agent_solution.py`,
`reflex_agent_with_state_solution.py`). The Lab 1 entry point is
`reflex_agent_with_state_solution.py` (it runs the Homework — the
4-square stateful reflex agent — which exercises every concept in the
lab end-to-end).
"""

# Re-export the original two-room enums so existing tests / scripts that
# `from Enums import ...` continue to work via either module name. The
# original file is left untouched per the no-edit-originals rule.
# NOTE: this re-export requires the original `Enums.py` to be importable
# (it sits next to this file in `Lab1-Agents/`). If a grader ships only
# the `*_solution.py` files, copy the three enums (States, Action,
# Location, LocationState) into this file verbatim.
from Enums import States, Action, Location, LocationState  # noqa: F401

from enum import Enum, auto


# KNOB: GRID_TOPOLOGY (default="GRID_2x2", allowed={"GRID_2x2", "LINE_4"})
#   What it does: selects the connectivity rule the 4-square world uses.
#     The KNOB is compared with `==` (case-sensitive string equality) —
#     it must be EXACTLY one of the two allowed strings (no "grid_2x2",
#     no "GRID2X2").
#   Effect:
#     - "GRID_2x2": four squares arranged as a 2x2 grid. From the
#       top-left (TL) the robot can go RIGHT to TR or DOWN to BL, and
#       so on. UP/DOWN are added to the action vocabulary.
#     - "LINE_4": four squares in a single row (order controlled by
#       LINE_4_ORDER below). Only LEFT and RIGHT are allowed; the
#       agent's policy reduces to the 2-room rule extended with extra
#       LEFT/RIGHT steps.
#   Exam variants: a 2-D 4-square world is the Homework default;
#     LINE_4 is the natural drop-in for variant 2 (3 or 4 rooms in a
#     line) — flip this knob and re-run.
GRID_TOPOLOGY: str = "GRID_2x2"


# KNOB: LINE_4_ORDER (default=("TL","TR","BL","BR"),
#        range=any permutation of {"TL","TR","BL","BR"})
#   What it does: row order used when GRID_TOPOLOGY == "LINE_4". The
#     tuple lists the four squares from leftmost to rightmost in the
#     1-D corridor. The reflex agents read this same KNOB (via import)
#     so the topology lives in ONE place — change it here and every
#     downstream agent picks it up.
#   Effect: determines which square is reached by LEFT vs RIGHT in
#     LINE_4 mode. Has no effect when GRID_TOPOLOGY == "GRID_2x2".
#   Exam variants: pick a different permutation if a variant question
#     asks for "BL is on the far left" or similar.
LINE_4_ORDER: tuple[str, ...] = ("TL", "TR", "BL", "BR")


class GridAction(Enum):
    """Action vocabulary for the 4-square (2x2 grid) world.

    SUCK / NO_OP carry the same meaning as in the original `Action`
    enum; UP / DOWN / LEFT / RIGHT are *grid moves* in compass form.
    The original 2-room `Action.LEFT` / `Action.RIGHT` enums still
    exist (imported above) for the 2-room agents — they are NOT the
    same Python objects as `GridAction.LEFT` / `GridAction.RIGHT`.
    """
    SUCK = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    NO_OP = auto()

    def __repr__(self):  # printed name in trace output, matching original
        return self.name


class GridLocation(Enum):
    """Four squares of the Exercise-3 / Homework world.

    Layout (compass):
        TL  TR
        BL  BR
    The enum values are arbitrary; only `allowed_moves()` and the
    actuator wiring (in the agent files) care about the *names*.
    """
    TL = auto()  # top-left
    TR = auto()  # top-right
    BL = auto()  # bottom-left
    BR = auto()  # bottom-right
    UNKNOWN = auto()  # used by the stateful agent before it has sensed

    def allowed_moves(self) -> tuple[GridAction, ...]:
        """Return the tuple of grid actions legal from this square.

        Mirrors `Location.allowed_moves` from the original `Enums.py`:
        SUCK and NO_OP are always allowed (they are square-local);
        directional moves are restricted by the topology knob and by
        the actual adjacency from the square in question. The robot
        cannot fall off the world.
        """
        # Local-action floor. The slides put SUCK/NO_OP into every move
        # set so the reflex rule can fire "Suck if Dirty" without first
        # checking adjacency — this is the slide-10 contract.
        always_allowed = (GridAction.SUCK, GridAction.NO_OP)

        # 1-D fallback: LINE_4 reduces the 2x2 to a row controlled by
        # the LINE_4_ORDER KNOB. The reflex controllers always consult
        # `allowed_moves()`, so flipping the topology never requires
        # editing them.
        if GRID_TOPOLOGY == "LINE_4":
            order = tuple(GridLocation[name] for name in LINE_4_ORDER)
            if self == GridLocation.UNKNOWN:
                return always_allowed
            idx = order.index(self)
            moves: list[GridAction] = []
            if idx > 0:
                moves.append(GridAction.LEFT)
            if idx < len(order) - 1:
                moves.append(GridAction.RIGHT)
            return (*moves, *always_allowed)

        # Default 2x2 grid adjacencies.
        if self == GridLocation.TL:
            return GridAction.RIGHT, GridAction.DOWN, *always_allowed
        if self == GridLocation.TR:
            return GridAction.LEFT, GridAction.DOWN, *always_allowed
        if self == GridLocation.BL:
            return GridAction.RIGHT, GridAction.UP, *always_allowed
        if self == GridLocation.BR:
            return GridAction.LEFT, GridAction.UP, *always_allowed
        return always_allowed  # UNKNOWN: only local actions are safe

    def __repr__(self):
        return self.name


# Convenience type alias for the 4-square world, mirroring the
# `LocationState = tuple[Location, States]` alias from the original
# `Enums.py`. Keeping the same name pattern means downstream files
# can read as if they were using the original enums.
type GridLocationState = tuple[GridLocation, States]


# 2x2 grid adjacency table. Centralised here (instead of duplicated in
# each agent file) so a topology change happens in ONE place. Reflex
# agents import this and consult it; the table is *static* topology so
# no agent ever rebuilds it.
GRID_2X2_ADJACENCY: dict[tuple[GridLocation, GridAction], GridLocation] = {
    (GridLocation.TL, GridAction.RIGHT): GridLocation.TR,
    (GridLocation.TL, GridAction.DOWN):  GridLocation.BL,
    (GridLocation.TR, GridAction.LEFT):  GridLocation.TL,
    (GridLocation.TR, GridAction.DOWN):  GridLocation.BR,
    (GridLocation.BL, GridAction.RIGHT): GridLocation.BR,
    (GridLocation.BL, GridAction.UP):    GridLocation.TL,
    (GridLocation.BR, GridAction.LEFT):  GridLocation.BL,
    (GridLocation.BR, GridAction.UP):    GridLocation.TR,
}


if __name__ == "__main__":
    # Sanity print: confirms the topology knob and the allowed-moves
    # table without needing to open any agent file.
    print(f"GRID_TOPOLOGY = {GRID_TOPOLOGY}")
    print(f"LINE_4_ORDER  = {LINE_4_ORDER}")
    print("Allowed moves per GridLocation:")
    for loc in GridLocation:
        print(f"  {loc.name:8s} -> {[m.name for m in loc.allowed_moves()]}")

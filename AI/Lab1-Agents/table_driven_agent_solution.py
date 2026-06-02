"""
LAB 1 — Exercise 1: A complicated history (Table-driven agent)
==============================================================

PROBLEM STATEMENT (from Lab 1.pdf, slide 7 — Exercise 1):
---------------------------------------------------------
1. Run the module (using run())
2. The percepts should now be:
   [('A', 'Clean'), ('A', 'Dirty'), ('B', 'Clean')]
   - The table contains all possible percept sequences to match with the
     percept history.
   - Enter:
       print(f"{TABLE_DRIVEN_AGENT(clean_B):{action_space}s}| {total_percepts}")
   - Explain the results.
3. How many table entries would be required if only the current (single)
   percept was used to select an action rather than the percept history?
4. How many table entries are required for an agent lifetime of T steps?

Pseudocode from slide 6:

    function TABLE-DRIVEN-AGENT(percept) returns an action
        static: percepts, a sequence, initially empty
                table, a table of actions, indexed by percept
                sequences, initially fully specified
        append percept to the end of percepts
        action = LOOKUP(percepts, table)
        return action

MENTAL MODEL (one-line analogy):
--------------------------------
The table-driven agent is like an infinite, impossible filing cabinet
keyed by every possible life-history of the robot — every drawer holds
the right answer, but the cabinet is the size of a galaxy because the
key is the entire percept sequence so far. (See L02 §2 "An infinite,
impossible filing cabinet" and §4.1 for the size argument.)

REFERENCES:
-----------
- Lecture L02 §4.1 "Table-driven agents" — defines the agent, gives
  the slide-6 pseudocode this file implements, and proves the
  table-size blow-up that Exercises 1.3 / 1.4 quiz on.
- Lecture L02 §3.2 "Percept, percept sequence, agent function, agent
  program" — formal definition of `f: P* -> A` that the table is the
  literal tabulation of.
- See study/lectures/L02-Agents.md.
- Glossary terms (L02): Agent function, Agent program, Percept,
  Percept sequence, Table-driven agent.

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
1. Exercise 1.2 — "Explain the result of TABLE_DRIVEN_AGENT(clean_B)
   after [clean_A, dirty_A, clean_B]": Read the comment block above
   the extra lookup plus the run() output (the demo prints this
   exact extra lookup) — no KNOB change needed.
2. Exercise 1.3 — "How many entries if only the *current* percept is
   used?": Set USE_FULL_HISTORY = False. The print at the end of run()
   reports `|P| = NUM_LOCATIONS * NUM_STATUSES = 4` table entries.
3. Exercise 1.4 — "How many entries for a lifetime of T steps?":
   Set LIFETIME_T to the desired T. The closed-form
   `sum_{k=1..T} |P|^k` (one row per percept history of length k for k
   in 1..T) is printed by `report_table_size()` for the chosen T.
4. To grow the percept space (variants 1 — extra sensor, or 2 — more
   rooms): set NUM_LOCATIONS and NUM_STATUSES; the table-size formula
   is `|P|^k` where `|P| = NUM_LOCATIONS * NUM_STATUSES`. The
   blow-up is the entire point of Exercise 1.

OUTPUTS WHEN RUN (captured 2026-05-23, py -3.12):
-------------------------------------------------
Running `py -3.12 table_driven_agent_solution.py` with all defaults
prints:

    Action        | Percepts
    RIGHT         | [(A, CLEAN)]
    SUCK          | [(A, CLEAN), (A, DIRTY)]
    LEFT          | [(A, CLEAN), (A, DIRTY), (B, CLEAN)]
    LEFT          | [(A, CLEAN), (A, DIRTY), (B, CLEAN), (B, CLEAN)]

    Table size using only the current percept: |P| = NUM_LOCATIONS * NUM_STATUSES = 4
    Table size with full history of length up to T=10: sum_(k=1..T) |P|^k = 1398100  (|P|=4)

Lines 2-4 are the three slide-7 percept lookups; line 5 is the extra
Exercise 1.2 lookup; the two final lines answer Exercises 1.3 and 1.4
under the default KNOBs (NUM_LOCATIONS=2, NUM_STATUSES=2, LIFETIME_T=10).

ENTRY POINT: no
---------------
This file demonstrates ONE of the three agent variants in Lab 1
(Exercise 1). The Lab 1 entry point is
reflex_agent_with_state_solution.py, which runs the Homework — the
4-square stateful reflex agent — and exercises every concept in the
lab end-to-end.
"""

from Enums import LocationState, Location, States, Action


type Percept = LocationState
type Percepts = list[Percept]


# --------------------------------------------------------------------
# Sizing knobs — these are the variables Exercise 1.3 / 1.4 quiz the
# student on. Promoting them to module-level KNOBs lets the exam
# agent answer "what if the world has 3 rooms" without rewriting any
# helper function.
# --------------------------------------------------------------------

# KNOB: NUM_LOCATIONS (default=2, range=any int >= 1)
#   What it does: number of distinct locations the cleaner can occupy.
#     The original Lab 1 vacuum world has 2 (A, B); Exercise 3 and the
#     Homework grow it to 4. The percept space size is
#     NUM_LOCATIONS * NUM_STATUSES.
#   Effect: table size for a lifetime of T grows as
#     sum_{k=1..T} (NUM_LOCATIONS * NUM_STATUSES) ** k.
#     Doubling NUM_LOCATIONS roughly squares the table at lifetime T.
#   Exam variants: 2 = default 2-room slides; 3 = "3 rooms in a line"
#     variant 2; 4 = Exercise 3 / Homework 2x2 grid world.
NUM_LOCATIONS: int = 2

# KNOB: NUM_STATUSES (default=2, range=any int >= 1)
#   What it does: number of distinct cleanliness levels a square may
#     have. The slides use 2 (CLEAN, DIRTY). Adding a "dust-level"
#     sensor (variant 1) raises this to 3 (CLEAN, LIGHT_DIRTY,
#     HEAVY_DIRTY).
#   Effect: identical multiplicative effect on the percept space and
#     therefore on the table size — `|P|` becomes NUM_LOCATIONS *
#     NUM_STATUSES, so the table at lifetime T has
#     sum_{k=1..T} |P|^k entries.
#   Exam variants: 2 = default; 3 = extra dust-level sensor.
NUM_STATUSES: int = 2

# KNOB: LIFETIME_T (default=10, range=any positive int)
#   What it does: the agent's lifetime in time steps, used to compute
#     the size of the percept-history-indexed table the lab asks
#     about in Exercise 1.4.
#   Effect: table size is sum_{k=1..T} |P|^k, dominated by the |P|^T
#     term. The growth is exponential in T — which is exactly the
#     pedagogical point of the exercise (the table-driven agent is
#     intractable for any non-trivial T).
#   Exam variants: 10 = short demo lifetime; 100 = the textbook
#     "moderately long" lifetime; vary freely for "what if T = ..."
#     style questions.
LIFETIME_T: int = 10

# KNOB: USE_FULL_HISTORY (default=True, range={True, False})
#   What it does: switches the size reporter between
#     "full history of length up to T" (True — the lab's table-driven
#     agent in its slide-6 form) and "current single percept only"
#     (False — Exercise 1.3 simplification).
#   Effect: True -> sum_{k=1..T} |P|^k ; False -> |P| (a constant).
#     The contrast is the textbook punchline: the stateless agent
#     uses |P| rules; the historical agent needs exponentially many.
#   Exam variants: leave True for 1.4-style questions, flip to False
#     for the 1.3 simplification. (The default run() prints BOTH
#     values, so a single run already answers 1.3 + 1.4.)
USE_FULL_HISTORY: bool = True

# KNOB: ACTION_COLUMN_WIDTH (default=14, range=any int >= len(longest action name))
#   What it does: column width for the Action column in the printed
#     trace. Cosmetic — does not affect agent behaviour.
#   Effect: wider = neater for long action names; narrower = more
#     compact stdout. Required because Python's f-string format spec
#     needs the width as a literal integer.
#   Exam variants: unchanged across variants; bump if you add longer
#     action names (e.g. a "STAY_AND_REPORT" verb).
ACTION_COLUMN_WIDTH: int = 14


# Module-level percept history used by the (literal) table-driven
# agent. The slides treat this as the `static: percepts` variable of
# the pseudocode on slide 6.
total_percepts: Percepts = []


# Common percept literals — kept identical to the original template so
# the lab's `print(f"...{TABLE_DRIVEN_AGENT(clean_B)}...")` instruction
# from Exercise 1.2 reads unchanged.
clean_A = (Location.A, States.CLEAN)
dirty_A = (Location.A, States.DIRTY)
clean_B = (Location.B, States.CLEAN)
dirty_B = (Location.B, States.DIRTY)


type LookupTable = dict[tuple[Percept, ...], Action]


# A *fully specified* table is what slide 6 demands — every possible
# percept-sequence prefix has an entry. We give a small illustrative
# subset that matches the slide; in practice the table would be
# astronomically big (KNOB-reported below).
table_definition: LookupTable = {
    (clean_A,): Action.RIGHT,
    (dirty_A,): Action.SUCK,
    (clean_B,): Action.LEFT,
    (dirty_B,): Action.SUCK,
    (clean_A, clean_A): Action.RIGHT,
    (clean_A, dirty_A): Action.SUCK,
    (clean_A, clean_A, clean_A): Action.RIGHT,
    (clean_A, clean_A, dirty_A): Action.SUCK,
    (clean_A, dirty_A, clean_B): Action.LEFT,
    # The Exercise 1.2 question hinges on this entry being present:
    # after the percept sequence (clean_A, dirty_A, clean_B), the
    # student is asked to look up `TABLE_DRIVEN_AGENT(clean_B)`. With
    # the next clean_B appended the key becomes
    # (clean_A, dirty_A, clean_B, clean_B) — which the table below
    # provides explicitly so the lookup succeeds rather than falling
    # back to NO_OP.
    (clean_A, dirty_A, clean_B, clean_B): Action.LEFT,
}


def LOOKUP(percepts: Percepts, table: LookupTable) -> Action:
    """Lookup appropriate action for `percepts`.

    :return: Action stored in `table` for the exact percept-sequence
    key, or Action.NO_OP when the sequence is not in the table.
    """
    # We key on `tuple(percepts)` (an immutable copy) rather than the
    # live list because dicts need hashable keys, and slide 6 indexes
    # the table by the immutable history-so-far. Falling back to
    # NO_OP instead of raising KeyError matches slide-6's "safe
    # no-op" convention — an unknown history is the textbook reason
    # the table-driven agent silently stops doing useful work once
    # the history grows past what was hand-specified.
    return table.get(tuple(percepts), Action.NO_OP)


def TABLE_DRIVEN_AGENT(percept: Percept) -> Action:
    """Determine action based on the table and the percept history.

    Matches the slide-6 pseudocode line-for-line:
        append percept to the end of percepts
        action = LOOKUP(percepts, table)
        return action
    """
    # Appending mutates the module-level `total_percepts` because the
    # slides describe this variable as `static` — i.e. preserved
    # across calls within the same lifetime. Mirroring that semantics
    # makes the exam variant 1.2 work exactly as the slide expects.
    total_percepts.append(percept)
    return LOOKUP(total_percepts, table_definition)


def percept_space_size() -> int:
    """|P| = NUM_LOCATIONS * NUM_STATUSES — the size of the percept
    set the slide-6 agent must distinguish at every step. Used by
    Exercise 1.3 and 1.4 reporting below."""
    return NUM_LOCATIONS * NUM_STATUSES


def table_size_for_lifetime(lifetime: int) -> int:
    """Number of entries a fully-specified percept-sequence table
    requires for the chosen `lifetime`.

    The slide-6 table is "indexed by percept sequences", so for a
    lifetime of T steps we need one row per possible history of
    length 1, 2, ..., T:

        sum_{k=1..T} |P|^k

    where |P| = NUM_LOCATIONS * NUM_STATUSES. This is the closed-form
    answer to Exercise 1.4. Variant questions can change
    NUM_LOCATIONS / NUM_STATUSES / LIFETIME_T and the formula stays
    correct because it is parameterised by the three KNOBs.
    """
    # We use the geometric-series closed form so the table size for
    # T = 100 doesn't take longer to compute than to print. (Iterating
    # would compute the same number with no algorithmic benefit; the
    # closed form is also the textbook expression students are
    # expected to reproduce.)
    p = percept_space_size()
    # geometric series sum_{k=1..T} p^k = p * (p^T - 1) / (p - 1) for p != 1
    if p == 1:
        # Degenerate world with only one percept: 1^k = 1, so the sum
        # is just `lifetime`. Guarding here avoids a divide-by-zero
        # in the closed form.
        return lifetime
    return p * (p**lifetime - 1) // (p - 1)


def report_table_size(use_full_history: bool | None = None) -> None:
    """Print the answer to Exercise 1.3 (use_full_history=False) or
    Exercise 1.4 (use_full_history=True) using the current KNOBs.

    Keeping the reporter inside a function (rather than inline in
    run()) lets an exam agent call it directly with different KNOBs.
    Passing `use_full_history=None` (the default) reads the module-
    level KNOB — that way the function obeys the public KNOB unless
    the caller explicitly overrides it.
    """
    full_history = USE_FULL_HISTORY if use_full_history is None else use_full_history
    p = percept_space_size()
    if full_history:
        # Exercise 1.4 form.
        size = table_size_for_lifetime(LIFETIME_T)
        print(
            f"Table size with full history of length up to T={LIFETIME_T}: "
            f"sum_(k=1..T) |P|^k = {size}  (|P|={p})"
        )
    else:
        # Exercise 1.3 form.
        print(
            f"Table size using only the current percept: |P| = "
            f"NUM_LOCATIONS * NUM_STATUSES = {p}"
        )


def run() -> None:
    """Run the agent on the three percepts the slide hands out and
    then perform the Exercise 1.2 extra lookup. After the percept
    trace, print the table-size answers to Exercise 1.3 and 1.4."""
    # Header.
    print(f"{'Action':{ACTION_COLUMN_WIDTH}s}| Percepts")

    # Three percepts the slide tells the student to feed in. The
    # printed name (`.name`) is the same string the slide shows so
    # the output reads identically to the lecture demo.
    print(f"{TABLE_DRIVEN_AGENT(clean_A).name:{ACTION_COLUMN_WIDTH}s}| {total_percepts}")
    print(f"{TABLE_DRIVEN_AGENT(dirty_A).name:{ACTION_COLUMN_WIDTH}s}| {total_percepts}")
    print(f"{TABLE_DRIVEN_AGENT(clean_B).name:{ACTION_COLUMN_WIDTH}s}| {total_percepts}")

    # Exercise 1.2 — the extra lookup the lab asks the student to add.
    # The percept history is now (clean_A, dirty_A, clean_B); appending
    # one more clean_B produces (clean_A, dirty_A, clean_B, clean_B),
    # which the table maps to LEFT (the robot is in B, sees clean, so
    # the policy is to move left back toward A). The pedagogical point:
    # the same percept (clean_B) appearing for the second time produces
    # a *different* row from the first time it was seen, because the
    # key is the *entire sequence so far*, not the latest percept
    # alone. This is the explosive cost the slide is warning about.
    print(
        f"{TABLE_DRIVEN_AGENT(clean_B).name:{ACTION_COLUMN_WIDTH}s}| "
        f"{total_percepts}"
    )

    print()  # blank line
    # Print BOTH Exercise 1.3 (current-percept-only) and 1.4 (full
    # history) so a single `run()` answers both sub-questions. We pass
    # the override flag explicitly rather than mutate the module-level
    # KNOB — this keeps the public KNOB stable for any caller that
    # imports the module and then calls `report_table_size()` later.
    report_table_size(use_full_history=False)
    report_table_size(use_full_history=True)


if __name__ == "__main__":
    run()

"""
LAB 6 — CSP (Map Colouring / Backtracking Search)
==================================================

PROBLEM STATEMENT (from Lab 6.pdf):
-----------------------------------
Exercise 1: Use the following pseudocode to complete the program
``constraints_template.py``. Implement the ``recursive_backtracking``
function. Remember to incorporate the other methods already present
in the file. The pseudocode (Lab 6.pdf slide 2):

    function RECURSIVE-BACKTRACKING(assignment, csp)
        if assignment is complete then return assignment
        var <- SELECT-UNASSIGNED-VARIABLE(VARIABLES[csp], assignment, csp)
        for each value in ORDER-DOMAIN-VALUES(var, assignment, csp)
            if value is consistent with assignment given CONSTRAINTS[csp]
                add {var = value} to assignment
                result <- RECURSIVE-BACKTRACKING(assignment, csp)
                if result != failure then return result
                remove {var = value} from assignment
        return failure

Exercise 2 (Lab 6.pdf slide 3-4): copy and modify the program to use
the map of South America and 4 colours (Red, Green, Blue, Yellow).

Homework Challenge (Lab 6.pdf slide 5): implement forward checking
and arc consistency.

MENTAL MODEL (one-line analogy):
--------------------------------
**Backtracking on a CSP is like filling in a sudoku.** You pick a
square, try a digit, and the moment that digit clashes with a row,
column, or 3x3 block you have already filled, you cross it out and
try the next digit. When *every* digit clashes, you erase the most
recent square and back up — exactly the recursion's "return failure"
that pops the parent's loop forward.

MRV (Minimum Remaining Values) is the rule "pick the most-constrained
square first" — the cell that has only 2 candidate digits left. LCV
(Least Constraining Value) is "of those 2 digits, try the one that
leaves the most options for the cell's neighbours". (See L07-CSP §3.4
"Backtracking variable/value-ordering heuristics".)

REFERENCES:
-----------
- Lecture 7 §1-§5: Constraint Satisfaction Problems
  (study/lectures/L07-CSP.md). Specifically:
    * §3 Variables, Domains, Constraints
    * §4.1 Backtracking search
    * §4.2 MRV and Degree (variable-ordering heuristics)
    * §4.3 LCV (value-ordering heuristic)
    * §4.4 Forward checking
    * §4.5 Arc consistency (AC-3)
- Glossary terms (study/_shared/glossary.md):
    Backtracking search (for CSPs), Minimum Remaining Values (MRV),
    Degree heuristic, Least Constraining Value (LCV), Forward
    checking, Arc consistency, Constraint graph, Constraint (CSP),
    Consistent assignment (CSP).

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
1. To run the **default exercise (Australia, 3 colours)**:
       MAP_NAME            = "australia"
       ACTIVE_COLORS       = [Color.Red, Color.Green, Color.Blue]
       USE_MRV             = False
       USE_DEGREE_TIEBREAK = False
       USE_LCV             = False
       USE_FORWARD_CHECK   = False
   This reproduces the textbook example: a complete consistent
   assignment of three colours to seven Australian regions.

2. To run **Exercise 2 (South America, 4 colours)**:
       MAP_NAME      = "south_america"
       ACTIVE_COLORS = [Color.Red, Color.Green, Color.Blue, Color.Yellow]
   Everything else may stay False; the four-colour theorem guarantees
   a solution.

3. To run **Variant 1** ("Replace the map ... solve with backtracking
   + MRV"):
       MAP_NAME            = "south_america"   (or another map)
       USE_MRV             = True
       USE_DEGREE_TIEBREAK = True   (optional but recommended)

4. To run **Variant 2** ("Add a 5th colour to the palette — does the
   solver succeed? With how many backtracks?"):
       MAP_NAME      = "south_america"
       ACTIVE_COLORS = [Color.Red, Color.Green, Color.Blue,
                        Color.Yellow, Color.Purple]
   Compare backtrack counts vs the 4-colour run — adding a colour
   only ever *reduces* backtracks. To stress-test the question's
   spirit, try ACTIVE_COLORS = [Color.Red, Color.Green, Color.Blue]
   on South America: the solver should report NO SOLUTION (Brazil
   has 10 neighbours; chromatic number of the map is 4).

5. To run **Variant 3** ("distance-based adjacency"):
       MAP_NAME = "distance_demo"
   The demo builds a CSP whose adjacency is computed from (x, y)
   coordinates and a DISTANCE_THRESHOLD knob: any two regions within
   the threshold are considered adjacent and must differ in colour.
   Tune DISTANCE_THRESHOLD to change the constraint graph's density.

6. To turn on **forward checking** (Homework Challenge):
       USE_FORWARD_CHECK = True
   When True, after each assignment the solver removes the assigned
   colour from every unassigned neighbour's domain. If any domain
   becomes empty the recursion immediately returns failure (fail-
   fast) — far fewer backtracks than blind chronological backtracking.

OUTPUTS WHEN RUN:
-----------------
Prints (for the active configuration) the chosen map name, the
heuristic flags in effect, the colour assignment per region, and the
number of recursive calls + backtracks consumed. Example for the
default 3-colour Australia run (output sorted by States enum value;
each line uses Python's default str() of the enum members, so the
colour reads "Color.Red" not bare "Red"):

    === Lab 6 — CSP / Map Colouring ===
    Map:                 australia
    Active colours:      Red, Green, Blue
    Heuristics:          MRV=False  Degree=False  LCV=False  FC=False  AC3=False
    Recursive calls:     8
    Backtracks:          0
    States.WA: Color.Red
    States.Q: Color.Red
    States.T: Color.Red
    States.V: Color.Red
    States.SA: Color.Green
    States.NT: Color.Blue
    States.NSW: Color.Blue

Note: ``Recursive calls`` is incremented at the TOP of every call —
including the call that returns by completion. For Australia's 7
variables you therefore see 8, not 7 (one entry per variable plus the
base-case completion call).

ENTRY POINT: yes
----------------
Run from the lab6/ directory:
    py -3.12 lab6\\constraints_template_solution.py
"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable
from typing import Dict, List, Optional, Tuple

from Colors_solution import Color
from States_solution import States

# Type aliases (kept identical to the template — Reviewer #1
# "Function signature preservation" cross-checks these).
type contraintFunction = Callable[[States, Color, States, Color], bool]
type Assignment = dict[States, Color]


# ----------------------------------------------------------------------
# KNOBs — set once at import time; the CSP reads them from the module
# globals when it makes decisions. Promoting these to a config block at
# the top makes every exam variant a one-line edit (Reviewer #2 hunts
# for magic numbers buried in function bodies — none should remain).
# ----------------------------------------------------------------------

# KNOB: MAP_NAME (default="australia", allowed={"australia",
#       "south_america", "distance_demo"})
#   What it does: selects which map (i.e. which set of variables,
#     domains, and constraints) the solver tackles.
#   Effect: drives create_csp() to build a different CSP instance.
#   Exam variants: "australia" (default), "south_america" (Exercise 2
#     and variant 1), "distance_demo" (variant 3 — distance-based
#     constraints).
MAP_NAME: str = "australia"

# KNOB: ACTIVE_COLORS (default=[Red, Green, Blue], range=any non-empty
#       subset of the Color enum from Colors_solution.py)
#   What it does: defines the domain D_i shared by every variable
#     (every region can take any of these colours).
#   Effect: more colours -> more freedom -> fewer backtracks. With
#     fewer colours than the map's chromatic number, NO SOLUTION
#     exists and the solver returns None.
#   Exam variants:
#     - 3 colours (Australia default):   [Red, Green, Blue]
#     - 4 colours (Exercise 2, S.Amer.): [Red, Green, Blue, Yellow]
#     - 5 colours (variant 2):           + Purple
ACTIVE_COLORS: List[Color] = [Color.Red, Color.Green, Color.Blue]

# KNOB: USE_MRV (default=False, range={True, False})
#   What it does: enables Minimum-Remaining-Values variable ordering.
#     With MRV on, ``select_unassigned_variable`` always picks the
#     unassigned variable whose current legal-domain count is
#     smallest. The mental-model line is "pick the most-constrained
#     sudoku square first".
#   Effect: typically reduces the number of backtracks by an order of
#     magnitude on dense constraint graphs. Has no effect on tiny
#     CSPs that backtrack zero times anyway.
#   Exam variants: turn on for variant 1; leave off to demonstrate
#     plain chronological backtracking.
USE_MRV: bool = False

# KNOB: USE_DEGREE_TIEBREAK (default=False, range={True, False})
#   What it does: when MRV is on and multiple variables tie on
#     remaining-domain size, pick the one that participates in the
#     most constraints with *unassigned* variables (degree heuristic).
#   Effect: usually breaks the first-step tie usefully (start with
#     the most central node of the constraint graph).
#   Exam variants: switch on alongside MRV for the "MRV + degree"
#     framing.
USE_DEGREE_TIEBREAK: bool = False

# KNOB: USE_LCV (default=False, range={True, False})
#   What it does: enables Least-Constraining-Value ordering. Sorts
#     ``order_domain_values`` by how many neighbour-domain values the
#     candidate value would rule out — try the value that prunes the
#     fewest neighbour options first.
#   Effect: improves the *first-found-solution* runtime, less impact
#     on proving infeasibility.
#   Exam variants: turn on to demonstrate value-ordering heuristics.
USE_LCV: bool = False

# KNOB: USE_FORWARD_CHECK (default=False, range={True, False})
#   What it does: enables forward checking. After every assignment
#     {var = value}, removes ``value`` from each unassigned
#     neighbour's *live domain*. If any domain becomes empty the
#     recursion returns failure immediately (fail-fast).
#   Effect: enormous reduction in backtracks on tightly-constrained
#     problems (often turns exponential search into low-polynomial).
#   Exam variants: turn on for Homework Challenge ("implement forward
#     checking ...").
USE_FORWARD_CHECK: bool = False

# KNOB: DISTANCE_THRESHOLD (default=2.5, range=any positive float)
#   What it does: only used when MAP_NAME == "distance_demo". Two
#     regions whose Euclidean distance (in the demo coordinate
#     system) is <= this threshold are considered adjacent and must
#     receive different colours.
#   Effect: large threshold -> dense graph -> harder problem; small
#     threshold -> sparse graph -> trivial problem.
#   Read at: create_distance_csp() build time. Mutating this KNOB
#     *after* create_csp() has been called has no effect on the
#     already-built CSP — set it BEFORE create_csp() and re-build
#     between runs.
#   Exam variants: variant 3 ("distance-based constraints"). With
#     the demo coordinates A=(0,0), B=(2,0), C=(1,1), D=(0,2), E=(2,2):
#       * threshold 1.5 -> star K_{1,4} (C touches A, B, D, E;
#         corners do NOT touch each other; chromatic number = 2);
#       * threshold 2.5 -> hub + corner-square (chromatic number = 3);
#       * threshold 3.5 -> complete K_5 (chromatic number = 5,
#         infeasible with 3 colours).
DISTANCE_THRESHOLD: float = 2.5

# KNOB: USE_AC3 (default=False, range={True, False})
#   What it does: when True, runs AC-3 as a pre-pass BEFORE
#     backtracking_search() in the __main__ harness. AC-3 enforces
#     arc consistency on the whole CSP in place (mutating
#     ``self.domains``) and reports if it detected infeasibility
#     (any domain wiped out) before search begins.
#   Effect: on binary not-equal CSPs with every domain size >= 2,
#     AC-3 is a no-op (every value has support in every neighbour);
#     it will return True without pruning. On tighter CSPs it can
#     amputate large infeasible subtrees before backtracking even
#     starts. Always safe to leave on; only meaningful when the
#     constraint shape allows pruning.
#   Read at: __main__ entry point, immediately after create_csp().
#   Exam variants: variant 5 ("AC-3 pre-pass on an over-constrained
#     CSP"). With USE_AC3=True the harness prints whether AC-3
#     declared infeasibility and how many domain values it removed.
USE_AC3: bool = False


# ----------------------------------------------------------------------
# CSP class
# ----------------------------------------------------------------------


class CSP:
    """Backtracking-search CSP with optional MRV / Degree / LCV /
    forward-checking heuristics.

    Public surface is identical to constraints_template.py (Reviewer
    #1 verifies). Three new helpers (``_select_mrv``, ``_lcv_sorted``,
    ``_forward_check``) are private — they sit *behind* the four
    template methods, which still own the public contract.
    """

    def __init__(
        self,
        variables: list[States],
        domains: dict[States, list[Color]],
        neighbours: dict[States, list[States]],
        constraints: dict[States, contraintFunction],
    ):
        self.variables: List[States] = variables
        self.domains: Dict[States, List[Color]] = domains
        self.neighbours: Dict[States, List[States]] = neighbours
        self.constraints: Dict[States, contraintFunction] = constraints
        # Lightweight instrumentation so the printout can report
        # "Recursive calls: N, Backtracks: M". Touched only by the
        # solver, never by callers.
        self._recursive_calls: int = 0
        self._backtracks: int = 0

    # ------------------------------------------------------------------
    # Entry point exposed by the template
    # ------------------------------------------------------------------

    def backtracking_search(self) -> dict[States, Color] | None:
        # Reset counters so successive calls give fresh stats. The
        # initial assignment is empty (slide 7 in L07).
        self._recursive_calls = 0
        self._backtracks = 0
        result = self.recursive_backtracking({})
        return result if result else None

    # ------------------------------------------------------------------
    # The function the lab asks the student to implement
    # ------------------------------------------------------------------

    def recursive_backtracking(self, assignment: Assignment) -> Optional[Assignment]:
        """Direct translation of the Lab 6.pdf pseudocode.

        We delegate variable selection, value ordering, and
        consistency checking to ``select_unassigned_variable``,
        ``order_domain_values``, and ``is_consistent`` respectively
        (per the pseudocode and the "Remember to incorporate the
        other methods" note on slide 2).
        """
        self._recursive_calls += 1

        # "if assignment is complete then return assignment"
        if self.is_complete(assignment):
            return assignment

        # "var <- SELECT-UNASSIGNED-VARIABLE(...)"
        variable = self.select_unassigned_variable(assignment)
        if variable is None:
            # Defensive: should not occur because is_complete already
            # returned True if every variable were assigned.
            return None

        # "for each value in ORDER-DOMAIN-VALUES(var, assignment, csp)"
        for value in self.order_domain_values(variable, assignment):
            # "if value is consistent with assignment given CONSTRAINTS[csp]"
            if self.is_consistent(variable, value, assignment):

                # "add {var = value} to assignment"
                assignment[variable] = value

                # Forward-checking snapshot: we save the domains we
                # are about to prune so we can restore them on
                # backtrack. This keeps the public ``self.domains``
                # dict honest across recursive calls.
                fc_snapshot: Optional[Dict[States, List[Color]]] = None
                fc_ok = True
                if USE_FORWARD_CHECK:
                    fc_snapshot, fc_ok = self._forward_check(variable, value, assignment)

                if fc_ok:
                    # "result <- RECURSIVE-BACKTRACKING(assignment, csp)"
                    result = self.recursive_backtracking(assignment)
                    # "if result != failure then return result"
                    if result is not None:
                        # Restore the FC snapshot even on success so
                        # the CSP instance is re-usable across runs
                        # (otherwise self.domains stays permanently
                        # pruned and the NEXT call to
                        # backtracking_search() starts from a stale,
                        # already-pruned state — silently producing
                        # garbage stats for multi-config driver
                        # scripts like Variant 4).
                        if fc_snapshot is not None:
                            self._restore_domains(fc_snapshot)
                        return result

                # Either forward-check wiped out a domain or the deeper
                # recursion returned failure: undo the assignment AND
                # the forward-checking prune, then try the next value.
                if fc_snapshot is not None:
                    self._restore_domains(fc_snapshot)
                # "remove {var = value} from assignment"
                del assignment[variable]
                self._backtracks += 1

        # "return failure"
        return None

    # ------------------------------------------------------------------
    # Helpers preserved from the template (signatures unchanged)
    # ------------------------------------------------------------------

    def select_unassigned_variable(self, assignment: Assignment) -> Optional[States]:
        """Default: first unassigned variable in declared order.

        When ``USE_MRV`` is True we instead pick the unassigned
        variable with the fewest legal values left in its (possibly
        forward-check-pruned) domain. With ``USE_DEGREE_TIEBREAK``
        also True, ties are broken by maximum constraint degree
        among unassigned neighbours.
        """
        if USE_MRV:
            return self._select_mrv(assignment)

        # Original behaviour (template).
        for variable in self.variables:
            if variable not in assignment:
                return variable
        return None

    def is_complete(self, assignment: Assignment) -> bool:
        # Why a manual loop and not ``len(assignment) == len(self.variables)``?
        # To keep the template's contract exact: any subclass that
        # added a derived variable would still answer correctly.
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable: States, assignment: Assignment) -> list[Color]:
        all_values = self.domains[variable][:]
        if USE_LCV:
            # LCV: try the value that rules out the fewest options for
            # the variable's unassigned neighbours first.
            all_values.sort(key=lambda v: self._lcv_count(variable, v, assignment))
        return all_values

    def is_consistent(self, variable: States, value: Color, assignment: Assignment) -> bool:
        # Same contract as the template, but tightened to be O(N) over
        # the variable's neighbour list (rather than O(V*N) over every
        # constraint key). For map-colouring every entry in
        # ``self.constraints`` is the same not-equal predicate so the
        # template's outer loop was correct-but-wasteful; here we pull
        # the per-variable constraint once and check only the neighbours
        # that have actually been assigned.
        #
        # Forward checking is the orthogonal mechanism that additionally
        # prunes the domains of *unassigned* neighbours.
        if not assignment:
            return True

        constraint = self.constraints[variable]
        for neighbour in self.neighbours[variable]:
            if neighbour not in assignment:
                continue
            neighbour_value = assignment[neighbour]
            if not constraint(variable, value, neighbour, neighbour_value):
                return False
        return True

    # ------------------------------------------------------------------
    # Private heuristic helpers
    # ------------------------------------------------------------------

    def _select_mrv(self, assignment: Assignment) -> Optional[States]:
        """Minimum-Remaining-Values selection, optionally tie-broken by
        the degree heuristic. See L07 §4.2.

        We count *legal* remaining values dynamically: for each value
        currently in ``self.domains[v]`` we test it against the existing
        partial assignment via ``is_consistent``. This is the textbook
        MRV (R&N §6.3.2) — it gives MRV meaningful work to do even when
        forward checking is OFF (without dynamic counting MRV would
        degenerate to declaration-order selection on a uniform-domain
        CSP because ``len(self.domains[v])`` would be the same constant
        for every unassigned variable).
        """
        unassigned = [v for v in self.variables if v not in assignment]
        if not unassigned:
            return None

        def legal_value_count(v: States) -> int:
            # Count how many values in the *live* domain are still
            # consistent with the current partial assignment. With FC
            # off, self.domains[v] is the declared domain; with FC on,
            # it is the already-pruned live domain.
            return sum(
                1 for val in self.domains[v]
                if self.is_consistent(v, val, assignment)
            )

        def degree(v: States) -> int:
            # Number of constraints (neighbours) on STILL-UNASSIGNED
            # variables. Higher is more constraining.
            return sum(1 for n in self.neighbours[v] if n not in assignment)

        # Smallest legal-value count first; if degree tie-break is
        # enabled, then *largest* degree wins among the MRV-tied
        # variables (we negate degree because Python sorts ascending).
        if USE_DEGREE_TIEBREAK:
            unassigned.sort(key=lambda v: (legal_value_count(v), -degree(v)))
        else:
            unassigned.sort(key=legal_value_count)
        return unassigned[0]

    def _lcv_count(self, variable: States, value: Color, assignment: Assignment) -> int:
        """How many neighbour-domain values would this value rule out?
        Lower count == less constraining == try first. See L07 §4.3.

        For the (variable, neighbour) pair we consult the per-variable
        constraint entries from both endpoints. In this map-colouring
        CSP every entry of ``self.constraints`` is the same not-equal
        predicate, so the result is identical regardless of which key
        we look up — but checking *both* keeps the LCV count honest
        if a future variant introduces asymmetric per-variable
        constraints (e.g. "Brazil cannot be Red" stored at
        ``self.constraints[Brazil]``).

        We count only neighbour-values that are still legal under the
        current partial assignment so LCV does meaningful work even
        without forward checking (without dynamic counting the score
        would be the same constant for every candidate on a uniform-
        domain CSP).
        """
        constraint_v = self.constraints[variable]
        ruled_out = 0
        for neighbour in self.neighbours[variable]:
            if neighbour in assignment:
                continue
            constraint_n = self.constraints[neighbour]
            for nv in self.domains[neighbour]:
                # Skip neighbour-values that are already inconsistent
                # with the current partial assignment — they would have
                # been ruled out anyway.
                if not self.is_consistent(neighbour, nv, assignment):
                    continue
                # ``value`` rules out ``nv`` if either endpoint's
                # constraint rejects the pair.
                if (
                    not constraint_v(variable, value, neighbour, nv)
                    or not constraint_n(neighbour, nv, variable, value)
                ):
                    ruled_out += 1
        return ruled_out

    def _forward_check(
        self,
        variable: States,
        value: Color,
        assignment: Assignment,
    ) -> Tuple[Dict[States, List[Color]], bool]:
        """Forward-checking prune of each unassigned neighbour's domain.
        Returns (snapshot-of-pruned-domains, all-domains-non-empty).

        For every unassigned neighbour ``Y`` and every candidate value
        ``ny`` in ``Y``'s live domain we test
        ``constraint(variable, value, Y, ny)`` and remove ``ny`` from
        ``Y``'s domain when the constraint rejects it. This is the
        textbook forward-checking step (L07 §4.4): "for each unassigned
        variable Y connected to X, remove from D_Y any value
        inconsistent with X = value".

        Note this is the *general* form — for a not-equal constraint it
        happens to remove just ``value`` itself, but for other binary
        constraints (e.g. ``<``, ``|x - y| != d``, n-queens diagonals)
        the prune removes *every* clashing value, not only the literal
        ``value`` we just assigned.

        The snapshot is handed back to ``_restore_domains`` so the
        caller can revert prunes cleanly on backtrack (and on success
        — see the caller).
        """
        constraint = self.constraints[variable]
        snapshot: Dict[States, List[Color]] = {}
        for neighbour in self.neighbours[variable]:
            if neighbour in assignment:
                continue
            original_domain = self.domains[neighbour]
            pruned_domain = [
                ny for ny in original_domain
                if constraint(variable, value, neighbour, ny)
            ]
            if len(pruned_domain) < len(original_domain):
                # Save a shallow copy of the pre-prune domain so we
                # can revert *exactly* (a deep copy is unnecessary
                # because Color enum members are singletons). The
                # snapshot is captured BEFORE the in-place assignment
                # so a wiped-out neighbour also gets its pre-prune
                # domain into the snapshot, ready for restore.
                snapshot[neighbour] = original_domain[:]
                self.domains[neighbour] = pruned_domain
                if not pruned_domain:
                    # Empty domain detected -> immediate failure. We
                    # still return the snapshot so the caller can
                    # restore *partial* prunes done before the wipe
                    # (including this wiped neighbour itself).
                    return snapshot, False
        return snapshot, True

    def _restore_domains(self, snapshot: Dict[States, List[Color]]) -> None:
        for variable, original_domain in snapshot.items():
            self.domains[variable] = original_domain

    # ------------------------------------------------------------------
    # Optional AC-3 pre-pass (Homework Challenge — arc consistency)
    # ------------------------------------------------------------------

    def ac3(self) -> bool:
        """Enforce arc consistency on the whole CSP before search.

        Returns False if any domain wipes out (problem infeasible),
        True otherwise. Mutates ``self.domains`` in place. The entry-
        point script does NOT call this by default (it would
        side-effect the printed backtrack counts); it is exposed so
        future variants can compose AC-3 with backtracking.
        """
        # Build the initial worklist of arcs (X -> Y) for every
        # neighbour pair.
        queue: deque[Tuple[States, States]] = deque()
        for x in self.variables:
            for y in self.neighbours[x]:
                queue.append((x, y))

        while queue:
            x, y = queue.popleft()
            if self._revise(x, y):
                if not self.domains[x]:
                    return False
                # Re-queue every arc Z -> X (Z != Y) because
                # shrinking D_x may break their support.
                for z in self.neighbours[x]:
                    if z != y:
                        queue.append((z, x))
        return True

    def _revise(self, x: States, y: States) -> bool:
        """Remove from D_x any value with no support in D_y. Returns
        True iff D_x changed.

        For the (x, y) arc we ask both endpoints' constraint functions
        to approve the pair. In this map-colouring CSP every entry of
        ``self.constraints`` is the same not-equal predicate, so the
        result is identical regardless of which key we consult — but
        querying both is the honest semantics for a constraint over a
        *pair* (L07 §3.1 defines a constraint as ``<scope, rel>`` where
        the relation is over the scope, not owned by one variable).
        """
        revised = False
        constraint_x = self.constraints[x]
        constraint_y = self.constraints[y]

        def pair_ok(vx: Color, vy: Color) -> bool:
            return (
                constraint_x(x, vx, y, vy)
                and constraint_y(y, vy, x, vx)
            )

        new_domain: List[Color] = []
        for vx in self.domains[x]:
            # A value vx has support iff *some* vy in D_y satisfies
            # the constraint with it.
            if any(pair_ok(vx, vy) for vy in self.domains[y]):
                new_domain.append(vx)
            else:
                revised = True
        self.domains[x] = new_domain
        return revised


# ----------------------------------------------------------------------
# Map factories
# ----------------------------------------------------------------------


def _make_not_equal_constraints(variables: List[States]) -> Dict[States, contraintFunction]:
    """Build a {variable: not-equal-predicate} dict.

    The constraint is **not-equal** for map colouring: two neighbouring
    regions must hold different colours. We mirror the template's
    convention: one entry per variable (the dictionary lookup happens
    in is_consistent / _lcv_count and is_consistent's loop over
    constraints.values() walks every entry).
    """

    def constraint_function(
        first_variable: States,
        first_value: Color,
        second_variable: States,
        second_value: Color,
    ) -> bool:
        """Returns true if neighbouring variables have different
        values (or if the comparison is degenerate, i.e. a variable
        against itself)."""
        return first_value != second_value or first_variable == second_variable

    return {v: constraint_function for v in variables}


def create_australia_csp() -> CSP:
    """Original lab example — Australia with 3 colours (default).

    Signature preserved from the template (Reviewer #1).
    """
    variables = [
        States.WA, States.Q, States.T, States.V,
        States.SA, States.NT, States.NSW,
    ]
    # Why ACTIVE_COLORS rather than a hard-coded [Red, Green, Blue]?
    # The whole point of the KNOB is to let the variant runner switch
    # colour palettes without editing this function.
    values = list(ACTIVE_COLORS)
    domains = {v: values[:] for v in variables}

    # Adjacency from the original lab template (Lab 6.pdf slide 1
    # implicit map). Tasmania (T) is an island with no neighbours;
    # leaving its list empty exercises the "isolated variable" case.
    neighbours = {
        States.WA: [States.SA, States.NT],
        States.Q: [States.SA, States.NT, States.NSW],
        States.T: [],
        States.V: [States.SA, States.NSW],
        States.SA: [States.WA, States.NT, States.Q, States.NSW, States.V],
        States.NT: [States.SA, States.WA, States.Q],
        States.NSW: [States.SA, States.Q, States.V],
    }

    constraints = _make_not_equal_constraints(variables)
    return CSP(variables, domains, neighbours, constraints)


def create_south_america_csp() -> CSP:
    """Exercise 2 — South America with the active colour palette.

    Adjacency taken from Lab 6.pdf slide 4 (the South-America map):
    - Colombia borders: Venezuela, Brazil, Peru, Ecuador
    - Venezuela borders: Colombia, Guyana, Brazil
    - Guyana borders: Venezuela, Suriname, Brazil
    - Suriname borders: Guyana, French Guyana, Brazil
    - French Guyana borders: Suriname, Brazil
    - Ecuador borders: Colombia, Peru
    - Peru borders: Ecuador, Colombia, Brazil, Bolivia, Chile
    - Brazil borders: Colombia, Venezuela, Guyana, Suriname,
                      French Guyana, Peru, Bolivia, Paraguay,
                      Argentina, Uruguay
    - Bolivia borders: Peru, Brazil, Paraguay, Argentina, Chile
    - Paraguay borders: Bolivia, Brazil, Argentina
    - Chile borders: Peru, Bolivia, Argentina
    - Argentina borders: Chile, Bolivia, Paraguay, Brazil, Uruguay
    - Uruguay borders: Brazil, Argentina
    """
    S = States
    variables = [
        S.COLOMBIA, S.VENEZUELA, S.GUYANA, S.SURINAME, S.FRENCH_GUYANA,
        S.ECUADOR, S.PERU, S.BRAZIL, S.BOLIVIA, S.PARAGUAY,
        S.CHILE, S.ARGENTINA, S.URUGUAY,
    ]
    values = list(ACTIVE_COLORS)
    domains = {v: values[:] for v in variables}

    neighbours: Dict[States, List[States]] = {
        S.COLOMBIA: [S.VENEZUELA, S.BRAZIL, S.PERU, S.ECUADOR],
        S.VENEZUELA: [S.COLOMBIA, S.GUYANA, S.BRAZIL],
        S.GUYANA: [S.VENEZUELA, S.SURINAME, S.BRAZIL],
        S.SURINAME: [S.GUYANA, S.FRENCH_GUYANA, S.BRAZIL],
        S.FRENCH_GUYANA: [S.SURINAME, S.BRAZIL],
        S.ECUADOR: [S.COLOMBIA, S.PERU],
        S.PERU: [S.ECUADOR, S.COLOMBIA, S.BRAZIL, S.BOLIVIA, S.CHILE],
        S.BRAZIL: [
            S.COLOMBIA, S.VENEZUELA, S.GUYANA, S.SURINAME, S.FRENCH_GUYANA,
            S.PERU, S.BOLIVIA, S.PARAGUAY, S.ARGENTINA, S.URUGUAY,
        ],
        S.BOLIVIA: [S.PERU, S.BRAZIL, S.PARAGUAY, S.ARGENTINA, S.CHILE],
        S.PARAGUAY: [S.BOLIVIA, S.BRAZIL, S.ARGENTINA],
        S.CHILE: [S.PERU, S.BOLIVIA, S.ARGENTINA],
        S.ARGENTINA: [S.CHILE, S.BOLIVIA, S.PARAGUAY, S.BRAZIL, S.URUGUAY],
        S.URUGUAY: [S.BRAZIL, S.ARGENTINA],
    }

    constraints = _make_not_equal_constraints(variables)
    return CSP(variables, domains, neighbours, constraints)


def create_distance_csp() -> CSP:
    """Variant 3 — distance-based adjacency.

    Demo coordinate layout (an arbitrary five-region toy map):

        A(0,0)   B(2,0)
           \\     /
            C(1,1)
           /     \\
        D(0,2)   E(2,2)

    Any two regions whose Euclidean distance is <= DISTANCE_THRESHOLD
    become adjacent and must therefore differ in colour.

    We reuse five enum members from States_solution.py (WA..V) as
    abstract region IDs — naming is irrelevant, only adjacency
    matters.
    """
    region_xy: Dict[States, Tuple[float, float]] = {
        States.WA: (0.0, 0.0),  # "A"
        States.NT: (2.0, 0.0),  # "B"
        States.Q:  (1.0, 1.0),  # "C"  -- the hub
        States.NSW:(0.0, 2.0),  # "D"
        States.V:  (2.0, 2.0),  # "E"
    }

    variables = list(region_xy.keys())
    values = list(ACTIVE_COLORS)
    domains = {v: values[:] for v in variables}

    def euclid(a: Tuple[float, float], b: Tuple[float, float]) -> float:
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

    neighbours: Dict[States, List[States]] = {v: [] for v in variables}
    for i, vi in enumerate(variables):
        for vj in variables[i + 1:]:
            if euclid(region_xy[vi], region_xy[vj]) <= DISTANCE_THRESHOLD:
                neighbours[vi].append(vj)
                neighbours[vj].append(vi)

    constraints = _make_not_equal_constraints(variables)
    return CSP(variables, domains, neighbours, constraints)


def create_csp() -> CSP:
    """Dispatch on MAP_NAME so the entry point stays a single call."""
    if MAP_NAME == "australia":
        return create_australia_csp()
    if MAP_NAME == "south_america":
        return create_south_america_csp()
    if MAP_NAME == "distance_demo":
        return create_distance_csp()
    raise ValueError(
        f"Unknown MAP_NAME={MAP_NAME!r}. "
        "Set MAP_NAME to one of: 'australia', 'south_america', 'distance_demo'."
    )


# ----------------------------------------------------------------------
# Entry-point harness
# ----------------------------------------------------------------------


def _print_report(csp: CSP, result: Optional[Assignment]) -> None:
    colour_names = ", ".join(c.name for c in ACTIVE_COLORS)
    print("=== Lab 6 — CSP / Map Colouring ===")
    print(f"Map:                 {MAP_NAME}")
    print(f"Active colours:      {colour_names}")
    print(
        f"Heuristics:          "
        f"MRV={USE_MRV}  Degree={USE_DEGREE_TIEBREAK}  "
        f"LCV={USE_LCV}  FC={USE_FORWARD_CHECK}  AC3={USE_AC3}"
    )
    print(f"Recursive calls:     {csp._recursive_calls}")
    print(f"Backtracks:          {csp._backtracks}")
    if result is None:
        print("NO SOLUTION — the active colour palette is too small "
              "for this map's chromatic number.")
        return
    # Print sorted by the States enum's integer value (States_solution
    # provides __lt__) so output is deterministic across runs.
    for area, color in sorted(result.items()):
        # str(area) -> "States.NT" etc. (matches original template).
        print("{}: {}".format(area, color))


def _domain_value_total(csp: CSP) -> int:
    """Total count of values across every variable's live domain.

    Used to report whether AC-3 actually pruned anything (the
    difference between before and after the pre-pass).
    """
    return sum(len(dom) for dom in csp.domains.values())


if __name__ == "__main__":
    # Default run reproduces the original lab exactly: Australia,
    # 3 colours, no heuristics. Flip any KNOB at the top of this file
    # to switch into a variant configuration.
    csp = create_csp()

    # USE_AC3: run AC-3 as a pre-pass before backtracking (Variant 5).
    # The pre-pass mutates csp.domains in place — backtracking then
    # operates on the (possibly) reduced domains.
    if USE_AC3:
        before = _domain_value_total(csp)
        ac3_feasible = csp.ac3()
        after = _domain_value_total(csp)
        pruned = before - after
        print(
            f"AC-3 pre-pass:       "
            f"feasible={ac3_feasible}  values_pruned={pruned}"
        )
        if not ac3_feasible:
            # AC-3 already proved infeasibility -- skip the backtrack
            # search entirely and print the report from a fresh CSP
            # (so the Recursive calls / Backtracks line is honestly
            # 0 / 0 rather than carrying garbage from a not-run
            # search).
            _print_report(csp, None)
            raise SystemExit(0)

    solution = csp.backtracking_search()
    _print_report(csp, solution)

    # Check at https://mapchart.net/australia.html
    # (or https://mapchart.net/world.html for South America)

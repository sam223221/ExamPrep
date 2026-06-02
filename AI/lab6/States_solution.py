"""
LAB 6 — CSP (Map Colouring): Region / "States" enumeration (solution)
=====================================================================

PROBLEM STATEMENT (from Lab 6.pdf):
-----------------------------------
The original lab uses the seven Australian states/territories
(WA, NT, Q, NSW, V, SA, T). Exercise 2 of the handout asks us to
colour the map of South America (Lab 6.pdf, slide 4): Colombia,
Venezuela, Guyana, Suriname, French Guyana (Fr), Ecuador, Peru,
Brazil, Bolivia, Paraguay, Chile, Argentina, Uruguay. This module
defines an Enum member for every region on either map; the entry
point picks the active subset via the MAP_NAME knob.

MENTAL MODEL (one-line analogy):
--------------------------------
Each enum member is a *named cell* in a colouring book — the cells
themselves never change, only the colour we drop in. This module is
the colouring-book outline.

REFERENCES:
-----------
- Lecture 7 §3 "Variables (CSP)" — see study/lectures/L07-CSP.md
- Glossary: "Constraint Satisfaction Problem (CSP)" defines the
  variable set $X_1, \\dots, X_n$.

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
1. To use **Australia** (default lab): the entry point picks the
   AUSTRALIA_REGIONS subset. No edit here.
2. To use **South America** (Exercise 2 + variant 1 "different map"):
   the entry point picks the SOUTH_AMERICA_REGIONS subset. No edit.
3. To add a *new* map (e.g. Iceland regions): add new enum members
   below with unique integer values, then in the entry point add
   - a regions list,
   - a neighbours dict,
   - a builder function.
   The solver itself does not need to change.

OUTPUTS WHEN RUN:
-----------------
This module produces no console output when imported. It is a data-
only module.

ENTRY POINT: no
---------------
Imported by constraints_template_solution.py (the entry point).
"""

from enum import Enum


class States(Enum):
    # ---- Australia (original lab) ----------------------------------
    WA = 1
    NT = 2
    Q = 3
    NSW = 4
    V = 5
    SA = 6
    T = 7

    # ---- South America (Exercise 2) -------------------------------
    # KNOB: ADJACENT MEMBERS may be added here. Numeric values are
    #       arbitrary identifiers — they do NOT encode adjacency.
    #       Adjacency is declared explicitly in the entry point's
    #       `neighbours` dict.
    COLOMBIA = 11
    VENEZUELA = 12
    GUYANA = 13
    SURINAME = 14
    FRENCH_GUYANA = 15
    ECUADOR = 16
    PERU = 17
    BRAZIL = 18
    BOLIVIA = 19
    PARAGUAY = 20
    CHILE = 21
    ARGENTINA = 22
    URUGUAY = 23

    # ---- Comparison helpers (unchanged from template) --------------
    # Why these are needed: the entry-point printout uses
    # ``sorted(result.items())`` which requires the keys (States enum
    # members) to be orderable.

    def __lt__(self, other):
        # Why: enable stable sorting of mixed-map result dicts.
        if type(other) != type(self):
            return False
        return self.value < other.value

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.value == other.value

    def __hash__(self):
        # Why: dict keys must be hashable; we hash on the repr so the
        # value stays distinct per member.
        return hash(repr(self))

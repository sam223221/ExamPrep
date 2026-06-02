"""
LAB 6 — CSP (Map Colouring): Colour-palette module (solution)
=============================================================

PROBLEM STATEMENT (from Lab 6.pdf, Exercise 2 + Variants):
----------------------------------------------------------
The original lab uses three colours (Red, Green, Blue) for Australia.
Exercise 2 of the handout asks us to colour the map of South America
using **four** colours (Red, Green, Blue, Yellow). The variant bank
(study/_exam/Lab6-CSP/variants.md, Variant 2) further asks "Add a 5th
colour to the palette" — so we expose all five colours here. The
KNOB ``ACTIVE_COLORS`` in constraints_template_solution.py decides
which subset of this palette becomes each variable's domain.

MENTAL MODEL (one-line analogy):
--------------------------------
The colour palette is the box of crayons sitting on the desk. The
problem (map) decides which crayons we are *allowed* to use; the box
itself may hold spares.

REFERENCES:
-----------
- Lecture 7 §3 "Domain (CSP)" — see study/lectures/L07-CSP.md
- Glossary: "Constraint Satisfaction Problem (CSP)" (uses $D_i$ for
  the domain of variable $X_i$).

HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS:
--------------------------------------------------
1. To run the **default 3-colour Australia** lab: leave ACTIVE_COLORS
   in the entry-point file set to [Red, Green, Blue].
2. To run **Exercise 2 (4-colour South America)**: set ACTIVE_COLORS
   to [Red, Green, Blue, Yellow].
3. To run **variant 2 (add a 5th colour)**: set ACTIVE_COLORS to
   [Red, Green, Blue, Yellow, Purple]. Purple is defined below so the
   entry point can flip a single KNOB without editing this module.
4. To add a *sixth* colour for a homemade variant: append another
   Enum member here (e.g. Orange = "Orange"). The CSP machinery makes
   no other assumption about colour identity.

OUTPUTS WHEN RUN:
-----------------
This module produces no console output when imported. It is a data-
only module.

ENTRY POINT: no
---------------
Imported by constraints_template_solution.py (which is the entry
point) and by States_solution.py (no direct use, but lives next to
it for convenience).
"""

from enum import Enum


class Color(Enum):
    # KNOB: COLOR palette membership (default = 5 members; the entry
    #       point picks the active subset via ACTIVE_COLORS).
    #   What it does: defines the universe of colours the solver can
    #     assign to map regions. The entry point's ACTIVE_COLORS list
    #     selects which of these are actually used.
    #   Effect: more colours -> more freedom -> fewer backtracks.
    #     With 4 colours every planar map is provably colourable
    #     (Four-Colour Theorem); with 3 colours some maps (e.g.
    #     South America with Brazil bordering 10 neighbours) become
    #     unsolvable.
    #   Exam variants:
    #     - 3 colours (default Australia): [Red, Green, Blue]
    #     - 4 colours (Exercise 2, South America): + Yellow
    #     - 5 colours (variant 2 "add a 5th colour"): + Purple
    Red = "Red"
    Green = "Green"
    Blue = "Blue"
    Yellow = "Yellow"
    Purple = "Purple"

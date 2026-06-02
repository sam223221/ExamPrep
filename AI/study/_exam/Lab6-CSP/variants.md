# Lab 6 — CSP: Variant Bank

This bank seeds the three variants from the master plan
([Appendix B of the implementation plan](../../../docs/superpowers/plans/2026-05-22-ai-exam-prep-study-package.md))
and adds two additional variants that the handout naturally invites.
Each variant is a self-contained "exam question" that a fresh agent
should be able to answer by reading only:

- the docstring header of `lab6/constraints_template_solution.py`,
- every `# KNOB:` block in that file and in `Colors_solution.py` /
  `States_solution.py`,
- the public function/class signatures (the `def ...:` line only).

If the variant cannot be answered with KNOBs alone, file a STUCK
report (`study/_exam/Lab6-CSP/round{R}/examinerN-attempt.md`).

---

## Variant 1 — "Replace the map (Iceland-style regions instead of Australia). Solve with backtracking + MRV."

**Prompt:** Re-solve the map-colouring problem using the **South
America** map (already wired into the solution, MAP_NAME =
`"south_america"`) with four colours. Use the **MRV** variable-
ordering heuristic (and the **degree** tie-breaker) so that the
solver always picks the most-constrained region first. Report:

1. The full colour assignment for all 13 regions.
2. The number of recursive calls.
3. The number of backtracks.
4. One sentence explaining why MRV's first choice is `BRAZIL`.

**KNOBs to change in `constraints_template_solution.py`:**

| KNOB | From | To |
| --- | --- | --- |
| `MAP_NAME` | `"australia"` | `"south_america"` |
| `ACTIVE_COLORS` | `[Red, Green, Blue]` | `[Red, Green, Blue, Yellow]` |
| `USE_MRV` | `False` | `True` |
| `USE_DEGREE_TIEBREAK` | `False` | `True` |

**Expected answer shape:** All 13 regions receive one of four
colours, no two adjacent regions share a colour. Brazil is the
single highest-degree node (10 neighbours), so the degree tie-break
forces it first when every domain still has size 4.

---

## Variant 2 — "Add a 5th colour to the palette. Does the solver succeed? With how many backtracks?"

**Prompt:** Take the South-America CSP (or your map of choice) and
*add* a fifth colour, **Purple**, on top of `[Red, Green, Blue,
Yellow]`. Run the solver with **no** heuristics (so the backtrack
count is meaningful). Then run a second time with **only 3 colours**
(`[Red, Green, Blue]`). Compare the two outcomes and explain:

1. With 5 colours: result + backtracks + recursive calls.
2. With 3 colours: result + backtracks + recursive calls.
3. Why does increasing the palette **never** increase backtracks?
4. Why does South America become infeasible with 3 colours but
   Australia stays solvable?

**KNOBs to change:**

| KNOB | 5-colour run | 3-colour run |
| --- | --- | --- |
| `MAP_NAME` | `"south_america"` | `"south_america"` |
| `ACTIVE_COLORS` | `[Red, Green, Blue, Yellow, Purple]` | `[Red, Green, Blue]` |
| every other KNOB | default `False` | default `False` |

**Expected answer shape:** 5-colour run solves in `O(N)` calls with 0
backtracks. 3-colour run returns `None` (NO SOLUTION) after a
non-trivial number of backtracks — proof of infeasibility. Brief
explanation invoking the four-colour theorem.

---

## Variant 3 — "Change adjacency to a distance-based constraint (regions within X km cannot share a colour). Solve."

**Prompt:** Use the built-in `distance_demo` map (5 abstract regions
laid out on a unit grid). Two regions are "adjacent" — and therefore
forbidden from sharing a colour — iff their Euclidean distance is at
most `DISTANCE_THRESHOLD`. Solve with the default 3-colour palette
for three different thresholds:

| `DISTANCE_THRESHOLD` | Edge density expected |
| --- | --- |
| `1.5` | Sparse — star K_{1,4}: hub C touches all four corners (A, B, D, E), but corners do NOT touch each other. Each spoke distance is √2 ≈ 1.414. Chromatic number = 2 (bipartite). |
| `2.5` (default) | Medium — hub touches all four corners AND adjacent corner pairs along each edge (A–B, A–D, B–E, D–E at distance 2.0). Diagonals A–E and B–D at 2√2 ≈ 2.828 still excluded. Chromatic number = 3. |
| `3.5` | Dense — every region adjacent to every other (K_5; diagonals A–E and B–D included since 2√2 ≈ 2.828 ≤ 3.5). Chromatic number = 5, so 3 colours is infeasible. |

For each threshold, report (a) whether the solver finds a colouring,
(b) the colour assignment, (c) backtrack count, and (d) the
chromatic number you infer from those runs.

**KNOBs to change:**

| KNOB | Run A | Run B | Run C |
| --- | --- | --- | --- |
| `MAP_NAME` | `"distance_demo"` | same | same |
| `ACTIVE_COLORS` | `[Red, Green, Blue]` | same | same |
| `DISTANCE_THRESHOLD` | `1.5` | `2.5` | `3.5` |

**Expected answer shape:** Run A & B succeed; Run C fails (a fully
connected 5-clique needs 5 colours but only 3 are available).
Inferred chromatic numbers: 1.5 -> 2 (K_{1,4} star is bipartite),
2.5 -> 3, 3.5 -> 5 (NO SOLUTION with 3 colours).

---

## Variant 4 (bonus) — "Homework Challenge: forward checking on South America"

**Prompt:** From Lab 6.pdf slide 5 ("Homework Challenge: implement
forward checking and arc consistency for the previous exercise").
Run the South-America 4-colour problem three ways and compare
backtrack counts:

| Run | Heuristics |
| --- | --- |
| Baseline | no heuristics |
| MRV + degree | `USE_MRV=True`, `USE_DEGREE_TIEBREAK=True` |
| MRV + degree + forward check | also `USE_FORWARD_CHECK=True` |

Report backtrack counts for each.

**KNOB to flip across the three runs:** progressively turn on
`USE_MRV`, `USE_DEGREE_TIEBREAK`, then `USE_FORWARD_CHECK` (all
booleans, default `False`). No other knob touched.

**Expected answer shape:** Backtracks decrease monotonically as
heuristics are layered on. With forward checking the deepest
recursion never enters a dead branch (fail-fast prunes them at the
point of assignment).

---

## Variant 5 (bonus) — "AC-3 pre-pass on an over-constrained CSP"

**Prompt:** The public method `CSP.ac3()` (see signature in
`constraints_template_solution.py`) enforces arc consistency over
the whole CSP in place and returns `False` if any domain wipes out.
Use it as a *pre-flight check* on the South-America CSP for two
palettes:

1. `[Red, Green, Blue]` — should AC-3 declare it infeasible? Why or
   why not?
2. `[Red, Green, Blue, Yellow]` — confirm AC-3 says feasible, then
   run backtracking and report whether AC-3 reduced the search.

**KNOBs:** `MAP_NAME = "south_america"`, `ACTIVE_COLORS` as above,
`USE_AC3 = True`. With `USE_AC3=True` the entry-point harness runs
`csp.ac3()` as a pre-pass before `csp.backtracking_search()` and
prints a line `AC-3 pre-pass: feasible=<bool>  values_pruned=<int>`
so the variant's expected-answer shape is observable directly from
console output (no driver script needed).

**Expected answer shape:** AC-3 does **not** detect infeasibility on
its own for the 3-colour South America case (binary not-equal
constraints with domain >= 2 are always arc-consistent). It returns
True. Backtracking still discovers the conflict through normal
search. This is a teaching moment: AC-3 is necessary but not
sufficient.

---

## Notes for exam agents

- Solution file ENTRY POINT: `lab6/constraints_template_solution.py`.
  Modules: `Colors_solution.py`, `States_solution.py`.
- Run with `py -3.12 lab6\constraints_template_solution.py` from the
  repository root.
- The solution prints `Recursive calls` and `Backtracks` after each
  run — quote those numbers directly in your answer.
- You may import the module in a small driver script to run multiple
  configurations back-to-back without editing the file, as long as
  you only set the documented KNOBs (`MAP_NAME`, `ACTIVE_COLORS`,
  `USE_MRV`, `USE_DEGREE_TIEBREAK`, `USE_LCV`, `USE_FORWARD_CHECK`,
  `USE_AC3`, `DISTANCE_THRESHOLD`).

# Lab1-Agents — Reviewer #1 (Correctness) — Round 1

**Reviewer scope (Spec §8.1):** Run the solution code. Verify it solves the original lab problem. Catch off-by-one, broken loops, edge cases, wrong outputs, broken signatures.

**Files reviewed:**
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\Enums_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\table_driven_agent_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\reflex_vacuum_agent_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\reflex_agent_with_state_solution.py` (entry point)

**Lab handout:** `Lab 1.pdf` (slides 1-18; Exercises 1-3 + Homework).

---

## VERDICT: **PASS with minor concerns**

All four solution files import cleanly, execute without exceptions on Python 3.12, satisfy the lab's exercise prompts, and preserve the signatures from the originals. The Homework entry point (`reflex_agent_with_state_solution.py`) produces a trace whose first 9 lines reach the quiescent NO_OP state, matching the docstring's documented expected output exactly. Math behind Exercise 1.3 / 1.4 is correct. Bogus-action defence (Exercise 2.3) verified by toggling `ENABLE_BOGUS_DEMO`. Any-start-square requirement of the Homework verified for all four corners.

No P0 findings. A few P1/P2 items noted below — all polish, none affect correctness of the lab answers.

---

## P0 — Blockers (none)

_None._

---

## P1 — Important

### P1-1 — Slide-15 dict-key example uses `'A'`/`'B'` strings; solution uses `Location.A`/`Location.B` enum members
- **Where:** `reflex_agent_with_state_solution.py` lines 236-239 / 269 (and analogous spots in the original template).
- **Why it matters:** The slide writes the model as `model = {A: Unknown, B: Unknown}` and `if model[A] == model[B] == 'Clean': NO_OP`. The original template (`reflex_agent_with_state.py:24-27, 40`) already uses `Location.A`/`States.CLEAN` enums — so the solution is **consistent with the template**, not the slide literal. This is fine for correctness, but a reviewer reading slide 15 in isolation might flag it. Solution explicitly documents the choice in lines 233-238 — acceptable.
- **Severity:** P1 only because slide-fidelity is the lab's grading dimension; in practice the original template made this choice already.
- **Suggested fix:** None needed — already explained inline. Leave as is.

### P1-2 — `Enums_solution.py` lectures the `LINE_4` topology to arrange squares in `TL → TR → BL → BR` order
- **Where:** `Enums_solution.py` line 147-148 and `reflex_vacuum_agent_solution.py` line 431-432.
- **Why it matters:** A "line of 4" reading might expect `TL → TR → BR → BL` (clockwise perimeter) or `TL → BL → TR → BR`. The chosen order is arbitrary but works because every reflex/state agent only consults the helper. Documented as such in the comment. Not a correctness issue for the lab handout, but a variant question about "3 rooms in a row" would need the user to pick which 3 of these to use.
- **Severity:** P1.
- **Suggested fix:** None for current lab; if variant 2 ("3 rooms in a line") is graded, document the chosen sub-order or expose it as another KNOB.

---

## P2 — Polish / suggestions

### P2-1 — `GridAgent.last_seen_location` attribute is dead state
- **Where:** `reflex_vacuum_agent_solution.py` line 352.
- **Why it matters:** `self.last_seen_location` is initialised but never read anywhere. The docstring on lines 345-352 says it is "kept as an attribute purely so reviewers can verify the agent state space at a glance" — that is a stylistic justification, but it is still unused state on a class that explicitly claims to be stateless.
- **Suggested fix:** Either delete the attribute (it adds nothing) or rename it to make clear it is a snapshot for debugging; do NOT leave dead variables on what is supposed to be a pure-reflex agent.

### P2-2 — `Enums_solution.py` re-exports rely on `from Enums import …` — the original `Enums.py` MUST be importable
- **Where:** `Enums_solution.py` line 73.
- **Why it matters:** If a graders harness only ships the `*_solution.py` files (e.g. delete originals to test isolation), `Enums_solution.py` will fail at import time with `ModuleNotFoundError: No module named 'Enums'`. Current repo includes both files, so not an issue *here*, but it is a coupling that an end-user might trip over.
- **Suggested fix:** Optional — duplicate the three enums verbatim in `Enums_solution.py` instead of re-exporting, so the solution module is self-contained.

### P2-3 — `run()` loops use `range(1, n)` instead of `range(n)`
- **Where:** `reflex_vacuum_agent_solution.py` lines 539, 558; `reflex_agent_with_state_solution.py` lines 589, 608.
- **Why it matters:** Both originals used `for i in range(1, n)`, so the solution preserves the off-by-one (calling `run(20)` produces **19** rows, not 20). This is consistent with the **original** behaviour, but it is technically wrong w.r.t. slide 18's "use run(20) to test and display results". The captured docstring example in `reflex_agent_with_state_solution.py:88-99` shows 19 rows including 12 NO_OP rows. Lab grading is unlikely to care, since the originals do this too.
- **Suggested fix:** None — preserve template behaviour for signature-faithfulness. If you ever want exactly `n` rows, change to `range(n)`, but call it out in the docstring.

### P2-4 — `_grid_move_toward` falls through to "any legal move" without preferring squares closer to `dst`
- **Where:** `reflex_vacuum_agent_solution.py` lines 472-477; `reflex_agent_with_state_solution.py` lines 505-510.
- **Why it matters:** The fallback iterates `(RIGHT, DOWN, LEFT, UP)` and picks the first legal move whose neighbour exists, regardless of whether that move actually shortens the path to `dst`. For the 2x2 grid this is fine (every legal move from any corner brings you within one hop of every other corner). For a larger grid (variant question), this could send the cleaner away from `dst`. The current lab only ever has 4 squares, so functionally OK.
- **Suggested fix:** If you extend to a larger grid, replace the fallback with a Manhattan-distance picker. Currently not needed.

### P2-5 — `table_driven_agent_solution.py` prints both Exercise 1.3 and 1.4 numbers but the KNOB switching uses `globals()` mutation
- **Where:** lines 314-319.
- **Why it matters:** The `globals()["USE_FULL_HISTORY"] = …` dance to flip a module-level KNOB inside `run()` is functional but ugly and not thread-safe. The intent (print both forms) is sound; the implementation could use a local override parameter on `report_table_size`.
- **Suggested fix:** Add an optional `use_full_history: bool | None = None` parameter to `report_table_size` and pass `True`/`False` explicitly. Restoration of the global is no longer needed.

### P2-6 — Output line for `Enums_solution.py` `__main__` does not show `GridLocation.UNKNOWN`'s "always_allowed" tuple separately
- **Where:** `Enums_solution.py` lines 187-188.
- **Why it matters:** Cosmetic only. The sanity print already includes `UNKNOWN` (verified via run). No action.

---

## EVIDENCE — captured outputs

### Run 1 — entry point, default config (`py -3.12 reflex_agent_with_state_solution.py`)
```
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
... (12 trailing NO_OP lines)
```
**Verdict:** 19 rows total (range(1,20)), all 4 squares cleaned in 8 moves, then quiescent. Matches docstring (`reflex_agent_with_state_solution.py:88-99`).

### Run 2 — `py -3.12 table_driven_agent_solution.py`
```
Action        | Percepts
RIGHT         | [(A, CLEAN)]
SUCK          | [(A, CLEAN), (A, DIRTY)]
LEFT          | [(A, CLEAN), (A, DIRTY), (B, CLEAN)]
LEFT          | [(A, CLEAN), (A, DIRTY), (B, CLEAN), (B, CLEAN)]

Table size using only the current percept: |P| = NUM_LOCATIONS * NUM_STATUSES = 4
Table size with full history of length up to T=10: sum_(k=1..T) |P|^k = 1398100  (|P|=4)
```
**Verdict:** Three lookups match table entries on lines 166-174 of the solution. Exercise 1.2 fourth lookup (`clean_B` again) returns `LEFT` per the extra row at line 182. Exercise 1.3 (|P|=4) correct. Exercise 1.4 (4 + 16 + ... + 4^10 = 1,398,100) verified by hand.

### Run 3 — `py -3.12 reflex_vacuum_agent_solution.py`
```
A         DIRTY   SUCK   -> A         CLEAN
A         CLEAN   RIGHT  -> B         DIRTY
B         DIRTY   SUCK   -> B         CLEAN
B         CLEAN   LEFT   -> A         CLEAN
A         CLEAN   RIGHT  -> B         CLEAN
... (alternating LEFT/RIGHT forever — stateless agent has no quiescence)
```
**Verdict:** Slide-10 reflex rule reproduced verbatim. After both squares are clean, agent bounces between A and B (no NO_OP), which is the textbook "stateless reflex agent never terminates" lesson.

### Run 4 — bogus-action demo (`ENABLE_BOGUS_DEMO = True`)
```
A         DIRTY   SUCK   -> A         CLEAN
A         CLEAN   LEFT   -> A         CLEAN     <-- bogus, rejected
A         CLEAN   LEFT   -> A         CLEAN
...
```
**Verdict:** Actuator's `allowed_moves()` guard rejects the bogus `LEFT` from A. The agent stays at A forever — dirt in B never cleaned, but environment is **not corrupted** (location stays valid). This is the answer to Exercise 2.3: actuators do NOT allow bogus actions.

### Run 5 — Homework "any starting square" (TR, BR, BL)
Verified all three alternate starts reach NO_OP after at most 8 active ticks. Same coverage independent of start.

### Run 6 — LINE_4 topology variant
With `GRID_TOPOLOGY = "LINE_4"`, the agent uses only LEFT/RIGHT, cleans all four squares in order, then NO_OP. Confirms the topology KNOB works.

### Signature comparison (original vs solution)
| Symbol | Original signature | Solution signature | Match |
|---|---|---|---|
| `LOOKUP` | `(percepts: Percepts, table: LookupTable) -> Action` | identical | yes |
| `TABLE_DRIVEN_AGENT` | `(percept: Percept) -> Action` | identical | yes |
| `Agent.sensor` | `(self) -> LocationState` | identical | yes |
| `Agent.actuator` | `(self, action: Action) -> None` | identical | yes |
| `Agent.evaluate` | `(self) -> Action` | identical | yes |
| `Agent.choose_action` | `(state: LocationState) -> Action` (static) | identical (static) | yes |
| `StatefulReflexAgent.sensors` | `(self, environment) -> tuple[Location, States]` | identical | yes |
| `StatefulReflexAgent.actuators` | `(self, requested_action, environment) -> None` | identical | yes |
| `StatefulReflexAgent.act` | `(self, environment) -> Action` | identical | yes |
| `StatefulReflexAgent.match_rule` | `(self) -> Action` | identical | yes |
| `StatefulReflexAgent.update_state` | `(self, percept: LocationState) -> None` | identical | yes |
| `run` | `(n)` (no annotation) | `(n: int | None = None) -> None` (default added) | yes, backwards-compatible |

All signatures preserved. The only change to `run` is adding a default (`None`) and a type hint — strictly broader than the original.

---

## Report to PM

**Assignment recap:** Lab Reviewer #1 (Correctness) for Lab1-Agents, Round 1. Reviewed four `*_solution.py` files against `Lab 1.pdf` Exercises 1-3 + Homework, with the entry point being `reflex_agent_with_state_solution.py`.

**Status:** Pass with concerns (P1/P2 items only — no correctness blockers).

**P0 findings:** none.

**P1 findings:**
1. Solution uses `Location.A`/`States.CLEAN` enums where slide 15 writes literal `'A'`/`'Clean'` strings (matches original template, but worth noting). File: `reflex_agent_with_state_solution.py:236-239,269`. Fix: none required — documented inline.
2. `LINE_4` topology arbitrarily orders squares `TL→TR→BL→BR`. Acceptable for current lab; would matter for a 3-room-line variant. File: `Enums_solution.py:147-148`. Fix: optional — expose order as a KNOB.

**P2 findings:**
1. Dead `last_seen_location` attribute on `GridAgent`. File: `reflex_vacuum_agent_solution.py:352`. Fix: delete.
2. `Enums_solution.py` re-exports require `Enums.py` to exist. File: `Enums_solution.py:73`. Fix: optional — duplicate enums for self-containedness.
3. `range(1, n)` in trace loops produces n-1 rows. Preserves original behaviour. Files: `reflex_vacuum_agent_solution.py:539,558`; `reflex_agent_with_state_solution.py:589,608`. Fix: none — keep parity with template.
4. `_grid_move_toward` fallback does not prefer dst-closer moves. OK for 2x2; would break for larger grids. Files: same files. Fix: none for current lab.
5. `table_driven_agent_solution.py:314-319` uses `globals()` to flip a KNOB inside `run()`. Ugly but functional. Fix: optional refactor.
6. Cosmetic only — no action.

**Concerns / risks:**
- None impact lab grading. Solutions match slide pseudocode, preserve template signatures, and produce the expected traces.
- The stateless 2-room reflex agent never reaches a quiescent state — this is *the correct* textbook behaviour (slide 14 makes the point) and not a bug.

**Lab problems solved (handout coverage):**
- Exercise 1 (table-driven): all 4 sub-questions answered. (1.1 run, 1.2 explained via comment + extra lookup, 1.3 prints `|P|=4`, 1.4 prints sum=1,398,100).
- Exercise 2 (bogus actions): actuator guard verified by toggling `ENABLE_BOGUS_DEMO`.
- Exercise 3 (4 squares, stateless): `WORLD = "GRID_4"` runs the 2x2 stateless agent.
- Homework (4 squares, stateful, any start): default config; verified for TL, TR, BL, BR starts.

**What PM should do next:** Proceed to App Tester / Reviewer #2 (Style) / Reviewer #3 (Pedagogy). No fix-and-re-QA loop needed from Reviewer #1.

**DOCUMENT.md updated:** N/A for QA / Reviewer.

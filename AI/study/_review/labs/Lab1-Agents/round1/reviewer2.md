# Lab Reviewer #2 — KNOB Coverage Audit (Lab1-Agents, Round 1)

**Reviewer role:** Lab Reviewer #2 (KNOB Coverage) per Spec §8.1
**Files audited (4):**
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\Enums_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\table_driven_agent_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\reflex_vacuum_agent_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\reflex_agent_with_state_solution.py`
**Mandate:** every `# KNOB:` block must declare default + range + effect + variants; every magic number buried in a body is P0 unless justified.

---

## Verdict

**Status: Fail — Pass with concerns blocked by 2 P0 findings.**

The four files declare **23 KNOBs**. Eighteen are textbook-perfect; five fall short. More damaging, two **hidden magic-number off-by-ones** in the simulator loop silently shorten every trace by one step, contradicting the slide handout (`run(10)` is supposed to produce 10 ticks, not 9). Fix the P0 items first, then tighten the partial KNOBs.

---

## P0 — Hidden Magic Numbers / Broken Behaviour

### P0-1. `range(1, steps)` off-by-one in `run()` — stateless reflex
**File:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\reflex_vacuum_agent_solution.py`
**Lines:** 539 (GRID_4 branch) and 558 (ROOMS_2 branch)
```python
for _ in range(1, steps):
```
The literal `1` is a buried magic number AND wrong. `run(10)` (Exercise 2.2 explicitly says `run(10)`) executes 9 iterations, not 10. The KNOB `NUM_STEPS` claims to control "number of agent ticks `run()` simulates" — the implementation contradicts the contract.
**Fix:** `for _ in range(steps):` — or, if the slides demand 1-indexed step numbers in the trace, replace `1` with a documented `STEP_INDEX_BASE` KNOB.

### P0-2. Same off-by-one in the stateful entry-point
**File:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\reflex_agent_with_state_solution.py`
**Lines:** 589 (GRID_4) and 608 (ROOMS_2)
```python
for _ in range(1, steps):
```
Slide 18 says `run(20)` for the Homework. This file delivers 19 ticks. The captured "OUTPUTS WHEN RUN" docstring at lines 86–99 even shows the 8th line beginning to NO_OP, but the contract advertised by `NUM_STEPS: int = 20` is broken. The entry point of the lab is wrong.
**Fix:** identical — `for _ in range(steps):`.

---

## P1 — KNOB Hygiene Failures and Hidden Heuristic Constants

### P1-1. Hidden `'New':8s` width in `_print_header`
**Files:**
- `reflex_vacuum_agent_solution.py:517` — `print(f"{'Current':{loc_w + sta_w + act_w}s}{ARROW}{'New':8s}")`
- `reflex_agent_with_state_solution.py:557` — identical line.

The trace claims to be controlled by the `COLUMN_WIDTHS` knob, but the `8` for the "New" header is a hardcoded magic number that does NOT track `loc_w + sta_w`. Widen any column and the header misaligns. Should be `loc_w + sta_w` (computed) or a fourth KNOB entry.

### P1-2. Hardcoded directional tie-break ordering in `_grid_move_toward`
**Files:**
- `reflex_vacuum_agent_solution.py:463-464` — `(GridAction.LEFT, GridAction.RIGHT, GridAction.UP, GridAction.DOWN)`
- `reflex_vacuum_agent_solution.py:473-474` — `(GridAction.RIGHT, GridAction.DOWN, GridAction.LEFT, GridAction.UP)` (diagonal fallback)
- `reflex_agent_with_state_solution.py:498-499`, `506-507` — same.

These tuples are **heuristic preferences** that visibly determine the trace produced by the lab (which neighbour the cleaner steps to when multiple are legal). They are not declared as KNOBs even though `GRID_TRAVERSAL_ORDER` claims to control the traversal pattern. Variant questions asking "what if the cleaner prefers vertical-first?" cannot be answered by flipping any documented knob. Promote to `MOVE_PREFERENCE_PRIMARY` and `MOVE_PREFERENCE_FALLBACK` KNOBs.

### P1-3. `MIXED` initial-dirt split is hidden 2/4
**Files:**
- `reflex_vacuum_agent_solution.py:205-207`
- `reflex_agent_with_state_solution.py:530-532`
```python
return {
    GridLocation.TL: States.DIRTY, GridLocation.TR: States.DIRTY,
    GridLocation.BL: States.CLEAN, GridLocation.BR: States.CLEAN,
}
```
The KNOB doc says "first half dirty, rest clean" — but `INITIAL_DIRT="MIXED"` actually freezes the partition as "top row dirty / bottom row clean". The notion of "first half" is itself a hidden 2-out-of-4 magic number. Variant questions asking "only BR dirty" cannot be expressed. Add `MIXED_DIRTY_SQUARES: tuple[GridLocation, ...]` KNOB or rename `INITIAL_DIRT` to expose more presets.

### P1-4. KNOB `ARROW` in `reflex_agent_with_state_solution.py:552` is malformed
**File:** `reflex_agent_with_state_solution.py:550-552`
```python
# KNOB: ARROW (default="-> ", range=any short string)
#   Cosmetic separator drawn between "before" and "after" columns.
ARROW: str = "-> "
```
The block has default + range + (one-line) what, but **no explicit Effect line and no Exam-variants line**. Spec §8.1 requires all four. Compare with the same KNOB in `reflex_vacuum_agent_solution.py:509-512` which is itself ALSO missing Effect / Exam variants. Both occurrences are partial.

### P1-5. KNOB `GRID_TRAVERSAL_ORDER` lacks an explicit "range / allowed" specification
**Files:**
- `reflex_vacuum_agent_solution.py:156-167`
- `reflex_agent_with_state_solution.py:176-186`
The block heading reads `(default=("TL","TR","BR","BL"))` with no `range=` or `allowed=` clause, unlike every other KNOB in the file. Spec §8.1 wants all four facets explicit. State it: `range=any permutation of {"TL","TR","BL","BR"}`.

### P1-6. `COLUMN_WIDTHS` KNOB in stateful file delegates effect explanation
**File:** `reflex_agent_with_state_solution.py:543-548`
```
#   Effect / Exam variants: same as in
#     reflex_vacuum_agent_solution.py — adjust only if longer enum
#     names are introduced.
```
Spec demands every KNOB be self-contained. Cross-file delegation is not a valid substitute for the Effect or Variants lines. Either duplicate them or import the documentation.

---

## P2 — Polish, Cleanup, Future Risk

### P2-1. `ACTION_COLUMN_WIDTH` is a function-local KNOB
**File:** `table_driven_agent_solution.py:275-283`
The KNOB block is correct, but the constant is defined **inside** `run()`. An auditor scanning module-top for KNOBs misses it. Promote to module scope alongside the other KNOBs in this file.

### P2-2. `LINE_4` ordering is a hardcoded tuple, not a KNOB
**Files:**
- `Enums_solution.py:147-148`
- `reflex_vacuum_agent_solution.py:431-432`
- `reflex_agent_with_state_solution.py:462-463`
All three locations bake `(TL, TR, BL, BR)` as the 1-D row order. If a variant exam asks "the row is BL-BR-TL-TR", three files need editing. Should be a `LINE_4_ORDER` KNOB in `Enums_solution.py` consumed by both reflex files.

### P2-3. Adjacency dict duplicated across two agent files
**Files:**
- `reflex_vacuum_agent_solution.py:419-428`
- `reflex_agent_with_state_solution.py:451-460`
Identical 8-row adjacency map. Not a KNOB violation per se, but the magic constants now live in two places. Move to `Enums_solution.py` (already the topology owner) and import.

### P2-4. `GRID_TRAVERSAL_ORDER` uses strings + `getattr`, not enum members
**Files:** same as P1-5. Resolving via `getattr(GridLocation, n)` (lines 447, 481) is fragile: a typo silently raises `AttributeError` at runtime rather than at edit time. Use `tuple[GridLocation, ...]` for type safety.

### P2-5. `ENABLE_BOGUS_DEMO` is not honoured in the stateful agent
**File:** `reflex_agent_with_state_solution.py`
The stateless file has `_maybe_make_bogus_2room` / `_maybe_make_bogus_grid` hooked into `evaluate()`. The stateful file imports the same actuator-guard pattern but provides **no** bogus-demo wiring. Variant 3 (stateless vs stateful comparison) cannot show the bogus-action check under the stateful agent. Either add the hook or declare `ENABLE_BOGUS_DEMO` explicitly unsupported in this file.

### P2-6. Geometric-series degenerate branch uses magic `1`
**File:** `table_driven_agent_solution.py:245-246`
```python
if p == 1:
    return lifetime
```
Mathematically justified (sum of 1+1+...+1 T times). Keep, but a one-line comment "degenerate world has only one percept; |P|^k = 1 ∀k" already exists, so this is the lightest possible P2 — leave as-is, noted for completeness.

### P2-7. `table_definition` literal entries are slide fixtures
**File:** `table_driven_agent_solution.py:165-183`
The hand-curated rows look like magic, but they are *required by Exercise 1.2* to exist verbatim (the exam asks the student to look up the exact key `(clean_A, dirty_A, clean_B, clean_B)`). Justified — no action.

---

## KNOB Inventory (23 total)

| # | File | KNOB | Default | Range | Effect | Variants | Verdict |
|---|------|------|---------|-------|--------|----------|---------|
| 1 | Enums_solution | GRID_TOPOLOGY | Y | Y | Y | Y | Pass |
| 2 | table_driven | NUM_LOCATIONS | Y | Y | Y | Y | Pass |
| 3 | table_driven | NUM_STATUSES | Y | Y | Y | Y | Pass |
| 4 | table_driven | LIFETIME_T | Y | Y | Y | Y | Pass |
| 5 | table_driven | USE_FULL_HISTORY | Y | Y | Y | Y | Pass |
| 6 | table_driven | ACTION_COLUMN_WIDTH | Y | Y | Y | Y | Pass (P2: local scope) |
| 7 | reflex_vacuum | WORLD | Y | Y | Y | Y | Pass |
| 8 | reflex_vacuum | ENABLE_BOGUS_DEMO | Y | Y | Y | Y | Pass |
| 9 | reflex_vacuum | NUM_STEPS | Y | Y | Y | Y | Pass (but see P0-1) |
|10 | reflex_vacuum | START_LOCATION_2ROOM | Y | Y | Y | Y | Pass |
|11 | reflex_vacuum | START_LOCATION_GRID | Y | Y | Y | Y | Pass |
|12 | reflex_vacuum | GRID_TRAVERSAL_ORDER | Y | **N** | Y | Y | **P1-5** |
|13 | reflex_vacuum | INITIAL_DIRT | Y | Y | Y | Y | Pass (but see P1-3) |
|14 | reflex_vacuum | COLUMN_WIDTHS | Y | Y | Y | Y | Pass |
|15 | reflex_vacuum | ARROW | Y | Y | **N** | **N** | **P1-4** |
|16 | reflex_state | WORLD | Y | Y | Y | Y | Pass |
|17 | reflex_state | AGENT_VARIANT | Y | Y | Y | Y | Pass |
|18 | reflex_state | NUM_STEPS | Y | Y | Y | Y | Pass (but see P0-2) |
|19 | reflex_state | START_LOCATION_2ROOM | Y | Y | Y | Y | Pass |
|20 | reflex_state | START_LOCATION_GRID | Y | Y | Y | Y | Pass |
|21 | reflex_state | GRID_TRAVERSAL_ORDER | Y | **N** | Y | Y | **P1-5** |
|22 | reflex_state | INITIAL_DIRT | Y | Y | Y | Y | Pass (but see P1-3) |
|23 | reflex_state | COLUMN_WIDTHS | Y | Y | **delegated** | **delegated** | **P1-6** |
|24 | reflex_state | ARROW | Y | Y | **N** | **N** | **P1-4** |

Net: 18 fully compliant, 5 partial, 0 missing-block-entirely — but 2 P0 magic numbers undermine the contract of `NUM_STEPS`.

---

## Hidden Magic Number Hunt — Summary

| Severity | Location | Constant | Why it matters |
|---|---|---|---|
| P0 | reflex_vacuum:539,558 | `1` in `range(1, steps)` | Contradicts NUM_STEPS contract & slide demo |
| P0 | reflex_state:589,608 | `1` in `range(1, steps)` | Same; breaks Homework `run(20)` |
| P1 | reflex_vacuum:517 / reflex_state:557 | `8` in `'New':8s` | Header width independent of COLUMN_WIDTHS |
| P1 | reflex_vacuum:463-474 / reflex_state:498-509 | Direction tuples | Hidden heuristic, not exposed as KNOB |
| P1 | reflex_vacuum:205-207 / reflex_state:530-532 | "2 dirty + 2 clean" MIXED split | Variant questions cannot adjust the partition |
| P2 | Enums:147 / reflex_vacuum:431 / reflex_state:462 | `(TL,TR,BL,BR)` LINE_4 order | Triplicated, should be KNOB |
| P2 | reflex_vacuum:419-428 / reflex_state:451-460 | 8-row adjacency dict | Duplicated topology data |
| P2 | table_driven:245 | `1` (degenerate geometric series) | Mathematical, justified |
| OK | table_driven:165-183 | table_definition rows | Slide fixture, justified |

---

## Report to PM

**Assignment recap:** Lab Reviewer #2 (KNOB Coverage) — Lab1-Agents Round 1, four solution files under `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\`.
**Status:** Fail (2 P0 + 6 P1 + 7 P2). The KNOB *declarations* are 78% perfect, but two hidden-magic-number bugs in the simulator loop violate Spec §8.1's contract that KNOB documentation must match runtime behaviour.

**P0 findings:**
1. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\reflex_vacuum_agent_solution.py:539,558` — `for _ in range(1, steps):` truncates every trace by one step; fix to `range(steps)` (or add a documented `STEP_INDEX_BASE` KNOB).
2. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\reflex_agent_with_state_solution.py:589,608` — identical off-by-one in the lab entry point; same fix.

**P1 findings:**
1. `reflex_vacuum_agent_solution.py:517` & `reflex_agent_with_state_solution.py:557` — hidden `8` for the "New" header width, independent of `COLUMN_WIDTHS`.
2. `reflex_vacuum_agent_solution.py:463-474` & `reflex_agent_with_state_solution.py:498-509` — hardcoded directional tie-break tuples; promote to `MOVE_PREFERENCE_PRIMARY` / `MOVE_PREFERENCE_FALLBACK` KNOBs.
3. `reflex_vacuum_agent_solution.py:205-207` & `reflex_agent_with_state_solution.py:530-532` — `MIXED` initial-dirt partition is hardcoded 2/2; add `MIXED_DIRTY_SQUARES` KNOB.
4. `reflex_vacuum_agent_solution.py:509-512` & `reflex_agent_with_state_solution.py:550-552` — `ARROW` KNOBs missing Effect and Exam-variants lines.
5. `reflex_vacuum_agent_solution.py:156-167` & `reflex_agent_with_state_solution.py:176-186` — `GRID_TRAVERSAL_ORDER` lacks explicit `range=` / `allowed=` line.
6. `reflex_agent_with_state_solution.py:543-548` — `COLUMN_WIDTHS` Effect / Variants delegated by reference to the other file; must be self-contained.

**P2 findings:**
1. `table_driven_agent_solution.py:275-283` — `ACTION_COLUMN_WIDTH` KNOB defined function-locally; promote to module scope.
2. `Enums_solution.py:147-148`, `reflex_vacuum_agent_solution.py:431-432`, `reflex_agent_with_state_solution.py:462-463` — LINE_4 row order triplicated; consolidate as KNOB in `Enums_solution.py`.
3. `reflex_vacuum_agent_solution.py:419-428` & `reflex_agent_with_state_solution.py:451-460` — adjacency dict duplicated; move to `Enums_solution.py`.
4. `GRID_TRAVERSAL_ORDER` stores names as strings and resolves via `getattr` — fragile; use `tuple[GridLocation, ...]`.
5. `reflex_agent_with_state_solution.py` — `ENABLE_BOGUS_DEMO` not honoured here; either wire it through or declare unsupported.
6. `table_driven_agent_solution.py:245-246` — magic `1` in degenerate geometric branch; justified, leave.
7. `table_driven_agent_solution.py:165-183` — literal table rows; justified by Exercise 1.2.

**QA Checklist (§7) status:** N/A for this reviewer role (KNOB-coverage audit only).
**Acceptance criteria (§1) status:** N/A.
**DOCUMENT.md audit:** Not in scope for Reviewer #2.
**Out-of-scope observations:**
- `reflex_agent_with_state_solution.py` duplicates `_grid_neighbour` and `_grid_move_toward` verbatim from the stateless file (lines 446-510). Pure refactor candidate.
- The stateful file's docstring captures "OUTPUTS WHEN RUN" (lines 88-99) — if the P0 off-by-one is fixed, that block will need to be regenerated (a 9th SUCK/NO_OP line will appear).
**Concerns / risks:**
- Variant-question coverage is weakened by P1-2 (move preference) and P1-3 (MIXED split): the exam agent cannot answer "what if the cleaner prefers UP first?" or "what if only BR is dirty?" by flipping a documented KNOB.
- The duplicate adjacency dicts (P2-3) are a maintenance trap — change the topology in one place, forget the other, and the two agents disagree.
- After fixing the P0 loop bounds, **re-run both files** and update the captured output block in `reflex_agent_with_state_solution.py:84-99` — otherwise the docstring will drift.
**What PM should do next:**
1. Dispatch `pm-backend` (or the relevant engineer) to fix P0-1 and P0-2.
2. Then address P1-1 through P1-6 in the same pass (small, mechanical).
3. Re-dispatch Reviewer #2 (this role) for round 2 to re-verify.
4. P2 items can be batched or deferred to a follow-up cleanup ticket.
**DOCUMENT.md updated:** N/A for QA.

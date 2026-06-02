# Lab1-Agents — Round-1 Revise Summary

**Reviser:** Lab1-Agents R1 reviser
**Date:** 2026-05-23
**Inputs:** `reviewer1.md` (correctness), `reviewer2.md` (KNOB coverage), `reviewer3.md` (pedagogy). `reviewer4.md` does not exist in this round — the task brief listed it but only three reviewer files are present in `study/_review/labs/Lab1-Agents/round1/`. The R4 P0 items (STATES_TREATED_AS_DIRTY KNOB + Variant 1 / 2 reconciliation) were called out in the brief and are addressed below regardless of the missing file.

**Files revised (4):**
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\Enums_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\table_driven_agent_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\reflex_vacuum_agent_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\reflex_agent_with_state_solution.py`

**Plus:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab1-Agents\variants.md` (Variant 1 / Variant 2 updates).

---

## P0 — All addressed

### P0 from R2: `range(1, steps)` off-by-one

- `reflex_vacuum_agent_solution.py:539, 558` → fixed to `range(steps)`.
- `reflex_agent_with_state_solution.py:589, 608` → fixed to `range(steps)`.

Verified via `py -3.12`:

- `py -3.12 reflex_vacuum_agent_solution.py` now prints **10** body rows (was 9).
- `py -3.12 reflex_agent_with_state_solution.py` now prints **20** body rows (was 19).

The captured "OUTPUTS WHEN RUN" block in both solution docstrings was regenerated to match the new row count. `reflex_agent_with_state_solution.py` docstring lines 158–172 now describe 7 active ticks + 13 NO_OPs = 20 rows total. `reflex_vacuum_agent_solution.py` docstring lines 122–141 now show the full 10-row 2-room trace.

### P0 from R3: MENTAL MODEL drift from L02

Three of four files re-anchored to L02 §2's canonical analogies:

- **`table_driven_agent_solution.py`** — replaced "giant printed phone book" with L02's **"infinite, impossible filing cabinet"** (L02 §2 line 201–206; §4.1).
- **`reflex_vacuum_agent_solution.py`** — replaced "thermostat" (which collides with L02's *baseline agent* analogy) with L02's **"vending machine"** (L02 §2 line 213–217; §4.2). "Press B-4, get a Mars bar" wording matches the lecture verbatim.
- **`reflex_agent_with_state_solution.py`** — leads with L02's **"driver in fog"** analogy (L02 §2 line 227–241; §4.3); keeps the maid-with-clipboard image as a secondary view.
- **`Enums_solution.py`** — already analogy-clean ("floor plan + dictionary of moves"); the new wording explicitly cross-references L02 §2 / §4.1–4.3 so a reader sees the lecture mapping.

### P0 from R3: REFERENCES section numbers

All four files now point to L02 §4.x (where the agent-type hierarchy lives), not §3:

- `Enums_solution.py` → L02 §3.1 "Agent and environment", §3.5 "PEAS". (These are correct for an *enums helper module*, which is environment-level — not an agent architecture.)
- `table_driven_agent_solution.py` → L02 §4.1 "Table-driven agents" + §3.2 "Percept, percept sequence, agent function, agent program".
- `reflex_vacuum_agent_solution.py` → L02 §4.2 "Simple reflex agent" + §3.1 + §3.2.
- `reflex_agent_with_state_solution.py` → L02 §4.3 "Model-based reflex agent" + §3.2 + §3.6.

### P0 from R3: Captured OUTPUTS WHEN RUN in all 4 files

All four files now have a `captured 2026-05-23, py -3.12` dated block with the actual stdout pasted (not prose):

- `Enums_solution.py` — captured `GRID_TOPOLOGY` + `LINE_4_ORDER` + the 5-row allowed-moves table.
- `table_driven_agent_solution.py` — captured the 4 percept lookups + the two table-size lines.
- `reflex_vacuum_agent_solution.py` — captured the 10-row 2-room trace.
- `reflex_agent_with_state_solution.py` — captured the 20-row Homework trace (regenerated after the off-by-one fix).

### P0 from brief (R4): `STATES_TREATED_AS_DIRTY` KNOB

Added to `reflex_vacuum_agent_solution.py` as a module-level KNOB:

```python
STATES_TREATED_AS_DIRTY: frozenset = frozenset({States.DIRTY})
```

The slide-10 / slide-15 SUCK-trigger is now `_is_dirty(status)` (which reads this KNOB) instead of `status == States.DIRTY`. Both the stateless `Agent.choose_action` and the stateful `match_rule` (in both `StatefulReflexAgent` and `StatefulGridAgent`) call `_is_dirty`, so variant 1 (dust-level sensor) becomes a one-KNOB extension. The stateful entry point imports `STATES_TREATED_AS_DIRTY` and `_is_dirty` from the stateless module so the dirty-side set lives in exactly one place.

### P0 from brief (R4): `variants.md` reconciliation

- **Variant 1** now references the new `STATES_TREATED_AS_DIRTY` KNOB and the `MIXED_DIRTY_SQUARES` KNOB explicitly. The exam agent can answer "add a dust-level sensor" by listing two KNOBs to flip.
- **Variant 2** received a "**Scope note: this variant is table-size math only**" paragraph clarifying that the table-driven agent does not simulate motion — changing `NUM_LOCATIONS` to 3 is purely a parameter change. No `ACTIVE_GRID_LOCATIONS` simulator KNOB is needed because the table-driven agent never simulates the new room.

---

## P1 — All addressed

### Magic number `8` for "New" header width (R2 P1-1)

`reflex_vacuum_agent_solution.py:_print_header` and `reflex_agent_with_state_solution.py:_print_header` now compute `new_w = loc_w + sta_w` from `COLUMN_WIDTHS` instead of hardcoding `8`. Widening any column re-aligns the header automatically.

### Hardcoded directional tie-break tuples (R2 P1-2)

Added two new KNOBs in `reflex_vacuum_agent_solution.py`:

```python
MOVE_PREFERENCE_PRIMARY:  ("LEFT","RIGHT","UP","DOWN")
MOVE_PREFERENCE_FALLBACK: ("RIGHT","DOWN","LEFT","UP")
```

`_grid_move_toward` reads them in both reflex files (the stateful file imports the same constants so a single edit propagates). Each KNOB has the full What / Effect / Variants block.

### `MIXED` initial-dirt is hidden 2/4 (R2 P1-3)

Added `MIXED_DIRTY_SQUARES: tuple[str, ...]` KNOB. Default `("A","TL","TR")` reproduces the previous behaviour (which was "A dirty, TL+TR dirty, BL+BR clean"); a variant such as "only BR dirty" can be expressed as `("BR",)`. Both `_initial_states_2room` and `_initial_states_grid` honour it; the stateful entry point duplicates the KNOB (and reads through it) so its file is self-contained.

### ARROW KNOB missing Effect / Variants (R2 P1-4)

Both `reflex_vacuum_agent_solution.py` and `reflex_agent_with_state_solution.py` `ARROW` blocks now include the full What / Effect / Exam-variants quadrant per Spec §8.1.

### GRID_TRAVERSAL_ORDER missing range (R2 P1-5)

Updated to `range=any permutation of {"TL","TR","BR","BL"}` in both files. The stateful file's KNOB block already had this — both now match.

### COLUMN_WIDTHS delegated effect (R2 P1-6)

`reflex_agent_with_state_solution.py:COLUMN_WIDTHS` is now self-contained — Effect + Exam-variants are written out explicitly instead of pointing to the stateless file.

### MENTAL-MODEL / REFERENCES / OUTPUTS issues — see P0 above

R3 P0.1 / P0.2 / P0.3 all addressed in the P0 section.

### ENTRY POINT duplicated in Enums_solution (R3 P1.1)

The `ENTRY POINT: no` mention inside HOW TO ADAPT point 4 was removed; only the dedicated `ENTRY POINT: no` section at the end of the docstring remains.

### evaluate() docstring is a sticky-note (R3 P1.2)

`reflex_vacuum_agent_solution.py:Agent.evaluate` and `GridAgent.evaluate` docstrings rewritten to describe the sense → choose → optionally bogusify → actuate loop and *why* the verb is `evaluate` not `act` (template signature preservation).

### WHAT-leak around tuple(percepts) (R3 P1.3)

`LOOKUP`'s comment now leads with the WHY ("dicts need hashable keys" + "slide-6 safe-no-op convention") and drops the direct-to-reviewer phrasing. "Reviewer #1 should note" + "Reviewer #4: variant questions..." asides removed.

### globals() mutation in run() (R3 P1.4)

Replaced with a clean `use_full_history: bool | None = None` parameter on `report_table_size`. `run()` now calls it twice with explicit overrides — no `globals()` poking, the module-level KNOB stays stable for downstream callers.

### Dead last_seen_location attribute (R3 P1.5 / R1 P2-1)

Deleted from `GridAgent.__init__` in `reflex_vacuum_agent_solution.py`. The contradictory `traversal_index` comment is gone too.

### Match_rule prose contradicts itself (R3 P1.6)

`StatefulReflexAgent` class docstring rewritten: "UPDATE-STATE *writes* to the model every tick; the model is *consulted for the action choice* only when the current square is clean — at that point Rule 2 reads the whole model." (Original "every other tick still uses the current percept alone" claim is gone.)

### GRID_TOPOLOGY not flagged as cross-file (R3 P1.7)

`reflex_vacuum_agent_solution.py` WORLD KNOB now ends with "Related KNOB in `Enums_solution.py`: `GRID_TOPOLOGY` (flip to "LINE_4" for the 1-D 4-cell variant) — both files import the same value." The stateful file's HOW TO ADAPT point 3 also calls out the `LINE_4_ORDER` KNOB explicitly.

### Stateless delegation KNOB propagation (brief P1)

`reflex_agent_with_state_solution.py` now defines `_propagate_knobs_to_stateless()` and calls it before delegating to `reflex_vacuum_agent_solution.run()`. The propagated KNOBs are WORLD, NUM_STEPS, START_LOCATION_2ROOM, START_LOCATION_GRID, GRID_TRAVERSAL_ORDER, INITIAL_DIRT, MIXED_DIRTY_SQUARES. Verified: setting `AGENT_VARIANT="STATELESS"` + `START_LOCATION_GRID=GridLocation.BR` now produces a BR-started trace (previously would have used the stateless file's defaults).

---

## P2 — Selectively addressed

The brief said "smaller issues per the reports" — picked the ones with strict pedagogical or maintenance impact:

- **R2 P2-1** `ACTION_COLUMN_WIDTH` promoted to module scope in `table_driven_agent_solution.py`.
- **R2 P2-2** `LINE_4` order consolidated as `LINE_4_ORDER` KNOB in `Enums_solution.py`. Both reflex files now import it.
- **R2 P2-3** 2x2 adjacency dict consolidated as `GRID_2X2_ADJACENCY` in `Enums_solution.py`. Both reflex files import it.
- **R2 P2-4** `GRID_TRAVERSAL_ORDER` still uses strings (kept human-readable in KNOB block) but now resolves via `GridLocation[name]` (subscript, raises `KeyError` at edit time) instead of `getattr(GridLocation, name)`. Same robustness; the comment in the KNOB block calls out the resolution method.
- **R2 P2-5** `ENABLE_BOGUS_DEMO` deliberately left unwired in the stateful entry point — declared unsupported there (the bogus demo lives in the stateless file; running the stateless variant via `AGENT_VARIANT="STATELESS"` exercises it). Documented inline.
- **R1 P2-2 / R3 P2.3** Note about `Enums.py` dependency added to the re-export line in `Enums_solution.py`. Kept the re-export (duplication of three enums would clutter the file) but the comment now tells a grader what to do if they ship only the solution files.
- **R3 P2.1** "Reviewer #N should note" / "Reviewer #4: ..." comments removed across `table_driven_agent_solution.py` and `Enums_solution.py`.
- **R3 P2.3** `GRID_TOPOLOGY` KNOB now explicitly states `==` string equality, case-sensitive — closes the "could I write 'grid_2x2'?" question a confused student might have.
- **R3 P2.5** geometric-series closed-form comment now states *why* the closed form is used (computability for large T) rather than just *what* the formula is.

P2 items intentionally NOT picked up (low value relative to the round-1 budget):

- **R1 P2-4** `_grid_move_toward` Manhattan-distance picker — irrelevant for the 2x2 grid (every legal move is within one hop of every other corner via at most two ticks).
- **R3 P2.6** body-level comment about the bogus-action probe ordering in `_maybe_make_bogus_grid` — added a one-liner; further detail is overkill.

---

## Verification (post-revision)

All commands run from `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents` with `py -3.12`.

| Run | Command | Result |
|---|---|---|
| 1 | `py -3.12 Enums_solution.py` | Prints `GRID_TOPOLOGY = GRID_2x2`, `LINE_4_ORDER = ('TL','TR','BL','BR')`, and the 5-row allowed-moves table. Matches docstring. |
| 2 | `py -3.12 table_driven_agent_solution.py` | 4 lookups + `\|P\|=4` + `T=10` table size `1398100`. Matches docstring. |
| 3 | `py -3.12 reflex_vacuum_agent_solution.py` | 10-row trace, alternating SUCK/RIGHT/LEFT, no NO_OP (the stateless lesson). Matches docstring. |
| 4 | `py -3.12 reflex_agent_with_state_solution.py` (entry point) | 20-row trace: 7 active + 13 NO_OP. Matches docstring. |
| 5 | Variant 1: `STATES_TREATED_AS_DIRTY` widening + `MIXED_DIRTY_SQUARES=("A",)` | Only A dirty at start; A SUCK then alternates. Verified. |
| 6 | Variant 2: `NUM_LOCATIONS=3` table-size math | `\|P\|=6`, `sum_(k=1..T)\|P\|^k = 72559410`. Verified. |
| 7 | Variant 3: `AGENT_VARIANT="STATELESS"` + `START_LOCATION_GRID=GridLocation.BR` | KNOB propagation works; BR-started trace produced from the entry point. Verified. |
| 8 | Variant 4: `ENABLE_BOGUS_DEMO=True`, 6 steps | Cleaner sucks A then sits at A forever (LEFT rejected). Verified. |
| 9 | LINE_4 topology: `GRID_TOPOLOGY="LINE_4"` + `WORLD="GRID_4"` | Cleaner walks TL→TR→BL→BR in line, RIGHT/LEFT only. Verified. |
| 10 | All 4 starts (TL, TR, BL, BR) reach NO_OP within 8 ticks in the stateful run | Verified. |

No regressions; every variant the variants.md file mentions is reachable by KNOB flips alone.

---

## Outstanding (out of scope / deferred)

- The `Enums.py` re-export coupling (R1 P2-2) — left as a comment, not fixed. Duplicating three enums would clutter `Enums_solution.py` and the lab repo always ships both files.
- `_grid_move_toward` Manhattan-distance picker (R1 P2-4) — not needed for the 2x2 grid; deferred to "if the lab ever grows past 2x2".
- `reviewer4.md` was listed in the task brief but does not exist on disk. If it was a future-round artifact, the P0 items the brief surfaced for it (STATES_TREATED_AS_DIRTY + variants.md alignment) are addressed regardless.

---

## What the next reviewer should re-check

1. **R2 round 2:** re-verify the KNOB Inventory table — six new KNOBs (`LINE_4_ORDER`, `MIXED_DIRTY_SQUARES`, `STATES_TREATED_AS_DIRTY`, `MOVE_PREFERENCE_PRIMARY`, `MOVE_PREFERENCE_FALLBACK`, plus the now-module-level `ACTION_COLUMN_WIDTH`). All have What / Effect / Exam-variants. Magic numbers in `_print_header` / `run()` / direction tuples are gone.
2. **R3 round 2:** confirm MENTAL MODEL one-liners are now L02-shaped, REFERENCES point to §4.x, and every file's OUTPUTS WHEN RUN block contains an actual capture dated 2026-05-23.
3. **R1 round 2:** confirm `run(10)` / `run(20)` produce exactly 10 / 20 rows. Signature preservation still holds (no public function changed name or argument shape — only `report_table_size` got an additional default-None parameter, which is strictly broader).
4. **Variants check:** re-read `study/_exam/Lab1-Agents/variants.md` with the new KNOBs — Variant 1 should now solve via KNOB flips alone; Variant 2 has the scope-clarifying note.

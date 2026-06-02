# Variant Bank — Lab 1: Agents (Reflex agents, vacuum world)

This file is the exam-agent gate input for **Lab1-Agents** per spec §8.3 and Appendix B of the implementation plan. Each variant below is a self-contained question that a fresh exam agent must be able to answer by reading **only** the docstring header + `# KNOB:` blocks + function signatures of:

- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\reflex_agent_with_state_solution.py` (ENTRY POINT)
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\reflex_vacuum_agent_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\table_driven_agent_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab1-Agents\Enums_solution.py`

Exam agents are forbidden from reading function bodies, helper modules, the lab handout PDF, or any lecture material.

---

## Variant 1 — Add a third sensor (dust-level meter)

**Question (paraphrased from Appendix B, row Lab1-Agents):**

> Add a third sensor (e.g. a *dust-level* meter that distinguishes
> `LIGHT_DIRTY` from `HEAVY_DIRTY`) to the simple reflex vacuum agent.
> How does the agent's decision rule change, and what does the new
> rule look like? Show the change with KNOB values, and report the
> trace from a 10-step run starting at location A with `INITIAL_DIRT
> = "MIXED"`.

**Expected agent actions (using only KNOBs + signatures):**

1. Note that the slide-10 reflex rule already factors as "if status indicates dirt, SUCK; else move toward the next room". Extending the `States` enum to add `LIGHT_DIRTY` / `HEAVY_DIRTY` keeps the rule unchanged *as long as the new states are listed in the `STATES_TREATED_AS_DIRTY` KNOB on `reflex_vacuum_agent_solution.py`* — the reflex rule reads `status in STATES_TREATED_AS_DIRTY` instead of `status == States.DIRTY`, so widening the dirty-side set is a one-knob change.
2. Configure the simple reflex run by editing KNOBs on `reflex_vacuum_agent_solution.py`:
   - `WORLD = "ROOMS_2"` (default — Exercise 2 world).
   - `START_LOCATION_2ROOM = Location.A` (default).
   - `INITIAL_DIRT = "MIXED"`, and `MIXED_DIRTY_SQUARES` to pick which squares start dirty (default `("A","TL","TR")`).
   - `NUM_STEPS = 10`.
   - `STATES_TREATED_AS_DIRTY = frozenset({States.DIRTY, States.LIGHT_DIRTY, States.HEAVY_DIRTY})` once the new `States` members exist.
3. Report the printed trace (the question's deliverable).
4. Answer in prose: the *condition* in the slide-10 rule becomes
   `if status in STATES_TREATED_AS_DIRTY: SUCK` — i.e. the
   `States` enum widens and the dirty-side KNOB widens with it, but
   the rule structure is identical. The actuator does NOT need to
   change because SUCK is square-local and always in
   `allowed_moves()`.

**Acceptance:** the exam agent's `VERDICT` is `SOLVED` if they correctly identify (a) the KNOB(s) to flip — including `STATES_TREATED_AS_DIRTY`, (b) the rule change is a *set widening on the dirty side*, and (c) the trace runs without error.

---

## Variant 2 — Three rooms in a line (changed state space)

**Scope note:** this variant is **table-size math only**. The
table-driven agent does not simulate room-to-room motion (it just
prints lookups + the table-size formula), so changing `NUM_LOCATIONS`
to 3 is purely a parameter change — no new `Location.C` enum member
or simulator rewiring is needed at the KNOB level. The reflex
simulators continue to use the 2-room or 4-square enums; varying
`NUM_LOCATIONS` only affects the table-size print at the end of
`table_driven_agent_solution.run()`.

**Question (paraphrased from Appendix B, row Lab1-Agents):**

> Change the environment from 2 rooms to 3 rooms arranged in a line
> (A — B — C). What is the new state space size, and how does the
> table-driven agent's table size scale at a lifetime of T = 10? Use
> the table-driven solution's KNOBs to report the table size.

**Expected agent actions:**

1. On `table_driven_agent_solution.py`, set:
   - `NUM_LOCATIONS = 3` (three rooms).
   - `NUM_STATUSES = 2` (CLEAN / DIRTY — unchanged).
   - `LIFETIME_T = 10` (matches slide-7 Exercise 1.4 framing).
   - `USE_FULL_HISTORY = True` for the 1.4 formula; flip to `False` to also report the 1.3 answer.
2. Run the module; the `report_table_size()` print at the end of `run()` reports both numbers automatically.
3. Answer in prose:
   - Percept-space size `|P| = NUM_LOCATIONS * NUM_STATUSES = 6`.
   - State space size of the world (positions × dirt-bits) is
     `3 * 2^3 = 24`.
   - Table size for T = 10 is `sum_{k=1..T} |P|^k = 6 * (6^10 - 1) / 5`
     which the helper prints as a single integer.
4. Optionally: note that the four-room *grid* (Exercise 3) instead
   has `|P| = 4 * 2 = 8` and `|state space| = 4 * 2^4 = 64`.

**Acceptance:** `SOLVED` if the agent correctly identifies the KNOBs to flip, runs the module, and reports both `|P|` and the lifetime-T table size from the run output.

---

## Variant 3 — Stateless reflex vs stateful reflex on a partially observable variant

**Question (paraphrased from Appendix B, row Lab1-Agents):**

> Compare the stateless simple reflex vacuum agent (slide 10) and the
> stateful reflex agent (slide 16) on the 4-square (2x2 grid) world
> starting at `BR`, running for 20 ticks each, with all squares
> initially dirty. Which agent terminates with NO_OP earlier, and
> why? Use KNOBs to switch between the two agents.

**Expected agent actions:**

1. Run the entry point twice with different `AGENT_VARIANT`:
   - Run A: `AGENT_VARIANT = "STATEFUL"`, `WORLD = "GRID_4"`,
     `START_LOCATION_GRID = GridLocation.BR`, `NUM_STEPS = 20`.
   - Run B: `AGENT_VARIANT = "STATELESS"`, same other KNOBs.
2. Compare the two traces. Expectation (matches the slide 14 framing): the stateful agent reaches `NO_OP` after about 7 ticks (4 SUCKs + 3 moves), because once its `model` shows every square CLEAN it fires Rule 2. The stateless agent NEVER fires NO_OP under the slide-10 rule — it keeps moving forever between clean squares because it has no memory that they have already been cleaned.
3. Answer in prose: the *memoryless* slide-10 rule cannot detect quiescence; the *stateful* slide-16 rule can because Rule 2 reads `self.model`.

**Acceptance:** `SOLVED` if the agent correctly identifies the KNOB combo, captures both traces, and explains the difference using the words "model" / "memory" / "quiescence" (or equivalent).

---

## Variant 4 (bonus) — Confirm the actuator refuses bogus actions (Exercise 2.3)

**Question:**

> Exercise 2.3 asks: "Should bogus actions be able to corrupt the
> environment? ... Do the Actuators allow bogus actions?" Use KNOBs
> to demonstrate the answer with a 10-step run of the 2-room world
> in which the agent deliberately requests a wrong directional move
> at every tick.

**Expected agent actions:**

1. On `reflex_vacuum_agent_solution.py`, set:
   - `WORLD = "ROOMS_2"`.
   - `ENABLE_BOGUS_DEMO = True`.
   - `NUM_STEPS = 10`.
2. Run the file. The trace will show:
   - SUCK ticks still succeed (SUCK is always in `allowed_moves()`).
   - Every directional tick should be a BOGUS one (LEFT at A, RIGHT at B). Because `allowed_moves()` excludes those, the cleaner stays in place: the trace shows the same location/status before and after the bogus action.
3. Answer in prose: **No, the actuators do not allow bogus actions.** Both `Agent.actuator` and `StatefulReflexAgent.actuators` check `action in location.allowed_moves()` (or its inverse early-return) before mutating the environment, so any directional move not legal from the current square is silently dropped.

**Acceptance:** `SOLVED` if the agent reports that the actuator rejects bogus directional moves and the trace evidence supports it.

---

## Variant 5 (bonus) — Exercise 1.2 ("Explain TABLE_DRIVEN_AGENT(clean_B)")

**Question:**

> After running `table_driven_agent.run()` the percept history is
> `[(A, CLEAN), (A, DIRTY), (B, CLEAN)]`. The lab then asks: enter
> `print(f"{TABLE_DRIVEN_AGENT(clean_B):...}| {total_percepts}")` and
> *explain the result*. What action does it return, why, and what
> does this tell you about the scaling of the table-driven approach?

**Expected agent actions:**

1. Note that the table-driven solution's `run()` already performs this exact extra lookup (see the OUTPUTS WHEN RUN section of the docstring) — no KNOB change is required; just run the file.
2. Inspect the printed output:
   - The lookup with key `(clean_A, dirty_A, clean_B, clean_B)` returns `LEFT` (the entry is in the small illustrative `table_definition`).
3. Answer in prose: the *same* percept (`clean_B`) appearing for the second time produces a *different* row from the first time it was seen, because the key is the *entire sequence so far*, not the latest percept alone. This makes the table grow exponentially with lifetime — for `T = 10` and `|P| = 4` the table needs ~1.4 million entries (as the solution prints via `report_table_size()`). This is the headline pedagogical point of slides 6–7.

**Acceptance:** `SOLVED` if the agent reports the action returned (`LEFT`), explains it is determined by the *full history*, and connects this to the explosive growth of the table.

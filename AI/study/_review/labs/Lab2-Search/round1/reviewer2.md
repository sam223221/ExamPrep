# Lab 2 — Search Solution — Reviewer #2 (KNOB Coverage) — Round 1

**Reviewer role:** Lab Reviewer #2 — KNOB coverage and magic-number hunt.
**File audited:** `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 2\Search_solution.py`
**Template reference:** `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab 2\Search.py`
**Verdict (one line):** **Pass with serious concerns.** Surface KNOB coverage is decent (15 KNOBs declared, each with docstring + exam-variant hints), but the file has at least **eight hardcoded constants** that pretend they are not KNOBs, **one "secret KNOB"** that mutates from inside a function via `global`, and **major missing variant axes** (depth limit, step cost, IDS/UCS, goal-predicate for Ex1/Ex3, multi-level dirtiness, N-item river crossing). An exam variant that hits any of these will require **editing function bodies**, which is exactly what the KNOBS block was supposed to prevent.

---

## 1. KNOB Inventory (what IS exposed)

| # | KNOB | Type | Default | Docstring quality |
|---|------|------|---------|-------------------|
| 1 | `KNOB_DEFAULT_STRATEGY` | `str \| None` | `None` | Good |
| 2 | `KNOB_PRINT_FRINGE_TRACE` | `bool` | `True` | Good — but see P0-3, it gets mutated by `global` |
| 3 | `KNOB_MAX_FRINGE_NODES` | `int` | `10_000` | Good, but misleading (see P1-1) |
| 4 | `KNOB_TRACK_VISITED` | `bool` | `True` | Good |
| 5–7 | `KNOB_RUN_EXERCISE_1/2/3` | `bool` | `True` | OK |
| 8 | `KNOB_EX1_STATE_SPACE` | `dict` | A..J tree | Good |
| 9 | `KNOB_EX1_INITIAL_STATE` | `str` | `"A"` | OK |
| 10 | `KNOB_EX1_GOAL_STATE` | `str` | `"J"` | OK |
| 11 | `KNOB_EX2_ROOMS` | `tuple` | `("A","B")` | OK |
| 12 | `KNOB_EX2_INITIAL_STATE` | `tuple` | `("A","Dirty","Dirty")` | OK |
| 13 | `KNOB_EX2_GOAL_STATE` | `tuple \| None` | `("B","Clean","Clean")` | Good — special-cases `None` |
| 14 | `KNOB_EX2_STATE_SPACE_OVERRIDE` | `dict \| None` | `None` | OK |
| 15 | `KNOB_EX3_BANKS` | `tuple[str,str]` | `("W","E")` | OK |
| 16 | `KNOB_EX3_INITIAL_STATE` | `tuple` | 4×W | OK |
| 17 | `KNOB_EX3_GOAL_STATE` | `tuple` | 4×E | OK |
| 18 | `KNOB_EX3_EAT_RULES` | `tuple[tuple[int,int],...]` | `((1,2),(2,3))` | Fragile — index-based; see P1-2 |
| 19 | `KNOB_EX3_PASSENGERS_PER_TRIP` | `int` | `1` | OK |

Count: **19 KNOBs declared.** Header banner reads "KNOBS" in ASCII art, every entry has a "Effect / Exam variants" block. On its face, this looks generous. The body of the file disagrees.

---

## 2. Magic numbers / hidden constants — HARSH FINDINGS

### P0-1 — `statuses = ("Dirty", "Clean")` is hardcoded inside `build_vacuum_state_space` (line 548)

```python
statuses = ("Dirty", "Clean")
```

This is a **literal in a function body**, not a KNOB. An exam variant that introduces a third dirt level (Lecture 4 / textbook chapter 3 exercise: "what if there is a Cleaner, Dirty, VeryDirty status?") cannot be handled by editing the KNOBS block. The docstring at line 92 promises "extending to 3 rooms grows the state space from 8 to 24 nodes" — but multi-level dirt is silently impossible.

**Fix:** introduce `KNOB_EX2_STATUSES: tuple[str, ...] = ("Dirty", "Clean")` and a `KNOB_EX2_SUCK_RULE: Callable | None` to define what Suck does when a status isn't binary.

### P0-2 — Farmer/Wolf/Goat/Cabbage state arity hardcoded to 4 (lines 626, 636)

```python
for state in product(banks, repeat=4):             # line 626
...
co_items_on_same_bank = [
    i for i in range(1, 4) if state[i] == farmer_bank   # line 636-638
]
```

Two separate literal `4`s, both representing "the number of items including farmer". An exam variant — and this is a classic — adds a **chicken/fox/grain** (5-item, 6-item) version, or generalises to **N missionaries / N cannibals**. The KNOBS block claims (line 102) that adding rules is enough to extend the puzzle, but you cannot add a fifth ITEM without editing `build_river_state_space`. This is exactly what the KNOBS block was supposed to prevent.

**Fix:** derive arity from `len(KNOB_EX3_INITIAL_STATE)` (or introduce `KNOB_EX3_ITEM_COUNT: int = 4`), and replace the `range(1, 4)` literal with `range(1, len(state))`. Even better: introduce `KNOB_EX3_ITEMS: tuple[str, ...] = ("farmer", "wolf", "goat", "cabbage")` and key eat-rules by **name**, not index — see P1-2.

### P0-3 — Two KNOBs are mutated at runtime via `global` (lines 726–728, 760–762)

```python
global KNOB_PRINT_FRINGE_TRACE
saved_trace = KNOB_PRINT_FRINGE_TRACE
KNOB_PRINT_FRINGE_TRACE = False
```

This is a **direct violation of the "all tunables at the top" contract** stated on lines 138–141. The KNOB is meant to be the source of truth; instead, two demo drivers temporarily clobber it. Consequences:

1. If `run_exercise_2()` raises before the `finally` clause finishes (e.g., a KeyboardInterrupt during `searcher.run`), the global is left at `False` and subsequent demos lose their fringe trace silently.
2. A student reading the KNOBS block to find out "why doesn't my fringe print for vacuum?" will spend ten minutes searching before finding the `global` hack hidden 600 lines below.
3. It is not thread-safe and not re-entrant.

**Fix:** Make `KNOB_PRINT_FRINGE_TRACE` per-demo (e.g., `KNOB_EX1_PRINT_FRINGE_TRACE`, `KNOB_EX2_PRINT_FRINGE_TRACE`, `KNOB_EX3_PRINT_FRINGE_TRACE`), or pass the flag into `tree_search()` as a parameter. The `global` keyword has no place in a "knobs-at-the-top" architecture.

### P0-4 — `searcher._track_visited = False` is a secret KNOB (line 689)

```python
# inside run_exercise_1()
searcher._track_visited = False
```

The KNOBS block at the top exposes `KNOB_TRACK_VISITED`. Then the Ex1 driver **silently overrides it** by reaching into a private attribute (`_track_visited`) on the instance. There is **no KNOB** that lets a student say "yes, even for Ex1, please track visited". The docstring comments at line 460 admit "run_exercise_1() forces it OFF" but this is not advertised in the KNOBS block.

This is a per-exercise behaviour decision masquerading as an implementation detail. It will silently sabotage any exam variant whose Ex1 state space is cyclic (e.g., Romania-style map asked via `KNOB_EX1_STATE_SPACE`).

**Fix:** add `KNOB_EX1_TRACK_VISITED: bool | None = False` (None = "use global"), and remove the `searcher._track_visited = False` line. Document the override in the KNOBS block.

### P0-5 — Goal-predicate for "all rooms clean" is hardcoded as a nested class inside `run_exercise_2` (lines 709–714)

```python
class AllCleanSearcher(Searcher):
    def _is_goal(self, state) -> bool:
        if self.goal_state is not None:
            return state == self.goal_state
        return all(status == "Clean" for status in state[1:])
```

The literal `"Clean"` and the slice `state[1:]` (skipping the agent location) are **baked into the function body**. If a student needs the same "any goal predicate" capability for Ex3 (e.g., "any state where everyone but the farmer is on east"), they cannot get it from the KNOBS block. The escape hatch `KNOB_EX2_GOAL_STATE = None` only exists for Ex2; Ex1 and Ex3 do not have it.

**Fix:** add per-exercise `KNOB_EXn_GOAL_PREDICATE: Callable[[state], bool] | None = None`. When set, it overrides the equality test. Then `AllCleanSearcher` can be deleted.

### P0-6 — No KNOB for depth limit, despite the docstring claiming Node.depth supports one

Lines 353–354 explicitly say:

> "The depth field is unused by BFS/DFS themselves but is useful when an exam variant adds a depth limit."

But there is **no `KNOB_MAX_DEPTH`**. Any variant asking "run depth-limited DFS with cutoff = 4" or "run iterative-deepening DFS" requires editing `tree_search()`. The author saw this coming and wrote a docstring acknowledging it — and then did not add the KNOB.

L03 (the reference cited on line 55) covers BFS, DFS, **IDS, UCS**. Two of those four uninformed-search strategies are **completely unreachable** from this file's KNOBs. That is a 50% coverage gap on the very lecture the file claims to operationalise.

**Fix:** add `KNOB_MAX_DEPTH: int | None = None` (None = unlimited). In `tree_search()`, skip nodes with `node.depth >= KNOB_MAX_DEPTH`. Add `KNOB_USE_IDS: bool = False` to drive iterative deepening. Add `KNOB_STEP_COST_FN: Callable | None = None` to enable UCS.

---

### P1-1 — `KNOB_MAX_FRINGE_NODES = 10_000` is **misleading insurance** (lines 162–171, 487–489)

The docstring claims this is "Cheap insurance against infinite loops if a buggy successor function (or a state space with cycles) ever sneaks in." That is **false**. The check is `len(fringe) > KNOB_MAX_FRINGE_NODES`. A cycle-free infinite chain (e.g., successor function that returns a single new state forever) keeps the fringe at size 1 and **never trips**. Also, with `KNOB_TRACK_VISITED = True` (the default) cycles are already handled — so the KNOB protects against a danger that the visited set has already neutralised.

The real concern is **expansion count** (which is unbounded). The KNOB is checking the wrong number.

**Fix:** rename to `KNOB_MAX_EXPANSIONS` and count `expansions += 1` per loop iteration. Or keep both: one cap on fringe memory, one cap on iterations.

### P1-2 — `KNOB_EX3_EAT_RULES` uses tuple indices, not item names (line 306)

```python
KNOB_EX3_EAT_RULES: tuple[tuple[int, int], ...] = ((1, 2), (2, 3))
```

Indices 1=wolf, 2=goat, 3=cabbage. Fragile because:

- If a variant adds a fifth item between wolf and goat, **every existing rule silently shifts** and the eat-rules now point at the wrong species.
- A reader has to count fingers to interpret `(1, 2)`.
- Variant suggestions in the docstring (e.g., "fox eats chicken") cannot be expressed cleanly because there's no name registry.

**Fix:** introduce `KNOB_EX3_ITEMS: tuple[str,...] = ("farmer", "wolf", "goat", "cabbage")` and re-key eat-rules: `((("wolf","goat"), ("goat","cabbage")))`. Resolve names to indices once at startup. This also unlocks P0-2's N-item generalisation.

### P1-3 — No `KNOB_EX1_TRACK_VISITED` / `KNOB_EX2_TRACK_VISITED` / `KNOB_EX3_TRACK_VISITED`

The global `KNOB_TRACK_VISITED` is overridden for Ex1 via a private attribute (see P0-4) and implicitly relied on for Ex2/Ex3. Per-exercise KNOBs would be **explicit**, not buried in instance mutation.

### P1-4 — Action labels ("Suck", "Left", "Right") hardcoded inside `build_vacuum_state_space` (lines 558, 567, 572)

The function emits successors but does **not annotate them with the action that produced them**. So the printed solution path shows only `(loc, A, B)` tuples, not "Suck → Left → Suck". A common exam variant asks "list the sequence of ACTIONS, not states". To answer that, a student would have to rewrite `Node` to carry an `action` field — exactly what the KNOBS block was meant to prevent.

**Fix:** carry an `action: Any` field on `Node`; let `build_vacuum_state_space` return `dict[state, list[(action, state)]]`; surface `KNOB_PRINT_ACTIONS: bool`.

### P1-5 — No KNOB for step cost (uniform-cost search is impossible)

L03 covers UCS. This file cannot do UCS. There is no place to attach a cost-per-edge to the state-space dict. The Node has `depth` but no `g_score`.

### P1-6 — No KNOB for tie-breaking / successor ordering

When multiple children expand at the same depth, BFS order depends on the order they appear in the state-space dict. There's no KNOB to reverse, sort, or shuffle — useful for an exam question that says "expand alphabetically" or "expand in reverse".

### P1-7 — `Node.expand` always uses `insert_as_first=True` internally (line 383)

```python
successors = insert(s, successors)
```

This builds the per-node child list in LIFO order regardless of the global strategy. The downstream `insert_all` then re-orders, but it means a hand-trace student who checks `node.expand(...)` in isolation sees a reversed children list. This is a **silent ordering quirk**, not exposed as a KNOB. The line-comment (376–379) acknowledges this is intentional, but a "KNOB_EXPAND_ORDER" would make it discoverable.

### P1-8 — `KNOB_EX2_STATE_SPACE_OVERRIDE` exists, but no Ex3 equivalent

Asymmetric. A student wanting to hand-craft a broken river state space (e.g., a one-way ferry) must edit `run_exercise_3`. Should be `KNOB_EX3_STATE_SPACE_OVERRIDE: dict | None = None` for consistency.

### P1-9 — `KNOB_EX2_STATE_SPACE_OVERRIDE or build_vacuum_state_space(...)` truthiness bug (line 704)

```python
space_dict = KNOB_EX2_STATE_SPACE_OVERRIDE or build_vacuum_state_space(KNOB_EX2_ROOMS)
```

If a student sets `KNOB_EX2_STATE_SPACE_OVERRIDE = {}` (empty dict, intentionally), the `or` short-circuits to `build_vacuum_state_space(...)` because `{}` is falsy. The correct test is `if KNOB_EX2_STATE_SPACE_OVERRIDE is not None`. This is both a magic-value bug **and** a KNOB-contract bug: the docstring (line 274) says "When None, a complete table is generated" — implying the discriminator is `None`, but the code uses truthiness.

---

### P2-1 — KNOBS block does not list ranges in a uniform format

Some entries use `range=>=1`, some use `allowed={...}`, some have no range at all. Pick one.

### P2-2 — `KNOB_DEFAULT_STRATEGY` accepts only `"BFS"`/`"DFS"`/`None` but is typed `str | None`

No validation at startup. A typo `"bfs"` silently runs both strategies (falls through both `if` branches in `_strategies_to_run`). Add an assert or a `Literal["BFS","DFS"]` type.

### P2-3 — Exercise 1 KNOB block lacks an OVERRIDE pattern parallel to Ex2

`KNOB_EX1_STATE_SPACE` IS the state space, so an "override" doesn't apply the same way — but for consistency, document that explicitly. A confused student will look for `KNOB_EX1_STATE_SPACE_OVERRIDE` based on the Ex2 pattern.

### P2-4 — The literal `(1, 2), (2, 3)` in `KNOB_EX3_EAT_RULES` is documented with a comment, not with the natural language ("wolf eats goat; goat eats cabbage")

The comment is in the surrounding docstring, but the value itself is opaque indices. Even a dict like `{"wolf": "goat", "goat": "cabbage"}` would be self-documenting.

### P2-5 — Silent abort returns `None`, identical to "no solution"

Line 489 returns `None` when the fringe cap is hit; line 506 returns `None` when the fringe empties without finding a goal. The caller (`run`) prints `"No solution found."` for both — but the first case is a **resource exhaustion**, the second is a **proof of no solution**. Worth distinguishing.

### P2-6 — `KNOB_PRINT_FRINGE_TRACE`'s effect under `global` mutation is logically equivalent to a per-exercise KNOB but harder to reason about

If you'd just defined `KNOB_EX1_TRACE`, `KNOB_EX2_TRACE`, `KNOB_EX3_TRACE` from the start, you would not need a `global` statement, would not need the `try / finally`, and a student could selectively enable Ex2's trace if they wanted to. It's the same number of lines and removes a footgun.

### P2-7 — No KNOB for "stop after K solutions" or "return all solutions"

A common exam variant: "list all shortest paths from A to J". Currently impossible without modifying `tree_search()` to not early-return.

### P2-8 — `from itertools import product` inside the function body (lines 546, 610)

Cosmetic, but inconsistent with PEP 8 / project convention (other imports are at the top). Twice.

---

## 3. Coverage matrix — lecture L03 strategies vs this file

| L03 strategy | Reachable via KNOBs? | Notes |
|---|---|---|
| BFS | YES | `KNOB_DEFAULT_STRATEGY = "BFS"` |
| DFS | YES | `KNOB_DEFAULT_STRATEGY = "DFS"` |
| Depth-limited DFS | **NO** | No `KNOB_MAX_DEPTH`, despite `Node.depth` existing for exactly this purpose |
| IDS | **NO** | No iterative deepening hook |
| UCS | **NO** | No step-cost on edges, no `g_score` on Node |
| Bidirectional | **NO** | (Not strictly required by the lab — but the file claims to cover L03) |

**Coverage = 2 / 6 = 33%** of L03's uninformed-search algorithms. The file's claim to be "every uninformed-search exam variant can be posed by changing one or more KNOBs" (line 67) is **overstated by 67%**.

---

## 4. Coverage matrix — classic problem variants vs this file

| Variant | Reachable via KNOBs only? |
|---|---|
| Ex1 — change tree shape | YES |
| Ex1 — change start/goal | YES |
| Ex1 — Romania-style cyclic map | NO — Ex1 has visited-tracking force-disabled (P0-4) |
| Ex2 — 3 rooms | YES |
| Ex2 — 3 dirt levels | NO — `("Dirty","Clean")` hardcoded (P0-1) |
| Ex2 — report action sequence not state sequence | NO (P1-4) |
| Ex2 — any-all-clean goal | YES (`KNOB_EX2_GOAL_STATE = None`) |
| Ex3 — different start/goal | YES |
| Ex3 — add a 5th item (chicken) | NO — arity `4` hardcoded (P0-2) |
| Ex3 — boat holds 2 | YES (`KNOB_EX3_PASSENGERS_PER_TRIP = 2`) |
| Ex3 — rename eat-rules by name | NO (P1-2) |
| Ex3 — broken-ferry override | NO (P1-8) |
| Any — depth-limited search | NO (P0-6) |
| Any — UCS | NO (P1-5) |
| Any — list all solutions | NO (P2-7) |
| Any — custom goal predicate | Only on Ex2 (P0-5) |

**Adapter coverage ~ 50%.** The "edit-only-KNOBs" promise holds for ~half the obvious variants.

---

## 5. Severity Summary

- **P0 (must fix before claiming "KNOB-driven adaptability"):** 6 findings (P0-1 through P0-6)
- **P1 (important gaps / fragility):** 9 findings (P1-1 through P1-9)
- **P2 (polish, consistency):** 8 findings (P2-1 through P2-8)

---

## 6. Report to PM

**Assignment recap:** Lab Reviewer #2, Lab2-Search Round 1, KNOB coverage audit of `Search_solution.py`. Hunt magic numbers, heuristic choices, depth limits, problem-definition constants that should be KNOBs but aren't.

**Status:** **Pass with concerns** — file runs, KNOBS block is real and useful, but coverage claims are inflated and several "tunable" parameters are actually hidden inside function bodies or mutated via `global`.

**P0 findings:**
1. Vacuum statuses `("Dirty","Clean")` hardcoded at `Search_solution.py:548` — blocks multi-level dirt variants. Add `KNOB_EX2_STATUSES`.
2. River state arity `4` hardcoded at `Search_solution.py:626` and `Search_solution.py:636-638` — blocks N-item variants. Derive from `len(KNOB_EX3_INITIAL_STATE)` or add `KNOB_EX3_ITEMS`.
3. `global KNOB_PRINT_FRINGE_TRACE` mutated at `Search_solution.py:726-728` and `Search_solution.py:760-762` — violates "KNOBS-at-the-top" contract; not re-entrant; surprises readers. Replace with per-exercise trace KNOBs OR pass as a parameter.
4. `searcher._track_visited = False` at `Search_solution.py:689` is a **secret KNOB** with no entry in the KNOBS block — silently disables visited tracking for Ex1. Add `KNOB_EX1_TRACK_VISITED`.
5. "All rooms clean" goal predicate is hardcoded as nested class `AllCleanSearcher` at `Search_solution.py:709-714` — Ex1 and Ex3 cannot have custom goal predicates. Add `KNOB_EXn_GOAL_PREDICATE`.
6. No `KNOB_MAX_DEPTH` despite `Node.depth` existing for that exact purpose and L03 covering Depth-Limited DFS + IDS. Add `KNOB_MAX_DEPTH`, `KNOB_USE_IDS`, `KNOB_STEP_COST_FN` (the last enables UCS).

**P1 findings:**
1. `KNOB_MAX_FRINGE_NODES` checks fringe size, but the docstring at `Search_solution.py:162-171` claims it protects against infinite loops; a cycle-free infinite chain keeps the fringe small and never trips. Either rename or add `KNOB_MAX_EXPANSIONS`.
2. `KNOB_EX3_EAT_RULES` keyed by **indices** (`Search_solution.py:306`) — fragile under any item-list change. Re-key by name.
3. No per-exercise `KNOB_TRACK_VISITED` overrides — currently smuggled via private attribute (see P0-4).
4. Action labels Suck/Left/Right are not surfaced in the solution path (`Search_solution.py:558,567,572`) — "list the actions, not the states" variants impossible without editing.
5. No step-cost / no UCS support — see P0-6.
6. No successor-ordering / tie-break KNOB.
7. `Node.expand` always inserts children LIFO (`Search_solution.py:383`); not exposed.
8. `KNOB_EX2_STATE_SPACE_OVERRIDE` has no Ex3 counterpart — asymmetric.
9. `KNOB_EX2_STATE_SPACE_OVERRIDE or build_vacuum_state_space(...)` (`Search_solution.py:704`) uses truthiness — `{}` silently misroutes. Use `is not None`.

**P2 findings:**
1. KNOB range annotations are inconsistent across the block.
2. `KNOB_DEFAULT_STRATEGY` typed as `str | None` but only 3 values are legal — no validation.
3. No `KNOB_EX1_STATE_SPACE_OVERRIDE` for parallel Ex2-style usage — at least document why.
4. `(1, 2), (2, 3)` eat-rules opaque; even a dict would self-document.
5. Fringe-cap abort returns `None`, indistinguishable from "no solution".
6. `global` hack and `try/finally` (`Search_solution.py:726-739`, `760-769`) replaceable by per-exercise trace KNOBs at zero extra cost.
7. No "all solutions" KNOB.
8. `from itertools import product` inside function bodies twice — move to top.

**Coverage verdict:** L03 strategies covered = 2 / 6 (33%). Classic-variant coverage ~50%. The file's claim that "every uninformed-search exam variant can be posed by changing one or more KNOBs" is materially overstated.

**Out-of-scope observations (not strictly KNOB issues but worth flagging):**
- `Search_solution.py:344` will raise `KeyError` on a missing-state-space access right after printing a warning; either both-or-neither.
- `StateSpace.successor` (`Search_solution.py:336`) silently dies with KeyError if a state has no entry — a "leaf vs missing" ambiguity. Recommend `state_space.get(state, [])`.
- `Searcher.__init__` annotates `state_space: StateSpace = None` (mutable default-ish) without `Optional` — minor.

**Concerns / risks:** The `global KNOB_PRINT_FRINGE_TRACE` mutation is the single scariest pattern in the file because it actively undermines the "all KNOBs at the top" promise. A student debugging "why is my trace empty" will spend non-trivial time on it. The hidden `_track_visited = False` in Ex1 is the second-scariest because it will silently corrupt any cyclic Ex1 variant.

**What PM should do next:** Send P0-1 through P0-6 to a follow-up engineer pass. P0-3 (global mutation), P0-4 (secret KNOB), and P0-6 (missing depth/IDS/UCS) are the highest-leverage fixes — each individually expands variant coverage by ~10–20%. Re-run this reviewer after the patch to confirm coverage matrix climbs above 80%.

**DOCUMENT.md updated:** N/A for QA.

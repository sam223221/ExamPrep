# Lab5-AlphaBeta — Round 1 — Reviewer #2 (KNOB Coverage)

**Reviewer role:** Lab Reviewer #2 — KNOB Coverage.
**Scope of brief:** Verify that the four named KNOBs — `MAX_DEPTH`, `EVALUATOR`, `USE_ALPHA_BETA_PRUNING`, `MOVE_ORDERING` — across `handout/handout/alpha_beta_solution.py` and `handout/handout/tictactoe_template_solution.py` actually serve the four variants in `study/_exam/Lab5-AlphaBeta/variants.md`. Inspection-only.

Files inspected:
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\alpha_beta_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\tictactoe_template_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\alpha_beta.py` (handout baseline)
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\tictactoe_template.py` (handout baseline)
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab5-AlphaBeta\variants.md`

---

## VERDICT

**FAIL — must revise before Round 2.**

The KNOB *names* are all present and the *machinery* mostly works in isolation, but the KNOB *system* is broken in three load-bearing ways: (1) the TTT module's docstring lies about KNOB propagation from the Nim module, (2) every KNOB silently accepts misspelt or unknown values and falls back to the default, and (3) variant 4 (the Nim slide-12 homework) asks for measurements the public API cannot deliver. There is also one mathematically-wrong heuristic implementation (`balanced-first`), a default-value mismatch with the variants.md text (`MAX_DEPTH = None` vs. variant 1 saying "Increase from 3 to 7"), and a docstring claim that the engine implements "standard alpha-beta" — but the root-level decision uses `max(iter, key=func)` which never threads alpha between sibling top-level children. These will all confuse a fresh exam agent reading only the docstrings.

---

## P0 — BLOCKING

### P0-1. TTT docstring lies about Nim → TTT KNOB propagation

**Location:** `tictactoe_template_solution.py` lines 127–134.

The header says, verbatim:

> Reuse the engine + KNOBs from the sister Nim module so that any change
> made there (USE_ALPHA_BETA_PRUNING, COUNT_NODES, etc.) flows through
> here automatically — see alpha_beta_solution.py for full KNOB docs.

That is **flat-out false**. The import block at lines 130–134 only imports `nodes_evaluated as _nim_nodes_evaluated`, `reset_node_counter`, and the module alias `_ab`. It imports **none** of the KNOB names. Then lines 171–200 of `tictactoe_template_solution.py` **redefine** `USE_ALPHA_BETA_PRUNING`, `COUNT_NODES`, `MOVE_ORDERING` as fresh module-level constants in the TTT module's namespace.

The `minmax_decision` function inside `tictactoe_template_solution.py` (lines 280–326) reads `USE_ALPHA_BETA_PRUNING` and `COUNT_NODES` via the module's own globals — NOT via `_ab.USE_ALPHA_BETA_PRUNING`.

**Concrete consequence.** A student following the docstring will open `alpha_beta_solution.py`, flip `USE_ALPHA_BETA_PRUNING = False` (line 119), run `tictactoe_template_solution.py`, and observe that nothing changes — TTT still prunes because TTT reads its own line-177 constant. This is the single most likely setup for variant 1, which is the most-tested variant ("nodes evaluated with and without pruning"). The variants.md walkthrough at variant 1 step 2 says: *"set ... USE_ALPHA_BETA_PRUNING = True / False"* — without telling the student **which file** to edit. With the docstring's lie, the student will edit Nim and see no effect, conclude the KNOB is broken, and write `VERDICT: STUCK`.

**Why this is P0, not P1.** The variants.md is the *primary* path the exam agent will take. The docstring is the *only* documentation the exam agent is allowed to read (per variants.md "How exam agents are expected to behave"). The combination guarantees a fresh agent will fail variant 1.

**Fix (pick one):**
- (a) **Genuinely propagate.** Delete TTT's local re-definitions at lines 171, 177, 184, 200, and make `minmax_decision` read `_ab.USE_ALPHA_BETA_PRUNING`, `_ab.COUNT_NODES`, etc. Then the docstring would be true. Keep TTT-only KNOBs (`MAX_DEPTH`, `EVALUATOR`, `DEMO_MODE`, `STARTING_BOARD`, `RANDOM_SEED`) local. Note: `MOVE_ORDERING` would still need to be TTT-local because Nim's values (`balanced-first` etc.) are meaningless for TTT — call it out in the docstring.
- (b) **Match docstring to reality.** Rewrite lines 127–134 to say: *"Each game has its own KNOB block. Setting `USE_ALPHA_BETA_PRUNING = False` in this file affects only the Tic-Tac-Toe game. The Nim file `alpha_beta_solution.py` has an independent block of the same name."* Then update variants.md variant 1 / variant 3 to specify the file the student must edit. This is the lower-risk fix.

**Evidence:** TTT lines 127–134 (docstring), 130–134 (import block), 171, 177, 184, 200 (re-defined KNOBs), 282, 295, 313 (uses of locals not `_ab.*`).

---

### P0-2. `MOVE_ORDERING = "balanced-first"` (Nim) ranks the wrong quantity

**Location:** `alpha_beta_solution.py` lines 289–295 and 322–329.

The KNOB documentation at lines 131–143 promises:

> "balanced-first" tries splits closest to equal halves first (often best for MAX).

The implementation at lines 289–295 sorts the **successor states** by `_imbalance_score`, which is defined at lines 324–329 as `max(piles) - min(piles)` over the **entire successor state** (not just the new pair).

Example trace. Suppose the current Nim state is `[4, 7]` (USER has already split [11] into [4,7]) and we want successors:

- Splitting pile 0 (the `4`) into [1,3] gives successor `[1, 3, 7]`. `_imbalance_score = 7 - 1 = 6`.
- Splitting pile 1 (the `7`) into [1,6] gives `[4, 1, 6]`. `_imbalance_score = 6 - 1 = 5`.
- Splitting pile 1 (the `7`) into [2,5] gives `[4, 2, 5]`. `_imbalance_score = 5 - 2 = 3`.
- Splitting pile 1 (the `7`) into [3,4] gives `[4, 3, 4]`. `_imbalance_score = 4 - 3 = 1`.

`balanced-first` sorts ascending, so the order is: `[4,3,4]`, `[4,2,5]`, `[4,1,6]`, `[1,3,7]`. **The first one IS the most-balanced split of the largest pile**, but only because the untouched `4` happens to match `[3,4]` closely. Consider state `[3, 9]`:

- [3]→[1,2] gives `[1, 2, 9]`. Score = 8.
- [9]→[1,8] gives `[3, 1, 8]`. Score = 7.
- [9]→[2,7] gives `[3, 2, 7]`. Score = 5.
- [9]→[3,6] gives `[3, 3, 6]`. Score = 3.
- [9]→[4,5] gives `[3, 4, 5]`. Score = 2.

`balanced-first` order: `[3,4,5]`, `[3,3,6]`, `[3,2,7]`, `[3,1,8]`, `[1,2,9]`. Here the heuristic *does* put the most-balanced new pair first ([4,5] is balanced; [1,8] is skewed). But this is a coincidence: the `[3]` is small, so the dominant term in `max - min` IS the new pair's spread.

Now consider state `[2, 9]` (i.e. a leftover pile of size 2 sits alongside the splittable pile):

- [9]→[1,8] gives `[2, 1, 8]`. Score = 7.
- [9]→[2,7] gives `[2, 2, 7]`. Score = 5.
- [9]→[3,6] gives `[2, 3, 6]`. Score = 4.
- [9]→[4,5] gives `[2, 4, 5]`. Score = 3.

Still ranks correctly because the leftover pile (size 2) is the *smallest*, so the `min` is fixed at 2 (or below) and the variation comes from the new pair's larger half. OK.

But consider `[10, 5]`:

- [10]→[1,9] gives `[1, 9, 5]`. Score = 9-1 = 8.
- [10]→[2,8] gives `[2, 8, 5]`. Score = 8-2 = 6.
- [10]→[3,7] gives `[3, 7, 5]`. Score = 7-3 = 4.
- [10]→[4,6] gives `[4, 6, 5]`. Score = 6-4 = 2.
- [5]→[1,4] gives `[10, 1, 4]`. Score = 10-1 = 9.
- [5]→[2,3] gives `[10, 2, 3]`. Score = 10-2 = 8.

`balanced-first` order: `[4,6,5]`, `[3,7,5]`, `[2,8,5]`, `[1,9,5]`+`[10,2,3]` (tie at 8), `[10,1,4]`. So the **most-balanced new pair** (`[4,6]`) does come first, but the **most-skewed new pair** (`[1,9]`) is ranked equally with the *least*-skewed split of `[5]` (`[2,3]`). And `[10]→[1,9]` is ranked AHEAD of `[5]→[1,4]` even though the latter is a more-skewed split of its own pile. So the heuristic is **conflating new-pair imbalance with whole-state imbalance**.

**Why this is P0:** Variant 3 of variants.md ("Move-ordering ablation") asks the student to compare pruning effectiveness across orderings. With `balanced-first` defined as "most-balanced new pair first" in the docstring but implemented as "smallest whole-state spread first", the student will draw the wrong conclusion about *why* one ordering prunes better than another. Worse, since this is the Nim file's only KNOB-3 value tied to a pedagogical claim, the variant 3 deliverable will rest on a wrong heuristic.

Additionally, the `_imbalance_score` is applied **to the post-split state**, which always contains the *unchanged* piles. For game states with many unchanged piles (deep into the game), the new-pair contribution is a small fraction of the total spread, and the heuristic essentially degenerates to "sort by largest leftover pile" — which has *nothing* to do with split balance.

**Fix:** Track the new pair in `successors_of` and pass it to the ordering function:

```python
for split in split_pile_options(pile):
    new_state = state[:i] + split + state[i + 1:]
    successors.append((new_state, split))  # tag with the new pair

if MOVE_ORDERING == "balanced-first":
    successors.sort(key=lambda x: max(x[1]) - min(x[1]))
elif MOVE_ORDERING == "skewed-first":
    successors.sort(key=lambda x: -(max(x[1]) - min(x[1])))

return [s for s, _ in successors]
```

Then either rewrite the docstring at lines 131–143 to match the (current, broken) "whole-state imbalance" semantics, or fix the code as above.

**Evidence:** Nim lines 131–143 (docstring), 289–295 (call site), 322–329 (heuristic body).

---

### P0-3. Variant 4 cannot be solved via the public Nim API

**Location:** Variants.md variant 4, plus `alpha_beta_solution.py` lines 172–225.

Variant 4 step 1 says:

> Inspect the root utility by importing and calling — or just play through

To "inspect the root utility" of state `[15]` from outside, an exam agent must call something like `min_value([15], -inf, +inf)` (because USER = MIN moves first). But `min_value` and `max_value` are **nested functions** defined inside `alpha_beta_decision` at lines 184 and 203. They are NOT exposed at module level.

The only public function is `alpha_beta_decision(state)` which returns the **best successor STATE for MAX** — not the utility value, and it assumes the *computer* is about to move. So from `[15]`:

- If COMPUTER_PLAYS_MAX = True and USER moves first, the examiner must first invoke a USER move. The examiner has no programmatic "MIN player" function and must therefore play interactively, which the variant explicitly tries to avoid ("or just play through" is the *fallback*, not the primary path).
- Alternatively the examiner could call `alpha_beta_decision([15])` directly, but that gives the *MAX-to-move* answer for `[15]` — which is the wrong root for variant 4's question (variant 4 asks: starting from [15] with USER going first, can COMPUTER force a win?).

The examiner has no public way to ask "what is `utility_of` at the root of an N-token Nim game assuming optimal play?" without rewriting `alpha_beta_decision` or copy-pasting `min_value`.

**Why this is P0:** Variant 4 is explicitly listed as an exam-question variant. A fresh agent cannot solve it from the docstrings + KNOBs alone, which is the variants.md ground rule. Either the variant must be downgraded ("optional, requires interactive play") or the API must expose `root_utility(state)` / `min_value` / `max_value`.

**Fix (pick one):**
- (a) Hoist `min_value` and `max_value` to module-level functions, exposed in `__all__`.
- (b) Add a convenience function `root_utility(state: Piles, *, to_move: str = "MIN") -> int` at module level that does the recursion and returns the int.
- (c) Add a KNOB `STARTING_PLAYER ∈ {"USER", "COMPUTER"}` and rewrite `main()` so that COMPUTER goes first when set — letting the exam agent observe whether COMPUTER wins by simply watching the game.

**Evidence:** variants.md variant 4 (lines 113–134); Nim lines 172–225 (nested-function structure).

---

## P1 — IMPORTANT

### P1-1. Every KNOB silently swallows misspelt or out-of-range values

**Locations:**
- Nim `successors_of` lines 291–295: unknown `MOVE_ORDERING` falls through to "natural" via the comment-only `else` branch.
- TTT `_apply_move_ordering` line 463: unknown `MOVE_ORDERING` returns successors unsorted (also "natural").
- TTT `_evaluate` line 485: unknown `EVALUATOR` falls back to `_score_lines(..., center_weight=1)`.
- Nim `utility_of` line 268–269: `COMPUTER_PLAYS_MAX` only checks truthiness, so `"True"` (string) silently behaves like `True`.

A student who writes `MOVE_ORDERING = "center first"` (space, not hyphen) or `EVALUATOR = "centered"` will get the default behaviour with **no warning and no exception**. They will then report numbers as if their KNOB took effect — which it didn't — and conclude that the KNOB doesn't actually change anything. This is precisely the failure mode the exam-prep agents are designed around.

**Fix:** Add an assertion at module top-of-file:

```python
assert MOVE_ORDERING in {"natural", "center-first", "corners-first", "random"}, \
    f"Unknown MOVE_ORDERING={MOVE_ORDERING!r}"
assert EVALUATOR in {"lines", "center-weighted", "rows-cols-diags"}, \
    f"Unknown EVALUATOR={EVALUATOR!r}"
assert isinstance(MAX_DEPTH, (int, type(None))), \
    f"MAX_DEPTH must be int or None, got {type(MAX_DEPTH).__name__}"
```

Same for Nim's `MOVE_ORDERING ∈ {"natural", "balanced-first", "skewed-first"}` and `COMPUTER_PLAYS_MAX is True or False`.

**Why P1 not P0:** With diligent typing the variants do run, so this doesn't BLOCK the variants — it just makes silent failures easy. Borderline P0 in my opinion; downgraded because a careful student would notice the same "lines" numbers across all EVALUATOR settings and re-check.

---

### P1-2. `MAX_DEPTH = None` default contradicts the variants.md text

**Location:** TTT line 151 (default `MAX_DEPTH: int | None = None`); variants.md variant 1 line 18.

Variant 1 reads, verbatim:

> Increase the minimax tree-depth limit from 3 to 7.

That assumes the **starting/default value is 3**. The actual default is `None` (full-depth search to terminal). The docstring at TTT lines 142–151 then describes 3 as "default in many course examples" — not "the default in this file".

This is a defect of *internal consistency* between the variants.md and the file. An exam agent reading "Increase from 3 to 7" will set `MAX_DEPTH = 3` then `MAX_DEPTH = 7`. Their *baseline* (MAX_DEPTH=3) measurement is then the one they should compare against. Fine. But if any other variant uses `MAX_DEPTH=None` (e.g. variant 3 explicitly does), then the running "default" shifts between variants in ways that the docstring should call out clearly.

**Fix:** Either change the default to `MAX_DEPTH = 3` (matching variant 1's phrasing), or rewrite variant 1 to say "Set MAX_DEPTH to 3, then 7". The current state mixes two conventions.

**Why P1:** Doesn't break correctness; just inconsistent.

---

### P1-3. Docstring claims "standard alpha-beta" but the root never threads alpha

**Location:** TTT `minmax_decision` lines 267–326; Nim `alpha_beta_decision` lines 172–225.

The TTT docstring at lines 271–273 says:

> Implementation: alpha-beta on top of the minimax framework from Lecture 6 §3.

And the Nim docstring at lines 177–181:

> The structure (max_value / min_value with running alpha and beta) is the
> standard alpha-beta search from Lecture 6 §3.

But the **root-level** decision in both files uses Python's `max(iter, key=func)` / `min(iter, key=func)` / `argmax(iter, lambda)`:

- TTT lines 323–325: `action, _ = max(children, key=lambda a: min_value(a[1], -infinity, infinity, 1))` and the mirror `min(...)` for O.
- Nim lines 221–225: `state = argmax(successors_of(state), lambda a: min_value(a, -infinity, infinity))`.

The `key=func` argument calls `func` on each child **independently**. There is no shared `alpha` variable updated across the iteration; each top-level child sees `alpha = -infinity`. Standard alpha-beta would say:

```python
alpha = -infinity
best = None
for child in children:
    v = min_value(child, alpha, +infinity, 1)
    if v > alpha:
        alpha = v
        best = child
```

This is the textbook form. The pattern used in the handout (`max(iter, key=func)`) is **a known suboptimality of the handout's template** — and it propagates to the solution unchanged.

Concrete cost: in TTT with `MAX_DEPTH = 3`, the root has 9 children. Each child is independently searched with `alpha = -infinity`, so a strong first child cannot tighten the alpha bound for siblings. The savings would be modest (perhaps 5–15% fewer nodes), but the variant 1 measurement is exactly counting these nodes — and the claim in the docstring is that this is "standard alpha-beta search". It is not.

**Why P1:** The variants still produce *correct* moves and *correct* qualitative observations (pruning < no-pruning). The numbers are just slightly higher than a true textbook alpha-beta would give. But the docstring should not call this "standard" — it is the handout's variant.

**Fix:** Rewrite the root loop to thread alpha (or call it out in the docstring as a "handout-style root, no top-level alpha update").

---

### P1-4. `MAX_DEPTH` is silently unavailable to the Nim game

**Locations:** Nim file (no `MAX_DEPTH` KNOB anywhere); TTT line 151.

The brief lists `MAX_DEPTH` as a KNOB to check across **both** solution files. The TTT file defines it. The Nim file does NOT. A student who reads "MAX_DEPTH = 3" advice from the L06 lecture and applies it to the Nim REPL will find no such constant in `alpha_beta_solution.py`. The Nim docstring at lines 86–143 lists KNOBs but `MAX_DEPTH` is absent.

This may be by design (Nim from `[7]` or `[15]` is small enough that full-depth search is feasible — that's the whole point of the slide-12 homework), but the asymmetry should be **explicitly called out** in the Nim docstring: *"This module deliberately omits MAX_DEPTH because Nim's branching factor is small. Use the TTT module if you want to experiment with depth-cut search."*

**Fix:** One sentence in the Nim docstring header. Or actually add a `MAX_DEPTH: int | None = None` KNOB to Nim and a `_evaluate(state)` heuristic for material-count, then mention this is unused at defaults but available for symmetry. The cleaner fix is the docstring sentence.

---

### P1-5. `EVALUATOR` is dead code at defaults; variant 2 requires `MAX_DEPTH ≠ None`

**Location:** TTT lines 153–169 (`EVALUATOR` KNOB), 287–290 and 307–308 (cutoff frontier — only place `_evaluate` is called).

`_evaluate` is only called inside `max_value`/`min_value` when `MAX_DEPTH is not None and depth >= MAX_DEPTH`. With the default `MAX_DEPTH = None`, the cutoff branch is never taken, and the EVALUATOR KNOB has **zero effect** on any measurement.

Variant 2 ("Centre-weighted evaluator") correctly tells the student to also set `MAX_DEPTH = 2`. Good. But the TTT docstring's KNOB block at lines 152–169 nowhere says "only relevant when MAX_DEPTH is finite" — it does at line 76 (in the HOW TO ADAPT section), but that's far from the KNOB definition. A student reading the KNOB block alone might think setting `EVALUATOR = "center-weighted"` would change something.

**Fix:** Add to the KNOB description at line 154–169: *"Has NO effect unless MAX_DEPTH is set to a finite value. At terminal leaves `utility_of` is always exact."*

---

### P1-6. `_score_lines` "lines" heuristic does not match its own docstring

**Location:** TTT lines 488–510.

The docstring at lines 489–494 says:

> each line in which exactly one player has any presence scores +1 (for X) or -1 (for O).

But the code at lines 495–503 does:

```python
xs = sum(1 for s in cells if s == Symbols.X)
os_ = sum(1 for s in cells if s == Symbols.O)
if xs > 0 and os_ == 0:
    score += xs       # NOT +1 — adds the count of Xs on this line
elif os_ > 0 and xs == 0:
    score -= os_
```

This scores +1 for one X, +2 for two Xs, +3 for three Xs (a terminal win). That is **NOT** what the docstring says ("+1 ... or -1"). The actual implementation is "the count of X's presence on a line MAX has uncontested" — which is a perfectly reasonable heuristic, but it doesn't match the docstring's flat "+1/-1" claim.

Variant 2 deliverables include "compare the final board against the run with `EVALUATOR = "lines"`". A student who memorises the docstring claim ("each open line scores +1 for X") will predict different numbers than what the code computes.

**Fix:** Rewrite the docstring at lines 489–494 to say *"each line where MAX has uncontested presence contributes the number of X's on it (1, 2, or 3); each line where MIN has uncontested presence contributes -(number of O's)"*. Or change the code to score a flat `+1` and `-1` to match the docstring (then `center-weighted` becomes more obviously different from `lines`).

---

### P1-7. `EVALUATOR = "rows-cols-diags"` has no MAX_DEPTH-safe property

**Location:** TTT lines 513–523 (`_score_open_lines`).

The "rows-cols-diags" heuristic counts winnable lines for each side. The KNOB docstring at line 165–166 describes this as "a coarser estimate". Fine. But there is no test in `_evaluate` that the value returned by `_score_open_lines` ever agrees in sign with `utility_of` at terminal-adjacent states. The KNOB documentation at line 477–478 promises: *"All three evaluators agree in sign with `utility_of` at every state where the latter is +/-1"*.

Test case: a state where X has won (utility +1) but the board still has open cells (some lines still have UNPLACED). `_score_open_lines` would count any line not containing O as winnable for X (`x_winnable`), and any line not containing X as winnable for O. For X-three-in-a-row on the diagonal `(0,4,8)` with otherwise empty board:
- `x_winnable`: lines not containing O = all 8 lines (no O anywhere). → 8.
- `o_winnable`: lines not containing X = lines that don't include 0, 4, or 8 = `{(3,4,5)? no, 4 in there. (1,4,7)? no. (2,4,6)? no. (0,3,6)? has 0. (1,4,7)? has 4. (2,5,8)? has 8. (0,1,2)? has 0. (6,7,8)? has 8. (3,4,5)? has 4.}` — so o_winnable = 0.
- Score = 8 - 0 = 8. Sign agrees with +1. OK.

But consider a state where X plays at (4), then O plays at (0), then X plays at (8), then O plays at (1) (not a winning line yet, no terminal):
- `x_winnable`: lines without O. O is at 0 and 1. Lines avoiding both: `(3,4,5)`, `(6,7,8)`, `(2,5,8)`, `(2,4,6)` = 4 lines.
- `o_winnable`: lines without X. X is at 4 and 8. Lines avoiding both: `(0,1,2)`, `(0,3,6)`, `(6,7,8)? has 8`, `(2,5,8)? has 8`. So `(0,1,2)` and `(0,3,6)` = 2 lines.
- Score = 4 - 2 = +2.

This is positive — would suggest X is winning. But O has the corner (0) and an edge (1) which is a known opening trap. The heuristic seems serviceable here.

The issue: `_score_open_lines` doesn't enforce the sign-agreement promise at *all* terminal-adjacent states. It is at least theoretically possible to construct a state where X has won via diagonal `(0,4,8)` but O has a strong presence on lines `(1,4,7)` and `(3,4,5)` — those lines lose X-winnability because of O, while X still has uncontested lines elsewhere. Let me not chase the edge case further: the *promise* in the docstring is unverified.

**Why P1:** The "agrees in sign" claim at line 477 is a load-bearing pedagogical claim. If a student writes that on an exam, the examiner could ask "prove it" and the answer is non-trivial. Better to weaken the claim to "the three evaluators are consistent in direction on most reachable states".

**Fix:** Weaken or remove the "agrees in sign" promise. Add a test or counterexample search to verify it (out of scope for this review).

---

### P1-8. `MOVE_ORDERING = "natural"` is a different starting point in TTT vs. Nim

**Locations:** TTT line 200 (default `MOVE_ORDERING = "center-first"`); Nim line 143 (default `MOVE_ORDERING = "natural"`).

The default `MOVE_ORDERING` differs between the two files:
- Nim defaults to `"natural"`.
- TTT defaults to `"center-first"`.

This is defensible (center-first is genuinely the best opening heuristic for TTT), but the inconsistency means:
- Variant 3 step 1 says "Keep ... `USE_ALPHA_BETA_PRUNING = True`, `COUNT_NODES = True`" but does NOT mention `MOVE_ORDERING` for the *baseline* — the student must explicitly switch to `"natural"` to recover the baseline TTT ordering.
- Variant 1 says "set `MAX_DEPTH = 3`" then read nodes. With the default `MOVE_ORDERING = "center-first"`, the nodes count for ply 1 is different from a true "natural" baseline.

The variants.md walkthroughs don't say "be sure to reset MOVE_ORDERING" — and a student running variant 1 then variant 3 without restarting Python may carry over a stale `MOVE_ORDERING` from a previous experiment (since the constants are module-level).

**Fix:** Either harmonise defaults (both `"natural"`) and let variants explicitly opt into other orderings, or add a "Defaults Used in This Variant" line at the top of each variants.md walkthrough. The cleaner fix is the latter.

---

### P1-9. `USE_ALPHA_BETA_PRUNING` does NOT change `COUNT_NODES` behaviour — but the print line claims otherwise

**Location:** Nim line 394–396; TTT line 569–571.

Both print blocks include `pruning={USE_ALPHA_BETA_PRUNING}` in the trace line:

Nim: `print(f"[alpha-beta] evaluated {nodes_evaluated} states (pruning={USE_ALPHA_BETA_PRUNING}, ordering={MOVE_ORDERING})")`

That correctly tags the trace with the current KNOB. But there is a subtle interaction the docstring should call out: when `USE_ALPHA_BETA_PRUNING = False`, the `expected_value >= beta` check and `v <= alpha` check are skipped, so the recursion becomes plain minimax. **However**, `nodes_evaluated` is incremented BEFORE the terminal/depth check at every call, so the count includes the root call to `max_value`/`min_value` plus every child call. With pruning off, the count grows as $O(b^d)$; with pruning on, it shrinks to roughly $O(b^{d/2})$ in the best case.

This is correct behaviour — but the docstring nowhere quantifies what the student should *expect* the ratio to look like at MAX_DEPTH=3 vs MAX_DEPTH=7. The variants.md does say "the ratio grows with depth". A student needs to read both docs to understand the variant's deliverable.

**Why P1:** Documentation gap. The KNOBs themselves work. Just hard to draw the right conclusion from them without more pedagogical scaffolding.

**Fix:** Add an expected-magnitude hint to the variants.md variant 1 (e.g. "at MAX_DEPTH=3, ply-1 nodes are ~O(10^2); at MAX_DEPTH=7, ~O(10^4)") so the student knows when their measurement is "in the right ballpark".

---

### P1-10. KNOB block for TTT's `RANDOM_SEED` is unreachable without `MOVE_ORDERING = "random"`

**Location:** TTT lines 202–206.

`RANDOM_SEED` is documented as serving the `"random"` move ordering. It does, at line 457. But `"random"` ordering is the only consumer of the seed — no other randomness exists in either file. The KNOB description at line 203–205 says "and any future randomised tie-breaker" — gesturing at functionality that doesn't exist.

**Why P1:** Misleads the student into thinking there's more randomness to control than there actually is.

**Fix:** Drop "and any future randomised tie-breaker" from line 204, or implement a tie-breaker. The honest fix is the docstring tweak.

---

### P1-11. `DEMO_MODE = "interactive"` is not tested by any variant and may be silently broken

**Location:** TTT lines 594–615.

`_interactive()` reads `input()` for the human's move. It is documented as "KEPT FOR PEDAGOGY — not used by the Verifier or the exam agents". No variant in variants.md uses it.

But the interactive function lacks the `KNOBS:` banner that `_self_play()` prints at lines 568–572, and it doesn't display the board BEFORE the first computer move (line 603 just makes the move with no display). A student switching DEMO_MODE will see different behaviour from the self-play they read about in the variants.md. Probably broken on first read, will work after squinting at the code.

**Why P1:** A KNOB that is documented but produces an inferior UX is still a usability bug.

**Fix:** Either delete `_interactive` (and the `DEMO_MODE` KNOB), or harmonise its output with `_self_play`.

---

## P2 — POLISH / MINOR

### P2-1. TTT line 132 `noqa: F401 (re-exposed below)` is a lie
The import `_nim_nodes_evaluated` is never re-exposed below; the comment promises something that doesn't happen. Remove the comment or actually re-export.

### P2-2. Nim line 245–269 `utility_of` returns `0` for non-terminal states
The docstring says "Non-terminal states do not have a defined utility". OK, but the code at line 263–266 explicitly returns 0 — and the minimax recursion only ever calls `utility_of` on terminal states (it checks `is_terminal` first). So this defensive branch is dead code. Either delete it or convert it to `raise ValueError("utility_of called on non-terminal state")` to surface bugs.

### P2-3. TTT line 343–347: `is_terminal` description
Says "someone has three in a row OR the board is completely filled". The actual `winner_of` already covers "three in a row OR diagonal". Wording fine, but "three in a row" reads as ambiguous (might mean a literal row); the slide language is "wins" — match the slide wording.

### P2-4. Both files: `nodes_evaluated` counter increments on ENTRY to `max_value`/`min_value`, not on leaf evaluation
The KNOB documentation at Nim lines 121–129 and TTT lines 179–184 says "count visited states". A student reading "states evaluated" might expect only leaf evaluations. The current count includes every internal node too. Variant 1 expects this (the slide phrasing is "nodes evaluated"), but worth one sentence: *"This counts every recursive call, including internal nodes — not just leaves."*

### P2-5. Nim line 313 `for j in range(1, pile)`
Already returned at line 316 once `j == pile // 2`. The outer loop continues running until `j = pile - 1`. With small piles (7, 15, 20) this is negligible. Trivial optimisation: `for j in range(1, pile // 2 + 1)`.

### P2-6. TTT line 322 `_to_move(state)` is recomputed once per call to `minmax_decision`
But `_to_move` re-counts the board O(9). Trivial. Could be replaced with a `side` parameter threaded through the recursion.

### P2-7. TTT line 200 default `MOVE_ORDERING = "center-first"`
The `Effect:` text at lines 195–199 says "a textbook ordering for Tic-Tac-Toe". Polish: cite the textbook explicitly (R&N AIMA §5.4 mentions move-ordering for TTT? — would need verification).

### P2-8. Nim line 132–139 (`MOVE_ORDERING` block) does not list the variants.md values it serves
The TTT MOVE_ORDERING block at line 186–199 names the relevant variants.md variant in line 198 ("variant 3"). The Nim MOVE_ORDERING block at line 141–142 also names "variant-3" but lower-cased and dashed. Cosmetic — pick a consistent variant-numbering convention.

### P2-9. TTT KNOB block formatting inconsistency
Some KNOBs use `(default=X, allowed={...})`, some use `(default=X, allowed=Y)`. The `allowed=` value is sometimes a set, sometimes a free-form sentence. Pick one.

### P2-10. Both files print the KNOB banner only for `DEMO_MODE = "self-play"`
Nim's `main` at line 383–399 has no KNOB banner. A student doing variant 4 (Nim, START_PILE=15) cannot tell from the transcript whether `USE_ALPHA_BETA_PRUNING` was True or False. The Nim file has the line at 394 ("pruning=...") but only after a move — and never with `START_PILE` echoed. Add a banner like `[alpha-beta] START_PILE=15, COMPUTER_PLAYS_MAX=True, ...` at the top of `main()`.

### P2-11. TTT line 254 `nodes_evaluated: int = 0` shadows Nim's line 159 same-named global
The two `nodes_evaluated` are in different modules so Python's namespace isolation handles it — but a debugger session that imports both modules and inspects "nodes_evaluated" gets the wrong one half the time. Rename one (e.g. TTT's to `ttt_nodes_evaluated`).

### P2-12. TTT line 469 `_to_move` parity rule is restated in code without docstring cross-reference
`open_count % 2 == 1` → X. The same parity rule is encoded twice — once in `successors_of` at line 409, once in `_to_move` at line 469. They agree, but if one is ever changed the other won't be. Extract a single `_side_to_move(state)` helper.

### P2-13. Nim line 290 (`_imbalance_score`) is named misleadingly
Returns `max(piles) - min(piles)`. That's the *range* (spread), not the *imbalance* (which would be a relative measure, like `(max - min) / mean`). Rename to `_state_range` or `_max_min_spread`.

### P2-14. TTT line 458 `import random` inside the function
Top-of-file imports are conventional; importing inside `_apply_move_ordering` is fine (it's only used for one branch) but defeats lint tools. Minor.

### P2-15. TTT line 568–572 KNOB banner prints `repr(EVALUATOR)` (with quotes) but `MAX_DEPTH` (without)
`KNOBS: MAX_DEPTH=3, EVALUATOR='lines', USE_ALPHA_BETA_PRUNING=True, MOVE_ORDERING='center-first'`. Cosmetic inconsistency.

### P2-16. TTT line 220–228 STARTING_BOARD KNOB
Allows examiner to set a custom starting board. But `_starting_board` at line 544–550 only validates `len == 9`, not the X/O count. The KNOB docstring at line 224–226 says "X must be played between 0 and 1 more times than O". That's checked only implicitly via `_to_move` parity. A board with two X's and zero O's would still be accepted; `_to_move` would say "O's turn" (correct — there are 7 unplaced cells, odd, so X-to-move? wait, `open_count = 7` → odd → X. But X has already played twice and O zero times — X is one ahead. Then X plays a third time without O moving. That's illegal in TTT.) The KNOB's promise is unenforced.

### P2-17. TTT line 467 `_to_move` returns `Symbols.X` or `Symbols.O` — but `is` comparison at line 322 uses `is`, not `==`
Enum instances compare correctly with `is` in CPython because each member is a singleton. Portable, but pedantic style hints in PEP 8 prefer `==` for enums (https://peps.python.org/pep-0008/ "Comparisons to singletons like None should always be done with is or is not, never the equality operators.") So `is` is OK for Symbols values too (they are singletons). Polish.

---

## EVIDENCE

| Issue | File | Line(s) |
|---|---|---|
| P0-1 docstring lies about KNOB propagation | TTT | 127–134, 171, 177, 184, 200, 282, 295, 313 |
| P0-2 `balanced-first` ranks wrong quantity | Nim | 131–143, 289–295, 322–329 |
| P0-3 variant 4 cannot use public API | Nim | 172–225 |
| P1-1 silent fallback on unknown KNOB values | Nim 291–295; TTT 463, 485 |  |
| P1-2 MAX_DEPTH default contradicts variants.md | TTT | 151; variants.md L18 |
| P1-3 root never threads alpha | TTT 323–325; Nim 221–225 |  |
| P1-4 MAX_DEPTH absent from Nim | Nim | (omission) |
| P1-5 EVALUATOR dead at defaults | TTT | 153–169, 287–290, 307–308 |
| P1-6 `_score_lines` doesn't match docstring | TTT | 488–510 |
| P1-7 `rows-cols-diags` sign-agreement claim unverified | TTT | 477, 513–523 |
| P1-8 MOVE_ORDERING defaults differ across files | TTT 200; Nim 143 |  |
| P1-9 USE_ALPHA_BETA_PRUNING magnitudes not in docs | both | KNOB blocks |
| P1-10 RANDOM_SEED docs reference non-existent feature | TTT | 202–206 |
| P1-11 DEMO_MODE="interactive" lacks banner | TTT | 594–615 |
| variants.md variant 1 phrasing baseline | variants.md | L18 ("from 3 to 7") |
| variants.md variant 2 EVALUATOR + MAX_DEPTH | variants.md | L62–63 |
| variants.md variant 3 ordering sweep | variants.md | L87–101 |
| variants.md variant 4 Nim API requirement | variants.md | L113–134 |

---

## Report to PM

**Assignment recap:** Lab5-AlphaBeta Round 1 — KNOB Coverage review. Verify that `MAX_DEPTH`, `EVALUATOR`, `USE_ALPHA_BETA_PRUNING`, `MOVE_ORDERING` in `alpha_beta_solution.py` and `tictactoe_template_solution.py` faithfully serve the four exam variants in `study/_exam/Lab5-AlphaBeta/variants.md`.

**Status:** Fail. Three P0 issues block Round 2; eleven P1 issues degrade KNOB usability; seventeen P2 polish items.

**P0 findings:**
1. **TTT docstring lies about KNOB propagation from Nim** (TTT lines 127–134 vs. lines 171, 177, 184, 200). The TTT module redefines `USE_ALPHA_BETA_PRUNING`, `COUNT_NODES`, `MOVE_ORDERING` locally; the docstring's claim that "any change made there ... flows through here automatically" is false. A fresh exam agent following the docstring will edit Nim, observe no change in TTT output, and conclude the KNOB is broken. **Fix: either rewrite the docstring to admit two independent KNOB blocks (low-risk), or refactor the TTT module to actually read `_ab.USE_ALPHA_BETA_PRUNING` (cleaner).** Affects variant 1 (the most-tested variant) and variant 3.
2. **`balanced-first` Nim move ordering ranks state-spread, not new-pair imbalance** (Nim lines 131–143, 289–295, 322–329). `_imbalance_score(piles) = max(piles) - min(piles)` is computed on the *entire* post-split state — including unchanged piles. With multi-pile states, the ranking can disagree with the docstring's "splits closest to equal halves first" promise. **Fix: tag successors with the new pair and sort by `max(pair) - min(pair)`.** Affects variant 3 (move-ordering ablation, on Nim).
3. **Variant 4 cannot be solved via the public Nim API** (variants.md variant 4 + Nim lines 172–225). `min_value`/`max_value` are nested inside `alpha_beta_decision` and not exposed. The examiner has no way to inspect "root utility from state [15] with USER to move" without rewriting the engine. **Fix: hoist `min_value`/`max_value` to module level, OR add a `root_utility(state, *, to_move)` convenience function, OR add a `STARTING_PLAYER` KNOB.**

**P1 findings:**
1. **P1-1.** Every KNOB silently swallows misspelt/unknown values (Nim line 295; TTT lines 463, 485). Add startup assertions.
2. **P1-2.** `MAX_DEPTH = None` default contradicts variants.md variant 1 phrasing "Increase from 3 to 7" (TTT line 151; variants.md line 18). Pick one convention.
3. **P1-3.** Both root-decision loops use `max(iter, key=func)` / `argmax` — never threading alpha across sibling top-level children (TTT lines 323–325; Nim lines 221–225). Docstring claim of "standard alpha-beta" is overpromised.
4. **P1-4.** `MAX_DEPTH` absent from the Nim file (Nim file). Docstring should explicitly call out the asymmetry or add the KNOB.
5. **P1-5.** `EVALUATOR` is dead code at defaults (`MAX_DEPTH = None` skips all calls to `_evaluate`) (TTT lines 153–169 + 287–290). KNOB block should say "no effect unless MAX_DEPTH is finite".
6. **P1-6.** `_score_lines` body does not match its docstring ("+1 per line" vs. "+(count of Xs on line)") (TTT lines 488–510).
7. **P1-7.** "All three evaluators agree in sign with `utility_of`" claim is unverified at edge cases (TTT line 477).
8. **P1-8.** `MOVE_ORDERING` default differs between Nim (`"natural"`) and TTT (`"center-first"`) (Nim 143; TTT 200). Cross-variant comparisons need explicit baseline reset.
9. **P1-9.** `USE_ALPHA_BETA_PRUNING` KNOB docs lack expected-magnitude hints. Variants.md alludes to "ratio grows with depth" but no concrete numbers.
10. **P1-10.** `RANDOM_SEED` docs reference "any future randomised tie-breaker" — non-existent feature (TTT lines 202–206).
11. **P1-11.** `DEMO_MODE = "interactive"` lacks the KNOB banner that self-play prints (TTT lines 594–615).

**P2 findings:**
1. P2-1 `noqa: F401 (re-exposed below)` is a lie — never re-exposed (TTT line 132).
2. P2-2 Defensive `return 0` for non-terminal `utility_of` is dead code (Nim 263–266).
3. P2-3 "three in a row" wording — slide says "wins" (TTT line 343–347).
4. P2-4 `nodes_evaluated` counts internal nodes, not just leaves — clarify.
5. P2-5 Nim line 313 loops past `pile // 2`.
6. P2-6 `_to_move` recomputed per call.
7. P2-7 "textbook ordering" needs citation (TTT line 195–199).
8. P2-8 Inconsistent variant-numbering style ("variant 3" vs "variant-3").
9. P2-9 KNOB block formatting inconsistency.
10. P2-10 No KNOB banner in Nim `main()`.
11. P2-11 `nodes_evaluated` name collides across modules.
12. P2-12 Parity-rule encoded twice (TTT line 409, line 469).
13. P2-13 `_imbalance_score` mis-named — actually returns range (Nim line 324).
14. P2-14 `import random` inside function (TTT line 458).
15. P2-15 KNOB banner mixes `repr` (with quotes) and direct values (TTT line 568–572).
16. P2-16 `STARTING_BOARD` X/O-count validation not enforced (TTT line 220–228, 544–550).
17. P2-17 `Symbols` `is` vs `==` — fine but pedantic.

**QA Checklist (§7) status (KNOB-coverage lens only):**
- [x] `MAX_DEPTH` KNOB present and wired — **Pass with concerns** (TTT only; not in Nim; default contradicts variants.md text).
- [x] `EVALUATOR` KNOB present, three options, hooked into `_evaluate` — **Pass with concerns** (dead at default MAX_DEPTH; docstring promise vs. code mismatch in `_score_lines`).
- [x] `USE_ALPHA_BETA_PRUNING` toggle works — **Pass with concerns** (P0-1 propagation lie; P1-3 root never threads alpha).
- [x] `MOVE_ORDERING` KNOB present in both files — **Fail** (P0-2 broken heuristic in Nim; P1-1 silent fallback on unknown values; P1-8 inconsistent defaults).
- [x] Variants 1–4 solvable from KNOBs + docstring alone — **Fail** (P0-3 variant 4 needs internal API; variant 1 likely-mis-set due to P0-1).
- [x] Silent KNOB swallowing — **Fail** (P1-1).

**Acceptance criteria (§1) status:** Variants.md is the de-facto acceptance criterion for this lab.
- Variant 1 (tree-depth + pruning comparison): **Not met** with confidence (P0-1 means the student will probably edit the wrong file; P1-2 default mismatch).
- Variant 2 (center-weighted evaluator): **Met with caveats** (KNOB works; P1-5 dead-at-default needs explicit MAX_DEPTH set per variants.md).
- Variant 3 (move-ordering ablation): **Partially met** (TTT side works; Nim side broken via P0-2).
- Variant 4 (Nim slide-12 homework): **Not met** (P0-3 — examiner can't get the answer from public API).

**DOCUMENT.md audit:** Out of scope for KNOB-coverage review; defer to structural reviewer.

**Out-of-scope observations:**
- The two solution files share a name `nodes_evaluated` and a name `USE_ALPHA_BETA_PRUNING` across modules. The TTT file imports `reset_node_counter` from Nim (line 132) but then defines its OWN `_reset_local_counter` (line 257). The Nim-imported `reset_node_counter` is **never called inside TTT** — line 577 of `_self_play` calls `_reset_local_counter()`, not the import. The import is dead. Remove the import or use it.
- The variants.md ground rules say exam agents "may NOT read function bodies". With the KNOBs documented only via the in-file docstring KNOB blocks, an agent who scrupulously follows this rule has *no way* to know that (a) `_score_lines` adds `xs` not `+1`, (b) `_imbalance_score` is whole-state, not new-pair, (c) the root loop is not standard alpha-beta. These three slippages between docstring and body are precisely the kind of thing the variants.md rule was designed to prevent — and the file violates it.
- The Nim docstring at line 50–53 mentions "with 7 tokens MIN (the human, who moves first) is certain to lose". This is a game-theoretic claim about Nim that the reviewer did not verify (out of scope for KNOB review, but worth a sanity check by Reviewer #1).
- The TTT docstring at line 110 promises that self-play "is always a draw (Tic-Tac-Toe is a solved game)". True for full-depth perfect play. With `MAX_DEPTH = 1` or 2 and a weak evaluator, self-play may produce a winner — verifying this would be a useful App Tester pass.

**Concerns / risks:**
- The P0-1 docstring lie is the single biggest risk for variant 1 — the most-likely-tested variant per the variants.md ordering.
- The P0-2 `balanced-first` bug is subtle enough that an examiner could write a question around it ("why does the predicted node-count differ from the measured one?") and the student would have no idea the heuristic is broken.
- The P0-3 API gap on variant 4 will probably manifest as `VERDICT: STUCK` from a fresh exam agent — which is the worst-case outcome for the variants-as-exam-questions design.
- The cumulative effect of P1-1 silent KNOB swallowing + P1-8 inconsistent defaults is that a student running variants 1 → 2 → 3 in sequence (without restarting Python) will accumulate stale KNOB state across measurements and report numbers that look reasonable but aren't the variant's intended measurement.

**What PM should do next:**
1. Dispatch Backend Engineer to fix P0-1 (docstring vs. reality on KNOB propagation) — choose the *low-risk* fix (rewrite docstring) unless full refactor is on the table. Update variants.md to specify which file to edit for variants 1 and 3.
2. Dispatch Backend Engineer to fix P0-2 (`balanced-first` semantic bug). Add a unit test that asserts the heuristic sorts by new-pair spread, not whole-state spread.
3. Dispatch Backend Engineer to fix P0-3 (variant 4 API gap). Recommended fix: add module-level `root_utility(state, *, to_move="MIN")` to `alpha_beta_solution.py` plus a one-paragraph variant-4 walkthrough in variants.md.
4. After P0 fixes, address P1-1 (assertion-based KNOB validation — cheapest win), P1-2 (default reconciliation), and P1-6 (docstring-code mismatch in `_score_lines`).
5. Do NOT proceed to App Tester until P0s are clear — App Tester's measurements of variants 1, 3, 4 will be wrong if the KNOBs they depend on don't behave as documented.
6. Defer P1-3 (root alpha-threading) and all P2s to a final-polish round.

**DOCUMENT.md updated:** N/A for QA.

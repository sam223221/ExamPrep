# Lab 5 — Alpha-Beta — Round 1 Revision Summary

**Role:** Reviser
**Files revised:**
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\alpha_beta_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\tictactoe_template_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab5-AlphaBeta\variants.md`

**Round 1 reviewers acted on:** Reviewer #1 (Correctness), Reviewer #2
(KNOB Coverage), Reviewer #3 (Pedagogical Clarity), Reviewer #4 (Variant
Adaptability).

---

## P0 fixes applied

### R2-P0-1 / R3-P0-2 / R4-P1-1 — "KNOB propagation" lie
**Symptom:** TTT header docstring claimed editing KNOBs in
`alpha_beta_solution.py` "flows through here automatically". In fact TTT
redefines its KNOBs locally; the Nim file's KNOBs do nothing to TTT.

**Fix (low-risk option):** rewrote the import block at TTT lines 124-132
to remove the dead imports (`reset_node_counter`,
`_nim_nodes_evaluated`, `_ab`) and replaced the misleading paragraph
with an explicit NOTE that each file has its own independent engine and
KNOB block. Updated the alpha_beta_solution.py "OUTPUTS WHEN RUN"
paragraph the same way.

### R2-P0-2 — `_imbalance_score` ranked the wrong quantity
**Symptom:** `_imbalance_score(state)` computed `max(state) - min(state)`
over the whole post-split state (including unchanged piles). For
multi-pile states this disagreed with the docstring promise "splits
closest to equal halves first".

**Fix:** changed `successors_of` to tag each successor with the new pair
and to sort by `_imbalance_score(pair)` rather than
`_imbalance_score(whole_state)`. Renamed the parameter from `piles` to
`pair` and updated the docstring. Verified empirically: from `[10, 5]`,
`balanced-first` now puts `[10,2,3]` (pair `[2,3]`, spread 1) first,
then `[4,6,5]` (pair `[4,6]`, spread 2), etc.

### R2-P0-3 — Variant 4 needed module-level `min_value`/`max_value`
**Symptom:** `min_value` and `max_value` were nested inside
`alpha_beta_decision`, so a fresh exam agent had no way to call
`min_value([15], -inf, +inf)` to inspect the root utility.

**Fix:** hoisted `max_value` and `min_value` to module level. Added a
new convenience function `root_utility(state, *, to_move="MIN")` that
exposes the recursion with the slide-10 default (MIN opens). Verified:
`root_utility([7]) → +1`, `root_utility([15]) → -1`,
`root_utility([20]) → +1`, and the sign flips when `COMPUTER_PLAYS_MAX`
is toggled (slide-12 step 3).

### R3-P0-1 — docstring "three TODOs" count wrong
**Symptom:** TTT header said "Slide 8 asks the student to: 1.
is_terminal; 2. utility_of; 3. successors_of" (three TODOs), but the
handout `tictactoe_template.py` ships five `raise NotImplementedError`
stubs (also `winner_of` and `is_full_board`). The section header at
line ~330 read `is_terminal / utility_of — the three slide-8 TODOs` but
only defined two functions in that block.

**Fix:** updated the header docstring to list all five TODOs explicitly
(three named on slide 8 + two helpers). Updated the section header to
match.

### R3-P0-3 — `reset_node_counter` cross-file reset (now moot)
**Symptom:** R3 reported that `reset_node_counter()` from the Nim module
was being called inside TTT, resetting the wrong counter. **Status:**
the actual call sites (`_self_play` and `_interactive`) were already
using `_reset_local_counter`. Removing the dead import in the R2-P0-1
fix also closes this footgun: the cross-file `reset_node_counter` name
is no longer in TTT's namespace, so a future maintainer cannot
accidentally call it.

### R3-P0 — `_score_lines` doesn't match L06 §3.4 "open lines" formula
**Symptom:** The function scored `+xs` (count of X's on the line) for
every line where X had uncontested presence. L06 §3.4 / pitfall #6
defines an open line as "no opponent on the line" and assigns it a flat
`+1` for X (or `-1` for O).

**Fix:** rewrote `_score_lines` to follow the L06 formula exactly: each
line with no O on it contributes `+1`; each line with no X on it
contributes `-1`. The centre-square bonus is then applied on top (this
is what differentiates `center-weighted` from `lines`). Updated the
docstring to cite L06 §3.4 explicitly. Also updated `_score_open_lines`
docstring to acknowledge it is now the same arithmetic.

### R4-P0-1 — Variant 2 degenerate at MAX_DEPTH=2
**Symptom:** At `MAX_DEPTH = 2`, `EVALUATOR ∈ {lines,
center-weighted}` produced byte-identical game transcripts — nothing
to report.

**Fix:** changed Variant 2's prescribed depth from `MAX_DEPTH = 2` to
`MAX_DEPTH = 3` in variants.md. Verified empirically: at depth 3,
`lines` → draw, `center-weighted` → X wins. Added explanation that
depth 2 is too shallow for the centre bonus to flip any decision.
(Combined with the R3-P0 fix to `_score_lines`, depth 3 is now the
canonical demo depth.)

### R4-P0-2 — Variant 3 "natural sits in between" was empirically false
**Symptom:** variants.md claimed `natural` ordering "sits in between"
center-first and corners-first. Actual node counts on ply 1:
center-first 15 705 < corners-first 20 666 < natural 30 709. Natural is
the WORST of the three.

**Fix:** rewrote the expected qualitative observation to match the
verified table (with empirical node counts) and explained the
intuition: `natural` walks cell indices 0,1,2,..., placing the centre
(cell 4) fifth, so alpha-beta sees four weaker children before the
strongest move.

---

## P1 fixes applied

### R1-P1-1 / R3-P0-2 (overlap) — dead imports
Removed the three dead imports from TTT (`nodes_evaluated as
_nim_nodes_evaluated`, `reset_node_counter`, `import alpha_beta_solution
as _ab`). Replaced with an explanatory NOTE block.

### R1-P1-3 — STARTING_BOARD validation gap
Strengthened `_starting_board()` to enforce all three docstring
promises:
- exactly 9 cells;
- every cell is a `Symbols` member;
- `x_count == o_count` OR `x_count == o_count + 1` (X moves first).
Also updated the type annotation from `list | None` to
`"list[Symbols] | None"`.

### R1-P1-4 — return-type annotations lied
`max_value` / `min_value` now annotated `-> float` (was `-> int`); they
can legitimately return `_INFINITY` from the bounds initialisers.

### R1-P1-5 — "only hit at draws" comment
Tightened the comment in `utility_of` to acknowledge the depth-cut
frontier path.

### R2-P1-1 / R4-P1-5 — silent KNOB fallback
- TTT `_apply_move_ordering` now raises `ValueError` on unknown
  `MOVE_ORDERING` values (was: silently returned unsorted).
- TTT `_evaluate` now raises `ValueError` on unknown `EVALUATOR`
  values (was: silently used `lines`).
- Nim `successors_of` now raises `ValueError` on unknown
  `MOVE_ORDERING` values (was: silently kept insertion order).

### R2-P1-5 — EVALUATOR dead at default
Updated the EVALUATOR KNOB block to explicitly call out that the KNOB
has NO effect unless `MAX_DEPTH` is finite.

### R2-P1-10 — RANDOM_SEED "any future randomised tie-breaker" lie
Removed the "and any future randomised tie-breaker" phrase from the
RANDOM_SEED KNOB block. Replaced with "Only consulted when
`MOVE_ORDERING == 'random'`".

### R4-P1-2 — Variant 1 phrasing "Increase from 3 to 7"
Rewrote variant 1 prose to "Set the minimax tree-depth limit to 3,
then to 7." Removed the implication of a 3-baseline that didn't exist.

### R4-P1-3 — Variant 1 ordering pinning
Added explicit "pin `MOVE_ORDERING = 'natural'`" instruction at step
2 so the variant 1 measurement does not get conflated with the default
`center-first` ordering used elsewhere.

### R4-P1-4 — Nim main() opener
Refactored `alpha_beta_solution.main()` to branch on
`COMPUTER_PLAYS_MAX`: when False the COMPUTER (= MIN) now correctly
opens (slide-12 step 3). Updated the docstring to mention the
conditional. Also added a one-line KNOB banner before the first move.

---

## P2 fixes applied (selected)

- **R1-P2-3** Added module-level `_INFINITY` in both files (no longer
  redefined inside every decision function).
- **R2-P0-1 follow-on** Reframed the Variant 4 walkthrough to use
  `root_utility` explicitly, matching the new module-level API.

P2 polish items NOT addressed in this round (deferred to a final-polish
pass): docstring citations (R3-P1-2, R3-P1-3, R3-P1-4, R3-P1-5,
R3-P2-1..6), R&N argmax citation, `_to_move` example, KNOB banner
formatting consistency. None of these affect correctness or variant
solvability.

---

## Verification

Verified end-to-end at `c:\Users\samgl\Documents\GitHub\ExamPrep\AI`:

```
py -3.12 handout\handout\tictactoe_template_solution.py
```
→ self-play completes, ends in a draw, exit code 0.

Variant 1 sweep (with `MOVE_ORDERING = "natural"`):
| MAX_DEPTH | Pruning | Move | Nodes  |
|-----------|---------|------|--------|
| 3         | on      | 4    | 272    |
| 3         | off     | 4    | 585    |
| 7         | on      | 0    | 9 688  |
| 7         | off     | 0    | 221 625|

Variant 2 sweep at `MAX_DEPTH = 3`:
- `EVALUATOR = "lines"` → draw, final board `OOX XXO OXX`.
- `EVALUATOR = "center-weighted"` → X wins on ply 5.

Variant 3 sweep (full depth):
| MOVE_ORDERING  | First move | Nodes  |
|----------------|------------|--------|
| natural        | 0          | 30 709 |
| center-first   | 4          | 15 705 |
| corners-first  | 0          | 20 666 |

Variant 4 sweep:
- `root_utility([7])`  → +1 (COMPUTER MAX wins)
- `root_utility([15])` → -1 (USER MIN wins)
- `root_utility([20])` → +1 (COMPUTER MAX wins)
- With `COMPUTER_PLAYS_MAX = False`: `root_utility([15])` → +1
  (sign flipped — slide-12 step 3 confirmed).

STARTING_BOARD validation also exercised — wrong length, non-Symbols
entries, and illegal X/O counts all raise informative `ValueError`.

---

## Files revised (paths)

1. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\alpha_beta_solution.py`
2. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\tictactoe_template_solution.py`
3. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab5-AlphaBeta\variants.md`

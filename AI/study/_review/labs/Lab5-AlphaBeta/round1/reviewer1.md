# Lab 5 — Alpha-Beta — Round 1 — Reviewer #1 (Correctness)

**Reviewer role:** Lab Reviewer #1 — Correctness
**Files reviewed:**
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\tictactoe_template_solution.py` (entry point)
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\alpha_beta_solution.py` (Nim sister module, imported)
**Handout:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\handout\handout\Lab 5.pdf`
**Run command:** `py -3.12 handout\handout\tictactoe_template_solution.py`
**Run result:** exit code 0, no exceptions, self-play game completed in 9 plies → draw (expected, Tic-Tac-Toe is solved).

---

## Report to PM

**Assignment recap:** Round-1 correctness review of the Lab 5 Alpha-Beta submission. Two files: a Tic-Tac-Toe entry point (slides 4–8) and a Nim sister module (slides 9–12) that is imported but never actually exercised by the entry point.

**Status:** Pass with concerns

The three slide-8 TODOs (`is_terminal`, `utility_of`, `successors_of`) are correctly implemented. Alpha-beta produces the same move as plain minimax but evaluates ~35× fewer nodes (15 705 vs 549 945 from the empty board). The Nim Lab still produces the slide-11 result (MAX wins from `[7]` against MIN). However, there is enough dishonest scaffolding, dead imports, type-annotation drift, and one undocumented validation gap that I cannot give this a clean pass.

---

### P0 findings (blockers)

None. The handout's required functions are correct, the entry point runs to completion, and the strategic decisions verified against worked-out positions are all optimal. There is no security or data-loss surface in a self-play Tic-Tac-Toe script.

---

### P1 findings (important)

1. **Dead imports leak into the public namespace of the entry-point module.**
   `tictactoe_template_solution.py:130-134` imports three things from `alpha_beta_solution`:
   ```python
   from alpha_beta_solution import (
       nodes_evaluated as _nim_nodes_evaluated,  # noqa: F401  (re-exposed below)
       reset_node_counter,
   )
   import alpha_beta_solution as _ab  # for read/write access to the live counter
   ```
   Grep proves none of these are used:
   - `reset_node_counter()` — 0 call sites (the file uses its own `_reset_local_counter()` for the local counter, 3 call sites).
   - `_nim_nodes_evaluated` — 1 textual occurrence (only in the import itself).
   - `_ab.` — 0 attribute accesses.

   The `# noqa: F401` and the comment "re-exposed below" are misleading — nothing is re-exposed. The "for read/write access to the live counter" comment for `_ab` is also a lie: the live counter is never touched. **Fix:** delete all three imports, or actually use `reset_node_counter()` instead of the parallel local `_reset_local_counter()` helper.

2. **Two parallel, unsynchronised node counters.**
   `alpha_beta_solution.nodes_evaluated` (the Nim counter) and `tictactoe_template_solution.nodes_evaluated` (the Tic-Tac-Toe counter) are two completely independent module-level integers. The docstring on the local counter (line 252–254) explains *why* they are separate, but the import block at line 130–134 strongly implies the entry-point module reuses the Nim counter. A future maintainer reading the imports would reasonably assume the engine in `alpha_beta_solution` is what runs Tic-Tac-Toe — but in fact `minmax_decision` is fully redefined locally (lines 267–326) and operates on its **own** counter. The comment at line 127–129 ("Reuse the engine + KNOBs from the sister Nim module so that any change made there flows through here automatically") is therefore **false** — the engine is duplicated, and KNOB changes in `alpha_beta_solution.py` do **not** flow into Tic-Tac-Toe. **Fix:** either truly reuse one engine, or update the comments to admit there are two.

3. **`STARTING_BOARD` validation gap vs. its own docstring.**
   `tictactoe_template_solution.py:224-227` documents:
   > "must contain exactly 9 cells; X must be played between 0 and 1 more times than O"

   `_starting_board()` at line 544–550 only checks length. I confirmed empirically:
   ```python
   STARTING_BOARD = [X, X, X, I, I, I, I, I, I]  # 3 X, 0 O → accepted, not validated
   ```
   The board is then passed straight into `minmax_decision`, where `_to_move` will lie about whose turn it is (parity rule says O, but the position is actually unreachable from a legal game). The docstring promises validation that the code does not perform. **Fix:** add the actual check, or weaken the docstring.

4. **Return-type annotation lies about types.**
   `max_value` and `min_value` (lines 280 and 300) are annotated `-> int`, but they can legitimately return `float('-inf')` / `float('inf')` (the `expected_value` / `v` initialisers) **and** the `_evaluate` heuristic. `_evaluate` is hinted `-> int` and currently does return int — but the function flow leaves no guarantee. With `MAX_DEPTH` set, the recursion's mathematical range is `[-inf, +inf]`, not `int`. Strictly this is a type-hint bug. **Fix:** change to `-> float` (or `int | float`), which is what the bounds parameters are already annotated as.

5. **`is_terminal` is also `True` at draws — verified — but the docstring says "win or tie (board full)".**
   The wording matches slide 6 verbatim, so this is not really a bug. However note the asymmetric semantics: at a *draw* `utility_of` returns 0, the same value it returns on a non-terminal state. The recursion only ever queries `utility_of` at known-terminal states (via the `is_terminal` guard), so the ambiguity never bites. But the comment at line 358–361 ("This branch is only hit at draws") is technically wrong when `MAX_DEPTH` is set: with `MAX_DEPTH=None` the only non-terminal path to `utility_of` doesn't exist; with `MAX_DEPTH` finite, the frontier path calls `_evaluate`, not `utility_of`. The comment is therefore right for the default but wrong in spirit. Minor. **Fix:** tighten the comment.

---

### P2 findings (polish)

1. **`Self` import is technically unused at runtime** (only referenced in the classmethod return annotation). Modern Python 3.12 handles this fine via PEP 695 lazy evaluation, but a linter will flag it depending on configuration. Cosmetic.

2. **The `_ab` import comment is wrong** ("for read/write access to the live counter"). See P1 #1 above.

3. **`COUNT_NODES = True` always (top-level default) leaks the alpha-beta node count into the Verifier's stdout** even on a clean run. The Verifier only checks exit code, so this is fine, but if any downstream test ever does an output diff, the deterministic-but-noisy "evaluated N states" lines will trip it. Consider setting `COUNT_NODES = False` as the production default and toggling for variant runs.

4. **`_evaluate` returns values outside `[-1, +1]`** (e.g. `_evaluate([X, X, X, ...])` returns `8`). Harmless because it's only called at the non-terminal cut-off frontier, but a future student reading the code and comparing with `utility_of` (which is strictly ±1, 0) may be confused. Add a one-line comment that the heuristic deliberately uses a coarser scale.

5. **Move ordering for "natural" is the only ordering that `successors_of` produces if `_apply_move_ordering` falls through.** That is fine, but the fall-through at line 462–463 silently masks typos in the `MOVE_ORDERING` knob (`"centre-first"` vs `"center-first"`). Consider raising `ValueError` for unknown values during a variant sweep so we don't accidentally measure the wrong ordering.

6. **`alpha_beta_solution.py:172-225` (`alpha_beta_decision`) returns a `Piles`, not a move tuple.** The docstring is clear about this and the surrounding game loop uses it correctly, but the function name suggests a "decision" whereas the return value is a "next state". This is a handout artifact, not the student's fault. Worth noting in the conventions doc.

7. **`split_pile_options` typed `-> list[Piles]` but `Piles = list[int]`, so the actual type is `list[list[int]]`.** Correct, just a little awkward. The example in the docstring (line 307) reads `[[1,6], [2,5], [3,4]]`, which I verified matches reality.

8. **`argmax` is a 3-line wrapper around `max(iterable, key=func)`** (line 332-334). Kept "for fidelity to the handout template" implicitly, but the comment doesn't say so. Trim or comment.

---

### QA Checklist (§7) status

This is a one-file academic lab. The standard "DOCUMENT.md, conventions.md, file-map" checklist from the global PM workflow does not really apply. I check the spirit of §7 against the lab handout instead.

| Item | Status | Note |
|---|---|---|
| Bug-free against scope (slides 4–8 TODOs) | **Pass** | `is_terminal`, `utility_of`, `successors_of` all verified by hand-rolled probes (winner detection, draw detection, parity-based side-to-move, three-in-a-row test). |
| Alpha-beta matches plain minimax (same move) | **Pass** | Same first move (cell 4), nodes 15 705 vs 549 945 — pruning is correct, not changing the strategy. |
| Slide-11 outcome (Nim from `[7]`: MAX wins from any MIN reply) | **Pass** | Computer picks `[2,4,1]` after `[6,1]`, `[1,4,2]` after `[5,2]`, `[1,3,3]` after `[4,3]` — all multiset-equal to the slide's bold arrows. |
| Move-ordering knob actually affects pruning ratio | **Pass** | `center-first`=15 705, `natural`=30 709, `corners-first`=20 666, `random` (seed 42)=26 506 — `center-first` is the clear winner (textbook). |
| Depth-limit + evaluator paths work | **Pass** | Three evaluators (`lines`, `center-weighted`, `rows-cols-diags`) all return cell 4 at depth=2 from the empty board, 81 nodes each. |
| `USE_ALPHA_BETA_PRUNING=False` recovers plain minimax | **Pass** | Same move, much higher node count. |
| Conventions adhered to | **Partial** | Naming and structure are fine. Dead imports (P1 #1) and false comments (P1 #2) violate the "production-ready, no placeholders" convention. |
| Tests | **N/A** | This lab does not ship a test suite. Manual probes above stand in. |
| `DOCUMENT.md` per directory | **N/A** | Single handout directory, no project-level docs expected. |

---

### Acceptance criteria (§1) status

Slide-8 explicit asks:
- ✅ Implement `is_terminal(state)` — present, correct.
- ✅ Implement `utility_of(state)` — present, correct (returns +1 / -1 / 0 per slide 6).
- ✅ Implement `successors_of(state)` — present, correct (returns `(move, new_state)` pairs).
- ✅ Run the resulting game — `py -3.12 tictactoe_template_solution.py` runs to completion without exception, exit code 0.

Slide-12 (Homework Nim) implicit asks (not exercised by the entry point):
- ✅ Nim rewritten using `alpha_beta_decision` — present in `alpha_beta_solution.py`.
- ⚠️ Tested with starting piles 15 and 20 — **the code supports it via `START_PILE`**, but no transcript or scripted verification accompanies the submission. Reviewer #2 may want to actually run those.
- ✅ Sign-flip via `COMPUTER_PLAYS_MAX = False` is implemented for slide-12 step 3.

---

### DOCUMENT.md audit

N/A — single-directory academic lab.

---

### Out-of-scope observations

1. The two files are entangled by an import that the entry point does not actually need. Untangling is trivial and would shrink the surface area. Worth a follow-up clean-up task.
2. The `alpha_beta_solution.main()` REPL still calls `input()` — fine for the Nim REPL, but if anyone ever sets `tictactoe_template_solution.DEMO_MODE = "interactive"` and the Verifier picks it up, the verifier will hang. Currently the default is `"self-play"`, so this is latent, not active.
3. The `STARTING_BOARD` typing annotation `list | None` should really be `list[Symbols] | None` for clarity (line 228). Cosmetic.
4. Self-play between two perfect minimax agents always draws — the code's "happy path" never exercises the win branch of `utility_of` end-to-end. Worth a synthetic test that injects a one-move-from-win board and asserts that `minmax_decision` picks the winning cell. (My hand-probe `[X,X,I,O,O,I,I,I,I]` → 2 confirms this works, but it's not in the script.)

---

### Concerns / risks

- The "shared engine" story in the file header is fiction. Two separate engines exist with two separate counters. A student who tweaks `alpha_beta_solution.MOVE_ORDERING` expecting Tic-Tac-Toe behaviour to change will be confused. This is a documentation lie, not a runtime bug — but it's exactly the kind of cleverness that bites during an exam variant sweep.
- The `# noqa: F401` masks a real dead import. Removing it would surface the dead code immediately. The fact that the author needed to silence the linter is itself a smell.
- All "KNOB" documentation is detailed and correct as far as I could verify, but the sheer surface area (8 KNOBs in tic-tac-toe, 5 in nim) is well beyond what slide 8 asks for. This is over-engineered for the handout. If the grader is checking against the slide-8 spec strictly, the extra KNOB infrastructure is harmless. If the grader objects to "scope creep beyond the lab", points may be lost.

---

### What PM should do next

1. **Send back for cleanup of P1 items** before App Tester runs:
   - Remove the three dead imports at `tictactoe_template_solution.py:130-134` (or wire them up properly).
   - Either implement the X/O-count validation in `_starting_board()` or weaken the docstring.
   - Fix the `-> int` return annotations on `max_value` / `min_value` to `-> float`.
   - Correct the "Reuse the engine + KNOBs" comment at line 127–129 — admit the two engines are duplicated, or actually share one.
2. **Then re-run QA** (round 2) to confirm fixes did not regress the slide-8 functionality.
3. **Then dispatch App Tester** to manually verify the slide-8 interactive game loop (set `DEMO_MODE = "interactive"`, play one game as O against the computer X) and to run `alpha_beta_solution.py` directly with `START_PILE` in `{7, 15, 20}`.
4. **Then Code Reviewer** on the diff, focused on whether the KNOB surface should be trimmed.

**DOCUMENT.md updated:** N/A for QA.

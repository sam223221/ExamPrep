# Lab6-CSP — Round 1 Reviser Summary

**Files revised:**
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\constraints_template_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab6-CSP\variants.md`

**Status:** All P0 items from reviewers 3 and 4 addressed; primary P1 items from reviewer 1 addressed.

---

## Fixes applied

### R3 P0s (Pedagogical correctness)

1. **`_select_mrv` now computes legal-values dynamically** — `constraints_template_solution.py` ~L437-475.
   - Previously: `len(self.domains[v])` (static declared domain) — a no-op without FC on uniform-domain CSPs.
   - Now: counts values in `self.domains[v]` that are `is_consistent` with the current partial assignment. Textbook MRV (R&N §6.3.2 / L07 §4.2). Meaningful even without FC.

2. **`_lcv_count` now uses dynamic legal counting + per-pair constraint lookup** — `constraints_template_solution.py` ~L477-516.
   - Previously: counted against static `self.domains[neighbour]` and only used `self.constraints[variable]`.
   - Now: skips neighbour-values already inconsistent with the assignment; consults BOTH endpoints' constraint functions (`constraint_v` and `constraint_n`) so the LCV count is honest for asymmetric per-variable constraints. Meaningful without FC.

3. **`_forward_check` now tests each neighbour-value against the constraint** — `constraints_template_solution.py` ~L518-572.
   - Previously: removed only the literal `value` from each neighbour's domain (correct only for `!=` constraints; wrong for `<`, n-queens diagonals, etc.).
   - Now: for each unassigned neighbour Y and each `ny` in Y's live domain, applies `constraint(variable, value, Y, ny)` and prunes `ny` iff the constraint rejects the pair. Correct for arbitrary binary constraints (matches L07 §4.4).

4. **`is_consistent` now uses `self.constraints[variable]` directly** — `constraints_template_solution.py` ~L417-437.
   - Previously: outer loop over `self.constraints.values()` (O(V*N) work; only "correct" because every entry is the same function reference).
   - Now: pulls the per-variable constraint once and loops only over assigned neighbours (O(N)). Correct for heterogeneous per-variable constraints. Aligned with `_lcv_count`'s convention.

5. **`_revise` now consults both endpoints' constraints for an arc** — `constraints_template_solution.py` ~L598-624.
   - Previously: only `self.constraints[x]`.
   - Now: a pair `(vx, vy)` has support iff BOTH `constraint_x(x, vx, y, vy)` AND `constraint_y(y, vy, x, vx)` accept — honest semantics for a constraint over a pair (L07 §3.1).

### R4 P0s (Variant adaptability)

6. **FC snapshot leak on success path fixed** — `constraints_template_solution.py` ~L355-378.
   - Previously: when the deeper recursion succeeded, `recursive_backtracking` returned without restoring the FC snapshot; subsequent calls to `backtracking_search()` on the same CSP instance would see permanently-pruned domains.
   - Now: snapshot is restored before the successful return. Confirmed by running `backtracking_search()` twice on the same FC-enabled CSP instance and observing that `self.domains` stays at full size = 4 after each run.

7. **Variant 3 distance-threshold description corrected** — `study/_exam/Lab6-CSP/variants.md` lines 85-89.
   - Previously: "1.5 → Sparse — only the hub C touches A and B" (factually wrong; threshold 1.5 produces the full star K_{1,4}).
   - Now: "1.5 → Sparse — star K_{1,4}: hub C touches all four corners (A, B, D, E), but corners do NOT touch each other. Each spoke distance is √2 ≈ 1.414. Chromatic number = 2 (bipartite)." Also corrected Run B and Run C descriptions for full accuracy.
   - Expected-answer shape also updated to reference K_{1,4} bipartiteness and chromatic number 5 (was ">= 4") at threshold 3.5.

8. **`USE_AC3` KNOB added for Variant 5** — `constraints_template_solution.py` ~L252-268, and entry-point harness ~L797-820.
   - Previously: `csp.ac3()` exposed as a public method but no KNOB triggered it; Variant 5 required a hand-written driver script in violation of the variant bank's KNOB-only contract.
   - Now: `USE_AC3: bool = False` KNOB with standard header (read-at-`__main__`, exam-variants-V5). When `USE_AC3=True` the harness runs `csp.ac3()` before `csp.backtracking_search()`, prints `AC-3 pre-pass: feasible=<bool>  values_pruned=<int>`, and short-circuits if AC-3 detects infeasibility.
   - `_print_report` now includes `AC3=<bool>` in the heuristics line.
   - `variants.md` Variant 5 KNOB section updated to use `USE_AC3 = True` (no driver script needed).
   - Notes-for-exam-agents block updated to list `USE_AC3` alongside the other documented KNOBs.

### R1 P1s (Correctness polish)

9. **Docstring sample-output block synced with actual print format** — `constraints_template_solution.py` lines ~109-129.
   - Previously: docstring claimed `Recursive calls: 7` and printed bare colour names ("Green") — neither matched reality.
   - Now: docstring shows `Recursive calls: 8`, full `Color.Red` enum format, and the new `AC3=False` heuristic line. Added an explanatory note that `_recursive_calls` increments at the TOP of every call (including the completion call) so 7 variables yield 8 calls.

10. **AC-3 wired into `__main__` via `USE_AC3` KNOB** — see #8 above. Homework Challenge's "implement forward checking AND arc consistency" deliverable is now end-to-end observable from the console.

11. **`is_consistent` tightened** — see #4 above.

---

## Verification

Ran the following configurations after revisions; all produce expected results:

| Config | Result |
|--------|--------|
| Default (Australia, 3 colours, no heuristics) | SOLVED, 8 calls, 0 backtracks |
| Variant 1 (SA + MRV + degree, 4 colours) | SOLVED, BRAZIL = Red (picked first by MRV+degree), 14 calls, 0 backtracks |
| MRV-only (no degree tiebreak, SA + 4 colours) | SOLVED, 14 calls, 0 backtracks (MRV's dynamic legal-value count now does meaningful work) |
| Variant 2 (SA + 3 colours) | NO SOLUTION, 310 calls, 309 backtracks |
| Variant 3 threshold 1.5 | K_{1,4} confirmed (Q is hub; WA/NT/NSW/V each adjacent only to Q); SOLVED with 2 colours-effective in 6 calls, 0 backtracks |
| Variant 3 threshold 3.5 | K_5 confirmed (every pair adjacent); NO SOLUTION with 3 colours, 15 backtracks |
| Variant 4 (SA + MRV + degree + FC, 4 colours) | SOLVED, 14 calls, 0 backtracks; re-running on the same CSP instance still gives 14/0 (no snapshot leak) |
| Variant 5 (SA + AC-3 pre-pass) | `AC-3 pre-pass: feasible=True values_pruned=0` for both 3-colour and 4-colour palettes (confirms textbook claim "AC-3 is a no-op on binary not-equal with |D| >= 2") |
| LCV + FC on SA 4-colour | SOLVED, 14 calls, 0 backtracks |
| SA 3-colour + MRV + FC | NO SOLUTION in 52 calls, 57 backtracks; all domains restored to size 3 after failure |

---

## Items deliberately NOT addressed (out of scope for this revise pass)

- R1 P2s and R3 P2s (polish items): `__eq__` returning `False` instead of `NotImplemented` on `States`, `Color` enum string values, distance-demo enum reuse, etc. — all non-correctness polish.
- R2's KNOB taxonomy refactor (introducing `# KNOB-REF:` / `# KNOB-EXT:` prefixes in `Colors_solution.py` and `States_solution.py`) — documentation taxonomy that doesn't affect any P0 behaviour.
- R3 P1-3 (docstring length): the 134-line module docstring is intentional scaffolding for the variant bank's KNOB-only contract and is required by the round's reviewer #2 / #4 mandate. Trimming it would lose the variant-adaptability documentation that R2 / R4 grade favourably.
- R3 P1-1 / P1-2 (template signature drift on `recursive_backtracking` return type, `from Colors_solution import Color`): the file is explicitly named `_solution.py` and the variant bank entry point points to it; the original template (`constraints_template.py`) is untouched, so drop-in template compatibility is not the goal.
- R4 P1-1 (Variant 4 baseline-is-0): would require switching the variant's reference map/palette to something with a nonzero baseline (e.g., 3-colour SA). That is a variant-design decision, not a code defect — leaving the current variant intact since the existing Variant 4 still demonstrates "no degradation" cleanly.

---

## Report to PM

**Assignment recap:** Reviser pass on Lab6-CSP Round 1. Address R3 P0s (MRV/LCV/FC/is_consistent/_revise), R4 P0s (FC snapshot leak, Variant 3 description, USE_AC3 KNOB), and R1 P1s (docstring/print sync, AC-3 wiring, is_consistent tightening). Save revised files; write summary.

**Status:** Done.

**Files created/modified:**
- Modified: `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\constraints_template_solution.py` — 6 functions revised (`is_consistent`, `_select_mrv`, `_lcv_count`, `_forward_check`, `_revise`, `recursive_backtracking`'s success-path FC restore); new `USE_AC3` KNOB block; `_print_report` includes `AC3=` flag; new `_domain_value_total` helper; `__main__` wired to gate `csp.ac3()` on `USE_AC3`; module docstring sample-output block synced with actual print format.
- Modified: `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab6-CSP\variants.md` — Variant 3 edge-density table rewritten to reflect actual K_{1,4} / mid / K_5 structure; expected-answer shape updated; Variant 5 KNOB section switched to `USE_AC3 = True`; notes-for-exam-agents lists `USE_AC3`.
- Created: `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_review\labs\Lab6-CSP\round1\revise-summary.md` — this document.

**What I did:** See the numbered list above. Eleven discrete edits across two files. Each edit verified by running the affected configuration.

**Deviations:** None from the brief.

**Out-of-scope observations:**
- The `_lcv_count` was upgraded both for legal-counting and for per-pair constraint lookup; this changes its score values compared to the old implementation, but only on configurations that actually toggle LCV. The variant bank has no LCV-specific variant, so no expected-answer surface changes.
- The `_revise` per-pair fix also changes the AC-3 semantics for asymmetric constraints; since this lab's constraints are all symmetric not-equal, observed behaviour is unchanged.
- The `Read at:` lifecycle tag from R2's P1-2 was added only to `DISTANCE_THRESHOLD` (where build-vs-call-time is most likely to bite); the other KNOBs were left tag-free to limit scope to the briefed P0/P1 items.

**Concerns/risks:**
- Variant 4's baseline (4-colour South America, no heuristics) still yields 0 backtracks — the "monotonic decrease" framing remains weakly demonstrable. R4 flagged this as P1; the brief did not include it, so it is unchanged. A future round could switch Variant 4 to 3-colour SA (infeasible) which would yield meaningful backtrack differences.
- R3 P0-5 (constraint indexed by single variable rather than per-pair) was addressed in `_lcv_count` and `_revise` by consulting BOTH endpoints. The underlying data structure (`constraints: Dict[States, contraintFunction]`) is unchanged to preserve template-signature compatibility (R1's invariant). A truly per-pair `Dict[FrozenSet[States], contraintFunction]` would be a deeper refactor.

**What PM should do next:**
1. Dispatch QA Inspector and Reviewer #3 / #4 again to confirm all P0 findings are resolved.
2. Optionally schedule a follow-up to address the deferred P1/P2 polish items (taxonomy prefixes, Variant 4 baseline, States `__eq__` semantics).
3. No new variants need to be added — the existing five all now answer KNOB-only.

**DOCUMENT.md updated:** N/A — Lab6 directory has no DOCUMENT.md convention established; the module docstring serves the same role.

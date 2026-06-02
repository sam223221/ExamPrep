# Lab6-CSP — Reviewer #1 (Correctness) — Round 1

## Report to PM

**Assignment recap:** Lab6-CSP Round 1 correctness review of:
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\constraints_template_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\Colors_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\States_solution.py`

Handout: `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\Lab 6.pdf` (Exercise 1 = `recursive_backtracking`; Exercise 2 = South America with 4 colours; Homework Challenge = forward checking + arc consistency).

Verification commands run:
- `py -3.12 lab6\constraints_template_solution.py` — default (Australia, 3 colours).
- Temporary copies to exercise Exercise 2 (South America, 4 colours), South America with 3 colours + MRV + FC (should be NO SOLUTION), and the `distance_demo` map.

**Status:** Pass with concerns

The exercise as set in the handout (Exercise 1 = recursive backtracking; Exercise 2 = South America with 4 colours; Homework = forward checking + AC-3) is correctly implemented. The default run produces a valid 3-colouring of Australia in 8 recursive calls with 0 backtracks. Exercise 2 (South America, 4 colours) produces a valid 4-colouring in 14 calls, 0 backtracks. South America with 3 colours + MRV + FC correctly reports `NO SOLUTION` after 57 backtracks. AC-3 (`ac3`) is implemented but is not wired into the default run — the docstring says this is intentional, but the Homework Challenge wording ("Implement forward checking **and** arc consistency for the previous exercise") can be read as wanting AC-3 as a *pre-pass before* backtracking on the South-America map. The current code lets a caller compose them but the entry-point harness does not.

---

### P0 findings

None. The solver returns a valid assignment for every map/palette configuration tried, and correctly reports infeasibility when the chromatic number exceeds the palette.

---

### P1 findings

1. **`is_consistent` iterates over every constraint instead of using `self.constraints[variable]`** — `constraints_template_solution.py:389`.

   ```python
   for constraint in self.constraints.values():
       for neighbour in self.neighbours[variable]:
   ```

   Because `_make_not_equal_constraints` stores the **same** function object under every variable key, the inner check is identical on every outer iteration. This is wasteful (each consistency check runs `len(variables)` times more work than needed: O(V*N) instead of O(N)) and, more importantly, it is **incorrect for heterogeneous CSPs** where different variables would carry different constraints. The original template apparently shipped this same pattern, so it is preserved for compatibility — but a single-line fix (`constraint = self.constraints[variable]` then loop only over neighbours) would be both faster and semantically correct. Compare with `_lcv_count` at line 440, which uses the singular form `self.constraints[variable]` — the inconsistency between the two helpers is itself a smell.

   *Suggested fix:* replace lines 389–395 with
   ```python
   constraint = self.constraints[variable]
   for neighbour in self.neighbours[variable]:
       if neighbour not in assignment:
           continue
       if not constraint(variable, value, neighbour, assignment[neighbour]):
           return False
   ```

2. **AC-3 is implemented but never invoked by the entry-point harness** — `constraints_template_solution.py:485` and `__main__` block at `:729`.

   The Homework Challenge explicitly asks for forward checking **and** arc consistency. Forward checking is gated behind `USE_FORWARD_CHECK` and wired through `recursive_backtracking`. AC-3 (`ac3`) exists but has no corresponding `USE_AC3` knob and is not called before `backtracking_search()`. A student grader looking for "AC-3 is used" will not see it without manually calling `csp.ac3()` first. The docstring at `:486` explicitly says "the entry-point script does NOT call this by default", but the *handout* arguably requires it.

   *Suggested fix:* add a `USE_AC3` knob, run `csp.ac3()` before `csp.backtracking_search()` in `__main__` when the knob is on, and warn if `ac3()` returns False.

3. **Docstring example output is out of date with the actual print format** — `constraints_template_solution.py:116-128`.

   The docstring promises:
   ```
   Recursive calls:     7
   ...
   States.NT:    Green
   States.Q:     Red
   ```

   But the program actually prints:
   ```
   Recursive calls:     8
   States.WA: Color.Red
   States.NT: Color.Blue
   ...
   ```

   - Recursive-call count differs by one (the implementation increments `_recursive_calls` at the *top* of every call, including the call that returns by completion — so for 7 variables you get 8 calls, not 7). The example in the docstring is wrong.
   - The example uses bare colour names ("Green") but the actual code prints `Color.Red` (enum `__str__`). The print format string at line 726 is `"{}: {}".format(area, color)` which yields the enum's `__str__`. To match the documented format the print should be `f"{area}: {color.name}"` (or `color.value`).

   This is "P1" because a TA who runs the program and diffs against the lab's expected output will see a different format than the docstring advertises. Pick one — fix the docstring or fix the print.

4. **`_make_not_equal_constraints` returns a dict keyed by variable, but the constraint function is identical for every key — wasted memory and confusing semantics** — `constraints_template_solution.py:535-556`.

   This is a structural carry-over from the template, but combined with finding #1 it means we keep a dict of N copies of the same function pointer. It is harmless, but worth a comment explaining *why* (template contract) so a future maintainer doesn't refactor it in a way that breaks compatibility.

5. **`States.__eq__` returns False instead of `NotImplemented` for non-States comparisons** — `States_solution.py:93-96`.

   ```python
   def __eq__(self, other):
       if type(other) != type(self):
           return False
       return self.value == other.value
   ```

   This means `States.WA == None` returns `False` (fine), but `None == States.WA` *also* returns `False` (because Python's default falls back). The convention is `return NotImplemented` so Python can try the other side's `__eq__`. Not a defect for this lab, but it's a minor "I'd flag this in a code review" item.

6. **`_forward_check` may leave a partial prune un-restored on the "early-exit" path** — `constraints_template_solution.py:445-475`.

   The function returns `(snapshot, False)` as soon as one neighbour's domain wipes out. The caller at line 333 then calls `_restore_domains(fc_snapshot)`. This is correct because the snapshot stores everything that was pruned up to and including the wipe. Verified by tracing — the wiped neighbour's *pre-prune* domain is captured before the prune at line 466, so the restore brings it back to the original. **Not a bug**, but the surrounding comment "We still return the snapshot so the caller can restore *partial* prunes" doesn't make it obvious that the wiped variable itself is in the snapshot. A clarifying comment would help.

---

### P2 findings

1. **`is_consistent`'s short-circuit `if not assignment: return True`** — `:386-387`. Removing this would not change behaviour (the loop body is a no-op on an empty `assignment`); it's a micro-optimisation that adds branching for unclear benefit.

2. **`backtracking_search` returns `result if result else None`** — `:278`. `result` is either a non-empty dict or `None`; the `if result else None` is a no-op for the success path (a non-empty dict is truthy). But if `result` happened to be the empty dict `{}` (impossible here because is_complete would only return True with `len(variables) == 0`), this would convert it to `None`. Edge case only.

3. **Counter naming `_recursive_calls` vs `_backtracks` is fine, but neither is publicly exposed** — `:265-266`. The print uses `csp._recursive_calls` from outside the class, dancing on the name-mangling line. A property would be cleaner.

4. **`Color` enum members use string values (`Red = "Red"`)** rather than `auto()`. Harmless but redundant — the name and value are identical.

5. **`States.__hash__` hashes on `repr(self)`** — `States_solution.py:101`. Works, but `hash(self.value)` would be cheaper and equivalent given the equality definition.

6. **`create_distance_csp` reuses Australia enum members (WA, NT, Q, NSW, V) as abstract IDs** — `:661-667`. Documented in the docstring, but a future reader hitting `States.WA` in a "distance demo" will be momentarily confused. A dedicated set of `REGION_A..REGION_E` enum members would be cleaner, at the cost of more enum entries.

7. **`USE_FORWARD_CHECK` toggles snapshot/restore even when no pruning happens.** Negligible cost.

8. **Docstring at file head says "Tasmania (T) is an island with no neighbours; leaving its list empty exercises the 'isolated variable' case"** — actually the assignment goes correctly (T: Red) but Tasmania is unconstrained and could be any colour. Good — but the docstring's expected output assigns `States.T: Red` while the actual produces the same. Fine.

---

### Acceptance criteria status

- **Exercise 1 (implement `recursive_backtracking` using the pseudocode):** Met. The implementation is a faithful one-to-one translation of the handout pseudocode (Lab 6.pdf slide 2): complete-check → select-unassigned → for each ordered value → consistency check → assign → recurse → undo on failure. Comments quote the pseudocode lines.
- **Exercise 1 (incorporate the other methods present in the file):** Met. `recursive_backtracking` calls `is_complete`, `select_unassigned_variable`, `order_domain_values`, and `is_consistent`.
- **Exercise 2 (South America, 4 colours):** Met. `create_south_america_csp` is defined; `MAP_NAME = "south_america"` + 4-colour palette produces a valid 4-colouring (verified by manual cross-check against the handout map, slide 4 — Brazil borders 10 countries, all 4 colours used, no neighbouring pair shares a colour).
- **Homework Challenge (forward checking):** Met. `USE_FORWARD_CHECK=True` activates `_forward_check` + `_restore_domains`; verified with South America + 3 colours, which correctly returns NO SOLUTION.
- **Homework Challenge (arc consistency):** Partial. `ac3` and `_revise` are implemented and correct (worklist algorithm, re-queues `Z → X` arcs on revision, returns False on domain wipeout). **However**, they are never invoked by the entry-point script. A grader reading the program top-to-bottom will not see AC-3 actually being applied unless they read the docstring and manually call it. See P1 #2.

---

### QA Checklist (handout §1/§2/Homework) status

- **Bug-free against scope:** Pass for Exercise 1, Exercise 2, Forward Checking. Pass-with-concerns for AC-3 (works but not wired in).
- **Implements the pseudocode faithfully:** Pass.
- **South America 4-colour assignment is valid:** Pass (manually verified).
- **South America 3-colour returns NO SOLUTION:** Pass.
- **Australia 3-colour assignment is valid:** Pass (WA=Red, NT=Blue, Q=Red, NSW=Blue, V=Red, SA=Green, T=Red — every adjacent pair differs).
- **All other methods are incorporated by `recursive_backtracking`:** Pass.
- **Function signatures match the template:** Pass (CSP class public surface preserves `backtracking_search`, `recursive_backtracking`, `select_unassigned_variable`, `is_complete`, `order_domain_values`, `is_consistent`).

---

### Out-of-scope observations

- `Colors_solution.py` defines `Purple` even though the handout only requires Red/Green/Blue (Australia) and +Yellow (South America). Harmless — it supports the documented variant 2 ("add a 5th colour"), which is study-aid material, not the handout.
- The `distance_demo` map is a study-aid variant, not in the handout. It works.
- The `ac3()` pre-pass is exposed publicly and works correctly on its own, but no test/demo invokes it. Worth a 3-line demo in `__main__` (or a `USE_AC3` knob) for completeness.
- `__main__` ends with two stale comments mentioning `mapchart.net` — they read like an instructor's note left from the template, not the student's. Harmless.

---

### Concerns / risks

- **`is_consistent`'s outer loop over `self.constraints.values()`** is the most surprising correctness-affecting carry-over from the template. It happens to work because the dictionary always holds the same function pointer, but it would silently misbehave the moment somebody introduces a per-variable constraint. Document the assumption or fix it.
- **The docstring's "OUTPUTS WHEN RUN" block is stale.** A reader comparing it to actual output will see a different recursive-call count and a different print format. Easy to fix; risks confusing whoever grades the lab if they pattern-match on the docstring.
- **AC-3 is dead code from the entry-point's perspective.** A grader who only runs the program will not see AC-3 used. Either wire it in behind a knob or add a comment in `__main__` ("To exercise AC-3, call `csp.ac3()` before `csp.backtracking_search()`").
- No tests / no test harness. The lab is small enough that this is acceptable, but a smoke-test asserting at least one valid colouring on Australia and South America would protect future edits.

---

### What PM should do next

Fix the P1 items in this order (lowest risk first), then re-QA:

1. Fix the docstring stale-output block OR fix the print format (P1 #3) — pick one and align.
2. Wire AC-3 into `__main__` behind a `USE_AC3` knob and document it (P1 #2). This is the only finding that touches handout scope (Homework Challenge).
3. Optionally clean up `is_consistent` to use `self.constraints[variable]` directly (P1 #1) — improves correctness for heterogeneous CSPs and aligns with `_lcv_count`.

After those, the lab is in solid shape to ship.

**DOCUMENT.md updated:** N/A for QA / Reviewer.

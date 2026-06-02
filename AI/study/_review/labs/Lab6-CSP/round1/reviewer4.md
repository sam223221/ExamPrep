# Lab 6 — CSP / Round 1 / Reviewer #4 (Variant Adaptability)

**Reviewer role:** Lab Reviewer #4 — Variant Adaptability.
**Mandate:** Verify that a fresh exam agent, reading ONLY the docstring header of `lab6/constraints_template_solution.py`, the `# KNOB:` blocks, and the public function/class signatures, can answer every variant in `study/_exam/Lab6-CSP/variants.md` correctly. Be harsh — every claim in the variant bank that the code does not actually deliver is an exam-points loss.

**Artifacts reviewed:**
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\constraints_template_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\Colors_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\States_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\Lab 6.pdf`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab6-CSP\variants.md`
- (Reference) `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\constraints_template.py` (the original template the solution must remain signature-compatible with).

---

## VERDICT

**FAIL — must revise before any exam agent can rely on the KNOB-only contract.**

The solution module is exceptionally well-documented and the KNOB block is the cleanest of any lab solution in this study package. But the variant bank makes three load-bearing claims that the code, as written, does not deliver:

1. **MRV is a no-op without forward checking.** The `_select_mrv` helper reads `self.domains[v]` directly, but `self.domains` is only mutated when `USE_FORWARD_CHECK=True` or after `ac3()`. With `USE_MRV=True` and FC off (Variant 1's exact configuration), every unassigned variable has identical domain size for the entire search — MRV degenerates to "first variable in declared order". Variant 1's promise that "the solver always picks the most-constrained region first" is **false** under its own listed KNOB settings; it is the degree tie-break (and the alphabetical-by-enum-value-tiebreak when degrees tie) that does all the work.

2. **Variant 3 Run A's edge description is wrong.** The variant table says "1.5 → Sparse — only the hub C touches A and B". With the coordinates in `create_distance_csp`, threshold 1.5 actually creates the full star K_{1,4} (C touches **all four** corners A, B, D, E — every spoke is √2 ≈ 1.414). The chromatic-number conclusion (=2) still holds, but the structural description is exam-fail-inducing.

3. **`backtracking_search` leaks pruned domains across re-runs when FC is on.** When the deepest recursion finds a solution, the code returns `result` immediately without restoring the forward-checking snapshot. The next call to `backtracking_search()` on the same `CSP` instance therefore starts with permanently-shrunken domains — a silent correctness landmine for any variant driver that loops through configurations (Variant 4 explicitly does this).

There are also two subtler issues — `is_consistent`'s O(|V|) redundant constraint-function iteration, and `Variant 2`'s baseline-backtrack claim for 4-color South America being trivially zero (so the variant comparison is uninteresting) — but those are P1/P2.

The doc-block is so good it earns Variant 2, Variant 4, and Variant 5 a pass with concerns. Variants 1 and 3 fail outright on their stated semantics.

---

## P0 — Blockers (a fresh agent reading only KNOBs will get the wrong answer)

### P0-1. MRV is a no-op without forward checking — Variant 1's central claim is false.

- **Where in code:** `constraints_template_solution.py:402-424` (`_select_mrv`).
- **What the code does:**
  ```python
  def domain_size(v: States) -> int:
      return len(self.domains[v])
  ...
  if USE_DEGREE_TIEBREAK:
      unassigned.sort(key=lambda v: (domain_size(v), -degree(v)))
  else:
      unassigned.sort(key=domain_size)
  ```
- **The problem:** `self.domains[v]` is the *static* declared domain. It is only mutated by `_forward_check` (line 467) or `ac3()` (line 526). Variant 1 explicitly sets `USE_FORWARD_CHECK=False` (it is not in the variant's KNOB table at all, so it stays at its default `False`). Therefore at every recursive call, every unassigned variable has `len(self.domains[v]) == 4` and the sort is a no-op. The `unassigned` list comes from `[v for v in self.variables if v not in assignment]`, which preserves declared order — so without degree tie-break, MRV picks the first declared unassigned variable, which is **COLOMBIA**, not BRAZIL.
- **Where in variants:** `study/_exam/Lab6-CSP/variants.md:25-30, 41-44`:
  > "Use the **MRV** variable-ordering heuristic (and the **degree** tie-breaker) so that the solver always picks the most-constrained region first."
  >
  > "Brazil is the single highest-degree node (10 neighbours), so the degree tie-break forces it first when every domain still has size 4."
- **Why this is P0:** the variant's *answer key* explicitly says "MRV forces BRAZIL first" but the code's MRV does no such thing — only the degree tie-break does. A student/agent who reads the variant prompt and toggles `USE_MRV=True` *without* `USE_DEGREE_TIEBREAK=True` will get COLOMBIA first, get a different (but still valid) coloring, and have no idea why their answer disagrees with the variant key.

  Worse: the textbook definition of MRV ("count *currently legal* values for each unassigned variable" — R&N §6.3.2, L07-CSP §4.2) is *not* what this code implements. The correct standalone MRV would compute, for each unassigned variable, how many values are consistent with the current partial assignment — i.e., walk `self.domains[v]` and for each value check `is_consistent(v, value, assignment)`. The "remaining values" then shrinks dynamically even without FC. This code skips that computation, so MRV-without-FC is identical to plain BFS-order selection. The doc-block at line 184-191 even claims "[MRV] typically reduces the number of backtracks by an order of magnitude on dense constraint graphs" — but with this implementation that only happens when FC is also on, and at that point most of the win is FC's, not MRV's.

- **Suggested fix (pick one):**
  - **(a)** In `_select_mrv`, replace `domain_size(v) = len(self.domains[v])` with a *legal-values count* that walks `self.domains[v]` and applies `is_consistent`. This is the textbook MRV and makes the variant's claim true without requiring FC.
  - **(b)** Document loudly in the `USE_MRV` KNOB block that "MRV in this implementation is meaningful only when forward checking is also enabled; without FC the sort is a no-op and behaviour reduces to declared-order selection (optionally with degree tie-break)". The doc-block must explicitly tell the variant agent to also flip `USE_DEGREE_TIEBREAK=True` for Variant 1's BRAZIL-first answer to materialize.
  - **(c)** Edit Variant 1's KNOB table in `variants.md` to call out that the BRAZIL pick is from the *degree tie-break*, not MRV, and rename the variant to "Backtracking with degree heuristic" to match reality.

### P0-2. Variant 3 Run A edge density description is factually wrong.

- **Where in variants:** `study/_exam/Lab6-CSP/variants.md:85-88`:
  | `DISTANCE_THRESHOLD` | Edge density expected |
  | `1.5` | **Sparse — only the hub C touches A and B** |
- **What the code actually builds** (`constraints_template_solution.py:661-684`):
  ```
  A=(0,0)  B=(2,0)  C=(1,1)  D=(0,2)  E=(2,2)
  ```
  Pairwise Euclidean distances:
  - A-C, B-C, C-D, C-E: all √2 ≈ 1.414 (all ≤ 1.5)
  - A-B, A-D, B-E, D-E: 2.0
  - A-E, B-D: 2√2 ≈ 2.828
- **At threshold 1.5:** the four spoke edges A-C, B-C, C-D, C-E all qualify. The graph is the **full star K_{1,4}** with C as hub, NOT just "C touches A and B". The variant's claim that only A-C and B-C exist is wrong; D-C and E-C are also ≤ 1.5.
- **Why this is P0:** an exam agent reading the variant table sees "C touches A and B only" and writes that as part of its answer. The actual code returns adjacency `{C: [A,B,D,E], A: [C], B: [C], D: [C], E: [C]}`. The chromatic-number = 2 conclusion (the variant's other claim) is still correct (K_{1,4} is bipartite), but the agent's structural description of the graph will be wrong, and any examiner asking "list the edges at threshold 1.5" will mark it down.
- **Suggested fix:** Change `variants.md:88` to "1.5 — Sparse — C touches all four corners (K_{1,4} star); corners do NOT touch each other." Optionally re-pick threshold 1.0 to actually deliver the "only C-A and C-B" graph the variant *intended* (but at 1.0 no edges form, since √2 > 1.0 — so the only way to get the variant's claimed sparse-graph would be to change the coordinates).

### P0-3. `backtracking_search` leaks forward-checking domain prunes across re-runs.

- **Where in code:** `constraints_template_solution.py:272-278, 323-328`:
  ```python
  def backtracking_search(self) -> dict[States, Color] | None:
      self._recursive_calls = 0
      self._backtracks = 0
      result = self.recursive_backtracking({})
      return result if result else None
  ```
  ```python
  if fc_ok:
      result = self.recursive_backtracking(assignment)
      if result is not None:
          return result          # ← returns WITHOUT restoring snapshot
  if fc_snapshot is not None:
      self._restore_domains(fc_snapshot)
  ```
- **The bug:** when the deeper recursion succeeds (`result is not None`), control immediately returns up the stack, skipping the `_restore_domains(fc_snapshot)` block below. Every successful FC prune therefore remains permanently applied to `self.domains` after `backtracking_search` returns.
- **What this breaks:** Variant 4 explicitly asks the agent to run the South-America 4-color problem **three times** and compare backtrack counts — the third run uses `USE_FORWARD_CHECK=True`. A naive driver script that creates **one** CSP and calls `backtracking_search()` three times will, on the second and third call, find `self.domains` already shrunk to the singleton/empty domains of the previous run's solution. The third call will either:
  - (a) succeed in 0 backtracks because the answer is already baked into the domains (artificially "good"), or
  - (b) return NO SOLUTION because some domain became empty during the first run's prune-on-success (artificially "bad").
- **Why this is P0 (not P1):** the variant bank's "Notes for exam agents" (line 170-174 of `variants.md`) actively encourages writing a driver script that imports the module and "run[s] multiple configurations back-to-back without editing the file". This is exactly the workflow that triggers the bug. And nothing in the KNOB doc-block warns the agent that the CSP instance is not re-usable after a successful FC run.
- **Suggested fix (pick one):**
  - **(a)** In `recursive_backtracking`, restore the FC snapshot before returning a successful result too (but **don't** lose the assignment dict). E.g.:
    ```python
    if fc_ok:
        result = self.recursive_backtracking(assignment)
        if result is not None:
            if fc_snapshot is not None:
                self._restore_domains(fc_snapshot)
            return result
    ```
  - **(b)** Snapshot the entire `self.domains` dict at the top of `backtracking_search` and restore it before returning. Cheap (a copy of a 13×4 dict) and bulletproof.
  - **(c)** Document loudly that a `CSP` instance is single-use after a successful FC search and require the variant driver to call `create_csp()` fresh per run.

### P0-4. Variant 5 KNOB table is missing the explicit `csp.ac3()` invocation — but the variant *requires* it.

- **Where in variants:** `study/_exam/Lab6-CSP/variants.md:149-151`:
  > "**KNOBs:** `MAP_NAME = "south_america"`, `ACTIVE_COLORS` as above. Call `csp.ac3()` BEFORE `csp.backtracking_search()` in a tiny test script (signatures only — no need to read AC-3's body)."
- **The problem:** there is **no KNOB** that causes `csp.ac3()` to be called from the main entry point. The variant tells the agent to write a "tiny test script" that imports the CSP, but the contract stated at the top of the variants file (line 6-12) says the agent should only need to read KNOB blocks and signatures.
- **Why this is a P0:** the variants file's own preamble (line 14-15) says "If the variant cannot be answered with KNOBs alone, file a STUCK report". Variant 5 cannot be answered with KNOBs alone — it requires a driver script that imports the module and calls `ac3()` then `backtracking_search()`. The note at line 173-174 grudgingly allows driver scripts but does not address the AC-3-specifically-requires-it case.
- **Suggested fix (pick one):**
  - **(a)** Add a `USE_AC3_PRE_PASS: bool = False` KNOB and a corresponding two-line invocation at the top of `__main__`: `if USE_AC3_PRE_PASS: csp.ac3()`. Then Variant 5 collapses to a one-KNOB flip.
  - **(b)** File a STUCK report per the variants.md contract and have the variant bank revised to include a driver script template.
  - **(c)** Accept the driver-script workflow but call it out explicitly in the doc-block — currently the doc-block doesn't mention `ac3()` at all (the `USE_FORWARD_CHECK` block is the only FC/AC discussion).

---

## P1 — Important issues (variant outputs are misleading or driver-fragile)

### P1-1. Variant 2 "5-colour run: 0 backtracks" claim is true but the 4-colour comparison baseline (which Variant 4 also uses) is trivially zero too.

- **Where in variants:** Variant 2 (`variants.md:50-73`) and Variant 4 (`variants.md:110-132`).
- **Tracing the code by hand for South America with 4 colors and no heuristics**, in declared variable order:
  - COLOMBIA → Red (no constraints yet)
  - VENEZUELA → must ≠ COLOMBIA (Red) → Green
  - GUYANA → must ≠ VENEZUELA (Green) → Red
  - SURINAME → must ≠ GUYANA (Red) → Green
  - FRENCH_GUYANA → must ≠ SURINAME (Green) → Red
  - ECUADOR → must ≠ COLOMBIA (Red) → Green
  - PERU → must ≠ ECUADOR, COLOMBIA → Blue
  - BRAZIL → must ≠ COLOMBIA(R), VENEZUELA(G), GUYANA(R), SURINAME(G), FRENCH_GUYANA(R), PERU(B) → Yellow
  - BOLIVIA → must ≠ PERU(B), BRAZIL(Y) → Red
  - PARAGUAY → must ≠ BOLIVIA(R), BRAZIL(Y) → Green
  - CHILE → must ≠ PERU(B), BOLIVIA(R) → Green
  - ARGENTINA → must ≠ CHILE(G), BOLIVIA(R), PARAGUAY(G), BRAZIL(Y) → Blue
  - URUGUAY → must ≠ BRAZIL(Y), ARGENTINA(B) → Red
- **Result:** 13 assignments, **0 backtracks**, on the very first try.
- **Why this is P1:** Variant 4's "Backtracks decrease monotonically as heuristics are layered on" implicitly assumes the baseline is *nonzero* — otherwise "monotonically decreasing" reduces to "all three runs are 0 → 0 → 0" and there is nothing to compare. The variant prompt as written does not get any pedagogical mileage from this map.

  Similarly Variant 2's headline "with 5 colours: 0 backtracks" is true but uninteresting — the 4-color baseline is also 0. The variant's intended takeaway ("adding a colour reduces backtracks") cannot be demonstrated on this map because there is no backtrack-y baseline to reduce from.
- **Suggested fix:** Variant 4 should switch to a map/palette combo where the baseline backtrack count is nonzero — e.g. **3-color South America** (which is *infeasible*, so the baseline will rack up dozens of backtracks before returning None, and the heuristic versions can at least demonstrate "fail-fast" behavior). Or use the `distance_demo` map at threshold 3.5 with 3 colors (also infeasible). Either way, the current 4-color South America run produces a flat 0-0-0 comparison.

  Variant 2 should either pick a different baseline palette or explicitly call out that "both runs are 0 — the point is that 5 is also 0, not that it's *less* than the 4-color count".

### P1-2. Variant 4 silently requires both `USE_MRV` and `USE_DEGREE_TIEBREAK` to be flipped together but doesn't say so.

- **Where in variants:** `variants.md:116-127`:
  | Baseline | no heuristics |
  | MRV + degree | `USE_MRV=True`, `USE_DEGREE_TIEBREAK=True` |
  | MRV + degree + forward check | also `USE_FORWARD_CHECK=True` |
- **The problem:** Variant 4 row 2 sets both MRV and degree-tiebreak. But as P0-1 establishes, MRV without FC is a no-op, so this row's behavior is **identical** to setting only `USE_DEGREE_TIEBREAK=True`. The variant doesn't tell the agent this — it claims "MRV + degree" as if both heuristics are contributing.
- **Why this is P1:** the agent will report "MRV + degree dropped backtracks from X to Y", but the only thing actually doing the work is degree. If pressed on the exam ("which heuristic did the heavy lifting?"), the agent will say "MRV", when the truthful answer is "degree, and MRV did literally nothing because FC was off".
- **Suggested fix:** Couple to P0-1's fix. If MRV is repaired to be FC-independent (option a), this issue evaporates. Otherwise, rename row 2 to "degree-tiebreak only (MRV is a no-op without FC)".

### P1-3. `is_consistent` runs the constraint function `O(|variables|)` times per neighbor pair (perf, not correctness).

- **Where in code:** `constraints_template_solution.py:389-395`:
  ```python
  for constraint in self.constraints.values():
      for neighbour in self.neighbours[variable]:
          if neighbour not in assignment:
              continue
          neighbour_value = assignment[neighbour]
          if not constraint(variable, value, neighbour, neighbour_value):
              return False
  ```
- **The problem:** `self.constraints.values()` yields the **same not-equal predicate** thirteen times for South America. The outer loop is iterating over irrelevant constraints (the predicate keyed at variable X is checked against variable Y's neighbors). It happens to be correct only because every entry in `self.constraints` is the *same function reference* — so the result of the check is identical for every outer-loop iteration. The early `return False` masks the redundancy.
- **Why this is P1 not P2:** Variant 2's 3-color South America run is supposed to demonstrate "a non-trivial number of backtracks". If a student is asked to *count constraint-function invocations* (a common exam variant), they will count 13× the true number. The docstring at line 381-385 acknowledges "same contract as the template" but does not flag the O(N) blow-up.
- **Suggested fix:** Replace the outer loop with the *single* relevant constraint:
  ```python
  constraint = self.constraints[variable]
  for neighbour in self.neighbours[variable]:
      if neighbour in assignment and not constraint(variable, value, neighbour, assignment[neighbour]):
          return False
  return True
  ```
  This matches the standard R&N is_consistent and brings the operation count to truth. Or document the inefficiency in the doc-block so an examiner asking "how many constraint-function calls were made?" knows what answer the code will produce.

### P1-4. The doc-block claims Variant 1's MRV "picks the most-constrained square first" but the code's MRV without FC does no such thing — and the doc-block is the *only* documentation a fresh agent reads.

- **Where in code:** `constraints_template_solution.py:38-42`:
  > "MRV (Minimum Remaining Values) is the rule 'pick the most-constrained square first' — the cell that has only 2 candidate digits left."
- And `constraints_template_solution.py:184-191`:
  > "What it does: enables Minimum-Remaining-Values variable ordering. With MRV on, ``select_unassigned_variable`` always picks the unassigned variable whose current legal-domain count is smallest."
- **The mismatch:** the doc-block describes textbook MRV ("currently legal-domain count"), but the implementation reads the static declared domain. Without FC, no domain ever changes size, and the heuristic is dead. The doc-block is honest in one place (line 188-189: "typically reduces the number of backtracks by an order of magnitude on dense constraint graphs") but the fresh agent has no way to know that "typically" really means "only when FC is also on".
- **Why this is P1:** the entire premise of the variant-adaptability contract is "KNOBs do what the doc says". Here, `USE_MRV=True` does much less than the doc says.
- **Suggested fix:** Same as P0-1. If the code is fixed to compute legal-values dynamically, the doc is honest. If not, the doc must be amended with a screaming warning: "MRV in this implementation requires `USE_FORWARD_CHECK=True` to be meaningful; otherwise the heuristic is a no-op."

### P1-5. The `_lcv_count` helper depends on `self.constraints[variable]` even though `is_consistent` iterates over all constraints — internal inconsistency.

- **Where in code:** `constraints_template_solution.py:440-443`:
  ```python
  constraint = self.constraints[variable]
  if not constraint(variable, value, neighbour, nv):
      ruled_out += 1
  ```
- **The mismatch:** `_lcv_count` does the right thing (use the constraint keyed at the assigned variable, since binary constraints are stored that way). But `is_consistent` does the wrong thing (P1-3). The two consistency checks therefore disagree on which constraint they're applying, even though it doesn't matter for this map because all constraints are identical references.
- **Why this is P1:** if a future variant introduces *asymmetric* constraints (e.g., region X must have higher color-index than region Y), `_lcv_count` will use the X-keyed constraint while `is_consistent` will use *all* constraints in random dict order. The two will produce different consistency verdicts. Subtle landmine.
- **Suggested fix:** Pick one convention. Either:
  - (a) Always use `self.constraints[variable]` (the assigned variable's constraint) — fix `is_consistent` per P1-3.
  - (b) Always iterate all relevant constraints — fix `_lcv_count` to match. (Worse choice, but at least consistent.)

### P1-6. AC-3 mutates `self.domains` permanently without warning.

- **Where in code:** `constraints_template_solution.py:485-511` (`ac3`).
- **What the docstring says** (line 492-493): "Mutates ``self.domains`` in place."
- **What it does NOT say:** that this mutation is **permanent across subsequent `backtracking_search()` calls**. There is no snapshot/restore. A driver script that does `csp.ac3(); csp.backtracking_search()` on the 3-color South America (Variant 5 Run 1) starts the backtracking with whatever AC-3 left in `self.domains` — which, for this case, is "no change" (AC-3 returns True without modification). So Variant 5 Run 1 happens to work by accident.
- **For the 4-color case (Variant 5 Run 2):** AC-3 returns True without modifying domains, then backtracking runs from full domains. Fine, but the doc-block makes no promise about this behavior — it's accidental.
- **Why this is P1:** the variant says "confirm AC-3 says feasible, then run backtracking and report whether AC-3 reduced the search". The expected-answer shape at line 153-158 says "Backtracking still discovers the conflict through normal search. This is a teaching moment: AC-3 is necessary but not sufficient." But the *underlying* fact — that AC-3 with binary not-equal constraints and |D| ≥ 2 will *never* reduce a domain in the first place, so its only output is True/False with no side-effect — is not stated in the doc-block. A fresh agent might assume AC-3 strengthened domains and report fewer backtracks; in fact it returns instantly with no change.
- **Suggested fix:** Add to the `ac3()` docstring: "On binary not-equal CSPs with all domain sizes ≥ 2, AC-3 is a no-op (every value has support in every neighbor). It will return True for feasibility check but will not actually prune anything. Use forward checking during search for actual pruning."

### P1-7. Variant 1's claimed "Brazil has 10 neighbours" is correct, but the variant fails to call out that Chile and Brazil do NOT border (an obvious source of confusion).

- **Where in variants:** `variants.md:42-44`:
  > "Brazil is the single highest-degree node (10 neighbours)."
- **Where in code:** `constraints_template_solution.py:628-631`:
  ```python
  S.BRAZIL: [
      S.COLOMBIA, S.VENEZUELA, S.GUYANA, S.SURINAME, S.FRENCH_GUYANA,
      S.PERU, S.BOLIVIA, S.PARAGUAY, S.ARGENTINA, S.URUGUAY,
  ],
  ```
  Confirmed 10 neighbors (no Chile, no Ecuador).
- **Why this is P1:** an agent looking at a South America map might confidently say "Brazil has 11 neighbours, including Ecuador" — but Ecuador and Brazil do not share a border. Same for Chile (Andes separate them). The doc-block at `constraints_template_solution.py:594-609` does list Brazil's 10 borders accurately, but an exam agent reading only the KNOB doc and skipping the function comment will not see this. The variant's claim of "10 neighbours" is verifiable only by reading the code, which violates the variant-adaptability contract.
- **Suggested fix:** Add to the variant prompt one line: "Brazil borders 10 countries (all of Colombia, Venezuela, Guyana, Suriname, French Guyana, Peru, Bolivia, Paraguay, Argentina, Uruguay — but NOT Ecuador or Chile, which the Andes separate)." This makes Variant 1's claim independently verifiable.

### P1-8. The `recursive_backtracking` increments `_backtracks` *even when the recursion succeeds at this level* — no, wait, let me re-read.

- **Where in code:** `constraints_template_solution.py:323-337`:
  ```python
  if fc_ok:
      result = self.recursive_backtracking(assignment)
      if result is not None:
          return result        # SUCCESS path — does NOT increment _backtracks
  if fc_snapshot is not None:
      self._restore_domains(fc_snapshot)
  del assignment[variable]
  self._backtracks += 1        # FAILURE path
  ```
- **Verdict:** OK — `_backtracks` is incremented only on the failure path. **However**, the counter increments **once per failed value**, not "once per backtrack-from-this-level". On a tight problem, a single failed variable that tries (and fails) all 4 values registers as 4 backtracks. R&N's standard convention is "1 backtrack = 1 return-failure from a recursive call". The convention here is closer to "number of times a value assignment was undone".
- **Why this is P1:** Variant 2 prompts "Why does increasing the palette never increase backtracks?" The student is comparing two numbers labeled "Backtracks: X". If the convention is "values undone", a 5-color run that succeeds in N assignments still increments _backtracks 0 times (each variable's first value works). A 3-color infeasible run increments _backtracks once per failed value. That's a meaningful comparison.

  But if a future variant asks "how many *recursive calls* were aborted?", the answer is different. The doc-block at line 263-266 says "Recursive calls: N, Backtracks: M" — neither term is defined.
- **Suggested fix:** Add to the `_backtracks` field comment: "Counts the number of times `assignment[variable] = value` was undone (i.e., once per failed value, not once per failed variable)." Same for `_recursive_calls`: "Counts each entry into `recursive_backtracking`, including the call that succeeds at the leaf."

---

## P2 — Polish and minor improvements

### P2-1. Type alias typo `contraintFunction` preserved from template.

- **Where:** `constraints_template_solution.py:147`. The template's typo (`contraintFunction` missing the 's') is preserved verbatim. The comment at line 145-147 says "kept identical to the template — Reviewer #1 'Function signature preservation' cross-checks these". Fine for compat, but worth a one-liner: "(yes, the typo is intentional for template compat)".

### P2-2. `backtracking_search` returns `None` when the assignment dict is empty.

- **Where:** `constraints_template_solution.py:278`: `return result if result else None`.
- **Issue:** for a zero-variable CSP (hypothetical), `is_complete({})` would return True and `recursive_backtracking` would return `{}`. The truthiness check `result if result else None` then converts `{}` to `None`. Should be `result if result is not None else None` or simply `return result`. Edge case but the failure mode is silent.

### P2-3. Variant 3's `distance_demo` reuses Australia enum members (WA, NT, Q, NSW, V) as "abstract regions".

- **Where:** `constraints_template_solution.py:661-667`. The comment says "naming is irrelevant, only adjacency matters", but the printout will say `States.WA: Red, States.Q: Green, ...` even though we're talking about an abstract A/B/C/D/E layout. The agent answering Variant 3 will paste output that mentions "WA" and "NT" — confusing for an examiner expecting the abstract names.
- **Suggested fix:** add explicit A/B/C/D/E enum members to `States_solution.py` (e.g. `A_NODE = 31`, etc.) OR have `_print_report` translate WA/NT/Q/NSW/V to A/B/C/D/E in the distance-demo case. Or at least mention the mapping in the printout: `# variables.WA == "A"`, `# variables.NT == "B"`, etc.

### P2-4. `Color.Purple` is loaded into the palette enum but never used by default.

- **Where:** `Colors_solution.py:74` defines `Purple = "Purple"`. The doc-block says it's there "so the entry point can flip a single KNOB without editing this module". Fine — but the comment at line 56-58 calls it a "KNOB" when it's actually an enum member, not a KNOB. Loose terminology.

### P2-5. `_print_report` accesses `csp._recursive_calls` and `csp._backtracks` (private attributes) from outside the class.

- **Where:** `constraints_template_solution.py:716-717`. Single-underscore "private" is a Python convention, not enforcement. But the `_print_report` is in the same module so this is fine. Still, exposing them as public counters (`csp.recursive_calls`) or via a `csp.stats()` method would be cleaner.

### P2-6. The doc-block "OUTPUTS WHEN RUN" example (line 116-129) is for the default Australia run.

- The example output shows `Recursive calls: 7, Backtracks: 0` — which a careful agent can verify by hand against the Australia graph. Good touch. But the doc-block does NOT show example outputs for any of the variants. An agent answering Variant 2 (5-color South America) has no anchor for "is my answer 'Backtracks: 0' the right shape?" Adding 2-3 sample outputs (one per variant family) would close this gap.

### P2-7. `create_distance_csp` uses `(0,0)`, `(2,0)`, etc. as floats but the variant table speaks of "edges" and "regions" abstractly.

- The doc-block comments are clear but the coordinate system is asymmetric: the hub C is at (1,1), not at the centroid (1.0, 1.0) — wait, it is at (1.0, 1.0). Never mind. But the diagram in the docstring at line 648-652 draws C at the center; that's visually fine.

### P2-8. The constraint dictionary stores `len(variables)` identical references to a single function.

- **Where:** `_make_not_equal_constraints` at `constraints_template_solution.py:535-556`. The dict has 13 entries, all pointing to the same closure. Memory-trivial but semantically misleading — looks like "each variable has its own constraint" when really there's one constraint shared. Could be replaced by a single attribute `self.constraint: contraintFunction` and dropping the per-variable dict, but this would break template-signature compat (the template specifies `constraints: dict[States, contraintFunction]`). So leave it for the template lock — but mention in the `_make_not_equal_constraints` docstring that "this dict is structurally identical for every variable in a not-equal-only CSP; the per-variable dict is a generality lever for future asymmetric-constraint variants".

### P2-9. Variant 2's "5-color run: 0 backtracks" expected-answer says "in O(N) calls".

- **Where in variants:** `variants.md:70-71`. The O-notation here is sloppy: each call processes one variable, so the call count is exactly N (the number of variables) when there are no backtracks. "O(N) calls" is technically correct but inviting confusion with the O(d^N) worst-case complexity of CSP. Recommend "exactly N+1 calls (one entry per variable, plus the base case)".

### P2-10. Variant 4's "Run | Heuristics" table doesn't list `MAP_NAME` or `ACTIVE_COLORS`.

- **Where in variants:** `variants.md:116-127`. The KNOB instruction at line 126-127 just says "progressively turn on USE_MRV..." but doesn't reset `MAP_NAME` or `ACTIVE_COLORS`. An agent who has just run Variant 1 (south_america, 4 colors) is in luck; an agent who jumps in fresh and forgets to set MAP_NAME=south_america will silently solve Australia. The table should explicitly include `MAP_NAME: "south_america"`, `ACTIVE_COLORS: [Red, Green, Blue, Yellow]` in every row.

### P2-11. Variant 5 KNOB table says "ACTIVE_COLORS as above" — ambiguous reference.

- **Where in variants:** `variants.md:149`. "As above" refers to the two palettes listed in the prose at line 144-148. But a fresh agent skimming the KNOB block at line 149 may overlook the prose. Replace with explicit `ACTIVE_COLORS = [Red, Green, Blue]` for Run 1 and `[Red, Green, Blue, Yellow]` for Run 2.

### P2-12. `_forward_check` returns `(snapshot, ok)` but the caller doesn't use the snapshot when `ok=False` to roll back partial prunes.

- Wait — re-reading `constraints_template_solution.py:319-322` carefully:
  ```python
  fc_snapshot, fc_ok = self._forward_check(variable, value, assignment)
  if fc_ok:
      result = self.recursive_backtracking(assignment)
      ...
  if fc_snapshot is not None:
      self._restore_domains(fc_snapshot)
  ```
  When `fc_ok=False`, the code skips the recursion (good) and then unconditionally restores the snapshot (good, since `fc_snapshot` is set whether or not FC succeeded). OK, this is correct. False alarm. **But** the variable `fc_snapshot` is only set inside `if USE_FORWARD_CHECK`, so when FC is off, `fc_snapshot` stays `None` (default) and the `if fc_snapshot is not None:` guard skips the restore — correct. So this code path is OK; remove this P2.

### P2-13. The `if result else None` idiom in `backtracking_search` line 278 hides the actual return type.

- Method signature is `-> dict[States, Color] | None`, so returning `{}` (a valid solution to a 0-variable CSP) gets coerced to None. See P2-2 — duplicate-flagged.

---

## Variant-by-variant adaptability scorecard

| Variant | KNOB-only contract holds? | Expected-answer text is achievable? | Verdict |
|---|---|---|---|
| 1 — MRV + degree on South America | **FAIL** — MRV is a no-op without FC; BRAZIL pick is from degree alone, not MRV. KNOB table conceals this. | Partial — BRAZIL pick works *only* because `USE_DEGREE_TIEBREAK=True` is in the table. Sentence "MRV's first choice is BRAZIL" is misleading. | **FAIL** |
| 2 — 5-color vs 3-color South America | PASS — KNOBs alone suffice. | PASS — 5-color: 0 backtracks. 3-color: returns None with nontrivial backtracks. The "why does increasing palette never increase backtracks" answer is supportable. | **PASS with concerns** — 4-color baseline (mentioned in Variant 4) is also 0, so "increasing palette reduces backtracks" only demonstrable at the 3-color boundary. |
| 3 — distance threshold | KNOB-only: yes. | **FAIL** — Run A description "only C touches A and B" is factually wrong; C touches all 4 corners at threshold 1.5. Chromatic-number conclusions still correct. | **FAIL** |
| 4 — forward checking comparison on South America | **FAIL** — MRV row is a no-op without FC (P0-1), and across runs domains leak (P0-3). Baseline backtracks are 0 so all three rows are 0-0-0. | **FAIL** — "Backtracks decrease monotonically" cannot be demonstrated on a 0-baseline. | **FAIL** |
| 5 — AC-3 pre-pass | KNOB-only: **FAIL** — requires a driver script (no KNOB triggers `ac3()` from main). | PASS — once the driver is written, the variant's expected-answer ("AC-3 returns True without reducing search") is achievable. | **FAIL on KNOB-only contract; PASS on substance.** |

**Aggregate: 1/5 fully PASS (Variant 2 with concerns); 0/5 PASS without concerns; 4/5 FAIL on either KNOB-only contract or expected-answer accuracy.**

---

## EVIDENCE — direct citations

### Solution code: `_select_mrv` reads static domain only
```python
def domain_size(v: States) -> int:
    return len(self.domains[v])           # ← unchanged by assignment alone
```
`constraints_template_solution.py:409-410`. With FC off, no code path mutates `self.domains` during search, so all unassigned variables tie and the sort is a no-op.

### Solution code: domains[neighbour] mutated only inside FC
```python
self.domains[neighbour] = [v for v in self.domains[neighbour] if v != value]
```
`constraints_template_solution.py:467-469`. The only write to `self.domains` in the entire search loop. `ac3()` also writes (`self.domains[x] = new_domain`, line 526) but that's a pre-pass.

### Solution code: success path skips snapshot restore
```python
if fc_ok:
    result = self.recursive_backtracking(assignment)
    if result is not None:
        return result                     # ← early return, no restore
if fc_snapshot is not None:
    self._restore_domains(fc_snapshot)    # ← only reached on failure
```
`constraints_template_solution.py:323-334`. Confirms P0-3.

### Distance-demo coordinates
```python
States.WA: (0.0, 0.0),  # "A"
States.NT: (2.0, 0.0),  # "B"
States.Q:  (1.0, 1.0),  # "C"  -- the hub
States.NSW:(0.0, 2.0),  # "D"
States.V:  (2.0, 2.0),  # "E"
```
`constraints_template_solution.py:662-666`. C-A = C-B = C-D = C-E = √2 ≈ 1.414 — all four spokes ≤ 1.5. Refutes Variant 3 Run A description.

### South America Brazil neighbour list (10 confirmed)
```python
S.BRAZIL: [
    S.COLOMBIA, S.VENEZUELA, S.GUYANA, S.SURINAME, S.FRENCH_GUYANA,
    S.PERU, S.BOLIVIA, S.PARAGUAY, S.ARGENTINA, S.URUGUAY,
],
```
`constraints_template_solution.py:628-631`. Confirms 10 neighbors. Confirms Brazil does NOT border Ecuador or Chile.

### Variant 1 KNOB table
```
| USE_MRV | False | True |
| USE_DEGREE_TIEBREAK | False | True |
```
`variants.md:38-39`. Both must flip; the variant's prose at line 23 reads "Use the **MRV** variable-ordering heuristic (and the **degree** tie-breaker)" — parenthesizing degree as if it were optional, when in fact degree alone does all the work.

### Variant 5 driver-script requirement
> "Call `csp.ac3()` BEFORE `csp.backtracking_search()` in a tiny test script (signatures only — no need to read AC-3's body)."

`variants.md:150-151`. Confirms there is no KNOB for AC-3 invocation.

---

## Report to PM

**Assignment recap:** Lab Reviewer #4 (Variant Adaptability) for Lab6-CSP Round 1. Reviewed `lab6\constraints_template_solution.py`, `lab6\Colors_solution.py`, `lab6\States_solution.py`, the lab handout PDF, and `study\_exam\Lab6-CSP\variants.md`. Mandate: verify the KNOB-only contract holds for every variant.

**Status:** **Fail** (4 P0, 8 P1, 11 P2; 4 of 5 variants fail on either contract or expected-answer accuracy).

**P0 findings:**
1. `constraints_template_solution.py:402-424` — `_select_mrv` reads static `self.domains[v]` instead of dynamic legal-values count. Without FC enabled, MRV is a no-op and degenerates to declared-order. Variant 1's "MRV picks BRAZIL first" claim is false; only degree tie-break achieves it. **Fix:** rewrite `_select_mrv` to count legal values dynamically via `is_consistent`, OR document loudly that MRV requires FC to be meaningful, OR rewrite Variant 1's KNOB table to credit degree explicitly.
2. `variants.md:88` — Variant 3 Run A claims "only the hub C touches A and B" at threshold 1.5; the actual code creates K_{1,4} (C touches all four corners A, B, D, E, since √2 ≈ 1.414 ≤ 1.5). Chromatic-number conclusion (=2) still holds but edge description is wrong. **Fix:** update variant table to reflect the full star.
3. `constraints_template_solution.py:323-334` — `recursive_backtracking` returns successful result without restoring forward-checking snapshot, leaving `self.domains` permanently corrupted for re-runs. Variant 4's three-run driver workflow will silently produce garbage on second/third call. **Fix:** restore snapshot before successful return, OR snapshot/restore `self.domains` in `backtracking_search` wrapper, OR document single-use semantics.
4. `variants.md:149-151` / `constraints_template_solution.py` (main entry) — Variant 5 requires `csp.ac3()` to be called explicitly, but no KNOB triggers it. Violates the variant-bank preamble's "KNOBs alone" contract (variants.md:6-15). **Fix:** add `USE_AC3_PRE_PASS: bool = False` KNOB and a two-line invocation in `__main__`, OR file a STUCK report and revise the variant.

**P1 findings:**
1. `variants.md:50-73, 110-132` — Variant 2 and Variant 4 baseline (South America 4 colors, no heuristics) yields 0 backtracks; the "increasing palette / adding heuristics reduces backtracks" comparisons are flat-zero on this map. Variant 4's "monotonic decrease" claim has nothing to decrease from. **Fix:** switch Variant 4's map/palette to a configuration with a nonzero baseline (e.g. 3-color South America).
2. `variants.md:116-127` — Variant 4 row 2 says "MRV + degree" but MRV without FC is a no-op (P0-1); the row's actual behavior equals "degree only". Mislabels which heuristic does the work. **Fix:** rename row, or fix P0-1.
3. `constraints_template_solution.py:389-395` — `is_consistent` iterates `self.constraints.values()` (length |variables|) for each neighbor check; redundant by O(|V|). Correctness is preserved only because all constraint functions are the same reference. Inflates any "constraint-call count" answer. **Fix:** use `self.constraints[variable]` directly.
4. `constraints_template_solution.py:38-42, 184-191` — Doc-block describes textbook MRV ("currently legal-domain count") but implementation reads static declared domain. Fresh agent reading only the doc will misinterpret what `USE_MRV=True` does. **Fix:** align doc with code, or fix code to match doc (preferred).
5. `constraints_template_solution.py:440-443` vs `381-396` — `_lcv_count` uses `self.constraints[variable]` (correct convention) while `is_consistent` iterates all constraints. Inconsistent within the same class. **Fix:** unify to single convention.
6. `constraints_template_solution.py:485-511` — `ac3()` permanently mutates `self.domains` with no snapshot/restore. Plus, on binary not-equal CSPs with |D| ≥ 2 it never prunes anything — doc-block doesn't mention this. **Fix:** add note to docstring that AC-3 is a no-op on the lab's specific constraint shape.
7. `variants.md:42-44` — Variant 1's "Brazil has 10 neighbours" claim is correct but not independently verifiable without reading code (an exam agent might wrongly include Ecuador or Chile). **Fix:** list the 10 borders explicitly in the variant prompt.
8. `constraints_template_solution.py:263-266, 337` — `_backtracks` counts "values undone" not "recursions aborted". Both `_recursive_calls` and `_backtracks` are undefined in the printout's mental model. **Fix:** define explicitly in the doc.

**P2 findings:** Type-alias typo preserved (P2-1); empty-assignment return-type coercion (P2-2); distance_demo reuses Australia enum members (P2-3); Purple enum mislabeled "KNOB" (P2-4); private-counter access from outside class (P2-5); no example outputs for variants (P2-6); coordinate diagram minor (P2-7); constraint-dict-of-identical-refs (P2-8); "O(N) calls" sloppy notation in Variant 2 (P2-9); Variant 4 KNOB table omits MAP_NAME / ACTIVE_COLORS (P2-10); Variant 5 KNOB "as above" ambiguous (P2-11); fc_snapshot-when-FC-off path verified OK (P2-12, retract); empty-result return idiom (P2-13).

**QA Checklist (§7 — Variant Adaptability) status:**
- KNOB-only contract holds for every variant → **Fail** (P0-1, P0-4)
- Expected-answer text in `variants.md` is accurate → **Fail** (P0-2 for V3; P1-1 for V4)
- Solution code is self-consistent across re-runs → **Fail** (P0-3)
- Doc-block matches code behavior → **Fail** (P1-4)
- All five variants demonstrably runnable with documented KNOBs → **Fail** (V5 needs driver script)
- Heuristic semantics (MRV, degree, LCV, FC, AC-3) match textbook → **Partial Fail** (MRV requires FC; AC-3 no-ops on this constraint shape — both undocumented)
- Constraint graph data (neighbours dicts) is geographically accurate → **Pass** (Brazil 10 confirmed, Tasmania isolated, etc.)
- Printout is deterministic and reproducible → **Pass** (sorted by enum value)
- Forward-checking restore-on-failure is correct → **Pass** (verified line-by-line)
- AC-3 implementation is correct → **Pass** (textbook AC-3, though no-op on this map)

**Acceptance criteria (§1) status:**
- V1 (MRV picks Brazil first) → **Not met** without degree tie-break; KNOB combination conceals which heuristic actually drives the pick.
- V2 (5-color vs 3-color comparison) → **Met** at face value; substance shaky because 4-color baseline is also 0.
- V3 (three thresholds: 2, 3, ≥4 chromatic) → **Met for chromatic numbers; not met for Run A edge description.**
- V4 (monotonic backtrack decrease) → **Not met** on this map/palette (all rows are 0).
- V5 (AC-3 doesn't detect 3-color infeasibility) → **Met in substance; not met on KNOB-only contract.**

**DOCUMENT.md audit:** N/A for lab review (the lab6/ directory has no DOCUMENT.md and the variant bank doesn't require one).

**Out-of-scope observations:**
- The solution code is *exceptionally* well-documented compared to the other labs in this study package. The doc-block's "HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS" section (line 60-108) is a model worth replicating in Lab1-Agents, Lab2-Search, Lab4-GA, Lab5-AlphaBeta.
- The MRV-needs-FC issue is a pedagogically interesting trap — *the textbook itself* (R&N §6.3.2) is ambiguous about whether MRV needs FC. Some implementations (e.g. AIMA-Python) compute legal-values on the fly; others assume FC maintains live domains. This solution is in the "FC required" camp without saying so. Worth a lecture-chapter footnote in L07-CSP.
- Variant 4 on a richer map (e.g. 3-color South America showing dozens of backtracks reduced to <10 by MRV+degree, then to 0 by adding FC) would be the *intended* pedagogy of forward checking. The current Variant 4 is "all zeros" — pedagogically weak even when the code is fixed.
- Tasmania's empty neighbour list (`States.T: []`) is a nice test of the "isolated variable" case — Australia variants implicitly rely on this. Good coverage.

**Concerns / risks:**
- An exam agent that toggles `USE_MRV=True` *alone* (no degree, no FC) will report "MRV gave me COLOMBIA first, not BRAZIL — the variant key is wrong". The agent is technically right (the code does pick COLOMBIA); the variant key is implicitly assuming degree-tiebreak is also on. This will burn 20 minutes of confusion per Variant 1 attempt.
- The FC snapshot leak (P0-3) is the single most dangerous bug — it silently corrupts state across runs and there is no in-band signal to detect it. An agent running Variant 4's three-row comparison via a single CSP instance will report garbage backtrack counts and have no way to know.
- Variant 3 Run A's edge-description error is small but will be the first thing a careful examiner catches when asking "draw the constraint graph at threshold 1.5". Mark-down risk: 1-2 points.
- The doc-block claims things ("MRV reduces backtracks by an order of magnitude on dense constraint graphs") that this implementation simply cannot deliver on its own. A student building flashcards from the doc-block will learn a half-truth.

**What PM should do next:**
1. Fix P0-1 first (MRV semantics) — either repair the code to compute legal values dynamically, or repair the doc-block and Variant 1 to credit degree-tiebreak explicitly. Recommend repairing the code — it's a 6-line change in `_select_mrv` and makes the doc-block honest.
2. Fix P0-3 (FC snapshot leak on success) — 3-line change in `recursive_backtracking`.
3. Fix P0-2 (Variant 3 Run A edge description) — one-line change in `variants.md`.
4. Address P0-4 by adding `USE_AC3_PRE_PASS` KNOB + 2-line invocation, OR file a STUCK report per the variant-bank preamble.
5. Then re-dispatch Reviewer #4 to verify all five variants pass on KNOB-only contract.
6. Defer P1s to Round 2 (especially the Variant 4 baseline-is-zero issue, which needs variant-bank surgery, not code surgery).
7. P2s can wait for polish pass.
8. Do not advance to Reviewer #5 (or whatever sits downstream) until at minimum P0-1 and P0-3 are fixed.

**DOCUMENT.md updated:** N/A for QA.

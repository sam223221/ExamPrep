# Lab6-CSP — Reviewer #3 (Pedagogical Clarity), Round 1

**Reviewer role:** Lab Reviewer #3 — Pedagogical Clarity
**Assignment recap:** Review `lab6/*_solution.py` against `study/lectures/L07-CSP.md` for pedagogical clarity (does a student reading this solution learn what the lecture promised?).
**Files inspected (absolute paths):**

- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\Colors_solution.py`
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\States_solution.py`
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\constraints_template_solution.py`
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\Colors.py` (template, for diff context)
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\States.py` (template, for diff context)
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\lab6\constraints_template.py` (template, for diff context)
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L07-CSP.md`

**Status:** **Fail** — multiple P0 pedagogical defects make the solution actively misleading for the very concepts the lab is meant to teach (MRV, LCV, forward-checking, arc consistency).

---

## P0 Findings (broken pedagogy / actively misleading)

### P0-1. MRV is a no-op without forward checking — student will conclude MRV is useless

**Location:** `constraints_template_solution.py:402–424` (`_select_mrv`) and the `USE_MRV` knob block at L181–192.

**Problem.** `_select_mrv` ranks unassigned variables by `len(self.domains[v])`. But `self.domains` is the **static, never-pruned** domain dict; it is only mutated when `USE_FORWARD_CHECK=True` triggers `_forward_check`. With MRV on and FC off (the natural "demonstrate MRV in isolation" configuration), every unassigned variable has the **same** domain size, so MRV degenerates to `unassigned[0]` — i.e. declaration order. The student turns MRV on, sees zero change in backtrack count, and walks away thinking MRV is theatre.

This directly contradicts the lecture, which presents MRV as a **standalone** heuristic (L07 §4.4 "Variable ordering — MRV and degree heuristic" never mentions that MRV requires FC to be useful) — the slide treats *remaining legal values* as a property computed from the current partial assignment, not a property of a statically-stored domain list. A correct MRV computes "values consistent with the current assignment", not `len(self.domains[v])`.

**Pedagogical damage.** The docstring at L186–188 *promises* "typically reduces the number of backtracks by an order of magnitude on dense constraint graphs". The default sample run config (Australia, 7 vars, FC off) reports 0 backtracks already, so the order-of-magnitude claim cannot even be observed. The student gets neither the claim nor the underlying lesson.

**Suggested fix.** Compute remaining legal values dynamically: `len([v for v in self.domains[var] if self.is_consistent(var, v, assignment)])`. Document explicitly that MRV requires either (a) dynamic legal-value counting or (b) live domains via FC.

---

### P0-2. LCV is a no-op for uniform-domain map-coloring — same trap as MRV

**Location:** `constraints_template_solution.py:426–443` (`_lcv_count`), L373–379 (`order_domain_values`), and the `USE_LCV` knob at L204–212.

**Problem.** `_lcv_count` iterates `for nv in self.domains[neighbour]`. With FC off, `self.domains[neighbour]` is the same `ACTIVE_COLORS` list for every neighbour. For a `≠` constraint with uniform domains, the count of "values that would be ruled out" is identical for every candidate value of every variable — every value rules out exactly one neighbour-value (itself) per unassigned neighbour. The sort key is a constant; LCV becomes a no-op identity sort.

The student turns LCV on, sees the same output, and concludes the heuristic is broken or fake. The lecture (§4.5) explicitly promises LCV "improves the first-found-solution runtime" — a promise this implementation cannot demonstrate on the only configuration a student is likely to run.

**Suggested fix.** Either (i) score LCV against neighbours' *live* domains (forcing FC to be on, with explicit documentation), or (ii) provide a deliberately non-uniform domain configuration in the demo set where LCV actually differentiates values. Currently the file does neither.

---

### P0-3. `is_consistent` does O(V × N) work for what should be O(N) — and the comment doesn't warn the student

**Location:** `constraints_template_solution.py:381–396` (`is_consistent`), also `constraints_template.py:40–52` (inherited from template).

**Problem.** The outer loop is `for constraint in self.constraints.values():` — iterating over **every variable's constraint function**, even though we're only checking the consistency of one variable. The inner loop then walks that variable's neighbours. So for Australia with 7 variables we run the constraint check 7× more often than necessary. For South America (13 variables) we run it 13×. Every recursive call's consistency test is multiplied by `V`.

This is a pre-existing template wart, but Reviewer #3 cares: the solution **preserves the bug, comments at L382 say "Same contract as the template"**, and the student walks away believing this is normal consistency-check shape. It's not. The textbook (and L07 §4.1) describe consistency as "check value against constraints involving currently-assigned neighbours" — a single inner loop, not a doubled one.

**Pedagogical damage.** When the student later tries to instrument or profile, the "Recursive calls / Backtracks" numbers will be honest but the *work per call* is bloated, distorting comparisons between FC-on vs FC-off runs.

**Suggested fix.** Drop the outer `for constraint in self.constraints.values():` loop; pull `constraint = self.constraints[variable]` once and run the inner neighbour loop. Add a comment explaining why the template's nested loop is wrong.

---

### P0-4. `_forward_check` is named generically but only works for `≠` constraints — abstraction lies

**Location:** `constraints_template_solution.py:445–475`.

**Problem.** The function prunes `value` from each unassigned neighbour's domain — i.e. it assumes "the only neighbour-value that conflicts with `value` is `value` itself". That is the **special case of `≠` constraints**. For *any* other constraint (`<`, `|x-y|≠d`, alldiff variants, the cryptarithmetic column-sum constraints from L07 §3.4.3, the n-queens diagonal constraints from L07 §4.7), this implementation is silently wrong.

The lecture (L07 §4.6) defines forward checking as "remove from $Y$'s domain every value that is inconsistent with $X = v$" — *test* each neighbour-value, don't *equate* it with `value`. The proper FC loop is `for nv in D[neighbour]: if not constraint(var, value, neighbour, nv): remove nv`. This solution short-circuits that loop.

**Pedagogical damage — severe.** A student who reads this solution and then tries to apply FC to the 4-queens trace from L07 §4.7 (slides 35–44, *the* worked example for FC in the lecture) will write the wrong code. The lecture's diagonal-constraint reasoning in L07 §4.7 (slides 36–37: "Stage 2: after $X_1=1$, $X_2 \in \{3,4\}, X_3 \in \{2,4\}, X_4 \in \{2,3\}$") is impossible to reproduce with the solution's FC routine — the pruning of column 2 from $X_2$, column 3 from $X_3$, column 4 from $X_4$ is *not* "remove value 1 from each future row's domain".

This is the single most damaging pedagogical issue in the entire submission, because the lab's stated **Homework Challenge** *is* forward checking, and the solution's FC is wrong for any constraint other than the toy `≠` one already on the page.

**Suggested fix.** Rewrite `_forward_check` to call `self.constraints[...]` on each candidate neighbour-value and remove only those that fail the constraint. Add a worked comment that maps the routine onto the 4-queens trace from L07 §4.7.

---

### P0-5. `_revise` (in AC-3) and `_lcv_count` look up the **wrong constraint**

**Location:** `constraints_template_solution.py:513–527` (`_revise`), L426–443 (`_lcv_count`).

**Problem.** Both functions resolve the constraint as `self.constraints[x]` (i.e. the constraint indexed by the *first* variable). In this map-coloring CSP every entry of `self.constraints` is the **same** `constraint_function` literal (built by `_make_not_equal_constraints`), so the bug is invisible. But the solution is presented as a *generalisable* CSP scaffold (see the elaborate "HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS" section at L60–108, which includes a distance-based variant). For any CSP where the constraint depends on the **pair** $(X, Y)$ (the n-queens diagonals, the cryptarithmetic column sums), this lookup gives the wrong relation.

The lecture (L07 §3.1) defines a constraint as `⟨scope, rel⟩` — the relation is over the pair, not owned by one variable. Indexing `constraints[x]` mis-teaches the data structure.

**Pedagogical damage.** A student transfers this code to a different CSP problem (one of the variants the docstring brags about supporting) and the code silently solves the wrong problem.

**Suggested fix.** Change the constraints data structure to `Dict[FrozenSet[States], contraintFunction]` or `Dict[Tuple[States, States], contraintFunction]`. At minimum, add a comment in `_revise` and `_lcv_count` saying "this implementation assumes a single global constraint relation across all pairs".

---

## P1 Findings (important pedagogical / convention issues)

### P1-1. `recursive_backtracking` return type silently drifts from the template

**Location:** `constraints_template_solution.py:284`, vs template `constraints_template.py:20`.

The template's signature is `-> Dict[States, Color]`. The solution's is `-> Optional[Assignment]`. Reviewer #1 (function-signature preservation) will flag this; from a Reviewer #3 lens, the docstring at L242–249 *brags* "Public surface is identical to constraints_template.py (Reviewer #1 verifies)" — but the public surface is **not** identical. This is a discipline failure: the comment claims a property the code does not satisfy.

**Suggested fix.** Pick one — either restore the original return type (`Dict[States, Color]` with `None`-as-failure shoehorned into the docstring) or update the boast in the docstring to "signature evolved to express the failure path explicitly".

---

### P1-2. `from Colors_solution import Color` / `from States_solution import States` breaks drop-in compatibility

**Location:** `constraints_template_solution.py:142–143`.

The template imports `from Colors import Color` and `from States import States`. The solution imports the `_solution` variants. A grader running the solution side-by-side with the template will get import-error churn or — worse — accidentally mix template and solution objects. Pedagogically, the file presents itself as "what a student should end up with" but isn't compatible with the lab's stated entry layout.

**Suggested fix.** Either rename `Colors_solution.py` → `Colors.py` for the submission, or have the solution import from the original modules and document the divergence.

---

### P1-3. Verbose docstrings drown the actual lesson

**Locations:**
- `Colors_solution.py:1–50` — 50 lines of docstring + KNOB comments for an 8-member Enum.
- `constraints_template_solution.py:1–134` — 134-line module docstring before any code.
- `constraints_template_solution.py:151–233` — 82 lines of "KNOB" comments before the class definition.

The module docstring's "HOW TO ADAPT THIS FOR DIFFERENT QUESTION VARIANTS" (10+ sub-bullets) is a configuration manual, not a lesson. A student opening the file to learn backtracking has to scroll past 230 lines of variant guides before reading any algorithm code. The lecture (L07 §4.1) presents the algorithm in 12 lines of pseudocode; the solution buries it under 20× that volume of prose.

**Pedagogical damage.** Important comments — the line-by-line pseudocode mapping at L293–340 — are lost in the noise. The student stops reading before reaching them.

**Suggested fix.** Move the variant manual to a sibling `README.md` or `DOCUMENT.md`. Keep the module docstring to ≤30 lines: one paragraph naming the lab, one referencing the lecture, one listing the entry-point command.

---

### P1-4. `__eq__` / `__hash__` override on `States` reintroduces the default Enum behaviour with extra fragility

**Location:** `States_solution.py:87–101` (also present in the template).

`Enum` already provides identity-based `__eq__` and hash. The override uses `self.value == other.value`, which would equate two members with the same integer value (impossible by default Enum semantics, but conceptually opens the door). Worse, `__eq__` returning `False` for `type(other) != type(self)` means `States.WA == "WA"` is `False` (fine) but the customised `__eq__` was never necessary in the first place — the comment at L87 says "Why: enable stable sorting of mixed-map result dicts" but that's `__lt__`'s job, not `__eq__`'s.

Pedagogically, this is mystery code: a student reads it, asks "why is this needed?", finds no good answer, and concludes Python's Enum is more fragile than it really is.

**Suggested fix.** Drop the `__eq__` / `__hash__` overrides; keep only `__lt__` with the comment explaining sorting. If the template requires them for some reason, document that reason.

---

### P1-5. `constraint_function` self-comparison short-circuit is unjustified

**Location:** `constraints_template_solution.py:545–554`, also `constraints_template.py:78–80`.

```python
return first_value != second_value or first_variable == second_variable
```

When would `is_consistent` call the constraint with `first_variable == second_variable`? Looking at the caller (L389–395), it iterates `neighbour in self.neighbours[variable]` — and a variable should never be in its own neighbours list. So the `or first_variable == second_variable` clause is dead-code that *appears* to handle a degenerate case. A student reading this thinks "oh, there must be self-loops in the constraint graph" — there aren't, and the lecture (L07 §3.3) is explicit that the constraint graph has no self-loops.

**Suggested fix.** Drop the `or first_variable == second_variable` clause; if the template insists on it, add a comment "defensive only; the call sites never pass identical variables".

---

### P1-6. `MAP_NAME="distance_demo"` reuses Australia enum members for non-Australia regions

**Location:** `constraints_template_solution.py:661–667`.

`create_distance_csp` assigns abstract coordinates to `States.WA, States.NT, States.Q, States.NSW, States.V`. The printout will say `States.WA: Red` for a variable that has nothing to do with Western Australia. The comment at L659 ("naming is irrelevant, only adjacency matters") acknowledges the issue but doesn't fix it. A student reading the output is confused; a student grading the demo wonders if the WA-NT adjacency from Australia somehow leaked in.

**Suggested fix.** Add five generic enum members (`R1, R2, R3, R4, R5`) for the distance demo; the lab already shows how to extend the States enum.

---

### P1-7. Sample-output block in module docstring (L116–128) lists 7 lines but the `is_consistent` reordering puts T first in the variable list

**Location:** `constraints_template_solution.py:116–128` (claimed output) vs L564–567 (variable order: WA, Q, T, V, SA, NT, NSW).

The docstring claims the output's first variable line is `States.NT: Green`, but the actual variable order starts with WA. The printed output is sorted by `__lt__` (numeric value), so the sample claim *is* approximately right (the sort puts WA first — value 1 — but the docstring shows NT first). The claimed output is internally inconsistent. Either the docstring is stale or someone fixed the sort and forgot to update the example.

**Suggested fix.** Run the script, paste the actual output, commit. Better: pin the example output into a doctest or a snapshot file so this drift is caught automatically.

---

### P1-8. AC-3 is implemented but never wired in — and the docstring punts on why

**Location:** `constraints_template_solution.py:485–511` and L489–493.

The `ac3` method is private-by-virtue-of-being-hidden: nothing in the entry-point harness ever calls it, and the docstring explicitly says "The entry-point script does NOT call this by default (it would side-effect the printed backtrack counts)". So the homework-challenge "implement arc consistency" deliverable is technically present but **unobservable**: a student running the file cannot see AC-3 in action, cannot compare backtrack counts before/after AC-3, and gets none of the lecture's L07 §4.8 lesson ("Arc consistency detects failure earlier than forward checking").

**Suggested fix.** Add a `USE_AC3_PREPASS` knob; gate the `ac3` call on it; print "AC-3 pre-pass pruned X domain values" in the report.

---

## P2 Findings (polish, suggestions)

### P2-1. Inconsistent attribute prefix conventions

Public attributes (`variables`, `domains`, `neighbours`, `constraints`) coexist with leading-underscore instrumentation (`_recursive_calls`, `_backtracks`) and the report function reaches into the underscore-prefixed names (`csp._recursive_calls` at L716). Either expose them as public counters or wrap them in a public accessor.

### P2-2. The `_lcv_count` docstring (L427) says "Lower count == less constraining == try first" but doesn't reference L07 §4.5

The whole file goes to lengths to cite the lecture; the LCV helper is an exception. Add the citation.

### P2-3. `Color` enum values are stringly-typed (`Red = "Red"`)

Idiomatic alternatives (`auto()`, `IntEnum`) would avoid the redundancy `Red = "Red"`. Not a bug, just clutter for a student copying the pattern.

### P2-4. `Type alias contraintFunction` carries forward a typo from the template

The template has `contraintFunction` (missing `s`). The solution preserves it (L147). At minimum, add a comment "spelling kept for template-compat; canonical name is constraintFunction".

### P2-5. The South-America adjacency comment block (L594–609) duplicates the dict that immediately follows

Two sources of truth → one will eventually drift. Either drop the prose, or generate it from the dict.

### P2-6. The lecture-doc URL at the bottom (`https://mapchart.net/...`) belongs at the top with the rest of the references, not as a trailing comment

Minor; affects discoverability of the verification tool the comment suggests.

---

## Lecture-Alignment Audit (does the solution teach what L07 promises?)

| Lecture concept | L07 reference | Solution coverage | Verdict |
|---|---|---|---|
| Variables, domains, constraints (the triple ⟨X, D, C⟩) | §3.1 | `CSP.__init__` parameters | OK |
| Backtracking pseudocode | §4.1, slide 24 | `recursive_backtracking` mirrors the pseudocode line-by-line | OK (one of the strongest parts) |
| MRV variable ordering | §4.4 | `_select_mrv` exists but **is a no-op without FC** | **BROKEN** (P0-1) |
| Degree heuristic tie-break | §4.4 | `_select_mrv` tie-breaks by `-degree(v)` | OK in isolation, but inherits MRV's no-op behaviour |
| LCV value ordering | §4.5 | `_lcv_count` exists but **is a no-op on uniform-domain map-coloring** | **BROKEN** (P0-2) |
| Forward checking | §4.6 | `_forward_check` prunes only `value` itself from neighbours — **wrong for any non-`≠` constraint** | **BROKEN** (P0-4) |
| Arc consistency (AC-3 style) | §4.8 | `ac3` implemented, but **never invoked**, so unobservable | half-broken (P1-8) |
| Constraint graph as data structure | §3.3 | `neighbours` dict — fine, but `constraints` dict mis-models pair-relations | half-broken (P0-5) |
| Solution vs consistent vs complete vocab | §6, pitfall #1 | not addressed in code or comments | missed teaching opportunity |
| n-queens compact formulation (the FC worked example) | §3.4.2, §4.7 | not in scope of this lab (map-coloring only) — but FC implementation would fail to reproduce the lecture's trace | indirect P0 via P0-4 |

**Net pedagogical verdict.** Four of the six lecture concepts the lab is *supposed* to teach (MRV, LCV, FC, AC) are either broken, hidden, or invisible in the default run configuration. A student who reads only this solution will leave with **less** understanding of the heuristics than a student who reads the lecture alone.

---

## Concerns / Risks

1. **Pre-existing template bugs were preserved without comment.** `is_consistent`'s nested constraint loop (P0-3), the `constraint_function`'s self-comparison clause (P1-5), the `__eq__` override (P1-4), and the `contraintFunction` typo (P2-4) all come from the template. The solution adds nothing pointing them out; a student studying the solution learns the wrong patterns by inheritance.
2. **The solution is over-engineered for a teaching artifact.** The "distance_demo" variant, the AC-3 pre-pass, the 134-line module docstring — these are scaffolding for the variants file, not for student comprehension. A solution should be the *minimum code that demonstrates the lesson*. This one is the maximum.
3. **No tests, no DOCUMENT.md.** I cannot verify any of the solution's claims about backtrack counts (the L120–128 sample output is internally inconsistent, P1-7). Running the file would help but is out of scope for Reviewer #3.
4. **Round 1 only — these issues compound.** Reviewer #1 (function-signature preservation) will likely flag the same import / return-type issues. Reviewer #2 (correctness) will likely catch the FC `≠`-only bug if their test inputs include any non-equality constraint. Reviewer #3's job is to make sure that *even when the code is correct* it teaches the right lesson. As it stands, the code is partially incorrect *and* the lesson is muddled.

---

## What the PM should do next

1. **Dispatch the engineer to fix P0-1, P0-2, P0-4, P0-5 first.** Without these, the file actively miseducates. P0-3 is lower priority because it affects performance, not correctness or pedagogy of the headline algorithms — but it should be fixed in the same pass.
2. **Then address P1-1 (return-type drift), P1-2 (import path), P1-3 (docstring bloat) and P1-8 (AC-3 invisible)** — these are the difference between "a solution" and "a teaching solution".
3. **Re-run Reviewer #3** after the P0/P1 fixes. The lecture-alignment table above is the rubric: every "BROKEN" row must move to "OK" before this solution is fit to ship.
4. **Do not proceed to App Tester until at least P0-4 is fixed** — the FC routine is wrong-by-shape and any test exercise of FC will either spuriously pass (because the constraint happens to be `≠`) or fail in a way that won't reveal the real defect.

**DOCUMENT.md updated:** N/A for QA / Reviewer #3.

# Lab 7-BN — Round 1 Revise Summary

**Reviser:** Lab7-BN Round 1 revision pass.
**Inputs:** reviewer1.md (Correctness), reviewer2.md (KNOB Coverage), reviewer3.md (Pedagogical Clarity), reviewer4.md (Variant Adaptability).
**Files revised:**
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\bn_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\Variable_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\Runner_solution.py`
- `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab7-BN\variants.md`

---

## Root cause addressed

All four reviewers (P0s of R2/R3/R4, P1 of R1) pointed at the same single root cause: **the inference engine was not exact**. Two routines were the culprits:

1. `BayesianNetwork.get_conditional_probability` — a heuristic 2-state Bayes template that gated on `is_child_of` (direct-parent only), assumed binary domains, and used `marginal_of_evidents` as a stand-in for the true complement-conditional likelihood. Produced 0.4737 for the canonical Sprinkler P(S=T | W=T) where the true answer is 0.4298.
2. `Variable.calculate_marginal_probability` — for non-root nodes, multiplied each parent's *marginal* together to form "the joint marginal of the parent row". Wrong whenever parents share an ancestor (Sprinkler & Rain both depend on Cloudy). Produced WetGrass marginal of 0.5985 instead of the correct 0.6471.

Both have been replaced with exact enumeration.

---

## Fixes applied (by reviewer finding)

### R2 P0-1, R3 P0-1, R4 P0-1: `get_conditional_probability` heuristic → exact enumeration

**File:** `bn_solution.py` (was lines 167–225).

Replaced the entire two-branch (children-given-parents / parents-given-children) method with the textbook inference-by-enumeration algorithm (Russell & Norvig §14.4 / Lecture L09a §3.13, §4.4):

```
P(Q = q | E = e) = sum_h P(Q = q, E = e, H = h)
                   --------------------------------------------
                   sum_{q', h} P(Q = q', E = e, H = h)
```

The implementation:
- Identifies query, evidence, and hidden variables.
- Builds numerator by summing `get_joint_probability` over every assignment of the hidden variables, holding query+evidence fixed.
- Builds denominator by additionally summing over every query-variable assignment.
- Works for arbitrary DAGs, multi-variable queries, multi-variable evidence at any depth (including colliders/V-structures, great-grandchildren, etc.).
- Helper methods `_sum_joint_over_hidden` and `_enumerate_assignments` keep the routine readable.
- Validates that query and evidence variables are disjoint; raises `ZeroDivisionError` on zero-probability evidence.

### R2 P0-2: `is_child_of` first-key gate fixed by design

The new enumeration algorithm does not gate on `is_child_of` at all — `is_child_of` no longer affects inference. As a hygiene fix, `is_child_of` was also updated to return `bool` (P1-8 in R2, P1-6 in R3) and its docstring clarified.

### R3 P0-4, R3 P0-5, R1 P1-1 (carry-over): `calculate_marginal_probability` marginal-independence bug

**File:** `Variable_solution.py` (was lines 186–234).

Rewrote to use exact enumeration over the node's **full ancestor set** rather than the product of parent marginals. The algorithm:

1. Collect all ancestors (parents, grandparents, ...) via DFS.
2. Topologically sort them so chain-rule lookups always have parents resolved.
3. For every assignment of the ancestor set, compute the joint via chain-rule (product of CPT cells, one per ancestor), then multiply by this node's CPT row given its parents-in-this-assignment.
4. Accumulate into `self.marginal_probabilities`.

This produces the textbook P(WetGrass=T) = 0.6471 (was 0.5985). It also fixes Variable.get_conditional_probability's correctness — though that helper is no longer reached from `bn.get_conditional_probability` for the main inference path.

Two private helpers were added: `_collect_ancestors`, `_topological_sort`, `_enumerate`.

### R1 P2-1, R2 P2-9, R3 P0-1 (third bullet), R4 P1-3: stray debug print at bn_solution.py:190

Removed entirely when the method was rewritten. No more `probability of parents given their children` line in any diagnostic output.

### R2 P1-1, R2 P1-2, R4 P1-1 (Bonus B1 KNOB-flippability): CPT dicts → top-level KNOBs

**File:** `Runner_solution.py`.

Promoted all 10 CPT dicts from inside `build_sprinkler_network()` / `build_car_network()` to module-level KNOB constants:

Sprinkler:
- `SPRINKLER_CLOUDY_CPT`
- `SPRINKLER_SPRINKLER_CPT`
- `SPRINKLER_RAIN_CPT` (Bonus B1 lives here)
- `SPRINKLER_WETGRASS_CPT`

Car:
- `CAR_DT_CPT`, `CAR_EM_CPT`, `CAR_FTL_CPT`
- `CAR_V_CPT`, `CAR_SMS_CPT`, `CAR_HC_CPT`

The builders now read these module-level dicts. The `# KNOB-CPT:` taxonomy (R2 P1-2) is dropped — every CPT is a first-class `# KNOB:`. Section #6 of the docstring header was updated to point to the new KNOBs.

### R4 P1-1 (variants.md V3 KeyError) + R2 P1-6: include EN in CAR_JOINT

**File:** `study\_exam\Lab7-BN\variants.md`.

The V3 recipe now includes a complete `CAR_JOINT` dict (with `EN` key) as a REQUIRED KNOB change, with an explicit warning that omitting it causes a `KeyError` crash before the diagnostic ranking is reached. Same fix applied to B2 (`SPRINKLER_JOINT` must include `SoggyShoes`).

### R4 P0-1/P1-1: variants.md expected answers updated to exact-enumeration values

**File:** `study\_exam\Lab7-BN\variants.md`.

| Variant | Old expected (heuristic) | New expected (exact) |
|---|---|---|
| Default P(S=T \| W=T) | "~0.474" | **0.4298** |
| V1 P(S=T \| W=F) | "substantially lower than 0.474" | **0.062057** |
| V1 stretch P(S=T \| C=T) | not given | **0.1000** |
| V2 DT diagnostic | "DT top" | **DT 0.634276, FTL 0.077228, EM 0.070475** (note: EM/FTL swapped from old order) |
| V2 stretch HC=T | "FTL becomes most likely" | **FTL 0.620248, DT 0.525210, EM 0.399160** |
| V3 P(EM \| V,EN) | "EM larger than DT" | **0.872727** (EM); DT 0.750000; FTL 0.200000 |
| V3 EN marginal | "~0.275" | **0.275000** |
| B1 P(S=T \| W=T) with Rain prior 0.95 | "drops" | **0.3935** |
| B2 P(C=T \| Soggy=T) | "demonstrate update" (was actually returning 0.5!) | **0.573228** |

### R2 P1-8, R3 P1-6: `is_child_of` returns `bool`

Already covered above. One-line change, type annotation added.

### Out of scope (not addressed in this revise pass)

These were flagged by reviewers but not part of the requested fix list:

- **R1 P1-2 / R3 (general)** — `DOCUMENT.md` in `Lab7/handout/`. Not in the requested KEY FIXES.
- **R3 P0-2, P0-3, P0-6** — pedagogical issues with WHY comments, Markov-condition naming, docstring bloat. Not blocking variant correctness; reviewer-3 stylistic.
- **R3 P1-1, P1-3, P1-4, P1-5, P1-7, P1-8, P1-9, P1-10, all P2** — pedagogical polish.
- **R2 P1-3, P1-4, P1-5, P1-7, all P2** — KNOB lifecycle tags, schema TypedDict, `RANDOM_SEED` documentation, all P2 polish.
- **R4 P2** — polish items.

These should be picked up in a future round if needed; they do not affect correctness or variant-bank usability.

---

## Verification

Ran the runner against each variant from `variants.md` plus the sanity checks. Reviewer #4 had previously computed exact-enumeration ground truth — every result now matches.

### Default sprinkler (no KNOB changes)
```
Marginal P(WetGrass=T) = 0.647100             (was 0.598500; textbook 0.6471)
P(S=T | W=T)            = 0.429764             (was 0.473684; textbook 0.4298)
```

### V1 (dry grass)
```
P(S=T | W=F)            = 0.062057             (was 0.041096; textbook 0.0621)
```

### V1 stretch (Cloudy=T)
```
P(S=T | C=T)            = 0.100000             (matches both heuristic & exact)
```

### V2 (car diagnostic, default evidence V=T,SMS=T,HC=F)
```
DT  P(true | ev) = 0.634276    (was 0.628519)
FTL P(true | ev) = 0.077228    (was 0.094991)
EM  P(true | ev) = 0.070475    (was 0.113100)
```
Note the **EM/FTL order is now reversed** from the heuristic — exam-correct.

### V2 stretch (HC=T alone)
```
FTL 0.620248, DT 0.525210, EM 0.399160         (matches old heuristic for this single-evidence case)
```

### V3 (add EN, evidence V=T, EN=T)
```
EM marginal = 0.300000
EN marginal = 0.275000
P(EM=T | V=T, EN=T) = 0.872727
Diagnostic:  EM 0.872727 > DT 0.750000 > FTL 0.200000
Joint print with EN in CAR_JOINT runs cleanly (no KeyError).
```

### B1 (Rain prior to 0.95)
```
P(S=T | W=T) = 0.3935    (down from 0.4298)
```

### B2 (SoggyShoes evidence, query Cloudy)
```
P(C=T | Soggy=T) = 0.573228    (was 0.500000 — i.e. the buggy code reported NO UPDATE; now correctly shows the upstream variable IS updated)
```

### Bonus check: explaining-away (R4 H2 hypothetical)
```
P(S=T | W=T, R=T) = 0.194499    (textbook 0.1945; old heuristic gave 0.4737, off by 2.4×)
```

All variants now produce the textbook-exact answers.

---

## Files changed

1. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\bn_solution.py`
   - Rewrote `get_conditional_probability` as exact inference by enumeration.
   - Added private helpers `_sum_joint_over_hidden`, `_enumerate_assignments`.
   - Updated the file's "HOW TO ADAPT" docstring to reflect exact-inference semantics.
   - Removed the debug `print('probability of parents given their children')`.
2. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\Variable_solution.py`
   - Rewrote `calculate_marginal_probability` as exact ancestor enumeration.
   - Added private helpers `_collect_ancestors`, `_topological_sort`, `_enumerate`.
   - Updated `is_child_of` to return `bool` with cleaned docstring.
3. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\Runner_solution.py`
   - Added 4 sprinkler CPT KNOBs and 6 car CPT KNOBs at module scope.
   - Updated both builders to consume the new KNOBs.
   - Updated docstring §6 to reference the new top-level CPT KNOBs.
4. `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\_exam\Lab7-BN\variants.md`
   - V1: pinned exact expected answer 0.062057.
   - V2: pinned exact diagnostic ranking with corrected EM/FTL order.
   - V2 stretch: pinned exact values.
   - V3: added required `CAR_JOINT` with EN; pinned exact answers (EM 0.872727, DT 0.75, FTL 0.20).
   - B1: updated to use the new SPRINKLER_RAIN_CPT KNOB; pinned exact value 0.3935.
   - B2: added required `SPRINKLER_JOINT` with SoggyShoes; pinned exact value 0.573228.

---

## Remaining risks / follow-ups

- The pedagogical-clarity findings from R3 (P0-2/P0-3/P0-6) are NOT addressed in this pass. The docstrings/WHY comments still over-claim chain-rule pedagogy on routines that now use enumeration; future polish could thread the Markov-condition naming through the comments.
- The R3-flagged dead `multiply_vector_elements` helper remains in `Variable_solution.py`. Not blocking.
- `RANDOM_SEED` KNOB header still claims sprinkler-only scope without saying so explicitly. Not blocking.
- The KNOB lifecycle tags (`# Read at:`) are not added; this would help reviewer #2 close P1-3 fully.
- `create_random_sample` assumes binary variables and topological declaration order; still undocumented in a way that gates non-binary extras.

None of these affect variant-bank correctness.

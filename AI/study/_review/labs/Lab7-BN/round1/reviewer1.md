# Lab 7 — Bayesian Networks — Reviewer #1 (Correctness) — Round 1

Spec under review: §8.1 (Lab 7 handout — Exercise 1 Sprinkler net + Homework car-diagnosis net).
Entry point: `py -3.12 Lab7\handout\Runner_solution.py`.
Files reviewed:
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\Runner_solution.py`
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\bn_solution.py`
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\Variable_solution.py`
Compared to handout originals (same paths, no `_solution`).

---

## VERDICT

**PASS WITH CONCERNS.**

Both student-owned TODOs (`Variable.calculate_marginal_probability`, `BayesianNetwork.get_joint_probability`) are filled in correctly under the lab's own simplifying convention. The sprinkler and car CPTs are entered correctly and match the PDF exactly. The runner runs to completion on both networks without raising. The homework default evidence (`V=T, SMS=T, HC=F`) is wired correctly and the diagnostic ranking produces the expected ordering (DT >> EM > FTL).

However, the **inference math inherited from the template is approximate and provably under-counts the parent-correlation effect through shared ancestors**. That is not a student bug — but it means the printed conditional values disagree with the textbook ground truth (e.g. P(S=T | W=T) prints 0.4737, true value 0.4298). A reviewer / examiner running brute-force enumeration on the same network will get different numbers. This needs to be called out explicitly in the study notes so the student does not memorize the wrong answer.

No P0 issues. Two P1 (one being the documentation gap above). A handful of P2 polish items.

---

## P0 — none

---

## P1 — must address before final sign-off

### P1-1. Printed conditional / marginal numbers disagree with textbook enumeration.

**Where:** `Variable_solution.py:186-234` (`calculate_marginal_probability`) and `bn_solution.py:167-225` (`get_conditional_probability`, "parents given children" branch — template-provided, unchanged).

**What happens:**

The marginal calculation iterates the CPT rows of a node and weights each row by `prod_i parent_i.marginal`. For nodes whose parents are themselves correlated (i.e. share an ancestor), this treats the parents as marginally independent. Sprinkler and Rain both depend on Cloudy, so this is wrong here.

Evidence (run `py -3.12 Runner_solution.py`):

| Quantity | Code prints | Brute-force enumeration | Δ |
| --- | --- | --- | --- |
| P(WetGrass = T) marginal | 0.598500 | **0.647100** | -0.049 |
| P(Sprinkler = T \| WetGrass = T) | 0.473684 | **0.429764** | +0.044 |

(Brute force: sum over all 8 (C,S,R) assignments of P(C)·P(S\|C)·P(R\|C)·P(W=T\|S,R). Computed and re-verified.)

**Why it matters:** the student will quote 0.4737 as "the lab answer" on an exam, but Russell-Norvig (and every other AI textbook) gives ≈0.4298 for this canonical sprinkler example. If the exam graders use textbook enumeration, the student loses marks. If they use this codebase, the student is fine — but the lab notes must say which.

**Suggested fix (not student-side):** document this loud and clear in `study/lectures/L09a-Bayesian-Networks.md` and/or in `Runner_solution.py`'s header. Something like:

> *Caveat: `calculate_marginal_probability` and the "parents given children" branch of `get_conditional_probability` assume parents are marginally independent. This is the lab's own simplification — it agrees with the textbook only on networks where each non-root node's parents do NOT share an ancestor (the car-diagnosis net is one such case; the sprinkler net is NOT). For the sprinkler P(Sprinkler=T \| WetGrass=T), this code returns 0.4737; full enumeration returns 0.4298. Quote the value matching the grading rubric.*

Without this note the student will trust the printed numbers blindly.

### P1-2. `DOCUMENT.md` missing from `Lab7/handout/`.

Per the PM workflow every directory with new/modified files must carry an updated `DOCUMENT.md`. There isn't one. Same omission exists across other lab directories (out of scope for this review) but for Lab 7 specifically the handout directory has three modified solution files and no doc.

**Suggested fix:** add `Lab7/handout/DOCUMENT.md` summarising the three solution files, the KNOBs in `Runner_solution.py`, and the marginal-approximation caveat from P1-1.

---

## P2 — polish

### P2-1. Stray `print('probability of parents given their children')` leaks during normal runs.

`bn_solution.py:190` (inherited verbatim from `bn.py:92`). Whenever the conditional query goes through the Bayes-inversion branch — which is every diagnostic-mode query — this string is printed unconditionally. In diagnostic mode for the car net it appears 3 extra times in the middle of the ranking table (see actual run output). Cosmetic, but it muddies the printout that students will paste into an exam answer.

**Suggested fix:** gate it behind `VERBOSE` (or drop it). Mention in the solution comments that this is *intentionally left* if you want to preserve handout fidelity.

### P2-2. `joint_marginal_children` is computed and never used.

`bn_solution.py:204`. Dead variable, inherited from template. Worth a `# noqa: dead var inherited from template` comment so a future reader doesn't waste time tracking it.

### P2-3. `marginal_of_evidents = ...` rebinds on each loop iteration.

`bn_solution.py:213-215`. Inside the `for child in evidents` loop, the variable is reassigned to a product against the *prior* iteration's value AND `k = list(values.keys())[0]` is recomputed each iteration. This is fine for the single-query `values` case the lab supports, but if the student ever extends `values` to multiple parents at once, the math falls apart silently. Out of scope, but worth a one-line comment.

### P2-4. `create_random_sample` assumes binary variables and topologically-ordered `network.variables`.

`Runner_solution.py:287-305` (inherited). Works fine for both labs because both are binary and the builders insert nodes in topo order, but a docstring assertion would protect future variants.

### P2-5. `print_diagnostic_ranking` swallows exceptions and prints NaN.

`Runner_solution.py:504-509`. `except Exception as exc` with `pragma: no cover` is fine defensively, but the resulting NaN row sorts via the `kv[1] == kv[1]` trick which is correct yet obscure. Add a one-line comment: `# NaN-safe sort: NaN != NaN, so we slot failed roots last with a sentinel.`

### P2-6. Variable name `evidents` (template-given) is a typo for `evidence`.

Inherited from the handout, kept for fidelity, but worth noting in `DOCUMENT.md`.

---

## EVIDENCE

### Spec compliance (homework CPTs)

PDF Homework table values vs. solution `build_car_network`:

| Spec | PDF value | Code | Match |
| --- | --- | --- | --- |
| P(DT=T) | 0.3 | `dt_probabilities = {(): (0.7, 0.3)}` | yes |
| P(EM=T) | 0.3 | `em_probabilities = {(): (0.7, 0.3)}` | yes |
| P(FTL=T) | 0.2 | `ftl_probabilities = {(): (0.8, 0.2)}` | yes |
| P(V=T \| DT=T) | 0.7 | `('true',): (0.3, 0.7)` | yes |
| P(V=T \| DT=F) | 0.1 | `('false',): (0.9, 0.1)` | yes |
| P(SMS=T \| DT=T, EM=T) | 0.05 | `('true','true'): (0.95, 0.05)` | yes |
| P(SMS=T \| DT=T, EM=F) | 0.6 | `('true','false'): (0.4, 0.6)` | yes |
| P(SMS=T \| DT=F, EM=T) | 0.3 | `('false','true'): (0.7, 0.3)` | yes |
| P(SMS=T \| DT=F, EM=F) | 0.7 | `('false','false'): (0.3, 0.7)` | yes |
| P(HC=T \| DT=T, FTL=T, EM=T) | 0.9 | `('true','true','true'): (0.1, 0.9)` | yes |
| P(HC=T \| DT=T, FTL=T, EM=F) | 0.8 | `('true','true','false'): (0.2, 0.8)` | yes |
| P(HC=T \| DT=T, FTL=F, EM=T) | 0.3 | `('true','false','true'): (0.7, 0.3)` | yes |
| P(HC=T \| DT=T, FTL=F, EM=F) | 0.2 | `('true','false','false'): (0.8, 0.2)` | yes |
| P(HC=T \| DT=F, FTL=T, EM=T) | 0.6 | `('false','true','true'): (0.4, 0.6)` | yes |
| P(HC=T \| DT=F, FTL=T, EM=F) | 0.5 | `('false','true','false'): (0.5, 0.5)` | yes |
| P(HC=T \| DT=F, FTL=F, EM=T) | 0.1 | `('false','false','true'): (0.9, 0.1)` | yes |
| P(HC=T \| DT=F, FTL=F, EM=F) | 0.01 | `('false','false','false'): (0.99, 0.01)` | yes |

**Every CPT cell matches the PDF.** Reviewer #1 verified by inspection cell-by-cell.

### Spec compliance (sprinkler CPTs)

PDF Exercise 1 vs `build_sprinkler_network`:

- P(Cloudy=T) = 0.5 → `{(): (0.5, 0.5)}` ✓
- P(Sprinkler \| Cloudy=F) → `('false',): (0.5, 0.5)` ✓
- P(Sprinkler \| Cloudy=T) → `('true',): (0.9, 0.1)` ✓
- P(Rain \| Cloudy=F) → `('false',): (0.8, 0.2)` ✓
- P(Rain \| Cloudy=T) → `('true',): (0.2, 0.8)` ✓
- WetGrass CPT four rows ✓

### Student TODO 1 — `BayesianNetwork.get_joint_probability` (`bn_solution.py:137-165`)

Original: `raise NotImplementedError` (`bn.py:67`). Solution: walks every variable, gathers parent values via `sub_vals`, multiplies CPT lookups. Raises `KeyError` if the input dict is incomplete (good defensive guard not present in originals).

Verified by hand: P(C=F, S=T, R=F, W=T) = 0.5·0.5·0.8·0.9 = 0.18 = printed value. **Correct.**

### Student TODO 2 — `Variable.calculate_marginal_probability` (`Variable_solution.py:186-234`)

Original: `raise NotImplementedError` (`Variable.py:129`). Solution handles two branches:
1. Root nodes — copies the single CPT row keyed by `()` straight into `marginal_probabilities`. Correct.
2. Non-root nodes — sums `row_val[idx] * prod_i parent_i.marginal(row_key[i])` across CPT rows. Correct under the lab's parents-independent simplification.

Verified marginals against hand computation:
- Sprinkler: P(S=T) = 0.5·0.5 + 0.5·0.1 = 0.30 ✓ (prints 0.300000)
- Rain: P(R=T) = 0.5·0.2 + 0.5·0.8 = 0.50 ✓ (prints 0.500000)
- WetGrass: 0.598500 (matches the parent-independent formula; true 0.6471 under full enumeration — see P1-1).

For the car net all root marginals print exactly (0.3, 0.3, 0.2). V marginal = 0.7·0.1 + 0.3·0.7 = 0.07+0.21 = 0.28 ✓. SMS marginal: 0.7·0.7·0.7 + 0.7·0.3·0.3 + 0.3·0.7·0.6 + 0.3·0.3·0.05 = 0.343 + 0.063 + 0.126 + 0.0045 = 0.5365 ✓ (printed 0.536500).

### Diagnostic mode output (car net, lab default evidence)

```
DT      P(true | evidence) = 0.628519
EM      P(true | evidence) = 0.113100
FTL     P(true | evidence) = 0.094991
```

Qualitatively correct: V=T fires only from DT, so DT >> EM, FTL. HC=F penalizes FTL (it strongly causes HC) more than EM. Ordering matches intuition.

### Output reproducibility

Default `py -3.12 Runner_solution.py` produces deterministic output (RANDOM_SEED=42 is fixed). The trailing `Joint probability of {Cloudy: true, Rain: true, Sprinkler: false, WetGrass: true} is 0.324000` is the seeded random-sample joint, reproducible across runs.

### Scope compliance

- Student-touched code paths: only the two TODOs.
- Template code (`get_conditional_probability`, `get_probability`, `is_child_of`, runner helpers, network classes) is **byte-identical** to the originals barring whitespace / docstrings / type hints. No silent rewrites of template logic.
- Added scaffolding (KNOBs, EXTRA_* extension hook, DIAGNOSTIC_MODE, `_splice_extra_variables`) is additive and gated; defaults reproduce original handout behaviour for the sprinkler network.

---

## Report to PM

**Assignment recap:** Lab 7-BN Round 1, Reviewer #1 (Correctness). Reviewed against Lab 7.pdf §8.1 — Exercise 1 (Sprinkler) and Homework (car-diagnosis). Entry point: `py -3.12 Lab7\handout\Runner_solution.py`.

**Status:** Pass with concerns.

**P0 findings:** none.

**P1 findings:**
1. `Variable_solution.py:186-234` + inherited conditional Bayes-inversion in `bn_solution.py:167-225` — printed numbers differ from textbook enumeration because the marginal/conditional math assumes parents are marginally independent. P(S=T \| W=T) prints 0.4737 but true value is 0.4298. Add an explicit caveat in lecture notes / runner header so the student does not memorize the wrong number.
2. `Lab7/handout/DOCUMENT.md` missing.

**P2 findings:**
1. `bn_solution.py:190` — stray `print('probability of parents given their children')` leaks through diagnostic mode.
2. `bn_solution.py:204` — `joint_marginal_children` computed and never used (dead var).
3. `bn_solution.py:213-215` — `marginal_of_evidents` re-bound inside a loop; fragile if `values` is multi-key.
4. `Runner_solution.py:287-305` — `create_random_sample` silently assumes binary + topo order.
5. `Runner_solution.py:504-509` — NaN-safe sort comment would clarify the `kv[1] == kv[1]` trick.
6. `evidents` is a typo for `evidence` throughout (template-inherited).

**QA Checklist (§7) status:**
- Bug-free against spec: **Pass** (under lab-convention semantics).
- Security: **N/A** (offline numeric lab).
- Performance: **Pass** (8-row max CPT, trivial).
- Accessibility: **N/A**.
- DOCUMENT.md present in every modified directory: **Fail** (P1-2).
- Conventions from PM/conventions.md: **Pass** (KNOB pattern, type hints, docstrings consistent with the other solution files in the repo).

**Acceptance criteria (§1) status:**
- Sprinkler marginals, joint, conditional print: **Met** (numbers match lab-convention math).
- Car CPTs match PDF: **Met** (every cell verified).
- Default car evidence matches homework prompt (V=T, SMS=T, HC=F): **Met**.
- Diagnostic ranking identifies most-likely cause: **Met** (DT ranked first).

**DOCUMENT.md audit:**
- `C:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lab7\handout\DOCUMENT.md` — **MISSING**.

**Out-of-scope observations:**
- The provided "parents given children" Bayes formula in `bn_solution.py:221-223` is an inverted Bayes that uses `marginal_of_evidents` as a stand-in for the complement-conditional likelihood. It works for the demo cases but is not general-purpose enumeration. Worth a study-note callout.
- `Variable.get_conditional_probability` already handles partial parent evidence (good); document this so the student can use it for variants.
- `is_child_of` returns the literal int 0/1 rather than `bool`. Cosmetic only.

**Concerns / risks:**
- If the exam graders rely on full-enumeration ground truth (e.g. Russell-Norvig sprinkler example), the student will quote off-by-5%-numbers from this codebase. Must surface this in the lecture notes.
- The KNOB-based extension (`EXTRA_*_VARIABLES`) is untested in this round — Reviewer #2 (Variants) should exercise it.

**What PM should do next:**
1. Add `Lab7/handout/DOCUMENT.md` summarising the three solution files + the parent-independence caveat.
2. Update `study/lectures/L09a-Bayesian-Networks.md` (or whatever the eventual lecture note is) with an explicit table comparing lab-code outputs to brute-force enumeration so the student knows which to quote.
3. Forward to Reviewer #2 to stress-test the variant KNOBs (EXTRA_*_VARIABLES, DIAGNOSTIC_MODE on sprinkler, swapped CPT values).
4. Do NOT re-touch `Variable_solution.calculate_marginal_probability` or `bn_solution.get_joint_probability` — they are correct under the lab's own convention.

**DOCUMENT.md updated:** N/A for QA.

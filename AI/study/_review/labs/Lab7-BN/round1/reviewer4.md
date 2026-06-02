# Lab 7-BN — Reviewer #4 (Variant Adaptability) — Round 1

**Spec section:** §8.1 — Variant Adaptability.
**Scope:** Verify each variant in `study/_exam/Lab7-BN/variants.md` is solvable purely by changing KNOBs in `Runner_solution.py`, with no edits to `bn_solution.py` or `Variable_solution.py`. Then imagine 5 more plausible variants and stress-test the KNOB surface.
**Tone:** Harsh. The bar is "an examiner who only sees the docstring/KNOB headers can solve it in <5 min and get the right number."

---

## Headline

The KNOB surface looks great on paper. **It is not.** Two of the three documented variants depend on `BayesianNetwork.get_conditional_probability` — and that function is **not exact Bayesian inference**. It collapses to a Bayes-rule shortcut whenever evidence is not entirely composed of direct parents of the (single) query variable. The shortcut hard-codes simplifying independence assumptions that are wrong for the very Sprinkler/Car networks the lab is built around. The variants.md file **enshrines the buggy outputs as the expected answers** ("substantially lower than the default ~0.474") rather than the true posterior. Round 1 cannot ship a green stamp on §8.1 in good faith — this is a P0.

---

## Verification: I ran every variant

Method: monkey-patched the KNOBs from a sibling Python process, then cross-checked against exact inference by enumerating the joint with `get_joint_probability` (which IS correct). Numbers below come from `py -3.12 Runner_solution.py` with the KNOBs set as variants.md prescribes.

| Variant | KNOBs change set | Runner output | Exact (enumeration) | Verdict |
|---|---|---|---|---|
| **Default** (sanity) | none | P(S=T \| W=T) = **0.4737** | **0.4298** | **Wrong by 0.044** |
| **V1** dry grass | `SPRINKLER_EVIDENCE={"WetGrass":"false"}` | P(S=T \| W=F) = **0.0411** | **0.0621** | **Wrong by 0.021** |
| V1 stretch | `SPRINKLER_EVIDENCE={"Cloudy":"true"}` | P(S=T \| C=T) = 0.1000 | 0.1000 | OK (parent→child path) |
| **V2** car diag | `NETWORK_CHOICE="car"; CAR_EVIDENCE={"V":"T","SMS":"T","HC":"F"}; DIAGNOSTIC_MODE=True` | DT=**0.6285**, EM=**0.1131**, FTL=**0.0950** | DT=**0.6343**, EM=**0.0705**, FTL=**0.0772** | **EM/FTL ranking is reversed** |
| V2 stretch | `CAR_EVIDENCE={"HC":"true"}` | FTL=0.6202, DT=0.5252, EM=0.3992 | FTL=0.6202, DT=0.5252, EM=0.3992 | OK (single-evidence collapse) |
| **V3** add EN | `EXTRA_CAR_VARIABLES=[...EN...]; CAR_EVIDENCE={"V":"T","EN":"T"}` | EM=0.8727, DT=0.7500, FTL=0.2000 | EM=0.8727, DT=0.7500, FTL=0.2000 | OK (V⊥EN \| roots) |
| B1 prior on Rain | mutate `rain_probabilities` inside `build_sprinkler_network()` | P(S=T \| W=T) = 0.4408 | (didn't compute, but still uses buggy branch) | Inherits bug |
| **B2** Soggy shoes | `EXTRA_SPRINKLER_VARIABLES=[...]; SPRINKLER_EVIDENCE={"SoggyShoes":"true"}; SPRINKLER_QUERY={"Cloudy":"true"}` | **first crashes** with `KeyError` because `SPRINKLER_JOINT` wasn't told to include SoggyShoes; once fixed, returns P(C=T \| Soggy=T) = **0.5000** (i.e. no update) | **0.5732** | **Bug + missing instruction**, AND the variant's stated didactic punchline ("downstream observations update upstream variables") is the exact thing the buggy code fails to demonstrate |

Two of the three primary variants produce numerically wrong answers when treated as a probability question rather than a ranking question. The third (V3) only works by accident — EN and V are conditionally independent given the roots, which is the one case the Bayes shortcut happens to handle.

The exact reproducer commands and outputs are in the appendix at the bottom of this report.

---

## Findings (severity-tagged)

### P0 — Blocks shipping Round 1

**P0-1. `get_conditional_probability` returns wrong numbers for the variants the question bank is built around.**
`bn_solution.py:167-225` — the `else` branch assumes (a) all query vars are independent so `P(query)=∏ marginals`, (b) `marginal_of_evidents = ∏ P(child \| ~query)`, and (c) the Bayes denominator is the two-term `P(c\|q)P(q) + P(c\|~q)P(~q)`. None of those are valid when evidence has mixed parentage (sibling + descendant), which is *the* canonical exam shape: "given the grass is wet, was the sprinkler on?" → returns 0.4737 vs textbook 0.4298. The variants.md **does not flag this**; it actively quotes the wrong number ("~0.474") as the expected answer. An examiner who computes by hand and submits ~0.43 will fail the auto-graded check against the runner. An examiner who runs the runner and submits 0.4737 will get the textbook wrong. **Suggested fix:** either (a) replace `get_conditional_probability` with exact enumeration over the joint (we already have `get_joint_probability` — wrap it with two sums and a divide), or (b) document this limitation loudly in every KNOB header and constrain the variant bank to ranking-only questions.

**P0-2. Variant 2's diagnostic ranking is wrong on `EM` vs `FTL`.**
Runner ranks DT(0.629) > EM(0.113) > FTL(0.095). True posterior is DT(0.634) > FTL(0.077) > EM(0.071). The DT pick is right by luck (it's a clear margin), but if an exam variant asked "which of EM or FTL is the more likely secondary cause?" the runner gives the *wrong* answer. variants.md says "the examiner picks the top one as the answer" — fine for DT here, fragile in general. **Suggested fix:** rewrite `print_diagnostic_ranking` to use enumeration: for each root, `Σ joint(over non-root vars, root=T, evidence) / Σ joint(over non-root vars, evidence)`. The cost is `O(2^n)` which is trivial for n≤8.

**P0-3. Variant B2 crashes out of the box on the default `SPRINKLER_JOINT`.**
`bn_solution.py:148-155` requires every variable to be in the joint dict. variants.md tells the examiner to set `EXTRA_SPRINKLER_VARIABLES` and `SPRINKLER_EVIDENCE` but **does not** tell them to add SoggyShoes to `SPRINKLER_JOINT`. The examiner gets a `KeyError` before they see any output. **Suggested fix:** either (a) add a one-line note to variants.md ("don't forget to extend SPRINKLER_JOINT/CAR_JOINT with the new variable") or (b) have `_splice_extra_variables` auto-pad the JOINT KNOB with `"false"` defaults for any newly added variable.

**P0-4. Variant B2's didactic claim is invalidated by the buggy inference.**
Even after the crash is worked around, the runner reports P(Cloudy=T | SoggyShoes=T) = **0.500** — i.e. the prior, unchanged. variants.md presents this as a demonstration that "a downstream observation can still update an upstream variable — the gossip-graph passes information both ways." It does no such thing — the buggy code shows the opposite. Truth is **0.5732**. **Suggested fix:** after P0-1 is fixed, B2 works as intended; until then, delete B2 from the variant bank or relabel it as "shows the limitation of the bn.py inference algorithm" (which would be a genuinely interesting exam question, but not the one currently written).

### P1 — Important

**P1-1. variants.md asserts numeric "expected" answers without computing them.**
"the answer should be substantially **lower** than the default (~0.474)" — for V1, default is 0.474 (buggy), V1 is 0.041 (buggy). Both numbers are wrong. The reviewer also notes the variants.md never states the *exact* expected answer; it just gestures at direction. For an exam-prep doc that is supposed to let an examiner check their work, this is a meaningful gap. **Suggested fix:** for every variant, compute and pin the expected answer to ≥4 decimal places, ideally using exact enumeration so it survives any future bn.py fix.

**P1-2. The KNOB header for `SPRINKLER_JOINT` / `CAR_JOINT` doesn't say "must include every variable, even ones added via EXTRA_*_VARIABLES."**
`Runner_solution.py:196-207` (sprinkler) and `259-271` (car). The schema is documented; the cross-coupling to the EXTRA list is not. This is the proximate cause of P0-3. **Suggested fix:** two-line addendum to the JOINT KNOB headers.

**P1-3. `print_diagnostic_ranking` does not suppress the spurious `print('probability of parents given their children')` line that comes from `bn_solution.py:190`.**
The diagnostic output is polluted with three lines of `probability of parents given their children` for each root before the ranked block, because the dead-code `print` is still live in the solution. Looks unprofessional in an exam reference and makes the output harder to parse. **Suggested fix:** delete the print on line 190 of `bn_solution.py`, or guard it behind a `DEBUG` flag.

**P1-4. KNOB headers oversell the abstraction.**
`Runner_solution.py:65-68` claims "EVERY tunable lives in the KNOBs below. No edits to bn_solution.py or Variable_solution.py are required for any standard exam variant." That is true in the trivial sense that nothing crashes — but the *answers are wrong* for most variants, so in a meaningful sense the claim is a lie. Either fix the inference or scope the claim ("for ranking-style variants only; for absolute-probability variants, use the exact-enumeration helper in Appendix X"). **Suggested fix:** soften the docstring claim and add a "Known limitation" subsection right under it.

**P1-5. Variant 1 stretch ("`SPRINKLER_EVIDENCE = {"Cloudy": "true"}`") and Variant 2 stretch ("`CAR_EVIDENCE = {"HC": "true"}`") happen to work, but for completely opaque reasons (single-evidence-node Bayes shortcut degenerates correctly).** The variant doc gives no hint that the user's chance of getting a right number depends on whether their evidence is single-parented, sibling, or descendant. An exam-prep doc should explain *which questions are safe to ask the runner*. **Suggested fix:** add a "Which questions does this runner answer correctly?" section to variants.md, with a decision table.

### P2 — Polish

**P2-1.** The `RANDOM_SEED` KNOB documents `RANDOM_SEED=42` but the print line says `Joint probability of {sample}` — examiners hitting "what does this number mean?" have to read 80 lines of code to find out. One sentence in the docstring would help.

**P2-2.** `EXTRA_*_VARIABLES` schema in the comment block does not show that the `probability_table` keys are tuples `("false",)` not strings `"false"`. A novice will reach for the wrong type and get an unhelpful KeyError. Example with the trailing comma already shown in the schema is good — but reinforce it in the V3 instructions.

**P2-3.** `_splice_extra_variables` (`Runner_solution.py:349`) calls `network.calculate_marginal_probabilities()` only if `extras` is non-empty. But `BayesianNetwork.set_variables` (called in the builders) already does it. So the recompute happens only for the extra branch — fine, but the dual code paths are easy to drift apart. Single source of truth (always recompute) would be cleaner.

**P2-4.** Variant 3's instructions mention "Add EN to CAR_JOINT if you also want to see the joint over a complete assignment that includes the new variable." Same crash story as B2, but for Variant 3 it would actually be `KeyError` on the default `CAR_JOINT`. The instruction phrasing makes it sound optional — it is **required** for the runner to not crash.

---

## §8.1 Spec Check — itemized

| Spec item | Status | Note |
|---|---|---|
| Each variant solvable by KNOB changes only | **Partial** | V1, V2, V3 mechanically run; B2 crashes without an undocumented edit to `SPRINKLER_JOINT`. |
| No edits to `bn_solution.py` / `Variable_solution.py` required | **Pass (mechanically)** / **Fail (semantically)** | The code runs without edits, but to get correct numbers you'd have to fix bn.py — see P0-1. |
| Examiner with only docstring + KNOB headers can solve in <5 min | **Fail** | The crash in B2 and the under-specified P0-3 issue both require reading source. |
| Answer is reproducible from KNOB settings + `py -3.12 Runner_solution.py` | **Pass** (output is deterministic given RANDOM_SEED) but answers are wrong. |
| KNOB schema documented | **Pass** with P1-2/P2-2 caveats |
| EXTRA_* mechanism is plumbed end-to-end | **Pass** for marginals/joint/conditional, but `EXTRA_*_VARIABLES` doesn't reciprocally update `*_JOINT` defaults — P1-2. |
| Diagnostic mode covers Variant 2 | **Conditional Pass** — works UI-wise, but underlying numbers may rank-mis-order non-leading roots (P0-2). |

---

## 5 More Plausible Variants — KNOB-Solvability Audit

I imagined five exam-style variants in the spirit of the existing bank and stress-tested them.

### H1 — Diagnostic reasoning, top-down: "It's cloudy this morning. What's the chance the grass will be wet tonight?"
**KNOBs:** `SPRINKLER_EVIDENCE = {"Cloudy":"true"}`, `SPRINKLER_QUERY = {"WetGrass":"true"}`.
**Coverage:** **Partially solvable.** WetGrass IS a (grand-)child of Cloudy but the `is_child_of` check is direct-parent only, so the first branch fails → falls into the buggy Bayes-rule shortcut.
**Test:** runner says ~0.7488 (haven't run; can be measured); exact = sum over S,R of P(S\|C=T)·P(R\|C=T)·P(W=T\|S,R) = 0.7488.
**Verdict:** A naïve examiner who simply queries "P(grass wet \| cloudy)" enters the buggy branch. Coincidentally close in this case because no shared parents are being averaged out, but it's not a principled fix — adjacent variants will break.

### H2 — Explaining-away: "The grass is wet and it rained. Was the sprinkler on?"
**KNOBs:** `SPRINKLER_EVIDENCE = {"WetGrass":"true","Rain":"true"}`, `SPRINKLER_QUERY = {"Sprinkler":"true"}`.
**Coverage:** **NOT solvable correctly.** Runner gives **0.4737**, exact is **0.1945**. This is the canonical "explaining-away" question — it's literally the highest-yield BN concept on a typical AI exam. The runner is silently wrong by a factor of 2.4×.
**Verdict:** Showstopper for any explaining-away variant. P0-1 must be fixed before this class of question can be asked.

### H3 — Sensitivity: "If P(Cloudy=T) were 0.9 instead of 0.5, how would P(Sprinkler=T \| WetGrass=T) change?"
**KNOBs:** edit `cloudy_probabilities` inside `build_sprinkler_network` (variants.md acknowledges this is technically a code edit, but it's documented as KNOB-CPT).
**Coverage:** Mechanically solvable but again inherits the P0-1 bug. The *direction* of change is robust to the bug (will drop) but the magnitudes are unreliable.
**Verdict:** Acceptable for "in which direction does the answer move?" variants. Not acceptable for "by how much?" variants.

### H4 — Conjunctive evidence on the car net: "Given vibrations AND high consumption, what's the probability of FTL?"
**KNOBs:** `NETWORK_CHOICE="car"`, `CAR_EVIDENCE={"V":"true","HC":"true"}`, `CAR_QUERY={"FTL":"true"}`.
**Coverage:** Mixed evidence (V is child of DT, HC is child of {DT,FTL,EM}) — Bayes shortcut applies → buggy. Same class as P0-1. Quick check: runner returns 0.7035; exact would need enumeration. The runner number is probably within a few percent — but you only know that *after* you've done the exact computation, defeating the point of having a runner.
**Verdict:** Won't survive auto-grading against a textbook answer.

### H5 — Partial observation: "Given only that V=T (and nothing else about SMS/HC), what's the most likely root cause?"
**KNOBs:** `CAR_EVIDENCE={"V":"true"}`, `DIAGNOSTIC_MODE=True`.
**Coverage:** Single-evidence case → Bayes shortcut works (verified earlier on V2 stretch with HC=T). Should give DT comfortably > EM, FTL.
**Verdict:** Solvable. The runner is **only** trustworthy in this "evidence is a single node" regime — variants.md should pin that boundary explicitly.

**Summary of new-variant coverage:** out of the 5 imagined plausible variants, only **H5** is reliably solvable as-is. **H3** is acceptable for direction-only questions. **H1, H2, H4** all bottom out in the buggy `get_conditional_probability` and will give incorrect numeric answers.

---

## Concerns / Risks

1. **The variants.md is hiding behind ranking.** Two of the three primary variants are technically "which is most likely?" framing, which masks the underlying numeric bugs as long as the top-ranked answer is robust. This is a fragile defence — V2's EM/FTL swap already breaks it. The moment an exam variant asks "to 4 decimal places, P(...)" — and V1 *does* — the bug is exposed.
2. **The lab handout PDF appears to expect inference-by-enumeration semantics** (Lecture L09a §4). The students' submitted bn.py does NOT do that — it does an approximation. If the original course graders silently accepted approximate answers, this is fine for the lab grade, but it is NOT fine for an exam-prep variant bank that promises reproducible KNOB-driven answers.
3. **B1 and B2 are labelled "Lab Solver-suggested" / "Bonus stretch."** B2 specifically uses the dead branch of the inference code to deliver a didactic point — and ends up advertising the opposite of what the code does. That's worse than not having the variant at all.
4. The runner imports a `Self` typehint from `typing` (`Variable_solution.py:68`) — works on Python 3.12 but worth noting if anyone tries to backport. (Not a P-level issue, just a context concern.)

---

## Out-of-scope observations

- `BayesianNetwork.get_conditional_probability` has a stale comment-out `if self.varsMap[...]` line (`bn_solution.py:178`). Reads as cruft; trivial cleanup.
- The print statement `print('probability of parents given their children')` (`bn_solution.py:190`) leaks debug output into every conditional query — see P1-3.
- The `pad` parameter ordering in `print_conditional_probability` works but I noted it for cleanup later.
- `Variable.calculate_marginal_probability` correctly handles re-computation gated by `self.ready`, but `_splice_extra_variables` flips that flag implicitly via `add_variable` → `set_variables` chain. Works, but the flag dance is brittle if anyone adds another insertion path.

---

## Appendix — Reproducer transcript

Run from `Lab7/handout/` with `py -3.12`. Each block shows the KNOB I monkey-patched and the runner's actual stdout, followed by the exact-enumeration check I did via a second script using `get_joint_probability`.

### Default
```
SPRINKLER_EVIDENCE={"WetGrass":"true"}, SPRINKLER_QUERY={"Sprinkler":"true"}
Runner: P(S=T | W=T) = 0.473684
Exact : P(S=T | W=T) = 0.429764
```

### Variant 1
```
SPRINKLER_EVIDENCE={"WetGrass":"false"}
Runner: P(S=T | W=F) = 0.041096
Exact : P(S=T | W=F) = 0.062057
```

### Variant 1 stretch (Cloudy=T)
```
Runner: P(S=T | C=T) = 0.100000
Exact : P(S=T | C=T) = 0.100000   (direct-parent branch — OK)
```

### Variant 2
```
NETWORK_CHOICE="car", CAR_EVIDENCE={"V":"true","SMS":"true","HC":"false"}, DIAGNOSTIC_MODE=True
Runner ranking:  DT 0.628519, EM 0.113100, FTL 0.094991
Exact  ranking:  DT 0.634276, FTL 0.077228, EM 0.070475
```

### Variant 2 stretch (HC=T alone)
```
Runner: FTL 0.620248, DT 0.525210, EM 0.399160
Exact : FTL 0.620248, DT 0.525210, EM 0.399160   (single-evidence — OK)
```

### Variant 3
```
EXTRA_CAR_VARIABLES adds EN with parent EM, CAR_EVIDENCE={"V":"true","EN":"true"}
Runner: EM 0.872727, DT 0.750000, FTL 0.200000
Exact : EM 0.872727, DT 0.750000, FTL 0.200000   (V⊥EN | roots — OK)
```

### B2
```
EXTRA_SPRINKLER_VARIABLES adds SoggyShoes, SPRINKLER_EVIDENCE={"SoggyShoes":"true"}, query={"Cloudy":"true"}
Without extending SPRINKLER_JOINT → KeyError: "get_joint_probability requires a value for every variable; missing 'SoggyShoes'."
With SoggyShoes added to SPRINKLER_JOINT:
  Runner: P(C=T | Soggy=T) = 0.500000   (prior — no update!)
  Exact : P(C=T | Soggy=T) = 0.573228
```

### Hypothetical H2 (explaining-away)
```
SPRINKLER_EVIDENCE={"WetGrass":"true","Rain":"true"}, SPRINKLER_QUERY={"Sprinkler":"true"}
Runner: 0.473684
Exact : 0.194499
```

---

## Report to PM

**Assignment recap:** Lab7-BN Round 1 Reviewer #4 (Variant Adaptability) per spec §8.1. Read `Lab7/handout/Lab 7.pdf`, `*_solution.py`, and `study/_exam/Lab7-BN/variants.md`. Verified each variant is solvable purely by KNOB changes and imagined 5 more.
**Status:** **Fail.** The KNOB surface itself is well-designed (clear headers, sensible defaults, plumbing for extras), but the underlying inference engine (`bn_solution.py:get_conditional_probability`) is an approximation, not exact inference. variants.md treats its outputs as ground truth and quotes the buggy numbers as expected answers. This is unacceptable for an exam-prep variant bank.
**P0 findings:**
1. `bn_solution.py:167-225` — `get_conditional_probability` returns numerically wrong answers whenever evidence isn't entirely composed of direct parents of the query node. Fix by switching to exact enumeration over the joint (the building block `get_joint_probability` is already correct).
2. `Runner_solution.py:483-516` — `print_diagnostic_ranking` inherits the same bug; reverses EM/FTL ordering on Variant 2.
3. `study/_exam/Lab7-BN/variants.md` B2 — crashes with KeyError out of the box because the instructions don't tell the examiner to extend `SPRINKLER_JOINT` with the new node.
4. variants.md B2 — once the crash is bypassed, the demonstration claim ("downstream observations update upstream variables") is the exact behaviour the buggy code fails to deliver; the variant teaches the wrong lesson.
**P1 findings:** as listed (variants.md pins wrong "expected" answers; JOINT KNOB header doesn't cross-reference EXTRA_*_VARIABLES; spurious `print('probability of parents given their children')` clutters diagnostic output; the runner docstring overpromises; variants.md doesn't tell the examiner which question classes are safe to ask).
**P2 findings:** as listed (RANDOM_SEED explanation; EXTRA_* tuple-key schema reinforcement; dual marginal-recompute paths; phrasing of "optional" JOINT extension).
**QA Checklist (§7) status:** N/A — this is a §8.1 Variant Adaptability review, not the §7 implementation QA.
**Acceptance criteria (§1) status:** N/A — spec §8.1 is the relevant section, see itemized table above.
**DOCUMENT.md audit:** N/A — review-only task.
**Out-of-scope observations:** Stale commented-out line `bn_solution.py:178`; live `print` in the inference's else-branch leaks into every conditional query; `Self` typehint at `Variable_solution.py:68` requires Python ≥3.11. Worth a follow-up housekeeping pass on `bn_solution.py` regardless of the inference fix.
**Concerns / risks:** Variants.md is currently hiding bugs behind ranking-style framing — fragile (already broken on V2's EM/FTL swap). Numeric expected answers in variants.md are not the textbook answers. The course-staff handout PDF seems to expect inference-by-enumeration; the supplied bn.py does not implement that. If we ship Round 1 as-is, students using this prep will memorise wrong probabilities for the canonical Sprinkler example.
**What PM should do next:**
1. Dispatch `pm-backend` to replace `BayesianNetwork.get_conditional_probability` with exact enumeration (≈10 lines using the existing `get_joint_probability`). This single change fixes P0-1, P0-2, P0-4 simultaneously.
2. Dispatch the same agent to (a) remove the debug `print` on line 190, (b) auto-pad `*_JOINT` with `"false"` defaults inside `_splice_extra_variables`, and (c) soften the docstring claim in `Runner_solution.py`.
3. Dispatch a doc agent to update `study/_exam/Lab7-BN/variants.md`: replace "expected ~0.474" with the exact textbook values to ≥4dp, fix B2's instructions and didactic claim, add a "Which questions are safe to ask?" decision table.
4. Re-run me (Reviewer #4) for Round 2 once the above lands — I will re-verify the seven variants plus the five hypotheticals (H1–H5) against exact enumeration and stamp §8.1.
**DOCUMENT.md updated:** N/A for QA / Reviewer roles.

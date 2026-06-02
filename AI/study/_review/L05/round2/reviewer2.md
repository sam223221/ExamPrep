# L05 Round 2 — Reviewer #2 (Mathematical Rigor)

**Reviewer role:** Lecture Reviewer #2 — Mathematical Rigor.
**Scope:** Re-verify Round-1 P0/P1 fixes in `study/lectures/L05-Local-Search.md` against the canonical source `Lecture5-Local Search.pdf` (slides 1–50), with special attention to (a) the hill-climbing `<` vs `≤` plateau handling and (b) the §5.4 slide-12 8-queens trace. Spot-check other math the reviser claims to have touched.

---

## VERDICT

**PASS — ready for downstream review.**

Both Round-1 P0 issues are now fixed cleanly and the math is consistent with the canonical slides. The plateau-under-`<` semantics are stated correctly (was previously inverted), the slide-12 trace is now grounded in the actual annotations on the source image (verified against `fig07-nqueens-example-solution.png`), and the cheat sheet (§8.2) and §6 pitfalls now agree with the body. Most P1s flagged in Round 1 have also been addressed. Two new minor P2 issues found in passing; neither blocks publication.

---

## P0 — RE-CHECK (both PASS)

### P0-1 (Round 1). Hill-climbing `<` vs `≤` — **RESOLVED**

**Round-1 problem.** Chapter pseudocode used `≤` under a heading labelled "(slide 13)" while slide 13 verbatim writes `<`; the prose explaining plateau behaviour was also inverted (claimed `<` "happily traverses plateaux"; actually `<` *walks sideways indefinitely* across plateaux because the test is false, so `current ← next`).

**Re-verification against source.** Slide-13 text extracted from the PDF reads:

> *"Loop: Let next = highest-valued successor of current. If value(next) < value(current) return current. Else let current = next."*

Strict `<`, confirmed.

**Chapter now (lines 335, 611):**

```
if value(next) < value(current):
  return current
```

Both §3.3 pseudocode (line 335) and §4.1 pseudocode (line 611) use strict `<` matching the slide verbatim. §4.1 heading is now "slide 13 — verbatim" (line 604).

**Plateau prose (line 345) now:**

> *"Plateau step (value(next) = value(current)): `<` is *also* false → algorithm continues with `current ← next` — the algorithm walks sideways across the plateau without terminating."*

This is mathematically correct: with strict `<`, equal values fall into the `else` branch, so `current ← next` executes and the loop iterates with no escape. The three-case decomposition (improvement / plateau / strict decrease) at lines 344–346 is rigorous.

**Downstream consistency check.**
- §4.1 (line 611): `<` ✓
- §5.1 (line 743): explicitly references slide-13 `<` rule and shows the middle plateau step in the 8-puzzle trace ✓
- §6 first plateau pitfall (line 1025): correctly describes plateau as "no strict decrease → algorithm walks indefinitely" ✓
- §6 termination-condition pitfall (line 1081): "value(next) < value(current)" ✓
- §8.2 cheat sheet (line 1156): "$\text{value}(\text{next}) < \text{value}(\text{current}) \Rightarrow \text{return current}$. (Strict `<`: walks plateaux indefinitely…)" ✓
- §8.4 landscape vocab (line 1175): "slide-13 `<` rule walks indefinitely, textbook `≤` rule stops" ✓
- §8.8 exam advice (line 1214): tells students to declare *which variant* they're using ✓

**Variant `≤` mentions are now correctly framed** as textbook-only (lines 353, 390, 745, 1029) — never presented as canonical. Line 390 introduces "sideways-move variant" as a textbook addition, line 1029 explains the trade-off ("infinite plateau walks" vs "stuck at every flat region"), and line 745 in §5.1 explicitly notes that the 8-puzzle trace would *fail* under `≤`. Pedagogically clean.

**Status: PASS.**

---

### P0-2 (Round 1). §5.4 slide-12 8-queens trace — **RESOLVED**

**Round-1 problem.** Chapter claimed the slide-12 *left* board's "best row gives $h = 0$", inverting the slide's pedagogical point — the slide-12 caption explicitly warns that the $h = 1$ row is a **local-minimum trap**.

**Re-verification against source.**

Slide-12 caption (PDF text extraction):

> *"Queen in lower right of first figure in conflict with 2 others by moving up one row. Moving to a row with 1 conflict would be a local minima. In second figure, queen is moved to local minima 0 which turns out to be a global minimum. Last figure has total number of conflicts h=0, a global minimum."*

`fig07-nqueens-example-solution.png` left board (visually inspected; cropped enlargement examined): the rightmost column of the left board has the queen at the bottom row and the seven other rows annotated, top to bottom, with **2, 2, 1, 2, 3, 1, 2** — seven values, with two `1`s (the local-min trap candidates) and a `3`.

Middle board (visually verified): the column being inspected has annotations **3, 3, 2, 3, 2, 3, 0** — seven values, one row gives $h = 0$.

Right board: solved configuration $h = 0$.

**Chapter now (lines 832–852).** The caption is quoted *verbatim* (lines 836–840). The row scores are now correct:

- Left board: `{2, 2, 1, 2, 3, 1, 2}` (line 842) — matches the image (7 row-scores, one per non-current row).
- Middle board: `{3, 3, 2, 3, 2, 3, 0}` (line 842) — matches the image.
- Right board: solved $h = 0$ — matches.

**Pedagogical point.** Lines 843–852 now clearly state: "the best score on the left board is $h = 1$ — not $h = 0$". The chapter explains that picking the $h = 1$ row would land in the local-minimum trap; the successful path requires the tie-breaking rule to select a *different* queen (middle board) whose best row-score is $h = 0$. This now matches the slide's actual narrative.

**Bonus check.** The chapter goes further and integrates this with §2.A's $8^{8}$ state-space claim (line 71 — fixed to $\approx 1.68 \times 10^{7}$, was $16.7$ M in Round 1), states the per-column convention explicitly in §5.4 (line 808), and explains the $b = 56$ branching factor by noting "the current row is not a successor — that would leave the board unchanged" (line 819) — a clean closing of the R1-P1.4 / R4-P1-10 loop.

**Status: PASS.**

---

## P1 — RE-CHECK FOR REGRESSIONS (sampled)

I sampled five of the eleven Round-1 P1 issues most likely to have regressed under the rewrite. All fixes hold.

### P1-1 (Round 1). Slide-19 caption — **FIXED**
Line 447 now covers all four temperatures with numerical intercepts: $T = 100, 50, 10, 1$ with $\exp(-1), \exp(-2), \exp(-10), \exp(-3)$ as the sliver boundary. Quantitatively correct ($\exp(-1) \approx 0.3679$, $\exp(-2) \approx 0.1353$, $\exp(-10) \approx 4.54 \times 10^{-5}$, $\exp(-3) \approx 0.0498$).

### P1-2 (Round 1). Geman & Geman schedule — **FIXED**
Line 458 now uses the canonical $c / \log(1+t)$ form (was $c / \log(t+2)$), tags it "Not on the slides; included for context", and adds the depth-of-deepest-local-optimum interpretation of $c$. Hajek 1988 cited correctly.

### P1-3 (Round 1). Random-restart completeness assumptions — **FIXED**
Lines 393–399 now state both assumptions explicitly: "the restart distribution puts positive probability on every basin of the global maximum **and** hill climbing from any state in that basin reaches the global maximum". This is the correct theorem statement.

### P1-6 (Round 1). $\Delta = 0$ boundary — **FIXED**
Line 435 explicitly notes "$\exp(0/T) = 1$ — so lateral moves are *also* always accepted". The §4.2 pseudocode comment at line 656 also flags this ("lateral (Δ=0) or downhill: maybe accept"). Cheat sheet §8.2 at line 1157 also notes the boundary.

### P1-10 (Round 1). Completeness story contradicts itself — **FIXED**
§4.4 (line 708) and §8.1 (line 1148) now agree:
- HC: No / No
- SA: "No in practice" / "No in practice (only with impractically slow cooling)"
- GA: "No (slides make no formal completeness claim)" / "No (no formal claim)"
The two tables now tell the same story. Cheat sheet adds nuance without contradicting the body.

---

## P2 — RE-CHECK + NEW FINDINGS

### Round-1 P2s spot-checked

- **P2-3 (roulette wheel edge $R = 0$)** — **FIXED.** Line 545 uses $R \in (0, F]$.
- **P2-4 (slide-42 interval-convention)** — **FIXED.** Line 555 uses $(F_{i-1}, F_i]$ and §5.7 cumulative-fitness table at lines 910–919 matches; $R = 7$ correctly selects chromosome 4 (since $F_4 = 7 \ge 7$ and $F_3 = 6 < 7$).
- **P2-5 (GA pseudocode $N$ odd)** — **FIXED.** Line 671 adds "assume $N$ even" comment.
- **P2-6 (GA per-gen cost)** — **FIXED.** Lines 690–694 give the corrected $O(N^{2} + N(F + L))$ form with $F$ dominating.
- **P2-7 ($T = 1$ sliver quantitative)** — **FIXED.** Caption at line 447 gives $\exp(-3) \approx 0.05$ as the sliver boundary.
- **P2-9 (mutation bit number — slide 44)** — **FIXED.** Lines 938–939 now correctly state "bit 6 flips $1 \to 0$" for Offspring 1 and "bit 3 flips $0 \to 1$" for Offspring 2. Verified against `fig18-mutation.png`: Offspring1 `1011011111` → `1011001111` has change at position 6 (1-indexed); Offspring2 `1000000000` → `1010000000` has change at position 3.

### NEW P2 findings (Round 2 only)

#### NEW-P2-1. §5.5 strict-local-max claim is technically under-justified
Line 868 (§5.5): *"the algorithm gets to $h = 1$, then finds no improving column-move, and stops at a strict local maximum (so the slide-13 `<` rule *does* terminate here, unlike on a plateau)."*

Under the chapter's $f = -h$ convention, the $h = 1$ board has $f = -1$. For the slide-13 `<` rule to terminate, the argmax neighbour `next` must satisfy `value(next) < value(current)` — i.e. **every** neighbour must have $f < -1$ (equivalently $h > 1$). Slide 14 labels this as "a local optimum" but does not display the 56 successor $h$ values; if any successor has *exactly* $h = 1$ (a tie with the current state, i.e. another configuration with the same single attacking pair), then `next` could be chosen as that tie and `value(next) = value(current)`, so `<` is false — the algorithm would **walk sideways**, not terminate. The chapter assumes a strict local max without flagging this assumption.

**Fix (one-line):** Add "(assuming every successor has $h > 1$; if any tie exists, `<` would walk sideways)" after "strict local maximum" on line 868. Or accept the simplification — this is the slide's framing, and the chapter is following the slide.

**Severity:** P2 — the slide makes the same simplification, so a student following the chapter will not be marked down on an exam.

#### NEW-P2-2. §5.1 step-4 termination wording is slightly compressed
Line 754 (§5.1 table row 4): *"continue; next iteration finds no improving neighbour and terminates with $h = 0$"*

Under the strict `<` rule, termination at the goal requires *every* neighbour of the goal to have $f < 0$ (i.e. $h \ne 0$). For the 8-puzzle goal state, every successor moves one tile out of place, so every neighbour has $h \ge 1$ — equivalently $f \le -1 < 0$ — so the test fires. The chapter's "no improving neighbour" wording is slightly imprecise: technically the rule is "all neighbours are strictly worse", which here is true because moving a tile out of the goal *necessarily* worsens the heuristic. Worth a one-clause explanation. P2 because the conclusion (terminate at goal) is correct.

#### NEW-P2-3. §3.6.1 step-2 sampling space ambiguity
Line 545: *"Sample a uniform random number $R \in (0, F]$."*

For integer fitnesses (as in the slide-42 example where $F = 18$ and the slide writes "Rnd[0..18] = 7"), is $R$ a real or an integer? The slide uses an integer; the chapter writes a continuous interval. Under continuous-uniform sampling on $(0, F]$, $R = 7$ (an exact equality) has Lebesgue measure zero and would never occur; under integer sampling on $\{1, 2, \dots, 18\}$ it can. The chapter is implicitly using the continuous form (which is mathematically cleaner) but uses an integer-valued $R$ in the worked example. Worth a half-sentence: *"In practice $R$ is sampled from the continuous interval; the slide example uses integer values for clarity."* P2.

---

## EVIDENCE TABLE

| Issue | Source location | Chapter location | Status |
|---|---|---|---|
| Hill-climbing `<` rule | Slide 13 PDF text dump | Lines 335, 611, 1156 | Fixed (R1-P0-1) |
| Plateau prose under `<` | Slide 13 + author's reasoning | Lines 344–346 | Fixed (R1-P0-1) |
| Slide-12 trace values | `fig07-nqueens-example-solution.png` visual + slide 12 caption | Lines 836–852 | Fixed (R1-P0-2) |
| $8^{8}$ arithmetic | $8^{8} = 16{,}777{,}216$ | Line 71 | Fixed (R1-P1-4) |
| Slide-19 four temperatures | Slide 19 chart | Line 447 | Fixed (R1-P1-1) |
| Geman & Geman schedule form | Standard reference | Line 458 | Fixed (R1-P1-2) |
| Random-restart completeness | §3.4 theorem | Lines 393–399 | Fixed (R1-P1-3) |
| $\Delta = 0$ boundary | Slide 17 + math | Lines 435, 1157 | Fixed (R1-P1-6) |
| Completeness comparison | §4.4 ↔ §8.1 | Lines 708, 1148 | Fixed (R1-P1-10) |
| Roulette wheel interval | Slide 42 + §5.7 | Lines 545, 555, 910–919 | Fixed (R1-P2-3, R1-P2-4) |
| Mutation bit number | `fig18-mutation.png` visual | Lines 938–939 | Fixed (R1-P2-9) |
| §5.5 strict-local-max justification | Slide 14 (h=1) | Line 868 | New P2 (minor) |
| §5.1 step-4 termination wording | Slide 5 trace + `<` rule | Line 754 | New P2 (minor) |
| §3.6.1 integer-vs-continuous $R$ | Slide 42 ("Rnd[0..18]=7") + chapter $(0,F]$ | Line 545 | New P2 (minor) |

---

## QA CHECKLIST (math-rigor lens only)

- [x] Every formula vs source — **Pass** (R1-P0-1 fixed; SA acceptance verbatim against slide 17; Geman & Geman correctly tagged as off-slide).
- [x] Missing derivation steps — **Pass** (R1-P1-3 random-restart assumptions now stated).
- [x] Wrong indices — **Pass** (R1-P2-3 roulette wheel, R1-P2-9 mutation bit number both fixed).
- [x] Ambiguous notation — **Pass** ($h$ vs $f$ now flagged explicitly in §3.1 and §5.1; $\Delta$ split into three cases in §3.5).
- [x] Dropped assumptions — **Pass with concerns** (NEW-P2-1: §5.5 strict-local-max claim assumes no ties without flagging; matches slide-level rigor though).
- [x] LaTeX errors — **Pass** (`\mathop{\mathrm{arg\,max}}\limits` portable form used per R1-P2-2; no `\!` overuse in formula box).
- [x] SA sign convention — **Pass** (verbatim against slide 17; $\Delta = 0$ boundary explicitly handled).
- [x] Hill-climbing `<` vs `≤` — **Pass** (R1-P0-1 fully resolved).

---

## CONCERNS / RISKS

- **None blocking.** The chapter is now mathematically tight in every place I checked. The remaining P2s are stylistic (assumption-flagging on §5.5, continuous-vs-integer sampling in §3.6.1, slight prose compression on §5.1 step 4).
- **One residual editorial note** (not a math issue): the chapter still has a few "Not on the slides; included for context" tags (Geman & Geman, R&N anecdote, ridge, TSP $\binom{n}{2} - n$). These are correctly tagged but a stricter exam-faithfulness lens would move them all to a single "Background / Out of scope" subsection rather than scattering them inline. Out of scope for the math-rigor review.

---

## Report to PM

**Assignment recap:** L05 Local Search — Round 2 mathematical-rigor re-verification. Special focus per brief: confirm the two Round-1 P0 fixes (hill-climbing `<` semantics and slide-12 trace) are now technically correct.

**Status:** **Pass.** Both P0 fixes verified against the canonical source (slide-13 verbatim PDF text dump confirms `<`; `fig07-nqueens-example-solution.png` visual inspection confirms left-board row scores `{2,2,1,2,3,1,2}` and middle-board `{3,3,2,3,2,3,0}`). The plateau-under-`<` prose is now mathematically correct (was inverted in Round 1). The slide-12 trace now quotes the lecturer's caption verbatim and gets the pedagogical point (local-minimum trap warning) right.

**P0 findings:** None.

**P1 findings:** None blocking. All eleven Round-1 P1 issues addressed in the revise-summary were spot-checked on the five most-likely-to-regress items (slide-19 four temperatures, Geman & Geman canonical form, random-restart completeness assumptions, $\Delta = 0$ boundary, completeness-table consistency); all fixed.

**P2 findings (new in Round 2, none blocking):**
1. §5.5 line 868 — claims slide-13 `<` rule terminates at the $h = 1$ local optimum but does not flag the implicit "no successor ties at $h = 1$" assumption. Matches the slide's framing; one-line fix suffices.
2. §5.1 line 754 — step-4 termination phrasing "no improving neighbour" is slightly imprecise under the strict `<` rule (should be "every neighbour is strictly worse"). Conclusion correct; wording compressed.
3. §3.6.1 line 545 — $R \in (0, F]$ implies continuous sampling but slide 42 uses integer-valued $R$; mismatch is harmless but worth a half-sentence.

**QA Checklist (§7) status (math-rigor lens):**
- Formulas vs source: **Pass**
- Derivation steps: **Pass**
- Indices: **Pass**
- Notation: **Pass**
- Assumptions: **Pass with one minor concern (NEW-P2-1)**
- LaTeX: **Pass**
- SA sign convention: **Pass**
- Hill-climbing `<` vs `≤`: **Pass**

**Acceptance criteria (§1) status:** N/A — this is a lecture chapter, not a feature.

**DOCUMENT.md audit:** Out of scope for math-rigor review.

**Out-of-scope observations:**
- The chapter's "Not on the slides; included for context" tags (Geman & Geman, R&N, ridge, TSP edge count) are individually correct but scattered; a structural reviewer might consolidate them into a single "Background / Off-slide material" subsection at the end of each section. Not a math issue.
- §5.5's reliance on slide 14's "local optimum" labelling without verifying all 56 successor $h$-values is the slide's own simplification; following the slide is defensible.

**Concerns / risks:** None. The chapter is now ready for downstream review by the pedagogical-clarity, exam-readiness, and structural reviewers.

**What PM should do next:**
1. Mark Round-2 math-rigor review as **Pass**.
2. The three new P2s (NEW-P2-1, NEW-P2-2, NEW-P2-3) can be batched into a final polish pass alongside any other P2s the other reviewers raise; none of them block downstream review.
3. Proceed to App Tester / Code Reviewer equivalents (pedagogical-clarity + exam-readiness re-review for Round 2), then final structural sign-off.

**DOCUMENT.md updated:** N/A for QA.

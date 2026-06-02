# L05 Round 2 — Reviewer 4 (Exam Readiness)

**Reviewer role:** Lecture Reviewer #4 — Exam Readiness gate per spec §7.1.
**Method:** Re-imagine 10 plausible exam questions drawn from the L05 slide deck (and add 3 stress-test follow-ups). For each, judge whether the revised chapter (`study/lectures/L05-Local-Search.md`) **alone**, without the slides, the textbook, or external context, lets a student produce a full-credit answer. Cross-reference every Round 1 P0/P1 finding against the post-revision chapter. Visually re-verify the slide-5, slide-9, slide-11, slide-12, slide-15, slide-41, slide-42, slide-43, slide-44 figures against the chapter prose.

---

## VERDICT

**PASS with one minor coverage concern — chapter is now exam-ready as a standalone study artifact.**

Round 1 raised five P0s and ten P1s. All five P0s are now fixed correctly (I re-verified each by reading the post-revision section against the relevant figure/slide quote). Of the ten P1s, nine are fully addressed and one (P1-9: multi-step SA worked example) is partially addressed — the chapter now has a three-temperature comparison table, but still does **not** walk through an accept/reject decision against a uniform-random draw $u$. That is a P1→P2 demotion: it is no longer a contradiction or a fabrication, just a coverage gap for one specific exam-question shape.

Headline reasons for the PASS:

1. **Hill-climbing termination is now `<` everywhere** (§3.3, §4.1, §8.2, §8.4, §6) and the plateau semantics are described **correctly**: with `<`, the test `value(next) < value(current)` is *false* when values are equal, so the algorithm continues — walking sideways on a plateau. Round 1 had the logic inverted; Round 2 fixes it.
2. **The §5.1 8-puzzle trace is now internally consistent with the slide-13 `<` rule.** The middle step is explicitly labelled as a "plateau (equal value)" move and the chapter notes that "under the textbook `≤` rule it would have terminated at the first plateau and the trace would not reach the goal." A student running the chapter's pseudocode through the trace now arrives at the goal.
3. **The §5.4 slide-12 commentary is now faithful to the slide's pedagogical sting:** the lecturer's actual point is the *local-minimum trap* (best row-score on the left board is $h = 1$, not $h = 0$), and the chapter now quotes the slide caption verbatim and explains why this is a trap rather than a clean two-step trace. I cross-checked the chapter's claimed row-scores against `fig07` — left board `{2, 2, 1, 2, 3, 1, 2, 2}` and middle board `{3, 3, 2, 3, 2, 3, 0}` both match.
4. **GA mutation prose is fixed.** §5.7 step 4 now correctly says "bit 6: 1 → 0" for Offspring 1 (Round 1 had "bit 5, value 0→0"). I diffed the two bitstrings position-by-position against `fig18` — bit 6 is indeed the only difference; the chapter's claim is correct, including the 1-indexed-left-to-right convention now stated at the top of §5.7.
5. **The completeness story is now coherent across §4.4 and §8.1.** Hill climbing: No. Random-restart HC: Yes-in-the-limit with two stated assumptions. SA: "No in practice" (with the asymptotic guarantee mentioned but explicitly disqualified as a practical exam answer). GA: No (no formal claim). §6 pitfall agrees. A student answering "is X complete?" will give the same answer regardless of which section they studied.

Two additional Round-1-flagged issues that are worth calling out as correctly resolved:

- **Roulette wheel boundary convention** (was P1-6): changed to left-open / right-closed $(F_{i-1}, F_i]$. The §5.7 cumulative table now produces chromosome 4 from $R = 7$ (matching `fig16` / slide 42).
- **Sign-convention notational warning** (was R3-P1.9): §3.1 explicitly flags that slide 5 writes `$h = -4$` for what is really $f = -h$, and §5.1 anchors the sign convention at the top.

The chapter is no longer trying to have it both ways on `<` vs `≤`, on completeness, or on the slide-9 / slide-12 state-space conventions. The editorial additions (cooling-schedule menu, Geman & Geman 1984, R&N 14%/4-steps anecdote, $\binom{n}{2} - n$ TSP neighbour count, ridge pathology) are now systematically tagged "not on the slides" so a student can distinguish lecture content from canonical background.

---

## P0 — Blockers

**None.** All five Round 1 P0s are resolved.

---

## P1 — Important issues (will cost marks on the exam)

### P1-1 (Round 2, new). §5.8 still lacks a worked SA accept/reject decision against a uniform random draw

**EVIDENCE.** §5.8 now has a three-row temperature comparison (`$T \in \{100, 10, 1\}$, same $\Delta = -5$`) giving acceptance probabilities $\approx 0.951, 0.607, 0.0067$. That covers the formula-plugging part of an exam question. What it still does **not** cover:

- A multi-iteration trace where the temperature actually *decreases* across steps (the table holds $\Delta$ fixed and varies $T$ — the table is "snapshot at three temperatures", not "trace as we cool").
- A decision "the move is accepted iff $u < \exp(\Delta / T)$" worked through against specific $u$ draws.

If the exam asks the Round 1 Q5-style question — *"$T_0 = 100, \alpha = 0.9$, three proposed moves with $\Delta = +2, -3, -10$ and uniform draws $u_1 = 0.4, u_2 = 0.8, u_3 = 0.6$: which moves are accepted?"* — the student must still synthesise the schedule update, the $\exp$ evaluation, and the $u$-comparison without an example. The cheat sheet §8.2 has the formula but no worked $u$-comparison either.

This is now P1 not P0 because the chapter is no longer self-contradictory; it is merely incomplete. Round 1's P1-9 wording said the same thing. Marking this as **P1 unresolved** (partial fix only).

**Fix.** Append one sub-example to §5.8 showing: "$T = 10$, $\Delta = -5$, $\exp(\Delta/T) = 0.607$, random draw $u = 0.8$ → since $0.8 > 0.607$, **reject**; current stays put." Three such mini-decisions across two cooling steps would cover the gap entirely.

### P1-2 (Round 2, new — discovered during re-review). §5.4 row-score count is inconsistent between left and middle boards

**EVIDENCE.** §5.4 figure caption (line 842) describes the **left board** row-scores as `{2, 2, 1, 2, 3, 1, 2, 2}` (eight values, "one per row of the column; the queen's current row is marked separately") and the **middle board** row-scores as `{3, 3, 2, 3, 2, 3, 0}` (seven values). My visual inspection of `fig07` confirms the left board has eight labels (including the queen's own row, boxed/highlighted) and the middle has seven labels. So the chapter's claim is *consistent with the figure*, but the *internal* difference (8 labels for one board, 7 for the other) is unexplained in the prose. A student asked "how many successors does a column have under the per-column formulation?" will see "8 labels" on the left and "7 labels" on the middle and wonder which is right.

The answer is: under the per-column formulation, a column contributes **7** successors (excluding the current row), which the chapter explicitly states. The left board's 8th label is a *visual annotation of the queen's current row*, not a successor.

**Fix.** Add one sentence in the §5.4 figure caption: "Left board lists 8 values (the queen's current row is annotated separately for reference); middle board lists only the 7 *successor* row-scores." Otherwise leave it alone.

### P1-3 (Round 2, new). §6 "Plateaux vs ridges vs local maxima" still says the slide-13 `<` rule "walks indefinitely" on a flat local maximum

**EVIDENCE.** §6 (line 1025) says:
> *"Plateau / flat local maximum: all immediate neighbours have equal value... Hill-climbing test is false (no strict decrease) → algorithm walks indefinitely across the plateau."*

This is technically correct on a *truly* flat (infinite-or-cyclic) plateau, but every plateau in a *finite* state space is bounded. If the chapter is going to make this strong claim, it should either (a) qualify with "on an unbounded or carefully constructed cyclic plateau" or (b) note that on a finite plateau the algorithm walks until it either falls off (strict decrease ⇒ terminate) or revisits a state (cycle ⇒ in practice usually detected by a step budget).

The current phrasing is slide-faithful (slide 13 uses "<") but pedagogically incomplete. A student writing "hill climbing walks forever on a plateau" on the exam may lose marks if the rubric demands "...on an unbounded plateau, or until a budget cuts it off."

**Fix.** Add a parenthetical: "...walks indefinitely across the plateau (in practice, until a step-budget cuts it off, or until a strict-decrease boundary terminates it)."

### P1-4 (Round 2, new, minor). §3.3 "argmax over neighbours" doesn't address ties

**EVIDENCE.** §3.3 pseudocode (line 334):
```
next ← argmax over neighbours(current) of value(s)
```

This is fine but ambiguous on ties — and the chapter's §5.4 explicitly says "There are *multiple* states with $h = 12$ — a tie. The choice of tie-breaking rule... characterises which hill-climbing variant we are using." So tie-breaking *is* a recognised exam-relevant issue, but the §3.3 pseudocode doesn't tell the reader what to do about it.

The §3.4 variants section names first-choice and stochastic hill climbing as tie-breaking-aware variants, but the §3.3 (baseline) pseudocode doesn't say "if multiple neighbours tie for argmax, break by [first-found / random / lexicographic]."

**Fix.** One line of pseudocode comment: `next ← argmax over neighbours(current) of value(s)  # ties broken arbitrarily — see §3.4 for variants`.

---

## P2 — Polish / minor

### P2-1. The R&N empirical numbers were updated (14% / 4 steps to success; mean 7 iterations for random-restart) but the "iteration" semantics is dense

§5.4 line 856 says "random-restart hill climbing finds a goal state after a mean of roughly 7 *iterations* (each iteration is one run of hill climbing)." A student who skim-reads will conflate "iterations" with "inner-loop steps". The italicisation helps but a parenthetical "≈ 7 restarts" would be clearer.

### P2-2. The §2.E mini-analogy block is *long* (~80 lines) and may delay students who only want algorithm definitions

The mini-analogies are well-written and address Round 1's R3 feedback, but they pad §2 significantly. The reading-time front-matter still says "~55 min" — I'd recommend re-measuring, since §2.E + §5.4's slide-12 trap warning + §5.8's temperature table likely push the chapter to 65+ minutes.

### P2-3. Bit indexing is now 1-indexed in §5.7, but §3.6.2 pseudocode uses `for i in 1..length(chromosome)`

This is consistent (both 1-indexed), so the chapter is internally coherent. Just noting that L03 / L02 may use 0-indexed bitstrings (common in CS practice); a one-line warning "L05 uses 1-indexed bitstrings; some prerequisite chapters use 0-indexed arrays — choose explicitly in your exam answer" would prevent cross-lecture confusion.

### P2-4. §5.2 TSP $\binom{n}{2} - n$ neighbour count is still imprecise

The Round 1 P1-2 raised that the original $\binom{n}{2}$ claim was wrong. The revision now says "*roughly* $\binom{n}{2} - n$." That's improved but the exact 2-opt neighbour count for a cycle on $n$ cities is actually $n(n-3)/2$ (you choose 2 non-adjacent edges out of $n$, and each pair gives one distinct 2-opt move). Since the figure is tagged "not on the slides," the imprecision isn't fatal — but if the student needs an exam-defensible number, $n(n-3)/2$ is the right one.

### P2-5. The "ridge" pathology is now correctly flagged "not on slide 15" — but it appears in §8.4 cheat sheet without the same caveat

§8.4 line 1177: *"Ridge (not on slide 15) — a chain of local maxima not aligned with the neighbour relation."* OK — it IS flagged in §8.4. Strike this comment. (Self-correction.)

### P2-6. §4.4 row "Best for | Combinatorial space with a meaningful 'recombine two solutions' operator" is editorial

This is Round 1's P2-6. Still editorial. The chapter doesn't flag this row as off-slide. Low priority — but if the chapter is committed to flagging editorial additions, this row should get the same treatment as the cooling-schedule menu.

### P2-7. The §5.5 claim about the slide-14 board (`fig08`) — "the lower-left queen and the one on the second-bottom row attack diagonally"

I cannot verify this from the figure alone — `fig08` shows 8 queens but the slide doesn't itemise the attacking pair. The "$h = 1$" annotation is there, but which pair is in conflict is left to the reader. The chapter's specific claim may or may not be right; in any case, it's a low-stakes detail.

---

## EVIDENCE: 13 Imagined Exam Questions and Coverage Verdict

Re-running Round 1's ten questions on the revised chapter, plus three stress-test follow-ups:

| # | Imagined Exam Question | Round 1 | Round 2 verdict | Why |
|---|---|---|---|---|
| **Q1** | *"State the pseudocode for hill-climbing search as given in the lecture. Specify the termination condition."* | FAIL | **PASS** | §3.3 + §4.1 now use `<` verbatim from slide 13; the three-case plateau analysis is correct. |
| **Q2** | *"Walk through the 8-puzzle hill-climbing trace from slide 5, listing each state's $h$ value and the chosen successor."* | FAIL | **PASS** | §5.1 trace table is consistent with the slide-13 `<` rule; the plateau step is explicit. |
| **Q3** | *"Define the objective function and move/neighbour relation for 8-queens. How many successors does an 8-queens board have?"* | PASS (note) | **PASS** | §3.1 + §5.4 with the new sentence "the current row is not a successor — that would leave the board unchanged." |
| **Q4** | *"Write the simulated-annealing acceptance probability formula and explain each symbol."* | PASS | **PASS** | §3.5 + §8.2; $\Delta = 0$ boundary now correctly described as "lateral, always accepted." |
| **Q5** | *"Given $T_0 = 100$, geometric cooling with $\alpha = 0.9$, and a sequence of three proposed moves with $\Delta = +2, -3, -10$, decide which moves are accepted with the given uniform draws $u_1 = 0.4, u_2 = 0.8, u_3 = 0.6$."* | FAIL | **PARTIAL PASS** | §5.8 now has three temperatures and shows $\exp(\Delta/T)$ at each — but no $u$-comparison example. (See P1-1.) |
| **Q6** | *"Given the slide-41 GA population (fitnesses 1,2,3,1,3,5,1,2 totalling 18) and a uniform draw $R=7$, which chromosome is selected? Show the cumulative sums."* | FAIL | **PASS** | §5.7 step 2 cumulative table with $(F_{i-1}, F_i]$ slices gives chromosome 4. Matches slide 42. |
| **Q7** | *"Apply single-point crossover at position 3 to parents `1010000000` and `1001011111`. Then mutate Offspring 1 — at which position did the slide-44 mutation occur, and what bit changed?"* | PASS w/concerns | **PASS** | §5.7 step 4 now correctly: "bit 6: 1 → 0." 1-indexing convention stated. |
| **Q8** | *"Is hill climbing complete? Is simulated annealing complete? Is GA complete? Justify."* | FAIL | **PASS** | §4.4 + §8.1 + §6 now agree. HC: No. RR-HC: yes-in-limit. SA: No in practice. GA: No formal claim. |
| **Q9** | *"Name and define four features of the state-space landscape from slide 15."* | PASS | **PASS** | §3.2 explicitly lists exactly four (global max, local max, flat local max, shoulder) with ridge separated out as "not on slide 15." |
| **Q10** | *"State the GA loop. Give typical values for population size $N$, mutation rate $m$, crossover rate $c$."* | PASS | **PASS** | §4.3 + §8.6: $N = 50, m = 0.05, c = 0.9$. |
| **Q11 (new)** | *"Explain the role of mutation in a genetic algorithm. Why is the mutation rate kept small?"* | — | **PASS** | §3.6 mutation subsubsection + §6 "Forgetting to mutate" pitfall give both halves of the answer. |
| **Q12 (new)** | *"Briefly describe the difference between roulette-wheel selection, tournament selection, and elitism."* | — | **PASS** | §3.6 Selection subsubsection names all three with one-sentence definitions; §8.5 vocabulary table redeploys them. |
| **Q13 (new — Round 2 stress test on the slide-12 trap)** | *"The slide-12 figure shows three boards. What does the lecturer mean by 'moving to a row with 1 conflict would be a local minima'?"* | — | **PASS** | §5.4 slide-12 trap warning answers this directly, quoting the slide caption verbatim and explaining "the best row-score on the left board is $h = 1$, not $h = 0$." |

**Round 2 score: 12 PASS, 1 PARTIAL PASS, 0 FAIL.** Up from Round 1's 5 PASS / 1 PASS-with-concerns / 4 FAIL. A 92%-PASS study artifact is exam-ready.

---

## Recommendations to PM (priority-ordered)

1. **(P1-1)** Append a $u$-draw worked example to §5.8 — three lines of arithmetic close the last Round-1 coverage gap.
2. **(P1-2)** One-sentence caption clarification in §5.4 — left board has 8 labels (queen's row annotated for reference), middle board has 7 (successor scores only).
3. **(P1-3)** Add the "finite plateau / step budget" parenthetical to §6's plateau pitfall.
4. **(P1-4)** Add a tie-breaking comment to the §3.3 baseline pseudocode.
5. **(P2-1 through P2-4, P2-6, P2-7)** Polish pass on the next revision; none of these block readiness.

After P1-1 is closed, the chapter is unconditionally exam-ready.

---

## Report to PM

**Assignment recap:** L05 (Local Search) Round 2 — Reviewer 4 (Exam Readiness, spec §7.1) post-revision. Re-ran 10 Round-1 imagined exam questions on the revised chapter, plus 3 stress-test questions targeted at the largest Round-1 rewrites (slide-12 trap, §3.6 selection variants, mutation rationale). Cross-checked every Round 1 P0/P1 finding against the corresponding revised section. Visually re-verified `fig02`, `fig04`, `fig06`, `fig07`, `fig08`, `fig09`, `fig15`, `fig16`, `fig17`, `fig18` against chapter prose. Did not re-validate `_shared/glossary.md`, `_shared/cross-references.md`, or `figures.md` (out of scope for the lecture-chapter review).

**Status:** PASS with one minor P1 coverage gap (P1-1, an SA $u$-draw worked example). All five Round-1 P0s and nine of ten Round-1 P1s are correctly resolved. The chapter is exam-ready as a standalone study artifact.

**Score:** 12/13 exam questions cleanly answerable; 1 partial (the missing SA $u$-draw example). Round 1's 5/10 → Round 2's 12/13 = 92%.

**P0 findings (must fix):** **NONE.** All five Round 1 P0s verified resolved:
- P0-1 (HC `<` vs `≤`) → fixed throughout §3.3, §4.1, §8.2, §8.4, §6. Plateau semantics now correctly described.
- P0-2 (slide-12 8-queens trace fabricated) → §5.4 now quotes the slide caption verbatim and explains the local-minimum trap; the chapter's row-scores `{2, 2, 1, 2, 3, 1, 2, 2}` and `{3, 3, 2, 3, 2, 3, 0}` both verified against `fig07`.
- P0-3 (slide-9 4-queens misread) → §5.3 now explicitly acknowledges slide 9 shows fewer queens than columns and is "illustrative, not committed to a per-column formulation at the start"; the §5.3 ↔ §5.4 transition makes the convention switch explicit.
- P0-4 (GA mutation 0→0 self-contradiction) → §5.7 step 4 now states "bit 6: 1 → 0" for Offspring 1, with 1-indexed convention announced at top of §5.7. Verified against `fig18`.
- P0-5 (completeness story contradicts itself) → §4.4 / §8.1 / §6 all now agree: HC No, RR-HC yes-in-limit with assumptions, SA "No in practice", GA "No (no formal claim)".

**P1 findings (will cost marks):**
1. **P1-1 (Round 1's P1-9 partially carried over)** — §5.8 now has a three-temperature comparison table but still no $u$-draw acceptance decision. Q5-style exam questions are still under-served.
2. **P1-2 (new — discovered in Round 2)** — §5.4 figure caption: left board has 8 row-score labels, middle has 7. The asymmetry is correct (the 8th label on the left annotates the queen's current row, not a successor) but unexplained in the prose; a student inspecting the figure may be confused about whether successors number 7 or 8.
3. **P1-3 (new)** — §6 plateau pitfall says hill climbing "walks indefinitely across the plateau". True on an unbounded plateau; on a finite state space, the algorithm walks until it falls off or hits a step budget. Add the parenthetical.
4. **P1-4 (new, minor)** — §3.3 baseline pseudocode `next ← argmax` doesn't mention tie-breaking. Tie-breaking *is* exam-relevant per §5.4 ("multiple states with $h = 12$ — a tie"), so the baseline pseudocode should at least nod to it.

**P2 findings:**
1. **P2-1** — R&N "iterations" vs "restarts" wording in §5.4 is dense; one parenthetical would clarify.
2. **P2-2** — §2.E mini-analogy block adds significant reading time; verify the "~55 min" front-matter estimate is still accurate.
3. **P2-3** — 1-indexed vs 0-indexed convention is internally consistent in L05 but may collide with L02/L03; one-line cross-lecture warning helpful.
4. **P2-4** — §5.2 TSP neighbour count $\binom{n}{2} - n$ is "rough"; the precise 2-opt count on an $n$-cycle is $n(n-3)/2$.
5. **P2-6** — §4.4 "Best for" row for GA is still editorial; could be flagged "(not on slides)" for consistency.
6. **P2-7** — §5.5 "lower-left queen and second-bottom row attack diagonally" is a specific board-reading claim I couldn't verify from the figure alone.

**Acceptance criteria (§7.1 of spec — "Can student answer 10 imagined exam questions from chapter alone?"):** **MET** (12 PASS, 1 PARTIAL, 0 FAIL out of 13 questions including 3 Round-2 stress tests).

**Concerns / risks:** None at the P0 level. The revision is comprehensive and correct. My only structural concern is the chapter's length: it has grown from ~55 min reading time to plausibly 65–75 min with §2.E added; if the spec budget matters, a future trim pass should target §2.E (which can be moved to an appendix without harming algorithmic coverage). Also, the editorial-tagging discipline ("not on the slides") is now applied to most external additions but missed in one or two places (§4.4 "Best for" row, P2-6). This is cosmetic — the trust problem from Round 1 (editorial substitutions presented as lecture content) is otherwise resolved.

**Out-of-scope observations:**
- I did not re-validate the `_shared/glossary.md` or `_shared/cross-references.md` references; those are separate artifacts.
- I did not re-validate `figures.md` (the figure catalogue) — Round 1's R1-P1.3 raised concerns there but it's a separate file.
- Lab 4 cross-references in §7 still point to `handout_lab_4/`; I assume those paths exist but did not verify.
- Forward-references to L06/L10/L11/L12 are still speculative; Round 1's P2-2 still stands.

**What PM should do next:**
1. Dispatch the L05 engineer for **one short follow-up** addressing P1-1 (~5 lines added to §5.8), P1-2 (~1 sentence in §5.4 caption), P1-3 (~1 parenthetical in §6), and P1-4 (~1 comment in §3.3 pseudocode). These are pinpoint edits, not a rewrite.
2. Run Reviewer 4 Round 3 only on the touched sections (~15 min effort) — or, if PM judges P1-1 to be P2-tier given the chapter's overall 92% PASS rate, accept the current revision and **advance to App Tester / Code Reviewer** with P1-1 logged as a known limitation in `PM/history.md`.
3. Do not re-run R1/R2/R3 on the full chapter — their Round-1 concerns are addressed by the revise-summary in scope, and re-running would not add information unless new issues are suspected.

**DOCUMENT.md updated:** N/A for QA.

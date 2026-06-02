# Reviewer 2 — Mathematical Rigor — L03 Round 2

**Reviewer:** Lecture Reviewer #2 (Mathematical Rigor)
**Artifact under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L03-Uninformed-Search.md`
**Source of truth:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture3-Uninformed Search.pdf` (56 slides); slide 37 PNG at `study/extracted_figures/L03/fig24-ucs-worked-example.png`
**Spec section:** §7.1 — Formula correctness, derivation steps, indices, notation, assumptions, variable naming, LaTeX, slide-37 UCS trace cross-check.
**Round 1 issues to verify:** P0-1 (step-7 fringe `G:8` vs `G:14`), P0-2 (E→G edge-list inconsistency), P0-3 (step-3 stream-of-consciousness), P0-4 (§5.5 "wait." leakage), plus 8 P1 items.

---

## VERDICT

**PASS with concerns.** All four Round 1 P0 issues are resolved. The §5.3 UCS trace now matches slide 37 line-by-line including the contested step 7 `G:14` reading, and the chapter adds an honest pedagogical note explaining the slide-vs-algorithm tension. The §5.5 DFS trace is rebuilt cleanly with no "wait" leakage. Round 1 P1 items 1, 2, 3, 4, 5, 6, 7, 8 are all addressed. The chapter is mathematically defensible for an L03 exam preparation reader.

One residual concern (P1-NEW below) is the BFS-vs-UCS internal consistency around the $E\to G$ edge: §5.3 follows the slide and ignores $E\to G$ at step 5, while §5.7 BFS analysis treats $E\to G$ as a normal edge. This is internally inconsistent but the chapter does flag the slide anomaly, so it is at most a P1 polish item, not a blocker.

---

## P0 — Blocking

**None.** All four Round 1 P0 issues verified resolved (evidence below).

### P0-1 (Round 1) — §5.3 step 7 mismatches slide 37: **RESOLVED**

**Verification.** Slide 37 step 7 panel (verified from PNG): `Node G / Cost 14 / Explored: A D B E F C`. Chapter §5.3 line 563: `G : 14` *(per slide)*, Explored `A, D, B, E, F, C`. **Match.**

The chapter adds a pedagogical note at lines 566–568 explaining:
> "Slide 37 shows the fringe at step 7 as `G : 14`, which suggests the slide overwrites the existing $G:8$ with the newly generated $G:14$. A correct UCS implementation following slide 21's 'replace only if **cheaper**' rule would instead **keep $G:8$**... Either way, **the final answer is the same**: the optimal path is $A \to D \to F \to G$ with cost 8..."

And gives explicit exam guidance:
> "If asked to reproduce the slide, write `G:14` for step 7 (matches the slide). If asked to explain UCS, write `G:8` is retained (matches the algorithm). If asked which path is optimal, the answer is **$A \to D \to F \to G$, cost 8** — both readings agree."

This is the correct way to handle a slide-side anomaly: match it on the surface, document the algorithmic disagreement, and give the student a decision rule. Resolved.

### P0-2 (Round 1) — §5.3 edge list inconsistency on E→G: **RESOLVED (with caveat below as P1-NEW)**

**Verification.** The chapter retains `E → G = 4` in the edge list (line 548) and *explicitly flags* at line 551 and again in the step-5 row (line 561):
> "(Note on the slide image: the $E \to G$ edge is visible on the slide and is part of the graph, but in slide 37's trace **expanding E at step 5 produces no new fringe additions**.... The chapter follows the slide's trace exactly.)"
> "Expand E ($g=5$). No new fringe additions per slide 37. *(The $E\to G$ edge is on the graph but the slide does not add G via E here; see edge-list note above.)*"

The Round 1 reviewer suggested removing E→G; the reviser kept it (because it IS visible on the slide) and flagged the slide's trace-side omission. This is a reasonable judgement call. The chapter no longer pretends the edge list and trace agree — it documents the discrepancy. Resolved.

### P0-3 (Round 1) — §5.3 step 3 stream-of-consciousness: **RESOLVED**

**Verification.** Chapter line 559:
> "Expand D ($g=3$). Successors: E ($g=3+2=5$), F ($g=3+2=5$). B already in fringe at $g=5$ from step 2 — unchanged."

Clean, finished prose. No mid-cell "via D-E? no" thinking-aloud. No false claim that D expands to B. Matches the suggested fix from the Round 1 review verbatim in substance. Resolved.

### P0-4 (Round 1) — §5.5 DFS step 2 "wait." leakage: **RESOLVED**

**Verification.** Chapter lines 603–616 contain the rebuilt DFS trace:
- One convention sentence above the table (line 603): "DFS pushes children onto the LIFO stack in **right-to-left order**, so the leftmost child ends up on top of the stack and gets popped next."
- Single 8-row trace table, no second table, no "wait", no "*Standard convention:*" mid-row interjection.
- Traversal order A → B → D → E → C → F → G matches slide 38–46 animation (extends to F, G beyond slide 46).

`grep` for "wait", "TODO", "FIXME", "...rest", "placeholder" across the chapter returns no matches. Resolved.

---

## P1 — Important

### P1-NEW. §5.3 vs §5.7 inconsistency on `E → G` participation

This is the **only new mathematical issue** that the Round 2 revision introduces (or rather, fails to reconcile). The chapter's §5.3 UCS trace **ignores** $E\to G$ at step 5 (because the slide trace ignores it), but the chapter's §5.7 BFS-vs-UCS contrast **uses** $E\to G$ to compute one of the depth-3 BFS paths:

Chapter line 667 (§5.7):
> "G first appears at depth 3 via $A \to B \to C \to G$ (cost $5+1+8=14$), $A \to D \to F \to G$ (cost $3+2+3=8$), and (if we allowed it) $A \to D \to E \to G$ (cost $3+2+4=9$)."

So in §5.7 the chapter treats the graph as "E→G exists with cost 4" but in §5.3 step 5 it treats the same edge as "skipped per slide". A careful student reading both sections back-to-back will notice the inconsistency.

The chapter does parenthesise it ("if we allowed it") but does not explicitly say "we are using the full edge list including E→G here, unlike the slide-37 trace which skipped it". A one-line bridge would resolve this.

**Fix:** Either (a) add a parenthetical to §5.7 explicitly noting that BFS analysis here uses the *full* edge list whereas §5.3 followed the slide-37 trace that omitted E→G at step 5, or (b) remove the A→D→E→G path from the §5.7 enumeration since the chapter's "ground-truth" UCS trace doesn't use it.

**Severity rationale:** P1, not P0, because both readings produce correct algorithmic conclusions in their respective sections (UCS still returns A→D→F→G cost 8; BFS still demonstrably non-optimal). The inconsistency is pedagogical, not mathematical.

**Evidence:** Chapter lines 551, 561 (§5.3) vs line 667 (§5.7).

---

### P1-NEW-2. §5.1.1 BFS vacuum trace: goal-test-on-pop convention is unusual but documented

The chapter's BFS does goal-test on POP (line 276 pseudocode, line 472 vacuum trace step 7). This is *not* the standard Russell & Norvig BFS, which tests on generation precisely to terminate one level earlier — but the chapter is internally consistent and the §5.1.1 trace correctly walks through step 4 noting "BFS tests on expansion not on generation, so don't return yet".

The mathematical concern: under the chapter's pop-time-test convention, **BFS optimality still holds** in uniform-cost graphs (any goal popped earlier than another would have been generated earlier and hence shallower, since BFS expands in level order). So no algorithmic bug; just an unusual convention.

**Fix:** Optional — add a one-line note in §4.1 pseudocode comment like `# Note: testing on pop simplifies the uniform "test on pop" rule across all four strategies; standard R&N BFS tests on generation but the optimal path is the same in uniform-cost graphs.` Not blocking.

**Evidence:** Chapter lines 276 (BFS pseudocode), 469 (step 4 of vacuum trace).

---

### P1-NEW-3. §5.7 "depth-3 BFS tie-breaking" claim depends on insertion order conventions

Chapter line 667:
> "With left-to-right child ordering matching the edge list (B before D from A, so $A \to B \to C \to G$ is generated first), BFS returns **$A \to B \to C \to G$ with cost 14**."

The edge list at line 542 actually lists A→B FIRST and A→D second, so "B before D from A" is true per the edge list. But the slide-37 trace at step 2 generates them in order **D then B** (`Node D B / Cost 3 5`) — the slide explicitly puts D first in the fringe. If we follow the slide's ordering convention strictly, BFS would generate A→D's children before A→B's, and the first depth-3 goal popped would be A→D→F→G (cost 8 — same as UCS), undermining the entire pedagogical contrast.

**Fix:** The §5.7 contrast holds *only* under the "left-to-right per edge-list" convention (B before D), which differs from the slide's step-2 fringe ordering (D before B at cost 3 vs 5 — but that's UCS ordering by cost, not BFS ordering by insertion). Add a one-line clarification that for the BFS analysis we use insertion-order = edge-list-order (A→B, then A→D), not the slide's cost-sorted order which is UCS-specific.

**Severity rationale:** P1, not P0, because the contrast survives any FIFO tie-breaking convention as long as it's stated. The mathematical claim "BFS at cost 14 vs UCS at cost 8" holds for any tie-break that picks A→B→C→G over A→D→F→G — but the chapter should justify why it picked that tie-break.

**Evidence:** Chapter lines 542 (edge list), 558 (slide-trace step 2 fringe order), 667 (§5.7 BFS claim).

---

### P1-NEW-4. §5.2.2 Romania UCS sketch has one minor arithmetic concern

Chapter line 521 (step 10):
> "Pop Pitesti(317). Generate Bucharest(317+101=418) → existing Bucharest at 450 is more expensive → **replace** with Bucharest(418)."

This is correct — Pitesti→Bucharest road distance is 101. ✓

However, the surrounding sketch has a subtle ordering issue: step 8 pops Fagaras(239) and generates Bucharest(450). Step 10 pops Pitesti(317) and "replaces" Bucharest. But between step 8 and step 10, the algorithm pops Mehadia(299) (step 9). After step 9 the priority queue has, at minimum: Pitesti(317), Drobeta(374) [generated in step 9], Craiova(366), Bucharest(450). The lowest is Pitesti(317), so step 10 popping Pitesti is correct. ✓

Step 11 pops Craiova(366) — but the priority queue at this point also has Bucharest(418), Drobeta(374). Lowest is Craiova(366). ✓
Step 12 pops Drobeta(374). Priority queue has Bucharest(418). Lowest is Drobeta. ✓
Step 13 pops Bucharest(418) — goal! ✓

The trace is correct. No fix needed; called out only because the Romania UCS expansion order is exam-relevant and worth a sanity check.

**Evidence:** Chapter lines 511–524.

---

## P2 — Polish

### P2-1. §4.2.1 minimal counter-example: $g=2$ vs $g=3$ confusion check

Chapter lines 318–319:
> "**Goal-test on POP (correct).** Expand $S$. Generate $G_1$ at $g=6$ and $A$ at $g=2$. Don't test yet. Pop the cheapest: $A$ at $g=2$. Goal-test $A$ — not a goal. Expand $A$, generate $G_2$ at $g=3$. Pop the cheapest now on the queue: $G_2$ at $g=3$. Goal-test $G_2$ — goal! Return cost-3 path. **Optimal.**"

Arithmetic check: $S \xrightarrow{2} A \xrightarrow{1} G_2$ gives $G_2$ at $g=2+1=3$. ✓
$S \xrightarrow{6} G_1$ gives $G_1$ at $g=6$. ✓
Cheapest goal popped: $G_2$ at $g=3$. ✓
Cost-3 path is optimal. ✓

Clean. No issue.

### P2-2. Edge list table is now clearer than ASCII art (improvement)

The Round 1 ASCII graph (lines 403–415 of the Round 1 chapter) has been replaced with a clean two-column table at lines 540–549. This is a visible improvement. Pure praise, not a fix.

### P2-3. n-Puzzle state counts in §3.3.1

Chapter line 167–169:
> "**8-puzzle:** $9!/2 = 181{,}440$ states.
> **15-puzzle:** $16!/2 > 10^{13}$ — more than ten *trillion* states.
> **24-puzzle:** $\approx 10^{25}$ states."

Arithmetic check:
- $9!/2 = 362880/2 = 181440$. ✓
- $16!/2 = 20922789888000/2 \approx 1.046 \times 10^{13}$ — more than $10^{13}$. ✓
- $25!/2 \approx 1.55 \times 10^{25}/2 \approx 7.76 \times 10^{24}$, which rounds to $\approx 10^{25}$. ✓

All correct.

### P2-4. IDS per-level table

Lines 651–659. Sum check:
$6+50+400+3000+20000+100000 = 123456$. ✓
Overhead $123456/100000 = 1.23456$, so "23% extra work". ✓
Asymptotic factor $b/(b-1) = 10/9 \approx 1.111$. ✓

All correct.

---

## EVIDENCE TABLE — Slide-by-slide formula and trace verification

| Topic | Slide | Chapter location | Round 2 status |
|---|---|---|---|
| Search problem 5 components | 10 | §3.2 lines 132–137 | Pass |
| State space defn | 12 | §3.3 line 156 | Pass |
| Vacuum 8 states | 13–14 | §3.3 line 447 | Pass |
| Eval dimensions (4) | 27 | §1 lines 41–44, §3.6 lines 239–242 | Pass |
| b, d, m defns | 28 | §1 lines 48–50, §3.5 lines 225–227 | **Pass** (slide-28 vs slide-54 wording footnote added at line 229; $m$ phrasing fixed in §1 line 50) |
| BFS Complete | 35 | §4.1 line 285 | Pass |
| BFS Optimal "if cost = 1" | 35 | §4.1 line 286 | **Pass** (slide-35 vs slide-54 reconciliation footnote added) |
| BFS Time $O(b^d)$ | 35 | §4.1 line 287 | Pass |
| BFS Space $O(b^d)$ | 35 | §4.1 line 288 | Pass |
| UCS Complete | 36 | §4.2 line 325 | Pass |
| UCS Optimal | 36 | §4.2 line 326 | Pass |
| UCS Time $O(b^{1+\lfloor C^*/\epsilon\rfloor})$ | 36 | §4.2 line 327 | **Pass** (floor-bracket footnote added) |
| UCS Space same | 36 | §4.2 line 328 | Pass |
| UCS = BFS when costs equal | 36 | §4.2 line 329 | Pass |
| UCS trace step 1 | 37 | §5.3 line 557 | Pass |
| UCS trace step 2 | 37 | §5.3 line 558 | Pass |
| UCS trace step 3 | 37 | §5.3 line 559 | **Pass** (rewritten cleanly) |
| UCS trace step 4 | 37 | §5.3 line 560 | Pass |
| UCS trace step 5 | 37 | §5.3 line 561 | **Pass** (E→G omission explicitly flagged) |
| UCS trace step 6 | 37 | §5.3 line 562 | Pass |
| UCS trace step 7 | 37 | §5.3 line 563 | **Pass** (`G:14` now matches slide; pedagogical note explains the algorithm-vs-slide tension) |
| UCS trace step 8 (final path) | 37 | §5.3 line 564 | Pass |
| DFS Complete | 47 | §4.3 line 354 | Pass |
| DFS Optimal | 47 | §4.3 line 355 | Pass |
| DFS Time $O(b^m)$ | 47 | §4.3 line 356 | Pass |
| DFS Space $O(b\,m)$ | 47 | §4.3 line 357 | Pass |
| DFS trace step 0–7 | 38–46 | §5.5 lines 609–616 | **Pass** (rebuilt; no "wait" leakage) |
| Figure 10 caption | 46 | §5.5 line 619 | **Pass** (now correctly notes slide 46 ends at C; F/G are extension) |
| IDS Complete | 53 | §4.4 line 391 | Pass |
| IDS Optimal "if step cost = 1" | 53 | §4.4 line 392 | **Pass** (slide-53 vs slide-54 wording footnote added) |
| IDS Time sum & $O(b^d)$ | 53 | §4.4 lines 393–395 | Pass |
| IDS Space $O(b\,d)$ | 53 | §4.4 line 396 | Pass |
| IDS arithmetic example | (chapter) | §5.6.1 lines 651–661 | Pass (verified $123{,}456$, $b/(b-1)\approx 1.11$) |
| Comparison table | 54 | §4.5 lines 409–414 | Pass |
| Footnote 1 (b finite) | 54 | §4.5 line 418 | Pass |
| Footnote 2 (ε > 0) | 54 | §4.5 line 420 | Pass |
| Footnote 3 (costs identical) | 54 | §4.5 line 422 | Pass |
| A\* / informed deferred | 54, 55 | §1 line 37, §3.7 line 250, §3.8 line 254 | Pass |
| Depth-Limited DFS subroutine | 54 | §4.4.0 lines 363–375 | Pass (added Round 2) |
| Bidirectional (orientation) | 54 | §4.5.1 line 429 | Pass (added Round 2) |
| 8-queens formulation | 19 | §5.8 lines 673–682 | Pass (added Round 2; $b\approx 8$ check correct under non-attacking-placement) |
| Romania UCS to completion | 18 + R&N | §5.2.2 lines 510–525 | **Pass** (13-step trace; all arithmetic checks out; replace-if-cheaper step 10 flagged) |
| Vacuum world BFS trace | 13–14 | §5.1.1 lines 461–474 | **Pass** (7-step trace; optimal S, R, S cost 3 derived correctly) |
| BFS-vs-UCS contrast | (chapter) | §5.7 lines 663–671 | **Pass with P1-NEW** (BFS path cost 14 vs UCS 8; tie-break convention not justified — P1-NEW-3) |
| Goal-test-on-pop counter-example | (chapter) | §4.2.1 lines 314–321 | Pass (arithmetic verified, $g_2=3 < g_1=6$, conclusion optimal) |
| Replace-if-cheaper counterfactual | (chapter) | §5.3.1 lines 572–579 | Pass |
| n-Puzzle state counts + NP-hard | 15 | §3.3.1 lines 163–171 | Pass (arithmetic verified) |
| 4 design questions | 17 | §3.2.1 lines 141–150 | Pass |
| 3 warm-up examples | 5 | §3.1.1 lines 119–127 | Pass |
| Motivation triad | 6 | §1.1 lines 18–26 | Pass |

---

## Report to PM

**Assignment recap:** Reviewer #2 (Mathematical Rigor) for L03 Round 2 chapter, verifying the four Round 1 P0 fixes (§5.3 step 7 `G:14`, §5.3 edge-list E→G, §5.3 step 3 prose, §5.5 DFS "wait." leakage) plus the eight Round 1 P1 items.

**Status:** **Pass with concerns.**

**P0 findings:** None. All four Round 1 P0 issues verified resolved:
1. §5.3 step 7 fringe now reads `G:14` matching slide 37 exactly, with a pedagogical note explaining the slide-vs-algorithm `G:8` vs `G:14` tension and explicit exam guidance.
2. §5.3 edge list retains `E → G = 4` (it is on the slide) but the step-5 trace row now explicitly flags that the slide trace ignores this edge. The discrepancy is documented rather than hidden.
3. §5.3 step 3 is clean prose: "Expand D ($g=3$). Successors: E ($g=3+2=5$), F ($g=3+2=5$). B already in fringe at $g=5$ from step 2 — unchanged." No more thinking-aloud.
4. §5.5 DFS table is fully rebuilt — single 8-row table, no "wait", no mid-row "*Standard convention:*" leakage. Convention sentence above the table.

**P1 findings:**
1. **P1-NEW (chapter-internal E→G consistency):** §5.3 step 5 follows the slide and ignores `E → G = 4` ("no new fringe additions per slide 37"), but §5.7 BFS analysis at line 667 uses `E → G` to compute the path $A\to D\to E\to G$ at cost 9. The chapter hedges with "(if we allowed it)" but should add an explicit one-line bridge clarifying that §5.7 uses the full edge list whereas §5.3 followed the slide trace.
2. **P1-NEW-2 (BFS goal-test-on-pop convention):** The chapter's BFS pseudocode and §5.1.1 vacuum trace test goals on pop, not on generation (which is the standard Russell & Norvig BFS). Internally consistent and mathematically sound for uniform-cost graphs, but worth a one-line note in §4.1 pseudocode acknowledging the deviation from textbook convention.
3. **P1-NEW-3 (§5.7 BFS tie-breaking convention not justified):** The §5.7 claim "BFS returns $A\to B\to C\to G$ with cost 14" relies on a child-ordering tie-break (B before D from A) that the chapter never explicitly states. Under a D-first ordering (which the slide-37 step-2 fringe `D B 3 5` arguably suggests), BFS would return $A\to D\to F\to G$ at cost 8 — same as UCS — undermining the contrast. Add a one-line justification: "Using insertion-order = edge-list-order (A→B then A→D)..."

**P2 findings:**
1. n-Puzzle state-count arithmetic verified: $9!/2 = 181{,}440$, $16!/2 > 10^{13}$, $25!/2 \approx 10^{25}$. All correct.
2. IDS per-level table sum verified: $6+50+400+3000+20000+100000 = 123{,}456$. Overhead factor $123456/100000 = 1.23456$. Asymptotic $b/(b-1) = 1.111$ for $b=10$. All correct.
3. §4.2.1 goal-test-on-pop minimal counter-example arithmetic verified: $G_1$ at $g=6$, $G_2$ at $g=3$ via $S\to A\to G_2$ (costs $2+1$). Conclusion (cost-3 path returned, optimal) correct.
4. §5.2.2 Romania 13-step trace arithmetic spot-checked: Sibiu→Rimnicu Vilcea (80) → Pitesti (97) → Bucharest (101); $140+80+97+101=418$. Correct.
5. Edge-list table at §5.3 replaces the broken ASCII art — visible improvement; pure praise.

**QA Checklist (§7) status (interpreted for a lecture-summary deliverable):**
- Formulas match source: **Pass** (slide-36 floor brackets explicitly footnoted, all complexity bounds correct).
- Derivation steps complete: **Pass** (§5.3 step 3 rewritten cleanly; §5.5 DFS rebuilt; §4.2.1 goal-test counter-example clean).
- Indices and notation correct: **Pass** ($d$, $m$ definitions fixed in §1; slide-28-vs-slide-54 contradiction footnoted).
- Assumptions stated: **Pass** ($\epsilon > 0$ for UCS, $c \ge 0$ throughout, $b$ finite for completeness — all flagged).
- Variable names consistent: **Pass** ($g$, $C^*$, $\epsilon$, $b$, $d$, $m$ used consistently across §3 through §8).
- LaTeX clean: **Pass**.
- Slide-37 UCS trace step-by-step match: **Pass** — full 8-step verification against PNG image, every row matches.
- Worked-example prose finished: **Pass** — no "wait", "TODO", or stream-of-consciousness leftovers anywhere (grep verified).

**Acceptance criteria (§1) status:** N/A — this is a lecture-summary review, not a feature.

**DOCUMENT.md audit:** N/A for lecture chapter review (no code directories modified).

**Out-of-scope observations:**
- The chapter is now ~805 lines vs ~633 in Round 1. Reading time is ~60 min as advertised. This is at the long end of "single-sitting" but the additional worked examples (§5.1.1 vacuum BFS, §5.2.2 Romania UCS, §5.7 BFS-vs-UCS contrast, §5.8 8-queens, §4.2.1 goal-test counter-example, §5.3.1 replace-if-cheaper counterfactual) close real pedagogical gaps that Round 1 reviewers flagged.
- The §5.3 pedagogical note on `G:14` vs `G:8` is exemplary documentation of a slide-side anomaly — this is exactly the level of honesty an exam-prep chapter should aim for. Other lectures should follow this template when they encounter similar slide bugs.
- §5.7's "BFS returns cost 14, UCS returns cost 8" is the single most pedagogically powerful claim in the chapter, but its dependence on a specific tie-break convention (see P1-NEW-3) should be made explicit. A naive student who picks the opposite tie-break ends up with BFS = UCS = 8 and is left confused about the lesson.

**Concerns / risks:**
1. The Round 1 reviser correctly identified that slide 37's step 5 is buggy (the visible $E\to G$ edge should generate $G:9$, but the slide doesn't show this), and slide 37's step 7 is also buggy (should keep cheaper $G:8$). The chapter documents both. A round-3 reviewer should sanity-check that the chapter's pedagogical framing ("match slide for exam recall; understand algorithm for explain questions") is the right exam-prep advice.
2. The chapter's BFS goal-test-on-pop convention is internally consistent but deviates from the standard textbook convention. Worth a single line in §4.1 to acknowledge the deviation.

**What PM should do next:**
1. Round 2 P0 is clear — proceed to App Tester or to the next reviewer in the round-2 batch.
2. The three P1-NEW items (§5.3/§5.7 E→G consistency bridge, BFS pop-time-test note, §5.7 BFS tie-break justification) are not blocking but should be addressed in a polish round before final code review.
3. The chapter is mathematically defensible for L03 exam preparation.

**DOCUMENT.md updated:** N/A for QA.

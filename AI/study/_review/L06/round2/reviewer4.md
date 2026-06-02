# L06 Round 2 — Reviewer #4 (Exam Readiness)

**Reviewer role:** Lecture Reviewer #4 — Exam Readiness (Spec §7.1).
**Source artifact:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture6-Adversarial Search.pdf` (42 slides), cross-checked against the page-render PNGs in `study\extracted_figures\L06\`.
**Chapter under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L06-Adversarial-Search.md` (630 lines, post-revision).
**Round 1 baseline:** 3 P0 (Poker fabrication, tic-tac-toe utility convention wrong, AlphaGo year + expectiminimax + complexity claims unsourced) + 10 P1 + 12 P2.
**Mandate:** Verify Round 1 P0/P1 fixes; be harsh on anything new or still wrong.

---

## VERDICT

**PASS WITH ONE RESIDUAL P0 + a handful of P1/P2.**

The three primary Round 1 P0s have been **fully fixed and verified against the slide-render PNGs**: Poker is gone from the slide-5 taxonomy, the tic-tac-toe utility convention is now correctly stated as {−1, 0, +1} (slide 8) with the coins game's {0, 1} (slide 17) explicitly split out, and the quantitative alpha-beta complexity claims (`O(b^{d/2})`, `O(b^d)`, "twice as deep") are now consistently flagged as R&N-supplementary throughout §3.3.1, §4.3, §4.4, §4.7, §5.4, §6 (pitfall 4), and §8 (cheat-sheet + checklist). The unsourced AlphaGo "2016" date and the four-case expectiminimax piecewise formula are now both explicitly tagged "chapter elaboration, not on slide". The cheat-sheet pseudocode now correctly distinguishes `UTILITY` at true terminals from `EVAL` at the depth-limit horizon. The glossary header is now meaningfully complete.

**However, one residual P0 survives Round 1's P1-5 / Round 2's P0-fix #8.** The chapter's Round 2 revision of Figure 8's caption asserts that slide 28 and slide 35 show the *"same 9-leaf tree"*. They do not. Slide 28's right-MIN has leaves **14, 5, 2** (all three visible and labelled, backed up to β = 2). Slide 35's right-MIN backs up to **β = 1**, which is arithmetically impossible from the leaves {14, 5, 2}. Slide 35 must therefore have at least one different leaf value (the second leaf is 1, not 5). The chapter's new wording — *"Slide 35 only labels the leaves the sweep actually visits — leaves whose values do not influence the pruning logic are drawn but left unlabelled"* — does not save the claim: if the unlabelled leaves were 5 and 2 (as on slide 28), the right-MIN would back up to β=2, not β=1. **This is the same factual error Round 1 flagged, restated in a more confident form.**

Round 2 is therefore one residual P0 short of ready-to-ship.

---

## ROUND 1 → ROUND 2 STATUS BOARD

| # | Round 1 P0 | Round 2 status | Evidence |
|---|---|---|---|
| 1 | Poker in slide-5 taxonomy | **FIXED** | Line 97 table now reads `Imperfect/Stochastic → Scrabble, Bridge` (no Poker). Line 99 explicitly states "Slide 3 also mentions Poker as a motivating modern AI benchmark, but it does **not** appear in slide 5's 2×2 taxonomy table". Verified against page05-render.png. |
| 2 | Tic-tac-toe utility "0 = MIN won or draw" | **FIXED** | Lines 119–122 now split the two conventions explicitly: slide 8 uses {−1, 0, +1} with 0 = draw (bolded in Figure 2 caption at line 127); slide 17 uses {0, 1}. Verified against page08-render.png and page18-render.png. |
| 3 | Alpha-beta complexity attributed to slides | **FIXED** | §4.3 (lines 309–317) now opens with *"The lecture itself gives no quantitative complexity bound for alpha-beta"* and explicitly tags the `O(b^{d/2})` best and `O(b^d)` worst as `[R&N 3e §5.3 — supplementary, not in slides]`. §5.4 line 504 and §8 checklist line 624 also marked supplementary. The `O(b^{3d/4})` "average case" claim is **removed**. |
| 4 | AlphaGo year + expectiminimax formula attributed to slides | **FIXED** | §4.6 line 349 explicitly prefaces the piecewise formula with *"the slide itself only states the chance-node case in words"*. §4.7 line 377 tags AlphaGo year as "chapter elaboration, not on slide"; §4.7 line 378 tags "AlphaStar" similarly; §4.7 line 374 splits Stockfish (alpha-beta + NNUE) from Leela (MCTS) and tags as chapter elaboration. |

| # | Round 1 P1 | Round 2 status |
|---|---|---|
| P1-1 | Glossary header incomplete | **FIXED** — line 5 now lists game tree, MAX/MIN node, minimax strategy, depth-limited search / search horizon / cut-off node, move ordering, ply, chance node, expectiminimax, Monte Carlo simulation, transposition table, forward pruning. |
| P1-2 | `O(bd)` space complexity unsourced | **FIXED** — line 173 explicitly states "Slide 19 does not state space complexity; this is the standard L03 DFS analysis applied here." |
| P1-3 | Expectiminimax row of comparison table used unsupported `O(b^d · n^d)` | **FIXED** — line 326 row reads `"not given by slides"` with footnote ‡ at line 328 clarifying. |
| P1-4 | §5.2 right-MIN cutoff fired but pruned nothing | **FIXED** — line 449 frame 26–27 now ends *"in this case all three children have already been examined… the only difference is that there are no remaining children left to skip, so the prune saves no work in this particular ordering."* Left-to-right DFS ordering also stated up front at line 442. |
| P1-5 | Slide 28 vs 35 "same tree" | **NOT FIXED** — see P0-NEW below. The chapter swung from "different tree" (Round 1) to "same tree" (Round 2). Both are wrong; the truth is "same structure (9 leaves total = 3+3+3), but with at least one different leaf value because slide 35's right-MIN β = 1 is unreachable from slide 28's leaf values {14, 5, 2}." |
| P1-6 | U(s) overloaded for terminal utility AND Eval | **FIXED** — line 184 "Notational discipline" paragraph reserves $U(s)$ for true terminal utility and $\text{Eval}(s)$ for cut-off heuristic. The §3.4 line 169 "sometimes also written $U(s)$" phrase is gone. Pitfall 8 (line 519) reinforces. (Caveat: slide 30 itself uses "Utility" as the label for the heuristic — see new P2 below.) |
| P1-7 | "Twice as deep" claim not in slides | **FIXED** — labelled supplementary at line 311 and 504. |
| P1-8 | Cheat-sheet checklist "the one thing" | **FIXED** — line 624 softened to *"Can I explain how the order in which children are expanded affects the number of nodes alpha-beta visits? (move ordering — R&N supplementary; lecture itself does not quantify this)"*. |
| P1-9 | Zero-sum imprecise phrasing | **FIXED** — §3.5 line 208 rewritten: *"Zero-sum is what lets us fold both utilities into a single number (MAX's utility, since MIN's is determined as constant − U_MAX) and measure everything from MAX's perspective."* Matches slide 6's framing. |
| P1-10 | Completeness/optimality unattributed | **FIXED** — line 175 *"completeness and space are L03 cross-references, not stated on L06 slides"*; line 313 *"the lecture itself does not formally analyse these properties for game trees"*. |

| # | Round 1 P2 | Round 2 status |
|---|---|---|
| P2-1 | Forward-ref to L07 before student has L07 | **FIXED** — line 13 "in upcoming material on Constraint-Satisfaction Problems". |
| P2-2 | $10^{123}$ cited 4× | **PARTIALLY FIXED** — now appears at lines 51, 498, 625. Down from 4 to 3. Acceptable. |
| P2-3 | `Successors` notation inconsistent | **NOT FIXED** (explicitly deferred per revise-summary). Still varies between `Successors(s)` (line 142), `SUCCESSORS(state)` (line 226), `Succ(s)` (line 565). Minor; left alone. |
| P2-4 | xkcd 832 inclusion contradictory | **NOT FIXED** (explicitly deferred). Acceptable. |
| P2-5 | "DAG search" undefined | **NOT FIXED** (explicitly deferred). Acceptable. |
| P2-6 | §6 pitfall 4 claiming slides 28 and 35 are different trees | **REWRITTEN** but now says they "walk the same 9-leaf abstract tree" — which is the SAME residual factual error as P0-NEW below. |
| P2-7 | L09a / L10 cross-ref section numbers | **DEFERRED** to cross-link review round (acceptable). |
| P2-8 | α "(≥ floor)" parenthetical | **FIXED** — line 614 now says "a **lower bound** (floor) on MAX's final achievable value". |
| P2-9 | §5.1 coins-game table too dense | **FIXED** — line 416 table rewritten as bottom-up sub-state-by-sub-state, with explicit note (line 427) that slide 18's left-to-right edge order differs from the table's by-size order. |
| P2-10 | Stockfish/Leela conflation | **FIXED** — line 374 splits them correctly. |
| P2-11 | "15 distinct movement-effects after symmetries" | **FIXED** — line 364 now reads "6 doubles + 15 non-double pairs". |
| P2-12 | 35-min reading time optimistic | **FIXED** — line 3 now says "~60–90 min". |

---

## P0 — Residual / new

### P0-NEW. Slide 28 vs slide 35 "same 9-leaf tree" claim is still factually wrong against the source images.

- **Where in chapter:** Figure 8 caption (line 460) — *"The same 9-leaf tree as Figure 7 (slide 28), re-annotated with explicit α/β values"*. Reinforced in body text at line 462: *"On slide 28's left-to-right ordering: … right MIN expands all 3 children (14, 5, 2). … Slide 35's annotation reflects the same algorithm on the same tree but emphasises a slightly different sweep where the right MIN's second child also triggers a cutoff at β = 1."* And again in §6 pitfall 4 at line 515.
- **Source (verified by direct inspection of page28-render.png and page35-render.png):**
  - Slide 28's right MIN has *three* triangle leaves drawn, *all labelled*: **14, 5, 2**. Backed up to **2**.
  - Slide 35's right MIN has *three* triangle leaves drawn, but only the *first two* labelled: **14, 1**. Backed up to **β = 1, prune!**
- **Why the "same tree" claim cannot stand:** The minimax value of the right MIN, taking the minimum over its children, must be ≤ the smallest child. If the children were {14, 5, 2} (slide 28's set), the smallest is 2, so β at this MIN can only reach 2 — never 1. For slide 35's β=1 to arise, **at least one leaf value must differ from slide 28's set**. The most parsimonious explanation: slide 35's right-MIN children are (14, 1, _) — i.e. the *second* leaf has changed from 5 to 1. That makes them **different trees**.
- **Why the chapter's escape-hatch wording doesn't work:** The chapter argues "slide 35 only labels the leaves the sweep actually visits — leaves whose values do not influence the pruning logic are drawn but left unlabelled". If that were true, the unlabelled leaves on slide 35's right MIN would have the values 5 and 2 (slide 28's missing values), and β would still bottom out at 2 — contradicting slide 35's explicit "β = 1, prune!".
- **Why this is P0 (not P1):** The chapter is **affirmatively asserting** that slide 35 shows the same tree as slide 28, and providing a (incorrect) explanation for the visible discrepancy. A student studying for an exam who reads this chapter will (a) believe the leaves are 14, 5, 2 on slide 35 just as on slide 28, and (b) be unable to reproduce the "β=1, prune!" annotation when working the example by hand. The chapter has *guaranteed* exam confusion on a directly-citable question. This was also flagged in Round 1 P1-5; the Round 2 fix went the wrong direction (claiming "same tree" instead of "different tree"), creating a stronger version of the same error.
- **Suggested fix:**
  - Option A (recommended, honest): Re-caption Figure 8 as *"A variant of the same tree topology (root MAX, three MIN children, three leaves each). Slide 35 uses **different leaf values** under the middle and right MINs (specifically: middle MIN's first child is 2 as in slide 28, but its other two children are not labelled; right MIN's first two children are 14 and 1 — different from slide 28's 14 and 5 — and the third is not labelled). This is deliberate: with these values, two cutoffs fire instead of one, demonstrating that alpha-beta savings can vary substantially with leaf values / move ordering."*
  - Option B (cheaper): Add an explicit warning *"⚠ slide 28 and slide 35 are visually similar but slide 35 has different leaf values under the right MIN (it would have to, to produce β=1). Do not try to reproduce slide 35's annotations from slide 28's leaves — they will not match."*
  - Rewrite §6 pitfall 4 (line 515) to drop the "walk the same 9-leaf abstract tree" assertion. Move ordering changes the prune *set* on a fixed tree; what slides 28 and 35 illustrate is more like "different trees, different prune counts" — the move-ordering pedagogy is *not* what the slides themselves demonstrate.

---

## P1 — Important issues (new in Round 2 review)

### P1-NEW-1. The "Sanity check on an empty board" for tic-tac-toe Eval is correct but the algebra in line 194 is non-obvious and slightly mis-presents the centre-move case.

- **Where:** line 194, §3.4. *"After X plays the centre, the 4 lines through the centre (1 row, 1 column, 2 diagonals) are still open for X (no O on them) but no longer open for O (each contains an X), while the remaining 4 lines are open for both. Open-for-X = 8, open-for-O = 4, so Eval = 8 − 4 = 4."*
- **Issue:** The four "remaining" lines (the two non-middle rows and the two non-middle columns) are open for *both* X and O (neither contains a mark), so they contribute equally to both terms and cancel — that's correct. But the chapter's phrasing "Open-for-X = 8, open-for-O = 4" is *the cumulative count after summing* — it sounds like *each* of the 8 lines is open for X, which is also actually true here (X has only one mark, in a cell that is on 4 lines, and those 4 lines are still open for X because there's no O on them; the other 4 lines are open for X because they contain no marks at all). OK on closer reading the chapter is correct — but the prose is dense and easy to misread. A diligent student counting "lines open for X = lines containing no O" might conclude **all 9 cells minus zero** … wait that doesn't parse either. The chapter's calculation is right; the prose just needs a worked sub-table.
- **Why P1:** Pedagogically dense. Risk: students misread the sanity check and conclude their own counts are wrong when in fact the chapter is right.
- **Suggested fix:** Add a small 8-row table listing each line (top row / middle row / bottom row / left col / middle col / right col / main diag / anti-diag), what marks it contains after X-centre, whether it's open for X, whether it's open for O. Final two columns each sum to 8 and 4 respectively.

### P1-NEW-2. The chapter introduces "$U_{\text{MAX}}$" notation in §3.5 (line 208) without ever defining it.

- **Where:** line 208. *"Zero-sum is what lets us **fold both utilities into a single number** (MAX's utility, since MIN's is determined as $\text{constant} - U_{\text{MAX}}$)…"*
- **Issue:** $U_{\text{MAX}}$ is used precisely once and never appears in the §8 symbols glossary. The reader has to infer that this is the same $U(s)$ used elsewhere — but with a "MAX" subscript, the obvious reading is "*some other quantity*, the part of $U$ that belongs to MAX". This is consistent with $U(s)$ everywhere else once you decode it but the notation is unintroduced.
- **Why P1:** A student building flashcards from the symbol glossary (line 605–615) will not find $U_{\text{MAX}}$ there and will not know whether it is a defined symbol or a one-off.
- **Suggested fix:** Either (a) replace $U_{\text{MAX}}$ with $U(s)$ at line 208 (the chapter convention everywhere else), or (b) add $U_{\text{MAX}}, U_{\text{MIN}}$ to the §8 symbols glossary with the explicit identity $U_{\text{MAX}}(s) + U_{\text{MIN}}(s) = \text{constant}$ for zero-sum games.

### P1-NEW-3. Chapter's "Notational discipline" in §3.4 ($U$ for terminal utility, Eval for heuristic) contradicts slide 30's actual notation.

- **Where:** §3.4 line 184 — chapter insists $U$ and Eval are kept strictly separate.
- **Source (verified against page30-render.png):** Slide 30 itself labels the heuristic formula `"Utility = X's open lines − O's open lines"`. The slide author uses the word **Utility** for the heuristic evaluation function. Not "Eval". The chapter's discipline is opposite to what the slide does.
- **Issue:** Round 1 P1-6 was reported as "the chapter overloads U(s) for both true utility AND evaluation". The chapter's Round 2 fix imposes a clean separation that is pedagogically *better* than the slide — but in doing so the chapter is silently departing from slide-30's terminology. A strict-slide exam question of the form "what does slide 30 call the function X's open lines − O's open lines?" — the slide-grounded answer is "**Utility**", but the chapter has trained the student to answer "Eval".
- **Why P1 (not P0):** The chapter's discipline is the standard R&N convention and is more correct; slide 30's "Utility" for the heuristic is genuinely sloppy slide design. But the chapter never *flags* the discrepancy. It should.
- **Suggested fix:** Add one explicit sentence in §3.4 around line 196 (already-present "Editorial note: slide 30 gives the formula without defining 'open line'…"). Expand to: *"Editorial note: slide 30 labels the formula 'Utility = X's open lines − O's open lines', but this is the **heuristic estimate at a cut-off non-terminal node**, not the rule-given utility at a true terminal. This chapter keeps the cleaner R&N terminology (Eval for the heuristic, U for the terminal utility); slide 30's labelling is unintentionally ambiguous on this point. See §6 pitfall 8."*

### P1-NEW-4. §5.4 "branching-factor reality check" uses $35^{80}$ where slide 7's "80 ply" deserves a clarification.

- **Where:** lines 496–498. *"$35^{80} \approx 10^{123}$ nodes for chess searched to the typical end."*
- **Issue:** $35^{80}$ is the number of *leaf-level* nodes if the tree branches uniformly with $b=35$ at every ply for 80 plies. It is **not** the total node count (which would be $\sum_{i=0}^{80} 35^i \approx \frac{35^{81}-1}{34}$, also $\approx 10^{123}$, so the order of magnitude survives). The chapter and slide both say "nodes" which is the right magnitude but technically loose. More importantly: 80 ply is the *length of an average chess game in half-moves*, not the depth at which exhaustive search becomes impossible. Exhaustive minimax search would have to look at trees of depth comparable to game length, which is what motivates the $10^{123}$ figure.
- **Why P1:** Chapter line 504 doubles down: *"with $b = 35$ and the standard R&N best-case result $O(b^{d/2})$ (supplementary, §4.3), alpha-beta can search to roughly twice the depth of minimax in the same time budget."* — applying $O(b^{d/2})$ to "twice the depth" is fine, but only if $b^{d/2}$ is a count of *leaves* (in which case "depth" here is leaves-as-deep-as). A student tying together the $35^{80}$ figure with the "twice as deep" claim might write "alpha-beta could search to depth 160 in chess" which is meaningless.
- **Suggested fix:** Add a clarifying parenthetical at line 498: *"(this is approximately the total number of distinct game-tree nodes; the total tree size is dominated by the leaves, $35^{80}$)"*, and clarify §5.4 by linking the "twice as deep" framing to "the depth alpha-beta can practically search" not to the $d=80$ figure.

### P1-NEW-5. §5.2 Frame 25 leaf count: "Those two leaves are *pruned*" leaves out the implicit assumption that "leaves" means "MAX-leaves of the middle MIN".

- **Where:** line 448, §5.2 Frame 25. *"the leaves 4 and 6. Those two leaves are pruned."*
- **Issue:** Earlier in §5.2 the chapter says left-to-right DFS ordering is assumed (line 442). On slide 11's tree, the middle MIN's children are $c_1, c_2, c_3$ with leaves 2, 4, 6. Left-to-right means visit 2 first; pruning fires after seeing 2; so the un-visited leaves are 4 and 6 — but the chapter's prose claim "Those two leaves are pruned" is technically true only under the left-to-right assumption. A student doing the same example right-to-left (perfectly valid expansion order) would see 6 first, get β=6 > α=3, continue to 4, get β=4 > α=3, continue to 2, β=2 ≤ α=3, then prune nothing because the middle MIN is fully expanded.
- **Why P1:** Same issue as Round 1 P1-4 — the chapter is correct under its stated ordering but doesn't double-emphasise the dependency. Round 2 added the upfront DFS-order statement (line 442), which is the right fix; but the inline frame walkthrough still says "Those two leaves are pruned" as if it were ordering-independent.
- **Suggested fix:** At line 448, say *"Those two leaves are pruned under the assumed left-to-right ordering — re-expanding right-to-left would yield a different prune set."*

### P1-NEW-6. The cheat-sheet's "Sensitive to move ordering? **YES**" property table row (line 603) is R&N-supplementary content that the cheat sheet does NOT label as such.

- **Where:** §8 line 603 "Properties at a glance" table.
- **Issue:** The cheat-sheet is supposed to be the night-before-exam single page. Every move-ordering claim in §4.3 / §6 pitfall 4 / §5.4 has been carefully tagged "R&N supplementary, not in slides". But line 603 quietly drops the tagging — it just says *"**YES** (this is the only way it pays off)"* — re-introducing R&N content as if it were slide content, exactly the class of error that Round 1's P0-3 was about.
- **Why P1:** A student cramming from the cheat sheet would not see the supplementary tag and could carry the wrong impression into the exam.
- **Suggested fix:** Change line 603 to *"**YES** (R&N supplementary; the lecture does not introduce move ordering as a knob)"*.

### P1-NEW-7. The §1 question-list answer pointers reference "§5.3 worked example" for evaluation functions but §5.3 is about *alpha-beta with* an evaluation function, not the evaluation function itself.

- **Where:** line 26 — *"**What do we do when the tree is still too deep to search to the end?** → Evaluation functions and depth-limited search. (§3.4 definition, §5.3 worked example)"*.
- **Issue:** §5.3 is titled *"Alpha-beta with an evaluation function — depth-limited tic-tac-toe"*. The student following the §1 → §5.3 link expecting a clean worked example of *evaluation* (e.g. compute Eval(s) on three different tic-tac-toe positions to build intuition) will instead get alpha-beta's pruning logic. The standalone evaluation worked example is the empty-board sanity check at §3.4 line 194, but that's not in §5.
- **Why P1:** Minor navigation friction. The cleanest fix is to *expand* §5.3's setup to include the explicit Eval computations on each board it draws, or to drop the §5.3 link from the §1 question pointer.
- **Suggested fix:** Either (a) make §5.3 also explicitly compute Eval on each board it draws, or (b) change the §1 line 26 pointer to *"§3.4 definition + sanity check; §5.3 worked example combining Eval with alpha-beta on a depth-limited tree"*.

---

## P2 — Polish

### P2-NEW-1. Figure 4 caption (line 271) says *"two MIN children whose leaves are (2, 7) and (1, ?)"*.

- Slide 20 actually has THREE levels: MAX → MIN → MAX (with the bottom-level MAX nodes as the "leaves" being 2, 7, 1, ?). The chapter's caption skips the bottom MAX layer. Not strictly wrong (the bottom MAX-leaves *are* the leaves in this tree), but the slide explicitly labels the bottom layer MAX too, and the chapter's caption doesn't mention them.
- Suggested fix: rewrite to *"… two MIN children, each with two MAX-grandchildren below: the left MIN's grandchildren are (2, 7) and the right MIN's are (1, ?)…"*.

### P2-NEW-2. Slide 11's MIN node labels are A, B, C, D — chapter Figure 3 caption (line 158) uses these correctly but inconsistently w.r.t. slide 11.

- Slide 11 names MAX node "A" and MIN nodes "B", "C", "D" (with actions $a_1, a_2, a_3$ from A). Chapter caption says "B = min(3, 12, 8) = 3" etc., which matches. But chapter at line 158 also says "**MAX should play $a_1$** (the action leading to B)" — verified correct against page11-render.png. No issue, just verifying.

### P2-NEW-3. §5.1 final cross-reference to slide-figure edge-order on line 427 is now correctly explained, but could add an explicit "(slide 18 draws **3-2-1** ordering of edges out of $N=4$ root)" annotation.

- Currently says "MIN's three branches in the order 3, 2, 1 from left to right" but the edge-ordering at the root MAX is also 3-2-1 (looking at page18-render.png the edges from N=4 are labelled 1, 2, 3 left-to-right with N=3 on the left, N=2 in the middle, N=1 on the right — so it's 1-2-3 ordering of *coins removed*). The chapter wording is right; this is a polish suggestion only.

### P2-NEW-4. The §6 pitfall 5 statement "Eval is only ever called at non-terminal cut-off nodes" line 516 is correct but could be cross-linked back to the §8 cheat-sheet pseudocode (line 575–589) which now correctly demonstrates this.

- Add `(see §8 pseudocode lines 576–577)` cross-reference. Minor.

### P2-NEW-5. The chapter's repeated "[Lecture 6, slide N]" citations are scattered; a few survive at locations where the slide attribution is now mixed.

- Example: line 102 caption says "(Lecture 6, slide 5.)" cleanly. Fine.
- Example: line 175 closes with *"[Lecture 6, slides 11–15, 19 for the time bound; completeness and space are L03 cross-references, not stated on L06 slides.]"* — this is exactly the kind of attribution the chapter should be doing consistently. Other citations could follow this dual-citation pattern more uniformly.
- Suggested fix: a final once-over to make every citation either pure-slide (one bracket) or pure-supplementary (one bracket) or both (the line-175 style).

### P2-NEW-6. Reading time at line 3 — "~60–90 min (dense; consider splitting into two sittings: §1–§4 first, §5–§8 second)" is the right shape, but §5–§8 is actually 5+6+7+8 = sections 5-8, which is shorter than §1-§4 in chapter line count. Maybe split at §4 / §5 boundary makes the *second* half shorter, not the first. Current wording suggests they're equal-weight.

- Suggested fix: *"consider splitting into two sittings: §1–§4 (concepts and algorithms) first, §5–§8 (worked examples, pitfalls, connections, cheat-sheet) second"*.

### P2-NEW-7. The cheat-sheet pseudocode at line 575–589 is now correct but uses `is_max` as a parameter while the rest of the chapter alternates "player(state) = MAX" (line 224) and a dedicated MAX-VALUE / MIN-VALUE function-pair (line 284-300).

- Three styles in the chapter now. The §8 cheat-sheet's `is_max` parameter is the simplest for cramming but doesn't mirror what the student would actually code from the §4.2.1 pseudocode.
- Suggested fix: optional — pick one style consistently. Lowest-effort fix is to add a one-line comment at the top of the §8 pseudocode: *"// This is the **combined** depth-limited form; for separate MAX-VALUE / MIN-VALUE functions see §4.2.1."*

### P2-NEW-8. The chapter is now 630 lines; with the expanded notes the cheat-sheet/exam-night value per line has dropped. Consider whether §6 pitfalls 1 + 2 could be merged (both about α/β direction confusion) — currently lines 512–514.

- Pitfall 1 is "α/β used vs assigned"; pitfall 2 is "cutoff direction (floor vs ceiling)". They're closely related and reading them sequentially the student bounces between two restated rules.
- Suggested fix: optional — merge into a single "α/β bookkeeping" pitfall with sub-bullets.

---

## EVIDENCE — direct citations and slide-render checks

### Slide 5 (taxonomy) — verified against page05-render.png
- Cells reproduced exactly: Perfect/Deterministic = "Chess, checkers, go"; Perfect/Stochastic = "Backgammon, monopoly"; Imperfect/Deterministic = "Battleships"; Imperfect/Stochastic = "Scrabble, bridge". **No Poker anywhere on the slide.**
- Chapter line 97 table matches. P0-1 fix verified.

### Slide 8 (tic-tac-toe game tree) — verified against page08-render.png
- Bottom row labelled "TERMINAL"; utilities below: **−1, 0, +1** (under three different terminal boards: O-wins, draw, X-wins).
- Chapter lines 120–122 + 127 match. P0-2 fix verified.

### Slide 11 (abstract game tree) — verified against page11-render.png
- Root labelled A (red); MIN children labelled B, C, D; actions $a_1, a_2, a_3$ from A; sub-actions $b_i, c_i, d_i$ from each MIN.
- Leaves 3, 12, 8 | 2, 4, 6 | 14, 5, 2. Backed-up MIN values 3, 2, 2. Root value 3.
- Chapter Figure 3 caption (line 158) matches.

### Slide 18 (coins game tree for $N=4$) — verified against page18-render.png
- Root N=4 (yellow=MAX). Three edges labelled 1, 2, 3 (left to right) to children N=3, N=2, N=1 (all red=MIN).
- All visible leaves are F(S)=1 or F(S)=0, consistent with chapter's bottom-up table at line 416.
- Chapter Figure 6 caption matches.

### Slide 20 (alpha-beta intuition) — verified against page20-render.png
- Root MAX α=2. Two MIN children with β=2 and β=1. Bottom row labelled MAX with leaf values 2, 7, 1, ?.
- Chapter line 271 caption is *almost* right — see new P2-1 above for the missed bottom-level MAX layer.

### Slide 22 (alpha-beta rules) — verified against page22-render.png
- Bulleted rules match chapter §4.2 lines 256–258 exactly, including the inequality formulations.

### Slide 28 (alpha-beta final state) — verified against page28-render.png
- Root MAX = **3** (red label). Left MIN = **3** (3 children labelled 3, 12, 8). Middle MIN = **≤2** (3 children drawn, only first labelled "2"). Right MIN = **2** (3 children labelled 14, 5, 2).
- Chapter Figure 7 caption (line 455) matches.

### Slide 30 (tic-tac-toe Eval setup) — verified against page30-render.png
- Box reads `Utility = X's open lines − O's open lines` (slide author uses "Utility" not "Eval" — see new P1-3).
- Mid-board shows X-centre with β:2. Bottom shows OX (top row) with leaf value 2.
- Chapter §3.4 line 190 formula matches the slide's algebra (chapter calls it Eval; slide calls it Utility — see P1-NEW-3).

### Slide 35 (second alpha-beta example) — verified against page35-render.png
- Root α=3. Left MIN β=3 (leaves labelled 3, 12, 8). Middle MIN β=2 prune! (3 children drawn, only first labelled "2"). **Right MIN β=1 prune!** (3 children drawn, only first two labelled: **14, 1**).
- **Critical:** with leaf values (14, 5, 2) as on slide 28, β at the right MIN cannot drop to 1 — it would bottom out at 2. Therefore slide 35 has at least one different leaf value (the right MIN's second leaf is 1, not 5). **Chapter line 460, 462, 515's assertion of "same tree" is wrong.** See P0-NEW above.

### Slide 38 (chance game tree) — verified against page38-render.png
- Drawn branches: 1/36 1,1 | 1/18 1,2 | … | 1/18 6,5 | 1/36 6,6. (Four representative branches with ellipses for the rest.)
- Bottom terminal values shown: 2, −1, 1, −1, 1.
- Chapter Figure 10 caption (line 347) matches.

---

## Exam-readiness scorecard (Spec §7.1)

| Criterion | Round 1 | Round 2 | Notes |
|---|---|---|---|
| Every slide concept covered | PASS | PASS | All 42 slides represented. |
| No fabricated slide content | **FAIL** | **PARTIAL FAIL** | Round 1 P0-1, P0-3, P0-4 all fixed; Round 2's "same tree" claim about slide 28 vs 35 is the lingering exception (P0-NEW). |
| Utility convention consistent with slides | **FAIL** | PASS | P0-2 fully fixed; slide-8 (−1, 0, +1) and slide-17 (0, 1) explicitly split. |
| Cheat sheet usable as single-page | Pass w/ concerns | PASS w/ ONE concern | move-ordering "YES" cell at line 603 should be tagged R&N-supplementary (P1-NEW-6); otherwise clean. |
| Glossary header complete | **FAIL** | PASS | Now includes game tree, MAX/MIN node, chance node, expectiminimax, MC simulation, transposition table, forward pruning, depth-limited search, move ordering, ply. |
| Worked examples reproducible | PASS | PASS | Coins-game table at line 416 is now a clean bottom-up walk; §5.2 walkthrough still relies on left-to-right DFS but states it up front (line 442). |
| Pitfalls list covers slide-21 confusions | PASS | PASS | §6 pitfall 1 (line 512) unpacks "used vs assigned" with concrete `α ← max(α, v)` annotation; clean. |
| Cross-refs to L02/L03/L05 accurate | PASS | PASS | Now also explicitly attributing space-complexity / completeness to L03 cross-references rather than slides. |
| Forward-refs to L07/L09a/L10 valid | Cannot verify | Deferred | Per revise-summary; OK to defer. |
| Figures correctly captioned | Pass w/ concerns | **PASS w/ ONE concern** | Figure 8 caption (line 460) — see P0-NEW. |

**Aggregate verdict:** **Pass with concerns** (1 P0-residual, 7 P1-new, 8 P2-new). The chapter is markedly stronger than Round 1, and an exam-prep student using it will *mostly* be safe — but the slide-28-vs-35 "same tree" claim is a specific factual error that a slide-grounded exam question could exploit. Fix that one P0 and the chapter is ready.

---

## Report to PM

**Assignment recap:** Lecture Reviewer #4 (Exam Readiness) for **L06 Round 2** post-revision. Re-verified the four Round 1 P0s plus all 10 P1s and 12 P2s against the slide-render PNGs in `study\extracted_figures\L06\` (slides 5, 8, 11, 18, 20, 22, 28, 30, 35, 38 all spot-checked directly).

**Status:** **Pass with concerns** — Round 1's three named P0s (Poker, tic-tac-toe utility, complexity claims) and the supplementary fourth P0 (AlphaGo year + expectiminimax formula) are all genuinely fixed and verifiable. One Round 1 P1 (slide 28 vs 35 "same/different tree") was *escalated* to P0-grade in this Round 2 review because the chapter's Round 2 fix went the wrong direction and now affirmatively states something verifiably false against the source images.

**P0 findings (Round 2):**
1. `L06-Adversarial-Search.md:460, 462, 515` — Figure 8 caption + body text + §6 pitfall 4 all assert that slide 28 and slide 35 show the *"same 9-leaf tree"*. They do not. Slide 28's right-MIN has leaves {14, 5, 2}, backed up to 2. Slide 35's right-MIN backs up to β=1, which is arithmetically impossible from {14, 5, 2} — at least one leaf value must differ (the visible second leaf is 1, not 5). Fix: recaption Figure 8 as "same topology, different leaf values" and rewrite pitfall 4 to not depend on the "same tree" claim. See P0-NEW above for two suggested rewrites.

**P1 findings (Round 2 — all new in this review; Round 1 P1s are all fixed):**
1. `L06:194` — §3.4 empty-board Eval sanity check is correct but pedagogically dense; add an 8-row line-by-line table.
2. `L06:208` — $U_{\text{MAX}}$ used without ever being defined or added to the §8 symbols glossary; replace with $U(s)$ or add to glossary.
3. `L06:184, 190, 196` — Chapter's "U vs Eval" notational discipline is *better* than slide 30's "Utility = X's open lines − O's open lines" labelling but the chapter never flags the discrepancy; add one editorial sentence to §3.4 noting that slide 30 itself uses "Utility" loosely.
4. `L06:498, 504` — $35^{80}$ is technically the leaf count not total node count (same order of magnitude, OK); "twice as deep" framing in §5.4 risks the student writing "depth 160 in chess" — clarify the tie between $b^{d/2}$ and game-tree depth.
5. `L06:448` — §5.2 frame 25 prose "Those two leaves are pruned" should remind once more that this depends on left-to-right DFS ordering.
6. `L06:603` — §8 cheat-sheet "Sensitive to move ordering? YES" cell does NOT carry the R&N-supplementary tag that the body text uniformly applies. Add the tag.
7. `L06:26` — §1 question-list pointer "§3.4 definition, §5.3 worked example" — §5.3 is actually alpha-beta-with-Eval, not a worked Eval example. Either expand §5.3 to also show Eval computations, or rewrite the pointer.

**P2 findings (selected):**
1. `L06:271` Figure 4 caption omits the bottom-level MAX layer that slide 20 explicitly draws — rewrite.
2. `L06:208` $U_{\text{MAX}}$ subscript notation new — add to symbol glossary.
3. `L06:603` cheat-sheet pseudocode `is_max` style is a third notation style on top of §4.2.1's MAX-VALUE/MIN-VALUE and §4.1's MINIMAX; consider one harmonisation comment.
4. `L06:3` reading-time split suggestion "§1–§4 first, §5–§8 second" is unbalanced; clarify.
5. `L06` general citation hygiene — adopt the line-175 dual-bracket style consistently.

**QA Checklist (§7.1 Exam-Readiness) status:**
- Every slide concept covered → Pass
- No fabricated slide content → **Partial Fail** (P0-NEW: slide 28 vs 35 "same tree")
- Utility convention consistent with slides → Pass (Round 1 P0-2 fixed)
- Cheat sheet usable as single-page → Pass with concerns (P1-NEW-6: move-ordering not tagged R&N)
- Glossary header complete → Pass (Round 1 P1-1 fixed)
- Worked examples reproducible → Pass (coins-game table at line 416 now clean)
- Pitfalls list covers slide-21 confusions → Pass
- Cross-refs to L02/L03/L05 accurate → Pass
- Forward-refs to L07/L09a/L10 valid → Deferred per revise-summary
- Figures correctly captioned → **Pass with one concern** (Figure 8 caption is the P0-NEW)

**Acceptance criteria status:** Cannot fully promote to "ready for student use as sole exam-prep resource" until the slide-28-vs-35 "same tree" P0-NEW is resolved. All other Round 1 blockers are genuinely closed.

**DOCUMENT.md audit:** N/A for lecture-chapter review.

**Out-of-scope observations:**
- The Round 2 revision is *substantially* stronger than Round 1. The notational discipline (U vs Eval, lecture-vs-R&N tagging, dual-bracket citation style at line 175) is the single highest-impact change — it should be templatised for every future lecture chapter so this Round 1 → Round 2 fix-pass doesn't have to be repeated for L07, L08, etc.
- The chapter author is clearly fact-checking against slide renders now — the page28 / page35 / page38 captions in revise-summary §"Verification" demonstrate this. The slide-28-vs-35 confusion is the *one* place where the author looked at the renders but didn't catch that β=1 is unreachable from {14, 5, 2}. Worth flagging to the author specifically as a "look once more at this one figure" check.
- The chapter's editorial notes that flag slide imprecision (line 196 about "open line" on slide 30, line 442 about left-to-right DFS not being explicit on the slides, line 460 about slide 35's leaf labelling convention) are pedagogically excellent — when accurate. The line-460 editorial note is the one that's substantively wrong.

**Concerns / risks:**
- An exam question of the form "On slide 35, what β value does the right MIN reach, and which leaves are pruned?" — a student studying from this chapter will say "β=2 (because that's the same value as slide 28's right MIN, and the chapter said it's the same tree)" and get docked.
- An exam question of the form "What does slide 30 call the function 'X's open lines − O's open lines'?" — chapter trains the student to say "Eval"; the slide-grounded answer is "Utility". Minor but real.
- Other than the P0-NEW, the chapter is now solid enough that I would advance it to App Tester / Code Reviewer assuming the lecture is being treated as a study text and not as a verbatim slide transcription.

**What PM should do next:**
1. Send P0-NEW back to the writer with the page35-render.png evidence: right MIN clearly shows leaves "14, 1" and "β=1, prune!", which cannot arise from slide 28's {14, 5, 2}. Required: recaption Figure 8 to drop the "same tree" claim, and rewrite §6 pitfall 4 accordingly.
2. Optionally apply the seven P1-NEW fixes in the same revision pass (all are small).
3. Once P0-NEW is fixed, advance to the next reviewer in sequence; the Round 1 → Round 2 work has produced a chapter that is exam-ready modulo this one figure caption.
4. For future lectures: bake the "dual-bracket lecture-vs-supplementary citation style" (chapter line 175) into the writing template so the Round 1 P0-3/P0-4 class of error doesn't recur.

**DOCUMENT.md updated:** N/A for QA / reviewer role.

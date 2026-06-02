# L06 Round 1 — Revise Summary

**Revised file:** `study/lectures/L06-Adversarial-Search.md`
**Reviewers consulted:** Reviewer 1 (Concept Completeness + Figures), Reviewer 3 (Pedagogical Clarity), Reviewer 4 (Exam Readiness). No reviewer2.md exists on disk.
**Sources verified:** `Lecture6-Adversarial Search.pdf` slides 5, 8, 18, 28, 35, 38 cross-checked directly against the page-render PNGs in `study/extracted_figures/L06/`.

---

## P0 fixes (from PM brief)

| # | Issue | Fix applied |
|---|---|---|
| 1 | "Poker" in §3.1 taxonomy table — not on slide 5 | Removed "Poker" from the Imperfect-Stochastic cell. Added clarifying sentence that slide 3 mentions Poker as a motivating example but it is **not** in the slide-5 taxonomy. |
| 2 | Tic-tac-toe utility convention contradicts slide 8 | Rewrote §3.2 to split the two slide conventions explicitly: slide 8 uses {−1, 0, +1} with 0 = draw; slide 17 (coins) uses {0, 1} with no draws. Figure 2 caption also bolded "draw" for the 0 value. |
| 3 | Unsourced complexity claims (`O(b^{3d/4})` average, "twice as deep") presented as slide content | §4.3 rewritten: the lecture itself does **not** quantify alpha-beta complexity. The `O(b^{d/2})` best and `O(b^d)` worst case are explicitly tagged as R&N 3e §5.3 supplementary. The `O(b^{3d/4})` "average case" claim removed entirely. §5.4 also fixed to remove "amateur vs club player" folk wisdom and re-tag the doubling-depth claim as R&N supplementary. |
| 4 | AlphaGo "(2016)" and expectiminimax piecewise formula attributed to slides that don't contain them | Both labelled as chapter elaboration: the AlphaGo year and the AlphaStar product name are marked "chapter elaboration, not on slide"; the four-case expectiminimax piecewise recursion is introduced with the preface that "slide 39 only states the chance-node case in words". |
| 5 | §8 cheat-sheet pseudocode used `EVAL(state)` at true terminals | Rewrote with explicit `if TERMINAL-TEST(state): return UTILITY(state)` branch BEFORE the `if depth = 0: return EVAL(state)` horizon branch. Added a reading note tying it to pitfall #5. Also added a `depth` parameter so the cheat-sheet pseudocode is recognizably the depth-limited variant. |
| 6 | §5.1 coins-game backup table prose was unparseable (mixed recursion levels) | Replaced the dense narration with a bottom-up "Sub-state / Player / Options / Recursion / Value" table covering every (N, who-moves) pair once, in size order from N=1 up to N=4. Added an explicit note that slide 18 draws MIN's branches in 3-2-1 order so the slide-figure order and the table order do not match one-for-one. Final answer (root=1, MAX plays take-3) unchanged. |
| 7 | §5.2 walkthrough contradicted §4.2.1 pseudocode (cutoffs return `v` vs "≤v") | Rewrote frames 3, 4–5 of §5.2 to call out that the function returns the running `v` exactly (per pseudocode) while slide 28's "≤2" annotation is the partial-information drawing convention. Frame 4–5 now explicitly notes "the same cutoff mechanism fires as in the middle MIN — the only difference is that there are no remaining children left to skip, so the prune saves no work in this particular ordering." Added an upfront sentence stating left-to-right DFS ordering is assumed. |
| 8 | Figure 8 caption — said slide 35 is a "different tree" from slide 28 | Per PM directive, rewrote caption: slide 35 is the **same 9-leaf tree** with explicit α/β annotations; the slide only labels the leaves the sweep actually visits. The "(now 8) leaves" leaf-count error in the surrounding paragraph also removed. |

---

## P1 fixes (from reviewers)

- **R1 P1-3 / R4 P0-3**: Average-case `O(b^{3d/4})` claim — removed entirely.
- **R1 P1-4 / R4 P1-2**: `O(bd)` space complexity — now explicitly attributed to L03 DFS analysis, not the slides.
- **R1 P1-5**: Frame 26–27 cutoff direction prose was misleading — rewrote to make the test (`β ≤ α`) and outcome ("no, continue") explicit at every step.
- **R1 P1-6**: Figure 8 caption — fixed per P0 fix #8.
- **R1 P1-7**: Figure 10 caption — rewrote to state slide 38 shows only 4 representative branches (doubles 1,1 and 6,6 at 1/36; non-doubles 1,2 and 6,5 at 1/18); removed the over-general "1/36 for each ordered pair, 1/18 for each unordered pair" gloss.
- **R1 P1-8**: §4.4 expectiminimax row — replaced unsupported `O(b^d · n^d)` time with "not given by slides"; qualified optimality as "optimal expected utility"; added footnote ‡ explaining all complexity formulas are R&N supplementary.
- **R1 P1-9 / R4 P1-10**: Completeness/optimality claims — explicitly labelled as L03 cross-references where the lecture itself is silent.
- **R1 P1-10**: Figure 6 caption — clarified yellow/red colour convention follows turn-alternation even at terminals.
- **R3 P0-1**: Coins backup table — see P0 fix #6.
- **R3 P0-2, P0-3**: §5.2 frames 3 and 4–5 — see P0 fix #7.
- **R3 P1-1**: α/β "used vs assigned" jargon — added explicit unpacking ("used in MIN nodes" = MIN's cutoff test **reads** α; "assigned in MAX nodes" = only MAX nodes **update** α via `α ← max(α, v)`).
- **R3 P1-2**: Forward references in §1 question list — corrected to point to §3.3 + §4.1 for minimax-the-algorithm, §4.2 + §4.3 for alpha-beta, and §3.4 + §5.3 for evaluation functions.
- **R3 P1-3**: L07 dangling reference — replaced "in L07" with "in upcoming material on Constraint-Satisfaction Problems".
- **R3 P1-4**: Floor/ceiling mnemonic — moved up to §2.2 as the **opening** gloss before the formal α/β definitions ("**$\alpha$ is the floor MAX has already guaranteed; $\beta$ is the ceiling MIN has already imposed**"). Repeated in §4.2 and §6 as before.
- **R3 P1-5**: Value-vs-decision distinction — added explicit "Two things come out of this mental simulation" paragraph at the end of §2.1, tying recursion-returns-a-value vs argmax-picks-an-action.
- **R3 P1-6**: Slide 28/35 "same tree" — see P0 fix #8.
- **R3 P1-7**: Figure 9 caption — explained that slide 34 draws only the one visited child; full game would have one per legal O-move.
- **R3 P1-8**: "Open line" definition — added explicit sanity check in §3.4 (empty board → Eval = 8 − 8 = 0; after X centre → Eval = 8 − 4 = 4). Pitfall 6 rewritten to use the precise "no opposing mark on it" definition.
- **R3 P1-9**: Cross-links from §4 / §5 to §6 pitfalls — added "(see §6 pitfall 2)" in §4.2 cutoff intro, "(See §6 pitfall 4.)" in §4.3 closing, and "(See §6 pitfall 5...)" in §5.3 closing.
- **R4 P0-1, P0-2, P0-3, P0-4**: covered by P0 fixes #1–#4 above.
- **R4 P1-1**: Glossary header at the top expanded to include game tree, MAX/MIN node, minimax strategy, depth-limited search/horizon/cut-off node, move ordering, ply, chance node, expectiminimax, Monte Carlo simulation, transposition table, forward pruning.
- **R4 P1-3**: Expectiminimax comparison-table row reworked — see R1 P1-8.
- **R4 P1-4**: §5.2 left-to-right DFS ordering — now stated explicitly before the walkthrough.
- **R4 P1-5**: Slide 35 reconciliation — see P0 fix #8.
- **R4 P1-6**: U(s) overload — added a "Notational discipline" paragraph in §3.4 stating U is reserved for terminal utility, Eval for cut-off heuristic. Removed the "sometimes also written U(s)" phrase. Pitfall 8 updated accordingly.
- **R4 P1-7**: "Twice as deep" claim — labelled R&N supplementary in §4.3 and §5.4.
- **R4 P1-8**: Cheat-sheet checklist — softened "the one thing alpha-beta is critically sensitive to" to "explain how the order in which children are expanded affects the number of nodes alpha-beta visits"; tagged as R&N supplementary.
- **R4 P1-9**: Zero-sum "one utility number" phrasing — rewrote §3.5 to follow slide 6's "utility for each player + constant sum" framing, with zero-sum "letting us fold both utilities into a single number".
- **R4 P1-10**: Completeness/optimality attribution — see R1 P1-9.

---

## P2 fixes incorporated

- **R1 P2-2**: chess "$10^{123}$ continuations" → "nodes in its full game tree".
- **R1 P2-3**: "amateur vs club player" line dropped from §5.4.
- **R1 P2-4**: "$U(s)$ for utility approximation" phrase deleted from §3.4.
- **R1 P2-9**: cheat-sheet α/β glossary entries — replaced unclear "(≥ floor)" parenthetical with explicit "lower bound (floor) on MAX's final achievable value" wording.
- **R3 P2-1**: §2.2 "or something even worse" hedge — strengthened with "MIN's job is to find the worst-for-you reply, so MIN's eventual pick will be the minimum across all replies, which is at most 2".
- **R3 P2-6**: §1 negotiation contradiction — softened to "zero-sum bidding" and "*strictly* opposing utilities" with a forward-reference to §2.4.
- **R3 P2-7**: §5.3 "left move" — clarified that the slide does not label the physical X-placement.
- **R4 P2-6**: §6 pitfall 4 — rewritten so it no longer claims slides 28 and 35 are different trees; correctly identifies the algorithmic point about ordering as R&N supplementary.
- **R4 P2-10**: Stockfish/Leela conflation — rewritten as chapter elaboration explicitly noting Stockfish uses alpha-beta + NNUE while Leela uses MCTS.
- **R4 P2-11**: "15 distinct movement-effects after symmetries" — replaced with the standard "6 doubles + 15 non-double pairs" breakdown.
- **R4 P2-12**: Reading time estimate — bumped from ~35 min to ~60–90 min with a suggestion to split.

---

## P2 fixes deferred

The following polish items were judged lower priority and not addressed in this revision:

- **R1 P2-1**: §5.1 narrative order — partly addressed by the new bottom-up table (which lists sub-states by size, not by slide-figure edge order); added an explicit note that the orders differ.
- **R1 P2-5**: "forward pruning" gloss aggressiveness — current wording is close enough to slide 36; left as is.
- **R1 P2-8**: §3.3 notation `Successors(s)` vs slide's `successors(state)` — kept the chapter's rigorous notation; no fix needed.
- **R1 P2-10**: Fail-soft vs fail-hard alpha-beta — slide deck doesn't distinguish; left out.
- **R1 P2-11**: Missing intermediate frames (slides 24, 25 page-renders) in §5.2 — the §5.2 prose walkthrough is now tight enough; embedding 5 figures for one example is overkill in a reference chapter.
- **R3 P2-2**: Completeness terminology — addressed in spirit by re-attributing the claim to L03 (P1 fix); no separate fix.
- **R3 P2-3**: Combined depth-limited alpha-beta pseudocode — §8 now provides this in unified form with `depth` parameter; sufficient.
- **R3 P2-5**: "Competitive" property in §3.1 — minor; not blocking.
- **R3 P2-8**: Promoting "Where the analogy breaks down" paragraphs to bold-italic — purely stylistic.
- **R3 P2-9**: $10^{123}$ in §1 with forward-pointer — already cross-references §3.1 derivation in the §2.1 update.
- **R3 P2-10**: Three pseudocode styles — left as is; the §8 cheat-sheet style is now the canonical "combined" form.
- **R4 P2-4**: xkcd 832 inclusion — left as is; the existing prose already labels it "too dense to study at chapter scale".
- **R4 P2-5**: "DAG search" undefined — left as is; one-off term in §4.5.
- **R4 P2-7**: Cross-ref section numbers to L09a / L10 — depends on those chapters existing; will be re-validated in the cross-link review round.

---

## Verification

- Slide 5 verified: page05-render.png shows only "Scrabble, bridge" — no Poker.
- Slide 8 verified: page08-render.png shows utilities labelled **−1, 0, +1** under three terminal positions (loss, draw, win for MAX).
- Slide 18 verified: page18-render.png shows the coin-game tree with MAX = yellow, MIN = red, and F(S) ∈ {0, 1} leaves consistent with the bottom-up backup table.
- Slide 28 verified: page28-render.png shows root=3, left MIN=3 (3,12,8), middle MIN=≤2 (only "2" leaf drawn under it), right MIN=2 (14, 5, 2 all drawn).
- Slide 35 verified: page35-render.png shows root α=3, left MIN β=3, middle MIN β=2 prune!, right MIN β=1 prune!. The leaves labelled are 3, 12, 8, 2, 14, 1 — six labelled, with three child-positions drawn under each MIN.
- Slide 38 verified: page38-render.png shows only four representative chance branches (1/36 1,1; 1/18 1,2; 1/18 6,5; 1/36 6,6), with "…" for the rest.

---

## What changed at a structural level

- §1: forward refs in question list corrected; L07 reference removed; negotiation softened.
- §2.1: value-vs-decision distinction added.
- §2.2: floor/ceiling mnemonic moved up as opening gloss.
- §3.1: Poker removed from taxonomy table; ply defined inline; chess-nodes derivation tied to §5.4 / cheat-sheet.
- §3.2: terminal-utility section rewritten to distinguish slide-8 vs slide-17 conventions.
- §3.3.1: completeness/space-complexity claims re-attributed (L03 cross-references, not slide content).
- §3.4: U(s) vs Eval(s) notation discipline added; empty-board sanity check added for tic-tac-toe Eval.
- §3.5: zero-sum justification rewritten to match slide 6's framing.
- §4.2: α/β "used vs assigned" jargon unpacked with concrete reads/updates.
- §4.3: ALL quantitative complexity claims for alpha-beta now R&N-tagged; average-case `O(b^{3d/4})` claim removed.
- §4.4: comparison table — expectiminimax row qualified, footnote added.
- §4.6: piecewise expectiminimax recursion labelled chapter elaboration.
- §4.7: AlphaGo year, AlphaStar name, Stockfish/Leela details all labelled chapter elaboration.
- §5.1: coins-game backup table rewritten as bottom-up sub-state-by-sub-state computation.
- §5.2: walkthrough frames 3, 4–5 rewritten to reconcile with §4.2.1 pseudocode; "same tree" caption corrected; left-to-right DFS ordering stated up front.
- §5.3: result clarified (move not specified by slide); cross-link to §6 pitfall 5 added.
- §5.4: ply defined; doubling-depth claim re-attributed to R&N.
- §6 pitfalls: pitfall 4 (move ordering) rewritten as R&N supplementary; pitfall 6 (open lines) rewritten with the precise definition; pitfall 8 (Eval vs U) rewritten with the notation discipline.
- §8 cheat-sheet: pseudocode fixed (UTILITY at terminals, EVAL at horizon); α/β symbol descriptions clarified; checklist softened.

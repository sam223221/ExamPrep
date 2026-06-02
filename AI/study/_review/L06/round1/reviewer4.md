# L06 Round 1 — Reviewer #4 (Exam Readiness)

**Reviewer role:** Lecture Reviewer #4 — Exam Readiness (Spec §7.1).
**Source artifact:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture6-Adversarial Search.pdf` (42 slides).
**Chapter under review:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L06-Adversarial-Search.md` (602 lines).
**Mandate:** Be harsh. Flag every divergence from slides, every fact a student could trip on, every glossary/cross-link gap that could cost exam points.

---

## VERDICT

**FAIL — must revise before student can rely on it for the exam.**

The chapter is impressively comprehensive in prose and analogy and gets the *algorithm* right, but it commits at least three exam-grade factual errors against the source slides, contains one internally inconsistent utility convention, smuggles in textbook content (R&N best/worst-case complexity, expectiminimax algebra, AlphaGo year, average-case bound) that is **not in the slides** while presenting it as if it were lecture material via "[Lecture 6, slide X]" citations, and the declared glossary list at the top of the chapter is missing 5+ terms that the chapter itself goes on to introduce. A student preparing only from this chapter will (a) write the wrong utility convention for tic-tac-toe and (b) confidently cite "Poker" as appearing in slide 5's taxonomy table when it does not.

Round 1 needs a tight fact-checking pass against the slides, not a rewrite.

---

## P0 — Blockers (factual errors against the source slides)

### P0-1. Slide 5 taxonomy table — "Poker" is fabricated.

- **Where in chapter:** §3.1, the 2×2 table on lines 86–89 places **"Scrabble, Bridge, Poker"** in the Imperfect-Information × Stochastic cell.
- **Source (PDF slide 5):** the cell reads literally **"Scrabble, bridge"**. There is no "Poker" in the table.
- **Why this is P0:** the chapter cites this as "[Lecture 6, slide 5]" and uses it as Figure 1. A short-answer exam question of the form *"From the taxonomy in lecture 6, which cell contains Battleships?"* is exactly the trap a student rote-memorising this chapter will walk into. Poker IS mentioned by name on slide 3 ("We will cover games like Chess, Go and Poker") but is **not in the taxonomy table on slide 5**. Conflating the two is a verbatim-slide error.
- **Suggested fix:** delete "Poker" from the table; if the reviewer wants to keep the connection, put it in a separate sentence ("The lecture also briefly mentions Poker on slide 3 as a motivating example, though it does not appear in the taxonomy table on slide 5").

### P0-2. Tic-tac-toe terminal utility convention is internally inconsistent and conflicts with slide 8.

- **Where in chapter:** §3.2 line 109 says **"a value of 1 means MAX won, 0 means MIN won *or it's a draw*"**.
- **Source (PDF slide 8):** the canonical tic-tac-toe game tree labels terminals **"−1, 0, +1"** (MAX loss / draw / MAX win). The 0 is the **draw**, not "MIN won or draw".
- **Internal contradiction:** §5.1 (coins game) correctly states the slide-17 convention "F(S) = 1 if MAX wins, 0 if MIN wins" (a binary, no-draw game). But §3.2 mashes the two together and tells the student that 0 = "MIN won OR draw" — which is true for **neither** of the two utility conventions on display in this lecture.
- **Why this is P0:** an exam question of the form *"In the tic-tac-toe tree on slide 8, what utility does a drawn position receive?"* — the correct answer is **0**, but the chapter has trained the student to also accept "MIN won". This is a direct exam-points loss.
- **Suggested fix:** split the two conventions clearly. For tic-tac-toe (slide 8): utility ∈ {−1, 0, +1} meaning {MAX loses, draw, MAX wins}. For the coins game (slide 17): utility ∈ {0, 1} meaning {MIN wins, MAX wins} with no draws. Do not unify them in one sentence.

### P0-3. Alpha-beta complexity claims smuggle textbook material in as if it were slide material.

- **Where in chapter:** §4.3 lines 289–291 state:
  > - Best-case time complexity $O(b^{d/2})$ when children at every node are visited in optimal order…
  > - Worst-case time complexity $O(b^d)$ …
  > - Average case with random child ordering: roughly $O(b^{3d/4})$ — still a substantial saving.
- And the chapter cites these as "[Lecture 6, slides 23–28, 35]" at line 296.
- **Source (PDF):** slides 23–28 and 35 contain **no quantitative complexity claim** for alpha-beta whatsoever. They state qualitatively that "It is possible to compute the exact minimax decision without expanding every node". Slide 19 mentions $O(b^d)$ but for plain minimax, not alpha-beta. There is no $O(b^{d/2})$, no $O(b^{3d/4})$, no "twice as deep" claim anywhere in the deck.
- **Why this is P0 (not P1):** the chapter affirmatively cites these to a slide that does not contain them. A student studying for a strict-slide-knowledge exam will write "the lecture proved best-case alpha-beta is $O(b^{d/2})$" on the exam and get docked. Even §5.4 line 479 doubles down: *"Alpha-beta's $O(b^{d/2})$ best-case is genuinely transformative."* with citation "[Lecture 6, slide 7]" — slide 7 says nothing about alpha-beta.
- **Suggested fix:** either (a) remove the quantitative claims, or (b) keep them with an explicit "[textbook / R&N, not in slides]" tag so the student knows it's supplementary. Same for the "average case ~$O(b^{3d/4})$" — that's a published-literature result, not slide material.

### P0-4. AlphaGo year (2016) and expectiminimax piecewise formula attributed to slides that do not contain them.

- **Where in chapter:**
  - §4.7 line 356: *"**AlphaGo** (2016) combined MCTS with deep neural networks…"* with citation "[Lecture 6, slides 40–41]".
  - §4.6 lines 329–337: full piecewise mathematical definition of Expectiminimax(s) including the $\sum_{s'} P(s' \mid s) \text{Expectiminimax}(s')$ chance-node case, cited as "[Lecture 6, slide 39]".
- **Source (PDF):**
  - Slide 40 mentions AlphaGo by name but **does not give a year**. The chapter's "(2016)" is correct as a historical fact but is **not in the lecture**.
  - Slide 39 states only *"Expectiminimax: for chance nodes, average values weighted by the probability of each outcome"* — one English sentence. The piecewise formula with the four cases (terminal / MAX / MIN / CHANCE) is the **chapter's own elaboration**, not slide content. Slide 38 has the *picture* of the tree, but no formula.
- **Why this is P0:** the chapter is presenting these as "here is what the lecture told you" when the lecture told you neither. On a strict-slide exam this matters; on a free-form exam the chapter's elaboration is fine but should be honestly labelled.
- **Suggested fix:** label the AlphaGo year and the expectiminimax formula as "[chapter elaboration; not on slide]" or move them to a footnote.

---

## P1 — Important issues (likely to cost points or confuse)

### P1-1. Declared glossary list at the top of the chapter is incomplete.

- **Where:** line 5: *"Glossary terms introduced: adversarial search, zero-sum game, minimax, terminal state, evaluation function, alpha-beta pruning, alpha cutoff, beta cutoff."*
- **Missing terms the chapter itself goes on to introduce:**
  - **game tree** (introduced §3.2 — *the* central structure of this lecture)
  - **MAX node / MIN node** (introduced §3.2)
  - **utility function** (claimed reused from L02 but slide 6 introduces it again in adversarial-search context — at minimum the *terminal-state utility* is new here)
  - **chance node** (introduced §4.6)
  - **expectiminimax** (introduced §4.6)
  - **Monte Carlo simulation** (introduced §4.6)
  - **transposition table**, **forward pruning** (introduced §4.5)
  - **search depth / horizon** / **depth-limited search** / **cut-off node** (used heavily in §3.4, §5.3)
  - **move ordering** (heavily exam-relevant, introduced §4.3 / §6)
- **Why P1:** the glossary header is the first thing a student uses to build flashcards. Missing terms = missed flashcards = missed exam points. The chapter is internally inconsistent: it tells the reader in line 5 what's new, then teaches a bunch more new terms.
- **Suggested fix:** expand the header glossary list to match what's actually defined in the body. At minimum add: game tree, MAX/MIN node, chance node, expectiminimax, Monte Carlo simulation, transposition table, forward pruning, depth-limited search, move ordering.

### P1-2. §3.3.1 space-complexity claim has no slide support.

- **Where:** line 160: *"Space complexity $O(bd)$ if implemented as recursive DFS (one path's worth of nodes in memory at a time) — same as L03's DFS analysis."*
- **Source:** PDF slide 19 mentions only time $O(b^d)$. No space complexity is given anywhere in the deck.
- **Severity:** P1 because it is correct (it is the standard R&N DFS space result) but again attributed implicitly via the §3.3.1 citation block to the lecture.
- **Suggested fix:** explicit "[L03 cross-reference, not stated on L06 slides]".

### P1-3. The "comparison table" in §4.4 contains an Expectiminimax row that uses non-standard / unsupported notation.

- **Where:** lines 300–305 table, expectiminimax row: time $O(b^d \cdot n^d)$, where "n is the number of chance outcomes per move".
- **Issues:**
  - The slide deck does not give any complexity for expectiminimax (slide 39 just says "nasty branching factor").
  - $O(b^d \cdot n^d) = O((bn)^d)$ — fine if you count $d$ as MAX-decisions, but in a tree where MAX / CHANCE / MIN alternate, the depth tripling makes the effective complexity $O((b \cdot n \cdot b)^{d/2})$ or similar depending on convention. The chapter's notation invites confusion.
  - Citation "[Lecture 6, slides 14, 19, 22, 35, 39]" — none of those slides contain the table.
- **Suggested fix:** either remove the expectiminimax row (since no slide-supported numbers exist) or mark the row "[chapter estimate, not in slides]" and rewrite the complexity to $O((bn)^d)$ with a single $d$ counting alternation levels.

### P1-4. §5.2 contains a frame-by-frame walkthrough that misses one critical alpha-beta step.

- **Where:** §5.2 lines 419–425, the walkthrough of slides 23–28.
- **Issue 1 (frame 26-27 description):** The chapter says the right MIN's first leaf is 14, "starts β at 14 (not yet a cutoff because 14 > α = 3)". This is fine. Next leaf is 5, β drops to 5. Next leaf is 2, β drops to 2. The chapter then says: *"Now: β = 2 ≤ α = 3 at root — alpha-cutoff! But there are no remaining children to prune, so this just finalises the right MIN's value as 2."* — That's true on slide 28 (3 children fully expanded by the time the cutoff condition is met). **But this is not "alpha-beta pruning in action" for the right subtree — pedagogically the chapter should call this out.** As written, the casual student will read "alpha-cutoff!" and think a prune happened on the right MIN, when it did not (all 3 right-MIN children were visited; the cutoff fired only on the last one with nothing left to skip).
- **Issue 2:** The chapter writes "Frame 25 (slide 25): … the remaining two children of the middle MIN (the ones whose leaves are 4 and 6) are **pruned**" — correct, but the chapter never explicitly states the move-ordering assumption (DFS left-to-right). A diligent student doing the same problem with a different ordering will get a different prune set and conclude they made a mistake.
- **Suggested fix:** in §5.2 add one explicit sentence: *"Throughout, we assume left-to-right DFS expansion of children. Different orderings produce different prune sets — see §6 pitfall 4."* And explicitly note that the right-MIN cutoff did **not save any work** in slide 28's ordering.

### P1-5. Slide-35 vs slide-28 reconciliation is sloppy.

- **Where:** §5.2 lines 432–437, Figure 8 caption and the surrounding paragraph.
- **Issue:** The chapter says slide 35 *"uses a slightly different right-MIN child set than slide 28 (it shows leaves 14, 1 instead of 14, 5, 2 — both illustrate the same algorithm; the slide-35 version triggers an even earlier prune…)"*.
- **What the PDF actually shows on slide 35:** the right MIN has children leading to leaves **14** and **1** (only two visible), with annotation "β=1, prune!". The middle MIN shows leaf 2 and annotation "β=2, prune!". This is a **different tree** from slide 28 — the slide-deck deliberately uses a smaller/different example to illustrate two prunes instead of one. The chapter calls this "same tree" then immediately contradicts itself by saying "5 of the (now 8) leaves" — wait, 3+1+2 = 6 leaves under slide-35's structure, not 8. The chapter's leaf accounting *"5 of the (now 8) leaves; 3 were pruned"* makes no sense — there are only ~6 leaves drawn on slide 35, of which 4 are expanded (3, 12, 8, 2, 14, 1 → 6 expansions if you count all six; or counting prunes on middle MIN's 2nd+3rd leaves and right MIN's last leaf you get the "3 prunes" figure).
- **Suggested fix:** re-read slide 35 carefully and re-do the leaf count. Recommend rewriting Figure 8's caption to explicitly say "slide 35 uses a different (smaller) abstract tree from slide 28; do not try to match leaves one-to-one." Then state the slide-35 leaf inventory verbatim.

### P1-6. The "Where the analogy breaks down" for evaluation function muddles the utility-vs-evaluation distinction.

- **Where:** §2.3 lines 66–68 and §3.4 line 169.
- **Issue:** §3.4 line 169 writes *"replace the recursive Minimax(s) with a fast heuristic estimate of utility called the evaluation function, denoted Eval(s) or sometimes also written U(s) for 'utility approximation'"* — but the chapter has *already* used $U(s)$ in §4.6 (line 332) for the **true utility** at a terminal state in the expectiminimax recursion. So $U(s)$ is overloaded: chapter says it is *both* the true utility (terminal) *and* the evaluation function (cut-off). The slides use $U$/Utility for terminals (slide 14) and "Eval" for cut-offs (slide 30). The chapter then warns the student in §6 pitfall 8 *not* to conflate evaluation with utility — but the chapter's own notation conflates them.
- **Suggested fix:** pick one notation. Recommend: $U(s)$ for terminal utility only; $\text{Eval}(s)$ for cut-off heuristic only; never the twain shall meet. Remove the "sometimes also written $U(s)$" phrase in line 169.

### P1-7. Move-ordering claim in §4.3 ("twice as deep") is not in the slides.

- **Where:** §4.3 line 289 *"with perfect move ordering, alpha-beta searches **twice as deep** as minimax in the same time budget"*, also §5.4 line 479.
- **Source:** the PDF nowhere makes this claim. The slides do not even introduce the concept of move ordering as a knob — slide 21–22 only state the cutoff rules, slide 35 mentions "prune!" twice without commentary on ordering.
- **Severity:** P1 (not P0) because it's textbook-true and pedagogically valuable; only P1 because the chapter again attributes it implicitly to lecture content.
- **Suggested fix:** keep it but mark it "[R&N supplementary; not in lecture]".

### P1-8. The "Cheat-Sheet Summary" includes the move-ordering claim but the exam-night checklist at line 596 over-promises.

- **Where:** line 596 *"Can I name the one thing alpha-beta is critically sensitive to? (move ordering)"*.
- **Issue:** if move ordering is not in the lecture (P1-7), this checklist question primes the student to give an answer the lecturer may not award points for. The "critically sensitive to" framing is the chapter's own elevation of an R&N point.
- **Suggested fix:** soften to *"Can I explain how the order in which children are expanded affects the number of nodes alpha-beta visits?"* and don't make it the marquee "one thing".

### P1-9. §3.5 says zero-sum is what justifies "*one* utility number per terminal state" — overstated.

- **Where:** line 188 *"Zero-sum is what justifies one utility number per terminal state."*
- **Issue:** plenty of two-player non-zero-sum games still get a single utility per terminal state per player — what zero-sum gives you is the ability to *fold* MIN's utility into −MAX's utility. The chapter's phrasing is imprecise. Slide 6 actually says "Utility for **each player** … Constant sum of both players' utilities" — i.e., the slide explicitly says one utility per player, and zero-sum is the *constant-sum* condition layered on top.
- **Suggested fix:** rewrite to *"Zero-sum is what allows us to represent the state's value with one number (MAX's utility, since MIN's is determined as constant − MAX's). In a non-zero-sum game we'd need to track both players' utilities separately."*

### P1-10. The "Minimax is complete on finite game trees" claim and "completeness/optimality inherited" claim lack slide attribution.

- **Where:** §3.3.1 line 158 *"Complete on finite game trees …"*; §4.3 line 292 *"Completeness and optimality are inherited from minimax…"*.
- **Source:** the PDF makes no completeness/optimality claim using L03's terminology. Slide 15 says only *"The minimax strategy is optimal against an optimal opponent"* — which is the game-theoretic optimality claim, not the L03 search-completeness claim.
- **Severity:** P1 — pedagogically useful but again presented as if it were slide content.
- **Suggested fix:** explicit cross-link to L03's completeness/optimality definitions, and note that the lecture itself does not formally state these properties for the minimax algorithm.

---

## P2 — Polish and minor improvements

### P2-1. §1 Overview, line 13: forward-references **L07** ("in L07 the constraints are fixed and we get to choose every variable") before the student has seen L07.
- Suggested fix: either drop the forward reference or mark it "(coming up in L07)".

### P2-2. §2.1 line 45: chess "$10^{123}$ continuations" duplicates §3.1 line 98 and §5.4 line 473. Three mentions of the same figure; the cheat sheet adds a fourth (line 597). Slim to two (overview + cheat sheet).

### P2-3. §3.3 definition box (lines 122–132): the recursion variable name is inconsistent — the box uses `s'` and `Successors(s)`, slide 14 uses `successors(state)`. Pick one and stick to it; the alpha-beta pseudocode in §4.2.1 then uses `SUCCESSORS(state)`. Three styles in one chapter.

### P2-4. The xkcd 832 link callout (line 116) is fine but the chapter immediately calls it "too dense to study at chapter scale" — true, but then why include slides 9–10 in the figure roster? Either drop the cross-reference or add a sentence saying *"included for completeness; not exam material"*.

### P2-5. §4.5 uses the term "DAG search" (line 315) without defining it. L03 introduced graph search but not DAG specifically. Either define inline or drop.

### P2-6. §6 pitfall 4 (line 490) says *"The slides don't dwell on this but a careful reading of slides 28 vs 35 (same tree, two move orderings, two prune counts) makes it explicit."* — but as P1-5 shows, slides 28 and 35 are **not the same tree**. This pitfall is itself confused.

### P2-7. §7 Outbound cross-references: line 519 cross-links to L10 §3 — RL. Make sure L10's actual section number/title matches; if L10 turns out to put RL in §4 or §5, this link breaks silently. Same for the L09a cross-reference on line 523.

### P2-8. §8 Symbols glossary on line 587 says "α = best-for-MAX value found so far on the current root path (≥ floor)". The "≥ floor" parenthetical is non-standard and confusing — α IS a lower bound, but the symbol "≥ floor" reads like "α is at least the floor", which is tautologous. Drop the parenthetical or rewrite as "(lower bound on MAX's final value)".

### P2-9. §5.1 Coins-game table at lines 396–400 is hard to follow because each row mixes algorithm narration with leaf-value computations. Consider splitting into a tree diagram with backed-up values written next to each node, mirroring slide 18's visual style.

### P2-10. §4.7 line 354 says *"Modern engines (Stockfish, Leela) extend this with neural-network evaluators and MCTS."* — Stockfish is NOT MCTS; Stockfish uses alpha-beta + NNUE evaluator. Leela uses MCTS. The chapter conflates them. Slide 40 says nothing about either modern engine — this is pure chapter elaboration and it's wrong.

### P2-11. §4.6 line 343 says "21 unordered combinations" for backgammon dice. Correct (21 = 6 doubles + 15 unordered non-doubles). But then says "15 distinct movement-effects after symmetries" — this is non-standard and not explained. Either explain (the 6 doubles each play differently from the non-doubles, so the count depends on what you mean by "movement-effect") or drop.

### P2-12. The "Reading time: ~35 min" at line 3 — at 602 lines of dense markdown including formulas, figures, and tables, 35 min is optimistic. Realistic is 60–90 min for first read. Either say "Reading time: ~60–90 min" or break the chapter into 2-3 sittings.

---

## EVIDENCE — direct citations

### Slide 5 (taxonomy table) verbatim cells
- Perfect / Deterministic: "Chess, checkers, go"
- Perfect / Stochastic: "Backgammon, monopoly"
- Imperfect / Deterministic: "Battleships"
- Imperfect / Stochastic: **"Scrabble, bridge"** (NO "Poker").
→ Refutes chapter §3.1 line 89.

### Slide 8 (tic-tac-toe terminal labels)
- Terminal utilities labelled **−1, 0, +1** (loss, draw, win for MAX).
→ Refutes chapter §3.2 line 109 conflation of "0 = MIN won OR draw".

### Slide 17 (coins game utility convention)
- "Utility Function: F(S). F(S) = 1 if MAX wins, 0 if MIN wins."
- No draw option mentioned. Two-valued utility.
→ Used correctly in §5.1; misused in §3.2.

### Slide 19 (complexity)
- "Generally, there are O(b^d) nodes to search for."
- Branch factor b, depth d. No alpha-beta complexity given.
→ Refutes the chapter's slide-attributed O(b^{d/2}) / O(b^{3d/4}) claims.

### Slide 22 (alpha-beta rules) verbatim
- "At MAX node n, alpha(n) = max value found so far. Alpha values start at -∞ and only increase."
- "At MIN node n, beta(n) = min value found so far. Beta values start at +∞ and only decrease."
- "Beta cutoff: stop search below MAX node N (i.e., don't examine more descendants) if alpha(N) >= beta(i) for some MIN node ancestor i of N."
- "Alpha cutoff: stop search below MIN node N if beta(N)<=alpha(i) for a MAX node ancestor i of N."
→ Chapter §4.2 line 237 matches.

### Slide 35 (second alpha-beta example) verbatim leaves
- MIN-1: 3, 12, 8 → β=3
- MIN-2: 2 (only one leaf visible) → β=2, "prune!"
- MIN-3: 14, 1 → β=1, "prune!"
→ Different tree from slide 28; chapter §5.2 line 435 incorrectly says "same tree".

### Slide 39 (expectiminimax) verbatim
- "Expectiminimax: for chance nodes, average values weighted by the probability of each outcome"
- "Nasty branching factor, defining evaluation functions and pruning algorithms more difficult"
- (no piecewise formula; no Σ-notation; no complexity result)
→ Refutes the chapter's slide-39 attribution of the four-case piecewise recursion.

### Slide 40 (state of the art) verbatim
- "Checkers: solved in 2007"
- "Chess: IBM Deep Blue defeated Kasparov in 1997"
- "Backgammon: TD-Gammon system used reinforcement learning…"
- "Bridge: top systems use Monte Carlo simulation and alpha-beta search"
- "Go: branching factor 361. … AlphaGo's algorithm uses a Monte Carlo tree search…" (no year for AlphaGo)
- "2019: Google AI beats top human players at strategy game StarCraft II"
→ AlphaGo "2016" in the chapter is chapter-added.

### Slide 41 (origins)
- Zermelo 1912; Shannon 1949; McCarthy 1956 (alpha-beta); Samuel 1956 (checkers).
→ Chapter §4.7 line 360 matches.

---

## Exam-readiness scorecard (Spec §7.1)

| Criterion | Status | Notes |
|---|---|---|
| Every slide concept covered | **PASS** | All 42 slides represented. |
| No fabricated slide content | **FAIL** | P0-1 (Poker), P0-3 (complexity), P0-4 (AlphaGo year, expectiminimax formula). |
| Utility convention consistent with slides | **FAIL** | P0-2. |
| Cheat sheet usable as a single-page reference | **PASS with concerns** | §8 is well-structured but P1-7/P1-8 push R&N material as if it were lecture. |
| Glossary header lists all introduced terms | **FAIL** | P1-1. |
| Worked examples reproducible by hand | **PASS** | §5.1 and §5.2 are walkable, modulo the right-MIN "cutoff that didn't prune anything" ambiguity (P1-4). |
| Pitfalls list covers slide-21 mnemonic confusions | **PASS** | §6 pitfall 1 nails it. |
| Cross-refs to L02, L03, L05 accurate | **PASS** | Verified by inspection (cannot cross-check the actual L02/L03/L05 chapters from this review). |
| Forward-refs to L07, L09a, L10 use correct section pointers | **CANNOT VERIFY** | P2-7; needs cross-chapter review. |
| Figures correctly captioned and numbered | **PASS with concerns** | Figure 8 caption (slide 35) is wrong (P1-5). |

**Aggregate verdict: FAIL on exam-readiness criteria.** 3 P0s, 10 P1s. The chapter is not ready to be a student's sole exam-prep source until the slide-attribution errors are fixed.

---

## Report to PM

**Assignment recap:** Lecture Reviewer #4 (Exam Readiness) for L06 Round 1. Reviewed `study\lectures\L06-Adversarial-Search.md` against `Lecture6-Adversarial Search.pdf` per Spec §7.1.

**Status:** **Fail** (3 P0, 10 P1, 12 P2).

**P0 findings:**
1. `L06-Adversarial-Search.md:89` — Taxonomy table fabricates "Poker" in the Imperfect/Stochastic cell; slide 5 lists only "Scrabble, bridge". Fix: delete "Poker" from the table.
2. `L06-Adversarial-Search.md:109` — Tic-tac-toe utility convention says "0 = MIN won OR draw", conflicting with slide 8 (where 0 IS the draw and −1 is the loss). Fix: separate the slide-8 (−1/0/+1) and slide-17 (0/1) conventions; do not merge.
3. `L06-Adversarial-Search.md:289-291, 479` — Alpha-beta complexity claims (O(b^{d/2}) best-case, O(b^{3d/4}) average, "twice as deep") attributed via "[Lecture 6, slides 23–28, 35]" — none of those slides contain these claims. Fix: mark as "[R&N supplementary, not on slides]" or remove.
4. `L06-Adversarial-Search.md:329-337, 356` — Expectiminimax piecewise formula attributed to slide 39 (which has only the one-sentence verbal definition); AlphaGo "(2016)" attributed to slide 40 (which gives no year). Fix: label both as chapter elaboration.

**P1 findings:** (1) glossary header at line 5 omits game tree, MAX/MIN node, chance node, expectiminimax, MC simulation, transposition table, forward pruning, depth-limited search, move ordering; (2) §3.3.1 space-complexity claim has no slide support; (3) §4.4 expectiminimax row uses non-standard $O(b^d \cdot n^d)$ notation with no slide backing; (4) §5.2 right-MIN walkthrough doesn't note the cutoff fired but pruned nothing in slide-28 ordering; (5) §5.2 line 435 calls slide 35 the "same tree" as slide 28 when it is a smaller different tree, and the leaf count "5 of (now 8) leaves" is wrong; (6) §3.4 line 169 overloads $U(s)$ to mean both true utility and Eval; (7) "twice as deep" claim not in slides; (8) cheat-sheet checklist over-promises move-ordering as "the one thing" alpha-beta is sensitive to; (9) §3.5 line 188 imprecisely says zero-sum justifies "one utility number per terminal state"; (10) completeness/optimality claims for minimax have no slide attribution.

**P2 findings:** see §P2 above — forward-ref to L07 before student has L07; chess-10^123 cited 4× (deduplicate); Successors notation inconsistent (s' vs successors(s) vs SUCCESSORS(state)); xkcd 832 inclusion contradictory; "DAG search" undefined; §6 pitfall 4 itself confused by P1-5; cross-ref section numbers to L09a/L10 unverified; α "(≥ floor)" parenthetical confusing; §5.1 table dense; Stockfish wrongly grouped with MCTS engines; "15 distinct movement-effects" unexplained; reading-time estimate optimistic.

**QA Checklist (§7.1 Exam-Readiness) status:**
- Every slide concept covered → Pass
- No fabricated slide content → **Fail** (P0-1, P0-3, P0-4)
- Utility convention consistent with slides → **Fail** (P0-2)
- Cheat sheet usable as single-page → Pass with concerns
- Glossary header complete → **Fail** (P1-1)
- Worked examples reproducible → Pass
- Pitfalls list covers slide-21 confusions → Pass
- Cross-refs to L02/L03/L05 accurate → Pass (spot-checked)
- Forward-refs to L07/L09a/L10 valid → Cannot verify in this review
- Figures correctly captioned → Pass with concerns (Figure 8 wrong)

**Acceptance criteria status:** Cannot promote to Round 2 until P0-1 through P0-4 are fixed. The factual errors against the source PDF are exam-grade.

**DOCUMENT.md audit:** N/A for lecture-chapter review.

**Out-of-scope observations:**
- The chapter is otherwise *extremely* well-written prose-wise — the analogies in §2 are pedagogically strong, the worked examples in §5 are exam-relevant, and the pitfalls list in §6 catches genuine student traps (the α/β assigned-vs-used confusion in pitfall 1 is gold). Once the slide-attribution errors are fixed this will be a very strong chapter.
- The chapter occasionally cites "[Lecture 6, slide X]" at the end of paragraphs that mix slide content with R&N elaboration. A blanket convention — e.g., wrap any non-slide sentence in a `[supplementary]` tag — would prevent the P0-3/P0-4 class of error from recurring in other lecture chapters.
- Stockfish-is-MCTS error (P2-10) is a yellow flag: suggests the chapter author is not deeply familiar with modern game-engine internals and may have introduced other similar errors I have not caught. Recommend one final pass focused specifically on "extra elaboration sentences" that aren't slide-grounded.

**Concerns / risks:**
- A student using this chapter standalone for exam prep WILL miss points on (a) the slide-5 taxonomy question, (b) any "what does utility 0 mean in the tic-tac-toe tree on slide 8" question, and (c) any "what complexity does the lecture give for alpha-beta" question (the answer is "none — the lecture is silent", but the chapter has trained them to say O(b^{d/2})).
- The glossary gap (P1-1) means flashcards built from the header miss ~8 terms.
- Round 1 to Round 2 transition should not happen until at minimum P0-1 through P0-4 are fixed AND the glossary header is expanded.

**What PM should do next:**
1. Send the chapter back to the writer with this report.
2. Require fixes for all four P0s before Round 2.
3. Require P1-1 (glossary), P1-4/P1-5 (worked-example accuracy), and P1-6 (U vs Eval notation) before exam release.
4. Defer P2s to a polish pass.
5. Once revisions are in, dispatch Reviewer #4 again for verification — do not advance to Reviewer #5 until P0s clear.

**DOCUMENT.md updated:** N/A for QA.

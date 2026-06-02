# L06 — Round 2 Review (Reviewer 2: Mathematical Rigor)

**Reviewer role:** Mathematical rigor — formulas, complexity bounds, worked-example arithmetic, sourcing of quantitative claims.
**File reviewed:** `study/lectures/L06-Adversarial-Search.md` (post-revision, 630 lines).
**Source of truth:** `Lecture6-Adversarial Search.pdf` cross-checked via the page-render PNGs in `study/extracted_figures/L06/` (slides 5, 8, 11, 18, 20, 22, 23–28, 30, 34, 35, 38).
**Round 1 carry-over from PM brief:** 2 P1s — (a) cheat-sheet pseudocode terminal-test vs depth-cutoff ordering; (b) unsourced `O(b^{3d/4})` average-case bound. The Round 1 `reviewer2.md` was never written to disk; the brief is the only Round 1 artifact.

---

## Round 1 carry-over — verification

| Round 1 P1 | Where addressed in current chapter | Verdict |
|---|---|---|
| Cheat-sheet pseudocode used `EVAL` at true terminals (no separate `TERMINAL-TEST → UTILITY` branch); cutoff condition placed before terminal/horizon test | §8 cheat-sheet pseudocode, lines 575–589 — now opens with `if TERMINAL-TEST(state): return UTILITY(state)` BEFORE `if depth = 0: return EVAL(state)`. A "Reading this" paragraph (line 591) explicitly ties the distinction to pitfall #5. Cutoff tests (`if v ≥ β: return v` / `if v ≤ α: return v`) are correctly placed after the recursive call and **before** the α/β update — matches §4.2.1's pseudocode exactly. | **Fixed.** |
| Unsourced `O(b^{3d/4})` "average-case" complexity for alpha-beta | §4.3 contains no such claim. The chapter now states "The lecture itself gives no quantitative complexity bound for alpha-beta" and labels `O(b^{d/2})` best / `O(b^d)` worst explicitly as R&N 3e §5.3 supplementary (line 311–312). `grep "3d/4"` on the file returns no matches. | **Fixed.** |

Both Round 1 P1s are clean. Moving on to fresh findings.

---

## P0 findings (mathematical rigor — blocks shipping)

None. The chapter's core recursions (minimax, expectiminimax, alpha-beta) and all supporting arithmetic (coin-game backup, $35^{80} \approx 10^{123}$, the tic-tac-toe Eval sanity check, the dice probabilities $1/36$ vs $1/18$, the 6 doubles + 15 non-double-pairs breakdown) are mathematically correct as written.

---

## P1 findings (mathematical rigor — important)

### P1-1. §5.2 + Figure 8 caption — "same 9-leaf tree" claim contradicts the leaf values on slide 35

**Location:** `study/lectures/L06-Adversarial-Search.md`
- Line 457: *"Slide 35 of the lecture revisits the **same 9-leaf abstract tree**..."*
- Line 460 (Figure 8 caption): *"The same 9-leaf tree as Figure 7 (slide 28), re-annotated with explicit α/β values: ... the right MIN ends with β = 1 followed by 'prune!'. Slide 35 only labels the leaves the sweep actually visits — leaves whose values do not influence the pruning logic are drawn but left unlabelled."*
- Line 462: *"Slide 35's annotation reflects the same algorithm on the same tree but emphasises a slightly different sweep where the right MIN's second child also triggers a cutoff at β = 1."*

**Why this is wrong.** Slide 11 (the canonical abstract tree) and slide 28 both show the right MIN with leaf values **14, 5, 2** (visible explicitly in `page28-render.png`). Slide 35 (`page35-render.png`) shows the right MIN with **two labelled leaves: 14 and 1** plus one drawn-but-unlabelled child position, and a β = 1 prune annotation. Trace the algorithm on slide 28's tree with left-to-right DFS at the right MIN:
- visit 14: $v = 14$, test $14 \le \alpha = 3$? **no**, $\beta \leftarrow \min(\beta, 14) = 14$
- visit 5: $v = \min(14, 5) = 5$, test $5 \le 3$? **no**, $\beta \leftarrow 5$
- visit 2: $v = \min(5, 2) = 2$, test $2 \le 3$? yes — but no children left

No β = 1 anywhere; no early prune at the right MIN. **The value "1" displayed on slide 35 is simply not in the leaf set of slide 11/28's tree.** Slide 35 is therefore using a *different* tree (or at minimum different leaf values at the right MIN), not "the same tree with a different sweep" as the chapter claims.

The chapter's hand-wave that "with a different child-ordering at the right MIN, alpha-beta can prune *more* than 2 leaves" (line 462) is a logical non-sequitur: reordering the multiset $\{14, 5, 2\}$ cannot make $\beta$ converge to $1$ because $1 \notin \{14, 5, 2\}$. This is a mathematical impossibility presented as a pedagogical observation.

**Severity.** P1 (not P0): the surrounding minimax/alpha-beta arithmetic is correct and the take-away message ("alpha-beta produces the same root decision faster") is intact. But a rigor-focused chapter cannot present a logically impossible reconciliation as fact, especially when this exact reconciliation was Round 1 P0 fix #8.

**Suggested fix.**
1. Drop the "same 9-leaf tree" framing. Rewrite Figure 8's caption and the surrounding prose to state: *"Slide 35 shows a **different example tree** with the same three-MIN-children structure but different leaf values (note in particular the right MIN's second child is 1, not 5). The point is the same — alpha-beta's pruning logic operates identically — but the prune pattern differs because the leaf values differ."*
2. Rewrite line 462's "How many leaves were visited?" paragraph to scope strictly to slide 28's tree; remove the false claim that slide 35 is the same tree with a different sweep.
3. If you want to keep a "more pruning is possible with better ordering" lesson, construct a *new* worked example where the slide 28 tree's leaves are visited in a different order and show the resulting prune pattern — without conflating that example with slide 35.

### P1-2. §3.3.1 — minimax time complexity attribution is loose

**Location:** Line 172: *"**Time complexity** $O(b^d)$, with $b$ the branching factor and $d$ the tree depth, because every node must be expanded (slide 19). The lecture motivates alpha-beta as the answer to 'how do we make this faster'."*

**Issue.** Slide 19 (titled "Properties of Minimax") states the tree statistics for the *coin game* — depth 5, branching factor 3, 15 nodes. It does not write the closed-form $O(b^d)$ on the slide. The closed-form is correct (and standard) but is not "given on slide 19"; saying *"because every node must be expanded (slide 19)"* implies the slide states the formula. It does not.

**Severity.** P1 — the chapter is otherwise scrupulous about distinguishing "stated on slide" from "R&N supplementary"; this is one place where that discipline slipped.

**Suggested fix.** Reword as *"Time complexity $O(b^d)$ since minimax-as-DFS expands every node down to depth $d$ (the lecture demonstrates the explosion concretely on slide 19 — depth 5, $b = 3$, 15 nodes — but does not state the closed-form bound; the formula is standard from L03's DFS analysis)."* Or similar — the point is to not claim slide 19 contains the formula.

### P1-3. §3.5 — "zero-sum" vs "constant-sum" terminology blurred

**Location:** Line 206: *"a **zero-sum game** is one in which the sum of all players' utilities at every terminal state is constant. (The constant is conventionally 0; equivalent definitions use 1 or any other fixed value — what matters is that one player's gain is exactly the other's loss.)"*

**Issue.** This conflates two distinct terms. *Zero-sum* means the constant is literally 0 (one player's gain equals the other's loss). *Constant-sum* is the more general property where the sum is any fixed constant. They are equivalent up to an affine transform of utilities, but they are not the same definition, and a rigor-focused chapter shouldn't claim "equivalent definitions use 1 or any other fixed value" without naming "constant-sum" as the umbrella term.

Slide 6 itself uses the constant-sum framing (per the chapter's own §3.5 note line 208: *"Slide 6 says each player has their own utility function, with the constant-sum property linking the two"*), so the chapter is internally inconsistent: it correctly identifies slide 6 as "constant-sum" then defines "zero-sum" as if those were the same word.

**Severity.** P1 — affects definitional precision in a key §3 concept; an exam answer that wrote "zero-sum means the sum is constant" would be marked down by a strict grader.

**Suggested fix.** Add one sentence: *"Strictly, **zero-sum** means the constant equals 0; the more general property where the sum equals some fixed nonzero constant is called **constant-sum**. The two are equivalent for algorithmic purposes (subtract a constant from one player's utility to convert constant-sum into zero-sum), and slide 6's 'constant-sum' framing applies to both. Throughout this chapter we use 'zero-sum' as shorthand for either."*

### P1-4. §4.2 — beta cutoff inequality could be misread as strict

**Location:** Lines 256–258 (beta/alpha cutoff definitions):
> **Beta cutoff** ... stop searching below $N$ ... as soon as $\alpha(N) \ge \beta(i)$ for some MIN ancestor $i$ of $N$.
> **Alpha cutoff** ... stop searching below $N$ as soon as $\beta(N) \le \alpha(i)$ for some MAX ancestor $i$ of $N$.

But the §4.2.1 pseudocode (lines 289, 298) uses `if v ≥ β: return v` and `if v ≤ α: return v`. These two formulations agree (since $\alpha(N) \leftarrow \max(\alpha, v)$ at a MAX node means the running $v$ is what triggers the test), but the chapter never explicitly states the equivalence. A student tracing the pseudocode by hand and then reading §4.2's definitions has to derive the equivalence themselves.

Additionally, both formulations use $\ge$ / $\le$ (non-strict). This is the correct fail-soft form, but the chapter does not justify *why* non-strict is correct (when v exactly equals β, pruning is still safe because further min-ing can only make this MIN node's value go *down* below β, still not influencing the parent MAX). For a rigor chapter this should be noted.

**Severity.** P1 — definitional precision issue that an attentive student will trip on.

**Suggested fix.** Add a one-line cross-walk after the cutoff definitions: *"In the §4.2.1 pseudocode, the beta-cutoff test is written as `if v ≥ β: return v` at a MAX node — this is exactly $\alpha(N) \ge \beta(i)$ because the running $v$ at a MAX node is what $\alpha(N)$ would be set to next; the test fires either before or right after the assignment depending on the implementation. The non-strict $\ge$ is correct: equality is enough to prune because any deeper child can only push the value *below* the bound, never above."*

### P1-5. §4.4 comparison table — "Optimal? yes vs optimal opp." is restrictive but unspecific

**Location:** Lines 322–326 (comparison table).

The table says **"yes vs optimal opp."** for Minimax and Alpha-beta, and **"optimal expected utility"** for Expectiminimax. The "yes vs optimal opp." cell is correct but elides a stronger property: minimax is *also* optimal against any opponent strategy in the sense that it maximises the *worst-case* payoff over all opponent strategies (not just the optimal-opponent realisation). Cell text could read **"yes (max worst-case payoff; tight vs optimal opp.)"**.

For Depth-limited alpha-beta + Eval, the cell says **"no (depends on Eval)"**. This is too coarse — optimality is undefined when Eval is heuristic; the more precise statement is *"optimal only if Eval(s) = Minimax(s) at every cut-off; in general no guarantee"*.

**Severity.** P1 — the table is the chapter's quick-reference; imprecise cells propagate to cheat-sheet recall.

**Suggested fix.** Tighten the Optimal? column wording for all four rows as above.

---

## P2 findings (mathematical rigor — polish)

### P2-1. §4.3 — "doubling the depth" mnemonic is approximate but stated as fact

**Location:** Line 311: *"with perfect move ordering, alpha-beta searches roughly twice as deep as minimax in the same time budget"*; also §5.4 line 504.

The $O(b^{d/2})$ best-case bound implies that for the **same node budget**, alpha-beta reaches depth $2d$ where minimax reaches depth $d$. "Twice as deep in the same time" is a useful mnemonic but assumes per-node work is roughly equal, which is true for plain DFS but not for sophisticated alpha-beta implementations with move-ordering heuristics, transposition tables, etc. The chapter already labels this "R&N supplementary" — that's enough hedging. P2 only because the phrasing could be sharpened: *"can reach approximately twice the depth"* rather than *"searches roughly twice as deep"*.

### P2-2. §5.4 — the chess argument mixes magnitudes

**Location:** Lines 497–500.

*"$35^{80} \approx 10^{123}$"* — exact computation: $\log_{10}(35^{80}) = 80 \log_{10}(35) \approx 80 \times 1.5441 = 123.5$, so $35^{80} \approx 10^{123.5} \approx 3 \times 10^{123}$. The chapter's $10^{123}$ rounding is the lecture's own (slide 7), but is technically a slight under-estimate. P2 — the rounding tradition is standard; mention it only if pursuing maximum rigor.

### P2-3. §3.1 — "Searching to the bottom of the game tree is ruled out for every interesting game" overstates

**Location:** Line 108.

This is true *as stated for chess and games of comparable branching/depth*. For checkers (depth ≤ 70, $b \approx 6$ on average), exhaustive solution is feasible (and was achieved in 2007 — the chapter says so in §4.7). The sentence is informal motivation, not a theorem, but a hard-rigor reader will notice the tension with the §4.7 "checkers solved in 2007" line. P2 — soften to *"every commercially interesting game"* or *"every game with chess-class branching"*.

### P2-4. §4.6 expectiminimax recursion — implicit assumption on the distribution

**Location:** Lines 350–358 (the piecewise expectiminimax formula).

The CHANCE case uses $\sum_{s'} P(s' \mid s) \, \text{Expectiminimax}(s')$. This silently assumes the children are *enumerated* over a *discrete* outcome space — fine for dice and card-draws but not stated. For a rigor chapter, one line noting *"summing over the discrete outcome space of the chance event; for continuous distributions replace the sum with an expectation"* would close the loop. P2.

### P2-5. §3.4 — the Eval sanity check is correct but doesn't show the sign convention

**Location:** Lines 193–195 (empty-board / X-centre sanity check).

The sanity check correctly computes Eval = 0 (empty) and Eval = 4 (after X centre). It doesn't show what Eval would look like *after O responds* (which is a more pedagogical demonstration of the sign convention). For instance, after X-centre + O-corner: open-for-X drops (the corner-O closes 3 lines), open-for-O drops (the centre-X already closed 4 lines, the corner-O now sits on 3 of them, but only 1 of the corner-O's lines was previously open for O...). Working out one MIN-response level would clinch the heuristic's behaviour. P2 — current sanity check is sufficient, more would be polish.

---

## Standing checks against §7 QA Checklist (mathematical rigor portion)

- [x] **Minimax recursion (eq. line 138–145):** correct piecewise definition; matches slide 14.
- [x] **Expectiminimax recursion (line 350–358):** correct four-case piecewise. Labelled chapter elaboration (slide 39 only states the chance-node case in words). ✓
- [x] **Alpha-beta pseudocode (§4.2.1 lines 280–301):** correct fail-soft alpha-beta; matches R&N 3e §5.3. Cutoff test sits between recursive call and α/β update — standard.
- [x] **Cheat-sheet pseudocode (§8 lines 575–589):** correct combined depth-limited alpha-beta. TERMINAL-TEST → UTILITY checked BEFORE depth-cutoff → EVAL. **Round 1 P1 cleared.**
- [x] **`O(b^{d/2})` best-case complexity:** correctly attributed to R&N 3e §5.3 supplementary (line 311). ✓
- [x] **`O(b^d)` worst-case complexity:** correctly attributed to R&N supplementary (line 312). ✓
- [x] **`O(b^{3d/4})` average-case:** **removed entirely** from the chapter. `grep "3d/4"` returns no matches. **Round 1 P1 cleared.**
- [x] **Coin-game (§5.1) backup table (lines 416–423):** every sub-state's recursion verified by hand against $F(S) \in \{0, 1\}$ convention. All correct. Root = 1 (MAX wins), action = take 3.
- [x] **Chess magnitudes (§3.1 line 108):** $b \approx 35$, $d \approx 80$ ply, $35^{80} \approx 10^{123}$. Arithmetic correct (precise: $10^{123.5}$); the $10^{123}$ rounding matches the lecture.
- [x] **Tic-tac-toe Eval sanity (§3.4 lines 193–195):** Eval(empty) = 0, Eval(X-centre) = 4. Both correct.
- [x] **Backgammon dice (§4.6, Figure 10 caption):** 36 ordered → 21 unordered = 6 doubles + 15 non-double pairs. Probabilities 1/36 (double) and 1/18 (non-double). All arithmetic correct.
- [x] **Alpha-beta cutoff equivalence:** $\alpha(N) \ge \beta(i)$ vs `v ≥ β` — equivalent. (P1-4 above: could be made explicit.)
- [ ] **Figure 8 / §5.2 "same 9-leaf tree" claim:** **FAIL.** See P1-1.
- [x] **Zero-sum vs constant-sum:** broadly correct; precision issue noted in P1-3.
- [x] **Minimax optimality proof sketch (§3.3.1 line 165):** correct induction argument. ✓
- [x] **Comparison table (§4.4):** entries arithmetically correct; coarse wording noted in P1-5.

---

## Out-of-scope observations

- Slide 35 itself is pedagogically muddled — most lecturers' decks show slide 28's tree throughout the alpha-beta walkthrough, so introducing a *different* tree at slide 35 (with leaf-value "1") without flagging the change is the underlying source of the chapter's P1-1 confusion. The chapter inherited this slide ambiguity and tried to paper over it. The honest move is to say "slide 35 quietly switches to a different example tree".
- The §4.5 mention of *forward pruning* could include a one-line caveat that forward pruning makes alpha-beta no longer return the exact minimax value — currently the chapter says it "discard plausibly-bad moves without proving they're bad" (line 337) which gestures at this but does not pin down that the **answer changes**, not just the search cost. (Already a Round 1 P2; deferred.)
- The chapter's claim (line 167) that "Against a sub-optimal opponent, minimax can only do at least as well" is true under the assumption that MIN's sub-optimal action yields a child with minimax value $\ge$ the actual minimum — which is exactly the definition of sub-optimal for MIN — so this is tautological. Not a rigor failure, but the phrasing could acknowledge the tautology more explicitly.

---

## Concerns / risks

The Round 1 fix #8 ("slides 28 and 35 are the same tree") was a course-correction in the wrong direction. The original (Round 1) chapter apparently said they were *different* trees, then the fix made them the *same* tree. Per my P1-1, they are in fact different trees, so the Round 1 chapter was closer to correct than the post-revision version. Recommend reverting the framing in §5.2 lines 457–462 and Figure 8 caption to acknowledge the example shift.

This is the kind of finding that, if missed, will be the first thing a sharp student catches and challenges the instructor with — and the chapter currently provides them with an indefensible "same tree" claim to anchor their challenge.

---

## Status

**Pass with concerns.** The two Round 1 P1 carry-overs are cleanly fixed. No new P0s. Five P1s and five P2s identified, with P1-1 (slide-35 same-tree claim) being the only one that materially breaks rigor; the rest are precision/attribution issues that a strict examiner would deduct partial credit for but that do not invalidate the chapter's main content.

---

## Report to PM

**Assignment recap:** L06 Round 2 — Mathematical Rigor review of `study/lectures/L06-Adversarial-Search.md`, against the Round 1 carry-over P1s (cheat-sheet pseudocode order; unsourced `O(b^{3d/4})`) plus a fresh mathematical-rigor pass on the entire chapter.

**Status:** Pass with concerns.

**P0 findings:** None.

**P1 findings:**
1. **`study/lectures/L06-Adversarial-Search.md` lines 457, 460, 462** — chapter claims slide 35 is "the same 9-leaf tree" as slide 28 and tries to explain the β = 1 prune as "a different sweep on the same tree". Mathematically impossible: slide 35's right MIN has a visible leaf value of `1` which is not in slide 28's right-MIN leaf set $\{14, 5, 2\}$. Reordering cannot conjure a `1` out of $\{14, 5, 2\}$. Suggested fix: rewrite as a **different example tree** with the same structure; remove the "same tree, different sweep" claim.
2. **Line 172** — minimax `O(b^d)` time complexity is attributed to slide 19, but slide 19 only gives tree statistics (depth 5, $b=3$, 15 nodes), not the closed-form bound. Suggested fix: reword to "standard L03 DFS analysis, motivated by slide 19's concrete tree statistics".
3. **Line 206** — definition conflates zero-sum (constant = 0) with constant-sum (any fixed constant). Suggested fix: add a one-line distinction; note that slide 6 actually uses the constant-sum framing.
4. **Lines 256–258 vs 289, 298** — cutoff definitions use $\alpha(N) \ge \beta(i)$ in prose but $v \ge \beta$ in pseudocode without bridging the two. Also non-strict $\ge / \le$ is not justified. Suggested fix: add one bridging sentence; justify non-strict in one line.
5. **§4.4 comparison table, lines 322–326** — "Optimal? yes vs optimal opp." is coarse; "no (depends on Eval)" for depth-limited is too vague. Suggested fix: tighten cell wording per P1-5 body.

**P2 findings:**
1. §4.3 / §5.4 "twice as deep" — accurate but could be reworded as "approximately twice the depth".
2. §5.4 chess: $35^{80}$ more precisely $\approx 10^{123.5}$; current $10^{123}$ matches the lecture, so optional.
3. §3.1 "ruled out for every interesting game" overstates given §4.7's "checkers solved" claim.
4. §4.6 expectiminimax sum implicitly assumes discrete outcome space.
5. §3.4 Eval sanity check could carry one more step (post-O-response) to clinch the sign convention.

**QA Checklist (§7) status — math-rigor portion only:**
- Minimax/expectiminimax/alpha-beta recursions and pseudocode: **Pass.**
- Coin-game backup table arithmetic: **Pass.**
- Chess magnitudes: **Pass.**
- Backgammon dice probabilities: **Pass.**
- Tic-tac-toe Eval sanity: **Pass.**
- Complexity bounds sourcing (`O(b^d)`, `O(b^{d/2})`, `O(b^{3d/4})`): **Pass** (R&N supplementary correctly tagged; the spurious `b^{3d/4}` claim is gone).
- Cheat-sheet pseudocode terminal/horizon order: **Pass.**
- Figure 8 / §5.2 "same tree" claim: **Fail** (P1-1).
- Zero-sum vs constant-sum: **Fail with caveat** (P1-3).

**Acceptance criteria (§1) status:** N/A for a rigor-only reviewer pass; lecture chapter has no formal acceptance criteria. Both Round 1 carry-over P1s are now **Met**.

**DOCUMENT.md audit:** N/A for a lecture chapter under `study/lectures/`. No code-style directories were modified.

**Out-of-scope observations:** The Round 1 P0 fix #8 (slides 28 and 35 reconciliation) was an over-correction — the original chapter's claim that they were *different* trees was closer to correct than the post-fix "same tree, different sweep" framing. Recommend reverting that framing.

**Concerns / risks:** P1-1 is the only finding that materially impairs rigor. The cleanest path is to acknowledge slide 35 as a different example with a different leaf set. If the chapter is going to claim "same tree", the leaf values in the prose must agree with slide 11 / slide 28 leaf values, in which case the β = 1 line has to go.

**What PM should do next:** Dispatch the relevant content engineer to fix the 5 P1s (priority: P1-1 first, since it contains a mathematical impossibility), then re-dispatch reviewer 2 for a Round 3 verification spot-check. P2s can ride into a polish pass later.

**DOCUMENT.md updated:** N/A for QA.

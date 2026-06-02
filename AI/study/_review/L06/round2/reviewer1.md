# L06 Round 2 — Reviewer 1 (Concept Completeness incl. Figures)

**Reviewer role:** Concept Completeness + Figures (Spec §7.1)
**Chapter under review:** `study/lectures/L06-Adversarial-Search.md` (post-Round-1 revision)
**Source of truth:** `Lecture6-Adversarial Search.pdf` (42 slides) + `study/extracted_figures/L06/figures.md` + page-renders (`page05`, `page08`, `page11`, `page18`, `page20`, `page22`, `page28`, `page34`, `page35`, `page38`).
**Stance:** Harsh. Same standard as Round 1.

---

## VERDICT: **REVISE** (one new P1 introduced by the Round-1 fix to P1-6; remaining items are P2 polish)

The Round-1 revision is mostly excellent. Seven of eight Round-1 P1s were resolved cleanly (the four "imported textbook fact" attributions are now uniform; the cut-off-direction prose in §5.2 frame 26–27 is correctly rewritten; the Figure 10, Figure 6 captions and §4.4 expectiminimax row are corrected and qualified; the coins-game backup table is rewritten as a clean bottom-up enumeration). However, the fix to **P1-6** (Figure 8 / slide 35 caption) **over-corrects in the opposite direction** and now states a factually incorrect claim — that slide 35 is the *same 9-leaf tree* as slide 28 with the same leaf set. It is not: slide 35's right-MIN second leaf is labelled **1**, while slide 11 / 28's right-MIN second leaf is **5**. The leaf set genuinely differs, and that is *why* the right MIN's β drops to 1 (which cannot happen on the slide-11 leaf set under any child-ordering). This blocks sign-off because §5.2 is the single most pedagogically important worked example of the chapter.

---

## P0 — None

No P0 issues found. Every algorithm, recursion, and worked-example result still matches the slides exactly.

---

## P1 — Must fix before sign-off

### P1-1. §5.2 / Figure 8 caption — "same 9-leaf tree" claim is factually wrong (new P1, introduced by Round-1 fix to old P1-6)

**Where:**
- chapter line ~459 (Figure 8 caption): *"The **same 9-leaf tree** as Figure 7 (slide 28), re-annotated with explicit $\alpha$/$\beta$ values: root MAX has $\alpha = 3$; the left MIN finishes with $\beta = 3$; the middle MIN ends with $\beta = 2$ followed by 'prune!'; the right MIN ends with $\beta = 1$ followed by 'prune!'. Slide 35 only labels the leaves the sweep actually visits — leaves whose values do not influence the pruning logic are drawn but left unlabelled."*
- chapter line ~457 (§5.2 prose): *"Slide 35 of the lecture revisits the **same 9-leaf abstract tree** and re-annotates the sweep with explicit $\alpha$ / $\beta$ values at each internal node"*
- chapter line ~462 (§5.2 closing): *"Slide 35's annotation reflects the same algorithm on the same tree but emphasises a slightly different sweep where the right MIN's second child also triggers a cutoff at $\beta = 1$ — illustrating that with a different child-ordering at the right MIN, alpha-beta can prune more than 2 leaves."*

**What slide 35 actually shows** (verified directly against `page35-render.png`): the right MIN has **three children drawn but only the first two labelled — 14 and 1** — and the β annotation drops to **1** followed by "prune!".

**Why this can't be the same tree as slide 28.** Slide 11 / slide 28's right-MIN children are $\{14, 5, 2\}$. On left-to-right DFS with $\alpha = 3$ inherited from the left subtree:
- visit leaf 14 → local $v = 14$, $v \le \alpha = 3$? No. Update $\beta \leftarrow 14$.
- visit leaf 5 → $v = \min(14, 5) = 5$, $v \le \alpha = 3$? No. Update $\beta \leftarrow 5$.
- visit leaf 2 → $v = \min(5, 2) = 2$, $v \le \alpha = 3$? Yes — return. *But this is the third child, so no work is pruned.*

The sweep on $\{14, 5, 2\}$ goes $\beta = 14 \to 5 \to 2$ — **at no point does $\beta$ drop to 1**, with or without re-ordering the children. The only way for slide 35's right MIN to show $\beta = 1$ followed by "prune!" is if the slide author **changed the leaf at position 8 from 5 to 1**. (Symmetrically, the third right-MIN leaf is unshown in slide 35, but does not need to be the slide-11 value 2 either.)

So slide 35 is **not** "the same 9-leaf tree". It is a tree with the same shape and the same first 7 leaves $\{3, 12, 8, 2, 4, 6, 14, \mathbf{?}, \mathbf{?}\}$ but the 8th leaf is $\mathbf{1}$ (not 5) and the 9th leaf is unspecified (the slide does not draw a label for it). This is also consistent with the *closing pedagogical point* the chapter is trying to make ("alpha-beta can prune more than 2 leaves") — but the right way to say that is *"with **different leaf values** in the right subtree"*, not "with a different **child-ordering**", because no permutation of $\{14, 5, 2\}$ produces $\beta = 1$.

**This is the exact opposite of the Round-1 P1-6 mistake.** Round 1 said the original chapter wrongly called slide 35 "a different tree"; the Round-1 reviewer's correction ("it's the same tree, just fewer drawn leaves") was *itself partly mistaken* — the leaves drawn are a subset of slide 11's leaves only for the left MIN and the middle MIN's pruned child; for the right MIN, slide 35 introduces the value 1, which does not appear in slide 11 / 28. The Round-1 fix accepted the reviewer's framing literally and is now wrong in the opposite direction.

**Severity:** P1 — affects the worked example that is the entire heart of §5.2 and the pedagogical "look, ordering matters" punch-line. The leaf-count arithmetic (6 visited on slide 35's ordering vs. 7 on slide 28's) is correct in the chapter, but the explanation of *why* slide 35 prunes more is wrong.

**Suggested fix.** Rewrite caption + closing paragraph to: *"Slide 35 shows the same 9-leaf tree **shape** with the same first seven leaves $\{3, 12, 8, 2, 4, 6, 14\}$, but **the second leaf of the right MIN has been changed from 5 to 1** (the third right-MIN leaf is not labelled). With this leaf-value change, the right MIN's $\beta$ drops to 1 on its second child, and since $\beta = 1 \le \alpha = 3$ from the left subtree, the right MIN's third child is pruned. So under slide 35's leaves $\{3, 12, 8, 2, 4, 6, 14, 1, ?\}$ the algorithm visits $3 + 1 + 2 = 6$ leaves of the 9-leaf tree (with 3 pruned: middle MIN's 4 and 6, plus the right MIN's third child). The pedagogical point: alpha-beta's prune count depends on the leaf values it encounters; small changes (here, $5 \to 1$) can move whole subtrees from 'visit' to 'prune'."*

This wording is honest about the slide having changed values and frames the "more aggressive pruning" lesson correctly. (Move-ordering as a separate knob can still be discussed in §6 pitfall 4 as a textbook supplement.)

---

## P2 — Should fix (polish, accuracy, helpfulness)

### P2-1. §4.2 / Figure 4 caption — slide 20 has three structural levels (MAX → MIN → MAX-leaves), not two

**Where:** chapter line ~271 (Figure 4 caption): *"MAX root with two MIN children whose leaves are (2, 7) and (1, ?)."*

**Slide 20 actually shows** three labelled levels: MAX (root) → MIN (two children) → MAX (four leaves labelled 2, 7, 1, ?). The chapter caption conflates "MIN's children" with "leaves", which is fine in a 2-deep example but loses the level-alternation point. Minor.

**Suggested fix:** *"MAX root with two MIN children; the children of each MIN are MAX-level leaves (2, 7) and (1, ?)."*

### P2-2. §5.2 frames 26–27 narrative — small wording issue around "all three children have already been examined"

**Where:** chapter line ~449 (frame 26–27): *"Cutoff test: $2 \le 3$? **Yes** — the function would return immediately, but in this case all three children have already been examined, so the return value is simply 2."*

This is technically right (the third child triggered the cutoff condition right at the moment its value was incorporated into $v$, but with no siblings left to skip), but the phrase "the function would return immediately" combined with "all three children have already been examined" reads as if the function were *prevented* from returning. A clearer phrasing: *"$2 \le 3$? **Yes** — the cutoff condition is satisfied, so the function returns $v = 2$. The third child was the last one, so the cutoff saves zero work in this particular ordering."*

### P2-3. §5.1 narrative order vs. slide-figure edge order — addressed in spirit but the parenthetical note belongs *before* the table, not after

**Where:** chapter line ~427 — note about slide 18's branch order (3, 2, 1) versus the table's size order is placed *after* the table.

Putting it *before* the table would let students re-frame their expectations on first read. Minor.

### P2-4. §6 pitfall 4 — phrasing "slides 28 and 35 both walk the same 9-leaf abstract tree" inherits the same P1-1 error

**Where:** chapter line ~515 (pitfall 4): *"The lecture itself does not introduce move ordering as a knob (it is not in slides 21–22 or 35); slides 28 and 35 both walk the same 9-leaf abstract tree but make different aspects of the sweep visible."*

If P1-1 is fixed, this sentence needs to be reconciled. Either rewrite to *"slide 28 and slide 35 walk **closely-related** 9-leaf abstract trees that differ only in the right-MIN's second leaf (5 vs 1)"* or drop the parenthetical entirely.

### P2-5. §4.7 — TD-Gammon "1992" year and Stockfish-NNUE / Leela-MCTS facts are still chapter elaboration

**Where:** chapter lines ~375 (Backgammon: TD-Gammon (1992)) and ~374 (Stockfish/Leela parenthetical).

The Round-1 revision labels the Stockfish/Leela line as "chapter elaboration"; the TD-Gammon 1992 date is *not* explicitly labelled the same way. If "AlphaGo (2016)" and "AlphaStar" got chapter-elaboration tags, "(1992)" should too — the slide itself may say only "TD-Gammon" without a year.

**Suggested fix:** *"TD-Gammon (chapter elaboration: 1992) used reinforcement learning…"* or verify against slide 40 and either keep the year as slide content with a citation or tag it.

### P2-6. §5.2 "Slide 35 ordering only prunes 3 leaves" — chapter implicitly assumes the third right-MIN leaf would have been pruned

The chapter says under slide 35's ordering, 6 leaves are visited (3 + 1 + 2) and 3 are pruned. This is correct (middle MIN's two pruned + right MIN's third pruned). But the chapter never *names* which 3 leaves are pruned by value, because under slide 35 the unlabelled leaves don't have known values. Make the count explicit and tie it to the visited-set: *"slide 35's ordering visits leaves $\{3, 12, 8, 2, 14, 1\}$ — six leaves — and prunes the remaining three positions (middle MIN's second and third children, and right MIN's third child)."*

### P2-7. Cheat-sheet pseudocode return inside cutoff — fail-hard vs. fail-soft still not flagged

The §8 cheat-sheet pseudocode returns `v` on cutoff (fail-hard variant — this is the textbook formulation). For Lab 5 students who later read other sources, a one-line footnote (*"this is the 'fail-hard' variant — some textbooks return α or β on cutoff instead, called 'fail-soft'; both produce the same root-decision"*) would close a frequent rabbit-hole. P2 because the slides don't distinguish either.

### P2-8. §5.3 right-MIN single-child caption could be tightened

**Where:** chapter line ~487 (Figure 9 caption): *"in the full game the right MIN would have one candidate per legal O-move from its parent position, but the alpha-cutoff stops the search after the first one without expanding the others."*

This is a useful clarification but the phrasing "one candidate per legal O-move from its parent position" is a mouthful. Compact form: *"in the full game tree this right MIN has one child per legal O-move; the alpha-cutoff stops search after the first."*

### P2-9. §4.4 footnote ‡ marker is on the alpha-beta "Time (best)" cell only — should also mark "Time (worst)"

**Where:** chapter line ~324 (table row "Alpha-beta"): *"$O(b^d)$ | $O(b^{d/2})$ ‡"*. The ‡ footnote covers both bounds in its text but the marker visually attaches to only the best-case cell. Add a ‡ on the $O(b^d)$ worst-case cell too, so a reader skimming the table sees both numbers as R&N-attributed.

### P2-10. §3.3.1 — claim about "every branch eventually hits a terminal" is the *definition* of a finite tree, not an additional property

**Where:** chapter line ~171: *"Complete on finite game trees (every branch eventually hits a terminal)."*

Round 1 flagged this as tautological; Round 2 added the L03 cross-reference but kept the parenthetical, which still reads as a definition rather than a property. Trivial polish; consider just *"Complete on **finite** game trees (the L03 §3 sense of completeness applied to alternating-turn trees)."*

---

## EVIDENCE — verification against slides

| Claim in chapter | Source check | Round 1 status | Round 2 status |
|---|---|---|---|
| Poker is in slide-5 taxonomy | Slide 5 | ✗ (Poker not on slide) | ✓ Removed; chapter clarifies slide 3 mentions Poker only as motivation |
| Tic-tac-toe utility $\{-1, 0, +1\}$ with 0 = draw | Slide 8 | ✓ but caption confusingly worded | ✓ Rewritten cleanly, 0 = draw bolded |
| Coin game utility $F(S) \in \{0, 1\}$, no draws | Slide 17 | ✓ | ✓ Now explicitly contrasted with slide-8 convention |
| Minimax recursion | Slide 14 | ✓ | ✓ unchanged |
| Alpha-beta cutoff rules | Slide 22 | ✓ | ✓ unchanged + cross-link to §6 pitfall 2 added |
| Tic-tac-toe Eval formula | Slide 30 | ✓ | ✓ + empty-board sanity check added |
| Chess $35^{80} \approx 10^{123}$ | Slide 7 | ✗ ("continuations") | ✓ Now "nodes in its full game tree" |
| Coin-game minimax answer = 1, MAX plays "take 3" | Slide 18 | ✓ correct conclusion, dense narration | ✓ Rewritten as bottom-up sub-state table |
| Abstract tree root = 3, MAX picks $a_1$ | Slide 11 | ✓ | ✓ |
| 7 of 9 leaves visited on slide-28 ordering | Slides 23–28 | ✓ | ✓ Frames 25, 26–27 prose rewritten cleanly |
| Slide 35 leaf set | Slide 35 | ✗ ("different tree") | ✗ ("same 9-leaf tree" — **new P1-1**) |
| Average case $O(b^{3d/4})$ | Slides 1–42 | ✗ (not in slides) | ✓ Removed entirely |
| Space $O(bd)$ | Slides 1–42 | ✗ (not in slides) | ✓ Attributed to L03 |
| Best-case $O(b^{d/2})$, worst-case $O(b^d)$ | Slides 1–42 | partial | ✓ Both tagged R&N supplementary in §4.3, §5.4, §6 pitfall 4 |
| Expectiminimax time complexity | Slides 1–42 | ✗ ($O(b^d n^d)$ unattributed) | ✓ Replaced with "not given by slides" + footnote |
| Expectiminimax "optimal" claim | Slide 39 | ✗ unqualified | ✓ Qualified to "optimal expected utility" |
| Completeness on finite trees | Slides 1–42 | ✗ unattributed | ✓ L03 cross-reference added (minor wording polish — P2-10) |
| Figure 10 caption — backgammon probabilities | Slide 38 | ✗ overgeneralised | ✓ Rewritten to "representative branches" |
| Figure 6 caption — yellow/red at leaves | Slide 18 | ✗ ambiguous | ✓ Clarified to turn-alternation rule even at terminals |
| AlphaGo 2016, AlphaStar | Slide 40 | ✗ unattributed | ✓ Tagged "chapter elaboration, not on slide" |
| Stockfish-NNUE / Leela-MCTS | Slide 40 | ✗ unattributed | ✓ Tagged "chapter elaboration" |
| TD-Gammon (1992) year | Slide 40 | not flagged | (P2-5: still unlabelled vs. other elaborations) |
| Zermelo / Shannon / McCarthy / Samuel dates | Slide 41 | ✓ | ✓ unchanged |

### Figure coverage audit

All ten chapter figures (1: slide 5, 2: slide 8, 3: slide 11, 4: slide 20, 5: slide 22, 6: slide 18, 7: slide 28, 8: slide 35, 9: slide 34, 10: slide 38) remain correctly embedded via their `page-render` rasters. Captions for Figures 1–7, 9, 10 are now accurate. **Figure 8's caption is the single remaining factual error.** No new figures need to be added; the Round-1 P2-11 suggestion to embed intermediate frames (slides 24, 25) was deferred and is acceptable for a reference chapter.

**Missing figure coverage:** None.

---

## What's missing / concerns

1. **Slide 40 verification not done with a page-render.** No `page40-render.png` exists in `extracted_figures/L06/`, so claims about slide 40's content (TD-Gammon date, AlphaGo year, Stockfish/Leela presence) rely on the lecturer's narration not the slide. The Round-1 fix tagged most of these as "chapter elaboration" but TD-Gammon 1992 is not tagged (P2-5).
2. **`page40-render.png` and `page41-render.png` could be generated** if the figures catalogue were exhaustive — slide 41 (origins) carries factual claims (Zermelo 1912, Shannon 1949, McCarthy 1956, Samuel 1956) that are currently verified only against the figures catalogue's prose summary.
3. **§5.2 leaf-arithmetic** is correct under both slide-28 ordering (7 visited) and slide-35 ordering (6 visited), but the *reason* slide 35 prunes more is the leaf-value change, not move ordering. The chapter still tries to use this example to motivate move ordering, which is the wrong takeaway — the right takeaway is "different leaf values can move whole branches in/out of the prune set". See P1-1.

---

## Report to PM

**Assignment recap:** L06 Round 2 — Reviewer 1 (Concept Completeness incl. Figures). Source: `Lecture6-Adversarial Search.pdf` (42 slides). Chapter: `study/lectures/L06-Adversarial-Search.md` (post-Round-1 revision). Round 1 reviewer: 8 P1, no P0. Round 1 reviewer file: `study/_review/L06/round1/reviewer1.md`. Revision summary: `study/_review/L06/round1/revise-summary.md`.

**Status:** Pass with concerns (REVISE — one P1 + minor polish)

**P0 findings:** None.

**P1 findings:**
1. **P1-1** — §5.2 / Figure 8 caption / §5.2 closing paragraph (chapter lines ~457, ~459, ~462) state that slide 35 is "the same 9-leaf tree as slide 28" and attribute the additional pruning to "a different child-ordering". This is **factually wrong**. Slide 35's right-MIN second leaf is labelled **1** (not 5 as in slide 11 / 28); no permutation of $\{14, 5, 2\}$ produces $\beta = 1$ at the right MIN. Slide 35 deliberately changes that leaf value to make a second prune fire. **Suggested fix:** rewrite the caption and the closing paragraph to state explicitly that slide 35 has the same tree *shape* and the same first seven leaves but changes the eighth leaf from 5 to 1; reframe the pedagogical point as "different leaf values move subtrees in/out of the prune set" rather than "different child-ordering". This is the only blocking item and it sits squarely in the chapter's most pedagogically important worked example.

**P2 findings:**
1. **P2-1** — Figure 4 caption (~line 271) lightly conflates "MIN's children" with "leaves" on slide 20's three-level tree. Trivial wording fix.
2. **P2-2** — §5.2 frame 26–27 prose (~line 449) phrases the third-child cutoff slightly awkwardly ("would return immediately, but…"). Compact rewrite suggested.
3. **P2-3** — §5.1 the parenthetical note about slide 18 drawing branches in 3-2-1 order (vs. the chapter's size-ordered table) is placed *after* the table; should be moved *before* for first-read clarity.
4. **P2-4** — §6 pitfall 4 (~line 515) repeats the "slides 28 and 35 both walk the same 9-leaf tree" framing; needs to be reconciled with the P1-1 fix.
5. **P2-5** — §4.7 (~line 375) TD-Gammon "(1992)" date is not labelled as chapter elaboration the way AlphaGo "(2016)" and AlphaStar are. Either label or verify against slide 40.
6. **P2-6** — §5.2 closing leaf-count under slide-35 ordering should name which 3 positions are pruned by location, not just by count.
7. **P2-7** — §8 cheat-sheet pseudocode is the fail-hard variant; a one-line note distinguishing fail-hard vs. fail-soft would close a rabbit-hole for Lab 5 implementers (slides don't either; lowest priority).
8. **P2-8** — Figure 9 caption (~line 487) "one candidate per legal O-move from its parent position" can be compacted.
9. **P2-9** — §4.4 table footnote ‡ marker is only on the best-case cell; should also mark the worst-case $O(b^d)$ cell so a skim-reader sees both numbers tagged R&N.
10. **P2-10** — §3.3.1 (~line 171) "(every branch eventually hits a terminal)" still reads as a definition of "finite", not an additional property. Trivial polish.

**QA Checklist (Spec §7.1) status:**
- Every glossary term from §3 covered in canonical form: **Pass** (Round-1 glossary expansion is comprehensive).
- Every algorithm from §4 has pseudocode or explicit recursion: **Pass**.
- Every worked example reproducible from the chapter alone: **Pass with concerns** — §5.2's slide-35 explanation is wrong (P1-1), but the slide-28 walkthrough is reproducible.
- Every figure in `figures.md` either embedded or with explicit skip rationale: **Pass**.
- All "Lecture 6, slide $X$" citations check out: **Pass** for slide-attributed content. Imported textbook facts (R&N) are now uniformly tagged supplementary or chapter elaboration. The remaining slide-40 elaborations (TD-Gammon year — P2-5) are minor.

**Acceptance criteria status:**
- Concept completeness vs source PDF: **Met with P1-1 fix** — all slide concepts are covered; the slide-35 leaf-change observation is the only outstanding factual gap.
- Figure coverage: **Met** — every diagram-bearing slide is referenced; Figure 8's caption is the lone inaccuracy.

**DOCUMENT.md audit:** N/A (study chapter, not implementation).

**Out-of-scope observations:**
- The Round-1 reviewer (myself) called slide 35 "the same tree, fewer drawn leaves" in P1-6. That framing was *itself* partly mistaken (the leaves drawn are a strict subset only on the left and middle MIN; the right MIN introduces the value 1 not in slide 11). The Round-1 fix accepted the reviewer's framing verbatim, propagating my error into the chapter. P1-1 above is the correction.
- The `page40-render.png` and `page41-render.png` would close minor verification gaps around slides 40–41 (state-of-the-art and origins). Not blocking; consider generating in a future figure-catalogue pass.
- §5.1 bottom-up table is a significant improvement over Round 1's narration — recommend it as a template for similar worked examples in other lectures.

**Concerns / risks:**
- §5.2 is the single most pedagogically important section of the chapter (Lab 5 directly builds on it). The P1-1 mis-attribution of slide 35's behaviour is exactly the kind of subtle error that erodes student trust at exam time, because a careful reader running the algorithm by hand on slide 11's leaves will not reproduce the slide-35 picture and will conclude *something* is wrong with the chapter. Fix this before the next reviewer pass.
- Otherwise the chapter is in very good shape: notation discipline ($U$ vs Eval) is now clean, citation discipline is now uniform, and the cheat-sheet is consistent with the body of the chapter.

**What PM should do next:** Dispatch a backend / chapter-author employee to fix the single P1-1 (slide-35 caption + §5.2 closing paragraph + §6 pitfall 4 P2-4 reconciliation). The P2 items are all polish and can be batched after other Round-2 reviewers report. **Re-QA only on §5.2 and §6 pitfall 4** is sufficient — the rest of the chapter does not need another pass from this reviewer.

**DOCUMENT.md updated:** N/A for QA / reviewer.

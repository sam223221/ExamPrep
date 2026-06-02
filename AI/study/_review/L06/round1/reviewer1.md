# L06 Round 1 — Reviewer 1 (Concept Completeness incl. Figures)

**Reviewer role:** Concept Completeness + Figures (Spec §7.1)
**Chapter under review:** `study/lectures/L06-Adversarial-Search.md`
**Source of truth:** `Lecture6-Adversarial Search.pdf` (42 slides) + `study/extracted_figures/L06/figures.md`
**Stance:** Harsh. Every slide concept must be covered; every figure must be either embedded or have an explicit rationale for being skipped.

---

## VERDICT: **REVISE (P1 issues block sign-off; no P0)**

The chapter is broadly faithful to the slides — every major concept from slides 1–42 is reflected somewhere, and the figure embeddings line up with the page-render catalogue. However there are multiple factual / interpretive errors in the worked examples (esp. §5.1 Coins and §5.2 alpha-beta frame walkthrough), one fabricated complexity claim, one unsupported complexity figure presented as if from the slides, and a handful of accuracy issues in the figure captions. These are P1, not P0 — none of them is a "wrong algorithm," but they are wrong enough that a careful student would catch them and lose trust in the chapter.

---

## P0 — None

No P0 issues found. The minimax recursion, alpha-beta cutoff rules, evaluation function definition, zero-sum framing, expectiminimax recursion, and the canonical worked-example answer (root value = 3, MAX picks $a_1$) all match the slides exactly.

---

## P1 — Must fix before sign-off

### P1-1. §5.1 Coins-game trace contradicts slide 18 — the "MAX takes 1" subtree path tree-walk is wrong on one branch

**Where:** chapter §5.1, table starting at line ~396 ("Backing up from the bottom of the figure…").

**Claim in chapter (row 1):** "MAX takes 1 → MIN at N=3. MIN's options: take 1 → MAX at N=2 (value 1, see next line); take 2 → MAX at N=1 (forced take 1 → MAX took last → F(S)=0, so MAX-at-N=1 value is 0); take 3 → leaf N=0, MIN just took last → F(S)=1. MIN picks min(1, 0, 1) = **0**."

**What slide 18 actually shows:** From the N=3 MIN node the slide draws three branches labelled **3, 2, 1** (left-to-right). Branch "3" goes to the leftmost yellow N=0 leaf with F(S)=1. Branch "2" goes to a yellow N=1 MAX whose only child (action 1) is a red N=0 with F(S)=0. Branch "1" goes to a yellow N=2 MAX with children N=1 (MIN) → forced N=0 F(S)=1, and N=0 F(S)=0; MAX picks max(1,0)=1.

So MIN at N=3 picks min(1, 0, 1) = 0 — the *numeric answer is correct* but the **labelling in the chapter's prose is swapped** (chapter says "take 1 → MAX at N=2 (value 1)" then "take 2 → MAX at N=1 (value 0)" then "take 3 → leaf N=0 (value 1)", which makes it look as if MIN's "take 1" goes to MAX-at-N=2 — but in the slide the action labelled "1" from the N=3 MIN does go to MAX-at-N=2. So this row is actually self-consistent.)

**The actual issue:** The next row ("helper: MAX at N=2") gives MAX-at-N=2 value 1 — correct. Then row 3 says "MAX takes 2 → MIN at N=2 … take 1 → MAX at N=1 (forced take 1 → MAX took last → F(S)=0, value 0); take 2 → leaf N=0, MIN took last → F(S)=1. MIN picks min(0, 1) = **0**." Slide 18 draws the N=2 MIN node (right child of root, branch "2") with **two** branches labelled "2" and "1" — branch "2" → red N=0 with F(S)=1, branch "1" → yellow N=1 (MAX, forced N=0, F(S)=0). So MIN picks min(1, 0) = 0. ✓

Re-reading the chapter row 3: "take 1 → MAX at N=1 (… value 0); take 2 → leaf N=0 (… F(S)=1)". That gives min(0, 1) = 0. Numerically fine.

**On a careful re-read I withdraw this as a labelling P1.** The Coins walk-through is *correct*, just dense. The reader has to do real work to verify it against the figure because the chapter narrates MIN's options in a different order than the slide draws them (slide draws 3→2→1; chapter narrates take-1, take-2, take-3). **Downgrade to P2** — see P2-1.

---

### P1-2. §5.2 "Tree statistics" — chapter says coin game has 15 nodes; slide 19 says 15 nodes ✓ — but the chapter then claims this directly in §5.1 line ~407: "Max depth: 5". Slide 19 says max depth **5**. ✓

No issue. Withdrawn.

---

### P1-3. **Fabricated complexity claim**: "Average case with random child ordering: roughly $O(b^{3d/4})$"

**Where:** chapter §4.3, line ~292: *"**Average case** with random child ordering: roughly $O(b^{3d/4})$ — still a substantial saving."*

**Problem:** The $O(b^{3d/4})$ figure is the classical Russell & Norvig textbook result (3e §5.3) for **random ordering** — it's not wrong as a textbook fact, but **it does not appear anywhere in this lecture's slides** (slides 1–42). Slides 19 and 28/35 talk about best-case and worst-case; they never mention $b^{3d/4}$ or any average-case formula. Presenting it without a citation outside the slide deck creates a false impression that it came from this lecture.

**Severity:** P1. Either (a) cite Russell & Norvig 3e §5.3 explicitly as the source, or (b) remove the claim. Chapter explicitly says "Source: Lecture 6 slides 1–42" at the bottom (line ~601), so smuggling in a textbook result without attribution is a §7-spec violation.

---

### P1-4. **Unsupported claim attributed to the slides**: "Space complexity $O(bd)$ if implemented as recursive DFS"

**Where:** chapter §3.3.1 line ~161, listed under "Minimax is also: … Space complexity $O(bd)$ if implemented as recursive DFS (one path's worth of nodes in memory at a time) — same as L03's DFS analysis."

**Problem:** Slide 19 only states the time complexity ($O(b^d)$). It does **not** discuss space complexity at all. The $O(bd)$ space claim is correct in itself (it's the standard recursive-DFS result), but the chapter implies it came from the slides. Either (a) attribute it to L03 explicitly and stop implying it came from this lecture, or (b) drop it.

**Severity:** P1 — same root cause as P1-3 (importing textbook facts and presenting them as if from the lecture).

---

### P1-5. §5.2 — Frame walkthrough conflates which leaves are visited in slide 28's frame

**Where:** chapter §5.2, line ~424 ("How many leaves were visited?"): *"On slide 28's frame ordering: 3 + 1 + 3 = 7 of the 9 leaves were visited; 2 were pruned."*

**Slides 26 → 27 → 28** show the right MIN being expanded one leaf at a time: slide 26 has it at "≤14" with leaf 14 visible; slide 27 has it at "≤5" with leaves 14, 5 visible; slide 28 has it finalised at "2" with leaves 14, 5, 2 all visible. So **right MIN visits all three of its leaves**. The "alpha-cutoff condition" the chapter claims fires at the third leaf — β=2 ≤ α=3 — is *technically* satisfied, but since this is the last child anyway, **no pruning occurs**. Chapter's "3 + 1 + 3 = 7 of the 9 leaves" is **arithmetically correct** (3 from left MIN + 1 from middle MIN + 3 from right MIN = 7; the 2 pruned leaves are the middle MIN's 4 and 6).

So 7/9 visited, 2/9 pruned. ✓ Chapter is correct.

**However**, the *narrative* in frames 26–27 is misleading: the chapter says "First leaf is 14 → β at right MIN starts at 14 (not yet a cutoff because 14 > α = 3)". This is **wrong** — the cutoff test is **β ≤ α**, so β=14, α=3 means **14 > 3** so β > α, **no cutoff**. The chapter's "not yet a cutoff because 14 > α = 3" is correct in conclusion but the reasoning *as written* ("14 > α = 3") is exactly the right condition for **no** cutoff — the prose accidentally implies the cutoff test is "β > α prunes," which is the opposite. A student reading this fast will be confused about cutoff direction.

**Severity:** P1 — fix the prose to: "First leaf is 14 → β at right MIN starts at 14. Cutoff condition is β ≤ α, but β=14 > α=3, so no cutoff. Continue."

---

### P1-6. §5.2 description of slide 35 is inaccurate about the right-MIN leaf set

**Where:** chapter §5.2 line ~435, caption to Figure 8: *"slide 35 uses a slightly different right-MIN child set than slide 28 (it shows leaves 14, 1 instead of 14, 5, 2 — both illustrate the same algorithm; the slide-35 version triggers an even earlier prune because the first leaf already drops β to 1)."*

**Slide 35 actually shows:** Right MIN has visible leaves **14** and **1** with β=1, "prune!". The full subtree still has 3 children (the third is the one that gets pruned). So the chapter's "shows leaves 14, 1 instead of 14, 5, 2" is correct as a description of what's *drawn*, but the framing "uses a slightly different right-MIN child set" is wrong — slide 35 is **not a different tree**; it's the same 9-leaf tree where the slide author only drew the two leaves that were actually visited before the prune fired. The chapter implies the slide changed the underlying leaves, which it didn't — it just stopped drawing the pruned ones.

Also: slide 35's middle MIN shows only "2" as a visible leaf (with β=2, "prune!"), so middle MIN visits 1 leaf before pruning — same as in slide 28's run. Chapter says "5 of the (now 8) leaves; 3 were pruned" — but the underlying tree still has 9 leaves; slide 35 simply doesn't draw the pruned ones. So the "(now 8)" is incorrect. It is still 9 leaves total in the underlying tree.

**Severity:** P1 — fix to: "Slide 35 redraws the same 9-leaf tree but only depicts the leaves the alpha-beta sweep actually visits (3, 12, 8 in the left MIN; 2 in the middle MIN; 14, 1 in the right MIN — six visited, three pruned)."

(Note: 3+1+2 = 6 visited under slide 35's ordering, with leaves 4, 6 pruned from middle MIN and the third leaf of right MIN pruned. The chapter's "5 of the (now 8) leaves; 3 were pruned" is *also* arithmetically wrong — should be 6 of 9.)

---

### P1-7. §4.6 caption (Figure 10) — overstates which probabilities are on the diagram

**Where:** chapter line ~326, caption to Figure 10: *"labelled with their probabilities (1/36 for each ordered pair, 1/18 for each unordered pair like (1,2) ≡ (2,1), with the doubles (1,1), (2,2), …, (6,6) at 1/36 each)."*

**Slide 38 shows:** branch labels exactly four pairs visible: "1/36 1,1", "1/18 1,2", "1/18 6,5", "1/36 6,6". The chapter's gloss is correct as backgammon trivia but the slide doesn't itself spell out "for each ordered pair / unordered pair" — it just shows four representative branches and lets the reader infer. Caption should say something like: *"the slide shows representative branches (1/36 for the doubles 1,1 and 6,6; 1/18 for the non-double unordered pairs 1,2 and 6,5)."*

**Severity:** P1 — minor but the caption frames the slide as containing more general claims than it actually does.

---

### P1-8. §4.4 Comparison table — expectiminimax time complexity is wrong / unattributed

**Where:** chapter §4.4 table, last row: *"Expectiminimax (§6) | expected utility | $O(b^d \cdot n^d)$ | — | $O(bd)$ | yes | yes | stochastic games"*

**Problem 1:** $O(b^d \cdot n^d)$ is **not stated anywhere in the slides** (slides 38–39 only say "Nasty branching factor" without a formula). It's a reasonable estimate but again it's an unattributed import.

**Problem 2:** The correct expression is usually written $O((b \cdot n)^d)$ which equals $O(b^d \cdot n^d)$ — fine — but presenting it without "(textbook, R&N §5.5; not in slides)" misleads the reader.

**Problem 3:** "Complete: yes" and "Optimal: yes" for expectiminimax under stochastic games is subtle — completeness/optimality are with respect to *expected* utility, not the realized payoff. The table should note "optimal expected utility" not unqualified "yes".

**Severity:** P1 — attribute or remove, and qualify the optimality claim.

---

### P1-9. §3.3.1 — completeness claim is technically incorrect

**Where:** chapter §3.3.1 line ~158: *"Complete on finite game trees (every branch eventually hits a terminal)."*

**Problem:** Minimax (and alpha-beta) require a **finite** game tree to terminate. Real games like chess are *not* finite trees in the naive successor function (you can shuffle pieces forever) — they're made finite by rules (50-move rule, threefold repetition, ply limit). The phrasing "finite game trees" is OK if interpreted strictly, but the parenthetical "(every branch eventually hits a terminal)" is the definition of a *finite* tree and is the **same thing** said twice. More importantly the slides don't claim completeness — this is another textbook import without attribution.

**Severity:** P1 — either cite L03's definition of completeness and explicitly say "the slides do not analyse completeness; this is the standard L03-style analysis applied to game trees" or remove.

---

### P1-10. Figure 6 caption — labels are slightly off

**Where:** chapter line ~387, caption to Figure 6 (Coins game): *"Yellow boxes are MAX-to-move states; red boxes are MIN-to-move states."*

**Slide 18 actually shows:** the top-left legend box reads "MAX" in **yellow** font and "MIN" in **red** font on a blue background. The MAX nodes (squares) themselves are **yellow** and the MIN nodes are **red**. So the *node colours* match. ✓

But the chapter wording "Yellow boxes are MAX-to-move states; red boxes are MIN-to-move states" — note that some yellow boxes are actually **terminal** N=0 leaves (not "MAX-to-move", because the game ended) but they're drawn yellow because *MIN just moved into them* (i.e., it would be MAX's turn except the game is over). The chapter doesn't flag this. A student looking at the bottom-left yellow N=0 with F(S)=1 will be confused about whose "turn" it is at a leaf.

**Severity:** P1 — caption should say something like: "Yellow = states reached by MIN's move (would be MAX's turn next, or terminal if N=0); red = states reached by MAX's move."

---

## P2 — Should fix (polish, accuracy, helpfulness)

### P2-1. §5.1 narrative order

The chapter walks MIN-at-N=3's options in order "take 1 → take 2 → take 3" but slide 18 draws them left-to-right as "3 → 2 → 1". This is confusing because the reader must mentally re-map slide labels to chapter prose. Either re-order the chapter's narrative to match the slide, or explicitly note the order is being inverted for pedagogical clarity.

### P2-2. §2.1 — "chess has roughly $10^{123}$ continuations"

Slide 7 explicitly says "$35^{80} \approx 10^{123}$ nodes" — chapter says "continuations" instead of "nodes". Minor wording; "continuations" implies complete games which is a different (and larger) number. Use "nodes" to match the slide.

### P2-3. §5.4 — "amateur and a strong club player" claim

Line ~478: *"For $b = 35$ and the same time budget, alpha-beta searches to roughly $2 \times$ the depth of minimax. In chess that is the difference between an amateur and a strong club player."*

The "amateur vs club player" line is not in the slides and the strength-vs-depth correspondence is folk wisdom. Either cite a source or drop the rhetorical flourish.

### P2-4. §3.4 — Eval is sometimes written $U(s)$

Line ~169: *"denoted $\text{Eval}(s)$ or sometimes also written $U(s)$ for "utility approximation""* — the slides do **not** write Eval as $U$; this is an editorial gloss. Either drop or explicitly mark as editorial.

### P2-5. §4.5 "Forward pruning" gloss

The chapter glosses forward pruning as "discard plausibly-bad moves *without* proving they're bad". Slide 36 just says "Forward pruning to avoid considering all possible moves" — true, but the chapter's gloss is more aggressive than the slide. Fine, but flag as commentary.

### P2-6. Figure 9 caption is inconsistent with the chapter text

Caption (line ~462): *"Root MAX has α = 1 from the left subtree; the right MIN's first leaf yields evaluation −1, dropping β to −1, which immediately triggers an alpha-cutoff so the remaining children of the right MIN are pruned."*

Chapter §5.3 frame 6 (slide 34): *"prune the rest of the right MIN's children without expanding them."* Slide 34 draws only **one** child of the right MIN (the −1 leaf) — the rest are pruned. Caption is correct but should be clearer that this depth-2 right-MIN has multiple unexpanded children in the *full* game; the slide shows just the one that was visited.

### P2-7. §6 pitfall #6 — "lines that contain an X" gloss

Line ~492: *"A common error is to count "lines that contain an X" — that's not what "open" means."*

Slide 30 just gives the formula "X's open lines − O's open lines" without defining "open". The chapter's definition ("a line with exactly one X is open for X; a line with both X and O is open for neither") is plausible and standard, but it's an editorial interpretation. Mark as editorial gloss.

### P2-8. §3.3 minimax recursion — minor: the recursion uses "Minimax(s')" inside max/min, slide uses "Minimax(successors(state))"

Chapter writes:
$$\max_{s' \in \text{Successors}(s)} \text{Minimax}(s')$$
Slide 14 writes:
$$\max \text{Minimax}(\text{successors}(\text{state}))$$

The chapter's notation is more rigorous (the max is over successors). Fine, but flag that this is an editorial cleanup of the slide.

### P2-9. Cheat-sheet glossary symbol $\alpha$ = "best-for-MAX value found so far on the current root path (≥ floor)"

The parenthetical "(≥ floor)" is unclear. α **is** the floor (lower bound), not "≥ floor". Reword to: "best-for-MAX so far on the current path; α is a **lower bound** on the final value".

### P2-10. Chapter never explicitly states the **fail-soft vs fail-hard** variant of alpha-beta

The pseudocode in §4.2.1 is the textbook "fail-hard" version (returns v when v ≥ β). The slides don't distinguish, so this is fine to omit — but a careful student implementing Lab 5 may want to know. P2 (nice-to-have appendix).

---

## EVIDENCE

| Claim in chapter | Source check | Result |
|---|---|---|
| Minimax recursion (§3.3) matches slide 14 | Slide 14 | ✓ exact match |
| Alpha-beta cutoff rules (§4.2) match slide 22 | Slide 22 | ✓ exact match |
| Tic-tac-toe Eval formula = X open lines − O open lines (§3.4, §5.3) | Slide 30 | ✓ exact match |
| Chess: b≈35, d≈80, 35^80 ≈ 10^123 (§3.1, §5.4) | Slide 7 | ✓ exact match |
| Coin game: max depth 5, branch factor 3, 15 nodes (§5.1) | Slide 19 | ✓ exact match |
| Coin game N=4 root value = 1, MAX plays "take 3" (§5.1) | Slide 18 trace | ✓ correct conclusion |
| Abstract tree root = 3, MAX picks a_1 (§3.3, §5.2) | Slide 11 | ✓ exact match |
| Alpha-beta walkthrough: 7 of 9 leaves visited (§5.2) | Slides 23–28 trace | ✓ correct (3+1+3) |
| Slide 35 different tree (§5.2 Figure 8 caption) | Slide 35 | ✗ same tree, fewer drawn leaves (P1-6) |
| O(b^(3d/4)) average case (§4.3) | Slides 1–42 | ✗ not in slides (P1-3) |
| O(bd) space (§3.3.1) | Slides 1–42 | ✗ not in slides (P1-4) |
| Expectiminimax time O(b^d · n^d) (§4.4) | Slides 1–42 | ✗ not in slides (P1-8) |
| Completeness on finite trees (§3.3.1) | Slides 1–42 | ✗ not in slides (P1-9) |
| Expectiminimax recursion (§4.6) matches slide 39 prose | Slide 39 | ✓ correct |
| Zermelo 1912, Shannon 1949, McCarthy 1956, Samuel 1956 (§4.7) | Slide 41 | ✓ exact match |
| All game-playing-today claims (§4.7) | Slide 40 | ✓ exact match |

### Figure coverage audit

| Figure in chapter | Source slide | Page-render present | Verdict |
|---|---|---|---|
| Figure 1 (env taxonomy) | Slide 5 | page05-render.png ✓ | OK |
| Figure 2 (tic-tac-toe tree) | Slide 8 | page08-render.png ✓ | OK |
| Figure 3 (abstract tree w/ minimax values) | Slide 11 | page11-render.png ✓ | OK |
| Figure 4 (4-leaf motivating example) | Slide 20 | page20-render.png ✓ | OK |
| Figure 5 (alpha-beta rules) | Slide 22 | page22-render.png ✓ | OK |
| Figure 6 (Coins N=4 tree) | Slide 18 | page18-render.png ✓ | OK except caption (P1-10) |
| Figure 7 (alpha-beta final state, 9-leaf) | Slide 28 | page28-render.png ✓ | OK |
| Figure 8 ("Another" alpha-beta example) | Slide 35 | page35-render.png ✓ | OK image, caption wrong (P1-6) |
| Figure 9 (alpha-beta tic-tac-toe final) | Slide 34 | page34-render.png ✓ | OK |
| Figure 10 (expectiminimax chance tree) | Slide 38 | page38-render.png ✓ | OK except caption (P1-7) |

**Missing figure coverage:** None. Every diagram-heavy slide is referenced. The catalogue's "SKIP decorative" decisions (Shannon photo, Kasparov photo, coin stock photos, backgammon photo, xkcd #832, slide 23–28 raw embeddings vs renders, slide 21 text-only) are all defensible.

**Page-renders not embedded:** Slides 12–15 are minimax build-up frames using the same image as slide 11 — chapter uses slide 11's render. Slides 23–27 are alpha-beta build-up frames; chapter uses slide 28 (final frame) plus slide 35 (alternate sweep). For a reference chapter this is fine, but a more thorough walkthrough would benefit from showing at least frames 24 and 25 (where the first prune happens) as a sequence. P2 — see P2-11.

### P2-11. Missing intermediate frames in §5.2 alpha-beta walkthrough

Chapter §5.2 narrates the 5-frame animation in prose but only embeds the **final** frame (Figure 7, slide 28) and the **alternate** sweep (Figure 8, slide 35). For a worked example labelled "frame-by-frame walkthrough" it would help to embed at least slide 24 (after left MIN backs up to 3) and slide 25 (where the first prune happens — this is the *pedagogical climax* of the alpha-beta example and currently has no visual). All of `page23-render.png` through `page27-render.png` exist in the figures directory.

---

## What's missing / concerns

1. **No explicit minimax pseudocode that returns the action** at the top — chapter has `MINIMAX-DECISION` but the body of the slide-14 recursion is condensed. Fine for a reference chapter; a student doing Lab 5 will want this.
2. **No mention of "ply" vs "move"** — chess "80 ply" is given as "80 ply (half-moves)" parenthetically. The slides use "ply" without defining it. A glossary entry for "ply" would help.
3. **§4.6 expectiminimax**: chapter says backgammon has "36 ordered dice-pairs… but only 21 unordered combinations". Slide 38 only shows 4 representative branches and probabilities 1/36, 1/18, 1/18, 1/36. The "21 unordered combinations" number isn't on the slide.
4. **§4.7 mentions AlphaStar 2019** — slide 40 just says "2019: Google AI beats top human players at strategy game StarCraft II, link" — the chapter expands this to "Google's AlphaStar". The product name "AlphaStar" is correct but not stated on the slide.
5. **§6 pitfall #4 ("Believing move ordering doesn't matter")** — strong pitfall; would benefit from a worked counter-example showing best-vs-worst move ordering on the same tree. Slide 35 vs slide 28 is *almost* this, but the chapter doesn't connect the dots. P2.

---

## Report to PM

**Assignment recap:** L06 Round 1 — Reviewer 1 (Concept Completeness incl. Figures). Source: `Lecture6-Adversarial Search.pdf` (42 slides). Chapter: `study/lectures/L06-Adversarial-Search.md`. Figure catalogue: `study/extracted_figures/L06/figures.md`.

**Status:** Pass with concerns (REVISE)

**P0 findings:** None.

**P1 findings:**
1. **P1-3** — Fabricated/unattributed average-case complexity $O(b^{3d/4})$ (chapter §4.3, line ~292). Not in slides. Either cite R&N or remove.
2. **P1-4** — Space complexity $O(bd)$ claim (chapter §3.3.1, line ~161). Not in slides. Attribute to L03 explicitly or remove.
3. **P1-5** — Frame-walkthrough prose in §5.2 frame 26–27 (line ~424) accidentally implies cutoff fires when β > α. Rewrite to: "β=14 > α=3, so no cutoff. Continue."
4. **P1-6** — Figure 8 caption (line ~435) wrongly says slide 35 uses a different right-MIN child set. It's the same tree; slide 35 just doesn't draw the pruned leaves. Also the "(now 8) leaves" tally is wrong — still 9 leaves, 6 visited (3+1+2).
5. **P1-7** — Figure 10 caption (line ~326) over-states what slide 38 actually draws (slide draws 4 representative branches, not the full "1/36 for each ordered pair, 1/18 for each unordered pair" claim).
6. **P1-8** — §4.4 expectiminimax row claims $O(b^d \cdot n^d)$ time and unqualified optimality. Not in slides; attribute or remove, and qualify "optimal expected utility".
7. **P1-9** — §3.3.1 minimax completeness claim is unattributed and slightly redundant. Either cite L03 or remove.
8. **P1-10** — Figure 6 caption (line ~387) — "Yellow boxes are MAX-to-move states" is incomplete (some yellow boxes are terminal leaves). Clarify.

**P2 findings:**
1. **P2-1** — §5.1 narrative order doesn't match slide 18's left-to-right branch order. Confusing.
2. **P2-2** — "chess has $10^{123}$ continuations" should be "$10^{123}$ nodes" to match slide 7.
3. **P2-3** — "amateur vs club player" line in §5.4 is folk wisdom; either source or drop.
4. **P2-4** — §3.4 introduces "$U(s)$" as an alternate name for Eval; not in slides.
5. **P2-5** — §4.5 "forward pruning" gloss is more aggressive than slide 36.
6. **P2-6** — Figure 9 caption could clarify that the depth-2 right-MIN has unshown children.
7. **P2-7** — §6 pitfall #6's gloss on "open lines" is editorial; slide 30 doesn't define "open".
8. **P2-8** — Minimax recursion notation in chapter is a rigorous cleanup of slide 14's notation.
9. **P2-9** — Cheat-sheet α/β glossary symbols use unclear "(≥ floor)" parenthetical.
10. **P2-10** — Fail-soft vs fail-hard alpha-beta not mentioned (slides don't either).
11. **P2-11** — §5.2 narrated as "frame-by-frame" but no intermediate render frames embedded (slide 24, 25 page-renders exist and are unused).

**QA Checklist (Spec §7.1) status:**
- Every glossary term from §3 covered in canonical form: **Pass**
- Every algorithm from §4 has pseudocode or explicit recursion: **Pass**
- Every worked example reproducible from the chapter alone: **Pass with concerns** (P1-5 and P1-6 muddy the §5.2 walkthrough)
- Every figure in `figures.md` either embedded or with explicit skip rationale: **Pass**
- All "Lecture 6, slide X" citations check out: **Mostly Pass**; the four imported-without-attribution facts (P1-3, P1-4, P1-8, P1-9) are not cited but are flagged via the `[Lecture 6, slide …]` apparatus elsewhere, which makes the chapter feel less rigorous than it is.

**Acceptance criteria status:**
- Concept completeness vs source PDF: **Met with P1 fixes** — every slide concept is covered; corrections are accuracy fixes, not additions.
- Figure coverage: **Met** — every diagram-bearing slide is referenced.

**DOCUMENT.md audit:** N/A (no implementation files; this is a study chapter review).

**Out-of-scope observations:**
- Slide 9 / 10 (xkcd 832) is correctly cited and the catalogue skip-with-link rationale is sound.
- Slide 36 ("Additional techniques") is a quick three-bullet slide; chapter §4.5 treats it well.
- Slide 42 ("Thank you for your attention") is correctly ignored.
- Lab 5 cross-reference in §7 is a nice forward link.

**Concerns / risks:**
- The chapter feels authoritative because of the consistent `[Lecture 6, slide N]` citations, but four facts (P1-3, P1-4, P1-8, P1-9) are imported from textbook context without citation. A careful student will trust the chapter, then be unable to find these facts in the slides at exam revision time — eroding trust. Either uniformly cite (e.g. `[R&N §5.3]` for textbook imports) or remove.
- The §5.2 alpha-beta walkthrough is the **single most pedagogically important section** of the chapter (alpha-beta is what Lab 5 implements). The current rendering has the P1-5 cutoff-direction prose bug and the P1-6 misleading "different tree" claim. These need fixing before students read this chapter to revise for the exam.

**What PM should do next:** Dispatch the Frontend/Backend Engineer responsible for `study/lectures/L06-Adversarial-Search.md` to fix the 8 P1 issues above. The P2 issues are polish and can be batched into a second pass after the other Round-1 reviewers (concept coverage, exam alignment, etc.) have reported. **Do NOT proceed to next-round QA until P1-5 and P1-6 are corrected** — those two affect the worked example that is the heart of the chapter.

**DOCUMENT.md updated:** N/A for QA / reviewer.

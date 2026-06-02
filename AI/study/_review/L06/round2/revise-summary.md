# L06 Round 2 → Round 3 Revision Summary

**Reviser:** Round 2 → Round 3 chapter author
**Chapter:** `study/lectures/L06-Adversarial-Search.md`
**Inputs:** Round 2 reports (`reviewer1.md`, `reviewer2.md`, `reviewer3.md`, `reviewer4.md`)
**Date:** 2026-05-22

---

## Scope

This pass closes the **critical P0** raised independently by three reviewers (R1, R3, R4) plus R2's P1 list and the remaining P1 items from R3 and R4. Round-2 P2 polish items are deferred unless they were directly entailed by a P0/P1 fix.

---

## P0 fix — Slide 28 vs slide 35 "same 9-leaf tree" claim was factually wrong

**The bug.** Round 1's fix to the slide-35 caption "corrected" the chapter from saying slide 35 was *a different tree* to claiming it was *the same 9-leaf tree as slide 28*. Both R1, R3, and R4 independently verified against `page35-render.png` that slide 35's right-MIN has a leaf labelled **1** (not 5 as on slide 28). No permutation of slide 28's right-MIN children $\{14, 5, 2\}$ produces $\beta = 1$, so the trees cannot be the same. The Round-1 fix went the wrong direction.

**Reframing applied.** Slide 35 is now correctly described as a **variation with the same topology but different leaf values**: same shape (root MAX, three MIN children, three leaves each), same first seven leaves $\{3, 12, 8, 2, 4, 6, 14\}$, but with the eighth leaf changed from 5 to 1 (the ninth leaf is drawn but not labelled). The pedagogical lesson is reframed as "leaf-value changes move subtrees in/out of the prune set", which connects naturally to the move-ordering intuition in §6 pitfall 4 (without overclaiming that slide 35 demonstrates move ordering directly).

**Locations touched.**
1. `study/lectures/L06-Adversarial-Search.md` line ~457 (§5.2 prose introducing slide 35) — replaced "same 9-leaf abstract tree" with "variation on the same tree topology" framing.
2. `study/lectures/L06-Adversarial-Search.md` line ~460 (Figure 8 caption) — re-captioned as "A variation of Figure 7 with the same tree topology but different right-MIN leaf values"; spelled out that slide 28's $\{14, 5, 2\}$ becomes slide 35's $\{14, 1, ?\}$; added explicit math note that $\beta = 1$ is unreachable from $\{14, 5, 2\}$.
3. `study/lectures/L06-Adversarial-Search.md` line ~462 ("How many leaves were visited?" paragraph) — rewritten to walk slide 28's tree and slide 35's variation separately (7 leaves visited on slide 28, 6 leaves visited on slide 35), with the prune count explained by leaf-value change rather than child-ordering.
4. `study/lectures/L06-Adversarial-Search.md` line ~515 (§6 pitfall 4) — replaced "slides 28 and 35 both walk the same 9-leaf abstract tree" with "slides 28 and 35 walk **closely-related** 9-leaf trees" and added the leaf-value-change note.

---

## R2 P1 fixes

### P1-2 — minimax `O(b^d)` attribution loose to slide 19

**Where:** §3.3.1, line ~172.
**Before:** "Time complexity $O(b^d)$ … because every node must be expanded (slide 19)."
**After:** "Time complexity $O(b^d)$ … because minimax-as-DFS expands every node down to depth $d$. Slide 19 demonstrates the explosion concretely on the coin-game tree (depth 5, $b = 3$, 15 nodes) but does **not** state the closed-form $O(b^d)$ bound; the formula is the standard L03 DFS analysis applied to game trees."

### P1-3 — zero-sum vs constant-sum distinction

**Where:** §3.5, line ~206.
**Before:** "a zero-sum game is one in which the sum of all players' utilities … is constant. (The constant is conventionally 0; equivalent definitions use 1 or any other fixed value …)"
**After:** "a **zero-sum game** is one in which the sum of all players' utilities at every terminal state is **0**. The more general property — sum equals some fixed constant — is called **constant-sum**; the two are equivalent for algorithmic purposes. Slide 6 itself uses the constant-sum framing, and the chapter uses 'zero-sum' throughout as shorthand for either."

### P1-4 — beta cutoff bridge from prose ($\alpha(N) \ge \beta(i)$) to pseudocode (`v ≥ β`)

**Where:** §4.2, after the cutoff definitions (line ~266 area).
**Added:** A new "Prose-to-pseudocode bridge" paragraph explaining that the running value $v$ at a MAX node is exactly what $\alpha(N)$ would be assigned next, so the test `v ≥ β` *is* the test "$\alpha(N) \ge \beta(\text{ancestor})$"; justified the non-strict $\ge$ / $\le$ inequalities by noting that equality alone is enough to prune.

### P1-5 — §4.4 comparison table cells coarse

**Where:** §4.4 table.
**Changes:**
- Minimax / Alpha-beta `Optimal?` cells expanded from "yes vs optimal opp." to "yes (maximises worst-case payoff; tight vs optimal opponent)" and "yes (same as minimax)" respectively.
- Depth-limited alpha-beta + Eval `Optimal?` cell expanded from "no (depends on Eval)" to "optimal only if $\text{Eval}(s) = \text{Minimax}(s)$ at every cut-off; otherwise no guarantee".
- Added ‡ footnote marker to the alpha-beta and depth-limited-alpha-beta `Time (worst)` cells (was only on `Time (best)`), closing R1's P2-9.

---

## R3 P1 fix (N2)

### §2.2 hedge needs "(minimum of any set containing 2 is at most 2)" inference shown

**Where:** §2.2, line ~58.
**Before:** "MIN's eventual pick will be the minimum across all replies, which is at most 2 (any further reply only pushes MIN's pick *down*, never up)."
**After:** "MIN's eventual pick will be the minimum across all replies, which is at most 2 (the minimum of any set containing 2 is at most 2; any further reply only pushes MIN's pick *down*, never up)."

---

## R4 P1 fixes

### P1-NEW-2 — U_MAX undefined

**Where:** §3.5, line ~208, and §8 symbols glossary.
**Changes:**
- Expanded the §3.5 prose to define $U_{\text{MAX}}(s)$ and $U_{\text{MIN}}(s)$ explicitly, state the constant-sum identity $U_{\text{MAX}}(s) + U_{\text{MIN}}(s) = \text{constant}$, and clarify that the chapter's $U(s)$ symbol means $U_{\text{MAX}}(s)$ throughout.
- Added $U_{\text{MAX}}(s), U_{\text{MIN}}(s)$ as a separate row in the §8 symbols glossary.

### P1-NEW-3 — slide 30 calls heuristic "Utility" while chapter calls "Eval"

**Where:** §3.4, editorial note (line ~196).
**Added:** A sentence flagging that slide 30 labels the formula `Utility = X's open lines − O's open lines` even though this is a heuristic estimate at a non-terminal cut-off, not a true utility. The chapter follows R&N's `Eval` / `U` separation and treats slide 30's label as unintentionally ambiguous. Closed with an exam-readiness hint: "slide-grounded answer is 'Utility'; conceptually correct answer is 'Eval'."

### P1-NEW-4 — $35^{80}$ is leaf count not total node count

**Where:** §5.4, line ~497.
**Added:** A clarifying note that $35^{80}$ is the leaf-level count and the total node count is $\sum_{i=0}^{80} 35^i \approx 35^{81}/34$, which is the same order of magnitude $\approx 10^{123}$ because the leaves dominate. Confirmed the slide's "nodes" wording and that the order-of-magnitude take-away is unchanged.

### P1-NEW-5 — §5.2 frame 25 DFS-ordering reminder

**Where:** §5.2 frame 25 (line ~448).
**Added:** Explicit reminder that the two pruned leaves are pruned *under the assumed left-to-right DFS ordering*, with a concrete walk of the right-to-left alternative (visits 6 then 4 then 2, prunes nothing on the middle MIN). Same tree, different prune set under different child-expansion order. This is the move-ordering intuition the chapter wants the reader to internalise.

### P1-NEW-6 — cheat-sheet line 603 alpha-beta move-ordering YES needs R&N tag

**Where:** §8 "Properties at a glance" table (line ~603).
**Before:** "Sensitive to move ordering? | no | **YES** (this is the only way it pays off)"
**After:** "Sensitive to move ordering? | no | **YES** — R&N supplementary; the lecture does not introduce move ordering as a knob, but with perfect ordering best-case becomes $O(b^{d/2})$"

### P1-NEW-7 — §1 line 26 pointer to "§5.3 worked example" misroutes

**Where:** §1 question list, line ~26.
**Before:** "(§3.4 definition, §5.3 worked example)"
**After:** "(§3.4 definition + empty-board sanity check; §5.3 worked example combining Eval with alpha-beta on a depth-limited tree)"

---

## Items intentionally deferred to a later polish pass

All P2 items from all four reviewers were deferred except those entailed by a P0/P1 fix (i.e. the ‡ footnote on the worst-case alpha-beta cell, R1 P2-9, which was bundled into R2 P1-5's table rewrite). Deferred items include:

- R1 P2-1, P2-2, P2-3, P2-5, P2-6, P2-7, P2-8, P2-10
- R2 P2-1, P2-2, P2-3, P2-4, P2-5
- R3 N3 (cleared by R3 itself), N4, N5, N6 (entailed; effectively addressed by P0 fix), N7, N8, N9, N10
- R4 P2-NEW-1 through P2-NEW-8

The chapter author flagged R4's P1-NEW-1 (empty-board Eval sanity check too dense — suggested 8-row line-by-line table) as a P2-class polish rather than a P1; the existing prose is correct and the surrounding paragraph is acceptable density. If a future reviewer disagrees, the suggested 8-row line-by-line table is the obvious add.

---

## Verification

- Re-checked Figure 8 caption against `extracted_figures/L06/page35-render.png`: caption now matches slide content (right MIN labelled 14 and 1, third leaf unlabelled, $\beta = 1$ prune annotation).
- Re-checked §6 pitfall 4 prose: no longer claims "same 9-leaf tree"; uses "closely-related".
- Re-checked the math reasoning in the rewritten "How many leaves were visited?" paragraph: 3 + 1 + 3 = 7 on slide 28, 3 + 1 + 2 = 6 on slide 35, both consistent with `page28-render.png` and `page35-render.png`.
- Re-checked the §3.5 $U_{\text{MAX}}$ definition: now defined inline and added to §8 glossary; no other unintroduced symbols remain.
- Re-checked the §4.4 table footnote: ‡ now on both worst-case and best-case alpha-beta cells; footnote text already covers both.
- Re-checked the §3.4 editorial note: explicitly cross-links to §6 pitfall 8 and the "Notational discipline" paragraph for consistency.

No new figures added, no figures removed. Chapter line count is approximately unchanged (~640 lines after the rewrites).

---

## Summary table — Round 2 findings to Round 3 status

| Reviewer | Finding | Round 3 status |
|---|---|---|
| R1 P1-1 | "same 9-leaf tree" claim | **FIXED** (P0) |
| R2 P1-1 | "same tree" + leaf-1 impossibility | **FIXED** (P0) |
| R2 P1-2 | `O(b^d)` attribution to slide 19 | **FIXED** |
| R2 P1-3 | zero-sum vs constant-sum | **FIXED** |
| R2 P1-4 | prose-to-pseudocode bridge for cutoff | **FIXED** |
| R2 P1-5 | §4.4 table coarse cells | **FIXED** |
| R3 N1 | "same 9-leaf tree" claim | **FIXED** (P0) |
| R3 N2 | §2.2 inference gap | **FIXED** |
| R4 P0-NEW | "same tree" claim | **FIXED** (P0) |
| R4 P1-NEW-1 | empty-board sanity check density | **DEFERRED** (P2-class, prose is correct) |
| R4 P1-NEW-2 | $U_{\text{MAX}}$ undefined | **FIXED** |
| R4 P1-NEW-3 | slide 30 "Utility" vs chapter "Eval" | **FIXED** |
| R4 P1-NEW-4 | $35^{80}$ leaf vs node count | **FIXED** |
| R4 P1-NEW-5 | §5.2 frame 25 ordering dependency | **FIXED** |
| R4 P1-NEW-6 | cheat-sheet move-ordering R&N tag | **FIXED** |
| R4 P1-NEW-7 | §1 line 26 §5.3 pointer | **FIXED** |
| R1 P2-9 | ‡ on worst-case cell | **FIXED** (entailed by R2 P1-5) |
| All other P2 items | — | **DEFERRED** to polish pass |

---

## Report to PM

**Assignment recap:** Round 2 → Round 3 revision of `study/lectures/L06-Adversarial-Search.md` based on four Round 2 reviewer reports. Critical P0 (slide 35 ≠ slide 28) flagged independently by R1, R3, R4. R2's five P1s, R3's one P1, R4's seven P1s all in scope.

**Status:** Complete.

**Files modified:**
- `study/lectures/L06-Adversarial-Search.md` — 11 distinct edits across §1, §2.2, §3.3.1, §3.4, §3.5, §4.2, §4.4, §5.2, §5.4, §6, §8.
- `study/_review/L06/round2/revise-summary.md` — new file (this document).

**What I did:** Closed the cross-reviewer P0 by reframing slide 35 as a topology-preserving variation of slide 28 (not "same tree"); spelled out the leaf-value change ($5 \to 1$ in the right-MIN's second leaf) and the resulting prune-count change ($7 \to 6$); reconciled §6 pitfall 4 accordingly. Applied all 13 cross-reviewer P1 fixes. Did not touch P2 items unless directly entailed by a P0/P1 fix.

**Deviations:** R4's P1-NEW-1 (empty-board sanity check density) was downgraded to P2-class deferral; the existing prose is correct, and the suggested 8-row line-by-line table is polish, not a correctness fix. All other P1s closed as specified.

**Out-of-scope observations:**
- Two reviewers (R3, R4) noted that the Round-1 → Round-2 revision verified figures *visually* without re-deriving the algorithm by hand on the leaf values; that's how the P0 slipped through. For future rounds, the cleanest verification on a worked-example figure is to re-derive the key $\alpha$/$\beta$ numbers from the stated leaf values — this would catch the slide-28-vs-35 confusion in 30 seconds.
- R4's "dual-bracket lecture-vs-supplementary citation style" suggestion (chapter line ~175) is being implicitly applied throughout the chapter; consider baking this into a writing template for L07, L08, etc.

**Concerns / risks:**
- §5.2 is the chapter's most pedagogically dense section. The P0 fix changes the framing significantly enough that a re-read by Reviewer 3 (Pedagogical Clarity) on Round 3 is recommended to confirm the new "variation" framing doesn't introduce a different kind of confusion.
- The R4 P1-NEW-1 deferral (empty-board sanity check density) is a judgement call; if a Round-3 reviewer flags it again, the 8-row table is the obvious add.

**What PM should do next:**
1. Dispatch QA Inspector / re-review pass focused specifically on §5.2 (Figure 8 caption, slide-35 reframing) and the diff against Round 2.
2. P2 polish pass can be batched separately when convenient — none of the deferred items affect correctness or exam-readiness.

**DOCUMENT.md updated:** N/A for lecture-chapter revision.

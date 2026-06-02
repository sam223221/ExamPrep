# L12 Clustering — Round 1 Revise Summary

**Artifact:** `study/lectures/L12-Clustering.md`
**Round:** 1 — Reviser (post R3 + R4)
**Status:** All P0s from R4 and all P1s from R1/R2/R3 addressed. File grew 545 → 613 lines.

---

## P0 fixes (R4)

### P0-1 — K-means iteration table re-aligned to slide convention
**§5.1, lines ~350-380.**

The chapter previously used a "$t = $ iteration after $t$-th update" convention; the slides use "$t = k$ is the **state at the start of iteration $k$**" (so slide 9's $t=1$ shows μ₁=2, μ₂=4 — the initial centroids). I re-labelled the table to match the slides verbatim:

| $t$ | $\mu_1$ | $\mu_2$ | Assignment |
|---|---|---|---|
| 1 (initial) | 2 | 4 | $C_1=\{2,3\}, C_2=\{4,10,...,30\}$ |
| 2 | 2.5 | 16 | $C_1=\{2,3,4\}, C_2=\{10,...,30\}$ |
| 3 | 3 | 18 | $C_1=\{2,3,4,10\}, C_2=\{11,...,30\}$ |
| 4 | 4.75 | 19.60 | $C_1=\{2,3,4,10,11,12\}, C_2=\{20,25,30\}$ |
| 5 (converged) | 7 | 25 | same as $t=4$ |

I also added an explicit **Convention** callout before the table ("$t=k$ records the state of the centroids at the start of iteration $k$"). The slide-9 figure caption was rewritten to underline the convention. Added a Slide-9 convention reminder to the cheat sheet (§8).

### P0-2 — Converged partition stated cleanly before SSE
**§5.1 end.**

Added an explicit "Final converged partition" sub-heading with $C_1 = \{2,3,4,10,11,12\}$ and $C_2 = \{20,25,30\}$ and the final centroids $\mu_1 = 7, \mu_2 = 25$ written out before the SSE = 150 computation. The SSE formula now visually groups its $C_1$ and $C_2$ terms via `\underbrace`.

### P0-3 — DBSCAN core-point ≥ vs > MinPts resolved
**§3.7, around lines 175-200.**

The table now says **"≥ MinPts (counting itself)"** consistently, matching the figure on slide 37 and the canonical Ester-et-al. (1996) / Tan-Steinbach-Kumar convention. A new callout block explicitly flags the slide-35 ("at least") vs slide-36 ("more than") inconsistency and tells the student which convention to use on the exam.

Also updated the §2 analogy ("Two house rules") to match: now says "≥ MinPts including itself" and forwards the reader to §3.7 for the canonical definition.

### P0-4 — Slide-23 dendrogram linkage declared as MIN
**§5.2, around line 400.**

Added a "**Linkage.**" preamble before the trace that:
1. Notes slide 23 itself does not label the linkage.
2. Reconstructs why MIN matches (merge heights 1.48, 1.49, 1.81, 4.82 match the figure's pattern).
3. Verifies that MAX would yield 5.05 at the last merge, not 4.82, ruling MAX out.
4. Reinforces the §6 pitfall ("when the exam says 'draw the dendrogram', state the linkage first").

### P0-5 — Slide 17 quoted verbatim
**§4.3.**

Replaced the previous 5-bullet paraphrase with a verbatim block-quote of slide 17's five bullet points (Multiple runs / Sample-and-hierarchical / Select more than k / Postprocessing / Bisecting K-means with their sub-bullets), followed by one-sentence glosses for each. The bullet ordering now matches the slide exactly.

---

## R1 P1 fixes

- **Slide 6 "Traditional vs Non-traditional"** added to §3.2 with a paragraph explaining the distinction.
- **Slide 7 divisive (top-down) clustering** named and explained as "named but never engaged again" in §3.2, with a cross-reference to bisecting K-means as the deck's only divisive instance. Cheat sheet updated.
- **Ward's method** now has its own §4.4.5 with the four slide-33 bullets preserved verbatim plus the "hierarchical analogue of K-means / initialiser" bonus. Each of the four geometric linkages (MIN, MAX, group-average, centroid) was given its own §4.4.1–§4.4.4 with the analogy moved next to its formula and slide figure (this also addresses R3 P1-3).
- **GTA / DSA letter-cloud naming** stripped from §5.3 — chapter now just says "three irregular letter-shaped clusters" without committing to a transcription, since the rendered slides are ambiguous.
- **Density-reachable** noted in §3.7 as a textbook decomposition that the slides collapse; we use slide's wording but acknowledge the layered Ester-et-al. definition.
- **Slide 18 / Figure 8 caption** rewritten to make clear it shows a single K=2 split (one bisection step), not the full recursion.
- **§6 pitfall 11** now includes slide 45's "entire-vs-individual" hinge clause about global vs per-cluster validation; CH/DB/ARI/NMI now sit behind an explicit "Not on the slides" disclaimer.
- **§4.7 complexity row** now has a "not on the slides — textbook figures" footnote.

## R2 P1 fixes

- **Density-connected** in §3.7 now distinguishes "slide phrasing (one-layer)" from the Ester-et-al. two-layer textbook definition (density-reachable + density-connected).
- **Convergence** wording in §4.1 changed from "SSE decreases at every step" to "SSE is **non-increasing**" (strict decrease when a point switches, equality otherwise), matching the textbook claim. Cheat sheet pitfall #1 also updated.
- **Centroid-linkage inversion** explanation in §4.4.4 now has a concrete 1-D example (clusters $\{0\}, \{10\}, \{4\}$) and replaces "dendrogram-monotonic" with the plain-English "heights stop being monotone as you climb the tree".

## R3 P1 fixes

- **Sorting-laundry analogy (P1-1)** now exists as the first analogy in §2 with its own "where it breaks down" clause. The two "Recall the sorting-laundry analogy" references (§3.1 line 90, §8 line 554) now point to a real anchor.
- **Centroid-linkage inversion gloss (P1-2)** rewritten with a concrete 1-D example as part of §4.4.4 (see R2 fixes).
- **Linkage analogies moved (P1-3)** out of §2 and into §4.4.1–§4.4.5 next to each linkage's formula and figure. §2 now ends with a brief pointer ("Each linkage rule has its own intuition — those analogies live in §4.4 next to their formulas").

## R3 P2 polish applied

- Bridge sentence added at top of §5.1 — 1-D dance-floor → number-line.
- "Crowd-counts the neighbourhood" removed; replaced with "Eps-radius circle contains at least MinPts pins (counting itself)".
- Figure 6 caption rewritten with the "look at the stranded centroids" pedagogical pointer.
- Stalactite analogy replaced with "upside-down family tree" both in §2 dendrogram section and in cheat sheet.
- MAX-linkage break-down rewritten to make clear MAX *prevents* large straggly merges rather than "splitting" anything.
- §2 closing line replaced with a "Hold these in your head; each definition below points back" transition.
- L05 cross-reference promoted from §7 to a §4.1 callout box ("K-means is local search in disguise").
- §3.4 dendogram-typo footnote now explicitly tells the student to expect the typo on the slides.
- "~4.82" → "exactly 4.82" in §5.2 wrap-up.

## R4 P1 polish applied

- **P1-2 / P1-3** complexity-row footnote tagging non-slide-grounded figures.
- **P1-4** linkage-rule self-inconsistency resolved by the §5.2 linkage declaration (see P0-4).
- **P1-5** dendogram typo coverage extended to §5.2 figure 11 / 12 captions implicitly via the new bridge sentence.
- **P1-6** bisecting K-means now has an explicit "Slide-grounded facts only" callout limiting what to quote on the exam.
- **P1-7** §5.2 wording corrected: slides 24-27 trace starts with $p_1, \ldots, p_{12}$, not $C_1, \ldots, C_5$.
- **P1-9** §6 pitfall 11 disclaimer added (see R1 list).
- **P1-10** §6 pitfall 9 now says "do not rank the algorithms" explicitly.
- **P1-11** centroid linkage / "distance between centroids" cross-named in the glossary line.
- **P1-12** centroid-linkage inversion remark explicitly tagged "not on the slides" in §4.4.4.

## R4 P2 polish applied

- §2 closing citation trimmed (slides 1-34 → kept; no further change needed).
- Glossary line 5 cleaned: MIN/MAX style normalised ("single-link linkage (MIN)" etc.), "centroid linkage" cross-named, "density edge" added.

---

## Items NOT changed (with rationale)

- **R3 P2-7 "marriage metaphor re-used inside its own break-down"** — left as-is; the breakdown re-uses the metaphor precisely to deliver the "once merged, never undone" concept which is the load-bearing fact. Trimming would lose that.
- **R4 OO concerns about K-medoids / OPTICS** — both already flagged in-text as "not on the slides"; no further action.
- **§8 cheat sheet duplication of §4-§6** — kept duplication intentionally; flagged as "must stay in sync" per R4 P2-4.

---

## Verification notes

- Slide 9 (`fig_p09_i1.png`) inspected directly: confirms (a) Initial dataset, (b) $t=1$ μ₁=2, μ₂=4, (c) $t=2$ μ₁=2.5 μ₂=16, (d) $t=3$ μ₁=3, μ₂=18. Slide-9 convention now exactly matches the chapter.
- Slide 10 (`fig_p10_i1.png`) inspected: (e) $t=4$ μ₁=4.75, μ₂=19.60, (f) $t=5$ (converged) μ₁=7, μ₂=25.
- Slide 23 (`slide_p23.png`) inspected: dendrogram heights ≈ 1.48, 1.49, 1.8, 4.8 confirm MIN linkage.
- Slide 37 (`fig_p37_i1.png`) inspected: visible MinPts=4, core-point circle contains 4 points — fits ≥ MinPts, not > MinPts. Resolves P0-3 in favour of ≥.
- Slide 18 (`fig_p18_i1.png`) inspected: shows one K=2 split (red vs blue starburst), not a recursive bisection — Figure 8 caption updated accordingly.
- PDF text dump confirms slide 35 ("at least MinPts") vs slide 36 ("more than … MinPts") inconsistency.
- PDF text dump confirms slide 45's hinge clause "For 2, 3, and 4, we can further distinguish whether we want to evaluate the entire clustering or just individual clusters" — now reflected in §6 pitfall 11.
- PDF text dump confirms slide 7 lists divisive ("Top-Down") clustering by name — now reflected in §3.2 catalogue.
- PDF text dump confirms slide 33 Ward bullets (squared error / similar to group-average / less susceptible to noise / globular bias / hierarchical analogue of K-means / can be used to initialise K-means) — now §4.4.5 verbatim.

File is ready for App Tester or final Code Reviewer.

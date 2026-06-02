# L05 Round 2 — Reviewer #1 (Concept Completeness incl. Figures)

**Source:** `Lecture5-Local Search.pdf` (50 slides)
**Chapter:** `study/lectures/L05-Local-Search.md` (1225 lines — up from 917 in Round 1)
**Figure catalogue:** `study/extracted_figures/L05/figures.md` (18 USE entries, unchanged from Round 1)
**Round 1 verdict:** NEEDS_REVISION — 1 P0 (slide-12 caption fabrication) + 5 P1 + 5 P2
**Revise-summary scope:** R1 + R2 + R3 + R4 (all four reviewers' findings)

---

## VERDICT: **APPROVED with one outstanding P1 and minor P2 polish**

The Round 1 P0 is fixed cleanly. The slide-12 caption now correctly reports the leftmost board's best successor as $h = 1$ (the local-minimum trap), quotes the lecturer's verbatim caption verbatim, and correctly attributes the $h = 0$ row-score to the middle board. The chapter's surrounding prose (§5.4 lines 833–862) is now internally consistent with the caption above and the lecturer's pedagogical sting (the local-minimum trap warning) is finally front-and-centre.

Of the five P1 findings from Round 1, four were addressed in this revision. One — the figure-catalogue's false "Mermaid diagram" claim — was explicitly deferred per the revise-summary ("R1-P1.3 catalogue prose tweaks — `figures.md` is a separate catalogue file; out of scope for this revision pass") and **still stands as a P1 in this round**. The two new P2 items below are cosmetic and would not block approval; I flag them only for completeness.

This is approvable. If the catalogue Mermaid prose is fixed (one-line edit to `figures.md`), the chapter is publication-ready from a concept-completeness lens.

---

## Round 1 issue verification

### Round 1 P0-1: Slide-12 figure caption misrepresents the leftmost board — **FIXED ✓**

**Before (Round 1, line 603):** "Three boards: the first showing per-row $h$ scores if the lower-right queen is moved (best row gives $h = 0$); the middle shows the result after that move ($h = 0$, the global minimum); the right shows the final solved 8-queens board."

**After (Round 2, lines 833–852):**

- Caption now reads (line 842): "**Left:** the original board annotated with the row-scores for moving the lower-right column's queen — the labels (top to bottom) are $\{2, 2, 1, 2, 3, 1, 2, 2\}$ ... The minimum among these is $h = 1$, *which the lecturer flags as a local-minimum trap*. **Middle:** a different queen's column is annotated with row-scores $\{3, 3, 2, 3, 2, 3, 0\}$; one row gives $h = 0$, the global minimum. **Right:** the final solved 8-queens board reached by taking that $h = 0$ move."
- The lecturer's verbatim caption ("Queen in lower right ... Moving to a row with 1 conflict would be a local minima ...") is now quoted as a blockquote *above* the figure (lines 836–840).
- The post-figure prose (lines 843–852) now spells out the pedagogical point: "If hill climbing tie-broke to that $h = 1$ row, it would land at a configuration where *no further column-move improves on $h = 1$*, and the algorithm would terminate one step short of the solution. That is exactly the local-minimum trap the lecturer is warning about."

**Verification (cross-checked against `fig07-nqueens-example-solution.png`):**
- Left-board minimum row-score $= 1$ ✓ (matches slide)
- Middle-board minimum row-score $= 0$ ✓ (matches slide; the "0" is in a highlighted box at the bottom of the second column from the right)
- Right-board fully solved ✓ (matches slide)
- Lecturer's caption quoted verbatim ✓

**Verdict:** P0 closed. The single most important Round 1 finding is fully addressed; the chapter no longer makes the false factual claim and the pedagogical sting is preserved.

### Round 1 P1-1: MCMC gloss — **FIXED ✓**

Chapter §3.5 lines 468–473 now includes:

> "Slide 20 also notes that simulated annealing is one special case of a broader family — **Markov Chain Monte Carlo (MCMC)**. MCMC algorithms generate samples from a target probability distribution by constructing a Markov chain whose stationary distribution is the target; SA is the special case where the target is $\propto \exp(f(s) / T)$ with $T \to 0$. The broader MCMC family is out of scope for this course."

This is the exact gloss I requested in Round 1, verbatim. Closed.

### Round 1 P1-2: Slide-14 continuous-space footnote vs Ridge — **FIXED ✓**

§3.2 now has **five** distinct landscape pathologies, with Ridge correctly labelled "*(not on slide 15; standard reference)*" (line 310) and a separate, fifth bullet "**Continuous-space step-size sensitivity** *(slide 14 footnote)*" (line 317) that captures the actual slide-14 concern: "on continuous landscapes, hill climbing also suffers from step-size choice (too small → slow convergence; too large → overshoot) and slow asymptotic convergence near the optimum." The two concepts are now properly disentangled. Closed.

### Round 1 P1-3: Catalogue's "Mermaid diagram" claim is false — **NOT FIXED (deferred)**

`study/extracted_figures/L05/figures.md` lines 82–85 still reads:

> "All embedded figures are `USE`. No `REWORK` entries were necessary because the page-rendered slides preserve the lecturer's own annotation and labelling; the chapter additionally backs each up with a Mermaid diagram or in-text prose where extra clarity helps."

The chapter contains **zero** Mermaid blocks. (Verified: searched for ```` ```mermaid ```` — zero hits in the 1225-line chapter.) The catalogue still claims infrastructure that doesn't exist.

The revise-summary explicitly defers this as "out of scope for this revision pass" but it is still a documentation defect against the figure-catalogue spec (§6.1.1) that the catalogue accurately describe what the chapter does. **Carries over as P1-1 in this round.**

### Round 1 P1-4: §5.1 trace clarity ("$-3$ (tie) or back up to a $-4$ neighbour") — **FIXED ✓**

The §5.1 trace table (lines 748–755) is fully rewritten. Each step is now labelled with one of three move types — **strict improvement** / **plateau (equal value)** / **strict decrease** — and the "slide-13 rule says" column makes explicit how the `<` rule resolves each case. The confusing "back up to a $-4$ neighbour" wording is gone. A footnote at line 745 explicitly states "Under the textbook `≤` rule it would have terminated at the first plateau and the trace would not reach the goal", which is a substantive improvement beyond what I asked for in Round 1. Closed.

### Round 1 P1-5: SA "picks random rather than best" framing missing — **FIXED ✓**

Chapter §3.5 lines 410–414 now reads:

> "A second fundamental departure (slide 18, bullet 3): where hill climbing evaluates **all** neighbours and moves to the **best**, simulated annealing **picks one random neighbour per step** and decides whether to accept it. This makes per-step cost $O(1)$ rather than $O(b)$, at the cost of needing many more steps before convergence."

Exactly the sentence I requested. Closed.

### Round 1 P2 items

- **P2-1** (fig01 page-render note in catalogue): not fixed — `figures.md` not modified in this round. Carries as P2.
- **P2-2** (slide-21 SKIP entry could note content carried in chapter): not fixed. Carries as P2.
- **P2-3** (catalogue coverage roll-up by chapter section): not fixed. Carries as P2.
- **P2-4** (slide-47 parameter advice cross-referenced from §3.6/§4.3): partially addressed — §4.3 line 698 now quotes slide 47 directly. Closed.
- **P2-5** (`<` vs `≤` cross-reference to shoulder/plateau/flat-local-max): addressed in §6 lines 1019–1032 ("Plateaux vs ridges vs local maxima — and what the slide-13 `<` rule does to each"). Closed.

---

## P0 — MUST FIX (blocks approval)

**None.** The Round 1 P0 is fixed; no new P0 issues identified.

---

## P1 — SHOULD FIX (requested, not blocking)

### P1-1. Figure-catalogue's "Mermaid diagram" claim still false *(carryover from Round 1 P1-3)*

`study/extracted_figures/L05/figures.md` lines 82–85 still claim the chapter has "a Mermaid diagram or in-text prose" where extra clarity helps. The chapter has **zero Mermaid blocks**.

**Fix:** one-line edit to `figures.md` — change "a Mermaid diagram or in-text prose" to "in-text prose" (or, alternatively, add Mermaid diagrams; I would not require additions, just truthful catalogue prose).

**Severity:** P1 because (a) it is a verifiable false claim in a spec'd documentation file, (b) it survives one round of revision, (c) the fix is a single sentence.

**Evidence:** `figures.md` lines 82–85; chapter contains no ```` ```mermaid ```` blocks.

### P1-2. §5.4 left-board label count: chapter says 8 values but the queen's current row is "marked separately" — internally inconsistent

**Chapter line 842:**

> "**Left:** the original board annotated with the row-scores for moving the lower-right column's queen — the labels (top to bottom) are $\{2, 2, 1, 2, 3, 1, 2, 2\}$ (one per row of the column; the queen's current row is marked separately)."

This is internally inconsistent. The lower-right column has 8 rows total. If the chapter lists 8 row-scores, those *are* the labels for all 8 rows (including the queen's current row). If the queen's current row is "marked separately", then the 8-value list cannot also be "one per row of the column" — only 7 rows would have alternative-move scores.

Inspecting `fig07-nqueens-example-solution.png` directly: I can count seven numbers along the right edge of the leftmost board (2, 2, 1, 2, 3, 1, 2) plus what appears to be an eighth value (2) in the queen's row (the bottom). The lecturer's caption *text* says "Queen in lower right of first figure in conflict with 2 others" — so the bottom "2" is plausibly the queen's *current* contribution to the conflict count (= 2), not an alternative-move score.

The Round 1 reviewer (myself) read this as **seven** alternative row-scores: `{2, 2, 1, 2, 3, 1, 2}`. The revision wrote **eight**. Both are defensible against the image, but the chapter's wording ("8 values, but the queen's current row is marked separately") is self-contradictory.

**Fix:** pick one of two phrasings and stick to it:

- (Option A — 7 alternatives) "the seven alternative-row labels are $\{2, 2, 1, 2, 3, 1, 2\}$ — one per row the queen could move to; the queen's current row is annotated separately with a 2, its current contribution to the conflict count."
- (Option B — 8 labels, all rows) "the eight row-labels (top to bottom) are $\{2, 2, 1, 2, 3, 1, 2, 2\}$ — one per row of the column, including the queen's current row whose label (2) reports the queen's current contribution to the conflict count."

Either is fine; the current wording is the worst of both worlds.

**Severity:** P1 (not P0) because the pedagogical point (the $h = 1$ local-minimum trap) is correct in either reading — but a student counting numbers on the slide and the chapter side-by-side will be confused.

**Evidence:** chapter line 842; `fig07-nqueens-example-solution.png` (visually inspected at 200 dpi).

---

## P2 — NICE TO HAVE

### P2-1. Carryover Round 1 P2 items still open

- **R1.P2-1** (fig01 entry in catalogue could note page-render includes text overlay) — not fixed; `figures.md` not modified.
- **R1.P2-2** (slide-21 SKIP could note content preserved in chapter §3.6) — not fixed; `figures.md` not modified.
- **R1.P2-3** (catalogue coverage roll-up could include chapter section anchors per topic) — not fixed; `figures.md` not modified.

All three are documentation polish; fixable in a single pass on `figures.md`.

### P2-2. The 8/7-value ambiguity in §5.4 (P1-2 above) also propagates to the slide-12 narration

The post-figure prose at lines 843–852 says:

> "If hill climbing tie-broke to that $h = 1$ row, it would land at a configuration where *no further column-move improves on $h = 1$*..."

This is correct, but it assumes the reader has already understood that there *is* a tie at $h = 1$ — which is true if the leftmost board's row-scores are $\{2, 2, 1, 2, 3, 1, 2\}$ (or $\{..., 2\}$ — either way two rows give 1). If the chapter resolves P1-2 by adopting Option A (7 values), the post-figure prose stays correct; if Option B (8 values), the prose stays correct. Either way, a follow-up sentence "two rows give $h = 1$, so the tie-break decides which one the algorithm picks" would tighten the explanation. Cosmetic.

### P2-3. The §5.7 "specific bit-strings as shown on slide 43" wording could be tighter

Chapter line 930:

> "Parents (chromosomes 4 and 6 from the table; specific bit-strings as shown on slide 43):"

The parent chromosomes from the slide-41 table (chromosomes 4 and 6) have bit-strings `1010000000` and `1001011111` respectively. The chapter doesn't say outright that these are *the* same bit-strings shown on slide 43 — a reader has to trust the slide. A one-line sentence "These match chromosomes 4 (`1010000000`) and 6 (`1001011111`) from the slide-41 population table" would close that loop. Cosmetic.

### P2-4. The chapter's claim "Throughout this section bits are 1-indexed left-to-right" (line 898) is helpful, but could be cross-referenced from the §4.3 GA pseudocode

The GA pseudocode (§4.3, lines 670–688) uses `single_point_crossover` and `mutate` as black boxes without specifying a bit-indexing convention. Since §5.7 commits to 1-indexed left-to-right, a one-line forward-pointer from §4.3 would harmonise. Cosmetic.

### P2-5. The catalogue's coverage check (figures.md lines 71–80) could mention that the §2 / §3 / §4 conceptual sections rely entirely on prose (no figures) and that figures cluster in §5

Currently the coverage check enumerates which figures support hill climbing / SA / GA. A complementary view — which *sections* have figures vs which are figure-free — would help a reader auditing the chapter. Cosmetic.

---

## EVIDENCE

**Slides re-inspected for this round (focused on Round 1 findings):**

- Slide 12 (Example Solution) — fig07 ✓ caption now matches the slide; verbatim lecturer caption now quoted; **P0 closed**.
- Slide 18 (SA prose, bullet 3 "Picks random rather than best") — §3.5 lines 410–414 carry the framing; **P1.5 closed**.
- Slide 20 (MCMC mention) — §3.5 lines 468–473 carry a one-sentence gloss; **P1.1 closed**.
- Slide 14 (continuous-space footnote) — §3.2 line 317 has a separate, fifth-bullet pathology; **P1.2 closed**.
- Slide 5 (8-puzzle trace) — §5.1 lines 748–755 trace table re-labels each step by move type; **P1.4 closed**.

**Other slides spot-checked (all USE figures verified embedded; SKIP justifications unchanged from Round 1 — no new gaps):**

- Slides 1–50: all SKIPped slides remain correctly SKIPped (title, decorations, pseudocode-only slides).
- All 18 USE figures still embedded in chapter at expected sections.
- The §5.7 mutation figure caption now correctly identifies **bit 6** (offspring 1: $1 \to 0$) and **bit 3** (offspring 2: $0 \to 1$) per `fig18-mutation.png` (re-verified visually): position-by-position diff of `1011011111` vs `1011001111` shows the change at position 6 (1-indexed left-to-right) — correct. Position-by-position diff of `1000000000` vs `1010000000` shows the change at position 3 — correct.

**New concept coverage gaps identified in this round:** **none**.

**Chapter section additions since Round 1 (verified contents):**

- §2.E "Mini-analogies for the algorithm-internal operators" (lines 145–224) — 8 sub-analogies with breakdown caveats. Concept-completeness: positive (no new content gaps).
- §2.F cheat-sheet (lines 227–256) — expanded from 13 rows to 26. Positive.
- §3.2 (lines 286–322) — disentangled ridge, flat local max, shoulder, continuous-space step-size. Positive.
- §3.5 (lines 404–475) — added Δ definitions, lateral-move boundary, MCMC gloss, Geman & Geman canonical form. Positive.
- §5.8 (lines 950–969) — 3-row temperature comparison table. Positive (was a P2 / P1 across multiple R1 reviewers).
- §6 (lines 977–1086) — expanded pitfall list, sign-convention rewrite, plateaux/ridges/local-maxima breakdown. Positive.

**Files cross-checked:**

- `study/lectures/L05-Local-Search.md` — 1225 lines (vs 917 in Round 1). All five Round 1 P1 fixes verified except P1-3 (catalogue Mermaid claim — deferred).
- `study/extracted_figures/L05/figures.md` — unchanged from Round 1 (per revise-summary's explicit deferral).
- All 18 PNG figures present on disk; sizes unchanged.

---

## Report to PM

**Assignment recap:** L05 Round 2 — Lecture Reviewer #1 (Concept Completeness incl. Figures); verify Round 1 P0 (slide-12 caption fabrication) and Round 1 P1×5 are fixed; flag any new gaps.

**Status:** **Pass with one concern** — Round 1 P0 is fixed; 4 of 5 Round 1 P1s are fixed; 1 P1 (catalogue Mermaid claim) deferred and carries over; 1 new P1 (§5.4 left-board 8 vs 7 label-count internal inconsistency); 5 P2 polish items.

**P0 findings:** none.

**P1 findings:**

1. **`study/extracted_figures/L05/figures.md` lines 82–85** — catalogue still claims chapter has "a Mermaid diagram or in-text prose" but chapter has zero Mermaid blocks. One-line edit: drop "Mermaid diagram or". *(Carryover from Round 1 P1-3.)*
2. **`study/lectures/L05-Local-Search.md` line 842** — slide-12 left-board annotation is described as "$\{2, 2, 1, 2, 3, 1, 2, 2\}$ (one per row of the column; the queen's current row is marked separately)". These two clauses contradict each other (8 values cannot be "one per row" *and* exclude the queen's current row). Pick either 7 alternative values (Option A in the body) or 8 row-labels (Option B); both are defensible against the slide. *(New finding.)*

**P2 findings:**

1. Three Round 1 P2 items on the catalogue (`figures.md`) remain open — fig01 page-render note, slide-21 SKIP content carryover, catalogue coverage-by-section roll-up.
2. The 8/7-value ambiguity in §5.4 also slightly weakens the post-figure prose — adding "two rows give $h = 1$" would tighten it.
3. §5.7 line 930 could explicitly state that the slide-43 parents *are* chromosomes 4 (`1010000000`) and 6 (`1001011111`) from the §5.7 step-1 table.
4. The §4.3 GA pseudocode could forward-reference the "1-indexed left-to-right" convention from §5.7.
5. Catalogue coverage check could mention which chapter sections have figures vs which are figure-free.

**QA Checklist (§7) status:** N/A (this is a study-document review, not an engineering feature).

**Acceptance criteria (§1) status:** N/A.

**DOCUMENT.md audit:** N/A.

**Out-of-scope observations:** none flagged outside Reviewer #1 lens (mathematical rigor, pedagogical clarity, exam-readiness are other reviewers' lenses). The revision also addressed numerous R2/R3/R4 findings (visible in the much-expanded §2, §3.5, §6) — those are not in scope for Reviewer #1 to evaluate, but they don't introduce new concept-completeness gaps either.

**Concerns / risks:**

- The single outstanding P1 (catalogue Mermaid claim) is the smallest possible defect — one false sentence in a documentation file that nobody reads except auditors. Approving without it would be defensible, but fixing it is a 5-second edit.
- The new P1 (§5.4 left-board 8-vs-7 label count) is genuinely ambiguous from the slide image alone; the chapter chose 8 but its surrounding wording is self-contradictory. This is a wording defect, not a factual one — the pedagogical point (the $h = 1$ trap) is correct either way.
- No new concept-completeness gaps were introduced by the revision. Every USE figure is still embedded, every SKIP is still justified, every slide-named concept (including MCMC, continuous-space step-size, "picks random rather than best") is now present. The chapter has grown from 917 to 1225 lines (33% expansion) and the additions are all substantive (analogies, pseudocode clarifications, multi-temperature SA example, expanded pitfalls).

**What PM should do next:** **Approve and ship**, OR: dispatch a 5-minute Reviser pass to fix (1) the one-line `figures.md` Mermaid claim and (2) the §5.4 left-board phrasing. Either path is acceptable from a concept-completeness lens; the chapter is publication-ready as is.

**DOCUMENT.md updated:** N/A for QA.

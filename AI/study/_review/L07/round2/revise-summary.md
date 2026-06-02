# L07 Round 2 → Round 3 — Revise Summary

**Chapter:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L07-CSP.md`
**Figures dir:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\extracted_figures\L07\`
**Figures catalogue:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\extracted_figures\L07\figures.md`

**Scope:** Round 2 → Round 3 revision pass. 5 P0 from Reviewer 1 (R1) and 1 P0 from Reviewer 4 (R4), plus selected P1s.

---

## P0 Fixes Applied

### P0-1 (R1) — K4 over-correction note removed
**Location:** §4.7 (`L07-CSP.md` lines around 477–479).

**Before:** Round-1 revision had added a "Note on the slide-35 picture" claiming the four-box diagram "visually emphasises only a subset of $K_4$'s six edges" with X1–X3 and X2–X4 "rendering less obviously" — a fabrication. Reviewer 1 verified that slide 35 actually draws all six K4 edges with equal weight.

**After:** Deleted the over-correction blockquote. The lead-in paragraph for §4.7 now reads:
> Every pair of rows interacts via both the column-equality $X_i \neq X_j$ and the diagonal constraint $|X_i - X_j| \neq |i - j|$, so the constraint graph is the **complete graph $K_4$** on $\{X_1, X_2, X_3, X_4\}$; slide 35 draws all six edges. Forward checking after assigning $X_1$ must therefore prune $X_2$, $X_3$, *and* $X_4$ as you will see immediately below.

Affirmation is one sentence with the downstream "must prune all three" conclusion preserved.

### P0-2 (R1) — fig01 and fig02 re-extracted from page renders
**Files:**
- `study/extracted_figures/L07/fig01-8queens-board-empty.png` ← now copy of `page03-render.png`
- `study/extracted_figures/L07/fig02-8queens-attacked-squares.png` ← now copy of `page04-render.png`

**Before:** The raw extraction had selected the slide-title text elements (`Motivating example: 8 Queens` and `What more do we need for 8 queens?`). The chapter captions referenced board imagery that wasn't in the files.

**After:** Replaced both files with the page-render versions, which contain the actual board imagery the captions describe — the empty 8×8 board with two red-star queens for fig01, and the same board overlaid with black dots marking attacked squares for fig02. Verified visually after replacement. Updated `figures.md` rows for both files to note the new source and corrected slide attribution (fig02 was attributed to slide 5 in the catalogue but is actually slide 4).

### P0-3 (R1) — fig09 re-extracted from page render
**File:** `study/extracted_figures/L07/fig09-nqueens-csp-board.png` ← now copy of `page12-render.png`

**Before:** The file showed a 4-queens solution board (queens at the four solution positions). The chapter caption claimed it showed "the $X_{ij}$ variable is one Boolean per cell" with a highlighted cell — neither was present.

**After:** Replaced with the page-12 render, which shows the slide 12 variable/domain/constraint list alongside the 4×4 board with cell `X_ij` labelled in blue. The labelled `X_ij` cell the chapter narrative depends on is now visible. Updated `figures.md` accordingly.

### P0-4 (R1) — fig10 re-extracted from page render
**File:** `study/extracted_figures/L07/fig10-cryptarithmetic-sum.png` ← now copy of `page13-render.png`

**Before:** The file showed only `TWO + TWO = FOUR` with no carry labels. The chapter caption referenced carry variables `X1 X2 X3` that weren't in the file.

**After:** Replaced with the page-13 render, which includes the `X_3 X_2 X_1` carry-label line above the addition, the slide's variables/domains/constraints list, and the constraint hypergraph. The carry labels the §3.4.3 narrative anchors on are now visible. Updated `figures.md` accordingly.

### P0-5 (R1) — fig06 re-extracted from page render
**File:** `study/extracted_figures/L07/fig06-constraint-graph-map.png` ← now copy of `page10-render.png`

**Before:** The file showed only the constraint graph; the chapter caption claimed "the Australia map and its constraint graph side by side". A reader was instructed to look at two things that were not visible together.

**After:** Replaced with the page-10 render showing the map and the graph side by side, with the slide's commentary bullets ("Nodes are variables, arcs show constraints…"). The caption now matches the figure. Alt text minor cleanup; caption left as "side by side" (now correct). Updated `figures.md` accordingly.

### P0-6 (R4) — §5.6 worklist initialisation cleaned up
**Location:** §5.6 (`L07-CSP.md` lines around 712–716).

**Before:** Round-1 worklist line included `NT→NSW (not adjacent, skip)` inside an enumeration of "every directed arc between unassigned variables", which is logically inconsistent (a non-adjacent pair produces no arc) and asymmetric (other non-edges NT–V, NT–T, SA–T, NSW–T, V–T were not enumerated-and-skipped).

**After:** Rewrote the worklist initialisation to enumerate only the eight directed arcs that genuinely exist between unassigned-and-constrained pairs:

> Seed the worklist with every directed arc between unassigned variables — only pairs that share a constraint produce arcs. From the Australia adjacency (§3.3), the unassigned-adjacent pairs are NT–SA, SA–NSW, SA–V, NSW–V (each yielding two directed arcs):
>
> `NT→SA, SA→NT, SA→NSW, NSW→SA, SA→V, V→SA, NSW→V, V→NSW`
>
> Eight directed arcs total. T is isolated and shares no constraint with anyone, so it contributes no arcs. NT shares no edge with NSW, V, or T, so it produces no arcs to them either. (The formal AC-3 worklist also seeds arcs *from* assigned variables WA and Q outward; we omit them here as an optimisation because the assigned variables' singleton domains cannot be pruned further.)

This addresses both Reviewer 2's P1-R2-3 (clean eight-arc enumeration) and Reviewer 4's P0-1 (no phantom skip-arc; explicit acknowledgement that this is an optimisation vs the formal AC-3 seed).

---

## P1 Fixes Applied

### R2 P1-1 — Stage 6 figure caption mis-anchor
**Location:** §4.7 (`L07-CSP.md` line ~507).

**Before:** "Stage 6 (slide 41): after X_2 = 4, X_3 ∈ {2}, X_4 ∈ {3}." But slide 41 actually shows X3 = {2,4}, X4 = {2,3} (FC pending); the post-FC state X3 = {2}, X4 = {3} appears on slide 42.

**After:** Re-anchored:
- Stage 5 caption now reads "(slide 40): try X_2 = 4 (queen at row 2, column 4); FC not yet propagated (X_3 still {2,4}, X_4 still {2,3})".
- Stage 6 caption now reads "(slide 42): after FC for X_2 = 4 propagates, X_3 ∈ {2}, X_4 ∈ {3}."
- Stage 7 caption updated from "(slide 42)" to "(slide 43): try X_3 = 2" to remove the duplicate slide-42 reference and align with the actual slide sequence.
- Updated `figures.md` row for `fig30-4q-x2-4-domains.png` to source slide 42 (was slide 41) and added a note about the FC-pending vs FC-applied distinction.

### R2 P1-2 — Slide 39 X4 = {3} artefact footnote
**Location:** §4.7 (`L07-CSP.md` line ~501).

**Before:** The chapter discussed only the X3 wipeout after X2 = 3 and did not flag that slide 39's depicted `X4 = {3}` is itself inconsistent with proper FC.

**After:** Added a blockquoted "Note on slide 39 (beyond the slide)" after the X3 explanation:

> Slide 39 depicts $D_{X_4} = \{3\}$ at this point, but proper FC after $X_2 = 3$ should give $D_{X_4} = \{2\}$: with $X_2$'s queen at $(2, 3)$, $X_4 = 3$ shares its column with $X_2$ (remove), while $X_4 = 2$ is non-conflicting (column diff $|2-3| = 1$, row diff $|4-2| = 2$, not equal — no diagonal conflict; column not shared — keep). The slide's depiction may be an artefact of the animation (once $X_3$'s wipeout signalled failure, FC was halted before fully updating $X_4$). Either way, the failure is correctly detected via $X_3$'s empty domain — the discrepancy is only in the displayed $X_4$ state, not in the algorithm's behaviour.

This is consistent with the chapter's pattern of flagging slide-side bugs (cf. the §3.4.2 "Note (beyond the slide)" on slide 12's missing qualifiers).

### R4 P1 — §4.7 4-queens continuation X4 arithmetic
**Location:** §4.7 (`L07-CSP.md` line ~527).

**Before:** "with $X_2 = 4$ propagated $X_3 \in \{1\}$ and $X_4 \in \{3\}$" — wrong at that stage; $X_4 \in \{1, 3\}$ until $X_3 = 1$ is also assigned and propagated.

**After:** Rewrote the continuation with the correct intermediate states:

> forward checking after $X_1 = 2$ leaves $X_2 \in \{4\}$ (the only column non-conflicting with row 1 / column 2), $X_3 \in \{1, 3\}$, and $X_4 \in \{1, 3, 4\}$. After $X_2 = 4$ is propagated, $X_3 \in \{1\}$ and $X_4 \in \{1, 3\}$. Then $X_3 = 1$ is assigned; propagating that, $X_4 \in \{3\}$; assign $X_4 = 3$ — yielding $(X_1, X_2, X_3, X_4) = (2, 4, 1, 3)$.

The continuation now shows the X4 domain shrinking step-by-step, matching proper FC arithmetic.

### R4 P1 — Unicode replacement chars in §3.5
**Location:** §3.5 (`L07-CSP.md` lines ~327, 332).

**Before:** The two slide-18 blockquotes contained `�` (Unicode U+FFFD replacement character) at the bullet positions — encoding artefact from when the slide text was pasted.

**After:** Replaced both `�` characters with the proper bullet `•` (U+2022). The blockquotes now read cleanly:

> In CSPs, variable assignments are commutative
> • For example, [WA = red then NT = green] is the same as [NT = green then WA = red]

> We only need to consider assignments to a single variable at each level (i.e., we fix the order of assignments)
> • Then there are only $m^n$ leaves ($n$ = number of variables and $m$ = number of values)

### R4 P1 — AC-3 naming rotation
**Location:** §4.8 (`L07-CSP.md` line ~566).

**Before:** The chapter rotated among three names — "arc-consistency algorithm", "AC-3-style propagation", and "AC-3" — within the body. Cost a few seconds of re-reading.

**After:** Updated the §4.8 disambiguation paragraph to declare a canonical term and stop the rotation:

> The cascade is precisely the classical **arc-consistency algorithm** — usually called **AC-3** in textbooks, but **the slide does not use the name "AC-3"**. We adopt **arc-consistency algorithm** as the canonical term throughout this chapter, noting "AC-3" once here as the textbook name; we do not claim "AC-3" is the slides' terminology. See the [glossary entry](../_shared/glossary.md) (open canonicalisation question §6) for the rationale. The slides' procedure is functionally identical to AC-3: maintain a worklist of arcs, pop an arc, prune the tail's domain, and on any change re-add the affected reverse arcs.

Did not chase every downstream use of "AC-3" — §6 pitfall #8 and §8 cheat-sheet still mention AC-3 in their explicit textbook-name disclaimer paragraphs, which is the correct usage (citing the textbook name once with the disclaimer). The body of §4.8 itself, and the §5.6 trace, now consistently say "arc consistency" / "arc-consistency algorithm".

---

## Items NOT Addressed (out of scope for this round, per brief)

The brief explicitly listed only the items above. Deferred items observed but not addressed in this pass:

- **R1 P1-3, P1-4, P1-6, P1-7, P1-8, P1-9, P1-10** — pedagogical and consistency polish; not load-bearing on figure or P0 fixes.
- **R2 P2 items** — wart fixes, mostly cosmetic.
- **R3 P2 items** — eight rendering / link-density / phrasing polishes; explicitly marked as non-blocking by R3.
- **R4 P1-5, P1-7, P1-8, P1-9, P2 items** — Lab note styling, hypothetical-cascade table truncation (the trace exists; expansion is a missed pedagogical opportunity but not a P0), carry-narrowing units-column nit, slide-numbering double-check (now partially covered via the Stage 6/7 re-anchor).

---

## Files Modified

| File | Change |
|---|---|
| `c:/Users/samgl/Documents/GitHub/ExamPrep/AI/study/lectures/L07-CSP.md` | §4.7 K4 note replaced with one sentence; §4.7 slide-39 footnote added; §4.7 figure captions for Stages 5–7 re-anchored; §4.7 4-queens continuation re-derived correctly; §3.5 `�` → `•`; §4.8 AC-3 naming canonicalised; §3.3 fig06 alt text aligned with new figure |
| `c:/Users/samgl/Documents/GitHub/ExamPrep/AI/study/extracted_figures/L07/fig01-8queens-board-empty.png` | Replaced with `page03-render.png` copy |
| `c:/Users/samgl/Documents/GitHub/ExamPrep/AI/study/extracted_figures/L07/fig02-8queens-attacked-squares.png` | Replaced with `page04-render.png` copy |
| `c:/Users/samgl/Documents/GitHub/ExamPrep/AI/study/extracted_figures/L07/fig06-constraint-graph-map.png` | Replaced with `page10-render.png` copy |
| `c:/Users/samgl/Documents/GitHub/ExamPrep/AI/study/extracted_figures/L07/fig09-nqueens-csp-board.png` | Replaced with `page12-render.png` copy |
| `c:/Users/samgl/Documents/GitHub/ExamPrep/AI/study/extracted_figures/L07/fig10-cryptarithmetic-sum.png` | Replaced with `page13-render.png` copy |
| `c:/Users/samgl/Documents/GitHub/ExamPrep/AI/study/extracted_figures/L07/figures.md` | Updated rows for fig01, fig02, fig06, fig09, fig10 (re-extraction note + new source) and fig30 (slide-42 attribution + FC-pending vs FC-applied clarification) |

## Verification

All five replaced figure files visually inspected after copy. Page renders confirmed to contain the imagery the chapter captions describe:
- fig01: 8×8 board with two red-star queens (slide 3).
- fig02: 8×8 board with two red-star queens and overlaid black-dot attacked squares (slide 4).
- fig06: Australia map and constraint graph side-by-side with slide commentary (slide 10).
- fig09: Variable/domain/constraint list + 4×4 board with cell `X_ij` labelled in blue (slide 12).
- fig10: `TWO + TWO = FOUR` with `X_3 X_2 X_1` carry labels above the columns + constraint hypergraph (slide 13).

Chapter render via Read tool confirmed:
- §4.7 lead-in is now a single concise paragraph terminating with "slide 35 draws all six edges".
- §4.7 Stage 5/6 captions distinguish FC-pending vs FC-applied states.
- §4.7 slide-39 footnote added immediately after the X3 wipeout explanation.
- §5.6 worklist initialisation lists eight arcs cleanly; no skip parenthetical; explicit optimisation note.
- §3.5 blockquotes now use proper `•` bullet.
- §4.8 AC-3 naming canonicalised to "arc-consistency algorithm".

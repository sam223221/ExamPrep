# L07 — Round 2 — Reviewer #1 (Concept Completeness incl. Figures)

**Chapter:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\lectures\L07-CSP.md`
**Source PDF:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\Lecture7-Constraint Satisfaction Problem.pdf`
**Figure catalogue:** `c:\Users\samgl\Documents\GitHub\ExamPrep\AI\study\extracted_figures\L07\figures.md`
**Round 1 reference:** `revise-summary.md` (Round 1's `reviewer1.md` was never produced — PM-supplied P0 list was used as substitute)

**Reviewer brief:** verify the eleven Round 1 P0 fixes claimed in `revise-summary.md` (item by item), then sweep the rest of the chapter and figure set for residual completeness gaps. Be harsh.

**Status: FAIL** (re-revise required).

---

## Headline

Round 1 fixed several real problems (notably the cryptarithmetic carry-domain, the §3.5 derivation, the §5.6 AC-3 trace, the §4.7 slide-41/43 reasoning) but the K4 "fix" introduced a **new fabrication** that is mathematically equivalent to the one it was supposed to remove, and a string of figure-caption claims still misrepresent what the underlying figure files actually contain. Concept coverage is broadly complete; concept *fidelity to the visual source* is not.

I am the first reviewer to physically open the extracted figure files and compare them to chapter captions. Several captions are demonstrably wrong about what their figure depicts. This is exactly the class of defect the §7 QA checklist is supposed to catch.

---

## P0 Findings (must fix before P1 or merge)

### P0-1 — The K4 "Note on the slide-35 picture" is itself a fabrication

**File:** `L07-CSP.md` §4.7, the paragraph beginning "**Note on the slide-35 picture.**"

**Chapter claim:**
> "The four-box diagram drawn on slide 35 visually emphasises only a subset of $K_4$'s six edges (X1–X2, X3–X4, X1–X4, X2–X3 are drawn most prominently); the left and right vertical edges X1–X3 and X2–X4 may render less obviously depending on rendering."

**What slide 35 actually shows** (verified by reading `fig24-4q-start.png` — the page-render of slide 35 — image attached to source PDF page 35): the constraint graph has **all six K4 edges fully drawn and equally weighted**:

- X1 — X2 (top horizontal)
- X3 — X4 (bottom horizontal)
- X1 — X3 (left vertical)
- X2 — X4 (right vertical)
- X1 — X4 (NE-SW diagonal of the X)
- X2 — X3 (NW-SE diagonal of the X)

There is no visual de-emphasis. The two verticals are drawn at exactly the same line weight as everything else. The Round 1 fix invented a problem that does not exist on the slide, in order to "explain" a non-existent omission.

This is the **same class of error** Round 1 P0 #1 was supposed to eliminate — fabricating slide content that isn't there.

**Fix:** delete the entire "Note on the slide-35 picture" paragraph (lines around §4.7, just after the "complete graph K_4" sentence). Replace with one sentence:

> The slide draws the constraint graph as the complete graph $K_4$ — all six pairs of variables share at least one constraint (either column-equality $X_i \neq X_j$ or the diagonal constraint $|X_i - X_j| \neq |i - j|$), and the slide picture reflects this by drawing all six edges.

The downstream "no row is spared, forward checking after $X_1$ must prune $X_2$, $X_3$, *and* $X_4$" conclusion is correct and should be kept.

---

### P0-2 — fig01 and fig02 are slide titles, not figures

**Files:**
- `study/extracted_figures/L07/fig01-8queens-board-empty.png`
- `study/extracted_figures/L07/fig02-8queens-attacked-squares.png`

These two files are not the figures the chapter and figures.md claim they are.

**fig01 actual content:** the white-on-grey text "Motivating example: 8 Queens". No chessboard. No queens. Just the slide title.

**fig02 actual content:** the white-on-grey text "What more do we need for 8 queens?" Also just a slide title.

**Chapter captions:**
- §3.4.2 captions fig01 as "8-queens motivating board. The text on the slide notes that with no redundancy reduction one would enumerate $8^8$ combinations."
- §3.4.2 captions fig02 as "after placing the two queens it is trivial to mark squares we can no longer use. The visual makes 'constraint propagation = early failure detection' obvious."

Both captions describe content that the file does not contain. The reader who follows these references sees only a title bar.

**Root cause:** the raw extraction (`raw_p03_i01.png`, etc.) selected the title-text element from PDF page 3/4 instead of the embedded board image. The page-render alternatives (`page03-render.png`, `page04-render.png`) presumably do contain the boards — but the `_rename.py` step picked the wrong source.

**Fix:** re-extract fig01 and fig02 from `page03-render.png` and `page04-render.png` (cropped to the board) or from a different raw_p0X_iYY image. Do *not* leave the current files in place — they are useless for the §3.4.2 motivation and silently break the visual narrative.

**Severity:** P0 because §3.4.2's claim that "constraints propagate, vast swathes of the board are forbidden — see the visual" has no visual to back it up. A reader who only consumes figures will get nothing here.

---

### P0-3 — fig09 caption misrepresents what slide 12 depicts

**File:** `study/extracted_figures/L07/fig09-nqueens-csp-board.png`
**Chapter location:** §3.4.2, immediately after the slide-12 constraint list.

**Chapter caption:** "the $X_{ij}$ variable is one Boolean per cell. (Lecture 7, slide 12.)"
**figures.md caption:** "Board with the cell `X_{ij}` highlighted, used to define the N-queens CSP."

**What fig09 actually shows:** a 4×4 chessboard with **four queens placed** at (1, 2), (2, 4), (3, 1), (4, 3) — i.e. the second 4-queens solution. No cell is highlighted. No "$X_{ij}$" label appears on the figure.

The figure cannot support the claim it is being used to make. The §3.4.2 paragraph it sits under is defining the *Boolean-per-cell* formulation; the figure shows the *compact integer-per-row* solution. These are different formulations of n-queens (the chapter itself spells this out two paragraphs later) — embedding the solution-board figure under the Boolean-per-cell definition actively confuses the reader.

**Fix:** either (a) re-extract a slide-12 image that actually shows a highlighted $X_{ij}$ cell on the empty board, or (b) move fig09 down to the "alternative formulation" paragraph and re-caption it as "a 4-queens solution under the compact formulation: $X_1=2, X_2=4, X_3=1, X_4=3$".

---

### P0-4 — fig10 is missing the carry-variable labels its caption advertises

**File:** `study/extracted_figures/L07/fig10-cryptarithmetic-sum.png`
**Chapter caption:** "cryptarithmetic puzzle `TWO + TWO = FOUR`. Each letter is a distinct digit; **carries `X1, X2, X3` are auxiliary variables**. (Lecture 7, slide 13.)"

**What fig10 actually shows:** the addition `TWO + TWO = FOUR` in plain text. Nothing else. No `X1 X2 X3` labels above the columns.

**What slide 13 actually shows** (verified via `page13-render.png`): the addition with `X_3 X_2 X_1` labels above the columns. So the carry labels exist on the slide; the extracted fig10 just doesn't include them.

This is a P0 because the chapter's §3.4.3 narrative immediately introduces `X_1, X_2, X_3` as the units/tens/hundreds carries, and the figure is the only place those names are visually anchored to columns. With the labels missing from fig10, a reader has no way to see which carry attaches to which column.

**Fix:** re-extract from `page13-render.png` and crop to include the `X_3 X_2 X_1` line above the sum.

---

### P0-5 — fig06 caption claims "side-by-side", figure is the graph alone

**File:** `study/extracted_figures/L07/fig06-constraint-graph-map.png`
**Chapter caption:** "the Australia map and its constraint graph **side by side**. Tasmania (T) has no neighbours and is therefore isolated in the graph. (Lecture 7, slide 10.)"

**Figure content:** the constraint graph only. The Australia map is not in the frame. T is shown isolated *in the graph* — that part of the caption is correct.

The "side by side" claim is wrong. The reader is told to look at two things they cannot see together.

**Fix:** either (a) re-extract from `page10-render.png` to produce a true side-by-side image (slide 10 does have them side by side per my read of the page render), or (b) re-word the caption to "the constraint graph alone" and let the slide-8 map (fig04) carry the map half of the comparison.

This is P0 because §3.3 is the *defining* section for "constraint graph" — getting the figure wrong here propagates downstream.

---

## P1 Findings

### P1-1 — figures.md table entry for fig30 contradicts the chapter

`figures.md` row for fig30 says: "After `X_2 = 4`: `X_3 ∈ {2}`, `X_4 ∈ {2,3}` (partially shown)."

The chapter §4.7 says (correctly, and matching the file): "After $X_2 = 4$ (queen at row 2, column 4), forward checking refines the domains as follows ... $D_{X_4} = \{3\}$."

So `figures.md` is wrong about fig30 (it says $X_4 \in \{2,3\}$; the figure and the chapter both have $X_4 = \{3\}$). This is a single-line inconsistency between the two documents. The chapter is right; figures.md is wrong.

**Fix:** correct the figures.md table entry for fig30 to read `X_3 ∈ {2}, X_4 ∈ {3}`.

### P1-2 — fig08 caption claims "two example boards", figure shows one board

`figures.md` row for fig08: "Two 4-queens example boards (one a non-solution, one a solution)."
**figure content:** a single 4×4 board with 4 queens placed (the solution $X_1=2, X_2=4, X_3=1, X_4=3$).

The chapter caption is shorter and ambiguous ("two 4-queens example boards (one is a solution)"), so the chapter inherits the same inaccuracy.

**Fix:** re-extract slide 11 (`page11-render.png`) which likely contains both boards, or correct the captions to match the single board actually present.

### P1-3 — Glossary front-matter says "Arc-consistency algorithm (textbook name: AC-3)" but body insists slides do not use "AC-3"

The chapter top matter lists glossary terms including "Arc-consistency algorithm (textbook name: AC-3)". §4.8 and §6 pitfall 8 both say "the slide does not use the name AC-3". This is internally consistent — the textbook-name parenthetical *is* the disclaimer in compact form — but a reader skimming the front matter and the §8 cheat-sheet picks up "AC-3" as a chapter-level term without seeing the disclaimer until §4.8. Recommend either (a) moving the disclaimer to the front-matter line itself, or (b) dropping "AC-3" from the front matter and keeping it only as the textbook attribution in §4.8 and §8.

### P1-4 — §3.4.2 slide-12 constraint set: chapter omits the unary "T ≠ 0, F ≠ 0" analogue and the *anti-diagonal* on-board qualifier wording is awkward

The qualifier paragraph is correct in spirit ("for every integer $k \neq 0$ such that $(i + k, j - k)$ is on the board") but uses *the same $k$* across the four pair-constraint families (row, column, two diagonals). That is technically fine because each family scopes its own $k$, but it reads as if one $k$ is being reused — a reader could legitimately misread it as a constraint coupling row/column/diagonal pruning through a shared $k$. Recommend renaming the $k$ inside each family (or stating "for each pair we re-quantify $k$ over $\mathbb{Z} \setminus \{0\}$ subject to the on-board condition").

### P1-5 — §4.7 forward-checking trace: the figure for "fig33-4q-x4-empty" was meant to be slide 44 ("backtrack to X_1 = 2") but is captioned as the dead-end state under X_1=1

`fig33-4q-x4-empty.png` (verified by Read): board shows X1=(1,1) and X3=(3,2) marked as stars; domains: $X_3 = \{2\}$, $X_4 = \{ , , , \}$ (empty). Chapter caption: "every branch under $X_1 = 1$ fails; backtrack to $X_1$ and try $X_1 = 2$."

The figure does show X4 empty (so "branch fails") but does NOT depict the backtrack action / a new X1=2 attempt. The caption overstates what the figure shows. The reader expecting to see "X1=2 being tried" won't find it on the slide; that step is the chapter's continuation paragraph, not a slide. Recommend tightening the caption: "$X_4$ empty under $X_1=1, X_3=2$ — the algorithm now backtracks past $X_3$, $X_2$, and finally $X_1$, and will try $X_1 = 2$ next (continuation not shown on slides)."

### P1-6 — §3.4.4 Sudoku: 27 Alldiff claim is correct but the constraint count assumes a 9×9 board only

§3.4.4 says "Sudoku has 27 `Alldiff` global constraints" without restricting to 9×9. The lecture's slide 14 also assumes 9×9 by default — this is fine — but a reader extrapolating to general 4×4 / 16×16 / etc. should know the count is $3 \times n$ for an $n \times n$ Sudoku (or more precisely $n$ row + $n$ column + $n$ box = $3n$ for the standard partitioning). A one-sentence note would close the gap.

### P1-7 — §4.8 pseudocode "snapshot of D_X" subtlety mentioned in code but not explained

The REVISE pseudocode comment says "iterate snapshot to avoid invalidation" — this anticipates a Python-style "don't mutate while iterating" pitfall. Good. But the chapter never tells the reader *why* this matters in the AC-3 setting. A one-sentence prose note ("If we remove values from $D_X$ mid-iteration we may skip the next candidate; iterating a snapshot is the standard textbook fix.") makes the comment carry weight. This was flagged P2 in Round 1 (Reviewer #2 P2-1) and marked fixed; the snapshot comment is present but the *why* is still missing.

### P1-8 — §2.10 Newton's-cradle analogy: "lossless" framing slightly misleading

"A Newton's cradle is symmetric and lossless; constraint propagation is asymmetric (arcs are directed) and lossy (every pruning step shrinks the search space, you never 'get values back')." This is correct in the math sense but the word "lossy" in computing usually means *information lost erroneously* (lossy compression). Pruning impossible values is not lossy in that sense — it loses *impossible* values, not information. Suggest "monotone-shrinking" or "one-way" instead of "lossy".

### P1-9 — figures.md "REWORK" verdict for fig18 not applied in the chapter

`figures.md` flags fig18 as REWORK with rationale "Embedded with a prose walk-through, because the slide is mostly text and the image is small." §4.4 embeds fig18 with a single-line caption but no prose walk-through of the slide's text. The promised rework is missing.

### P1-10 — DOCUMENT.md presence (standing check)

`PM/conventions.md` (per global PM rules) requires a `DOCUMENT.md` in every directory where files were created/modified. I did not see a `study/lectures/DOCUMENT.md`, `study/extracted_figures/L07/DOCUMENT.md`, or `study/_review/L07/DOCUMENT.md`. If the project convention exempts study-content directories, that is an explicit waiver the PM should record; otherwise this is a standing P1.

---

## P2 Findings

### P2-1 — §2 mapping table redundant with subsection titles
The "How to read this section" table is helpful as a one-glance index but each row repeats information from the immediately-following subsection title. Consider a tighter format (e.g. just `§2.1 Sudoku → §3.1, §3.4.4`).

### P2-2 — Cross-link density may be too high
Every §3/§4 subsection now has a "*Recall §2.x…*" line. For the §3 subsections that are deeply formal, the recall lines occasionally interrupt the flow. Consider clustering them at the end of each major section instead of inline.

### P2-3 — "Beyond the slide" prose colour
The phrase "beyond the slide" appears 5+ times. Consider varying with "from the textbook (R&N)" or "from later course material" once or twice for prose variety.

### P2-4 — fig07 (constraint-graph-only redraw) duplicates the mermaid in §3.3
§3.3 has the constraint graph as a Mermaid diagram AND embeds fig07. figures.md calls this redundancy intentional ("REWORK" verdict). For exam-prep purposes the Mermaid is more readable; the fig07 PNG could be cut to reduce visual clutter.

### P2-5 — `T ≠ 0` and `F ≠ 0` unary constraints not visualised on the cryptarithmetic hypergraph
§3.4.3 lists `T ≠ 0` and `F ≠ 0` as unary constraints. fig11 (the hypergraph) shows the column-sum, $X_3=F$, and Alldiff constraints but not the unary ones. Optional addition: a parenthetical "(unary constraints `T ≠ 0`, `F ≠ 0` not drawn — by convention unary constraints absorb into the variable's initial domain)".

### P2-6 — §5.6 hypothetical cascade table is incomplete ("...continue")
The "Hypothetical cascade" table in §5.6 trails off with a "...continue" row. Either complete it or remove it; trailing it half-finished suggests work-in-progress. The Round 1 revise-summary flagged this as a question to the reviewer — my recommendation is to either complete the cascade with a real terminal state or replace the table with a one-paragraph prose description of the worst case.

### P2-7 — §3.5 commutativity quote uses garbled bullet character
The block-quote of slide 18 contains a `�` (replacement character) where a bullet `•` should be. Cosmetic but visible.

### P2-8 — §4.8 cost note repeats the same disclaimer text in §4.8 and §8 cheat-sheet
Both places say the same paragraph about "the slides do not state this bound". Fine, but one factoring (e.g. just "AC-3 worst case $O(c \cdot d^3)$ — beyond the slide") would suffice in the cheat-sheet.

---

## Verification of Round 1 P0 Fixes (item-by-item)

Using the 11 items listed in `revise-summary.md`:

| # | Round 1 claim | Verdict | Note |
|---|---|---|---|
| 1 | §4.7 K4 claim — clarified with "Note on the slide-35 picture" | **FAIL** | The new note is itself a fabrication; see P0-1. The K4 graph on slide 35 has all six edges fully drawn. |
| 2 | Figure-to-slide alignment in §4.7 (slides 40–43) | **PASS (partially)** | The chapter text now correctly traces $X_2=4 \Rightarrow X_3=\{2\}, X_4=\{3\}$ and $X_3=2 \Rightarrow D_{X_4} = \emptyset$. The trace matches figs 29–32. fig33 is over-captioned (see P1-5). |
| 3 | Cryptarithmetic carry domains — match slide | **PASS** | §3.4.3 now reads "{0,1,...,9} for *all* variables" with the {0,1} narrowing tagged "beyond the slide". |
| 4 | Slide 18 block-quote fabrication — replaced | **PASS** | Two separate verbatim quotes now present in §3.5. Minor: a `�` rendering artefact remains (P2-7). |
| 5 | §3.2 goal-test attribution mixes slides 7 and 16 | **PASS** | §3.2 now opens with explicit dual-citation. Each bullet attributed. |
| 6 | Concrete AC-3 worklist trace for §5.6 | **PASS** | §5.6 now has starting-state table, worklist init, step-by-step trace, hypothetical cascade. The cascade is mid-sentence "…continue" (P2-6) but the main trace is solid. |
| 7 | §4.7 4-queens trace at slide 39 — both X3 removals explained | **PASS** | Per-value diagonal arithmetic spelled out. |
| 8 | §3.4.2 4-queens diagonal constraint — k ≠ 0 / j ≠ k scoping | **PASS** | Qualifiers added; "Note (beyond the slide)" present. Minor scoping awkwardness P1-4. |
| 9 | Missing §2 analogies for Consistent / Degree / Constraint propagation | **PASS** | §2.8, §2.9, §2.10 added; consistent visual format with `> **Where it breaks down.**` blockquotes. |
| 10 | Cross-links from §3/§4 to §2 | **PASS** | "*Recall §2.x…*" lines added throughout. May be too dense (P2-2). |
| 11 | $O(c·d^3)$ AC-3 complexity not on slides — source-tagged | **PASS** | §4.8 and §8 both now tag the bound as textbook (R&N), not slide. |

**Net verification:** 9 of 11 pass; 1 fails (P0-1); 1 passes with non-trivial subordinate P1 (#2 + P1-5).

---

## Out-of-scope observations

- The chapter is otherwise in good shape concept-wise. The §2 → §3 → §4 → §5 → §6 → §8 spine reads coherently. The pitfall list (§6) is the strongest section of the chapter and would survive an exam-day read on its own.
- The Tetris analogy (§2.8) is the weakest of the §2 set — Tetris is dynamic and CSP is static, so the analogy collides with the actual semantics in a way the breakdown caveat doesn't fully neutralise. Consider an alternative (e.g. "a half-finished crossword without contradictions yet") for a future round.
- The §7 / Lab 6 cross-link points at `AI/lab6/` files that I did not verify exist. The Investigator agent should confirm `Colors.py`, `States.py`, `constraints_template.py` actually exist before the chapter ships.

---

## Concerns / risks

- **The K4 P0 (Round 1 #1) keeps drifting between two failure modes.** Round 0: chapter said "constraint graph is K4" but didn't engage with the slide picture. Round 1: chapter added a note inventing a partial-edge slide. Round 2 needs to *just describe the slide correctly*: K4 with all six edges drawn. If we don't pin this down now we'll see a third variation in Round 3.

- **Figure extraction quality is the bottleneck.** Fig01, fig02, fig09, fig10 are wrong-content extractions, not authorial errors. The chapter author wrote captions assuming the slides' canonical contents; the extractor picked the wrong embedded PNG. This is fixable by re-running `_rename.py` against the `pageNN-render.png` versions (which I verified do contain the right content for slide 13).

- **figures.md has drifted from the chapter** (P1-1, P1-2). The two documents need a single canonicalisation pass.

- **DOCUMENT.md (standing P1)** is the only checklist item I cannot verify from the chapter alone — the PM should confirm whether study-content directories are exempted.

---

## Report to PM

**Assignment recap:** L07 Round 2 review — Concept Completeness incl. Figures. Verifying Round 1's 11 P0 fixes plus residual sweep.

**Status:** **Fail** — re-revise required.

**P0 findings:**
1. **P0-1** — §4.7 "Note on the slide-35 picture" is a fabrication. Slide 35 draws all six K4 edges; the chapter's claim that the slide "emphasises only a subset" is false. Fix: replace the entire note with a single sentence affirming all six edges are drawn. *(file: `study/lectures/L07-CSP.md` §4.7 — the paragraph right after the "complete graph K_4" sentence.)*
2. **P0-2** — `fig01-8queens-board-empty.png` and `fig02-8queens-attacked-squares.png` are extracted slide titles, not figures. They contain no board / no queens / no attacked-square dots. Fix: re-extract from `page03-render.png` and `page04-render.png`.
3. **P0-3** — `fig09-nqueens-csp-board.png` does not show a highlighted $X_{ij}$ cell; it shows a complete 4-queens solution. The chapter caption is wrong, and the figure is mis-placed under the Boolean-per-cell formulation section. Fix: re-extract or re-position.
4. **P0-4** — `fig10-cryptarithmetic-sum.png` is missing the `X_3 X_2 X_1` carry-label line that the chapter's narrative depends on. The labels exist on slide 13 (verified via `page13-render.png`). Fix: re-extract with the carry line included.
5. **P0-5** — `fig06-constraint-graph-map.png` is captioned "map and graph side by side" but contains only the graph. Fix: re-extract or re-word.

**P1 findings:**
1. **P1-1** — `figures.md` row for fig30 contradicts the chapter (`X_4 ∈ {2,3}` vs the correct `X_4 ∈ {3}`).
2. **P1-2** — fig08 shows one board, not two as both `figures.md` and the chapter claim.
3. **P1-3** — Glossary front-matter advertises "AC-3" without the disclaimer that §4.8 carries.
4. **P1-4** — §3.4.2 quantifier $k$ scoping reads as if shared across constraint families.
5. **P1-5** — §4.7 fig33 caption overstates what the slide shows (depicts dead-end, not backtrack action).
6. **P1-6** — §3.4.4 Sudoku constraint count assumes 9×9 board only; one-line note needed.
7. **P1-7** — §4.8 REVISE "snapshot" comment is present but the *why* is missing.
8. **P1-8** — §2.10 "lossy" wording is misleading (loss-as-in-compression vs loss-as-in-pruning).
9. **P1-9** — figures.md REWORK verdict for fig18 not applied (no prose walk-through in §4.4).
10. **P1-10** — `DOCUMENT.md` presence in `study/lectures/`, `study/extracted_figures/L07/`, `study/_review/L07/` not verified — standing PM/conventions check.

**P2 findings:** see P2-1 through P2-8 above. Cosmetic / polish only.

**QA Checklist (§7) status (mapped to standing reviewer-#1 concerns):**
- Concept coverage of slides 1–55: **Pass** — every concept-bearing slide has chapter coverage.
- Figure-to-slide alignment: **Fail** (P0-2, P0-3, P0-4, P0-5).
- Verbatim-quote integrity: **Pass** (modulo P2-7 cosmetic).
- Source-tagging of non-slide claims: **Pass** (R&N AC-3 bound is correctly attributed throughout).
- Internal cross-link consistency: **Pass** (with P2-2 density caveat).
- Pitfalls / cheat-sheet alignment with body: **Pass**.

**Acceptance criteria (§1) status:** Round 1 fixes that succeeded materially improve exam readiness. The unfixed P0s (notably P0-1 and P0-2) leave the chapter still vulnerable to a "what is the constraint graph on slide 35?" or "what does slide 3 show?" exam question.

**DOCUMENT.md audit:** N/A for this directory (`study/_review/L07/round2/`). Standing P1-10 above flags the broader presence.

**Out-of-scope observations:**
- The §2.8 Tetris analogy is the weakest of the analogy set; consider replacement in a later round.
- Lab 6 cross-links assume `AI/lab6/Colors.py` etc. exist — un-verified by this reviewer.

**Concerns / risks:**
- P0-1 has now drifted across two rounds. Round 3 must lock the K4 description by simply describing the slide, not theorising about it.
- Figure-extraction quality is the systemic bottleneck — fixable in one re-run of `_rename.py` against the page renders.

**What PM should do next:**
1. Dispatch the figure-extraction agent (or whoever runs `_rename.py`) to re-anchor fig01, fig02, fig09, fig10, fig06 against the `pageNN-render.png` sources.
2. Dispatch the lecture-extractor / chapter author to delete the §4.7 "Note on the slide-35 picture" paragraph and replace with the single sentence proposed in P0-1.
3. Dispatch the figures.md maintainer to reconcile the fig30 and fig08 captions.
4. Once those three are done, re-run reviewers #1 (me) and #4 (Exam Readiness) for a closure pass. Do not advance to App Tester / Code Reviewer until P0s clear.

**DOCUMENT.md updated:** N/A for QA.

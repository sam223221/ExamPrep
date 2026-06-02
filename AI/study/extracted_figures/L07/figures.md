# L07 — Figure catalogue

Source PDF: `AI/Lecture7-Constraint Satisfaction Problem.pdf` (55 slide pages).

Extraction tooling:
- `_extract.py` — PyMuPDF (`fitz`) pass that (a) dumps every embedded `raw_pNN_iII.png`
  image and (b) re-renders selected whole slide pages at 200 dpi as `pageNN-render.png`
  (`EXTRACTION_METHOD: page-render`).
- `_rename.py` — copies the chosen raw/page-render files to stable `figNN-slug.png`
  names referenced from the chapter.

Verdict legend:
- **USE** — embedded in the chapter as-is.
- **REWORK** — embedded plus a Mermaid diagram / prose description alongside,
  because the extracted image is low-resolution or visually busy.
- **SKIP** — decorative; not embedded. Rationale must be given.

Whole-slide page renders are tagged `EXTRACTION_METHOD: page-render` because the
source PDF lays composite "queens + arrows + domain bars" diagrams that don't
decompose into single embedded images.

| fig file | source page(s) | slide caption / context | verdict | rationale |
|---|---|---|---|---|
| `fig01-8queens-board-empty.png` | 3 | Page-render of slide 3 ("Motivating example: 8 Queens"): the 8×8 board with two queens shown as red stars, plus the slide's prose noting $8^8 = 16{,}777{,}216$ combinations. | USE | Iconic example; needed in §1 / §2 to set up the puzzle. Previously the raw extraction picked the slide-title text; now sourced from `page03-render.png`. |
| `fig02-8queens-attacked-squares.png` | 4 | Page-render of slide 4 ("Motivating example: 8-Queens"): board overlaid with black dots showing every square attacked by either placed queen. | USE | Crucial visual for the "constraint propagation = early failure" intuition. Previously the raw extraction picked the slide-title text; now sourced from `page04-render.png`. |
| `fig03-rubiks-cube.png` | 6 | Decorative Rubik's-cube image on the CSP-Definitions slide. | SKIP | Decorative only; no informational content. Rationale: the slide caption uses it as a motivational hook, not to teach a concept. |
| `fig04-australia-map.png` | 8 | Australia outline labelled with the 7 territories (definition of Map-Coloring). | USE | The canonical CSP example map — needed everywhere downstream. |
| `fig05-australia-colored.png` | 9 | Same map with a complete consistent colouring `WA=red, NT=green, Q=red, …` | USE | First explicit "solution" picture; reinforces consistent/complete distinction. |
| `fig06-constraint-graph-map.png` | 10 | Page-render of slide 10 ("Constraint Graph"): Australia map and its constraint graph side by side (nodes WA NT Q SA NSW V T; T isolated), with the slide's commentary bullets. | USE | Defines what a constraint graph is. Sourced from `page10-render.png` so the side-by-side comparison the caption advertises is actually present. |
| `fig07-constraint-graph-nodes.png` | 10 | The graph alone. | REWORK | Embedded plus a Mermaid graph in §3 for clean text rendering. |
| `fig08-4queens-boards.png` | 11 | Two 4-queens example boards (one a non-solution, one a solution). | USE | Bridges 8-queens → general n-queens. |
| `fig09-nqueens-csp-board.png` | 12 | Page-render of slide 12 ("Example: N-Queens"): the slide's variable/domain/constraint list alongside a 4-queens board with the cell `X_ij` labelled in blue. | USE | Anchors the binary-variable formulation. Sourced from `page12-render.png` so the labelled `X_ij` cell the chapter narrative depends on is visible. |
| `fig10-cryptarithmetic-sum.png` | 13 | Page-render of slide 13 ("Example: Cryptarithmetic"): the puzzle `TWO + TWO = FOUR` with carry variables `X_3 X_2 X_1` labelled above the columns, alongside the variable/domain/constraint list and the hypergraph. | USE | Example illustrating non-binary / global constraints. Sourced from `page13-render.png` so the `X_3 X_2 X_1` carry labels the chapter narrative depends on are visible. |
| `fig11-cryptarithmetic-cgraph.png` | 13 | Constraint hypergraph: letters + carries connected through square constraint nodes. | USE | Shows how non-binary constraints can be drawn. |
| `fig12-sudoku-grid.png` | 14 | A partially filled Sudoku grid. | USE | Final motivating real-world example. |
| `fig13-backtracking-tree-1.png` | 19 | First step of the backtracking-search tree on map-coloring (root only). | USE | First panel of the tree-expansion sequence. |
| `fig14-backtracking-tree-2.png` | 20 | Tree after assigning WA = {red, green, blue}. | USE | Second panel. |
| `fig15-backtracking-tree-3.png` | 21 | Tree after extending the WA=red branch with NT choices. | USE | Third panel. |
| `fig16-backtracking-tree-4.png` | 22 | Tree extended with Q assignments below WA=red, NT=green. | USE | Fourth panel. |
| `fig17-backtracking-failure.png` | 23 | Failure point: SA cannot be coloured under `WA=red, NT=green, Q=green`; algorithm backtracks. | USE | Climactic panel — illustrates the actual "backtrack" step. |
| `fig18-mrv-small-map.png` | 26 | Small map with annotation showing MRV pick. | REWORK | Embedded with a prose walk-through, because the slide is mostly text and the image is small. |
| `fig19-lcv-choice.png` | 29 | Sequence of small maps illustrating the choice for variable Q (red vs blue) under LCV. | USE | Important to see the "which value leaves the most options" reasoning. |
| `fig20-fc-stage0-domains.png` | 31 | Forward-checking stage 0: all 7 variables have domain `{r,g,b}`, no assignments yet. | USE | First panel of the FC sequence. |
| `fig21-fc-stage1-wa-red.png` | 32 | Stage 1: WA=red ⇒ NT and SA lose red from their domains. | USE | FC panel 2. |
| `fig22-fc-stage2-q-green.png` | 33 | Stage 2: Q=green ⇒ NT, SA, NSW lose green. | USE | FC panel 3. |
| `fig23-fc-stage3-v-blue.png` | 34 | Stage 3: V=blue ⇒ SA's domain wipes out → backtrack. | USE | FC panel 4 — shows the early-failure detection. |
| `fig24-4q-start.png` | 35 | 4-queens initial CSP: four variables `X_i ∈ {1,2,3,4}`. | USE | Sets up the 4-queens FC trace. |
| `fig25-4q-x1-1.png` | 36 | 4-queens after `X_1 = 1` is highlighted (no FC pruning shown yet). | USE | FC panel 1 of the 4-queens trace. |
| `fig26-4q-x1-1-domains.png` | 37 | After `X_1 = 1`, neighbour domains pruned: `X_2 ∈ {3,4}`, `X_3 ∈ {2,4}`, `X_4 ∈ {2,3}`. | USE | FC panel 2 — pruning made explicit. |
| `fig27-4q-x2-3.png` | 38 | Try `X_2 = 3` (highlighted in red). | USE | FC panel 3. |
| `fig28-4q-x2-3-x3-empty.png` | 39 | After `X_2 = 3`, X_3's domain is empty — backtrack. | USE | FC panel 4 — first failure / backtrack. |
| `fig29-4q-x2-4.png` | 40 | Try `X_2 = 4`. | USE | FC panel 5 — second branch. |
| `fig30-4q-x2-4-domains.png` | 42 | After FC for `X_2 = 4` propagates: `X_3 ∈ {2}`, `X_4 ∈ {3}`. (Slide 41 actually shows the FC-pending state with `X_3 ∈ {2,4}`, `X_4 ∈ {2,3}`; slide 42 shows the FC-applied state captured here.) | USE | FC panel 6. |
| `fig31-4q-x3-2.png` | 42 | Try `X_3 = 2`. | USE | FC panel 7. |
| `fig32-4q-x3-2-domains.png` | 43 | After `X_3 = 2`: `X_4` domain empty — backtrack again. | USE | FC panel 8 — second failure. |
| `fig33-4q-x4-empty.png` | 44 | Final state showing `X_4` cannot be assigned under the current branch — total dead-end. | USE | FC panel 9 — concludes the trace. |
| `fig34-constraint-prop-nt-sa-blue.png` | 45 | Map after `WA=red`, `Q=green`; SA, NSW, V still have `{b}`; NT still has `{b}`; FC has not detected that NT and SA cannot both be blue. | USE | Motivates arc consistency over forward checking. |
| `fig35-arc-consistency-consistent.png` | 46 | Arc-consistency definition slide: `X→Y` consistent iff every X value has a supporting Y value. Example arc is consistent. | USE | First panel of the AC sequence. |
| `fig36-arc-consistency-check.png` | 47 | Checking arc V→NSW; the arrow indicator below the row. | USE | Sequence panel. |
| `fig37-arc-consistency-prune-nsw.png` | 48 | A value of NSW is pruned (×). | USE | Sequence panel showing pruning step. |
| `fig38-arc-consistency-recheck.png` | 49 | After pruning, neighbour arcs Z→X are re-queued. | USE | Sequence panel — illustrates the worklist re-check. |
| `fig39-arc-consistency-prune-v.png` | 50 | Another value of V is then pruned in cascade. | USE | Sequence panel. |
| `fig40-arc-consistency-cascade.png` | 51 | Cascade reaches SA — its domain shrinks further. | USE | Sequence panel — shows propagation reaching SA. |
| `fig41-arc-consistency-final.png` | 52 | Final reduced domains after AC; failure (or further constraint) detected earlier than FC. | USE | Sequence panel — completes the AC trace. |
| `fig42-arc-consistency-xy-example.png` | 53 | Toy AC example: `D_x = D_y = {1,2,3}`, constraint `X < Y` ⇒ `D'_x = {1,2}`, `D'_y = {2,3}`. | USE | Clean self-contained AC example for the exam-prep cheat sheet. |

## Coverage notes

- Slides **2, 7, 15, 16, 17, 18, 24, 25, 28, 30, 54, 55** are pure-text /
  list-only slides (no figures worth extracting). They are covered in the
  chapter text. Slide 55 is a "Thank you" slide — no content.
- Slides **20–22** are progressive expansions of the same backtracking tree
  (figs 14–16); the chapter embeds all four panels (figs 13–16) so the reader
  can see the tree grow.
- Slides **35–44** (`fig24`–`fig33`) form the canonical 4-queens forward-checking
  trace. All ten panels are kept because the exam is likely to ask the student
  to reproduce them.
- Slides **46–52** (`fig35`–`fig41`) form the arc-consistency animation. Kept
  in full for the same reason.
- The Rubik's-cube on slide 6 (`fig03`) is the only SKIP — it is purely
  decorative on a definitions slide.

# L05 — Local Search — Figure Catalogue

This catalogue documents every figure extracted from `Lecture5-Local Search.pdf`
(50 slides total). Every figure listed as **USE** or **REWORK** is embedded in
`study/lectures/L05-Local-Search.md`; **SKIP** figures are decorative or
duplicates.

Extraction method (see plan §6.1.1): the source slides combine vector text,
shapes, and small embedded images, so naive image-level extraction returns
only thumbnails (e.g. the `h=1` mini-board on slide 14 extracted as a
206×206 pixel block stripped of its annotation). For every informative
diagram we therefore use `EXTRACTION_METHOD: page-render` via
`fitz.Page.get_pixmap(dpi=200)`, which preserves the entire slide including
the surrounding text, labels, and any embedded raster art. Pure title /
"thank-you" / question-mark / DNA-decoration pages were never rendered.

All embedded figures live under `study/extracted_figures/L05/` and are
referenced from the chapter with relative paths
`../extracted_figures/L05/figNN-<slug>.png`.

---

## Catalogue

| # | Filename | Source page | Surrounding text / caption | Verdict | Rationale |
|---|---|---|---|---|---|
| 1 | `fig01-objective-landscape.png` | slide 2 | "Local search algorithms — objective function (3-D bumpy paraboloid graphic)" | USE | Visualises an objective function over a 2-D parameter space; embeds at §1 to motivate the "tells us about the quality of a possible solution" idea. EXTRACTION_METHOD: page-render. |
| 2 | `fig02-hill-climbing-8puzzle.png` | slide 5 | "Hill Climbing Example — 8-puzzle with $f(n)=-($tiles out of place$)$, sequence of moves from start to goal with heuristic values $h=-4, -3, -3, -2, -1, 0$" | USE | Canonical worked example of hill climbing on the 8-puzzle. Embeds at §5 Worked Examples. EXTRACTION_METHOD: page-render. |
| 3 | `fig03-tsp-pairwise-exchange.png` | slide 7 | "Traveling Salesman Problem — pairwise exchange `ABDEC → ABCED` shown on a 5-city graph" | USE | Shows the neighbour-generation move in TSP local search. Embeds at §5. EXTRACTION_METHOD: page-render. |
| 4 | `fig04-nqueens-local-improvement-h5.png` | slide 9 | "4-queens problem: local improvement reduces conflicts $h=5 \to h=2 \to h=0$" | USE | Three-stage 4-queens illustration. Embeds at §5. EXTRACTION_METHOD: page-render. |
| 5 | `fig05-nqueens-h17-board.png` | slide 10 | "8-queens example: board with $h = 17$ conflicting pairs" | USE | Sets up the $h=17$ starting state used by the next slide. Embeds at §5. EXTRACTION_METHOD: page-render. |
| 6 | `fig06-nqueens-h17-successors.png` | slide 11 | "Successor function returns all $8 \times 7 = 56$ states; each empty square shows the successor's $h$" | USE | Same board with per-square successor heuristic estimates; the most-cited diagram of hill climbing in the deck. Embeds at §5. EXTRACTION_METHOD: page-render. |
| 7 | `fig07-nqueens-example-solution.png` | slide 12 | "Example Solution — three successive boards, the queen in the lower-right column is moved up to local minimum 0, the global minimum" | USE | Shows the two-step path from the $h=17$ state to a global minimum and the local-minimum trap. Embeds at §5. EXTRACTION_METHOD: page-render. |
| 8 | `fig08-local-maximum-8queens.png` | slide 14 | "Hill-climbing search — local maximum for 8-queens ($h=1$) + 1-D state-space curve labelling global maximum and local maximum" | USE | Two diagrams on one slide: the canonical 1-D landscape and an 8-queens board stuck at $h=1$. Embeds at §3 (Local maximum) and §6 (pitfalls). EXTRACTION_METHOD: page-render. |
| 9 | `fig09-state-space-landscape.png` | slide 15 | "The state-space landscape — global maximum, local maximum, flat local maximum, shoulder, current state" | USE | Master 1-D landscape figure used to define every local-search pathology. Embeds at §3.1 / §3.5. EXTRACTION_METHOD: page-render. |
| 10 | `fig10-temperature-effect-curves.png` | slide 19 | "Effect of temperature — $\exp(\Delta / T)$ plotted for $T \in \{100, 50, 10, 1\}$, $\Delta \in [-100, 0]$" | USE | The single most important quantitative figure for simulated annealing. Embeds at §3.5 / §4.2 / §5. EXTRACTION_METHOD: page-render. |
| 11 | `fig11-oil-road-positions.png` | slide 29 | "Where to drill for oil? — two oil-rig icons at positions 300 and 900 on a 1km road" | USE | Sets up the oil-drilling running example for GA. Embeds at §5. EXTRACTION_METHOD: page-render. |
| 12 | `fig12-binary-string-table.png` | slide 31 | "Convert to binary string — table mapping 900, 300, 1023 to 10-bit bitstrings" | USE | Concrete encoding-to-chromosome demonstration. Embeds at §5. EXTRACTION_METHOD: page-render. |
| 13 | `fig13-oil-fitness-curve.png` | slide 32 | "Drilling for Oil — solutions 300 (chromosome `0100101100`) and 900 (`1110000100`) with fitness 30 and 5 on an oil-depth curve" | USE | Connects bitstrings to a fitness landscape. Embeds at §5. EXTRACTION_METHOD: page-render. |
| 14 | `fig14-fitness-landscapes-3d.png` | slide 35 | "Fitness landscapes — three 3-D surfaces: smooth bimodal, rugged moderate, extremely-rugged noise" | USE | Three landscape regimes side-by-side, motivating why GA can or cannot work. Embeds at §3.7 / §6. EXTRACTION_METHOD: page-render. |
| 15 | `fig15-example-population-table.png` | slide 41 | "Example population — 8 chromosomes (10-bit bitstrings) each with a fitness value" | USE | The starting table for the roulette-wheel example. Embeds at §5. EXTRACTION_METHOD: page-render. |
| 16 | `fig16-roulette-wheel-selection.png` | slide 42 | "Roulette wheel selection — cumulative-fitness bar of length 18, random draws $R=7$ select chromosome 4, $R=12$ selects chromosome 6" | USE | Definitive visualisation of roulette-wheel selection. Embeds at §4.3 / §5. EXTRACTION_METHOD: page-render. |
| 17 | `fig17-crossover-recombination.png` | slide 43 | "Crossover — single-point on `1010000000` + `1001011111` → `1011011111` + `1000000000`; crossover rate typically 0.8–0.95" | USE | Single-point crossover with concrete bitstrings. Embeds at §4.3 / §5. EXTRACTION_METHOD: page-render. |
| 18 | `fig18-mutation.png` | slide 44 | "Mutation — flips an offspring bit; rate typically 0.001–0.1" | USE | Companion to fig17, completing the GA operator triad. Embeds at §4.3 / §5. EXTRACTION_METHOD: page-render. |

## SKIP rationale (figures that were *not* extracted at all)

The following slides were inspected and excluded from extraction because
they contain no informative diagram for an exam-prep chapter:

- Slide 1 (title page with SDU logo).
- Slide 3 (text-only bullet list of approaches).
- Slide 4 (text-only hill-climbing motivation).
- Slide 6 (US-map screenshot of an arbitrary TSP tour — decorative; the
  textbook concept is captured by slide 7 instead).
- Slide 8 (4-queens problem statement: two small chessboards illustrating
  bad placements; the embedded raster was 235×246 px each — subsumed by
  slide 9 which adds the local-improvement narrative and uses the same
  imagery to better effect).
- Slides 13, 16–18, 20, 22, 24–28, 30, 33–34, 36–40, 45–49 (text-only
  algorithm pseudocode / bulleted exposition). The pseudocode is
  re-typeset in the chapter as proper code blocks, so embedding a
  page-render would add nothing.
- Slide 21 (stock DNA-helix illustration introducing GA history — purely
  decorative).
- Slide 23 (wooden-mannequin "?" stock photo).
- Slide 50 ("Thank you" closing slide).

## Coverage check

Every "Approaches" topic from slide 3 is represented in at least one
embedded figure:

- **Hill climbing** — figures 2, 4, 5, 6, 7, 8, 9.
- **Simulated annealing** — figure 10 (the only quantitative diagram in
  that section; the algorithm itself is text-only on slides 16–18, 20).
- **Genetic algorithms** — figures 11, 12, 13, 14, 15, 16, 17, 18.

Plus the master landscape (figure 1) at §1 and the rugged-landscape
panel (figure 14) at §3.7 / §6.

All embedded figures are `USE`. No `REWORK` entries were necessary
because the page-rendered slides preserve the lecturer's own annotation
and labelling; the chapter additionally backs each up with in-text prose
where extra clarity helps.

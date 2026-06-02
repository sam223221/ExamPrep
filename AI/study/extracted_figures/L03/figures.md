# L03 — Uninformed Search — Figures Catalogue

Source: `Lecture3-Uninformed Search.pdf` (56 slides). Figures were extracted with PyMuPDF using `study/extracted_figures/L03/_extract.py`.

Two extraction methods were used:

- **page-render** — full slide rasterised at 180 dpi via `fitz.Page.get_pixmap(dpi=180)`. Used for slides where the lecturer's diagram is a composite of text, arrows, colour overlays, and embedded images (e.g. BFS / DFS step-by-step frames where the red arrow and the green-fill node are slide-overlays on top of an embedded line drawing). Image-level extraction reliably loses the arrow/label.
- **image-extract** — individual embedded image objects extracted via `fitz.Pixmap(doc, xref)`. These are cleaner (no slide background) but on this deck they often capture only one fragment of a composite figure (e.g. the bare tree without the arrow showing which node is being expanded).

The verdict column uses one of three values:

- **USE** — the figure is embedded in the chapter `.md` at a sensible section.
- **REWORK** — the figure is embedded *and* accompanied by an extra prose/table backup, because the slide diagram alone is unclear or low-info.
- **SKIP** — the figure is present in this directory but **not** embedded in the chapter, with a justification recorded below.

Slide numbers below are 1-indexed PDF page numbers, matching `[Lecture 3, slide N]` references in the chapter.

## Page-render catalogue

| Seq | File | Slide | Verdict | What it shows / why |
|---|---|---|---|---|
| 01 | `fig01-maze-cover.png` | 2 | **SKIP** | Decorative maze image on the "Solving problems by searching" section opener. The chapter motivation re-uses the same idea verbally; no informational content lost by not embedding. |
| 02 | `fig02-problem-solving-flowchart.png` | 3 | **SKIP** | Joke "Problem Solving Flowchart" meme (yellow boxes with "Does the thing work? / You fool!"). Decorative; no concept to learn. |
| 03 | `fig03-search-maze-labelled.png` | 8 | **USE** | The labelled maze with "Start state" arrow at top-left and "Goal state" arrow at bottom-right. The canonical illustration of "search task = find a path from start to goal in a discrete state graph". Embedded in §2. |
| 04 | `fig04-search-problem-components.png` | 10 | **USE** | Same maze re-used to label the five components of a search problem. Embedded in §3.2 alongside the formal definitions. |
| 05 | `fig05-romania-map-and-graph.png` | 11 | **SKIP** | Slide 11's combined Romania map + road graph. Pedagogically redundant with `fig11` (slide 18's larger and cleaner road-graph render), which **is** embedded as Figure 6 of the chapter. Keeping only the cleaner of the two avoids visual clutter. |
| 06 | `fig06-vacuum-world-initial.png` | 13 | **SKIP** | The 2-cell vacuum world cells image. Superseded by `fig07` (the *full state-space graph*, slide 14) which is what we actually want students to look at — `fig07` is embedded as Figure 3. The slide-13 cell picture by itself only sets up the next slide. |
| 07 | `fig07-vacuum-world-state-space.png` | 14 | **USE** | Full state-space graph of the 2-cell vacuum world. Embedded as Figure 3 in §3.3 — worked example of "state space = directed graph". |
| 08 | `fig08-8-puzzle.png` | 15 | **SKIP** | 8-puzzle figure. The 8-puzzle is *named* in the chapter (§3.5 branching factor; common-pitfall mention) and we describe it verbally, but a dedicated figure is not necessary — the lecturer's point (state count is 9!/2 = 181,440) is captured better as a number than as a tile picture. Embedding it would inflate the chapter without aiding comprehension. |
| 09 | `fig09-3-puzzle-trace.png` | 16 | **SKIP** | 7-step move sequence on a 3-puzzle. Used in the slides to illustrate "solution = sequence of actions". The chapter conveys this idea both in §2.1 (maze analogy) and explicitly in §3.2 (path = sequence of actions). The 3-puzzle is a one-off example and adds little beyond what the Romania example already provides. |
| 10 | `fig10-building-goal-based-agents.png` | 17 | **SKIP** | Slide 17's "start tile → search-space cloud → goal tile" picture. The "search-space cloud" is a loose graphical metaphor that adds noise; the chapter explains the same idea precisely in §3.3 / §3.4. Embedding the slide would mix a precise text definition with a fuzzy bitmap. |
| 11 | `fig11-romania-route-graph.png` | 18 | **USE** | Romania graph with edge weights — the cleaner standalone version of `fig05`. Embedded as Figure 6 in §5.2. |
| 12 | `fig12-8-queens.png` | 19 | **SKIP** | Non-attacking 8-queens placement. The 8-queens problem is mentioned in the slides as an example of a "goal is a state property, not a path"; the chapter notes this in passing but does not develop n-queens here — it is the subject of Lecture 5 (local search). Embedding a chessboard would foreshadow material not yet covered. |
| 13 | `fig13-tree-search-diagram.png` | 20 | **USE** | Generic search-tree diagram. Embedded as Figure 4 in §3.4 as the anchor for the tree-search concept. |
| 14 | `fig14-tree-search-step1.png` | 22 | **USE** | Romania search tree, step 1 (Arad expanded). Embedded as Figure 7a in §5.2. |
| 15 | `fig15-tree-search-step2.png` | 23 | **SKIP** | Intermediate step of the Romania search-tree animation (Sibiu selected). Superseded by `fig17` (the *next* step where Sibiu is actually expanded), which **is** embedded as Figure 7b. Embedding both consecutive frames would be redundant. |
| 16 | `fig16-tree-search-step3-fringe.png` | 24 | **SKIP** | Frame between `fig15` and `fig17` showing the fringe outline at an earlier step. The frontier concept is illustrated by `fig18` (slide 26) — the version where the fringe is largest and the red dotted outline is unambiguous. We prefer that one. |
| 17 | `fig17-tree-search-step4.png` | 25 | **USE** | Romania search tree, step 4 (Sibiu expanded; four new children). Embedded as Figure 7b in §5.2. |
| 18 | `fig18-tree-search-step5-fringe.png` | 26 | **REWORK** | The same expanded tree with the red dotted "Fringe" outline. Embedded as Figure 7c in §5.2 and *accompanied* by a prose enumeration of the frontier set so the picture's visual point is also stated in text. |
| 19 | `fig19-bfs-step1.png` | 30 | **SKIP** | First frame of the BFS binary-tree animation. The animation runs from slide 30 to slide 34. We embed only **one** representative frame — `fig23` (the *final* frame on slide 34), which shows the most-expanded state of the tree — and supplement it with a tabular trace in §5.4 of the chapter. Embedding all five frames would inflate the chapter with near-duplicate images. |
| 20 | `fig20-bfs-step2.png` | 31 | **SKIP** | BFS animation frame 2. Same reason as `fig19`. |
| 21 | `fig21-bfs-step3.png` | 32 | **SKIP** | BFS animation frame 3. Same reason as `fig19`. |
| 22 | `fig22-bfs-step4.png` | 33 | **SKIP** | BFS animation frame 4. Same reason as `fig19`. |
| 23 | `fig23-bfs-step5.png` | 34 | **USE** | BFS animation final frame — chosen representative. Embedded as Figure 9 in §5.4. |
| 24 | `fig24-ucs-worked-example.png` | 37 | **USE** | UCS worked example: weighted directed graph with the 8-step trace. Embedded as Figure 8 in §5.3; the most exam-relevant figure in the lecture, supplemented by a step-by-step table in the chapter. |
| 25 | `fig25-dfs-step1.png` | 38 | **SKIP** | DFS animation frame 1. The DFS animation runs from slide 38 to slide 46 (nine frames). We embed only the **final** frame (`fig33`) plus a tabular trace, by the same logic as BFS. |
| 26 | `fig26-dfs-step2.png` | 39 | **SKIP** | DFS animation frame 2. Same reason as `fig25`. |
| 27 | `fig27-dfs-step3.png` | 40 | **SKIP** | DFS animation frame 3. Same reason as `fig25`. |
| 28 | `fig28-dfs-step4.png` | 41 | **SKIP** | DFS animation frame 4. Same reason as `fig25`. |
| 29 | `fig29-dfs-step5.png` | 42 | **SKIP** | DFS animation frame 5. Same reason as `fig25`. |
| 30 | `fig30-dfs-step6.png` | 43 | **SKIP** | DFS animation frame 6. Same reason as `fig25`. |
| 31 | `fig31-dfs-step7.png` | 44 | **SKIP** | DFS animation frame 7. Same reason as `fig25`. |
| 32 | `fig32-dfs-step8.png` | 45 | **SKIP** | DFS animation frame 8. Same reason as `fig25`. |
| 33 | `fig33-dfs-step9.png` | 46 | **USE** | DFS animation final frame — chosen representative. Embedded as Figure 10 in §5.5. |
| 34 | `fig34-ids-limit-0.png` | 49 | **SKIP** | IDS at depth limit 0 — a single node visited. Trivial enough to describe verbally; the chapter's §5.6 bullet "$\ell = 0$: only the root $A$ is visited" carries the full content. |
| 35 | `fig35-ids-limit-1.png` | 50 | **USE** | IDS at depth limit 1 — three frames showing A → B → C. Embedded as Figure 11 in §5.6. |
| 36 | `fig36-ids-limit-2.png` | 51 | **USE** | IDS at depth limit 2 — eight frames covering the full 7-node tree. Embedded as Figure 12 in §5.6. |
| 37 | `fig37-ids-limit-3.png` | 52 | **USE** | IDS at depth limit 3 — twelve frames on a 15-node tree. Embedded as Figure 13 in §5.6. |
| 38 | `fig38-comparison-table.png` | 54 | **USE** | The slide-54 comparison table. Embedded as Figure 5 in §4.5 with a typeset duplicate for cheat-sheet copy-pasting. |

## Image-extract catalogue (all SKIP)

Every embedded image picked up by `fitz.Pixmap(doc, xref)` either duplicates a region already captured by the page-render of the same slide, or is a tiny decorative item (the SDU logo on every slide, the puzzle-tile glyphs on slide 16, etc.). They are kept on disk for forensic completeness but **none are embedded in the chapter**.

| Seq | File | Slide | Verdict | Why not used |
|---|---|---|---|---|
| 39 | `fig39-page01-img1.png` | 1 | SKIP | SDU university logo bitmap. |
| 40 | `fig40-page02-img1.png` | 2 | SKIP | The maze drawing, cropped from the title slide; redundant with `fig01`. |
| 41 | `fig41-page03-img1.png` | 3 | SKIP | Joke meme bitmap; same content as `fig02`. |
| 42 | `fig42-page08-img1.png` | 8 | SKIP | SDU watermark. |
| 43 | `fig43-page10-img1.png` | 10 | SKIP | SDU watermark. |
| 44 | `fig44-page11-img1.png` | 11 | SKIP | Romania map (geographic) cropped — covered by page-render `fig11` (the version actually embedded). |
| 45 | `fig45-page11-img2.png` | 11 | SKIP | Romania weighted road graph cropped; redundant with `fig11`. |
| 46 | `fig46-page13-img1.png` | 13 | SKIP | Vacuum-world cells image. |
| 47 | `fig47-page14-img1.png` | 14 | SKIP | Vacuum-world state-space graph as a single embedded image — same as `fig07` minus the slide background; we keep `fig07`. |
| 48 | `fig48-page15-img1.png` | 15 | SKIP | 8-puzzle start state tiles only. |
| 49 | `fig49-page15-img2.png` | 15 | SKIP | 8-puzzle goal state tiles only. |
| 50 | `fig50-page15-img3.png` | 15 | SKIP | 8-puzzle three-successor diagram. |
| 51 | `fig51-page16-img18.png` | 16 | SKIP | Single 3-puzzle tile glyph. |
| 52 | `fig52-page16-img19.png` | 16 | SKIP | Single 3-puzzle tile glyph. |
| 53 | `fig53-page17-img1.png` | 17 | SKIP | 8-puzzle start tiles fragment. |
| 54 | `fig54-page17-img2.png` | 17 | SKIP | 8-puzzle goal tiles fragment. |
| 55 | `fig55-page17-img3.png` | 17 | SKIP | The "search space cloud" middle bitmap. |
| 56 | `fig56-page18-img1.png` | 18 | SKIP | Romania road graph standalone; covered by `fig11`. |
| 57 | `fig57-page19-img1.png` | 19 | SKIP | 8-queens chessboard. |
| 58 | `fig58-page22-img1.png` | 22 | SKIP | Search-tree bitmap without the slide's annotations. |
| 59 | `fig59-page22-img2.png` | 22 | SKIP | Romania road graph cropped. |
| 60–67 | `fig60..fig67` | 23–26 | SKIP | The same tree-and-graph pair repeating across slides 23/24/25/26; the slide-level annotation (which node is being expanded / the red Fringe outline) lives on the page, not in the embedded image — so we keep the page-renders only. |
| 68 | `fig68-page37-img1.png` | 37 | SKIP | The UCS graph (nodes A–G with edge weights), no step-trace; the page-render `fig24` already includes the trace beside the graph. |
| 69–71 | `fig69..fig71` | 50–52 | SKIP | The IDS frame strips as one embedded image per slide; we kept the page-renders (`fig35`–`fig37`) so caption-style row labels remain visible. |
| 72–73 | `fig72..fig73` | 54 | SKIP | Two image fragments of the comparison table; covered by `fig38`. |

## Summary

- 73 figures in this directory in total.
- **15 USE/REWORK figures embedded** in the chapter `.md` (page-renders only).
  - USE: `fig03`, `fig04`, `fig07`, `fig11`, `fig13`, `fig14`, `fig17`, `fig23`, `fig24`, `fig33`, `fig35`, `fig36`, `fig37`, `fig38`.
  - REWORK: `fig18` (embedded with accompanying prose enumeration of the frontier set).
- **58 SKIP** figures with explicit justification (decoration, duplicates, mid-animation frames superseded by the final/representative frame chosen for embedding).
- **No informative figure from the source PDF is dropped silently.** Every slide that carries a non-trivial diagram is either (a) embedded directly, (b) embedded via a representative frame of a multi-slide animation with all other frames flagged in this catalogue as superseded, or (c) reproduced as a typeset table / prose paragraph in the chapter when the slide content is best communicated that way.

## Reproducing this extraction

```
py -3.12 study/extracted_figures/L03/_extract.py
```

Outputs PNGs + `_inventory.txt` into this directory. Idempotent — re-running overwrites in place.

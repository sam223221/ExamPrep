# L06 — Adversarial Search — Figure Catalogue

Source PDF: `Lecture6-Adversarial Search.pdf` (42 slides).

Extraction performed with PyMuPDF (`fitz`) v1.24.9.

Two pools of files live in this directory:

1. **`fig_pNN_imgM.{png|jpg}`** — embedded images lifted by
   `page.get_images()` + `doc.extract_image()`. One entry per embedded image
   per page.
2. **`pageNN-render.png`** — whole-slide page renders at DPI 200 produced by
   `page.get_pixmap(dpi=200)`. Used as a fallback when the lecture slide is a
   *composite* (text + diagram + labels combined by the slide editor rather
   than embedded as a single image). Tagged `EXTRACTION_METHOD: page-render`.

The chapter `study/lectures/L06-Adversarial-Search.md` embeds the
`pageNN-render.png` variants for every diagram-heavy slide because the
embedded images alone (e.g. `fig_p11_img1.png`) carry the diagram drawn by
the slide author but lose the surrounding labels (`α=3`, `prune!`,
`Minmax values`, etc.) that are rendered on top of it by the slide editor.

Verdict legend:

- **USE** — embed in chapter as-is.
- **REWORK** — embed alongside a Mermaid / prose backup because the image
  alone is unclear or context-dependent.
- **SKIP** — decorative or redundant; never embedded.

---

## Embedded-image catalogue (`fig_*`)

| Filename | Source page | Surrounding text / caption | Verdict | Rationale |
|---|---|---|---|---|
| `fig_p01_img1.png` (290×161) | 1 — Title slide "Adversarial Search / Serkan Ayvaz" | (no caption — title-slide ornament) | SKIP | Decorative title-slide background block; carries no instructional content. |
| `fig_p02_img1.jpeg` (442×369) | 2 — "Games and adversarial search" header | Photo of Claude Shannon at a chess board (1949 era). | SKIP | Historical photo only. Slide 41 names Shannon as the originator of evaluation-function chess play; we cite him there in prose without re-using the photo. |
| `fig_p02_img2.jpeg` (442×369) | 2 — same header | Photo of Garry Kasparov vs Deep Blue (1997 era). | SKIP | Historical photo only. Slide 40 mentions Deep Blue's 1997 win; we cite it in prose. |
| `fig_p08_img1.png` (635×452) | 8 — "Game tree" — tic-tac-toe between MAX(X) and MIN(O) | Russell & Norvig classic tic-tac-toe game tree showing MAX (X) at root, branching into nine MIN (O) replies, deepening to a TERMINAL row with utilities −1, 0, +1. | USE | This is THE canonical illustration of a game tree. Embedded directly under §3.2 "Game tree". |
| `fig_p09_img1.png` (740×906) | 9 — "http://xkcd.com/832/" | xkcd comic "Tic-Tac-Toe" — exhaustive optimal-play decision chart. | REWORK | The comic is instructive (it IS the complete minimax solution of tic-tac-toe for the X-player), but at 740×906 it is too dense to read at chapter scale. We embed a small reference image and tell the student to open the xkcd link if they want to study the decision chart in full. |
| `fig_p10_img1.png` (740×772) | 10 — same xkcd reference | The O-player half of the xkcd "Tic-Tac-Toe" comic. | REWORK | Same rationale as `fig_p09`. Referenced once in §3.2; not re-shown. |
| `fig_p11_img1.png` (1747×772) | 11 — "A more abstract game tree" | The abstract game tree used as the running minimax example: leaves 3,12,8,2,4,6,14,5,2 under three MIN nodes B/C/D under root A. | USE | The single most-referenced diagram of the lecture. We embed it via the page-render `page11-render.png` which keeps the "Minmax values 3, 3, 2, 2" red overlays the slide editor draws on top of this image. The raw `fig_p11_img1` (without overlays) is also kept here as the bare tree. |
| `fig_p12_img1.png` … `fig_p15_img1.png` | 12–15 | Same image as `fig_p11_img1` re-used on every slide of §3.3 (build-up of minimax across four slides). | SKIP (duplicate) | Byte-identical to `fig_p11_img1.png`. Kept in this directory for traceability but not re-embedded. The build-up across slides 11→12→13→14→15 is captured by re-using `page11-render.png` (slide 11 = final minimax-values frame). |
| `fig_p16_img1.jpeg` (1432×1080) | 16 — "Example — Coins game" | Stock photo of stacks of coins. | SKIP | Decorative; the Coins-game rules on the slide are textual. |
| `fig_p17_img1.jpeg` (1198×904) | 17 — "Coins Game: Formal Definition" | Same/similar stock coin photo as `fig_p16`. | SKIP | Decorative. |
| `fig_p23_img1.png` (720×324) | 23 — first frame of the alpha-beta worked example | Same abstract-tree shape as `fig_p11` but redrawn larger, with no values yet labelled on the internal nodes — the slide author then animates labels across slides 24–28. | USE (via page-render) | We embed `page23-render.png` through `page28-render.png` as the build-up frames; the alpha-beta sweep is meaningless without the per-frame label overlays. |
| `fig_p24_img1.png` … `fig_p28_img1.png` | 24–28 | Same base image as `fig_p23_img1`. The labels (`3`, `≤2`, `3`, `2`, `14`, `5`, `2`, `≤2` etc.) are drawn ON TOP OF this image by the slide editor; the embedded image itself is unchanged across the five frames. | SKIP (duplicate) | Byte-identical to `fig_p23_img1.png`. The five animated frames live in `page23-render.png` through `page28-render.png`. |
| `fig_p34_img1.png` (758×103) | 34 — Alpha-Beta Tic-Tac-Toe Example | A thin caption strip ("Discontinue search below a MIN node whose beta value ≤ alpha value of one of its MAX ancestors"). | SKIP | A label strip; the same text is reproduced in §4.2 of the chapter. |
| `fig_p34_img2.png` (775×108) | 34 — same | Another caption strip from the same slide. | SKIP | Same rationale. |
| `fig_p37_img1.jpeg` (800×533) | 37 — "Games of chance" | Photo of a backgammon board with dice. | SKIP | Decorative; backgammon is discussed in prose in §4.6 / §4.7. |
| `fig_p38_img1.png` (851×683) | 38 — Games of chance — diagram | Game tree with explicit CHANCE nodes between MAX and MIN levels — illustrates expectiminimax structure. | USE (via page-render) | Embedded as `page38-render.png` because the embedded `fig_p38_img1.png` is missing the level labels ("MAX", "CHANCE", "MIN", "TERMINAL", "1/36", "1/18" etc.) which are critical to reading the diagram. |

## Whole-slide renders (`pageNN-render.png`)

These are 200-DPI rasters of the full slide, taken with
`fitz.Page.get_pixmap(dpi=200)`. Used because the slide author composed
several elements (text + arrows + colored boxes + labels) on top of an
embedded image; capturing just the embedded image would lose the labels.

| Filename | Source slide | What it shows | Used where in chapter |
|---|---|---|---|
| `page05-render.png` | 5 | The 2×2 game-environment taxonomy table (Deterministic vs Stochastic × Perfect vs Imperfect information). | §3.1 — game environments. |
| `page08-render.png` | 8 | Tic-tac-toe game tree, full slide with MAX(X) / MIN(O) labels. | §3.2 — game tree. |
| `page11-render.png` | 11 | Abstract game tree with MAX root A, MIN children B/C/D, leaves 3,12,8,2,4,6,14,5,2, with red "Minmax values" overlay 3/3/2/2 on the internal nodes. | §3.3 — minimax value (running example). |
| `page18-render.png` | 18 | Complete coin-game tree for N=4: MAX root (yellow), MIN children (red), F(S) utility leaves. | §5.1 — Coins-game worked example. |
| `page20-render.png` | 20 | First introduction of α and β with a small 4-leaf example: leaves 2, 7, 1, ?, β:2, β:1, α:2, and the call-out "We don't need to compute the value at this node". | §4.1 — alpha-beta motivation. |
| `page22-render.png` | 22 | The alpha-beta rule slide: DFS order, alpha at MAX nodes, beta at MIN nodes, beta-cutoff / alpha-cutoff conditions, with a small tree on the right. | §4.2 — alpha-beta rules. |
| `page23-render.png` to `page28-render.png` | 23–28 | Six-frame animation of alpha-beta running on the 9-leaf abstract tree (same as slide 11). Frame 23: bare tree. Frame 24: leftmost MIN ← 3. Frame 25: middle MIN sees a 2. Frame 26: middle MIN has 14 (would be β). Frame 27: 5. Frame 28: final state — root MAX=3, left MIN=3, middle MIN ≤ 2 (pruned), right MIN = 2. | §5.2 — full alpha-beta walkthrough. |
| `page29-render.png` to `page34-render.png` | 29–34 | Six-frame animation of alpha-beta on a depth-2 tic-tac-toe tree with evaluation function "X's open lines − O's open lines"; leaves 2, 1, −1; root α=1, right-MIN β=−1 triggers an alpha cutoff. | §5.3 — alpha-beta + evaluation function worked example. |
| `page35-render.png` | 35 | Same 9-leaf abstract tree as slide 11, now with the alpha-beta result annotated: α=3 root, β=3 left, β=2 middle "prune!", β=1 right "prune!". | §5.2 — summary frame of the alpha-beta walkthrough. |
| `page38-render.png` | 38 | Expectiminimax game tree showing alternating MAX / CHANCE / MIN / CHANCE / MAX / TERMINAL levels with branch probabilities (1/36, 1/18, ...) and dice-roll labels (1,1; 1,2; 6,5; 6,6). | §4.6 — games of chance (expectiminimax). |

`EXTRACTION_METHOD` for every `pageNN-render.png` is **`page-render`**.

---

## Coverage statement

Every slide that contains a non-decorative diagram (slides 5, 8, 11–15, 18, 20, 22, 23–28, 29–34, 35, 38) is represented either by an embedded image (USE) or by a page-render (which I use whenever the slide carries label overlays). Slides without diagrams (1 title, 2 header, 3 environment text, 4 motivation text, 6 zero-sum text, 7 branching-factor text, 13–17 text/numbers, 19 analysis text, 21 alpha-beta text rules, 36 additional-techniques text, 37 chance-games header, 39 chance-games text, 40 game-playing-today text, 41 origins text, 42 thank-you) are covered by prose in the chapter and do not need an image. Decorative photos (Shannon, Kasparov, coin stacks, backgammon board) are SKIPped with rationale above.

No informative figure has been silently dropped.

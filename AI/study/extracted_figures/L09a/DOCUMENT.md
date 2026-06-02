# `study/extracted_figures/L09a/` — L09a Bayesian Networks figure cache

This directory holds every image extracted from `Lecture9-Bayesian Networks.pdf` plus a `figures.md` catalogue with per-image USE/REWORK/SKIP verdicts.

## Contents

- **16 raster images** (`fig{NN}-xref{X}-slide{S}.{ext}`) — bitmap images embedded in the PowerPoint deck (decorative photos, the Bayes portrait, slide ornaments). All but `fig15-xref215-slide63.jpeg` (the real-world BN diagram) are SKIP.
- **28 page renders** (`page{SS}-{slug}.png`) — composite slides (DAG nodes + vector text + tables) rendered as PNG at 200 dpi. 26 are USE; 2 are SKIP because their content is redundant or covered inline.
- **`figures.md`** — the per-image catalogue. Reviewers must consult this file before deciding to add or remove a figure from the chapter.

## Round 1 revision notes (2026-05-22)

- All four USE-marked figures previously flagged as missing from the chapter (`page08-atomic-events.png`, `page33-anthrax-bn.png`, `page34-joint-table-2k.png`, `page55-compute-joint-entry-example.png`) are now embedded in `study/lectures/L09a-Bayesian-Networks.md`.
- `figures.md`'s P20 SKIP rationale for `page48-alarm-network-clean.png` has been updated to explain that the slide's unique content (factorisation formula + sample joint $P(+b, \neg e, +a, \neg j, +m)$) is reproduced inline in the chapter (§3.10 and §5.6), not omitted.
- The summary block in `figures.md` now correctly accounts for the one REWORK image (fig09, absorbed by page-render P7) and the corrected SKIP count.

## How to add a new figure

1. Add the image file to this directory (use the existing naming convention).
2. Add a row to `figures.md` with verdict USE/REWORK/SKIP and rationale.
3. Embed (or not) in `study/lectures/L09a-Bayesian-Networks.md` with a `_Figure 9.NN:_` caption.
4. Renumber any downstream figures whose numbers shift.

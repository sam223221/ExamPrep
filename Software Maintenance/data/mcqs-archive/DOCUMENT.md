# DOCUMENT.md — `data/mcqs-archive/`

## What lives here

The **full original MCQ bank** — all 20 lecture JSON files (set-1
`lecture-NN-<slug>.json`, 2,337 direct-recall questions + set-2
`lecture-NN-<slug>-v2.json`, 2,000 perspective-shifted questions, IDs offset at
`LNN-Q501`) totalling **4,337 questions**. Archived **losslessly** on 2026-06-10
when the live bank in `data/mcqs/` was reduced to a 500-question curated
selection: the files were moved here byte-identically (`Move-Item`, no
re-serialization), including the 2026-06-10 Capers Jones corrections to L01.

Per-file counts: L01 149+130, L02 252+220, L03 252+220, L04 261+230, L05 274+230,
L06 300+250, L07 291+250, L09 175+150, L10 199+170, L11 184+150 (set-1 + set-2).

This folder is **outside** the quiz loader's `data/mcqs/*.json` glob and is never
loaded or validated by the app. It is reference/restore material only.

## How to restore the full bank

1. Delete the 10 curated `lecture-*.json` files in `data/mcqs/` (they are pure
   subsets of this archive — every question exists here byte-identically, so
   nothing is lost).
2. Move all 20 JSON files from this folder back:
   `Move-Item data\mcqs-archive\lecture-*.json data\mcqs\`
3. Re-run the gate: `python -m app.validate_mcqs data\mcqs` → expect
   "MCQ validation OK — 20 file(s) valid."
4. Restart the app so the quiz loader re-reads the glob.

Do **not** copy the archive in alongside the curated files — the curated files
reuse the same question IDs and stems, so the validator (globally unique IDs, no
duplicate stems) will fail until the curated files are removed.

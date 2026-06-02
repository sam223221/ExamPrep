# `src/components/hmm` — HMM tab UI

React UI for the Hidden Markov Model tab. Renders editors for the model and
displays Forward / Viterbi results. **No probability logic lives here** — all
math is delegated to `src/lib/hmm`.

## Files

- **`Hmm.tsx`** — the tab orchestrator (default export, no props). Owns editable
  model state (states, symbols, π, optional end, transition `A`, emission `B`)
  and the observation-sequence string. Buttons: **Run Forward**, **Run
  Viterbi**, **Load Lab 8 ice-cream example**, **Clear**. Validates the model
  via `validateModel` and the sequence via `symbolsToIndices` before running;
  surfaces problems in an inline alert. Calls `forward` / `viterbi` and feeds the
  result to `TrellisTable`.
- **`MatrixEditor.tsx`** — reusable, controlled, accessible numeric grid with
  row/column headers. Optional per-row sum validation (`rowSumTarget`) with the
  current sum shown and off-target rows highlighted. `extraRowWeight` lets the
  transition matrix validate `row + end[i] = 1`. Inputs clamp to `[0, 1]`.
- **`TrellisTable.tsx`** — presentational DP table (states × timesteps). Used for
  the α table (Forward), and the δ + backpointer tables (Viterbi). `pathIndices`
  highlights the recovered best-path cell in each column. Tiny probabilities are
  shown in scientific notation.

## Key decisions

- The Lab 8 preset includes an explicit `end = [0.2, 0.2]`; the "Use explicit end
  probabilities" checkbox toggles between that and textbook Forward (end = 1).
- Resizing the states/symbols lists preserves overlapping matrix/vector cells and
  fills new ones with 0, so editing never silently corrupts existing values.
- Results are computed only on button press (not live) so the user can edit a
  full model before running; validation messaging is live.

## Styling

Uses the shell's design tokens (`bg-surface`, `border-border`, `text-ink`,
`text-accent`, etc.) and the mono font for all numbers. Responsive two-column
panels collapse to one column on narrow widths.

## Connections

Imported by `src/App.tsx` as the `hmm` tab panel (the shell is owned by the
setup phase and is not modified here).

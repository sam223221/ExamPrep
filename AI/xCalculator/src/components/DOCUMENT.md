# DOCUMENT — src/components/

UI components. `Tabs.tsx` is the finished, fixed tab bar. Each of the four study modules
lives in its own subdirectory with a default-exported root component; all four are now fully
implemented. Supporting components are documented in each subdirectory's own `DOCUMENT.md`.

## Files in this directory

| File / dir                       | Purpose                                                                            |
| -------------------------------- | ---------------------------------------------------------------------------------- |
| `Tabs.tsx`                       | Accessible tab bar (ARIA `tablist`/`tab`, arrow/Home/End keyboard nav). Reports selection to `App`. Finished — do not modify in feature phases. |
| `calculator/Calculator.tsx`      | Button-grid + keyboard arithmetic calculator with session history. Evaluates via `lib/calc.ts`; errors surface inline. Default export, no props. |
| `probability/Probability.tsx`    | Probability module: Combinatorics, Probability rules, and Bayes' theorem sections, each a live form over `lib/probability.ts`. Default export, no props. |
| `bayes/BayesNetwork.tsx`         | Bayesian-network editor: a React Flow (`@xyflow/react`) DAG canvas with editable per-node CPTs, import/export, and a live query panel. Inference via `lib/bayes`. Default export, no props. |
| `hmm/Hmm.tsx`                    | HMM module: editable model + observation sequence, running Forward (P(O) + α trellis) and Viterbi (best path + δ/backpointer tables) via `lib/hmm`. Default export, no props. |
| `DOCUMENT.md`                    | This file.                                                                          |

## Subdirectory contents

Each module subdirectory contains its root component plus any supporting components, and its
own `DOCUMENT.md` describing them in detail:

- **`calculator/`** — `Calculator.tsx`.
- **`probability/`** — `Probability.tsx` (the three sections are internal sub-components in
  the same file).
- **`bayes/`** — `BayesNetwork.tsx` (orchestrator), `BayesNode.tsx` (custom React Flow node:
  name/state editing + embedded CPT editor and connection handles), `CptTable.tsx` (editable
  conditional probability table with per-row sum check + normalize), `QueryPanel.tsx` (query
  variable + evidence pickers showing `P(query | evidence)`).
- **`hmm/`** — `Hmm.tsx` (orchestrator), `MatrixEditor.tsx` (reusable labelled numeric grid
  with optional per-row sum validation), `TrellisTable.tsx` (states × timesteps DP table for
  the α / δ / backpointer trellises, with best-path highlighting).

## Component contract

Every module root component is a default-exported function component with no required props
(e.g. `export default function Calculator() { ... }`). `App.tsx` imports them by the paths
above and renders the active one. Each module owns its subdirectory; all math is delegated to
the framework-free modules under `src/lib/**`, so components hold presentation and input
handling only. `Tabs.tsx` is the shell's tab bar and must not be modified in feature phases.

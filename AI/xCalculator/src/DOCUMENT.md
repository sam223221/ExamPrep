# DOCUMENT — src/

The React renderer. The app shell (`App.tsx` + `components/Tabs.tsx`) is finished and fixed;
feature engineers fill in the module components under `components/**` and algorithm modules
under `lib/**` (added in later phases).

## Files in this directory

| File         | Purpose                                                                                          |
| ------------ | ------------------------------------------------------------------------------------------------ |
| `main.tsx`   | React entry. Mounts `<App />` into `#root` inside `<StrictMode>` and imports `index.css`.         |
| `App.tsx`    | App shell: owns active-tab state, renders the header, `<Tabs>`, and the active module panel.      |
| `index.css`  | Tailwind v4 import (`@import "tailwindcss";`) plus theme tokens defined with `@theme`.            |
| `DOCUMENT.md`| This file.                                                                                       |

## Tab contract (relied on by feature agents)

`App.tsx` imports each module by these exact paths and renders the active one by tab id:

- `./components/calculator/Calculator` (id `calculator`, label "Calculator")
- `./components/probability/Probability` (id `probability`, label "Probability")
- `./components/bayes/BayesNetwork` (id `bayes`, label "Bayesian Network")
- `./components/hmm/Hmm` (id `hmm`, label "HMM")

Each is a **default-exported** React function component with **no required props**. Feature
agents replace only the inner module components — never `App.tsx` or `components/Tabs.tsx`.

## Algorithm modules — `lib/`

`src/lib/` exists and is populated. Algorithm modules live there framework-free so they stay
independently testable; the UI components import them and contain no math logic:

- `calc.ts` — safe arithmetic evaluator (shunting-yard, no `eval`).
- `probability.ts` — combinatorics and probability rules (incl. Bayes' theorem).
- `bayes/` — discrete Bayesian-network types and exact inference by enumeration.
- `hmm/` — Hidden Markov Model types plus the Forward and Viterbi algorithms.
- `__tests__/` — Vitest specs for all of the above.

Vitest is configured in `vite.config.ts` to pick up `src/**/__tests__/**/*.{test,spec}.ts`.
See `src/lib/DOCUMENT.md` (and the per-subdirectory `DOCUMENT.md` files) for details.

# xCalculator

A desktop study tool for an AI university exam. It bundles four calculators behind a single
offline app, built with React + Vite + TypeScript, wrapped in Electron, and packaged as a
portable Windows `.exe` (double-click, no install, runs offline).

## The four tabs

- **Calculator** — arithmetic calculator backed by a safe shunting-yard expression parser (no `eval`).
- **Probability** — combinatorics (`n!`, `nPr`, `nCr`), probability rules, and Bayes' theorem.
- **Bayesian Network** — visual editor (drag-to-connect nodes, editable CPTs) with exact inference by enumeration.
- **HMM** — Hidden Markov Model calculator: Forward (P(O) + α trellis) and Viterbi (best path + δ/backpointer tables).

## Prerequisites

- **Node.js** (LTS, v20+ recommended). Required only to develop and build.
- Windows is the packaging target; development works on any OS Node supports.

## Setup

```bash
npm install
```

## Run

```bash
# Launch the app in an Electron window with Vite hot reload.
npm run dev

# Type-check the renderer and build the renderer + Electron bundles.
npm run build

# Type-check only (no emit).
npm run typecheck

# Run the unit tests (math modules).
npm run test

# Build, then package a portable Windows executable.
npm run dist
```

`npm run dist` produces `release/xCalculator.exe` — a single portable executable
(~100–150 MB; it bundles Chromium), double-clickable and fully offline. Building the
`.exe` requires Node and downloads Electron binaries on first run.

## Project structure

```
xCalculator/
  index.html              # Vite entry (renderer)
  vite.config.ts          # React + Tailwind v4 + vite-plugin-electron; base: './'
  electron-builder.yml    # Windows portable target -> release/xCalculator.exe
  electron/
    main.ts               # BrowserWindow; hardened webPreferences
    preload.ts            # minimal/empty
  src/
    main.tsx              # React root render
    App.tsx               # tab shell + active-tab state
    index.css             # Tailwind import + theme tokens
    components/
      Tabs.tsx            # accessible tab bar
      calculator/         # Calculator module
      probability/        # Probability module
      bayes/              # Bayesian-network module
      hmm/                # HMM module
    lib/                  # framework-free algorithm modules (added by feature engineers)
```

## Architecture overview

All algorithms live in framework-free TypeScript modules under `src/lib/`. UI components
call into these modules but contain no probability logic, which keeps every algorithm
independently testable with Vitest.

The desktop shell is Electron. The renderer is a normal Vite single-page app; in development
it loads the Vite dev server, and in a packaged build it loads `dist/index.html` over
`file://` (hence `base: './'` in `vite.config.ts`). The renderer is sandboxed with
`contextIsolation: true`, `nodeIntegration: false`, and `sandbox: true`; the preload exposes
no privileged APIs. The app makes no network calls.

## Tech stack

| Concern        | Choice                                  |
| -------------- | --------------------------------------- |
| UI             | React 18 + TypeScript                   |
| Build          | Vite 7 + `@vitejs/plugin-react`         |
| Styling        | Tailwind CSS v4 (`@tailwindcss/vite`)   |
| Graph editor   | React Flow (`@xyflow/react` v12)        |
| Desktop shell  | Electron + `vite-plugin-electron`       |
| Packaging      | `electron-builder` (Windows portable)   |
| Tests          | Vitest                                  |

# DOCUMENT — xCalculator (project root)

Scaffold for the xCalculator desktop study app (React + Vite + TypeScript + Electron,
packaged as a portable Windows `.exe`). This directory holds project configuration and the
entry HTML; application code lives under `src/` and the Electron shell under `electron/`.

## Files in this directory

| File                   | Purpose                                                                                  |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| `package.json`         | Dependencies and scripts (`dev`, `build`, `typecheck`, `test`, `dist`). `main` points at `dist-electron/main.js`. |
| `tsconfig.json`        | Solution-style root config: references `tsconfig.app.json` and `tsconfig.node.json` (built with `tsc -b`). |
| `tsconfig.app.json`    | TypeScript config for the renderer (`src/`): DOM libs, React JSX, strict mode, composite. |
| `tsconfig.node.json`   | TypeScript config for Node-side code (`vite.config.ts`, `electron/`): Node types, composite. |
| `vite.config.ts`       | Vite config: `@vitejs/plugin-react`, `@tailwindcss/vite`, `vite-plugin-electron`; `base: './'`; Vitest `test` block. |
| `electron-builder.yml` | Packaging config: Windows `portable` x64 target -> `release/xCalculator.exe`; `asar: true`. |
| `index.html`           | Vite renderer entry; includes a strict Content-Security-Policy meta tag.                 |
| `.gitignore`           | Ignores `node_modules`, build output (`dist`, `dist-electron`, `release`, `out`), caches, `*.local`. |
| `README.md`            | Project summary, the four tabs, prerequisites, run/build commands, architecture.         |
| `DOCUMENT.md`          | This file.                                                                               |

## Key decisions

- **React 18.3.1** (spec's safe default). `@xyflow/react` v12 peers `react >= 17`, so 18 is fully supported.
- **Vite 7.3.5** with **`vite-plugin-electron` 0.29.1** — the proven stable pairing; the flat
  project layout uses the plugin's `simple` API (`electron/main.ts` + `electron/preload.ts`).
  (Vite 8 + `vite-plugin-electron` 1.0.0 is bleeding-edge and was deliberately avoided.)
- **Tailwind CSS v4** via `@tailwindcss/vite`; no `tailwind.config.js` — tokens defined with `@theme` in `src/index.css`.
- **Solution-style tsconfigs** (`tsconfig.json` references `tsconfig.app.json` + `tsconfig.node.json`, built via `tsc -b`) cleanly separate DOM-typed renderer code from Node-typed build/Electron code.

## How it connects

`npm run dev` starts Vite; `vite-plugin-electron` builds the Electron bundles and launches
Electron, which loads the Vite dev server. `npm run build` type-checks and emits `dist/`
(renderer) + `dist-electron/` (main + preload). `npm run dist` then runs `electron-builder`
to package `release/xCalculator.exe`.

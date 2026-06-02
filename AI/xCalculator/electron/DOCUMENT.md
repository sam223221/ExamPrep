# DOCUMENT — electron/

The Electron desktop shell. These files are bundled by `vite-plugin-electron` into
`dist-electron/` and are the main + preload processes that wrap the React renderer.

## Files in this directory

| File         | Purpose                                                                                       |
| ------------ | --------------------------------------------------------------------------------------------- |
| `main.ts`    | Electron main process. Creates the `BrowserWindow`, loads the Vite dev server in development and `dist/index.html` over `file://` in production. |
| `preload.ts` | Minimal preload. Exposes no APIs to the renderer (empty by design) to preserve the security boundary. |
| `DOCUMENT.md`| This file.                                                                                    |

## Security posture

`main.ts` hardens the window: `contextIsolation: true`, `nodeIntegration: false`,
`sandbox: true`, `webSecurity: true`. External links are opened in the system browser
(`setWindowOpenHandler` denies in-app windows); in-app navigation away from the bundled
renderer is blocked (`will-navigate`). No remote content is loaded.

## How it connects

- `vite.config.ts` wires `main.ts` (→ `dist-electron/main.js`) and `preload.ts`
  (→ `dist-electron/preload.mjs`) via the plugin's `simple` API.
- `package.json`'s `main` field points at `dist-electron/main.js`.
- In dev, `main.ts` reads `process.env.VITE_DEV_SERVER_URL` (injected by the plugin) to load
  the live renderer; otherwise it loads the built `dist/index.html`.

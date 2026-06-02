import { app, BrowserWindow, shell } from 'electron';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// vite-plugin-electron injects this in dev; it is undefined in a packaged build.
const VITE_DEV_SERVER_URL = process.env.VITE_DEV_SERVER_URL;

// Built renderer lives in dist/, sibling to this file's dist-electron/ output.
const RENDERER_DIST = path.join(__dirname, '../dist');
const PRELOAD_PATH = path.join(__dirname, 'preload.mjs');

let mainWindow: BrowserWindow | null = null;

function createWindow(): void {
  mainWindow = new BrowserWindow({
    width: 1180,
    height: 820,
    minWidth: 900,
    minHeight: 640,
    backgroundColor: '#0b0f17',
    show: false,
    title: 'xCalculator',
    webPreferences: {
      preload: PRELOAD_PATH,
      // Security hardening: renderer has no Node access and runs sandboxed.
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      webSecurity: true,
    },
  });

  mainWindow.once('ready-to-show', () => {
    mainWindow?.show();
  });

  // Open any external link in the user's browser instead of inside the app.
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    void shell.openExternal(url);
    return { action: 'deny' };
  });

  // Block in-app navigation away from the bundled renderer.
  mainWindow.webContents.on('will-navigate', (event, url) => {
    const allowed = VITE_DEV_SERVER_URL ?? '';
    if (allowed && url.startsWith(allowed)) return;
    event.preventDefault();
  });

  if (VITE_DEV_SERVER_URL) {
    void mainWindow.loadURL(VITE_DEV_SERVER_URL);
  } else {
    void mainWindow.loadFile(path.join(RENDERER_DIST, 'index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

/// <reference types="vitest/config" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import electron from 'vite-plugin-electron/simple';

// Relative base so the packaged app loads renderer assets over file:// inside Electron.
export default defineConfig({
  base: './',
  plugins: [
    react(),
    tailwindcss(),
    electron({
      main: {
        // Electron main process entry; bundled to dist-electron/main.js.
        entry: 'electron/main.ts',
      },
      preload: {
        // Preload script; bundled to dist-electron/preload.mjs.
        input: 'electron/preload.ts',
      },
      // No Node.js APIs are exposed to the renderer; it stays a plain web context.
      renderer: undefined,
    }),
  ],
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
  test: {
    globals: true,
    environment: 'node',
    include: ['src/**/__tests__/**/*.{test,spec}.ts'],
    // Scaffold has no specs yet; feature engineers add them. Avoids a false
    // failure when the suite is run before any test file exists.
    passWithNoTests: true,
  },
});

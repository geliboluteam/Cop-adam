import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'node:path';

// The lab: the episode's shots + a sound engine in the browser, for trying the mix by hand.
//   npm run lab      -> http://localhost:3440
// It reuses the studio's src/ and its public/ (fonts, wavs), so there is nothing to copy.
export default defineConfig({
  root: resolve(__dirname, 'lab'),
  publicDir: resolve(__dirname, 'public'),
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3440,
    strictPort: true,
    allowedHosts: true,
  },
  optimizeDeps: { include: ['react', 'react-dom'] },
});

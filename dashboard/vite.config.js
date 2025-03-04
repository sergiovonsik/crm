import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/', // Ensures correct path resolution
  build: {
    outDir: 'build', // Make sure it's named 'build' for Render
  },
  server: {
    historyApiFallback: true,
  },
});

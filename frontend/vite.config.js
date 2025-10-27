import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Configurazione ottimizzata per applicazione desktop Electron
export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    rollupOptions: {
      output: {
        manualChunks: undefined
      }
    }
  }
})

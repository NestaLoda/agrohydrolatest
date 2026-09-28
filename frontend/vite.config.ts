import { defineConfig } from 'vite'

export default defineConfig({
  server: { port: 5173, strictPort: true, proxy: { '/api': 'http://127.0.0.1:8000' } },
  preview: { port: 4173 },
  worker: { format: 'es' },
  build: { chunkSizeWarningLimit: 1600 },
})

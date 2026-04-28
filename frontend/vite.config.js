import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Proxy API calls to FastAPI during development
      '/auth':         { target: 'http://localhost:8000', changeOrigin: true },
      '/upload':       { target: 'http://localhost:8000', changeOrigin: true },
      '/results':      { target: 'http://localhost:8000', changeOrigin: true },
      '/compare':      { target: 'http://localhost:8000', changeOrigin: true },
      '/uploads':      { target: 'http://localhost:8000', changeOrigin: true },
      '/dataset_media':{ target: 'http://localhost:8000', changeOrigin: true },
      '/health':       { target: 'http://localhost:8000', changeOrigin: true },
    },
  },
})

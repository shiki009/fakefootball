import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5174,
    allowedHosts: ['localhost', '.ngrok-free.dev', '.ngrok.io', '.trycloudflare.com', '.loca.lt'],
    proxy: {
      '/api': 'http://localhost:8001',
    },
  },
})

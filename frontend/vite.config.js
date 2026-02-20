import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000, // ton port local
    strictPort: true,
    host: true,
    // Autoriser le domaine ngrok
    allowedHosts: ['devastatingly-nonasbestine-amelie.ngrok-free.dev']
  }
})
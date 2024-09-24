import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: "0.0.0.0",
    proxy: {
      "/api": {
        target: "http://localhost:8008", // 你的FastAPI后端地址
        changeOrigin: true,
        // 不需要 rewrite 配置，因为前后端路径一致
      },
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vue: ['vue', 'vue-router', 'pinia'],
          crypto: ['crypto-js'],
        },
      },
    },
  },
});

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: "0.0.0.0",
    proxy: {
      "/api": {
        target: "http://localhost:8000", // 你的FastAPI后端地址
        changeOrigin: true,
        // 不需要 rewrite 配置，因为前后端路径一致
      },
    },
  },
});

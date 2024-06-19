import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import legacy from '@vitejs/plugin-legacy';
import ViteCompression from 'vite-plugin-compression';
import ViteComponents from 'unplugin-vue-components/vite';
import { AntDesignVueResolver } from 'unplugin-vue-components/resolvers';
import { EleAdminResolver, styleDeps } from 'ele-admin-pro/lib/utils/resolvers';
import { DynamicAntdLess } from 'ele-admin-pro/lib/utils/dynamic-theme';
import { resolve } from 'path';

export default defineConfig(({ command }) => {
  const isBuild = command === 'build';
  return {
    resolve: {
      alias: {
        '@/': resolve(__dirname, 'src') + '/',
        'vue-i18n': 'vue-i18n/dist/vue-i18n.cjs.js'
      }
    },
    plugins: [
      vue(),
      // 组件按需引入
      ViteComponents({
        dts: false,
        resolvers: [
          AntDesignVueResolver({
            importStyle: 'less'
          }),
          EleAdminResolver({
            importStyle: true
          })
        ]
      }),
      // gzip 压缩
      ViteCompression({
        disable: !isBuild,
        threshold: 10240,
        algorithm: 'gzip',
        ext: '.gz'
      }),
      // 兼容低版本浏览器
      legacy({
        targets: ['Chrome 63'],
        modernPolyfills: true
      })
    ],
    css: {
      preprocessorOptions: {
        less: {
          javascriptEnabled: true,
          plugins: [new DynamicAntdLess()]
        }
      }
    },
    optimizeDeps: {
      include: [
        ...styleDeps,
        'ant-design-vue',
        'ant-design-vue/es',
        'ele-admin-pro',
        'ele-admin-pro/es',
        '@ant-design/icons-vue',
        'vuedraggable',
        'dayjs',
        'echarts/core',
        'echarts/charts',
        'echarts/renderers',
        'echarts/components',
        'vue-echarts',
        'echarts-wordcloud',
        'xlsx'
      ]
    },
    server: {
      proxy: {
      //   // '/api': 'http://localhost:9100'
      //   // '/api': 'https://app-gateway-dev.cfhy.work/cfhy-auth-center',
      //   '/auth/': {
      //     target: 'https://tech-dev.cfhy.work/auth',
      //     // target: 'http://192.168.200.232:9100',
      //     changeOrigin: true,
      //     rewrite: (path) => path.replace(/^\/auth/, '')
      //   },
      //   '/api/': {
      //     target: 'https://tech-dev.cfhy.work/api',
      //     // target: 'http://192.168.200.232:9001',
      //     changeOrigin: true,
      //     rewrite: (path) => path.replace(/^\/api/, '')
      //   },
      //   '/sys/': {
      //     target: 'https://tech-dev.cfhy.work/sys',
      //     // target: 'http://192.168.200.232:9000',
      //     changeOrigin: true,
      //     rewrite: (path) => path.replace(/^\/sys/, '')
      //   }
      // }
    },
    build: {
      target: 'chrome63',
      chunkSizeWarningLimit: 2000,
      rollupOptions: {
        output: {
          external: [],
          // 分包
          manualChunks(id) {
            if (id.includes('node_modules')) {
              return id
                  .toString()
                  .split('node_modules/')[1]
                  .split('/')[0]
                  .toString();
            }
          }
        }
      }
    }
  };
});

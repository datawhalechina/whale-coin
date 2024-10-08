import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'

import ArcoVue from '@arco-design/web-vue'
import ArcoVueIcon from '@arco-design/web-vue/es/icon'
import '@arco-design/web-vue/dist/arco.css'
import '@/assets/styles/main.css'


// 引入router
import router from "./router";
import {createPinia} from "pinia";
import {usePersist} from "pinia-use-persist";
import './style.css'
import App from './App.vue'


const pinia = createPinia()
pinia.use(usePersist)
const app = createApp(App)
app.use(ElementPlus)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
  
app.use(pinia)
app.use(ArcoVue)
app.use(ArcoVueIcon)

app.use(router).mount('#app')

import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router'

import 'vfonts/Lato.css'
import '@/styles/common.css'

import axios from 'axios'
axios.defaults.baseURL = import.meta.env.VITE_APP_BACKEND_BASE_URL

createApp(App).use(router).mount('#app')
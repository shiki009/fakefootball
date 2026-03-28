import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { inject } from '@vercel/analytics'
import router from './router.js'
import App from './app.vue'
import './style.css'

inject()

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')

import './assets/main.css'

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

import Home from './pages/Home.vue'
import Account from './pages/Account.vue'
import Networks from './pages/Networks.vue'

const app = createApp(App)

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/account', name: 'Account', component: Account },
  { path: '/login', name: 'Login', component: Home },
  { path: '/logout', name: 'Logout', component: Home },
  { path: '/signup', name: 'Signup', component: Home },
  { path: '/networks', name: 'Networks', component: Networks },
  { path: '/network', name: 'Network', component: Home }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

app.use(router)

app.mount('#app')

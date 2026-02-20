import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import AuthCallback from './views/AuthCallback.vue'
import Dashboard from './views/Dashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/auth/callback',
    name: 'AuthCallback',
    component: AuthCallback
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    next('/')
  } else if (to.name === 'Login' && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
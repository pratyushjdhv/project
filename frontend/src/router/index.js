import Signup from '@/components/signup.vue'
import login from '@/components/login.vue'
import { createRouter, createWebHistory } from 'vue-router'
import Studentdashboard from '@/components/studentdashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path :'/signup',
      name: 'signup',
      component : Signup,
    },
    {
      path : '/login',
      name: 'login',
      component: login,
    },
    {
      path : '/studentdashboard',
      name: 'studentdashboard',
      component: Studentdashboard,
    },
  ],
})

export default router

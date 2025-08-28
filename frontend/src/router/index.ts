import { createRouter, createWebHistory } from 'vue-router'
import LoginForm from '@/components/LoginForm.vue'
import HabitsView from '@/views/HabitsView.vue'

const routes = [
  {
    path: "/",
    name: "Login",
    component: LoginForm
  },
  {
    path: "/habits",
    name: "HabitsView",
    component: HabitsView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

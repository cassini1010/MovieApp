import { createRouter, createWebHistory } from 'vue-router'
import MoviePage from '../views/MoviePage.vue'
import AdminPage from '../views/AdminPage.vue'

const routes = [
  {
    path: "/",
    name: 'movie',
    component: MoviePage
  },
  { 
    path: "/admin",
    name: 'admin',
    component: AdminPage
   },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

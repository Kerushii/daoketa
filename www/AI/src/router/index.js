import { createRouter, createWebHistory } from 'vue-router'
import annotate from '../views/annotate.vue'
import assist from '../views/assist.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'assist',
      component: assist
    },
    {
      path: '/assist',
      name: 'assist',
      component: assist
    },
    {
      path: '/annotate',
      name: 'annotate',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: annotate
    }
  ]
})

export default router

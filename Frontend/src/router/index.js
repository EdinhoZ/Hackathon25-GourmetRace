import { createRouter, createWebHistory } from 'vue-router'
import homepageview from '@/views/homepageview.vue'
import GraphComponent from '@/components/GraphComponent.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: homepageview,
    },
    {
      path: '/graph',
      name: 'graph',
      component: GraphComponent,
    }

  ]
})

export default router

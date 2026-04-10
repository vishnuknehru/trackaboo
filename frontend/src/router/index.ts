import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard',
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
    },
    // New paths
    {
      path: '/expense/inflows',
      name: 'inflows',
      component: () => import('@/views/InflowView.vue'),
    },
    {
      path: '/expense/outflows',
      name: 'outflows',
      component: () => import('@/views/OutflowView.vue'),
    },
    {
      path: '/settings/categories',
      name: 'categories',
      component: () => import('@/views/CategoriesView.vue'),
    },
    // Legacy redirects (backward compat)
    { path: '/inflows', redirect: '/expense/inflows' },
    { path: '/outflows', redirect: '/expense/outflows' },
    { path: '/categories', redirect: '/settings/categories' },
  ],
})

export default router

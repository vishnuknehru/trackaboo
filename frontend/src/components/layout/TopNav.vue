<script setup lang="ts">
import { useRoute } from 'vue-router'
import DropdownMenu from '@/components/shared/DropdownMenu.vue'

const route = useRoute()

function isDashboardActive(): boolean {
  return route.path === '/dashboard'
}

const expenseItems = [
  { label: 'Inflows', to: '/expense/inflows' },
  { label: 'Outflows', to: '/expense/outflows' },
]

const settingsItems = [
  { label: 'Categories', to: '/settings/categories' },
]
</script>

<template>
  <nav class="bg-white border-b border-gray-200 px-6 h-14 flex items-center justify-between flex-shrink-0">

    <!-- Left: brand -->
    <div class="flex items-center gap-2">
      <svg class="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 11h.01M12 11h.01M15 11h.01M4 20h16a2 2 0 002-2V6a2 2 0 00-2-2H4a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
      <span class="text-base font-semibold text-gray-900 tracking-tight">Trackaboo</span>
    </div>

    <!-- Center: primary nav links -->
    <div class="flex items-center gap-6">
      <RouterLink
        to="/dashboard"
        :class="[
          'text-sm font-medium pb-1 transition-colors',
          isDashboardActive()
            ? 'text-primary-600 border-b-2 border-primary-600'
            : 'text-gray-600 hover:text-gray-900',
        ]"
      >
        Dashboard
      </RouterLink>

      <DropdownMenu label="Expense" :items="expenseItems" />
    </div>

    <!-- Right: icon buttons + settings -->
    <div class="flex items-center gap-1">
      <!-- API Docs -->
      <a
        href="http://localhost:8000/docs"
        target="_blank"
        rel="noopener"
        class="p-2 rounded-button text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
        title="API Docs"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
        </svg>
      </a>

      <!-- Settings gear dropdown -->
      <DropdownMenu :items="settingsItems" :icon-only="true" />
    </div>

  </nav>
</template>

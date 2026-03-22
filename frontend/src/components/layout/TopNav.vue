<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()

const links = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Inflows', to: '/inflows' },
  { label: 'Outflows', to: '/outflows' },
]

function isActive(path: string): boolean {
  return route.path === path
}
</script>

<template>
  <nav class="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
    <span class="text-xl font-bold text-gray-900">Trackaboo</span>
    <div class="flex items-center gap-6">
      <RouterLink
        v-for="link in links"
        :key="link.to"
        :to="link.to"
        :class="[
          'text-sm font-medium pb-1',
          isActive(link.to)
            ? 'text-blue-600 border-b-2 border-blue-600'
            : 'text-gray-600 hover:text-gray-900',
        ]"
      >
        {{ link.label }}
      </RouterLink>
    </div>
  </nav>
</template>

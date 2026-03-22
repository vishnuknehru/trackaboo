<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()

const links = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Inflows', to: '/inflows' },
  { label: 'Outflows', to: '/outflows' },
  { label: 'Categories', to: '/categories' },
]

function isActive(path: string): boolean {
  return route.path === path
}
</script>

<template>
  <aside class="w-[220px] min-w-[220px] bg-slate-800 flex flex-col h-screen">
    <!-- Brand -->
    <div class="flex items-center gap-2 px-5 py-5 border-b border-slate-700">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-7 w-7 text-emerald-400 shrink-0"
        viewBox="0 0 24 24"
        fill="currentColor"
      >
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm1 5.5v.545A3.502 3.502 0 0 1 15.5 11.5c0 .828-.672 1.5-1.5 1.5s-1.5-.672-1.5-1.5c0-.276-.224-.5-.5-.5s-.5.224-.5.5a2.5 2.5 0 0 0 2 2.45V14.5a1 1 0 1 1-2 0v-.545A3.502 3.502 0 0 1 8.5 11.5c0-.828.672-1.5 1.5-1.5s1.5.672 1.5 1.5c0 .276.224.5.5.5s.5-.224.5-.5a2.5 2.5 0 0 0-2-2.45V7.5a1 1 0 1 1 2 0z"
        />
      </svg>
      <span class="text-white font-bold text-lg tracking-tight">Trackaboo</span>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 px-3 py-4 flex flex-col gap-1">
      <RouterLink
        v-for="link in links"
        :key="link.to"
        :to="link.to"
        :class="[
          'flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors',
          isActive(link.to)
            ? 'bg-slate-600 text-white'
            : 'text-slate-300 hover:bg-slate-700 hover:text-white',
        ]"
      >
        <!-- Dashboard icon: grid -->
        <svg
          v-if="link.to === '/dashboard'"
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4 shrink-0"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <rect x="3" y="3" width="7" height="7" rx="1" />
          <rect x="14" y="3" width="7" height="7" rx="1" />
          <rect x="3" y="14" width="7" height="7" rx="1" />
          <rect x="14" y="14" width="7" height="7" rx="1" />
        </svg>

        <!-- Inflows icon: arrow-down -->
        <svg
          v-else-if="link.to === '/inflows'"
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4 shrink-0"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m0 0-6-6m6 6 6-6" />
        </svg>

        <!-- Outflows icon: arrow-up -->
        <svg
          v-else-if="link.to === '/outflows'"
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4 shrink-0"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 20V4m0 0 6 6m-6-6-6 6" />
        </svg>

        <!-- Categories icon: tag -->
        <svg
          v-else-if="link.to === '/categories'"
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4 shrink-0"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M7 7h.01M3 5.5A2.5 2.5 0 0 1 5.5 3h5.086a2 2 0 0 1 1.414.586l7.914 7.914a2 2 0 0 1 0 2.828l-5.086 5.086a2 2 0 0 1-2.828 0L4.586 11.5A2 2 0 0 1 4 10.086V5.5Z"
          />
        </svg>

        {{ link.label }}
      </RouterLink>
    </nav>
  </aside>
</template>

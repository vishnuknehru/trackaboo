<script setup lang="ts">
interface Props {
  title: string
  description: string
  actionLabel?: string
}

defineProps<Props>()

const emit = defineEmits<{
  action: []
}>()
</script>

<template>
  <div class="flex flex-col items-center justify-center py-16 px-4">
    <div class="border-2 border-dashed border-gray-200 rounded-card bg-gray-50/50 flex flex-col items-center text-center p-12 w-full max-w-sm">
      <!-- SVG illustration -->
      <svg class="h-14 w-14 text-gray-300 mb-4" fill="none" viewBox="0 0 48 48" stroke="currentColor" stroke-width="1.2">
        <rect x="8" y="10" width="32" height="28" rx="3" stroke-linejoin="round" />
        <path stroke-linecap="round" d="M16 18h16M16 24h10M16 30h8" />
      </svg>
      <h3 class="text-base font-semibold text-gray-700 mb-1">{{ title }}</h3>
      <p class="text-sm text-gray-400 mb-6">{{ description }}</p>
      <button
        v-if="actionLabel"
        type="button"
        class="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-button hover:bg-primary-700 transition-colors"
        @click="emit('action')"
      >
        {{ actionLabel }}
      </button>
    </div>
  </div>
</template>

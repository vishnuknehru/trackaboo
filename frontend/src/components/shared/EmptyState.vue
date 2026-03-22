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
  <div class="flex flex-col items-center justify-center py-16 px-4 text-center">
    <div class="text-5xl mb-4" aria-hidden="true">📭</div>
    <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ title }}</h3>
    <p class="text-sm text-gray-500 max-w-sm mb-6">{{ description }}</p>
    <button
      v-if="actionLabel"
      type="button"
      class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors"
      @click="emit('action')"
    >
      {{ actionLabel }}
    </button>
  </div>
</template>

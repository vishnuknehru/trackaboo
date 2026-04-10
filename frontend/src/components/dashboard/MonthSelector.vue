<script setup lang="ts">
import { formatMonth, shiftMonth } from '@/lib/formatters'

interface Props {
  modelValue: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

function prev() {
  emit('update:modelValue', shiftMonth(props.modelValue, -1))
}

function next() {
  emit('update:modelValue', shiftMonth(props.modelValue, 1))
}
</script>

<template>
  <div class="flex items-center bg-white border border-gray-200 rounded-button shadow-sm px-1 py-1 gap-1">
    <button
      type="button"
      class="p-1.5 rounded text-gray-400 hover:text-gray-700 hover:bg-gray-100 transition-colors"
      aria-label="Previous month"
      @click="prev"
    >
      <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    <span class="text-sm font-semibold text-gray-800 min-w-32 text-center px-1">
      {{ formatMonth(modelValue) }}
    </span>
    <button
      type="button"
      class="p-1.5 rounded text-gray-400 hover:text-gray-700 hover:bg-gray-100 transition-colors"
      aria-label="Next month"
      @click="next"
    >
      <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
      </svg>
    </button>
  </div>
</template>

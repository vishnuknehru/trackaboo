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
  <div class="flex items-center gap-4">
    <button
      type="button"
      class="p-2 rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-100 transition-colors"
      aria-label="Previous month"
      @click="prev"
    >
      &#8249;
    </button>
    <span class="text-base font-semibold text-gray-900 min-w-36 text-center">
      {{ formatMonth(modelValue) }}
    </span>
    <button
      type="button"
      class="p-2 rounded-md text-gray-500 hover:text-gray-900 hover:bg-gray-100 transition-colors"
      aria-label="Next month"
      @click="next"
    >
      &#8250;
    </button>
  </div>
</template>

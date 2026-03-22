<script setup lang="ts">
import { computed } from 'vue'
import { formatCurrency } from '@/lib/formatters'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'

interface Props {
  title: string
  amount: number
  variant: 'inflow' | 'outflow' | 'net'
  isLoading: boolean
}

const props = defineProps<Props>()

const amountColorClass = computed(() => {
  if (props.variant === 'inflow') return 'text-emerald-600'
  if (props.variant === 'outflow') return 'text-red-600'
  // net variant
  if (props.amount > 0) return 'text-emerald-600'
  if (props.amount < 0) return 'text-red-600'
  return 'text-gray-500'
})
</script>

<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <p class="text-sm font-medium text-gray-500 mb-2">{{ title }}</p>
    <div v-if="isLoading" class="flex items-center justify-center h-8">
      <LoadingSpinner size="sm" />
    </div>
    <p v-else :class="[amountColorClass, 'text-2xl font-bold']">
      {{ formatCurrency(amount) }}
    </p>
  </div>
</template>

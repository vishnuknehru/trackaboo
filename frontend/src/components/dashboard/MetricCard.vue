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

const accentClass = computed(() => {
  if (props.variant === 'inflow') return 'bg-emerald-500'
  if (props.variant === 'outflow') return 'bg-red-500'
  return 'bg-indigo-500'
})

const amountColorClass = computed(() => {
  if (props.variant === 'inflow') return 'text-emerald-600'
  if (props.variant === 'outflow') return 'text-red-600'
  if (props.amount > 0) return 'text-emerald-600'
  if (props.amount < 0) return 'text-red-600'
  return 'text-gray-500'
})
</script>

<template>
  <div class="bg-white rounded-card shadow-card hover:shadow-card-hover transition-shadow overflow-hidden flex">
    <!-- Left accent bar -->
    <div :class="['w-1.5 flex-shrink-0', accentClass]" />

    <div class="flex-1 p-5">
      <!-- Icon + title row -->
      <div class="flex items-center gap-2 mb-3">
        <!-- Inflow icon -->
        <svg v-if="variant === 'inflow'" class="h-4 w-4 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m0 0l-4-4m4 4l4-4" />
        </svg>
        <!-- Outflow icon -->
        <svg v-else-if="variant === 'outflow'" class="h-4 w-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 20V4m0 0l-4 4m4-4l4 4" />
        </svg>
        <!-- Net icon -->
        <svg v-else class="h-4 w-4 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 6h18M3 12h18M3 18h18" />
        </svg>
        <p class="text-xs font-medium uppercase tracking-wider text-gray-500">{{ title }}</p>
      </div>

      <!-- Amount -->
      <div v-if="isLoading" class="flex items-center h-9">
        <LoadingSpinner size="sm" />
      </div>
      <p v-else :class="[amountColorClass, 'text-3xl font-bold tracking-tight']">
        {{ formatCurrency(amount) }}
      </p>
    </div>
  </div>
</template>

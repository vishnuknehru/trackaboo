<script setup lang="ts">
import { computed } from 'vue'
import { formatCurrency } from '@/lib/formatters'

interface Props {
  amount: number
  variant: 'inflow' | 'outflow' | 'net'
}

const props = defineProps<Props>()

const colorClass = computed(() => {
  if (props.variant === 'inflow') return 'text-emerald-600'
  if (props.variant === 'outflow') return 'text-red-600'
  // net: positive = emerald, negative = red, zero = gray
  if (props.amount > 0) return 'text-emerald-600'
  if (props.amount < 0) return 'text-red-600'
  return 'text-gray-500'
})

const prefix = computed(() => {
  if (props.variant !== 'net') return ''
  if (props.amount > 0) return '+'
  return ''
})
</script>

<template>
  <span :class="colorClass" class="font-semibold">
    {{ prefix }}{{ formatCurrency(props.amount) }}
  </span>
</template>

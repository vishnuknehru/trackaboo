<script setup lang="ts">
import { computed } from 'vue'
import { useMonthStore } from '@/stores/useMonthStore'
import { useMetrics } from '@/composables/useMetrics'
import MonthSelector from '@/components/dashboard/MonthSelector.vue'
import MetricCard from '@/components/dashboard/MetricCard.vue'
import CategoryBreakdown from '@/components/dashboard/CategoryBreakdown.vue'

const monthStore = useMonthStore()
const month = computed({
  get: () => monthStore.month,
  set: (v) => monthStore.setMonth(v),
})

const { data: metrics, isPending } = useMetrics(computed(() => monthStore.month))
</script>

<template>
  <div class="max-w-6xl mx-auto px-6 py-8">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="text-sm text-gray-500 mt-0.5">Your financial overview at a glance</p>
      </div>
      <MonthSelector v-model="month" />
    </div>

    <!-- Metric cards -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
      <MetricCard
        title="Total Inflow"
        :amount="metrics?.totalInflow ?? 0"
        variant="inflow"
        :isLoading="isPending"
      />
      <MetricCard
        title="Total Outflow"
        :amount="metrics?.totalOutflow ?? 0"
        variant="outflow"
        :isLoading="isPending"
      />
      <MetricCard
        title="Net Flow"
        :amount="metrics?.netFlow ?? 0"
        variant="net"
        :isLoading="isPending"
      />
    </div>

    <!-- Category breakdown -->
    <CategoryBreakdown
      :breakdown="metrics?.categoryBreakdown ?? []"
      :isLoading="isPending"
    />

    <!-- Quick links -->
    <div class="mt-6 flex gap-3">
      <RouterLink
        :to="`/expense/inflows?month=${monthStore.month}`"
        class="inline-flex items-center gap-1.5 text-sm font-medium text-primary-600 hover:text-primary-700 transition-colors"
      >
        View Inflows
        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
        </svg>
      </RouterLink>
      <RouterLink
        :to="`/expense/outflows?month=${monthStore.month}`"
        class="inline-flex items-center gap-1.5 text-sm font-medium text-primary-600 hover:text-primary-700 transition-colors"
      >
        View Outflows
        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
        </svg>
      </RouterLink>
    </div>
  </div>
</template>

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
  <div class="max-w-5xl mx-auto px-6 py-8">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
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
    <div class="mt-6 flex gap-4">
      <RouterLink
        :to="`/inflows?month=${monthStore.month}`"
        class="text-sm text-blue-600 hover:underline"
      >
        View Inflows &rarr;
      </RouterLink>
      <RouterLink
        :to="`/outflows?month=${monthStore.month}`"
        class="text-sm text-blue-600 hover:underline"
      >
        View Outflows &rarr;
      </RouterLink>
    </div>
  </div>
</template>

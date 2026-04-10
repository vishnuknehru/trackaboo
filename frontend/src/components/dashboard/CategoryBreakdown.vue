<script setup lang="ts">
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  type ChartData,
} from 'chart.js'
import type { CategoryBreakdownItem } from '@/types/api'
import { formatCurrency, formatPercentage } from '@/lib/formatters'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'

ChartJS.register(ArcElement, Tooltip, Legend)

interface Props {
  breakdown: CategoryBreakdownItem[]
  isLoading: boolean
}

const props = defineProps<Props>()

const chartData = computed<ChartData<'doughnut'>>(() => ({
  labels: props.breakdown.map((b) => b.categoryName),
  datasets: [
    {
      data: props.breakdown.map((b) => b.amount),
      backgroundColor: props.breakdown.map((b) => b.color ?? '#94a3b8'),
      borderWidth: 2,
      borderColor: '#ffffff',
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      display: false,
    },
  },
}
</script>

<template>
  <div class="bg-white rounded-card shadow-card p-6">
    <h3 class="text-base font-semibold text-gray-900 mb-5">Spending by Category</h3>

    <div v-if="isLoading" class="flex items-center justify-center py-12">
      <LoadingSpinner size="lg" />
    </div>

    <div v-else-if="breakdown.length === 0" class="flex items-center justify-center py-12">
      <p class="text-sm text-gray-400">No spending data for this month.</p>
    </div>

    <div v-else>
      <div class="max-w-xs mx-auto mb-6">
        <Doughnut :data="chartData" :options="chartOptions" />
      </div>

      <ul class="space-y-1">
        <li
          v-for="item in breakdown"
          :key="item.categoryId"
          class="flex items-center justify-between px-3 py-2.5 rounded-lg hover:bg-gray-50 transition-colors -mx-3"
        >
          <div class="flex items-center gap-2.5">
            <span
              class="inline-block h-3.5 w-3.5 rounded-full flex-shrink-0 ring-2 ring-white"
              :style="{ backgroundColor: item.color ?? '#94a3b8' }"
            />
            <span class="text-sm text-gray-700">{{ item.categoryName }}</span>
          </div>
          <div class="flex items-center gap-3 text-sm">
            <span class="text-gray-400">{{ formatPercentage(item.percentage) }}</span>
            <span class="font-semibold text-gray-900">{{ formatCurrency(item.amount) }}</span>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

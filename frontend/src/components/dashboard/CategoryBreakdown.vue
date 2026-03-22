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
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <h3 class="text-base font-semibold text-gray-900 mb-4">Spending by Category</h3>

    <div v-if="isLoading" class="flex items-center justify-center py-12">
      <LoadingSpinner size="lg" />
    </div>

    <div v-else-if="breakdown.length === 0" class="flex items-center justify-center py-12">
      <p class="text-sm text-gray-500">No spending data for this month.</p>
    </div>

    <div v-else>
      <div class="max-w-xs mx-auto mb-6">
        <Doughnut :data="chartData" :options="chartOptions" />
      </div>

      <ul class="space-y-2">
        <li
          v-for="item in breakdown"
          :key="item.categoryId"
          class="flex items-center justify-between py-2 border-b border-gray-100 last:border-0"
        >
          <div class="flex items-center gap-2">
            <span
              class="inline-block h-3 w-3 rounded-full flex-shrink-0"
              :style="{ backgroundColor: item.color ?? '#94a3b8' }"
            />
            <span class="text-sm text-gray-700">{{ item.categoryName }}</span>
          </div>
          <div class="flex items-center gap-3 text-sm">
            <span class="text-gray-500">{{ formatPercentage(item.percentage) }}</span>
            <span class="font-medium text-gray-900">{{ formatCurrency(item.amount) }}</span>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Inflow } from '@/types/api'
import { formatCurrency, formatDate } from '@/lib/formatters'
import { apiClient } from '@/lib/api/client'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'
import { ref } from 'vue'

interface Props {
  inflows: Inflow[]
  isLoading: boolean
}

defineProps<Props>()

const emit = defineEmits<{
  edit: [inflow: Inflow]
  deleted: []
}>()

const deletingId = ref<number | null>(null)

async function handleDelete(inflow: Inflow) {
  if (!confirm(`Delete inflow "${inflow.source}"?`)) return
  deletingId.value = inflow.id
  try {
    await apiClient.delete(`/inflows/${inflow.id}`)
    emit('deleted')
  } finally {
    deletingId.value = null
  }
}
</script>

<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
    <div v-if="isLoading" class="flex items-center justify-center py-12">
      <LoadingSpinner size="lg" />
    </div>

    <table v-else class="w-full text-sm">
      <thead class="bg-gray-50 border-b border-gray-200">
        <tr>
          <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Date
          </th>
          <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Source
          </th>
          <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Description
          </th>
          <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
            Amount
          </th>
          <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
            Actions
          </th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100">
        <tr v-for="inflow in inflows" :key="inflow.id" class="hover:bg-gray-50">
          <td class="px-4 py-3 text-gray-600 whitespace-nowrap">
            {{ formatDate(inflow.date) }}
          </td>
          <td class="px-4 py-3 font-medium text-gray-900">{{ inflow.source }}</td>
          <td class="px-4 py-3 text-gray-500">{{ inflow.description ?? '—' }}</td>
          <td class="px-4 py-3 text-right font-semibold text-emerald-600 whitespace-nowrap">
            {{ formatCurrency(inflow.amount) }}
          </td>
          <td class="px-4 py-3 text-right whitespace-nowrap">
            <button
              type="button"
              class="text-blue-600 hover:text-blue-800 text-xs font-medium mr-3"
              @click="emit('edit', inflow)"
            >
              Edit
            </button>
            <button
              type="button"
              class="text-red-500 hover:text-red-700 text-xs font-medium"
              :disabled="deletingId === inflow.id"
              @click="handleDelete(inflow)"
            >
              {{ deletingId === inflow.id ? 'Deleting…' : 'Delete' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

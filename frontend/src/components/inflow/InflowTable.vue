<script setup lang="ts">
import { ref } from 'vue'
import type { Inflow } from '@/types/api'
import { formatCurrency, formatDate } from '@/lib/formatters'
import { apiClient } from '@/lib/api/client'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'

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
const deleteConfirmId = ref<number | null>(null)

async function confirmDelete(inflow: Inflow) {
  deletingId.value = inflow.id
  deleteConfirmId.value = null
  try {
    await apiClient.delete(`/inflows/${inflow.id}`)
    emit('deleted')
  } finally {
    deletingId.value = null
  }
}
</script>

<template>
  <div class="bg-white rounded-card shadow-card overflow-hidden">
    <div v-if="isLoading" class="flex items-center justify-center py-12">
      <LoadingSpinner size="lg" />
    </div>

    <table v-else class="w-full text-sm">
      <thead class="bg-gray-50 border-b border-gray-100">
        <tr>
          <th class="px-5 py-3.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
          <th class="px-5 py-3.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Source</th>
          <th class="px-5 py-3.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
          <th class="px-5 py-3.5 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
          <th class="px-5 py-3.5 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-50">
        <tr
          v-for="inflow in inflows"
          :key="inflow.id"
          class="hover:bg-primary-50/30 transition-colors even:bg-gray-50/50"
        >
          <td class="px-5 py-4 text-gray-500 whitespace-nowrap text-xs">
            {{ formatDate(inflow.date) }}
          </td>
          <td class="px-5 py-4 font-medium text-gray-900">{{ inflow.source }}</td>
          <td class="px-5 py-4 text-gray-400 text-xs">{{ inflow.description ?? '—' }}</td>
          <td class="px-5 py-4 text-right font-bold text-emerald-600 whitespace-nowrap">
            {{ formatCurrency(inflow.amount) }}
          </td>
          <td class="px-5 py-4 text-right whitespace-nowrap">
            <div class="flex items-center justify-end gap-1">
              <button
                type="button"
                class="px-2.5 py-1 text-xs font-medium text-gray-600 rounded hover:bg-gray-100 transition-colors"
                @click="emit('edit', inflow)"
              >
                Edit
              </button>

              <!-- Inline delete confirm -->
              <template v-if="deleteConfirmId === inflow.id">
                <span class="text-xs text-gray-400">Sure?</span>
                <button
                  type="button"
                  class="px-2.5 py-1 text-xs font-medium text-white bg-red-600 rounded hover:bg-red-700 transition-colors"
                  :disabled="deletingId === inflow.id"
                  @click="confirmDelete(inflow)"
                >
                  {{ deletingId === inflow.id ? '…' : 'Yes' }}
                </button>
                <button
                  type="button"
                  class="px-2.5 py-1 text-xs font-medium text-gray-600 rounded hover:bg-gray-100 transition-colors"
                  @click="deleteConfirmId = null"
                >
                  No
                </button>
              </template>
              <button
                v-else
                type="button"
                class="px-2.5 py-1 text-xs font-medium text-red-500 rounded hover:bg-red-50 transition-colors"
                @click="deleteConfirmId = inflow.id"
              >
                Delete
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

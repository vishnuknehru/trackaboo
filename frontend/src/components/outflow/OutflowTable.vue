<script setup lang="ts">
import { ref } from 'vue'
import type { Outflow, Category } from '@/types/api'
import { formatCurrency, formatDate } from '@/lib/formatters'
import { apiClient } from '@/lib/api/client'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'

interface Props {
  outflows: Outflow[]
  isLoading: boolean
  categories: Category[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  edit: [outflow: Outflow]
  deleted: []
}>()

const deletingId = ref<number | null>(null)
const deleteConfirmId = ref<number | null>(null)

function categoryFor(id: number): Category | undefined {
  return props.categories.find((c) => c.id === id)
}

async function confirmDelete(outflow: Outflow) {
  deletingId.value = outflow.id
  deleteConfirmId.value = null
  try {
    await apiClient.delete(`/outflows/${outflow.id}`)
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
          <th class="px-5 py-3.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
          <th class="px-5 py-3.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
          <th class="px-5 py-3.5 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
          <th class="px-5 py-3.5 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-50">
        <tr
          v-for="outflow in outflows"
          :key="outflow.id"
          class="hover:bg-primary-50/30 transition-colors even:bg-gray-50/50"
        >
          <td class="px-5 py-4 text-gray-500 whitespace-nowrap text-xs">
            {{ formatDate(outflow.date) }}
          </td>
          <td class="px-5 py-4">
            <span class="inline-flex items-center gap-2">
              <span
                v-if="categoryFor(outflow.categoryId)?.color"
                class="inline-block h-3 w-3 rounded-full flex-shrink-0 ring-2 ring-white"
                :style="{ backgroundColor: categoryFor(outflow.categoryId)?.color ?? '#94a3b8' }"
              />
              <span class="text-gray-700 font-medium">
                {{ categoryFor(outflow.categoryId)?.name ?? '—' }}
              </span>
            </span>
          </td>
          <td class="px-5 py-4 text-gray-400 text-xs">{{ outflow.description ?? '—' }}</td>
          <td class="px-5 py-4 text-right font-bold text-red-600 whitespace-nowrap">
            {{ formatCurrency(outflow.amount) }}
          </td>
          <td class="px-5 py-4 text-right whitespace-nowrap">
            <div class="flex items-center justify-end gap-1">
              <button
                type="button"
                class="px-2.5 py-1 text-xs font-medium text-gray-600 rounded hover:bg-gray-100 transition-colors"
                @click="emit('edit', outflow)"
              >
                Edit
              </button>

              <!-- Inline delete confirm -->
              <template v-if="deleteConfirmId === outflow.id">
                <span class="text-xs text-gray-400">Sure?</span>
                <button
                  type="button"
                  class="px-2.5 py-1 text-xs font-medium text-white bg-red-600 rounded hover:bg-red-700 transition-colors"
                  :disabled="deletingId === outflow.id"
                  @click="confirmDelete(outflow)"
                >
                  {{ deletingId === outflow.id ? '…' : 'Yes' }}
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
                @click="deleteConfirmId = outflow.id"
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

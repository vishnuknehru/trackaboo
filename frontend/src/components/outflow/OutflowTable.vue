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

function categoryFor(id: number): Category | undefined {
  return props.categories.find((c) => c.id === id)
}

async function handleDelete(outflow: Outflow) {
  if (!confirm('Delete this outflow?')) return
  deletingId.value = outflow.id
  try {
    await apiClient.delete(`/outflows/${outflow.id}`)
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
            Category
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
        <tr v-for="outflow in outflows" :key="outflow.id" class="hover:bg-gray-50">
          <td class="px-4 py-3 text-gray-600 whitespace-nowrap">
            {{ formatDate(outflow.date) }}
          </td>
          <td class="px-4 py-3">
            <span class="inline-flex items-center gap-1.5">
              <span
                v-if="categoryFor(outflow.categoryId)?.color"
                class="inline-block h-2.5 w-2.5 rounded-full flex-shrink-0"
                :style="{ backgroundColor: categoryFor(outflow.categoryId)?.color ?? '#94a3b8' }"
              />
              <span class="text-gray-700">
                {{ categoryFor(outflow.categoryId)?.name ?? '—' }}
              </span>
            </span>
          </td>
          <td class="px-4 py-3 text-gray-500">{{ outflow.description ?? '—' }}</td>
          <td class="px-4 py-3 text-right font-semibold text-red-600 whitespace-nowrap">
            {{ formatCurrency(outflow.amount) }}
          </td>
          <td class="px-4 py-3 text-right whitespace-nowrap">
            <button
              type="button"
              class="text-blue-600 hover:text-blue-800 text-xs font-medium mr-3"
              @click="emit('edit', outflow)"
            >
              Edit
            </button>
            <button
              type="button"
              class="text-red-500 hover:text-red-700 text-xs font-medium"
              :disabled="deletingId === outflow.id"
              @click="handleDelete(outflow)"
            >
              {{ deletingId === outflow.id ? 'Deleting…' : 'Delete' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

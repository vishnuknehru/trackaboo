<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQueryClient } from '@tanstack/vue-query'
import type { Outflow } from '@/types/api'
import { useOutflows } from '@/composables/useOutflows'
import { useCategories } from '@/composables/useCategories'
import { currentMonth } from '@/lib/formatters'
import MonthSelector from '@/components/dashboard/MonthSelector.vue'
import OutflowTable from '@/components/outflow/OutflowTable.vue'
import OutflowForm from '@/components/outflow/OutflowForm.vue'
import EmptyState from '@/components/shared/EmptyState.vue'

const route = useRoute()
const router = useRouter()
const queryClient = useQueryClient()

const month = computed({
  get: () => (route.query.month as string) || currentMonth(),
  set: (v) => router.replace({ query: { ...route.query, month: v } }),
})

const categoryType = ref<string>('outflow')

const params = computed(() => ({
  month: month.value,
  page: 1,
  limit: 20,
}))

const { data, isPending, refetch } = useOutflows(params)
const { data: categoriesData } = useCategories(categoryType)

const categories = computed(() => categoriesData.value?.data ?? [])

const formOpen = ref(false)
const editItem = ref<Outflow | null>(null)

function openCreate() {
  editItem.value = null
  formOpen.value = true
}

function openEdit(outflow: Outflow) {
  editItem.value = outflow
  formOpen.value = true
}

async function onSaved() {
  await queryClient.invalidateQueries({ queryKey: ['outflows'] })
  refetch()
}

async function onDeleted() {
  await queryClient.invalidateQueries({ queryKey: ['outflows'] })
  refetch()
}
</script>

<template>
  <div class="max-w-6xl mx-auto px-6 py-8">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Outflows</h1>
        <p class="text-sm text-gray-500 mt-0.5">Track your expenses and spending</p>
      </div>
      <div class="flex items-center gap-3">
        <MonthSelector v-model="month" />
        <button
          type="button"
          class="px-4 py-2.5 bg-primary-600 text-white text-sm font-medium rounded-button hover:bg-primary-700 transition-colors"
          @click="openCreate"
        >
          + Add Outflow
        </button>
      </div>
    </div>

    <OutflowTable
      v-if="(data?.data?.length ?? 0) > 0 || isPending"
      :outflows="data?.data ?? []"
      :isLoading="isPending"
      :categories="categories"
      @edit="openEdit"
      @deleted="onDeleted"
    />

    <EmptyState
      v-else
      title="No outflows yet"
      description="Record your first expense for this month."
      actionLabel="Add Outflow"
      @action="openCreate"
    />

    <OutflowForm
      v-model:open="formOpen"
      :editItem="editItem"
      :categories="categories"
      @saved="onSaved"
    />
  </div>
</template>

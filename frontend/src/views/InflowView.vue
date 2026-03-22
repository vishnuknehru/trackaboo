<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQueryClient } from '@tanstack/vue-query'
import type { Inflow } from '@/types/api'
import { useInflows } from '@/composables/useInflows'
import { useCategories } from '@/composables/useCategories'
import { currentMonth } from '@/lib/formatters'
import MonthSelector from '@/components/dashboard/MonthSelector.vue'
import InflowTable from '@/components/inflow/InflowTable.vue'
import InflowForm from '@/components/inflow/InflowForm.vue'
import EmptyState from '@/components/shared/EmptyState.vue'

const route = useRoute()
const router = useRouter()
const queryClient = useQueryClient()

const month = computed({
  get: () => (route.query.month as string) || currentMonth(),
  set: (v) => router.replace({ query: { ...route.query, month: v } }),
})

const params = computed(() => ({
  month: month.value,
  page: 1,
  limit: 20,
}))

const { data, isPending, refetch } = useInflows(params)

const categoryType = ref<string>('inflow')
const { data: categoriesData } = useCategories(categoryType)
const categories = computed(() => categoriesData.value?.data ?? [])

const formOpen = ref(false)
const editItem = ref<Inflow | null>(null)

function openCreate() {
  editItem.value = null
  formOpen.value = true
}

function openEdit(inflow: Inflow) {
  editItem.value = inflow
  formOpen.value = true
}

async function onSaved() {
  await queryClient.invalidateQueries({ queryKey: ['inflows'] })
  refetch()
}

async function onDeleted() {
  await queryClient.invalidateQueries({ queryKey: ['inflows'] })
  refetch()
}
</script>

<template>
  <div class="max-w-5xl mx-auto px-6 py-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Inflows</h1>
      <div class="flex items-center gap-4">
        <MonthSelector v-model="month" />
        <button
          type="button"
          class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors"
          @click="openCreate"
        >
          + Add Inflow
        </button>
      </div>
    </div>

    <InflowTable
      v-if="(data?.data?.length ?? 0) > 0 || isPending"
      :inflows="data?.data ?? []"
      :isLoading="isPending"
      @edit="openEdit"
      @deleted="onDeleted"
    />

    <EmptyState
      v-else
      title="No inflows yet"
      description="Record your first income or earnings for this month."
      actionLabel="Add Inflow"
      @action="openCreate"
    />

    <InflowForm
      v-model:open="formOpen"
      :editItem="editItem"
      :categories="categories"
      @saved="onSaved"
    />
  </div>
</template>

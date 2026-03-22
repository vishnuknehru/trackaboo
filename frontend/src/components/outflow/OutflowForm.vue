<script setup lang="ts">
import { watch } from 'vue'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import type { Outflow, Category } from '@/types/api'
import { createOutflowSchema, updateOutflowSchema } from '@/lib/validations/outflow'
import { apiClient } from '@/lib/api/client'

interface Props {
  open: boolean
  editItem: Outflow | null
  categories: Category[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  saved: []
}>()

const { handleSubmit, errors, defineField, resetForm, setValues } = useForm({
  validationSchema: toTypedSchema(
    props.editItem ? updateOutflowSchema : createOutflowSchema,
  ),
})

const [amount, amountAttrs] = defineField('amount')
const [date, dateAttrs] = defineField('date')
const [categoryId, categoryIdAttrs] = defineField('categoryId')
const [description, descriptionAttrs] = defineField('description')

watch(
  () => props.editItem,
  (item) => {
    if (item) {
      setValues({
        amount: item.amount,
        date: item.date,
        categoryId: item.categoryId,
        description: item.description ?? undefined,
      })
    } else {
      resetForm()
    }
  },
  { immediate: true },
)

const onSubmit = handleSubmit(async (values) => {
  if (props.editItem) {
    await apiClient.patch(`/outflows/${props.editItem.id}`, values)
  } else {
    await apiClient.post('/outflows', values)
  }
  emit('saved')
  emit('update:open', false)
  resetForm()
})

function close() {
  emit('update:open', false)
  resetForm()
}
</script>

<template>
  <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center">
    <div class="absolute inset-0 bg-black/40" @click="close" />
    <div class="relative bg-white rounded-lg shadow-xl w-full max-w-md p-6 mx-4">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">
        {{ editItem ? 'Edit Outflow' : 'Add Outflow' }}
      </h2>

      <form class="space-y-4" @submit.prevent="onSubmit">
        <!-- Amount -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Amount</label>
          <input
            v-bind="amountAttrs"
            v-model.number="amount"
            type="number"
            step="0.01"
            min="0.01"
            placeholder="0.00"
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <p v-if="errors.amount" class="text-red-500 text-xs mt-1">{{ errors.amount }}</p>
        </div>

        <!-- Date -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Date</label>
          <input
            v-bind="dateAttrs"
            v-model="date"
            type="date"
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <p v-if="errors.date" class="text-red-500 text-xs mt-1">{{ errors.date }}</p>
        </div>

        <!-- Category -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
          <select
            v-bind="categoryIdAttrs"
            v-model.number="categoryId"
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
          >
            <option value="" disabled>Select a category</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
          <p v-if="errors.categoryId" class="text-red-500 text-xs mt-1">{{ errors.categoryId }}</p>
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Description <span class="text-gray-400">(optional)</span>
          </label>
          <textarea
            v-bind="descriptionAttrs"
            v-model="description"
            rows="3"
            placeholder="Additional notes…"
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
          <p v-if="errors.description" class="text-red-500 text-xs mt-1">{{ errors.description }}</p>
        </div>

        <div class="flex justify-end gap-3 pt-2">
          <button
            type="button"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
            @click="close"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors"
          >
            {{ editItem ? 'Save Changes' : 'Add Outflow' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

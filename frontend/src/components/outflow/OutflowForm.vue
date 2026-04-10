<script setup lang="ts">
import { watch } from 'vue'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { toast } from 'vue-sonner'
import type { Outflow, Category } from '@/types/api'
import { createOutflowSchema, updateOutflowSchema } from '@/lib/validations/outflow'
import { apiClient } from '@/lib/api/client'
import SlideOver from '@/components/shared/SlideOver.vue'
import CurrencyInput from '@/components/shared/CurrencyInput.vue'

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

const { handleSubmit, errors, defineField, resetForm, setValues, isSubmitting } = useForm({
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
  try {
    if (props.editItem) {
      await apiClient.patch(`/outflows/${props.editItem.id}`, values)
      toast.success('Outflow updated successfully')
    } else {
      await apiClient.post('/outflows', values)
      toast.success('Outflow added successfully')
    }
    emit('saved')
    emit('update:open', false)
    resetForm()
  } catch {
    toast.error('Failed to save outflow. Please try again.')
  }
})

function close() {
  emit('update:open', false)
  resetForm()
}
</script>

<template>
  <SlideOver :open="open" :title="editItem ? 'Edit Outflow' : 'Add Outflow'" @update:open="close">
    <form class="flex flex-col gap-5 p-6" @submit.prevent="onSubmit">

      <!-- Amount -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1.5">Amount</label>
        <CurrencyInput
          v-bind="amountAttrs"
          v-model="amount"
          placeholder="0.00"
        />
        <p class="text-xs text-gray-400 mt-1">Enter the amount spent</p>
        <p v-if="errors.amount" class="text-red-500 text-xs mt-1">{{ errors.amount }}</p>
      </div>

      <!-- Date -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1.5">Date</label>
        <input
          v-bind="dateAttrs"
          v-model="date"
          type="date"
          class="w-full border border-gray-200 rounded-input px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
        />
        <p v-if="errors.date" class="text-red-500 text-xs mt-1">{{ errors.date }}</p>
      </div>

      <!-- Category (required for outflows) -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1.5">Category</label>
        <select
          v-bind="categoryIdAttrs"
          v-model.number="categoryId"
          class="w-full border border-gray-200 rounded-input px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors bg-white"
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
        <label class="block text-sm font-medium text-gray-700 mb-1.5">
          Description <span class="text-gray-400 font-normal">(optional)</span>
        </label>
        <textarea
          v-bind="descriptionAttrs"
          v-model="description"
          rows="3"
          placeholder="Additional notes…"
          class="w-full border border-gray-200 rounded-input px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors resize-none"
        />
        <p v-if="errors.description" class="text-red-500 text-xs mt-1">{{ errors.description }}</p>
      </div>

      <!-- Actions -->
      <div class="flex gap-3 pt-2 mt-auto">
        <button
          type="button"
          class="flex-1 px-4 py-2.5 text-sm font-medium text-gray-600 bg-transparent border border-gray-200 rounded-button hover:bg-gray-50 transition-colors"
          @click="close"
        >
          Cancel
        </button>
        <button
          type="submit"
          :disabled="isSubmitting"
          class="flex-1 px-4 py-2.5 text-sm font-medium text-white bg-primary-600 rounded-button hover:bg-primary-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {{ isSubmitting ? 'Saving…' : (editItem ? 'Save Changes' : 'Add Outflow') }}
        </button>
      </div>

    </form>
  </SlideOver>
</template>

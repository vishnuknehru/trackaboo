<script setup lang="ts">
import { ref, computed } from 'vue'
import { useQueryClient } from '@tanstack/vue-query'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { toast } from 'vue-sonner'
import type { Category } from '@/types/api'
import { useCategories } from '@/composables/useCategories'
import { createCategorySchema, updateCategorySchema } from '@/lib/validations/category'
import { apiClient } from '@/lib/api/client'
import SlideOver from '@/components/shared/SlideOver.vue'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'

const queryClient = useQueryClient()

const { data, isPending } = useCategories()

const categories = computed(() => data.value?.data ?? [])

const formOpen = ref(false)
const editItem = ref<Category | null>(null)
const deleteConfirmId = ref<number | null>(null)
const deletingId = ref<number | null>(null)

const { handleSubmit, errors, defineField, resetForm, setValues, isSubmitting } = useForm({
  validationSchema: computed(() =>
    toTypedSchema(editItem.value ? updateCategorySchema : createCategorySchema),
  ),
})

const [name, nameAttrs] = defineField('name')
const [type, typeAttrs] = defineField('type')
const [color, colorAttrs] = defineField('color')
const [description, descriptionAttrs] = defineField('description')

function openCreate() {
  editItem.value = null
  resetForm({ values: { type: 'outflow' } })
  formOpen.value = true
}

function openEdit(cat: Category) {
  editItem.value = cat
  setValues({
    name: cat.name,
    type: cat.type,
    color: cat.color ?? undefined,
    description: cat.description ?? undefined,
  })
  formOpen.value = true
}

function closeForm() {
  formOpen.value = false
  editItem.value = null
  resetForm()
}

const onSubmit = handleSubmit(async (values) => {
  try {
    if (editItem.value) {
      await apiClient.patch(`/categories/${editItem.value.id}`, values)
      toast.success('Category updated')
    } else {
      await apiClient.post('/categories', values)
      toast.success('Category created')
    }
    await queryClient.invalidateQueries({ queryKey: ['categories'] })
    closeForm()
  } catch {
    toast.error('Failed to save category. Please try again.')
  }
})

async function confirmDelete(id: number) {
  deletingId.value = id
  deleteConfirmId.value = null
  try {
    await apiClient.delete(`/categories/${id}`)
    await queryClient.invalidateQueries({ queryKey: ['categories'] })
    toast.success('Category deleted')
  } catch {
    toast.error('Cannot delete — category is in use by existing outflows.')
  } finally {
    deletingId.value = null
  }
}

const typeBadgeClass: Record<string, string> = {
  outflow: 'bg-red-100 text-red-700',
  inflow: 'bg-emerald-100 text-emerald-700',
  any: 'bg-gray-100 text-gray-600',
}
</script>

<template>
  <div class="max-w-6xl mx-auto px-6 py-8">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Categories</h1>
        <p class="text-sm text-gray-500 mt-0.5">Organise your inflows and outflows</p>
      </div>
      <button
        type="button"
        class="px-4 py-2.5 bg-primary-600 text-white text-sm font-medium rounded-button hover:bg-primary-700 transition-colors"
        @click="openCreate"
      >
        + Add Category
      </button>
    </div>

    <!-- Loading -->
    <div v-if="isPending" class="flex items-center justify-center py-16">
      <LoadingSpinner size="lg" />
    </div>

    <!-- Empty -->
    <div v-else-if="categories.length === 0" class="flex flex-col items-center justify-center py-16 px-4">
      <div class="border-2 border-dashed border-gray-200 rounded-card bg-gray-50/50 flex flex-col items-center text-center p-12 w-full max-w-sm">
        <svg class="h-14 w-14 text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
        </svg>
        <h3 class="text-base font-semibold text-gray-700 mb-1">No categories yet</h3>
        <p class="text-sm text-gray-400 mb-6">Add categories to organise your transactions.</p>
        <button
          type="button"
          class="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded-button hover:bg-primary-700 transition-colors"
          @click="openCreate"
        >
          Add Category
        </button>
      </div>
    </div>

    <!-- Table -->
    <div v-else class="bg-white rounded-card shadow-card overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-100">
          <tr>
            <th class="text-left px-5 py-3.5 text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
            <th class="text-left px-5 py-3.5 text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
            <th class="text-left px-5 py-3.5 text-xs font-medium text-gray-500 uppercase tracking-wider">Color</th>
            <th class="text-left px-5 py-3.5 text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
            <th class="text-right px-5 py-3.5 text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-50">
          <tr
            v-for="cat in categories"
            :key="cat.id"
            class="hover:bg-primary-50/30 transition-colors even:bg-gray-50/50"
          >
            <td class="px-5 py-4 font-medium text-gray-900">{{ cat.name }}</td>
            <td class="px-5 py-4">
              <span
                :class="['inline-block px-2.5 py-0.5 rounded-full text-xs font-medium capitalize', typeBadgeClass[cat.type] ?? 'bg-gray-100 text-gray-600']"
              >
                {{ cat.type }}
              </span>
            </td>
            <td class="px-5 py-4">
              <span
                v-if="cat.color"
                class="inline-block h-5 w-5 rounded-full border-2 border-white shadow-sm"
                :style="{ backgroundColor: cat.color }"
                :title="cat.color"
              />
              <span v-else class="text-gray-300">—</span>
            </td>
            <td class="px-5 py-4 text-gray-400 text-xs">{{ cat.description ?? '—' }}</td>
            <td class="px-5 py-4 text-right">
              <div class="flex items-center justify-end gap-1">
                <button
                  type="button"
                  class="px-2.5 py-1 text-xs font-medium text-gray-600 rounded hover:bg-gray-100 transition-colors"
                  @click="openEdit(cat)"
                >
                  Edit
                </button>

                <template v-if="deleteConfirmId === cat.id">
                  <span class="text-xs text-gray-400">Sure?</span>
                  <button
                    type="button"
                    class="px-2.5 py-1 text-xs font-medium text-white bg-red-600 rounded hover:bg-red-700 transition-colors"
                    :disabled="deletingId === cat.id"
                    @click="confirmDelete(cat.id)"
                  >
                    {{ deletingId === cat.id ? '…' : 'Yes' }}
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
                  @click="deleteConfirmId = cat.id"
                >
                  Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add / Edit drawer -->
    <SlideOver :open="formOpen" :title="editItem ? 'Edit Category' : 'Add Category'" @update:open="closeForm">
      <form class="flex flex-col gap-5 p-6" @submit.prevent="onSubmit">

        <!-- Name -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Name</label>
          <input
            v-bind="nameAttrs"
            v-model="name"
            type="text"
            placeholder="e.g. Groceries"
            class="w-full border border-gray-200 rounded-input px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
          />
          <p v-if="errors.name" class="text-red-500 text-xs mt-1">{{ errors.name }}</p>
        </div>

        <!-- Type -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Type</label>
          <select
            v-bind="typeAttrs"
            v-model="type"
            class="w-full border border-gray-200 rounded-input px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors bg-white"
          >
            <option value="outflow">Outflow</option>
            <option value="inflow">Inflow</option>
            <option value="any">Any</option>
          </select>
          <p v-if="errors.type" class="text-red-500 text-xs mt-1">{{ errors.type }}</p>
        </div>

        <!-- Color -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">
            Color <span class="text-gray-400 font-normal">(optional)</span>
          </label>
          <div class="flex items-center gap-3">
            <input
              v-bind="colorAttrs"
              v-model="color"
              type="color"
              class="h-10 w-20 border border-gray-200 rounded-input cursor-pointer p-1"
            />
            <button
              v-if="color"
              type="button"
              class="text-xs text-gray-400 hover:text-gray-600 transition-colors"
              @click="color = undefined"
            >
              Clear
            </button>
          </div>
          <p v-if="errors.color" class="text-red-500 text-xs mt-1">{{ errors.color }}</p>
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">
            Description <span class="text-gray-400 font-normal">(optional)</span>
          </label>
          <textarea
            v-bind="descriptionAttrs"
            v-model="description"
            rows="2"
            placeholder="Optional notes…"
            class="w-full border border-gray-200 rounded-input px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors resize-none"
          />
          <p v-if="errors.description" class="text-red-500 text-xs mt-1">{{ errors.description }}</p>
        </div>

        <!-- Actions -->
        <div class="flex gap-3 pt-2 mt-auto">
          <button
            type="button"
            class="flex-1 px-4 py-2.5 text-sm font-medium text-gray-600 bg-transparent border border-gray-200 rounded-button hover:bg-gray-50 transition-colors"
            @click="closeForm"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="flex-1 px-4 py-2.5 text-sm font-medium text-white bg-primary-600 rounded-button hover:bg-primary-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {{ isSubmitting ? 'Saving…' : (editItem ? 'Save Changes' : 'Add Category') }}
          </button>
        </div>

      </form>
    </SlideOver>
  </div>
</template>

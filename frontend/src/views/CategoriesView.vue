<script setup lang="ts">
import { ref, computed } from 'vue'
import { useQueryClient } from '@tanstack/vue-query'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import type { Category } from '@/types/api'
import { useCategories } from '@/composables/useCategories'
import { createCategorySchema, updateCategorySchema } from '@/lib/validations/category'
import { apiClient } from '@/lib/api/client'

const queryClient = useQueryClient()

const { data, isPending } = useCategories()

const categories = computed(() => data.value?.data ?? [])

const formOpen = ref(false)
const editItem = ref<Category | null>(null)
const deleteConfirmId = ref<number | null>(null)

// Form
const { handleSubmit, errors, defineField, resetForm, setValues } = useForm({
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
  if (editItem.value) {
    await apiClient.patch(`/categories/${editItem.value.id}`, values)
  } else {
    await apiClient.post('/categories', values)
  }
  await queryClient.invalidateQueries({ queryKey: ['categories'] })
  closeForm()
})

async function confirmDelete(id: number) {
  await apiClient.delete(`/categories/${id}`)
  await queryClient.invalidateQueries({ queryKey: ['categories'] })
  deleteConfirmId.value = null
}

const typeBadgeClass: Record<string, string> = {
  outflow: 'bg-red-100 text-red-700',
  inflow: 'bg-green-100 text-green-700',
  any: 'bg-gray-100 text-gray-700',
}
</script>

<template>
  <div class="max-w-5xl mx-auto px-6 py-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Categories</h1>
      <button
        type="button"
        class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors"
        @click="openCreate"
      >
        + Add Category
      </button>
    </div>

    <!-- Table -->
    <div v-if="isPending" class="text-sm text-gray-500">Loading…</div>

    <div v-else-if="categories.length === 0" class="text-center py-16 text-gray-400 text-sm">
      No categories yet. Add one to get started.
    </div>

    <div v-else class="bg-white rounded-lg border border-gray-200 overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="text-left px-4 py-3 font-medium text-gray-600">Name</th>
            <th class="text-left px-4 py-3 font-medium text-gray-600">Type</th>
            <th class="text-left px-4 py-3 font-medium text-gray-600">Color</th>
            <th class="text-left px-4 py-3 font-medium text-gray-600">Description</th>
            <th class="text-right px-4 py-3 font-medium text-gray-600">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="cat in categories" :key="cat.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 font-medium text-gray-900">{{ cat.name }}</td>
            <td class="px-4 py-3">
              <span
                :class="['inline-block px-2 py-0.5 rounded-full text-xs font-medium capitalize', typeBadgeClass[cat.type] ?? 'bg-gray-100 text-gray-700']"
              >
                {{ cat.type }}
              </span>
            </td>
            <td class="px-4 py-3">
              <span
                v-if="cat.color"
                class="inline-block h-5 w-5 rounded-full border border-gray-200"
                :style="{ backgroundColor: cat.color }"
                :title="cat.color"
              />
              <span v-else class="text-gray-400">—</span>
            </td>
            <td class="px-4 py-3 text-gray-600">{{ cat.description ?? '—' }}</td>
            <td class="px-4 py-3 text-right">
              <div class="flex items-center justify-end gap-2">
                <button
                  type="button"
                  class="text-xs px-2 py-1 rounded text-blue-600 hover:bg-blue-50 transition-colors"
                  @click="openEdit(cat)"
                >
                  Edit
                </button>
                <button
                  v-if="deleteConfirmId !== cat.id"
                  type="button"
                  class="text-xs px-2 py-1 rounded text-red-600 hover:bg-red-50 transition-colors"
                  @click="deleteConfirmId = cat.id"
                >
                  Delete
                </button>
                <template v-else>
                  <span class="text-xs text-gray-500">Sure?</span>
                  <button
                    type="button"
                    class="text-xs px-2 py-1 rounded text-white bg-red-600 hover:bg-red-700 transition-colors"
                    @click="confirmDelete(cat.id)"
                  >
                    Yes
                  </button>
                  <button
                    type="button"
                    class="text-xs px-2 py-1 rounded text-gray-600 hover:bg-gray-100 transition-colors"
                    @click="deleteConfirmId = null"
                  >
                    No
                  </button>
                </template>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="formOpen" class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-black/40" @click="closeForm" />
      <div class="relative bg-white rounded-lg shadow-xl w-full max-w-md p-6 mx-4">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">
          {{ editItem ? 'Edit Category' : 'Add Category' }}
        </h2>

        <form class="space-y-4" @submit.prevent="onSubmit">
          <!-- Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
            <input
              v-bind="nameAttrs"
              v-model="name"
              type="text"
              placeholder="e.g. Groceries"
              class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p v-if="errors.name" class="text-red-500 text-xs mt-1">{{ errors.name }}</p>
          </div>

          <!-- Type -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Type</label>
            <select
              v-bind="typeAttrs"
              v-model="type"
              class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
            >
              <option value="outflow">Outflow</option>
              <option value="inflow">Inflow</option>
              <option value="any">Any</option>
            </select>
            <p v-if="errors.type" class="text-red-500 text-xs mt-1">{{ errors.type }}</p>
          </div>

          <!-- Color -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Color <span class="text-gray-400">(optional)</span>
            </label>
            <div class="flex items-center gap-3">
              <input
                v-bind="colorAttrs"
                v-model="color"
                type="color"
                class="h-9 w-16 border border-gray-300 rounded-md cursor-pointer p-0.5"
              />
              <button
                v-if="color"
                type="button"
                class="text-xs text-gray-400 hover:text-gray-600"
                @click="color = undefined"
              >
                Clear
              </button>
            </div>
            <p v-if="errors.color" class="text-red-500 text-xs mt-1">{{ errors.color }}</p>
          </div>

          <!-- Description -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Description <span class="text-gray-400">(optional)</span>
            </label>
            <textarea
              v-bind="descriptionAttrs"
              v-model="description"
              rows="2"
              placeholder="Optional notes…"
              class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            />
            <p v-if="errors.description" class="text-red-500 text-xs mt-1">{{ errors.description }}</p>
          </div>

          <div class="flex justify-end gap-3 pt-2">
            <button
              type="button"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
              @click="closeForm"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors"
            >
              {{ editItem ? 'Save Changes' : 'Add Category' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

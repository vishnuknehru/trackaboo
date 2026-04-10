<script setup lang="ts">
import { ref, watch } from 'vue'

interface Props {
  modelValue: number | undefined
  currency?: string
  placeholder?: string
}

const props = withDefaults(defineProps<Props>(), {
  currency: '$',
  placeholder: '0.00',
})

const emit = defineEmits<{
  'update:modelValue': [value: number | undefined]
}>()

defineOptions({ inheritAttrs: false })

const displayValue = ref('')

watch(
  () => props.modelValue,
  (val) => {
    if (val === undefined || val === null) {
      displayValue.value = ''
    } else if (document.activeElement !== inputRef.value) {
      displayValue.value = formatForDisplay(val)
    }
  },
  { immediate: true },
)

const inputRef = ref<HTMLInputElement | null>(null)

function formatForDisplay(val: number): string {
  return val.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function onFocus() {
  if (props.modelValue !== undefined) {
    displayValue.value = String(props.modelValue)
  }
}

function onBlur() {
  const parsed = parseFloat(displayValue.value.replace(/[^0-9.]/g, ''))
  if (isNaN(parsed)) {
    displayValue.value = ''
    emit('update:modelValue', undefined)
  } else {
    emit('update:modelValue', parsed)
    displayValue.value = formatForDisplay(parsed)
  }
}

function onInput(e: Event) {
  const raw = (e.target as HTMLInputElement).value
  displayValue.value = raw
  const cleaned = raw.replace(/[^0-9.]/g, '')
  const parsed = parseFloat(cleaned)
  emit('update:modelValue', isNaN(parsed) ? undefined : parsed)
}
</script>

<template>
  <div class="relative">
    <span class="absolute inset-y-0 left-3 flex items-center text-sm text-gray-400 pointer-events-none select-none">
      {{ currency }}
    </span>
    <input
      ref="inputRef"
      v-bind="$attrs"
      type="text"
      inputmode="decimal"
      :value="displayValue"
      :placeholder="placeholder"
      class="w-full pl-7 pr-3 py-2.5 border border-gray-200 rounded-input text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
      @focus="onFocus"
      @blur="onBlur"
      @input="onInput"
    />
  </div>
</template>

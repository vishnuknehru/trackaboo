<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

interface MenuItem {
  label: string
  to: string
}

interface Props {
  label?: string
  items: MenuItem[]
  iconOnly?: boolean
}

withDefaults(defineProps<Props>(), {
  iconOnly: false,
})

const route = useRoute()
const isOpen = ref(false)
const containerRef = ref<HTMLElement | null>(null)

function toggle() {
  isOpen.value = !isOpen.value
}

function close() {
  isOpen.value = false
}

function isAnyChildActive(items: MenuItem[]): boolean {
  return items.some((item) => route.path.startsWith(item.to))
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') close()
}

function handleClickOutside(e: MouseEvent) {
  if (containerRef.value && !containerRef.value.contains(e.target as Node)) {
    close()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div ref="containerRef" class="relative">
    <!-- Icon-only trigger (for settings gear) -->
    <button
      v-if="iconOnly"
      type="button"
      :class="[
        'p-2 rounded-button transition-colors',
        isAnyChildActive(items)
          ? 'text-primary-600'
          : 'text-gray-500 hover:text-gray-900 hover:bg-gray-100',
      ]"
      :aria-expanded="isOpen"
      @click.stop="toggle"
    >
      <slot name="icon">
        <!-- Default gear icon -->
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.75">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </slot>
    </button>

    <!-- Label trigger (for Expense dropdown) -->
    <button
      v-else
      type="button"
      :class="[
        'flex items-center gap-1 text-sm font-medium pb-1 transition-colors',
        isAnyChildActive(items)
          ? 'text-primary-600 border-b-2 border-primary-600'
          : 'text-gray-600 hover:text-gray-900',
      ]"
      :aria-expanded="isOpen"
      @click.stop="toggle"
    >
      {{ label }}
      <svg
        :class="['h-4 w-4 transition-transform duration-150', isOpen ? 'rotate-180' : '']"
        fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Dropdown panel -->
    <Transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isOpen"
        class="absolute right-0 mt-2 w-44 origin-top-right bg-white rounded-lg shadow-lg ring-1 ring-black/5 py-1 z-50"
      >
        <RouterLink
          v-for="item in items"
          :key="item.to"
          :to="item.to"
          :class="[
            'block px-4 py-2 text-sm transition-colors',
            route.path.startsWith(item.to)
              ? 'text-primary-600 bg-primary-50'
              : 'text-gray-700 hover:bg-gray-50',
          ]"
          @click="close"
        >
          {{ item.label }}
        </RouterLink>
      </div>
    </Transition>
  </div>
</template>

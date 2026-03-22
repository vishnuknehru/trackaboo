<script setup lang="ts">
interface Props {
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
})

const sizeClasses = {
  sm: 'h-4 w-4 border-2',
  md: 'h-8 w-8 border-2',
  lg: 'h-12 w-12 border-4',
}
</script>

<template>
  <div
    :class="[
      'animate-spin rounded-full border-gray-300 border-t-blue-600',
      sizeClasses[props.size],
    ]"
    role="status"
    aria-label="Loading"
  />
</template>

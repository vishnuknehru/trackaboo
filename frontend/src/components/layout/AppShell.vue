<script setup lang="ts">
import TopNav from './TopNav.vue'
</script>

<template>
  <div class="flex flex-col h-screen bg-gray-50 overflow-hidden">
    <TopNav />
    <main class="flex-1 overflow-y-auto">
      <slot />
    </main>
  </div>
</template>

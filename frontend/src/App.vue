<script setup lang="ts">
import { Toaster } from 'vue-sonner'
import AppShell from '@/components/layout/AppShell.vue'
</script>

<template>
  <AppShell>
    <RouterView />
  </AppShell>
  <Toaster richColors position="top-right" />
</template>

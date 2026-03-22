import { ref } from 'vue'
import { defineStore } from 'pinia'
import { currentMonth } from '@/lib/formatters'

export const useMonthStore = defineStore('month', () => {
  const month = ref(currentMonth())

  function setMonth(m: string) {
    month.value = m
  }

  return { month, setMonth }
})

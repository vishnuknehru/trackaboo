import { computed, type Ref } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { apiClient } from '@/lib/api/client'
import type { MonthlyMetrics } from '@/types/api'

export function useMetrics(month: Ref<string>) {
  return useQuery({
    queryKey: computed(() => ['metrics', month.value]),
    queryFn: () => apiClient.get<MonthlyMetrics>(`/metrics?month=${month.value}`),
    enabled: computed(() => !!month.value),
  })
}

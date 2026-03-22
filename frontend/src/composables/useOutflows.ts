import { computed, type Ref } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { apiClient } from '@/lib/api/client'
import type { Outflow, PaginatedResponse } from '@/types/api'

interface OutflowParams {
  month?: string
  page: number
  limit: number
}

export function useOutflows(params: Ref<OutflowParams>) {
  return useQuery({
    queryKey: computed(() => ['outflows', params.value]),
    queryFn: () => {
      const q = new URLSearchParams()
      if (params.value.month) q.set('month', params.value.month)
      q.set('page', String(params.value.page))
      q.set('limit', String(params.value.limit))
      return apiClient.get<PaginatedResponse<Outflow>>(`/outflows?${q}`)
    },
  })
}

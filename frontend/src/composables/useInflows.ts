import { computed, type Ref } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { apiClient } from '@/lib/api/client'
import type { Inflow, PaginatedResponse } from '@/types/api'

interface InflowParams {
  month?: string
  page: number
  limit: number
}

export function useInflows(params: Ref<InflowParams>) {
  return useQuery({
    queryKey: computed(() => ['inflows', params.value]),
    queryFn: () => {
      const q = new URLSearchParams()
      if (params.value.month) q.set('month', params.value.month)
      q.set('page', String(params.value.page))
      q.set('limit', String(params.value.limit))
      return apiClient.get<PaginatedResponse<Inflow>>(`/inflows?${q}`)
    },
  })
}

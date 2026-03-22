import { computed, type Ref } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { apiClient } from '@/lib/api/client'
import type { Category } from '@/types/api'

export function useCategories(type?: Ref<string | undefined>) {
  return useQuery({
    queryKey: computed(() => ['categories', type?.value]),
    queryFn: () => {
      const path = type?.value ? `/categories?type=${type.value}` : '/categories'
      return apiClient.get<{ data: Category[] }>(path)
    },
  })
}

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { ref } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { useCategories } from './useCategories'
import { apiClient } from '@/lib/api/client'
import type { UseQueryReturnType } from '@tanstack/vue-query'

vi.mock('@tanstack/vue-query', () => ({
  useQuery: vi.fn(),
}))

vi.mock('@/lib/api/client', () => ({
  apiClient: {
    get: vi.fn(),
  },
}))

function mockQueryReturn() {
  return { data: { value: null }, isPending: { value: false } } as unknown as UseQueryReturnType<unknown, unknown>
}

describe('useCategories', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('calls /categories without type param when no type provided', async () => {
    vi.mocked(useQuery).mockReturnValue(mockQueryReturn())
    vi.mocked(apiClient.get).mockResolvedValue({ data: [] } as never)

    useCategories()

    const callArg = vi.mocked(useQuery).mock.calls[0]?.[0] as unknown as {
      queryFn: () => unknown
    }
    expect(callArg).toBeDefined()
    await callArg.queryFn()

    expect(apiClient.get).toHaveBeenCalledWith('/categories')
  })

  it('includes type param when type is "outflow"', async () => {
    const type = ref<string | undefined>('outflow')
    vi.mocked(useQuery).mockReturnValue(mockQueryReturn())
    vi.mocked(apiClient.get).mockResolvedValue({ data: [] } as never)

    useCategories(type)

    const callArg = vi.mocked(useQuery).mock.calls[0]?.[0] as unknown as {
      queryFn: () => unknown
    }
    expect(callArg).toBeDefined()
    await callArg.queryFn()

    expect(apiClient.get).toHaveBeenCalledWith('/categories?type=outflow')
  })

  it('calls /categories without type param when type is undefined', async () => {
    const type = ref<string | undefined>(undefined)
    vi.mocked(useQuery).mockReturnValue(mockQueryReturn())
    vi.mocked(apiClient.get).mockResolvedValue({ data: [] } as never)

    useCategories(type)

    const callArg = vi.mocked(useQuery).mock.calls[0]?.[0] as unknown as {
      queryFn: () => unknown
    }
    expect(callArg).toBeDefined()
    await callArg.queryFn()

    expect(apiClient.get).toHaveBeenCalledWith('/categories')
  })

  it('queryKey is defined for cache differentiation', () => {
    const type = ref<string | undefined>('inflow')
    vi.mocked(useQuery).mockReturnValue(mockQueryReturn())

    useCategories(type)

    const callArg = vi.mocked(useQuery).mock.calls[0]?.[0] as Record<string, unknown>
    expect(callArg).toBeDefined()
    expect(callArg['queryKey']).toBeDefined()
  })
})

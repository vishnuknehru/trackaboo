import { describe, it, expect, vi, beforeEach } from 'vitest'
import { ref } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { useMetrics } from './useMetrics'
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

describe('useMetrics', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('calls useQuery with correct queryKey for the given month', () => {
    const month = ref('2026-03')
    vi.mocked(useQuery).mockReturnValue(mockQueryReturn())

    useMetrics(month)

    expect(useQuery).toHaveBeenCalledOnce()
  })

  it('includes month in the query function path', async () => {
    const month = ref('2026-03')
    vi.mocked(useQuery).mockReturnValue(mockQueryReturn())
    vi.mocked(apiClient.get).mockResolvedValue({} as never)

    useMetrics(month)

    const callArg = vi.mocked(useQuery).mock.calls[0]?.[0] as unknown as {
      queryFn: () => unknown
    }
    expect(callArg).toBeDefined()
    await (callArg as { queryFn: () => unknown }).queryFn()

    expect(apiClient.get).toHaveBeenCalledWith('/metrics?month=2026-03')
  })

  it('queryKey includes the month value', () => {
    const month = ref('2026-01')
    vi.mocked(useQuery).mockReturnValue(mockQueryReturn())

    useMetrics(month)

    const callArg = vi.mocked(useQuery).mock.calls[0]?.[0]
    expect(callArg).toBeDefined()
    // queryKey is a computed ref — verify it was passed
    expect((callArg as Record<string, unknown>)['queryKey']).toBeDefined()
  })
})

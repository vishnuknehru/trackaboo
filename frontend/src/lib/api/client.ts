import { ofetch } from 'ofetch'

const BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'

export const apiClient = {
  get: <T>(path: string) => ofetch<T>(`${BASE}${path}`),
  post: <T>(path: string, body: unknown) =>
    ofetch<T>(`${BASE}${path}`, { method: 'POST', body: body as Record<string, unknown> }),
  patch: <T>(path: string, body: unknown) =>
    ofetch<T>(`${BASE}${path}`, { method: 'PATCH', body: body as Record<string, unknown> }),
  delete: (path: string) => ofetch(`${BASE}${path}`, { method: 'DELETE' }),
}

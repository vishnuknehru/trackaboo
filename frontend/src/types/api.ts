export interface Category {
  id: number
  name: string
  type: 'outflow' | 'inflow' | 'any'
  color: string | null
  description: string | null
  createdAt: string
  updatedAt: string
}

export interface Inflow {
  id: number
  amount: number
  date: string
  source: string
  description: string | null
  categoryId: number | null
  createdAt: string
  updatedAt: string
}

export interface Outflow {
  id: number
  amount: number
  date: string
  categoryId: number
  description: string | null
  createdAt: string
  updatedAt: string
}

export interface CategoryBreakdownItem {
  categoryId: number
  categoryName: string
  amount: number
  percentage: number
  color: string | null
}

export interface MonthlyMetrics {
  month: string
  totalInflow: number
  totalOutflow: number
  netFlow: number
  categoryBreakdown: CategoryBreakdownItem[]
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  limit: number
}

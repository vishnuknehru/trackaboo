export function formatCurrency(amount: number, currency = 'USD', locale = 'en-US'): string {
  return new Intl.NumberFormat(locale, { style: 'currency', currency }).format(amount)
}

export function formatDate(date: string, locale = 'en-US'): string {
  // Parse as UTC to avoid timezone drift
  const d = new Date(date + 'T00:00:00Z')
  return d.toLocaleDateString(locale, { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' })
}

export function formatPercentage(value: number): string {
  return value.toFixed(1) + '%'
}

export function currentMonth(): string {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  return `${year}-${month}`
}

export function shiftMonth(month: string, delta: number): string {
  const parts = month.split('-')
  const yearStr = parts[0] ?? ''
  const monthStr = parts[1] ?? ''
  const year = parseInt(yearStr, 10)
  const m = parseInt(monthStr, 10)
  const date = new Date(year, m - 1 + delta, 1)
  const newYear = date.getFullYear()
  const newMonth = String(date.getMonth() + 1).padStart(2, '0')
  return `${newYear}-${newMonth}`
}

export function formatMonth(month: string, locale = 'en-US'): string {
  const parts = month.split('-')
  const yearStr = parts[0] ?? ''
  const monthStr = parts[1] ?? ''
  const year = parseInt(yearStr, 10)
  const m = parseInt(monthStr, 10)
  const date = new Date(Date.UTC(year, m - 1, 1))
  return date.toLocaleDateString(locale, { year: 'numeric', month: 'long', timeZone: 'UTC' })
}

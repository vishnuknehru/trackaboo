import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import {
  formatCurrency,
  formatDate,
  formatPercentage,
  currentMonth,
  shiftMonth,
  formatMonth,
} from './formatters'

describe('formatCurrency', () => {
  it('formats a positive USD amount', () => {
    expect(formatCurrency(1234.56)).toBe('$1,234.56')
  })

  it('formats zero', () => {
    expect(formatCurrency(0)).toBe('$0.00')
  })

  it('formats a negative amount', () => {
    expect(formatCurrency(-500)).toBe('-$500.00')
  })

  it('formats a large amount', () => {
    expect(formatCurrency(1000000)).toBe('$1,000,000.00')
  })

  it('respects the currency parameter', () => {
    const result = formatCurrency(100, 'EUR', 'de-DE')
    expect(result).toContain('100')
    expect(result).toContain('€')
  })
})

describe('formatDate', () => {
  it('formats a YYYY-MM-DD date as UTC', () => {
    // Mar 1, 2026 UTC should be "Mar 1, 2026"
    expect(formatDate('2026-03-01')).toBe('Mar 1, 2026')
  })

  it('formats a date at month boundary without off-by-one errors', () => {
    // Jan 1 should not become Dec 31 due to timezone
    expect(formatDate('2026-01-01')).toBe('Jan 1, 2026')
  })

  it('formats a different date', () => {
    expect(formatDate('2025-12-25')).toBe('Dec 25, 2025')
  })
})

describe('formatPercentage', () => {
  it('rounds to 1 decimal', () => {
    expect(formatPercentage(46.9)).toBe('46.9%')
  })

  it('formats zero', () => {
    expect(formatPercentage(0)).toBe('0.0%')
  })

  it('formats 100', () => {
    expect(formatPercentage(100)).toBe('100.0%')
  })

  it('rounds correctly', () => {
    expect(formatPercentage(33.333)).toBe('33.3%')
  })
})

describe('currentMonth', () => {
  it('returns YYYY-MM format', () => {
    const result = currentMonth()
    expect(result).toMatch(/^\d{4}-\d{2}$/)
  })

  it('matches today\'s year and month', () => {
    const now = new Date()
    const expected = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
    expect(currentMonth()).toBe(expected)
  })
})

describe('shiftMonth', () => {
  it('moves forward one month', () => {
    expect(shiftMonth('2026-01', 1)).toBe('2026-02')
  })

  it('moves backward one month', () => {
    expect(shiftMonth('2026-03', -1)).toBe('2026-02')
  })

  it('handles year boundary forward (Dec → Jan)', () => {
    expect(shiftMonth('2025-12', 1)).toBe('2026-01')
  })

  it('handles year boundary backward (Jan → Dec)', () => {
    expect(shiftMonth('2026-01', -1)).toBe('2025-12')
  })

  it('shifts multiple months', () => {
    expect(shiftMonth('2026-01', 6)).toBe('2026-07')
  })

  it('shifts backward multiple months crossing year boundary', () => {
    expect(shiftMonth('2026-02', -14)).toBe('2024-12')
  })
})

describe('formatMonth', () => {
  it('formats YYYY-MM as full month name and year', () => {
    expect(formatMonth('2026-03')).toBe('March 2026')
  })

  it('formats January', () => {
    expect(formatMonth('2026-01')).toBe('January 2026')
  })

  it('formats December', () => {
    expect(formatMonth('2025-12')).toBe('December 2025')
  })
})

import { useState, useEffect } from 'react'
import { api } from '../services/api'
import type { PortfolioSummary } from '../types/api'

interface UsePortfolioResult {
  data: PortfolioSummary | null
  loading: boolean
  error: string | null
  retry: () => void
}

export function usePortfolio(): UsePortfolioResult {
  const [data, setData] = useState<PortfolioSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  async function fetchData() {
    setLoading(true)
    setError(null)
    try {
      const summary = await api.getPortfolioSummary()
      setData(summary)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load portfolio data')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  return { data, loading, error, retry: fetchData }
}

import type { PortfolioSummary, ContactMessagePayload } from '../types/api'

const API_BASE = '/api/v1'

class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message)
    this.name = 'APIError'
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ error: 'Unknown error' }))
    throw new APIError(response.status, errorData.detail || errorData.error || 'Request failed')
  }
  return response.json()
}

export const portfolioAPI = {
  /**
   * Fetches the complete portfolio summary in a single request.
   * This is the primary endpoint for initial page load.
   */
  async getPortfolioSummary(): Promise<PortfolioSummary> {
    const response = await fetch(`${API_BASE}/summary/`)
    return handleResponse<PortfolioSummary>(response)
  },

  /**
   * Sends a contact form message.
   */
  async sendContactMessage(payload: ContactMessagePayload): Promise<void> {
    const response = await fetch(`${API_BASE}/contact/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    await handleResponse(response)
  },

  /**
   * Gets resume download URL (for direct link).
   */
  getResumeDownloadUrl(): string {
    return `${API_BASE}/resume/download`
  },
}

// Backward compatibility
export const api = portfolioAPI

export { APIError }

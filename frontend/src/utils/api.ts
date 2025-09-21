import axios, { AxiosResponse } from 'axios'
import { ApiResponse, DocumentUploadResponse, ProcessingStatus, ProcessedDocument } from '@/types'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Log the API base URL for debugging
console.log('API Base URL:', api.defaults.baseURL)

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth headers here if needed
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  (error) => {
    // Handle common errors
    if (error.response?.status === 413) {
      throw new Error('File too large. Maximum size is 50MB.')
    }
    if (error.response?.status === 415) {
      throw new Error('Unsupported file type.')
    }
    if (error.response?.status >= 500) {
      throw new Error('Server error. Please try again later.')
    }
    return Promise.reject(error)
  }
)

// API functions
export const apiClient = {
  // Health check
  health: async (): Promise<ApiResponse> => {
    const response = await api.get('/health')
    return response.data
  },

  // Upload document
  uploadDocument: async (file: File): Promise<DocumentUploadResponse> => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // Get processing status
  getStatus: async (jobId: string): Promise<ProcessingStatus> => {
    const response = await api.get(`/status/${jobId}`)
    return response.data
  },

  // Get processed document
  getResult: async (jobId: string): Promise<ProcessedDocument> => {
    const response = await api.get(`/result/${jobId}`)
    return response.data
  },

  // Download processed document
  downloadResult: async (jobId: string, format: 'markdown' | 'html' | 'json' = 'markdown'): Promise<Blob> => {
    const response = await api.get(`/download/${jobId}`, {
      params: { format },
      responseType: 'blob',
    })
    return response.data
  },
}

export default api

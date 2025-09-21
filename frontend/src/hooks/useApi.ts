import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/utils/api'
import { DocumentUploadResponse, ProcessingStatus, ProcessedDocument } from '@/types'
import toast from 'react-hot-toast'

/**
 * Hook for uploading documents
 */
export const useUploadDocument = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (file: File) => apiClient.uploadDocument(file),
    onSuccess: (data: DocumentUploadResponse) => {
      toast.success('Document uploaded successfully!')
      // Invalidate and refetch any related queries
      queryClient.invalidateQueries({ queryKey: ['jobs'] })
    },
    onError: (error: Error) => {
      toast.error(error.message || 'Upload failed')
    },
  })
}

/**
 * Hook for checking job status
 */
export const useJobStatus = (jobId: string, enabled: boolean = true) => {
  return useQuery({
    queryKey: ['job-status', jobId],
    queryFn: () => apiClient.getStatus(jobId),
    enabled: enabled && !!jobId,
    refetchInterval: (data) => {
      // Stop polling if job is completed or failed
      if (data?.status === 'completed' || data?.status === 'failed') {
        return false
      }
      // Poll every 2 seconds for active jobs
      return 2000
    },
    retry: (failureCount, error: any) => {
      // Don't retry if job not found
      if (error?.response?.status === 404) {
        return false
      }
      return failureCount < 3
    },
  })
}

/**
 * Hook for getting job result
 */
export const useJobResult = (jobId: string, enabled: boolean = true) => {
  return useQuery({
    queryKey: ['job-result', jobId],
    queryFn: () => apiClient.getResult(jobId),
    enabled: enabled && !!jobId,
    retry: (failureCount, error: any) => {
      // Don't retry if job not found or not completed
      if (error?.response?.status === 404) {
        return false
      }
      return failureCount < 3
    },
  })
}

/**
 * Hook for downloading results
 */
export const useDownloadResult = () => {
  return useMutation({
    mutationFn: ({ jobId, format }: { jobId: string; format: 'markdown' | 'html' | 'json' }) =>
      apiClient.downloadResult(jobId, format),
    onSuccess: (blob, variables) => {
      // Create download link
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      
      const extensions = {
        markdown: 'md',
        html: 'html',
        json: 'json',
      }
      
      link.download = `document.${extensions[variables.format]}`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
      
      toast.success('Download started!')
    },
    onError: (error: Error) => {
      toast.error(error.message || 'Download failed')
    },
  })
}

/**
 * Hook for health check
 */
export const useHealthCheck = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: () => apiClient.health(),
    refetchInterval: 30000, // Check every 30 seconds
    retry: 1,
  })
}

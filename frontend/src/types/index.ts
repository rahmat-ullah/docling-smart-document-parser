// API Response types
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

// Document processing types
export interface DocumentUploadResponse {
  job_id: string
  filename: string
  file_size: number
  upload_time: string
}

export interface ProcessingStatus {
  job_id: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  progress: number
  message?: string
  started_at?: string
  completed_at?: string
  error?: string
}

export interface ProcessedDocument {
  job_id: string
  original_filename: string
  processed_content: {
    markdown: string
    html: string
    json: any
  }
  metadata: {
    pages: number
    processing_time: number
    elements_detected: number
    model_used: string
  }
  created_at: string
}

// File upload types
export interface FileUpload {
  file: File
  preview?: string
  progress?: number
  status?: 'pending' | 'uploading' | 'uploaded' | 'error'
  error?: string
}

// Supported file types
export const SUPPORTED_FILE_TYPES = {
  'application/pdf': ['.pdf'],
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
  'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
  'text/html': ['.html'],
  'image/png': ['.png'],
  'image/jpeg': ['.jpg', '.jpeg'],
  'image/tiff': ['.tiff', '.tif'],
  'audio/wav': ['.wav'],
  'audio/mpeg': ['.mp3'],
} as const

export const MAX_FILE_SIZE = 50 * 1024 * 1024 // 50MB

// UI Component types
export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  children: React.ReactNode
  onClick?: () => void
  type?: 'button' | 'submit' | 'reset'
  className?: string
}

export interface ProgressBarProps {
  progress: number
  className?: string
  showPercentage?: boolean
}

// Error types
export interface AppError {
  code: string
  message: string
  details?: any
}

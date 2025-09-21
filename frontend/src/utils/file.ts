import { SUPPORTED_FILE_TYPES, MAX_FILE_SIZE } from '@/types'

/**
 * Validate if a file is supported
 */
export const isFileSupported = (file: File): boolean => {
  const supportedTypes = Object.keys(SUPPORTED_FILE_TYPES)
  return supportedTypes.includes(file.type)
}

/**
 * Validate file size
 */
export const isFileSizeValid = (file: File): boolean => {
  return file.size <= MAX_FILE_SIZE
}

/**
 * Get file extension from filename
 */
export const getFileExtension = (filename: string): string => {
  return filename.slice(filename.lastIndexOf('.'))
}

/**
 * Format file size for display
 */
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * Get file type icon
 */
export const getFileTypeIcon = (file: File): string => {
  if (file.type.startsWith('image/')) return '🖼️'
  if (file.type.includes('pdf')) return '📄'
  if (file.type.includes('word')) return '📝'
  if (file.type.includes('presentation')) return '📊'
  if (file.type.includes('spreadsheet')) return '📈'
  if (file.type.includes('html')) return '🌐'
  if (file.type.startsWith('audio/')) return '🎵'
  return '📄'
}

/**
 * Validate file before upload
 */
export const validateFile = (file: File): { valid: boolean; error?: string } => {
  if (!isFileSupported(file)) {
    return {
      valid: false,
      error: `File type "${file.type}" is not supported. Please upload a PDF, DOCX, PPTX, XLSX, HTML, image, or audio file.`
    }
  }
  
  if (!isFileSizeValid(file)) {
    return {
      valid: false,
      error: `File size (${formatFileSize(file.size)}) exceeds the maximum limit of ${formatFileSize(MAX_FILE_SIZE)}.`
    }
  }
  
  return { valid: true }
}

/**
 * Create a preview URL for supported file types
 */
export const createFilePreview = (file: File): string | null => {
  if (file.type.startsWith('image/')) {
    return URL.createObjectURL(file)
  }
  return null
}

/**
 * Download a blob as a file
 */
export const downloadBlob = (blob: Blob, filename: string): void => {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

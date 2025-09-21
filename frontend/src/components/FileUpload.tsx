import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, File, X, AlertCircle, CheckCircle } from 'lucide-react'
import { cn } from '@/utils/cn'
import { SUPPORTED_FILE_TYPES, MAX_FILE_SIZE } from '@/types'
import Button from './ui/Button'

interface FileUploadProps {
  onFileSelect: (file: File) => void
  disabled?: boolean
  className?: string
}

interface FilePreview {
  file: File
  preview?: string
  error?: string
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  disabled = false,
  className,
}) => {
  const [filePreview, setFilePreview] = useState<FilePreview | null>(null)
  
  const validateFile = useCallback((file: File): string | null => {
    // Check file size
    if (file.size > MAX_FILE_SIZE) {
      return `File size (${(file.size / 1024 / 1024).toFixed(1)}MB) exceeds maximum allowed size (${MAX_FILE_SIZE / 1024 / 1024}MB)`
    }

    // Check file type
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
    const supportedExtensions = Object.values(SUPPORTED_FILE_TYPES).flat()

    if (!supportedExtensions.includes(fileExtension)) {
      return `File type "${fileExtension}" is not supported. Supported types: ${supportedExtensions.join(', ')}`
    }

    return null
  }, [])
  
  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
    if (rejectedFiles.length > 0) {
      const rejection = rejectedFiles[0]
      setFilePreview({
        file: rejection.file,
        error: rejection.errors[0]?.message || 'File rejected',
      })
      return
    }
    
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0]
      const error = validateFile(file)
      
      if (error) {
        setFilePreview({ file, error })
        return
      }
      
      // Create preview for images
      let preview: string | undefined
      if (file.type.startsWith('image/')) {
        preview = URL.createObjectURL(file)
      }
      
      setFilePreview({ file, preview })
      onFileSelect(file)
    }
  }, [onFileSelect, validateFile])
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: SUPPORTED_FILE_TYPES,
    maxSize: MAX_FILE_SIZE,
    multiple: false,
    disabled,
  })
  
  const clearFile = () => {
    if (filePreview?.preview) {
      URL.revokeObjectURL(filePreview.preview)
    }
    setFilePreview(null)
  }
  
  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }
  
  return (
    <div className={cn('w-full', className)}>
      {!filePreview ? (
        <div
          {...getRootProps()}
          className={cn(
            'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors',
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-gray-400',
            disabled && 'opacity-50 cursor-not-allowed'
          )}
        >
          <input {...getInputProps()} />
          
          <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          
          <div className="space-y-2">
            <p className="text-lg font-medium text-gray-900">
              {isDragActive ? 'Drop your file here' : 'Upload a document'}
            </p>
            <p className="text-sm text-gray-600">
              Drag and drop your file here, or click to browse
            </p>
            <p className="text-xs text-gray-500">
              Supports: PDF, DOCX, PPTX, XLSX, HTML, PNG, JPG, TIFF, WAV, MP3
            </p>
            <p className="text-xs text-gray-500">
              Maximum file size: {MAX_FILE_SIZE / 1024 / 1024}MB
            </p>
          </div>
        </div>
      ) : (
        <div className="border border-gray-200 rounded-lg p-4">
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-3">
              {filePreview.preview ? (
                <img
                  src={filePreview.preview}
                  alt="Preview"
                  className="w-12 h-12 object-cover rounded"
                />
              ) : (
                <File className="h-12 w-12 text-gray-400" />
              )}
              
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {filePreview.file.name}
                </p>
                <p className="text-sm text-gray-500">
                  {formatFileSize(filePreview.file.size)}
                </p>
                
                {filePreview.error ? (
                  <div className="flex items-center mt-2 text-red-600">
                    <AlertCircle className="h-4 w-4 mr-1" />
                    <span className="text-xs">{filePreview.error}</span>
                  </div>
                ) : (
                  <div className="flex items-center mt-2 text-green-600">
                    <CheckCircle className="h-4 w-4 mr-1" />
                    <span className="text-xs">File ready for upload</span>
                  </div>
                )}
              </div>
            </div>
            
            <Button
              variant="outline"
              size="sm"
              onClick={clearFile}
              className="ml-2"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
          
          {!filePreview.error && (
            <div className="mt-4">
              <Button
                onClick={() => onFileSelect(filePreview.file)}
                disabled={disabled}
                className="w-full"
              >
                Process Document
              </Button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default FileUpload

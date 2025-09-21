import React, { useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Download, Eye, RefreshCw } from 'lucide-react'
import { useJobStatus, useJobResult, useDownloadResult } from '@/hooks/useApi'
import ProcessingStatusComponent from '@/components/ProcessingStatus'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import Button from '@/components/ui/Button'
import LoadingSpinner from '@/components/LoadingSpinner'
import toast from 'react-hot-toast'

const Process: React.FC = () => {
  const { jobId } = useParams<{ jobId: string }>()
  const navigate = useNavigate()
  
  const {
    data: status,
    isLoading: statusLoading,
    error: statusError,
    refetch: refetchStatus,
  } = useJobStatus(jobId!, !!jobId)
  
  const {
    data: result,
    isLoading: resultLoading,
    refetch: refetchResult,
  } = useJobResult(jobId!, status?.status === 'completed')
  
  const downloadMutation = useDownloadResult()
  
  // Redirect if no job ID
  useEffect(() => {
    if (!jobId) {
      navigate('/')
    }
  }, [jobId, navigate])
  
  // Auto-refresh result when processing completes
  useEffect(() => {
    if (status?.status === 'completed' && !result) {
      refetchResult()
    }
  }, [status?.status, result, refetchResult])
  
  const handleDownload = (format: 'markdown' | 'html' | 'json') => {
    if (!jobId) return
    
    downloadMutation.mutate({ jobId, format })
  }
  
  const handlePreview = () => {
    if (!jobId) return
    
    // Open preview in new tab
    const previewUrl = `${import.meta.env.VITE_API_URL}/api/preview/${jobId}?format=html`
    window.open(previewUrl, '_blank')
  }
  
  const handleRetry = () => {
    refetchStatus()
    if (status?.status === 'completed') {
      refetchResult()
    }
  }
  
  if (!jobId) {
    return null
  }
  
  if (statusLoading) {
    return (
      <div className="max-w-4xl mx-auto">
        <LoadingSpinner size="lg" text="Loading job status..." />
      </div>
    )
  }
  
  if (statusError) {
    return (
      <div className="max-w-4xl mx-auto">
        <Card>
          <CardContent className="text-center py-12">
            <p className="text-red-600 mb-4">Failed to load job status</p>
            <Button onClick={handleRetry}>
              <RefreshCw className="h-4 w-4 mr-2" />
              Retry
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }
  
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button
            variant="outline"
            onClick={() => navigate('/')}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Upload
          </Button>
          
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Document Processing
            </h1>
            <p className="text-gray-600">Job ID: {jobId}</p>
          </div>
        </div>
        
        <Button
          variant="outline"
          onClick={handleRetry}
          disabled={status?.status === 'processing'}
        >
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>
      
      {/* Processing Status */}
      {status && (
        <ProcessingStatusComponent
          status={status.status}
          progress={status.progress}
          message={status.message}
          error={status.error}
          startedAt={status.started_at}
          completedAt={status.completed_at}
        />
      )}
      
      {/* Results Section */}
      {status?.status === 'completed' && (
        <div className="space-y-6">
          {/* Download Options */}
          <Card>
            <CardHeader>
              <CardTitle>Download Results</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <Button
                  variant="outline"
                  onClick={() => handleDownload('markdown')}
                  disabled={downloadMutation.isPending}
                  className="w-full"
                >
                  <Download className="h-4 w-4 mr-2" />
                  Markdown
                </Button>
                
                <Button
                  variant="outline"
                  onClick={() => handleDownload('html')}
                  disabled={downloadMutation.isPending}
                  className="w-full"
                >
                  <Download className="h-4 w-4 mr-2" />
                  HTML
                </Button>
                
                <Button
                  variant="outline"
                  onClick={() => handleDownload('json')}
                  disabled={downloadMutation.isPending}
                  className="w-full"
                >
                  <Download className="h-4 w-4 mr-2" />
                  JSON
                </Button>
                
                <Button
                  onClick={handlePreview}
                  className="w-full"
                >
                  <Eye className="h-4 w-4 mr-2" />
                  Preview
                </Button>
              </div>
            </CardContent>
          </Card>
          
          {/* Document Metadata */}
          {result && (
            <Card>
              <CardHeader>
                <CardTitle>Document Information</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-3">File Details</h4>
                    <dl className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <dt className="text-gray-600">Original filename:</dt>
                        <dd className="font-medium">{result.original_filename}</dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-gray-600">File size:</dt>
                        <dd className="font-medium">
                          {(result.metadata.file_size / 1024 / 1024).toFixed(2)} MB
                        </dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-gray-600">File type:</dt>
                        <dd className="font-medium">{result.metadata.file_type}</dd>
                      </div>
                    </dl>
                  </div>
                  
                  <div>
                    <h4 className="font-medium text-gray-900 mb-3">Processing Results</h4>
                    <dl className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <dt className="text-gray-600">Pages processed:</dt>
                        <dd className="font-medium">{result.metadata.pages}</dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-gray-600">Elements detected:</dt>
                        <dd className="font-medium">{result.metadata.elements_detected}</dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-gray-600">Processing time:</dt>
                        <dd className="font-medium">{result.metadata.processing_time.toFixed(2)}s</dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-gray-600">Model used:</dt>
                        <dd className="font-medium">{result.metadata.model_used}</dd>
                      </div>
                    </dl>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
          
          {/* Content Preview */}
          {result && (
            <Card>
              <CardHeader>
                <CardTitle>Content Preview</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Markdown Output</h4>
                    <pre className="bg-gray-50 p-4 rounded-lg text-sm overflow-auto max-h-64 border">
                      {result.processed_content.markdown.substring(0, 1000)}
                      {result.processed_content.markdown.length > 1000 && '...'}
                    </pre>
                  </div>
                  
                  <p className="text-sm text-gray-600">
                    This is a preview of the first 1000 characters. Download the full content using the buttons above.
                  </p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
      
      {/* Failed State Actions */}
      {status?.status === 'failed' && (
        <Card>
          <CardContent className="text-center py-8">
            <p className="text-gray-600 mb-4">
              Processing failed. You can try uploading the document again.
            </p>
            <Button onClick={() => navigate('/')}>
              Upload New Document
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default Process

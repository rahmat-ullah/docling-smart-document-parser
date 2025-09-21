import React from 'react'
import { Clock, CheckCircle, XCircle, Loader2, AlertTriangle } from 'lucide-react'
import { ProcessingStatus as Status } from '@/types'
import { cn } from '@/utils/cn'
import ProgressBar from './ui/ProgressBar'
import { Card, CardContent } from './ui/Card'

interface ProcessingStatusProps {
  status: Status
  progress?: number
  message?: string
  error?: string
  startedAt?: string
  completedAt?: string
  className?: string
}

const ProcessingStatusComponent: React.FC<ProcessingStatusProps> = ({
  status,
  progress = 0,
  message,
  error,
  startedAt,
  completedAt,
  className,
}) => {
  const getStatusIcon = () => {
    switch (status) {
      case 'pending':
        return <Clock className="h-5 w-5 text-yellow-500" />
      case 'processing':
        return <Loader2 className="h-5 w-5 text-blue-500 animate-spin" />
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'failed':
        return <XCircle className="h-5 w-5 text-red-500" />
      default:
        return <AlertTriangle className="h-5 w-5 text-gray-500" />
    }
  }
  
  const getStatusText = () => {
    switch (status) {
      case 'pending':
        return 'Queued for processing'
      case 'processing':
        return 'Processing document...'
      case 'completed':
        return 'Processing completed'
      case 'failed':
        return 'Processing failed'
      default:
        return 'Unknown status'
    }
  }
  
  const getStatusColor = () => {
    switch (status) {
      case 'pending':
        return 'text-yellow-700 bg-yellow-50 border-yellow-200'
      case 'processing':
        return 'text-blue-700 bg-blue-50 border-blue-200'
      case 'completed':
        return 'text-green-700 bg-green-50 border-green-200'
      case 'failed':
        return 'text-red-700 bg-red-50 border-red-200'
      default:
        return 'text-gray-700 bg-gray-50 border-gray-200'
    }
  }
  
  const formatTime = (timeString?: string) => {
    if (!timeString) return null
    
    try {
      const date = new Date(timeString)
      return date.toLocaleString()
    } catch {
      return timeString
    }
  }
  
  const calculateDuration = () => {
    if (!startedAt || !completedAt) return null
    
    try {
      const start = new Date(startedAt)
      const end = new Date(completedAt)
      const duration = (end.getTime() - start.getTime()) / 1000
      
      if (duration < 60) {
        return `${duration.toFixed(1)}s`
      } else {
        const minutes = Math.floor(duration / 60)
        const seconds = Math.floor(duration % 60)
        return `${minutes}m ${seconds}s`
      }
    } catch {
      return null
    }
  }
  
  return (
    <Card className={cn('', className)}>
      <CardContent>
        <div className="space-y-4">
          {/* Status header */}
          <div className={cn('flex items-center justify-between p-3 rounded-lg border', getStatusColor())}>
            <div className="flex items-center space-x-3">
              {getStatusIcon()}
              <div>
                <p className="font-medium">{getStatusText()}</p>
                {message && (
                  <p className="text-sm opacity-75">{message}</p>
                )}
              </div>
            </div>
            
            {status === 'processing' && (
              <div className="text-sm font-medium">
                {progress}%
              </div>
            )}
          </div>
          
          {/* Progress bar for processing status */}
          {status === 'processing' && (
            <ProgressBar progress={progress} />
          )}
          
          {/* Error message */}
          {error && status === 'failed' && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
              <div className="flex items-start space-x-2">
                <XCircle className="h-5 w-5 text-red-500 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm font-medium text-red-800">Error Details</p>
                  <p className="text-sm text-red-700 mt-1">{error}</p>
                </div>
              </div>
            </div>
          )}
          
          {/* Timing information */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm text-gray-600">
            {startedAt && (
              <div>
                <span className="font-medium">Started:</span>
                <br />
                {formatTime(startedAt)}
              </div>
            )}
            
            {completedAt && (
              <div>
                <span className="font-medium">Completed:</span>
                <br />
                {formatTime(completedAt)}
                {calculateDuration() && (
                  <span className="text-gray-500"> ({calculateDuration()})</span>
                )}
              </div>
            )}
          </div>
          
          {/* Processing stages for active jobs */}
          {status === 'processing' && (
            <div className="space-y-2">
              <p className="text-sm font-medium text-gray-700">Processing stages:</p>
              <div className="space-y-1 text-sm text-gray-600">
                <div className={cn('flex items-center space-x-2', progress >= 10 && 'text-green-600')}>
                  <div className={cn('w-2 h-2 rounded-full', progress >= 10 ? 'bg-green-500' : 'bg-gray-300')} />
                  <span>File validation</span>
                </div>
                <div className={cn('flex items-center space-x-2', progress >= 30 && 'text-green-600')}>
                  <div className={cn('w-2 h-2 rounded-full', progress >= 30 ? 'bg-green-500' : 'bg-gray-300')} />
                  <span>Document analysis</span>
                </div>
                <div className={cn('flex items-center space-x-2', progress >= 60 && 'text-green-600')}>
                  <div className={cn('w-2 h-2 rounded-full', progress >= 60 ? 'bg-green-500' : 'bg-gray-300')} />
                  <span>Content extraction</span>
                </div>
                <div className={cn('flex items-center space-x-2', progress >= 90 && 'text-green-600')}>
                  <div className={cn('w-2 h-2 rounded-full', progress >= 90 ? 'bg-green-500' : 'bg-gray-300')} />
                  <span>Format conversion</span>
                </div>
                <div className={cn('flex items-center space-x-2', progress >= 100 && 'text-green-600')}>
                  <div className={cn('w-2 h-2 rounded-full', progress >= 100 ? 'bg-green-500' : 'bg-gray-300')} />
                  <span>Finalization</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

export default ProcessingStatusComponent

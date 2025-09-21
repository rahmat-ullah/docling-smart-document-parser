import React from 'react'
import { useParams } from 'react-router-dom'
import { Download, Eye, FileText } from 'lucide-react'

const ResultsPage: React.FC = () => {
  const { jobId } = useParams<{ jobId: string }>()

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Processing Results</h1>
          <p className="text-gray-600">Job ID: {jobId}</p>
        </div>
        <div className="flex space-x-3">
          <button className="btn-outline">
            <Download className="h-4 w-4 mr-2" />
            Download
          </button>
          <button className="btn-primary">
            <Eye className="h-4 w-4 mr-2" />
            View Details
          </button>
        </div>
      </div>

      {/* Side-by-side comparison placeholder */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Original Document */}
        <div className="card">
          <div className="p-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <FileText className="h-5 w-5 mr-2" />
              Original Document
            </h3>
          </div>
          <div className="p-6 h-96 bg-gray-50 flex items-center justify-center">
            <p className="text-gray-500">Document preview will be displayed here</p>
          </div>
        </div>

        {/* Processed Output */}
        <div className="card">
          <div className="p-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <FileText className="h-5 w-5 mr-2" />
              Processed Output
            </h3>
          </div>
          <div className="p-6 h-96 bg-gray-50 flex items-center justify-center">
            <p className="text-gray-500">Structured output will be displayed here</p>
          </div>
        </div>
      </div>

      {/* Processing Summary */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Processing Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <span className="text-gray-500">Processing Time:</span>
            <span className="ml-2 font-medium">2.3 seconds</span>
          </div>
          <div>
            <span className="text-gray-500">Pages Processed:</span>
            <span className="ml-2 font-medium">5</span>
          </div>
          <div>
            <span className="text-gray-500">Elements Detected:</span>
            <span className="ml-2 font-medium">23</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ResultsPage

import React from 'react'
import { useParams } from 'react-router-dom'
import { Loader2 } from 'lucide-react'

const ProcessingPage: React.FC = () => {
  const { jobId } = useParams<{ jobId: string }>()

  return (
    <div className="max-w-2xl mx-auto">
      <div className="card p-8 text-center">
        <Loader2 className="mx-auto h-12 w-12 text-primary-600 animate-spin" />
        <h2 className="mt-4 text-xl font-semibold text-gray-900">
          Processing Document
        </h2>
        <p className="mt-2 text-gray-600">
          Job ID: {jobId}
        </p>
        <p className="mt-4 text-sm text-gray-500">
          Your document is being processed using the Granite Docling model. 
          This may take a few moments depending on the document size and complexity.
        </p>
        
        {/* Progress placeholder */}
        <div className="mt-6">
          <div className="bg-gray-200 rounded-full h-2">
            <div className="bg-primary-600 h-2 rounded-full animate-pulse" style={{ width: '60%' }}></div>
          </div>
          <p className="mt-2 text-sm text-gray-500">Processing...</p>
        </div>
      </div>
    </div>
  )
}

export default ProcessingPage

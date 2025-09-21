import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FileText, Upload as UploadIcon, ArrowRight } from 'lucide-react'
import FileUpload from '@/components/FileUpload'
import { useUploadDocument } from '@/hooks/useApi'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import Button from '@/components/ui/Button'
import LoadingSpinner from '@/components/LoadingSpinner'
import toast from 'react-hot-toast'

const Upload: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const navigate = useNavigate()
  const uploadMutation = useUploadDocument()
  
  const handleFileSelect = (file: File) => {
    setSelectedFile(file)
  }
  
  const handleUpload = async () => {
    if (!selectedFile) {
      toast.error('Please select a file first')
      return
    }
    
    try {
      const result = await uploadMutation.mutateAsync(selectedFile)
      
      // Navigate to processing page with job ID
      navigate(`/process/${result.job_id}`)
    } catch (error) {
      console.error('Upload failed:', error)
      // Error is already handled by the mutation
    }
  }
  
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center">
        <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-primary-100 mb-4">
          <FileText className="h-8 w-8 text-primary-600" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Document Processing
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Upload your documents and convert them to structured formats using IBM Granite Docling AI model.
          Supports PDF, Word documents, presentations, spreadsheets, and more.
        </p>
      </div>
      
      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="text-center p-6">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 mb-4">
              <UploadIcon className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Easy Upload
            </h3>
            <p className="text-gray-600">
              Drag and drop or click to upload your documents. Supports multiple formats.
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="text-center p-6">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100 mb-4">
              <FileText className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              AI Processing
            </h3>
            <p className="text-gray-600">
              Advanced document understanding using IBM Granite Docling model.
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="text-center p-6">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-purple-100 mb-4">
              <ArrowRight className="h-6 w-6 text-purple-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Multiple Formats
            </h3>
            <p className="text-gray-600">
              Export to Markdown, HTML, or JSON with preserved structure and formatting.
            </p>
          </CardContent>
        </Card>
      </div>
      
      {/* Upload Section */}
      <Card>
        <CardHeader>
          <CardTitle>Upload Document</CardTitle>
        </CardHeader>
        <CardContent>
          {uploadMutation.isPending ? (
            <div className="py-12">
              <LoadingSpinner size="lg" text="Uploading document..." />
            </div>
          ) : (
            <div className="space-y-6">
              <FileUpload
                onFileSelect={handleFileSelect}
                disabled={uploadMutation.isPending}
              />
              
              {selectedFile && !uploadMutation.isPending && (
                <div className="flex justify-center">
                  <Button
                    onClick={handleUpload}
                    size="lg"
                    className="px-8"
                  >
                    <UploadIcon className="h-5 w-5 mr-2" />
                    Start Processing
                  </Button>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>
      
      {/* Supported Formats */}
      <Card>
        <CardHeader>
          <CardTitle>Supported Formats</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Documents</h4>
              <ul className="space-y-1 text-gray-600">
                <li>PDF (.pdf)</li>
                <li>Word (.docx)</li>
                <li>PowerPoint (.pptx)</li>
                <li>Excel (.xlsx)</li>
                <li>HTML (.html)</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Images</h4>
              <ul className="space-y-1 text-gray-600">
                <li>PNG (.png)</li>
                <li>JPEG (.jpg, .jpeg)</li>
                <li>TIFF (.tiff)</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Audio</h4>
              <ul className="space-y-1 text-gray-600">
                <li>WAV (.wav)</li>
                <li>MP3 (.mp3)</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Limits</h4>
              <ul className="space-y-1 text-gray-600">
                <li>Max size: 50MB</li>
                <li>Processing time: ~1-5 min</li>
                <li>Concurrent jobs: 5</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Upload

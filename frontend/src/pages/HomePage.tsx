import React from 'react'
import { Upload, FileText, Zap, Eye } from 'lucide-react'

const HomePage: React.FC = () => {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
          Document Processing
          <span className="block text-primary-600">Made Simple</span>
        </h1>
        <p className="mt-6 max-w-2xl mx-auto text-xl text-gray-600">
          Transform your documents into structured, searchable content using IBM's 
          state-of-the-art Granite Docling model. Upload, process, and analyze 
          documents with ease.
        </p>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="text-center">
          <div className="mx-auto h-12 w-12 flex items-center justify-center rounded-lg bg-primary-100">
            <Upload className="h-6 w-6 text-primary-600" />
          </div>
          <h3 className="mt-4 text-lg font-semibold text-gray-900">Easy Upload</h3>
          <p className="mt-2 text-gray-600">
            Drag and drop your documents or click to browse. Supports PDF, DOCX, 
            PPTX, XLSX, and more.
          </p>
        </div>

        <div className="text-center">
          <div className="mx-auto h-12 w-12 flex items-center justify-center rounded-lg bg-primary-100">
            <Zap className="h-6 w-6 text-primary-600" />
          </div>
          <h3 className="mt-4 text-lg font-semibold text-gray-900">AI-Powered Processing</h3>
          <p className="mt-2 text-gray-600">
            Advanced document understanding with layout detection, table extraction, 
            and formula recognition.
          </p>
        </div>

        <div className="text-center">
          <div className="mx-auto h-12 w-12 flex items-center justify-center rounded-lg bg-primary-100">
            <Eye className="h-6 w-6 text-primary-600" />
          </div>
          <h3 className="mt-4 text-lg font-semibold text-gray-900">Side-by-Side View</h3>
          <p className="mt-2 text-gray-600">
            Compare your original document with the processed structured output 
            in an intuitive interface.
          </p>
        </div>
      </div>

      {/* Upload Section Placeholder */}
      <div className="card p-8">
        <div className="text-center">
          <FileText className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-4 text-lg font-semibold text-gray-900">
            Upload Component Coming Soon
          </h3>
          <p className="mt-2 text-gray-600">
            The file upload component will be implemented in the next phase.
          </p>
        </div>
      </div>

      {/* Supported Formats */}
      <div className="bg-gray-100 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Supported Formats</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600">
          <div>📄 PDF Documents</div>
          <div>📝 Word Documents (.docx)</div>
          <div>📊 PowerPoint (.pptx)</div>
          <div>📈 Excel Spreadsheets (.xlsx)</div>
          <div>🌐 HTML Files</div>
          <div>🖼️ Images (PNG, JPEG, TIFF)</div>
          <div>🎵 Audio Files (WAV, MP3)</div>
          <div>📋 And more...</div>
        </div>
      </div>
    </div>
  )
}

export default HomePage

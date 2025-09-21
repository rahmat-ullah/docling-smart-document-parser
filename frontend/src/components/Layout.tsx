import React from 'react'
import { Link, Outlet } from 'react-router-dom'
import { FileText, Github, ExternalLink } from 'lucide-react'
import { useHealthCheck } from '@/hooks/useApi'

interface LayoutProps {
  children?: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { data: health } = useHealthCheck()
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-2">
              <FileText className="h-8 w-8 text-primary-600" />
              <span className="text-xl font-semibold text-gray-900">
                Docling Processor
              </span>
            </Link>
            
            <div className="flex items-center space-x-4">
              {/* Health status */}
              <div className="flex items-center">
                <div className={`h-2 w-2 rounded-full mr-2 ${
                  health?.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'
                }`} />
                <span className="text-sm text-gray-600">
                  {health?.status === 'healthy' ? 'Online' : 'Offline'}
                </span>
              </div>

              <nav className="flex items-center space-x-4">
                <a
                  href="https://docling-project.github.io/docling/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-600 hover:text-gray-900 flex items-center space-x-1"
                >
                  <span>Documentation</span>
                  <ExternalLink className="h-4 w-4" />
                </a>
                <a
                  href="https://github.com/docling-project/docling"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-600 hover:text-gray-900"
                >
                  <Github className="h-5 w-5" />
                </a>
              </nav>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children || <Outlet />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-600">
            <p>
              Powered by{' '}
              <a
                href="https://huggingface.co/ibm-granite/granite-docling-258M"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary-600 hover:text-primary-700"
              >
                IBM Granite Docling 258M
              </a>
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Layout

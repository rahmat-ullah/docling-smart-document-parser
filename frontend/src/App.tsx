import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Upload from './pages/Upload'
import Process from './pages/Process'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Upload />} />
        <Route path="/process/:jobId" element={<Process />} />
      </Routes>
    </Layout>
  )
}

export default App

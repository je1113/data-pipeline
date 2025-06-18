import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Box } from '@mui/material'

import Layout from './components/layout/Layout'
import Dashboard from './pages/Dashboard'
import PipelineBuilder from './pages/PipelineBuilder'
import DataSources from './pages/DataSources'
import Executions from './pages/Executions'
import Settings from './pages/Settings'

function App() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/pipelines" element={<PipelineBuilder />} />
          <Route path="/pipelines/:id" element={<PipelineBuilder />} />
          <Route path="/data-sources" element={<DataSources />} />
          <Route path="/executions" element={<Executions />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Box>
  )
}

export default App

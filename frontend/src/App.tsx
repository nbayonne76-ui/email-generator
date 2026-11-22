import { Route, Routes } from 'react-router-dom'
import HomePage from './pages/HomePage'
import TemplatesPage from './pages/TemplatesPage'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/templates" element={<TemplatesPage />} />
    </Routes>
  )
}

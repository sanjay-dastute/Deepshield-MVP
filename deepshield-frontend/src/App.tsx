import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { ProtectedRoute } from './components/ProtectedRoute'
import { Login } from './pages/Login'
import { Register } from './pages/Register'
import { AdminPanel } from './pages/AdminPanel'
import { KYCVerification } from './pages/KYCVerification'
import { ContentReporting } from './pages/ContentReporting'
import { FlaggedContent } from './pages/FlaggedContent'
import './App.css'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<ProtectedRoute><ContentReporting /></ProtectedRoute>} />
          <Route path="/kyc" element={<ProtectedRoute><KYCVerification /></ProtectedRoute>} />
          <Route path="/flagged" element={<ProtectedRoute><FlaggedContent /></ProtectedRoute>} />
          <Route path="/admin" element={<ProtectedRoute><AdminPanel /></ProtectedRoute>} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App

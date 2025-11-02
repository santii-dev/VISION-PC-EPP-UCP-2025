import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import Dashboard from './pages/Dashboard'
import Entrenar from './pages/Entrenar'
import Avanzado from './pages/Avanzado'
import './App.css'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isSystemActive, setIsSystemActive] = useState(false)

  // Agregar clase al html cuando esté autenticado
  useEffect(() => {
    if (isAuthenticated) {
      document.documentElement.classList.add('authenticated')
    } else {
      document.documentElement.classList.remove('authenticated')
    }
  }, [isAuthenticated])

  return (
    <Router>
      <Routes>
        <Route 
          path="/" 
          element={
            isAuthenticated ? 
            <Navigate to="/dashboard" /> : 
            <LandingPage onLogin={() => setIsAuthenticated(true)} />
          } 
        />
        <Route 
          path="/dashboard" 
          element={
            isAuthenticated ? 
            <Dashboard 
              isSystemActive={isSystemActive}
              setIsSystemActive={setIsSystemActive}
              onLogout={() => setIsAuthenticated(false)}
            /> : 
            <Navigate to="/" />
          } 
        />
        <Route 
          path="/entrenar" 
          element={
            isAuthenticated ? 
            <Entrenar /> : 
            <Navigate to="/" />
          } 
        />
        <Route 
          path="/avanzado" 
          element={
            isAuthenticated ? 
            <Avanzado /> : 
            <Navigate to="/" />
          } 
        />
      </Routes>
    </Router>
  )
}

export default App


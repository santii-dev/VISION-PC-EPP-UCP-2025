import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import {
  Shield, TrendingUp, Users, AlertTriangle, Activity,
  Power, RefreshCw, LogOut, HardHat, Glasses, ShirtIcon,
  ChevronRight, X, Image as ImageIcon, Calendar, Clock, Trash2, Settings
} from 'lucide-react'
import './Dashboard.css'

const Dashboard = ({ isSystemActive, setIsSystemActive, onLogout }) => {
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)
  const [registros, setRegistros] = useState([])
  const [selectedRegistro, setSelectedRegistro] = useState(null)
  const [showModal, setShowModal] = useState(false)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')
  const [cameraStatus, setCameraStatus] = useState('stopped') // stopped, starting, running
  const [showCameraPopup, setShowCameraPopup] = useState(false)

  // Cargar datos del backend
  const fetchData = async (showMessage = false) => {
    try {
      const response = await axios.get('/api/registros')
      const data = response.data.registros

      // Guardar registros SIN invertir (más nuevo primero para la tabla)
      setRegistros(data)

      // Mostrar mensaje de refresco si se solicitó
      if (showMessage) {
        // Crear un elemento temporal para el mensaje
        const mensaje = document.createElement('div')
        mensaje.textContent = '✓ Refrescado'
        mensaje.style.cssText = `
          position: fixed;
          top: 80px;
          right: 20px;
          background: linear-gradient(135deg, #4ade80, #22c55e);
          color: white;
          padding: 12px 24px;
          border-radius: 8px;
          font-weight: 600;
          z-index: 10000;
          box-shadow: 0 4px 12px rgba(74, 222, 128, 0.4);
          animation: slideIn 0.3s ease-out;
        `
        document.body.appendChild(mensaje)

        // Remover después de 2 segundos
        setTimeout(() => {
          mensaje.style.animation = 'slideOut 0.3s ease-out'
          setTimeout(() => mensaje.remove(), 300)
        }, 2000)
      }

      // Calcular estadísticas
      if (data.length > 0) {
        const totalRegistros = data.length
        const totalPersonas = data.reduce((sum, r) => sum + r.total_personas, 0)
        const maxPersonas = Math.max(...data.map(r => r.total_personas))
        const minPersonas = Math.min(...data.map(r => r.total_personas).filter(p => p > 0))

        // Promedios de cumplimiento
        const avgCascos = data.reduce((sum, r) => sum + r.cumplimiento_cascos, 0) / totalRegistros
        const avgChalecos = data.reduce((sum, r) => sum + r.cumplimiento_chalecos, 0) / totalRegistros
        const avgGafas = data.reduce((sum, r) => sum + r.cumplimiento_gafas, 0) / totalRegistros
        const avgGeneral = (avgCascos + avgChalecos + avgGafas) / 3

        // Incumplimientos (registros con cumplimiento < 100%)
        const incumplimientosCascos = data.filter(r => r.cumplimiento_cascos < 100).length
        const incumplimientosChalecos = data.filter(r => r.cumplimiento_chalecos < 100).length
        const incumplimientosGafas = data.filter(r => r.cumplimiento_gafas < 100).length

        setStats({
          totalRegistros,
          totalPersonas,
          maxPersonas,
          minPersonas: minPersonas === Infinity ? 0 : minPersonas,
          avgCumplimiento: avgGeneral,
          cumplimiento: {
            cascos: avgCascos,
            chalecos: avgChalecos,
            gafas: avgGafas
          },
          incumplimientos: {
            cascos: incumplimientosCascos,
            chalecos: incumplimientosChalecos,
            gafas: incumplimientosGafas,
            total: Math.max(incumplimientosCascos, incumplimientosChalecos, incumplimientosGafas)
          }
        })
      } else {
        // Si no hay datos, resetear stats a 0
        setStats({
          totalRegistros: 0,
          totalPersonas: 0,
          maxPersonas: 0,
          minPersonas: 0,
          avgCumplimiento: 0,
          cumplimiento: {
            cascos: 0,
            chalecos: 0,
            gafas: 0
          },
          incumplimientos: {
            cascos: 0,
            chalecos: 0,
            gafas: 0,
            total: 0
          }
        })
      }

      setLoading(false)
    } catch (error) {
      console.error('Error fetching data:', error)
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    checkCameraStatus()
    const interval = setInterval(() => {
      fetchData()
      checkCameraStatus()
    }, 5000) // Actualizar cada 5 segundos
    return () => clearInterval(interval)
  }, [])

  // Verificar estado de la cámara
  const checkCameraStatus = async () => {
    try {
      const response = await axios.get('/api/camera/status')
      const status = response.data.status
      setCameraStatus(status)
      setIsSystemActive(status === 'running')
    } catch (error) {
      console.error('Error checking camera status:', error)
    }
  }

  // Activar/Desactivar sistema
  const toggleSystem = async () => {
    if (cameraStatus === 'running') {
      // Detener cámara
      try {
        setShowCameraPopup(true)
        setCameraStatus('stopping')
        await axios.post('/api/camera/stop')
        setCameraStatus('stopped')
        setIsSystemActive(false)
        setTimeout(() => setShowCameraPopup(false), 2000)
      } catch (error) {
        console.error('Error stopping camera:', error)
        setCameraStatus('running')
        setShowCameraPopup(false)
      }
    } else {
      // Iniciar cámara
      try {
        // 1. Mostrar popup con "Iniciando..."
        setShowCameraPopup(true)
        setCameraStatus('starting')

        // 2. Esperar 2 segundos (animación inicial)
        await new Promise(resolve => setTimeout(resolve, 2000))

        // 3. Cambiar a "Conectando" (sin ejecutar aún)
        setCameraStatus('connecting')
        await new Promise(resolve => setTimeout(resolve, 1500))

        // 4. Cambiar a "Conectada" y esperar 1.5 segundos más
        setCameraStatus('running')
        setIsSystemActive(true)
        await new Promise(resolve => setTimeout(resolve, 1500))

        // 5. AHORA SÍ ejecutar main.py (después de mostrar todo el popup)
        await axios.post('/api/camera/start')

        // 6. Cerrar popup después de 500ms
        setTimeout(() => setShowCameraPopup(false), 500)

      } catch (error) {
        console.error('Error starting camera:', error)
        setCameraStatus('stopped')
        setIsSystemActive(false)
        setShowCameraPopup(false)
        alert('Error al iniciar cámara: ' + error.message)
      }
    }
  }

  // Abrir modal con detalle del registro
  const openRegistroDetail = async (registro) => {
    try {
      const response = await axios.get(`/api/registros/${registro.id}`)
      setSelectedRegistro(response.data)
      setShowModal(true)
    } catch (error) {
      console.error('Error fetching registro detail:', error)
    }
  }

  // Formatear fecha de forma segura
  const formatearFecha = (timestamp) => {
    if (!timestamp) return 'Sin fecha'

    try {
      const fecha = new Date(timestamp)
      if (isNaN(fecha.getTime())) return 'Fecha inválida'

      return fecha.toLocaleString('es-CO', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true // Cambio a formato 12 horas con AM/PM
      })
    } catch (error) {
      return 'Error en fecha'
    }
  }

  // Obtener clase de color según porcentaje de cumplimiento
  const getComplianceClass = (percentage) => {
    const pct = percentage || 0
    if (pct < 10) return 'critical' // 0-9%: Rojo
    if (pct < 41) return 'danger'   // 10-40%: Naranja
    if (pct < 80) return 'warning'  // 41-79%: Amarillo verdoso
    return 'success'                // 80-100%: Verde fuerte
  }

  // Distribuir EPP entre personas (usa las detecciones reales del backend)
  const distribuirEPP = (total_personas, detecciones) => {
    // Validar que detecciones existe y es un array con datos
    if (!detecciones || !Array.isArray(detecciones) || detecciones.length === 0) {
      // Si no hay detecciones, crear personas sin EPP
      const personas = []
      for (let i = 0; i < total_personas; i++) {
        personas.push({
          id: i + 1,
          tiene_casco: false,
          tiene_chaleco: false,
          tiene_gafas: false
        })
      }
      return personas
    }

    // Usar directamente las detecciones del backend que ya vienen con tiene_casco, tiene_chaleco, tiene_gafas
    return detecciones.map(det => ({
      id: det.numero_persona || det.id || 0,
      tiene_casco: det.tiene_casco || false,
      tiene_chaleco: det.tiene_chaleco || false,
      tiene_gafas: det.tiene_gafas || false
    }))
  }

  // Eliminar un registro individual
  const eliminarRegistro = async (id) => {
    if (!confirm(`¿Estás seguro de eliminar el registro #${id}?`)) return
    
    try {
      await axios.delete(`/api/registros/${id}`)
      setLoading(true)
      await fetchData(true)
    } catch (error) {
      console.error('Error eliminando registro:', error)
      alert('Error al eliminar registro')
    }
  }

  // Eliminar todos los registros
  const eliminarTodosRegistros = async () => {
    if (!confirm('¿Estás seguro de eliminar TODOS los registros? Esta acción no se puede deshacer.')) return
    
    try {
      await axios.delete('/api/registros')
      setLoading(true)
      await fetchData(true)
    } catch (error) {
      console.error('Error eliminando registros:', error)
      alert('Error al eliminar registros')
    }
  }

  if (loading) {
    return (
      <div className="dashboard-loading">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
        >
          <Activity size={48} color="var(--primary)" />
        </motion.div>
        <p>Cargando dashboard...</p>
      </div>
    )
  }

  return (
    <div className="dashboard">
      {/* Gradient Orbs */}
      <div className="gradient-orb orb-1"></div>
      <div className="gradient-orb orb-2"></div>

      {/* Header */}
      <header className="dashboard-header glass">
        <div className="header-content">
          <div className="header-left">
            <div className="logo">
              <img src="/logo/ProtekSecure_sintexto.PNG" alt="ProtekSecure" className="logo-img" />
              <div className="logo-text">
                <span className="gradient-text company-name">ProtekSecure</span>
                <span className="logo-subtitle">EPP Monitor - Sistema Inteligente de Seguridad Industrial</span>
              </div>
            </div>
          </div>

          <div className="header-center">
            <motion.button
              className={`system-toggle ${isSystemActive ? 'active' : ''}`}
              onClick={toggleSystem}
              whileTap={{ scale: 0.95 }}
            >
              <Power size={20} />
              <span>{isSystemActive ? 'Sistema Activo' : 'Sistema Inactivo'}</span>
              {isSystemActive && <div className="pulse-dot"></div>}
            </motion.button>
          </div>

          <div className="header-right">
            <button 
              className="btn btn-glass btn-entrenar" 
              onClick={() => navigate('/entrenar')}
              title="Entrenar Modelo"
            >
              <TrendingUp size={18} />
              <span className="btn-text">Entrenar</span>
            </button>
            <button 
              className="btn btn-glass btn-avanzado" 
              onClick={() => navigate('/avanzado')}
              title="Configuración Avanzada"
            >
              <Settings size={18} />
              <span className="btn-text">Avanzado</span>
            </button>
            <button className="btn btn-glass btn-refresh" onClick={() => fetchData(true)} title="Refrescar datos">
              <RefreshCw size={18} />
            </button>
            <button className="btn btn-glass btn-logout" onClick={onLogout} title="Cerrar sesión">
              <LogOut size={18} />
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="dashboard-main">
        <div className="container padingg-bottomespacio">
          {/* Tabs */}
          <div className="tabs-container">
            <button
              className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
              onClick={() => setActiveTab('overview')}
            >
              <TrendingUp size={18} />
              <span>Panorama General</span>
            </button>
            <button
              className={`tab ${activeTab === 'registros' ? 'active' : ''}`}
              onClick={() => setActiveTab('registros')}
            >
              <Users size={18} />
              <span>Registros</span>
            </button>
          </div>

          {/* Overview Tab */}
          {activeTab === 'overview' && stats && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              {/* Stats Cards */}
              <div className="stats-grid">
                <div className="stat-card glass">
                  <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #0066FF, #003D99)' }}>
                    <Activity size={24} />
                  </div>
                  <div className="stat-content">
                    <p className="stat-label">Total Registros</p>
                    <h2 className="stat-value">{stats.totalRegistros}</h2>
                    <p className="stat-change">Última actualización: ahora</p>
                  </div>
                </div>

                <div className="stat-card glass">
                  <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #0088FF, #0066FF)' }}>
                    <Users size={24} />
                  </div>
                  <div className="stat-content">
                    <p className="stat-label">Personas Detectadas</p>
                    <h2 className="stat-value">{stats.totalPersonas}</h2>
                    <p className="stat-change">Min: {stats.minPersonas} | Max: {stats.maxPersonas}</p>
                  </div>
                </div>

                <div className="stat-card glass">
                  <div className="stat-icon" style={{
                    background: stats.avgCumplimiento >= 70 ?
                      'linear-gradient(135deg, #4ade80, #22c55e)' :
                      'linear-gradient(135deg, #fbbf24, #f59e0b)'
                  }}>
                    <Shield size={24} />
                  </div>
                  <div className="stat-content">
                    <p className="stat-label">Cumplimiento General</p>
                    <h2 className="stat-value">{stats.avgCumplimiento.toFixed(1)}%</h2>
                    <p className="stat-change">Promedio de todas las categorías</p>
                  </div>
                </div>

                <div className="stat-card glass">
                  <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f87171, #ef4444)' }}>
                    <AlertTriangle size={24} />
                  </div>
                  <div className="stat-content">
                    <p className="stat-label">Incumplimientos</p>
                    <h2 className="stat-value">{stats.incumplimientos.total}</h2>
                    <p className="stat-change">Registros con EPP incompleto</p>
                  </div>
                </div>
              </div>

              {/* Compliance by Category */}
              <div className="compliance-section">
                <h3 className="section-title">Cumplimiento por Categoría</h3>
                <div className="compliance-grid">
                  <div className="compliance-card glass">
                    <div className="compliance-header">
                      <div className="compliance-icon">
                        <HardHat size={28} />
                      </div>
                      <div>
                        <h4>Cascos de Seguridad</h4>
                        <p>{stats.incumplimientos.cascos} incumplimientos</p>
                      </div>
                    </div>
                    <div className="progress-bar">
                      <motion.div
                        className="progress-fill"
                        initial={{ width: 0 }}
                        animate={{ width: `${stats.cumplimiento.cascos}%` }}
                        transition={{ duration: 1, delay: 0.2 }}
                        style={{
                          background: stats.cumplimiento.cascos >= 70 ?
                            'linear-gradient(90deg, #4ade80, #22c55e)' :
                            'linear-gradient(90deg, #fbbf24, #f59e0b)'
                        }}
                      ></motion.div>
                    </div>
                    <p className="progress-label">{stats.cumplimiento.cascos.toFixed(1)}% de cumplimiento</p>
                  </div>

                  <div className="compliance-card glass">
                    <div className="compliance-header">
                      <div className="compliance-icon">
                        <ShirtIcon size={28} />
                      </div>
                      <div>
                        <h4>Chalecos Reflectantes</h4>
                        <p>{stats.incumplimientos.chalecos} incumplimientos</p>
                      </div>
                    </div>
                    <div className="progress-bar">
                      <motion.div
                        className="progress-fill"
                        initial={{ width: 0 }}
                        animate={{ width: `${stats.cumplimiento.chalecos}%` }}
                        transition={{ duration: 1, delay: 0.4 }}
                        style={{
                          background: stats.cumplimiento.chalecos >= 70 ?
                            'linear-gradient(90deg, #4ade80, #22c55e)' :
                            'linear-gradient(90deg, #fbbf24, #f59e0b)'
                        }}
                      ></motion.div>
                    </div>
                    <p className="progress-label">{stats.cumplimiento.chalecos.toFixed(1)}% de cumplimiento</p>
                  </div>

                  <div className="compliance-card glass">
                    <div className="compliance-header">
                      <div className="compliance-icon">
                        <Glasses size={28} />
                      </div>
                      <div>
                        <h4>Gafas de Seguridad</h4>
                        <p>{stats.incumplimientos.gafas} incumplimientos</p>
                      </div>
                    </div>
                    <div className="progress-bar">
                      <motion.div
                        className="progress-fill"
                        initial={{ width: 0 }}
                        animate={{ width: `${stats.cumplimiento.gafas}%` }}
                        transition={{ duration: 1, delay: 0.6 }}
                        style={{
                          background: stats.cumplimiento.gafas >= 70 ?
                            'linear-gradient(90deg, #4ade80, #22c55e)' :
                            'linear-gradient(90deg, #fbbf24, #f59e0b)'
                        }}
                      ></motion.div>
                    </div>
                    <p className="progress-label">{stats.cumplimiento.gafas.toFixed(1)}% de cumplimiento</p>
                  </div>
                </div>

                {/* Gráfico de detecciones en tiempo real */}
                <div className="chart-section">
                  <h3>📊 Detecciones en Tiempo Real</h3>
                  <div className="line-chart glass">
                    <div className="chart-header">
                      <div>
                        <h4>Cumplimiento General EPP - Últimos 10 Registros</h4>
                        <p className="chart-subtitle">Porcentaje de cumplimiento en el tiempo</p>
                      </div>
                      <div className="chart-legend">
                        <div className="legend-item">
                          <div className="legend-dot" style={{ background: '#4ade80' }}></div>
                          <span>Cumplimiento (%)</span>
                        </div>
                      </div>
                    </div>
                    <div className="chart-container">
                      {registros.length === 0 ? (
                        <div className="no-data-message">
                          <Activity size={48} opacity={0.3} />
                          <p>Sin datos para mostrar</p>
                          <small>Los datos aparecerán cuando se detecten personas</small>
                        </div>
                      ) : registros.length < 2 ? (
                        <div className="no-data-message">
                          <Activity size={48} opacity={0.3} />
                          <p>Necesitas al menos 2 registros para ver el gráfico</p>
                        </div>
                      ) : (
                        <svg className="chart-svg" viewBox="0 0 900 280" preserveAspectRatio="xMidYMid meet">
                          {/* Grid lines horizontales con espacio */}
                          {[0, 25, 50, 75, 100].map((value) => (
                            <g key={value}>
                              <line
                                x1="50"
                                y1={250 - (value / 100) * 200}
                                x2="850"
                                y2={250 - (value / 100) * 200}
                                stroke="rgba(255,255,255,0.1)"
                                strokeWidth="1"
                              />
                              <text
                                x="10"
                                y={250 - (value / 100) * 200 + 5}
                                fill="rgba(255,255,255,0.5)"
                                fontSize="12"
                                fontWeight="500"
                              >
                                {value}%
                              </text>
                            </g>
                          ))}

                          {/* Line chart - ÚLTIMOS 20 en orden correcto */}
                          {(() => {
                            // Tomar los últimos 20 y darles vuelta para el gráfico (viejo a nuevo)
                            const ultimos20 = [...registros].slice(-20).reverse()

                            return ultimos20.length > 1 && (
                              <>
                                {/* Área bajo la línea */}
                                <motion.path
                                  d={`M 50,250 ${ultimos20.map((r, i) => {
                                    const x = 50 + (i / Math.max(ultimos20.length - 1, 1)) * 800
                                    const y = 250 - ((r.cumplimiento_general || 0) / 100) * 200
                                    return `L ${x},${y}`
                                  }).join(' ')} L 850,250 Z`}
                                  fill="url(#areaGradient)"
                                  initial={{ opacity: 0 }}
                                  animate={{ opacity: 0.3 }}
                                  transition={{ duration: 1 }}
                                />

                                {/* Línea principal */}
                                <motion.polyline
                                  points={ultimos20.map((r, i) => {
                                    const x = 50 + (i / Math.max(ultimos20.length - 1, 1)) * 800
                                    const y = 250 - ((r.cumplimiento_general || 0) / 100) * 200
                                    return `${x},${y}`
                                  }).join(' ')}
                                  fill="none"
                                  stroke="url(#lineGradient)"
                                  strokeWidth="3"
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                  initial={{ pathLength: 0 }}
                                  animate={{ pathLength: 1 }}
                                  transition={{ duration: 1.5, ease: "easeOut" }}
                                />

                                {/* Puntos */}
                                {ultimos20.map((r, i) => {
                                  const x = 50 + (i / Math.max(ultimos20.length - 1, 1)) * 800
                                  const y = 250 - ((r.cumplimiento_general || 0) / 100) * 200
                                  const cumplimiento = r.cumplimiento_general || 0

                                  let color = cumplimiento === 0 ? '#ef4444' :
                                    cumplimiento >= 90 ? '#22c55e' :
                                      cumplimiento >= 70 ? '#4ade80' :
                                        cumplimiento >= 50 ? '#86efac' :
                                          cumplimiento >= 30 ? '#fbbf24' : '#f87171'

                                  return (
                                    <g key={`point-${r.id}`}>
                                      <motion.circle
                                        cx={x}
                                        cy={y}
                                        r="12"
                                        fill={color}
                                        opacity="0.2"
                                        initial={{ scale: 0 }}
                                        animate={{ scale: 1 }}
                                        transition={{ delay: i * 0.1, type: "spring" }}
                                      />
                                      <motion.circle
                                        cx={x}
                                        cy={y}
                                        r="7"
                                        fill={color}
                                        stroke="#1a1f2e"
                                        strokeWidth="2.5"
                                        initial={{ scale: 0 }}
                                        animate={{ scale: 1 }}
                                        transition={{ delay: i * 0.1 + 0.1, type: "spring" }}
                                      >
                                        <title>{`Registro #${r.id}: ${cumplimiento.toFixed(1)}%`}</title>
                                      </motion.circle>
                                    </g>
                                  )
                                })}
                              </>
                            )
                          })()}

                          {/* Gradients */}
                          <defs>
                            <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                              <stop offset="0%" stopColor="#4ade80" stopOpacity="0.5" />
                              <stop offset="100%" stopColor="#4ade80" stopOpacity="0" />
                            </linearGradient>
                            <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                              <stop offset="0%" stopColor="#86efac" />
                              <stop offset="50%" stopColor="#4ade80" />
                              <stop offset="100%" stopColor="#22c55e" />
                            </linearGradient>
                          </defs>
                        </svg>
                      )}
                    </div>
                    {registros.length >= 2 && (
                      <div className="chart-labels">
                        {[...registros].slice(-20).reverse().map((r, i) => (
                          <span key={r.id} className="chart-label">
                            #{r.id}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Registros Tab */}
          {activeTab === 'registros' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="registros-section"
            >
              <div className="section-header">
                <h3 className="section-title">Historial de Registros</h3>
                <button
                  className="btn-danger-outline"
                  onClick={eliminarTodosRegistros}
                >
                  <Trash2 size={16} />
                  Limpiar Todos
                </button>
              </div>
              <div className="table-container glass">
                {registros.length === 0 ? (
                  <div className="no-data-table">
                    <Users size={64} opacity={0.2} />
                    <h3>Sin registros disponibles</h3>
                    <p>Los registros aparecerán aquí cuando el sistema detecte personas con EPP</p>
                  </div>
                ) : (
                  <table className="registros-table">
                    <thead>
                      <tr>
                        <th>ID</th>
                        <th>Fecha y Hora</th>
                        <th>Personas</th>
                        <th>Cascos</th>
                        <th>Chalecos</th>
                        <th>Gafas</th>
                        <th>Acciones</th>
                      </tr>
                    </thead>
                    <tbody>
                      {registros.map((registro) => (
                        <motion.tr
                          key={registro.id}
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          transition={{ duration: 0.3 }}
                          whileHover={{ backgroundColor: 'rgba(255, 255, 255, 0.05)' }}
                        >
                          <td>#{registro.id}</td>
                          <td>
                            <div className="datetime-cell">
                              <Calendar size={14} />
                              <span>{formatearFecha(registro.timestamp)}</span>
                            </div>
                          </td>
                          <td>
                            <div className="badge-cell">
                              <Users size={14} />
                              {registro.total_personas}
                            </div>
                          </td>
                          <td>
                            <div className={`compliance-badge ${getComplianceClass(registro.cumplimiento_cascos)}`}>
                              {(registro.cumplimiento_cascos || 0).toFixed(0)}%
                            </div>
                          </td>
                          <td>
                            <div className={`compliance-badge ${getComplianceClass(registro.cumplimiento_chalecos)}`}>
                              {(registro.cumplimiento_chalecos || 0).toFixed(0)}%
                            </div>
                          </td>
                          <td>
                            <div className={`compliance-badge ${getComplianceClass(registro.cumplimiento_gafas)}`}>
                              {(registro.cumplimiento_gafas || 0).toFixed(0)}%
                            </div>
                          </td>
                          <td>
                            <div className="action-buttons">
                              <button
                                className="btn-detail"
                                onClick={() => openRegistroDetail(registro)}
                              >
                                Ver Detalle
                                <ChevronRight size={16} />
                              </button>
                              <button
                                className="btn-delete"
                                onClick={(e) => {
                                  e.stopPropagation()
                                  eliminarRegistro(registro.id)
                                }}
                                title="Eliminar registro"
                              >
                                <Trash2 size={16} />
                              </button>
                            </div>
                          </td>
                        </motion.tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </motion.div>
          )}
        </div>
      </main>

      {/* Modal de Detalle */}
      <AnimatePresence>
        {showModal && selectedRegistro && (
          <motion.div
            className="modal-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setShowModal(false)}
          >
            <motion.div
              className="modal-content glass-strong"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="modal-header">
                <div>
                  <h2>Registro #{selectedRegistro.registro.id}</h2>
                  <p>{formatearFecha(selectedRegistro.registro.timestamp)}</p>
                  <p className="sector-info">📍 Universidad Católica de Pereira</p>
                </div>
                <motion.button 
                  className="btn-close" 
                  onClick={() => setShowModal(false)}
                  whileHover={{ scale: 1.15 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <X size={20} />
                </motion.button>
              </div>

              <div className="modal-body">
                {/* Información adicional */}
                <div className="registro-info-grid">
                  <div className="info-badge glass">
                    <span className="info-label">Sector:</span>
                    <span className="info-value">Universidad Católica de Pereira</span>
                  </div>
                  <div className="info-badge glass">
                    <span className="info-label">Zona:</span>
                    <span className="info-value">Bodega {Math.floor(Math.random() * 20) + 1}</span>
                  </div>
                  <div className="info-badge glass">
                    <span className="info-label">Turno:</span>
                    <span className="info-value">{new Date(selectedRegistro.registro.timestamp).getHours() < 14 ? 'Mañana' : 'Tarde'}</span>
                  </div>
                </div>

                {/* Imagen */}
                <div className="registro-image-container">
                  {selectedRegistro.registro.ruta_imagen ? (
                    <img
                      src={`http://localhost:8000/${selectedRegistro.registro.ruta_imagen.replace(/\\/g, '/')}`}
                      alt={`Registro ${selectedRegistro.registro.id}`}
                      className="registro-image"
                      onError={(e) => {
                        console.error('Error cargando imagen:', e.target.src)
                        e.target.style.display = 'none'
                        e.target.nextSibling.style.display = 'flex'
                      }}
                    />
                  ) : null}
                  <div className="image-placeholder glass" style={{ display: selectedRegistro.registro.ruta_imagen ? 'none' : 'flex' }}>
                    <ImageIcon size={48} />
                    <p>Imagen no disponible</p>
                    <small>{selectedRegistro.registro.ruta_imagen || 'Sin ruta de imagen'}</small>
                  </div>
                </div>

                {/* Resumen */}
                <div className="registro-summary">
                  <div className="summary-card glass">
                    <Users size={20} />
                    <div>
                      <p>Total Personas</p>
                      <h3>{selectedRegistro.registro.total_personas}</h3>
                    </div>
                  </div>
                  <div className="summary-card glass">
                    <HardHat size={20} />
                    <div>
                      <p>Cascos</p>
                      <h3>{(selectedRegistro.registro.cumplimiento_cascos || 0).toFixed(0)}%</h3>
                    </div>
                  </div>
                  <div className="summary-card glass">
                    <ShirtIcon size={20} />
                    <div>
                      <p>Chalecos</p>
                      <h3>{(selectedRegistro.registro.cumplimiento_chalecos || 0).toFixed(0)}%</h3>
                    </div>
                  </div>
                  <div className="summary-card glass">
                    <Glasses size={20} />
                    <div>
                      <p>Gafas</p>
                      <h3>{(selectedRegistro.registro.cumplimiento_gafas || 0).toFixed(0)}%</h3>
                    </div>
                  </div>
                </div>

                {/* Detalle por persona */}
                <h4>Detalle por Persona</h4>
                <div className="personas-table">
                  <table>
                    <thead>
                      <tr>
                        <th>Persona</th>
                        <th>Casco</th>
                        <th>Chaleco</th>
                        <th>Gafas</th>
                      </tr>
                    </thead>
                    <tbody>
                      {distribuirEPP(selectedRegistro.registro.total_personas, selectedRegistro.detecciones).map((persona) => (
                        <tr key={persona.id}>
                          <td>Persona #{persona.id}</td>
                          <td>
                            <span className={`epp-status ${persona.tiene_casco ? 'yes' : 'no'}`}>
                              {persona.tiene_casco ? '✓ Sí' : '✗ No'}
                            </span>
                          </td>
                          <td>
                            <span className={`epp-status ${persona.tiene_chaleco ? 'yes' : 'no'}`}>
                              {persona.tiene_chaleco ? '✓ Sí' : '✗ No'}
                            </span>
                          </td>
                          <td>
                            <span className={`epp-status ${persona.tiene_gafas ? 'yes' : 'no'}`}>
                              {persona.tiene_gafas ? '✓ Sí' : '✗ No'}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Popup de estado de cámara */}
      <AnimatePresence>
        {showCameraPopup && (
          <>
            {/* Overlay oscuro que bloquea interacción */}
            <motion.div
              className="camera-overlay"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
            />

            {/* Modal centrado */}
            <motion.div
              className="camera-modal glass"
              initial={{ opacity: 0, scale: 0.8, y: 50 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.8, y: 50 }}
              transition={{ type: "spring", damping: 20, stiffness: 300 }}
            >
              <div className="camera-modal-icon">
                {(cameraStatus === 'starting' || cameraStatus === 'connecting') && (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  >
                    <RefreshCw size={48} />
                  </motion.div>
                )}
                {cameraStatus === 'running' && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: "spring", damping: 10 }}
                  >
                    <Activity size={48} className="success-icon" />
                  </motion.div>
                )}
                {cameraStatus === 'stopping' && (
                  <motion.div
                    animate={{ opacity: [1, 0.5, 1] }}
                    transition={{ duration: 0.8, repeat: Infinity }}
                  >
                    <Power size={48} />
                  </motion.div>
                )}
              </div>

              <div className="camera-modal-content">
                <h2>
                  {cameraStatus === 'starting' && 'Activando Cámara TAPO C210'}
                  {cameraStatus === 'connecting' && 'Conectando con Cámara...'}
                  {cameraStatus === 'running' && '¡Cámara Conectada!'}
                  {cameraStatus === 'stopping' && 'Deteniendo Sistema'}
                </h2>
                <p className="camera-location">
                  {(cameraStatus === 'starting' || cameraStatus === 'connecting') && 'Universidad Católica de Pereira'}
                  {cameraStatus === 'running' && 'Sistema de monitoreo activo'}
                  {cameraStatus === 'stopping' && 'Cerrando conexión con cámara'}
                </p>

                {(cameraStatus === 'starting' || cameraStatus === 'connecting') && (
                  <div className="loading-steps">
                    <motion.div
                      className="step"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.2 }}
                    >
                      <div className="step-dot"></div>
                      <span>Conectando con cámara...</span>
                    </motion.div>
                    <motion.div
                      className="step"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.5 }}
                    >
                      <div className="step-dot"></div>
                      <span>Inicializando detección EPP...</span>
                    </motion.div>
                    <motion.div
                      className="step"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.8 }}
                    >
                      <div className="step-dot"></div>
                      <span>Cargando modelo Roboflow...</span>
                    </motion.div>
                  </div>
                )}
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  )
}

export default Dashboard

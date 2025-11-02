import { useState, useEffect, useMemo } from 'react'
import { motion, useMotionValue } from 'framer-motion'
import { Shield, Eye, TrendingUp, Lock, ArrowRight, Zap, Award, Globe, HardHat, AlertTriangle, UserCheck, Brain, Mail } from 'lucide-react'
import './LandingPage.css'

const LandingPage = ({ onLogin }) => {
  const [credentials, setCredentials] = useState({ username: '', password: '' })
  const [showLogin, setShowLogin] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  // Generar configuración de burbujas solo una vez
  const bubbles = useMemo(() => 
    Array.from({ length: 15 }, (_, i) => ({
      id: i,
      initialX: Math.random() * 100,
      width: 20 + Math.random() * 80,
      height: 20 + Math.random() * 80,
      xPath: [
        Math.random() * 100,
        Math.random() * 100,
        Math.random() * 100
      ],
      duration: 15 + Math.random() * 10,
      delay: Math.random() * 5
    })),
    []
  )

  // Mouse tracking para iconos que evitan el cursor
  const mouseX = useMotionValue(0)
  const mouseY = useMotionValue(0)

  useEffect(() => {
    const handleMouseMove = (e) => {
      mouseX.set(e.clientX)
      mouseY.set(e.clientY)
    }
    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [mouseX, mouseY])

  const handleLogin = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    
    // Simular carga del sistema
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Cualquier credencial es válida (demo)
    if (credentials.username && credentials.password) {
      onLogin()
    }
  }

  // Elementos flotantes de seguridad
  const floatingElements = [
    { icon: Shield, x: 10, y: 20, delay: 0, color: '#10b981' },
    { icon: Lock, x: 85, y: 15, delay: 0.5, color: '#34d399' },
    { icon: HardHat, x: 15, y: 70, delay: 1, color: '#059669' },
    { icon: AlertTriangle, x: 90, y: 65, delay: 1.5, color: '#10b981' },
    { icon: UserCheck, x: 50, y: 10, delay: 0.8, color: '#34d399' },
    { icon: Shield, x: 5, y: 50, delay: 1.2, color: '#059669' },
  ]

  return (
    <div className="landing-page">
      {/* Burbujas flotantes de fondo */}
      <div className="bubbles-container">
        {bubbles.map((bubble) => (
          <motion.div
            key={bubble.id}
            className="bubble"
            initial={{ y: '100vh', x: `${bubble.initialX}%` }}
            animate={{
              y: '-20vh',
              x: bubble.xPath.map(x => `${x}%`)
            }}
            transition={{
              duration: bubble.duration,
              repeat: Infinity,
              delay: bubble.delay,
              ease: 'linear'
            }}
            style={{
              width: `${bubble.width}px`,
              height: `${bubble.height}px`,
              left: `${bubble.initialX}%`,
            }}
          />
        ))}
      </div>

      {/* Elementos flotantes de seguridad */}
      {!showLogin && floatingElements.map((item, index) => {
        const IconComponent = item.icon
        return (
          <motion.div
            key={index}
            className="floating-security-icon"
            style={{
              left: `${item.x}%`,
              top: `${item.y}%`,
              color: item.color,
            }}
            animate={{
              y: [0, -20, 0],
              rotate: [-5, 5, -5],
              scale: [1, 1.1, 1],
            }}
            transition={{
              duration: 4 + index,
              repeat: Infinity,
              delay: item.delay,
              ease: 'easeInOut',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translate(30px, 30px) scale(1.2)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translate(0, 0) scale(1)'
            }}
          >
            <IconComponent size={28} />
          </motion.div>
        )
      })}

      {/* Gradient Orbs - Solo el del centro */}
      <div className={`gradient-orb orb-3 ${showLogin && (credentials.username || credentials.password) ? 'no-animation' : ''}`}></div>

      {/* Hero Section */}
      {!showLogin ? (
        <motion.div 
          className="hero-section"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <div className="container">
            <motion.div 
              className="hero-content"
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.1, duration: 0.4 }}
            >
              <div className="logo-hero">
                <div className="logo-decoration">
                  <motion.div 
                    className="glow-ring ring-1"
                    animate={{
                      rotate: 360,
                      scale: [1, 1.05, 1],
                    }}
                    transition={{
                      rotate: { duration: 20, repeat: Infinity, ease: "linear" },
                      scale: { duration: 2, repeat: Infinity, ease: "easeInOut" }
                    }}
                  />
                  <motion.div 
                    className="glow-ring ring-2"
                    animate={{
                      rotate: -360,
                      scale: [1, 1.08, 1],
                    }}
                    transition={{
                      rotate: { duration: 15, repeat: Infinity, ease: "linear" },
                      scale: { duration: 3, repeat: Infinity, ease: "easeInOut" }
                    }}
                  />
                  <motion.div 
                    className="glow-ring ring-3"
                    animate={{
                      rotate: 360,
                      scale: [1, 1.1, 1],
                    }}
                    transition={{
                      rotate: { duration: 25, repeat: Infinity, ease: "linear" },
                      scale: { duration: 4, repeat: Infinity, ease: "easeInOut" }
                    }}
                  />
                  <motion.div 
                    className="pulse-circle"
                    animate={{
                      scale: [1, 1.5, 1],
                      opacity: [0.5, 0, 0.5],
                    }}
                    transition={{
                      duration: 3,
                      repeat: Infinity,
                      ease: "easeInOut"
                    }}
                  />
                </div>
                <motion.div 
                  className="logo-glass-container"
                  whileHover={{ 
                    scale: 1.05,
                    y: -10,
                    boxShadow: "0 20px 60px rgba(16, 185, 129, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.4)"
                  }}
                  transition={{
                    type: "spring",
                    stiffness: 300,
                    damping: 20
                  }}
                >
                  <img src="/logo/ProtekSecure.png" alt="ProtekSecure" className="hero-logo-img" />
                </motion.div>
              </div>

              <div className="badge glass">
                <Zap size={14} />
                <span>Powered by AI & Computer Vision</span>
              </div>

              <h1 className="hero-title">
                <span className="company-brand">ProtekSecure</span>
                <span className="gradient-text">EPP Monitor </span>
                Sistema Inteligente de<br />
                Seguridad Industrial
              </h1>

              <div className="university-info">
                <h2 className="university-name">Universidad Católica de Pereira</h2>
                <p className="project-info">Proyecto Integrador</p>
                <div className="participants">
                  <span className="participant">Telecomunicaciones III</span>
                  <span className="separator">•</span>
                  <span className="participant">Ingeniería del Software II</span>
                </div>
              </div>

              <p className="hero-description">
                Monitoreo en tiempo real del cumplimiento de Equipos de Protección Personal
                mediante visión artificial. Protege a tu equipo con tecnología de última generación.
              </p>

              <div className="hero-buttons">
                <button className="btn btn-primary" onClick={() => setShowLogin(true)}>
                  <span>Comenzar Ahora</span>
                  <ArrowRight size={20} />
                </button>
                <button className="btn btn-glass" onClick={() => setShowLogin(true)}>
                  <span>Ver Demo</span>
                </button>
              </div>

              {/* Features Grid */}
              <div className="features-grid">
                <motion.div 
                  className="feature-card glass"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3, duration: 0.5 }}
                  whileHover={{ y: -5, scale: 1.02 }}
                >
                  <div className="feature-icon">
                    <Eye size={24} />
                  </div>
                  <h3>Detección en Tiempo Real</h3>
                  <p>Análisis automático de cámaras RTSP con IA avanzada</p>
                </motion.div>

                <motion.div 
                  className="feature-card glass"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4, duration: 0.5 }}
                  whileHover={{ y: -5, scale: 1.02 }}
                >
                  <div className="feature-icon">
                    <Shield size={24} />
                  </div>
                  <h3>Cumplimiento EPP</h3>
                  <p>Monitoreo de cascos, chalecos y gafas de seguridad</p>
                </motion.div>

                <motion.div 
                  className="feature-card glass"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5, duration: 0.5 }}
                  whileHover={{ y: -5, scale: 1.02 }}
                >
                  <div className="feature-icon">
                    <TrendingUp size={24} />
                  </div>
                  <h3>Analytics Avanzados</h3>
                  <p>Dashboard interactivo con métricas y tendencias</p>
                </motion.div>

                <motion.div 
                  className="feature-card glass"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.6, duration: 0.5 }}
                  whileHover={{ y: -5, scale: 1.02 }}
                >
                  <div className="feature-icon">
                    <Award size={24} />
                  </div>
                  <h3>Reportes Detallados</h3>
                  <p>Evidencia fotográfica y registros históricos</p>
                </motion.div>

                <motion.div 
                  className="feature-card glass"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7, duration: 0.5 }}
                  whileHover={{ y: -5, scale: 1.02 }}
                >
                  <div className="feature-icon">
                    <Brain size={24} />
                  </div>
                  <h3>Aprendizaje Autónomo</h3>
                  <p>Modelo IA que aprende y mejora continuamente de forma automática</p>
                </motion.div>

                <motion.div 
                  className="feature-card glass"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.8, duration: 0.5 }}
                  whileHover={{ y: -5, scale: 1.02 }}
                >
                  <div className="feature-icon">
                    <Mail size={24} />
                  </div>
                  <h3>Notificaciones Email</h3>
                  <p>Alertas instantáneas al correo electrónico con evidencia fotográfica</p>
                </motion.div>
              </div>
            </motion.div>
          </div>
        </motion.div>
      ) : (
        <motion.div 
          className="login-section"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          {/* Iconos de fondo que aparecen al escribir */}
          {(credentials.username || credentials.password) && (
            <>
              <motion.div 
                className="login-bg-icon icon-1"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 0.15, scale: 1 }}
                transition={{ duration: 0.6 }}
              >
                <Shield size={120} />
              </motion.div>
              <motion.div 
                className="login-bg-icon icon-2"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 0.1, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.1 }}
              >
                <Lock size={100} />
              </motion.div>
              <motion.div 
                className="login-bg-icon icon-3"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 0.12, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <HardHat size={90} />
              </motion.div>
              <motion.div 
                className="login-bg-icon icon-4"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 0.08, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.3 }}
              >
                <Eye size={110} />
              </motion.div>
            </>
          )}

          <div className="login-container glass-strong">
            {isLoading ? (
              <div className="loading-state">
                <motion.div
                  className="loading-icon"
                  animate={{ rotate: 360 }}
                  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                >
                  <Shield size={60} />
                </motion.div>
                <h2>Inicializando Sistema...</h2>
                <p>Cargando módulos de seguridad</p>
                <div className="loading-steps">
                  <motion.div 
                    className="loading-step"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3 }}
                  >
                    ✓ Conectando con API Backend
                  </motion.div>
                  <motion.div 
                    className="loading-step"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 }}
                  >
                    ✓ Verificando base de datos
                  </motion.div>
                  <motion.div 
                    className="loading-step"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.9 }}
                  >
                    ✓ Inicializando Dashboard
                  </motion.div>
                  <motion.div 
                    className="loading-step"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 1.2 }}
                  >
                    ✓ Listo para operar
                  </motion.div>
                </div>
              </div>
            ) : (
              <>
                <div className="login-header">
                  <div className="login-icon">
                    <Lock size={32} />
                  </div>
                  <h2>Acceso al Sistema</h2>
                  <p>Ingresa tus credenciales para continuar</p>
                </div>

                <form onSubmit={handleLogin} className="login-form">
                  <div className="form-group">
                    <label>Usuario</label>
                    <input
                      type="text"
                      placeholder="Ingresa tu usuario"
                      value={credentials.username}
                      onChange={(e) => setCredentials({...credentials, username: e.target.value})}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label>Contraseña</label>
                    <input
                      type="password"
                      placeholder="Ingresa tu contraseña"
                      value={credentials.password}
                      onChange={(e) => setCredentials({...credentials, password: e.target.value})}
                      required
                    />
                  </div>

                  <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '8px' }}>
                    <span>Iniciar Sesión</span>
                    <ArrowRight size={20} />
                  </button>

                  <button 
                    type="button" 
                    className="btn btn-glass" 
                    style={{ width: '100%', marginTop: '12px' }}
                    onClick={() => setShowLogin(false)}
                  >
                    Volver
                  </button>
                </form>

                <div className="login-footer">
                  <p>💡 Tip: Usa cualquier credencial para acceder (modo demo)</p>
                </div>
              </>
            )}
          </div>
        </motion.div>
      )}

      {/* Footer */}
      <footer className="landing-footer">
        <div className="footer-content">
          <div className="footer-project">
            <h4>PROYECTO COLECTIVO</h4>
            <p>Universidad Católica de Pereira</p>
          </div>
          <div className="footer-creators">
            <p className="creators-label">Creadores:</p>
            <p className="creators-names">
              Santiago Taba Sepúlveda • Juan Sebastián Moreno • Ángel David Sánchez Calle • Nicolás Patiño Rivera
            </p>
          </div>
          <div className="footer-copyright">
            <p>EPP Monitor © 2025 - Tecnología al servicio de la seguridad</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage

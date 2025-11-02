import { motion } from 'framer-motion'
import { ArrowLeft, Database, Settings, TrendingUp, AlertTriangle, FileText, Users, Zap, Shield, Lock } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import './Avanzado.css'

const Avanzado = () => {
  const navigate = useNavigate()

  const handleFeatureClick = (featureName) => {
    alert(`⚠️ Función "${featureName}" en desarrollo\n\nEsta característica estará disponible en la versión 2.0`)
  }

  const features = [
    {
      icon: <Database size={32} />,
      title: 'Gestión de Base de Datos',
      description: 'Configuración avanzada de la base de datos, backups automáticos y optimización de consultas',
      color: '#667eea'
    },
    {
      icon: <Settings size={32} />,
      title: 'Configuración del Sistema',
      description: 'Ajustes de rendimiento, configuración de cámaras, umbrales de detección y alertas',
      color: '#f093fb'
    },
    {
      icon: <TrendingUp size={32} />,
      title: 'Análisis Avanzado',
      description: 'Métricas detalladas, tendencias, predicciones y reportes personalizados',
      color: '#4facfe'
    },
    {
      icon: <AlertTriangle size={32} />,
      title: 'Sistema de Alertas',
      description: 'Configuración de notificaciones, webhooks, emails y alertas en tiempo real',
      color: '#fa709a'
    },
    {
      icon: <FileText size={32} />,
      title: 'Reportes Automáticos',
      description: 'Generación automática de reportes diarios, semanales y mensuales en PDF',
      color: '#fee140'
    },
    {
      icon: <Users size={32} />,
      title: 'Gestión de Usuarios',
      description: 'Control de accesos, roles, permisos y auditoría de actividades',
      color: '#30cfd0'
    },
    {
      icon: <Zap size={32} />,
      title: 'Integraciones API',
      description: 'Conecta con sistemas externos, webhooks y automatizaciones avanzadas',
      color: '#a8edea'
    },
    {
      icon: <Shield size={32} />,
      title: 'Seguridad Avanzada',
      description: 'Autenticación de dos factores, encriptación y logs de seguridad',
      color: '#ff9a9e'
    },
    {
      icon: <Lock size={32} />,
      title: 'Backup y Restauración',
      description: 'Programación de backups automáticos y restauración de datos',
      color: '#fbc2eb'
    }
  ]

  return (
    <div className="avanzado-page">
      <div className="gradient-bg">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
      </div>

      {/* Header */}
      <header className="avanzado-header glass">
        <motion.button
          className="btn-back"
          onClick={() => navigate('/dashboard')}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <ArrowLeft size={20} />
          <span>Volver al Dashboard</span>
        </motion.button>

        <div className="header-title">
          <h1>Opciones Avanzadas</h1>
          <p>Configuración y herramientas avanzadas del sistema</p>
        </div>

        <div className="version-badge">
          <span className="version-text">v2.0</span>
          <span className="status-badge">En Desarrollo</span>
        </div>
      </header>

      {/* Features Grid */}
      <div className="features-container">
        <div className="features-grid">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              className="feature-card glass"
              onClick={() => handleFeatureClick(feature.title)}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.02, y: -4 }}
              whileTap={{ scale: 0.98 }}
            >
              <div className="feature-icon" style={{ color: feature.color }}>
                {feature.icon}
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
              <div className="dev-badge">🚧 En desarrollo</div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Footer Info */}
      <div className="footer-info glass">
        <p>
          💡 <strong>Nota:</strong> Estas funcionalidades estarán disponibles en la versión 2.0 del sistema.
          Actualmente en fase de desarrollo.
        </p>
      </div>
    </div>
  )
}

export default Avanzado

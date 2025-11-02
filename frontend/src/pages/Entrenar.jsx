import { motion } from 'framer-motion'
import { ArrowLeft, ExternalLink } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import './Entrenar.css'

const Entrenar = () => {
  const navigate = useNavigate()

  return (
    <div className="entrenar-page">
      <div className="gradient-bg">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
      </div>

      {/* Header */}
      <header className="entrenar-header glass">
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
          <h1>Entrenar Modelo IA</h1>
          <p>Roboflow Training Platform</p>
        </div>

        <a
          href="https://app.roboflow.com/epp-taba/epp-ucp-vk3pf/upload"
          target="_blank"
          rel="noopener noreferrer"
          className="btn-external"
        >
          <ExternalLink size={18} />
          <span>Abrir en nueva pestaña</span>
        </a>
      </header>

      {/* Iframe Container */}
      <div className="iframe-container glass">
        <iframe
          src="https://app.roboflow.com/epp-taba/epp-ucp-vk3pf/upload"
          title="Roboflow Training"
          className="roboflow-iframe"
          allow="camera; microphone; clipboard-read; clipboard-write"
        />
      </div>
    </div>
  )
}

export default Entrenar

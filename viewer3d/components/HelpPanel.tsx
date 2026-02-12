'use client'

import { useState } from 'react'

export default function HelpPanel() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      {/* Botón de ayuda flotante */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          bottom: '20px',
          left: '20px',
          width: '50px',
          height: '50px',
          borderRadius: '50%',
          background: 'rgba(139, 92, 246, 0.9)',
          backdropFilter: 'blur(10px)',
          border: '2px solid rgba(255, 255, 255, 0.2)',
          color: '#fff',
          fontSize: '24px',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          transition: 'all 0.3s',
          boxShadow: '0 4px 12px rgba(139, 92, 246, 0.4)',
          zIndex: 1001
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.1) rotate(15deg)'
          e.currentTarget.style.boxShadow = '0 6px 20px rgba(139, 92, 246, 0.6)'
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1) rotate(0deg)'
          e.currentTarget.style.boxShadow = '0 4px 12px rgba(139, 92, 246, 0.4)'
        }}
      >
        {isOpen ? '✕' : '?'}
      </button>

      {/* Panel de ayuda */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          bottom: '90px',
          left: '20px',
          width: '400px',
          maxHeight: '70vh',
          overflowY: 'auto',
          background: 'rgba(10, 10, 10, 0.95)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(139, 92, 246, 0.3)',
          borderRadius: '16px',
          padding: '24px',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.5)',
          zIndex: 1000,
          animation: 'slideUp 0.3s ease-out'
        }}>
          <style jsx>{`
            @keyframes slideUp {
              from {
                opacity: 0;
                transform: translateY(20px);
              }
              to {
                opacity: 1;
                transform: translateY(0);
              }
            }
          `}</style>

          <h2 style={{
            fontSize: '20px',
            fontWeight: 'bold',
            marginBottom: '16px',
            background: 'linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text'
          }}>
            🎮 Guía de Controles
          </h2>

          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '16px',
            fontSize: '14px',
            color: '#ccc'
          }}>
            {/* Navegación */}
            <section>
              <h3 style={{
                fontSize: '14px',
                fontWeight: 'bold',
                color: '#8b5cf6',
                marginBottom: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <span>🧭</span> Navegación
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#888' }}>Click Izq + Arrastrar</span>
                  <span>Rotar</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#888' }}>Click Der + Arrastrar</span>
                  <span>Mover (Pan)</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#888' }}>Scroll</span>
                  <span>Zoom</span>
                </div>
              </div>
            </section>

            {/* Interacción */}
            <section>
              <h3 style={{
                fontSize: '14px',
                fontWeight: 'bold',
                color: '#ec4899',
                marginBottom: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <span>🖱️</span> Interacción
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#888' }}>Click en Modelo</span>
                  <span>Toggle Auto-Rotación</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#888' }}>Botón 📸</span>
                  <span>Capturar Screenshot</span>
                </div>
              </div>
            </section>

            {/* Atajos de teclado */}
            <section>
              <h3 style={{
                fontSize: '14px',
                fontWeight: 'bold',
                color: '#3b82f6',
                marginBottom: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <span>⌨️</span> Atajos (Próximamente)
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', opacity: 0.5 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#888' }}>Espacio</span>
                  <span>Play/Pause Timeline</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#888' }}>R</span>
                  <span>Reset Cámara</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#888' }}>G</span>
                  <span>Toggle Grid</span>
                </div>
              </div>
            </section>

            {/* Features */}
            <section>
              <h3 style={{
                fontSize: '14px',
                fontWeight: 'bold',
                color: '#10b981',
                marginBottom: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <span>✨</span> Features
              </h3>
              <ul style={{ 
                margin: 0, 
                paddingLeft: '20px',
                display: 'flex',
                flexDirection: 'column',
                gap: '4px'
              }}>
                <li>Core Engine Profesional</li>
                <li>Iluminación Dinámica</li>
                <li>Postprocessing (Bloom + SSAO)</li>
                <li>Performance Stats en Tiempo Real</li>
                <li>Sistema de Eventos</li>
                <li>Timeline Interno</li>
              </ul>
            </section>

            {/* Links */}
            <section style={{
              paddingTop: '16px',
              borderTop: '1px solid rgba(255, 255, 255, 0.1)'
            }}>
              <h3 style={{
                fontSize: '14px',
                fontWeight: 'bold',
                color: '#f59e0b',
                marginBottom: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <span>📚</span> Documentación
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <a 
                  href="/viewer3d/CORE_ENGINE.md" 
                  target="_blank"
                  style={{ color: '#60a5fa', textDecoration: 'none' }}
                >
                  → Core Engine Architecture
                </a>
                <a 
                  href="/viewer3d/QUICKSTART.md" 
                  target="_blank"
                  style={{ color: '#60a5fa', textDecoration: 'none' }}
                >
                  → Quick Start Guide
                </a>
                <a 
                  href="/viewer3d/SETUP.md" 
                  target="_blank"
                  style={{ color: '#60a5fa', textDecoration: 'none' }}
                >
                  → Setup Instructions
                </a>
              </div>
            </section>
          </div>

          {/* Footer */}
          <div style={{
            marginTop: '20px',
            paddingTop: '16px',
            borderTop: '1px solid rgba(255, 255, 255, 0.1)',
            fontSize: '12px',
            color: '#666',
            textAlign: 'center'
          }}>
            Core Engine v1.0 • Creador3D Ecosystem
          </div>
        </div>
      )}
    </>
  )
}

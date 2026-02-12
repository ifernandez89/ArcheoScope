'use client'

import { useState } from 'react'

export default function UI() {
  const [showInfo, setShowInfo] = useState(true)

  return (
    <>
      {/* Header */}
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        padding: '1.5rem 2rem',
        background: 'rgba(10, 10, 10, 0.8)',
        backdropFilter: 'blur(10px)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        zIndex: 1000,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div>
          <h1 style={{
            fontSize: '1.5rem',
            fontWeight: 'bold',
            margin: 0,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text'
          }}>
            🏛️ ArcheoScope 3D Viewer
          </h1>
          <p style={{
            fontSize: '0.875rem',
            color: '#888',
            margin: '0.25rem 0 0 0'
          }}>
            Visualizador interactivo de modelos 3D
          </p>
        </div>
        
        <button
          onClick={() => setShowInfo(!showInfo)}
          style={{
            padding: '0.5rem 1rem',
            background: 'rgba(255, 255, 255, 0.1)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            borderRadius: '6px',
            color: '#fff',
            cursor: 'pointer',
            fontSize: '0.875rem',
            transition: 'all 0.2s'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)'
          }}
        >
          {showInfo ? '❌ Ocultar Info' : 'ℹ️ Mostrar Info'}
        </button>
      </div>

      {/* Panel de información */}
      {showInfo && (
        <div style={{
          position: 'fixed',
          bottom: '2rem',
          left: '2rem',
          padding: '1.5rem',
          background: 'rgba(10, 10, 10, 0.9)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: '12px',
          maxWidth: '400px',
          zIndex: 1000,
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.5)'
        }}>
          <h3 style={{
            fontSize: '1rem',
            fontWeight: 'bold',
            marginBottom: '1rem',
            color: '#fff'
          }}>
            🎮 Controles
          </h3>
          
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '0.75rem',
            fontSize: '0.875rem',
            color: '#ccc'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ 
                background: 'rgba(102, 126, 234, 0.2)',
                padding: '0.25rem 0.5rem',
                borderRadius: '4px',
                fontFamily: 'monospace',
                fontSize: '0.75rem'
              }}>
                🖱️ Click Izq + Arrastrar
              </span>
              <span>Rotar</span>
            </div>
            
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ 
                background: 'rgba(102, 126, 234, 0.2)',
                padding: '0.25rem 0.5rem',
                borderRadius: '4px',
                fontFamily: 'monospace',
                fontSize: '0.75rem'
              }}>
                🖱️ Click Der + Arrastrar
              </span>
              <span>Mover (Pan)</span>
            </div>
            
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ 
                background: 'rgba(102, 126, 234, 0.2)',
                padding: '0.25rem 0.5rem',
                borderRadius: '4px',
                fontFamily: 'monospace',
                fontSize: '0.75rem'
              }}>
                🖱️ Scroll
              </span>
              <span>Zoom</span>
            </div>
            
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ 
                background: 'rgba(102, 126, 234, 0.2)',
                padding: '0.25rem 0.5rem',
                borderRadius: '4px',
                fontFamily: 'monospace',
                fontSize: '0.75rem'
              }}>
                🖱️ Click en Modelo
              </span>
              <span>Toggle Auto-Rotación</span>
            </div>
          </div>

          <div style={{
            marginTop: '1rem',
            paddingTop: '1rem',
            borderTop: '1px solid rgba(255, 255, 255, 0.1)',
            fontSize: '0.75rem',
            color: '#888'
          }}>
            💡 Tip: Usa la rueda del mouse para acercarte y ver detalles
          </div>
        </div>
      )}

      {/* Stats badge */}
      <div style={{
        position: 'fixed',
        top: '6rem',
        right: '2rem',
        padding: '0.75rem 1rem',
        background: 'rgba(10, 10, 10, 0.8)',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        borderRadius: '8px',
        fontSize: '0.75rem',
        color: '#888',
        zIndex: 1000
      }}>
        <div style={{ marginBottom: '0.5rem' }}>
          <span style={{ color: '#4ade80' }}>●</span> Modelo: warrior.glb
        </div>
        <div>
          <span style={{ color: '#60a5fa' }}>●</span> Engine: Three.js + R3F
        </div>
      </div>
    </>
  )
}

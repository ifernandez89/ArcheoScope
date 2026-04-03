'use client'

import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import { loadGameSettings, updateControlSettings } from '@/types/gameSettings'

export default function ControlsPage() {
  const router = useRouter()
  const [mouseSensitivity, setMouseSensitivity] = useState(1.0)
  const [invertY, setInvertY] = useState(false)

  // Cargar configuración guardada
  useEffect(() => {
    const settings = loadGameSettings()
    setMouseSensitivity(settings.controls.mouseSensitivity)
    setInvertY(settings.controls.invertY)
  }, [])

  // Guardar cambios
  const handleSave = () => {
    updateControlSettings({
      mouseSensitivity,
      invertY
    })
    console.log('🎮 Configuración de controles guardada')
    router.push('/menu')
  }

  return (
    <main style={{
      width: '100vw',
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'flex-start',
      background: '#000000',
      margin: 0,
      padding: '40px 20px',
      overflow: 'auto',
      color: '#ffffff'
    }}>
      <h1 style={{
        fontSize: '48px',
        marginBottom: '40px',
        letterSpacing: '4px'
      }}>
        CONTROLES
      </h1>

      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
        width: '800px',
        maxWidth: '90%',
        marginBottom: '40px'
      }}>
        {/* Navegación */}
        <div style={{
          background: 'rgba(255, 255, 255, 0.05)',
          padding: '20px',
          borderRadius: '8px',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <h2 style={{
            fontSize: '20px',
            marginBottom: '15px',
            color: '#8b5cf6',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}>
            <span>🧭</span> Navegación
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '16px' }}>
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
        </div>

        {/* Interacción */}
        <div style={{
          background: 'rgba(255, 255, 255, 0.05)',
          padding: '20px',
          borderRadius: '8px',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <h2 style={{
            fontSize: '20px',
            marginBottom: '15px',
            color: '#ec4899',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}>
            <span>🖱️</span> Interacción
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#888' }}>Click en Modelo</span>
              <span>Toggle Auto-Rotación</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#888' }}>Click en Objeto</span>
              <span>Interactuar / Recoger</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#888' }}>Menú</span>
              <span>M o ESC</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#888' }}>Botón 📸</span>
              <span>Capturar Screenshot</span>
            </div>
          </div>
        </div>

        {/* Controles de Movimiento */}
        <div style={{
          background: 'rgba(255, 255, 255, 0.05)',
          padding: '20px',
          borderRadius: '8px',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <h2 style={{
            fontSize: '20px',
            marginBottom: '15px',
            color: '#3b82f6',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}>
            <span>⌨️</span> Controles de Movimiento
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#888' }}>W / S</span>
              <span>Adelante / Atrás</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#888' }}>A / D</span>
              <span>Izquierda / Derecha</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#888' }}>Q / E</span>
              <span>Rotar Avatar</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#888' }}>SHIFT + MOUSE UP</span>
              <span>Vuelo hacia arriba</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#888' }}>SHIFT + MOUSE DOWN</span>
              <span>Vuelo hacia abajo</span>
            </div>
          </div>
        </div>

        {/* Features del Motor */}
        <div style={{
          background: 'rgba(255, 255, 255, 0.05)',
          padding: '20px',
          borderRadius: '8px',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <h2 style={{
            fontSize: '20px',
            marginBottom: '15px',
            color: '#10b981',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}>
            <span>✨</span> Features del Motor
          </h2>
          <ul style={{ 
            margin: 0, 
            paddingLeft: '20px',
            display: 'flex',
            flexDirection: 'column',
            gap: '6px',
            fontSize: '16px'
          }}>
            <li>Core Engine Profesional</li>
            <li>Iluminación Dinámica</li>
            <li>Postprocessing (Bloom + SSAO)</li>
            <li>Performance Stats en Tiempo Real</li>
            <li>Sistema de Eventos</li>
            <li>Timeline Interno</li>
          </ul>
        </div>

        {/* Configuración */}
        <div style={{
          background: 'rgba(255, 255, 255, 0.05)',
          padding: '20px',
          borderRadius: '8px',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <h2 style={{
            fontSize: '20px',
            marginBottom: '15px',
            color: '#f59e0b',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}>
            <span>⚙️</span> Configuración
          </h2>
          
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '15px'
          }}>
            <label style={{
              fontSize: '16px',
              letterSpacing: '1px'
            }}>
              Sensibilidad del Mouse: {mouseSensitivity.toFixed(1)}x
            </label>
            <input
              type="range"
              min="0.1"
              max="2.0"
              step="0.1"
              value={mouseSensitivity}
              onChange={(e) => setMouseSensitivity(parseFloat(e.target.value))}
              style={{
                width: '100%',
                height: '8px',
                borderRadius: '4px',
                outline: 'none',
                background: `linear-gradient(to right, #4a9eff 0%, #4a9eff ${(mouseSensitivity - 0.1) / 1.9 * 100}%, #333333 ${(mouseSensitivity - 0.1) / 1.9 * 100}%, #333333 100%)`,
                cursor: 'pointer'
              }}
            />
            
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              marginTop: '10px'
            }}>
              <input
                type="checkbox"
                checked={invertY}
                onChange={(e) => setInvertY(e.target.checked)}
                style={{
                  width: '20px',
                  height: '20px',
                  cursor: 'pointer'
                }}
              />
              <label style={{ fontSize: '16px' }}>
                Invertir Eje Y
              </label>
            </div>
          </div>
        </div>
      </div>

      {/* Botones - MISMO TAMAÑO QUE EL MENÚ PRINCIPAL */}
      <div style={{
        display: 'flex',
        gap: '20px'
      }}>
        <button
          onClick={() => router.push('/menu')}
          style={{
            padding: '20px 80px',
            fontSize: '24px',
            fontWeight: 'bold',
            color: '#ffffff',
            background: 'transparent',
            border: '2px solid #ffffff',
            borderRadius: '8px',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
            letterSpacing: '2px',
            textTransform: 'uppercase',
            width: '350px'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = '#ffffff'
            e.currentTarget.style.color = '#000000'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'transparent'
            e.currentTarget.style.color = '#ffffff'
          }}
        >
          Volver
        </button>

        <button
          onClick={handleSave}
          style={{
            padding: '20px 80px',
            fontSize: '24px',
            fontWeight: 'bold',
            color: '#000000',
            background: '#4a9eff',
            border: '2px solid #4a9eff',
            borderRadius: '8px',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
            letterSpacing: '2px',
            textTransform: 'uppercase',
            width: '350px'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = '#6ab7ff'
            e.currentTarget.style.borderColor = '#6ab7ff'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = '#4a9eff'
            e.currentTarget.style.borderColor = '#4a9eff'
          }}
        >
          Guardar
        </button>
      </div>
    </main>
  )
}

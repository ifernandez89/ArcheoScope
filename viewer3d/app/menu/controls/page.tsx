'use client'

import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import { loadGameSettings, updateControlSettings } from '@/types/gameSettings'

export default function ControlsPage() {
  const router = useRouter()
  const [mouseSensitivity, setMouseSensitivity] = useState(1.0)
  const [invertY, setInvertY] = useState(false)
  const [isMobile, setIsMobile] = useState(false)

  // Detectar mobile
  useEffect(() => {
    const check = () => setIsMobile(
      /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768
    )
    check()
    window.addEventListener('resize', check)
    return () => window.removeEventListener('resize', check)
  }, [])

  // Cargar configuración guardada
  useEffect(() => {
    const settings = loadGameSettings()
    setMouseSensitivity(settings.controls.mouseSensitivity)
    setInvertY(settings.controls.invertY)
  }, [])

  // Guardar cambios
  const handleSave = () => {
    updateControlSettings({ mouseSensitivity, invertY })
    console.log('🎮 Configuración de controles guardada')
    router.push('/menu')
  }

  // Estilos comunes
  const sectionStyle = (isMob: boolean) => ({
    background: 'rgba(255, 255, 255, 0.05)',
    padding: isMob ? '16px' : '20px',
    borderRadius: '8px',
    border: '1px solid rgba(255, 255, 255, 0.1)'
  })

  const h2Style = (color: string, isMob: boolean) => ({
    fontSize: isMob ? '18px' : '20px',
    marginBottom: isMob ? '12px' : '15px',
    color,
    display: 'flex' as const,
    alignItems: 'center' as const,
    gap: '10px',
    fontFamily: 'Archeoscope, serif'
  })

  const rowStyle = { display: 'flex' as const, justifyContent: 'space-between' as const }
  const labelStyle = { color: '#888' }

  return (
    <main style={{
      width: '100vw', height: '100vh',
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'flex-start',
      background: '#000000', margin: 0,
      padding: isMobile ? '20px 16px' : '40px 20px',
      overflow: 'auto', color: '#ffffff'
    }}>
      <h1 style={{
        fontSize: isMobile ? '28px' : '48px',
        marginBottom: isMobile ? '24px' : '40px',
        letterSpacing: '4px',
        fontFamily: 'Archeoscope, serif'
      }}>
        CONTROLES
      </h1>

      <div style={{
        display: 'flex', flexDirection: 'column',
        gap: isMobile ? '16px' : '20px',
        width: isMobile ? '100%' : '800px',
        maxWidth: '90%',
        marginBottom: isMobile ? '24px' : '40px'
      }}>

        {/* ═══════════════════════════════════════════════════════════════════
            MOBILE CONTROLS
        ═══════════════════════════════════════════════════════════════════ */}
        {isMobile ? (
          <>
            {/* Movimiento de Nave — Escena Terrestre */}
            <div style={sectionStyle(true)}>
              <h2 style={h2Style('#3b82f6', true)}>
                <span>🛸</span> Movimiento de Nave (Terrestre)
              </h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '15px' }}>
                <div style={rowStyle}><span style={labelStyle}>▲ / ▼</span><span>Adelante / Atrás</span></div>
                <div style={rowStyle}><span style={labelStyle}>◀ / ▶</span><span>Izquierda / Derecha</span></div>
                <div style={rowStyle}><span style={labelStyle}>↺ / ↻</span><span>Rotar nave</span></div>
                <div style={rowStyle}><span style={labelStyle}>Botón habilidad</span><span>Activar poder especial</span></div>
              </div>
            </div>

            {/* Navegación Espacial */}
            <div style={sectionStyle(true)}>
              <h2 style={h2Style('#8b5cf6', true)}>
                <span>🌌</span> Navegación Espacial
              </h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '15px' }}>
                <div style={rowStyle}><span style={labelStyle}>1 dedo + arrastrar</span><span>Rotar cámara</span></div>
                <div style={rowStyle}><span style={labelStyle}>2 dedos + pinza</span><span>Zoom</span></div>
                <div style={rowStyle}><span style={labelStyle}>Tap en planeta</span><span>Ver info / Viajar</span></div>
              </div>
            </div>

            {/* Interacción */}
            <div style={sectionStyle(true)}>
              <h2 style={h2Style('#ec4899', true)}>
                <span>🖱️</span> Interacción
              </h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '15px' }}>
                <div style={rowStyle}><span style={labelStyle}>Tap en objeto</span><span>Interactuar / Recoger</span></div>
                <div style={rowStyle}><span style={labelStyle}>Tap en NPC</span><span>Hablar</span></div>
                <div style={rowStyle}><span style={labelStyle}>Botón ☰</span><span>Menú</span></div>
              </div>
            </div>

            {/* Cómo Jugar */}
            <div style={{
              background: 'rgba(102, 126, 234, 0.08)',
              padding: '16px', borderRadius: '8px',
              border: '1px solid rgba(102, 126, 234, 0.3)'
            }}>
              <h2 style={h2Style('#a78bfa', true)}>
                <span>🎮</span> Cómo Jugar
              </h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '14px', lineHeight: '1.5' }}>
                <p style={{ color: '#ccc', margin: 0 }}>🌍 Explora el sistema solar y viaja a la Tierra.</p>
                <p style={{ color: '#ccc', margin: 0 }}>🗿 Toca los NPCs para interactuar con ellos.</p>
                <p style={{ color: '#ccc', margin: 0 }}>📦 Recoge objetos sagrados y completa misiones.</p>
                <p style={{ color: '#ccc', margin: 0 }}>⚠️ Cuidado: algunas acciones son irreversibles.</p>
              </div>
            </div>
          </>
        ) : (
          <>
            {/* ═══════════════════════════════════════════════════════════════════
                PC CONTROLS
            ═══════════════════════════════════════════════════════════════════ */}
            {/* Navegación */}
            <div style={sectionStyle(false)}>
              <h2 style={h2Style('#8b5cf6', false)}><span>🧭</span> Navegación</h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '19px' }}>
                <div style={rowStyle}><span style={labelStyle}>Click Izq + Arrastrar</span><span>Rotar</span></div>
                <div style={rowStyle}><span style={labelStyle}>Click Der + Arrastrar</span><span>Mover (Pan)</span></div>
                <div style={rowStyle}><span style={labelStyle}>Scroll</span><span>Zoom</span></div>
              </div>
            </div>

            {/* Interacción */}
            <div style={sectionStyle(false)}>
              <h2 style={h2Style('#ec4899', false)}><span>🖱️</span> Interacción</h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '19px' }}>
                <div style={rowStyle}><span style={labelStyle}>Click en Modelo</span><span>Toggle Auto-Rotación</span></div>
                <div style={rowStyle}><span style={labelStyle}>Click en Objeto</span><span>Interactuar / Recoger</span></div>
                <div style={rowStyle}><span style={labelStyle}>Menú</span><span>M o ESC</span></div>
                <div style={rowStyle}><span style={labelStyle}>Botón 📸</span><span>Capturar Screenshot</span></div>
              </div>
            </div>

            {/* Cómo Jugar */}
            <div style={{
              background: 'rgba(102, 126, 234, 0.08)',
              padding: '20px', borderRadius: '8px',
              border: '1px solid rgba(102, 126, 234, 0.3)'
            }}>
              <h2 style={h2Style('#a78bfa', false)}><span>🎮</span> Cómo Jugar</h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '18px', lineHeight: '1.6' }}>
                <p style={{ color: '#ccc', margin: 0 }}>🌍 Explora el globo terráqueo y viaja a sitios arqueológicos.</p>
                <p style={{ color: '#ccc', margin: 0 }}>🗿 Interactúa con los NPCs haciendo <strong style={{color:'#fff'}}>click</strong> sobre ellos.</p>
                <p style={{ color: '#ccc', margin: 0 }}>📦 Recoge objetos sagrados y completa misiones en cada sitio.</p>
                <p style={{ color: '#ccc', margin: 0 }}>🌋 Completa las 4 misiones principales y activa la final.</p>
                <p style={{ color: '#ccc', margin: 0 }}>⚠️ Cuidado: algunas acciones tienen consecuencias irreversibles.</p>
              </div>
            </div>

            {/* Controles de Movimiento */}
            <div style={sectionStyle(false)}>
              <h2 style={h2Style('#3b82f6', false)}><span>⌨️</span> Controles de Movimiento</h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '19px' }}>
                <div style={rowStyle}><span style={labelStyle}>W / S</span><span>Adelante / Atrás</span></div>
                <div style={rowStyle}><span style={labelStyle}>A / D</span><span>Izquierda / Derecha</span></div>
                <div style={rowStyle}><span style={labelStyle}>Q / E</span><span>Rotar Avatar</span></div>
                <div style={rowStyle}><span style={labelStyle}>SHIFT + MOUSE UP</span><span>Vuelo hacia arriba</span></div>
                <div style={rowStyle}><span style={labelStyle}>SHIFT + MOUSE DOWN</span><span>Vuelo hacia abajo</span></div>
                <div style={rowStyle}><span style={labelStyle}>BARRA ESPACIADORA</span><span>Habilidad Espacial</span></div>
              </div>
            </div>

            {/* Features del Motor */}
            <div style={sectionStyle(false)}>
              <h2 style={h2Style('#10b981', false)}><span>✨</span> Features del Motor</h2>
              <ul style={{ margin: 0, paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '19px' }}>
                <li>Core Engine Profesional</li>
                <li>Iluminación Dinámica</li>
                <li>Postprocessing (Bloom + SSAO)</li>
                <li>Performance Stats en Tiempo Real</li>
                <li>Sistema de Eventos</li>
                <li>Timeline Interno</li>
              </ul>
            </div>

            {/* Configuración */}
            <div style={sectionStyle(false)}>
              <h2 style={h2Style('#f59e0b', false)}><span>⚙️</span> Configuración</h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                <label style={{ fontSize: '19px', letterSpacing: '1px' }}>
                  Sensibilidad del Mouse: {mouseSensitivity.toFixed(1)}x
                </label>
                <input
                  type="range" min="0.1" max="2.0" step="0.1"
                  value={mouseSensitivity}
                  onChange={(e) => setMouseSensitivity(parseFloat(e.target.value))}
                  style={{
                    width: '100%', height: '8px', borderRadius: '4px', outline: 'none',
                    background: `linear-gradient(to right, #4a9eff 0%, #4a9eff ${(mouseSensitivity - 0.1) / 1.9 * 100}%, #333333 ${(mouseSensitivity - 0.1) / 1.9 * 100}%, #333333 100%)`,
                    cursor: 'pointer'
                  }}
                />
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '10px' }}>
                  <input
                    type="checkbox" checked={invertY}
                    onChange={(e) => setInvertY(e.target.checked)}
                    style={{ width: '20px', height: '20px', cursor: 'pointer' }}
                  />
                  <label style={{ fontSize: '19px' }}>Invertir Eje Y</label>
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Botones */}
      <div style={{
        display: 'flex',
        gap: isMobile ? '12px' : '20px',
        flexDirection: isMobile ? 'column' : 'row',
        width: isMobile ? '100%' : 'auto'
      }}>
        <button
          onClick={() => router.push('/menu')}
          style={{
            padding: isMobile ? '14px 24px' : '20px 80px',
            fontSize: isMobile ? '16px' : '24px',
            fontWeight: 'bold', color: '#ffffff',
            background: 'transparent', border: '2px solid #ffffff',
            borderRadius: '8px', cursor: 'pointer',
            transition: 'all 0.3s ease', letterSpacing: '2px',
            textTransform: 'uppercase', width: isMobile ? '100%' : '350px'
          }}
          onMouseEnter={(e) => { e.currentTarget.style.background = '#ffffff'; e.currentTarget.style.color = '#000000' }}
          onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = '#ffffff' }}
        >
          Volver
        </button>

        {!isMobile && (
          <button
            onClick={handleSave}
            style={{
              padding: '20px 80px', fontSize: '24px',
              fontWeight: 'bold', color: '#000000',
              background: '#4a9eff', border: '2px solid #4a9eff',
              borderRadius: '8px', cursor: 'pointer',
              transition: 'all 0.3s ease', letterSpacing: '2px',
              textTransform: 'uppercase', width: '350px'
            }}
            onMouseEnter={(e) => { e.currentTarget.style.background = '#6ab7ff'; e.currentTarget.style.borderColor = '#6ab7ff' }}
            onMouseLeave={(e) => { e.currentTarget.style.background = '#4a9eff'; e.currentTarget.style.borderColor = '#4a9eff' }}
          >
            Guardar
          </button>
        )}
      </div>
    </main>
  )
}

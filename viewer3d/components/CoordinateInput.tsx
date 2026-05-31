'use client'

import { useState, useEffect } from 'react'
import { loadMissionState } from '@/types/missionState'

interface CoordinateInputProps {
  onCoordinateSubmit: (lat: number, lon: number) => void
  currentLocation?: { lat: number, lon: number } | null
  disabled?: boolean
  /** Modo actual del juego — el botón solo pulsa en modo globo */
  mode?: 'globe' | 'transition' | 'model' | 'exploration'
  /** Clima actual — afecta el color del botón */
  weatherCode?: number
}

// Cuerpos celestes — solo necesitan id, nombre y metadata.
// La posición de cámara se calcula dinámicamente desde la posición real del planeta.
const CELESTIAL_BODIES = [
  { id: 'sun',     name: 'Sol',      emoji: '☀️', color: '#fbbf24', description: 'Estrella central · 1.4M km diámetro' },
  { id: 'mercury', name: 'Mercurio', emoji: '⚫', color: '#9c9c9c', description: 'Planeta rocoso · 88 días/órbita' },
  { id: 'venus',   name: 'Venus',    emoji: '🟡', color: '#f5e6d3', description: 'Planeta rocoso · 225 días/órbita' },
  { id: 'earth',   name: 'Tierra',   emoji: '🌍', color: '#4A90E2', description: 'Nuestro hogar · 365 días/órbita' },
  { id: 'moon',    name: 'Luna',     emoji: '🌕', color: '#e2e8f0', description: 'Satélite natural · 27 días/órbita' },
  { id: 'mars',    name: 'Marte',    emoji: '🔴', color: '#E27B58', description: 'Planeta rojo · 687 días/órbita' },
  { id: 'jupiter', name: 'Júpiter',  emoji: '🟠', color: '#D4A574', description: 'Gigante gaseoso · 12 años/órbita' },
  { id: 'saturn',  name: 'Saturno',  emoji: '🪐', color: '#FAD5A5', description: 'Anillos icónicos · 29 años/órbita' },
  { id: 'uranus',  name: 'Urano',    emoji: '🔵', color: '#4FD0E7', description: 'Gigante de hielo · 84 años/órbita' },
  { id: 'neptune', name: 'Neptuno',  emoji: '💙', color: '#4166F5', description: 'Vientos más rápidos · 165 años/órbita' },
  { id: 'pluto',   name: 'Plutón',   emoji: '⚪', color: '#A0826D', description: 'Planeta enano · 248 años/órbita' },
]

// Sitios arqueológicos con nombre
const FAMOUS_SITES = [
  { lat: -16.56164569638123, lon: -68.67952141492464, name: 'Puma Punku', emoji: '🗿' },
  { lat: 29.9792, lon: 31.1342, name: 'Giza', emoji: '🔺' },
  { lat: 19.6925, lon: -98.8438, name: 'Teotihuacán', emoji: '🏛️' },
  { lat: 18.4667, lon: -95.4500, name: 'Tres Zapotes', emoji: '🗿' },
  { lat: -27.1254, lon: -109.2778, name: 'Isla de Pascua', emoji: '🗿' },
  { lat: -75.2509, lon: 0.0714, name: 'Antártida', emoji: '❄️' },
  { lat: 37.2231, lon: 38.9225, name: 'Göbekli Tepe', emoji: '🏺' },
]

export default function CoordinateInput({
  onCoordinateSubmit,
  currentLocation,
  disabled = false,
  mode = 'globe',
  weatherCode = 0,
}: CoordinateInputProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [lat, setLat] = useState(currentLocation?.lat.toFixed(4) || '')
  const [lon, setLon] = useState(currentLocation?.lon.toFixed(4) || '')
  const [pulse, setPulse] = useState(false)
  const [missionsCompleted, setMissionsCompleted] = useState(0)
  const [zoomToast, setZoomToast] = useState<string | null>(null)

  const isMobile = typeof window !== 'undefined' &&
    (/Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768)

  // Leer misiones completadas para el color reactivo
  useEffect(() => {
    try {
      const ms = loadMissionState()
      setMissionsCompleted(ms.stats.totalMissionsCompleted)
    } catch {}
  }, [])

  // Pulso periódico cuando está en modo globo y no está abierto
  useEffect(() => {
    if (mode !== 'globe' || isOpen || disabled) return
    const interval = setInterval(() => {
      setPulse(true)
      setTimeout(() => setPulse(false), 800)
    }, 4000)
    return () => clearInterval(interval)
  }, [mode, isOpen, disabled])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const latitude = parseFloat(lat)
    const longitude = parseFloat(lon)
    if (isNaN(latitude) || isNaN(longitude)) { alert('Por favor ingresa coordenadas válidas'); return }
    if (latitude < -90 || latitude > 90) { alert('Latitud debe estar entre -90 y 90'); return }
    if (longitude < -180 || longitude > 180) { alert('Longitud debe estar entre -180 y 180'); return }
    onCoordinateSubmit(latitude, longitude)
    setIsOpen(false)
  }

  // Enfocar cuerpo celeste — emite evento; RealisticSolarSystem calcula la posición real
  const focusCelestialBody = (body: typeof CELESTIAL_BODIES[0]) => {
    window.dispatchEvent(new CustomEvent('celestial-focus', {
      detail: { id: body.id }
    }))
    setIsOpen(false)
    // Mostrar mensaje orientativo de zoom unos segundos
    setZoomToast(`${body.emoji} Viajando a ${body.name} · usá la rueda del mouse para acercar/alejar 🔍`)
    setTimeout(() => setZoomToast(null), 5000)
  }

  // Color reactivo del botón según estado del juego
  const getButtonColor = () => {
    if (disabled) return 'rgba(60,60,60,0.5)'
    if (missionsCompleted >= 5) return 'rgba(34,197,94,0.9)'   // verde — todas completadas
    if (missionsCompleted >= 3) return 'rgba(251,191,36,0.9)'  // dorado — progreso
    if (weatherCode >= 80) return 'rgba(239,68,68,0.9)'        // rojo — tormenta
    return 'rgba(102,126,234,0.9)'                              // azul — default
  }

  const getButtonGlow = () => {
    if (disabled) return 'none'
    if (missionsCompleted >= 5) return '0 0 20px rgba(34,197,94,0.6), 0 4px 12px rgba(0,0,0,0.4)'
    if (missionsCompleted >= 3) return '0 0 20px rgba(251,191,36,0.5), 0 4px 12px rgba(0,0,0,0.4)'
    if (weatherCode >= 80) return '0 0 20px rgba(239,68,68,0.5), 0 4px 12px rgba(0,0,0,0.4)'
    return '0 0 16px rgba(102,126,234,0.4), 0 4px 12px rgba(0,0,0,0.4)'
  }

  const btnColor = getButtonColor()
  const btnGlow = getButtonGlow()

  return (
    <>
      <style>{`
        @keyframes coordPulse {
          0%   { transform: scale(1); box-shadow: ${btnGlow}; }
          40%  { transform: scale(1.06); box-shadow: 0 0 28px rgba(102,126,234,0.8), 0 4px 16px rgba(0,0,0,0.5); }
          100% { transform: scale(1); box-shadow: ${btnGlow}; }
        }
        @keyframes coordShake {
          0%,100% { transform: translateX(0) }
          20%     { transform: translateX(-3px) }
          40%     { transform: translateX(3px) }
          60%     { transform: translateX(-2px) }
          80%     { transform: translateX(2px) }
        }
        .coord-btn-pulse { animation: coordPulse 0.8s ease-out; }
        .coord-btn-shake { animation: coordShake 0.5s ease-out; }
      `}</style>

      {/* ── Botón principal ── */}
      <button
        onClick={() => !disabled && setIsOpen(!isOpen)}
        disabled={disabled}
        className={pulse ? 'coord-btn-pulse' : ''}
        style={{
          position: 'fixed',
          top: '20px',
          right: '20px',
          zIndex: 1001,
          padding: '12px 20px',
          background: btnColor,
          border: `1.5px solid ${disabled ? 'rgba(255,255,255,0.1)' : 'rgba(255,255,255,0.35)'}`,
          borderRadius: '10px',
          color: disabled ? 'rgba(255,255,255,0.3)' : 'white',
          fontSize: '14px',
          fontWeight: 'bold',
          cursor: disabled ? 'not-allowed' : 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          transition: 'background 0.3s, box-shadow 0.3s',
          boxShadow: btnGlow,
          opacity: disabled ? 0.5 : 1,
          letterSpacing: '0.5px',
          minHeight: '44px',
          WebkitTapHighlightColor: 'transparent',
        }}
        onMouseEnter={(e) => {
          if (!disabled) e.currentTarget.style.background = btnColor.replace('0.9', '1')
        }}
        onMouseLeave={(e) => {
          if (!disabled) e.currentTarget.style.background = btnColor
        }}
      >
        {disabled ? '🔒 Bloqueado' : (
          <>
            <span style={{ fontSize: '16px' }}>🧭</span>
            Coordenadas
            {missionsCompleted > 0 && (
              <span style={{
                background: 'rgba(255,255,255,0.2)',
                borderRadius: '10px',
                padding: '1px 7px',
                fontSize: '11px',
                fontWeight: 'bold',
              }}>
                {missionsCompleted}/6
              </span>
            )}
          </>
        )}
      </button>

      {/* ── Panel ── */}
      {isOpen && (
        <div style={{
          position: 'fixed',
          top: '72px',
          right: '20px',
          zIndex: 1000,
          width: '320px',
          maxHeight: 'calc(100vh - 90px)',
          background: 'rgba(5,5,15,0.97)',
          backdropFilter: 'blur(16px)',
          borderRadius: '14px',
          padding: '20px',
          boxShadow: '0 8px 40px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.08)',
          border: '1px solid rgba(255,255,255,0.1)',
          overflowY: 'auto',
          overflowX: 'hidden',
        }}>
          {/* Header */}
          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            marginBottom: '16px',
            position: 'sticky', top: '-20px',
            background: 'rgba(5,5,15,0.97)',
            paddingTop: '20px', paddingBottom: '10px',
            marginTop: '-20px', zIndex: 1,
          }}>
            <h3 style={{ margin: 0, color: 'white', fontSize: '16px', fontWeight: 'bold' }}>
              🧭 Navegación
            </h3>
            <button
              onClick={() => setIsOpen(false)}
              style={{
                background: 'rgba(255,255,255,0.08)', border: 'none',
                borderRadius: '6px', color: 'rgba(255,255,255,0.6)',
                fontSize: '18px', cursor: 'pointer', padding: '2px 8px',
                lineHeight: 1,
              }}
            >×</button>
          </div>

          {/* Ubicación actual */}
          {currentLocation && (
            <div style={{
              padding: '10px 12px',
              background: 'rgba(102,126,234,0.12)',
              borderRadius: '8px',
              marginBottom: '16px',
              fontSize: '12px',
              color: 'rgba(255,255,255,0.7)',
              border: '1px solid rgba(102,126,234,0.2)',
            }}>
              <div style={{ fontWeight: 'bold', marginBottom: '4px', color: '#a5b4fc' }}>📍 Ubicación actual</div>
              <div>{currentLocation.lat.toFixed(4)}°, {currentLocation.lon.toFixed(4)}°</div>
            </div>
          )}

          {/* Formulario manual — solo PC */}
          {!isMobile && (
            <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
              <div style={{ marginBottom: '10px' }}>
                <label style={{ display: 'block', color: 'rgba(255,255,255,0.6)', fontSize: '11px', marginBottom: '4px', letterSpacing: '0.5px' }}>
                  LATITUD (-90 a 90)
                </label>
                <input
                  type="text" value={lat} onChange={(e) => setLat(e.target.value)}
                  placeholder="-13.1631"
                  style={{
                    width: '100%', padding: '9px 12px',
                    background: 'rgba(255,255,255,0.07)',
                    border: '1px solid rgba(255,255,255,0.15)',
                    borderRadius: '7px', color: 'white', fontSize: '14px', outline: 'none',
                    boxSizing: 'border-box',
                  }}
                />
              </div>
              <div style={{ marginBottom: '12px' }}>
                <label style={{ display: 'block', color: 'rgba(255,255,255,0.6)', fontSize: '11px', marginBottom: '4px', letterSpacing: '0.5px' }}>
                  LONGITUD (-180 a 180)
                </label>
                <input
                  type="text" value={lon} onChange={(e) => setLon(e.target.value)}
                  placeholder="-72.5450"
                  style={{
                    width: '100%', padding: '9px 12px',
                    background: 'rgba(255,255,255,0.07)',
                    border: '1px solid rgba(255,255,255,0.15)',
                    borderRadius: '7px', color: 'white', fontSize: '14px', outline: 'none',
                    boxSizing: 'border-box',
                  }}
                />
              </div>
              <button
                type="submit"
                style={{
                  width: '100%', padding: '11px',
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  border: 'none', borderRadius: '8px', color: 'white',
                  fontSize: '14px', fontWeight: 'bold', cursor: 'pointer',
                  letterSpacing: '0.5px',
                }}
              >
                🌍 Viajar
              </button>
            </form>
          )}

          {/* ── Sitios arqueológicos ── */}
          <div style={{ marginBottom: '20px' }}>
            <div style={{
              color: 'rgba(255,255,255,0.45)', fontSize: '10px',
              marginBottom: '8px', fontWeight: 'bold', letterSpacing: '1.5px',
            }}>
              🏛️ SITIOS ARQUEOLÓGICOS
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
              {FAMOUS_SITES.map((site, i) => (
                <button
                  key={i}
                  onClick={() => {
                    if (isMobile) {
                      onCoordinateSubmit(site.lat, site.lon)
                      setIsOpen(false)
                    } else {
                      setLat(site.lat.toFixed(4))
                      setLon(site.lon.toFixed(4))
                    }
                  }}
                  style={{
                    padding: '8px 12px',
                    background: 'rgba(255,255,255,0.04)',
                    border: '1px solid rgba(255,255,255,0.08)',
                    borderRadius: '7px', color: 'white',
                    cursor: 'pointer', fontSize: '13px',
                    textAlign: 'left', transition: 'all 0.15s',
                    display: 'flex', alignItems: 'center', gap: '8px',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = 'rgba(102,126,234,0.18)'
                    e.currentTarget.style.borderColor = 'rgba(102,126,234,0.4)'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = 'rgba(255,255,255,0.04)'
                    e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)'
                  }}
                >
                  <span style={{ fontSize: '15px' }}>{site.emoji}</span>
                  <div>
                    <div style={{ fontWeight: '600', fontSize: '13px' }}>{site.name}</div>
                    <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.4)' }}>
                      {site.lat.toFixed(4)}°, {site.lon.toFixed(4)}°
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* ── Cuerpos celestes — solo en modo globo (espacio) ── */}
          {(mode === 'globe' || mode === 'transition') && (
          <div>
            <div style={{
              color: 'rgba(255,255,255,0.45)', fontSize: '10px',
              marginBottom: '8px', fontWeight: 'bold', letterSpacing: '1.5px',
            }}>
              🪐 CUERPOS CELESTES
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
              {CELESTIAL_BODIES.map((body) => (
                <button
                  key={body.id}
                  onClick={() => focusCelestialBody(body)}
                  style={{
                    padding: '8px 12px',
                    background: `rgba(${body.color === '#fbbf24' ? '251,191,36' : '255,255,255'},0.04)`,
                    border: `1px solid ${body.color}22`,
                    borderRadius: '7px', color: 'white',
                    cursor: 'pointer', fontSize: '13px',
                    textAlign: 'left', transition: 'all 0.15s',
                    display: 'flex', alignItems: 'center', gap: '8px',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = `${body.color}22`
                    e.currentTarget.style.borderColor = `${body.color}55`
                    e.currentTarget.style.boxShadow = `0 0 12px ${body.color}33`
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = 'rgba(255,255,255,0.04)'
                    e.currentTarget.style.borderColor = `${body.color}22`
                    e.currentTarget.style.boxShadow = 'none'
                  }}
                >
                  <span style={{ fontSize: '16px' }}>{body.emoji}</span>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: '600', fontSize: '13px', color: body.color }}>
                      {body.name}
                    </div>
                    <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.35)' }}>
                      {body.description}
                    </div>
                  </div>
                  <span style={{ fontSize: '10px', color: 'rgba(255,255,255,0.25)' }}>→</span>
                </button>
              ))}
            </div>
          </div>
          )}

          {/* Nota — solo en modo globo */}
          {(mode === 'globe' || mode === 'transition') && (
          <div style={{
            marginTop: '14px', padding: '10px 12px',
            background: 'rgba(255,255,255,0.03)',
            borderRadius: '8px', fontSize: '11px',
            color: 'rgba(255,255,255,0.3)', lineHeight: '1.5',
          }}>
            💡 Los cuerpos celestes mueven la cámara a una vista cercana en el Sistema Solar
          </div>
          )}
        </div>
      )}

      {/* Toast orientativo de zoom — aparece al viajar a un cuerpo celeste */}
      {zoomToast && (
        <div style={{
          position: 'fixed',
          bottom: '40px',
          left: '50%',
          transform: 'translateX(-50%)',
          zIndex: 1002,
          background: 'rgba(5,5,15,0.92)',
          backdropFilter: 'blur(12px)',
          border: '1.5px solid rgba(102,126,234,0.5)',
          borderRadius: '14px',
          padding: '14px 24px',
          color: 'white',
          fontSize: '14px',
          fontWeight: 500,
          letterSpacing: '0.3px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.5), 0 0 20px rgba(102,126,234,0.2)',
          maxWidth: '90vw',
          textAlign: 'center',
          animation: 'zoomToastIn 0.35s ease-out',
          pointerEvents: 'none',
        }}>
          {zoomToast}
        </div>
      )}

      {/* Animaciones del toast */}
      <style>{`
        @keyframes zoomToastIn {
          from { opacity: 0; transform: translateX(-50%) translateY(12px); }
          to   { opacity: 1; transform: translateX(-50%) translateY(0); }
        }
      `}</style>

      {/* Scrollbar personalizada */}
      <style>{`
        div::-webkit-scrollbar { width: 6px; }
        div::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); border-radius: 3px; }
        div::-webkit-scrollbar-thumb { background: rgba(102,126,234,0.4); border-radius: 3px; }
        div::-webkit-scrollbar-thumb:hover { background: rgba(102,126,234,0.7); }
      `}</style>
    </>
  )
}

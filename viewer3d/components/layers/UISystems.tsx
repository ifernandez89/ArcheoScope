'use client'

import React from 'react'

/**
 * UISystems - Controles UI, Botones, Información
 * 
 * Responsabilidades:
 * - Botones de control (volver al globo, cambiar modo)
 * - Información de ubicación
 * - Instrucciones de movimiento
 * - Transiciones cinematográficas
 * 
 * Cargado SIEMPRE (no lazy). UI crítica.
 * Muy pequeño, cero overhead.
 */

interface UISystemsProps {
  mode: 'globe' | 'transition' | 'model' | 'exploration'
  location?: { lat: number; lon: number } | null
  selectedSite?: { name: string; culture: string; period: string } | null
  movementMode?: 'orbit' | 'avatar'
  showLocationInfo?: boolean
  onReturnToGlobe?: () => void
  onToggleMovementMode?: () => void
  onToggleLocationInfo?: () => void
  onUfoChange?: (ufoNumber: number) => void
  currentUfo?: number
}

export default function UISystems({
  mode,
  location,
  selectedSite,
  movementMode = 'avatar',
  showLocationInfo = false,
  onReturnToGlobe,
  onToggleMovementMode,
  onToggleLocationInfo,
  onUfoChange,
  currentUfo = 1
}: UISystemsProps) {
  const [showUfoSelector, setShowUfoSelector] = React.useState(false)

  return (
    <>
      {/* Transición cinematográfica */}
      {mode === 'transition' && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            zIndex: 2000,
            background: 'radial-gradient(circle, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.95) 100%)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            animation: 'fadeIn 0.5s ease-in-out',
            pointerEvents: 'none'
          }}
        >
          <div
            style={{
              fontSize: '48px',
              marginBottom: '20px',
              animation: 'pulse 1.5s infinite'
            }}
          >
            🌍
          </div>
          <div
            style={{
              color: 'white',
              fontSize: '24px',
              fontWeight: 'bold',
              textShadow: '0 0 20px rgba(102, 126, 234, 0.8)'
            }}
          >
            {selectedSite
              ? `Viajando a ${selectedSite.name}...`
              : location
                ? 'Teletransportando...'
                : 'Regresando al globo...'}
          </div>
          {location && (
            <div
              style={{
                color: '#888',
                fontSize: '14px',
                marginTop: '10px'
              }}
            >
              📍 Lat: {location.lat.toFixed(4)}° | Lon: {location.lon.toFixed(4)}°
            </div>
          )}
          {selectedSite && (
            <div
              style={{
                color: '#fbbf24',
                fontSize: '12px',
                marginTop: '8px'
              }}
            >
              {selectedSite.culture} • {selectedSite.period}
            </div>
          )}
        </div>
      )}

      {/* Botones de control */}
      {mode === 'model' && (
        <div
          style={{
            position: 'fixed',
            top: '20px',
            left: '20px',
            zIndex: 1001,
            display: 'flex',
            flexDirection: 'column',
            gap: '10px',
            pointerEvents: 'auto'
          }}
        >
          <ControlButton
            label="🌍 Volver al Globo"
            onClick={onReturnToGlobe}
            color="rgba(102, 126, 234, 0.9)"
          />

          {/* Botón UFO con selector desplegable */}
          <div style={{ position: 'relative' }}>
            <ControlButton
              label={`ðŸŒ`}
              onClick={() => setShowUfoSelector(!showUfoSelector)}
              color="rgba(139, 92, 246, 0.9)"
            />
            
            {/* Selector desplegable de UFOs */}
            {showUfoSelector && (
              <div
                style={{
                  position: 'absolute',
                  top: '100%',
                  left: 0,
                  marginTop: '5px',
                  background: 'rgba(0, 0, 0, 0.9)',
                  backdropFilter: 'blur(10px)',
                  borderRadius: '8px',
                  border: '1px solid rgba(255,255,255,0.3)',
                  padding: '8px',
                  minWidth: '150px',
                  zIndex: 2000,
                  pointerEvents: 'auto'
                }}
              >
                {[1, 2, 3, 4, 5].map(ufoNum => (
                  <button
                    key={ufoNum}
                    onClick={() => {
                      onUfoChange?.(ufoNum)
                      setShowUfoSelector(false)
                    }}
                    style={{
                      width: '100%',
                      padding: '8px 12px',
                      background: currentUfo === ufoNum 
                        ? 'rgba(139, 92, 246, 0.5)' 
                        : 'transparent',
                      border: 'none',
                      borderRadius: '4px',
                      color: 'white',
                      fontSize: '14px',
                      cursor: 'pointer',
                      textAlign: 'left',
                      marginBottom: '4px',
                      transition: 'all 0.2s'
                    }}
                    onMouseEnter={(e) => {
                      if (currentUfo !== ufoNum) {
                        e.currentTarget.style.background = 'rgba(139, 92, 246, 0.3)'
                      }
                    }}
                    onMouseLeave={(e) => {
                      if (currentUfo !== ufoNum) {
                        e.currentTarget.style.background = 'transparent'
                      }
                    }}
                  >
                    🌍
                  </button>
                ))}
              </div>
            )}
          </div>

          <ControlButton
            label={`ℹ️ ${showLocationInfo ? 'Ocultar Info' : 'Mostrar Info'}`}
            onClick={onToggleLocationInfo}
            color={
              showLocationInfo
                ? 'rgba(102, 126, 234, 0.9)'
                : 'rgba(75, 85, 99, 0.7)'
            }
          />
        </div>
      )}

      {/* Instrucciones de movimiento */}
      {mode === 'model' && movementMode === 'avatar' && (
        <div
          style={{
            position: 'fixed',
            bottom: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            zIndex: 1001,
            background: 'rgba(0, 0, 0, 0.8)',
            backdropFilter: 'blur(10px)',
            padding: '12px 24px',
            borderRadius: '8px',
            border: '1px solid rgba(255,255,255,0.2)',
            color: 'white',
            fontSize: '12px',
            display: 'flex',
            gap: '20px',
            pointerEvents: 'none'
          }}
        >
          <span>⬆️ W/S - Adelante/Atrás</span>
          <span>A/D - Izquierda/Derecha</span>
          <span>Q/E - Rotar</span>
          <span>🚀 SHIFT + Mouse↑↓ - Subir/Bajar Nave</span>
        </div>
      )}
    </>
  )
}

/**
 * ControlButton - Botón reutilizable
 */
function ControlButton({
  label,
  onClick,
  color
}: {
  label: string
  onClick?: () => void
  color: string
}) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: '12px 24px',
        background: color,
        border: '1px solid rgba(255,255,255,0.3)',
        borderRadius: '8px',
        color: 'white',
        fontSize: '14px',
        fontWeight: 'bold',
        cursor: 'pointer',
        transition: 'all 0.2s',
        boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
        display: 'flex',
        alignItems: 'center',
        gap: '8px'
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.opacity = '1'
        e.currentTarget.style.transform = 'scale(1.05)'
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.opacity = '0.9'
        e.currentTarget.style.transform = 'scale(1)'
      }}
    >
      {label}
    </button>
  )
}

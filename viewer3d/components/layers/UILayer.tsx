/**
 * UILayer - Capa de interfaz de usuario
 * Responsabilidad: Gestionar todos los controles y paneles UI
 */

'use client'

import { Suspense, lazy } from 'react'
import type { WeatherState } from '../WeatherControl'

const WeatherControl = lazy(() => import('../WeatherControl'))
const LocationInfo = lazy(() => import('../LocationInfo'))

interface UILayerProps {
  mode: 'globe' | 'model'
  location: { lat: number; lon: number } | null
  showLocationInfo: boolean
  onWeatherChange: (weather: WeatherState) => void
  onReturnToGlobe?: () => void
}

export default function UILayer({ 
  mode,
  location,
  showLocationInfo,
  onWeatherChange,
  onReturnToGlobe
}: UILayerProps) {
  return (
    <div className="ui-layer">
      {/* Control de clima (solo en modo modelo) */}
      {mode === 'model' && (
        <Suspense fallback={null}>
          <WeatherControl onWeatherChange={onWeatherChange} />
        </Suspense>
      )}
      
      {/* Información de ubicación */}
      {showLocationInfo && location && (
        <Suspense fallback={null}>
          <LocationInfo location={location} />
        </Suspense>
      )}
      
      {/* Botón para volver al globo */}
      {mode === 'model' && onReturnToGlobe && (
        <button
          onClick={onReturnToGlobe}
          style={{
            position: 'fixed',
            top: '20px',
            left: '20px',
            zIndex: 1000,
            padding: '10px 16px',
            background: 'rgba(66, 153, 225, 0.85)',
            border: '1px solid rgba(255,255,255,0.3)',
            borderRadius: '8px',
            color: 'white',
            fontSize: '13px',
            fontWeight: '600',
            cursor: 'pointer',
            backdropFilter: 'blur(10px)',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            transition: 'all 0.2s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = 'rgba(66, 153, 225, 0.95)'
            e.currentTarget.style.transform = 'translateY(-2px)'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'rgba(66, 153, 225, 0.85)'
            e.currentTarget.style.transform = 'translateY(0)'
          }}
        >
          🌍 Volver al Globo
        </button>
      )}
    </div>
  )
}

'use client'

/**
 * OptionalSystems - Clima, Audio, Sistemas Opcionales
 * 
 * Responsabilidades:
 * - Sistema de clima (lluvia, nieve, viento)
 * - Audio ambiental
 * - Efectos atmosféricos
 * 
 * LAZY + CONDICIONAL: Solo se carga si está habilitado
 */

import { Suspense } from 'react'
import dynamic from 'next/dynamic'

// Lazy load de WeatherSystem
const WeatherSystem = dynamic(() => import('@/utils/lazy-systems').then(m => ({ default: m.WeatherSystem })), { ssr: false })

interface OptionalSystemsProps {
  weatherEnabled?: boolean
  weatherType?: 'clear' | 'rain' | 'storm' | 'snow'
  windEnabled?: boolean
  windSpeed?: number
  audioEnabled?: boolean
  weather?: any
  isIceBiome?: boolean
}

export default function OptionalSystems({
  weatherEnabled = false,
  weatherType = 'clear',
  windEnabled = false,
  windSpeed = 1.0,
  audioEnabled = false,
  weather,
  isIceBiome = false
}: OptionalSystemsProps) {
  if (!weatherEnabled && !windEnabled && !audioEnabled && !weather) {
    return null
  }

  return (
    <Suspense fallback={null}>
      <group name="optional-systems">
        {/* Sistema de clima completo */}
        {weather && (
          <WeatherSystem weather={weather} isIceBiome={isIceBiome} />
        )}
      </group>
    </Suspense>
  )
}

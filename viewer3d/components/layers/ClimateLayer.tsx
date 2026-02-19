/**
 * ClimateLayer - Capa de clima (efectos atmosféricos)
 * Responsabilidad: Gestionar todos los efectos climáticos
 */

'use client'

import { Suspense, lazy } from 'react'
import type { WeatherState } from '../WeatherControl'

// Lazy load del sistema climático
const WeatherSystem = lazy(() => import('../systems/WeatherSystem'))

interface ClimateLayerProps {
  weather: WeatherState
  isIceBiome: boolean
  enabled: boolean
}

export default function ClimateLayer({ 
  weather, 
  isIceBiome,
  enabled 
}: ClimateLayerProps) {
  if (!enabled) return null
  
  // Verificar si hay algún efecto climático activo
  const hasActiveWeather = Object.values(weather).some(value => value === true)
  
  if (!hasActiveWeather && !isIceBiome) return null
  
  return (
    <group name="climate-layer">
      <Suspense fallback={null}>
        <WeatherSystem weather={weather} isIceBiome={isIceBiome} />
      </Suspense>
    </group>
  )
}

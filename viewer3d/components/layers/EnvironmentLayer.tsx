/**
 * EnvironmentLayer - Capa de entorno (cielo, agua, iluminación)
 * Responsabilidad: Gestionar elementos ambientales visuales
 */

'use client'

import { Suspense, lazy } from 'react'
import { useBiomeSystem } from '@/hooks/useBiomeSystem'
import { useWeatherIntegration } from '@/hooks/useWeatherIntegration'
import type { WeatherState } from '../WeatherControl'

const EnvironmentSystem = lazy(() => import('../systems/EnvironmentSystem'))

interface EnvironmentLayerProps {
  location: { lat: number; lon: number } | null
  isDay: boolean
  weather: WeatherState
  enabled: boolean
}

export default function EnvironmentLayer({ 
  location, 
  isDay,
  weather,
  enabled 
}: EnvironmentLayerProps) {
  const { skyColor, fogColor, isIceBiome } = useBiomeSystem(location, isDay)
  const { stormDarkness } = useWeatherIntegration(weather)
  
  if (!enabled) return null
  
  return (
    <group name="environment-layer">
      <Suspense fallback={null}>
        <EnvironmentSystem
          isDay={isDay}
          skyColor={skyColor}
          fogColor={fogColor}
          stormDarkness={stormDarkness}
          fogDensity={isIceBiome ? 0.012 : 0.008}
          showWater={!isIceBiome}
          waterPosition={[0, -0.5, 0]}
          waterSize={150}
          waterColor="#1e3a5f"
        />
      </Suspense>
    </group>
  )
}

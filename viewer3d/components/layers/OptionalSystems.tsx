'use client'

/**
 * OptionalSystems - Sistemas opcionales y condicionales
 * 
 * Responsabilidades:
 * - Weather System (clima dinámico)
 * - Audio System
 * - Climate Effects
 * 
 * **LAZY + CONDICIONAL**: Nunca cargar si no están activos
 * Se montan solo cuando:
 * - Usuario activa clima en UI
 * - Audio está habilitado en settings
 */

import { Suspense, lazy, useMemo } from 'react'
import type { WeatherState } from '../WeatherControl'

const WeatherSystem = lazy(() => import('../WeatherControl').then(m => ({ default: m.WeatherSystem })))

interface OptionalSystemsProps {
  enableWeather?: boolean
  enableAudio?: boolean
  enableClimate?: boolean
  weatherState?: WeatherState
  isIceBiome?: boolean
  onWeatherChange?: (weather: WeatherState) => void
}

export default function OptionalSystems({
  enableWeather = false,
  enableAudio = false,
  enableClimate = false,
  weatherState = {},
  isIceBiome = false,
  onWeatherChange
}: OptionalSystemsProps) {
  return (
    <group name="optional-systems">
      {/* Weather System - Solo cargar si está activo */}
      {enableWeather && weatherState && (
        <Suspense fallback={null}>
          <WeatherSystemWrapper
            weather={weatherState}
            isIceBiome={isIceBiome}
          />
        </Suspense>
      )}

      {/* Audio System - Solo cargar si está habilitado */}
      {enableAudio && (
        <Suspense fallback={null}>
          <AudioSystemWrapper />
        </Suspense>
      )}

      {/* Climate Effects - Solo si está activo */}
      {enableClimate && (
        <Suspense fallback={null}>
          <ClimateEffectsWrapper />
        </Suspense>
      )}
    </group>
  )
}

/**
 * WeatherSystemWrapper - Envolvente para Weather System
 */
function WeatherSystemWrapper({
  weather,
  isIceBiome
}: {
  weather: WeatherState
  isIceBiome: boolean
}) {
  // Implementación del sistema de clima
  // Muy ligera, solo aplica efectos visuales
  return (
    <group name="weather-system">
      {/* Lluvia, nieve, viento - efectos visuales */}
      {weather.rainHeavy && <div>/rain heavy/</div>}
      {weather.snow && <div>/snow/</div>}
      {weather.lightning && <div>/lightning/</div>}
    </group>
  )
}

/**
 * AudioSystemWrapper - Para futuro sistema de audio
 */
function AudioSystemWrapper() {
  return null
}

/**
 * ClimateEffectsWrapper - Para efectos de clima
 */
function ClimateEffectsWrapper() {
  return null
}

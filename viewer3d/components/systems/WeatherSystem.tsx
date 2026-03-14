'use client'

/**
 * WeatherSystem - Sistema climático modular
 * Se carga solo cuando hay efectos climáticos activos
 */

import { useEffect } from 'react'
import SnowParticles from '../SnowParticles'
import RainParticles from '../RainParticles'
import { LightWind } from '../weather/RealisticWind'
import ProceduralLightning from '../weather/ProceduralLightning'
import { LightFog } from '../weather/RealisticFog'
import { LightClouds } from '../weather/CloudSky'
import TornadoEffect from '../weather/TornadoEffect'
import EarthquakeEffect from '../weather/EarthquakeEffect'
import VisibleSun from '../weather/VisibleSun'
import WeatherManager from '../weather/WeatherManager'
import type { WeatherState } from '../WeatherControl'
import { getClimateAudio } from '@/systems/ClimateAudioSystem'
import { loggers } from '@/core/Logger'

interface WeatherSystemProps {
  weather: WeatherState
  isIceBiome: boolean
  solarDirection?: { x: number; y: number; z: number }
}

export default function WeatherSystem({ weather, isIceBiome, solarDirection = { x: 0, y: 1, z: 0 } }: WeatherSystemProps) {
  // Determinar estado del clima
  const weatherState = weather.storm 
    ? 'storm' 
    : weather.rainHeavy || weather.rainModerate || weather.rainLight 
      ? 'rain' 
      : weather.snow 
        ? 'snow' 
        : 'clear'

  const intensity = weather.rainHeavy ? 1 : weather.rainModerate ? 0.6 : weather.rainLight ? 0.3 : 0.5
  
  // Determinar bioma para el viento
  const biome = isIceBiome ? 'ice' : 'default'
  
  // Log para debug
  loggers.weather.debug('WeatherSystem state:', { 
    wind: weather.wind, 
    biome,
    weatherState 
  })
  
  // Integrar audio procedural
  useEffect(() => {
    const climateAudio = getClimateAudio()
    climateAudio.initialize()
    
    // Actualizar audio según clima
    const rainIntensity = weather.rainHeavy ? 0.9 : weather.rainModerate ? 0.6 : weather.rainLight ? 0.3 : 0
    const windIntensity = weather.wind ? 0.7 : 0
    const tornadoIntensity = weather.tornado ? 0.8 : 0
    
    climateAudio.updateWeather({
      rain: rainIntensity,
      wind: windIntensity,
      tornado: tornadoIntensity,
      snow: weather.snow ? 0.5 : 0,
      thunder: weather.storm || weather.lightning
    })
    
    // NO necesitamos truenos manuales aquí
    // El LightningSystem los maneja automáticamente
  }, [weather])

  return (
    <WeatherManager
      config={{
        state: weatherState,
        intensity,
        windStrength: weather.wind ? 0.7 : 0,
        fogDensity: weather.fog ? 0.8 : 0,
        lightningFrequency: weather.storm ? 12 : 0,
        transitionSpeed: 0.5
      }}
    >
      {/* Precipitación */}
      {weather.snow && <SnowParticles />}
      {weather.rainLight && <RainParticles intensity="light" />}
      {weather.rainModerate && <RainParticles intensity="moderate" />}
      {weather.rainHeavy && <RainParticles intensity="heavy" />}
      
      {/* Viento realista (nueva implementación) */}
      {weather.wind && (
        <LightWind strength={0.7} biome={biome} />
      )}
      
      {/* Niebla realista */}
      {weather.fog && (
        <LightFog density={0.8} color="#b0b0b0" />
      )}
      
      {/* Nubes atmosféricas */}
      {weather.clouds && (
        <LightClouds 
          opacity={0.9} 
          stormMode={weather.storm || weather.lightning}
        />
      )}
      
      {/* Fenómenos extremos */}
      {(weather.storm || weather.lightning) && (
        <ProceduralLightning
          enabled={true}
          intensity={weather.storm ? 1.0 : 0.7}
          showBolt={true}
          minDistance={200}
          maxDistance={weather.storm ? 2000 : 3000}
          minInterval={weather.storm ? 1500 : 2500}
          maxInterval={weather.storm ? 4000 : 6000}
        />
      )}
      {weather.tornado && <TornadoEffect position={[20, 0, 20]} intensity={0.8} height={40} />}
      {weather.earthquake && <EarthquakeEffect />}
      
      {/* Sol visible en el cielo */}
      {weather.visibleSun && (
        <VisibleSun 
          solarDirection={solarDirection}
          intensity={3.0}
          distance={500}
        />
      )}
      
      {/* Nieve automática solo en biomas helados si no hay clima manual activo */}
      {!weather.snow && !weather.rainLight && !weather.rainModerate && !weather.rainHeavy && isIceBiome && (
        <SnowParticles />
      )}
    </WeatherManager>
  )
}

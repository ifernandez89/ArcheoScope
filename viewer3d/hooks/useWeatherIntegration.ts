/**
 * useWeatherIntegration - Hook para integración de clima con EventBus
 * Emite eventos cuando cambia el estado del clima
 */

import { useEffect } from 'react'
import eventBus, { EVENTS } from '@/core/EventBus'

export interface WeatherState {
  snow: boolean
  rainLight: boolean
  rainModerate: boolean
  rainHeavy: boolean
  wind: boolean
  fog: boolean
  storm: boolean
  lightning: boolean
  tornado: boolean
  clouds: boolean
}

export function useWeatherIntegration(weather: WeatherState) {
  // Emitir eventos cuando cambia el clima
  useEffect(() => {
    // Storm
    if (weather.storm) {
      eventBus.emit(EVENTS.WEATHER.STORM_START, { intensity: 1.0 })
    } else {
      eventBus.emit(EVENTS.WEATHER.STORM_END)
    }
  }, [weather.storm])
  
  useEffect(() => {
    // Rain
    const rainIntensity = weather.rainHeavy ? 0.9 : weather.rainModerate ? 0.6 : weather.rainLight ? 0.3 : 0
    
    if (rainIntensity > 0) {
      eventBus.emit(EVENTS.WEATHER.RAIN_START, { intensity: rainIntensity })
    } else {
      eventBus.emit(EVENTS.WEATHER.RAIN_END)
    }
  }, [weather.rainLight, weather.rainModerate, weather.rainHeavy])
  
  useEffect(() => {
    // Wind
    if (weather.wind) {
      eventBus.emit(EVENTS.WEATHER.WIND_START, { intensity: 0.7 })
    } else {
      eventBus.emit(EVENTS.WEATHER.WIND_END)
    }
  }, [weather.wind])
  
  useEffect(() => {
    // Fog
    if (weather.fog) {
      eventBus.emit(EVENTS.WEATHER.FOG_START, { density: 0.8 })
    } else {
      eventBus.emit(EVENTS.WEATHER.FOG_END)
    }
  }, [weather.fog])
  
  useEffect(() => {
    // Tornado
    if (weather.tornado) {
      eventBus.emit(EVENTS.WEATHER.TORNADO_START, { intensity: 0.8 })
    } else {
      eventBus.emit(EVENTS.WEATHER.TORNADO_END)
    }
  }, [weather.tornado])
  
  useEffect(() => {
    // Clouds
    eventBus.emit(EVENTS.WEATHER.CLOUDS_CHANGE, { 
      enabled: weather.clouds,
      stormMode: weather.storm || weather.lightning
    })
  }, [weather.clouds, weather.storm, weather.lightning])
  
  // Calcular oscurecimiento del cielo
  const stormDarkness = weather.storm || weather.tornado ? 0.7 : 
                        weather.rainHeavy || weather.lightning ? 0.5 : 
                        0
  
  return {
    stormDarkness
  }
}

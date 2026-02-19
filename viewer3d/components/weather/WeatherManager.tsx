'use client'

import { useRef, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'

export type WeatherState = 'clear' | 'rain' | 'storm' | 'snow' | 'fog' | 'wind'

interface WeatherConfig {
  state: WeatherState
  intensity: number // 0-1
  windStrength: number
  fogDensity: number
  lightningFrequency: number // rayos por minuto
  transitionSpeed: number
}

interface WeatherManagerProps {
  config: WeatherConfig
  onStateChange?: (state: WeatherState) => void
  children?: React.ReactNode
}

export default function WeatherManager({ config, onStateChange, children }: WeatherManagerProps) {
  const timeRef = useRef(0)
  const lastLightningRef = useRef(0)
  const transitionRef = useRef(0)
  
  useFrame((state, delta) => {
    timeRef.current += delta
    
    // Actualizar transición
    if (transitionRef.current < 1) {
      transitionRef.current = Math.min(1, transitionRef.current + delta * config.transitionSpeed)
    }
    
    // Sistema de rayos (para tormentas)
    if (config.state === 'storm' && config.lightningFrequency > 0) {
      const timeSinceLastLightning = timeRef.current - lastLightningRef.current
      const averageInterval = 60 / config.lightningFrequency // segundos entre rayos
      
      // Probabilidad de rayo basada en tiempo transcurrido
      if (timeSinceLastLightning > averageInterval * 0.5) {
        const probability = Math.min(1, timeSinceLastLightning / averageInterval)
        if (Math.random() < probability * delta * 2) {
          lastLightningRef.current = timeRef.current
          // Trigger lightning event
          if (typeof window !== 'undefined') {
            window.dispatchEvent(new CustomEvent('weather:lightning', { 
              detail: { intensity: config.intensity } 
            }))
          }
        }
      }
    }
  })
  
  // Notificar cambios de estado
  useEffect(() => {
    transitionRef.current = 0
    if (onStateChange) {
      onStateChange(config.state)
    }
  }, [config.state, onStateChange])
  
  return <>{children}</>
}

// Hook para acceder al tiempo del weather manager
export function useWeatherTime() {
  const timeRef = useRef(0)
  
  useFrame((state, delta) => {
    timeRef.current += delta
  })
  
  return timeRef.current
}

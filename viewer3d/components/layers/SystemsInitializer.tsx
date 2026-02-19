/**
 * SystemsInitializer - Inicializa y registra sistemas en EngineLoop
 * Responsabilidad: Configurar el motor y sus sistemas
 */

'use client'

import { useEffect } from 'react'
import engineLoop, { type System } from '@/core/EngineLoop'
import eventBus, { EVENTS } from '@/core/EventBus'

interface SystemsInitializerProps {
  enabled: boolean
}

export default function SystemsInitializer({ enabled }: SystemsInitializerProps) {
  useEffect(() => {
    if (!enabled) return
    
    // Iniciar el motor
    engineLoop.start()
    
    if (process.env.NODE_ENV === 'development') {
      console.log('🎮 EngineLoop iniciado')
      
      // Log de métricas cada 5 segundos
      const metricsInterval = setInterval(() => {
        const metrics = engineLoop.getMetrics()
        console.log('📊 Métricas:', metrics)
      }, 5000)
      
      return () => {
        clearInterval(metricsInterval)
        engineLoop.stop()
      }
    }
    
    return () => {
      engineLoop.stop()
    }
  }, [enabled])
  
  // Registrar sistemas básicos
  useEffect(() => {
    if (!enabled) return
    
    // Sistema de tiempo (ejemplo)
    const timeSystem: System = {
      name: 'TimeSystem',
      priority: 0,
      enabled: true,
      
      update(delta: number, time: number) {
        // Emitir evento de tiempo cada segundo
        if (Math.floor(time) !== Math.floor(time - delta)) {
          eventBus.emit(EVENTS.WORLD.TIME_CHANGE, { time })
        }
      }
    }
    
    engineLoop.registerSystem(timeSystem)
    
    return () => {
      engineLoop.unregisterSystem('TimeSystem')
    }
  }, [enabled])
  
  return null
}

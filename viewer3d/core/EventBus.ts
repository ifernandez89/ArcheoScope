/**
 * EventBus - Sistema de eventos desacoplado para el motor
 * 
 * Permite comunicación entre sistemas sin dependencias directas.
 * Inspirado en arquitecturas ECS y motores de juegos.
 */

import { loggers } from './Logger'

type EventCallback = (data?: any) => void

interface EventSubscription {
  id: string
  callback: EventCallback
}

class EventBus {
  private events: Map<string, EventSubscription[]> = new Map()
  private eventHistory: Array<{ event: string; data: any; timestamp: number }> = []
  private maxHistorySize = 100
  
  /**
   * Suscribirse a un evento
   */
  on(event: string, callback: EventCallback): () => void {
    const subscription: EventSubscription = {
      id: `${event}_${Date.now()}_${Math.random()}`,
      callback
    }
    
    if (!this.events.has(event)) {
      this.events.set(event, [])
    }
    
    this.events.get(event)!.push(subscription)
    
    // Retornar función de cleanup
    return () => this.off(event, subscription.id)
  }
  
  /**
   * Suscribirse a un evento una sola vez
   */
  once(event: string, callback: EventCallback): () => void {
    const wrappedCallback = (data?: any) => {
      callback(data)
      this.off(event, subscription.id)
    }
    
    const subscription: EventSubscription = {
      id: `${event}_once_${Date.now()}_${Math.random()}`,
      callback: wrappedCallback
    }
    
    if (!this.events.has(event)) {
      this.events.set(event, [])
    }
    
    this.events.get(event)!.push(subscription)
    
    return () => this.off(event, subscription.id)
  }
  
  /**
   * Desuscribirse de un evento
   */
  off(event: string, subscriptionId: string): void {
    const subscriptions = this.events.get(event)
    if (!subscriptions) return
    
    const index = subscriptions.findIndex(sub => sub.id === subscriptionId)
    if (index !== -1) {
      subscriptions.splice(index, 1)
    }
    
    // Limpiar si no hay más suscripciones
    if (subscriptions.length === 0) {
      this.events.delete(event)
    }
  }
  
  /**
   * Emitir un evento
   */
  emit(event: string, data?: any): void {
    const subscriptions = this.events.get(event)
    
    // Guardar en historial
    this.eventHistory.push({
      event,
      data,
      timestamp: Date.now()
    })
    
    // Limitar tamaño del historial
    if (this.eventHistory.length > this.maxHistorySize) {
      this.eventHistory.shift()
    }
    
    // Ejecutar callbacks
    if (subscriptions) {
      subscriptions.forEach(sub => {
        try {
          sub.callback(data)
        } catch (error) {
          loggers.engine.error(`Error en evento "${event}":`, error)
        }
      })
    }
  }
  
  /**
   * Limpiar todas las suscripciones
   */
  clear(): void {
    this.events.clear()
    this.eventHistory = []
  }
  
  /**
   * Obtener historial de eventos (debug)
   */
  getHistory(): Array<{ event: string; data: any; timestamp: number }> {
    return [...this.eventHistory]
  }
  
  /**
   * Obtener eventos activos (debug)
   */
  getActiveEvents(): string[] {
    return Array.from(this.events.keys())
  }
  
  /**
   * Obtener número de suscriptores por evento (debug)
   */
  getSubscriberCount(event: string): number {
    return this.events.get(event)?.length || 0
  }
}

// Instancia global singleton
const eventBus = new EventBus()

export default eventBus

/**
 * EVENTOS DEL SISTEMA
 * Documentación de todos los eventos disponibles
 */

export const EVENTS = {
  // Sistema Climático
  WEATHER: {
    STORM_START: 'weather:storm:start',
    STORM_END: 'weather:storm:end',
    RAIN_START: 'weather:rain:start',
    RAIN_END: 'weather:rain:end',
    WIND_START: 'weather:wind:start',
    WIND_END: 'weather:wind:end',
    LIGHTNING_STRIKE: 'weather:lightning:strike',
    TORNADO_START: 'weather:tornado:start',
    TORNADO_END: 'weather:tornado:end',
    FOG_START: 'weather:fog:start',
    FOG_END: 'weather:fog:end',
    CLOUDS_CHANGE: 'weather:clouds:change'
  },
  
  // Sistema de Mundo
  WORLD: {
    BIOME_CHANGE: 'world:biome:change',
    TIME_CHANGE: 'world:time:change',
    DAY_START: 'world:day:start',
    NIGHT_START: 'world:night:start',
    TELEPORT: 'world:teleport',
    LOCATION_CHANGE: 'world:location:change'
  },
  
  // Sistema de Avatar
  AVATAR: {
    SPAWN: 'avatar:spawn',
    MOVE: 'avatar:move',
    JUMP: 'avatar:jump',
    LAND: 'avatar:land',
    INTERACT: 'avatar:interact',
    PROXIMITY: 'avatar:proximity'
  },
  
  // Sistema de Cámara
  CAMERA: {
    SHAKE: 'camera:shake',
    ZOOM: 'camera:zoom',
    FOCUS: 'camera:focus',
    MODE_CHANGE: 'camera:mode:change'
  },
  
  // Sistema de Audio
  AUDIO: {
    PLAY: 'audio:play',
    STOP: 'audio:stop',
    VOLUME_CHANGE: 'audio:volume:change',
    MUTE: 'audio:mute'
  },
  
  // Sistema de UI
  UI: {
    PANEL_OPEN: 'ui:panel:open',
    PANEL_CLOSE: 'ui:panel:close',
    NOTIFICATION: 'ui:notification',
    LOADING_START: 'ui:loading:start',
    LOADING_END: 'ui:loading:end'
  },
  
  // Sistema de Performance
  PERFORMANCE: {
    FPS_DROP: 'performance:fps:drop',
    MEMORY_WARNING: 'performance:memory:warning',
    QUALITY_CHANGE: 'performance:quality:change'
  },
  
  // Sistema de Motor
  ENGINE: {
    INIT: 'engine:init',
    UPDATE: 'engine:update',
    RENDER: 'engine:render',
    PAUSE: 'engine:pause',
    RESUME: 'engine:resume',
    SYSTEM_REGISTER: 'engine:system:register',
    SYSTEM_UNREGISTER: 'engine:system:unregister'
  }
} as const

/**
 * Hook de React para usar EventBus
 */
export function useEventBus() {
  return {
    on: eventBus.on.bind(eventBus),
    once: eventBus.once.bind(eventBus),
    off: eventBus.off.bind(eventBus),
    emit: eventBus.emit.bind(eventBus),
    EVENTS
  }
}

/**
 * Tipos para eventos tipados
 */
export type WeatherEventData = {
  intensity?: number
  duration?: number
  position?: { x: number; y: number; z: number }
}

export type WorldEventData = {
  biome?: string
  location?: { lat: number; lon: number }
  time?: number
}

export type AvatarEventData = {
  position?: { x: number; y: number; z: number }
  velocity?: { x: number; y: number; z: number }
  target?: any
}

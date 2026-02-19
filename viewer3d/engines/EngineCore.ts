/**
 * EngineCore - Loop central del motor
 * Separa lógica del mundo de rendering React
 * 
 * CRÍTICO: Reduce re-renders innecesarios
 */

import { WorldCore } from './WorldCore'
import PerformanceMonitor from '@/utils/performance-monitor'

export interface EngineSystem {
  update(delta: number): void
  enabled: boolean
}

export class EngineCore {
  private static instance: EngineCore
  
  private systems: Map<string, EngineSystem> = new Map()
  private isRunning: boolean = false
  private lastTime: number = 0
  private accumulatedTime: number = 0
  private fixedTimeStep: number = 1 / 60 // 60 FPS
  
  // Callbacks que NO disparan re-renders
  private updateCallbacks: Set<(delta: number) => void> = new Set()
  private renderCallbacks: Set<() => void> = new Set()
  
  // Renderer reference (para métricas)
  private renderer: any = null
  
  private constructor() {
    console.log('🎮 EngineCore: Inicializado')
  }
  
  static getInstance(): EngineCore {
    if (!EngineCore.instance) {
      EngineCore.instance = new EngineCore()
    }
    return EngineCore.instance
  }
  
  /**
   * Registrar sistema
   */
  registerSystem(name: string, system: EngineSystem): void {
    this.systems.set(name, system)
    console.log(`🔧 EngineCore: Sistema registrado - ${name}`)
  }
  
  /**
   * Desregistrar sistema
   */
  unregisterSystem(name: string): void {
    this.systems.delete(name)
    console.log(`🔧 EngineCore: Sistema removido - ${name}`)
  }
  
  /**
   * Registrar callback de update (NO dispara re-renders)
   */
  onUpdate(callback: (delta: number) => void): () => void {
    this.updateCallbacks.add(callback)
    
    return () => {
      this.updateCallbacks.delete(callback)
    }
  }
  
  /**
   * Registrar callback de render (NO dispara re-renders)
   */
  onRender(callback: () => void): () => void {
    this.renderCallbacks.add(callback)
    
    return () => {
      this.renderCallbacks.delete(callback)
    }
  }
  
  /**
   * Establecer renderer (para métricas)
   */
  setRenderer(renderer: any): void {
    this.renderer = renderer
  }
  
  /**
   * Tick principal - Llamado desde useFrame
   */
  tick(time: number, delta: number): void {
    if (!this.isRunning) return
    
    // Verificar si está pausado
    if (WorldCore.State.getPaused()) return
    
    // Aplicar time scale
    const timeScale = WorldCore.State.getTimeScale()
    const scaledDelta = delta * timeScale
    
    // Fixed timestep para física
    this.accumulatedTime += scaledDelta
    
    while (this.accumulatedTime >= this.fixedTimeStep) {
      this.update(this.fixedTimeStep)
      this.accumulatedTime -= this.fixedTimeStep
    }
    
    // Render (siempre)
    this.render()
    
    // Actualizar métricas
    this.updateMetrics()
  }
  
  /**
   * Update - Lógica del mundo
   */
  private update(delta: number): void {
    // Actualizar WorldCore
    WorldCore.Time.update(delta, WorldCore.State.getTimeScale())
    
    // Actualizar sistemas registrados
    this.systems.forEach((system, name) => {
      if (system.enabled) {
        try {
          system.update(delta)
        } catch (error) {
          console.error(`Error en sistema ${name}:`, error)
        }
      }
    })
    
    // Ejecutar callbacks de update
    this.updateCallbacks.forEach(callback => {
      try {
        callback(delta)
      } catch (error) {
        console.error('Error en update callback:', error)
      }
    })
  }
  
  /**
   * Render - Preparación para renderizado
   */
  private render(): void {
    // Ejecutar callbacks de render
    this.renderCallbacks.forEach(callback => {
      try {
        callback()
      } catch (error) {
        console.error('Error en render callback:', error)
      }
    })
  }
  
  /**
   * Actualizar métricas de performance
   */
  private updateMetrics(): void {
    if (this.renderer) {
      PerformanceMonitor.updateThreeMetrics(this.renderer)
    }
    
    PerformanceMonitor.updateMemoryMetrics()
  }
  
  /**
   * Iniciar motor
   */
  start(): void {
    if (this.isRunning) return
    
    this.isRunning = true
    this.lastTime = performance.now()
    console.log('▶️ EngineCore: Motor iniciado')
  }
  
  /**
   * Detener motor
   */
  stop(): void {
    if (!this.isRunning) return
    
    this.isRunning = false
    console.log('⏸️ EngineCore: Motor detenido')
  }
  
  /**
   * Pausar/Resumir
   */
  pause(): void {
    WorldCore.State.pause()
  }
  
  resume(): void {
    WorldCore.State.resume()
  }
  
  /**
   * Obtener estado
   */
  getState(): {
    isRunning: boolean
    isPaused: boolean
    timeScale: number
    systemCount: number
    updateCallbackCount: number
    renderCallbackCount: number
  } {
    return {
      isRunning: this.isRunning,
      isPaused: WorldCore.State.getPaused(),
      timeScale: WorldCore.State.getTimeScale(),
      systemCount: this.systems.size,
      updateCallbackCount: this.updateCallbacks.size,
      renderCallbackCount: this.renderCallbacks.size
    }
  }
  
  /**
   * Limpiar
   */
  dispose(): void {
    this.stop()
    this.systems.clear()
    this.updateCallbacks.clear()
    this.renderCallbacks.clear()
    console.log('🧹 EngineCore: Limpiado')
  }
}

export default EngineCore.getInstance()

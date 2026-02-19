/**
 * EngineLoop - Core del motor con update/render loop
 * 
 * Separa la lógica del motor de React.
 * React solo monta el canvas, el motor maneja el loop.
 */

import eventBus, { EVENTS } from './EventBus'
import { loggers } from './Logger'

export interface System {
  name: string
  priority: number // Orden de ejecución (menor = primero)
  enabled: boolean
  update(delta: number, time: number): void
  dispose?(): void
}

class EngineLoop {
  private systems: System[] = []
  private running = false
  private lastTime = 0
  private deltaTime = 0
  private elapsedTime = 0
  private frameCount = 0
  private fps = 60
  private fpsUpdateInterval = 1000 // 1 segundo
  private lastFpsUpdate = 0
  private animationFrameId: number | null = null
  
  // Configuración
  private targetFPS = 60
  private maxDeltaTime = 0.1 // Limitar delta para evitar saltos
  
  constructor() {
    eventBus.emit(EVENTS.ENGINE.INIT)
  }
  
  /**
   * Registrar un sistema
   */
  registerSystem(system: System): void {
    // Verificar que no exista ya
    const exists = this.systems.find(s => s.name === system.name)
    if (exists) {
      loggers.engine.warn(`Sistema "${system.name}" ya está registrado`)
      return
    }
    
    this.systems.push(system)
    
    // Ordenar por prioridad
    this.systems.sort((a, b) => a.priority - b.priority)
    
    eventBus.emit(EVENTS.ENGINE.SYSTEM_REGISTER, { system: system.name })
    
    loggers.engine.debug(`Sistema registrado: ${system.name} (prioridad: ${system.priority})`)
  }
  
  /**
   * Desregistrar un sistema
   */
  unregisterSystem(systemName: string): void {
    const index = this.systems.findIndex(s => s.name === systemName)
    if (index === -1) return
    
    const system = this.systems[index]
    
    // Llamar dispose si existe
    if (system.dispose) {
      system.dispose()
    }
    
    this.systems.splice(index, 1)
    
    eventBus.emit(EVENTS.ENGINE.SYSTEM_UNREGISTER, { system: systemName })
    
    loggers.engine.debug(`Sistema desregistrado: ${systemName}`)
  }
  
  /**
   * Obtener un sistema por nombre
   */
  getSystem<T extends System>(systemName: string): T | undefined {
    return this.systems.find(s => s.name === systemName) as T | undefined
  }
  
  /**
   * Habilitar/deshabilitar un sistema
   */
  setSystemEnabled(systemName: string, enabled: boolean): void {
    const system = this.systems.find(s => s.name === systemName)
    if (system) {
      system.enabled = enabled
    }
  }
  
  /**
   * Iniciar el loop
   */
  start(): void {
    if (this.running) return
    
    this.running = true
    this.lastTime = performance.now()
    this.lastFpsUpdate = this.lastTime
    
    this.loop()
    
    loggers.engine.info('EngineLoop iniciado')
  }
  
  /**
   * Detener el loop
   */
  stop(): void {
    if (!this.running) return
    
    this.running = false
    
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId)
      this.animationFrameId = null
    }
    
    loggers.engine.info('EngineLoop detenido')
  }
  
  /**
   * Pausar el loop
   */
  pause(): void {
    this.running = false
    eventBus.emit(EVENTS.ENGINE.PAUSE)
  }
  
  /**
   * Reanudar el loop
   */
  resume(): void {
    if (this.running) return
    
    this.running = true
    this.lastTime = performance.now()
    this.loop()
    
    eventBus.emit(EVENTS.ENGINE.RESUME)
  }
  
  /**
   * Loop principal
   */
  private loop = (): void => {
    if (!this.running) return
    
    const currentTime = performance.now()
    this.deltaTime = Math.min((currentTime - this.lastTime) / 1000, this.maxDeltaTime)
    this.lastTime = currentTime
    this.elapsedTime += this.deltaTime
    this.frameCount++
    
    // Actualizar FPS
    if (currentTime - this.lastFpsUpdate >= this.fpsUpdateInterval) {
      this.fps = Math.round((this.frameCount * 1000) / (currentTime - this.lastFpsUpdate))
      this.frameCount = 0
      this.lastFpsUpdate = currentTime
      
      // Emitir warning si FPS bajo
      if (this.fps < 30) {
        eventBus.emit(EVENTS.PERFORMANCE.FPS_DROP, { fps: this.fps })
      }
    }
    
    // Update phase
    this.update(this.deltaTime, this.elapsedTime)
    
    // Render phase (emitir evento para que Three.js renderice)
    eventBus.emit(EVENTS.ENGINE.RENDER, { 
      delta: this.deltaTime, 
      time: this.elapsedTime 
    })
    
    // Siguiente frame
    this.animationFrameId = requestAnimationFrame(this.loop)
  }
  
  /**
   * Fase de actualización
   */
  private update(delta: number, time: number): void {
    // Ejecutar sistemas habilitados en orden de prioridad
    for (const system of this.systems) {
      if (system.enabled) {
        try {
          system.update(delta, time)
        } catch (error) {
          loggers.engine.error(`Error en sistema "${system.name}":`, error)
        }
      }
    }
    
    // Emitir evento de update
    eventBus.emit(EVENTS.ENGINE.UPDATE, { delta, time })
  }
  
  /**
   * Obtener métricas
   */
  getMetrics() {
    return {
      fps: this.fps,
      deltaTime: this.deltaTime,
      elapsedTime: this.elapsedTime,
      systemCount: this.systems.length,
      enabledSystems: this.systems.filter(s => s.enabled).length
    }
  }
  
  /**
   * Obtener lista de sistemas
   */
  getSystems(): System[] {
    return [...this.systems]
  }
  
  /**
   * Limpiar todo
   */
  dispose(): void {
    this.stop()
    
    // Dispose de todos los sistemas
    this.systems.forEach(system => {
      if (system.dispose) {
        system.dispose()
      }
    })
    
    this.systems = []
    
    loggers.engine.info('EngineLoop disposed')
  }
}

// Instancia global singleton
const engineLoop = new EngineLoop()

export default engineLoop

/**
 * Hook de React para usar EngineLoop
 */
export function useEngineLoop() {
  return {
    registerSystem: engineLoop.registerSystem.bind(engineLoop),
    unregisterSystem: engineLoop.unregisterSystem.bind(engineLoop),
    getSystem: engineLoop.getSystem.bind(engineLoop),
    setSystemEnabled: engineLoop.setSystemEnabled.bind(engineLoop),
    start: engineLoop.start.bind(engineLoop),
    stop: engineLoop.stop.bind(engineLoop),
    pause: engineLoop.pause.bind(engineLoop),
    resume: engineLoop.resume.bind(engineLoop),
    getMetrics: engineLoop.getMetrics.bind(engineLoop),
    getSystems: engineLoop.getSystems.bind(engineLoop)
  }
}

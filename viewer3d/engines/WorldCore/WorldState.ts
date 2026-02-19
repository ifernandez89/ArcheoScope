/**
 * WorldState - Estado global del mundo
 * Responsable de: Estado centralizado, eventos, sincronización
 */

import { EventEmitter } from 'events'

export interface WorldConfig {
  renderDistance: number
  lodLevels: number
  chunkSize: number
  enableStreaming: boolean
  enablePersistence: boolean
}

export interface WorldMetrics {
  fps: number
  drawCalls: number
  triangles: number
  loadedChunks: number
  activeObjects: number
  memoryUsage: number
}

export class WorldState extends EventEmitter {
  private static instance: WorldState
  
  private config: WorldConfig = {
    renderDistance: 1000,
    lodLevels: 4,
    chunkSize: 50,
    enableStreaming: true,
    enablePersistence: false
  }
  
  private metrics: WorldMetrics = {
    fps: 60,
    drawCalls: 0,
    triangles: 0,
    loadedChunks: 0,
    activeObjects: 0,
    memoryUsage: 0
  }
  
  private isPaused: boolean = false
  private timeScale: number = 1.0
  
  private constructor() {
    super()
    console.log('🌍 WorldState: Inicializado')
  }
  
  static getInstance(): WorldState {
    if (!WorldState.instance) {
      WorldState.instance = new WorldState()
    }
    return WorldState.instance
  }
  
  // Configuration
  getConfig(): WorldConfig {
    return { ...this.config }
  }
  
  updateConfig(partial: Partial<WorldConfig>): void {
    this.config = { ...this.config, ...partial }
    this.emit('config:changed', this.config)
    console.log('⚙️ WorldState: Config actualizada', partial)
  }
  
  // Metrics
  getMetrics(): WorldMetrics {
    return { ...this.metrics }
  }
  
  updateMetrics(partial: Partial<WorldMetrics>): void {
    this.metrics = { ...this.metrics, ...partial }
    this.emit('metrics:updated', this.metrics)
  }
  
  // Pause/Resume
  pause(): void {
    this.isPaused = true
    this.emit('world:paused')
    console.log('⏸️ WorldState: Mundo pausado')
  }
  
  resume(): void {
    this.isPaused = false
    this.emit('world:resumed')
    console.log('▶️ WorldState: Mundo resumido')
  }
  
  getPaused(): boolean {
    return this.isPaused
  }
  
  // Time Scale
  setTimeScale(scale: number): void {
    this.timeScale = Math.max(0, Math.min(10, scale))
    this.emit('timescale:changed', this.timeScale)
    console.log('⏱️ WorldState: TimeScale =', this.timeScale)
  }
  
  getTimeScale(): number {
    return this.timeScale
  }
  
  // Reset
  reset(): void {
    this.isPaused = false
    this.timeScale = 1.0
    this.metrics = {
      fps: 60,
      drawCalls: 0,
      triangles: 0,
      loadedChunks: 0,
      activeObjects: 0,
      memoryUsage: 0
    }
    this.emit('world:reset')
    console.log('🔄 WorldState: Reset completo')
  }
}

export default WorldState.getInstance()

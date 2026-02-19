/**
 * Performance Monitor - Sistema de monitoreo de rendimiento
 * Mide y reporta métricas clave de performance
 */

export interface PerformanceMetrics {
  fps: number
  frameTime: number
  memory: {
    used: number
    total: number
    limit: number
  }
  drawCalls: number
  triangles: number
  geometries: number
  textures: number
  programs: number
  loadTime: number
}

export class PerformanceMonitor {
  private static instance: PerformanceMonitor
  
  private metrics: PerformanceMetrics = {
    fps: 60,
    frameTime: 16.67,
    memory: { used: 0, total: 0, limit: 0 },
    drawCalls: 0,
    triangles: 0,
    geometries: 0,
    textures: 0,
    programs: 0,
    loadTime: 0
  }
  
  private frameCount = 0
  private lastTime = performance.now()
  private fpsHistory: number[] = []
  private maxHistorySize = 60
  
  private listeners: Set<(metrics: PerformanceMetrics) => void> = new Set()
  
  private constructor() {
    this.startMonitoring()
  }
  
  static getInstance(): PerformanceMonitor {
    if (!PerformanceMonitor.instance) {
      PerformanceMonitor.instance = new PerformanceMonitor()
    }
    return PerformanceMonitor.instance
  }
  
  /**
   * Iniciar monitoreo
   */
  private startMonitoring() {
    if (typeof window === 'undefined') return
    
    // Medir tiempo de carga
    window.addEventListener('load', () => {
      const perfData = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming
      if (perfData) {
        this.metrics.loadTime = perfData.loadEventEnd - perfData.fetchStart
      }
    })
    
    // Monitorear FPS
    this.measureFPS()
  }
  
  /**
   * Medir FPS
   */
  private measureFPS() {
    const now = performance.now()
    const delta = now - this.lastTime
    
    this.frameCount++
    
    if (delta >= 1000) {
      const fps = Math.round((this.frameCount * 1000) / delta)
      this.metrics.fps = fps
      this.metrics.frameTime = 1000 / fps
      
      this.fpsHistory.push(fps)
      if (this.fpsHistory.length > this.maxHistorySize) {
        this.fpsHistory.shift()
      }
      
      this.frameCount = 0
      this.lastTime = now
      
      this.notifyListeners()
    }
    
    requestAnimationFrame(() => this.measureFPS())
  }
  
  /**
   * Actualizar métricas de Three.js
   */
  updateThreeMetrics(renderer: any) {
    if (!renderer || !renderer.info) return
    
    this.metrics.drawCalls = renderer.info.render.calls
    this.metrics.triangles = renderer.info.render.triangles
    this.metrics.geometries = renderer.info.memory.geometries
    this.metrics.textures = renderer.info.memory.textures
    this.metrics.programs = renderer.info.programs?.length || 0
    
    this.notifyListeners()
  }
  
  /**
   * Actualizar métricas de memoria
   */
  updateMemoryMetrics() {
    if (typeof window === 'undefined') return
    
    // @ts-ignore - performance.memory es específico de Chrome
    if (performance.memory) {
      // @ts-ignore
      this.metrics.memory = {
        // @ts-ignore
        used: Math.round(performance.memory.usedJSHeapSize / 1048576), // MB
        // @ts-ignore
        total: Math.round(performance.memory.totalJSHeapSize / 1048576),
        // @ts-ignore
        limit: Math.round(performance.memory.jsHeapSizeLimit / 1048576)
      }
      
      this.notifyListeners()
    }
  }
  
  /**
   * Obtener métricas actuales
   */
  getMetrics(): PerformanceMetrics {
    return { ...this.metrics }
  }
  
  /**
   * Obtener FPS promedio
   */
  getAverageFPS(): number {
    if (this.fpsHistory.length === 0) return 60
    
    const sum = this.fpsHistory.reduce((a, b) => a + b, 0)
    return Math.round(sum / this.fpsHistory.length)
  }
  
  /**
   * Obtener FPS mínimo
   */
  getMinFPS(): number {
    if (this.fpsHistory.length === 0) return 60
    return Math.min(...this.fpsHistory)
  }
  
  /**
   * Obtener FPS máximo
   */
  getMaxFPS(): number {
    if (this.fpsHistory.length === 0) return 60
    return Math.max(...this.fpsHistory)
  }
  
  /**
   * Verificar si el rendimiento es bueno
   */
  isPerformanceGood(): boolean {
    return this.metrics.fps >= 50 && this.metrics.memory.used < this.metrics.memory.limit * 0.8
  }
  
  /**
   * Obtener nivel de performance
   */
  getPerformanceLevel(): 'excellent' | 'good' | 'fair' | 'poor' {
    const fps = this.metrics.fps
    
    if (fps >= 55) return 'excellent'
    if (fps >= 45) return 'good'
    if (fps >= 30) return 'fair'
    return 'poor'
  }
  
  /**
   * Suscribirse a cambios de métricas
   */
  subscribe(callback: (metrics: PerformanceMetrics) => void) {
    this.listeners.add(callback)
    
    return () => {
      this.listeners.delete(callback)
    }
  }
  
  /**
   * Notificar a listeners
   */
  private notifyListeners() {
    this.listeners.forEach(callback => callback(this.metrics))
  }
  
  /**
   * Obtener recomendaciones de optimización
   */
  getOptimizationSuggestions(): string[] {
    const suggestions: string[] = []
    
    if (this.metrics.fps < 30) {
      suggestions.push('FPS muy bajo. Considera reducir la calidad gráfica.')
    }
    
    if (this.metrics.drawCalls > 200) {
      suggestions.push('Muchos draw calls. Considera usar instancing o combinar geometrías.')
    }
    
    if (this.metrics.triangles > 1000000) {
      suggestions.push('Muchos triángulos. Implementa LOD o reduce complejidad de modelos.')
    }
    
    if (this.metrics.memory.used > this.metrics.memory.limit * 0.8) {
      suggestions.push('Uso de memoria alto. Libera recursos no utilizados.')
    }
    
    if (this.metrics.textures > 50) {
      suggestions.push('Muchas texturas. Considera usar atlas de texturas.')
    }
    
    if (this.metrics.geometries > 100) {
      suggestions.push('Muchas geometrías. Reutiliza geometrías cuando sea posible.')
    }
    
    return suggestions
  }
  
  /**
   * Exportar métricas como JSON
   */
  exportMetrics(): string {
    return JSON.stringify({
      timestamp: Date.now(),
      metrics: this.metrics,
      stats: {
        avgFPS: this.getAverageFPS(),
        minFPS: this.getMinFPS(),
        maxFPS: this.getMaxFPS(),
        performanceLevel: this.getPerformanceLevel()
      },
      suggestions: this.getOptimizationSuggestions()
    }, null, 2)
  }
  
  /**
   * Reset de métricas
   */
  reset() {
    this.fpsHistory = []
    this.frameCount = 0
    this.lastTime = performance.now()
  }
}

export default PerformanceMonitor.getInstance()

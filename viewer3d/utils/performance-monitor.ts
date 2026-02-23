/**
 * Performance Monitor - Sistema de monitoreo de rendimiento
 * Solo logging en consola, sin UI
 */

import * as THREE from 'three'
import { fileLogger } from './file-logger'

// Función para enviar logs al servidor
async function sendLogToServer(category: string, message: string, data?: any) {
  try {
    const logLine = `[${new Date().toISOString()}] [${category}] ${message}${data ? ' | ' + JSON.stringify(data) : ''}`
    await fetch('/api/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ log: logLine })
    })
  } catch (e) {
    // Silencioso
  }
}

interface PerformanceMetrics {
  fps: number
  frameTime: number
  drawCalls: number
  triangles: number
  geometries: number
  textures: number
  programs: number
  memoryUsed?: number
  timestamp: number
}

interface PerformanceSnapshot {
  location: string
  weather: string
  anomaliesActive: number
  metrics: PerformanceMetrics
  warnings: string[]
}

export class PerformanceMonitor {
  private renderer: THREE.WebGLRenderer | null = null
  private lastTime: number = performance.now()
  private frameCount: number = 0
  private fpsHistory: number[] = []
  private frameTimeHistory: number[] = []
  private logInterval: number = 2000 // Log cada 2 segundos
  private lastLogTime: number = 0
  private snapshots: PerformanceSnapshot[] = []
  
  // Umbrales de alerta
  private readonly THRESHOLDS = {
    FPS_CRITICAL: 25,
    FPS_WARNING: 30,
    FRAME_TIME_CRITICAL: 40, // ms
    FRAME_TIME_WARNING: 33, // ms
    DRAW_CALLS_WARNING: 200,
    DRAW_CALLS_CRITICAL: 300,
    TRIANGLES_WARNING: 500000,
    TRIANGLES_CRITICAL: 1000000
  }
  
  constructor() {
    console.log('📊 PerformanceMonitor initialized')
    console.log('🎯 Thresholds:', this.THRESHOLDS)
    fileLogger.log('PERF_INIT', 'PerformanceMonitor initialized', this.THRESHOLDS)
    sendLogToServer('PERF_INIT', 'PerformanceMonitor initialized', this.THRESHOLDS)
  }
  
  /**
   * Registrar renderer de Three.js
   */
  setRenderer(renderer: THREE.WebGLRenderer): void {
    this.renderer = renderer
    console.log('🎨 Renderer registered for monitoring')
  }
  
  /**
   * Actualizar métricas cada frame
   */
  update(): PerformanceMetrics | null {
    if (!this.renderer) return null
    
    const now = performance.now()
    const delta = now - this.lastTime
    this.lastTime = now
    
    // Calcular FPS
    this.frameCount++
    const fps = 1000 / delta
    this.fpsHistory.push(fps)
    this.frameTimeHistory.push(delta)
    
    // Mantener solo últimos 60 frames
    if (this.fpsHistory.length > 60) {
      this.fpsHistory.shift()
      this.frameTimeHistory.shift()
    }
    
    // CRÍTICO: Leer renderer.info DESPUÉS del render, no antes
    // El renderer.info se actualiza DURANTE el render, no antes
    const info = this.renderer.info
    const renderInfo = info.render
    const memoryInfo = info.memory
    
    const metrics: PerformanceMetrics = {
      fps: Math.round(fps),
      frameTime: parseFloat(delta.toFixed(2)),
      drawCalls: renderInfo.calls,
      triangles: renderInfo.triangles,
      geometries: memoryInfo.geometries,
      textures: memoryInfo.textures,
      programs: info.programs?.length || 0,
      timestamp: now
    }
    
    // Intentar obtener memoria (solo en Chrome)
    if ('memory' in performance) {
      const mem = (performance as any).memory
      metrics.memoryUsed = Math.round(mem.usedJSHeapSize / 1048576) // MB
    }
    
    // Log periódico
    if (now - this.lastLogTime > this.logInterval) {
      this.logMetrics(metrics)
      this.lastLogTime = now
    }
    
    return metrics
  }
  
  /**
   * Log de métricas en consola
   */
  private logMetrics(metrics: PerformanceMetrics): void {
    const avgFps = this.getAverageFPS()
    const avgFrameTime = this.getAverageFrameTime()
    const minFps = Math.min(...this.fpsHistory)
    const maxFrameTime = Math.max(...this.frameTimeHistory)
    
    // LOG EN ARCHIVO
    fileLogger.log('PERF_METRICS', 'Performance snapshot', {
      fps: avgFps.toFixed(1),
      fpsMin: minFps.toFixed(1),
      frameTime: avgFrameTime.toFixed(2),
      frameTimeMax: maxFrameTime.toFixed(2),
      drawCalls: metrics.drawCalls,
      triangles: metrics.triangles,
      memory: metrics.memoryUsed
    })
    
    // LOG AL SERVIDOR
    sendLogToServer('PERF_METRICS', 'Performance snapshot', {
      fps: avgFps.toFixed(1),
      fpsMin: minFps.toFixed(1),
      frameTime: avgFrameTime.toFixed(2),
      frameTimeMax: maxFrameTime.toFixed(2),
      drawCalls: metrics.drawCalls,
      triangles: metrics.triangles,
      memory: metrics.memoryUsed
    })
    
    console.group('📊 PERFORMANCE METRICS')
    
    // FPS
    const fpsStatus = this.getFPSStatus(avgFps)
    console.log(`%c🎯 FPS: ${avgFps.toFixed(1)} (min: ${minFps.toFixed(1)}) [${fpsStatus.status}]`, 
      `color: ${fpsStatus.color}; font-weight: bold`)
    
    // Frame Time
    const frameTimeStatus = this.getFrameTimeStatus(avgFrameTime)
    console.log(`%c⏱️ Frame Time: ${avgFrameTime.toFixed(2)}ms (max: ${maxFrameTime.toFixed(2)}ms) [${frameTimeStatus.status}]`, 
      `color: ${frameTimeStatus.color}; font-weight: bold`)
    
    // Draw Calls
    const drawCallsStatus = this.getDrawCallsStatus(metrics.drawCalls)
    console.log(`%c🎨 Draw Calls: ${metrics.drawCalls} [${drawCallsStatus.status}]`, 
      `color: ${drawCallsStatus.color}`)
    
    // Triángulos
    const trianglesStatus = this.getTrianglesStatus(metrics.triangles)
    console.log(`%c🔺 Triangles: ${this.formatNumber(metrics.triangles)} [${trianglesStatus.status}]`, 
      `color: ${trianglesStatus.color}`)
    
    // Geometrías y Texturas
    console.log(`📦 Geometries: ${metrics.geometries}`)
    console.log(`🖼️ Textures: ${metrics.textures}`)
    console.log(`🔧 Programs: ${metrics.programs}`)
    
    // Memoria (si disponible)
    if (metrics.memoryUsed) {
      console.log(`💾 Memory: ${metrics.memoryUsed}MB`)
    }
    
    // Warnings
    const warnings = this.getWarnings(metrics, avgFps, avgFrameTime)
    if (warnings.length > 0) {
      console.warn('⚠️ WARNINGS:')
      warnings.forEach(w => console.warn(`  - ${w}`))
      fileLogger.log('PERF_WARNING', 'Performance warnings', warnings)
    }
    
    console.groupEnd()
  }
  
  /**
   * Crear snapshot de performance
   */
  createSnapshot(location: string, weather: string, anomaliesActive: number): void {
    if (!this.renderer) return
    
    const metrics = this.update()
    if (!metrics) return
    
    const avgFps = this.getAverageFPS()
    const avgFrameTime = this.getAverageFrameTime()
    const warnings = this.getWarnings(metrics, avgFps, avgFrameTime)
    
    const snapshot: PerformanceSnapshot = {
      location,
      weather,
      anomaliesActive,
      metrics,
      warnings
    }
    
    this.snapshots.push(snapshot)
    
    // LOG EN ARCHIVO
    fileLogger.log('SNAPSHOT', `Snapshot #${this.snapshots.length}: ${location}`, {
      location,
      weather,
      anomalies: anomaliesActive,
      fps: avgFps.toFixed(1),
      frameTime: avgFrameTime.toFixed(2),
      drawCalls: metrics.drawCalls,
      triangles: metrics.triangles,
      memory: metrics.memoryUsed,
      warnings: warnings.length
    })
    
    // LOG AL SERVIDOR
    sendLogToServer('SNAPSHOT', `Snapshot #${this.snapshots.length}: ${location}`, {
      location,
      weather,
      anomalies: anomaliesActive,
      fps: avgFps.toFixed(1),
      frameTime: avgFrameTime.toFixed(2),
      drawCalls: metrics.drawCalls,
      triangles: metrics.triangles,
      memory: metrics.memoryUsed,
      warnings
    })
    
    console.group(`📸 PERFORMANCE SNAPSHOT #${this.snapshots.length}`)
    console.log(`%c📍 Location: ${location}`, 'font-weight: bold; font-size: 14px')
    console.log(`🌦️ Weather: ${weather}`)
    console.log(`🌌 Anomalies: ${anomaliesActive}`)
    console.log(`📊 FPS: ${avgFps.toFixed(1)} (${this.getFPSStatus(avgFps).status})`)
    console.log(`⏱️ Frame Time: ${avgFrameTime.toFixed(2)}ms (${this.getFrameTimeStatus(avgFrameTime).status})`)
    console.log(`🎨 Draw Calls: ${metrics.drawCalls} (${this.getDrawCallsStatus(metrics.drawCalls).status})`)
    console.log(`🔺 Triangles: ${this.formatNumber(metrics.triangles)} (${this.getTrianglesStatus(metrics.triangles).status})`)
    console.log(`📦 Geometries: ${metrics.geometries}`)
    console.log(`🖼️ Textures: ${metrics.textures}`)
    console.log(`🔧 Programs: ${metrics.programs}`)
    if (metrics.memoryUsed) {
      console.log(`💾 Memory: ${metrics.memoryUsed}MB`)
    }
    
    if (warnings.length > 0) {
      console.warn('⚠️ Warnings:', warnings)
      fileLogger.log('SNAPSHOT_WARNING', 'Snapshot has warnings', warnings)
    } else {
      console.log('✅ No warnings - Performance is good!')
    }
    console.groupEnd()
    
    // Log separador
    console.log('═'.repeat(80))
  }
  
  /**
   * Generar reporte completo
   */
  generateReport(): string {
    if (this.snapshots.length === 0) {
      return 'No snapshots available'
    }
    
    let report = '\n'
    report += '═══════════════════════════════════════════════════════\n'
    report += '📊 ARCHEOSCOPE PERFORMANCE REPORT\n'
    report += '═══════════════════════════════════════════════════════\n\n'
    
    this.snapshots.forEach((snapshot, i) => {
      report += `\n📸 SNAPSHOT ${i + 1}\n`
      report += `${'─'.repeat(50)}\n`
      report += `📍 Location: ${snapshot.location}\n`
      report += `🌦️ Weather: ${snapshot.weather}\n`
      report += `🌌 Anomalies: ${snapshot.anomaliesActive}\n`
      report += `\n📊 Metrics:\n`
      report += `  FPS: ${snapshot.metrics.fps}\n`
      report += `  Frame Time: ${snapshot.metrics.frameTime}ms\n`
      report += `  Draw Calls: ${snapshot.metrics.drawCalls}\n`
      report += `  Triangles: ${this.formatNumber(snapshot.metrics.triangles)}\n`
      report += `  Geometries: ${snapshot.metrics.geometries}\n`
      report += `  Textures: ${snapshot.metrics.textures}\n`
      if (snapshot.metrics.memoryUsed) {
        report += `  Memory: ${snapshot.metrics.memoryUsed}MB\n`
      }
      
      if (snapshot.warnings.length > 0) {
        report += `\n⚠️ Warnings:\n`
        snapshot.warnings.forEach(w => {
          report += `  - ${w}\n`
        })
      }
      report += '\n'
    })
    
    // Análisis comparativo
    if (this.snapshots.length > 1) {
      report += '\n📈 COMPARATIVE ANALYSIS\n'
      report += `${'─'.repeat(50)}\n`
      
      const avgFps = this.snapshots.reduce((sum, s) => sum + s.metrics.fps, 0) / this.snapshots.length
      const avgFrameTime = this.snapshots.reduce((sum, s) => sum + s.metrics.frameTime, 0) / this.snapshots.length
      const avgDrawCalls = this.snapshots.reduce((sum, s) => sum + s.metrics.drawCalls, 0) / this.snapshots.length
      
      report += `Average FPS: ${avgFps.toFixed(1)}\n`
      report += `Average Frame Time: ${avgFrameTime.toFixed(2)}ms\n`
      report += `Average Draw Calls: ${Math.round(avgDrawCalls)}\n`
      
      const worstSnapshot = this.snapshots.reduce((worst, current) => 
        current.metrics.fps < worst.metrics.fps ? current : worst
      )
      
      report += `\n🔴 Worst Performance:\n`
      report += `  Location: ${worstSnapshot.location}\n`
      report += `  Weather: ${worstSnapshot.weather}\n`
      report += `  FPS: ${worstSnapshot.metrics.fps}\n`
      report += `  Frame Time: ${worstSnapshot.metrics.frameTime}ms\n`
    }
    
    report += '\n═══════════════════════════════════════════════════════\n'
    
    return report
  }
  
  /**
   * Imprimir reporte en consola
   */
  printReport(): void {
    console.log(this.generateReport())
  }
  
  /**
   * Limpiar snapshots
   */
  clearSnapshots(): void {
    this.snapshots = []
    console.log('🧹 Snapshots cleared')
  }
  
  // Métodos auxiliares
  
  private getAverageFPS(): number {
    if (this.fpsHistory.length === 0) return 0
    return this.fpsHistory.reduce((a, b) => a + b, 0) / this.fpsHistory.length
  }
  
  private getAverageFrameTime(): number {
    if (this.frameTimeHistory.length === 0) return 0
    return this.frameTimeHistory.reduce((a, b) => a + b, 0) / this.frameTimeHistory.length
  }
  
  private getFPSStatus(fps: number): { status: string, color: string } {
    if (fps < this.THRESHOLDS.FPS_CRITICAL) return { status: 'CRITICAL', color: '#ff0000' }
    if (fps < this.THRESHOLDS.FPS_WARNING) return { status: 'WARNING', color: '#ff9900' }
    return { status: 'GOOD', color: '#00ff00' }
  }
  
  private getFrameTimeStatus(frameTime: number): { status: string, color: string } {
    if (frameTime > this.THRESHOLDS.FRAME_TIME_CRITICAL) return { status: 'CRITICAL', color: '#ff0000' }
    if (frameTime > this.THRESHOLDS.FRAME_TIME_WARNING) return { status: 'WARNING', color: '#ff9900' }
    return { status: 'GOOD', color: '#00ff00' }
  }
  
  private getDrawCallsStatus(drawCalls: number): { status: string, color: string } {
    if (drawCalls > this.THRESHOLDS.DRAW_CALLS_CRITICAL) return { status: 'CRITICAL', color: '#ff0000' }
    if (drawCalls > this.THRESHOLDS.DRAW_CALLS_WARNING) return { status: 'WARNING', color: '#ff9900' }
    return { status: 'GOOD', color: '#00ff00' }
  }
  
  private getTrianglesStatus(triangles: number): { status: string, color: string } {
    if (triangles > this.THRESHOLDS.TRIANGLES_CRITICAL) return { status: 'CRITICAL', color: '#ff0000' }
    if (triangles > this.THRESHOLDS.TRIANGLES_WARNING) return { status: 'WARNING', color: '#ff9900' }
    return { status: 'GOOD', color: '#00ff00' }
  }
  
  private getWarnings(metrics: PerformanceMetrics, avgFps: number, avgFrameTime: number): string[] {
    const warnings: string[] = []
    
    if (avgFps < this.THRESHOLDS.FPS_CRITICAL) {
      warnings.push(`FPS crítico: ${avgFps.toFixed(1)} (objetivo: >${this.THRESHOLDS.FPS_WARNING})`)
    }
    
    if (avgFrameTime > this.THRESHOLDS.FRAME_TIME_CRITICAL) {
      warnings.push(`Frame time crítico: ${avgFrameTime.toFixed(2)}ms (objetivo: <${this.THRESHOLDS.FRAME_TIME_WARNING}ms)`)
    }
    
    if (metrics.drawCalls > this.THRESHOLDS.DRAW_CALLS_WARNING) {
      warnings.push(`Draw calls alto: ${metrics.drawCalls} (objetivo: <${this.THRESHOLDS.DRAW_CALLS_WARNING})`)
    }
    
    if (metrics.triangles > this.THRESHOLDS.TRIANGLES_WARNING) {
      warnings.push(`Triángulos alto: ${this.formatNumber(metrics.triangles)} (objetivo: <${this.formatNumber(this.THRESHOLDS.TRIANGLES_WARNING)})`)
    }
    
    return warnings
  }
  
  private formatNumber(num: number): string {
    if (num >= 1000000) return `${(num / 1000000).toFixed(2)}M`
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
    return num.toString()
  }
}

// Singleton global
export const performanceMonitor = new PerformanceMonitor()

// Export default también para compatibilidad
export default performanceMonitor

// Exponer globalmente para debugging
if (typeof window !== 'undefined') {
  (window as any).perfMonitor = performanceMonitor
}

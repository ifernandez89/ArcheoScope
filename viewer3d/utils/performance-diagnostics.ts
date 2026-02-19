/**
 * Performance Diagnostics - Diagnóstico rápido de performance
 * Identifica cuellos de botella automáticamente
 */

import PerformanceMonitor from './performance-monitor'
import CullingSystem from '@/systems/CullingSystem'
import InstanceManager from '@/systems/InstanceManager'
import GraphicsPresetManager from '@/systems/GraphicsPresets'

export interface DiagnosticResult {
  severity: 'ok' | 'warning' | 'critical'
  category: 'fps' | 'drawCalls' | 'memory' | 'culling' | 'instancing' | 'graphics'
  message: string
  suggestion: string
}

export class PerformanceDiagnostics {
  private static instance: PerformanceDiagnostics
  
  private constructor() {}
  
  static getInstance(): PerformanceDiagnostics {
    if (!PerformanceDiagnostics.instance) {
      PerformanceDiagnostics.instance = new PerformanceDiagnostics()
    }
    return PerformanceDiagnostics.instance
  }
  
  /**
   * Ejecutar diagnóstico completo
   */
  diagnose(): DiagnosticResult[] {
    const results: DiagnosticResult[] = []
    
    // Obtener métricas
    const metrics = PerformanceMonitor.getMetrics()
    const cullingStats = CullingSystem.getStats()
    const instancingStats = InstanceManager.getStats()
    const preset = GraphicsPresetManager.getPreset()
    
    // 1. FPS
    if (metrics.fps < 30) {
      results.push({
        severity: 'critical',
        category: 'fps',
        message: `FPS crítico: ${metrics.fps.toFixed(0)} FPS`,
        suggestion: 'Cambiar a preset LOW y verificar si mejora'
      })
    } else if (metrics.fps < 50) {
      results.push({
        severity: 'warning',
        category: 'fps',
        message: `FPS bajo: ${metrics.fps.toFixed(0)} FPS`,
        suggestion: 'Reducir preset gráfico o activar más culling'
      })
    } else {
      results.push({
        severity: 'ok',
        category: 'fps',
        message: `FPS óptimo: ${metrics.fps.toFixed(0)} FPS`,
        suggestion: 'Performance excelente'
      })
    }
    
    // 2. Draw Calls
    if (metrics.drawCalls > 100) {
      results.push({
        severity: 'critical',
        category: 'drawCalls',
        message: `Draw calls excesivos: ${metrics.drawCalls}`,
        suggestion: 'Usar más InstancedMesh para objetos repetidos'
      })
    } else if (metrics.drawCalls > 50) {
      results.push({
        severity: 'warning',
        category: 'drawCalls',
        message: `Draw calls altos: ${metrics.drawCalls}`,
        suggestion: 'Considerar instancing para reducir draw calls'
      })
    } else {
      results.push({
        severity: 'ok',
        category: 'drawCalls',
        message: `Draw calls óptimos: ${metrics.drawCalls}`,
        suggestion: 'Buen uso de instancing'
      })
    }
    
    // 3. Memoria
    const memoryUsed = typeof metrics.memory === 'number' ? metrics.memory : metrics.memory.used
    if (memoryUsed > 500) {
      results.push({
        severity: 'critical',
        category: 'memory',
        message: `Memoria alta: ${memoryUsed.toFixed(0)}MB`,
        suggestion: 'Activar disposal en CullingSystem'
      })
    } else if (memoryUsed > 300) {
      results.push({
        severity: 'warning',
        category: 'memory',
        message: `Memoria moderada: ${memoryUsed.toFixed(0)}MB`,
        suggestion: 'Monitorear uso de memoria'
      })
    } else {
      results.push({
        severity: 'ok',
        category: 'memory',
        message: `Memoria óptima: ${memoryUsed.toFixed(0)}MB`,
        suggestion: 'Uso eficiente de memoria'
      })
    }
    
    // 4. Culling
    const cullingEfficiency = cullingStats.totalObjects > 0
      ? (cullingStats.culledObjects / cullingStats.totalObjects) * 100
      : 0
    
    if (cullingEfficiency < 20 && cullingStats.totalObjects > 100) {
      results.push({
        severity: 'warning',
        category: 'culling',
        message: `Culling bajo: ${cullingEfficiency.toFixed(0)}% objetos culled`,
        suggestion: 'Aumentar maxRenderDistance o mejorar distribución de objetos'
      })
    } else if (cullingStats.totalObjects > 0) {
      results.push({
        severity: 'ok',
        category: 'culling',
        message: `Culling activo: ${cullingEfficiency.toFixed(0)}% objetos culled`,
        suggestion: 'Sistema de culling funcionando correctamente'
      })
    }
    
    // 5. Instancing
    if (instancingStats.savedDrawCalls > 1000) {
      results.push({
        severity: 'ok',
        category: 'instancing',
        message: `Instancing excelente: ${instancingStats.savedDrawCalls} draw calls ahorrados`,
        suggestion: 'Uso óptimo de instancing'
      })
    } else if (instancingStats.totalInstances > 100 && instancingStats.savedDrawCalls < 50) {
      results.push({
        severity: 'warning',
        category: 'instancing',
        message: `Instancing subóptimo: Solo ${instancingStats.savedDrawCalls} draw calls ahorrados`,
        suggestion: 'Agrupar más objetos en InstancedMesh'
      })
    }
    
    // 6. Graphics Preset
    if (preset === 'ULTRA' && metrics.fps < 50) {
      results.push({
        severity: 'warning',
        category: 'graphics',
        message: 'Preset ULTRA con FPS bajo',
        suggestion: 'Reducir a HIGH o MEDIUM'
      })
    } else if (preset === 'LOW' && metrics.fps >= 55) {
      results.push({
        severity: 'ok',
        category: 'graphics',
        message: 'Preset LOW con buen FPS',
        suggestion: 'Puedes aumentar a MEDIUM o HIGH'
      })
    }
    
    return results
  }
  
  /**
   * Generar reporte en consola
   */
  report(): void {
    const results = this.diagnose()
    
    console.log('🔍 Performance Diagnostics Report')
    console.log('=' .repeat(50))
    
    const critical = results.filter(r => r.severity === 'critical')
    const warnings = results.filter(r => r.severity === 'warning')
    const ok = results.filter(r => r.severity === 'ok')
    
    if (critical.length > 0) {
      console.log('\n🔴 CRITICAL ISSUES:')
      critical.forEach(r => {
        console.log(`  ${r.message}`)
        console.log(`  → ${r.suggestion}`)
      })
    }
    
    if (warnings.length > 0) {
      console.log('\n🟡 WARNINGS:')
      warnings.forEach(r => {
        console.log(`  ${r.message}`)
        console.log(`  → ${r.suggestion}`)
      })
    }
    
    if (ok.length > 0) {
      console.log('\n🟢 OK:')
      ok.forEach(r => {
        console.log(`  ${r.message}`)
      })
    }
    
    console.log('\n' + '='.repeat(50))
    
    // Resumen
    const metrics = PerformanceMonitor.getMetrics()
    const memoryUsed = typeof metrics.memory === 'number' ? metrics.memory : metrics.memory.used
    console.log('\n📊 Summary:')
    console.log(`  FPS: ${metrics.fps.toFixed(0)}`)
    console.log(`  Frame Time: ${metrics.frameTime.toFixed(1)}ms`)
    console.log(`  Draw Calls: ${metrics.drawCalls}`)
    console.log(`  Memory: ${memoryUsed.toFixed(0)}MB`)
    console.log(`  Preset: ${GraphicsPresetManager.getPreset()}`)
  }
  
  /**
   * Sugerencia automática de preset
   */
  suggestPreset(): 'LOW' | 'MEDIUM' | 'HIGH' | 'ULTRA' {
    const metrics = PerformanceMonitor.getMetrics()
    
    if (metrics.fps < 30) return 'LOW'
    if (metrics.fps < 50) return 'MEDIUM'
    if (metrics.fps < 55) return 'HIGH'
    return 'ULTRA'
  }
}

export default PerformanceDiagnostics.getInstance()

/**
 * Uso:
 * 
 * import PerformanceDiagnostics from '@/utils/performance-diagnostics'
 * 
 * // Diagnóstico completo
 * const results = PerformanceDiagnostics.diagnose()
 * 
 * // Reporte en consola
 * PerformanceDiagnostics.report()
 * 
 * // Sugerencia de preset
 * const preset = PerformanceDiagnostics.suggestPreset()
 * GraphicsPresetManager.setPreset(preset)
 */

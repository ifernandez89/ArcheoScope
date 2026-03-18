/**
 * Sistema de Métricas 3D Personalizadas
 * Mide carga de motor 3D, modelos, FPS, etc.
 */

interface Performance3DMetric {
  name: string
  value: number
  timestamp: number
  metadata?: Record<string, any>
}

class Performance3DMonitor {
  private metrics: Performance3DMetric[] = []
  private marks: Map<string, number> = new Map()
  
  // Marcar inicio de operación
  mark(name: string) {
    const timestamp = performance.now()
    this.marks.set(name, timestamp)
    performance.mark(name)
  }
  
  // Medir duración desde marca
  measure(name: string, startMark: string, metadata?: Record<string, any>) {
    if (!this.marks.has(startMark)) {
      console.warn(`[Performance3D] Start mark "${startMark}" not found`)
      return
    }
    
    const endTime = performance.now()
    const startTime = this.marks.get(startMark)!
    const duration = endTime - startTime
    
    // Crear medida en Performance API
    try {
      performance.measure(name, startMark)
    } catch (e) {
      // Ignorar si la marca no existe en Performance API
    }
    
    // Guardar métrica
    const metric: Performance3DMetric = {
      name,
      value: Math.round(duration),
      timestamp: Date.now(),
      metadata
    }
    
    this.metrics.push(metric)
    
    // Log en desarrollo
    if (process.env.NODE_ENV === 'development') {
      console.log(`[3D Metric] ${name}: ${Math.round(duration)}ms`, metadata || '')
    }
    
    // Guardar en localStorage
    this.saveToLocalStorage(metric)
    
    return duration
  }
  
  // Medir carga de modelo
  async measureModelLoad<T>(
    modelName: string,
    loadFn: () => Promise<T>
  ): Promise<T> {
    const markName = `model-${modelName}-start`
    this.mark(markName)
    
    try {
      const result = await loadFn()
      this.measure(`model-load-${modelName}`, markName, { modelName })
      return result
    } catch (error) {
      console.error(`[Performance3D] Error loading model ${modelName}:`, error)
      throw error
    }
  }
  
  // Medir FPS promedio
  measureFPS(duration: number = 1000): Promise<number> {
    return new Promise((resolve) => {
      let frames = 0
      const startTime = performance.now()
      
      const countFrame = () => {
        frames++
        const elapsed = performance.now() - startTime
        
        if (elapsed < duration) {
          requestAnimationFrame(countFrame)
        } else {
          const fps = Math.round((frames / elapsed) * 1000)
          
          const metric: Performance3DMetric = {
            name: 'fps-measurement',
            value: fps,
            timestamp: Date.now(),
            metadata: { duration, frames }
          }
          
          this.metrics.push(metric)
          this.saveToLocalStorage(metric)
          
          if (process.env.NODE_ENV === 'development') {
            console.log(`[3D Metric] FPS: ${fps} (${frames} frames in ${Math.round(elapsed)}ms)`)
          }
          
          resolve(fps)
        }
      }
      
      requestAnimationFrame(countFrame)
    })
  }
  
  // Obtener todas las métricas
  getMetrics(): Performance3DMetric[] {
    return [...this.metrics]
  }
  
  // Obtener métricas por nombre
  getMetricsByName(name: string): Performance3DMetric[] {
    return this.metrics.filter(m => m.name === name)
  }
  
  // Obtener resumen
  getSummary() {
    const summary: Record<string, { count: number; avg: number; min: number; max: number }> = {}
    
    this.metrics.forEach(metric => {
      if (!summary[metric.name]) {
        summary[metric.name] = {
          count: 0,
          avg: 0,
          min: Infinity,
          max: -Infinity
        }
      }
      
      const s = summary[metric.name]
      s.count++
      s.avg = ((s.avg * (s.count - 1)) + metric.value) / s.count
      s.min = Math.min(s.min, metric.value)
      s.max = Math.max(s.max, metric.value)
    })
    
    // Redondear promedios
    Object.keys(summary).forEach(key => {
      summary[key].avg = Math.round(summary[key].avg)
    })
    
    return summary
  }
  
  // Limpiar métricas
  clear() {
    this.metrics = []
    this.marks.clear()
    try {
      localStorage.removeItem('archeoscope_3d_metrics')
    } catch {
      // Ignorar
    }
  }
  
  // Guardar en localStorage
  private saveToLocalStorage(metric: Performance3DMetric) {
    try {
      const key = 'archeoscope_3d_metrics'
      const stored = localStorage.getItem(key)
      const metrics = stored ? JSON.parse(stored) : []
      
      metrics.push(metric)
      
      // Mantener solo últimas 100 métricas
      if (metrics.length > 100) {
        metrics.shift()
      }
      
      localStorage.setItem(key, JSON.stringify(metrics))
    } catch {
      // Ignorar errores
    }
  }
  
  // Obtener métricas de localStorage
  getLocalStorageMetrics(): Performance3DMetric[] {
    try {
      const stored = localStorage.getItem('archeoscope_3d_metrics')
      return stored ? JSON.parse(stored) : []
    } catch {
      return []
    }
  }
}

// Singleton
export const performance3D = new Performance3DMonitor()

// Helpers para uso común
export function mark3D(name: string) {
  performance3D.mark(name)
}

export function measure3D(name: string, startMark: string, metadata?: Record<string, any>) {
  return performance3D.measure(name, startMark, metadata)
}

export async function measureModelLoad<T>(modelName: string, loadFn: () => Promise<T>): Promise<T> {
  return performance3D.measureModelLoad(modelName, loadFn)
}

export function measureFPS(duration?: number): Promise<number> {
  return performance3D.measureFPS(duration)
}

export function get3DMetrics() {
  return performance3D.getMetrics()
}

export function get3DSummary() {
  return performance3D.getSummary()
}

export function clear3DMetrics() {
  performance3D.clear()
}

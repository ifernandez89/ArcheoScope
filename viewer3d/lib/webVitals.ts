/**
 * Sistema de Web Vitals - Métricas Reales de Performance
 * Mide FCP, LCP, TTFB, CLS, INP en usuarios reales
 */

import { onCLS, onFCP, onINP, onLCP, onTTFB, type Metric } from 'web-vitals'

interface MetricData {
  name: string
  value: number
  rating: 'good' | 'needs-improvement' | 'poor'
  delta: number
  id: string
  navigationType: string
  route: string
  device: string
  timestamp: number
}

// Almacenamiento local de métricas
const metricsStore: MetricData[] = []

// Detectar tipo de dispositivo
function getDeviceType(): string {
  if (typeof window === 'undefined') return 'unknown'
  
  const ua = navigator.userAgent
  if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
    return 'tablet'
  }
  if (/Mobile|Android|iP(hone|od)|IEMobile|BlackBerry|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(ua)) {
    return 'mobile'
  }
  return 'desktop'
}

// Obtener ruta actual
function getCurrentRoute(): string {
  if (typeof window === 'undefined') return 'unknown'
  return window.location.pathname
}

// Procesar métrica
function processMetric(metric: Metric) {
  const metricData: MetricData = {
    name: metric.name,
    value: Math.round(metric.value),
    rating: metric.rating,
    delta: Math.round(metric.delta),
    id: metric.id,
    navigationType: metric.navigationType,
    route: getCurrentRoute(),
    device: getDeviceType(),
    timestamp: Date.now()
  }
  
  // Guardar en store local
  metricsStore.push(metricData)
  
  // Log en consola (desarrollo)
  if (process.env.NODE_ENV === 'development') {
    console.log(`[Web Vital] ${metric.name}:`, {
      value: `${metricData.value}ms`,
      rating: metricData.rating,
      route: metricData.route,
      device: metricData.device
    })
  }
  
  // Enviar a analytics (producción)
  if (process.env.NODE_ENV === 'production') {
    sendToAnalytics(metricData)
  }
  
  // Guardar en localStorage para análisis posterior
  saveToLocalStorage(metricData)
}

// Enviar a sistema de analytics
function sendToAnalytics(metric: MetricData) {
  // Aquí se puede integrar con:
  // - Google Analytics
  // - Custom backend
  // - Vercel Analytics
  // - etc.
  
  // Por ahora, usar navigator.sendBeacon para envío no bloqueante
  if (typeof navigator !== 'undefined' && navigator.sendBeacon) {
    const blob = new Blob([JSON.stringify(metric)], { type: 'application/json' })
    navigator.sendBeacon('/api/metrics', blob)
  }
}

// Guardar en localStorage
function saveToLocalStorage(metric: MetricData) {
  try {
    const key = 'archeoscope_metrics'
    const stored = localStorage.getItem(key)
    const metrics = stored ? JSON.parse(stored) : []
    
    // Mantener solo últimas 100 métricas
    metrics.push(metric)
    if (metrics.length > 100) {
      metrics.shift()
    }
    
    localStorage.setItem(key, JSON.stringify(metrics))
  } catch (error) {
    // Ignorar errores de localStorage
  }
}

// Inicializar Web Vitals
export function initWebVitals() {
  if (typeof window === 'undefined') return
  
  // Registrar listeners para cada métrica
  onCLS(processMetric)
  onFCP(processMetric)
  onINP(processMetric)
  onLCP(processMetric)
  onTTFB(processMetric)
  
  console.log('📊 Web Vitals initialized')
}

// Obtener métricas almacenadas
export function getStoredMetrics(): MetricData[] {
  return [...metricsStore]
}

// Obtener métricas de localStorage
export function getLocalStorageMetrics(): MetricData[] {
  try {
    const stored = localStorage.getItem('archeoscope_metrics')
    return stored ? JSON.parse(stored) : []
  } catch {
    return []
  }
}

// Limpiar métricas
export function clearMetrics() {
  metricsStore.length = 0
  try {
    localStorage.removeItem('archeoscope_metrics')
  } catch {
    // Ignorar
  }
}

// Obtener resumen de métricas
export function getMetricsSummary() {
  const metrics = getLocalStorageMetrics()
  
  const summary = {
    fcp: { values: [] as number[], avg: 0, min: 0, max: 0 },
    lcp: { values: [] as number[], avg: 0, min: 0, max: 0 },
    ttfb: { values: [] as number[], avg: 0, min: 0, max: 0 },
    cls: { values: [] as number[], avg: 0, min: 0, max: 0 },
    inp: { values: [] as number[], avg: 0, min: 0, max: 0 }
  }
  
  metrics.forEach(m => {
    const key = m.name.toLowerCase() as keyof typeof summary
    if (summary[key]) {
      summary[key].values.push(m.value)
    }
  })
  
  // Calcular estadísticas
  Object.keys(summary).forEach(key => {
    const k = key as keyof typeof summary
    const values = summary[k].values
    if (values.length > 0) {
      summary[k].avg = Math.round(values.reduce((a, b) => a + b, 0) / values.length)
      summary[k].min = Math.min(...values)
      summary[k].max = Math.max(...values)
    }
  })
  
  return summary
}

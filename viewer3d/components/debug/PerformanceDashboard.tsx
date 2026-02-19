'use client'

import { useEffect, useState } from 'react'
import PerformanceMonitor, { type PerformanceMetrics } from '@/utils/performance-monitor'

export function PerformanceDashboard() {
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null)
  const [isOpen, setIsOpen] = useState(false)
  const [suggestions, setSuggestions] = useState<string[]>([])

  useEffect(() => {
    const monitor = PerformanceMonitor

    // Suscribirse a cambios
    const unsubscribe = monitor.subscribe((newMetrics) => {
      setMetrics(newMetrics)
      setSuggestions(monitor.getOptimizationSuggestions())
    })

    // Actualizar memoria cada segundo
    const memoryInterval = setInterval(() => {
      monitor.updateMemoryMetrics()
    }, 1000)

    return () => {
      unsubscribe()
      clearInterval(memoryInterval)
    }
  }, [])

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed top-4 right-4 bg-purple-600 hover:bg-purple-700 text-white px-3 py-2 rounded-lg text-sm z-50"
      >
        ⚡ Performance
      </button>
    )
  }

  if (!metrics) return null

  const performanceLevel = PerformanceMonitor.getPerformanceLevel()
  const avgFPS = PerformanceMonitor.getAverageFPS()
  const minFPS = PerformanceMonitor.getMinFPS()
  const maxFPS = PerformanceMonitor.getMaxFPS()

  return (
    <div className="fixed top-4 right-4 bg-black/95 backdrop-blur-md text-white p-4 rounded-lg border border-white/20 w-96 max-h-[90vh] overflow-y-auto z-50">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <h3 className="font-bold text-lg">⚡ Performance</h3>
          <span className={`text-xs px-2 py-1 rounded ${getPerformanceLevelColor(performanceLevel)}`}>
            {performanceLevel.toUpperCase()}
          </span>
        </div>
        <button
          onClick={() => setIsOpen(false)}
          className="text-white/60 hover:text-white"
        >
          ✕
        </button>
      </div>

      {/* FPS */}
      <div className="mb-4 pb-4 border-b border-white/10">
        <div className="flex items-end justify-between mb-2">
          <div>
            <div className="text-sm text-white/60">FPS</div>
            <div className="text-3xl font-bold">{metrics.fps}</div>
          </div>
          <div className="text-right text-xs text-white/60">
            <div>Avg: {avgFPS}</div>
            <div>Min: {minFPS}</div>
            <div>Max: {maxFPS}</div>
          </div>
        </div>
        
        {/* FPS Bar */}
        <div className="h-2 bg-white/10 rounded-full overflow-hidden">
          <div
            className={`h-full transition-all ${getFPSColor(metrics.fps)}`}
            style={{ width: `${Math.min((metrics.fps / 60) * 100, 100)}%` }}
          />
        </div>
        
        <div className="text-xs text-white/60 mt-1">
          Frame Time: {metrics.frameTime.toFixed(2)}ms
        </div>
      </div>

      {/* Memory */}
      <div className="mb-4 pb-4 border-b border-white/10">
        <div className="text-sm text-white/60 mb-2">Memory Usage</div>
        <div className="space-y-2">
          <div className="flex justify-between text-xs">
            <span>Used</span>
            <span className="font-mono">{metrics.memory.used} MB</span>
          </div>
          <div className="h-2 bg-white/10 rounded-full overflow-hidden">
            <div
              className="h-full bg-blue-500 transition-all"
              style={{ width: `${(metrics.memory.used / metrics.memory.limit) * 100}%` }}
            />
          </div>
          <div className="flex justify-between text-xs text-white/60">
            <span>Total: {metrics.memory.total} MB</span>
            <span>Limit: {metrics.memory.limit} MB</span>
          </div>
        </div>
      </div>

      {/* Rendering Stats */}
      <div className="mb-4 pb-4 border-b border-white/10">
        <div className="text-sm text-white/60 mb-2">Rendering</div>
        <div className="grid grid-cols-2 gap-2 text-xs">
          <StatItem label="Draw Calls" value={metrics.drawCalls} />
          <StatItem label="Triangles" value={formatNumber(metrics.triangles)} />
          <StatItem label="Geometries" value={metrics.geometries} />
          <StatItem label="Textures" value={metrics.textures} />
          <StatItem label="Programs" value={metrics.programs} />
          <StatItem label="Load Time" value={`${(metrics.loadTime / 1000).toFixed(2)}s`} />
        </div>
      </div>

      {/* Optimization Suggestions */}
      {suggestions.length > 0 && (
        <div className="mb-4">
          <div className="text-sm text-white/60 mb-2">💡 Suggestions</div>
          <div className="space-y-2">
            {suggestions.map((suggestion, index) => (
              <div
                key={index}
                className="text-xs bg-yellow-500/10 border border-yellow-500/30 rounded p-2 text-yellow-200"
              >
                {suggestion}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-2">
        <button
          onClick={() => {
            const data = PerformanceMonitor.exportMetrics()
            console.log('Performance Metrics:', data)
            
            // Copiar al clipboard
            navigator.clipboard.writeText(data)
            alert('Metrics copied to clipboard!')
          }}
          className="flex-1 bg-white/10 hover:bg-white/20 px-3 py-2 rounded text-xs transition-colors"
        >
          📋 Export
        </button>
        <button
          onClick={() => {
            PerformanceMonitor.reset()
          }}
          className="flex-1 bg-white/10 hover:bg-white/20 px-3 py-2 rounded text-xs transition-colors"
        >
          🔄 Reset
        </button>
      </div>
    </div>
  )
}

function StatItem({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="bg-white/5 rounded p-2">
      <div className="text-white/60 text-[10px]">{label}</div>
      <div className="font-mono text-sm">{value}</div>
    </div>
  )
}

function getPerformanceLevelColor(level: string): string {
  switch (level) {
    case 'excellent': return 'bg-green-500/20 text-green-400'
    case 'good': return 'bg-blue-500/20 text-blue-400'
    case 'fair': return 'bg-yellow-500/20 text-yellow-400'
    case 'poor': return 'bg-red-500/20 text-red-400'
    default: return 'bg-gray-500/20 text-gray-400'
  }
}

function getFPSColor(fps: number): string {
  if (fps >= 55) return 'bg-green-500'
  if (fps >= 45) return 'bg-blue-500'
  if (fps >= 30) return 'bg-yellow-500'
  return 'bg-red-500'
}

function formatNumber(num: number): string {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toString()
}

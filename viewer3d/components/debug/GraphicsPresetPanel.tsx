/**
 * GraphicsPresetPanel - Panel para cambiar presets gráficos
 * CRÍTICO: Medir antes de optimizar
 */

'use client'

import { useState, useEffect } from 'react'
import GraphicsPresetManager, { QualityPreset, GraphicsConfig } from '@/systems/GraphicsPresets'
import PerformanceMonitor from '@/utils/performance-monitor'

export default function GraphicsPresetPanel() {
  const [preset, setPreset] = useState<QualityPreset>(GraphicsPresetManager.getPreset())
  const [config, setConfig] = useState<GraphicsConfig>(GraphicsPresetManager.getConfig())
  const [metrics, setMetrics] = useState(PerformanceMonitor.getMetrics())
  
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(PerformanceMonitor.getMetrics())
    }, 100)
    
    return () => clearInterval(interval)
  }, [])
  
  const handlePresetChange = (newPreset: QualityPreset) => {
    setPreset(newPreset)
    GraphicsPresetManager.setPreset(newPreset)
    setConfig(GraphicsPresetManager.getConfig())
    
    // Recargar para aplicar cambios
    window.location.reload()
  }
  
  const presets: QualityPreset[] = ['LOW', 'MEDIUM', 'HIGH', 'ULTRA']
  
  const getPresetColor = (p: QualityPreset) => {
    switch (p) {
      case 'LOW': return 'bg-gray-600'
      case 'MEDIUM': return 'bg-blue-600'
      case 'HIGH': return 'bg-green-600'
      case 'ULTRA': return 'bg-purple-600'
    }
  }
  
  const getFPSColor = (fps: number) => {
    if (fps >= 55) return 'text-green-400'
    if (fps >= 30) return 'text-yellow-400'
    return 'text-red-400'
  }
  
  return (
    <div className="fixed top-4 left-1/2 -translate-x-1/2 bg-black/90 text-white p-4 rounded-lg font-mono text-xs w-96 z-50">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-bold">🎨 Graphics Quality</h3>
        <span className={`text-lg font-bold ${getFPSColor(metrics.fps)}`}>
          {metrics.fps.toFixed(0)} FPS
        </span>
      </div>
      
      {/* Presets */}
      <div className="grid grid-cols-4 gap-2 mb-4">
        {presets.map(p => (
          <button
            key={p}
            onClick={() => handlePresetChange(p)}
            className={`px-3 py-2 rounded text-xs font-bold transition-all ${
              preset === p
                ? getPresetColor(p)
                : 'bg-gray-700 hover:bg-gray-600'
            }`}
          >
            {p}
          </button>
        ))}
      </div>
      
      {/* Configuración actual */}
      <div className="border-t border-gray-700 pt-3 space-y-2 text-[10px]">
        <h4 className="font-bold mb-2">Current Settings:</h4>
        
        <div className="grid grid-cols-2 gap-2">
          <div>
            <p className="text-gray-400">Shadows:</p>
            <p className={config.shadows ? 'text-green-400' : 'text-red-400'}>
              {config.shadows ? `✓ ${config.shadowMapSize}px` : '✗ Disabled'}
            </p>
          </div>
          
          <div>
            <p className="text-gray-400">Antialias:</p>
            <p className={config.antialias ? 'text-green-400' : 'text-red-400'}>
              {config.antialias ? '✓ Enabled' : '✗ Disabled'}
            </p>
          </div>
          
          <div>
            <p className="text-gray-400">Bloom:</p>
            <p className={config.bloom ? 'text-green-400' : 'text-red-400'}>
              {config.bloom ? '✓ Enabled' : '✗ Disabled'}
            </p>
          </div>
          
          <div>
            <p className="text-gray-400">SSAO:</p>
            <p className={config.ssao ? 'text-green-400' : 'text-red-400'}>
              {config.ssao ? '✓ Enabled' : '✗ Disabled'}
            </p>
          </div>
          
          <div>
            <p className="text-gray-400">Pixel Ratio:</p>
            <p className="text-white">{config.pixelRatio.toFixed(2)}x</p>
          </div>
          
          <div>
            <p className="text-gray-400">Max Distance:</p>
            <p className="text-white">{config.maxDrawDistance}m</p>
          </div>
        </div>
      </div>
      
      {/* Métricas de performance */}
      <div className="border-t border-gray-700 pt-3 mt-3 space-y-1 text-[10px]">
        <h4 className="font-bold mb-2">Performance:</h4>
        
        <div className="flex justify-between">
          <span className="text-gray-400">Frame Time:</span>
          <span className="text-white">{metrics.frameTime.toFixed(1)}ms</span>
        </div>
        
        <div className="flex justify-between">
          <span className="text-gray-400">Draw Calls:</span>
          <span className="text-white">{metrics.drawCalls}</span>
        </div>
        
        <div className="flex justify-between">
          <span className="text-gray-400">Triangles:</span>
          <span className="text-white">{(metrics.triangles / 1000).toFixed(1)}K</span>
        </div>
        
        <div className="flex justify-between">
          <span className="text-gray-400">Memory:</span>
          <span className="text-white">
            {typeof metrics.memory === 'object' && 'used' in metrics.memory
              ? `${metrics.memory.used.toFixed(0)}MB`
              : `${(metrics.memory as number).toFixed(0)}MB`}
          </span>
        </div>
      </div>
      
      {/* Diagnóstico */}
      <div className="border-t border-gray-700 pt-3 mt-3 text-[10px]">
        <h4 className="font-bold mb-2">💡 Diagnosis:</h4>
        {metrics.fps < 30 && (
          <p className="text-red-400">
            ⚠️ Low FPS detected. Try LOW preset.
          </p>
        )}
        {metrics.fps >= 55 && preset !== 'ULTRA' && (
          <p className="text-green-400">
            ✓ Good performance. Try higher preset.
          </p>
        )}
        {metrics.drawCalls > 100 && (
          <p className="text-yellow-400">
            ⚠️ High draw calls. Use more instancing.
          </p>
        )}
      </div>
      
      <div className="border-t border-gray-700 pt-3 mt-3 text-[10px] text-gray-500">
        <p>💡 Si LOW es fluido y HIGH no → problema en postprocesado</p>
      </div>
    </div>
  )
}

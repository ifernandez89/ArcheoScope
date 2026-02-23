/**
 * GraphicsPresetPanel - Panel para cambiar presets gráficos
 * TEMPORALMENTE DESHABILITADO - Usar nuevo sistema de performance con performanceMonitor
 */

'use client'

import { useState } from 'react'
import GraphicsPresetManager, { QualityPreset, GraphicsConfig } from '@/systems/GraphicsPresets'

export default function GraphicsPresetPanel() {
  const [preset, setPreset] = useState<QualityPreset>(GraphicsPresetManager.getPreset())
  const [config, setConfig] = useState<GraphicsConfig>(GraphicsPresetManager.getConfig())
  
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
  
  return (
    <div className="fixed top-4 left-1/2 -translate-x-1/2 bg-black/90 text-white p-4 rounded-lg font-mono text-xs w-96 z-50">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-bold">🎨 Graphics Quality</h3>
        <span className="text-sm text-gray-400">
          Use window.perfMonitor.printReport() in console
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
      
      <div className="border-t border-gray-700 pt-3 mt-3 text-[10px] text-gray-400">
        <p>💡 Open browser console and use:</p>
        <p className="text-white mt-1">window.perfMonitor.printReport()</p>
        <p className="text-white">window.perfMonitor.createSnapshot("Location", "Weather", 1)</p>
      </div>
    </div>
  )
}

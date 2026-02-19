/**
 * CullingDebugPanel - Panel de debug para CullingSystem
 * Muestra estadísticas en tiempo real
 */

'use client'

import { useEffect, useState } from 'react'
import CullingSystem from '@/systems/CullingSystem'

export default function CullingDebugPanel() {
  const [stats, setStats] = useState({
    totalObjects: 0,
    visibleObjects: 0,
    culledObjects: 0,
    disposedObjects: 0,
    savedDrawCalls: 0
  })

  const [config, setConfig] = useState({
    enableFrustumCulling: true,
    enableDistanceCulling: true,
    enableDisposal: true,
    maxRenderDistance: 2000,
    disposalDistance: 2500
  })

  useEffect(() => {
    const interval = setInterval(() => {
      setStats(CullingSystem.getStats())
    }, 100)

    return () => clearInterval(interval)
  }, [])

  const handleConfigChange = (key: string, value: any) => {
    const newConfig = { ...config, [key]: value }
    setConfig(newConfig)
    CullingSystem.configure(newConfig)
  }

  const visibilityPercent = stats.totalObjects > 0
    ? ((stats.visibleObjects / stats.totalObjects) * 100).toFixed(1)
    : '0.0'

  const culledPercent = stats.totalObjects > 0
    ? ((stats.culledObjects / stats.totalObjects) * 100).toFixed(1)
    : '0.0'

  return (
    <div className="fixed top-4 right-4 bg-black/80 text-white p-4 rounded-lg font-mono text-xs w-80 z-50">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-bold">✂️ Culling System</h3>
        <button
          onClick={() => CullingSystem.cleanupDisposed()}
          className="px-2 py-1 bg-red-600 hover:bg-red-700 rounded text-xs"
        >
          🧹 Cleanup
        </button>
      </div>

      {/* Estadísticas */}
      <div className="space-y-2 mb-4">
        <div className="flex justify-between">
          <span className="text-gray-400">Total Objects:</span>
          <span className="text-white font-bold">{stats.totalObjects}</span>
        </div>

        <div className="flex justify-between">
          <span className="text-gray-400">Visible:</span>
          <span className="text-green-400 font-bold">
            {stats.visibleObjects} ({visibilityPercent}%)
          </span>
        </div>

        <div className="flex justify-between">
          <span className="text-gray-400">Culled:</span>
          <span className="text-yellow-400 font-bold">
            {stats.culledObjects} ({culledPercent}%)
          </span>
        </div>

        <div className="flex justify-between">
          <span className="text-gray-400">Disposed:</span>
          <span className="text-red-400 font-bold">{stats.disposedObjects}</span>
        </div>

        <div className="flex justify-between">
          <span className="text-gray-400">Saved Draw Calls:</span>
          <span className="text-cyan-400 font-bold">{stats.savedDrawCalls}</span>
        </div>
      </div>

      {/* Barra de progreso visual */}
      <div className="mb-4">
        <div className="h-4 bg-gray-700 rounded overflow-hidden flex">
          <div
            className="bg-green-500"
            style={{ width: `${visibilityPercent}%` }}
            title={`Visible: ${visibilityPercent}%`}
          />
          <div
            className="bg-yellow-500"
            style={{ width: `${culledPercent}%` }}
            title={`Culled: ${culledPercent}%`}
          />
        </div>
        <div className="flex justify-between text-[10px] text-gray-500 mt-1">
          <span>Visible</span>
          <span>Culled</span>
        </div>
      </div>

      {/* Configuración */}
      <div className="border-t border-gray-700 pt-3 space-y-2">
        <h4 className="text-xs font-bold mb-2">Configuration</h4>

        <label className="flex items-center justify-between">
          <span className="text-gray-400">Frustum Culling:</span>
          <input
            type="checkbox"
            checked={config.enableFrustumCulling}
            onChange={(e) => handleConfigChange('enableFrustumCulling', e.target.checked)}
            className="w-4 h-4"
          />
        </label>

        <label className="flex items-center justify-between">
          <span className="text-gray-400">Distance Culling:</span>
          <input
            type="checkbox"
            checked={config.enableDistanceCulling}
            onChange={(e) => handleConfigChange('enableDistanceCulling', e.target.checked)}
            className="w-4 h-4"
          />
        </label>

        <label className="flex items-center justify-between">
          <span className="text-gray-400">Auto Disposal:</span>
          <input
            type="checkbox"
            checked={config.enableDisposal}
            onChange={(e) => handleConfigChange('enableDisposal', e.target.checked)}
            className="w-4 h-4"
          />
        </label>

        <div>
          <label className="flex items-center justify-between mb-1">
            <span className="text-gray-400">Max Render Distance:</span>
            <span className="text-white">{config.maxRenderDistance}m</span>
          </label>
          <input
            type="range"
            min="500"
            max="5000"
            step="100"
            value={config.maxRenderDistance}
            onChange={(e) => handleConfigChange('maxRenderDistance', parseInt(e.target.value))}
            className="w-full"
          />
        </div>

        <div>
          <label className="flex items-center justify-between mb-1">
            <span className="text-gray-400">Disposal Distance:</span>
            <span className="text-white">{config.disposalDistance}m</span>
          </label>
          <input
            type="range"
            min="1000"
            max="6000"
            step="100"
            value={config.disposalDistance}
            onChange={(e) => handleConfigChange('disposalDistance', parseInt(e.target.value))}
            className="w-full"
          />
        </div>
      </div>

      {/* Leyenda */}
      <div className="border-t border-gray-700 pt-3 mt-3 text-[10px] text-gray-500">
        <p>🟢 Visible: Renderizando</p>
        <p>🟡 Culled: Oculto (memoria activa)</p>
        <p>🔴 Disposed: Desmontado (memoria liberada)</p>
      </div>
    </div>
  )
}

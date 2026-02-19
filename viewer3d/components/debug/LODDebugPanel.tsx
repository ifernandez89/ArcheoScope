'use client'

import { useEffect, useState } from 'react'
import { WorldCore } from '@/engines/WorldCore'

/**
 * LODDebugPanel - Panel de debug para visualizar estadísticas LOD
 */
export function LODDebugPanel() {
  const [stats, setStats] = useState({
    totalObjects: 0,
    byLevel: {} as Record<number, number>
  })
  const [isOpen, setIsOpen] = useState(true)

  useEffect(() => {
    const interval = setInterval(() => {
      setStats(WorldCore.LOD.getStats())
    }, 100)

    return () => clearInterval(interval)
  }, [])

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-4 right-4 bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg text-sm"
      >
        📊 LOD Stats
      </button>
    )
  }

  const levels = Object.keys(stats.byLevel).sort()
  const maxCount = Math.max(...Object.values(stats.byLevel), 1)

  return (
    <div className="fixed bottom-4 right-4 bg-black/90 backdrop-blur-md text-white p-4 rounded-lg border border-white/20 w-80">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-bold text-lg">🎚️ LOD Statistics</h3>
        <button
          onClick={() => setIsOpen(false)}
          className="text-white/60 hover:text-white"
        >
          ✕
        </button>
      </div>

      {/* Total Objects */}
      <div className="mb-4 pb-3 border-b border-white/10">
        <div className="text-sm text-white/60">Total Objects</div>
        <div className="text-2xl font-bold">{stats.totalObjects}</div>
      </div>

      {/* Distribution by Level */}
      <div className="space-y-2">
        <div className="text-sm text-white/60 mb-2">Distribution by Level</div>
        
        {levels.map((levelStr) => {
          const level = parseInt(levelStr)
          const count = stats.byLevel[level] || 0
          const percentage = stats.totalObjects > 0 
            ? (count / stats.totalObjects) * 100 
            : 0
          const barWidth = (count / maxCount) * 100

          return (
            <div key={level} className="space-y-1">
              <div className="flex items-center justify-between text-xs">
                <span className="text-white/80">
                  {getLevelName(level)}
                </span>
                <span className="text-white/60">
                  {count} ({percentage.toFixed(1)}%)
                </span>
              </div>
              
              {/* Progress Bar */}
              <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                <div
                  className={`h-full transition-all duration-300 ${getLevelColor(level)}`}
                  style={{ width: `${barWidth}%` }}
                />
              </div>
            </div>
          )
        })}
      </div>

      {/* Legend */}
      <div className="mt-4 pt-3 border-t border-white/10">
        <div className="text-xs text-white/60 space-y-1">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-500 rounded" />
            <span>LOD 0: High Detail (&lt;50m)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-blue-500 rounded" />
            <span>LOD 1: Medium Detail (50-150m)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-yellow-500 rounded" />
            <span>LOD 2: Low Detail (150-300m)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-red-500 rounded" />
            <span>LOD 3+: Billboard (&gt;300m)</span>
          </div>
        </div>
      </div>

      {/* Performance Tip */}
      {stats.byLevel[0] > 50 && (
        <div className="mt-3 p-2 bg-yellow-500/20 border border-yellow-500/30 rounded text-xs text-yellow-200">
          ⚠️ Many objects at LOD 0. Consider moving camera or adjusting distances.
        </div>
      )}
    </div>
  )
}

function getLevelName(level: number): string {
  switch (level) {
    case 0: return 'LOD 0 (High)'
    case 1: return 'LOD 1 (Medium)'
    case 2: return 'LOD 2 (Low)'
    case 3: return 'LOD 3 (Billboard)'
    default: return `LOD ${level}`
  }
}

function getLevelColor(level: number): string {
  switch (level) {
    case 0: return 'bg-green-500'
    case 1: return 'bg-blue-500'
    case 2: return 'bg-yellow-500'
    case 3: return 'bg-red-500'
    default: return 'bg-gray-500'
  }
}

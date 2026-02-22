/**
 * Terrain Control UI
 * 
 * Panel de control para el sistema de terreno mejorado
 */

import { useState, useEffect } from 'react'
import { terrainDataService, type CacheStats } from '../services/TerrainDataService'

interface TerrainControlProps {
  enabled: boolean
  onToggle: (enabled: boolean) => void
  exaggeration: number
  onExaggerationChange: (value: number) => void
  enableLOD: boolean
  onLODToggle: (enabled: boolean) => void
}

export default function TerrainControl({
  enabled,
  onToggle,
  exaggeration,
  onExaggerationChange,
  enableLOD,
  onLODToggle
}: TerrainControlProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [cacheStats, setCacheStats] = useState<CacheStats | null>(null)
  const [isLoadingStats, setIsLoadingStats] = useState(false)
  
  // Cargar estadísticas del caché
  const loadCacheStats = async () => {
    setIsLoadingStats(true)
    try {
      const stats = await terrainDataService.getCacheStats()
      setCacheStats(stats)
    } catch (error) {
      console.error('Error loading cache stats:', error)
    } finally {
      setIsLoadingStats(false)
    }
  }
  
  // Cargar stats cuando se expande el panel
  useEffect(() => {
    if (isExpanded && !cacheStats) {
      loadCacheStats()
    }
  }, [isExpanded])
  
  // Limpiar caché
  const handleClearCache = async () => {
    if (!confirm('¿Limpiar caché de terreno mayor a 30 días?')) return
    
    try {
      const result = await terrainDataService.clearCache(30)
      alert(`✅ ${result.cleared_tiles} tiles eliminados`)
      loadCacheStats()
    } catch (error) {
      alert('❌ Error limpiando caché')
    }
  }
  
  // Pre-fetch sitios comunes
  const handlePrefetch = async () => {
    try {
      await terrainDataService.prefetchCommonSites()
      alert('✅ Pre-descarga iniciada para sitios arqueológicos comunes')
      setTimeout(loadCacheStats, 2000)
    } catch (error) {
      alert('❌ Error en pre-descarga')
    }
  }
  
  return (
    <div style={{
      position: 'absolute',
      top: '20px',
      right: '20px',
      zIndex: 1001,
      background: 'rgba(0, 0, 0, 0.85)',
      backdropFilter: 'blur(10px)',
      borderRadius: '12px',
      border: '1px solid rgba(255,255,255,0.2)',
      padding: '16px',
      minWidth: '280px',
      maxWidth: '320px',
      color: 'white',
      fontSize: '13px',
      fontFamily: 'system-ui',
      boxShadow: '0 8px 32px rgba(0,0,0,0.5)'
    }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '12px',
        paddingBottom: '12px',
        borderBottom: '1px solid rgba(255,255,255,0.1)'
      }}>
        <div style={{ fontWeight: 'bold', fontSize: '15px' }}>
          🗺️ Terreno Mejorado
        </div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          style={{
            background: 'none',
            border: 'none',
            color: 'white',
            cursor: 'pointer',
            fontSize: '18px',
            padding: '4px'
          }}
        >
          {isExpanded ? '▼' : '▶'}
        </button>
      </div>
      
      {/* Toggle principal */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: isExpanded ? '16px' : '0'
      }}>
        <span>Activar DEM Real</span>
        <label style={{ position: 'relative', display: 'inline-block', width: '48px', height: '24px' }}>
          <input
            type="checkbox"
            checked={enabled}
            onChange={(e) => onToggle(e.target.checked)}
            style={{ opacity: 0, width: 0, height: 0 }}
          />
          <span style={{
            position: 'absolute',
            cursor: 'pointer',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: enabled ? '#4ade80' : '#6b7280',
            borderRadius: '24px',
            transition: '0.3s'
          }}>
            <span style={{
              position: 'absolute',
              content: '',
              height: '18px',
              width: '18px',
              left: enabled ? '26px' : '3px',
              bottom: '3px',
              background: 'white',
              borderRadius: '50%',
              transition: '0.3s'
            }} />
          </span>
        </label>
      </div>
      
      {/* Controles expandidos */}
      {isExpanded && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Exageración vertical */}
          <div>
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between',
              marginBottom: '8px',
              fontSize: '12px',
              color: '#aaa'
            }}>
              <span>Exageración Vertical</span>
              <span>{exaggeration.toFixed(1)}x</span>
            </div>
            <input
              type="range"
              min="0.5"
              max="3.0"
              step="0.1"
              value={exaggeration}
              onChange={(e) => onExaggerationChange(parseFloat(e.target.value))}
              disabled={!enabled}
              style={{
                width: '100%',
                cursor: enabled ? 'pointer' : 'not-allowed',
                opacity: enabled ? 1 : 0.5
              }}
            />
          </div>
          
          {/* LOD */}
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <span style={{ fontSize: '12px', color: '#aaa' }}>Level of Detail (LOD)</span>
            <label style={{ position: 'relative', display: 'inline-block', width: '40px', height: '20px' }}>
              <input
                type="checkbox"
                checked={enableLOD}
                onChange={(e) => onLODToggle(e.target.checked)}
                disabled={!enabled}
                style={{ opacity: 0, width: 0, height: 0 }}
              />
              <span style={{
                position: 'absolute',
                cursor: enabled ? 'pointer' : 'not-allowed',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: enableLOD && enabled ? '#4ade80' : '#6b7280',
                borderRadius: '20px',
                transition: '0.3s',
                opacity: enabled ? 1 : 0.5
              }}>
                <span style={{
                  position: 'absolute',
                  height: '14px',
                  width: '14px',
                  left: enableLOD ? '22px' : '3px',
                  bottom: '3px',
                  background: 'white',
                  borderRadius: '50%',
                  transition: '0.3s'
                }} />
              </span>
            </label>
          </div>
          
          {/* Estadísticas del caché */}
          <div style={{
            paddingTop: '12px',
            borderTop: '1px solid rgba(255,255,255,0.1)'
          }}>
            <div style={{ 
              fontWeight: 'bold', 
              marginBottom: '8px',
              fontSize: '12px',
              color: '#aaa'
            }}>
              Caché
            </div>
            
            {isLoadingStats ? (
              <div style={{ fontSize: '11px', color: '#888' }}>Cargando...</div>
            ) : cacheStats ? (
              <div style={{ fontSize: '11px', color: '#ccc', lineHeight: '1.6' }}>
                <div>Memoria: {cacheStats.memory_tiles} tiles</div>
                <div>Disco: {cacheStats.disk_tiles} tiles ({cacheStats.disk_size_mb.toFixed(1)} MB)</div>
              </div>
            ) : (
              <div style={{ fontSize: '11px', color: '#888' }}>No disponible</div>
            )}
            
            <div style={{ 
              display: 'flex', 
              gap: '8px', 
              marginTop: '12px'
            }}>
              <button
                onClick={handleClearCache}
                style={{
                  flex: 1,
                  padding: '6px 12px',
                  background: 'rgba(239, 68, 68, 0.2)',
                  border: '1px solid rgba(239, 68, 68, 0.5)',
                  borderRadius: '6px',
                  color: '#ef4444',
                  fontSize: '11px',
                  cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
                onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(239, 68, 68, 0.3)'}
                onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(239, 68, 68, 0.2)'}
              >
                🗑️ Limpiar
              </button>
              
              <button
                onClick={handlePrefetch}
                style={{
                  flex: 1,
                  padding: '6px 12px',
                  background: 'rgba(59, 130, 246, 0.2)',
                  border: '1px solid rgba(59, 130, 246, 0.5)',
                  borderRadius: '6px',
                  color: '#3b82f6',
                  fontSize: '11px',
                  cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
                onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(59, 130, 246, 0.3)'}
                onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(59, 130, 246, 0.2)'}
              >
                📥 Pre-fetch
              </button>
            </div>
          </div>
          
          {/* Info */}
          <div style={{
            fontSize: '10px',
            color: '#666',
            lineHeight: '1.4',
            paddingTop: '8px',
            borderTop: '1px solid rgba(255,255,255,0.1)'
          }}>
            Fuentes: SRTM, Copernicus GLO-30, OpenTopography
          </div>
        </div>
      )}
    </div>
  )
}

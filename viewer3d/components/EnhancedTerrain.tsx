/**
 * Enhanced Terrain Component
 * 
 * Integra TerrainEngine con datos DEM reales del backend
 */

import { useEffect, useRef, useState } from 'react'
import { useThree } from '@react-three/fiber'
import * as THREE from 'three'
import { TerrainEngineAdvanced, type DEMData } from '../engines/TerrainEngineAdvanced'
import { terrainDataService } from '../services/TerrainDataService'
import { loggers } from '@/core/Logger'

interface EnhancedTerrainProps {
  location?: { lat: number, lon: number } | null
  enabled?: boolean
  radius?: number  // Radio en grados alrededor de la ubicación
  resolution?: number  // Resolución del heightmap
  exaggeration?: number  // Factor de exageración vertical
  enableLOD?: boolean
  enableHydrography?: boolean
  onLoadingChange?: (loading: boolean) => void
}

export default function EnhancedTerrain({
  location,
  enabled = true,
  radius = 0.05,  // ~5.5 km
  resolution = 256,
  exaggeration = 1.5,
  enableLOD = true,
  enableHydrography = false,
  onLoadingChange
}: EnhancedTerrainProps) {
  const { scene } = useThree()
  const terrainEngineRef = useRef<TerrainEngineAdvanced | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  useEffect(() => {
    if (!enabled || !location) {
      // Limpiar terreno si está deshabilitado o no hay ubicación
      if (terrainEngineRef.current) {
        terrainEngineRef.current.dispose()
        terrainEngineRef.current = null
      }
      return
    }
    
    // Inicializar TerrainEngine
    if (!terrainEngineRef.current) {
      terrainEngineRef.current = new TerrainEngineAdvanced(scene, {
        segments: resolution,
        exaggeration,
        enableLOD,
        enableHydrography,
        erosionStrength: 0.3,
        multiScaleDetail: true,
        directionalBias: { x: 0.8, y: 1.3 },
        microDetailStrength: 0.5,
        atmosphericFog: true,
        anomalyStrength: 0.2
      })
      
      loggers.engine.info('TerrainEngineAdvanced inicializado con mejoras geométricas')
    }
    
    // Cargar datos de terreno
    loadTerrainData()
    
    return () => {
      // Cleanup
      if (terrainEngineRef.current) {
        terrainEngineRef.current.dispose()
        terrainEngineRef.current = null
      }
    }
  }, [location, enabled, radius, resolution, exaggeration, enableLOD, enableHydrography, scene])
  
  const loadTerrainData = async () => {
    if (!location || !terrainEngineRef.current) return
    
    setIsLoading(true)
    setError(null)
    
    // Notificar al padre que estamos cargando
    if (onLoadingChange) {
      onLoadingChange(true)
    }
    
    try {
      loggers.engine.info('Cargando datos de terreno...', {
        lat: location.lat,
        lon: location.lon,
        radius
      })
      
      // Calcular bounds
      const latMin = location.lat - radius
      const latMax = location.lat + radius
      const lonMin = location.lon - radius
      const lonMax = location.lon + radius
      
      // Obtener datos del backend
      const terrainData = await terrainDataService.getTerrainData(
        latMin,
        latMax,
        lonMin,
        lonMax,
        resolution
      )
      
      // Convertir a Float32Array
      const elevationArray = terrainDataService.convertToFloat32Array(terrainData.data)
      
      // Crear DEMData
      const demData: DEMData = {
        width: terrainData.data_shape[1],
        height: terrainData.data_shape[0],
        data: elevationArray,
        bounds: {
          minLat: terrainData.bounds.minLat,
          maxLat: terrainData.bounds.maxLat,
          minLon: terrainData.bounds.minLon,
          maxLon: terrainData.bounds.maxLon
        },
        resolution: terrainData.resolution,
        minElevation: terrainData.elevation_range[0],
        maxElevation: terrainData.elevation_range[1]
      }
      
      // Cargar en TerrainEngine
      await terrainEngineRef.current.loadDEM(elevationArray, demData.bounds)
      
      // Generar terreno
      terrainEngineRef.current.generateTerrain()
      
      loggers.engine.info('Terreno generado exitosamente', {
        source: terrainData.source,
        elevationRange: terrainData.elevation_range,
        resolution: terrainData.resolution
      })
      
      setIsLoading(false)
      
      // Notificar al padre que terminamos de cargar
      if (onLoadingChange) {
        onLoadingChange(false)
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error desconocido'
      loggers.engine.error('Error cargando terreno:', errorMessage)
      setError(errorMessage)
      setIsLoading(false)
      
      // Notificar al padre que terminamos (con error)
      if (onLoadingChange) {
        onLoadingChange(false)
      }
    }
  }
  
  // Este componente no renderiza nada directamente
  // TerrainEngine agrega el mesh a la escena
  return null
}

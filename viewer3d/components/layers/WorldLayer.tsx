/**
 * WorldLayer - Capa de mundo (terreno, biomas, tiempo)
 * Responsabilidad: Gestionar el entorno físico del mundo
 */

'use client'

import { useMemo } from 'react'
import ProceduralTerrain from '../ProceduralTerrain'
import { useBiomeSystem } from '@/hooks/useBiomeSystem'

interface WorldLayerProps {
  location: { lat: number; lon: number } | null
  isDay: boolean
  showTerrain: boolean
}

export default function WorldLayer({ 
  location, 
  isDay,
  showTerrain 
}: WorldLayerProps) {
  const { biome, isIceBiome } = useBiomeSystem(location, isDay)
  
  // Configuración del terreno según bioma
  const terrainConfig = useMemo(() => {
    switch (biome.type) {
      case 'ice':
        return {
          color: '#e8f4f8',
          roughness: 0.9,
          metalness: 0.1
        }
      case 'desert':
        return {
          color: '#d4a574',
          roughness: 0.95,
          metalness: 0.0
        }
      case 'volcanic':
        return {
          color: '#4a4a4a',
          roughness: 0.8,
          metalness: 0.2
        }
      default:
        return {
          color: '#8b7355',
          roughness: 0.9,
          metalness: 0.0
        }
    }
  }, [biome.type])
  
  if (!showTerrain || !location) return null
  
  return (
    <group name="world-layer">
      <ProceduralTerrain
        location={location}
        size={100}
        segments={64}
        heightScale={isIceBiome ? 8 : 12}
        color={terrainConfig.color}
        roughness={terrainConfig.roughness}
        metalness={terrainConfig.metalness}
      />
    </group>
  )
}

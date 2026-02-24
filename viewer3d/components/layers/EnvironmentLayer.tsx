'use client'

/**
 * EnvironmentLayer - Terreno, Agua, Vegetación
 * 
 * Responsabilidades:
 * - Terreno 3D (ProceduralTerrain, EnhancedTerrain)
 * - Vegetación (Tree3DModel, Rock3DModel)
 * - Biomas y ambiente
 * 
 * LAZY LOADING: Solo se carga cuando se necesita
 */

import { Suspense } from 'react'
import ProceduralTerrain from '../ProceduralTerrain'
import EnhancedTerrain from '../EnhancedTerrain'
import Tree3DModel, { type TreeType } from '../Tree3DModel'
import Rock3DModel from '../Rock3DModel'

interface EnvironmentLayerProps {
  location?: { lat: number; lon: number } | null
  enhancedTerrainEnabled?: boolean
  terrainExaggeration?: number
  terrainLOD?: boolean
  children?: React.ReactNode
}

export default function EnvironmentLayer({
  location,
  enhancedTerrainEnabled = false,
  terrainExaggeration = 1.5,
  terrainLOD = true,
  children
}: EnvironmentLayerProps) {
  return (
    <Suspense fallback={null}>
      <group name="environment-layer">
        {/* Terreno mejorado con DEM real */}
        {enhancedTerrainEnabled && location && (
          <EnhancedTerrain
            location={location}
            enabled={enhancedTerrainEnabled}
            radius={0.05}
            resolution={256}
            exaggeration={terrainExaggeration}
            enableLOD={terrainLOD}
          />
        )}

        {/* Contenido adicional (vegetación, etc.) */}
        {children}
      </group>
    </Suspense>
  )
}

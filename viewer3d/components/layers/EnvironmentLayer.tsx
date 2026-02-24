'use client'

/**
 * EnvironmentLayer - Terreno, Agua, Vegetación, Cielo
 * 
 * Responsabilidades:
 * - Terreno procedural (VolcanicTerrain, IceTerrain)
 * - Sistema de agua
 * - Vegetación dinámica (árboles, flores, rocas)
 * - Cielo y ambiente
 * - Iluminación base
 * 
 * Lazy-loaded después de CoreEngine listo
 * Se monta cuando: Scene lista + GPU detectada OK
 */

import { useMemo, useRef } from 'react'
import * as THREE from 'three'

import VolcanicTerrain from '../VolcanicTerrain'
import IceTerrain from '../IceTerrain'
import EnhancedTerrain from '../EnhancedTerrain'
import MilkyWayBackground from '../MilkyWayBackground'
import Stars from '../Stars'
import Tree3DModel from '../Tree3DModel'
import Rock3DModel from '../Rock3DModel'
import { 
  LightingSystem,
  EnvironmentSystem
} from '@/utils/lazy-systems'
import { detectBiome, getSkyColorForBiome, getFogColorForBiome } from '@/utils/biome-detector'

interface EnvironmentLayerProps {
  location?: { lat: number; lon: number } | null
  isDay: boolean
  showTerrain: boolean
  showVegetation: boolean
  enhancedTerrainEnabled?: boolean
  terrainExaggeration?: number
  terrainLOD?: boolean
  weatherState?: { storm?: boolean; rainHeavy?: boolean; lightning?: boolean }
  solarDirection?: { x: number; y: number; z: number }
  onTerrainLoadingChange?: (loading: boolean) => void
}

export default function EnvironmentLayer({
  location,
  isDay,
  showTerrain = true,
  showVegetation = true,
  enhancedTerrainEnabled = false,
  terrainExaggeration = 1.5,
  terrainLOD = true,
  weatherState = {},
  solarDirection = { x: 0, y: 1, z: 0 },
  onTerrainLoadingChange
}: EnvironmentLayerProps) {
  const terrainRef = useRef<THREE.Mesh>(null)

  // Detectar bioma basado en ubicación
  const biome = useMemo(() => {
    if (!location) return {
      type: 'default' as const,
      name: 'Genérico',
      description: '',
      temperature: 20,
      humidity: 50
    }
    return detectBiome(location.lat, location.lon)
  }, [location?.lat, location?.lon])

  const isIceBiome = biome.type === 'ice'

  // Colores dinámicos según bioma
  const skyColor = useMemo(() => getSkyColorForBiome(biome.type, isDay), [biome.type, isDay])
  const fogColor = useMemo(() => getFogColorForBiome(biome.type), [biome.type])

  // Oscuridad por tormenta
  const stormDarkness = useMemo(() => {
    if (!weatherState) return 0
    return weatherState.storm || weatherState.lightning ? 0.7 :
           weatherState.rainHeavy ? 0.5 : 0
  }, [weatherState])

  return (
    <group name="environment-layer">
      {/* Iluminación cinematográfica - adaptada al bioma */}
      <LightingSystem
        biomeType={biome.type}
        solarDirection={solarDirection}
        enableShadows={true}
        sunIntensity={2.5}
        hemisphereIntensity={1.2}
      />

      {/* Sistema de entorno (cielo, niebla, agua) */}
      <EnvironmentSystem
        isDay={isDay}
        skyColor={skyColor}
        fogColor={fogColor}
        stormDarkness={stormDarkness}
        fogDensity={isIceBiome ? 0.012 : 0.008}
        showWater={!isIceBiome}
        waterPosition={[0, -0.5, 0]}
        waterSize={150}
        waterColor="#1e3a5f"
      />

      {/* Terreno - adaptado al bioma */}
      {showTerrain && (
        isIceBiome ? (
          <IceTerrain location={location} ref={terrainRef} />
        ) : (
          <VolcanicTerrain location={location} ref={terrainRef} />
        )
      )}

      {/* Terreno mejorado con DEM real - opcional */}
      {enhancedTerrainEnabled && (
        <EnhancedTerrain
          location={location}
          enabled={enhancedTerrainEnabled}
          radius={0.05}
          resolution={256}
          exaggeration={terrainExaggeration}
          enableLOD={terrainLOD}
          enableHydrography={false}
          onLoadingChange={onTerrainLoadingChange}
        />
      )}

      {/* Grid sutil para referencia - OCULTO */}
      <gridHelper
        args={[200, 100, '#3a3a3a', '#2a2a2a']}
        position={[0, 0.01, 0]}
        visible={false}
      />

      {/* Vegetación dinámica según ubicación */}
      {showVegetation && (
        <EnvironmentElements location={location} />
      )}

      {/* Fondo - siempre en globo, nunca en modelo */}
      {/* <MilkyWayBackground />
      <Stars /> */}
    </group>
  )
}

/**
 * EnvironmentElements - Elementos decorativos dinámicos según ubicación
 */
function EnvironmentElements({
  location
}: {
  location?: { lat: number; lon: number } | null
}) {
  const seed = useMemo(() => {
    if (!location) return 0
    return Math.floor(location.lat * 1000 + location.lon * 1000)
  }, [location?.lat, location?.lon])

  const biome = useMemo(() => {
    if (!location) return 'temperate'
    const absLat = Math.abs(location.lat)
    if (absLat < 10) return 'tropical'
    if (absLat > 20 && absLat < 35) return 'desert'
    if (absLat > 60) return 'arctic'
    return 'temperate'
  }, [location])

  const elements = useMemo(() => {
    const random = (index: number) => {
      const x = Math.sin(seed + index * 12.9898) * 43758.5453
      return x - Math.floor(x)
    }

    const counts: Record<string, Record<string, number>> = {
      tropical: { trees: 15, bushes: 20, rocks: 10, palms: 8, flowers: 25 },
      temperate: { trees: 12, bushes: 15, rocks: 15, logs: 5, flowers: 15 },
      desert: { trees: 3, bushes: 5, rocks: 25, cacti: 12, crystals: 8 },
      arctic: { trees: 5, bushes: 8, rocks: 30, crystals: 5, flowers: 5 }
    }

    const count = counts[biome] || counts.temperate
    const items: any[] = []
    let index = 0

    // Generar árboles
    for (let i = 0; i < count.trees; i++) {
      const angle = random(index++) * Math.PI * 2
      const radius = 15 + random(index++) * 30
      const x = Math.cos(angle) * radius + (random(index++) - 0.5) * 10
      const z = Math.sin(angle) * radius + (random(index++) - 0.5) * 10
      const heightInMeters = 2 + random(index++) * 8
      const treeTypeRandom = random(index++)
      let treeType: 'default' | 'tree1' | 'tree2' | 'tree3' = 'default'
      if (treeTypeRandom < 0.25) treeType = 'default'
      else if (treeTypeRandom < 0.5) treeType = 'tree1'
      else if (treeTypeRandom < 0.75) treeType = 'tree2'
      else treeType = 'tree3'
      items.push({
        type: 'tree',
        x,
        z,
        heightInMeters,
        rotation: random(index++) * Math.PI * 2,
        treeType
      })
    }

    // Generar rocas
    for (let i = 0; i < count.rocks; i++) {
      const angle = random(index++) * Math.PI * 2
      const radius = 12 + random(index++) * 35
      const x = Math.cos(angle) * radius + (random(index++) - 0.5) * 10
      const z = Math.sin(angle) * radius + (random(index++) - 0.5) * 10
      const scale = 0.2 + random(index++) * 0.6
      items.push({
        type: 'rock',
        x,
        z,
        scale,
        rotation: random(index++) * Math.PI * 2
      })
    }

    return items
  }, [seed, biome])

  return (
    <group name="environment-elements">
      {elements.map((item, i) => {
        if (item.type === 'tree') {
          return (
            <Tree3DModel
              key={`tree-${i}`}
              position={[item.x, 0, item.z]}
              scale={item.heightInMeters * 0.05}
              rotation={item.rotation}
              treeType={item.treeType}
            />
          )
        }
        if (item.type === 'rock') {
          return (
            <Rock3DModel
              key={`rock-${i}`}
              position={[item.x, 0, item.z]}
              scale={item.scale * 0.5}
              rotation={item.rotation}
            />
          )
        }
        return null
      })}
    </group>
  )
}

'use client'

import { useState, useMemo } from 'react'
import Tree3DModel from './Tree3DModel'
import Rock3DModel from './Rock3DModel'
import SelectableObject from './SelectableObject'
import { useObjectSelection } from './ObjectSelectionContext'

// ─── Movable wrappers ────────────────────────────────────────────────────────

function MovableTree({ id, initialPosition, scale, rotation, treeType }: {
  id: string; initialPosition: [number, number, number]; scale: number; rotation: number; treeType: any
}) {
  const [pos, setPos] = useState<[number, number, number]>(initialPosition)
  return (
    <SelectableObject id={id} position={pos} onMove={setPos}>
      <Tree3DModel position={[0, 0, 0]} scale={scale} rotation={rotation} treeType={treeType} />
    </SelectableObject>
  )
}

function MovableRock({ id, initialPosition, scale, rotation }: {
  id: string; initialPosition: [number, number, number]; scale: number; rotation: number
}) {
  const [pos, setPos] = useState<[number, number, number]>(initialPosition)
  return (
    <SelectableObject id={id} position={pos} onMove={setPos}>
      <Rock3DModel position={[0, 0, 0]} scale={scale} rotation={rotation} />
    </SelectableObject>
  )
}

// ─── Wrapper que lee blockMoved dentro del ObjectSelectionProvider ────────────

export function EnvironmentElementsWithTrees({ location }: { location?: { lat: number; lon: number } | null }) {
  const { blockMoved } = useObjectSelection()
  return <EnvironmentElements location={location} treeMultiplier={blockMoved ? 3 : 1} />
}

// ─── Generador procedural principal ──────────────────────────────────────────

export default function EnvironmentElements({
  location,
  treeMultiplier = 1
}: {
  location?: { lat: number; lon: number } | null
  treeMultiplier?: number
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
      tropical:  { trees: 15, bushes: 20, rocks: 10, palms: 8,  flowers: 25 },
      temperate: { trees: 12, bushes: 15, rocks: 15, logs: 5,   flowers: 15 },
      desert:    { trees: 3,  bushes: 5,  rocks: 25, cacti: 12, crystals: 8 },
      arctic:    { trees: 5,  bushes: 8,  rocks: 30, crystals: 5, flowers: 5 }
    }
    const count = counts[biome] || counts.temperate
    const items: any[] = []
    let index = 0

    // Zonas ocupadas: [x, z, radioExclusión]
    // Estructura de Puma Punku en [8, -8], radio 12
    const occupied: Array<[number, number, number]> = [[8, -8, 12]]

    const isTooClose = (x: number, z: number): boolean => {
      for (const [ox, oz, r] of occupied) {
        if (Math.sqrt((x - ox) ** 2 + (z - oz) ** 2) < r) return true
      }
      return false
    }

    // Árboles — los extra van en radio exterior (≥35) para no chocar con la estructura
    for (let i = 0; i < count.trees * treeMultiplier; i++) {
      const isExtra = i >= count.trees
      let x = 0, z = 0, attempts = 0
      do {
        const angle = random(index++) * Math.PI * 2
        const minR = isExtra ? 35 : 15
        const radius = minR + random(index++) * 25
        x = Math.cos(angle) * radius + (random(index++) - 0.5) * 8
        z = Math.sin(angle) * radius + (random(index++) - 0.5) * 8
        attempts++
      } while (isTooClose(x, z) && attempts < 8)

      const heightInMeters = 2 + random(index++) * 8
      const tr = random(index++)
      const treeType = tr < 0.25 ? 'default' : tr < 0.5 ? 'tree1' : tr < 0.75 ? 'tree2' : 'tree3'
      items.push({ type: 'tree', x, z, heightInMeters, rotation: random(index++) * Math.PI * 2, treeType })
      occupied.push([x, z, 4])
    }

    // Arbustos
    for (let i = 0; i < count.bushes; i++) {
      const angle = random(index++) * Math.PI * 2
      const radius = 10 + random(index++) * 35
      items.push({ type: 'bush', x: Math.cos(angle) * radius + (random(index++) - 0.5) * 8, z: Math.sin(angle) * radius + (random(index++) - 0.5) * 8, scale: 0.3 + random(index++) * 0.5 })
    }

    // Rocas
    for (let i = 0; i < count.rocks; i++) {
      const angle = random(index++) * Math.PI * 2
      const radius = 12 + random(index++) * 35
      items.push({ type: 'rock', x: Math.cos(angle) * radius + (random(index++) - 0.5) * 10, z: Math.sin(angle) * radius + (random(index++) - 0.5) * 10, scale: 0.2 + random(index++) * 0.6, rotation: random(index++) * Math.PI * 2 })
    }

    // Palmeras (tropical)
    if (biome === 'tropical' && count.palms) {
      for (let i = 0; i < count.palms; i++) {
        const angle = random(index++) * Math.PI * 2
        const radius = 18 + random(index++) * 25
        items.push({ type: 'palm', x: Math.cos(angle) * radius, z: Math.sin(angle) * radius, height: 2.5 + random(index++) * 1.5 })
      }
    }

    // Cactus (desert)
    if (biome === 'desert' && count.cacti) {
      for (let i = 0; i < count.cacti; i++) {
        const angle = random(index++) * Math.PI * 2
        const radius = 15 + random(index++) * 30
        items.push({ type: 'cactus', x: Math.cos(angle) * radius, z: Math.sin(angle) * radius, height: 1.0 + random(index++) * 2.0 })
      }
    }

    // Troncos (temperate)
    if (biome === 'temperate' && count.logs) {
      for (let i = 0; i < count.logs; i++) {
        const angle = random(index++) * Math.PI * 2
        const radius = 20 + random(index++) * 25
        items.push({ type: 'log', x: Math.cos(angle) * radius, z: Math.sin(angle) * radius, rotation: random(index++) * Math.PI * 2 })
      }
    }

    // Flores
    if (count.flowers) {
      for (let i = 0; i < count.flowers; i++) {
        const angle = random(index++) * Math.PI * 2
        const radius = 8 + random(index++) * 35
        items.push({ type: 'flower', x: Math.cos(angle) * radius + (random(index++) - 0.5) * 5, z: Math.sin(angle) * radius + (random(index++) - 0.5) * 5, scale: 0.1 + random(index++) * 0.15, colorIndex: Math.floor(random(index++) * 4) })
      }
    }

    // Cristales
    if (count.crystals) {
      for (let i = 0; i < count.crystals; i++) {
        const angle = random(index++) * Math.PI * 2
        const radius = 20 + random(index++) * 25
        items.push({ type: 'crystal', x: Math.cos(angle) * radius, z: Math.sin(angle) * radius, scale: 0.3 + random(index++) * 0.5, rotation: random(index++) * Math.PI })
      }
    }

    return items
  }, [seed, biome, treeMultiplier])

  const flowerColors = ['#ff6b9d', '#ffd93d', '#a8e6cf', '#c7b3ff']

  return (
    <group>
      {elements.map((item, i) => {
        switch (item.type) {
          case 'tree':
            return (
              <MovableTree key={`tree-${seed}-${i}`} id={`tree-${seed}-${i}`}
                initialPosition={[item.x, 0, item.z]} scale={item.heightInMeters * 0.05}
                rotation={item.rotation} treeType={item.treeType} />
            )
          case 'rock':
            return (
              <MovableRock key={`rock-${seed}-${i}`} id={`rock-${seed}-${i}`}
                initialPosition={[item.x, 0, item.z]} scale={item.scale * 0.5} rotation={item.rotation} />
            )
          case 'flower':
            return (
              <group key={`flower-${i}`} position={[item.x, 0, item.z]}>
                <mesh position={[0, item.scale * 2, 0]}>
                  <cylinderGeometry args={[0.02, 0.02, item.scale * 4, 4]} />
                  <meshStandardMaterial color="#2d5016" />
                </mesh>
                <mesh position={[0, item.scale * 4, 0]} castShadow>
                  <sphereGeometry args={[item.scale, 6, 6]} />
                  <meshStandardMaterial color={flowerColors[item.colorIndex]} emissive={flowerColors[item.colorIndex]} emissiveIntensity={0.2} />
                </mesh>
              </group>
            )
          case 'crystal':
            return (
              <mesh key={`crystal-${i}`} position={[item.x, item.scale * 0.8, item.z]} rotation={[0, item.rotation, 0]} castShadow receiveShadow>
                <coneGeometry args={[item.scale * 0.5, item.scale * 1.5, 6]} />
                <meshStandardMaterial color="#88ccff" metalness={0.3} roughness={0.2} transparent opacity={0.8} emissive="#88ccff" emissiveIntensity={0.3} />
              </mesh>
            )
          default:
            return null
        }
      })}
    </group>
  )
}

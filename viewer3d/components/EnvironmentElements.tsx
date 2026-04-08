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

function MovableRock({ id, initialPosition, scale, rotation, canCollect, onCollect }: {
  id: string; initialPosition: [number, number, number]; scale: number; rotation: number
  canCollect?: boolean
  onCollect?: () => void
}) {
  const [pos, setPos] = useState<[number, number, number]>(initialPosition)
  const [collected, setCollected] = useState(false)

  if (collected) return null

  return (
    <SelectableObject id={id} position={pos} onMove={setPos}>
      <group
        onClick={(e) => {
          if (!canCollect || !onCollect) return
          e.stopPropagation()
          setCollected(true)
          onCollect()
        }}
        onPointerOver={() => { if (canCollect) document.body.style.cursor = 'pointer' }}
        onPointerOut={() => { document.body.style.cursor = 'default' }}
      >
        <Rock3DModel position={[0, 0, 0]} scale={scale} rotation={rotation} />
      </group>
    </SelectableObject>
  )
}

// ─── Wrapper que lee blockMoved dentro del ObjectSelectionProvider ────────────

export function EnvironmentElementsWithTrees({ location, rockInInventory, onRockCollect }: { 
  location?: { lat: number; lon: number } | null
  rockInInventory?: boolean
  onRockCollect?: () => void
}) {
  const { blockMoved } = useObjectSelection()
  return <EnvironmentElements location={location} treeMultiplier={blockMoved ? 3 : 1} rockInInventory={rockInInventory} onRockCollect={onRockCollect} />
}

// ─── Generador procedural principal ──────────────────────────────────────────

export default function EnvironmentElements({
  location,
  treeMultiplier = 1,
  rockInInventory = false,
  onRockCollect
}: {
  location?: { lat: number; lon: number } | null
  treeMultiplier?: number
  rockInInventory?: boolean
  onRockCollect?: () => void
}) {
  const seed = useMemo(() => {
    if (!location) return 0
    return Math.floor(location.lat * 1000 + location.lon * 1000)
  }, [location?.lat, location?.lon])

  const biome = useMemo(() => {
    if (!location) return 'temperate'
    const absLat = Math.abs(location.lat)
    
    // Altiplano - Lago Titicaca
    if (absLat > 15.5 && absLat < 16.5 && location.lon > -70 && location.lon < -68.5) {
      return 'altiplano'
    }
    
    if (absLat < 10) return 'tropical'
    if (absLat > 20 && absLat < 35) return 'desert'
    if (absLat > 60) return 'arctic'
    return 'temperate'
  }, [location])

  // Detectar si estamos en Puma Punku
  const isPumaPunku = useMemo(() => {
    if (!location) return false
    const lat = location.lat
    const lon = location.lon
    // Coordenadas de Puma Punku: -16.5596°S, -68.6788°W
    return Math.abs(lat + 16.5596) < 0.05 && Math.abs(lon + 68.6788) < 0.05
  }, [location])

  const elements = useMemo(() => {
    const random = (index: number) => {
      const x = Math.sin(seed + index * 12.9898) * 43758.5453
      return x - Math.floor(x)
    }

    const counts: Record<string, Record<string, number>> = {
      tropical:  { trees: 25, bushes: 20, rocks: 10, palms: 8 },
      temperate: { trees: 25, bushes: 15, rocks: 15, logs: 5 },
      altiplano: { trees: 5, bushes: 25, rocks: 20, logs: 3 }, // Reducido para Titicaca
      desert:    { trees: 15, bushes: 5,  rocks: 25, cacti: 12, crystals: 8 },  // Menos árboles en desierto
      arctic:    { trees: 20, bushes: 8,  rocks: 30, crystals: 5 }
    }
    const count = counts[biome] || counts.temperate
    const items: any[] = []
    let index = 0

    // Zonas ocupadas: [x, z, radioExclusión]
    const occupied: Array<[number, number, number]> = []
    
    // Detectar si estamos en Giza
    const isGiza = location && Math.abs(location.lat - 29.9792) < 0.05 && Math.abs(location.lon - 31.1342) < 0.05
    
    // Detectar si estamos en Teotihuacán
    const isTeotihuacan = location && Math.abs(location.lat - 19.6925) < 0.05 && Math.abs(location.lon - (-98.8438)) < 0.05
    
    // Detectar si estamos en Veracruz (Tres Zapotes)
    const isVeracruz = location && Math.abs(location.lat - 18.4667) < 0.05 && Math.abs(location.lon - (-95.4500)) < 0.05
    
    // Detectar si estamos en Isla de Pascua
    const isEasterIsland = location && Math.abs(location.lat - (-27.1254)) < 0.05 && Math.abs(location.lon - (-109.2778)) < 0.05
    
    // Reducir árboles en sitios específicos
    if ((isTeotihuacan || isVeracruz || isEasterIsland) && count.trees) {
      count.trees = isEasterIsland ? 5 : 15
    }
    
    // En Puma Punku: proteger estructura y Viracocha con radios GRANDES
    if (isPumaPunku) {
      occupied.push([8, -8, 25])       // Estructura principal (radio muy amplio)
      occupied.push([13.634, 0.83, 15]) // Viracocha (radio amplio)
      occupied.push([70, 60, 20])       // Puerta del Sol (radio amplio)
      // Proteger todos los bloques dispersos
      occupied.push([-12, 8, 8])
      occupied.push([15, -6, 8])
      occupied.push([-8, -18, 8])
      occupied.push([20, 14, 8])
      occupied.push([-20, -10, 8])
      occupied.push([6, 22, 8])
      occupied.push([-16, 18, 8])
      occupied.push([10, -22, 8])
    }
    
    // En Giza: proteger pirámide y esfinge con radios MUY GRANDES
    if (isGiza) {
      occupied.push([0, 0, 80])        // Gran Pirámide (radio enorme)
      occupied.push([100, 50, 30])     // Esfinge (radio grande)
      occupied.push([0, 0, 50])        // Templo del Valle (bajo la pirámide)
    }

    const isTooClose = (x: number, z: number): boolean => {
      for (const [ox, oz, r] of occupied) {
        if (Math.sqrt((x - ox) ** 2 + (z - oz) ** 2) < r) return true
      }
      return false
    }

    // Árboles — los extra van en radio exterior (≥45 en Puma Punku) para no chocar con la estructura
    // En Puma Punku: FORZAR solo 1 árbol sin importar treeMultiplier
    const finalTreeCount = isPumaPunku ? count.trees : count.trees * treeMultiplier
    for (let i = 0; i < finalTreeCount; i++) {
      const isExtra = i >= count.trees
      let x = 0, z = 0, attempts = 0
      
      if (isPumaPunku) {
        // En Puma Punku: posiciones aleatorias respetando zonas de exclusión
        do {
          const angle = random(index++) * Math.PI * 2
          const radius = 30 + random(index++) * 40  // Entre 30 y 70 metros
          x = Math.cos(angle) * radius + (random(index++) - 0.5) * 10
          z = Math.sin(angle) * radius + (random(index++) - 0.5) * 10
          attempts++
        } while (isTooClose(x, z) && attempts < 50)
      } else {
        do {
          const angle = random(index++) * Math.PI * 2
          const minR = isExtra ? 35 : 15
          const radius = minR + random(index++) * 25
          x = Math.cos(angle) * radius + (random(index++) - 0.5) * 8
          z = Math.sin(angle) * radius + (random(index++) - 0.5) * 8
          attempts++
        } while (isTooClose(x, z) && attempts < 20)
      }
      
      console.log(`[EnvironmentElements] Árbol generado: x=${x.toFixed(2)}, z=${z.toFixed(2)}, isPumaPunku=${isPumaPunku}`)

      // Seleccionar tipo de árbol: distribuir equitativamente entre los 3 tipos finales
      // Altura: mínimo 2.2m (mitad de Viracocha), máximo 5m
      const heightInMeters = 2.2 + random(index++) * 2.8  // Entre 2.2m y 5m
      const tr = random(index++)
      let treeType: any
      // En todas las escenas: distribuir equitativamente entre los 3 tipos
      if (tr < 0.33) treeType = 'default'     // tree_new.glb (33%)
      else if (tr < 0.66) treeType = 'tree1'  // tree_new2.glb (33%)
      else treeType = 'tree2'                 // tree_new3.glb (33%)
      
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

    // Cristales
    if (count.crystals) {
      for (let i = 0; i < count.crystals; i++) {
        const angle = random(index++) * Math.PI * 2
        const radius = 20 + random(index++) * 25
        items.push({ type: 'crystal', x: Math.cos(angle) * radius, z: Math.sin(angle) * radius, scale: 0.3 + random(index++) * 0.5, rotation: random(index++) * Math.PI })
      }
    }

    return items
  }, [seed, biome, treeMultiplier, isPumaPunku])

  return (
    <group>
      {elements.map((item, i) => {
        switch (item.type) {
          case 'tree':
            // Escala basada en altura (heightInMeters ya está entre 2.2 y 5)
            const treeY = 0
            const treeScale = item.heightInMeters * 0.1  // Aumentado de 0.05 a 0.1 para hacerlos más grandes
            return (
              <MovableTree key={`tree-${seed}-${i}`} id={`tree-${seed}-${i}`}
                initialPosition={[item.x, treeY, item.z]} scale={treeScale}
                rotation={item.rotation} treeType={item.treeType} />
            )
          case 'rock':
            return (
              <MovableRock key={`rock-${seed}-${i}`} id={`rock-${seed}-${i}`}
                initialPosition={[item.x, 0, item.z]} scale={item.scale * 0.5} rotation={item.rotation}
                canCollect={!rockInInventory}
                onCollect={onRockCollect}
              />
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

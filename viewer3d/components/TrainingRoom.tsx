'use client'

import { useRef, useState, useEffect, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Sky, Stars, PerspectiveCamera, OrbitControls } from '@react-three/drei'
import * as THREE from 'three'
import IceTerrain from './IceTerrain'
import IceLighting from './IceLighting'
import WalkableAvatar from './WalkableAvatar'
import Rock3DModel from './Rock3DModel'
import Tree3DModel from './Tree3DModel'
import SelectableObject from './SelectableObject'
import TerrainClickReceiver from './TerrainClickReceiver'
import SnowParticles from './SnowParticles'
// DroppableItem — sistema unificado de items en el suelo (mismo que el juego principal)
import DroppableItem from './DroppableItem'
import { ObjectSelectionProvider } from './ObjectSelectionContext'
import { loadPlayerState } from '@/types/player'
import { getAssetPath } from '@/lib/paths'
import AmbientAudio from './AmbientAudio'
import { getClimateAudio } from '../systems/ClimateAudioSystem'
import { getProceduralAudio } from '../systems/ProceduralAudio'
import { loadGameSettings } from '@/types/gameSettings'
import ProximityHelpDetector, { type HelpZone } from './ProximityHelpDetector'
import HelpBubble, { type HelpTip } from './HelpBubble'
import helpTipsData from '@/data/helpTips.json'

/** Wrapper que lazy-imports HelpBubble para evitar SSR issues */
function HelpBubbleWrapper({ tip }: { tip: HelpTip }) {
  return <HelpBubble tip={tip} />
}

// Store compartido para comunicar 3D → UI (inventario)
// Exportamos las funciones para que TrainingUI pueda suscribirse
type InventoryListener = (items: InventoryEntry[]) => void
export interface InventoryEntry {
  id: string
  modelPath: string
  itemName: string
  scale: number
  rotation: number
}

const inventoryListeners: Set<InventoryListener> = new Set()
let currentInventory: InventoryEntry[] = []

export function subscribeInventory(listener: InventoryListener) {
  inventoryListeners.add(listener)
  // Emitir estado actual al suscribirse
  listener(currentInventory)
  return () => { inventoryListeners.delete(listener) }
}

function setInventory(items: InventoryEntry[]) {
  currentInventory = items
  inventoryListeners.forEach(fn => fn(items))
}

// Store compartido para drop requests (UI → 3D)
type DropRequestListener = (itemId: string) => void
const dropListeners: Set<DropRequestListener> = new Set()

export function subscribeDropRequest(listener: DropRequestListener) {
  dropListeners.add(listener)
  return () => { dropListeners.delete(listener) }
}

export function requestDrop(itemId: string) {
  dropListeners.forEach(fn => fn(itemId))
}

// Store compartido para Oracle scan (3D → UI)
type ScanListener = (entity: { name: string, desc: string } | null) => void
const scanListeners: Set<ScanListener> = new Set()

export function subscribeScan(listener: ScanListener) {
  scanListeners.add(listener)
  return () => { scanListeners.delete(listener) }
}

function emitScan(entity: { name: string, desc: string } | null) {
  scanListeners.forEach(fn => fn(entity))
}

// Store compartido para zona de ayuda más cercana (3D → UI)
type HelpZoneListener = (zone: HelpZone | null) => void
const helpZoneListeners: Set<HelpZoneListener> = new Set()

export function subscribeHelpZone(listener: HelpZoneListener) {
  helpZoneListeners.add(listener)
  return () => { helpZoneListeners.delete(listener) }
}

function emitHelpZone(zone: HelpZone | null) {
  helpZoneListeners.forEach(fn => fn(zone))
}
function TrainingScene() {
  const [playerShip, setPlayerShip] = useState<string>(getAssetPath('/ufo_1.glb'))
  const [abilityActive, setAbilityActive] = useState(false)
  const [abilityCooldown, setAbilityCooldown] = useState(false)
  const [scannedEntity, setScannedEntity] = useState<{ name: string, desc: string } | null>(null)

  // Emitir scan al UI
  useEffect(() => { emitScan(scannedEntity) }, [scannedEntity])
  const [audioEnabled, setAudioEnabled] = useState(false)
  const [playerPosition, setPlayerPosition] = useState<THREE.Vector3>(new THREE.Vector3(0, 0, 0))
  const avatarPositionRef = useRef<THREE.Vector3>(new THREE.Vector3(0, 0, 0))
  const terrainRef = useRef<THREE.Mesh>(null)

  // Estado inicial de las rocas y árboles
  const initialObjects = useMemo(() => {
    const items: any[] = []
    // 6 Árboles
    for (let i = 0; i < 6; i++) {
      const angle = (i / 6) * Math.PI * 2
      const radius = 20 + Math.random() * 5
      items.push({
        type: 'tree',
        id: `training-tree-${i}`,
        position: [Math.cos(angle) * radius, 0, Math.sin(angle) * radius] as [number, number, number],
        scale: 0.4 + Math.random() * 0.2,
        rotation: Math.random() * Math.PI * 2
      })
    }
    // 9 Rocas iniciales
    for (let i = 0; i < 9; i++) {
      const angle = (i / 9) * Math.PI * 2 + 0.3
      const radius = 12 + Math.random() * 4
      items.push({
        type: 'rock',
        id: `training-rock-init-${i}`,
        position: [Math.cos(angle) * radius, 0, Math.sin(angle) * radius] as [number, number, number],
        scale: 0.3 + Math.random() * 0.2,
        rotation: Math.random() * Math.PI * 2
      })
    }
    return items
  }, [])

  const [worldTrees] = useState(initialObjects.filter(o => o.type === 'tree'))
  const [worldRocks, setWorldRocks] = useState(initialObjects.filter(o => o.type === 'rock'))

  // Inventario: lista de rocas recogidas (pueden ser varias)
  const [inventory, setLocalInventory] = useState<InventoryEntry[]>([])

  // Rocas dropeadas (misma escala que la original)
  const [droppedRocks, setDroppedRocks] = useState<Array<{
    id: string
    position: [number, number, number]
    scale: number
    rotation: number
  }>>([])

  // Sincronizar inventario local con el store compartido
  useEffect(() => {
    setInventory(inventory)
  }, [inventory])

  // Suscribirse a drop requests desde la UI
  useEffect(() => {
    const unsub = subscribeDropRequest((itemId: string) => {
      // Encontrar el item en el inventario
      const item = inventory.find(i => i.id === itemId)
      if (!item) return

      // Quitar del inventario
      setLocalInventory(prev => prev.filter(i => i.id !== itemId))

      // Crear roca dropeada cerca del jugador con la MISMA escala original
      const dropId = `training-rock-dropped-${Date.now()}`
      setDroppedRocks(prev => [...prev, {
        id: dropId,
        position: [playerPosition.x + (Math.random() - 0.5) * 4, 1.5, playerPosition.z + (Math.random() - 0.5) * 4],
        scale: item.scale,
        rotation: item.rotation
      }])

      console.log(`✨ Roca soltada desde inventario (escala: ${item.scale.toFixed(2)}).`)
    })
    return unsub
  }, [inventory, playerPosition])


  useEffect(() => {
    const state = loadPlayerState()
    if (state?.ship?.model) {
      setPlayerShip(getAssetPath(state.ship.model))
    }

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.code === 'Space' && !abilityCooldown) {
        setAbilityActive(true)

        // Oracle (nave 4): escanear objeto más cercano
        const ufoNum = playerShip.includes('ufo_5') ? 5 : playerShip.includes('ufo_4') ? 4 : playerShip.includes('ufo_3') ? 3 : playerShip.includes('ufo_2') ? 2 : 1
        if (ufoNum === 4) {
          // Buscar el objeto más cercano al jugador
          const px = playerPosition.x, pz = playerPosition.z
          let closest = '', closestDist = Infinity
          worldTrees.forEach(t => {
            const dx = t.position[0] - px, dz = t.position[2] - pz
            const d = dx*dx + dz*dz
            if (d < closestDist) { closestDist = d; closest = 'Árbol' }
          })
          worldRocks.forEach(r => {
            const dx = r.position[0] - px, dz = r.position[2] - pz
            const d = dx*dx + dz*dz
            if (d < closestDist) { closestDist = d; closest = 'Roca' }
          })
          droppedRocks.forEach(r => {
            const dx = r.position[0] - px, dz = r.position[2] - pz
            const d = dx*dx + dz*dz
            if (d < closestDist) { closestDist = d; closest = 'Roca' }
          })

          const SCAN_DATA: Record<string, string> = {
            'Árbol': "Organismo vivo que conecta tres mundos: sus raíces penetran el inframundo, su tronco habita la tierra, y sus ramas tocan el cielo. Los antiguos lo consideraban el eje del cosmos — el axis mundi.",
            'Roca': "Fragmento de la corteza terrestre con millones de años de memoria geológica. Cada mineral en su interior registra las condiciones del planeta en el momento de su formación. La piedra no olvida."
          }

          if (closest && closestDist < 900) { // ~30m de radio
            setScannedEntity({ name: closest, desc: SCAN_DATA[closest] || '' })
          }

          setTimeout(() => {
            setAbilityActive(false)
            setScannedEntity(null)
            setAbilityCooldown(true)
            setTimeout(() => setAbilityCooldown(false), 3000)
          }, 2000)
        }
      }
    }
    const handleKeyUp = (e: KeyboardEvent) => {
      if (e.code === 'Space') {
        // Oracle maneja su propio timeout, las demás naves desactivan al soltar
        const ufoNum = playerShip.includes('ufo_4') ? 4 : 0
        if (ufoNum !== 4) setAbilityActive(false)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    window.addEventListener('keyup', handleKeyUp)
    return () => {
      window.removeEventListener('keydown', handleKeyDown)
      window.removeEventListener('keyup', handleKeyUp)
    }
  }, [playerShip, playerPosition, worldTrees, worldRocks, droppedRocks, abilityCooldown])

  // Sincronizar audio climático y volumen
  useEffect(() => {
    const climate = getClimateAudio()
    climate.initialize()
    // Activar viento y nieve procedural para la atmósfera (viento ligero)
    climate.updateWeather({ wind: 0.1, snow: 0.05 })
    
    const interval = setInterval(() => {
      const settings = loadGameSettings()
      if (settings?.audio?.masterVolume !== undefined) {
        const vol = settings.audio.masterVolume
        climate.setMasterVolume(vol)
        getProceduralAudio().setMasterVolume(vol)
      }
    }, 1000)
    
    return () => clearInterval(interval)
  }, [])

  // Habilitar audio procedural en interacción
  useEffect(() => {
    if (audioEnabled) return
    const enableAudio = async () => {
      try {
        await getProceduralAudio().enable()
        setAudioEnabled(true)
        console.log('🔊 Audio procedural habilitado')
      } catch (e) {
        console.warn('Error habilitando audio:', e)
      }
    }
    window.addEventListener('click', enableAudio)
    window.addEventListener('keydown', enableAudio)
    window.addEventListener('touchstart', enableAudio)
    return () => {
      window.removeEventListener('click', enableAudio)
      window.removeEventListener('keydown', enableAudio)
      window.removeEventListener('touchstart', enableAudio)
    }
  }, [audioEnabled])

  // Recoger roca del mundo (rocas iniciales) — guardar escala original
  const collectRock = (id: string) => {
    const rock = worldRocks.find(r => r.id === id)
    const originalScale = rock?.scale ?? 0.35
    const originalRotation = rock?.rotation ?? 0
    setWorldRocks(prev => prev.filter(r => r.id !== id))
    const newEntry: InventoryEntry = {
      id: `inv-rock-${Date.now()}-${Math.random().toString(36).substr(2,4)}`,
      modelPath: '/rock_blender.glb',
      itemName: 'Roca',
      scale: originalScale,
      rotation: originalRotation
    }
    setLocalInventory(prev => [...prev, newEntry])
    console.log(`🪨 Roca recogida → inventario (escala: ${originalScale.toFixed(2)}).`)
  }

  // Recoger roca dropeada (del piso) — preservar escala
  const collectDroppedRock = (dropId: string) => {
    const dropped = droppedRocks.find(r => r.id === dropId)
    const droppedScale = dropped?.scale ?? 0.35
    const droppedRotation = dropped?.rotation ?? 0
    setDroppedRocks(prev => prev.filter(r => r.id !== dropId))
    const newEntry: InventoryEntry = {
      id: `inv-rock-${Date.now()}-${Math.random().toString(36).substr(2,4)}`,
      modelPath: '/rock_blender.glb',
      itemName: 'Roca',
      scale: droppedScale,
      rotation: droppedRotation
    }
    setLocalInventory(prev => [...prev, newEntry])
    console.log(`🪨 Roca dropeada recogida → inventario (escala: ${droppedScale.toFixed(2)}).`)
  }


  return (
    <>
      <Sky sunPosition={[30, 40, 30]} />
      <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
      {/* Environment preset removido — cargaba dikhololo_night_1k.hdr externamente (falla en producción) */}
      {/* La iluminación la maneja IceLighting + ambientLight en la escena */}
      
      <IceLighting />
      <IceTerrain ref={terrainRef} location={{ lat: -75.2509, lon: 0.0714 }} />
      <SnowParticles />
      <AmbientAudio />

      {/* Avatar del Jugador */}
      <WalkableAvatar 
        modelPath={playerShip} 
        terrainRef={terrainRef} 
        initialPosition={[0, 10, 0]}
        abilityActive={abilityActive}
        onPositionChange={(pos) => {
          setPlayerPosition(pos)
          avatarPositionRef.current.copy(pos)
        }}
        currentUfo={
          playerShip.includes('ufo_5') ? 5 :
          playerShip.includes('ufo_4') ? 4 :
          playerShip.includes('ufo_3') ? 3 :
          playerShip.includes('ufo_2') ? 2 : 1
        }
      />

      {/* Sistema de ayuda por proximidad */}
      <ProximityHelpDetector
        zones={[
          // Rocas del mundo (clickeables para recoger)
          ...worldRocks.map(r => ({
            id: `help-rock-${r.id}`,
            position: r.position as [number, number, number],
            radius: 10,
            tip: (helpTipsData as any).rock,
          })),
          // Rocas dropeadas en el piso
          ...droppedRocks.map(r => ({
            id: `help-dropped-${r.id}`,
            position: r.position as [number, number, number],
            radius: 8,
            tip: (helpTipsData as any).droppedRock,
          })),
          // Árboles (movibles)
          ...worldTrees.map(t => ({
            id: `help-tree-${t.id}`,
            position: t.position as [number, number, number],
            radius: 12,
            tip: (helpTipsData as any).tree,
          })),
        ]}
        avatarPositionRef={avatarPositionRef}
        onNearestChange={emitHelpZone}
      />

      {/* Árboles (movibles con SelectableObject) */}
      {worldTrees.map((obj) => (
        <TrainingTree
          key={obj.id}
          obj={obj}
        />
      ))}

      {/* Rocas del mundo (clickeables para recoger - SIN SelectableObject) */}
      {worldRocks.map((obj) => (
        <CollectableRock
          key={obj.id}
          obj={obj}
          onCollect={() => collectRock(obj.id)}
        />
      ))}

      {/* Rocas dropeadas en el piso — usa DroppableItem (mismo sistema que el juego) */}
      {droppedRocks.map((rock) => (
        <DroppableItem
          key={rock.id}
          modelPath="/rock_blender.glb"
          position={[rock.position[0], 0, rock.position[2]]}
          onCollect={() => collectDroppedRock(rock.id)}
          scale={1.0}
          floatHeight={1.0}
          glowColor="#ffd700"
          itemName="Roca"
        />
      ))}

      <TerrainClickReceiver size={200} />
    </>
  )
}

/** Roca coleccionable: click directo sin SelectableObject (que interceptaba eventos) */
function CollectableRock({ obj, onCollect }: { obj: any, onCollect: () => void }) {
  const groupRef = useRef<THREE.Group>(null)
  const [hovered, setHovered] = useState(false)

  return (
    <group
      ref={groupRef}
      position={obj.position}
    >
      <Rock3DModel
        position={[0, 0, 0]}
        scale={obj.scale}
        rotation={obj.rotation}
      />
      {/* Esfera invisible grande para facilitar click — radio 2.5 unidades */}
      <mesh
        onClick={(e) => { e.stopPropagation(); onCollect() }}
        onPointerOver={(e) => { e.stopPropagation(); setHovered(true); document.body.style.cursor = 'pointer' }}
        onPointerOut={(e) => { e.stopPropagation(); setHovered(false); document.body.style.cursor = 'default' }}
      >
        <sphereGeometry args={[2.5, 8, 8]} />
        <meshBasicMaterial transparent opacity={0} />
      </mesh>
      {/* Glow visible para indicar que es interactivo */}
      <pointLight
        color={hovered ? '#ffd700' : '#ffaa44'}
        intensity={hovered ? 5 : 1.5}
        distance={8}
        position={[0, 0.5, 0]}
      />
      {/* Esfera wireframe hover para feedback visual */}
      {hovered && (
        <mesh position={[0, 0.3, 0]}>
          <sphereGeometry args={[1.5, 16, 16]} />
          <meshBasicMaterial
            color="#ffd700"
            wireframe
            transparent
            opacity={0.35}
          />
        </mesh>
      )}
    </group>
  )
}

/** Árbol decorativo: usa SelectableObject para poder moverlo */
function TrainingTree({ obj }: { obj: any }) {
  const [pos, setPos] = useState<[number, number, number]>(obj.position)
  const groupRef = useRef<THREE.Group>(null)

  // Efecto de viento para árboles
  useFrame((state) => {
    if (!groupRef.current) return
    const time = state.clock.getElapsedTime()
    groupRef.current.rotation.x = Math.sin(time * 0.5) * 0.02
    groupRef.current.rotation.z = Math.cos(time * 0.4) * 0.02
  })

  return (
    <SelectableObject 
      id={obj.id} 
      position={pos} 
      onMove={setPos}
    >
      <group ref={groupRef}>
        <Tree3DModel 
          position={[0, 0, 0]} 
          scale={obj.scale} 
          rotation={obj.rotation} 
          treeType="tree1" 
        />
      </group>
    </SelectableObject>
  )
}

export default function TrainingRoom() {
  const [nearestHelpZone, setNearestHelpZone] = useState<HelpZone | null>(null)

  useEffect(() => {
    const unsub = subscribeHelpZone(setNearestHelpZone)
    return unsub
  }, [])

  return (
    <div style={{ width: '100vw', height: '100vh', background: '#000000' }}>
      <ObjectSelectionProvider>
        <Canvas
          shadows
          camera={{ position: [0, 14, -14], fov: 60 }}
          dpr={[1, 2]}
          gl={{
            antialias: true,
            alpha: false,
            powerPreference: 'high-performance',
            toneMapping: THREE.ACESFilmicToneMapping,
            toneMappingExposure: 1.2
          }}
        >
          {/* Sin PerspectiveCamera duplicada — WalkableAvatar controla la cámara via useFrame */}
          <TrainingScene />
        </Canvas>
      </ObjectSelectionProvider>

      {/* HelpBubble — fuera del Canvas, sobre el HUD */}
      {nearestHelpZone && (
        <HelpBubbleWrapper tip={nearestHelpZone.tip} />
      )}
    </div>
  )
}

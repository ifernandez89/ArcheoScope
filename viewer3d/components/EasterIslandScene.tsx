'use client'

import { useRef, Suspense, useEffect, useMemo, useState } from 'react'
import { useGLTF, Html } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import { Vector3 } from 'three'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'
import EasterIslandDialogue from './EasterIslandDialogue'
import RanoKauVolcano, { type VolcanoState } from './RanoKauVolcano'
import { loadMissionState } from '@/types/missionState'
import Merkaba from './Merkaba'
import EnergySphere from './EnergySphere'
import CropCircle, { CropCirclePortal } from './CropCircle'
import Geoglyph from './Geoglyph'
import { isMissionCompleted } from '@/types/missionState'
import DroppableItem from './DroppableItem'

/**
 * Escena de Isla de Pascua (Rapa Nui)
 * Moai y Atlante enfrentados "charlando"
 * Modelos optimizados con compresión Draco
 * Sistema de diálogo sobre la red energética planetaria
 */

/**
 * 🔄 Loading placeholder para Isla de Pascua
 */
// Partículas de ceniza volcánica
function VolcanicAsh() {
  const COUNT = 300
  const meshRef = useRef<THREE.InstancedMesh>(null)
  const tempObj = useMemo(() => new THREE.Object3D(), [])
  const tempColor = useMemo(() => new THREE.Color(), [])

  // Posiciones iniciales aleatorias en el cielo
  const data = useMemo(() => Array.from({ length: COUNT }, () => ({
    x: (Math.random() - 0.5) * 120,
    y: 5 + Math.random() * 30,
    z: (Math.random() - 0.5) * 120,
    vy: -(0.5 + Math.random() * 1.5), // caída lenta
    vx: (Math.random() - 0.5) * 0.3,
    vz: (Math.random() - 0.5) * 0.3,
    size: 0.1 + Math.random() * 0.25,
  })), [])

  useFrame((_, delta) => {
    if (!meshRef.current) return
    for (let i = 0; i < COUNT; i++) {
      const p = data[i]
      p.y += p.vy * delta
      p.x += p.vx * delta
      p.z += p.vz * delta
      if (p.y < 0) { // reciclar cuando toca el suelo
        p.y = 20 + Math.random() * 20
        p.x = (Math.random() - 0.5) * 120
        p.z = (Math.random() - 0.5) * 120
      }
      tempObj.position.set(p.x, p.y, p.z)
      tempObj.scale.setScalar(p.size)
      tempObj.updateMatrix()
      meshRef.current.setMatrixAt(i, tempObj.matrix)
      const g = 0.3 + Math.random() * 0.2
      tempColor.setRGB(g, g, g)
      meshRef.current.setColorAt(i, tempColor)
    }
    meshRef.current.instanceMatrix.needsUpdate = true
    if (meshRef.current.instanceColor) meshRef.current.instanceColor.needsUpdate = true
  })

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, COUNT]}>
      <sphereGeometry args={[0.5, 4, 4]} />
      <meshBasicMaterial vertexColors transparent opacity={0.6} depthWrite={false} />
    </instancedMesh>
  )
}

function LoadingEasterIsland() {
  return (
    <Html center>
      <div style={{
        background: 'rgba(0, 0, 0, 0.8)',
        padding: '20px 40px',
        borderRadius: '12px',
        color: 'white',
        fontFamily: 'system-ui, sans-serif',
        textAlign: 'center',
        border: '2px solid rgba(255, 215, 0, 0.3)'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '10px' }}>🗿</div>
        <div>Cargando Isla de Pascua...</div>
      </div>
    </Html>
  )
}

interface EasterIslandSceneProps {
  avatarPositionRef?: React.RefObject<Vector3>
  volcanicEruption?: boolean
  onEruptionEnd?: () => void
  showJadeMask?: boolean
  jadeMaskCollected?: boolean
  onJadeMaskCollect?: () => void
  onMerkabaActivate?: () => void
  onTriggerEruption?: () => void
  skullInInventory?: boolean
  showSkull?: boolean
  skullDropPosition?: {x: number, z: number} | null
  onSkullCollect?: () => void
  merkabaMissionDone?: boolean
  onShipChange?: (ufoNumber: number) => void
  currentUfo?: number
  abilityActive?: boolean
  onObeliskActivate?: () => void
  tonatiuhInInventory?: boolean
  tonatiuhOnGround?: boolean
  tonatiuhDropPosition?: {x: number, z: number} | null
  onTonatiuhCollect?: () => void
  magnaBowlLentInInventory?: boolean
  magnaBowlOnGround?: boolean
  magnaBowlDropPosition?: {x: number, z: number} | null
  onMagnaBowlCollect?: () => void
}

export default function EasterIslandScene({ avatarPositionRef, volcanicEruption, onEruptionEnd, showJadeMask, jadeMaskCollected, onJadeMaskCollect, onMerkabaActivate, onTriggerEruption, skullInInventory, showSkull, skullDropPosition, onSkullCollect, merkabaMissionDone, onShipChange, currentUfo, abilityActive, onObeliskActivate, tonatiuhInInventory, tonatiuhOnGround, tonatiuhDropPosition, onTonatiuhCollect, magnaBowlLentInInventory, magnaBowlOnGround, magnaBowlDropPosition, onMagnaBowlCollect }: EasterIslandSceneProps) {
  return (
    <Suspense fallback={<LoadingEasterIsland />}>
      <EasterIslandSceneContent 
        avatarPositionRef={avatarPositionRef} 
        volcanicEruption={volcanicEruption} 
        onEruptionEnd={onEruptionEnd} 
        showJadeMask={showJadeMask} 
        jadeMaskCollected={jadeMaskCollected} 
        onJadeMaskCollect={onJadeMaskCollect} 
        onMerkabaActivate={onMerkabaActivate} 
        onTriggerEruption={onTriggerEruption}
        skullInInventory={skullInInventory}
        showSkull={showSkull}
        skullDropPosition={skullDropPosition}
        onSkullCollect={onSkullCollect}
        merkabaMissionDone={merkabaMissionDone}
        onShipChange={onShipChange}
        currentUfo={currentUfo}
        abilityActive={abilityActive}
        onObeliskActivate={onObeliskActivate}
        tonatiuhInInventory={tonatiuhInInventory}
        tonatiuhOnGround={tonatiuhOnGround}
        tonatiuhDropPosition={tonatiuhDropPosition}
        onTonatiuhCollect={onTonatiuhCollect}
        magnaBowlLentInInventory={magnaBowlLentInInventory}
        magnaBowlOnGround={magnaBowlOnGround}
        magnaBowlDropPosition={magnaBowlDropPosition}
        onMagnaBowlCollect={onMagnaBowlCollect}
      />
    </Suspense>
  )
}

function EasterIslandSceneContent({ 
  avatarPositionRef, 
  volcanicEruption, 
  onEruptionEnd, 
  showJadeMask, 
  jadeMaskCollected, 
  onJadeMaskCollect, 
  onMerkabaActivate, 
  onTriggerEruption,
  skullInInventory,
  showSkull,
  skullDropPosition,
  onSkullCollect,
  merkabaMissionDone,
  onShipChange,
  currentUfo,
  abilityActive,
  onObeliskActivate,
  tonatiuhInInventory,
  tonatiuhOnGround,
  tonatiuhDropPosition,
  onTonatiuhCollect,
  magnaBowlLentInInventory,
  magnaBowlOnGround,
  magnaBowlDropPosition,
  onMagnaBowlCollect
}: EasterIslandSceneProps) {
  const moaiModel = useGLTF(getAssetPath('/moai.glb'))
  const atlanteModel = useGLTF(getAssetPath('/atlante.glb'))
  const jadeMaskModel = useGLTF(getAssetPath('/jade_mask.glb'))
  const crystalSkullModel = useGLTF(getAssetPath('/crystal-skull.glb'))

  const [merkabaClickable, setMerkabaClickable] = useState(false)
  const [merkabaActive, setMerkabaActive] = useState(false)
  const [showEnergySphere, setShowEnergySphere] = useState(false)
  const [skullStolen, setSkullStolen] = useState(false)

  // Verificar si la misión está completa - lee de localStorage al montar o via prop
  const [missionDone, setMissionDone] = useState(false)
  useEffect(() => {
    if (merkabaActive || merkabaMissionDone || isMissionCompleted('easterIsland', 'activate_merkaba')) setMissionDone(true)
  }, [merkabaActive, merkabaMissionDone])

  useEffect(() => {
    const ms = loadMissionState()
    const pmDone = ms.sites.pumaPunku.missionsCompleted.length > 0
    const gizaDone = ms.sites.giza.missionsCompleted.length > 0
    const teoDone = ms.sites.teotihuacan.missionsCompleted.length > 0
    const verDone = (ms.sites.veracruz?.missionsCompleted?.length || 0) > 0
    const result = pmDone && gizaDone && teoDone && verDone
    setMerkabaClickable(result)

    if (ms.sites.easterIsland.missionsCompleted.includes('activate_merkaba')) {
      setMerkabaActive(true)
      setShowEnergySphere(true)
    }
  }, [])

  const volcanoState = useMemo<VolcanoState>(() => {
    // 'erupting' SOLO cuando el usuario activa la erupción volcánica manualmente
    if (volcanicEruption) return 'erupting'
    return 'dormant'
  }, [volcanicEruption])

  const moaiInstancedRef = useRef<THREE.InstancedMesh>(null)
  const atlanteInstancedRef = useRef<THREE.InstancedMesh>(null)

  const moaiData = useMemo(() => {
    let geometry: THREE.BufferGeometry | null = null
    let material: THREE.Material | null = null
    moaiModel.scene.traverse((child: any) => {
      if (child.isMesh && !geometry) {
        geometry = child.geometry
        material = child.material
      }
    })
    return { geometry, material }
  }, [moaiModel])

  const atlanteData = useMemo(() => {
    let geometry: THREE.BufferGeometry | null = null
    let material: THREE.Material | null = null
    atlanteModel.scene.traverse((child: any) => {
      if (child.isMesh && !geometry) {
        geometry = child.geometry
        material = child.material
      }
    })
    return { geometry, material }
  }, [atlanteModel])

  const npcState = useRef({
    moai: [
      { pos: [ -4, 3, 0 ], rot: [ 0, Math.PI / 4 - Math.PI / 6, 0 ], curY: 3, origY: 3 },
      { pos: [ 0, 3, -29 ], rot: [ 0, Math.PI, 0 ], curY: 3, origY: 3 },
      { pos: [ 29, 3, 0 ], rot: [ 0, -Math.PI / 2, 0 ], curY: 3, origY: 3 }
    ],
    atlante: [
      { pos: [ 4, 2, 0 ], rot: [ Math.PI / 2, 0, -Math.PI / 4 ], curY: 2, origY: 2 },
      { pos: [ 0, 2, 29 ], rot: [ Math.PI / 2, 0, 0 ], curY: 2, origY: 2 },
      { pos: [ -29, 2, 0 ], rot: [ Math.PI / 2, 0, Math.PI / 2 ], curY: 2, origY: 2 }
    ]
  })

  const sceneGroupRef = useRef<THREE.Group>(null)
  const shakeTimeRef = useRef(0)
  const eruptionTimerRef = useRef(0)
  const redirectedRef = useRef(false)
  const skullGroupRef = useRef<THREE.Group>(null)
  const tempObj = useMemo(() => new THREE.Object3D(), [])

  // Inicializar matrices de los NPCs al montar (evita frame inicial en posición incorrecta)
  useEffect(() => {
    if (!moaiInstancedRef.current || !atlanteInstancedRef.current) return
    const t = new THREE.Object3D()
    npcState.current.moai.forEach((m, i) => {
      t.position.set(m.pos[0], m.origY, m.pos[2])
      t.rotation.set(m.rot[0], m.rot[1], m.rot[2])
      t.scale.setScalar(5)
      t.updateMatrix()
      moaiInstancedRef.current!.setMatrixAt(i, t.matrix)
    })
    npcState.current.atlante.forEach((a, i) => {
      t.position.set(a.pos[0], a.origY, a.pos[2])
      t.rotation.set(a.rot[0], a.rot[1], a.rot[2])
      t.scale.setScalar(5)
      t.updateMatrix()
      atlanteInstancedRef.current!.setMatrixAt(i, t.matrix)
    })
    moaiInstancedRef.current.instanceMatrix.needsUpdate = true
    atlanteInstancedRef.current.instanceMatrix.needsUpdate = true
  }, [moaiInstancedRef.current, atlanteInstancedRef.current])

  useFrame(({ clock }, delta) => {
    if (skullGroupRef.current) {
      skullGroupRef.current.position.y = 16 + Math.sin(clock.elapsedTime * 2) * 0.5
      skullGroupRef.current.rotation.y += delta * 0.5
    }

    if (!sceneGroupRef.current || !moaiInstancedRef.current || !atlanteInstancedRef.current) return

    if (volcanicEruption) {
      shakeTimeRef.current += delta
      sceneGroupRef.current.position.x = Math.sin(shakeTimeRef.current * 19) * 0.06
      sceneGroupRef.current.position.z = Math.cos(shakeTimeRef.current * 13) * 0.06

      const sinkSpeed = 0.8 * delta
      npcState.current.moai.forEach((m, i) => {
        const target = m.origY - 1.5
        if (m.curY > target) m.curY = Math.max(target, m.curY - sinkSpeed)
        tempObj.position.set(m.pos[0], m.curY, m.pos[2])
        tempObj.rotation.set(m.rot[0], m.rot[1], m.rot[2])
        tempObj.scale.setScalar(5)
        tempObj.updateMatrix()
        moaiInstancedRef.current!.setMatrixAt(i, tempObj.matrix)
      })
      npcState.current.atlante.forEach((a, i) => {
        const target = a.origY - 1.5
        if (a.curY > target) a.curY = Math.max(target, a.curY - sinkSpeed)
        tempObj.position.set(a.pos[0], a.curY, a.pos[2])
        tempObj.rotation.set(a.rot[0], a.rot[1], a.rot[2])
        tempObj.scale.setScalar(5)
        tempObj.updateMatrix()
        atlanteInstancedRef.current!.setMatrixAt(i, tempObj.matrix)
      })

      eruptionTimerRef.current += delta
      if (eruptionTimerRef.current > 8 && !redirectedRef.current && onEruptionEnd) {
        redirectedRef.current = true
        onEruptionEnd()
      }
    } else {
      sceneGroupRef.current.position.x *= 0.8
      sceneGroupRef.current.position.z *= 0.8

      // Solo actualizar matrices si los NPCs no están en su posición original
      const needsReset = npcState.current.moai.some(m => Math.abs(m.curY - m.origY) > 0.01)
      if (!needsReset) return

      npcState.current.moai.forEach((m, i) => {
        m.curY = m.origY
        tempObj.position.set(m.pos[0], m.curY, m.pos[2])
        tempObj.rotation.set(m.rot[0], m.rot[1], m.rot[2])
        tempObj.scale.setScalar(5)
        tempObj.updateMatrix()
        moaiInstancedRef.current!.setMatrixAt(i, tempObj.matrix)
      })
      npcState.current.atlante.forEach((a, i) => {
        a.curY = a.origY
        tempObj.position.set(a.pos[0], a.curY, a.pos[2])
        tempObj.rotation.set(a.rot[0], a.rot[1], a.rot[2])
        tempObj.scale.setScalar(5)
        tempObj.updateMatrix()
        atlanteInstancedRef.current!.setMatrixAt(i, tempObj.matrix)
      })
    }

    moaiInstancedRef.current.instanceMatrix.needsUpdate = true
    atlanteInstancedRef.current.instanceMatrix.needsUpdate = true
  })

  useEffect(() => {
    import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
      const harmonia = getHarmoniaMundi()
      if (harmonia.isEnabled()) harmonia.activateArchitecture('easter-island')
    })
    return () => {
      import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
        getHarmoniaMundi().deactivateArchitecture('easter-island')
      })
    }
  }, [])

  const moaiPosition = useMemo(() => new Vector3(-4, 3, 0), [])
  const atlantePosition = useMemo(() => new Vector3(4, 2, 0), [])

  return (
    <group ref={sceneGroupRef}>
      {volcanicEruption && <VolcanicAsh />}
      
      {moaiData.geometry && (
        <instancedMesh ref={moaiInstancedRef} args={[moaiData.geometry, moaiData.material as unknown as THREE.Material, 3]} frustumCulled={false} />
      )}
      {atlanteData.geometry && (
        <instancedMesh ref={atlanteInstancedRef} args={[atlanteData.geometry, atlanteData.material as unknown as THREE.Material, 3]} frustumCulled={false} />
      )}

      <EasterIslandDialogue
        moaiPosition={moaiPosition}
        atlantePosition={atlantePosition}
        enabled={!showEnergySphere}
      />
      
      <RanoKauVolcano state={volcanoState} />

      <Merkaba
        position={[0, 12, 0]}
        size={1.5}
        color="#ffd700"
        speed={merkabaActive ? 0 : 0.4}
        clickable={false}
        onActivate={() => {
          setMerkabaActive(true)
          setShowEnergySphere(true)
          if (onMerkabaActivate) onMerkabaActivate()
        }}
      />

      {/* Detector de pulso Titan para activar Merkaba */}
      <TitanPulseDetector
        position={[0, 12, 0]}
        radius={25}
        currentUfo={currentUfo}
        abilityActive={abilityActive}
        avatarPositionRef={avatarPositionRef}
        enabled={merkabaClickable && !merkabaActive}
        onActivate={() => {
          setMerkabaActive(true)
          setShowEnergySphere(true)
          if (onMerkabaActivate) onMerkabaActivate()
        }}
      />

      <EnergySphere position={[0, 8, 0]} size={2} visible={showEnergySphere} />

      {/* 🐳 Geoglifo: Ballena de Nazca — esquina noreste (opuesta al volcán en suroeste) */}
      <Geoglyph svgPath="/geoglyphs/ballena.svg" position={[55, 1, -55]} size={18} />

      {/* 💠 Crop Circle: Hilbert - Nave 4 Oracle (Isla de Pascua) */}
      {/* Volcán en [-55, 0, 55] → crop circle en esquina opuesta */}
      <CropCircle 
        type="hilbert" 
        position={[55, 1, -55]} 
        scale={1.5} 
        visible={missionDone} 
      />
      <CropCirclePortal
        position={[55, 1, -55]}
        ufoNumber={4}
        missionDone={missionDone}
        avatarPositionRef={avatarPositionRef}
        onShipChange={onShipChange}
        currentUfo={currentUfo}
      />

      {/* Obelisco Lanzón Chavín — aparece al completar las 5 misiones */}
      {missionDone && (
        <Suspense fallback={null}>
          <LanzonObelisk
            avatarPositionRef={avatarPositionRef}
            onActivate={onObeliskActivate}
          />
        </Suspense>
      )}

      {showJadeMask && !jadeMaskCollected && (
        <group
          position={[15, 0.5, -10]}
          onClick={(e) => { e.stopPropagation(); if (onJadeMaskCollect) onJadeMaskCollect() }}
          onPointerOver={() => { document.body.style.cursor = 'pointer' }}
          onPointerOut={() => { document.body.style.cursor = 'default' }}
        >
          <primitive object={jadeMaskModel.scene} scale={2} />
          <mesh>
            <boxGeometry args={[3, 3, 3]} />
            <meshBasicMaterial color="#00ff88" wireframe transparent opacity={0.3} />
          </mesh>
          <pointLight color="#00ff88" intensity={2} distance={8} />
        </group>
      )}

      {!skullInInventory && (showSkull ? true : true) && crystalSkullModel.scene && (
        <group
          ref={skullGroupRef}
          position={showSkull && skullDropPosition ? [skullDropPosition.x, 16, skullDropPosition.z] : [-55, 16, 55]}
          onClick={(e) => {
            e.stopPropagation()
            if (onSkullCollect) onSkullCollect()
          }}
          onPointerOver={() => { document.body.style.cursor = 'pointer' }}
          onPointerOut={() => { document.body.style.cursor = 'default' }}
        >
          <primitive object={crystalSkullModel.scene} scale={1.5} />
          <mesh>
            <boxGeometry args={[2, 2, 2]} />
            <meshBasicMaterial color="#ff00ff" wireframe transparent opacity={0.3} />
          </mesh>
          <pointLight color="#ff00ff" intensity={2} distance={10} />
        </group>
      )}

      {/* 🌞 Tonatiuh soltado en el suelo */}
      {!tonatiuhInInventory && tonatiuhOnGround && tonatiuhDropPosition && (
        <DroppableItem
          modelPath="/tonatiuh_aztec_sun.glb"
          position={[tonatiuhDropPosition.x, 0, tonatiuhDropPosition.z]}
          onCollect={onTonatiuhCollect}
          scale={1.5}
          floatHeight={1.5}
          glowColor="#ffaa00"
          itemName="Tonatiuh"
        />
      )}

      {/* 🏺 Fuente Magna prestada — soltada en el suelo */}
      {!magnaBowlLentInInventory && magnaBowlOnGround && magnaBowlDropPosition && (
        <DroppableItem
          modelPath="/magna_bowl.glb"
          position={[magnaBowlDropPosition.x, 0, magnaBowlDropPosition.z]}
          onCollect={onMagnaBowlCollect}
          scale={1.5}
          floatHeight={1.5}
          glowColor="#4488ff"
          itemName="Fuente Magna"
        />
      )}

      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={0.8} />
    </group>
  )
}

// ─── TITAN PULSE DETECTOR ─────────────────────────────────────────────────────
// Solo Titan (nave 5) con habilidad activa y en proximidad puede activar el objeto
function TitanPulseDetector({
  position,
  radius,
  currentUfo,
  abilityActive,
  avatarPositionRef,
  enabled,
  onActivate
}: {
  position: [number, number, number]
  radius: number
  currentUfo?: number
  abilityActive?: boolean
  avatarPositionRef?: React.RefObject<THREE.Vector3>
  enabled: boolean
  onActivate: () => void
}) {
  const firedRef = useRef(false)

  useEffect(() => {
    if (!enabled || firedRef.current) return
    if (currentUfo !== 5 || !abilityActive) return
    const av = avatarPositionRef?.current
    if (!av) return
    const dx = av.x - position[0]
    const dz = av.z - position[2]
    if (dx * dx + dz * dz < radius * radius) {
      firedRef.current = true
      onActivate()
      console.log('💥 Titan pulse activó el Merkaba!')
    }
  }, [abilityActive])

  return null
}

// ─── LANZÓN CHAVÍN — Obelisco sagrado ────────────────────────────────────────
// Aparece en la esquina noreste (opuesta al volcán en [-55,2,55])
// Solo visible al completar las 5 misiones
// Se activa por PROXIMIDAD del avatar — no por click
function LanzonObelisk({ avatarPositionRef, onActivate }: {
  avatarPositionRef?: React.RefObject<THREE.Vector3>
  onActivate?: () => void
}) {
  const { scene } = useGLTF(getAssetPath('/lanzon_chavin.glb'))
  const groupRef = useRef<THREE.Group>(null)
  const activatedRef = useRef(false)
  const OBELISK_POS = [55, 0, -55] as const
  const RADIUS = 15  // metros de proximidad

  const { scale, yOffset } = useMemo(() => {
    const box = new THREE.Box3().setFromObject(scene)
    const size = box.getSize(new THREE.Vector3())
    const sc = 12 / size.y
    const yo = -box.min.y * sc
    return { scale: sc, yOffset: yo }
  }, [scene])

  const cloned = useMemo(() => scene.clone(true), [scene])

  const lightRef = useRef<THREE.PointLight>(null)
  const [nearPlayer, setNearPlayer] = useState(false)

  useFrame(({ clock }) => {
    // Pulso de luz — más intenso cuando el avatar está cerca
    if (lightRef.current) {
      lightRef.current.intensity = (nearPlayer ? 3 : 0.5) + Math.sin(clock.elapsedTime * 0.8) * 0.3
    }

    // Detección de proximidad
    if (!avatarPositionRef?.current || !onActivate || activatedRef.current) return
    const av = avatarPositionRef.current
    const dx = av.x - OBELISK_POS[0]
    const dz = av.z - OBELISK_POS[2]
    const distSq = dx * dx + dz * dz
    const isNear = distSq < RADIUS * RADIUS

    if (isNear !== nearPlayer) setNearPlayer(isNear)

    if (isNear) {
      activatedRef.current = true
      console.log('🏛️ Obelisco activado — viajando a Göbekli Tepe')
      setTimeout(() => onActivate(), 1500) // pequeño delay dramático
    }
  })

  return (
    <group ref={groupRef} position={[OBELISK_POS[0], yOffset, OBELISK_POS[2]]}>
      <primitive object={cloned} scale={scale} />
      <pointLight ref={lightRef} color="#ffcc44" intensity={0.5} distance={40} position={[0, 6, 0]} />
      {/* Anillo de proximidad visible */}
      {nearPlayer && (
        <mesh position={[0, 0.1, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <ringGeometry args={[RADIUS * 0.8, RADIUS, 48]} />
          <meshBasicMaterial color="#ffcc44" transparent opacity={0.15} depthWrite={false} />
        </mesh>
      )}
    </group>
  )
}

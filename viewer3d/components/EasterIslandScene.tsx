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
}

export default function EasterIslandScene({ avatarPositionRef, volcanicEruption, onEruptionEnd, showJadeMask, jadeMaskCollected, onJadeMaskCollect, onMerkabaActivate }: EasterIslandSceneProps) {
  return (
    <Suspense fallback={<LoadingEasterIsland />}>
      <EasterIslandSceneContent avatarPositionRef={avatarPositionRef} volcanicEruption={volcanicEruption} onEruptionEnd={onEruptionEnd} showJadeMask={showJadeMask} jadeMaskCollected={jadeMaskCollected} onJadeMaskCollect={onJadeMaskCollect} onMerkabaActivate={onMerkabaActivate} />
    </Suspense>
  )
}

function EasterIslandSceneContent({ avatarPositionRef, volcanicEruption, onEruptionEnd, showJadeMask, jadeMaskCollected, onJadeMaskCollect, onMerkabaActivate }: EasterIslandSceneProps) {
  const moaiModel = useGLTF(getAssetPath('/moai.glb'))
  const atlanteModel = useGLTF(getAssetPath('/atlante.glb'))
  const jadeMaskModel = useGLTF(getAssetPath('/jade_mask.glb'))

  const [merkabaClickable, setMerkabaClickable] = useState(false)
  const [merkabaActive, setMerkabaActive] = useState(false)
  const [showEnergySphere, setShowEnergySphere] = useState(false)

  useEffect(() => {
    const ms = loadMissionState()
    const pmDone = ms.sites.pumaPunku.missionsCompleted.length > 0
    const gizaDone = ms.sites.giza.missionsCompleted.length > 0
    const teoDone = ms.sites.teotihuacan.missionsCompleted.length > 0
    const verDone = ms.sites.veracruz?.missionsCompleted?.length > 0
    const result = pmDone && gizaDone && teoDone && verDone
    setMerkabaClickable(result)

    if (ms.sites.easterIsland.missionsCompleted.includes('activate_merkaba')) {
      setMerkabaActive(true)
      setShowEnergySphere(true)
    }
  }, [])

  const volcanoState = useMemo<VolcanoState>(() => {
    if (volcanicEruption) return 'erupting'
    const ms = loadMissionState()
    const total = ms.stats.totalMissionsCompleted
    if (total >= 3) return 'erupting'
    if (total >= 1) return 'active'
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
      { pos: [ 4, 2, 0 ], rot: [ 0, 0, 0 ], curY: 2, origY: 2 },
      { pos: [ 0, 2, 29 ], rot: [ 0, 0, 0 ], curY: 2, origY: 2 },
      { pos: [ -29, 2, 0 ], rot: [ 0, Math.PI / 2, 0 ], curY: 2, origY: 2 }
    ]
  })

  const sceneGroupRef = useRef<THREE.Group>(null)
  const shakeTimeRef = useRef(0)
  const eruptionTimerRef = useRef(0)
  const redirectedRef = useRef(false)
  const tempObj = useMemo(() => new THREE.Object3D(), [])

  useFrame((_, delta) => {
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
        clickable={merkabaClickable}
        onActivate={() => {
          setMerkabaActive(true)
          setShowEnergySphere(true)
          if (onMerkabaActivate) onMerkabaActivate()
        }}
      />

      <EnergySphere position={[0, 8, 0]} size={2} visible={showEnergySphere} />

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

      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={0.8} />
    </group>
  )
}

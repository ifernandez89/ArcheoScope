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

  // Chequear si las 4 misiones específicas están completas → merkaba clickeable
  // Se recalcula cada vez que el componente se monta (al entrar a la escena)
  const [merkabaClickable, setMerkabaClickable] = useState(false)
  useEffect(() => {
    const ms = loadMissionState()
    const pmDone = ms.sites.pumaPunku.missionsCompleted.length > 0
    const gizaDone = ms.sites.giza.missionsCompleted.length > 0
    const teoDone = ms.sites.teotihuacan.missionsCompleted.length > 0
    const verDone = ms.sites.veracruz?.missionsCompleted?.length > 0
    const result = pmDone && gizaDone && teoDone && verDone
    setMerkabaClickable(result)
    console.log('Merkaba clickable:', result, { pmDone, gizaDone, teoDone, verDone })
  }, [])

  // Esfera energética aparece al activar el Merkaba
  const [showEnergySphere, setShowEnergySphere] = useState(false)

  const moaiNorth    = useMemo(() => moaiModel.scene.clone(true),    [moaiModel.scene])
  const moaiEast     = useMemo(() => moaiModel.scene.clone(true),    [moaiModel.scene])
  const atlanteSouth = useMemo(() => atlanteModel.scene.clone(true), [atlanteModel.scene])
  const atlanteWest  = useMemo(() => atlanteModel.scene.clone(true), [atlanteModel.scene])

  // Estado del volcán: erupción climática tiene prioridad sobre misiones
  const volcanoState = useMemo<VolcanoState>(() => {
    if (volcanicEruption) return 'erupting'
    const ms = loadMissionState()
    const total = ms.stats.totalMissionsCompleted
    if (total >= 3) return 'erupting'
    if (total >= 1) return 'active'
    return 'dormant'
  }, [volcanicEruption])

  // Ref del grupo raíz para el temblor
  const sceneGroupRef = useRef<THREE.Group>(null)
  const shakeTimeRef = useRef(0)
  // Refs de los NPCs para hundirlos
  const moaiCentralRef   = useRef<THREE.Group>(null)
  const atlanteCentralRef = useRef<THREE.Group>(null)
  const moaiNorthRef     = useRef<THREE.Group>(null)
  const moaiEastRef      = useRef<THREE.Group>(null)
  const atlanteSouthRef  = useRef<THREE.Group>(null)
  const atlanteWestRef   = useRef<THREE.Group>(null)
  // Timer para redirect
  const eruptionTimerRef = useRef(0)
  const redirectedRef    = useRef(false)

  // Posiciones Y originales de cada NPC (no tocar si no hay erupción)
  const ORIGINAL_Y: Record<string, number> = {
    moaiCentral: 3, atlanteCentral: 2,
    moaiNorth: 3, atlanteSouth: 2, moaiEast: 3, atlanteWest: 2
  }

  useFrame((_, delta) => {
    if (!sceneGroupRef.current) return

    if (volcanicEruption) {
      shakeTimeRef.current += delta
      const intensity = 0.06
      sceneGroupRef.current.position.x = Math.sin(shakeTimeRef.current * 19) * intensity
      sceneGroupRef.current.position.z = Math.cos(shakeTimeRef.current * 13) * intensity
      sceneGroupRef.current.position.y = 0
      sceneGroupRef.current.rotation.set(0, 0, 0)

      // Hundir NPCs desde su Y original hacia -1.5 relativo
      const sinkSpeed = 0.8 * delta
      const entries: [React.RefObject<THREE.Group>, number][] = [
        [moaiCentralRef,    ORIGINAL_Y.moaiCentral    - 1.5],
        [atlanteCentralRef, ORIGINAL_Y.atlanteCentral - 1.5],
        [moaiNorthRef,      ORIGINAL_Y.moaiNorth      - 1.5],
        [moaiEastRef,       ORIGINAL_Y.moaiEast       - 1.5],
        [atlanteSouthRef,   ORIGINAL_Y.atlanteSouth   - 1.5],
        [atlanteWestRef,    ORIGINAL_Y.atlanteWest    - 1.5],
      ]
      for (const [ref, target] of entries) {
        if (ref.current && ref.current.position.y > target) {
          ref.current.position.y = Math.max(target, ref.current.position.y - sinkSpeed)
        }
      }

      eruptionTimerRef.current += delta
      if (eruptionTimerRef.current > 8 && !redirectedRef.current && onEruptionEnd) {
        redirectedRef.current = true
        onEruptionEnd()
      }
    } else {
      sceneGroupRef.current.position.x *= 0.8
      sceneGroupRef.current.position.z *= 0.8
      sceneGroupRef.current.position.y = 0
      sceneGroupRef.current.rotation.set(0, 0, 0)
      eruptionTimerRef.current = 0
      redirectedRef.current = false
      // Restaurar NPCs a su Y original exacta
      const entries: [React.RefObject<THREE.Group>, number][] = [
        [moaiCentralRef,    ORIGINAL_Y.moaiCentral],
        [atlanteCentralRef, ORIGINAL_Y.atlanteCentral],
        [moaiNorthRef,      ORIGINAL_Y.moaiNorth],
        [moaiEastRef,       ORIGINAL_Y.moaiEast],
        [atlanteSouthRef,   ORIGINAL_Y.atlanteSouth],
        [atlanteWestRef,    ORIGINAL_Y.atlanteWest],
      ]
      for (const [ref, target] of entries) {
        if (ref.current) {
          ref.current.position.y = target // restaurar inmediatamente sin animación
        }
      }
    }
  })
  
  // 🎼 Activar arquitectura de Isla de Pascua
  useEffect(() => {
    import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
      const harmonia = getHarmoniaMundi()
      if (harmonia.isEnabled()) {
        harmonia.activateArchitecture('easter-island')
        console.log('🏛️ Arquitectura de Isla de Pascua activada')
      }
    })
    
    return () => {
      import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
        const harmonia = getHarmoniaMundi()
        harmonia.deactivateArchitecture('easter-island')
      })
    }
  }, [])
  
  // Posiciones para el sistema de diálogo (constantes, no recrear cada render)
  const moaiPosition = useMemo(() => new Vector3(-4, 3, 0), [])
  const atlantePosition = useMemo(() => new Vector3(4, 2, 0), [])
  
  // Radio del borde - 1 metro adentro del límite visible
  const BORDER = 29

  return (
    <group ref={sceneGroupRef}>
      {/* Ceniza volcánica - partículas grises durante erupción */}
      {volcanicEruption && <VolcanicAsh />}
      {/* Moai central - posición y rotación ORIGINALES */}
      <group ref={moaiCentralRef} position={[-4, 3, 0]} rotation={[0, Math.PI / 4 - Math.PI / 6, 0]}>
        <primitive object={moaiModel.scene} scale={5} />
      </group>
      
      {/* Atlante central - posición y rotación ORIGINALES */}
      <group ref={atlanteCentralRef} position={[4, 2, 0]} rotation={[0, 0, 0]}>
        <primitive object={atlanteModel.scene} scale={5} />
      </group>

      {/* BORDE NORTE: Moai mirando al sur (hacia el centro) */}
      <group ref={moaiNorthRef} position={[0, 3, -BORDER]} rotation={[0, Math.PI, 0]}>
        <primitive object={moaiNorth} scale={5} />
      </group>

      {/* BORDE SUR: Atlante mirando al norte (hacia el centro) */}
      <group ref={atlanteSouthRef} position={[0, 2, BORDER]} rotation={[0, 0, 0]}>
        <primitive object={atlanteSouth} scale={5} />
      </group>

      {/* BORDE ESTE: Moai mirando al oeste (hacia el centro) */}
      <group ref={moaiEastRef} position={[BORDER, 3, 0]} rotation={[0, -Math.PI / 2, 0]}>
        <primitive object={moaiEast} scale={5} />
      </group>

      {/* BORDE OESTE: Atlante mirando al este (hacia el centro) */}
      <group ref={atlanteWestRef} position={[-BORDER, 2, 0]} rotation={[0, Math.PI / 2, 0]}>
        <primitive object={atlanteWest} scale={5} />
      </group>
      
      {/* Sistema de diálogo entre Moai y Atlante - se detiene al activar Merkaba */}
      <EasterIslandDialogue
        moaiPosition={moaiPosition}
        atlantePosition={atlantePosition}
        enabled={!showEnergySphere}
      />
      
      {/* 🌋 Volcán Rano Kau - suroeste, igual que el real */}
      <RanoKauVolcano state={volcanoState} />

      {/* ✡️ Merkaba - estrella tetraédrica girando en el centro */}
      <Merkaba
        position={[0, 12, 0]}
        size={1.5}
        color="#ffd700"
        speed={0.4}
        clickable={merkabaClickable}
        onActivate={() => {
          setShowEnergySphere(true)
          if (onMerkabaActivate) onMerkabaActivate()
        }}
      />

      {/* Esfera energética de estabilización - aparece al completar las 5 misiones */}
      <EnergySphere position={[0, 8, 0]} size={2} visible={showEnergySphere} />

      {/* Jade Mask - visible cuando la mision de la cueva esta activa */}
      {showJadeMask && !jadeMaskCollected && (
        <group
          position={[15, 0.5, -10]}
          onClick={(e) => { e.stopPropagation(); if (onJadeMaskCollect) onJadeMaskCollect() }}
          onPointerOver={() => { document.body.style.cursor = 'pointer' }}
          onPointerOut={() => { document.body.style.cursor = 'default' }}
        >
          <primitive object={jadeMaskModel.scene} scale={2} />
          {/* Mesh para capturar clicks */}
          <mesh>
            <boxGeometry args={[3, 3, 3]} />
            <meshBasicMaterial color="#00ff88" wireframe transparent opacity={0.3} />
          </mesh>
          <pointLight color="#00ff88" intensity={2} distance={8} />
        </group>
      )}

      {/* Iluminación */}
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={0.8} />
    </group>
  )
}

'use client'

import { useState, useRef, useMemo, useEffect, Suspense } from 'react'
import { useGLTF, Html } from '@react-three/drei'
import { useFrame, useThree } from '@react-three/fiber'
import { Group, Mesh, MeshStandardMaterial, Color, Vector3 } from 'three'

// Colores reutilizables (evita crear en cada frame)
const HOVER_COLOR = new Color('#ffd700')
const DEFAULT_COLOR = new Color('#000000')
import PumaPunkuBlock from './PumaPunkuBlock'
import PumaPunkuStructure from './PumaPunkuStructure'
import SelectableObject from './SelectableObject'
import { useObjectSelection } from './ObjectSelectionContext'
import { getAssetPath } from '@/lib/paths'
import SunGate from './SunGate'
import PortalDetector from './PortalDetector'
import CropCircle from './CropCircle'
import { isMissionCompleted } from '@/types/missionState'

/**
 * 🔄 Loading placeholder para Puma Punku
 */
function LoadingPumaPunku() {
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
        <div>Cargando Puma Punku...</div>
      </div>
    </Html>
  )
}

/** Escena completa de Puma Punku: estructura + bloque central + 8 bloques dispersos */
export default function PumaPunkuScene({ 
  onViracochaSpeak,
  onPortalEnter,
  avatarPositionRef
}: { 
  onViracochaSpeak?: () => void
  onPortalEnter?: () => void
  avatarPositionRef?: React.RefObject<Vector3>
}) {
  return (
    <Suspense fallback={<LoadingPumaPunku />}>
      <PumaPunkuSceneContent 
        onViracochaSpeak={onViracochaSpeak}
        onPortalEnter={onPortalEnter}
        avatarPositionRef={avatarPositionRef}
      />
    </Suspense>
  )
}

function PumaPunkuSceneContent({ 
  onViracochaSpeak,
  onPortalEnter,
  avatarPositionRef
}: { 
  onViracochaSpeak?: () => void
  onPortalEnter?: () => void
  avatarPositionRef?: React.RefObject<Vector3>
}) {
  const { blockMoved } = useObjectSelection()
  
  // 🎼 Activar arquitectura de Puma Punku
  useEffect(() => {
    import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
      const harmonia = getHarmoniaMundi()
      if (harmonia.isEnabled()) {
        harmonia.activateArchitecture('puma-punku')
        console.log('🏛️ Arquitectura de Puma Punku activada')
      }
    })
    
    return () => {
      import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
        const harmonia = getHarmoniaMundi()
        harmonia.deactivateArchitecture('puma-punku')
      })
    }
  }, [])
  
  // Cargar estado persistente de la misión
  const [gateRevealed, setGateRevealed] = useState(() => {
    if (typeof window !== 'undefined') {
      return sessionStorage.getItem('viracocha_gate_revealed') === 'true'
    }
    return false
  })

  const [magnaBowlCollected, setMagnaBowlCollected] = useState(() => {
    if (typeof window !== 'undefined') {
      return sessionStorage.getItem('item_magna_bowl_collected') === 'true'
    }
    return false
  })

  // Sincronizar con sessionStorage cuando cambia el estado del item
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const checkMagnaBowl = () => {
        const collected = sessionStorage.getItem('item_magna_bowl_collected') === 'true'
        setMagnaBowlCollected(collected)
      }
      
      // Verificar cada 5 segundos si se recolectó el item
      const interval = setInterval(checkMagnaBowl, 5000)
      return () => clearInterval(interval)
    }
  }, [])

  const handleViracochaSpeak = () => {
    // Revelar la puerta la primera vez que habla
    if (!gateRevealed) {
      setGateRevealed(true)
      if (typeof window !== 'undefined') {
        sessionStorage.setItem('viracocha_gate_revealed', 'true')
      }
    }
    // Llamar al callback original con el estado de la misión
    if (onViracochaSpeak) {
      onViracochaSpeak()
    }
  }

  const extraBlocks: Array<{ id: string; pos: [number, number, number]; rot: number }> = [
    { id: 'pp-b1', pos: [-12, 0,   8], rot: 0.3 },
    { id: 'pp-b2', pos: [ 15, 0,  -6], rot: 1.1 },
    { id: 'pp-b3', pos: [ -8, 0, -18], rot: 2.0 },
    { id: 'pp-b4', pos: [ 20, 0,  14], rot: 0.7 },
    { id: 'pp-b5', pos: [-20, 0, -10], rot: 1.5 },
    { id: 'pp-b6', pos: [  6, 0,  22], rot: 0.9 },
    { id: 'pp-b7', pos: [-16, 0,  18], rot: 2.4 },
    { id: 'pp-b8', pos: [ 10, 0, -22], rot: 0.2 },
  ]

  // Verificar si la misión está completa - lee de localStorage al montar
  const [missionDone, setMissionDone] = useState(false)
  useEffect(() => {
    setMissionDone(isMissionCompleted('pumaPunku', 'reveal_structure'))
  }, [blockMoved])

  return (
    <>
      {/* Estructura megalítica — fija, se revela al mover un bloque */}
      <PumaPunkuStructure position={[8, 0, -8]} rotation={[0, Math.PI / 6, 0]} revealed={blockMoved} />

      {/* Viracocha — guardián en la entrada de la estructura */}
      <ViracochaGuardian 
        revealed={blockMoved} 
        onSpeak={handleViracochaSpeak}
        magnaBowlCollected={magnaBowlCollected}
      />

      {/* Puerta del Sol - aparece cuando Viracocha habla por primera vez */}
      <SunGate 
        position={[70, 8, 60]} 
        rotation={[0, -Math.PI / 2 - Math.PI / 12 + Math.PI / 6 + Math.PI / 12, 0]} 
        revealed={gateRevealed} 
      />

      {/* 💠 Crop Circle: Grid Modular H-Blocks (Tecnología Alienígena) */}
      <CropCircle 
        type="hBlock" 
        position={[83, 0.3, 67]} 
        scale={1.5} 
        visible={missionDone} 
      />

      {/* Detector de portal - teletransporta al Lago Titicaca */}
      {gateRevealed && avatarPositionRef && onPortalEnter && (
        <PortalDetector
          avatarPositionRef={avatarPositionRef}
          portalPosition={[70, 8, 60]}
          portalRotation={[0, -Math.PI / 2 - Math.PI / 12 + Math.PI / 6 + Math.PI / 12, 0]}
          portalScale={20}
          onPortalEnter={onPortalEnter}
          enabled={gateRevealed}
        />
      )}

      {/* Bloque central */}
      <MovablePumaPunkuBlock />

      {/* Bloques dispersos */}
      {extraBlocks.map((b) => (
        <MovableExtraBlock key={b.id} id={b.id} position={b.pos} rotation={b.rot} />
      ))}
    </>
  )
}

function MovablePumaPunkuBlock() {
  const [pos, setPos] = useState<[number, number, number]>([0, 0, 0])
  const { notifyBlockMoved } = useObjectSelection()
  return (
    <SelectableObject id="puma-punku-block" position={pos} onMove={(p) => { setPos(p); notifyBlockMoved() }}>
      <PumaPunkuBlock position={[0, 0.3, 0]} scale={0.075} rotation={[0, Math.PI / 4, 0]} />
    </SelectableObject>
  )
}

function MovableExtraBlock({ id, position, rotation }: { id: string; position: [number, number, number]; rotation: number }) {
  const [pos, setPos] = useState<[number, number, number]>(position)
  const { notifyBlockMoved } = useObjectSelection()
  return (
    <SelectableObject id={id} position={pos} onMove={(p) => { setPos(p); notifyBlockMoved() }}>
      <PumaPunkuBlock position={[0, 0.3, 0]} scale={0.075} rotation={[0, rotation, 0]} />
    </SelectableObject>
  )
}

/** Viracocha parado en la entrada de la estructura megalítica */
function ViracochaGuardian({ 
  revealed, 
  onSpeak,
  magnaBowlCollected 
}: { 
  revealed: boolean
  onSpeak?: () => void
  magnaBowlCollected: boolean
}) {
  const { scene } = useGLTF(getAssetPath('/viracocha.glb'))
  const groupRef = useRef<Group>(null)
  const opacityRef = useRef(0)
  const [hovered, setHovered] = useState(false)
  const { camera, gl } = useThree()

  const SCALE = 4
  const OFFSET_Y = 0.206 * SCALE

  // Clonar escena y preparar materiales transparentes
  const { cloned, meshes } = useMemo(() => {
    const cloned = scene.clone(true)
    const meshes: Mesh[] = []
    cloned.traverse((child) => {
      if (child instanceof Mesh) {
        child.material = (child.material as any).clone()
        ;(child.material as MeshStandardMaterial).transparent = true
        ;(child.material as MeshStandardMaterial).opacity = 0
        meshes.push(child)
      }
    })
    return { cloned, meshes }
  }, [scene])

  useFrame(({ camera }, delta) => {
    if (!groupRef.current) return

    // Fade-in/out igual que PumaPunkuStructure (~3s)
    if (revealed && opacityRef.current < 1) {
      opacityRef.current = Math.min(1, opacityRef.current + delta * 0.35)
      meshes.forEach(m => {
        ;(m.material as MeshStandardMaterial).opacity = opacityRef.current
      })
    } else if (!revealed && opacityRef.current > 0) {
      opacityRef.current = 0
      meshes.forEach(m => {
        ;(m.material as MeshStandardMaterial).opacity = 0
      })
    }

    // Outline dorado cuando está hovered
    if (revealed && opacityRef.current > 0) {
      meshes.forEach(m => {
        if (hovered) {
          ;(m.material as MeshStandardMaterial).emissive = HOVER_COLOR
          ;(m.material as MeshStandardMaterial).emissiveIntensity = 0.3
        } else {
          ;(m.material as MeshStandardMaterial).emissive = DEFAULT_COLOR
          ;(m.material as MeshStandardMaterial).emissiveIntensity = 0
        }
      })
    }

    // Seguir la cámara con la mirada (solo eje Y)
    if (opacityRef.current > 0) {
      const pos = groupRef.current.position
      const dx = camera.position.x - pos.x
      const dz = camera.position.z - pos.z
      groupRef.current.rotation.y = Math.atan2(dx, dz)
    }
  })

  // Cambiar cursor cuando está visible y hovered
  useFrame(() => {
    if (revealed && opacityRef.current > 0.5) {
      gl.domElement.style.cursor = hovered ? 'pointer' : 'auto'
    }
  })

  const handleClick = (e: any) => {
    if (revealed && opacityRef.current > 0.5 && onSpeak) {
      e.stopPropagation()
      onSpeak()
    }
  }

  return (
    <group
      ref={groupRef}
      position={[14.5 - 0.866, OFFSET_Y + 4.4, 0.33 + 0.5]}
      scale={SCALE}
      onClick={handleClick}
      onPointerOver={() => revealed && opacityRef.current > 0.5 && setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      <primitive object={cloned} />
    </group>
  )
}

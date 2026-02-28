'use client'

import { useState, useRef, useMemo } from 'react'
import { useGLTF } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import PumaPunkuBlock from './PumaPunkuBlock'
import PumaPunkuStructure from './PumaPunkuStructure'
import SelectableObject from './SelectableObject'
import { useObjectSelection } from './ObjectSelectionContext'
import { getAssetPath } from '@/lib/paths'

/** Escena completa de Puma Punku: estructura + bloque central + 8 bloques dispersos */
export default function PumaPunkuScene() {
  const { blockMoved } = useObjectSelection()

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

  return (
    <>
      {/* Estructura megalítica — fija, se revela al mover un bloque */}
      <PumaPunkuStructure position={[8, 0, -8]} rotation={[0, Math.PI / 6, 0]} revealed={blockMoved} />

      {/* Viracocha — guardián en la entrada de la estructura */}
      <ViracochaGuardian revealed={blockMoved} />

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
function ViracochaGuardian({ revealed }: { revealed: boolean }) {
  const { scene } = useGLTF(getAssetPath('/viracocha.glb'))
  const groupRef = useRef<THREE.Group>(null)
  const opacityRef = useRef(0)

  const SCALE = 4
  const OFFSET_Y = 0.206 * SCALE

  // Clonar escena y preparar materiales transparentes (igual que PumaPunkuStructure)
  const { cloned, meshes } = useMemo(() => {
    const cloned = scene.clone(true)
    const meshes: THREE.Mesh[] = []
    cloned.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        child.material = (child.material as THREE.Material).clone()
        ;(child.material as THREE.MeshStandardMaterial).transparent = true
        ;(child.material as THREE.MeshStandardMaterial).opacity = 0
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
        ;(m.material as THREE.MeshStandardMaterial).opacity = opacityRef.current
      })
    } else if (!revealed && opacityRef.current > 0) {
      opacityRef.current = 0
      meshes.forEach(m => {
        ;(m.material as THREE.MeshStandardMaterial).opacity = 0
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

  return (
    <group
      ref={groupRef}
      position={[14.5 - 0.866, OFFSET_Y + 4.4, 0.33 + 0.5]}
      scale={SCALE}
    >
      <primitive object={cloned} />
    </group>
  )
}

useGLTF.preload(getAssetPath('/viracocha.glb'))

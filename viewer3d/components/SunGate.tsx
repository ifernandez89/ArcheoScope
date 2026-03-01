'use client'

import { useRef, useMemo } from 'react'
import { useGLTF } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

interface SunGateProps {
  position: [number, number, number]
  rotation: [number, number, number]
  revealed: boolean
}

/** Puerta del Sol - aparece lentamente cuando Viracocha habla por primera vez */
export default function SunGate({ position, rotation, revealed }: SunGateProps) {
  const { scene } = useGLTF(getAssetPath('/puerta del sol front.glb'))
  const groupRef = useRef<THREE.Group>(null)
  const opacityRef = useRef(0)

  const SCALE = 20 // Tamaño grande para que sea visible
  const OFFSET_Y = 0 // Ajustar si es necesario para que la base toque el suelo

  // Clonar escena y preparar materiales transparentes
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

  useFrame((_, delta) => {
    if (!groupRef.current) return

    // Fade-in lento cuando se revela (~4 segundos)
    if (revealed && opacityRef.current < 1) {
      opacityRef.current = Math.min(1, opacityRef.current + delta * 0.25)
      meshes.forEach(m => {
        ;(m.material as THREE.MeshStandardMaterial).opacity = opacityRef.current
      })
    }
  })

  return (
    <group
      ref={groupRef}
      position={[position[0], position[1] + OFFSET_Y, position[2]]}
      rotation={rotation}
      scale={SCALE}
    >
      <primitive object={cloned} />
    </group>
  )
}

useGLTF.preload(getAssetPath('/puerta del sol front.glb'))

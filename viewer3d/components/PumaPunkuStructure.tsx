'use client'

import { useMemo, useRef } from 'react'
import { useGLTF } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

interface PumaPunkuStructureProps {
  position?: [number, number, number]
  scale?: number
  rotation?: [number, number, number]
  revealed?: boolean  // true = fade-in, false = invisible
}

export default function PumaPunkuStructure({
  position = [0, 0, 0],
  scale = 65.03,
  rotation = [0, 0, 0],
  revealed = false
}: PumaPunkuStructureProps) {
  const { scene } = useGLTF(getAssetPath('/pm_structure.glb'))
  const opacityRef = useRef(0)
  const groupRef = useRef<THREE.Group>(null)

  const { cloned, offsetY, meshes } = useMemo(() => {
    const cloned = scene.clone(true)
    cloned.scale.set(scale, scale, scale)
    cloned.updateMatrixWorld(true)

    const box = new THREE.Box3().setFromObject(cloned)
    const minY = box.min.y

    const meshes: THREE.Mesh[] = []
    cloned.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        child.castShadow = true
        child.receiveShadow = true
        // Hacer material transparente para poder animar opacity
        if (child.material) {
          child.material = (child.material as THREE.Material).clone()
          ;(child.material as THREE.MeshStandardMaterial).transparent = true
          ;(child.material as THREE.MeshStandardMaterial).opacity = 0
        }
        meshes.push(child)
      }
    })

    return { cloned, offsetY: minY < 0 ? -minY : 0, meshes }
  }, [scene, scale])

  // Animar opacity en cada frame
  useFrame((_, delta) => {
    if (revealed && opacityRef.current < 1) {
      // Fade-in: ~3 segundos para llegar a 1
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
  })

  return (
    <group ref={groupRef} position={[position[0], position[1] + offsetY, position[2]]} rotation={rotation}>
      <primitive object={cloned} />
    </group>
  )
}

useGLTF.preload(getAssetPath('/pm_structure.glb'))

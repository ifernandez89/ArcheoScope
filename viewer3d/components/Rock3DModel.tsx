/**
 * Rock3DModel - Roca 3D usando modelo GLB de Blender
 * 
 * Carga el modelo rock_blender.glb
 */

import { useRef, useEffect, useMemo } from 'react'
import { useGLTF } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

interface Rock3DModelProps {
  position: [number, number, number]
  scale?: number
  rotation?: number
}

export default function Rock3DModel({ position, scale = 1, rotation = 0 }: Rock3DModelProps) {
  const groupRef = useRef<THREE.Group>(null)
  
  // Cargar modelo GLB
  const { scene } = useGLTF(getAssetPath('/rock_blender.glb'))
  
  // Clonar el modelo para cada instancia - SOLO UNA VEZ con useMemo
  const clonedScene = useMemo(() => {
    const cloned = scene.clone(true)
    cloned.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        child.castShadow = true
        child.receiveShadow = true
        if (child.material) {
          child.material = (child.material as THREE.Material).clone()
        }
      }
    })
    return cloned
  }, [scene])
  
  useEffect(() => {
    if (clonedScene) {
      clonedScene.scale.set(scale, scale, scale)
      clonedScene.rotation.y = rotation
    }
  }, [clonedScene, scale, rotation])
  
  return (
    <group ref={groupRef} position={position}>
      <primitive object={clonedScene} />
    </group>
  )
}

// Precargar el modelo
useGLTF.preload(getAssetPath('/rock_blender.glb'))

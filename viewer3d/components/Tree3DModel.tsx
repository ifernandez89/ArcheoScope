/**
 * Tree3DModel - Árbol 3D usando modelo GLB de Blender
 * 
 * Carga el modelo tree_blender.glb
 */

import { useRef, useEffect } from 'react'
import { useGLTF } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

interface Tree3DModelProps {
  position: [number, number, number]
  scale?: number
  rotation?: number
}

export default function Tree3DModel({ position, scale = 1, rotation = 0 }: Tree3DModelProps) {
  const groupRef = useRef<THREE.Group>(null)
  
  // Cargar modelo GLB
  const { scene } = useGLTF(getAssetPath('/tree_blender.glb'))
  
  // Clonar el modelo para cada instancia
  const clonedScene = scene.clone()
  
  useEffect(() => {
    if (clonedScene) {
      // Ajustar escala y rotación
      clonedScene.scale.set(scale, scale, scale)
      clonedScene.rotation.y = rotation
      
      // Habilitar sombras
      clonedScene.traverse((child) => {
        if (child instanceof THREE.Mesh) {
          child.castShadow = true
          child.receiveShadow = true
        }
      })
    }
  }, [clonedScene, scale, rotation])
  
  return (
    <group ref={groupRef} position={position}>
      <primitive object={clonedScene} />
    </group>
  )
}

// Precargar el modelo
useGLTF.preload(getAssetPath('/tree_blender.glb'))

/**
 * Tree3DModel - Árbol 3D usando modelos GLB de Blender
 * 
 * Soporta 4 tipos de árboles: tree_blender.glb, tree_1.glb, tree_2.glb, tree_3.glb
 */

import { useRef, useEffect } from 'react'
import { useGLTF } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

export type TreeType = 'default' | 'tree1' | 'tree2' | 'tree3'

interface Tree3DModelProps {
  position: [number, number, number]
  scale?: number
  rotation?: number
  treeType?: TreeType
}

// Mapeo de tipos de árbol a rutas de archivo
const TREE_MODELS: Record<TreeType, string> = {
  default: '/tree_blender.glb',
  tree1: '/tree_1.glb',
  tree2: '/tree_2.glb',
  tree3: '/tree_3.glb'
}

export default function Tree3DModel({ 
  position, 
  scale = 1, 
  rotation = 0,
  treeType = 'default'
}: Tree3DModelProps) {
  const groupRef = useRef<THREE.Group>(null)
  
  // Cargar modelo GLB según el tipo
  const modelPath = getAssetPath(TREE_MODELS[treeType])
  const { scene } = useGLTF(modelPath)
  
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

// Precargar todos los modelos
useGLTF.preload(getAssetPath('/tree_blender.glb'))
useGLTF.preload(getAssetPath('/tree_1.glb'))
useGLTF.preload(getAssetPath('/tree_2.glb'))
useGLTF.preload(getAssetPath('/tree_3.glb'))

/**
 * Tree3DModel - Árbol 3D usando modelos GLB de Blender
 * 
 * Soporta 4 tipos de árboles: tree_blender.glb, tree_1.glb, tree_2.glb, tree_3.glb
 * Con texturas: BarkDecidious0143_5_S.jpg, BarkDecidious0194_7_S.jpg, Leaves0120_35_S.png, etc.
 */

import { useRef, useEffect, useMemo } from 'react'
import { useGLTF, useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

export type TreeType = 'default' | 'tree1' | 'tree2' | 'tree3' | 'tree4' | 'treeNew1' | 'treeNew4'

interface Tree3DModelProps {
  position: [number, number, number]
  scale?: number
  rotation?: number
  treeType?: TreeType
}

// Mapeo de tipos de árbol a rutas de archivo
const TREE_MODELS: Record<TreeType, string> = {
  default: '/tree_new.glb',    // Nuevo modelo 1
  tree1: '/tree_new2.glb',     // Nuevo modelo 2
  tree2: '/tree_new3.glb',     // Nuevo modelo 3
  tree3: '/tree_new4.glb',     // Nuevo modelo 4
  tree4: '/tree_new4.glb',     // Alias
  treeNew1: '/tree_new.glb',   // Alias
  treeNew4: '/tree_new4.glb'   // El que usamos en Puma Punku
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
  
  // Cargar texturas
  const barkTexture1 = useTexture(getAssetPath('/BarkDecidious0143_5_S.jpg'))
  const leavesTexture1 = useTexture(getAssetPath('/Leaves0120_35_S.png'))
  
  // ROTACIONES HARDCODEADAS por archivo GLB específico para que estén siempre verticales
  const modelRotations: Record<string, [number, number, number]> = {
    '/tree_blender.glb': [Math.PI / 2, 0, 0],  // 90° en X para levantar tree_blender.glb
    '/tree_1.glb': [0, 0, 0],                   // Por definir
    '/tree_2.glb': [0, 0, 0],                   // Por definir
    '/tree_3.glb': [0, 0, 0],                   // Por definir
    '/tree_4.glb': [0, 0, 0]                    // Por definir
  }
  
  const baseRotation = modelRotations[TREE_MODELS[treeType]] || [0, 0, 0]
  
  // Clonar el modelo para cada instancia - SOLO UNA VEZ con useMemo
  const clonedScene = useMemo(() => {
    const cloned = scene.clone(true)
    cloned.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        child.castShadow = true
        child.receiveShadow = true
        if (child.material) {
          child.material = (child.material as THREE.Material).clone()
          const material = child.material as THREE.MeshStandardMaterial
          material.depthWrite = true
          material.depthTest = true
          if (material.name && (material.name.toLowerCase().includes('bark') || 
                                material.name.toLowerCase().includes('trunk') ||
                                material.name.toLowerCase().includes('wood'))) {
            material.map = barkTexture1
            material.needsUpdate = true
          }
          if (material.name && (material.name.toLowerCase().includes('leaf') || 
                                material.name.toLowerCase().includes('leaves'))) {
            material.map = leavesTexture1
            material.transparent = true
            material.alphaTest = 0.5
            material.side = THREE.DoubleSide
            material.depthWrite = false
            material.needsUpdate = true
          }
        }
      }
    })
    return cloned
  }, [scene, treeType, barkTexture1, leavesTexture1])
  
  useEffect(() => {
    if (clonedScene) {
      clonedScene.scale.set(scale, scale, scale)
    }
  }, [clonedScene, scale])
  
  return (
    <group ref={groupRef} position={position} rotation={[
      TREE_MODELS[treeType] === '/tree_blender.glb' ? Math.PI / 2 : 0,
      rotation,
      0
    ]}>
      <primitive object={clonedScene} />
    </group>
  )
}

// Árboles y texturas se cargan bajo demanda al entrar al terreno

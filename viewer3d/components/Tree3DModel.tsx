/**
 * Tree3DModel - Árbol 3D usando modelos GLB de Blender
 * 
 * Soporta 4 tipos de árboles: tree_blender.glb, tree_1.glb, tree_2.glb, tree_3.glb
 * Con texturas: BarkDecidious0143_5_S.jpg, BarkDecidious0194_7_S.jpg, Leaves0120_35_S.png, etc.
 */

import { useRef, useEffect } from 'react'
import { useGLTF, useTexture } from '@react-three/drei'
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
  
  // Cargar texturas
  const barkTexture1 = useTexture(getAssetPath('/BarkDecidious0143_5_S.jpg'))
  const barkTexture2 = useTexture(getAssetPath('/BarkDecidious0194_7_S.jpg'))
  const leavesTexture1 = useTexture(getAssetPath('/Leaves0120_35_S.png'))
  const leavesTexture2 = useTexture(getAssetPath('/Leaves0142_4_S.png'))
  const leavesTexture3 = useTexture(getAssetPath('/Leaves0156_1_S.png'))
  
  // Clonar el modelo para cada instancia
  const clonedScene = scene.clone()
  
  useEffect(() => {
    if (clonedScene) {
      // Ajustar escala y rotación
      clonedScene.scale.set(scale, scale, scale)
      clonedScene.rotation.y = rotation
      
      // Aplicar texturas y habilitar sombras
      clonedScene.traverse((child) => {
        if (child instanceof THREE.Mesh) {
          child.castShadow = true
          child.receiveShadow = true
          
          // Aplicar texturas según el nombre del material
          if (child.material) {
            const material = child.material as THREE.MeshStandardMaterial
            
            // Si el material tiene "bark" o "trunk" en el nombre, aplicar textura de corteza
            if (material.name && (material.name.toLowerCase().includes('bark') || 
                                  material.name.toLowerCase().includes('trunk') ||
                                  material.name.toLowerCase().includes('wood'))) {
              material.map = barkTexture1
              material.needsUpdate = true
            }
            
            // Si el material tiene "leaf" o "leaves" en el nombre, aplicar textura de hojas
            if (material.name && (material.name.toLowerCase().includes('leaf') || 
                                  material.name.toLowerCase().includes('leaves'))) {
              material.map = leavesTexture1
              material.transparent = true
              material.alphaTest = 0.5
              material.side = THREE.DoubleSide
              material.needsUpdate = true
            }
          }
        }
      })
    }
  }, [clonedScene, scale, rotation, barkTexture1, leavesTexture1])
  
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

// Precargar texturas
useTexture.preload(getAssetPath('/BarkDecidious0143_5_S.jpg'))
useTexture.preload(getAssetPath('/BarkDecidious0194_7_S.jpg'))
useTexture.preload(getAssetPath('/Leaves0120_35_S.png'))
useTexture.preload(getAssetPath('/Leaves0142_4_S.png'))
useTexture.preload(getAssetPath('/Leaves0156_1_S.png'))

/**
 * Rock3DModel - Roca 3D usando modelo OBJ real
 * 
 * Carga el modelo Rock1.obj con su textura
 */

import { useRef, useEffect } from 'react'
import { useLoader } from '@react-three/fiber'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js'
import { MTLLoader } from 'three/examples/jsm/loaders/MTLLoader.js'
import * as THREE from 'three'

interface Rock3DModelProps {
  position: [number, number, number]
  scale?: number
  rotation?: number
}

export default function Rock3DModel({ position, scale = 1, rotation = 0 }: Rock3DModelProps) {
  const groupRef = useRef<THREE.Group>(null)
  
  // Cargar materiales y modelo OBJ
  const materials = useLoader(MTLLoader, '/Rock1.mtl')
  const obj = useLoader(OBJLoader, '/Rock1.obj', (loader) => {
    materials.preload()
    loader.setMaterials(materials)
  })
  
  // Clonar el modelo para cada instancia
  const clonedObj = obj.clone()
  
  useEffect(() => {
    if (clonedObj) {
      // Ajustar escala y rotación
      clonedObj.scale.set(scale * 0.015, scale * 0.015, scale * 0.015) // OBJ suele venir en escala grande
      clonedObj.rotation.y = rotation
      
      // Habilitar sombras
      clonedObj.traverse((child) => {
        if (child instanceof THREE.Mesh) {
          child.castShadow = true
          child.receiveShadow = true
          
          // Asegurar que el material sea visible
          if (child.material) {
            if (Array.isArray(child.material)) {
              child.material.forEach(mat => {
                mat.side = THREE.DoubleSide
              })
            } else {
              child.material.side = THREE.DoubleSide
            }
          }
        }
      })
    }
  }, [clonedObj, scale, rotation])
  
  return (
    <group ref={groupRef} position={position}>
      <primitive object={clonedObj} />
    </group>
  )
}

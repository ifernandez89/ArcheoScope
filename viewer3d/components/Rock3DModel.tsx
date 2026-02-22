/**
 * Rock3DModel - Roca 3D usando modelo OBJ real
 * 
 * Carga el modelo Rock1.obj con su textura
 */

import { useRef, useEffect } from 'react'
import { useLoader } from '@react-three/fiber'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js'
import { MTLLoader } from 'three/examples/jsm/loaders/MTLLoader.js'
import { TextureLoader } from 'three'
import * as THREE from 'three'

interface Rock3DModelProps {
  position: [number, number, number]
  scale?: number
  rotation?: number
}

export default function Rock3DModel({ position, scale = 1, rotation = 0 }: Rock3DModelProps) {
  const groupRef = useRef<THREE.Group>(null)
  
  // Cargar textura directamente
  const texture = useLoader(TextureLoader, '/Rock-Texture-Surface.jpg')
  
  // Cargar modelo OBJ sin MTL para evitar problemas
  const obj = useLoader(OBJLoader, '/Rock1.obj')
  
  // Clonar el modelo para cada instancia
  const clonedObj = obj.clone()
  
  useEffect(() => {
    if (clonedObj && texture) {
      // Ajustar escala y rotación
      clonedObj.scale.set(scale * 0.015, scale * 0.015, scale * 0.015)
      clonedObj.rotation.y = rotation
      
      // Aplicar textura y configurar material
      clonedObj.traverse((child) => {
        if (child instanceof THREE.Mesh) {
          child.castShadow = true
          child.receiveShadow = true
          
          // Crear material con la textura
          child.material = new THREE.MeshStandardMaterial({
            map: texture,
            roughness: 0.95,
            metalness: 0.05,
            side: THREE.FrontSide // Solo cara frontal, sin transparencia
          })
        }
      })
    }
  }, [clonedObj, texture, scale, rotation])
  
  return (
    <group ref={groupRef} position={position}>
      <primitive object={clonedObj} />
    </group>
  )
}

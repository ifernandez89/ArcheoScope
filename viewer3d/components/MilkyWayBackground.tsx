'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

/**
 * Fondo de la Vía Láctea - Esfera envolvente con textura
 * 
 * CARACTERÍSTICAS:
 * - Esfera gigante invertida (BackSide)
 * - Textura 8K de la Vía Láctea
 * - Rotación muy lenta
 * - Se combina con estrellas procedurales
 * 
 * FILOSOFÍA:
 * - Profundidad espacial
 * - Contexto galáctico
 * - Inmersión total
 */
export default function MilkyWayBackground() {
  const sphereRef = useRef<THREE.Mesh>(null)
  
  // Cargar textura de la Vía Láctea
  const milkyWayTexture = useTexture(getAssetPath('/textures/8k_stars_milky_way.jpg'), (texture) => {
    console.log('🌌 Textura de la Vía Láctea cargada')
    texture.mapping = THREE.EquirectangularReflectionMapping
  })
  
  // Rotación muy lenta
  useFrame((state, delta) => {
    if (sphereRef.current) {
      sphereRef.current.rotation.y += delta * 0.001 // Muy lento
    }
  })
  
  return (
    <mesh ref={sphereRef}>
      {/* Esfera gigante que envuelve todo */}
      <sphereGeometry args={[1000, 64, 64]} />
      <meshBasicMaterial
        map={milkyWayTexture}
        side={THREE.BackSide} // Visible desde dentro
        transparent={false}
        depthWrite={false}
      />
    </mesh>
  )
}

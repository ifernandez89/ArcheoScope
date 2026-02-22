/**
 * Rock3DModel - Roca 3D realista con geometría procedural
 * 
 * Genera rocas con:
 * - Forma irregular usando dodecaedro deformado
 * - Textura de piedra realista
 * - Variación natural basada en posición
 */

import { useRef, useMemo } from 'react'
import * as THREE from 'three'

interface Rock3DModelProps {
  position: [number, number, number]
  scale?: number
  rotation?: number
}

export default function Rock3DModel({ position, scale = 1, rotation = 0 }: Rock3DModelProps) {
  const groupRef = useRef<THREE.Group>(null)
  
  // Generar variación basada en posición
  const seed = position[0] * 1000 + position[2] * 1000
  const random = (offset: number) => {
    const x = Math.sin(seed + offset) * 43758.5453
    return x - Math.floor(x)
  }
  
  // Crear geometría deformada para aspecto irregular
  const geometry = useMemo(() => {
    const geo = new THREE.DodecahedronGeometry(scale, 1)
    const positions = geo.attributes.position
    
    // Deformar vértices para aspecto irregular
    for (let i = 0; i < positions.count; i++) {
      const x = positions.getX(i)
      const y = positions.getY(i)
      const z = positions.getZ(i)
      
      // Aplicar deformación aleatoria basada en seed
      const deform = random(i * 3) * 0.3
      positions.setXYZ(
        i,
        x * (1 + deform),
        y * (0.6 + random(i * 3 + 1) * 0.4), // Aplanar un poco
        z * (1 + random(i * 3 + 2) * 0.3)
      )
    }
    
    geo.computeVertexNormals()
    return geo
  }, [scale, seed])
  
  // Colores variados de roca
  const rockColors = [
    '#4a3a2a', // Marrón oscuro
    '#5a4a3a', // Marrón medio
    '#6a5a4a', // Marrón claro
    '#3a2a1a'  // Casi negro
  ]
  
  const rockColor = rockColors[Math.floor(random(100) * rockColors.length)]
  
  return (
    <group ref={groupRef} position={position} rotation={[0, rotation, 0]}>
      <mesh 
        geometry={geometry}
        castShadow 
        receiveShadow
        rotation={[
          random(10) * Math.PI * 0.3,
          random(20) * Math.PI * 2,
          random(30) * Math.PI * 0.3
        ]}
      >
        <meshStandardMaterial 
          color={rockColor}
          roughness={0.95}
          metalness={0.05}
        />
      </mesh>
    </group>
  )
}

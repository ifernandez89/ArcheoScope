/**
 * Tree3DModel - Árbol 3D realista con geometría procedural mejorada
 * 
 * Genera árboles con:
 * - Tronco texturizado con corteza
 * - Copa volumétrica con múltiples niveles
 * - Ramas laterales
 * - Variación natural basada en posición
 */

import { useRef } from 'react'
import * as THREE from 'three'

interface Tree3DModelProps {
  position: [number, number, number]
  scale?: number
  rotation?: number
}

export default function Tree3DModel({ position, scale = 1, rotation = 0 }: Tree3DModelProps) {
  const groupRef = useRef<THREE.Group>(null)
  
  // Generar variación basada en posición
  const seed = position[0] * 1000 + position[2] * 1000
  const random = (offset: number) => {
    const x = Math.sin(seed + offset) * 43758.5453
    return x - Math.floor(x)
  }
  
  const trunkHeight = scale * (2.0 + random(1) * 0.8)
  const trunkRadius = scale * 0.18
  const crownHeight = scale * (2.5 + random(2) * 1.2)
  const crownRadius = scale * (1.2 + random(3) * 0.6)
  
  // Colores variados para el follaje
  const foliageColors = [
    '#1a4d2e', // Verde oscuro
    '#2d5016', // Verde medio
    '#3a6b35', // Verde claro
    '#4a7c59'  // Verde muy claro
  ]
  
  return (
    <group ref={groupRef} position={position} rotation={[0, rotation, 0]}>
      {/* Tronco principal con textura de corteza */}
      <mesh position={[0, trunkHeight / 2, 0]} castShadow receiveShadow>
        <cylinderGeometry args={[trunkRadius * 0.85, trunkRadius, trunkHeight, 8, 4]} />
        <meshStandardMaterial 
          color="#3d2817"
          roughness={0.98}
          metalness={0.0}
        />
      </mesh>
      
      {/* Ramas principales saliendo del tronco */}
      {[0, 1, 2, 3, 4, 5].map((i) => {
        const angle = (i / 6) * Math.PI * 2 + random(i + 10)
        const height = trunkHeight * (0.5 + random(i + 20) * 0.3)
        const length = scale * (0.4 + random(i + 30) * 0.3)
        const thickness = trunkRadius * (0.3 + random(i + 40) * 0.2)
        
        return (
          <mesh
            key={`branch-${i}`}
            position={[
              Math.cos(angle) * trunkRadius * 0.7,
              height,
              Math.sin(angle) * trunkRadius * 0.7
            ]}
            rotation={[0, angle, Math.PI / 2.5]}
            castShadow
          >
            <cylinderGeometry args={[thickness * 0.5, thickness, length, 6]} />
            <meshStandardMaterial color="#3d2817" roughness={0.95} />
          </mesh>
        )
      })}
      
      {/* Copa - Nivel inferior (más ancho) */}
      <mesh position={[0, trunkHeight + crownHeight * 0.25, 0]} castShadow receiveShadow>
        <sphereGeometry args={[crownRadius * 1.1, 8, 8]} />
        <meshStandardMaterial 
          color={foliageColors[0]}
          roughness={0.9}
        />
      </mesh>
      
      {/* Copa - Nivel medio */}
      <mesh position={[0, trunkHeight + crownHeight * 0.5, 0]} castShadow receiveShadow>
        <sphereGeometry args={[crownRadius * 0.95, 8, 8]} />
        <meshStandardMaterial 
          color={foliageColors[1]}
          roughness={0.88}
        />
      </mesh>
      
      {/* Copa - Nivel superior */}
      <mesh position={[0, trunkHeight + crownHeight * 0.75, 0]} castShadow receiveShadow>
        <sphereGeometry args={[crownRadius * 0.75, 8, 8]} />
        <meshStandardMaterial 
          color={foliageColors[2]}
          roughness={0.86}
        />
      </mesh>
      
      {/* Copa - Punta */}
      <mesh position={[0, trunkHeight + crownHeight * 0.95, 0]} castShadow>
        <sphereGeometry args={[crownRadius * 0.5, 6, 6]} />
        <meshStandardMaterial 
          color={foliageColors[3]}
          roughness={0.84}
        />
      </mesh>
      
      {/* Grupos de hojas adicionales para más volumen */}
      {[0, 1, 2, 3].map((i) => {
        const angle = (i / 4) * Math.PI * 2 + random(i + 50)
        const heightOffset = random(i + 60) * crownHeight * 0.4
        const radiusOffset = random(i + 70) * crownRadius * 0.5
        
        return (
          <mesh
            key={`foliage-${i}`}
            position={[
              Math.cos(angle) * radiusOffset,
              trunkHeight + crownHeight * 0.5 + heightOffset,
              Math.sin(angle) * radiusOffset
            ]}
            castShadow
          >
            <sphereGeometry args={[crownRadius * 0.4, 6, 6]} />
            <meshStandardMaterial 
              color={foliageColors[Math.floor(random(i + 80) * 4)]}
              roughness={0.87}
            />
          </mesh>
        )
      })}
    </group>
  )
}

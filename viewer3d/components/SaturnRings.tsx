/**
 * 🪐 Saturn Rings - Anillos de Saturno
 */

'use client'

import * as THREE from 'three'

interface SaturnRingsProps {
  saturnRadius: number
  ringTexture: THREE.Texture
  tilt?: number
}

export default function SaturnRings({ 
  saturnRadius, 
  ringTexture,
  tilt = 26.7 
}: SaturnRingsProps) {
  const innerRadius = saturnRadius * 1.2
  const outerRadius = saturnRadius * 2.3
  const tiltRadians = (tilt * Math.PI) / 180
  
  console.log('🪐 SaturnRings rendering:', { saturnRadius, innerRadius, outerRadius, tilt })
  
  return (
    <group rotation={[Math.PI / 2, 0, tiltRadians]}>
      {/* Anillo con textura */}
      <mesh castShadow receiveShadow>
        <ringGeometry args={[innerRadius, outerRadius, 128]} />
        <meshStandardMaterial
          map={ringTexture}
          alphaMap={ringTexture}
          transparent
          opacity={0.95}
          side={THREE.DoubleSide}
          depthWrite={false}
          color="#fad5a5"
          roughness={0.8}
          metalness={0.0}
        />
      </mesh>
      
      {/* Anillo de respaldo (sin textura, solo color) para debug */}
      <mesh position={[0, 0, 0.5]}>
        <ringGeometry args={[innerRadius, outerRadius, 64]} />
        <meshBasicMaterial
          color="#fad5a5"
          transparent
          opacity={0.3}
          side={THREE.DoubleSide}
          depthWrite={false}
        />
      </mesh>
    </group>
  )
}

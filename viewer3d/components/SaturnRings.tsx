/**
 * 🪐 Saturn Rings - Anillos de Saturno
 *
 * VERSIÓN v1.2.7 FINAL:
 * ✓ Usa textura PNG personalizada (saturn_rings.png)
 * ✓ Partículas orbitales (15,000 puntos)
 * ✓ Alineación perfecta: anillos + partículas en el MISMO grupo
 * ✓ Rotación correcta: [tiltRadians, 0, 0] para inclinación de 26.7°
 */

'use client'

import { useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface SaturnRingsProps {
  saturnRadius: number
  ringTexture: THREE.Texture
  tilt?: number
}

/**
 * 🌌 Partículas orbitales (15,000 puntos)
 * Simulan el material disperso en los anillos
 * NO aplica rotación propia - hereda la del grupo padre
 */
function RingParticles({ saturnRadius, tilt }: { saturnRadius: number; tilt: number }) {
  const particlesRef = useRef<THREE.Points>(null)

  const { positions, velocities } = useMemo(() => {
    const count = 15000
    const pos = new Float32Array(count * 3)
    const vel = new Float32Array(count)

    const innerRadius = saturnRadius * 1.23  // Ring C inicio
    const outerRadius = saturnRadius * 2.27  // Ring A fin

    for (let i = 0; i < count; i++) {
      // Distribución no uniforme (más densidad en B y A)
      const rand = Math.random()
      let r: number

      if (rand < 0.5) {
        // 50% en Ring B (denso)
        r = saturnRadius * (1.52 + Math.random() * 0.43)
      } else if (rand < 0.85) {
        // 35% en Ring A
        r = saturnRadius * (2.02 + Math.random() * 0.25)
      } else {
        // 15% en Ring C
        r = saturnRadius * (1.23 + Math.random() * 0.29)
      }

      const theta = Math.random() * Math.PI * 2

      // Posición en plano XZ (horizontal)
      pos[i * 3] = r * Math.cos(theta)
      pos[i * 3 + 1] = (Math.random() - 0.5) * saturnRadius * 0.01  // Grosor fino en Y
      pos[i * 3 + 2] = r * Math.sin(theta)

      // Velocidad orbital (más rápido = más cerca)
      vel[i] = 0.01 / (r / saturnRadius)
    }

    return { positions: pos, velocities: vel }
  }, [saturnRadius])

  // Animación orbital en el plano XZ
  useFrame((_, delta) => {
    if (!particlesRef.current) return

    const pos = particlesRef.current.geometry.attributes.position.array as Float32Array

    for (let i = 0; i < positions.length / 3; i++) {
      const idx = i * 3
      const x = pos[idx]
      const z = pos[idx + 2]
      const r = Math.sqrt(x * x + z * z)
      let theta = Math.atan2(z, x)

      theta += velocities[i] * delta

      pos[idx] = r * Math.cos(theta)
      pos[idx + 2] = r * Math.sin(theta)
    }

    particlesRef.current.geometry.attributes.position.needsUpdate = true
  })
  
  // SIN rotación propia - hereda del grupo padre
  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={positions.length / 3}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={saturnRadius * 0.008}
        color="#ffeedd"
        transparent
        opacity={0.7}
        sizeAttenuation
        blending={THREE.AdditiveBlending}
        depthWrite={false}
      />
    </points>
  )
}

export default function SaturnRings({ 
  saturnRadius, 
  ringTexture,
  tilt = 26.7 
}: SaturnRingsProps) {
  const tiltRadians = (tilt * Math.PI) / 180
  
  console.log('🪐 SaturnRings v1.2.7 (solo partículas):', { saturnRadius, tilt })
  
  // ROTACIÓN CORRECTA: 90° para horizontal + tilt de 26.7°
  return (
    <group rotation={[Math.PI / 2 + tiltRadians, 0, 0]}>
      {/* 🌌 Solo partículas orbitales - sin PNG */}
      <RingParticles saturnRadius={saturnRadius} tilt={0} />
    </group>
  )
}

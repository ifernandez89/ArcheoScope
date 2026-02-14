'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

/**
 * Wrapper que hace orbitar la Tierra alrededor del Sol
 * Sistema híbrido profesional: Tierra a 100 unidades del Sol
 */
export default function EarthOrbitWrapper({ children }: { children: React.ReactNode }) {
  const orbitGroupRef = useRef<THREE.Group>(null)
  
  useFrame((state) => {
    if (orbitGroupRef.current) {
      const time = state.clock.elapsedTime
      const earthOrbitSpeed = 1.0 // Velocidad de referencia
      const earthOrbitDistance = 100 // Distancia al Sol
      const orbitAngle = time * earthOrbitSpeed * 0.05
      
      // Posición orbital de la Tierra alrededor del Sol (en el centro)
      orbitGroupRef.current.position.x = Math.cos(orbitAngle) * earthOrbitDistance
      orbitGroupRef.current.position.z = Math.sin(orbitAngle) * earthOrbitDistance
      orbitGroupRef.current.position.y = 0
    }
  })
  
  return (
    <group ref={orbitGroupRef}>
      {children}
    </group>
  )
}

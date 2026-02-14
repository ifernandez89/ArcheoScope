'use client'

import { useRef, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import { useTexture, Html } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

/**
 * Mercurio - El más pequeño y cercano al Sol
 * 
 * SISTEMA HÍBRIDO PROFESIONAL:
 * - Tierra_orbita = 100 unidades
 * - Mercurio = 0.38 (tamaño real proporcional)
 * - Órbita = 39 unidades (0.39 UA - proporción real)
 * - Velocidad = 4.15 (el más rápido del sistema)
 * 
 * CARACTERÍSTICAS:
 * - Superficie gris rocosa (similar a la Luna)
 * - Sin atmósfera
 * - Cráteres visibles
 * - Muy cercano al Sol
 */
export default function Mercury({ 
  earthRadius = 1, 
  visible = true 
}: { 
  earthRadius?: number
  visible?: boolean 
}) {
  const mercuryRef = useRef<THREE.Mesh>(null)
  const [labelPosition, setLabelPosition] = useState<[number, number, number]>([0, 0, 0])
  
  // Cargar textura de la Luna como placeholder para Mercurio (similar)
  const mercuryTexture = useTexture(getAssetPath('/textures/8k_moon.jpg'), (texture) => {
    console.log('☿️ Textura de Mercurio cargada (usando textura lunar)')
  })
  
  // SISTEMA HÍBRIDO PROFESIONAL
  // Proporciones orbitales REALES (Tierra = 100)
  const mercuryRadius = earthRadius * 0.38  // Tamaño real proporcional
  const mercuryDistance = 39                // Órbita real proporcional (0.39 UA)
  const mercurySpeed = 4.15                 // El más rápido
  
  // Animación orbital
  useFrame((state) => {
    if (mercuryRef.current) {
      const time = state.clock.elapsedTime
      const orbitAngle = time * mercurySpeed * 0.1
      
      // Posición orbital
      mercuryRef.current.position.x = Math.cos(orbitAngle) * mercuryDistance
      mercuryRef.current.position.z = Math.sin(orbitAngle) * mercuryDistance
      mercuryRef.current.position.y = 0
      
      // Actualizar posición de la etiqueta
      setLabelPosition([
        mercuryRef.current.position.x,
        mercuryRef.current.position.y + mercuryRadius + 0.5,
        mercuryRef.current.position.z
      ])
      
      // Rotación propia (muy lenta, acoplamiento de marea parcial)
      mercuryRef.current.rotation.y += 0.00015
    }
  })
  
  return (
    <group>
      {/* Mercurio - Superficie rocosa gris */}
      <mesh ref={mercuryRef} castShadow receiveShadow>
        <sphereGeometry args={[mercuryRadius, 64, 64]} />
        <meshStandardMaterial
          map={mercuryTexture}
          color="#9c9c9c" // Gris más claro que la Luna
          roughness={0.95}
          metalness={0.05}
        />
      </mesh>
      
      {/* Etiqueta sobre Mercurio */}
      <Html position={labelPosition} center>
        <div style={{
          color: '#9c9c9c',
          fontSize: '11px',
          fontWeight: 'bold',
          textShadow: '0 0 4px rgba(0,0,0,0.9)',
          pointerEvents: 'none',
          whiteSpace: 'nowrap'
        }}>
          ☿ Mercurio
        </div>
      </Html>
    </group>
  )
}

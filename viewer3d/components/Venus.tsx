'use client'

import { useRef, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import { useTexture, Html } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

/**
 * Venus - Presencia brillante discreta
 * 
 * CARACTERÍSTICAS:
 * - Escala: 0.95 diámetro Tierra (casi gemela)
 * - Distancia: 46 radios terrestres (reinterpretada artísticamente)
 * - Visual: Crema pálido, opaco, sin superficie visible
 * - Atmósfera: Densa y cerrada
 * - Movimiento: Velocidad 0.6 (más rápida que Tierra)
 * - Brillo: Emisión 0.15 (refleja mucha luz solar)
 * 
 * PRESENCIA NARRATIVA:
 * - Solo visible en modo solar y sistema
 * - Esfera silenciosa y cerrada
 * - Brilla ligeramente más que Marte
 * - Mantiene jerarquía: Sol → Tierra → Luna → Venus → Marte
 */
export default function Venus({ 
  earthRadius = 1, 
  visible = true 
}: { 
  earthRadius?: number
  visible?: boolean 
}) {
  const venusRef = useRef<THREE.Mesh>(null)
  const atmosphereRef = useRef<THREE.Mesh>(null)
  const [labelPosition, setLabelPosition] = useState<[number, number, number]>([0, 0, 0])
  
  // Cargar textura de Venus
  const venusTexture = useTexture(getAssetPath('/textures/4k_venus_atmosphere.jpg'), (texture) => {
    console.log('✅ Textura de Venus cargada')
  })
  
  // SISTEMA HÍBRIDO PROFESIONAL
  // Proporciones orbitales REALES (Tierra = 100)
  const venusRadius = earthRadius * 0.95  // Tamaño real proporcional
  const venusDistance = 72                // Órbita real proporcional (0.72 UA)
  const venusSpeed = 1.62                 // Velocidad proporcional
  
  // Animación orbital
  useFrame((state) => {
    if (venusRef.current) {
      const time = state.clock.elapsedTime
      const orbitAngle = time * venusSpeed * 0.1
      
      // Posición orbital
      venusRef.current.position.x = Math.cos(orbitAngle) * venusDistance
      venusRef.current.position.z = Math.sin(orbitAngle) * venusDistance
      venusRef.current.position.y = 0
      
      // Actualizar posición de la etiqueta
      setLabelPosition([
        venusRef.current.position.x,
        venusRef.current.position.y + venusRadius + 1,
        venusRef.current.position.z
      ])
      
      // Rotación propia (muy lenta, Venus rota al revés)
      venusRef.current.rotation.y -= 0.0001
    }
    
    // Atmósfera sigue a Venus
    if (atmosphereRef.current && venusRef.current) {
      atmosphereRef.current.position.copy(venusRef.current.position)
    }
  })
  
  return (
    <group>
      {/* Venus - Esfera opaca y cerrada */}
      <mesh ref={venusRef} castShadow receiveShadow>
        <sphereGeometry args={[venusRadius, 64, 64]} />
        <meshStandardMaterial
          map={venusTexture}
          color="#f5e6d3" // Crema pálido
          roughness={0.9}
          metalness={0.0}
          emissive="#f5e6d3"
          emissiveIntensity={0.15} // Brilla más que Marte
        />
      </mesh>
      
      {/* Atmósfera densa - Muy tenue */}
      <mesh ref={atmosphereRef} scale={1.05}>
        <sphereGeometry args={[venusRadius, 32, 32]} />
        <meshBasicMaterial
          color="#f5e6d3"
          transparent
          opacity={0.3}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          side={THREE.BackSide}
        />
      </mesh>
      
      {/* Etiqueta sobre Venus */}
      <Html position={labelPosition} center>
        <div style={{
          color: '#f5e6d3',
          fontSize: '11px',
          fontWeight: 'bold',
          textShadow: '0 0 4px rgba(0,0,0,0.9)',
          pointerEvents: 'none',
          whiteSpace: 'nowrap'
        }}>
          ♀ Venus
        </div>
      </Html>
    </group>
  )
}

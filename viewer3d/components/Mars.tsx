'use client'

import { useRef, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import { useTexture, Html } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

/**
 * Marte - Presencia distante y sobria
 * 
 * CARACTERÍSTICAS:
 * - Carácter superficial visible
 * - Tonos rojizos no saturados (óxido, no semáforo)
 * - Atmósfera marciana tenue
 * - Oscurecido para evitar caricatura
 * 
 * ESCALA ARTÍSTICA:
 * - Tamaño: 0.53 del diámetro terrestre
 * - Distancia: 42.5 unidades (más lejos que la Tierra)
 * - Velocidad orbital: 1.9 (más lento que la Tierra)
 */

interface MarsProps {
  earthRadius: number
  visible?: boolean
}

export default function Mars({ earthRadius, visible = true }: MarsProps) {
  const marsRef = useRef<THREE.Mesh>(null)
  const atmosphereRef = useRef<THREE.Mesh>(null)
  const [labelPosition, setLabelPosition] = useState<[number, number, number]>([0, 0, 0])
  
  // Cargar textura de Marte
  const marsTexture = useTexture(getAssetPath('/textures/2k_mars.jpg'), (texture) => {
    console.log('🔴 Textura de Marte cargada')
  })
  
  // SISTEMA HÍBRIDO PROFESIONAL
  // Proporciones orbitales REALES (Tierra = 200)
  // Tamaños ajustados: Marte = mitad de la Tierra actual
  const marsRadius = earthRadius * 0.5    // Mitad de la Tierra
  const marsDistance = 304                // Órbita proporcional (1.52 × 200)
  const marsSpeed = 0.53                  // Velocidad proporcional (más lento)
  
  // Animación orbital
  useFrame((state) => {
    if (marsRef.current) {
      const time = state.clock.elapsedTime
      const angle = time * marsSpeed * 0.05 + Math.PI // +Math.PI para ponerlo del otro lado
      
      // Órbita circular
      marsRef.current.position.x = Math.cos(angle) * marsDistance
      marsRef.current.position.z = Math.sin(angle) * marsDistance
      
      // Actualizar posición de la etiqueta
      setLabelPosition([
        marsRef.current.position.x,
        marsRef.current.position.y + marsRadius + 0.7,
        marsRef.current.position.z
      ])
      
      // Rotación similar a la Tierra
      marsRef.current.rotation.y += 0.0001
    }
    
    // Atmósfera sigue a Marte
    if (atmosphereRef.current && marsRef.current) {
      atmosphereRef.current.position.copy(marsRef.current.position)
    }
  })
  
  return (
    <group>
      {/* Núcleo de Marte - Superficie rojiza */}
      <mesh ref={marsRef}>
        <sphereGeometry args={[marsRadius, 64, 64]} />
        <meshStandardMaterial
          map={marsTexture}
          color="#8b6f5f" // Rojo terroso apagado (óxido)
          roughness={0.95}
          metalness={0.0}
        />
      </mesh>
      
      {/* Atmósfera marciana - Muy tenue */}
      <mesh ref={atmosphereRef} scale={1.03}>
        <sphereGeometry args={[marsRadius, 32, 32]} />
        <meshBasicMaterial
          color="#c97a5f"
          transparent
          opacity={0.04}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          side={THREE.BackSide}
        />
      </mesh>
      
      {/* Etiqueta sobre Marte */}
      <Html position={labelPosition} center>
        <div style={{
          color: '#c97a5f',
          fontSize: '11px',
          fontWeight: 'bold',
          textShadow: '0 0 4px rgba(0,0,0,0.9)',
          pointerEvents: 'none',
          whiteSpace: 'nowrap'
        }}>
          ♂ Marte
        </div>
      </Html>
    </group>
  )
}

'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

/**
 * Luna orbitando la Tierra con escala emocional coherente
 * 
 * Escala física real (no usable):
 * - Tamaño: 27% del diámetro terrestre
 * - Distancia: 30 diámetros terrestres (~384,400 km)
 * 
 * Escala emocional (usada aquí):
 * - Tamaño: 27% del radio terrestre (correcto)
 * - Distancia: 12 radios terrestres (reinterpretación honesta)
 * - Inclinación orbital: ~5° (real)
 * - Rotación sincrónica: siempre misma cara hacia la Tierra (real)
 */
export default function SimpleMoon() {
  const moonRef = useRef<THREE.Mesh>(null)
  
  // Cargar textura de la Luna de forma segura
  const moonTexture = useTexture(getAssetPath('/textures/8k_moon.jpg'), (texture) => {
    console.log('✅ Textura de Luna cargada')
  })
  
  useFrame((state) => {
    if (moonRef.current) {
      const time = state.clock.elapsedTime
      
      // Parámetros orbitales
      const orbitSpeed = 0.08 // Velocidad orbital (más lenta, más realista)
      const orbitRadius = 12 // Distancia emocional coherente (12 radios terrestres)
      const orbitalInclination = 5 * (Math.PI / 180) // Inclinación real de 5°
      
      // Ángulo orbital
      const angle = time * orbitSpeed
      
      // Posición orbital con inclinación
      moonRef.current.position.x = Math.cos(angle) * orbitRadius
      moonRef.current.position.z = Math.sin(angle) * orbitRadius
      moonRef.current.position.y = Math.sin(angle) * orbitRadius * Math.sin(orbitalInclination)
      
      // Rotación sincrónica: la Luna siempre muestra la misma cara a la Tierra
      // Esto significa que rota a la misma velocidad que orbita
      moonRef.current.rotation.y = -angle // Negativo para que mire hacia la Tierra
    }
  })
  
  return (
    <mesh ref={moonRef} castShadow receiveShadow>
      <sphereGeometry args={[0.27, 64, 64]} />
      <meshStandardMaterial
        map={moonTexture}
        color="#FFFFFF"
        roughness={0.95}
        metalness={0.05}
      />
    </mesh>
  )
}

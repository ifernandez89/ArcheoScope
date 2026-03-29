'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

/**
 * Luna orbitando la Tierra con escala emocional coherente y tidal locking real
 * 
 * ESCALA FÍSICA REAL (no usable visualmente):
 * - Tamaño: 27% del diámetro terrestre
 * - Distancia: 30 diámetros terrestres (~384,400 km)
 * 
 * ESCALA EMOCIONAL (usada aquí):
 * - Tamaño: 27% del radio terrestre (físicamente correcto)
 * - Distancia: 12 radios terrestres (reinterpretación visual honesta)
 * - Inclinación orbital: ~5° (real)
 * 
 * VELOCIDAD ORBITAL PROPORCIONAL:
 * - Luna: 27.3 días para orbitar la Tierra
 * - Tierra: 365 días para orbitar el Sol
 * - Proporción: 365/27.3 = 13.4x más rápida
 * - Velocidad Luna: 0.67 (13.4x más que Tierra que va a 0.05)
 * 
 * TIDAL LOCKING (Bloqueo por marea):
 * - La Luna rota exactamente al mismo ritmo que orbita
 * - Velocidad de rotación = Velocidad orbital
 * - Si avanza θ en órbita → rota θ sobre su eje
 * - Resultado: siempre vemos la misma cara (los mismos cráteres)
 * - Esto es física real, no una simplificación
 * 
 * VERIFICACIÓN:
 * - Acelera la órbita y observa desde cámara fija
 * - Los cráteres visibles NO deben cambiar
 * - Si cambian, el bloqueo está roto
 */
export default function SimpleMoon() {
  const moonRef = useRef<THREE.Mesh>(null)
  
  // Cargar textura de la Luna de forma segura
  const moonTexture = useTexture(getAssetPath('/textures/2k_moon.jpg'), (texture) => {
    console.log('✅ Textura de Luna cargada')
  })
  
  useFrame((state) => {
    if (moonRef.current) {
      const time = state.clock.elapsedTime
      
      // Parámetros orbitales - VELOCIDAD PROPORCIONAL REAL
      // Luna: 27.3 días vs Tierra: 365 días = 13.4x más rápida
      const orbitSpeed = 0.67 // 13.4x más rápida que la Tierra (0.05 * 13.4)
      const orbitRadius = 12 // Distancia emocional coherente (12 radios terrestres)
      const orbitalInclination = 5 * (Math.PI / 180) // Inclinación real de 5°
      
      // Ángulo orbital (θ)
      const orbitAngle = time * orbitSpeed
      
      // Posición orbital con inclinación
      moonRef.current.position.x = Math.cos(orbitAngle) * orbitRadius
      moonRef.current.position.z = Math.sin(orbitAngle) * orbitRadius
      moonRef.current.position.y = Math.sin(orbitAngle) * orbitRadius * Math.sin(orbitalInclination)
      
      // 🌙 TIDAL LOCKING (Bloqueo por marea)
      // La Luna rota exactamente al mismo ritmo que orbita
      moonRef.current.rotation.y = orbitAngle
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

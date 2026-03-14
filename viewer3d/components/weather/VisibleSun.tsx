'use client'

/**
 * VisibleSun - Sol visible en el cielo que sigue la posición astronómica real
 * 
 * Características:
 * - Se posiciona según solarDirection (calculado astronómicamente)
 * - Sale por el Este y se oculta por el Oeste
 * - La luz direccional apunta desde el sol hacia el origen
 * - Las sombras coinciden con la posición del sol
 * - Tamaño aparente realista en el horizonte
 */

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface VisibleSunProps {
  solarDirection: { x: number; y: number; z: number }
  intensity?: number
  distance?: number
}

export default function VisibleSun({ 
  solarDirection, 
  intensity = 3.0,
  distance = 500 // Distancia del sol (muy lejos para simular infinito)
}: VisibleSunProps) {
  const sunRef = useRef<THREE.Mesh>(null)
  const glowRef = useRef<THREE.Mesh>(null)
  const lightRef = useRef<THREE.DirectionalLight>(null)
  
  // Calcular posición del sol en el cielo
  const sunPosition = useMemo(() => {
    const dir = new THREE.Vector3(solarDirection.x, solarDirection.y, solarDirection.z)
    dir.normalize()
    return dir.multiplyScalar(distance)
  }, [solarDirection, distance])
  
  // Calcular intensidad según altura del sol
  const sunIntensity = useMemo(() => {
    // Cuando el sol está bajo (y < 0.2), reducir intensidad
    const heightFactor = Math.max(0, Math.min(1, solarDirection.y * 2))
    return intensity * heightFactor
  }, [solarDirection.y, intensity])
  
  // Color del sol según altura
  const sunColor = useMemo(() => {
    const y = solarDirection.y
    if (y < 0.1) {
      // Amanecer/atardecer: naranja rojizo
      return new THREE.Color('#ff6b35')
    } else if (y < 0.3) {
      // Mañana/tarde: amarillo dorado
      return new THREE.Color('#ffaa33')
    } else {
      // Mediodía: amarillo brillante
      return new THREE.Color('#fff8e7')
    }
  }, [solarDirection.y])
  
  // Tamaño aparente del sol (más grande en el horizonte)
  const sunSize = useMemo(() => {
    const y = solarDirection.y
    if (y < 0.2) {
      // Horizonte: más grande (ilusión óptica)
      return 25
    } else {
      // Alto en el cielo: tamaño normal
      return 20
    }
  }, [solarDirection.y])
  
  // Animación sutil de pulsación
  useFrame((state) => {
    const time = state.clock.elapsedTime
    
    if (sunRef.current) {
      // Pulsación muy sutil
      const pulse = 1 + Math.sin(time * 0.5) * 0.02
      sunRef.current.scale.setScalar(pulse)
    }
    
    if (glowRef.current) {
      // Glow respira más
      const breathe = 1 + Math.sin(time * 0.3) * 0.1
      glowRef.current.scale.setScalar(breathe)
    }
  })
  
  // Solo renderizar si el sol está sobre el horizonte
  if (solarDirection.y < -0.1) {
    return null
  }
  
  return (
    <group position={[sunPosition.x, sunPosition.y, sunPosition.z]}>
      {/* Núcleo del sol */}
      <mesh ref={sunRef}>
        <sphereGeometry args={[sunSize, 32, 32]} />
        <meshBasicMaterial
          color={sunColor}
          transparent
          opacity={0.95}
        />
      </mesh>
      
      {/* Glow exterior */}
      <mesh ref={glowRef} scale={1.5}>
        <sphereGeometry args={[sunSize, 24, 24]} />
        <meshBasicMaterial
          color={sunColor}
          transparent
          opacity={0.3}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          side={THREE.BackSide}
        />
      </mesh>
      
      {/* Corona exterior */}
      <mesh scale={2.0}>
        <sphereGeometry args={[sunSize, 16, 16]} />
        <meshBasicMaterial
          color={sunColor}
          transparent
          opacity={0.1}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          side={THREE.BackSide}
        />
      </mesh>
      
      {/* Luz direccional desde el sol hacia el origen */}
      <directionalLight
        ref={lightRef}
        color={sunColor}
        intensity={sunIntensity}
        position={[0, 0, 0]} // En la posición del sol
        target-position={[0, 0, 0]} // Apunta al origen
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-far={600}
        shadow-camera-left={-100}
        shadow-camera-right={100}
        shadow-camera-top={100}
        shadow-camera-bottom={-100}
        shadow-bias={-0.0001}
      />
      
      {/* Luz ambiental suave */}
      <pointLight
        color={sunColor}
        intensity={sunIntensity * 0.3}
        distance={800}
        decay={2}
      />
    </group>
  )
}

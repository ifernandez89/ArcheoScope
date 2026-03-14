'use client'

/**
 * VisibleMoon - Luna visible en el cielo nocturno
 * 
 * Características:
 * - Se posiciona opuesta al sol (180° de diferencia)
 * - Ilumina la escena con luz azulada suave
 * - Fases lunares simuladas
 * - Sombras nocturnas
 */

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface VisibleMoonProps {
  solarDirection: { x: number; y: number; z: number }
  intensity?: number
  distance?: number
}

export default function VisibleMoon({ 
  solarDirection, 
  intensity = 0.8,
  distance = 500
}: VisibleMoonProps) {
  const moonRef = useRef<THREE.Mesh>(null)
  const glowRef = useRef<THREE.Mesh>(null)
  const lightRef = useRef<THREE.DirectionalLight>(null)
  
  // Calcular posición de la luna (opuesta al sol)
  const moonPosition = useMemo(() => {
    const dir = new THREE.Vector3(solarDirection.x, solarDirection.y, solarDirection.z)
    dir.normalize()
    // Invertir dirección (180° opuesta al sol)
    dir.multiplyScalar(-1)
    return dir.multiplyScalar(distance)
  }, [solarDirection, distance])
  
  // Intensidad según altura de la luna
  const moonIntensity = useMemo(() => {
    // Luna opuesta al sol, así que usamos -solarDirection.y
    const moonHeight = -solarDirection.y
    const heightFactor = Math.max(0, Math.min(1, moonHeight * 2))
    return intensity * heightFactor
  }, [solarDirection.y, intensity])
  
  // Color de la luna (azul plateado)
  const moonColor = useMemo(() => {
    return new THREE.Color('#c0d0e8')
  }, [])
  
  // Tamaño de la luna
  const moonSize = 18
  
  // Animación sutil
  useFrame((state) => {
    const time = state.clock.elapsedTime
    
    if (moonRef.current) {
      const pulse = 1 + Math.sin(time * 0.3) * 0.015
      moonRef.current.scale.setScalar(pulse)
    }
    
    if (glowRef.current) {
      const breathe = 1 + Math.sin(time * 0.2) * 0.08
      glowRef.current.scale.setScalar(breathe)
    }
  })
  
  // Solo renderizar si la luna está sobre el horizonte (noche)
  // Luna está arriba cuando sol está abajo (y < 0)
  if (solarDirection.y > -0.1) {
    return null
  }
  
  return (
    <group position={[moonPosition.x, moonPosition.y, moonPosition.z]}>
      {/* Núcleo de la luna */}
      <mesh ref={moonRef}>
        <sphereGeometry args={[moonSize, 32, 32]} />
        <meshBasicMaterial
          color={moonColor}
          transparent
          opacity={0.9}
        />
      </mesh>
      
      {/* Glow exterior */}
      <mesh ref={glowRef} scale={1.4}>
        <sphereGeometry args={[moonSize, 24, 24]} />
        <meshBasicMaterial
          color={moonColor}
          transparent
          opacity={0.2}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          side={THREE.BackSide}
        />
      </mesh>
      
      {/* Halo exterior */}
      <mesh scale={2.0}>
        <sphereGeometry args={[moonSize, 16, 16]} />
        <meshBasicMaterial
          color={moonColor}
          transparent
          opacity={0.08}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          side={THREE.BackSide}
        />
      </mesh>
      
      {/* Luz direccional desde la luna */}
      <directionalLight
        ref={lightRef}
        color="#a0b8d8"
        intensity={moonIntensity}
        position={[0, 0, 0]}
        target-position={[0, 0, 0]}
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
      
      {/* Luz ambiental nocturna suave */}
      <pointLight
        color="#6080b0"
        intensity={moonIntensity * 0.2}
        distance={800}
        decay={2}
      />
    </group>
  )
}

'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Vector3, BufferGeometry, BufferAttribute, AdditiveBlending } from 'three'

interface WindEffectProps {
  strength: number // 0-1
  direction?: [number, number, number]
  gustFrequency?: number
  children?: React.ReactNode
}

export default function WindEffect({ 
  strength = 0.5, 
  direction = [1, 0, 0],
  gustFrequency = 0.5,
  children 
}: WindEffectProps) {
  const windVectorRef = useRef(new Vector3(...direction))
  const timeRef = useRef(0)
  
  useFrame((state, delta) => {
    timeRef.current += delta
    
    // Oscilación del viento con ruido
    const baseWind = strength
    const gust = Math.sin(timeRef.current * gustFrequency) * 0.3
    const turbulence = Math.sin(timeRef.current * 2.5) * 0.1
    
    const currentStrength = baseWind + gust + turbulence
    
    windVectorRef.current.set(...direction).multiplyScalar(currentStrength)
    
    // Dispatch wind data para que otros componentes lo usen
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('weather:wind', {
        detail: {
          vector: windVectorRef.current.clone(),
          strength: currentStrength,
          time: timeRef.current
        }
      }))
    }
  })
  
  return <>{children}</>
}

// Partículas de viento (hojas, polvo, etc.)
export function WindParticles({ strength = 0.5 }: { strength: number }) {
  const pointsRef = useRef<any>(null)
  const velocitiesRef = useRef<Float32Array>()
  
  const geometry = useRef(
    (() => {
      const count = 500
      const positions = new Float32Array(count * 3)
      const velocities = new Float32Array(count * 3)
      
      for (let i = 0; i < count; i++) {
        const i3 = i * 3
        positions[i3] = (Math.random() - 0.5) * 100
        positions[i3 + 1] = Math.random() * 20
        positions[i3 + 2] = (Math.random() - 0.5) * 100
        
        velocities[i3] = Math.random() * 2 - 1
        velocities[i3 + 1] = Math.random() * 0.5 - 0.25
        velocities[i3 + 2] = Math.random() * 2 - 1
      }
      
      velocitiesRef.current = velocities
      
      const geo = new BufferGeometry()
      geo.setAttribute('position', new BufferAttribute(positions, 3))
      return geo
    })()
  ).current
  
  useFrame((state, delta) => {
    if (!pointsRef.current || !velocitiesRef.current) return
    
    const positions = pointsRef.current.geometry.attributes.position.array as Float32Array
    const velocities = velocitiesRef.current
    const time = state.clock.elapsedTime
    
    for (let i = 0; i < positions.length; i += 3) {
      // Aplicar viento con turbulencia
      const turbulence = Math.sin(time * 2 + positions[i] * 0.1) * 0.5
      positions[i] += (velocities[i] * strength + turbulence) * delta * 3
      positions[i + 1] += velocities[i + 1] * delta
      positions[i + 2] += (velocities[i + 2] * strength + turbulence * 0.5) * delta * 3
      
      // Reset si sale del área
      if (Math.abs(positions[i]) > 50) {
        positions[i] = -Math.sign(positions[i]) * 50
      }
      if (positions[i + 1] < 0 || positions[i + 1] > 20) {
        positions[i + 1] = Math.random() * 20
      }
      if (Math.abs(positions[i + 2]) > 50) {
        positions[i + 2] = -Math.sign(positions[i + 2]) * 50
      }
    }
    
    pointsRef.current.geometry.attributes.position.needsUpdate = true
  })
  
  return (
    <points ref={pointsRef} geometry={geometry}>
      <pointsMaterial
        size={0.15}
        color="#d4c5a0"
        transparent
        opacity={0.4}
        blending={AdditiveBlending}
        depthWrite={false}
      />
    </points>
  )
}

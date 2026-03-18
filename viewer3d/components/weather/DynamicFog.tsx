'use client'

import { useRef, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { FogExp2, Fog, BufferGeometry, BufferAttribute, NormalBlending } from 'three'

interface DynamicFogProps {
  density: number // 0-1
  color?: string
  near?: number
  far?: number
  animated?: boolean
}

export default function DynamicFog({ 
  density = 0.5, 
  color = '#cccccc',
  near = 10,
  far = 100,
  animated = true
}: DynamicFogProps) {
  const { scene } = useThree()
  const targetDensityRef = useRef(density)
  const currentDensityRef = useRef(0)
  const timeRef = useRef(0)
  
  // Actualizar fog en la escena
  useEffect(() => {
    if (!scene.fog) {
      scene.fog = new FogExp2(color, 0)
    }
    targetDensityRef.current = density
  }, [scene, density, color])
  
  useFrame((state, delta) => {
    if (!scene.fog) return
    
    timeRef.current += delta
    
    // Transición suave de densidad
    const transitionSpeed = 0.5
    currentDensityRef.current += (targetDensityRef.current - currentDensityRef.current) * transitionSpeed * delta
    
    // Animación de pulsación si está habilitada
    let finalDensity = currentDensityRef.current
    if (animated) {
      const pulse = Math.sin(timeRef.current * 0.3) * 0.1
      finalDensity = Math.max(0, currentDensityRef.current + pulse)
    }
    
    // Aplicar a la niebla
    if (scene.fog instanceof FogExp2) {
      scene.fog.density = finalDensity * 0.02 // Escalar para valores razonables
      scene.fog.color.set(color)
    } else if (scene.fog instanceof Fog) {
      scene.fog.near = near
      scene.fog.far = far - (finalDensity * 50)
      scene.fog.color.set(color)
    }
  })
  
  return null
}

// Partículas de niebla volumétrica
export function FogParticles({ density = 0.5 }: { density: number }) {
  const pointsRef = useRef<any>(null)
  
  const geometry = useRef(
    (() => {
      const count = 1000
      const positions = new Float32Array(count * 3)
      const scales = new Float32Array(count)
      
      for (let i = 0; i < count; i++) {
        const i3 = i * 3
        positions[i3] = (Math.random() - 0.5) * 100
        positions[i3 + 1] = Math.random() * 30
        positions[i3 + 2] = (Math.random() - 0.5) * 100
        scales[i] = Math.random() * 2 + 1
      }
      
      const geo = new BufferGeometry()
      geo.setAttribute('position', new BufferAttribute(positions, 3))
      geo.setAttribute('scale', new BufferAttribute(scales, 1))
      return geo
    })()
  ).current
  
  useFrame((state, delta) => {
    if (!pointsRef.current) return
    
    const positions = pointsRef.current.geometry.attributes.position.array as Float32Array
    const time = state.clock.elapsedTime
    
    for (let i = 0; i < positions.length; i += 3) {
      // Movimiento lento y ondulante
      positions[i] += Math.sin(time * 0.2 + positions[i + 2] * 0.1) * delta * 0.5
      positions[i + 2] += Math.cos(time * 0.15 + positions[i] * 0.1) * delta * 0.5
      
      // Mantener dentro del área
      if (Math.abs(positions[i]) > 50) {
        positions[i] = -Math.sign(positions[i]) * 50
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
        size={3}
        color="#e0e0e0"
        transparent
        opacity={density * 0.3}
        blending={NormalBlending}
        depthWrite={false}
        sizeAttenuation={true}
      />
    </points>
  )
}

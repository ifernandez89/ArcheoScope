'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

export default function SnowParticles() {
  const pointsRef = useRef<THREE.Points>(null)
  
  // Generar partículas de nieve
  const [positions, velocities] = useMemo(() => {
    const count = 2000
    const pos = new Float32Array(count * 3)
    const vel = new Float32Array(count * 3)
    
    for (let i = 0; i < count; i++) {
      const i3 = i * 3
      
      // Posición inicial aleatoria
      pos[i3] = (Math.random() - 0.5) * 100
      pos[i3 + 1] = Math.random() * 50 + 10
      pos[i3 + 2] = (Math.random() - 0.5) * 100
      
      // Velocidad de caída
      vel[i3] = (Math.random() - 0.5) * 0.1 // Deriva horizontal
      vel[i3 + 1] = -Math.random() * 0.3 - 0.1 // Caída
      vel[i3 + 2] = (Math.random() - 0.5) * 0.1 // Deriva horizontal
    }
    
    return [pos, vel]
  }, [])
  
  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry()
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    return geo
  }, [positions])
  
  const material = useMemo(() => {
    return new THREE.PointsMaterial({
      color: '#ffffff',
      size: 0.15,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    })
  }, [])
  
  // Animar caída de nieve
  useFrame(() => {
    if (!pointsRef.current) return
    
    const pos = pointsRef.current.geometry.attributes.position.array as Float32Array
    
    for (let i = 0; i < pos.length; i += 3) {
      // Aplicar velocidad
      pos[i] += velocities[i]
      pos[i + 1] += velocities[i + 1]
      pos[i + 2] += velocities[i + 2]
      
      // Resetear si cae muy bajo
      if (pos[i + 1] < 0) {
        pos[i + 1] = 50 + Math.random() * 10
        pos[i] = (Math.random() - 0.5) * 100
        pos[i + 2] = (Math.random() - 0.5) * 100
      }
      
      // Mantener dentro del área
      if (Math.abs(pos[i]) > 50) {
        pos[i] = (Math.random() - 0.5) * 100
      }
      if (Math.abs(pos[i + 2]) > 50) {
        pos[i + 2] = (Math.random() - 0.5) * 100
      }
    }
    
    pointsRef.current.geometry.attributes.position.needsUpdate = true
  })
  
  return <points ref={pointsRef} geometry={geometry} material={material} />
}

'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface RainParticlesProps {
  intensity?: 'light' | 'moderate' | 'heavy'
}

export default function RainParticles({ intensity = 'light' }: RainParticlesProps) {
  const pointsRef = useRef<THREE.Points>(null)
  
  // Configuración según intensidad — reducida 50% para mejor rendimiento mobile
  const config = useMemo(() => {
    switch (intensity) {
      case 'light':
        return { count: 2000, speed: 1.2, size: 0.06, opacity: 0.5, spread: 100 }
      case 'moderate':
        return { count: 4000, speed: 1.8, size: 0.08, opacity: 0.65, spread: 100 }
      case 'heavy':
        return { count: 8000, speed: 2.5, size: 0.1, opacity: 0.8, spread: 100 }
    }
  }, [intensity])
  
  // Generar partículas de lluvia
  const [positions, velocities] = useMemo(() => {
    const pos = new Float32Array(config.count * 3)
    const vel = new Float32Array(config.count * 3)
    
    for (let i = 0; i < config.count; i++) {
      const i3 = i * 3
      
      // Posición inicial aleatoria - SIEMPRE desde arriba
      pos[i3] = (Math.random() - 0.5) * config.spread
      pos[i3 + 1] = Math.random() * 40 + 20 // Entre 20 y 60 unidades de altura
      pos[i3 + 2] = (Math.random() - 0.5) * config.spread
      
      // Velocidad de caída - SIEMPRE hacia abajo (Y negativo)
      vel[i3] = (Math.random() - 0.5) * 0.15 // Deriva horizontal muy leve
      vel[i3 + 1] = -(Math.random() * 0.5 + config.speed) // Caída hacia abajo
      vel[i3 + 2] = (Math.random() - 0.5) * 0.15 // Deriva horizontal muy leve
    }
    
    return [pos, vel]
  }, [config])
  
  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry()
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    return geo
  }, [positions])
  
  const material = useMemo(() => {
    return new THREE.PointsMaterial({
      color: '#88aaff', // Azul claro para lluvia
      size: config.size,
      transparent: true,
      opacity: config.opacity,
      blending: THREE.NormalBlending,
      depthWrite: false
    })
  }, [config])
  
  // Animar caída de lluvia
  useFrame(() => {
    if (!pointsRef.current) return
    
    const pos = pointsRef.current.geometry.attributes.position.array as Float32Array
    
    for (let i = 0; i < pos.length; i += 3) {
      // Aplicar velocidad
      pos[i] += velocities[i]
      pos[i + 1] += velocities[i + 1] // Siempre negativo, cae hacia abajo
      pos[i + 2] += velocities[i + 2]
      
      // Resetear si cae muy bajo - VOLVER ARRIBA
      if (pos[i + 1] < 0) {
        pos[i + 1] = 50 + Math.random() * 10 // Volver arriba
        pos[i] = (Math.random() - 0.5) * config.spread
        pos[i + 2] = (Math.random() - 0.5) * config.spread
      }
      
      // Mantener dentro del área horizontal
      if (Math.abs(pos[i]) > config.spread / 2) {
        pos[i] = (Math.random() - 0.5) * config.spread
      }
      if (Math.abs(pos[i + 2]) > config.spread / 2) {
        pos[i + 2] = (Math.random() - 0.5) * config.spread
      }
    }
    
    pointsRef.current.geometry.attributes.position.needsUpdate = true
  })
  
  return <points ref={pointsRef} geometry={geometry} material={material} />
}

'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface TornadoEffectProps {
  position?: [number, number, number]
  intensity?: number // 0-1
  height?: number
}

export default function TornadoEffect({ 
  position = [0, 0, 0], 
  intensity = 0.7,
  height = 40
}: TornadoEffectProps) {
  const particlesRef = useRef<THREE.Points>(null)
  const timeRef = useRef(0)
  
  // Generar partículas en espiral
  const [positions, velocities, radii, heights] = useMemo(() => {
    const count = 2000
    const pos = new Float32Array(count * 3)
    const vel = new Float32Array(count * 3)
    const rad = new Float32Array(count)
    const hgt = new Float32Array(count)
    
    for (let i = 0; i < count; i++) {
      const i3 = i * 3
      const t = i / count
      
      // Altura en el tornado
      const h = t * height
      hgt[i] = h
      
      // Radio aumenta con la altura (forma de embudo)
      const radius = 1 + (h / height) * 8
      rad[i] = radius
      
      // Ángulo inicial aleatorio
      const angle = Math.random() * Math.PI * 2
      
      pos[i3] = position[0] + Math.cos(angle) * radius
      pos[i3 + 1] = position[1] + h
      pos[i3 + 2] = position[2] + Math.sin(angle) * radius
      
      // Velocidad angular
      vel[i3] = Math.random() * 2 + 1 // velocidad de rotación
      vel[i3 + 1] = Math.random() * 0.5 + 0.2 // velocidad vertical
      vel[i3 + 2] = 0
    }
    
    return [pos, vel, rad, hgt]
  }, [position, height])
  
  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry()
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    return geo
  }, [positions])
  
  const material = useMemo(() => {
    return new THREE.PointsMaterial({
      color: '#8b7355',
      size: 0.3,
      transparent: true,
      opacity: 0.6,
      blending: THREE.NormalBlending,
      depthWrite: false
    })
  }, [])
  
  useFrame((state, delta) => {
    if (!particlesRef.current) return
    
    timeRef.current += delta
    const pos = particlesRef.current.geometry.attributes.position.array as Float32Array
    
    for (let i = 0; i < pos.length / 3; i++) {
      const i3 = i * 3
      const currentHeight = heights[i]
      const currentRadius = radii[i]
      const angularVelocity = velocities[i3]
      
      // Calcular nueva posición en espiral
      const angle = timeRef.current * angularVelocity * intensity
      const x = position[0] + Math.cos(angle) * currentRadius
      const z = position[2] + Math.sin(angle) * currentRadius
      
      // Movimiento vertical con oscilación
      heights[i] += velocities[i3 + 1] * delta * intensity * 10
      
      // Reset si llega arriba
      if (heights[i] > height) {
        heights[i] = 0
        radii[i] = 1
      }
      
      // Actualizar radio (crece con altura)
      radii[i] = 1 + (heights[i] / height) * 8
      
      // Aplicar posición
      pos[i3] = x + Math.sin(timeRef.current * 3 + i * 0.1) * 0.5 // turbulencia
      pos[i3 + 1] = position[1] + heights[i]
      pos[i3 + 2] = z + Math.cos(timeRef.current * 3 + i * 0.1) * 0.5 // turbulencia
    }
    
    particlesRef.current.geometry.attributes.position.needsUpdate = true
  })
  
  return (
    <>
      <points ref={particlesRef} geometry={geometry} material={material} />
      
      {/* Núcleo oscuro del tornado */}
      <mesh position={position}>
        <cylinderGeometry args={[0.5, 2, height, 16, 20, true]} />
        <meshBasicMaterial
          color="#4a4a4a"
          transparent
          opacity={0.3}
          side={THREE.DoubleSide}
          blending={THREE.NormalBlending}
        />
      </mesh>
    </>
  )
}

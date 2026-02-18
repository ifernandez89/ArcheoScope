'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface TornadoEffectProps {
  position?: [number, number, number]
  intensity?: number // 0-1
  height?: number
}

// Función de ruido simple (Perlin-like)
function noise(x: number): number {
  return Math.sin(x * 1.5) * Math.cos(x * 0.7) * 0.5 + 0.5
}

export default function TornadoEffect({ 
  position = [0, 0, 0], 
  intensity = 0.7,
  height = 40
}: TornadoEffectProps) {
  const particlesRef = useRef<THREE.Points>(null)
  const dustParticlesRef = useRef<THREE.Points>(null)
  const timeRef = useRef(0)
  
  // Generar partículas principales del tornado (columna)
  const [positions, velocities, radii, heights, angles] = useMemo(() => {
    const count = 3000 // Más partículas para densidad
    const pos = new Float32Array(count * 3)
    const vel = new Float32Array(count * 3)
    const rad = new Float32Array(count)
    const hgt = new Float32Array(count)
    const ang = new Float32Array(count)
    
    for (let i = 0; i < count; i++) {
      const i3 = i * 3
      const t = i / count
      
      // Altura en el tornado
      const h = t * height
      hgt[i] = h
      
      // Radio con taper (base estrecha, arriba ancho) + ruido
      const baseRadius = 1.5
      const taperFactor = 0.25 // Ensanchamiento
      const noiseVariation = noise(h * 0.1) * 0.3
      const radius = baseRadius + (h / height) * height * taperFactor + noiseVariation
      rad[i] = radius
      
      // Ángulo inicial aleatorio
      const angle = Math.random() * Math.PI * 2
      ang[i] = angle
      
      pos[i3] = position[0] + Math.cos(angle) * radius
      pos[i3 + 1] = position[1] + h
      pos[i3 + 2] = position[2] + Math.sin(angle) * radius
      
      // Velocidad angular (más rápida abajo)
      vel[i3] = (2 + Math.random()) * (1 - t * 0.5) // Rotación
      vel[i3 + 1] = Math.random() * 0.8 + 0.4 // Velocidad vertical
      vel[i3 + 2] = 0.3 + Math.random() * 0.2 // Succión hacia centro
    }
    
    return [pos, vel, rad, hgt, ang]
  }, [position, height])
  
  // Generar partículas de polvo en la base (falda de debris)
  const [dustPositions, dustVelocities] = useMemo(() => {
    const count = 1500
    const pos = new Float32Array(count * 3)
    const vel = new Float32Array(count * 3)
    
    for (let i = 0; i < count; i++) {
      const i3 = i * 3
      const angle = Math.random() * Math.PI * 2
      const radius = 2 + Math.random() * 12 // Radio más grande
      
      pos[i3] = position[0] + Math.cos(angle) * radius
      pos[i3 + 1] = position[1] + Math.random() * 5 // Baja altura
      pos[i3 + 2] = position[2] + Math.sin(angle) * radius
      
      vel[i3] = Math.random() * 3 + 1 // Rotación horizontal
      vel[i3 + 1] = Math.random() * 0.3 // Poco movimiento vertical
      vel[i3 + 2] = 0
    }
    
    return [pos, vel]
  }, [position])
  
  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry()
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    return geo
  }, [positions])
  
  const dustGeometry = useMemo(() => {
    const geo = new THREE.BufferGeometry()
    geo.setAttribute('position', new THREE.BufferAttribute(dustPositions, 3))
    return geo
  }, [dustPositions])
  
  // Material con gradiente (centro oscuro, bordes translúcidos)
  const material = useMemo(() => {
    return new THREE.PointsMaterial({
      color: '#4a3a2a',
      size: 0.4,
      transparent: true,
      opacity: 0.7,
      blending: THREE.NormalBlending,
      depthWrite: false
    })
  }, [])
  
  const dustMaterial = useMemo(() => {
    return new THREE.PointsMaterial({
      color: '#8b7355',
      size: 0.6,
      transparent: true,
      opacity: 0.5,
      blending: THREE.NormalBlending,
      depthWrite: false
    })
  }, [])
  
  useFrame((state, delta) => {
    if (!particlesRef.current || !dustParticlesRef.current) return
    
    timeRef.current += delta
    const pos = particlesRef.current.geometry.attributes.position.array as Float32Array
    const dustPos = dustParticlesRef.current.geometry.attributes.position.array as Float32Array
    
    // Actualizar partículas principales
    for (let i = 0; i < pos.length / 3; i++) {
      const i3 = i * 3
      const currentHeight = heights[i]
      const currentRadius = radii[i]
      const angularVelocity = velocities[i3]
      const suctionForce = velocities[i3 + 2]
      
      // Rotación con turbulencia
      const turbulence = Math.sin(timeRef.current * 3 + currentHeight * 0.1) * 0.15
      angles[i] += (angularVelocity + turbulence) * delta * intensity * 3
      
      // Succión hacia el centro
      const targetRadius = currentRadius * (0.8 + Math.sin(timeRef.current * 2 + i * 0.1) * 0.2)
      
      // Calcular posición en espiral con succión
      const x = position[0] + Math.cos(angles[i]) * targetRadius
      const z = position[2] + Math.sin(angles[i]) * targetRadius
      
      // Movimiento vertical con oscilación
      heights[i] += velocities[i3 + 1] * delta * intensity * 12
      
      // Reset si llega arriba
      if (heights[i] > height) {
        heights[i] = 0
        radii[i] = 1.5 + Math.random() * 0.5
        angles[i] = Math.random() * Math.PI * 2
      }
      
      // Actualizar radio con taper + ruido
      const baseRadius = 1.5
      const taperFactor = 0.25
      const noiseVar = noise(heights[i] * 0.1 + timeRef.current) * 0.4
      radii[i] = baseRadius + (heights[i] / height) * height * taperFactor + noiseVar
      
      // Vibración lateral
      const lateralVibration = Math.sin(timeRef.current * 5 + i * 0.5) * 0.3
      
      // Aplicar posición
      pos[i3] = x + lateralVibration
      pos[i3 + 1] = position[1] + heights[i]
      pos[i3 + 2] = z + lateralVibration * 0.5
    }
    
    // Actualizar polvo en la base
    for (let i = 0; i < dustPos.length / 3; i++) {
      const i3 = i * 3
      const angle = timeRef.current * dustVelocities[i3] * intensity
      const radius = 2 + Math.sin(timeRef.current + i) * 10
      
      dustPos[i3] = position[0] + Math.cos(angle) * radius
      dustPos[i3 + 1] = position[1] + Math.random() * 5
      dustPos[i3 + 2] = position[2] + Math.sin(angle) * radius
    }
    
    particlesRef.current.geometry.attributes.position.needsUpdate = true
    dustParticlesRef.current.geometry.attributes.position.needsUpdate = true
  })
  
  return (
    <>
      {/* Partículas principales del tornado */}
      <points ref={particlesRef} geometry={geometry} material={material} />
      
      {/* Polvo en la base (falda de debris) */}
      <points ref={dustParticlesRef} geometry={dustGeometry} material={dustMaterial} />
      
      {/* Flash interno ocasional */}
      {Math.sin(timeRef.current * 10) > 0.95 && (
        <pointLight
          position={[position[0], position[1] + height * 0.5, position[2]]}
          intensity={2}
          distance={20}
          color="#a0c0ff"
        />
      )}
    </>
  )
}

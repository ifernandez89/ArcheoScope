import { useRef, useMemo } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { Sky, Cloud, Stars } from '@react-three/drei'
import * as THREE from 'three'

interface DynamicEnvironmentProps {
  timeOfDay?: number // 0-24 horas
  cloudCoverage?: number // 0-1
  weatherType?: 'clear' | 'cloudy' | 'rainy' | 'stormy'
  enableStars?: boolean
  enableClouds?: boolean
}

/**
 * Entorno dinámico con ciclo día/noche
 */
export function DynamicEnvironment({
  timeOfDay = 12,
  cloudCoverage = 0.3,
  weatherType = 'clear',
  enableStars = true,
  enableClouds = true
}: DynamicEnvironmentProps) {
  const { scene } = useThree()
  
  // Calcular posición del sol basado en hora
  const sunPosition = useMemo(() => {
    const angle = (timeOfDay / 24) * Math.PI * 2 - Math.PI / 2
    return new THREE.Vector3(
      Math.cos(angle) * 100,
      Math.sin(angle) * 100,
      0
    )
  }, [timeOfDay])
  
  // Calcular color del cielo
  const skyColor = useMemo(() => {
    if (timeOfDay >= 6 && timeOfDay < 8) {
      // Amanecer
      return new THREE.Color(0xff9966)
    } else if (timeOfDay >= 8 && timeOfDay < 18) {
      // Día
      return new THREE.Color(0x87ceeb)
    } else if (timeOfDay >= 18 && timeOfDay < 20) {
      // Atardecer
      return new THREE.Color(0xff6633)
    } else {
      // Noche
      return new THREE.Color(0x000033)
    }
  }, [timeOfDay])
  
  // Actualizar color de fondo
  useFrame(() => {
    scene.background = skyColor
  })
  
  const isNight = timeOfDay < 6 || timeOfDay > 20
  
  return (
    <group>
      {/* Cielo procedural */}
      <Sky
        sunPosition={sunPosition}
        turbidity={weatherType === 'clear' ? 2 : 10}
        rayleigh={weatherType === 'clear' ? 0.5 : 2}
        mieCoefficient={0.005}
        mieDirectionalG={0.8}
      />
      
      {/* Estrellas (solo de noche) */}
      {enableStars && isNight && (
        <Stars
          radius={300}
          depth={50}
          count={5000}
          factor={4}
          saturation={0}
          fade
          speed={0.5}
        />
      )}
      
      {/* Nubes */}
      {enableClouds && cloudCoverage > 0 && (
        <Clouds coverage={cloudCoverage} weatherType={weatherType} />
      )}
      
      {/* Luz direccional del sol */}
      <directionalLight
        position={sunPosition}
        intensity={isNight ? 0.1 : 1.5}
        color={isNight ? '#4466ff' : '#ffffff'}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-far={500}
        shadow-camera-left={-100}
        shadow-camera-right={100}
        shadow-camera-top={100}
        shadow-camera-bottom={-100}
      />
      
      {/* Luz ambiental */}
      <ambientLight intensity={isNight ? 0.05 : 0.3} color={skyColor} />
      
      {/* Luz hemisférica */}
      <hemisphereLight
        skyColor={skyColor}
        groundColor={new THREE.Color(0x444444)}
        intensity={isNight ? 0.1 : 0.5}
      />
    </group>
  )
}

/**
 * Sistema de nubes procedurales
 */
function Clouds({ 
  coverage, 
  weatherType 
}: { 
  coverage: number
  weatherType: string
}) {
  const cloudCount = Math.floor(coverage * 20)
  const clouds = useMemo(() => {
    return Array.from({ length: cloudCount }, (_, i) => ({
      position: [
        (Math.random() - 0.5) * 200,
        20 + Math.random() * 10,
        (Math.random() - 0.5) * 200
      ] as [number, number, number],
      speed: 0.1 + Math.random() * 0.2,
      scale: 3 + Math.random() * 2
    }))
  }, [cloudCount])
  
  return (
    <group>
      {clouds.map((cloud, i) => (
        <Cloud
          key={i}
          position={cloud.position}
          speed={cloud.speed}
          opacity={weatherType === 'stormy' ? 0.8 : 0.5}
          color={weatherType === 'stormy' ? '#666666' : '#ffffff'}
          segments={20}
          bounds={[cloud.scale, cloud.scale / 2, cloud.scale]}
        />
      ))}
    </group>
  )
}

/**
 * Clima procedural con partículas
 */
export function ProceduralWeather({ type }: { type: 'rain' | 'snow' | 'none' }) {
  const particlesRef = useRef<THREE.Points>(null)
  
  const particleCount = type === 'none' ? 0 : 1000
  
  const particles = useMemo(() => {
    const positions = new Float32Array(particleCount * 3)
    const velocities = new Float32Array(particleCount)
    
    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 100
      positions[i * 3 + 1] = Math.random() * 50
      positions[i * 3 + 2] = (Math.random() - 0.5) * 100
      
      velocities[i] = type === 'rain' ? 0.5 + Math.random() * 0.5 : 0.1 + Math.random() * 0.1
    }
    
    return { positions, velocities }
  }, [particleCount, type])
  
  useFrame((state, delta) => {
    if (!particlesRef.current || type === 'none') return
    
    const positions = particlesRef.current.geometry.attributes.position.array as Float32Array
    
    for (let i = 0; i < particleCount; i++) {
      positions[i * 3 + 1] -= particles.velocities[i] * delta * 10
      
      // Reset si llega al suelo
      if (positions[i * 3 + 1] < 0) {
        positions[i * 3 + 1] = 50
      }
    }
    
    particlesRef.current.geometry.attributes.position.needsUpdate = true
  })
  
  if (type === 'none') return null
  
  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={particleCount}
          array={particles.positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={type === 'rain' ? 0.1 : 0.3}
        color={type === 'rain' ? '#4488ff' : '#ffffff'}
        transparent
        opacity={0.6}
        sizeAttenuation
      />
    </points>
  )
}

/**
 * Iluminación volumétrica (God Rays)
 */
export function VolumetricLighting({ sunPosition }: { sunPosition: THREE.Vector3 }) {
  return (
    <group>
      {/* Spotlight para simular rayos de luz */}
      <spotLight
        position={sunPosition}
        angle={0.3}
        penumbra={0.5}
        intensity={0.5}
        castShadow
        shadow-mapSize-width={1024}
        shadow-mapSize-height={1024}
      />
      
      {/* Mesh para visualizar rayos */}
      <mesh position={sunPosition} rotation={[0, 0, Math.PI / 4]}>
        <coneGeometry args={[20, 100, 32, 1, true]} />
        <meshBasicMaterial
          color="#ffaa00"
          transparent
          opacity={0.1}
          side={THREE.DoubleSide}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
        />
      </mesh>
    </group>
  )
}

/**
 * Hook para ciclo día/noche automático
 */
export function useDayNightCycle(speed: number = 1) {
  const timeRef = useRef(12) // Empezar al mediodía
  
  useFrame((state, delta) => {
    timeRef.current += delta * speed / 60 // speed = minutos por segundo real
    if (timeRef.current >= 24) {
      timeRef.current -= 24
    }
  })
  
  return timeRef.current
}

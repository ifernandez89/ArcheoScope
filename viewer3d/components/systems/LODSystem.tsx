import { useRef, useMemo } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

interface LODSystemProps {
  children: React.ReactNode
  position?: [number, number, number]
  distances?: number[] // [high, medium, low] distances
  scales?: number[] // [high, medium, low] scales for optimization
}

/**
 * Sistema LOD (Level of Detail) automático
 * Ajusta la calidad de renderizado basado en distancia a cámara
 */
export function LODSystem({ 
  children, 
  position = [0, 0, 0],
  distances = [10, 50, 200], // distancias para cambiar LOD
  scales = [1, 0.8, 0.5] // escalas de detalle
}: LODSystemProps) {
  const groupRef = useRef<THREE.Group>(null)
  const { camera } = useThree()
  const lodLevel = useRef(0)

  useFrame(() => {
    if (!groupRef.current) return

    const distance = camera.position.distanceTo(groupRef.current.position)
    
    let newLodLevel = 0
    if (distance > distances[2]) {
      newLodLevel = 3 // muy lejos - no renderizar o mínimo detalle
    } else if (distance > distances[1]) {
      newLodLevel = 2 // lejos - bajo detalle
    } else if (distance > distances[0]) {
      newLodLevel = 1 // medio - detalle medio
    } else {
      newLodLevel = 0 // cerca - alto detalle
    }

    // Solo actualizar si cambió el nivel
    if (newLodLevel !== lodLevel.current) {
      lodLevel.current = newLodLevel
      
      // Ajustar visibilidad y escala según LOD
      if (groupRef.current) {
        groupRef.current.visible = newLodLevel < 3
        
        if (newLodLevel < 3) {
          const scale = scales[newLodLevel] || 1
          groupRef.current.scale.setScalar(scale)
        }
      }
    }
  })

  return (
    <group ref={groupRef} position={position}>
      {children}
    </group>
  )
}

interface PlanetLODProps {
  position: [number, number, number]
  radius: number
  segments?: { high: number; medium: number; low: number }
  texture?: THREE.Texture
  children?: React.ReactNode
}

/**
 * Sistema LOD específico para planetas
 * Cambia la geometría según distancia
 */
export function PlanetLOD({ 
  position, 
  radius, 
  segments = { high: 64, medium: 32, low: 16 },
  texture,
  children 
}: PlanetLODProps) {
  const meshRef = useRef<THREE.Mesh>(null)
  const { camera } = useThree()
  
  // Crear geometrías con diferentes niveles de detalle
  const geometries = useMemo(() => ({
    high: new THREE.SphereGeometry(radius, segments.high, segments.high),
    medium: new THREE.SphereGeometry(radius, segments.medium, segments.medium),
    low: new THREE.SphereGeometry(radius, segments.low, segments.low)
  }), [radius, segments])

  useFrame(() => {
    if (!meshRef.current) return

    const distance = camera.position.distanceTo(new THREE.Vector3(...position))
    
    // Cambiar geometría según distancia
    let targetGeometry = geometries.high
    if (distance > 100) {
      targetGeometry = geometries.low
    } else if (distance > 30) {
      targetGeometry = geometries.medium
    }

    if (meshRef.current.geometry !== targetGeometry) {
      meshRef.current.geometry = targetGeometry
    }
  })

  return (
    <mesh ref={meshRef} position={position}>
      <meshStandardMaterial map={texture} />
      {children}
    </mesh>
  )
}

/**
 * Hook para obtener el nivel LOD actual basado en distancia
 */
export function useLODLevel(position: THREE.Vector3, distances: number[] = [10, 50, 200]) {
  const { camera } = useThree()
  const lodLevel = useRef(0)

  useFrame(() => {
    const distance = camera.position.distanceTo(position)
    
    if (distance > distances[2]) {
      lodLevel.current = 3
    } else if (distance > distances[1]) {
      lodLevel.current = 2
    } else if (distance > distances[0]) {
      lodLevel.current = 1
    } else {
      lodLevel.current = 0
    }
  })

  return lodLevel.current
}

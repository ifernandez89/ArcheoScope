import { useRef, useMemo } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

interface OptimizedPlanetProps {
  radius: number
  texture: THREE.Texture
  color?: string
  roughness?: number
  metalness?: number
  emissive?: string
  emissiveIntensity?: number
  rotationSpeed?: number
  retrograde?: boolean
}

/**
 * Planeta optimizado con LOD automático
 * Cambia la geometría según distancia a cámara
 */
export function OptimizedPlanet({
  radius,
  texture,
  color = '#ffffff',
  roughness = 0.95,
  metalness = 0.05,
  emissive,
  emissiveIntensity = 0,
  rotationSpeed = 0,
  retrograde = false
}: OptimizedPlanetProps) {
  const meshRef = useRef<THREE.Mesh>(null)
  const { camera } = useThree()
  
  // Vector reutilizable para evitar crear objetos cada frame
  const tempVector = useMemo(() => new THREE.Vector3(), [])
  
  // Crear geometrías con diferentes niveles de detalle
  const geometries = useMemo(() => ({
    high: new THREE.SphereGeometry(radius, 64, 64),
    medium: new THREE.SphereGeometry(radius, 32, 32),
    low: new THREE.SphereGeometry(radius, 16, 16),
    veryLow: new THREE.SphereGeometry(radius, 8, 8)
  }), [radius])

  // Material optimizado
  const material = useMemo(() => 
    new THREE.MeshStandardMaterial({
      map: texture,
      color,
      roughness,
      metalness,
      emissive: emissive ? new THREE.Color(emissive) : undefined,
      emissiveIntensity
    }),
    [texture, color, roughness, metalness, emissive, emissiveIntensity]
  )

  useFrame((state, delta) => {
    if (!meshRef.current) return

    // Rotación axial
    if (rotationSpeed > 0) {
      meshRef.current.rotation.y += delta * rotationSpeed * (retrograde ? -1 : 1)
    }

    // LOD basado en distancia - reutilizar vector
    const distance = camera.position.distanceTo(meshRef.current.getWorldPosition(tempVector))
    
    let targetGeometry = geometries.high
    if (distance > 200) {
      targetGeometry = geometries.veryLow
    } else if (distance > 100) {
      targetGeometry = geometries.low
    } else if (distance > 30) {
      targetGeometry = geometries.medium
    }

    if (meshRef.current.geometry !== targetGeometry) {
      meshRef.current.geometry = targetGeometry
    }
  })

  return (
    <mesh ref={meshRef} geometry={geometries.high} material={material} />
  )
}

interface OptimizedAtmosphereProps {
  radius: number
  color: string
  opacity: number
  scale?: number
}

/**
 * Atmósfera optimizada con LOD
 */
export function OptimizedAtmosphere({
  radius,
  color,
  opacity,
  scale = 1.05
}: OptimizedAtmosphereProps) {
  const meshRef = useRef<THREE.Mesh>(null)
  const { camera } = useThree()
  
  // Vector reutilizable
  const tempVector = useMemo(() => new THREE.Vector3(), [])

  const geometries = useMemo(() => ({
    high: new THREE.SphereGeometry(radius, 32, 32),
    medium: new THREE.SphereGeometry(radius, 16, 16),
    low: new THREE.SphereGeometry(radius, 8, 8)
  }), [radius])

  const material = useMemo(() =>
    new THREE.MeshStandardMaterial({
      color,
      transparent: true,
      opacity,
      roughness: 0.8,
      metalness: 0.0,
      side: THREE.DoubleSide
    }),
    [color, opacity]
  )

  useFrame(() => {
    if (!meshRef.current) return

    const distance = camera.position.distanceTo(meshRef.current.getWorldPosition(tempVector))
    
    // Ocultar atmósfera si está muy lejos
    if (distance > 300) {
      meshRef.current.visible = false
      return
    }
    
    meshRef.current.visible = true
    
    let targetGeometry = geometries.high
    if (distance > 100) {
      targetGeometry = geometries.low
    } else if (distance > 50) {
      targetGeometry = geometries.medium
    }

    if (meshRef.current.geometry !== targetGeometry) {
      meshRef.current.geometry = targetGeometry
    }
  })

  return (
    <mesh ref={meshRef} scale={scale} geometry={geometries.high} material={material} />
  )
}

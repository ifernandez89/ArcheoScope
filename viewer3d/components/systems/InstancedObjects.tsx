import { useRef, useMemo, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface InstancedObjectsProps {
  positions: Array<[number, number, number]>
  geometry?: THREE.BufferGeometry
  material?: THREE.Material
  scale?: number
  color?: string
}

/**
 * Sistema de renderizado masivo con InstancedMesh
 * Dibuja miles de objetos con un solo draw call
 */
export function InstancedObjects({ 
  positions, 
  geometry,
  material,
  scale = 1,
  color = '#ffffff'
}: InstancedObjectsProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null)
  
  const count = positions.length
  
  // Crear geometría y material por defecto si no se proveen
  const defaultGeometry = useMemo(() => 
    geometry || new THREE.SphereGeometry(0.1, 8, 8), 
    [geometry]
  )
  
  const defaultMaterial = useMemo(() => 
    material || new THREE.MeshStandardMaterial({ color }), 
    [material, color]
  )

  // Configurar posiciones de instancias
  useEffect(() => {
    if (!meshRef.current) return

    const tempObject = new THREE.Object3D()
    
    positions.forEach((position, i) => {
      tempObject.position.set(...position)
      tempObject.scale.setScalar(scale)
      tempObject.updateMatrix()
      meshRef.current!.setMatrixAt(i, tempObject.matrix)
    })
    
    meshRef.current.instanceMatrix.needsUpdate = true
  }, [positions, scale])

  return (
    <instancedMesh 
      ref={meshRef} 
      args={[defaultGeometry, defaultMaterial, count]}
      frustumCulled
    />
  )
}

interface InstancedMarkersProps {
  sites: Array<{
    position: [number, number, number]
    color?: string
    scale?: number
  }>
  baseScale?: number
}

/**
 * Marcadores instanciados para sitios arqueológicos
 * Optimizado para renderizar cientos de marcadores
 */
export function InstancedMarkers({ sites, baseScale = 0.05 }: InstancedMarkersProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null)
  const count = sites.length

  const geometry = useMemo(() => 
    new THREE.ConeGeometry(1, 2, 8), 
    []
  )
  
  const material = useMemo(() => 
    new THREE.MeshStandardMaterial({ 
      color: '#ff6b6b',
      emissive: '#ff0000',
      emissiveIntensity: 0.3
    }), 
    []
  )

  useEffect(() => {
    if (!meshRef.current) return

    const tempObject = new THREE.Object3D()
    const tempColor = new THREE.Color()
    
    sites.forEach((site, i) => {
      tempObject.position.set(...site.position)
      tempObject.scale.setScalar((site.scale || 1) * baseScale)
      tempObject.rotation.x = Math.PI // Apuntar hacia abajo
      tempObject.updateMatrix()
      
      meshRef.current!.setMatrixAt(i, tempObject.matrix)
      
      // Color individual si se especifica
      if (site.color) {
        tempColor.set(site.color)
        meshRef.current!.setColorAt(i, tempColor)
      }
    })
    
    meshRef.current.instanceMatrix.needsUpdate = true
    if (meshRef.current.instanceColor) {
      meshRef.current.instanceColor.needsUpdate = true
    }
  }, [sites, baseScale])

  // Animación sutil de flotación
  useFrame(({ clock }) => {
    if (!meshRef.current) return
    
    const time = clock.getElapsedTime()
    const tempObject = new THREE.Object3D()
    
    sites.forEach((site, i) => {
      meshRef.current!.getMatrixAt(i, tempObject.matrix)
      tempObject.matrix.decompose(tempObject.position, tempObject.quaternion, tempObject.scale)
      
      // Flotación sutil
      const offset = Math.sin(time * 2 + i * 0.5) * 0.02
      tempObject.position.y = site.position[1] + offset
      
      tempObject.updateMatrix()
      meshRef.current!.setMatrixAt(i, tempObject.matrix)
    })
    
    meshRef.current.instanceMatrix.needsUpdate = true
  })

  return (
    <instancedMesh 
      ref={meshRef} 
      args={[geometry, material, count]}
      frustumCulled
    />
  )
}

/**
 * Partículas instanciadas para efectos ambientales
 */
export function InstancedParticles({ 
  count = 1000, 
  spread = 50,
  color = '#ffffff'
}: { 
  count?: number
  spread?: number
  color?: string
}) {
  const meshRef = useRef<THREE.InstancedMesh>(null)
  
  const geometry = useMemo(() => 
    new THREE.SphereGeometry(0.05, 4, 4), 
    []
  )
  
  const material = useMemo(() => 
    new THREE.MeshBasicMaterial({ 
      color,
      transparent: true,
      opacity: 0.6
    }), 
    [color]
  )

  // Generar posiciones aleatorias
  const positions = useMemo(() => {
    return Array.from({ length: count }, () => [
      (Math.random() - 0.5) * spread,
      (Math.random() - 0.5) * spread,
      (Math.random() - 0.5) * spread
    ] as [number, number, number])
  }, [count, spread])

  useEffect(() => {
    if (!meshRef.current) return

    const tempObject = new THREE.Object3D()
    
    positions.forEach((position, i) => {
      tempObject.position.set(...position)
      tempObject.scale.setScalar(Math.random() * 0.5 + 0.5)
      tempObject.updateMatrix()
      meshRef.current!.setMatrixAt(i, tempObject.matrix)
    })
    
    meshRef.current.instanceMatrix.needsUpdate = true
  }, [positions])

  // Animación de movimiento
  useFrame(({ clock }) => {
    if (!meshRef.current) return
    
    const time = clock.getElapsedTime()
    const tempObject = new THREE.Object3D()
    
    positions.forEach((position, i) => {
      const offset = Math.sin(time + i) * 0.1
      tempObject.position.set(
        position[0] + offset,
        position[1] + Math.cos(time * 0.5 + i) * 0.1,
        position[2]
      )
      tempObject.scale.setScalar(Math.random() * 0.5 + 0.5)
      tempObject.updateMatrix()
      meshRef.current!.setMatrixAt(i, tempObject.matrix)
    })
    
    meshRef.current.instanceMatrix.needsUpdate = true
  })

  return (
    <instancedMesh 
      ref={meshRef} 
      args={[geometry, material, count]}
      frustumCulled
    />
  )
}

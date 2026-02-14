'use client'

import { useRef, useMemo, forwardRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface IceTerrainProps {
  location?: { lat: number, lon: number } | null
}

const IceTerrain = forwardRef<THREE.Mesh, IceTerrainProps>(
  function IceTerrain({ location }, ref) {
  const meshRef = useRef<THREE.Mesh>(null)
  
  const actualRef = (ref as React.RefObject<THREE.Mesh>) || meshRef
  
  // Generar geometría con relieve helado
  const geometry = useMemo(() => {
    const geo = new THREE.PlaneGeometry(200, 200, 120, 120)
    const positions = geo.attributes.position.array as Float32Array
    
    const seed = location ? (location.lat * 1000 + location.lon * 1000) : 0
    
    // Función de ruido para hielo
    const noise = (x: number, y: number, scale: number, offset: number) => {
      return Math.sin((x + offset) * scale) * Math.cos((y + offset) * scale)
    }
    
    // Terreno helado con grietas y formaciones
    for (let i = 0; i < positions.length; i += 3) {
      const x = positions[i]
      const y = positions[i + 1]
      
      // Ondulaciones suaves de hielo
      let z = noise(x, y, 0.02, seed) * 1.5
      
      // Grietas y crestas
      z += noise(x, y, 0.08, seed * 2) * 0.8
      
      // Formaciones de hielo (seracs)
      z += Math.abs(noise(x, y, 0.15, seed * 3)) * 1.2
      
      // Suavizar el terreno
      z += noise(x, y, 0.01, seed * 4) * 2.0
      
      positions[i + 2] = z
    }
    
    geo.computeVertexNormals()
    return geo
  }, [location])
  
  // Material de hielo con reflejos
  const material = useMemo(() => {
    return new THREE.MeshStandardMaterial({
      color: '#e8f4f8',
      roughness: 0.3,
      metalness: 0.1,
      emissive: '#b8d4e8',
      emissiveIntensity: 0.1,
      envMapIntensity: 1.5
    })
  }, [])
  
  // Animación sutil de brillo
  useFrame((state) => {
    if (actualRef.current) {
      const time = state.clock.getElapsedTime()
      material.emissiveIntensity = 0.1 + Math.sin(time * 0.3) * 0.05
    }
  })
  
  return (
    <mesh
      ref={actualRef}
      geometry={geometry}
      material={material}
      rotation={[-Math.PI / 2, 0, 0]}
      receiveShadow
      castShadow
    />
  )
})

export default IceTerrain

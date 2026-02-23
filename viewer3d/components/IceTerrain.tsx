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
  
  // Detectar si las coordenadas están en océano abierto
  const isInOcean = useMemo(() => {
    if (!location) return false
    
    const { lat, lon } = location
    
    // OCÉANO PACÍFICO CENTRAL - La zona más grande
    // Longitud entre -180 y -70 (excluyendo costas de América)
    if (lon < -70) {
      // Excluir costa oeste de América del Norte (lat > 30, lon > -130)
      if (lat > 30 && lon > -130) return false
      
      // Excluir costa oeste de América del Sur (lat < -10, lon > -85)
      if (lat < -10 && lon > -85) return false
      
      // Excluir costa de Chile (lat < -15, lon > -75)
      if (lat < -15 && lon > -75) return false
      
      // Excluir Alaska (lat > 50, lon > -170)
      if (lat > 50 && lon > -170) return false
      
      // TODO LO DEMÁS EN ESTA LONGITUD ES OCÉANO PACÍFICO
      // Esto incluye (8.7783°, -144.8885°)
      return true
    }
    
    // Océano Pacífico occidental (Asia-Oceanía)
    // Longitud entre 100 y 180
    if (lon > 100) {
      // Excluir Australia (lat < -10, lon < 155)
      if (lat < -10 && lat > -45 && lon < 155) return false
      
      // Excluir Asia (lat > 0, lon < 140)
      if (lat > 0 && lon < 140) return false
      
      // Todo lo demás es océano
      return true
    }
    
    // Océano Atlántico central
    if (lon > -50 && lon < -10) {
      // Excluir costas de África y América del Sur
      if (Math.abs(lat) > 40) return false
      if (lat > 10 && lon > -30) return false // África
      if (lat < -5 && lon < -30) return false // Brasil
      return true
    }
    
    // Océano Índico
    if (lon > 40 && lon < 100) {
      // Excluir África (lon < 55, lat > -35)
      if (lon < 55 && lat > -35) return false
      // Excluir India (lat > 5, lon < 80)
      if (lat > 5 && lon < 80) return false
      return true
    }
    
    return false
  }, [location])
  
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
  
  // No renderizar terreno si está en océano abierto
  if (isInOcean) {
    return null
  }
  
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

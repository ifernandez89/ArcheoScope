'use client'

import { useRef, useEffect } from 'react'
import * as THREE from 'three'

interface TerrainSystemProps {
  location: { lat: number, lon: number }
  size?: number
  resolution?: number
}

export default function TerrainSystem({ 
  location, 
  size = 50, 
  resolution = 128 
}: TerrainSystemProps) {
  const terrainRef = useRef<THREE.Mesh>(null)
  
  useEffect(() => {
    if (!terrainRef.current) return
    
    // Generar terreno procedural basado en coordenadas
    const geometry = new THREE.PlaneGeometry(size, size, resolution, resolution)
    const positions = geometry.attributes.position.array as Float32Array
    
    // Aplicar elevación procedural
    for (let i = 0; i < positions.length; i += 3) {
      const x = positions[i]
      const y = positions[i + 1]
      
      // Ruido procedural simple (Perlin-like)
      const elevation = 
        Math.sin(x * 0.1 + location.lat) * 0.5 +
        Math.cos(y * 0.1 + location.lon) * 0.5 +
        Math.sin(x * 0.05) * Math.cos(y * 0.05) * 1.0
      
      positions[i + 2] = elevation
    }
    
    geometry.attributes.position.needsUpdate = true
    geometry.computeVertexNormals()
    
    terrainRef.current.geometry = geometry
    
    console.log('🏔️ Terreno generado para:', location)
  }, [location, size, resolution])
  
  return (
    <mesh
      ref={terrainRef}
      rotation={[-Math.PI / 2, 0, 0]}
      position={[0, -1, 0]}
      receiveShadow
    >
      <planeGeometry args={[size, size, resolution, resolution]} />
      <meshStandardMaterial
        color="#4a5d3f"
        roughness={0.9}
        metalness={0.1}
        wireframe={false}
      />
    </mesh>
  )
}

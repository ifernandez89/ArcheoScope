/**
 * ProceduralGrass - Césped procedural con instancing
 * 5000 briznas = 1 draw call
 */

'use client'

import { useMemo } from 'react'
import * as THREE from 'three'
import { useInstancedMesh, useInstances, useProceduralInstances } from '@/hooks/useInstancing'

interface ProceduralGrassProps {
  count?: number
  radius?: number
  seed?: number
}

export default function ProceduralGrass({
  count = 5000,
  radius = 500,
  seed = 456
}: ProceduralGrassProps) {
  // Geometría de brizna (muy simple)
  const geometry = useMemo(() => {
    const geo = new THREE.PlaneGeometry(0.1, 1, 1, 3)
    
    // Curvar hacia arriba
    const positions = geo.attributes.position
    for (let i = 0; i < positions.count; i++) {
      const y = positions.getY(i)
      if (y > 0) {
        const bend = y * 0.2
        positions.setX(i, positions.getX(i) + bend)
      }
    }
    
    geo.translate(0, 0.5, 0) // Pivot en base
    return geo
  }, [])
  
  const material = useMemo(() => 
    new THREE.MeshStandardMaterial({
      color: '#4a7c2e',
      side: THREE.DoubleSide,
      roughness: 0.9,
      vertexColors: true
    }),
  [])
  
  const mesh = useInstancedMesh('grass', {
    geometry,
    material,
    count
  })
  
  // Generar posiciones
  const instances = useProceduralInstances(count, (i) => {
    const random = (seed: number) => {
      const x = Math.sin(seed) * 10000
      return x - Math.floor(x)
    }
    
    const angle = random(i * seed) * Math.PI * 2
    const distance = Math.sqrt(random(i * seed + 1)) * radius
    
    const x = Math.cos(angle) * distance
    const z = Math.sin(angle) * distance
    
    const scale = 0.8 + random(i * seed + 2) * 0.4
    const rotation = random(i * seed + 3) * Math.PI * 2
    
    // Variación de color
    const colorVariation = 0.8 + random(i * seed + 4) * 0.4
    
    return {
      position: new THREE.Vector3(x, 0, z),
      rotation: new THREE.Euler(0, rotation, 0),
      scale: new THREE.Vector3(scale, scale, scale),
      color: new THREE.Color('#4a7c2e').multiplyScalar(colorVariation)
    }
  })
  
  useInstances('grass', instances, [instances])
  
  return mesh ? <primitive object={mesh} /> : null
}

/**
 * ProceduralRocks - Rocas procedurales con instancing
 * 500 rocas = 1 draw call
 */

'use client'

import { useMemo } from 'react'
import * as THREE from 'three'
import { useInstancedMesh, useInstances, useProceduralInstances } from '@/hooks/useInstancing'

interface ProceduralRocksProps {
  count?: number
  radius?: number
  seed?: number
}

export default function ProceduralRocks({
  count = 500,
  radius = 500,
  seed = 123
}: ProceduralRocksProps) {
  // Geometría procedural de roca
  const geometry = useMemo(() => {
    const geo = new THREE.DodecahedronGeometry(1, 0)
    
    // Deformar para hacer más irregular
    const positions = geo.attributes.position
    for (let i = 0; i < positions.count; i++) {
      const x = positions.getX(i)
      const y = positions.getY(i)
      const z = positions.getZ(i)
      
      const noise = Math.sin(x * 3) * Math.cos(y * 3) * Math.sin(z * 3) * 0.2
      
      positions.setXYZ(
        i,
        x * (1 + noise),
        y * (1 + noise),
        z * (1 + noise)
      )
    }
    
    geo.computeVertexNormals()
    return geo
  }, [])
  
  const material = useMemo(() => 
    new THREE.MeshStandardMaterial({
      color: '#6b6b6b',
      roughness: 0.95,
      metalness: 0.1
    }),
  [])
  
  const mesh = useInstancedMesh('rocks', {
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
    
    const scaleBase = 0.5 + random(i * seed + 2) * 2
    const scaleX = scaleBase * (0.8 + random(i * seed + 3) * 0.4)
    const scaleY = scaleBase * (0.8 + random(i * seed + 4) * 0.4)
    const scaleZ = scaleBase * (0.8 + random(i * seed + 5) * 0.4)
    
    const rotX = random(i * seed + 6) * Math.PI * 2
    const rotY = random(i * seed + 7) * Math.PI * 2
    const rotZ = random(i * seed + 8) * Math.PI * 2
    
    return {
      position: new THREE.Vector3(x, scaleY * 0.5, z),
      rotation: new THREE.Euler(rotX, rotY, rotZ),
      scale: new THREE.Vector3(scaleX, scaleY, scaleZ)
    }
  })
  
  useInstances('rocks', instances, [instances])
  
  return mesh ? <primitive object={mesh} /> : null
}

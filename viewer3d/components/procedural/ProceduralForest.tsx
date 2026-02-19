/**
 * ProceduralForest - Bosque procedural con instancing
 * 1000 árboles = 1 draw call
 */

'use client'

import { useMemo } from 'react'
import * as THREE from 'three'
import { useInstancedMesh, useInstances, useProceduralInstances } from '@/hooks/useInstancing'

interface ProceduralForestProps {
  count?: number
  radius?: number
  seed?: number
}

export default function ProceduralForest({
  count = 1000,
  radius = 500,
  seed = 42
}: ProceduralForestProps) {
  // Geometría compartida
  const trunkGeometry = useMemo(() => 
    new THREE.CylinderGeometry(0.5, 0.7, 5, 8),
  [])
  
  const foliageGeometry = useMemo(() => 
    new THREE.ConeGeometry(2, 4, 8),
  [])
  
  // Materiales
  const trunkMaterial = useMemo(() => 
    new THREE.MeshStandardMaterial({
      color: '#4a3728',
      roughness: 0.9
    }),
  [])
  
  const foliageMaterial = useMemo(() => 
    new THREE.MeshStandardMaterial({
      color: '#2d5016',
      roughness: 0.8
    }),
  [])
  
  // Crear instanced meshes
  const trunkMesh = useInstancedMesh('forest-trunks', {
    geometry: trunkGeometry,
    material: trunkMaterial,
    count
  })
  
  const foliageMesh = useInstancedMesh('forest-foliage', {
    geometry: foliageGeometry,
    material: foliageMaterial,
    count
  })
  
  // Generar posiciones procedurales
  const instances = useProceduralInstances(count, (i) => {
    // Seeded random
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
    
    return {
      position: new THREE.Vector3(x, 0, z),
      rotation: new THREE.Euler(0, rotation, 0),
      scale: new THREE.Vector3(scale, scale, scale)
    }
  })
  
  // Instancias de follaje (offset en Y)
  const foliageInstances = useMemo(() => 
    instances.map(inst => ({
      ...inst,
      position: inst.position.clone().add(new THREE.Vector3(0, 5, 0))
    })),
  [instances])
  
  // Actualizar instancias
  useInstances('forest-trunks', instances, [instances])
  useInstances('forest-foliage', foliageInstances, [foliageInstances])
  
  return (
    <group>
      {trunkMesh && <primitive object={trunkMesh} />}
      {foliageMesh && <primitive object={foliageMesh} />}
    </group>
  )
}

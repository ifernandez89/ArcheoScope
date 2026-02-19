/**
 * useInstancing - Hook para usar InstanceManager con React
 */

import { useEffect, useRef, useMemo } from 'react'
import * as THREE from 'three'
import InstanceManager, { InstanceConfig, InstanceData } from '@/systems/InstanceManager'

/**
 * Hook para crear instanced mesh
 */
export function useInstancedMesh(
  id: string,
  config: InstanceConfig
): THREE.InstancedMesh | null {
  const meshRef = useRef<THREE.InstancedMesh | null>(null)

  useEffect(() => {
    meshRef.current = InstanceManager.create(id, config)

    return () => {
      InstanceManager.remove(id)
    }
  }, [id])

  return meshRef.current
}

/**
 * Hook para actualizar instancias
 */
export function useInstances(
  id: string,
  instances: InstanceData[],
  deps: any[] = []
) {
  useEffect(() => {
    InstanceManager.setInstances(id, instances)
  }, [id, ...deps])
}

/**
 * Hook para generar posiciones procedurales
 */
export function useProceduralInstances(
  count: number,
  generator: (index: number) => InstanceData
): InstanceData[] {
  return useMemo(() => {
    const instances: InstanceData[] = []
    
    for (let i = 0; i < count; i++) {
      instances.push(generator(i))
    }
    
    return instances
  }, [count, generator])
}

/**
 * Ejemplo de uso:
 * 
 * function Trees() {
 *   const geometry = useMemo(() => new THREE.CylinderGeometry(0.5, 0.5, 5), [])
 *   const material = useMemo(() => new THREE.MeshStandardMaterial({ color: 'brown' }), [])
 *   
 *   const mesh = useInstancedMesh('trees', {
 *     geometry,
 *     material,
 *     count: 1000
 *   })
 *   
 *   const instances = useProceduralInstances(1000, (i) => ({
 *     position: new THREE.Vector3(
 *       Math.random() * 100 - 50,
 *       0,
 *       Math.random() * 100 - 50
 *     ),
 *     rotation: new THREE.Euler(0, Math.random() * Math.PI * 2, 0),
 *     scale: new THREE.Vector3(1, 1, 1)
 *   }))
 *   
 *   useInstances('trees', instances, [])
 *   
 *   return mesh ? <primitive object={mesh} /> : null
 * }
 */

/**
 * useCulling - Hook para integrar CullingSystem con React
 * Permite registrar objetos para culling automático
 */

import { useEffect, useRef } from 'react'
import { useThree } from '@react-three/fiber'
import * as THREE from 'three'
import CullingSystem from '@/systems/CullingSystem'

/**
 * Hook para registrar objeto en CullingSystem
 */
export function useCulling(
  object3D: THREE.Object3D | null,
  options: {
    id?: string
    priority?: number
    maxDistance?: number
    enabled?: boolean
  } = {}
) {
  const {
    id = `object-${Math.random().toString(36).substr(2, 9)}`,
    priority = 0.5,
    maxDistance = 2000,
    enabled = true
  } = options

  const registeredRef = useRef(false)
  const idRef = useRef(id)

  useEffect(() => {
    if (!object3D || !enabled || registeredRef.current) return

    // Calcular bounds
    const bounds = new THREE.Box3().setFromObject(object3D)
    const position = new THREE.Vector3()
    bounds.getCenter(position)

    // Registrar en CullingSystem
    CullingSystem.register({
      id: idRef.current,
      object3D,
      position,
      bounds,
      priority,
      maxDistance
    })

    registeredRef.current = true

    return () => {
      CullingSystem.unregister(idRef.current)
      registeredRef.current = false
    }
  }, [object3D, enabled, priority, maxDistance])

  return idRef.current
}

/**
 * Hook para inicializar CullingSystem con la cámara
 */
export function useCullingCamera() {
  const { camera } = useThree()

  useEffect(() => {
    CullingSystem.setCamera(camera)
  }, [camera])
}

/**
 * Hook para configurar CullingSystem
 */
export function useCullingConfig(config: {
  enableFrustumCulling?: boolean
  enableDistanceCulling?: boolean
  enableDisposal?: boolean
  maxRenderDistance?: number
  disposalDistance?: number
  updateInterval?: number
}) {
  useEffect(() => {
    CullingSystem.configure(config)
  }, [config])
}

/**
 * Hook para obtener estadísticas de culling
 */
export function useCullingStats() {
  const statsRef = useRef(CullingSystem.getStats())

  useEffect(() => {
    const interval = setInterval(() => {
      statsRef.current = CullingSystem.getStats()
    }, 100)

    return () => clearInterval(interval)
  }, [])

  return statsRef.current
}

/**
 * Ejemplo de uso:
 * 
 * // En el componente raíz de la escena
 * function Scene() {
 *   useCullingCamera() // Configurar cámara
 *   
 *   return <group>...</group>
 * }
 * 
 * // En objetos individuales
 * function MyObject() {
 *   const meshRef = useRef<THREE.Mesh>(null)
 *   
 *   useCulling(meshRef.current, {
 *     priority: 0.8,
 *     maxDistance: 1500
 *   })
 *   
 *   return <mesh ref={meshRef} />
 * }
 * 
 * // Configuración global
 * function App() {
 *   useCullingConfig({
 *     maxRenderDistance: 2500,
 *     disposalDistance: 3000
 *   })
 *   
 *   return <Canvas>...</Canvas>
 * }
 */

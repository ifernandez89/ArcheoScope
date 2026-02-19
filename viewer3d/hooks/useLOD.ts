/**
 * useLOD - Hook para integrar LOD en componentes personalizados
 */

import { useRef, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'
import { WorldCore } from '@/engines/WorldCore'
import { loggers } from '@/core/Logger'

export interface UseLODOptions {
  distances?: number[]
  autoUpdate?: boolean
  onLevelChange?: (level: number) => void
}

/**
 * Hook para obtener el nivel LOD actual basado en distancia a cámara
 */
export function useLOD(
  position: THREE.Vector3 | [number, number, number],
  options: UseLODOptions = {}
) {
  const {
    distances = [50, 150, 300, 500],
    autoUpdate = true,
    onLevelChange
  } = options

  const { camera } = useThree()
  const currentLevel = useRef(0)
  const posVector = useRef(
    Array.isArray(position) 
      ? new THREE.Vector3(...position) 
      : position.clone()
  )

  useFrame(() => {
    if (!autoUpdate) return

    const distance = camera.position.distanceTo(posVector.current)
    
    let newLevel = distances.length
    for (let i = 0; i < distances.length; i++) {
      if (distance < distances[i]) {
        newLevel = i
        break
      }
    }

    if (newLevel !== currentLevel.current) {
      currentLevel.current = newLevel
      onLevelChange?.(newLevel)
    }
  })

  return {
    level: currentLevel.current,
    distance: camera.position.distanceTo(posVector.current),
    isVisible: currentLevel.current < distances.length
  }
}

/**
 * Hook para registrar objeto en WorldCore LOD
 */
export function useWorldCoreLOD(
  id: string,
  position: THREE.Vector3,
  levels: THREE.Object3D[]
) {
  useEffect(() => {
    WorldCore.LOD.register(id, position, levels)

    return () => {
      WorldCore.LOD.unregister(id)
    }
  }, [id, position, levels])

  const { camera } = useThree()

  useFrame(() => {
    WorldCore.LOD.updateCamera(camera.position)
    WorldCore.LOD.update()
  })
}

/**
 * Hook para obtener nivel de detalle recomendado
 */
export function useDetailLevel(distance: number): number {
  return WorldCore.LOD.getDetailLevel(distance)
}

/**
 * Hook para crear geometría con LOD dinámico
 */
export function useDynamicGeometry<T extends THREE.BufferGeometry>(
  createGeometry: (detail: number) => T,
  position: THREE.Vector3 | [number, number, number],
  distances: number[] = [50, 150, 300]
) {
  const geometryRef = useRef<T>()
  const { level } = useLOD(position, { distances })

  useEffect(() => {
    // Calcular nivel de detalle (0-1)
    const detail = 1 - (level / distances.length)
    
    // Crear nueva geometría
    const newGeometry = createGeometry(detail)
    
    // Limpiar geometría anterior
    if (geometryRef.current) {
      geometryRef.current.dispose()
    }
    
    geometryRef.current = newGeometry
  }, [level, createGeometry, distances])

  return geometryRef.current
}

/**
 * Hook para estadísticas de LOD
 */
export function useLODStats() {
  const stats = useRef(WorldCore.LOD.getStats())

  useFrame(() => {
    stats.current = WorldCore.LOD.getStats()
  })

  return stats.current
}

/**
 * Ejemplo de uso:
 * 
 * function MyTree({ position }: { position: [number, number, number] }) {
 *   const { level, distance } = useLOD(position, {
 *     distances: [30, 80, 200],
 *     onLevelChange: (level) => loggers.performance.debug('LOD changed to', level)
 *   })
 * 
 *   return (
 *     <group position={position}>
 *       {level === 0 && <HighDetailTree />}
 *       {level === 1 && <MediumDetailTree />}
 *       {level === 2 && <LowDetailTree />}
 *       {level === 3 && <TreeBillboard />}
 *     </group>
 *   )
 * }
 */

'use client'

/**
 * TerrainClickReceiver - Mesh invisible sobre el terreno que captura clicks
 * cuando hay un objeto seleccionado, para moverlo a esa posición.
 */

import { useCallback } from 'react'
import * as THREE from 'three'
import { useObjectSelection } from './ObjectSelectionContext'

interface TerrainClickReceiverProps {
  size?: number
}

export default function TerrainClickReceiver({ size = 200 }: TerrainClickReceiverProps) {
  const { selectedId, requestMove } = useObjectSelection()

  const handleClick = useCallback((e: any) => {
    if (!selectedId) return
    e.stopPropagation()
    const point = e.point as THREE.Vector3
    requestMove([point.x, 0, point.z])
  }, [selectedId, requestMove])

  // Solo activo cuando hay algo seleccionado
  if (!selectedId) return null

  return (
    <mesh
      position={[0, 0.01, 0]}
      rotation={[-Math.PI / 2, 0, 0]}
      onClick={handleClick}
      visible={false}
    >
      <planeGeometry args={[size, size]} />
      <meshBasicMaterial transparent opacity={0} side={THREE.DoubleSide} />
    </mesh>
  )
}

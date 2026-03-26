'use client'

/**
 * SelectableObject - Wrapper que hace cualquier objeto 3D hoverable, seleccionable y movible.
 *
 * Uso:
 *   <SelectableObject id="rock-0" onMove={(pos) => setPos(pos)}>
 *     <Rock3DModel ... />
 *   </SelectableObject>
 *
 * Cuando el usuario apunta el mouse → brilla (emissive boost en todos los meshes hijos).
 * Click → queda seleccionado (brillo más intenso + cursor crosshair).
 * Click en terreno (TerrainClickReceiver) → llama onMove con la nueva posición.
 */

import { useRef, useState, useCallback, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { useObjectSelection } from './ObjectSelectionContext'

interface SelectableObjectProps {
  id: string
  children: React.ReactNode
  position?: [number, number, number]
  onMove?: (newPosition: [number, number, number]) => void
}

export default function SelectableObject({
  id,
  children,
  position = [0, 0, 0],
  onMove
}: SelectableObjectProps) {
  const groupRef = useRef<THREE.Group>(null)
  const [hovered, setHovered] = useState(false)
  const { selectedId, setSelected, pendingMove, consumeMove } = useObjectSelection()
  const isSelected = selectedId === id

  // Guardar emissive originales para restaurar + cache de meshes
  const originalEmissive = useRef<Map<THREE.Mesh, { color: THREE.Color; intensity: number }>>(new Map())
  const cachedMeshes = useRef<THREE.Mesh[]>([])
  const initialized = useRef(false)

  // Inicializar emissive originales una vez que los meshes están listos
  useEffect(() => {
    if (!groupRef.current || initialized.current) return
    const timer = setTimeout(() => {
      cachedMeshes.current = []
      groupRef.current?.traverse((child) => {
        if (child instanceof THREE.Mesh && child.material) {
          const mat = child.material as THREE.MeshStandardMaterial
          if (mat.emissive !== undefined) {
            originalEmissive.current.set(child, {
              color: mat.emissive.clone(),
              intensity: mat.emissiveIntensity ?? 0
            })
            cachedMeshes.current.push(child)
          }
        }
      })
      initialized.current = true
    }, 200)
    return () => clearTimeout(timer)
  }, [])

  // Aplicar/quitar highlight en cada frame según estado - OPTIMIZADO: usa cache
  useFrame(() => {
    if (!initialized.current || cachedMeshes.current.length === 0) return

    for (const mesh of cachedMeshes.current) {
      const mat = mesh.material as THREE.MeshStandardMaterial
      if (mat.emissive === undefined) continue

      const orig = originalEmissive.current.get(mesh)
      if (!orig) continue

      if (isSelected) {
        mat.emissive.set('#00aaff')
        mat.emissiveIntensity = 0.6 + Math.sin(Date.now() * 0.004) * 0.2 // pulso
      } else if (hovered) {
        mat.emissive.set('#ffdd88')
        mat.emissiveIntensity = 0.4
      } else {
        mat.emissive.copy(orig.color)
        mat.emissiveIntensity = orig.intensity
      }
    }
  })

  // Consumir movimiento pendiente
  useFrame(() => {
    if (!isSelected || !pendingMove || !groupRef.current) return
    const move = consumeMove()
    if (move && onMove) {
      onMove(move)
    }
  })

  const handlePointerOver = useCallback((e: any) => {
    e.stopPropagation()
    setHovered(true)
    document.body.style.cursor = 'pointer'
  }, [])

  const handlePointerOut = useCallback((e: any) => {
    e.stopPropagation()
    setHovered(false)
    if (selectedId !== id) document.body.style.cursor = 'default'
  }, [selectedId, id])

  const handleClick = useCallback((e: any) => {
    e.stopPropagation()
    if (isSelected) {
      // Deseleccionar si ya estaba seleccionado
      setSelected(null)
      document.body.style.cursor = 'default'
    } else {
      setSelected(id)
      document.body.style.cursor = 'crosshair'
    }
  }, [isSelected, id, setSelected])

  // Limpiar cursor al desmontar
  useEffect(() => {
    return () => {
      if (isSelected) {
        document.body.style.cursor = 'default'
      }
    }
  }, [isSelected])

  return (
    <group
      ref={groupRef}
      position={position}
      onPointerOver={handlePointerOver}
      onPointerOut={handlePointerOut}
      onClick={handleClick}
    >
      {children}
    </group>
  )
}

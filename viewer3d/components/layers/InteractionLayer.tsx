'use client'

/**
 * InteractionLayer - Raycasting, Input, Interacciones
 * 
 * Responsabilidades:
 * - Raycasting para detección de objetos
 * - Input handling (mouse, teclado)
 * - Interacciones con el mundo
 * - Selección de objetos
 * 
 * SEMI-LAZY: Se carga cuando hay interacción activa
 * Bundle size: ~50KB
 */

import { useEffect, useRef } from 'react'
import { useThree } from '@react-three/fiber'
import * as THREE from 'three'

interface InteractionLayerProps {
  enabled?: boolean
  onObjectClick?: (object: THREE.Object3D) => void
  onTerrainClick?: (point: THREE.Vector3) => void
}

export default function InteractionLayer({
  enabled = true,
  onObjectClick,
  onTerrainClick
}: InteractionLayerProps) {
  const { camera, scene, gl } = useThree()
  const raycaster = useRef(new THREE.Raycaster())
  const mouse = useRef(new THREE.Vector2())

  useEffect(() => {
    if (!enabled) return

    const handleClick = (event: MouseEvent) => {
      // Calcular posición del mouse normalizada
      mouse.current.x = (event.clientX / window.innerWidth) * 2 - 1
      mouse.current.y = -(event.clientY / window.innerHeight) * 2 + 1

      // Raycast
      raycaster.current.setFromCamera(mouse.current, camera)
      const intersects = raycaster.current.intersectObjects(scene.children, true)

      if (intersects.length > 0) {
        const firstHit = intersects[0]
        
        // Detectar si es terreno o objeto
        if (firstHit.object.name === 'terrain') {
          onTerrainClick?.(firstHit.point)
        } else {
          onObjectClick?.(firstHit.object)
        }
      }
    }

    gl.domElement.addEventListener('click', handleClick)
    return () => gl.domElement.removeEventListener('click', handleClick)
  }, [enabled, camera, scene, gl, onObjectClick, onTerrainClick])

  return null
}

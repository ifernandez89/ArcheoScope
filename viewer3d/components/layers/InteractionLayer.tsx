'use client'

/**
 * InteractionLayer - Raycasting, Input, Physics
 * 
 * Responsabilidades:
 * - Raycasting contra objetos
 * - Input handling
 * - Highlighting / selection
 * - Physics interactions
 * 
 * Semi-lazy: Se puede montar después del primer render
 * Critical: Muy pequeño, negligible overhead
 */

import { useRef, useEffect, useState } from 'react'
import { useThree } from '@react-three/fiber'
import * as THREE from 'three'

interface InteractionLayerProps {
  enabled?: boolean
  onObjectSelected?: (object: THREE.Object3D) => void
  onObjectHovered?: (object: THREE.Object3D | null) => void
}

export default function InteractionLayer({
  enabled = true,
  onObjectSelected,
  onObjectHovered
}: InteractionLayerProps) {
  const { camera, scene, raycaster, mouse } = useThree()
  const [hoveredObject, setHoveredObject] = useState<THREE.Object3D | null>(null)

  // Raycasting on click
  useEffect(() => {
    if (!enabled) return

    const handleClick = (event: MouseEvent) => {
      // Normalizar coordenadas
      mouse.x = (event.clientX / window.innerWidth) * 2 - 1
      mouse.y = -(event.clientY / window.innerHeight) * 2 + 1

      // Raycast
      raycaster.setFromCamera(mouse, camera)
      const intersects = raycaster.intersectObjects(scene.children, true)

      if (intersects.length > 0 && onObjectSelected) {
        onObjectSelected(intersects[0].object)
      }
    }

    window.addEventListener('click', handleClick)
    return () => window.removeEventListener('click', handleClick)
  }, [enabled, camera, scene, raycaster, mouse, onObjectSelected])

  // Raycasting on move (hover)
  useEffect(() => {
    if (!enabled || !onObjectHovered) return

    const handleMouseMove = (event: MouseEvent) => {
      mouse.x = (event.clientX / window.innerWidth) * 2 - 1
      mouse.y = -(event.clientY / window.innerHeight) * 2 + 1

      raycaster.setFromCamera(mouse, camera)
      const intersects = raycaster.intersectObjects(scene.children, true)

      const newHovered = intersects.length > 0 ? intersects[0].object : null

      if (newHovered !== hoveredObject) {
        setHoveredObject(newHovered)
        onObjectHovered(newHovered)
      }
    }

    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [enabled, camera, scene, raycaster, mouse, onObjectHovered, hoveredObject])

  return null
}

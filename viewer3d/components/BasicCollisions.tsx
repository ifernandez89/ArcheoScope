'use client'

import { useRef, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

interface BasicCollisionsProps {
  terrainRef?: React.RefObject<THREE.Mesh>
  obstacles?: THREE.Object3D[]
  enabled?: boolean
}

export default function BasicCollisions({ 
  terrainRef, 
  obstacles = [], 
  enabled = true 
}: BasicCollisionsProps) {
  const { camera, scene } = useThree()
  const raycaster = useRef(new THREE.Raycaster())
  const minHeight = useRef(1.6) // Altura del jugador (ojos)
  
  useFrame(() => {
    if (!enabled || !terrainRef?.current) return
    
    // Raycast hacia abajo para mantener jugador sobre terreno
    raycaster.current.set(
      camera.position,
      new THREE.Vector3(0, -1, 0)
    )
    
    const intersects = raycaster.current.intersectObject(terrainRef.current, true)
    
    if (intersects.length > 0) {
      const groundHeight = intersects[0].point.y
      const targetHeight = groundHeight + minHeight.current
      
      // Ajustar suavemente la altura de la cámara
      if (camera.position.y < targetHeight) {
        camera.position.y = targetHeight
      } else if (camera.position.y > targetHeight + 0.5) {
        // Permitir saltos pequeños pero no volar
        camera.position.y = Math.max(camera.position.y - 0.1, targetHeight)
      }
    }
    
    // Límites del mundo (no salir del terreno)
    const worldLimit = 95 // Un poco menos que 100 (mitad del terreno de 200x200)
    camera.position.x = Math.max(-worldLimit, Math.min(worldLimit, camera.position.x))
    camera.position.z = Math.max(-worldLimit, Math.min(worldLimit, camera.position.z))
    
    // Colisiones simples con obstáculos (bounding spheres)
    obstacles.forEach(obstacle => {
      const obstaclePos = new THREE.Vector3()
      obstacle.getWorldPosition(obstaclePos)
      
      const distance = camera.position.distanceTo(obstaclePos)
      const minDistance = 2.0 // Radio de colisión
      
      if (distance < minDistance) {
        // Empujar al jugador fuera del obstáculo
        const direction = new THREE.Vector3()
          .subVectors(camera.position, obstaclePos)
          .normalize()
        
        camera.position.copy(
          obstaclePos.clone().add(direction.multiplyScalar(minDistance))
        )
      }
    })
  })
  
  return null
}

// Hook para registrar obstáculos automáticamente
export function useCollisionObstacle(ref: React.RefObject<THREE.Object3D>) {
  const obstacles = useRef<THREE.Object3D[]>([])
  
  useEffect(() => {
    if (ref.current) {
      obstacles.current.push(ref.current)
    }
    
    return () => {
      if (ref.current) {
        const index = obstacles.current.indexOf(ref.current)
        if (index > -1) {
          obstacles.current.splice(index, 1)
        }
      }
    }
  }, [ref])
  
  return obstacles.current
}

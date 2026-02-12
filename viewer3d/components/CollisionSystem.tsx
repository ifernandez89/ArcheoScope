'use client'

import { useRef, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

interface CollisionSystemProps {
  enabled: boolean
  model?: THREE.Object3D | null
}

export default function CollisionSystem({ enabled, model }: CollisionSystemProps) {
  const { camera } = useThree()
  const boundingBoxes = useRef<THREE.Box3[]>([])
  
  useEffect(() => {
    if (!model || !enabled) return
    
    // Generar bounding boxes del modelo
    const boxes: THREE.Box3[] = []
    
    model.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh
        const box = new THREE.Box3().setFromObject(mesh)
        boxes.push(box)
      }
    })
    
    boundingBoxes.current = boxes
    console.log('🛡️ Sistema de colisiones activado:', boxes.length, 'objetos')
  }, [model, enabled])
  
  useFrame(() => {
    if (!enabled || boundingBoxes.current.length === 0) return
    
    // Verificar colisiones con la cámara
    const cameraBox = new THREE.Box3().setFromCenterAndSize(
      camera.position,
      new THREE.Vector3(0.5, 1.8, 0.5)
    )
    
    for (const box of boundingBoxes.current) {
      if (cameraBox.intersectsBox(box)) {
        // Retroceder cámara si hay colisión
        const direction = new THREE.Vector3()
        camera.getWorldDirection(direction)
        camera.position.addScaledVector(direction, -0.1)
      }
    }
  })
  
  return null
}

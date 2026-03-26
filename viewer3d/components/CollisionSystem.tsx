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
  
  // Objetos reutilizables para evitar crear en cada frame
  const cameraBox = useRef(new THREE.Box3())
  const cameraSize = useRef(new THREE.Vector3(0.5, 1.8, 0.5))
  const direction = useRef(new THREE.Vector3())
  
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
    cameraBox.current.setFromCenterAndSize(camera.position, cameraSize.current)
    
    for (const box of boundingBoxes.current) {
      if (cameraBox.current.intersectsBox(box)) {
        // Retroceder cámara si hay colisión
        camera.getWorldDirection(direction.current)
        camera.position.addScaledVector(direction.current, -0.1)
      }
    }
  })
  
  return null
}

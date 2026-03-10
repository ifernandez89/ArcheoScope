'use client'

import { useThree, useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface CompassTrackerProps {
  onRotationChange: (rotation: number) => void
}

/**
 * Componente que rastrea la rotación de la cámara
 * Debe renderizarse DENTRO del Canvas
 */
export default function CompassTracker({ onRotationChange }: CompassTrackerProps) {
  const { camera } = useThree()
  
  useFrame(() => {
    // Obtener la dirección hacia donde mira la cámara
    const direction = new THREE.Vector3()
    camera.getWorldDirection(direction)
    
    // Calcular el ángulo en el plano horizontal (ignorar Y)
    const angle = Math.atan2(direction.x, direction.z)
    
    // Convertir a grados (0° = Norte, 90° = Este, 180° = Sur, 270° = Oeste)
    let degrees = THREE.MathUtils.radToDeg(angle)
    
    // Normalizar a 0-360
    if (degrees < 0) degrees += 360
    
    onRotationChange(degrees)
  })
  
  return null
}

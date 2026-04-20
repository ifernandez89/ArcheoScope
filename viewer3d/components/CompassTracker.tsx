'use client'

import { useThree, useFrame } from '@react-three/fiber'
import { useRef } from 'react'
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
  
  // Vector reutilizable para evitar crear en cada frame
  const directionRef = useRef(new THREE.Vector3())
  
  useFrame(() => {
    // Obtener la dirección hacia donde mira la cámara
    camera.getWorldDirection(directionRef.current)
    
    // Calcular el ángulo en el plano horizontal (ignorar Y)
    // En Three.js, -Z es 'hacia adelante', que se mapea como Norte (0°)
    const angle = Math.atan2(directionRef.current.x, -directionRef.current.z)
    
    // Convertir a grados (0° = Norte, 90° = Este, 180° = Sur, 270° = Oeste)
    let degrees = THREE.MathUtils.radToDeg(angle)
    
    // Normalizar a 0-360
    if (degrees < 0) degrees += 360
    
    onRotationChange(degrees)
  })
  
  return null
}

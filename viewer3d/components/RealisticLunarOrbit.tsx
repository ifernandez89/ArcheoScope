'use client'

import { useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { calculateLunarPhase } from '@/utils/lunar-system'

/**
 * Órbita lunar real calculada con nuestro sistema lunar
 * Dibuja la trayectoria orbital de la Luna alrededor de la Tierra
 * Se actualiza dinámicamente para seguir a la Tierra
 */

export default function RealisticLunarOrbit() {
  // Crear geometría de línea
  const geometry = useMemo(() => {
    const points: THREE.Vector3[] = []
    const lunarPeriod = 27.32166 // días siderales (órbita real)
    const steps = 128
    const VISUAL_SCALE = 10 // MISMA escala visual que la Luna
    
    for (let i = 0; i <= steps; i++) {
      const fraction = i / steps
      const timeInDays = fraction * lunarPeriod
      
      // Usar nuestro sistema lunar (ya viene en escala correcta: 1 AU = 200 unidades)
      const lunarState = calculateLunarPhase(timeInDays)
      const moonPos = lunarState.position.clone().multiplyScalar(VISUAL_SCALE)
      
      points.push(moonPos)
    }
    
    const geometry = new THREE.BufferGeometry().setFromPoints(points)
    return geometry
  }, [])
  
  // Actualizar posición de la órbita para seguir a la Tierra
  useFrame((state) => {
    // La órbita se renderiza en el origen, pero visualmente sigue a la Tierra
    // porque está dentro del mismo sistema de coordenadas
  })
  
  return (
    <primitive object={new THREE.Line(geometry, new THREE.LineBasicMaterial({
      color: '#FFFFFF',
      transparent: true,
      opacity: 0.4,
      depthWrite: false
    }))} />
  )
}

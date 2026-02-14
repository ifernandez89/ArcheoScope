'use client'

import { useRef, useEffect } from 'react'
import * as THREE from 'three'
import * as Astronomy from 'astronomy-engine'

/**
 * Órbita lunar real calculada con astronomy-engine
 * Dibuja la trayectoria orbital de la Luna alrededor de la Tierra
 */

export default function RealisticLunarOrbit() {
  const lineRef = useRef<THREE.Line | null>(null)
  
  useEffect(() => {
    // Calcular órbita completa de la Luna (27.3 días)
    const points: THREE.Vector3[] = []
    const startDate = new Date()
    const lunarPeriod = 27.3 // días
    const steps = 128
    const scale = 200 * 12 // Escala visual (12 radios terrestres)
    
    for (let i = 0; i <= steps; i++) {
      const fraction = i / steps
      const daysOffset = fraction * lunarPeriod
      const date = new Date(startDate.getTime() + daysOffset * 24 * 60 * 60 * 1000)
      
      // Posición geocéntrica de la Luna
      const pos = Astronomy.GeoVector('Moon' as any, date, false)
      
      // Convertir a coordenadas de escena (intercambiar Y y Z)
      points.push(new THREE.Vector3(
        pos.x * scale,
        pos.z * scale,
        pos.y * scale
      ))
    }
    
    // Crear geometría y material
    const geometry = new THREE.BufferGeometry().setFromPoints(points)
    const material = new THREE.LineBasicMaterial({
      color: '#FFFFFF',
      transparent: true,
      opacity: 0.3,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    })
    
    // Crear línea
    lineRef.current = new THREE.Line(geometry, material)
  }, [])
  
  return (
    <primitive object={lineRef.current || new THREE.Line()} />
  )
}

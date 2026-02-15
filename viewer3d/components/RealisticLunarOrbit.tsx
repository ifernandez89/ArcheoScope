'use client'

import { useState, useEffect, useMemo } from 'react'
import * as THREE from 'three'
import * as Astronomy from 'astronomy-engine'

/**
 * Órbita lunar real calculada con astronomy-engine
 * Dibuja la trayectoria orbital de la Luna alrededor de la Tierra
 */

export default function RealisticLunarOrbit() {
  const [isReady, setIsReady] = useState(false)
  
  // Calcular puntos de la órbita
  const orbitPoints = useMemo(() => {
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
    
    return points
  }, [])
  
  useEffect(() => {
    setIsReady(true)
  }, [])
  
  if (!isReady || orbitPoints.length === 0) {
    return null
  }
  
  return (
    <line>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={orbitPoints.length}
          array={new Float32Array(orbitPoints.flatMap(p => [p.x, p.y, p.z]))}
          itemSize={3}
        />
      </bufferGeometry>
      <lineBasicMaterial
        color="#FFFFFF"
        transparent
        opacity={0.4}
        depthWrite={false}
      />
    </line>
  )
}

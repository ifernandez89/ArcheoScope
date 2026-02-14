'use client'

import { useRef, useEffect } from 'react'
import * as THREE from 'three'
import * as Astronomy from 'astronomy-engine'

/**
 * Órbitas reales calculadas con astronomy-engine
 * Dibuja las trayectorias orbitales reales de los planetas
 */

interface OrbitProps {
  body: string
  color: string
  opacity?: number
  segments?: number
  scale?: number
}

function RealisticOrbit({ body, color, opacity = 0.35, segments = 256, scale = 200 }: OrbitProps) {
  const groupRef = useRef<THREE.Group>(null)
  
  useEffect(() => {
    if (!groupRef.current) return
    
    // Calcular órbita completa (1 año de posiciones)
    const points: THREE.Vector3[] = []
    const startDate = new Date()
    
    // Período orbital en días
    const periods: { [key: string]: number } = {
      'Mercury': 88,
      'Venus': 225,
      'Earth': 365,
      'Mars': 687
    }
    
    const period = periods[body] || 365
    const steps = segments
    
    for (let i = 0; i <= steps; i++) {
      const fraction = i / steps
      const daysOffset = fraction * period
      const date = new Date(startDate.getTime() + daysOffset * 24 * 60 * 60 * 1000)
      
      const pos = Astronomy.HelioVector(body as any, date)
      
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
      color,
      transparent: true,
      opacity,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    })
    
    // Crear línea y agregarla al grupo
    const line = new THREE.Line(geometry, material)
    groupRef.current.add(line)
    
    return () => {
      groupRef.current?.remove(line)
      geometry.dispose()
      material.dispose()
    }
  }, [body, segments, scale, color, opacity])
  
  return <group ref={groupRef} />
}

export default function RealisticOrbits() {
  return (
    <group>
      {/* Órbita de Mercurio */}
      <RealisticOrbit body="Mercury" color="#9c9c9c" opacity={0.35} />
      
      {/* Órbita de Venus */}
      <RealisticOrbit body="Venus" color="#f5e6d3" opacity={0.35} />
      
      {/* Órbita de la Tierra */}
      <RealisticOrbit body="Earth" color="#4a9eff" opacity={0.45} />
      
      {/* Órbita de Marte */}
      <RealisticOrbit body="Mars" color="#c97a5f" opacity={0.35} />
    </group>
  )
}

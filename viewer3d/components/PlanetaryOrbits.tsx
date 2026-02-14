'use client'

import { useMemo } from 'react'
import { Html } from '@react-three/drei'
import * as THREE from 'three'

/**
 * Órbitas planetarias visibles con etiquetas
 * Sistema híbrido profesional con proporciones reales
 */

interface OrbitProps {
  radius: number
  color: string
  opacity?: number
  segments?: number
  label?: string
}

function Orbit({ radius, color, opacity = 0.3, segments = 128, label }: OrbitProps) {
  const orbitLine = useMemo(() => {
    const geometry = new THREE.BufferGeometry()
    const points: THREE.Vector3[] = []
    
    for (let i = 0; i <= segments; i++) {
      const angle = (i / segments) * Math.PI * 2
      const x = Math.cos(angle) * radius
      const z = Math.sin(angle) * radius
      points.push(new THREE.Vector3(x, 0, z))
    }
    
    geometry.setFromPoints(points)
    
    const material = new THREE.LineBasicMaterial({
      color,
      transparent: true,
      opacity,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    })
    
    return new THREE.Line(geometry, material)
  }, [radius, segments, color, opacity])
  
  return <primitive object={orbitLine} />
}

export default function PlanetaryOrbits({ visible = true }: { visible?: boolean }) {
  if (!visible) return null
  
  return (
    <group>
      {/* NO mostrar órbita de la Luna aquí - está en coordenadas de la Tierra */}
      
      {/* Órbita de Mercurio */}
      <Orbit radius={39} color="#9c9c9c" opacity={0.35} segments={128} />
      
      {/* Órbita de Venus */}
      <Orbit radius={72} color="#f5e6d3" opacity={0.35} segments={128} />
      
      {/* Órbita de la Tierra (referencia) */}
      <Orbit radius={100} color="#4a9eff" opacity={0.45} segments={128} />
      
      {/* Órbita de Marte */}
      <Orbit radius={152} color="#c97a5f" opacity={0.35} segments={128} />
    </group>
  )
}

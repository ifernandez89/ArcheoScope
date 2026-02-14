'use client'

import { useMemo } from 'react'
import * as THREE from 'three'

/**
 * Órbita de la Luna alrededor de la Tierra
 * En coordenadas relativas a la Tierra (no al Sol)
 */
export default function LunarOrbitLine() {
  const orbitGeometry = useMemo(() => {
    const points: THREE.Vector3[] = []
    const segments = 64
    const radius = 12 // Mismo radio que SimpleMoon
    const inclination = 5 * (Math.PI / 180) // Inclinación de 5°
    
    for (let i = 0; i <= segments; i++) {
      const angle = (i / segments) * Math.PI * 2
      const x = Math.cos(angle) * radius
      const z = Math.sin(angle) * radius
      const y = Math.sin(angle) * radius * Math.sin(inclination)
      points.push(new THREE.Vector3(x, y, z))
    }
    
    return new THREE.BufferGeometry().setFromPoints(points)
  }, [])
  
  return (
    <primitive object={new THREE.Line(orbitGeometry, new THREE.LineBasicMaterial({
      color: '#888888',
      transparent: true,
      opacity: 0.25,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    }))} />
  )
}

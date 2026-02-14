'use client'

import { useMemo } from 'react'
import * as THREE from 'three'

/**
 * Estrellas procedurales de fondo
 */
export default function Stars() {
  const starsGeometry = useMemo(() => {
    const geometry = new THREE.BufferGeometry()
    const count = 15000
    const positions = new Float32Array(count * 3)
    const colors = new Float32Array(count * 3)
    
    for (let i = 0; i < count; i++) {
      const i3 = i * 3
      positions[i3] = (Math.random() - 0.5) * 2000
      positions[i3 + 1] = (Math.random() - 0.5) * 2000
      positions[i3 + 2] = (Math.random() - 0.5) * 2000
      
      const color = new THREE.Color()
      color.setHSL(Math.random() * 0.2 + 0.5, 0.3, 0.8 + Math.random() * 0.2)
      colors[i3] = color.r
      colors[i3 + 1] = color.g
      colors[i3 + 2] = color.b
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))
    
    return geometry
  }, [])
  
  const starsMaterial = useMemo(() => {
    return new THREE.PointsMaterial({
      size: 1.5,
      vertexColors: true,
      transparent: true,
      opacity: 0.8,
      sizeAttenuation: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    })
  }, [])
  
  return <points name="Stars" geometry={starsGeometry} material={starsMaterial} />
}

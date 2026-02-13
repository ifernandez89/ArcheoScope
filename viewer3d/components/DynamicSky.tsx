'use client'

/**
 * DynamicSky - Cielo que cambia entre día (azul) y noche (negro con estrellas)
 * Controlado por el sistema astronómico
 */

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface DynamicSkyProps {
  isDay?: boolean
  sunPosition?: THREE.Vector3
}

export default function DynamicSky({ isDay = true, sunPosition }: DynamicSkyProps) {
  const skyRef = useRef<THREE.Mesh>(null)
  const starsRef = useRef<THREE.Points>(null)
  
  // Geometría de estrellas
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
      size: 3,
      vertexColors: true,
      transparent: true,
      opacity: 0,  // Empezar invisible
      sizeAttenuation: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    })
  }, [])
  
  // Actualizar visibilidad según hora del día
  useFrame(() => {
    if (skyRef.current && starsRef.current) {
      const skyMaterial = skyRef.current.material as THREE.MeshBasicMaterial
      const starsMat = starsRef.current.material as THREE.PointsMaterial
      
      if (isDay) {
        // Día: cielo azul, sin estrellas
        skyMaterial.color.lerp(new THREE.Color('#87ceeb'), 0.05)
        starsMat.opacity += (0 - starsMat.opacity) * 0.05
      } else {
        // Noche: cielo negro, con estrellas
        skyMaterial.color.lerp(new THREE.Color('#000814'), 0.05)
        starsMat.opacity += (0.9 - starsMat.opacity) * 0.05
      }
    }
  })
  
  return (
    <>
      {/* Esfera de cielo */}
      <mesh ref={skyRef}>
        <sphereGeometry args={[500, 32, 32]} />
        <meshBasicMaterial 
          color="#87ceeb"
          side={THREE.BackSide}
          fog={false}
        />
      </mesh>
      
      {/* Estrellas */}
      <points 
        ref={starsRef} 
        name="Stars" 
        geometry={starsGeometry} 
        material={starsMaterial} 
      />
    </>
  )
}

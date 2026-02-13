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
    const count = 10000 // Reducido de 15000 a 10000 (33% menos densidad)
    const positions = new Float32Array(count * 3)
    const colors = new Float32Array(count * 3)
    const sizes = new Float32Array(count) // Tamaños variables
    
    for (let i = 0; i < count; i++) {
      const i3 = i * 3
      positions[i3] = (Math.random() - 0.5) * 2000
      positions[i3 + 1] = (Math.random() - 0.5) * 2000
      positions[i3 + 2] = (Math.random() - 0.5) * 2000
      
      // Colores más variados y sutiles
      const color = new THREE.Color()
      const hue = Math.random() * 0.15 + 0.55 // Azul-blanco
      const saturation = Math.random() * 0.2 + 0.1 // Baja saturación
      const lightness = 0.7 + Math.random() * 0.3 // Brillante
      color.setHSL(hue, saturation, lightness)
      colors[i3] = color.r
      colors[i3 + 1] = color.g
      colors[i3 + 2] = color.b
      
      // Tamaños variables (algunas estrellas más grandes, la mayoría muy pequeñas)
      sizes[i] = Math.random() < 0.05 ? Math.random() * 2 + 1 : Math.random() * 0.8 + 0.3
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))
    geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1))
    
    return geometry
  }, [])
  
  const starsMaterial = useMemo(() => {
    // Crear textura circular suave para las estrellas
    const canvas = document.createElement('canvas')
    canvas.width = 32
    canvas.height = 32
    const ctx = canvas.getContext('2d')!
    
    // Gradiente radial para efecto de glow suave
    const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16)
    gradient.addColorStop(0, 'rgba(255, 255, 255, 1)')
    gradient.addColorStop(0.2, 'rgba(255, 255, 255, 0.8)')
    gradient.addColorStop(0.4, 'rgba(255, 255, 255, 0.4)')
    gradient.addColorStop(0.7, 'rgba(255, 255, 255, 0.1)')
    gradient.addColorStop(1, 'rgba(255, 255, 255, 0)')
    
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, 32, 32)
    
    const texture = new THREE.CanvasTexture(canvas)
    texture.needsUpdate = true
    
    return new THREE.PointsMaterial({
      size: 1.2, // Reducido de 2 a 1.2 (40% más pequeñas)
      vertexColors: true,
      transparent: true,
      opacity: 0,  // Empezar invisible
      sizeAttenuation: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
      map: texture, // Textura circular suave
      alphaTest: 0.01, // Eliminar bordes duros
      fog: false // No afectadas por niebla
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
        // Noche: cielo negro, con estrellas más sutiles
        skyMaterial.color.lerp(new THREE.Color('#000814'), 0.05)
        starsMat.opacity += (0.6 - starsMat.opacity) * 0.05 // Reducido de 0.9 a 0.6
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

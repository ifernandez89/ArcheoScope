/**
 * 🪐 Saturn Rings - Anillos de Saturno
 * 
 * MEJORAS IMPLEMENTADAS (v1.2.6):
 * ✓ División de Cassini visible (gap entre anillos A y B)
 * ✓ Múltiples bandas (D, C, B, Cassini, A, F)
 * ✓ Textura radial procedural con variación
 * ✓ Opacidad variable por región
 * ✓ Propiedades físicas realistas (hielo)
 */

'use client'

import { useMemo } from 'react'
import * as THREE from 'three'

interface SaturnRingsProps {
  saturnRadius: number
  ringTexture: THREE.Texture
  tilt?: number
}

/**
 * Generar textura radial procedural con bandas de Saturno
 * Incluye: Ring D, C, B, Cassini Division, A, F
 */
function generateRingTexture(size = 2048): THREE.CanvasTexture {
  const canvas = document.createElement('canvas')
  canvas.width = size
  canvas.height = 1
  const ctx = canvas.getContext('2d')!
  
  const gradient = ctx.createLinearGradient(0, 0, size, 0)
  
  // Ring D (innermost, very faint)
  gradient.addColorStop(0.00, 'rgba(250, 213, 165, 0.05)')
  gradient.addColorStop(0.10, 'rgba(250, 213, 165, 0.08)')
  
  // Ring C (translucent gray)
  gradient.addColorStop(0.10, 'rgba(240, 220, 190, 0.15)')
  gradient.addColorStop(0.25, 'rgba(235, 215, 185, 0.25)')
  
  // Ring B (bright, dense) — más brillante antes de Cassini
  gradient.addColorStop(0.25, 'rgba(255, 240, 220, 0.85)')
  gradient.addColorStop(0.42, 'rgba(250, 235, 210, 0.90)')
  
  // ⭐ CASSINI DIVISION (gap) — completamente vacío
  gradient.addColorStop(0.42, 'rgba(0, 0, 0, 0.0)')
  gradient.addColorStop(0.47, 'rgba(0, 0, 0, 0.0)')
  
  // Ring A (bright) — más brillante después de Cassini
  gradient.addColorStop(0.47, 'rgba(250, 235, 210, 0.80)')
  gradient.addColorStop(0.75, 'rgba(245, 225, 200, 0.75)')
  
  // Encke Gap (mini gap en A)
  gradient.addColorStop(0.68, 'rgba(240, 220, 190, 0.30)')
  gradient.addColorStop(0.70, 'rgba(240, 220, 190, 0.30)')
  
  // Ring F (thin, faint outer ring)
  gradient.addColorStop(0.75, 'rgba(0, 0, 0, 0.0)')
  gradient.addColorStop(0.82, 'rgba(245, 220, 190, 0.20)')
  gradient.addColorStop(0.85, 'rgba(245, 220, 190, 0.15)')
  gradient.addColorStop(0.90, 'rgba(0, 0, 0, 0.0)')
  
  ctx.fillStyle = gradient
  ctx.fillRect(0, 0, size, 1)
  
  // Agregar variación procedural (líneas finas, turbulencia)
  const imageData = ctx.getImageData(0, 0, size, 1)
  const data = imageData.data
  
  for (let i = 0; i < size; i++) {
    const idx = i * 4
    const noise = Math.random() * 0.1 - 0.05
    const radialNoise = Math.sin(i * 0.05) * 0.08
    
    // Aplicar variación sutil
    data[idx] = Math.max(0, Math.min(255, data[idx] * (1 + noise + radialNoise)))
    data[idx + 1] = Math.max(0, Math.min(255, data[idx + 1] * (1 + noise + radialNoise)))
    data[idx + 2] = Math.max(0, Math.min(255, data[idx + 2] * (1 + noise + radialNoise)))
  }
  
  ctx.putImageData(imageData, 0, 0)
  
  // Convertir a DataTexture
  const texture = new THREE.CanvasTexture(canvas)
  texture.wrapS = THREE.ClampToEdgeWrapping
  texture.wrapT = THREE.ClampToEdgeWrapping
  texture.needsUpdate = true
  
  console.log('🪐 Textura radial procedural generada con División de Cassini')
  
  return texture
}

export default function SaturnRings({ 
  saturnRadius, 
  ringTexture,
  tilt = 26.7 
}: SaturnRingsProps) {
  // Radio real de los anillos de Saturno (en relación al radio del planeta)
  // Ring D: 1.11 - 1.23
  // Ring C: 1.23 - 1.52
  // Ring B: 1.52 - 1.95
  // Cassini Division: 1.95 - 2.02
  // Ring A: 2.02 - 2.27
  // Ring F: 2.32
  
  const innerRadius = saturnRadius * 1.11  // Ring D interior
  const outerRadius = saturnRadius * 2.32  // Ring F exterior
  const tiltRadians = (tilt * Math.PI) / 180
  
  // Generar textura procedural con bandas y Cassini Division
  const proceduralTexture = useMemo(() => generateRingTexture(2048), [])
  
  console.log('🪐 SaturnRings rendering (enhanced):', { saturnRadius, innerRadius, outerRadius, tilt })
  
  return (
    <group rotation={[Math.PI / 2, 0, tiltRadians]}>
      {/* Anillo principal con textura procedural y Cassini Division */}
      <mesh castShadow receiveShadow>
        <ringGeometry args={[innerRadius, outerRadius, 256]} />
        <meshStandardMaterial
          map={proceduralTexture}
          alphaMap={proceduralTexture}
          transparent
          opacity={1.0}
          side={THREE.DoubleSide}
          depthWrite={false}
          color="#ffffff"  // Blanco puro para que el mapa de color domine
          roughness={0.7}   // Hielo: superficie mate pero reflectante
          metalness={0.0}   // Hielo: no metálico
          emissive="#000000"
          emissiveIntensity={0}
        />
      </mesh>
      
      {/* Anillo trasero (cara inferior) con menos opacidad para profundidad */}
      <mesh position={[0, 0, -0.2]} receiveShadow>
        <ringGeometry args={[innerRadius, outerRadius, 256]} />
        <meshStandardMaterial
          map={proceduralTexture}
          alphaMap={proceduralTexture}
          transparent
          opacity={0.6}
          side={THREE.BackSide}
          depthWrite={false}
          color="#f5e5d0"
          roughness={0.8}
          metalness={0.0}
        />
      </mesh>
    </group>
  )
}

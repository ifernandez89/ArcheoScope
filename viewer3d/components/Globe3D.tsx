'use client'

import { useRef, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import { Sphere, useTexture } from '@react-three/drei'
import * as THREE from 'three'

interface Globe3DProps {
  onLocationClick?: (lat: number, lon: number) => void
}

export default function Globe3D({ onLocationClick }: Globe3DProps) {
  const globeRef = useRef<THREE.Mesh>(null)
  const [isRotating, setIsRotating] = useState(true)

  // Cargar texturas de la Tierra (usando texturas públicas)
  // En producción, usar texturas de mejor calidad
  const earthTexture = useTexture('/earth-texture.jpg', (texture) => {
    // Fallback: crear textura procedural si no existe
    if (!texture) {
      const canvas = document.createElement('canvas')
      canvas.width = 2048
      canvas.height = 1024
      const ctx = canvas.getContext('2d')!
      
      // Gradiente azul para océanos
      const gradient = ctx.createLinearGradient(0, 0, 0, 1024)
      gradient.addColorStop(0, '#1e3a8a')
      gradient.addColorStop(0.5, '#2563eb')
      gradient.addColorStop(1, '#1e3a8a')
      ctx.fillStyle = gradient
      ctx.fillRect(0, 0, 2048, 1024)
      
      // Agregar "continentes" simples
      ctx.fillStyle = '#22c55e'
      ctx.globalAlpha = 0.7
      
      // Simular continentes con formas aleatorias
      for (let i = 0; i < 50; i++) {
        const x = Math.random() * 2048
        const y = Math.random() * 1024
        const size = Math.random() * 200 + 50
        ctx.beginPath()
        ctx.arc(x, y, size, 0, Math.PI * 2)
        ctx.fill()
      }
      
      return new THREE.CanvasTexture(canvas)
    }
    return texture
  })

  // Rotación automática del globo
  useFrame((state, delta) => {
    if (globeRef.current && isRotating) {
      globeRef.current.rotation.y += delta * 0.1
    }
  })

  // Manejar click en el globo
  const handleClick = (event: THREE.Event) => {
    event.stopPropagation()
    
    if (!globeRef.current || !onLocationClick) return

    // Obtener punto de intersección
    const point = event.point
    
    // Convertir punto 3D a lat/lon
    const radius = 5
    const lat = Math.asin(point.y / radius) * (180 / Math.PI)
    const lon = Math.atan2(point.x, point.z) * (180 / Math.PI)
    
    console.log(`Click en globo: lat=${lat.toFixed(2)}, lon=${lon.toFixed(2)}`)
    
    // Detener rotación al hacer click
    setIsRotating(false)
    
    onLocationClick(lat, lon)
  }

  return (
    <group>
      {/* Globo terráqueo */}
      <Sphere
        ref={globeRef}
        args={[5, 64, 64]}
        onClick={handleClick}
        onPointerOver={() => document.body.style.cursor = 'pointer'}
        onPointerOut={() => document.body.style.cursor = 'default'}
      >
        <meshStandardMaterial
          map={earthTexture}
          roughness={0.8}
          metalness={0.2}
        />
      </Sphere>

      {/* Atmósfera (glow effect) */}
      <Sphere args={[5.1, 64, 64]}>
        <meshBasicMaterial
          color="#4a90e2"
          transparent
          opacity={0.1}
          side={THREE.BackSide}
        />
      </Sphere>

      {/* Luz ambiental para el globo */}
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
    </group>
  )
}

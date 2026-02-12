'use client'

import { useRef, useState, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface Globe3DProps {
  onLocationClick?: (lat: number, lon: number) => void
  markerPosition?: { lat: number, lon: number } | null
}

export default function Globe3D({ onLocationClick, markerPosition }: Globe3DProps) {
  const globeRef = useRef<THREE.Mesh>(null)
  const markerRef = useRef<THREE.Mesh>(null)
  const [isRotating, setIsRotating] = useState(true)
  const [earthTexture, setEarthTexture] = useState<THREE.Texture | null>(null)

  // Cargar texturas reales desde archivos locales
  useEffect(() => {
    const loader = new THREE.TextureLoader()
    
    // Cargar textura principal de la Tierra (8K)
    loader.load(
      '/textures/earth_8k.jpg',
      (texture) => {
        console.log('✅ Textura real 8K cargada exitosamente!')
        setEarthTexture(texture)
      },
      undefined,
      (error) => {
        console.error('❌ Error cargando textura real, usando fallback procedural')
        setEarthTexture(createProceduralEarthTexture())
      }
    )
  }, [])

  // Actualizar posición del marcador
  useEffect(() => {
    if (markerRef.current && markerPosition) {
      const pos = latLonToVector3(markerPosition.lat, markerPosition.lon, 5.2)
      markerRef.current.position.copy(pos)
    }
  }, [markerPosition])

  // Rotación automática del globo
  useFrame((state, delta) => {
    if (globeRef.current && isRotating) {
      globeRef.current.rotation.y += delta * 0.05
    }
    
    // Pulsar marcador
    if (markerRef.current && markerPosition) {
      const scale = 1 + Math.sin(state.clock.elapsedTime * 3) * 0.2
      markerRef.current.scale.setScalar(scale)
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
    
    console.log(`🌍 Click en globo: lat=${lat.toFixed(4)}, lon=${lon.toFixed(4)}`)
    
    // Detener rotación al hacer click
    setIsRotating(false)
    
    onLocationClick(lat, lon)
  }

  return (
    <group>
      {/* Globo terráqueo */}
      {earthTexture && (
        <mesh
          ref={globeRef}
          onClick={handleClick}
          onPointerOver={() => document.body.style.cursor = 'pointer'}
          onPointerOut={() => document.body.style.cursor = 'default'}
        >
          <sphereGeometry args={[5, 128, 128]} />
          <meshStandardMaterial
            map={earthTexture}
            roughness={0.7}
            metalness={0.1}
            emissive="#0a1929"
            emissiveIntensity={0.2}
          />
        </mesh>
      )}

      {/* Atmósfera (glow effect) */}
      <mesh>
        <sphereGeometry args={[5.15, 64, 64]} />
        <meshBasicMaterial
          color="#4a90e2"
          transparent
          opacity={0.15}
          side={THREE.BackSide}
        />
      </mesh>

      {/* Marcador de ubicación */}
      {markerPosition && (
        <mesh ref={markerRef}>
          <sphereGeometry args={[0.08, 16, 16]} />
          <meshBasicMaterial
            color="#ff0000"
            emissive="#ff0000"
            emissiveIntensity={2}
          />
        </mesh>
      )}

      {/* Iluminación */}
      <ambientLight intensity={0.3} />
      <directionalLight position={[10, 10, 5]} intensity={1.5} />
      <pointLight position={[-10, 0, -10]} intensity={0.5} color="#4a90e2" />
    </group>
  )
}

// Convertir lat/lon a posición 3D en esfera
function latLonToVector3(lat: number, lon: number, radius: number): THREE.Vector3 {
  const phi = (90 - lat) * (Math.PI / 180)
  const theta = (lon + 180) * (Math.PI / 180)
  
  const x = -radius * Math.sin(phi) * Math.cos(theta)
  const z = radius * Math.sin(phi) * Math.sin(theta)
  const y = radius * Math.cos(phi)
  
  return new THREE.Vector3(x, y, z)
}

// Crear textura procedural de alta calidad (fallback)
function createProceduralEarthTexture(): THREE.Texture {
  const canvas = document.createElement('canvas')
  canvas.width = 4096
  canvas.height = 2048
  const ctx = canvas.getContext('2d')!
  
  // Fondo oceánico con gradiente realista
  const oceanGradient = ctx.createLinearGradient(0, 0, 0, 2048)
  oceanGradient.addColorStop(0, '#0a1929')
  oceanGradient.addColorStop(0.3, '#1e3a5f')
  oceanGradient.addColorStop(0.5, '#2563eb')
  oceanGradient.addColorStop(0.7, '#1e3a5f')
  oceanGradient.addColorStop(1, '#0a1929')
  ctx.fillStyle = oceanGradient
  ctx.fillRect(0, 0, 4096, 2048)
  
  // Agregar textura de agua
  ctx.globalAlpha = 0.1
  for (let i = 0; i < 5000; i++) {
    const x = Math.random() * 4096
    const y = Math.random() * 2048
    const size = Math.random() * 3
    ctx.fillStyle = Math.random() > 0.5 ? '#3b82f6' : '#1e40af'
    ctx.fillRect(x, y, size, size)
  }
  ctx.globalAlpha = 1
  
  // Continentes con colores realistas
  const continentColor = '#2d5016'
  
  // América del Norte
  ctx.fillStyle = continentColor
  ctx.globalAlpha = 0.9
  ctx.beginPath()
  ctx.moveTo(600, 400)
  ctx.bezierCurveTo(700, 350, 800, 380, 850, 450)
  ctx.bezierCurveTo(900, 500, 880, 600, 820, 650)
  ctx.bezierCurveTo(750, 700, 650, 680, 600, 620)
  ctx.bezierCurveTo(550, 560, 520, 480, 600, 400)
  ctx.fill()
  
  // América del Sur
  ctx.beginPath()
  ctx.moveTo(750, 750)
  ctx.bezierCurveTo(800, 720, 850, 750, 870, 820)
  ctx.bezierCurveTo(880, 900, 850, 980, 800, 1020)
  ctx.bezierCurveTo(750, 1050, 700, 1030, 680, 980)
  ctx.bezierCurveTo(660, 920, 680, 850, 750, 750)
  ctx.fill()
  
  // Europa
  ctx.beginPath()
  ctx.moveTo(2000, 450)
  ctx.bezierCurveTo(2100, 420, 2200, 440, 2250, 500)
  ctx.bezierCurveTo(2280, 550, 2260, 600, 2200, 620)
  ctx.bezierCurveTo(2140, 640, 2050, 620, 2000, 580)
  ctx.bezierCurveTo(1960, 540, 1950, 490, 2000, 450)
  ctx.fill()
  
  // África
  ctx.beginPath()
  ctx.moveTo(2050, 650)
  ctx.bezierCurveTo(2150, 620, 2250, 650, 2300, 720)
  ctx.bezierCurveTo(2350, 800, 2340, 900, 2300, 980)
  ctx.bezierCurveTo(2250, 1060, 2150, 1100, 2050, 1080)
  ctx.bezierCurveTo(1980, 1060, 1950, 1000, 1960, 920)
  ctx.bezierCurveTo(1970, 840, 2000, 750, 2050, 650)
  ctx.fill()
  
  // Asia
  ctx.beginPath()
  ctx.moveTo(2400, 400)
  ctx.bezierCurveTo(2600, 350, 2800, 380, 3000, 450)
  ctx.bezierCurveTo(3200, 520, 3300, 600, 3350, 700)
  ctx.bezierCurveTo(3380, 780, 3350, 850, 3280, 900)
  ctx.bezierCurveTo(3200, 950, 3050, 920, 2900, 880)
  ctx.bezierCurveTo(2750, 840, 2600, 780, 2500, 700)
  ctx.bezierCurveTo(2400, 620, 2350, 520, 2400, 400)
  ctx.fill()
  
  // Australia
  ctx.beginPath()
  ctx.moveTo(3200, 1100)
  ctx.bezierCurveTo(3300, 1080, 3400, 1100, 3450, 1160)
  ctx.bezierCurveTo(3480, 1220, 3460, 1280, 3400, 1310)
  ctx.bezierCurveTo(3340, 1340, 3250, 1330, 3180, 1300)
  ctx.bezierCurveTo(3120, 1270, 3100, 1200, 3200, 1100)
  ctx.fill()
  
  // Agregar variación de terreno
  ctx.globalAlpha = 0.4
  ctx.fillStyle = '#4a6b2e'
  for (let i = 0; i < 50; i++) {
    const x = Math.random() * 4096
    const y = Math.random() * 2048
    const size = Math.random() * 100 + 50
    ctx.beginPath()
    ctx.arc(x, y, size, 0, Math.PI * 2)
    ctx.fill()
  }
  
  // Nubes realistas
  ctx.fillStyle = '#ffffff'
  ctx.globalAlpha = 0.15
  for (let i = 0; i < 200; i++) {
    const x = Math.random() * 4096
    const y = Math.random() * 2048
    const size = Math.random() * 80 + 40
    ctx.beginPath()
    ctx.arc(x, y, size, 0, Math.PI * 2)
    ctx.fill()
    
    ctx.globalAlpha = 0.08
    ctx.beginPath()
    ctx.arc(x + size * 0.5, y, size * 0.7, 0, Math.PI * 2)
    ctx.fill()
    ctx.globalAlpha = 0.15
  }
  
  const texture = new THREE.CanvasTexture(canvas)
  texture.needsUpdate = true
  return texture
}

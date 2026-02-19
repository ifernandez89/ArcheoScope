'use client'

/**
 * RealisticFog - Sistema de niebla profesional
 * 
 * Nivel 1: THREE.FogExp2 (base, casi cero costo)
 * Nivel 2: Ground mist layers (capas sutiles cerca del suelo)
 * Nivel 3: Volumetric fake (planos grandes con textura suave)
 */

import { useRef, useEffect, useMemo } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

interface RealisticFogProps {
  density: number // 0-1
  color?: string
  animated?: boolean
  groundMist?: boolean // Niebla cerca del suelo
  volumetricLayers?: boolean // Capas volumétricas sutiles
}

export default function RealisticFog({ 
  density = 0.5, 
  color = '#bfdfff',
  animated = true,
  groundMist = true,
  volumetricLayers = false
}: RealisticFogProps) {
  const { scene, gl } = useThree()
  const targetDensityRef = useRef(density)
  const currentDensityRef = useRef(0)
  const timeRef = useRef(0)
  
  // Configurar fog exponencial (base)
  useEffect(() => {
    if (!scene.fog) {
      scene.fog = new THREE.FogExp2(color, 0)
    }
    
    // Configurar color de fondo para que coincida
    gl.setClearColor(color)
    
    targetDensityRef.current = density
    
    console.log('🌫️ Niebla realista activada:', { 
      density, 
      color, 
      groundMist, 
      volumetricLayers 
    })
    
    return () => {
      scene.fog = null
      gl.setClearColor('#000000')
    }
  }, [scene, gl, color])
  
  // Animar densidad de niebla
  useFrame((state, delta) => {
    if (!scene.fog) return
    
    timeRef.current += delta
    
    // Transición suave de densidad
    const transitionSpeed = 0.5
    currentDensityRef.current += (targetDensityRef.current - currentDensityRef.current) * transitionSpeed * delta
    
    // Animación de pulsación sutil si está habilitada
    let finalDensity = currentDensityRef.current
    if (animated) {
      const pulse = Math.sin(timeRef.current * 0.2) * 0.05 // Muy sutil
      finalDensity = Math.max(0, currentDensityRef.current + pulse)
    }
    
    // Aplicar a la niebla (escalar para valores razonables)
    if (scene.fog instanceof THREE.FogExp2) {
      scene.fog.density = finalDensity * 0.015 // Densidad exponencial
      scene.fog.color.set(color)
    }
  })
  
  return (
    <>
      {/* Capas de niebla cerca del suelo */}
      {groundMist && density > 0.3 && (
        <GroundMistLayers density={density} color={color} />
      )}
      
      {/* Capas volumétricas sutiles (opcional, más pesado) */}
      {volumetricLayers && density > 0.5 && (
        <VolumetricLayers density={density} color={color} />
      )}
    </>
  )
}

/**
 * GroundMistLayers - Capas de niebla cerca del suelo
 * Simula niebla que se acumula en valles y zonas bajas
 */
function GroundMistLayers({ density, color }: { density: number; color: string }) {
  const groupRef = useRef<THREE.Group>(null)
  
  // Crear capas de niebla (planos horizontales sutiles)
  const layers = useMemo(() => {
    const layerCount = 3 // Pocas capas, muy sutiles
    const result: JSX.Element[] = []
    
    for (let i = 0; i < layerCount; i++) {
      const height = i * 2 + 0.5 // Altura escalonada
      const size = 200 - i * 20 // Más grande abajo, más pequeño arriba
      const opacity = (0.15 - i * 0.04) * density // Muy sutil
      
      result.push(
        <mesh 
          key={i}
          position={[0, height, 0]}
          rotation={[-Math.PI / 2, 0, 0]}
        >
          <planeGeometry args={[size, size, 1, 1]} />
          <meshBasicMaterial
            color={color}
            transparent
            opacity={opacity}
            depthWrite={false}
            side={THREE.DoubleSide}
            blending={THREE.NormalBlending}
          />
        </mesh>
      )
    }
    
    return result
  }, [density, color])
  
  // Animación sutil de rotación
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.05) * 0.1
    }
  })
  
  return <group ref={groupRef}>{layers}</group>
}

/**
 * VolumetricLayers - Capas volumétricas con textura de ruido
 * Más pesado, solo para hardware potente
 */
function VolumetricLayers({ density, color }: { density: number; color: string }) {
  const groupRef = useRef<THREE.Group>(null)
  
  // Crear textura de ruido procedural
  const noiseTexture = useMemo(() => {
    const size = 256
    const canvas = document.createElement('canvas')
    canvas.width = size
    canvas.height = size
    const ctx = canvas.getContext('2d')!
    
    // Gradiente radial suave
    const gradient = ctx.createRadialGradient(
      size / 2, size / 2, 0,
      size / 2, size / 2, size / 2
    )
    gradient.addColorStop(0, 'rgba(255, 255, 255, 0.8)')
    gradient.addColorStop(0.5, 'rgba(255, 255, 255, 0.4)')
    gradient.addColorStop(1, 'rgba(255, 255, 255, 0)')
    
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, size, size)
    
    // Agregar ruido sutil
    const imageData = ctx.getImageData(0, 0, size, size)
    const data = imageData.data
    for (let i = 0; i < data.length; i += 4) {
      const noise = Math.random() * 30 - 15
      data[i] += noise
      data[i + 1] += noise
      data[i + 2] += noise
    }
    ctx.putImageData(imageData, 0, 0)
    
    const texture = new THREE.CanvasTexture(canvas)
    texture.needsUpdate = true
    return texture
  }, [])
  
  // Crear pocas capas grandes con billboard
  const layers = useMemo(() => {
    const layerCount = 20 // Pocas capas, grandes
    const result: JSX.Element[] = []
    
    for (let i = 0; i < layerCount; i++) {
      const angle = (i / layerCount) * Math.PI * 2
      const radius = 30 + Math.random() * 40
      const x = Math.cos(angle) * radius
      const z = Math.sin(angle) * radius
      const y = Math.random() * 15 + 2
      const scale = 15 + Math.random() * 10
      const opacity = (0.1 + Math.random() * 0.1) * density
      
      result.push(
        <Billboard
          key={i}
          position={[x, y, z]}
          scale={scale}
          texture={noiseTexture}
          color={color}
          opacity={opacity}
        />
      )
    }
    
    return result
  }, [noiseTexture, color, density])
  
  // Animación muy lenta
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.elapsedTime * 0.01
    }
  })
  
  return <group ref={groupRef}>{layers}</group>
}

/**
 * Billboard - Sprite que siempre mira a la cámara
 */
function Billboard({ 
  position, 
  scale, 
  texture, 
  color, 
  opacity 
}: { 
  position: [number, number, number]
  scale: number
  texture: THREE.Texture
  color: string
  opacity: number
}) {
  const meshRef = useRef<THREE.Mesh>(null)
  const { camera } = useThree()
  
  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.lookAt(camera.position)
    }
  })
  
  return (
    <mesh ref={meshRef} position={position}>
      <planeGeometry args={[scale, scale]} />
      <meshBasicMaterial
        map={texture}
        color={color}
        transparent
        opacity={opacity}
        depthWrite={false}
        blending={THREE.NormalBlending}
      />
    </mesh>
  )
}

/**
 * Preset de niebla ligera (recomendado para ArcheoScope)
 */
export function LightFog({ density = 0.5, color = '#bfdfff' }: { density: number; color?: string }) {
  return (
    <RealisticFog
      density={density}
      color={color}
      animated={true}
      groundMist={true}
      volumetricLayers={false} // Desactivado para ligereza
    />
  )
}

/**
 * Preset de niebla pesada (para escenas dramáticas)
 */
export function HeavyFog({ density = 0.8, color = '#a0b0c0' }: { density: number; color?: string }) {
  return (
    <RealisticFog
      density={density}
      color={color}
      animated={true}
      groundMist={true}
      volumetricLayers={true} // Activado para efecto dramático
    />
  )
}

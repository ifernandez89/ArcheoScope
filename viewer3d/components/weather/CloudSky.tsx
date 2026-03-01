'use client'

/**
 * CloudSky - Sky dome con nubes atmosféricas
 * 
 * Características:
 * - Esfera invertida gigante (sky dome)
 * - Textura de nubes equirectangular
 * - Rotación lenta sincronizada con WindSystem
 * - Muy ligero (solo geometría + textura)
 * - Coherencia sistémica con viento
 */

import { useRef, useMemo } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { globalWind } from './RealisticWind'
import { getAssetPath } from '@/lib/paths'
import { loggers } from '@/core/Logger'

interface CloudSkyProps {
  enabled?: boolean
  opacity?: number // 0-1
  speed?: number // Velocidad de rotación
  height?: number // Altura del dome
  radius?: number // Radio del dome
  stormMode?: boolean // Nubes oscuras para tormenta
}

export default function CloudSky({
  enabled = true,
  opacity = 0.9,
  speed = 1.0,
  height = 100,
  radius = 500,
  stormMode = false
}: CloudSkyProps) {
  
  loggers.weather.debug('CloudSky renderizado:', { enabled, opacity, height, radius, stormMode })
  const meshRef = useRef<THREE.Mesh>(null)
  const { camera } = useThree()
  
  // Cargar textura de nubes
  // TODO: Agregar textura real cuando esté disponible
  // const cloudTexture = useTexture(getAssetPath('/textures/2k_earth_clouds.jpg'))
  
  // Crear textura procedural temporal (mientras no hay archivo)
  const cloudTexture = useMemo(() => {
    const canvas = document.createElement('canvas')
    canvas.width = 1024
    canvas.height = 512
    const ctx = canvas.getContext('2d')!
    
    // Fondo transparente
    ctx.clearRect(0, 0, 1024, 512)
    
    // Colores según modo tormenta
    const cloudColors = stormMode ? {
      core: 'rgba(60, 60, 70, 0.95)',      // Gris muy oscuro
      mid: 'rgba(80, 80, 90, 0.85)',       // Gris oscuro
      edge: 'rgba(100, 100, 110, 0.5)',    // Gris medio
      fade: 'rgba(120, 120, 130, 0)'       // Fade gris
    } : {
      core: 'rgba(255, 255, 255, 0.95)',   // Blanco
      mid: 'rgba(250, 250, 250, 0.8)',     // Blanco suave
      edge: 'rgba(240, 240, 245, 0.5)',    // Blanco azulado
      fade: 'rgba(230, 230, 240, 0)'       // Fade blanco
    }
    
    // Crear nubes SOLO en la mitad superior (cielo)
    const cloudCount = stormMode ? 120 : 60 // DUPLICADO: Más nubes en tormenta (era 60:30)
    
    for (let i = 0; i < cloudCount; i++) {
      const x = Math.random() * 1024
      const y = Math.random() * 256 // Solo en la mitad superior (0-256)
      const baseWidth = stormMode 
        ? 25 + Math.random() * 40  // Ancho base (más grande en tormenta)
        : 20 + Math.random() * 30
      const baseHeight = baseWidth * (0.4 + Math.random() * 0.3) // Altura 40-70% del ancho (ovalada)
      
      // Cada nube tiene varios "puffs" para aspecto esponjoso
      const puffCount = 4 + Math.floor(Math.random() * 4) // 4-7 puffs
      
      for (let j = 0; j < puffCount; j++) {
        // Distribuir puffs más horizontalmente (forma ovalada)
        const offsetX = (Math.random() - 0.5) * baseWidth * 1.5
        const offsetY = (Math.random() - 0.5) * baseHeight * 0.8
        
        // Radio de cada puff (elíptico)
        const puffRadiusX = baseWidth * (0.4 + Math.random() * 0.3)
        const puffRadiusY = baseHeight * (0.5 + Math.random() * 0.4)
        
        // Usar escala para crear elipse
        ctx.save()
        ctx.translate(x + offsetX, y + offsetY)
        ctx.scale(puffRadiusX / puffRadiusY, 1) // Escalar horizontalmente
        
        // Gradiente radial suave (circular, pero escalado = elipse)
        const gradient = ctx.createRadialGradient(0, 0, 0, 0, 0, puffRadiusY)
        gradient.addColorStop(0, cloudColors.core)
        gradient.addColorStop(0.3, cloudColors.mid)
        gradient.addColorStop(0.6, cloudColors.edge)
        gradient.addColorStop(1, cloudColors.fade)
        
        ctx.fillStyle = gradient
        ctx.beginPath()
        ctx.arc(0, 0, puffRadiusY, 0, Math.PI * 2)
        ctx.fill()
        ctx.restore()
      }
    }
    
    const texture = new THREE.CanvasTexture(canvas)
    texture.wrapS = THREE.RepeatWrapping
    texture.wrapT = THREE.ClampToEdgeWrapping
    
    loggers.weather.debug(`Textura de nubes esponjosas creada: ${stormMode ? 'TORMENTA (oscuras)' : 'normales (blancas)'}`)
    return texture
  }, [stormMode])
  
  // Geometría de esfera invertida
  const geometry = useMemo(() => {
    const geo = new THREE.SphereGeometry(radius, 32, 16)
    // Invertir normales para que se vea desde dentro
    geo.scale(-1, 1, 1)
    return geo
  }, [radius])
  
  // Material
  const material = useMemo(() => {
    return new THREE.MeshBasicMaterial({
      map: cloudTexture,
      transparent: true,
      opacity: opacity,
      side: THREE.DoubleSide, // Visible desde ambos lados
      depthWrite: false,
      fog: false // No afectado por niebla
    })
  }, [cloudTexture, opacity])
  
  // Animar rotación basada en viento
  useFrame((state, delta) => {
    if (!meshRef.current || !enabled) return
    
    // Seguir cámara (sky dome siempre centrado en cámara)
    meshRef.current.position.copy(camera.position)
    meshRef.current.position.y = camera.position.y + height // Cambié a + para que esté arriba
    
    // Rotar según dirección del viento (muy lento)
    const windDirection = globalWind.direction
    const windStrength = globalWind.strength
    
    // Rotación en Y basada en dirección del viento
    const rotationSpeed = windStrength * speed * 0.00005 // Muy lento
    meshRef.current.rotation.y += rotationSpeed
    
    // Pequeña oscilación en X (efecto de deriva)
    meshRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.05) * 0.02
  })
  
  if (!enabled) return null
  
  return (
    <mesh
      ref={meshRef}
      geometry={geometry}
      material={material}
      renderOrder={-100} // Renderizar muy atrás (fondo del cielo)
      frustumCulled={false} // No hacer culling (siempre visible)
    />
  )
}

/**
 * CloudLayers - Capas de nubes en planos (alternativa más detallada)
 * Más pesado pero más control
 */
export function CloudLayers({
  enabled = true,
  layerCount = 3,
  opacity = 0.4,
  speed = 1.0
}: {
  enabled?: boolean
  layerCount?: number
  opacity?: number
  speed?: number
}) {
  const groupRef = useRef<THREE.Group>(null)
  
  // Crear textura procedural para cada capa
  const layerTextures = useMemo(() => {
    const textures: THREE.Texture[] = []
    
    for (let i = 0; i < layerCount; i++) {
      const canvas = document.createElement('canvas')
      canvas.width = 512
      canvas.height = 512
      const ctx = canvas.getContext('2d')!
      
      // Fondo transparente
      ctx.clearRect(0, 0, 512, 512)
      
      // Nubes con gradiente radial
      const cloudCount = 5 + Math.floor(Math.random() * 5)
      for (let j = 0; j < cloudCount; j++) {
        const x = Math.random() * 512
        const y = Math.random() * 512
        const radius = 40 + Math.random() * 80
        
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius)
        gradient.addColorStop(0, `rgba(255, 255, 255, ${0.6 + Math.random() * 0.3})`)
        gradient.addColorStop(0.5, `rgba(255, 255, 255, ${0.3 + Math.random() * 0.2})`)
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0)')
        
        ctx.fillStyle = gradient
        ctx.beginPath()
        ctx.arc(x, y, radius, 0, Math.PI * 2)
        ctx.fill()
      }
      
      const texture = new THREE.CanvasTexture(canvas)
      texture.wrapS = THREE.RepeatWrapping
      texture.wrapT = THREE.RepeatWrapping
      textures.push(texture)
    }
    
    return textures
  }, [layerCount])
  
  // Crear capas
  const layers = useMemo(() => {
    return Array.from({ length: layerCount }, (_, i) => {
      const height = 30 + i * 15 // Altura escalonada
      const size = 300 + i * 50 // Más grande arriba
      const layerOpacity = opacity * (1 - i * 0.2) // Más transparente arriba
      
      return {
        height,
        size,
        opacity: layerOpacity,
        texture: layerTextures[i],
        speed: 1 + i * 0.3 // Más rápido arriba
      }
    })
  }, [layerCount, opacity, layerTextures])
  
  // Animar capas
  useFrame((state, delta) => {
    if (!groupRef.current || !enabled) return
    
    groupRef.current.children.forEach((child, i) => {
      if (child instanceof THREE.Mesh) {
        const layer = layers[i]
        
        // Mover según viento
        const windDirection = globalWind.direction
        const windStrength = globalWind.strength
        
        child.position.x += windDirection.x * windStrength * layer.speed * speed * delta * 0.5
        child.position.z += windDirection.z * windStrength * layer.speed * speed * delta * 0.5
        
        // Wrap around (ciclo infinito)
        if (Math.abs(child.position.x) > 200) {
          child.position.x = -Math.sign(child.position.x) * 200
        }
        if (Math.abs(child.position.z) > 200) {
          child.position.z = -Math.sign(child.position.z) * 200
        }
      }
    })
  })
  
  if (!enabled) return null
  
  return (
    <group ref={groupRef}>
      {layers.map((layer, i) => (
        <mesh
          key={i}
          position={[0, layer.height, 0]}
          rotation={[-Math.PI / 2, 0, 0]}
        >
          <planeGeometry args={[layer.size, layer.size]} />
          <meshBasicMaterial
            map={layer.texture}
            transparent
            opacity={layer.opacity}
            depthWrite={false}
            side={THREE.DoubleSide}
          />
        </mesh>
      ))}
    </group>
  )
}

/**
 * Preset ligero (recomendado)
 */
export function LightClouds({ 
  opacity = 0.85,
  stormMode = false 
}: { 
  opacity?: number
  stormMode?: boolean 
}) {
  if (stormMode) {
    // Tormenta: 3 capas densas a distintas alturas y velocidades
    return (
      <>
        {/* Capa baja - muy densa y oscura */}
        <CloudSky enabled={true} opacity={0.98} speed={1.8} height={60}  radius={350} stormMode={true} />
        {/* Capa media - cobertura total */}
        <CloudSky enabled={true} opacity={0.92} speed={1.2} height={100} radius={500} stormMode={true} />
        {/* Capa alta - más difusa, movimiento lento */}
        <CloudSky enabled={true} opacity={0.75} speed={0.6} height={160} radius={700} stormMode={true} />
      </>
    )
  }

  return (
    <CloudSky
      enabled={true}
      opacity={opacity}
      speed={1.0}
      height={80}
      radius={400}
      stormMode={false}
    />
  )
}

/**
 * Preset con capas (más detallado)
 */
export function LayeredClouds({ opacity = 0.4 }: { opacity?: number }) {
  return (
    <>
      <CloudSky enabled={true} opacity={opacity * 0.5} speed={0.5} />
      <CloudLayers enabled={true} layerCount={2} opacity={opacity} speed={1.0} />
    </>
  )
}

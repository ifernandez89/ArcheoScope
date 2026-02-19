'use client'

/**
 * ProceduralLightning - Flash visual sincronizado con audio
 * 
 * Efectos:
 * - Flash global (ambient light)
 * - Aumento de exposure
 * - Sombras intensas momentáneas
 * - Opcional: línea de rayo en el cielo
 */

import { useRef, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'
import { getLightningManager, type LightningStrike } from '@/systems/LightningSystem'

interface ProceduralLightningProps {
  enabled: boolean
  intensity?: number // 0-1
  showBolt?: boolean // Mostrar línea de rayo
  minDistance?: number
  maxDistance?: number
  minInterval?: number
  maxInterval?: number
}

export default function ProceduralLightning({
  enabled,
  intensity = 1.0,
  showBolt = false,
  minDistance = 200,
  maxDistance = 3000,
  minInterval = 3000,
  maxInterval = 10000
}: ProceduralLightningProps) {
  const { scene, gl } = useThree()
  const flashLightRef = useRef<THREE.DirectionalLight>(null)
  const flashIntensityRef = useRef(0)
  const boltRef = useRef<THREE.Line | null>(null)
  const lightningManager = getLightningManager()
  
  // Inicializar sistema de rayos
  useEffect(() => {
    if (!enabled) {
      lightningManager.stop()
      return
    }
    
    // Configurar
    lightningManager.updateConfig({
      minDistance,
      maxDistance,
      minInterval,
      maxInterval,
      intensity
    })
    
    // Callback para flash visual
    lightningManager.onFlash((strike: LightningStrike) => {
      triggerFlash(strike)
    })
    
    // Iniciar
    lightningManager.start()
    
    return () => {
      lightningManager.stop()
    }
  }, [enabled, intensity, minDistance, maxDistance, minInterval, maxInterval])
  
  /**
   * Disparar flash visual
   */
  const triggerFlash = (strike: LightningStrike) => {
    // Intensidad del flash basada en distancia
    const flashIntensity = Math.max(0.3, 1 - (strike.distance / 4000)) * strike.intensity
    flashIntensityRef.current = flashIntensity
    
    // Crear línea de rayo si está habilitado
    if (showBolt && boltRef.current) {
      createBolt(strike)
    }
    
    console.log(`⚡ Flash visual: ${strike.distance.toFixed(0)}m, intensidad: ${flashIntensity.toFixed(2)}`)
  }
  
  /**
   * Crear línea de rayo zigzag
   */
  const createBolt = (strike: LightningStrike) => {
    if (!boltRef.current) return
    
    // Generar puntos zigzag
    const points: THREE.Vector3[] = []
    const segments = 8 + Math.floor(Math.random() * 4) // 8-12 segmentos
    const startHeight = 50 + Math.random() * 30
    const distance = strike.distance * 0.5 // Más cerca visualmente
    
    const startX = strike.direction.x * distance
    const startZ = strike.direction.z * distance
    
    points.push(new THREE.Vector3(startX, startHeight, startZ))
    
    for (let i = 1; i < segments; i++) {
      const t = i / segments
      const x = startX + (Math.random() - 0.5) * 10
      const y = startHeight * (1 - t) + Math.random() * 5
      const z = startZ + (Math.random() - 0.5) * 10
      points.push(new THREE.Vector3(x, y, z))
    }
    
    // Punto final en el suelo
    points.push(new THREE.Vector3(
      startX + (Math.random() - 0.5) * 5,
      0,
      startZ + (Math.random() - 0.5) * 5
    ))
    
    // Actualizar geometría
    const geometry = new THREE.BufferGeometry().setFromPoints(points)
    boltRef.current.geometry.dispose()
    boltRef.current.geometry = geometry
    boltRef.current.visible = true
    
    // Ocultar después de un momento
    setTimeout(() => {
      if (boltRef.current) {
        boltRef.current.visible = false
      }
    }, 100 + Math.random() * 100) // 100-200ms
  }
  
  // Animar flash
  useFrame((state, delta) => {
    // Decay del flash
    if (flashIntensityRef.current > 0) {
      flashIntensityRef.current -= delta * 8 // Decay rápido
      flashIntensityRef.current = Math.max(0, flashIntensityRef.current)
      
      // Aplicar a luz direccional
      if (flashLightRef.current) {
        flashLightRef.current.intensity = flashIntensityRef.current * 3
      }
      
      // Aplicar a ambient light de la escena (si existe)
      scene.traverse((object) => {
        if (object instanceof THREE.AmbientLight) {
          const baseIntensity = 0.5 // Intensidad base
          object.intensity = baseIntensity + flashIntensityRef.current * 2
        }
      })
      
      // Ajustar exposure del renderer (opcional)
      if (flashIntensityRef.current > 0.5) {
        gl.toneMappingExposure = 1.2 + flashIntensityRef.current * 0.5
      } else {
        gl.toneMappingExposure = 1.2
      }
    }
  })
  
  if (!enabled) return null
  
  return (
    <>
      {/* Luz direccional para el flash */}
      <directionalLight
        ref={flashLightRef}
        position={[0, 50, 0]}
        intensity={0}
        color="#a0d0ff"
        castShadow={false}
      />
      
      {/* Línea de rayo (opcional) */}
      {showBolt && (
        <line
          ref={(ref) => {
            if (ref) boltRef.current = ref as unknown as THREE.Line
          }}
        >
          <bufferGeometry />
          <lineBasicMaterial
            color="#ffffff"
            linewidth={3}
            transparent
            opacity={0.9}
          />
        </line>
      )}
    </>
  )
}

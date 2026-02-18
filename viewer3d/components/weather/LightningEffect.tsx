'use client'

import { useRef, useState, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

interface LightningEffectProps {
  enabled: boolean
  intensity?: number
}

export default function LightningEffect({ enabled, intensity = 1 }: LightningEffectProps) {
  const [isFlashing, setIsFlashing] = useState(false)
  const [flashPhase, setFlashPhase] = useState(0) // 0: apagado, 1: primer flash, 2: pausa, 3: segundo flash
  const flashIntensityRef = useRef(0)
  const phaseTimerRef = useRef(0)
  const { scene, gl } = useThree()
  const originalExposureRef = useRef(1)
  
  // Escuchar eventos de rayo
  useEffect(() => {
    if (!enabled) return
    
    const handleLightning = (e: Event) => {
      const customEvent = e as CustomEvent
      triggerLightning(customEvent.detail?.intensity || 1)
    }
    
    window.addEventListener('weather:lightning', handleLightning)
    return () => window.removeEventListener('weather:lightning', handleLightning)
  }, [enabled])
  
  const triggerLightning = (strength: number) => {
    setIsFlashing(true)
    setFlashPhase(1) // Primer flash
    flashIntensityRef.current = strength
    phaseTimerRef.current = 0
    
    // Guardar exposure original
    if (gl.toneMappingExposure) {
      originalExposureRef.current = gl.toneMappingExposure
    }
  }
  
  useFrame((state, delta) => {
    if (!enabled) return
    
    // Manejar fases del rayo (doble descarga)
    if (isFlashing) {
      phaseTimerRef.current += delta
      
      switch (flashPhase) {
        case 1: // Primer flash (80ms)
          if (phaseTimerRef.current > 0.08) {
            setFlashPhase(2)
            phaseTimerRef.current = 0
            flashIntensityRef.current = 0
          }
          break
        case 2: // Pausa (50ms)
          if (phaseTimerRef.current > 0.05) {
            setFlashPhase(3)
            phaseTimerRef.current = 0
            flashIntensityRef.current = intensity * 0.6 // Segundo flash más débil
          }
          break
        case 3: // Segundo flash (40ms)
          if (phaseTimerRef.current > 0.04) {
            setFlashPhase(0)
            setIsFlashing(false)
            flashIntensityRef.current = 0
          }
          break
      }
    }
    
    // Fade out del flash
    if (flashIntensityRef.current > 0 && flashPhase === 0) {
      flashIntensityRef.current = Math.max(0, flashIntensityRef.current - delta * 10)
    }
    
    // Aplicar flash ambiental con exposure
    if (flashIntensityRef.current > 0) {
      // Aumentar exposure durante el flash
      gl.toneMappingExposure = originalExposureRef.current + flashIntensityRef.current * 0.4
      
      // Aplicar emissive a materiales
      scene.traverse((obj) => {
        if (obj instanceof THREE.Mesh && obj.material) {
          const material = obj.material as THREE.MeshStandardMaterial
          if (material.emissive) {
            material.emissiveIntensity = flashIntensityRef.current * 0.3
          }
        }
      })
    } else {
      // Restaurar exposure
      gl.toneMappingExposure = originalExposureRef.current
    }
  })
  
  if (!enabled) return null
  
  return (
    <>
      {/* Flash ambiental intenso */}
      {isFlashing && flashPhase !== 2 && (
        <>
          <ambientLight 
            intensity={flashIntensityRef.current * 4} 
            color="#e0f0ff" 
          />
          {/* Múltiples luces direccionales para simular el rayo */}
          <directionalLight
            position={[(Math.random() - 0.5) * 40, 50, (Math.random() - 0.5) * 40]}
            intensity={flashIntensityRef.current * 8}
            color="#ffffff"
          />
          <directionalLight
            position={[(Math.random() - 0.5) * 40, 45, (Math.random() - 0.5) * 40]}
            intensity={flashIntensityRef.current * 5}
            color="#a0c0ff"
          />
          {/* Luz puntual en el punto de impacto */}
          <pointLight
            position={[(Math.random() - 0.5) * 30, 0, (Math.random() - 0.5) * 30]}
            intensity={flashIntensityRef.current * 10}
            distance={30}
            color="#ffffff"
          />
        </>
      )}
    </>
  )
}

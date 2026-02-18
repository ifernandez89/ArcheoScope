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
  const flashIntensityRef = useRef(0)
  const lightningMeshRef = useRef<THREE.Mesh>(null)
  const { scene } = useThree()
  
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
    flashIntensityRef.current = strength
    
    // Sonido de trueno (opcional, después del flash)
    setTimeout(() => {
      // Aquí se podría agregar sonido
      console.log('⚡ Thunder!')
    }, 300 + Math.random() * 500)
  }
  
  useFrame((state, delta) => {
    if (!enabled) return
    
    // Fade out del flash
    if (flashIntensityRef.current > 0) {
      flashIntensityRef.current = Math.max(0, flashIntensityRef.current - delta * 8)
      
      if (flashIntensityRef.current === 0) {
        setIsFlashing(false)
      }
      
      // Aplicar flash ambiental
      scene.traverse((obj) => {
        if (obj instanceof THREE.Mesh && obj.material) {
          const material = obj.material as THREE.MeshStandardMaterial
          if (material.emissive) {
            material.emissiveIntensity = flashIntensityRef.current * 0.5
          }
        }
      })
    }
  })
  
  if (!enabled) return null
  
  return (
    <>
      {/* Flash ambiental */}
      {isFlashing && (
        <>
          <ambientLight 
            intensity={flashIntensityRef.current * 3} 
            color="#a0c0ff" 
          />
          {/* Luz direccional para simular el rayo */}
          <directionalLight
            position={[(Math.random() - 0.5) * 50, 50, (Math.random() - 0.5) * 50]}
            intensity={flashIntensityRef.current * 5}
            color="#ffffff"
          />
        </>
      )}
    </>
  )
}

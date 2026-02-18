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
        <ambientLight 
          intensity={flashIntensityRef.current * 3} 
          color="#a0c0ff" 
        />
      )}
      
      {/* Rayo visual (mesh procedural) */}
      {isFlashing && (
        <LightningBolt intensity={flashIntensityRef.current} />
      )}
    </>
  )
}

// Componente del rayo visual
function LightningBolt({ intensity }: { intensity: number }) {
  const meshRef = useRef<THREE.Mesh>(null)
  const geometryRef = useRef<THREE.BufferGeometry>()
  
  useEffect(() => {
    // Generar geometría del rayo
    const points: THREE.Vector3[] = []
    const segments = 20
    const startY = 50
    const endY = 0
    
    let currentX = (Math.random() - 0.5) * 30
    let currentZ = (Math.random() - 0.5) * 30
    
    for (let i = 0; i <= segments; i++) {
      const t = i / segments
      const y = startY - t * startY
      
      // Agregar variación aleatoria
      if (i > 0 && i < segments) {
        currentX += (Math.random() - 0.5) * 3
        currentZ += (Math.random() - 0.5) * 3
      }
      
      points.push(new THREE.Vector3(currentX, y, currentZ))
      
      // Ramificaciones ocasionales
      if (Math.random() > 0.7 && i > 5 && i < segments - 5) {
        const branchLength = Math.floor(segments * 0.3)
        let branchX = currentX
        let branchZ = currentZ
        
        for (let j = 0; j < branchLength; j++) {
          branchX += (Math.random() - 0.5) * 2
          branchZ += (Math.random() - 0.5) * 2
          const branchY = y - j * 2
          points.push(new THREE.Vector3(branchX, branchY, branchZ))
        }
      }
    }
    
    const geometry = new THREE.BufferGeometry().setFromPoints(points)
    geometryRef.current = geometry
  }, [])
  
  if (!geometryRef.current) return null
  
  return (
    <line ref={meshRef}>
      <bufferGeometry attach="geometry" {...geometryRef.current} />
      <lineBasicMaterial
        attach="material"
        color="#a0d0ff"
        linewidth={3}
        transparent
        opacity={intensity}
        blending={THREE.AdditiveBlending}
      />
    </line>
  )
}

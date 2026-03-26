'use client'

import { useRef, useState, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { Mesh, MeshStandardMaterial } from 'three'
import VisualLightningBolt from './VisualLightningBolt'

interface LightningEffectProps {
  enabled: boolean
  intensity?: number
  showVisualBolts?: boolean
}

interface LightningBolt {
  id: number
  startPosition: [number, number, number]
  endPosition: [number, number, number]
}

export default function LightningEffect({ 
  enabled, 
  intensity = 1,
  showVisualBolts = true 
}: LightningEffectProps) {
  const [isFlashing, setIsFlashing] = useState(false)
  const [flashPhase, setFlashPhase] = useState(0)
  const [activeBolts, setActiveBolts] = useState<LightningBolt[]>([])
  const flashIntensityRef = useRef(0)
  const phaseTimerRef = useRef(0)
  const boltIdCounter = useRef(0)
  const nextBoltTimeRef = useRef(0)
  const { scene, gl } = useThree()
  const originalExposureRef = useRef(1)
  
  // Cache de meshes con emissive para evitar traverse cada frame
  const cachedEmissiveMeshes = useRef<{ mesh: Mesh, material: MeshStandardMaterial }[]>([])
  const meshesCached = useRef(false)
  
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
    setFlashPhase(1)
    flashIntensityRef.current = strength
    phaseTimerRef.current = 0
    
    if (gl.toneMappingExposure) {
      originalExposureRef.current = gl.toneMappingExposure
    }
    
    // Generar rayo visual
    if (showVisualBolts) {
      spawnLightningBolt()
    }
  }
  
  const spawnLightningBolt = () => {
    const startX = (Math.random() - 0.5) * 60
    const startZ = (Math.random() - 0.5) * 60
    const endX = startX + (Math.random() - 0.5) * 20
    const endZ = startZ + (Math.random() - 0.5) * 20
    
    const newBolt: LightningBolt = {
      id: boltIdCounter.current++,
      startPosition: [startX, 50, startZ],
      endPosition: [endX, 0, endZ]
    }
    
    setActiveBolts(prev => [...prev, newBolt])
  }
  
  const removeBolt = (id: number) => {
    setActiveBolts(prev => prev.filter(bolt => bolt.id !== id))
  }
  
  useFrame((state, delta) => {
    if (!enabled) return
    
    // Generar rayos visuales periódicamente
    if (showVisualBolts && enabled) {
      nextBoltTimeRef.current -= delta
      if (nextBoltTimeRef.current <= 0) {
        // Intervalo aleatorio entre 2-5 segundos
        nextBoltTimeRef.current = 2 + Math.random() * 3
        spawnLightningBolt()
        // Trigger flash también
        triggerLightning(intensity)
      }
    }
    
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
            flashIntensityRef.current = intensity * 0.6
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
      gl.toneMappingExposure = originalExposureRef.current + flashIntensityRef.current * 0.4
      
      // Cache meshes con emissive solo una vez
      if (!meshesCached.current) {
        cachedEmissiveMeshes.current = []
        scene.traverse((obj) => {
          if (obj instanceof Mesh && obj.material) {
            const material = obj.material as MeshStandardMaterial
            if (material.emissive) {
              cachedEmissiveMeshes.current.push({ mesh: obj, material })
            }
          }
        })
        meshesCached.current = true
      }
      
      // Aplicar a meshes cacheados
      for (const { material } of cachedEmissiveMeshes.current) {
        material.emissiveIntensity = flashIntensityRef.current * 0.3
      }
    } else {
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
          <pointLight
            position={[(Math.random() - 0.5) * 30, 0, (Math.random() - 0.5) * 30]}
            intensity={flashIntensityRef.current * 10}
            distance={30}
            color="#ffffff"
          />
        </>
      )}
      
      {/* Rayos visuales activos */}
      {showVisualBolts && activeBolts.map(bolt => (
        <VisualLightningBolt
          key={bolt.id}
          startPosition={bolt.startPosition}
          endPosition={bolt.endPosition}
          onComplete={() => removeBolt(bolt.id)}
          duration={0.15}
        />
      ))}
    </>
  )
}

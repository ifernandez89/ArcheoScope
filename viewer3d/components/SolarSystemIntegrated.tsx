'use client'

import { useState, useEffect } from 'react'
import { useThree } from '@react-three/fiber'
import SolarSystem from './SolarSystem'

/**
 * Sistema Solar Integrado con transición basada en zoom
 * 
 * Lógica de transición:
 * - Distancia < 20: Modo contemplation (solo Tierra y Luna)
 * - Distancia 20-50: Modo revelation (aparece Sol pequeño)
 * - Distancia 50-100: Modo expansion (aparecen Marte y Venus)
 * - Distancia > 100: Modo system (vista completa)
 */

interface SolarSystemIntegratedProps {
  latitude: number;
  longitude: number;
}

export default function SolarSystemIntegrated({
  latitude,
  longitude
}: SolarSystemIntegratedProps) {
  const { camera } = useThree()
  const [mode, setMode] = useState<'contemplation' | 'revelation' | 'expansion' | 'system'>('contemplation')
  const [showEcliptic, setShowEcliptic] = useState(false)
  const [showOrbits, setShowOrbits] = useState(false)
  
  useEffect(() => {
    const updateMode = () => {
      // Calcular distancia de la cámara al origen
      const distance = camera.position.length()
      
      // Transición suave basada en distancia
      if (distance < 20) {
        setMode('contemplation')
        setShowEcliptic(false)
        setShowOrbits(false)
      } else if (distance < 50) {
        setMode('revelation')
        setShowEcliptic(true)
        setShowOrbits(false)
      } else if (distance < 100) {
        setMode('expansion')
        setShowEcliptic(true)
        setShowOrbits(true)
      } else {
        setMode('system')
        setShowEcliptic(true)
        setShowOrbits(true)
      }
    }
    
    // Actualizar cada frame
    const interval = setInterval(updateMode, 100)
    
    return () => clearInterval(interval)
  }, [camera])
  
  return (
    <SolarSystem
      latitude={latitude}
      longitude={longitude}
      mode={mode}
      showEcliptic={showEcliptic}
      showOrbits={showOrbits}
    />
  )
}

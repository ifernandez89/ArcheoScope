'use client'

import { useState, useRef } from 'react'
import { useThree, useFrame } from '@react-three/fiber'
import SolarSystem from './SolarSystem'

interface SolarSystemIntegratedProps {
  latitude: number;
  longitude: number;
}

export default function SolarSystemIntegrated({ latitude, longitude }: SolarSystemIntegratedProps) {
  const { camera } = useThree()
  const [mode, setMode] = useState<'contemplation' | 'revelation' | 'expansion' | 'system'>('contemplation')
  const [showEcliptic, setShowEcliptic] = useState(false)
  const [showOrbits, setShowOrbits] = useState(false)
  const lastDistRef = useRef(0)
  
  // Reemplaza setInterval con useFrame - solo actualiza si la distancia cambió significativamente
  useFrame(() => {
    const distance = camera.position.length()
    if (Math.abs(distance - lastDistRef.current) < 1) return // sin cambio significativo
    lastDistRef.current = distance
    
    if (distance < 20) {
      setMode('contemplation'); setShowEcliptic(false); setShowOrbits(false)
    } else if (distance < 50) {
      setMode('revelation'); setShowEcliptic(true); setShowOrbits(false)
    } else if (distance < 100) {
      setMode('expansion'); setShowEcliptic(true); setShowOrbits(true)
    } else {
      setMode('system'); setShowEcliptic(true); setShowOrbits(true)
    }
  })
  
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

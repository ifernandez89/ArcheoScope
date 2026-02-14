'use client'

import { useState } from 'react'
import RealisticSolarSystemScene from '@/components/RealisticSolarSystemScene'

/**
 * Página de prueba para el Sistema Solar Realista
 * 
 * Acceso: http://localhost:3000/realistic-solar
 */
export default function RealisticSolarPage() {
  const [selectedLocation, setSelectedLocation] = useState<{ lat: number, lon: number } | null>(null)
  
  const handleLocationClick = (lat: number, lon: number) => {
    console.log(`🌍 Click en: lat=${lat.toFixed(4)}, lon=${lon.toFixed(4)}`)
    setSelectedLocation({ lat, lon })
  }
  
  return (
    <main style={{ width: '100vw', height: '100vh', margin: 0, padding: 0 }}>
      <RealisticSolarSystemScene 
        onLocationClick={handleLocationClick}
        markerPosition={selectedLocation}
      />
    </main>
  )
}

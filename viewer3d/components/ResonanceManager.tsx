/**
 * ResonanceManager - Gestor de anomalías de resonancia
 * Detecta y renderiza campos de anomalía según ubicación
 */

'use client'

import { useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import ResonanceField from './ResonanceField'
import { resonanceSystem } from '../physics/ResonanceSystem'
import { detectAnomalies, configToField } from '@/utils/anomaly-detector'

interface ResonanceManagerProps {
  location?: { lat: number, lon: number } | null
  enabled?: boolean
}

// Función para obtener nombre de ubicación
function getLocationName(lat: number, lon: number): string {
  // Machu Picchu
  if (Math.abs(lat - (-13.1631)) < 0.1 && Math.abs(lon - (-72.5450)) < 0.1) {
    return 'Machu Picchu'
  }
  // Isla de Pascua
  if (Math.abs(lat - (-27.1127)) < 0.1 && Math.abs(lon - (-109.3497)) < 0.1) {
    return 'Easter Island'
  }
  // Nazca
  if (Math.abs(lat - (-14.7390)) < 0.2 && Math.abs(lon - (-75.1300)) < 0.2) {
    return 'Nazca Lines'
  }
  // Stonehenge
  if (Math.abs(lat - 51.1789) < 0.1 && Math.abs(lon - (-1.8262)) < 0.1) {
    return 'Stonehenge'
  }
  // Giza
  if (Math.abs(lat - 29.9792) < 0.1 && Math.abs(lon - 31.1342) < 0.1) {
    return 'Giza Pyramids'
  }
  // Angkor Wat
  if (Math.abs(lat - 13.4125) < 0.1 && Math.abs(lon - 103.8670) < 0.1) {
    return 'Angkor Wat'
  }
  // Teotihuacán
  if (Math.abs(lat - 19.6925) < 0.1 && Math.abs(lon - (-98.8438)) < 0.1) {
    return 'Teotihuacan'
  }
  // Petra
  if (Math.abs(lat - 30.3285) < 0.1 && Math.abs(lon - 35.4444) < 0.1) {
    return 'Petra'
  }
  
  return `Location (${lat.toFixed(2)}, ${lon.toFixed(2)})`
}

export default function ResonanceManager({ 
  location, 
  enabled = true 
}: ResonanceManagerProps) {
  
  // Detectar y cargar anomalías cuando cambia la ubicación
  useEffect(() => {
    if (!location || !enabled) {
      resonanceSystem.clear()
      return
    }
    
    // Limpiar anomalías anteriores
    resonanceSystem.clear()
    
    // Detectar anomalías en esta ubicación
    const anomalyConfigs = detectAnomalies(location.lat, location.lon)
    
    // Agregar al sistema
    for (const config of anomalyConfigs) {
      const field = configToField(config)
      resonanceSystem.addAnomaly(field)
    }
    
    const locationName = getLocationName(location.lat, location.lon)
    console.log(`🌌 ${anomalyConfigs.length} anomalías cargadas para ${locationName}`)
    
    // LOG EN ARCHIVO
    if (typeof window !== 'undefined' && (window as any).fileLogger) {
      ;(window as any).fileLogger.log('LOCATION', `Arrived at ${locationName}`, {
        lat: location.lat,
        lon: location.lon,
        anomalies: anomalyConfigs.length
      })
    }
    
    // 📊 CAPTURAR SNAPSHOT AUTOMÁTICO al llegar a la ubicación
    if (typeof window !== 'undefined' && (window as any).perfMonitor) {
      setTimeout(() => {
        ;(window as any).perfMonitor.createSnapshot(locationName, 'Clear', anomalyConfigs.length)
        console.log(`📸 Snapshot automático capturado: ${locationName}`)
      }, 2000) // Esperar 2 segundos para que todo cargue
    }
    
    // Cleanup al desmontar
    return () => {
      resonanceSystem.clear()
    }
  }, [location, enabled])
  
  // Actualizar sistema cada frame
  useFrame((state, delta) => {
    if (enabled) {
      resonanceSystem.update(delta)
    }
  })
  
  // Renderizar campos visuales
  const activeAnomalies = resonanceSystem.getActiveAnomalies()
  
  if (!enabled || activeAnomalies.length === 0) {
    return null
  }
  
  return (
    <group>
      {activeAnomalies.map((anomaly) => (
        <ResonanceField
          key={anomaly.id}
          position={[anomaly.position.x, anomaly.position.y, anomaly.position.z]}
          radius={anomaly.radius}
          intensity={anomaly.intensity}
          type={anomaly.type}
        />
      ))}
    </group>
  )
}

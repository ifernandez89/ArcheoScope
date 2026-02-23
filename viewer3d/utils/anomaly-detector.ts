/**
 * Detector de Anomalías por Ubicación
 * Define qué anomalías existen en cada sitio arqueológico
 */

import * as THREE from 'three'
import { AnomalyField } from '../physics/types'

interface AnomalyConfig {
  id: string
  position: [number, number, number]
  radius: number
  intensity: number
  frequency: number
  type: 'gravity' | 'mass' | 'spatial' | 'temporal'
}

/**
 * Verificar si coordenadas están cerca de un punto
 */
function isNear(lat: number, lon: number, targetLat: number, targetLon: number, threshold = 0.5): boolean {
  const latDiff = Math.abs(lat - targetLat)
  const lonDiff = Math.abs(lon - targetLon)
  return latDiff < threshold && lonDiff < threshold
}

/**
 * Detectar anomalías según ubicación geográfica
 */
export function detectAnomalies(lat: number, lon: number): AnomalyConfig[] {
  const anomalies: AnomalyConfig[] = []
  
  // 🏔️ MACHU PICCHU - Anomalía Gravitacional
  // Coordenadas: -13.1631°, -72.5450°
  if (isNear(lat, lon, -13.1631, -72.5450, 0.1)) {
    anomalies.push({
      id: 'machu-picchu-gravity',
      position: [0, 8, 0],
      radius: 25,
      intensity: 0.9,
      frequency: 0.4,
      type: 'gravity'
    })
    
    console.log('🏔️ Machu Picchu: Anomalía gravitacional detectada')
  }
  
  // 🗿 ISLA DE PASCUA - Anomalía de Masa
  // Coordenadas: -27.1127°, -109.3497°
  if (isNear(lat, lon, -27.1127, -109.3497, 0.1)) {
    anomalies.push({
      id: 'easter-island-mass',
      position: [0, 5, 0],
      radius: 20,
      intensity: 1.1,
      frequency: 0.3,
      type: 'mass'
    })
    
    console.log('🗿 Isla de Pascua: Anomalía de masa detectada')
  }
  
  // 🌀 LÍNEAS DE NAZCA - Anomalía Espacial
  // Coordenadas: -14.7390°, -75.1300°
  if (isNear(lat, lon, -14.7390, -75.1300, 0.2)) {
    anomalies.push({
      id: 'nazca-spatial',
      position: [0, 3, 0],
      radius: 50,
      intensity: 1.3,
      frequency: 0.25,
      type: 'spatial'
    })
    
    console.log('🌀 Nazca: Anomalía espacial detectada')
  }
  
  // ⏰ STONEHENGE - Anomalía Temporal
  // Coordenadas: 51.1789°, -1.8262°
  if (isNear(lat, lon, 51.1789, -1.8262, 0.1)) {
    anomalies.push({
      id: 'stonehenge-temporal',
      position: [0, 4, 0],
      radius: 18,
      intensity: 0.8,
      frequency: 0.5,
      type: 'temporal'
    })
    
    console.log('⏰ Stonehenge: Anomalía temporal detectada')
  }
  
  // 🔺 PIRÁMIDES DE GIZA - Anomalía Gravitacional + Espacial
  // Coordenadas: 29.9792°, 31.1342°
  if (isNear(lat, lon, 29.9792, 31.1342, 0.1)) {
    anomalies.push({
      id: 'giza-gravity',
      position: [0, 10, 0],
      radius: 30,
      intensity: 1.0,
      frequency: 0.35,
      type: 'gravity'
    })
    
    anomalies.push({
      id: 'giza-spatial',
      position: [15, 5, 15],
      radius: 20,
      intensity: 0.7,
      frequency: 0.4,
      type: 'spatial'
    })
    
    console.log('🔺 Giza: Anomalías múltiples detectadas')
  }
  
  // 🏛️ ANGKOR WAT - Anomalía de Masa
  // Coordenadas: 13.4125°, 103.8670°
  if (isNear(lat, lon, 13.4125, 103.8670, 0.1)) {
    anomalies.push({
      id: 'angkor-mass',
      position: [0, 6, 0],
      radius: 22,
      intensity: 0.85,
      frequency: 0.45,
      type: 'mass'
    })
    
    console.log('🏛️ Angkor Wat: Anomalía de masa detectada')
  }
  
  // 🌋 TEOTIHUACÁN - Anomalía Espacial
  // Coordenadas: 19.6925°, -98.8438°
  if (isNear(lat, lon, 19.6925, -98.8438, 0.1)) {
    anomalies.push({
      id: 'teotihuacan-spatial',
      position: [0, 7, 0],
      radius: 28,
      intensity: 1.0,
      frequency: 0.3,
      type: 'spatial'
    })
    
    console.log('🌋 Teotihuacán: Anomalía espacial detectada')
  }
  
  // 🗻 PETRA - Anomalía Temporal
  // Coordenadas: 30.3285°, 35.4444°
  if (isNear(lat, lon, 30.3285, 35.4444, 0.1)) {
    anomalies.push({
      id: 'petra-temporal',
      position: [0, 5, 0],
      radius: 20,
      intensity: 0.75,
      frequency: 0.55,
      type: 'temporal'
    })
    
    console.log('🗻 Petra: Anomalía temporal detectada')
  }
  
  return anomalies
}

/**
 * Convertir configuración a AnomalyField
 */
export function configToField(config: AnomalyConfig): AnomalyField {
  return {
    id: config.id,
    position: new THREE.Vector3(...config.position),
    radius: config.radius,
    intensity: config.intensity,
    frequency: config.frequency,
    type: config.type,
    active: true
  }
}

/**
 * Obtener descripción de anomalía
 */
export function getAnomalyDescription(type: string): string {
  const descriptions = {
    gravity: 'Campo gravitacional alterado - Flotación y caída invertida',
    mass: 'Densidad dimensional aumentada - Movimiento ralentizado',
    spatial: 'Distorsión del espacio-tiempo - Geometría no euclidiana',
    temporal: 'Dilatación temporal - Percepción del tiempo alterada'
  }
  
  return descriptions[type as keyof typeof descriptions] || 'Anomalía desconocida'
}

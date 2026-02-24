/**
 * AnomalyManager - Gestor de anomalías con campo de resonancia
 * 
 * Modelo simple:
 * - Cada anomalía tiene posición, radio, intensidad, frecuencia
 * - Campo de resonancia calculado por superposición
 * - Sin física compleja, solo matemática simple
 */

import * as THREE from 'three'

export interface Anomaly {
  id: string
  position: THREE.Vector3
  radius: number          // Radio de influencia
  intensity: number       // Intensidad [0, 1]
  frequency: number       // Frecuencia de oscilación
  active: boolean
}

export class AnomalyManager {
  private anomalies: Map<string, Anomaly> = new Map()
  private time: number = 0
  
  /**
   * Agregar anomalía
   */
  addAnomaly(anomaly: Anomaly): void {
    this.anomalies.set(anomaly.id, anomaly)
    console.log(`🌀 Anomalía agregada: ${anomaly.id}`)
  }
  
  /**
   * Remover anomalía
   */
  removeAnomaly(id: string): void {
    this.anomalies.delete(id)
    console.log(`🌀 Anomalía removida: ${id}`)
  }
  
  /**
   * Obtener anomalía
   */
  getAnomaly(id: string): Anomaly | undefined {
    return this.anomalies.get(id)
  }
  
  /**
   * Obtener todas las anomalías
   */
  getAllAnomalies(): Anomaly[] {
    return Array.from(this.anomalies.values())
  }
  
  /**
   * Actualizar tiempo (llamar cada frame)
   */
  update(deltaTime: number): void {
    this.time += deltaTime
  }
  
  /**
   * 🌊 Calcular resonancia en una posición
   * Retorna valor [-1, 1]
   */
  getResonanceAtPosition(pos: THREE.Vector3): number {
    let total = 0
    
    this.anomalies.forEach(anomaly => {
      if (!anomaly.active) return
      
      const distance = pos.distanceTo(anomaly.position)
      
      // Solo afecta dentro del radio
      if (distance < anomaly.radius) {
        // Falloff lineal
        const falloff = 1 - (distance / anomaly.radius)
        
        // Oscilación temporal
        const oscillation = Math.sin(this.time * anomaly.frequency)
        
        // Contribución de esta anomalía
        total += oscillation * anomaly.intensity * falloff
      }
    })
    
    // Clamp a [-1, 1]
    return Math.max(-1, Math.min(1, total))
  }
  
  /**
   * 🌊 Calcular resonancia con ruido Perlin (más orgánico)
   * Requiere función de ruido externa
   */
  getResonanceAtPositionWithNoise(
    pos: THREE.Vector3, 
    noiseFn: (x: number, z: number) => number,
    noiseScale: number = 0.1
  ): number {
    let total = 0
    
    this.anomalies.forEach(anomaly => {
      if (!anomaly.active) return
      
      const distance = pos.distanceTo(anomaly.position)
      
      if (distance < anomaly.radius) {
        // Falloff lineal base
        const falloff = 1 - (distance / anomaly.radius)
        
        // Ruido para hacer el campo irregular
        const noiseValue = noiseFn(pos.x * noiseScale, pos.z * noiseScale)
        const noiseFalloff = falloff * (0.5 + noiseValue * 0.5)
        
        // Oscilación temporal
        const oscillation = Math.sin(this.time * anomaly.frequency)
        
        // Contribución
        total += oscillation * anomaly.intensity * noiseFalloff
      }
    })
    
    return Math.max(-1, Math.min(1, total))
  }
  
  /**
   * Verificar si una posición está dentro de alguna anomalía
   */
  isInsideAnomaly(pos: THREE.Vector3): boolean {
    for (const anomaly of this.anomalies.values()) {
      if (!anomaly.active) continue
      
      const distance = pos.distanceTo(anomaly.position)
      if (distance < anomaly.radius) {
        return true
      }
    }
    return false
  }
  
  /**
   * Obtener anomalía más cercana
   */
  getClosestAnomaly(pos: THREE.Vector3): Anomaly | null {
    let closest: Anomaly | null = null
    let minDistance = Infinity
    
    this.anomalies.forEach(anomaly => {
      if (!anomaly.active) return
      
      const distance = pos.distanceTo(anomaly.position)
      if (distance < minDistance) {
        minDistance = distance
        closest = anomaly
      }
    })
    
    return closest
  }
  
  /**
   * Limpiar todas las anomalías
   */
  clear(): void {
    this.anomalies.clear()
    console.log('🌀 Todas las anomalías removidas')
  }
  
  /**
   * Obtener tiempo actual
   */
  getTime(): number {
    return this.time
  }
}

// Singleton
let anomalyManager: AnomalyManager | null = null

export function getAnomalyManager(): AnomalyManager {
  if (!anomalyManager) {
    anomalyManager = new AnomalyManager()
  }
  return anomalyManager
}

export default AnomalyManager

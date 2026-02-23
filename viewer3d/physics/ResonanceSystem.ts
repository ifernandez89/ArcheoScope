/**
 * ResonanceSystem - Sistema principal de resonancia dimensional
 * Gestiona todas las anomalías y aplica efectos
 */

import * as THREE from 'three'
import { AnomalyField } from './AnomalyField'
import { AnomalyField as IAnomalyField, ResonanceData, ResonanceEffect } from './types'

export class ResonanceSystem {
  private anomalies: Map<string, AnomalyField> = new Map()
  private enabled: boolean = true
  
  constructor() {
    console.log('🌌 ResonanceSystem initialized')
  }
  
  /**
   * Agregar una anomalía al sistema
   */
  addAnomaly(config: IAnomalyField): void {
    const anomaly = new AnomalyField(config)
    this.anomalies.set(anomaly.id, anomaly)
    console.log(`✨ Anomaly added: ${anomaly.id} (${anomaly.type})`)
  }
  
  /**
   * Remover una anomalía
   */
  removeAnomaly(id: string): void {
    this.anomalies.delete(id)
    console.log(`🗑️ Anomaly removed: ${id}`)
  }
  
  /**
   * Obtener anomalía por ID
   */
  getAnomaly(id: string): AnomalyField | undefined {
    return this.anomalies.get(id)
  }
  
  /**
   * Actualizar todas las anomalías
   */
  update(deltaTime: number): void {
    if (!this.enabled) return
    
    for (const anomaly of this.anomalies.values()) {
      anomaly.update(deltaTime)
    }
  }
  
  /**
   * FUNCIÓN CLAVE: Obtener resonancia total en una posición
   */
  getResonanceAtPosition(position: THREE.Vector3): ResonanceData[] {
    const resonances: ResonanceData[] = []
    
    for (const anomaly of this.anomalies.values()) {
      const value = anomaly.getResonanceAt(position)
      
      if (value > 0) {
        resonances.push({
          value,
          distance: anomaly.position.distanceTo(position),
          anomalyId: anomaly.id,
          type: anomaly.type
        })
      }
    }
    
    return resonances
  }
  
  /**
   * Obtener resonancia total (suma de todas)
   */
  getTotalResonance(position: THREE.Vector3): number {
    const resonances = this.getResonanceAtPosition(position)
    return resonances.reduce((sum, r) => sum + r.value, 0)
  }
  
  /**
   * Calcular efectos de resonancia para física
   */
  calculateEffects(position: THREE.Vector3): ResonanceEffect {
    const resonances = this.getResonanceAtPosition(position)
    
    const effects: ResonanceEffect = {
      massMultiplier: 1,
      gravityScale: 1,
      spatialDistortion: 0,
      temporalDilation: 1
    }
    
    for (const resonance of resonances) {
      switch (resonance.type) {
        case 'gravity':
          // Gravedad invertida o reducida
          effects.gravityScale -= resonance.value * 1.5
          break
          
        case 'mass':
          // Masa aumentada (movimiento más lento)
          effects.massMultiplier += resonance.value * 0.8
          break
          
        case 'spatial':
          // Distorsión espacial visual
          effects.spatialDistortion += resonance.value
          break
          
        case 'temporal':
          // Dilatación temporal (slow motion)
          effects.temporalDilation -= resonance.value * 0.3
          break
      }
    }
    
    // Clamp valores
    effects.gravityScale = Math.max(-2, Math.min(2, effects.gravityScale))
    effects.massMultiplier = Math.max(0.5, Math.min(3, effects.massMultiplier))
    effects.temporalDilation = Math.max(0.3, Math.min(1.5, effects.temporalDilation))
    
    return effects
  }
  
  /**
   * Aplicar efectos a uniforms de shader
   */
  applyToShader(material: THREE.ShaderMaterial, position: THREE.Vector3): void {
    const totalResonance = this.getTotalResonance(position)
    
    if (material.uniforms.resonance) {
      material.uniforms.resonance.value = totalResonance
    }
    
    // Encontrar anomalía más cercana para centro de distorsión
    let closestAnomaly: AnomalyField | null = null
    let minDistance = Infinity
    
    for (const anomaly of this.anomalies.values()) {
      const distance = anomaly.position.distanceTo(position)
      if (distance < minDistance && anomaly.active) {
        minDistance = distance
        closestAnomaly = anomaly
      }
    }
    
    if (closestAnomaly && material.uniforms.anomalyCenter) {
      material.uniforms.anomalyCenter.value.copy(closestAnomaly.position)
      material.uniforms.anomalyRadius.value = closestAnomaly.radius
    }
  }
  
  /**
   * Obtener anomalías activas
   */
  getActiveAnomalies(): AnomalyField[] {
    return Array.from(this.anomalies.values()).filter(a => a.active)
  }
  
  /**
   * Limpiar todas las anomalías
   */
  clear(): void {
    this.anomalies.clear()
    console.log('🧹 All anomalies cleared')
  }
  
  /**
   * Habilitar/deshabilitar sistema
   */
  setEnabled(enabled: boolean): void {
    this.enabled = enabled
    console.log(`🌌 ResonanceSystem ${enabled ? 'enabled' : 'disabled'}`)
  }
}

// Singleton global
export const resonanceSystem = new ResonanceSystem()

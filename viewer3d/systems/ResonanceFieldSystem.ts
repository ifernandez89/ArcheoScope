/**
 * ResonanceFieldSystem - Sistema de campo de resonancia ambiental
 * 
 * Integra:
 * - AnomalyManager (fuente de anomalías)
 * - Audio (modulación de sonido)
 * - Visual (uniforms para shaders)
 * - Física (impulsos sutiles)
 * 
 * Filosofía: Variable universal que todo consulta
 */

import * as THREE from 'three'
import { getAnomalyManager } from './AnomalyManager'
import { getClimateAudio } from './ClimateAudioSystem'

export interface ResonanceFieldConfig {
  updateInterval: number    // ms entre actualizaciones
  audioEnabled: boolean
  visualEnabled: boolean
  physicsEnabled: boolean
}

export class ResonanceFieldSystem {
  private anomalyManager = getAnomalyManager()
  private climateAudio = getClimateAudio()
  private config: ResonanceFieldConfig
  private lastUpdate = 0
  private currentResonance = 0
  
  // Uniforms para shaders (si se necesitan)
  public uniforms = {
    uResonance: { value: 0 },
    uTime: { value: 0 }
  }
  
  constructor(config: Partial<ResonanceFieldConfig> = {}) {
    this.config = {
      updateInterval: 50, // 20 FPS para resonancia
      audioEnabled: true,
      visualEnabled: true,
      physicsEnabled: false, // Deshabilitado por defecto
      ...config
    }
  }
  
  /**
   * Actualizar sistema (llamar cada frame)
   */
  update(deltaTime: number, playerPosition?: THREE.Vector3): void {
    // Actualizar tiempo en anomaly manager
    this.anomalyManager.update(deltaTime)
    
    // Throttle: solo actualizar cada X ms
    const now = Date.now()
    if (now - this.lastUpdate < this.config.updateInterval) {
      return
    }
    this.lastUpdate = now
    
    // Calcular resonancia en posición del jugador (o centro si no hay jugador)
    const position = playerPosition || new THREE.Vector3(0, 0, 0)
    this.currentResonance = this.anomalyManager.getResonanceAtPosition(position)
    
    // Actualizar uniforms para shaders
    if (this.config.visualEnabled) {
      this.uniforms.uResonance.value = this.currentResonance
      this.uniforms.uTime.value = this.anomalyManager.getTime()
    }
    
    // Actualizar audio
    if (this.config.audioEnabled && this.climateAudio.isResonanceEnabled()) {
      this.climateAudio.updateWithResonance(deltaTime)
    }
  }
  
  /**
   * Obtener resonancia actual
   */
  getCurrentResonance(): number {
    return this.currentResonance
  }
  
  /**
   * Obtener resonancia en posición específica
   */
  getResonanceAt(position: THREE.Vector3): number {
    return this.anomalyManager.getResonanceAtPosition(position)
  }
  
  /**
   * Aplicar efecto de resonancia a física (sutil)
   */
  applyPhysicsEffect(rigidBody: any): void {
    if (!this.config.physicsEnabled) return
    
    const resonance = this.currentResonance
    
    // Impulso vertical sutil
    // Positivo: ligera flotación
    // Negativo: más peso
    const impulse = {
      x: 0,
      y: resonance * 0.05, // Muy sutil
      z: 0
    }
    
    if (rigidBody && rigidBody.applyImpulse) {
      rigidBody.applyImpulse(impulse, true)
    }
  }
  
  /**
   * Obtener descripción del estado actual
   */
  getStateDescription(): {
    resonance: number
    state: 'harmonic' | 'dissonant' | 'neutral'
    description: string
  } {
    const resonance = this.currentResonance
    const absResonance = Math.abs(resonance)
    
    if (absResonance < 0.3) {
      return {
        resonance,
        state: 'neutral',
        description: 'Estado normal - Sin anomalías significativas'
      }
    } else if (resonance > 0.3) {
      return {
        resonance,
        state: 'harmonic',
        description: 'Zona armónica - Claridad y elevación'
      }
    } else {
      return {
        resonance,
        state: 'dissonant',
        description: 'Zona disonante - Inestabilidad y peso'
      }
    }
  }
  
  /**
   * Habilitar/deshabilitar audio
   */
  setAudioEnabled(enabled: boolean): void {
    this.config.audioEnabled = enabled
  }
  
  /**
   * Habilitar/deshabilitar visual
   */
  setVisualEnabled(enabled: boolean): void {
    this.config.visualEnabled = enabled
  }
  
  /**
   * Habilitar/deshabilitar física
   */
  setPhysicsEnabled(enabled: boolean): void {
    this.config.physicsEnabled = enabled
  }
}

// Singleton
let resonanceFieldSystem: ResonanceFieldSystem | null = null

export function getResonanceFieldSystem(): ResonanceFieldSystem {
  if (!resonanceFieldSystem) {
    resonanceFieldSystem = new ResonanceFieldSystem()
  }
  return resonanceFieldSystem
}

export default ResonanceFieldSystem

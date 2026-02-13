/**
 * MicroMotion - Micro-movimientos ambientales sutiles
 * Respiración lenta, nunca mareante, siempre contemplativo
 */

import * as THREE from 'three'

export interface MotionState {
  cameraSway: THREE.Vector3
  windIntensity: number
  atmosphericPulse: number
}

export class MicroMotion {
  private idleTime: number = 0
  private windTime: number = 0
  private userActive: boolean = false
  private lastUserActivity: number = 0
  
  // Frecuencias muy bajas
  private cameraSwayFrequencyX: number = 0.05
  private cameraSwayFrequencyY: number = 0.04
  private cameraSwayAmplitude: number = 0.002 // Casi imperceptible
  
  private windFrequency: number = 0.02
  private windAmplitude: number = 0.03

  /**
   * Notificar actividad del usuario (resetea idle)
   */
  notifyUserActivity() {
    this.userActive = true
    this.lastUserActivity = Date.now()
    this.idleTime = 0
  }

  /**
   * Actualizar estado de movimiento
   */
  update(deltaTime: number): MotionState {
    // Incrementar timers
    this.idleTime += deltaTime
    this.windTime += deltaTime
    
    // Detectar si usuario está inactivo (>2 segundos)
    const timeSinceActivity = (Date.now() - this.lastUserActivity) / 1000
    this.userActive = timeSinceActivity < 2
    
    // Oscilación de cámara (solo si está quieto)
    const cameraSway = new THREE.Vector3()
    if (!this.userActive && this.idleTime > 2) {
      const swayX = Math.sin(this.idleTime * this.cameraSwayFrequencyX) * this.cameraSwayAmplitude
      const swayY = Math.cos(this.idleTime * this.cameraSwayFrequencyY) * this.cameraSwayAmplitude * 0.75
      const swayZ = Math.sin(this.idleTime * this.cameraSwayFrequencyX * 0.5) * this.cameraSwayAmplitude * 0.5
      
      cameraSway.set(swayX, swayY, swayZ)
    }
    
    // Intensidad de viento atmosférico
    const windIntensity = 
      Math.sin(this.windTime * this.windFrequency) * this.windAmplitude +
      Math.sin(this.windTime * this.windFrequency * 1.7) * this.windAmplitude * 0.5
    
    // Pulso atmosférico (para variación de luz ambiental)
    const atmosphericPulse = Math.sin(this.windTime * 0.01) * 0.02
    
    return {
      cameraSway,
      windIntensity,
      atmosphericPulse
    }
  }

  /**
   * Resetear estado
   */
  reset() {
    this.idleTime = 0
    this.windTime = 0
    this.userActive = false
  }
}

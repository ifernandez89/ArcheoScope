/**
 * AnomalyField - Campo de anomalía individual
 * Representa una zona con física alterada
 */

import * as THREE from 'three'
import { AnomalyField as IAnomalyField, AnomalyType } from './types'

export class AnomalyField {
  public id: string
  public position: THREE.Vector3
  public radius: number
  public intensity: number
  public frequency: number
  public type: AnomalyType
  public active: boolean
  
  private time: number = 0
  private baseIntensity: number
  
  constructor(config: IAnomalyField) {
    this.id = config.id
    this.position = config.position.clone()
    this.radius = config.radius
    this.intensity = config.intensity
    this.baseIntensity = config.intensity
    this.frequency = config.frequency
    this.type = config.type
    this.active = config.active
  }
  
  /**
   * Actualizar oscilación temporal
   */
  update(deltaTime: number): void {
    if (!this.active) return
    
    this.time += deltaTime
    
    // Oscilación sinusoidal de intensidad
    const oscillation = Math.sin(this.time * this.frequency)
    this.intensity = this.baseIntensity * (0.7 + oscillation * 0.3)
  }
  
  /**
   * Calcular resonancia en una posición
   */
  getResonanceAt(position: THREE.Vector3): number {
    if (!this.active) return 0
    
    const distance = this.position.distanceTo(position)
    
    if (distance >= this.radius) return 0
    
    // Factor de caída suave (1 en centro, 0 en borde)
    const falloff = 1 - (distance / this.radius)
    
    // Resonancia = intensidad * caída
    return this.intensity * falloff
  }
  
  /**
   * Verificar si una posición está dentro del campo
   */
  contains(position: THREE.Vector3): boolean {
    return this.position.distanceTo(position) < this.radius
  }
  
  /**
   * Obtener distancia normalizada (0-1) desde el centro
   */
  getNormalizedDistance(position: THREE.Vector3): number {
    const distance = this.position.distanceTo(position)
    return Math.min(distance / this.radius, 1)
  }
}

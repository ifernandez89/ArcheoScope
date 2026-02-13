/**
 * SeasonalLight - Temperatura de color estacional sutil
 * Cambios lentos, transiciones suaves, sin datos técnicos
 */

import * as THREE from 'three'

export interface SeasonalState {
  seasonFactor: number // 0-1 (invierno a verano)
  lightColor: THREE.Color
  ambientIntensity: number
  seasonName: string
}

export class SeasonalLight {
  private winterColor: THREE.Color
  private summerColor: THREE.Color
  private currentColor: THREE.Color
  private targetColor: THREE.Color
  private smoothingSpeed: number = 0.005 // Muy lento

  constructor() {
    // Colores sutiles
    this.winterColor = new THREE.Color(0.85, 0.9, 1.0)   // Frío azulado
    this.summerColor = new THREE.Color(1.0, 0.95, 0.85)  // Cálido dorado
    this.currentColor = new THREE.Color()
    this.targetColor = new THREE.Color()
  }

  /**
   * Calcular estado estacional basado en fecha
   */
  calculateSeasonalState(): SeasonalState {
    const now = new Date()
    
    // Día del año
    const startOfYear = new Date(now.getFullYear(), 0, 0)
    const diff = now.getTime() - startOfYear.getTime()
    const dayOfYear = Math.floor(diff / 86400000)
    
    // Factor estacional (0 = invierno, 1 = verano)
    // Offset de 81 días para alinear con equinoccios
    const seasonFactor = (Math.sin((2 * Math.PI / 365) * (dayOfYear - 81)) + 1) / 2
    
    // Interpolar color
    const seasonalColor = this.winterColor.clone().lerp(this.summerColor, seasonFactor)
    
    // Intensidad ambiental sutil según estación
    const ambientIntensity = 0.3 + seasonFactor * 0.2
    
    // Nombre de estación (solo para debug, no mostrar)
    let seasonName = 'Transición'
    if (seasonFactor < 0.25) seasonName = 'Invierno'
    else if (seasonFactor < 0.5) seasonName = 'Primavera'
    else if (seasonFactor < 0.75) seasonName = 'Verano'
    else seasonName = 'Otoño'
    
    return {
      seasonFactor,
      lightColor: seasonalColor,
      ambientIntensity,
      seasonName
    }
  }

  /**
   * Actualizar color con interpolación suave
   */
  update(deltaTime: number): SeasonalState {
    const state = this.calculateSeasonalState()
    
    // Actualizar target
    this.targetColor.copy(state.lightColor)
    
    // Interpolación suave
    this.currentColor.lerp(this.targetColor, this.smoothingSpeed)
    
    return {
      ...state,
      lightColor: this.currentColor.clone()
    }
  }

  /**
   * Obtener color actual (suavizado)
   */
  getCurrentColor(): THREE.Color {
    return this.currentColor.clone()
  }
}

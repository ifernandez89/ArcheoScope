/**
 * SkyEngine - Cielo dinámico con rotación estelar
 * Movimiento continuo, transiciones suaves, sin catálogo completo
 */

import * as THREE from 'three'

export interface SkyState {
  siderealRotation: number
  skyIntensity: number
  starVisibility: number
  milkyWayVisible: boolean
}

export class SkyEngine {
  private siderealTime: number = 0
  private latitude: number = 0

  constructor(latitude: number = 0) {
    this.latitude = latitude
  }

  setLatitude(lat: number) {
    this.latitude = lat
  }

  /**
   * Calcular estado del cielo
   */
  calculateSkyState(solarAltitude: number): SkyState {
    const now = new Date()
    
    // Hora del día (0-24)
    const timeOfDay = 
      now.getHours() + 
      now.getMinutes() / 60 + 
      now.getSeconds() / 3600
    
    // Rotación sideral (rotación de las estrellas)
    // Las estrellas rotan ~4 minutos más rápido que el sol cada día
    const siderealRotation = (timeOfDay / 24) * 2 * Math.PI
    
    // Intensidad del cielo según altura solar
    let skyIntensity = 1.0
    if (solarAltitude > 0) {
      // Día: cielo brillante
      skyIntensity = Math.min(1, solarAltitude * 3)
    } else {
      // Noche: cielo oscuro
      skyIntensity = Math.max(0, 1 + solarAltitude * 5)
    }
    
    // Visibilidad de estrellas (inversa a intensidad del cielo)
    const starVisibility = Math.max(0, 1 - skyIntensity)
    
    // Vía láctea visible solo en noches oscuras
    const milkyWayVisible = starVisibility > 0.8
    
    return {
      siderealRotation,
      skyIntensity,
      starVisibility,
      milkyWayVisible
    }
  }

  /**
   * Actualizar rotación estelar continua
   */
  update(deltaTime: number, solarAltitude: number): SkyState {
    // Incrementar tiempo sideral (muy lento)
    this.siderealTime += deltaTime * 0.00005
    
    const state = this.calculateSkyState(solarAltitude)
    
    return {
      ...state,
      siderealRotation: state.siderealRotation + this.siderealTime
    }
  }
}

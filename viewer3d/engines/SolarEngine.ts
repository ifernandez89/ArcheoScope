/**
 * SolarEngine - Motor solar continuo basado en fecha y latitud real
 * Movimiento lento, transiciones suaves, sin cálculos pesados
 */

import * as THREE from 'three'

export interface SolarState {
  sunDirection: THREE.Vector3
  solarAltitude: number
  solarAzimuth: number
  declination: number
  hourAngle: number
  isDay: boolean
  dayProgress: number // 0-1 (amanecer a atardecer)
}

export class SolarEngine {
  private latitude: number = 0
  private longitude: number = 0
  private currentSunDirection: THREE.Vector3
  private targetSunDirection: THREE.Vector3
  private smoothingSpeed: number = 0.01 // Muy lento

  constructor(latitude: number = 0, longitude: number = 0) {
    this.latitude = latitude * (Math.PI / 180) // Convertir a radianes
    this.longitude = longitude
    this.currentSunDirection = new THREE.Vector3(0, 1, 0)
    this.targetSunDirection = new THREE.Vector3(0, 1, 0)
  }

  setLatitude(lat: number) {
    this.latitude = lat * (Math.PI / 180)
  }

  setLongitude(lon: number) {
    this.longitude = lon
  }

  setLocation(lat: number, lon: number) {
    this.latitude = lat * (Math.PI / 180)
    this.longitude = lon
  }

  /**
   * Calcular estado solar actual basado en fecha y hora real
   */
  calculateSolarState(): SolarState {
    const now = new Date()
    
    // Día del año (1-365)
    const startOfYear = new Date(now.getFullYear(), 0, 0)
    const diff = now.getTime() - startOfYear.getTime()
    const dayOfYear = Math.floor(diff / 86400000)
    
    // Hora del día en UTC (0-24 con decimales)
    const utcHour = 
      now.getUTCHours() + 
      now.getUTCMinutes() / 60 + 
      now.getUTCSeconds() / 3600
    
    // Ajustar por longitud para obtener hora solar local
    // Cada 15° de longitud = 1 hora de diferencia
    const timeOfDay = utcHour + (this.longitude / 15)

    console.log('⏰ Hora UTC:', utcHour.toFixed(2), 'Hora Solar Local:', timeOfDay.toFixed(2), 'Lat:', (this.latitude * 180 / Math.PI).toFixed(2), 'Lon:', this.longitude.toFixed(2))

    // Declinación solar (inclinación axial de la Tierra)
    const axialTilt = 23.44 * Math.PI / 180
    const declination = axialTilt * Math.sin((2 * Math.PI / 365) * (dayOfYear - 81))

    // Ángulo horario (posición del sol en el cielo)
    const hourAngle = ((timeOfDay - 12) / 12) * Math.PI

    // Altura solar (elevación sobre el horizonte)
    const solarAltitude = Math.asin(
      Math.sin(this.latitude) * Math.sin(declination) +
      Math.cos(this.latitude) * Math.cos(declination) * Math.cos(hourAngle)
    )

    // Azimut solar (dirección en el horizonte)
    const solarAzimuth = Math.atan2(
      -Math.sin(hourAngle),
      Math.tan(declination) * Math.cos(this.latitude) -
      Math.sin(this.latitude) * Math.cos(hourAngle)
    )

    // Dirección del sol como vector 3D
    const sunDirection = new THREE.Vector3(
      Math.cos(solarAltitude) * Math.sin(solarAzimuth),
      Math.sin(solarAltitude),
      Math.cos(solarAltitude) * Math.cos(solarAzimuth)
    )

    // Determinar si es de día
    const isDay = solarAltitude > -0.1 // Incluir crepúsculo

    // Progreso del día (0 = amanecer, 0.5 = mediodía, 1 = atardecer)
    const dayProgress = Math.max(0, Math.min(1, (timeOfDay - 6) / 12))

    return {
      sunDirection,
      solarAltitude,
      solarAzimuth,
      declination,
      hourAngle,
      isDay,
      dayProgress
    }
  }

  /**
   * Actualizar posición del sol con interpolación suave
   */
  update(deltaTime: number): SolarState {
    const state = this.calculateSolarState()
    
    // Actualizar target
    this.targetSunDirection.copy(state.sunDirection)
    
    // Interpolación suave (lerp)
    this.currentSunDirection.lerp(this.targetSunDirection, this.smoothingSpeed)
    
    return {
      ...state,
      sunDirection: this.currentSunDirection.clone()
    }
  }

  /**
   * Obtener dirección actual del sol (suavizada)
   */
  getCurrentDirection(): THREE.Vector3 {
    return this.currentSunDirection.clone()
  }
}

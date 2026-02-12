/**
 * AstroEngine - Motor astronómico
 * Responsable de: Cálculo solar, Alineamientos, Simulación histórica
 */

import * as THREE from 'three'

export interface SolarPosition {
  altitude: number  // Altura solar en grados
  azimuth: number   // Azimut en grados
  intensity: number // Intensidad de luz (0-1)
  color: string     // Color de la luz
}

export class AstroEngine {
  private static instance: AstroEngine
  
  private constructor() {}
  
  static getInstance(): AstroEngine {
    if (!AstroEngine.instance) {
      AstroEngine.instance = new AstroEngine()
    }
    return AstroEngine.instance
  }
  
  /**
   * Calcular posición solar para ubicación y fecha
   */
  calculateSolarPosition(
    lat: number,
    lon: number,
    date: Date = new Date()
  ): SolarPosition {
    // Día del año
    const startOfYear = new Date(date.getFullYear(), 0, 0)
    const diff = date.getTime() - startOfYear.getTime()
    const dayOfYear = Math.floor(diff / 86400000)
    
    // Hora decimal
    const hour = date.getHours() + date.getMinutes() / 60 + date.getSeconds() / 3600
    
    // Declinación solar (simplificado)
    const declination = 23.45 * Math.sin((360 / 365) * (dayOfYear - 81) * Math.PI / 180)
    
    // Ángulo horario
    const hourAngle = 15 * (hour - 12)
    
    // Altura solar
    const altitude = Math.asin(
      Math.sin(lat * Math.PI / 180) * Math.sin(declination * Math.PI / 180) +
      Math.cos(lat * Math.PI / 180) * Math.cos(declination * Math.PI / 180) * 
      Math.cos(hourAngle * Math.PI / 180)
    ) * 180 / Math.PI
    
    // Azimut solar (simplificado)
    const azimuth = hourAngle
    
    // Intensidad basada en altura
    const intensity = Math.max(0.2, Math.min(1.5, Math.sin(altitude * Math.PI / 180) * 1.5))
    
    // Color basado en altura
    let color = '#ffffff'
    if (altitude < 0) {
      color = '#1a1a2e' // Noche
    } else if (altitude < 15) {
      color = '#ff9966' // Amanecer/atardecer
    } else {
      color = '#ffffff' // Día
    }
    
    return { altitude, azimuth, intensity, color }
  }
  
  /**
   * Convertir posición solar a Vector3 para luz direccional
   */
  solarPositionToVector3(position: SolarPosition, distance: number = 15): THREE.Vector3 {
    const { altitude, azimuth } = position
    
    const x = distance * Math.cos(altitude * Math.PI / 180) * Math.sin(azimuth * Math.PI / 180)
    const y = distance * Math.sin(altitude * Math.PI / 180)
    const z = distance * Math.cos(altitude * Math.PI / 180) * Math.cos(azimuth * Math.PI / 180)
    
    return new THREE.Vector3(x, Math.max(y, 2), z)
  }
  
  /**
   * Calcular solsticio de verano para latitud
   */
  calculateSummerSolstice(year: number): Date {
    // Aproximación: 21 de junio
    return new Date(year, 5, 21, 12, 0, 0)
  }
  
  /**
   * Calcular solsticio de invierno para latitud
   */
  calculateWinterSolstice(year: number): Date {
    // Aproximación: 21 de diciembre
    return new Date(year, 11, 21, 12, 0, 0)
  }
  
  /**
   * Calcular equinoccio de primavera
   */
  calculateSpringEquinox(year: number): Date {
    // Aproximación: 20 de marzo
    return new Date(year, 2, 20, 12, 0, 0)
  }
  
  /**
   * Calcular equinoccio de otoño
   */
  calculateAutumnEquinox(year: number): Date {
    // Aproximación: 22 de septiembre
    return new Date(year, 8, 22, 12, 0, 0)
  }
  
  /**
   * Verificar si hay alineamiento solar en fecha
   */
  checkSolarAlignment(
    lat: number,
    lon: number,
    targetAzimuth: number,
    date: Date,
    tolerance: number = 5
  ): boolean {
    const position = this.calculateSolarPosition(lat, lon, date)
    const diff = Math.abs(position.azimuth - targetAzimuth)
    
    return diff <= tolerance
  }
  
  /**
   * Simular día completo (24 horas)
   */
  simulateFullDay(lat: number, lon: number, date: Date): SolarPosition[] {
    const positions: SolarPosition[] = []
    
    for (let hour = 0; hour < 24; hour++) {
      const testDate = new Date(date)
      testDate.setHours(hour, 0, 0, 0)
      
      positions.push(this.calculateSolarPosition(lat, lon, testDate))
    }
    
    return positions
  }
  
  /**
   * Obtener fase lunar (simplificado)
   */
  getMoonPhase(date: Date): number {
    let year = date.getFullYear()
    let month = date.getMonth() + 1
    const day = date.getDate()
    
    let c = 0
    let e = 0
    let jd = 0
    let b = 0
    
    if (month < 3) {
      year = year - 1
      month = month + 12
    }
    
    ++month
    c = 365.25 * year
    e = 30.6 * month
    jd = c + e + day - 694039.09
    jd /= 29.5305882
    b = Math.floor(jd)
    jd -= b
    b = Math.round(jd * 8)
    
    if (b >= 8) b = 0
    
    return b
  }
}

export default AstroEngine.getInstance()

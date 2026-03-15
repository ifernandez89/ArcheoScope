/**
 * SolarEngine - Motor solar continuo basado en fecha y latitud real
 * Movimiento lento, transiciones suaves, sin cálculos pesados
 */

import * as THREE from 'three'
import { calculateAllPlanets, type PlanetPosition } from '@/utils/planetary-orbits'
import { calculateLunarPhase, detectEclipse, type LunarState, type EclipseEvent } from '@/utils/lunar-system'

export interface SolarState {
  sunDirection: THREE.Vector3
  solarAltitude: number
  solarAzimuth: number
  declination: number
  hourAngle: number
  isDay: boolean
  dayProgress: number // 0-1 (amanecer a atardecer)
  season: 'spring' | 'summer' | 'autumn' | 'winter'
  dayOfYear: number
  precessionAngle: number // Ángulo de precesión axial
  // Nuevas propiedades FASE 2
  planets: PlanetPosition[]
  lunarState: LunarState
  eclipse: EclipseEvent
  timeInDays: number // Tiempo total en días para cálculos orbitales
  simulatedTime: Date // Tiempo simulado actual
}

export class SolarEngine {
  private latitude: number = 0
  private longitude: number = 0
  private currentSunDirection: THREE.Vector3
  private targetSunDirection: THREE.Vector3
  private smoothingSpeed: number = 0.01 // Muy lento
  
  // Sistema de tiempo acelerado
  private simulatedTime: Date
  private timeScale: number = 60 // 1 segundo real = 1 minuto simulado (1 minuto real = 1 hora simulada)
  private startTime: Date // Tiempo de referencia para cálculos orbitales
  
  // Constantes astronómicas
  private readonly AXIAL_TILT = 23.44 * Math.PI / 180 // Oblicuidad de la Tierra
  private readonly PRECESSION_CYCLE = 25772 // Ciclo de precesión en años
  private readonly REFERENCE_YEAR = 2000 // Año de referencia (J2000.0)

  constructor(latitude: number = 0, longitude: number = 0) {
    this.latitude = latitude * (Math.PI / 180) // Convertir a radianes
    this.longitude = longitude
    this.currentSunDirection = new THREE.Vector3(0, 1, 0)
    this.targetSunDirection = new THREE.Vector3(0, 1, 0)
    this.simulatedTime = new Date() // Iniciar con hora actual
    this.startTime = new Date(this.simulatedTime) // Referencia para órbitas
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
   * Calcular precesión axial para un año dado
   * La Tierra completa un ciclo de precesión cada 25,772 años
   * Esto causa que las constelaciones "se muevan" lentamente
   */
  private calculatePrecession(year: number): number {
    const yearsSinceReference = year - this.REFERENCE_YEAR
    return (2 * Math.PI / this.PRECESSION_CYCLE) * yearsSinceReference
  }
  
  /**
   * Determinar estación del año basada en día del año
   * Hemisferio Norte: Primavera (80), Verano (172), Otoño (266), Invierno (355)
   */
  private calculateSeason(dayOfYear: number, latitude: number): 'spring' | 'summer' | 'autumn' | 'winter' {
    // Invertir estaciones para hemisferio sur
    const isNorthern = latitude >= 0
    
    let season: 'spring' | 'summer' | 'autumn' | 'winter'
    if (dayOfYear < 80 || dayOfYear > 355) {
      season = 'winter'
    } else if (dayOfYear < 172) {
      season = 'spring'
    } else if (dayOfYear < 266) {
      season = 'summer'
    } else {
      season = 'autumn'
    }
    
    // Invertir para hemisferio sur
    if (!isNorthern) {
      const seasonMap = {
        'spring': 'autumn' as const,
        'summer': 'winter' as const,
        'autumn': 'spring' as const,
        'winter': 'summer' as const
      }
      season = seasonMap[season]
    }
    
    return season
  }

  /**
   * Calcular estado solar actual basado en fecha y hora simulada (acelerada)
   * Incluye precesión axial, estaciones, planetas, luna y eclipses
   */
  calculateSolarState(): SolarState {
    const now = this.simulatedTime
    
    // Tiempo total en días desde el inicio
    const timeInDays = (now.getTime() - this.startTime.getTime()) / (1000 * 60 * 60 * 24)
    
    // Día del año (1-365)
    const startOfYear = new Date(now.getFullYear(), 0, 0)
    const diff = now.getTime() - startOfYear.getTime()
    const dayOfYear = Math.floor(diff / 86400000)
    
    // Calcular precesión axial
    const precessionAngle = this.calculatePrecession(now.getFullYear())
    
    // Calcular estación
    const season = this.calculateSeason(dayOfYear, this.latitude * 180 / Math.PI)
    
    // Hora del día en UTC (0-24 con decimales)
    const utcHour = 
      now.getUTCHours() + 
      now.getUTCMinutes() / 60 + 
      now.getUTCSeconds() / 3600
    
    // Ajustar por longitud para obtener hora solar local
    // Cada 15° de longitud = 1 hora de diferencia
    const timeOfDay = utcHour + (this.longitude / 15)

    // Declinación solar (inclinación axial de la Tierra)
    // Aplicar precesión para cálculos históricos precisos
    const declination = this.AXIAL_TILT * Math.sin((2 * Math.PI / 365) * (dayOfYear - 81) + precessionAngle)

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

    // NUEVOS CÁLCULOS FASE 2
    // Calcular posiciones planetarias
    const planets = calculateAllPlanets(timeInDays, 15) // escala para visualización
    
    // Calcular estado lunar
    const lunarState = calculateLunarPhase(timeInDays)
    
    // Detectar eclipses
    const eclipse = detectEclipse(lunarState, sunDirection, { 
      lat: this.latitude * 180 / Math.PI, 
      lon: this.longitude 
    })

    return {
      sunDirection,
      solarAltitude,
      solarAzimuth,
      declination,
      hourAngle,
      isDay,
      dayProgress,
      season,
      dayOfYear,
      precessionAngle,
      planets,
      lunarState,
      eclipse,
      timeInDays,
      simulatedTime: new Date(this.simulatedTime) // Clonar para evitar mutaciones
    }
  }

  /**
   * Actualizar posición del sol con interpolación suave
   */
  update(deltaTime: number): SolarState {
    // Avanzar tiempo simulado (1 segundo real = 60 segundos simulados = 1 minuto)
    // Esto significa: 1 minuto real = 1 hora simulada
    const simulatedSeconds = deltaTime * this.timeScale
    this.simulatedTime = new Date(this.simulatedTime.getTime() + simulatedSeconds * 1000)
    
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

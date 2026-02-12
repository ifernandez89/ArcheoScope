// Solar Calculator - Cálculo de posición solar
// Basado en algoritmos astronómicos simplificados

import * as THREE from 'three'
import type { GeographicCoordinates } from '@/geo/coordinate-system'

export interface SolarPosition {
  azimuth: number    // Ángulo horizontal (0-360°, 0=Norte)
  altitude: number   // Ángulo vertical (-90 a 90°)
  distance: number   // Distancia al sol (UA)
  declination: number // Declinación solar
  hourAngle: number  // Ángulo horario
}

export interface CelestialTime {
  julianDay: number
  localSiderealTime: number
  greenwichSiderealTime: number
}

export class SolarCalculator {
  // Calcular posición del sol
  static calculateSunPosition(
    date: Date,
    location: GeographicCoordinates
  ): SolarPosition {
    // Calcular día juliano
    const jd = this.dateToJulianDay(date)
    
    // Calcular siglos julianos desde J2000.0
    const T = (jd - 2451545.0) / 36525.0
    
    // Longitud media del sol
    const L0 = (280.46646 + 36000.76983 * T + 0.0003032 * T * T) % 360
    
    // Anomalía media del sol
    const M = (357.52911 + 35999.05029 * T - 0.0001537 * T * T) % 360
    const MRad = THREE.MathUtils.degToRad(M)
    
    // Ecuación del centro
    const C = (1.914602 - 0.004817 * T - 0.000014 * T * T) * Math.sin(MRad) +
              (0.019993 - 0.000101 * T) * Math.sin(2 * MRad) +
              0.000289 * Math.sin(3 * MRad)
    
    // Longitud verdadera del sol
    const sunLon = (L0 + C) % 360
    
    // Oblicuidad de la eclíptica
    const epsilon = 23.439291 - 0.0130042 * T
    const epsilonRad = THREE.MathUtils.degToRad(epsilon)
    
    // Declinación solar
    const sunLonRad = THREE.MathUtils.degToRad(sunLon)
    const declination = THREE.MathUtils.radToDeg(
      Math.asin(Math.sin(epsilonRad) * Math.sin(sunLonRad))
    )
    
    // Ascensión recta
    const RA = THREE.MathUtils.radToDeg(
      Math.atan2(Math.cos(epsilonRad) * Math.sin(sunLonRad), Math.cos(sunLonRad))
    )
    
    // Tiempo sidéreo de Greenwich
    const GST = this.calculateGreenwichSiderealTime(jd)
    
    // Tiempo sidéreo local
    const LST = (GST + location.longitude) % 360
    
    // Ángulo horario
    const hourAngle = (LST - RA) % 360
    
    // Convertir a coordenadas horizontales
    const latRad = THREE.MathUtils.degToRad(location.latitude)
    const decRad = THREE.MathUtils.degToRad(declination)
    const haRad = THREE.MathUtils.degToRad(hourAngle)
    
    // Altitud (elevación)
    const altitude = THREE.MathUtils.radToDeg(
      Math.asin(
        Math.sin(latRad) * Math.sin(decRad) +
        Math.cos(latRad) * Math.cos(decRad) * Math.cos(haRad)
      )
    )
    
    // Azimut
    const azimuth = THREE.MathUtils.radToDeg(
      Math.atan2(
        Math.sin(haRad),
        Math.cos(haRad) * Math.sin(latRad) - Math.tan(decRad) * Math.cos(latRad)
      )
    ) + 180 // Ajustar para que 0° sea Norte
    
    return {
      azimuth: (azimuth + 360) % 360,
      altitude,
      distance: 1.0, // Simplificado (1 UA)
      declination,
      hourAngle
    }
  }

  // Convertir fecha a día juliano
  static dateToJulianDay(date: Date): number {
    const year = date.getUTCFullYear()
    const month = date.getUTCMonth() + 1
    const day = date.getUTCDate()
    const hour = date.getUTCHours()
    const minute = date.getUTCMinutes()
    const second = date.getUTCSeconds()
    
    let y = year
    let m = month
    
    if (month <= 2) {
      y -= 1
      m += 12
    }
    
    const A = Math.floor(y / 100)
    const B = 2 - A + Math.floor(A / 4)
    
    const JD = Math.floor(365.25 * (y + 4716)) +
               Math.floor(30.6001 * (m + 1)) +
               day + B - 1524.5 +
               (hour + minute / 60 + second / 3600) / 24
    
    return JD
  }

  // Calcular tiempo sidéreo de Greenwich
  static calculateGreenwichSiderealTime(jd: number): number {
    const T = (jd - 2451545.0) / 36525.0
    
    let GST = 280.46061837 +
              360.98564736629 * (jd - 2451545.0) +
              0.000387933 * T * T -
              T * T * T / 38710000.0
    
    return (GST % 360 + 360) % 360
  }

  // Calcular amanecer y atardecer
  static calculateSunriseSunset(
    date: Date,
    location: GeographicCoordinates
  ): { sunrise: Date; sunset: Date; solarNoon: Date } {
    const jd = this.dateToJulianDay(date)
    const T = (jd - 2451545.0) / 36525.0
    
    // Simplificado: usar -0.833° para horizonte
    const zenith = 90.833
    
    // Calcular declinación para el día
    const M = (357.52911 + 35999.05029 * T) % 360
    const L = (280.46646 + 36000.76983 * T) % 360
    const C = 1.914602 * Math.sin(THREE.MathUtils.degToRad(M))
    const lambda = L + C
    const epsilon = 23.439291 - 0.0130042 * T
    
    const decRad = Math.asin(
      Math.sin(THREE.MathUtils.degToRad(epsilon)) *
      Math.sin(THREE.MathUtils.degToRad(lambda))
    )
    const declination = THREE.MathUtils.radToDeg(decRad)
    
    // Ángulo horario
    const latRad = THREE.MathUtils.degToRad(location.latitude)
    const cosH = (
      Math.cos(THREE.MathUtils.degToRad(zenith)) -
      Math.sin(latRad) * Math.sin(decRad)
    ) / (Math.cos(latRad) * Math.cos(decRad))
    
    if (cosH > 1 || cosH < -1) {
      // Sol no sale o no se pone (regiones polares)
      return {
        sunrise: new Date(date),
        sunset: new Date(date),
        solarNoon: new Date(date)
      }
    }
    
    const H = THREE.MathUtils.radToDeg(Math.acos(cosH))
    
    // Tiempos en horas
    const solarNoonHour = 12 - location.longitude / 15
    const sunriseHour = solarNoonHour - H / 15
    const sunsetHour = solarNoonHour + H / 15
    
    // Crear fechas
    const sunrise = new Date(date)
    sunrise.setUTCHours(Math.floor(sunriseHour), (sunriseHour % 1) * 60, 0, 0)
    
    const sunset = new Date(date)
    sunset.setUTCHours(Math.floor(sunsetHour), (sunsetHour % 1) * 60, 0, 0)
    
    const solarNoon = new Date(date)
    solarNoon.setUTCHours(Math.floor(solarNoonHour), (solarNoonHour % 1) * 60, 0, 0)
    
    return { sunrise, sunset, solarNoon }
  }

  // Verificar si es de día
  static isDaytime(date: Date, location: GeographicCoordinates): boolean {
    const position = this.calculateSunPosition(date, location)
    return position.altitude > -0.833 // Horizonte con refracción
  }

  // Calcular duración del día
  static calculateDayLength(date: Date, location: GeographicCoordinates): number {
    const { sunrise, sunset } = this.calculateSunriseSunset(date, location)
    return (sunset.getTime() - sunrise.getTime()) / (1000 * 60 * 60) // horas
  }

  // Convertir posición solar a Vector3 (para iluminación)
  static sunPositionToVector3(position: SolarPosition, distance: number = 100): THREE.Vector3 {
    const azimuthRad = THREE.MathUtils.degToRad(position.azimuth)
    const altitudeRad = THREE.MathUtils.degToRad(position.altitude)
    
    const x = distance * Math.cos(altitudeRad) * Math.sin(azimuthRad)
    const y = distance * Math.sin(altitudeRad)
    const z = distance * Math.cos(altitudeRad) * Math.cos(azimuthRad)
    
    return new THREE.Vector3(x, y, z)
  }
}

// Celestial Simulator - Simulador celestial
export class CelestialSimulator {
  private currentDate: Date = new Date()
  private location: GeographicCoordinates = { latitude: 0, longitude: 0, altitude: 0 }
  private timeSpeed: number = 1 // 1 = tiempo real
  private isRunning: boolean = false
  private animationFrameId: number | null = null
  private lastUpdateTime: number = Date.now()
  private onUpdate?: (position: SolarPosition) => void

  // Establecer ubicación
  setLocation(location: GeographicCoordinates): void {
    this.location = location
  }

  // Establecer fecha
  setDate(date: Date): void {
    this.currentDate = new Date(date)
  }

  // Establecer velocidad de tiempo
  setTimeSpeed(speed: number): void {
    this.timeSpeed = speed
  }

  // Iniciar simulación
  start(): void {
    if (this.isRunning) return

    this.isRunning = true
    this.lastUpdateTime = Date.now()
    this.update()
    console.log('☀️ Simulación celestial iniciada')
  }

  // Detener simulación
  stop(): void {
    this.isRunning = false
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId)
      this.animationFrameId = null
    }
    console.log('☀️ Simulación celestial detenida')
  }

  // Loop de actualización
  private update = (): void => {
    if (!this.isRunning) return

    const now = Date.now()
    const deltaTime = (now - this.lastUpdateTime) * this.timeSpeed
    this.lastUpdateTime = now

    // Avanzar tiempo
    this.currentDate = new Date(this.currentDate.getTime() + deltaTime)

    // Calcular posición solar
    const position = SolarCalculator.calculateSunPosition(this.currentDate, this.location)

    // Callback
    if (this.onUpdate) {
      this.onUpdate(position)
    }

    // Continuar loop
    this.animationFrameId = requestAnimationFrame(this.update)
  }

  // Registrar callback de actualización
  setOnUpdate(callback: (position: SolarPosition) => void): void {
    this.onUpdate = callback
  }

  // Obtener fecha actual
  getCurrentDate(): Date {
    return new Date(this.currentDate)
  }

  // Obtener posición solar actual
  getCurrentSunPosition(): SolarPosition {
    return SolarCalculator.calculateSunPosition(this.currentDate, this.location)
  }

  // Verificar si está corriendo
  isSimulationRunning(): boolean {
    return this.isRunning
  }

  // Saltar a fecha específica
  jumpToDate(date: Date): void {
    this.currentDate = new Date(date)
    
    if (this.isRunning) {
      const position = SolarCalculator.calculateSunPosition(this.currentDate, this.location)
      if (this.onUpdate) {
        this.onUpdate(position)
      }
    }
  }

  // Saltar a hora del día
  jumpToTimeOfDay(hour: number): void {
    const newDate = new Date(this.currentDate)
    newDate.setHours(hour, 0, 0, 0)
    this.jumpToDate(newDate)
  }
}

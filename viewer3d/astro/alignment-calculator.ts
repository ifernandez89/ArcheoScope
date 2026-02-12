// Alignment Calculator - Cálculo de alineamientos astronómicos
// Calcula alineamientos de estructuras con eventos celestiales

import * as THREE from 'three'
import type { GeographicCoordinates } from '@/geo/coordinate-system'
import { SolarCalculator, type SolarPosition } from './solar-calculator'

export interface AlignmentConfig {
  structure: string
  location: GeographicCoordinates
  date: Date
  azimuth: number // Orientación de la estructura (0-360°)
  tolerance: number // Tolerancia en grados
}

export interface AlignmentResult {
  isAligned: boolean
  angleDifference: number
  celestialBody: 'sun' | 'moon' | 'star'
  event: string // 'sunrise', 'sunset', 'solstice', etc.
  accuracy: number // 0-100%
  description: string
}

export interface HistoricalAlignment {
  name: string
  structure: string
  location: GeographicCoordinates
  azimuth: number
  event: 'summer-solstice' | 'winter-solstice' | 'equinox' | 'custom'
  date?: Date
  description: string
}

export class AlignmentCalculator {
  // Calcular alineamiento solar
  static calculateSolarAlignment(config: AlignmentConfig): AlignmentResult {
    const sunPos = SolarCalculator.calculateSunPosition(config.date, config.location)
    
    // Calcular diferencia angular
    let angleDiff = Math.abs(sunPos.azimuth - config.azimuth)
    if (angleDiff > 180) {
      angleDiff = 360 - angleDiff
    }
    
    // Verificar alineamiento
    const isAligned = angleDiff <= config.tolerance
    const accuracy = Math.max(0, 100 - (angleDiff / config.tolerance) * 100)
    
    // Determinar evento
    let event = 'custom'
    if (Math.abs(sunPos.altitude) < 1) {
      event = sunPos.azimuth < 180 ? 'sunrise' : 'sunset'
    }
    
    return {
      isAligned,
      angleDifference: angleDiff,
      celestialBody: 'sun',
      event,
      accuracy,
      description: `${config.structure} ${isAligned ? 'está alineado' : 'no está alineado'} con el sol (${event})`
    }
  }

  // Calcular alineamiento en solsticio de verano
  static calculateSummerSolsticeAlignment(
    location: GeographicCoordinates,
    structureAzimuth: number,
    year: number = new Date().getFullYear()
  ): AlignmentResult {
    // Solsticio de verano (aproximadamente 21 de junio)
    const solsticeDate = new Date(year, 5, 21, 6, 0, 0)
    
    return this.calculateSolarAlignment({
      structure: 'Structure',
      location,
      date: solsticeDate,
      azimuth: structureAzimuth,
      tolerance: 2.0
    })
  }

  // Calcular alineamiento en solsticio de invierno
  static calculateWinterSolsticeAlignment(
    location: GeographicCoordinates,
    structureAzimuth: number,
    year: number = new Date().getFullYear()
  ): AlignmentResult {
    // Solsticio de invierno (aproximadamente 21 de diciembre)
    const solsticeDate = new Date(year, 11, 21, 6, 0, 0)
    
    return this.calculateSolarAlignment({
      structure: 'Structure',
      location,
      date: solsticeDate,
      azimuth: structureAzimuth,
      tolerance: 2.0
    })
  }

  // Calcular alineamiento en equinoccio
  static calculateEquinoxAlignment(
    location: GeographicCoordinates,
    structureAzimuth: number,
    year: number = new Date().getFullYear(),
    spring: boolean = true
  ): AlignmentResult {
    // Equinoccio de primavera (20 marzo) o otoño (22 septiembre)
    const equinoxDate = spring 
      ? new Date(year, 2, 20, 6, 0, 0)
      : new Date(year, 8, 22, 6, 0, 0)
    
    return this.calculateSolarAlignment({
      structure: 'Structure',
      location,
      date: equinoxDate,
      azimuth: structureAzimuth,
      tolerance: 2.0
    })
  }

  // Encontrar fecha de alineamiento óptimo
  static findOptimalAlignmentDate(
    location: GeographicCoordinates,
    structureAzimuth: number,
    startDate: Date,
    endDate: Date,
    stepDays: number = 1
  ): { date: Date; result: AlignmentResult } | null {
    let bestDate: Date | null = null
    let bestResult: AlignmentResult | null = null
    let bestAccuracy = 0

    const current = new Date(startDate)
    
    while (current <= endDate) {
      const result = this.calculateSolarAlignment({
        structure: 'Structure',
        location,
        date: new Date(current),
        azimuth: structureAzimuth,
        tolerance: 5.0
      })
      
      if (result.accuracy > bestAccuracy) {
        bestAccuracy = result.accuracy
        bestDate = new Date(current)
        bestResult = result
      }
      
      current.setDate(current.getDate() + stepDays)
    }
    
    if (bestDate && bestResult) {
      return { date: bestDate, result: bestResult }
    }
    
    return null
  }

  // Calcular azimut de amanecer/atardecer para una fecha
  static calculateSunriseAzimuth(date: Date, location: GeographicCoordinates): number {
    const { sunrise } = SolarCalculator.calculateSunriseSunset(date, location)
    const sunPos = SolarCalculator.calculateSunPosition(sunrise, location)
    return sunPos.azimuth
  }

  static calculateSunsetAzimuth(date: Date, location: GeographicCoordinates): number {
    const { sunset } = SolarCalculator.calculateSunriseSunset(date, location)
    const sunPos = SolarCalculator.calculateSunPosition(sunset, location)
    return sunPos.azimuth
  }

  // Verificar si una estructura apunta al norte verdadero
  static checkCardinalAlignment(structureAzimuth: number, tolerance: number = 2): {
    cardinal: 'north' | 'south' | 'east' | 'west' | 'none'
    accuracy: number
  } {
    const cardinals = [
      { name: 'north' as const, azimuth: 0 },
      { name: 'east' as const, azimuth: 90 },
      { name: 'south' as const, azimuth: 180 },
      { name: 'west' as const, azimuth: 270 }
    ]
    
    for (const cardinal of cardinals) {
      let diff = Math.abs(structureAzimuth - cardinal.azimuth)
      if (diff > 180) diff = 360 - diff
      
      if (diff <= tolerance) {
        const accuracy = Math.max(0, 100 - (diff / tolerance) * 100)
        return { cardinal: cardinal.name, accuracy }
      }
    }
    
    return { cardinal: 'none', accuracy: 0 }
  }
}

// Star Positions - Posiciones estelares simplificadas
export interface StarData {
  name: string
  rightAscension: number // Horas (0-24)
  declination: number    // Grados (-90 a 90)
  magnitude: number      // Brillo aparente
  constellation: string
}

export class StarPositions {
  // Estrellas principales (simplificado)
  private static readonly MAJOR_STARS: StarData[] = [
    { name: 'Sirius', rightAscension: 6.75, declination: -16.72, magnitude: -1.46, constellation: 'Canis Major' },
    { name: 'Canopus', rightAscension: 6.40, declination: -52.70, magnitude: -0.72, constellation: 'Carina' },
    { name: 'Arcturus', rightAscension: 14.26, declination: 19.18, magnitude: -0.05, constellation: 'Boötes' },
    { name: 'Vega', rightAscension: 18.62, declination: 38.78, magnitude: 0.03, constellation: 'Lyra' },
    { name: 'Capella', rightAscension: 5.28, declination: 45.99, magnitude: 0.08, constellation: 'Auriga' },
    { name: 'Rigel', rightAscension: 5.24, declination: -8.20, magnitude: 0.12, constellation: 'Orion' },
    { name: 'Betelgeuse', rightAscension: 5.92, declination: 7.41, magnitude: 0.50, constellation: 'Orion' },
    { name: 'Altair', rightAscension: 19.85, declination: 8.87, magnitude: 0.77, constellation: 'Aquila' },
    { name: 'Aldebaran', rightAscension: 4.60, declination: 16.51, magnitude: 0.85, constellation: 'Taurus' },
    { name: 'Antares', rightAscension: 16.49, declination: -26.43, magnitude: 1.09, constellation: 'Scorpius' }
  ]

  // Obtener todas las estrellas
  static getAllStars(): StarData[] {
    return [...this.MAJOR_STARS]
  }

  // Obtener estrella por nombre
  static getStarByName(name: string): StarData | undefined {
    return this.MAJOR_STARS.find(
      star => star.name.toLowerCase() === name.toLowerCase()
    )
  }

  // Calcular posición horizontal de una estrella
  static calculateStarPosition(
    star: StarData,
    date: Date,
    location: GeographicCoordinates
  ): { azimuth: number; altitude: number } {
    // Convertir RA a grados
    const RA = star.rightAscension * 15 // 1 hora = 15 grados
    
    // Calcular tiempo sidéreo local
    const jd = SolarCalculator.dateToJulianDay(date)
    const GST = SolarCalculator.calculateGreenwichSiderealTime(jd)
    const LST = (GST + location.longitude) % 360
    
    // Ángulo horario
    const hourAngle = (LST - RA) % 360
    
    // Convertir a coordenadas horizontales
    const latRad = THREE.MathUtils.degToRad(location.latitude)
    const decRad = THREE.MathUtils.degToRad(star.declination)
    const haRad = THREE.MathUtils.degToRad(hourAngle)
    
    // Altitud
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
    ) + 180
    
    return {
      azimuth: (azimuth + 360) % 360,
      altitude
    }
  }

  // Encontrar estrellas visibles
  static getVisibleStars(
    date: Date,
    location: GeographicCoordinates,
    minAltitude: number = 0
  ): Array<StarData & { azimuth: number; altitude: number }> {
    return this.MAJOR_STARS
      .map(star => {
        const pos = this.calculateStarPosition(star, date, location)
        return { ...star, ...pos }
      })
      .filter(star => star.altitude >= minAltitude)
      .sort((a, b) => a.magnitude - b.magnitude) // Ordenar por brillo
  }

  // Calcular alineamiento con estrella
  static calculateStarAlignment(
    star: StarData,
    date: Date,
    location: GeographicCoordinates,
    structureAzimuth: number,
    tolerance: number = 2
  ): AlignmentResult {
    const pos = this.calculateStarPosition(star, date, location)
    
    let angleDiff = Math.abs(pos.azimuth - structureAzimuth)
    if (angleDiff > 180) angleDiff = 360 - angleDiff
    
    const isAligned = angleDiff <= tolerance
    const accuracy = Math.max(0, 100 - (angleDiff / tolerance) * 100)
    
    return {
      isAligned,
      angleDifference: angleDiff,
      celestialBody: 'star',
      event: `alignment-${star.name}`,
      accuracy,
      description: `Estructura ${isAligned ? 'alineada' : 'no alineada'} con ${star.name}`
    }
  }
}

// Historical Alignments - Alineamientos históricos conocidos
export const KNOWN_ALIGNMENTS: HistoricalAlignment[] = [
  {
    name: 'Gran Pirámide de Giza',
    structure: 'Pirámide de Keops',
    location: { latitude: 29.9792, longitude: 31.1342, altitude: 60 },
    azimuth: 0, // Norte verdadero
    event: 'custom',
    description: 'Alineada con precisión al norte verdadero (error < 0.05°)'
  },
  {
    name: 'Stonehenge',
    structure: 'Círculo de piedras',
    location: { latitude: 51.1789, longitude: -1.8262, altitude: 100 },
    azimuth: 49.9, // Amanecer de solsticio de verano
    event: 'summer-solstice',
    description: 'Alineado con el amanecer del solsticio de verano'
  },
  {
    name: 'Templo de Karnak',
    structure: 'Eje principal',
    location: { latitude: 25.7188, longitude: 32.6573, altitude: 75 },
    azimuth: 116, // Amanecer de solsticio de invierno
    event: 'winter-solstice',
    description: 'Alineado con el amanecer del solsticio de invierno'
  },
  {
    name: 'Chichén Itzá',
    structure: 'El Castillo',
    location: { latitude: 20.6843, longitude: -88.5678, altitude: 25 },
    azimuth: 90, // Este (equinoccio)
    event: 'equinox',
    description: 'Fenómeno de la serpiente en equinoccios'
  },
  {
    name: 'Machu Picchu',
    structure: 'Intihuatana',
    location: { latitude: -13.1631, longitude: -72.5450, altitude: 2430 },
    azimuth: 0, // Norte
    event: 'custom',
    description: 'Reloj solar alineado con eventos astronómicos'
  }
]

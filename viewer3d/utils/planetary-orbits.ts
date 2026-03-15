/**
 * Planetary Orbits - Sistema de órbitas planetarias mejorado
 * Incluye inclinaciones orbitales, excentricidades y períodos reales
 */

import * as THREE from 'three'

export interface PlanetaryData {
  name: string
  period: number      // días
  radius: number      // AU (Unidades Astronómicas)
  inclination: number // grados
  eccentricity: number // 0-1
  color: string
  size: number        // radio visual
  initialAngle: number // ángulo inicial en radianes
}

export const PLANETS: Record<string, PlanetaryData> = {
  mercury: {
    name: 'Mercurio',
    period: 88,
    radius: 0.39,
    inclination: 7.0,
    eccentricity: 0.206,
    color: '#8c7853',
    size: 0.38,
    initialAngle: 85 * Math.PI / 180 // Posición aproximada marzo 2026
  },
  venus: {
    name: 'Venus',
    period: 225,
    radius: 0.72,
    inclination: 3.4,
    eccentricity: 0.007,
    color: '#ffc649',
    size: 0.95,
    initialAngle: 160 * Math.PI / 180 // Posición aproximada marzo 2026
  },
  earth: {
    name: 'Tierra',
    period: 365,
    radius: 1.0,
    inclination: 0.0,
    eccentricity: 0.017,
    color: '#6b93d6',
    size: 1.0,
    initialAngle: 354 * Math.PI / 180 // 15 marzo = día 74, ~74/365 * 360° = 73°, pero desde perihelio
  },
  mars: {
    name: 'Marte',
    period: 687,
    radius: 1.52,
    inclination: 1.85,
    eccentricity: 0.093,
    color: '#c1440e',
    size: 0.53,
    initialAngle: 45 * Math.PI / 180 // Posición aproximada marzo 2026
  },
  jupiter: {
    name: 'Júpiter',
    period: 11.86 * 365,
    radius: 5.2,
    inclination: 1.3,
    eccentricity: 0.049,
    color: '#c8a87a',
    size: 11.2,
    initialAngle: 30 * Math.PI / 180 // Júpiter se mueve lento
  },
  saturn: {
    name: 'Saturno',
    period: 29.46 * 365,
    radius: 9.58,
    inclination: 2.5,
    eccentricity: 0.057,
    color: '#e8d5a0',
    size: 9.4,
    initialAngle: 320 * Math.PI / 180 // Saturno muy lento
  },
  uranus: {
    name: 'Urano',
    period: 84.01 * 365,
    radius: 19.2,
    inclination: 0.8,
    eccentricity: 0.046,
    color: '#7de8e8',
    size: 4.0,
    initialAngle: 50 * Math.PI / 180 // Urano extremadamente lento
  },
  neptune: {
    name: 'Neptuno',
    period: 164.8 * 365,
    radius: 30.05,
    inclination: 1.8,
    eccentricity: 0.009,
    color: '#4b70dd',
    size: 3.9,
    initialAngle: 355 * Math.PI / 180 // Neptuno casi inmóvil
  },
  pluto: {
    name: 'Plutón',
    period: 248 * 365,
    radius: 39.5,
    inclination: 17.1, // Muy inclinado
    eccentricity: 0.248, // Muy elíptico
    color: '#8c7853',
    size: 0.18,
    initialAngle: 110 * Math.PI / 180 // Posición aproximada
  }
}

export interface PlanetPosition {
  position: THREE.Vector3
  angle: number
  planet: PlanetaryData
}
/**
 * Calcular posición de un planeta en su órbita
 */
export function calculatePlanetPosition(
  planet: PlanetaryData, 
  timeInDays: number,
  scale: number = 10
): PlanetPosition {
  // Ángulo orbital (0-2π) + posición inicial
  const angle = (2 * Math.PI * timeInDays) / planet.period + planet.initialAngle
  
  // Distancia con excentricidad (aproximación simple)
  const distance = planet.radius * (1 + planet.eccentricity * Math.cos(angle)) * scale
  
  // Posición en el plano orbital
  const x = distance * Math.cos(angle)
  const z = distance * Math.sin(angle)
  
  // Aplicar inclinación orbital
  const inclinationRad = planet.inclination * Math.PI / 180
  const y = z * Math.sin(inclinationRad)
  const zInclined = z * Math.cos(inclinationRad)
  
  return {
    position: new THREE.Vector3(x, y, zInclined),
    angle,
    planet
  }
}

/**
 * Calcular todas las posiciones planetarias
 */
export function calculateAllPlanets(timeInDays: number, scale: number = 10): PlanetPosition[] {
  return Object.values(PLANETS).map(planet => 
    calculatePlanetPosition(planet, timeInDays, scale)
  )
}

/**
 * Detectar conjunciones planetarias (planetas alineados)
 */
export function detectConjunctions(positions: PlanetPosition[]): Array<{
  planets: string[]
  angle: number
  separation: number
}> {
  const conjunctions = []
  
  for (let i = 0; i < positions.length; i++) {
    for (let j = i + 1; j < positions.length; j++) {
      const planet1 = positions[i]
      const planet2 = positions[j]
      
      // Calcular separación angular
      const separation = Math.abs(planet1.angle - planet2.angle)
      const normalizedSep = Math.min(separation, 2 * Math.PI - separation)
      
      // Conjunción si están a menos de 10 grados
      if (normalizedSep < (10 * Math.PI / 180)) {
        conjunctions.push({
          planets: [planet1.planet.name, planet2.planet.name],
          angle: (planet1.angle + planet2.angle) / 2,
          separation: normalizedSep * 180 / Math.PI
        })
      }
    }
  }
  
  return conjunctions
}
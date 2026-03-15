/**
 * Lunar System - Fases lunares y eclipses
 * Cálculos precisos basados en astronomía real
 */

import * as THREE from 'three'

export interface LunarState {
  phase: 'new' | 'waxing_crescent' | 'first_quarter' | 'waxing_gibbous' | 
         'full' | 'waning_gibbous' | 'last_quarter' | 'waning_crescent'
  illumination: number // 0-1
  position: THREE.Vector3
  age: number // días desde luna nueva
  distance: number // km
  angularSize: number // grados
}

export interface EclipseEvent {
  type: 'solar' | 'lunar'
  magnitude: number // 0-1 (parcial) o >1 (total)
  duration: number // minutos
  visibility: 'visible' | 'partial' | 'not_visible'
  phase: 'beginning' | 'maximum' | 'ending' | 'none'
}

const LUNAR_CYCLE = 29.53059 // días sinódicos
const LUNAR_DISTANCE = 384400 // km promedio
const LUNAR_ORBITAL_PERIOD = 27.32166 // días siderales

/**
 * Calcular fase lunar basada en días desde luna nueva
 */
export function calculateLunarPhase(daysSinceNewMoon: number): LunarState {
  const age = daysSinceNewMoon % LUNAR_CYCLE
  const phaseAngle = (age / LUNAR_CYCLE) * 2 * Math.PI
  
  // Determinar fase
  let phase: LunarState['phase']
  if (age < 1) phase = 'new'
  else if (age < 7.4) phase = 'waxing_crescent'
  else if (age < 8.4) phase = 'first_quarter'
  else if (age < 14.8) phase = 'waxing_gibbous'
  else if (age < 15.8) phase = 'full'
  else if (age < 22.1) phase = 'waning_gibbous'
  else if (age < 23.1) phase = 'last_quarter'
  else if (age < 29.5) phase = 'waning_crescent'
  else phase = 'new'
  
  // Calcular iluminación
  const illumination = (1 - Math.cos(phaseAngle)) / 2
  
  // Posición lunar (órbita simplificada)
  const lunarAngle = (age / LUNAR_ORBITAL_PERIOD) * 2 * Math.PI
  const distance = LUNAR_DISTANCE * (1 + 0.055 * Math.cos(lunarAngle)) // excentricidad
  
  // ESCALA CONSISTENTE: 1 AU = 200 unidades (igual que los planetas)
  // Luna: 384,400 km = 0.00257 AU
  const AU_TO_KM = 149597871
  const distanceInAU = distance / AU_TO_KM
  const SCALE = 200 // Misma escala que los planetas
  
  const position = new THREE.Vector3(
    distanceInAU * SCALE * Math.cos(lunarAngle),
    0,
    distanceInAU * SCALE * Math.sin(lunarAngle)
  )
  
  // Tamaño angular (varía con distancia)
  const angularSize = 0.5181 * (LUNAR_DISTANCE / distance) // grados
  
  return {
    phase,
    illumination,
    position,
    age,
    distance,
    angularSize
  }
}
/**
 * Detectar eclipses solares y lunares
 */
export function detectEclipse(
  lunarState: LunarState,
  solarPosition: THREE.Vector3,
  observerLocation: { lat: number, lon: number }
): EclipseEvent {
  const moonPos = lunarState.position
  const sunPos = solarPosition.clone().normalize()
  const moonDir = moonPos.clone().normalize()
  
  // Calcular alineación (producto punto)
  const alignment = Math.abs(sunPos.dot(moonDir))
  
  // Eclipse solar (luna nueva + alineación)
  if (lunarState.phase === 'new' && alignment > 0.999) {
    const magnitude = Math.min(1.2, (alignment - 0.999) * 1000)
    return {
      type: 'solar',
      magnitude,
      duration: magnitude > 1 ? 7.5 : 4.2, // minutos
      visibility: magnitude > 0.1 ? 'visible' : 'partial',
      phase: magnitude > 0.5 ? 'maximum' : 'beginning'
    }
  }
  
  // Eclipse lunar (luna llena + alineación)
  if (lunarState.phase === 'full' && alignment > 0.998) {
    const magnitude = Math.min(1.8, (alignment - 0.998) * 500)
    return {
      type: 'lunar',
      magnitude,
      duration: magnitude > 1 ? 103 : 60, // minutos
      visibility: 'visible', // siempre visible si es de noche
      phase: magnitude > 0.7 ? 'maximum' : 'beginning'
    }
  }
  
  return {
    type: 'solar',
    magnitude: 0,
    duration: 0,
    visibility: 'not_visible',
    phase: 'none'
  }
}

/**
 * Nombres de fases lunares en español
 */
export const LUNAR_PHASE_NAMES = {
  new: 'Luna Nueva',
  waxing_crescent: 'Luna Creciente',
  first_quarter: 'Cuarto Creciente',
  waxing_gibbous: 'Gibosa Creciente',
  full: 'Luna Llena',
  waning_gibbous: 'Gibosa Menguante',
  last_quarter: 'Cuarto Menguante',
  waning_crescent: 'Luna Menguante'
}

/**
 * Iconos de fases lunares
 */
export const LUNAR_PHASE_ICONS = {
  new: '🌑',
  waxing_crescent: '🌒',
  first_quarter: '🌓',
  waxing_gibbous: '🌔',
  full: '🌕',
  waning_gibbous: '🌖',
  last_quarter: '🌗',
  waning_crescent: '🌘'
}
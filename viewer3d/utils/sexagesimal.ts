/**
 * Utilidades para conversión sexagesimal (base 60)
 * Sistema heredado de la civilización babilónica
 * Usado en astronomía y navegación antigua
 */

export interface SexagesimalCoordinate {
  degrees: number
  minutes: number  // 0-59
  seconds: number  // 0-59
  direction?: 'N' | 'S' | 'E' | 'W'
}

/**
 * Convertir decimal a sexagesimal (grados, minutos, segundos)
 * Ejemplo: 19.7867° → 19° 47' 12"
 */
export function toSexagesimal(decimal: number): SexagesimalCoordinate {
  const degrees = Math.floor(Math.abs(decimal))
  const minutesDecimal = (Math.abs(decimal) - degrees) * 60
  const minutes = Math.floor(minutesDecimal)
  const seconds = Math.round((minutesDecimal - minutes) * 60)
  
  return { degrees, minutes, seconds }
}

/**
 * Convertir sexagesimal a decimal
 * Ejemplo: 19° 47' 12" → 19.7867°
 */
export function fromSexagesimal(coord: SexagesimalCoordinate): number {
  return coord.degrees + coord.minutes / 60 + coord.seconds / 3600
}

/**
 * Formatear coordenada geográfica en formato sexagesimal
 * Ejemplo: (29.9792, 31.1342) → "29° 58' 45" N, 31° 8' 3" E"
 */
export function formatLatLon(lat: number, lon: number): string {
  const latSex = toSexagesimal(lat)
  const lonSex = toSexagesimal(lon)
  
  const latDir = lat >= 0 ? 'N' : 'S'
  const lonDir = lon >= 0 ? 'E' : 'W'
  
  return `${latSex.degrees}° ${latSex.minutes}' ${latSex.seconds}" ${latDir}, ${lonSex.degrees}° ${lonSex.minutes}' ${lonSex.seconds}" ${lonDir}`
}

/**
 * Formatear ángulo astronómico (0-360°)
 * Ejemplo: 287.5° → "287° 30' 0""
 */
export function formatAngle(angle: number): string {
  const sex = toSexagesimal(angle)
  return `${sex.degrees}° ${sex.minutes}' ${sex.seconds}"`
}

/**
 * Convertir radianes a formato sexagesimal
 */
export function radiansToSexagesimal(radians: number): SexagesimalCoordinate {
  const degrees = radians * (180 / Math.PI)
  return toSexagesimal(degrees)
}

/**
 * Formatear hora en formato sexagesimal (24h)
 * Ejemplo: 14.5 → "14h 30m 0s"
 */
export function formatTime(hours: number): string {
  const h = Math.floor(hours)
  const minutesDecimal = (hours - h) * 60
  const m = Math.floor(minutesDecimal)
  const s = Math.round((minutesDecimal - m) * 60)
  
  return `${h.toString().padStart(2, '0')}h ${m.toString().padStart(2, '0')}m ${s.toString().padStart(2, '0')}s`
}

/**
 * Calcular diferencia angular en formato sexagesimal
 * Útil para alineaciones de templos
 */
export function angleDifference(angle1: number, angle2: number): SexagesimalCoordinate {
  let diff = Math.abs(angle1 - angle2)
  if (diff > 180) diff = 360 - diff
  return toSexagesimal(diff)
}

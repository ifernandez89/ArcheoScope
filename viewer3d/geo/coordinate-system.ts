// Coordinate System - Sistema de coordenadas geoespaciales
// Conversión entre coordenadas geográficas y 3D

import * as THREE from 'three'

export interface GeographicCoordinates {
  latitude: number  // -90 a 90
  longitude: number // -180 a 180
  altitude: number  // metros sobre nivel del mar
}

export interface CartesianCoordinates {
  x: number
  y: number
  z: number
}

export class CoordinateSystem {
  // Radio de la Tierra en metros
  private static readonly EARTH_RADIUS = 6371000

  // Convertir coordenadas geográficas a cartesianas (ECEF)
  static geographicToCartesian(coords: GeographicCoordinates): CartesianCoordinates {
    const { latitude, longitude, altitude } = coords
    
    // Convertir a radianes
    const latRad = THREE.MathUtils.degToRad(latitude)
    const lonRad = THREE.MathUtils.degToRad(longitude)
    
    // Radio desde el centro de la Tierra
    const radius = this.EARTH_RADIUS + altitude
    
    // Conversión a coordenadas cartesianas (ECEF)
    const x = radius * Math.cos(latRad) * Math.cos(lonRad)
    const y = radius * Math.cos(latRad) * Math.sin(lonRad)
    const z = radius * Math.sin(latRad)
    
    return { x, y, z }
  }

  // Convertir coordenadas cartesianas a geográficas
  static cartesianToGeographic(coords: CartesianCoordinates): GeographicCoordinates {
    const { x, y, z } = coords
    
    // Calcular radio
    const radius = Math.sqrt(x * x + y * y + z * z)
    
    // Calcular latitud y longitud
    const latitude = THREE.MathUtils.radToDeg(Math.asin(z / radius))
    const longitude = THREE.MathUtils.radToDeg(Math.atan2(y, x))
    const altitude = radius - this.EARTH_RADIUS
    
    return { latitude, longitude, altitude }
  }

  // Convertir a Vector3 de Three.js (escala reducida para visualización)
  static geographicToVector3(coords: GeographicCoordinates, scale: number = 1): THREE.Vector3 {
    const cartesian = this.geographicToCartesian(coords)
    return new THREE.Vector3(
      cartesian.x * scale,
      cartesian.z * scale, // Y es arriba en Three.js
      -cartesian.y * scale // Invertir para coincidir con convención
    )
  }

  // Calcular distancia entre dos puntos geográficos (Haversine)
  static calculateDistance(
    coord1: GeographicCoordinates,
    coord2: GeographicCoordinates
  ): number {
    const lat1 = THREE.MathUtils.degToRad(coord1.latitude)
    const lat2 = THREE.MathUtils.degToRad(coord2.latitude)
    const deltaLat = lat2 - lat1
    const deltaLon = THREE.MathUtils.degToRad(coord2.longitude - coord1.longitude)
    
    const a = Math.sin(deltaLat / 2) * Math.sin(deltaLat / 2) +
              Math.cos(lat1) * Math.cos(lat2) *
              Math.sin(deltaLon / 2) * Math.sin(deltaLon / 2)
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
    
    return this.EARTH_RADIUS * c
  }

  // Calcular bearing (dirección) entre dos puntos
  static calculateBearing(
    from: GeographicCoordinates,
    to: GeographicCoordinates
  ): number {
    const lat1 = THREE.MathUtils.degToRad(from.latitude)
    const lat2 = THREE.MathUtils.degToRad(to.latitude)
    const deltaLon = THREE.MathUtils.degToRad(to.longitude - from.longitude)
    
    const y = Math.sin(deltaLon) * Math.cos(lat2)
    const x = Math.cos(lat1) * Math.sin(lat2) -
              Math.sin(lat1) * Math.cos(lat2) * Math.cos(deltaLon)
    
    const bearing = Math.atan2(y, x)
    return (THREE.MathUtils.radToDeg(bearing) + 360) % 360
  }

  // Calcular punto intermedio entre dos coordenadas
  static interpolate(
    from: GeographicCoordinates,
    to: GeographicCoordinates,
    t: number // 0 a 1
  ): GeographicCoordinates {
    const lat1 = THREE.MathUtils.degToRad(from.latitude)
    const lon1 = THREE.MathUtils.degToRad(from.longitude)
    const lat2 = THREE.MathUtils.degToRad(to.latitude)
    const lon2 = THREE.MathUtils.degToRad(to.longitude)
    
    const d = this.calculateDistance(from, to) / this.EARTH_RADIUS
    const a = Math.sin((1 - t) * d) / Math.sin(d)
    const b = Math.sin(t * d) / Math.sin(d)
    
    const x = a * Math.cos(lat1) * Math.cos(lon1) + b * Math.cos(lat2) * Math.cos(lon2)
    const y = a * Math.cos(lat1) * Math.sin(lon1) + b * Math.cos(lat2) * Math.sin(lon2)
    const z = a * Math.sin(lat1) + b * Math.sin(lat2)
    
    const lat = Math.atan2(z, Math.sqrt(x * x + y * y))
    const lon = Math.atan2(y, x)
    
    return {
      latitude: THREE.MathUtils.radToDeg(lat),
      longitude: THREE.MathUtils.radToDeg(lon),
      altitude: from.altitude + (to.altitude - from.altitude) * t
    }
  }

  // Obtener radio de la Tierra
  static getEarthRadius(): number {
    return this.EARTH_RADIUS
  }
}

// Location Manager - Gestor de ubicaciones arqueológicas
export interface ArchaeologicalSite {
  id: string
  name: string
  description: string
  coordinates: GeographicCoordinates
  modelPath?: string
  culture: string
  period: string
  discovered?: number
}

export class LocationManager {
  private sites: Map<string, ArchaeologicalSite> = new Map()

  // Registrar sitio
  registerSite(site: ArchaeologicalSite): void {
    this.sites.set(site.id, site)
    console.log(`📍 Sitio registrado: ${site.name}`)
  }

  // Registrar múltiples sitios
  registerSites(sites: ArchaeologicalSite[]): void {
    sites.forEach(site => this.registerSite(site))
  }

  // Obtener sitio por ID
  getSite(id: string): ArchaeologicalSite | undefined {
    return this.sites.get(id)
  }

  // Obtener todos los sitios
  getAllSites(): ArchaeologicalSite[] {
    return Array.from(this.sites.values())
  }

  // Buscar sitios cercanos
  findNearby(
    coords: GeographicCoordinates,
    radiusKm: number
  ): ArchaeologicalSite[] {
    const radiusMeters = radiusKm * 1000
    const nearby: ArchaeologicalSite[] = []

    this.sites.forEach(site => {
      const distance = CoordinateSystem.calculateDistance(coords, site.coordinates)
      if (distance <= radiusMeters) {
        nearby.push(site)
      }
    })

    return nearby.sort((a, b) => {
      const distA = CoordinateSystem.calculateDistance(coords, a.coordinates)
      const distB = CoordinateSystem.calculateDistance(coords, b.coordinates)
      return distA - distB
    })
  }

  // Buscar por cultura
  findByCulture(culture: string): ArchaeologicalSite[] {
    return Array.from(this.sites.values()).filter(
      site => site.culture.toLowerCase().includes(culture.toLowerCase())
    )
  }

  // Buscar por período
  findByPeriod(period: string): ArchaeologicalSite[] {
    return Array.from(this.sites.values()).filter(
      site => site.period.toLowerCase().includes(period.toLowerCase())
    )
  }

  // Calcular centro geográfico de todos los sitios
  calculateCenter(): GeographicCoordinates {
    const sites = Array.from(this.sites.values())
    if (sites.length === 0) {
      return { latitude: 0, longitude: 0, altitude: 0 }
    }

    let sumLat = 0
    let sumLon = 0
    let sumAlt = 0

    sites.forEach(site => {
      sumLat += site.coordinates.latitude
      sumLon += site.coordinates.longitude
      sumAlt += site.coordinates.altitude
    })

    return {
      latitude: sumLat / sites.length,
      longitude: sumLon / sites.length,
      altitude: sumAlt / sites.length
    }
  }

  // Limpiar sitios
  clear(): void {
    this.sites.clear()
  }

  // Obtener cantidad de sitios
  count(): number {
    return this.sites.size
  }
}

// Teleport System - Sistema de teletransporte cinematográfico
export interface TeleportConfig {
  from: GeographicCoordinates
  to: GeographicCoordinates
  duration: number // ms
  altitude: number // altura de vuelo
  easing?: 'linear' | 'easeIn' | 'easeOut' | 'easeInOut'
  onProgress?: (progress: number, current: GeographicCoordinates) => void
  onComplete?: () => void
}

export class TeleportSystem {
  private isActive: boolean = false
  private animationFrameId: number | null = null

  // Teletransportar con animación
  async teleport(config: TeleportConfig): Promise<void> {
    if (this.isActive) {
      console.warn('⚠️ Teletransporte ya en progreso')
      return
    }

    this.isActive = true
    const startTime = Date.now()

    return new Promise((resolve) => {
      const animate = () => {
        const elapsed = Date.now() - startTime
        const progress = Math.min(elapsed / config.duration, 1)

        // Aplicar easing
        const easedProgress = this.applyEasing(progress, config.easing || 'easeInOut')

        // Calcular posición actual
        const current = CoordinateSystem.interpolate(
          config.from,
          config.to,
          easedProgress
        )

        // Agregar altitud de vuelo (parábola)
        const altitudeBoost = Math.sin(easedProgress * Math.PI) * config.altitude
        current.altitude += altitudeBoost

        // Callback de progreso
        if (config.onProgress) {
          config.onProgress(easedProgress, current)
        }

        // Continuar o finalizar
        if (progress < 1) {
          this.animationFrameId = requestAnimationFrame(animate)
        } else {
          this.isActive = false
          if (config.onComplete) {
            config.onComplete()
          }
          resolve()
        }
      }

      animate()
    })
  }

  // Cancelar teletransporte
  cancel(): void {
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId)
      this.animationFrameId = null
    }
    this.isActive = false
  }

  // Verificar si está activo
  isTeleporting(): boolean {
    return this.isActive
  }

  // Aplicar easing
  private applyEasing(t: number, easing: string): number {
    switch (easing) {
      case 'linear':
        return t
      case 'easeIn':
        return t * t
      case 'easeOut':
        return t * (2 - t)
      case 'easeInOut':
        return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t
      default:
        return t
    }
  }
}

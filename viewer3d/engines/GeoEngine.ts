/**
 * GeoEngine - Motor de geografía y coordenadas
 * Responsable de: Globo, Tiles, DEM, Conversiones lat/lon
 */

import * as THREE from 'three'

export class GeoEngine {
  private static instance: GeoEngine
  
  private constructor() {}
  
  static getInstance(): GeoEngine {
    if (!GeoEngine.instance) {
      GeoEngine.instance = new GeoEngine()
    }
    return GeoEngine.instance
  }
  
  /**
   * Convertir coordenadas geográficas a posición 3D en esfera
   */
  latLonToVector3(lat: number, lon: number, radius: number): THREE.Vector3 {
    const phi = (90 - lat) * (Math.PI / 180)
    const theta = (lon + 180) * (Math.PI / 180)
    
    const x = -radius * Math.sin(phi) * Math.cos(theta)
    const z = radius * Math.sin(phi) * Math.sin(theta)
    const y = radius * Math.cos(phi)
    
    return new THREE.Vector3(x, y, z)
  }
  
  /**
   * Convertir posición 3D a coordenadas geográficas
   */
  vector3ToLatLon(position: THREE.Vector3, radius: number): { lat: number, lon: number } {
    const lat = Math.asin(position.y / radius) * (180 / Math.PI)
    const lon = Math.atan2(position.x, position.z) * (180 / Math.PI)
    
    return { lat, lon }
  }
  
  /**
   * Calcular distancia entre dos puntos geográficos (Haversine)
   */
  calculateDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
    const R = 6371 // Radio de la Tierra en km
    const dLat = (lat2 - lat1) * Math.PI / 180
    const dLon = (lon2 - lon1) * Math.PI / 180
    
    const a = 
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2)
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
    
    return R * c
  }
  
  /**
   * Cargar texturas del globo
   */
  async loadGlobeTextures(): Promise<{
    day: THREE.Texture
    night: THREE.Texture
    clouds?: THREE.Texture
    normal?: THREE.Texture
    specular?: THREE.Texture
  }> {
    const loader = new THREE.TextureLoader()
    
    try {
      const [day, night] = await Promise.all([
        loader.loadAsync('/textures/earth_8k.jpg'),
        loader.loadAsync('/textures/earth_night_8k.jpg')
      ])
      
      console.log('✅ GeoEngine: Texturas cargadas')
      
      return { day, night }
    } catch (error) {
      console.error('❌ GeoEngine: Error cargando texturas', error)
      throw error
    }
  }
}

export default GeoEngine.getInstance()

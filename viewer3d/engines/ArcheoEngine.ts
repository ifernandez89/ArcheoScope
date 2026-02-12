/**
 * ArcheoEngine - Motor arqueológico
 * Responsable de: Modelos arqueológicos, Base de datos sitios, Carga dinámica
 */

import sitesData from '../data/archaeological-sites.json'

export interface ArchaeologicalSite {
  id: string
  name: string
  lat: number
  lon: number
  model: string
  description: string
  period: string
  culture: string
}

export class ArcheoEngine {
  private static instance: ArcheoEngine
  private sites: ArchaeologicalSite[] = []
  private loadedModels: Map<string, any> = new Map()
  
  private constructor() {
    this.loadSites()
  }
  
  static getInstance(): ArcheoEngine {
    if (!ArcheoEngine.instance) {
      ArcheoEngine.instance = new ArcheoEngine()
    }
    return ArcheoEngine.instance
  }
  
  /**
   * Cargar base de datos de sitios
   */
  private loadSites(): void {
    this.sites = sitesData.sites as ArchaeologicalSite[]
    console.log('🏛️ ArcheoEngine: Sitios cargados:', this.sites.length)
  }
  
  /**
   * Obtener todos los sitios
   */
  getAllSites(): ArchaeologicalSite[] {
    return this.sites
  }
  
  /**
   * Buscar sitio por ID
   */
  getSiteById(id: string): ArchaeologicalSite | undefined {
    return this.sites.find(site => site.id === id)
  }
  
  /**
   * Buscar sitios cercanos a coordenadas
   */
  getNearestSites(lat: number, lon: number, maxDistance: number = 1000): ArchaeologicalSite[] {
    return this.sites
      .map(site => ({
        site,
        distance: this.calculateDistance(lat, lon, site.lat, site.lon)
      }))
      .filter(({ distance }) => distance <= maxDistance)
      .sort((a, b) => a.distance - b.distance)
      .map(({ site }) => site)
  }
  
  /**
   * Calcular distancia entre coordenadas (Haversine)
   */
  private calculateDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
    const R = 6371
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
   * Obtener modelo para sitio
   */
  getModelForSite(site: ArchaeologicalSite): string {
    return site.model
  }
  
  /**
   * Cachear modelo cargado
   */
  cacheModel(path: string, model: any): void {
    this.loadedModels.set(path, model)
    console.log('💾 ArcheoEngine: Modelo cacheado:', path)
  }
  
  /**
   * Obtener modelo cacheado
   */
  getCachedModel(path: string): any | undefined {
    return this.loadedModels.get(path)
  }
  
  /**
   * Buscar sitios por cultura
   */
  getSitesByCulture(culture: string): ArchaeologicalSite[] {
    return this.sites.filter(site => 
      site.culture.toLowerCase().includes(culture.toLowerCase())
    )
  }
  
  /**
   * Buscar sitios por período
   */
  getSitesByPeriod(period: string): ArchaeologicalSite[] {
    return this.sites.filter(site => 
      site.period.toLowerCase().includes(period.toLowerCase())
    )
  }
}

export default ArcheoEngine.getInstance()

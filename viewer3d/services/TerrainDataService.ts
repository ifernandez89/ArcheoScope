/**
 * Terrain Data Service - Cliente para obtener datos DEM del backend
 */

export interface TerrainBounds {
  minLat: number
  maxLat: number
  minLon: number
  maxLon: number
}

export interface TerrainData {
  tile_id: string
  bounds: TerrainBounds
  resolution: number  // metros por píxel
  source: string
  data_shape: [number, number]
  elevation_range: [number, number]
  data: number[][]  // Heightmap 2D
}

export interface CacheStats {
  memory_tiles: number
  disk_tiles: number
  disk_size_mb: number
  cache_dir: string
}

export class TerrainDataService {
  private baseUrl: string
  private cache: Map<string, TerrainData> = new Map()
  
  constructor(baseUrl: string = 'http://localhost:8003') {
    this.baseUrl = baseUrl
  }
  
  /**
   * Obtiene datos de terreno para un área específica
   */
  async getTerrainData(
    latMin: number,
    latMax: number,
    lonMin: number,
    lonMax: number,
    resolution: number = 256
  ): Promise<TerrainData> {
    // Generar cache key
    const cacheKey = `${latMin.toFixed(4)}_${latMax.toFixed(4)}_${lonMin.toFixed(4)}_${lonMax.toFixed(4)}_${resolution}`
    
    // Buscar en caché local
    if (this.cache.has(cacheKey)) {
      console.log('✅ Terrain data from local cache:', cacheKey)
      return this.cache.get(cacheKey)!
    }
    
    try {
      console.log('📥 Fetching terrain data:', { latMin, latMax, lonMin, lonMax, resolution })
      
      const response = await fetch(`${this.baseUrl}/api/terrain/data`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          lat_min: latMin,
          lat_max: latMax,
          lon_min: lonMin,
          lon_max: lonMax,
          resolution
        })
      })
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      const data: TerrainData = await response.json()
      
      // Cachear localmente
      this.cache.set(cacheKey, data)
      
      console.log('✅ Terrain data received:', {
        tile_id: data.tile_id,
        source: data.source,
        shape: data.data_shape,
        elevation_range: data.elevation_range
      })
      
      return data
    } catch (error) {
      console.error('❌ Error fetching terrain data:', error)
      throw error
    }
  }
  
  /**
   * Obtiene estadísticas del caché del backend
   */
  async getCacheStats(): Promise<CacheStats> {
    try {
      const response = await fetch(`${this.baseUrl}/api/terrain/cache/stats`)
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('❌ Error fetching cache stats:', error)
      throw error
    }
  }
  
  /**
   * Limpia caché antiguo del backend
   */
  async clearCache(olderThanDays: number = 30): Promise<{ cleared_tiles: number }> {
    try {
      const response = await fetch(
        `${this.baseUrl}/api/terrain/cache/clear?older_than_days=${olderThanDays}`,
        { method: 'POST' }
      )
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('❌ Error clearing cache:', error)
      throw error
    }
  }
  
  /**
   * Pre-descarga tiles para sitios arqueológicos comunes
   */
  async prefetchCommonSites(): Promise<void> {
    try {
      const response = await fetch(
        `${this.baseUrl}/api/terrain/prefetch/common-sites`,
        { method: 'POST' }
      )
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      console.log('✅ Prefetch initiated for common archaeological sites')
    } catch (error) {
      console.error('❌ Error prefetching sites:', error)
      throw error
    }
  }
  
  /**
   * Convierte datos de terreno a Float32Array para TerrainEngine
   */
  convertToFloat32Array(data: number[][]): Float32Array {
    const height = data.length
    const width = data[0]?.length || 0
    const array = new Float32Array(height * width)
    
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        array[y * width + x] = data[y][x]
      }
    }
    
    return array
  }
  
  /**
   * Limpia caché local
   */
  clearLocalCache(): void {
    this.cache.clear()
    console.log('🗑️ Local terrain cache cleared')
  }
  
  /**
   * Obtiene tamaño del caché local
   */
  getLocalCacheSize(): number {
    return this.cache.size
  }
}

// Instancia singleton
export const terrainDataService = new TerrainDataService()

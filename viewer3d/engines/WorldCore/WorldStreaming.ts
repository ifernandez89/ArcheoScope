/**
 * WorldStreaming - Sistema de streaming de contenido
 * Responsable de: Carga/descarga dinámica, chunks, priorización
 */

import * as THREE from 'three'

export interface Chunk {
  id: string
  x: number
  z: number
  loaded: boolean
  loading: boolean
  priority: number
  data?: any
}

export interface StreamingStats {
  loadedChunks: number
  loadingChunks: number
  queuedChunks: number
  totalMemory: number
}

export class WorldStreaming {
  private static instance: WorldStreaming
  
  private chunkSize: number = 50
  private loadRadius: number = 3 // chunks
  private unloadRadius: number = 5 // chunks
  
  private chunks: Map<string, Chunk> = new Map()
  private loadQueue: string[] = []
  private maxConcurrentLoads: number = 4
  private currentLoads: number = 0
  
  private playerPosition: THREE.Vector3 = new THREE.Vector3()
  
  private constructor() {
    console.log('📦 WorldStreaming: Inicializado')
  }
  
  static getInstance(): WorldStreaming {
    if (!WorldStreaming.instance) {
      WorldStreaming.instance = new WorldStreaming()
    }
    return WorldStreaming.instance
  }
  
  /**
   * Configurar parámetros
   */
  configure(config: {
    chunkSize?: number
    loadRadius?: number
    unloadRadius?: number
    maxConcurrentLoads?: number
  }): void {
    if (config.chunkSize) this.chunkSize = config.chunkSize
    if (config.loadRadius) this.loadRadius = config.loadRadius
    if (config.unloadRadius) this.unloadRadius = config.unloadRadius
    if (config.maxConcurrentLoads) this.maxConcurrentLoads = config.maxConcurrentLoads
    
    console.log('⚙️ WorldStreaming: Configurado', config)
  }
  
  /**
   * Obtener clave de chunk
   */
  private getChunkKey(x: number, z: number): string {
    return `${x},${z}`
  }
  
  /**
   * Obtener coordenadas de chunk para posición
   */
  private getChunkCoords(position: THREE.Vector3): { x: number; z: number } {
    return {
      x: Math.floor(position.x / this.chunkSize),
      z: Math.floor(position.z / this.chunkSize)
    }
  }
  
  /**
   * Actualizar posición del jugador
   */
  updatePlayerPosition(position: THREE.Vector3): void {
    this.playerPosition.copy(position)
  }
  
  /**
   * Actualizar streaming (llamar cada frame)
   */
  update(): void {
    const playerChunk = this.getChunkCoords(this.playerPosition)
    
    // Determinar chunks a cargar
    const chunksToLoad: string[] = []
    
    for (let dx = -this.loadRadius; dx <= this.loadRadius; dx++) {
      for (let dz = -this.loadRadius; dz <= this.loadRadius; dz++) {
        const chunkX = playerChunk.x + dx
        const chunkZ = playerChunk.z + dz
        const key = this.getChunkKey(chunkX, chunkZ)
        
        const chunk = this.chunks.get(key)
        
        if (!chunk) {
          // Crear nuevo chunk
          const distance = Math.sqrt(dx * dx + dz * dz)
          this.chunks.set(key, {
            id: key,
            x: chunkX,
            z: chunkZ,
            loaded: false,
            loading: false,
            priority: 1 / (distance + 1)
          })
          chunksToLoad.push(key)
        } else if (!chunk.loaded && !chunk.loading) {
          chunksToLoad.push(key)
        }
      }
    }
    
    // Agregar a cola de carga (ordenar por prioridad)
    for (const key of chunksToLoad) {
      if (!this.loadQueue.includes(key)) {
        this.loadQueue.push(key)
      }
    }
    
    this.loadQueue.sort((a, b) => {
      const chunkA = this.chunks.get(a)!
      const chunkB = this.chunks.get(b)!
      return chunkB.priority - chunkA.priority
    })
    
    // Procesar cola de carga
    this.processLoadQueue()
    
    // Descargar chunks lejanos
    this.unloadDistantChunks(playerChunk)
  }
  
  /**
   * Procesar cola de carga
   */
  private processLoadQueue(): void {
    while (this.loadQueue.length > 0 && this.currentLoads < this.maxConcurrentLoads) {
      const key = this.loadQueue.shift()!
      const chunk = this.chunks.get(key)
      
      if (chunk && !chunk.loaded && !chunk.loading) {
        this.loadChunk(chunk)
      }
    }
  }
  
  /**
   * Cargar chunk (placeholder - implementar lógica real)
   */
  private async loadChunk(chunk: Chunk): Promise<void> {
    chunk.loading = true
    this.currentLoads++
    
    // Simular carga asíncrona
    await new Promise(resolve => setTimeout(resolve, 100))
    
    // Aquí iría la lógica real de carga
    chunk.data = { /* datos del chunk */ }
    chunk.loaded = true
    chunk.loading = false
    this.currentLoads--
    
    console.log(`📦 Chunk cargado: ${chunk.id}`)
  }
  
  /**
   * Descargar chunks lejanos
   */
  private unloadDistantChunks(playerChunk: { x: number; z: number }): void {
    const toUnload: string[] = []
    
    for (const [key, chunk] of this.chunks.entries()) {
      const dx = chunk.x - playerChunk.x
      const dz = chunk.z - playerChunk.z
      const distance = Math.sqrt(dx * dx + dz * dz)
      
      if (distance > this.unloadRadius && chunk.loaded) {
        toUnload.push(key)
      }
    }
    
    for (const key of toUnload) {
      this.unloadChunk(key)
    }
  }
  
  /**
   * Descargar chunk
   */
  private unloadChunk(key: string): void {
    const chunk = this.chunks.get(key)
    if (chunk) {
      // Liberar recursos
      chunk.data = undefined
      chunk.loaded = false
      this.chunks.delete(key)
      console.log(`📤 Chunk descargado: ${key}`)
    }
  }
  
  /**
   * Obtener estadísticas
   */
  getStats(): StreamingStats {
    let loadedChunks = 0
    let loadingChunks = 0
    
    Array.from(this.chunks.values()).forEach(chunk => {
      if (chunk.loaded) loadedChunks++
      if (chunk.loading) loadingChunks++
    })
    
    return {
      loadedChunks,
      loadingChunks,
      queuedChunks: this.loadQueue.length,
      totalMemory: this.chunks.size * 1024 // Estimación
    }
  }
  
  /**
   * Limpiar todo
   */
  clear(): void {
    this.chunks.clear()
    this.loadQueue = []
    this.currentLoads = 0
    console.log('🧹 WorldStreaming: Limpiado')
  }
}

export default WorldStreaming.getInstance()

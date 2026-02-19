/**
 * WorldSpatialIndex - Índice espacial para queries eficientes
 * Responsable de: Búsqueda espacial, culling, nearest neighbors
 */

import * as THREE from 'three'

export interface SpatialObject {
  id: string
  position: THREE.Vector3
  bounds: THREE.Box3
  data?: any
}

export interface QueryResult {
  object: SpatialObject
  distance: number
}

/**
 * Grid espacial simple para búsquedas O(1) en promedio
 */
export class WorldSpatialIndex {
  private static instance: WorldSpatialIndex
  
  private cellSize: number = 50
  private grid: Map<string, SpatialObject[]> = new Map()
  private objects: Map<string, SpatialObject> = new Map()
  
  private constructor() {
    console.log('🗺️ WorldSpatialIndex: Inicializado')
  }
  
  static getInstance(): WorldSpatialIndex {
    if (!WorldSpatialIndex.instance) {
      WorldSpatialIndex.instance = new WorldSpatialIndex()
    }
    return WorldSpatialIndex.instance
  }
  
  /**
   * Configurar tamaño de celda
   */
  setCellSize(size: number): void {
    this.cellSize = size
    this.rebuild()
    console.log(`📐 WorldSpatialIndex: Cell size = ${size}`)
  }
  
  /**
   * Obtener clave de celda para posición
   */
  private getCellKey(x: number, z: number): string {
    const cellX = Math.floor(x / this.cellSize)
    const cellZ = Math.floor(z / this.cellSize)
    return `${cellX},${cellZ}`
  }
  
  /**
   * Agregar objeto al índice
   */
  add(object: SpatialObject): void {
    const key = this.getCellKey(object.position.x, object.position.z)
    
    if (!this.grid.has(key)) {
      this.grid.set(key, [])
    }
    
    this.grid.get(key)!.push(object)
    this.objects.set(object.id, object)
  }
  
  /**
   * Remover objeto del índice
   */
  remove(id: string): boolean {
    const object = this.objects.get(id)
    if (!object) return false
    
    const key = this.getCellKey(object.position.x, object.position.z)
    const cell = this.grid.get(key)
    
    if (cell) {
      const index = cell.findIndex(obj => obj.id === id)
      if (index !== -1) {
        cell.splice(index, 1)
      }
    }
    
    this.objects.delete(id)
    return true
  }
  
  /**
   * Actualizar posición de objeto
   */
  update(id: string, newPosition: THREE.Vector3): boolean {
    const object = this.objects.get(id)
    if (!object) return false
    
    // Remover de celda anterior
    const oldKey = this.getCellKey(object.position.x, object.position.z)
    const newKey = this.getCellKey(newPosition.x, newPosition.z)
    
    if (oldKey !== newKey) {
      this.remove(id)
      object.position.copy(newPosition)
      this.add(object)
    } else {
      object.position.copy(newPosition)
    }
    
    return true
  }
  
  /**
   * Buscar objetos en radio
   */
  queryRadius(center: THREE.Vector3, radius: number): QueryResult[] {
    const results: QueryResult[] = []
    const radiusSq = radius * radius
    
    // Calcular celdas a revisar
    const cellRadius = Math.ceil(radius / this.cellSize)
    const centerCellX = Math.floor(center.x / this.cellSize)
    const centerCellZ = Math.floor(center.z / this.cellSize)
    
    for (let dx = -cellRadius; dx <= cellRadius; dx++) {
      for (let dz = -cellRadius; dz <= cellRadius; dz++) {
        const key = `${centerCellX + dx},${centerCellZ + dz}`
        const cell = this.grid.get(key)
        
        if (cell) {
          for (const object of cell) {
            const distSq = object.position.distanceToSquared(center)
            if (distSq <= radiusSq) {
              results.push({
                object,
                distance: Math.sqrt(distSq)
              })
            }
          }
        }
      }
    }
    
    return results.sort((a, b) => a.distance - b.distance)
  }
  
  /**
   * Buscar K objetos más cercanos
   */
  queryKNearest(center: THREE.Vector3, k: number, maxRadius: number = 1000): QueryResult[] {
    const results = this.queryRadius(center, maxRadius)
    return results.slice(0, k)
  }
  
  /**
   * Buscar objetos en frustum (placeholder)
   */
  queryFrustum(frustum: THREE.Frustum): SpatialObject[] {
    const results: SpatialObject[] = []
    
    Array.from(this.objects.values()).forEach(object => {
      if (frustum.intersectsBox(object.bounds)) {
        results.push(object)
      }
    })
    
    return results
  }
  
  /**
   * Obtener estadísticas
   */
  getStats(): { totalObjects: number; totalCells: number; avgObjectsPerCell: number } {
    const totalObjects = this.objects.size
    const totalCells = this.grid.size
    const avgObjectsPerCell = totalCells > 0 ? totalObjects / totalCells : 0
    
    return { totalObjects, totalCells, avgObjectsPerCell }
  }
  
  /**
   * Reconstruir índice
   */
  rebuild(): void {
    const objects = Array.from(this.objects.values())
    this.clear()
    
    for (const object of objects) {
      this.add(object)
    }
    
    console.log('🔄 WorldSpatialIndex: Reconstruido')
  }
  
  /**
   * Limpiar índice
   */
  clear(): void {
    this.grid.clear()
    this.objects.clear()
    console.log('🧹 WorldSpatialIndex: Limpiado')
  }
}

export default WorldSpatialIndex.getInstance()

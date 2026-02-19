/**
 * EntitySystem - Sistema de entidades para WorldCore
 * ECS ligero para gestionar objetos del mundo
 */

import * as THREE from 'three'

export interface Entity {
  id: string
  type: string
  position: THREE.Vector3
  rotation: THREE.Euler
  scale: THREE.Vector3
  data: Record<string, any>
  active: boolean
  created: number
  updated: number
}

export class EntitySystem {
  private entities: Map<string, Entity> = new Map()
  private entitiesByType: Map<string, Set<string>> = new Map()
  
  private stats = {
    totalEntities: 0,
    activeEntities: 0,
    entityTypes: 0
  }
  
  constructor() {
    console.log('🎯 EntitySystem: Inicializado')
  }
  
  /**
   * Crear entidad
   */
  create(
    id: string,
    type: string,
    position: THREE.Vector3,
    data: Record<string, any> = {}
  ): Entity {
    const now = performance.now()
    
    const entity: Entity = {
      id,
      type,
      position: position.clone(),
      rotation: new THREE.Euler(0, 0, 0),
      scale: new THREE.Vector3(1, 1, 1),
      data,
      active: true,
      created: now,
      updated: now
    }
    
    this.entities.set(id, entity)
    
    // Indexar por tipo
    if (!this.entitiesByType.has(type)) {
      this.entitiesByType.set(type, new Set())
      this.stats.entityTypes++
    }
    this.entitiesByType.get(type)!.add(id)
    
    this.stats.totalEntities++
    this.stats.activeEntities++
    
    return entity
  }
  
  /**
   * Obtener entidad
   */
  get(id: string): Entity | undefined {
    return this.entities.get(id)
  }
  
  /**
   * Obtener entidades por tipo
   */
  getByType(type: string): Entity[] {
    const ids = this.entitiesByType.get(type)
    if (!ids) return []
    
    return Array.from(ids)
      .map(id => this.entities.get(id))
      .filter(e => e !== undefined) as Entity[]
  }
  
  /**
   * Actualizar entidad
   */
  update(id: string, updates: Partial<Entity>): void {
    const entity = this.entities.get(id)
    if (!entity) return
    
    Object.assign(entity, updates)
    entity.updated = performance.now()
  }
  
  /**
   * Eliminar entidad
   */
  remove(id: string): void {
    const entity = this.entities.get(id)
    if (!entity) return
    
    // Remover de índice por tipo
    const typeSet = this.entitiesByType.get(entity.type)
    if (typeSet) {
      typeSet.delete(id)
      if (typeSet.size === 0) {
        this.entitiesByType.delete(entity.type)
        this.stats.entityTypes--
      }
    }
    
    this.entities.delete(id)
    this.stats.totalEntities--
    if (entity.active) this.stats.activeEntities--
  }
  
  /**
   * Activar/Desactivar entidad
   */
  setActive(id: string, active: boolean): void {
    const entity = this.entities.get(id)
    if (!entity) return
    
    if (entity.active !== active) {
      entity.active = active
      this.stats.activeEntities += active ? 1 : -1
    }
  }
  
  /**
   * Query por radio
   */
  queryRadius(center: THREE.Vector3, radius: number): Entity[] {
    const results: Entity[] = []
    const radiusSq = radius * radius
    
    Array.from(this.entities.values()).forEach(entity => {
      if (!entity.active) return
      
      const distSq = entity.position.distanceToSquared(center)
      if (distSq <= radiusSq) {
        results.push(entity)
      }
    })
    
    return results
  }
  
  /**
   * Obtener estadísticas
   */
  getStats() {
    return { ...this.stats }
  }
  
  /**
   * Limpiar
   */
  clear(): void {
    this.entities.clear()
    this.entitiesByType.clear()
    this.stats = {
      totalEntities: 0,
      activeEntities: 0,
      entityTypes: 0
    }
  }
}

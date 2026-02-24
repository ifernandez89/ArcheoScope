/**
 * WorldManager - Orquestador central de mundos
 * REGLA: Solo 1 mundo activo a la vez
 * 
 * Garantiza que nunca haya más de un mundo cargado simultáneamente,
 * previniendo problemas de escalabilidad y uso excesivo de memoria.
 */

import * as THREE from 'three'
import { loggers } from '@/core/Logger'

export interface WorldInstance {
  id: string
  scene: THREE.Scene
  createdAt: number
  metadata?: {
    type: 'globe' | 'terrain' | 'exploration'
    location?: { lat: number, lon: number }
  }
}

class WorldManager {
  private activeWorld: string | null = null
  private worlds: Map<string, WorldInstance> = new Map()
  private disposeCallbacks: Map<string, (() => void)[]> = new Map()

  /**
   * Activar un mundo (desactiva el anterior automáticamente)
   */
  setActiveWorld(worldId: string, scene?: THREE.Scene, metadata?: WorldInstance['metadata']): void {
    // Si ya es el mundo activo, no hacer nada
    if (this.activeWorld === worldId) {
      loggers.world.debug(`Mundo ya activo: ${worldId}`)
      return
    }

    // Dispose del mundo anterior
    if (this.activeWorld && this.activeWorld !== worldId) {
      loggers.world.info(`Cambiando de mundo: ${this.activeWorld} → ${worldId}`)
      this.disposeWorld(this.activeWorld)
    }

    // Registrar nuevo mundo
    if (scene) {
      this.worlds.set(worldId, {
        id: worldId,
        scene,
        createdAt: Date.now(),
        metadata
      })
    }

    this.activeWorld = worldId
    loggers.world.info(`✅ Mundo activo: ${worldId}`, metadata)
  }

  /**
   * Obtener mundo activo (siempre 0 o 1)
   */
  getActiveWorldCount(): number {
    return this.activeWorld ? 1 : 0
  }

  /**
   * Obtener ID del mundo activo
   */
  getActiveWorldId(): string | null {
    return this.activeWorld
  }

  /**
   * Registrar callback de dispose para un mundo
   */
  registerDisposeCallback(worldId: string, callback: () => void): void {
    if (!this.disposeCallbacks.has(worldId)) {
      this.disposeCallbacks.set(worldId, [])
    }
    this.disposeCallbacks.get(worldId)!.push(callback)
  }

  /**
   * Dispose completo de un mundo
   */
  private disposeWorld(worldId: string): void {
    const world = this.worlds.get(worldId)
    
    if (!world) {
      loggers.world.debug(`Mundo ${worldId} no encontrado para dispose`)
      return
    }

    const startTime = Date.now()
    let disposedObjects = 0

    // Ejecutar callbacks de dispose registrados
    const callbacks = this.disposeCallbacks.get(worldId) || []
    callbacks.forEach(callback => {
      try {
        callback()
      } catch (error) {
        loggers.world.error(`Error en dispose callback para ${worldId}:`, error)
      }
    })
    this.disposeCallbacks.delete(worldId)

    // Cleanup de recursos Three.js
    world.scene.traverse((obj) => {
      if (obj instanceof THREE.Mesh) {
        // Dispose geometry
        if (obj.geometry) {
          obj.geometry.dispose()
          disposedObjects++
        }

        // Dispose materials
        if (Array.isArray(obj.material)) {
          obj.material.forEach(m => {
            this.disposeMaterial(m)
            disposedObjects++
          })
        } else if (obj.material) {
          this.disposeMaterial(obj.material)
          disposedObjects++
        }
      }

      // Dispose de texturas en sprites
      if (obj instanceof THREE.Sprite && obj.material) {
        this.disposeMaterial(obj.material)
        disposedObjects++
      }
    })

    // Limpiar la escena
    while (world.scene.children.length > 0) {
      world.scene.remove(world.scene.children[0])
    }

    this.worlds.delete(worldId)

    const elapsed = Date.now() - startTime
    loggers.world.info(`🗑️ Mundo disposed: ${worldId}`, {
      objects: disposedObjects,
      time: `${elapsed}ms`,
      lifetime: `${((Date.now() - world.createdAt) / 1000).toFixed(1)}s`
    })
  }

  /**
   * Dispose de un material y sus texturas
   */
  private disposeMaterial(material: THREE.Material): void {
    // Dispose de texturas
    const materialWithMaps = material as any
    if (materialWithMaps.map) materialWithMaps.map.dispose()
    if (materialWithMaps.lightMap) materialWithMaps.lightMap.dispose()
    if (materialWithMaps.bumpMap) materialWithMaps.bumpMap.dispose()
    if (materialWithMaps.normalMap) materialWithMaps.normalMap.dispose()
    if (materialWithMaps.specularMap) materialWithMaps.specularMap.dispose()
    if (materialWithMaps.envMap) materialWithMaps.envMap.dispose()
    if (materialWithMaps.alphaMap) materialWithMaps.alphaMap.dispose()
    if (materialWithMaps.aoMap) materialWithMaps.aoMap.dispose()
    if (materialWithMaps.displacementMap) materialWithMaps.displacementMap.dispose()
    if (materialWithMaps.emissiveMap) materialWithMaps.emissiveMap.dispose()
    if (materialWithMaps.gradientMap) materialWithMaps.gradientMap.dispose()
    if (materialWithMaps.metalnessMap) materialWithMaps.metalnessMap.dispose()
    if (materialWithMaps.roughnessMap) materialWithMaps.roughnessMap.dispose()

    // Dispose del material
    material.dispose()
  }

  /**
   * Forzar dispose de todos los mundos (para cleanup completo)
   */
  disposeAll(): void {
    loggers.world.info('🗑️ Disposing todos los mundos...')
    const worldIds = Array.from(this.worlds.keys())
    worldIds.forEach(id => this.disposeWorld(id))
    this.activeWorld = null
  }

  /**
   * Obtener estadísticas del WorldManager
   */
  getStats(): {
    activeWorld: string | null
    activeCount: number
    totalWorlds: number
    worlds: Array<{ id: string, type?: string, age: number }>
  } {
    return {
      activeWorld: this.activeWorld,
      activeCount: this.getActiveWorldCount(),
      totalWorlds: this.worlds.size,
      worlds: Array.from(this.worlds.values()).map(w => ({
        id: w.id,
        type: w.metadata?.type,
        age: Math.floor((Date.now() - w.createdAt) / 1000)
      }))
    }
  }
}

// Singleton instance
export const worldManager = new WorldManager()

// Export para debugging
if (typeof window !== 'undefined') {
  (window as any).__worldManager = worldManager
}

export default worldManager

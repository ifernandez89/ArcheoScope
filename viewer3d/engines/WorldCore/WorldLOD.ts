/**
 * WorldLOD - Sistema de Level of Detail
 * Responsable de: LOD automático, transiciones, optimización de rendimiento
 */

import * as THREE from 'three'

export interface LODLevel {
  distance: number
  detail: number // 0-1 (0 = mínimo, 1 = máximo)
}

export interface LODObject {
  id: string
  position: THREE.Vector3
  levels: THREE.Object3D[]
  currentLevel: number
}

export class WorldLOD {
  private static instance: WorldLOD
  
  private lodLevels: LODLevel[] = [
    { distance: 50, detail: 1.0 },   // Cerca - máximo detalle
    { distance: 150, detail: 0.6 },  // Medio - detalle medio
    { distance: 300, detail: 0.3 },  // Lejos - bajo detalle
    { distance: 500, detail: 0.1 }   // Muy lejos - mínimo detalle
  ]
  
  private objects: Map<string, LODObject> = new Map()
  private cameraPosition: THREE.Vector3 = new THREE.Vector3()
  
  private constructor() {
    console.log('🎚️ WorldLOD: Inicializado')
  }
  
  static getInstance(): WorldLOD {
    if (!WorldLOD.instance) {
      WorldLOD.instance = new WorldLOD()
    }
    return WorldLOD.instance
  }
  
  /**
   * Configurar niveles de LOD
   */
  setLODLevels(levels: LODLevel[]): void {
    this.lodLevels = levels.sort((a, b) => a.distance - b.distance)
    console.log('🎚️ WorldLOD: Niveles configurados', levels.length)
  }
  
  /**
   * Obtener niveles de LOD
   */
  getLODLevels(): LODLevel[] {
    return [...this.lodLevels]
  }
  
  /**
   * Registrar objeto con LOD
   */
  register(id: string, position: THREE.Vector3, levels: THREE.Object3D[]): void {
    this.objects.set(id, {
      id,
      position,
      levels,
      currentLevel: 0
    })
  }
  
  /**
   * Desregistrar objeto
   */
  unregister(id: string): boolean {
    return this.objects.delete(id)
  }
  
  /**
   * Actualizar posición de cámara
   */
  updateCamera(position: THREE.Vector3): void {
    this.cameraPosition.copy(position)
  }
  
  /**
   * Calcular nivel de LOD para distancia
   */
  calculateLODLevel(distance: number): number {
    for (let i = 0; i < this.lodLevels.length; i++) {
      if (distance < this.lodLevels[i].distance) {
        return i
      }
    }
    return this.lodLevels.length - 1
  }
  
  /**
   * Actualizar LOD de todos los objetos
   */
  update(): { changed: number; total: number } {
    let changed = 0
    
    Array.from(this.objects.values()).forEach(object => {
      const distance = object.position.distanceTo(this.cameraPosition)
      const newLevel = this.calculateLODLevel(distance)
      
      if (newLevel !== object.currentLevel) {
        // Ocultar nivel anterior
        if (object.levels[object.currentLevel]) {
          object.levels[object.currentLevel].visible = false
        }
        
        // Mostrar nuevo nivel
        if (object.levels[newLevel]) {
          object.levels[newLevel].visible = true
        }
        
        object.currentLevel = newLevel
        changed++
      }
    })
    
    return { changed, total: this.objects.size }
  }
  
  /**
   * Obtener nivel de detalle para distancia
   */
  getDetailLevel(distance: number): number {
    const level = this.calculateLODLevel(distance)
    return this.lodLevels[level]?.detail ?? 0.1
  }
  
  /**
   * Obtener estadísticas
   */
  getStats(): { 
    totalObjects: number
    byLevel: Record<number, number>
  } {
    const byLevel: Record<number, number> = {}
    
    Array.from(this.objects.values()).forEach(object => {
      byLevel[object.currentLevel] = (byLevel[object.currentLevel] || 0) + 1
    })
    
    return {
      totalObjects: this.objects.size,
      byLevel
    }
  }
  
  /**
   * Limpiar
   */
  clear(): void {
    this.objects.clear()
    console.log('🧹 WorldLOD: Limpiado')
  }
}

export default WorldLOD.getInstance()

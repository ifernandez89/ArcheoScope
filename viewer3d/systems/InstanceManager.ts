/**
 * InstanceManager - Sistema de instancing agresivo
 * 
 * Regla: Si se repite → InstancedMesh
 * Meta: 1 draw call por tipo de objeto
 */

import * as THREE from 'three'
import { loggers } from '@/core/Logger'

export interface InstanceConfig {
  geometry: THREE.BufferGeometry
  material: THREE.Material
  count: number
  frustumCulled?: boolean
}

export interface InstanceData {
  position: THREE.Vector3
  rotation: THREE.Euler
  scale: THREE.Vector3
  color?: THREE.Color
  visible?: boolean
}

export class InstanceManager {
  private static instance: InstanceManager
  
  private instancedMeshes: Map<string, THREE.InstancedMesh> = new Map()
  private instanceData: Map<string, InstanceData[]> = new Map()
  private needsUpdate: Set<string> = new Set()
  
  private stats = {
    totalTypes: 0,
    totalInstances: 0,
    drawCalls: 0,
    savedDrawCalls: 0
  }
  
  private constructor() {
    loggers.performance.info('InstanceManager inicializado')
  }
  
  static getInstance(): InstanceManager {
    if (!InstanceManager.instance) {
      InstanceManager.instance = new InstanceManager()
    }
    return InstanceManager.instance
  }
  
  /**
   * Crear instanced mesh
   */
  create(
    id: string,
    config: InstanceConfig
  ): THREE.InstancedMesh {
    if (this.instancedMeshes.has(id)) {
      loggers.performance.warn(`InstanceManager: ${id} ya existe`)
      return this.instancedMeshes.get(id)!
    }
    
    const mesh = new THREE.InstancedMesh(
      config.geometry,
      config.material,
      config.count
    )
    
    mesh.frustumCulled = config.frustumCulled ?? true
    mesh.name = id
    
    // Inicializar matrices
    const matrix = new THREE.Matrix4()
    for (let i = 0; i < config.count; i++) {
      mesh.setMatrixAt(i, matrix)
    }
    
    // Inicializar colores si el material lo soporta
    if ((config.material as any).vertexColors) {
      mesh.instanceColor = new THREE.InstancedBufferAttribute(
        new Float32Array(config.count * 3),
        3
      )
    }
    
    this.instancedMeshes.set(id, mesh)
    this.instanceData.set(id, [])
    
    this.stats.totalTypes++
    this.stats.drawCalls++
    
    loggers.performance.debug(`InstanceManager: Creado ${id} (${config.count} instancias)`)
    
    return mesh
  }
  
  /**
   * Actualizar instancia individual
   */
  setInstance(
    id: string,
    index: number,
    data: InstanceData
  ): void {
    const mesh = this.instancedMeshes.get(id)
    if (!mesh) {
      loggers.performance.warn(`InstanceManager: ${id} no existe`)
      return
    }
    
    if (index >= mesh.count) {
      loggers.performance.warn(`InstanceManager: índice ${index} fuera de rango`)
      return
    }
    
    // Actualizar matriz
    const matrix = new THREE.Matrix4()
    matrix.compose(
      data.position,
      new THREE.Quaternion().setFromEuler(data.rotation),
      data.scale
    )
    mesh.setMatrixAt(index, matrix)
    
    // Actualizar color si existe
    if (data.color && mesh.instanceColor) {
      mesh.instanceColor.setXYZ(index, data.color.r, data.color.g, data.color.b)
    }
    
    // Guardar data
    const dataArray = this.instanceData.get(id)!
    dataArray[index] = data
    
    this.needsUpdate.add(id)
  }
  
  /**
   * Actualizar múltiples instancias (batch)
   */
  setInstances(
    id: string,
    instances: InstanceData[]
  ): void {
    const mesh = this.instancedMeshes.get(id)
    if (!mesh) {
      loggers.performance.warn(`InstanceManager: ${id} no existe`)
      return
    }
    
    const count = Math.min(instances.length, mesh.count)
    
    for (let i = 0; i < count; i++) {
      const data = instances[i]
      
      const matrix = new THREE.Matrix4()
      matrix.compose(
        data.position,
        new THREE.Quaternion().setFromEuler(data.rotation),
        data.scale
      )
      mesh.setMatrixAt(i, matrix)
      
      if (data.color && mesh.instanceColor) {
        mesh.instanceColor.setXYZ(i, data.color.r, data.color.g, data.color.b)
      }
    }
    
    this.instanceData.set(id, instances)
    this.needsUpdate.add(id)
    
    this.stats.totalInstances = instances.length
    this.stats.savedDrawCalls = instances.length - 1
  }
  
  /**
   * Update - Aplicar cambios pendientes
   */
  update(): void {
    for (const id of this.needsUpdate) {
      const mesh = this.instancedMeshes.get(id)
      if (mesh) {
        mesh.instanceMatrix.needsUpdate = true
        
        if (mesh.instanceColor) {
          mesh.instanceColor.needsUpdate = true
        }
      }
    }
    
    this.needsUpdate.clear()
  }
  
  /**
   * Obtener mesh
   */
  get(id: string): THREE.InstancedMesh | undefined {
    return this.instancedMeshes.get(id)
  }
  
  /**
   * Obtener data de instancias
   */
  getData(id: string): InstanceData[] {
    return this.instanceData.get(id) || []
  }
  
  /**
   * Eliminar instanced mesh
   */
  remove(id: string): void {
    const mesh = this.instancedMeshes.get(id)
    if (mesh) {
      mesh.geometry.dispose()
      
      if (Array.isArray(mesh.material)) {
        mesh.material.forEach(mat => mat.dispose())
      } else {
        mesh.material.dispose()
      }
      
      this.instancedMeshes.delete(id)
      this.instanceData.delete(id)
      this.needsUpdate.delete(id)
      
      this.stats.totalTypes--
      this.stats.drawCalls--
      
      loggers.performance.debug(`InstanceManager: Eliminado ${id}`)
    }
  }
  
  /**
   * Obtener estadísticas
   */
  getStats(): typeof InstanceManager.prototype.stats {
    return { ...this.stats }
  }
  
  /**
   * Limpiar todo
   */
  clear(): void {
    for (const id of this.instancedMeshes.keys()) {
      this.remove(id)
    }
    
    this.stats = {
      totalTypes: 0,
      totalInstances: 0,
      drawCalls: 0,
      savedDrawCalls: 0
    }
    
    loggers.performance.info('InstanceManager limpiado')
  }
}

export default InstanceManager.getInstance()

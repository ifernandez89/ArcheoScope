/**
 * CullingSystem - Culling agresivo para performance
 * 
 * Regla: Si no se ve → no existe
 * - Frustum culling
 * - Distance culling
 * - Desmontaje real de objetos lejanos
 */

import * as THREE from 'three'
import { WorldCore } from '@/engines/WorldCore'

export interface CullableObject {
  id: string
  object3D: THREE.Object3D
  position: THREE.Vector3
  bounds: THREE.Box3
  priority: number // 0-1 (1 = crítico, 0 = descartable)
  maxDistance: number // Distancia máxima antes de desmontar
  isCulled: boolean
  isDisposed: boolean
}

export class CullingSystem {
  private static instance: CullingSystem
  
  private objects: Map<string, CullableObject> = new Map()
  private camera: THREE.Camera | null = null
  private frustum: THREE.Frustum = new THREE.Frustum()
  private projScreenMatrix: THREE.Matrix4 = new THREE.Matrix4()
  
  // Configuración
  private config = {
    enableFrustumCulling: true,
    enableDistanceCulling: true,
    enableDisposal: true,
    maxRenderDistance: 2000, // 2km
    disposalDistance: 2500, // 2.5km - desmontar completamente
    updateInterval: 100, // ms entre updates
  }
  
  private lastUpdate: number = 0
  private stats = {
    totalObjects: 0,
    visibleObjects: 0,
    culledObjects: 0,
    disposedObjects: 0,
    savedDrawCalls: 0
  }
  
  private constructor() {
    console.log('✂️ CullingSystem: Inicializado')
  }
  
  static getInstance(): CullingSystem {
    if (!CullingSystem.instance) {
      CullingSystem.instance = new CullingSystem()
    }
    return CullingSystem.instance
  }
  
  /**
   * Configurar sistema
   */
  configure(config: Partial<typeof CullingSystem.prototype.config>): void {
    this.config = { ...this.config, ...config }
    console.log('⚙️ CullingSystem: Configurado', config)
  }
  
  /**
   * Establecer cámara
   */
  setCamera(camera: THREE.Camera): void {
    this.camera = camera
  }
  
  /**
   * Registrar objeto para culling
   */
  register(object: Omit<CullableObject, 'isCulled' | 'isDisposed'>): void {
    this.objects.set(object.id, {
      ...object,
      isCulled: false,
      isDisposed: false
    })
    
    this.stats.totalObjects++
  }
  
  /**
   * Desregistrar objeto
   */
  unregister(id: string): void {
    const object = this.objects.get(id)
    if (object) {
      if (!object.isDisposed) {
        this.disposeObject(object)
      }
      this.objects.delete(id)
      this.stats.totalObjects--
    }
  }
  
  /**
   * Update principal - Llamar desde EngineCore
   */
  update(delta: number): void {
    if (!this.camera) return
    
    const now = performance.now()
    if (now - this.lastUpdate < this.config.updateInterval) return
    
    this.lastUpdate = now
    
    // Actualizar frustum
    if (this.config.enableFrustumCulling) {
      this.updateFrustum()
    }
    
    // Reset stats
    this.stats.visibleObjects = 0
    this.stats.culledObjects = 0
    this.stats.savedDrawCalls = 0
    
    // Procesar cada objeto
    for (const object of this.objects.values()) {
      this.processObject(object)
    }
  }
  
  /**
   * Actualizar frustum de cámara
   */
  private updateFrustum(): void {
    if (!this.camera) return
    
    this.camera.updateMatrixWorld()
    this.projScreenMatrix.multiplyMatrices(
      this.camera.projectionMatrix,
      this.camera.matrixWorldInverse
    )
    this.frustum.setFromProjectionMatrix(this.projScreenMatrix)
  }
  
  /**
   * Procesar objeto individual
   */
  private processObject(object: CullableObject): void {
    if (object.isDisposed) return
    if (!this.camera) return
    
    const distance = this.camera.position.distanceTo(object.position)
    
    // 1. Distance-based disposal (AGRESIVO)
    if (this.config.enableDisposal && distance > this.config.disposalDistance) {
      this.disposeObject(object)
      this.stats.disposedObjects++
      return
    }
    
    // 2. Distance culling
    if (this.config.enableDistanceCulling && distance > this.config.maxRenderDistance) {
      this.cullObject(object, 'distance')
      this.stats.culledObjects++
      this.stats.savedDrawCalls++
      return
    }
    
    // 3. Frustum culling
    if (this.config.enableFrustumCulling) {
      if (!this.frustum.intersectsBox(object.bounds)) {
        this.cullObject(object, 'frustum')
        this.stats.culledObjects++
        this.stats.savedDrawCalls++
        return
      }
    }
    
    // 4. Objeto visible
    this.showObject(object)
    this.stats.visibleObjects++
  }
  
  /**
   * Ocultar objeto (culling)
   */
  private cullObject(object: CullableObject, reason: 'frustum' | 'distance'): void {
    if (object.isCulled) return
    
    object.object3D.visible = false
    object.isCulled = true
    
    // Opcional: Desactivar traverse para ahorrar más CPU
    object.object3D.traverse((child) => {
      if ((child as any).isMesh) {
        (child as THREE.Mesh).frustumCulled = false
      }
    })
  }
  
  /**
   * Mostrar objeto
   */
  private showObject(object: CullableObject): void {
    if (!object.isCulled) return
    
    object.object3D.visible = true
    object.isCulled = false
    
    object.object3D.traverse((child) => {
      if ((child as any).isMesh) {
        (child as THREE.Mesh).frustumCulled = true
      }
    })
  }
  
  /**
   * Desmontar objeto completamente (liberar memoria)
   */
  private disposeObject(object: CullableObject): void {
    if (object.isDisposed) return
    
    // Ocultar
    object.object3D.visible = false
    
    // Liberar geometrías y materiales
    object.object3D.traverse((child) => {
      if ((child as any).isMesh) {
        const mesh = child as THREE.Mesh
        
        // Geometría
        if (mesh.geometry) {
          mesh.geometry.dispose()
        }
        
        // Material
        if (mesh.material) {
          if (Array.isArray(mesh.material)) {
            mesh.material.forEach(mat => this.disposeMaterial(mat))
          } else {
            this.disposeMaterial(mesh.material)
          }
        }
      }
    })
    
    // Remover de escena si tiene parent
    if (object.object3D.parent) {
      object.object3D.parent.remove(object.object3D)
    }
    
    object.isDisposed = true
    
    console.log(`🗑️ CullingSystem: Objeto ${object.id} desmontado`)
  }
  
  /**
   * Liberar material
   */
  private disposeMaterial(material: THREE.Material): void {
    // Texturas
    if ((material as any).map) (material as any).map.dispose()
    if ((material as any).lightMap) (material as any).lightMap.dispose()
    if ((material as any).bumpMap) (material as any).bumpMap.dispose()
    if ((material as any).normalMap) (material as any).normalMap.dispose()
    if ((material as any).specularMap) (material as any).specularMap.dispose()
    if ((material as any).envMap) (material as any).envMap.dispose()
    
    material.dispose()
  }
  
  /**
   * Obtener estadísticas
   */
  getStats(): typeof CullingSystem.prototype.stats {
    return { ...this.stats }
  }
  
  /**
   * Obtener objetos visibles
   */
  getVisibleObjects(): CullableObject[] {
    return Array.from(this.objects.values()).filter(obj => !obj.isCulled && !obj.isDisposed)
  }
  
  /**
   * Obtener objetos culled
   */
  getCulledObjects(): CullableObject[] {
    return Array.from(this.objects.values()).filter(obj => obj.isCulled && !obj.isDisposed)
  }
  
  /**
   * Forzar update de bounds
   */
  updateBounds(id: string): void {
    const object = this.objects.get(id)
    if (object) {
      object.bounds.setFromObject(object.object3D)
    }
  }
  
  /**
   * Limpiar objetos disposed
   */
  cleanupDisposed(): void {
    const toRemove: string[] = []
    
    for (const [id, object] of this.objects.entries()) {
      if (object.isDisposed) {
        toRemove.push(id)
      }
    }
    
    toRemove.forEach(id => this.objects.delete(id))
    
    console.log(`🧹 CullingSystem: ${toRemove.length} objetos limpiados`)
  }
  
  /**
   * Reset completo
   */
  reset(): void {
    // Desmontar todos los objetos
    for (const object of this.objects.values()) {
      if (!object.isDisposed) {
        this.disposeObject(object)
      }
    }
    
    this.objects.clear()
    this.stats = {
      totalObjects: 0,
      visibleObjects: 0,
      culledObjects: 0,
      disposedObjects: 0,
      savedDrawCalls: 0
    }
    
    console.log('🔄 CullingSystem: Reset completo')
  }
}

export default CullingSystem.getInstance()

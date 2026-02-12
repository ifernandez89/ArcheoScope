/**
 * OptimizationSystem - Sistema de optimización y performance
 * Lazy loading, LOD, Frustum culling, Instancing
 */

import * as THREE from 'three'

export class OptimizationSystem {
  private static instance: OptimizationSystem
  private loadedAssets: Map<string, any> = new Map()
  private activeModels: Set<string> = new Set()
  private maxConcurrentLoads = 3
  
  private constructor() {}
  
  static getInstance(): OptimizationSystem {
    if (!OptimizationSystem.instance) {
      OptimizationSystem.instance = new OptimizationSystem()
    }
    return OptimizationSystem.instance
  }
  
  /**
   * Lazy load de asset con caché
   */
  async lazyLoadAsset(path: string, loader: any): Promise<any> {
    // Verificar caché
    if (this.loadedAssets.has(path)) {
      console.log('📦 Asset cacheado:', path)
      return this.loadedAssets.get(path)
    }
    
    // Cargar asset
    console.log('⏳ Cargando asset:', path)
    const asset = await loader.loadAsync(path)
    
    // Cachear
    this.loadedAssets.set(path, asset)
    console.log('✅ Asset cargado y cacheado:', path)
    
    return asset
  }
  
  /**
   * Descargar assets no usados
   */
  unloadUnusedAssets(currentAssets: string[]): void {
    const toUnload: string[] = []
    
    this.loadedAssets.forEach((asset, path) => {
      if (!currentAssets.includes(path)) {
        toUnload.push(path)
      }
    })
    
    toUnload.forEach(path => {
      const asset = this.loadedAssets.get(path)
      
      // Liberar memoria
      if (asset.geometry) asset.geometry.dispose()
      if (asset.material) {
        if (Array.isArray(asset.material)) {
          asset.material.forEach((m: any) => m.dispose())
        } else {
          asset.material.dispose()
        }
      }
      
      this.loadedAssets.delete(path)
      console.log('🗑️ Asset descargado:', path)
    })
  }
  
  /**
   * Optimizar geometría con Draco (simulado)
   */
  optimizeGeometry(geometry: THREE.BufferGeometry): THREE.BufferGeometry {
    // Simplificar si tiene demasiados vértices
    const positions = geometry.attributes.position
    
    if (positions && positions.count > 100000) {
      console.log('⚠️ Geometría muy pesada, considerar simplificar')
    }
    
    // Computar bounding sphere para frustum culling
    geometry.computeBoundingSphere()
    geometry.computeBoundingBox()
    
    return geometry
  }
  
  /**
   * Crear LOD (Level of Detail) para modelo
   */
  createLOD(model: THREE.Object3D, distances: number[] = [0, 10, 20]): THREE.LOD {
    const lod = new THREE.LOD()
    
    // LOD 0 - Alta calidad (cerca)
    lod.addLevel(model.clone(), distances[0])
    
    // LOD 1 - Media calidad
    const mediumQuality = model.clone()
    mediumQuality.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh
        // Reducir calidad de material
        if (mesh.material) {
          (mesh.material as THREE.MeshStandardMaterial).roughness = 0.8
        }
      }
    })
    lod.addLevel(mediumQuality, distances[1])
    
    // LOD 2 - Baja calidad (lejos)
    const lowQuality = model.clone()
    lowQuality.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh
        mesh.castShadow = false
        mesh.receiveShadow = false
      }
    })
    lod.addLevel(lowQuality, distances[2])
    
    console.log('🎚️ LOD creado con', lod.levels.length, 'niveles')
    
    return lod
  }
  
  /**
   * Instancing para marcadores (miles sin costo)
   */
  createInstancedMarkers(
    positions: THREE.Vector3[],
    geometry: THREE.BufferGeometry,
    material: THREE.Material
  ): THREE.InstancedMesh {
    const count = positions.length
    const mesh = new THREE.InstancedMesh(geometry, material, count)
    
    const matrix = new THREE.Matrix4()
    
    positions.forEach((position, i) => {
      matrix.setPosition(position)
      mesh.setMatrixAt(i, matrix)
    })
    
    mesh.instanceMatrix.needsUpdate = true
    
    console.log('🔢 Instancing creado:', count, 'marcadores')
    
    return mesh
  }
  
  /**
   * Comprimir textura
   */
  compressTexture(texture: THREE.Texture, maxSize: number = 2048): THREE.Texture {
    if (texture.image) {
      const { width, height } = texture.image
      
      if (width > maxSize || height > maxSize) {
        console.log('🗜️ Comprimiendo textura de', width, 'x', height)
        
        // Crear canvas para redimensionar
        const canvas = document.createElement('canvas')
        const scale = maxSize / Math.max(width, height)
        canvas.width = width * scale
        canvas.height = height * scale
        
        const ctx = canvas.getContext('2d')!
        ctx.drawImage(texture.image, 0, 0, canvas.width, canvas.height)
        
        texture.image = canvas
        texture.needsUpdate = true
      }
    }
    
    return texture
  }
  
  /**
   * Obtener estadísticas de performance
   */
  getPerformanceStats(): {
    loadedAssets: number
    activeModels: number
    memoryUsage: string
  } {
    return {
      loadedAssets: this.loadedAssets.size,
      activeModels: this.activeModels.size,
      memoryUsage: `~${(this.loadedAssets.size * 5).toFixed(0)} MB`
    }
  }
  
  /**
   * Limpiar todo
   */
  dispose(): void {
    this.loadedAssets.forEach((asset, path) => {
      if (asset.geometry) asset.geometry.dispose()
      if (asset.material) {
        if (Array.isArray(asset.material)) {
          asset.material.forEach((m: any) => m.dispose())
        } else {
          asset.material.dispose()
        }
      }
    })
    
    this.loadedAssets.clear()
    this.activeModels.clear()
    
    console.log('🧹 OptimizationSystem limpiado')
  }
}

export default OptimizationSystem.getInstance()

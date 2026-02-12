/**
 * WorldEngine - Motor de mundo 3D
 * Responsable de: Terreno, Colisiones, Navegación, LOD
 */

import * as THREE from 'three'

export class WorldEngine {
  private static instance: WorldEngine
  private collisionBoxes: THREE.Box3[] = []
  
  private constructor() {}
  
  static getInstance(): WorldEngine {
    if (!WorldEngine.instance) {
      WorldEngine.instance = new WorldEngine()
    }
    return WorldEngine.instance
  }
  
  /**
   * Generar terreno procedural con elevación
   */
  generateTerrain(
    location: { lat: number, lon: number },
    size: number = 50,
    resolution: number = 128
  ): THREE.Mesh {
    const geometry = new THREE.PlaneGeometry(size, size, resolution, resolution)
    const positions = geometry.attributes.position.array as Float32Array
    
    // Aplicar elevación procedural basada en coordenadas
    for (let i = 0; i < positions.length; i += 3) {
      const x = positions[i]
      const y = positions[i + 1]
      
      // Ruido procedural multi-octava
      const elevation = 
        Math.sin(x * 0.1 + location.lat) * 0.5 +
        Math.cos(y * 0.1 + location.lon) * 0.5 +
        Math.sin(x * 0.05) * Math.cos(y * 0.05) * 1.0 +
        Math.sin(x * 0.2) * 0.2 +
        Math.cos(y * 0.2) * 0.2
      
      positions[i + 2] = elevation
    }
    
    geometry.attributes.position.needsUpdate = true
    geometry.computeVertexNormals()
    
    const material = new THREE.MeshStandardMaterial({
      color: '#4a5d3f',
      roughness: 0.9,
      metalness: 0.1,
      wireframe: false
    })
    
    const mesh = new THREE.Mesh(geometry, material)
    mesh.rotation.x = -Math.PI / 2
    mesh.position.y = -1
    mesh.receiveShadow = true
    
    console.log('🏔️ WorldEngine: Terreno generado')
    
    return mesh
  }
  
  /**
   * Registrar objetos para colisiones
   */
  registerCollisionObjects(model: THREE.Object3D): void {
    this.collisionBoxes = []
    
    model.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh
        const box = new THREE.Box3().setFromObject(mesh)
        this.collisionBoxes.push(box)
      }
    })
    
    console.log('🛡️ WorldEngine: Colisiones registradas:', this.collisionBoxes.length)
  }
  
  /**
   * Verificar colisión con posición
   */
  checkCollision(position: THREE.Vector3, size: THREE.Vector3 = new THREE.Vector3(0.5, 1.8, 0.5)): boolean {
    const box = new THREE.Box3().setFromCenterAndSize(position, size)
    
    for (const collisionBox of this.collisionBoxes) {
      if (box.intersectsBox(collisionBox)) {
        return true
      }
    }
    
    return false
  }
  
  /**
   * Obtener altura del terreno en posición
   */
  getTerrainHeight(x: number, z: number): number {
    // Simplificado - en producción usar raycasting
    return Math.sin(x * 0.1) * 0.5 + Math.cos(z * 0.1) * 0.5
  }
  
  /**
   * Limpiar recursos
   */
  dispose(): void {
    this.collisionBoxes = []
    console.log('🧹 WorldEngine: Recursos liberados')
  }
}

export default WorldEngine.getInstance()

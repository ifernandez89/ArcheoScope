/**
 * ProceduralGenerator - Generación procedural para WorldCore
 * Genera contenido del mundo de forma determinista
 */

import * as THREE from 'three'

export interface GeneratorConfig {
  seed: number
  density: number
  minDistance: number
}

export class ProceduralGenerator {
  private seed: number = 42
  
  constructor(seed: number = 42) {
    this.seed = seed
    console.log('🌱 ProceduralGenerator: Inicializado (seed:', seed, ')')
  }
  
  /**
   * Seeded random
   */
  private random(seed: number): number {
    const x = Math.sin(seed) * 10000
    return x - Math.floor(x)
  }
  
  /**
   * Noise 2D simple (Perlin-like)
   */
  noise2D(x: number, y: number): number {
    const n = Math.sin(x * 12.9898 + y * 78.233) * 43758.5453
    return n - Math.floor(n)
  }
  
  /**
   * Noise multi-octava
   */
  fbm(x: number, y: number, octaves: number = 4): number {
    let value = 0
    let amplitude = 1
    let frequency = 1
    let maxValue = 0
    
    for (let i = 0; i < octaves; i++) {
      value += this.noise2D(x * frequency, y * frequency) * amplitude
      maxValue += amplitude
      amplitude *= 0.5
      frequency *= 2
    }
    
    return value / maxValue
  }
  
  /**
   * Generar posiciones en grid
   */
  generateGrid(
    config: GeneratorConfig,
    bounds: { min: THREE.Vector2; max: THREE.Vector2 }
  ): THREE.Vector3[] {
    const positions: THREE.Vector3[] = []
    const { density, minDistance } = config
    
    const width = bounds.max.x - bounds.min.x
    const height = bounds.max.y - bounds.min.y
    
    const cols = Math.floor(width / minDistance)
    const rows = Math.floor(height / minDistance)
    
    for (let i = 0; i < cols; i++) {
      for (let j = 0; j < rows; j++) {
        // Probabilidad basada en densidad
        if (this.random(this.seed + i * 1000 + j) > density) continue
        
        const x = bounds.min.x + (i + this.random(this.seed + i * 2000 + j)) * minDistance
        const z = bounds.min.y + (j + this.random(this.seed + i * 3000 + j)) * minDistance
        
        // Altura basada en noise
        const y = this.fbm(x * 0.01, z * 0.01, 3) * 10
        
        positions.push(new THREE.Vector3(x, y, z))
      }
    }
    
    return positions
  }
  
  /**
   * Generar posiciones en círculo
   */
  generateCircle(
    config: GeneratorConfig,
    center: THREE.Vector2,
    radius: number
  ): THREE.Vector3[] {
    const positions: THREE.Vector3[] = []
    const { density, minDistance } = config
    
    const count = Math.floor((Math.PI * radius * radius) / (minDistance * minDistance) * density)
    
    for (let i = 0; i < count; i++) {
      const angle = this.random(this.seed + i * 1000) * Math.PI * 2
      const distance = Math.sqrt(this.random(this.seed + i * 2000)) * radius
      
      const x = center.x + Math.cos(angle) * distance
      const z = center.y + Math.sin(angle) * distance
      
      const y = this.fbm(x * 0.01, z * 0.01, 3) * 10
      
      positions.push(new THREE.Vector3(x, y, z))
    }
    
    return positions
  }
  
  /**
   * Generar terreno
   */
  generateTerrain(
    width: number,
    height: number,
    resolution: number
  ): Float32Array {
    const size = resolution * resolution
    const data = new Float32Array(size)
    
    for (let i = 0; i < resolution; i++) {
      for (let j = 0; j < resolution; j++) {
        const x = (i / resolution) * width
        const z = (j / resolution) * height
        
        const elevation = this.fbm(x * 0.01, z * 0.01, 5) * 50
        
        data[i * resolution + j] = elevation
      }
    }
    
    return data
  }
  
  /**
   * Cambiar seed
   */
  setSeed(seed: number): void {
    this.seed = seed
    console.log('🌱 Seed cambiado:', seed)
  }
}

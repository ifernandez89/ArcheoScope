/**
 * Environment Worker - Generación procedural en background
 * NO bloquea el main thread
 */

import { detectBiome, getSkyColorForBiome, getFogColorForBiome } from '../utils/biome-detector'

export interface TerrainGenerationRequest {
  type: 'generateTerrain'
  location: { lat: number; lon: number }
  size: number
  resolution: number
  seed?: number
}

export interface BiomeAnalysisRequest {
  type: 'analyzeBiome'
  location: { lat: number; lon: number }
  isDay: boolean
}

export interface EnvironmentGenerationRequest {
  type: 'generateEnvironment'
  location: { lat: number; lon: number }
  size: number
  resolution: number
  isDay: boolean
}

export type WorkerRequest = 
  | TerrainGenerationRequest 
  | BiomeAnalysisRequest 
  | EnvironmentGenerationRequest

export interface TerrainData {
  positions: Float32Array
  normals: Float32Array
  uvs: Float32Array
  indices: Uint32Array
}

export interface BiomeData {
  type: string
  name: string
  description: string
  temperature: number
  humidity: number
  skyColor: string
  fogColor: string
}

export interface EnvironmentData {
  terrain: TerrainData
  biome: BiomeData
  vegetation: Array<{ x: number; y: number; z: number; type: string }>
  rocks: Array<{ x: number; y: number; z: number; scale: number }>
}

/**
 * Generar terreno procedural
 */
function generateTerrain(
  location: { lat: number; lon: number },
  size: number,
  resolution: number,
  seed: number = 0
): TerrainData {
  const segments = resolution
  const vertices = (segments + 1) * (segments + 1)
  const positions = new Float32Array(vertices * 3)
  const normals = new Float32Array(vertices * 3)
  const uvs = new Float32Array(vertices * 2)
  const indices = new Uint32Array(segments * segments * 6)
  
  const halfSize = size / 2
  const segmentSize = size / segments
  
  // Generar posiciones y UVs
  let vertexIndex = 0
  for (let iy = 0; iy <= segments; iy++) {
    const y = iy * segmentSize - halfSize
    
    for (let ix = 0; ix <= segments; ix++) {
      const x = ix * segmentSize - halfSize
      
      // Ruido procedural multi-octava
      const elevation = calculateElevation(x, y, location, seed)
      
      positions[vertexIndex * 3] = x
      positions[vertexIndex * 3 + 1] = y
      positions[vertexIndex * 3 + 2] = elevation
      
      uvs[vertexIndex * 2] = ix / segments
      uvs[vertexIndex * 2 + 1] = iy / segments
      
      vertexIndex++
    }
  }
  
  // Generar índices
  let indexOffset = 0
  for (let iy = 0; iy < segments; iy++) {
    for (let ix = 0; ix < segments; ix++) {
      const a = ix + (segments + 1) * iy
      const b = ix + (segments + 1) * (iy + 1)
      const c = (ix + 1) + (segments + 1) * (iy + 1)
      const d = (ix + 1) + (segments + 1) * iy
      
      indices[indexOffset++] = a
      indices[indexOffset++] = b
      indices[indexOffset++] = d
      
      indices[indexOffset++] = b
      indices[indexOffset++] = c
      indices[indexOffset++] = d
    }
  }
  
  // Calcular normales
  computeNormals(positions, indices, normals)
  
  return { positions, normals, uvs, indices }
}

/**
 * Calcular elevación con ruido procedural
 */
function calculateElevation(
  x: number,
  y: number,
  location: { lat: number; lon: number },
  seed: number
): number {
  // Ruido multi-octava
  const octave1 = Math.sin(x * 0.1 + location.lat + seed) * 0.5 +
                  Math.cos(y * 0.1 + location.lon + seed) * 0.5
  
  const octave2 = Math.sin(x * 0.05 + seed) * Math.cos(y * 0.05 + seed) * 1.0
  
  const octave3 = Math.sin(x * 0.2 + seed) * 0.2 +
                  Math.cos(y * 0.2 + seed) * 0.2
  
  const octave4 = Math.sin(x * 0.4 + seed) * 0.1 +
                  Math.cos(y * 0.4 + seed) * 0.1
  
  return octave1 + octave2 + octave3 + octave4
}

/**
 * Calcular normales
 */
function computeNormals(
  positions: Float32Array,
  indices: Uint32Array,
  normals: Float32Array
) {
  // Inicializar normales a 0
  for (let i = 0; i < normals.length; i++) {
    normals[i] = 0
  }
  
  // Calcular normales por triángulo
  for (let i = 0; i < indices.length; i += 3) {
    const i1 = indices[i] * 3
    const i2 = indices[i + 1] * 3
    const i3 = indices[i + 2] * 3
    
    // Vectores del triángulo
    const v1x = positions[i2] - positions[i1]
    const v1y = positions[i2 + 1] - positions[i1 + 1]
    const v1z = positions[i2 + 2] - positions[i1 + 2]
    
    const v2x = positions[i3] - positions[i1]
    const v2y = positions[i3 + 1] - positions[i1 + 1]
    const v2z = positions[i3 + 2] - positions[i1 + 2]
    
    // Producto cruz
    const nx = v1y * v2z - v1z * v2y
    const ny = v1z * v2x - v1x * v2z
    const nz = v1x * v2y - v1y * v2x
    
    // Acumular normales
    normals[i1] += nx
    normals[i1 + 1] += ny
    normals[i1 + 2] += nz
    
    normals[i2] += nx
    normals[i2 + 1] += ny
    normals[i2 + 2] += nz
    
    normals[i3] += nx
    normals[i3 + 1] += ny
    normals[i3 + 2] += nz
  }
  
  // Normalizar
  for (let i = 0; i < normals.length; i += 3) {
    const length = Math.sqrt(
      normals[i] * normals[i] +
      normals[i + 1] * normals[i + 1] +
      normals[i + 2] * normals[i + 2]
    )
    
    if (length > 0) {
      normals[i] /= length
      normals[i + 1] /= length
      normals[i + 2] /= length
    }
  }
}

/**
 * Analizar bioma
 */
function analyzeBiome(
  location: { lat: number; lon: number },
  isDay: boolean
): BiomeData {
  const biome = detectBiome(location.lat, location.lon)
  const skyColor = getSkyColorForBiome(biome.type, isDay)
  const fogColor = getFogColorForBiome(biome.type)
  
  return {
    type: biome.type,
    name: biome.name,
    description: biome.description,
    temperature: biome.temperature,
    humidity: biome.humidity,
    skyColor,
    fogColor
  }
}

/**
 * Generar vegetación procedural
 */
function generateVegetation(
  terrain: TerrainData,
  biome: BiomeData,
  size: number,
  density: number = 0.1
): Array<{ x: number; y: number; z: number; type: string }> {
  const vegetation: Array<{ x: number; y: number; z: number; type: string }> = []
  
  // Densidad basada en bioma
  let biomeDensity = density
  if (biome.type === 'ice') biomeDensity *= 0.1
  if (biome.type === 'desert') biomeDensity *= 0.2
  if (biome.type === 'forest') biomeDensity *= 2.0
  
  const count = Math.floor((size * size) * biomeDensity)
  
  for (let i = 0; i < count; i++) {
    const x = (Math.random() - 0.5) * size
    const z = (Math.random() - 0.5) * size
    const y = getHeightAt(x, z, terrain, size)
    
    // Tipo de vegetación según bioma
    let type = 'tree'
    if (biome.type === 'ice') type = 'ice_rock'
    if (biome.type === 'desert') type = 'cactus'
    if (biome.type === 'volcanic') type = 'dead_tree'
    
    vegetation.push({ x, y, z, type })
  }
  
  return vegetation
}

/**
 * Generar rocas procedurales
 */
function generateRocks(
  terrain: TerrainData,
  biome: BiomeData,
  size: number,
  density: number = 0.05
): Array<{ x: number; y: number; z: number; scale: number }> {
  const rocks: Array<{ x: number; y: number; z: number; scale: number }> = []
  
  const count = Math.floor((size * size) * density)
  
  for (let i = 0; i < count; i++) {
    const x = (Math.random() - 0.5) * size
    const z = (Math.random() - 0.5) * size
    const y = getHeightAt(x, z, terrain, size)
    const scale = 0.5 + Math.random() * 1.5
    
    rocks.push({ x, y, z, scale })
  }
  
  return rocks
}

/**
 * Obtener altura en posición
 */
function getHeightAt(
  x: number,
  z: number,
  terrain: TerrainData,
  size: number
): number {
  // Simplificado - interpolación básica
  return 0
}

/**
 * Generar entorno completo
 */
function generateEnvironment(
  location: { lat: number; lon: number },
  size: number,
  resolution: number,
  isDay: boolean
): EnvironmentData {
  const terrain = generateTerrain(location, size, resolution)
  const biome = analyzeBiome(location, isDay)
  const vegetation = generateVegetation(terrain, biome, size)
  const rocks = generateRocks(terrain, biome, size)
  
  return { terrain, biome, vegetation, rocks }
}

/**
 * Message handler
 */
self.onmessage = (event: MessageEvent<WorkerRequest>) => {
  const request = event.data
  
  try {
    switch (request.type) {
      case 'generateTerrain': {
        const terrain = generateTerrain(
          request.location,
          request.size,
          request.resolution,
          request.seed
        )
        self.postMessage({ type: 'terrainGenerated', data: terrain })
        break
      }
      
      case 'analyzeBiome': {
        const biome = analyzeBiome(request.location, request.isDay)
        self.postMessage({ type: 'biomeAnalyzed', data: biome })
        break
      }
      
      case 'generateEnvironment': {
        const environment = generateEnvironment(
          request.location,
          request.size,
          request.resolution,
          request.isDay
        )
        self.postMessage({ type: 'environmentGenerated', data: environment })
        break
      }
    }
  } catch (error) {
    self.postMessage({ 
      type: 'error', 
      error: error instanceof Error ? error.message : 'Unknown error' 
    })
  }
}

// Export para TypeScript
export {}

import { useRef, useMemo, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { createNoise2D } from 'simplex-noise'

interface ProceduralTerrainEngineProps {
  size?: number
  resolution?: number
  heightScale?: number
  seed?: number
  octaves?: number
  persistence?: number
  lacunarity?: number
  biome?: 'desert' | 'mountain' | 'valley' | 'plains'
}

/**
 * Motor de terreno procedural con Simplex Noise
 * Genera terrenos infinitos sin necesidad de assets
 */
export function ProceduralTerrainEngine({
  size = 100,
  resolution = 128,
  heightScale = 10,
  seed = 12345,
  octaves = 4,
  persistence = 0.5,
  lacunarity = 2.0,
  biome = 'plains'
}: ProceduralTerrainEngineProps) {
  const meshRef = useRef<THREE.Mesh>(null)
  
  // Crear generador de ruido
  const noise2D = useMemo(() => createNoise2D(() => seed), [seed])
  
  // Generar geometría del terreno
  const geometry = useMemo(() => {
    const geo = new THREE.PlaneGeometry(size, size, resolution, resolution)
    const positions = geo.attributes.position.array as Float32Array
    
    // Aplicar ruido multi-octava para altura
    for (let i = 0; i < positions.length; i += 3) {
      const x = positions[i]
      const z = positions[i + 1]
      
      let height = 0
      let amplitude = 1
      let frequency = 1
      let maxValue = 0
      
      // Multi-octave noise (Fractal Brownian Motion)
      for (let octave = 0; octave < octaves; octave++) {
        const sampleX = x * frequency / size
        const sampleZ = z * frequency / size
        
        const noiseValue = noise2D(sampleX, sampleZ)
        height += noiseValue * amplitude
        
        maxValue += amplitude
        amplitude *= persistence
        frequency *= lacunarity
      }
      
      // Normalizar y escalar
      height = (height / maxValue) * heightScale
      
      // Aplicar modificadores de bioma
      height = applyBiomeModifier(height, x, z, size, biome)
      
      positions[i + 2] = height
    }
    
    geo.computeVertexNormals()
    return geo
  }, [size, resolution, heightScale, seed, octaves, persistence, lacunarity, biome, noise2D])
  
  // Material basado en bioma
  const material = useMemo(() => {
    const colors = getBiomeColors(biome)
    
    return new THREE.MeshStandardMaterial({
      color: colors.base,
      roughness: 0.9,
      metalness: 0.0,
      flatShading: false
    })
  }, [biome])
  
  return (
    <mesh 
      ref={meshRef} 
      geometry={geometry} 
      material={material}
      rotation={[-Math.PI / 2, 0, 0]}
      receiveShadow
    />
  )
}

/**
 * Aplicar modificadores específicos de bioma
 */
function applyBiomeModifier(
  height: number, 
  x: number, 
  z: number, 
  size: number, 
  biome: string
): number {
  const distanceFromCenter = Math.sqrt(x * x + z * z) / (size / 2)
  
  switch (biome) {
    case 'mountain':
      // Montañas más pronunciadas en el centro
      return height * (1 + distanceFromCenter * 0.5)
    
    case 'valley':
      // Valle en el centro, montañas en los bordes
      return height * (1 - Math.exp(-distanceFromCenter * 2))
    
    case 'desert':
      // Dunas suaves
      return height * 0.3 + Math.sin(x * 0.1) * 0.5
    
    case 'plains':
    default:
      // Llanuras suaves
      return height * 0.5
  }
}

/**
 * Obtener colores según bioma
 */
function getBiomeColors(biome: string) {
  switch (biome) {
    case 'desert':
      return {
        base: '#d4a574',
        accent: '#c19a6b'
      }
    
    case 'mountain':
      return {
        base: '#8b8680',
        accent: '#ffffff'
      }
    
    case 'valley':
      return {
        base: '#7cb342',
        accent: '#558b2f'
      }
    
    case 'plains':
    default:
      return {
        base: '#8bc34a',
        accent: '#689f38'
      }
  }
}

interface ChunkedTerrainProps {
  chunkSize?: number
  viewDistance?: number
  heightScale?: number
  seed?: number
}

/**
 * Terreno chunkeado para mundos infinitos
 * Genera chunks dinámicamente según posición de cámara
 */
export function ChunkedTerrain({
  chunkSize = 50,
  viewDistance = 150,
  heightScale = 10,
  seed = 12345
}: ChunkedTerrainProps) {
  const chunksRef = useRef<Map<string, THREE.Mesh>>(new Map())
  const groupRef = useRef<THREE.Group>(null)
  const noise2D = useMemo(() => createNoise2D(() => seed), [seed])
  
  // Generar chunk en posición específica
  const generateChunk = (chunkX: number, chunkZ: number) => {
    const chunkId = `${chunkX}_${chunkZ}`
    
    if (chunksRef.current.has(chunkId)) {
      return chunksRef.current.get(chunkId)!
    }
    
    const resolution = 64
    const geometry = new THREE.PlaneGeometry(chunkSize, chunkSize, resolution, resolution)
    const positions = geometry.attributes.position.array as Float32Array
    
    const offsetX = chunkX * chunkSize
    const offsetZ = chunkZ * chunkSize
    
    // Generar altura con ruido
    for (let i = 0; i < positions.length; i += 3) {
      const x = positions[i] + offsetX
      const z = positions[i + 1] + offsetZ
      
      const height = noise2D(x / 50, z / 50) * heightScale
      positions[i + 2] = height
    }
    
    geometry.computeVertexNormals()
    
    const material = new THREE.MeshStandardMaterial({
      color: '#8bc34a',
      roughness: 0.9,
      metalness: 0.0
    })
    
    const mesh = new THREE.Mesh(geometry, material)
    mesh.rotation.x = -Math.PI / 2
    mesh.position.set(offsetX, 0, offsetZ)
    mesh.receiveShadow = true
    
    chunksRef.current.set(chunkId, mesh)
    
    return mesh
  }
  
  useFrame(({ camera }) => {
    if (!groupRef.current) return
    
    const cameraPos = camera.position
    const chunkX = Math.floor(cameraPos.x / chunkSize)
    const chunkZ = Math.floor(cameraPos.z / chunkSize)
    
    const chunksRadius = Math.ceil(viewDistance / chunkSize)
    const activeChunks = new Set<string>()
    
    // Generar chunks visibles
    for (let x = chunkX - chunksRadius; x <= chunkX + chunksRadius; x++) {
      for (let z = chunkZ - chunksRadius; z <= chunkZ + chunksRadius; z++) {
        const chunkId = `${x}_${z}`
        activeChunks.add(chunkId)
        
        const chunk = generateChunk(x, z)
        
        if (!groupRef.current.children.includes(chunk)) {
          groupRef.current.add(chunk)
        }
        
        chunk.visible = true
      }
    }
    
    // Ocultar chunks fuera de rango
    chunksRef.current.forEach((chunk, chunkId) => {
      if (!activeChunks.has(chunkId)) {
        chunk.visible = false
      }
    })
  })
  
  return <group ref={groupRef} />
}

interface TerrainWithBiomesProps {
  size?: number
  resolution?: number
  heightScale?: number
  seed?: number
}

/**
 * Terreno con múltiples biomas mezclados
 */
export function TerrainWithBiomes({
  size = 200,
  resolution = 256,
  heightScale = 15,
  seed = 12345
}: TerrainWithBiomesProps) {
  const meshRef = useRef<THREE.Mesh>(null)
  const noise2D = useMemo(() => createNoise2D(() => seed), [seed])
  const biomeNoise = useMemo(() => createNoise2D(() => seed + 1000), [seed])
  
  const geometry = useMemo(() => {
    const geo = new THREE.PlaneGeometry(size, size, resolution, resolution)
    const positions = geo.attributes.position.array as Float32Array
    const colors = new Float32Array(positions.length)
    
    for (let i = 0; i < positions.length; i += 3) {
      const x = positions[i]
      const z = positions[i + 1]
      
      // Determinar bioma con ruido
      const biomeValue = biomeNoise(x / 100, z / 100)
      
      // Generar altura
      let height = noise2D(x / 50, z / 50) * heightScale
      
      // Modificar según bioma
      let color = new THREE.Color()
      
      if (biomeValue < -0.3) {
        // Desierto
        height *= 0.3
        color.setHex(0xd4a574)
      } else if (biomeValue < 0) {
        // Llanuras
        height *= 0.5
        color.setHex(0x8bc34a)
      } else if (biomeValue < 0.3) {
        // Bosque
        height *= 0.7
        color.setHex(0x558b2f)
      } else {
        // Montañas
        height *= 1.5
        color.setHex(0x8b8680)
      }
      
      positions[i + 2] = height
      
      // Aplicar color
      colors[i] = color.r
      colors[i + 1] = color.g
      colors[i + 2] = color.b
    }
    
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3))
    geo.computeVertexNormals()
    
    return geo
  }, [size, resolution, heightScale, noise2D, biomeNoise])
  
  const material = useMemo(() => 
    new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.9,
      metalness: 0.0
    }),
    []
  )
  
  return (
    <mesh 
      ref={meshRef} 
      geometry={geometry} 
      material={material}
      rotation={[-Math.PI / 2, 0, 0]}
      receiveShadow
    />
  )
}

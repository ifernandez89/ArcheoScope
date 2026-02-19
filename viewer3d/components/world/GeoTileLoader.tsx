import { useRef, useState, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

interface GeoTile {
  id: string
  x: number
  y: number
  zoom: number
  bounds: {
    minLat: number
    maxLat: number
    minLon: number
    maxLon: number
  }
  loaded: boolean
  texture?: THREE.Texture
  heightmap?: Float32Array
}

interface GeoTileLoaderProps {
  center?: { lat: number; lon: number }
  zoom?: number
  tileSize?: number
  viewDistance?: number
  heightScale?: number
  dataSource?: 'static' | 'preprocessed'
}

/**
 * Cargador de tiles geográficos preprocesados
 * Integra datos satelitales y arqueológicos
 */
export function GeoTileLoader({
  center = { lat: 0, lon: 0 },
  zoom = 10,
  tileSize = 50,
  viewDistance = 150,
  heightScale = 10,
  dataSource = 'static'
}: GeoTileLoaderProps) {
  const groupRef = useRef<THREE.Group>(null)
  const tilesRef = useRef<Map<string, THREE.Mesh>>(new Map())
  const [loadedTiles, setLoadedTiles] = useState<Set<string>>(new Set())
  
  // Convertir lat/lon a coordenadas de tile
  const latLonToTile = (lat: number, lon: number, zoom: number) => {
    const x = Math.floor((lon + 180) / 360 * Math.pow(2, zoom))
    const y = Math.floor((1 - Math.log(Math.tan(lat * Math.PI / 180) + 1 / Math.cos(lat * Math.PI / 180)) / Math.PI) / 2 * Math.pow(2, zoom))
    return { x, y }
  }
  
  // Cargar tile desde fuente de datos
  const loadTile = async (tileX: number, tileY: number, zoom: number): Promise<GeoTile> => {
    const tileId = `${zoom}_${tileX}_${tileY}`
    
    // Calcular bounds del tile
    const n = Math.pow(2, zoom)
    const minLon = tileX / n * 360 - 180
    const maxLon = (tileX + 1) / n * 360 - 180
    const minLat = Math.atan(Math.sinh(Math.PI * (1 - 2 * (tileY + 1) / n))) * 180 / Math.PI
    const maxLat = Math.atan(Math.sinh(Math.PI * (1 - 2 * tileY / n))) * 180 / Math.PI
    
    const tile: GeoTile = {
      id: tileId,
      x: tileX,
      y: tileY,
      zoom,
      bounds: { minLat, maxLat, minLon, maxLon },
      loaded: false
    }
    
    try {
      if (dataSource === 'preprocessed') {
        // Cargar desde tiles preprocesados
        const response = await fetch(`/tiles/${zoom}/${tileX}/${tileY}.json`)
        if (response.ok) {
          const data = await response.json()
          tile.heightmap = new Float32Array(data.heightmap)
          tile.loaded = true
        }
      } else {
        // Usar datos estáticos (placeholder)
        tile.loaded = true
      }
    } catch (error) {
      console.warn(`Failed to load tile ${tileId}:`, error)
      tile.loaded = true // Marcar como cargado para evitar reintentos
    }
    
    return tile
  }
  
  // Crear mesh para tile
  const createTileMesh = (tile: GeoTile) => {
    const resolution = 64
    const geometry = new THREE.PlaneGeometry(tileSize, tileSize, resolution, resolution)
    
    // Aplicar heightmap si existe
    if (tile.heightmap) {
      const positions = geometry.attributes.position.array as Float32Array
      const heightmapSize = Math.sqrt(tile.heightmap.length)
      
      for (let i = 0; i < positions.length; i += 3) {
        const x = positions[i]
        const z = positions[i + 1]
        
        // Mapear posición a heightmap
        const u = (x / tileSize + 0.5) * (heightmapSize - 1)
        const v = (z / tileSize + 0.5) * (heightmapSize - 1)
        
        const u0 = Math.floor(u)
        const v0 = Math.floor(v)
        const u1 = Math.min(u0 + 1, heightmapSize - 1)
        const v1 = Math.min(v0 + 1, heightmapSize - 1)
        
        // Interpolación bilinear
        const fu = u - u0
        const fv = v - v0
        
        const h00 = tile.heightmap[v0 * heightmapSize + u0]
        const h10 = tile.heightmap[v0 * heightmapSize + u1]
        const h01 = tile.heightmap[v1 * heightmapSize + u0]
        const h11 = tile.heightmap[v1 * heightmapSize + u1]
        
        const h0 = h00 * (1 - fu) + h10 * fu
        const h1 = h01 * (1 - fu) + h11 * fu
        const height = h0 * (1 - fv) + h1 * fv
        
        positions[i + 2] = height * heightScale
      }
      
      geometry.computeVertexNormals()
    }
    
    const material = new THREE.MeshStandardMaterial({
      color: '#8bc34a',
      roughness: 0.9,
      metalness: 0.0,
      wireframe: false
    })
    
    const mesh = new THREE.Mesh(geometry, material)
    mesh.rotation.x = -Math.PI / 2
    
    // Posicionar tile en el mundo
    const worldX = tile.x * tileSize
    const worldZ = tile.y * tileSize
    mesh.position.set(worldX, 0, worldZ)
    mesh.receiveShadow = true
    
    return mesh
  }
  
  useFrame(async ({ camera }) => {
    if (!groupRef.current) return
    
    // Calcular tile actual de la cámara
    const cameraLat = center.lat // Simplificado, debería calcularse desde posición
    const cameraLon = center.lon
    const centerTile = latLonToTile(cameraLat, cameraLon, zoom)
    
    const tilesRadius = Math.ceil(viewDistance / tileSize)
    const activeTiles = new Set<string>()
    
    // Cargar tiles visibles
    for (let x = centerTile.x - tilesRadius; x <= centerTile.x + tilesRadius; x++) {
      for (let y = centerTile.y - tilesRadius; y <= centerTile.y + tilesRadius; y++) {
        const tileId = `${zoom}_${x}_${y}`
        activeTiles.add(tileId)
        
        if (!tilesRef.current.has(tileId) && !loadedTiles.has(tileId)) {
          // Cargar tile
          setLoadedTiles(prev => new Set(prev).add(tileId))
          
          const tile = await loadTile(x, y, zoom)
          const mesh = createTileMesh(tile)
          
          tilesRef.current.set(tileId, mesh)
          groupRef.current.add(mesh)
        }
        
        // Hacer visible
        const mesh = tilesRef.current.get(tileId)
        if (mesh) {
          mesh.visible = true
        }
      }
    }
    
    // Ocultar tiles fuera de rango
    tilesRef.current.forEach((mesh, tileId) => {
      if (!activeTiles.has(tileId)) {
        mesh.visible = false
      }
    })
  })
  
  return <group ref={groupRef} />
}

/**
 * Overlay de datos arqueológicos sobre tiles
 */
export function ArchaeologicalDataOverlay({
  sites,
  tileSize = 50
}: {
  sites: Array<{ lat: number; lon: number; data: any }>
  tileSize?: number
}) {
  const groupRef = useRef<THREE.Group>(null)
  
  return (
    <group ref={groupRef}>
      {sites.map((site, index) => (
        <mesh key={index} position={[site.lon * tileSize, 0.1, site.lat * tileSize]}>
          <sphereGeometry args={[0.5, 8, 8]} />
          <meshStandardMaterial 
            color="#ff6b6b" 
            emissive="#ff0000"
            emissiveIntensity={0.5}
          />
        </mesh>
      ))}
    </group>
  )
}

/**
 * Sistema de caché para tiles
 */
export class TileCache {
  private cache: Map<string, GeoTile>
  private maxSize: number
  private accessOrder: string[]
  
  constructor(maxSize = 100) {
    this.cache = new Map()
    this.maxSize = maxSize
    this.accessOrder = []
  }
  
  get(tileId: string): GeoTile | undefined {
    const tile = this.cache.get(tileId)
    
    if (tile) {
      // Actualizar orden de acceso (LRU)
      const index = this.accessOrder.indexOf(tileId)
      if (index > -1) {
        this.accessOrder.splice(index, 1)
      }
      this.accessOrder.push(tileId)
    }
    
    return tile
  }
  
  set(tileId: string, tile: GeoTile): void {
    // Eliminar tiles antiguos si excede el límite
    if (this.cache.size >= this.maxSize) {
      const oldestTileId = this.accessOrder.shift()
      if (oldestTileId) {
        this.cache.delete(oldestTileId)
      }
    }
    
    this.cache.set(tileId, tile)
    this.accessOrder.push(tileId)
  }
  
  clear(): void {
    this.cache.clear()
    this.accessOrder = []
  }
  
  getSize(): number {
    return this.cache.size
  }
}

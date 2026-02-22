/**
 * TerrainEngine - Sistema de terreno 3D realista con datos DEM
 * 
 * Integra:
 * - DEM (Digital Elevation Model) para elevación real
 * - Hidrografía (ríos, lagos)
 * - Texturas procedurales según elevación
 * - LOD (Level of Detail) para performance
 * 
 * Fuentes de datos:
 * - SRTM (Shuttle Radar Topography Mission) - 30m resolución
 * - Copernicus GLO-30 - 30m resolución global
 * - USGS 3DEP - Alta resolución para EEUU
 * - Natural Earth - Hidrografía vectorial
 */

import * as THREE from 'three'

export interface DEMData {
  width: number
  height: number
  data: Float32Array  // Valores de elevación en metros
  bounds: {
    minLat: number
    maxLat: number
    minLon: number
    maxLon: number
  }
  resolution: number  // metros por píxel
  minElevation: number
  maxElevation: number
}

export interface HydrographyData {
  rivers: Array<{
    points: Array<[number, number]>  // [lat, lon]
    width: number
    name?: string
  }>
  lakes: Array<{
    polygon: Array<[number, number]>  // [lat, lon]
    name?: string
  }>
}

export interface TerrainConfig {
  segments: number  // Resolución del mesh (default: 256)
  exaggeration: number  // Factor de exageración vertical (default: 1.5)
  enableLOD: boolean  // Activar LOD (default: true)
  enableHydrography: boolean  // Mostrar ríos/lagos (default: true)
  textureResolution: number  // Resolución de texturas (default: 2048)
}

export class TerrainEngine {
  private scene: THREE.Scene
  private terrainMesh: THREE.Mesh | null = null
  private demData: DEMData | null = null
  private hydrographyData: HydrographyData | null = null
  private config: TerrainConfig
  
  // Materiales y texturas
  private terrainMaterial: THREE.MeshStandardMaterial | null = null
  private waterMaterial: THREE.MeshStandardMaterial | null = null
  
  // LOD
  private lodLevels: THREE.LOD | null = null
  
  constructor(scene: THREE.Scene, config: Partial<TerrainConfig> = {}) {
    this.scene = scene
    this.config = {
      segments: config.segments || 256,
      exaggeration: config.exaggeration || 1.5,
      enableLOD: config.enableLOD !== false,
      enableHydrography: config.enableHydrography !== false,
      textureResolution: config.textureResolution || 2048
    }
  }
  
  /**
   * Carga datos DEM desde una fuente
   * 
   * Soporta:
   * - GeoTIFF (via geotiff.js)
   * - Heightmap PNG/JPG
   * - Array de elevaciones
   */
  async loadDEM(source: string | Float32Array, bounds: DEMData['bounds']): Promise<void> {
    if (typeof source === 'string') {
      // Cargar desde URL (GeoTIFF o imagen)
      if (source.endsWith('.tif') || source.endsWith('.tiff')) {
        this.demData = await this.loadGeoTIFF(source, bounds)
      } else {
        this.demData = await this.loadHeightmapImage(source, bounds)
      }
    } else {
      // Datos directos
      const width = Math.sqrt(source.length)
      const height = width
      
      this.demData = {
        width,
        height,
        data: source,
        bounds,
        resolution: this.calculateResolution(bounds, width),
        minElevation: Math.min(...Array.from(source)),
        maxElevation: Math.max(...Array.from(source))
      }
    }
    
    console.log('✅ DEM cargado:', this.demData)
  }
  
  /**
   * Carga heightmap desde imagen PNG/JPG
   */
  private async loadHeightmapImage(url: string, bounds: DEMData['bounds']): Promise<DEMData> {
    return new Promise((resolve, reject) => {
      const img = new Image()
      img.crossOrigin = 'anonymous'
      
      img.onload = () => {
        const canvas = document.createElement('canvas')
        canvas.width = img.width
        canvas.height = img.height
        
        const ctx = canvas.getContext('2d')!
        ctx.drawImage(img, 0, 0)
        
        const imageData = ctx.getImageData(0, 0, img.width, img.height)
        const elevations = new Float32Array(img.width * img.height)
        
        // Convertir valores de píxel (0-255) a elevaciones
        // Asumimos que negro = 0m, blanco = 8848m (Everest)
        for (let i = 0; i < elevations.length; i++) {
          const pixelValue = imageData.data[i * 4] // Canal R
          elevations[i] = (pixelValue / 255) * 8848
        }
        
        resolve({
          width: img.width,
          height: img.height,
          data: elevations,
          bounds,
          resolution: this.calculateResolution(bounds, img.width),
          minElevation: Math.min(...Array.from(elevations)),
          maxElevation: Math.max(...Array.from(elevations))
        })
      }
      
      img.onerror = reject
      img.src = url
    })
  }
  
  /**
   * Carga GeoTIFF (requiere geotiff.js)
   */
  private async loadGeoTIFF(url: string, bounds: DEMData['bounds']): Promise<DEMData> {
    // TODO: Implementar con geotiff.js cuando esté disponible
    console.warn('GeoTIFF loading not implemented yet, falling back to heightmap')
    return this.loadHeightmapImage(url, bounds)
  }
  
  /**
   * Genera mesh de terreno 3D desde DEM
   */
  generateTerrain(): THREE.Mesh | null {
    if (!this.demData) {
      console.error('No DEM data loaded')
      return null
    }
    
    const { width, height, data, minElevation, maxElevation } = this.demData
    const { segments, exaggeration } = this.config
    
    // Crear geometría
    const geometry = new THREE.PlaneGeometry(
      100, // Ancho en unidades Three.js
      100, // Alto en unidades Three.js
      segments - 1,
      segments - 1
    )
    
    // Aplicar elevaciones
    const positions = geometry.attributes.position.array as Float32Array
    
    for (let i = 0; i < positions.length / 3; i++) {
      const x = i % segments
      const y = Math.floor(i / segments)
      
      // Mapear a índice del DEM
      const demX = Math.floor((x / segments) * width)
      const demY = Math.floor((y / segments) * height)
      const demIndex = demY * width + demX
      
      // Obtener elevación y normalizar
      const elevation = data[demIndex] || 0
      const normalizedElevation = (elevation - minElevation) / (maxElevation - minElevation)
      
      // Aplicar a Z con exageración
      positions[i * 3 + 2] = normalizedElevation * 10 * exaggeration
    }
    
    geometry.computeVertexNormals()
    geometry.computeBoundingBox()
    geometry.computeBoundingSphere()
    
    // Crear material con textura procedural
    this.terrainMaterial = this.createTerrainMaterial()
    
    // Crear mesh
    this.terrainMesh = new THREE.Mesh(geometry, this.terrainMaterial)
    this.terrainMesh.rotation.x = -Math.PI / 2
    this.terrainMesh.receiveShadow = true
    this.terrainMesh.castShadow = true
    
    // Agregar a escena
    this.scene.add(this.terrainMesh)
    
    // Generar LOD si está habilitado
    if (this.config.enableLOD) {
      this.generateLOD()
    }
    
    console.log('✅ Terreno generado:', {
      vertices: positions.length / 3,
      segments,
      elevationRange: [minElevation, maxElevation]
    })
    
    return this.terrainMesh
  }
  
  /**
   * Crea material de terreno con texturas procedurales según elevación
   */
  private createTerrainMaterial(): THREE.MeshStandardMaterial {
    const canvas = document.createElement('canvas')
    canvas.width = this.config.textureResolution
    canvas.height = this.config.textureResolution
    const ctx = canvas.getContext('2d')!
    
    // Gradiente de elevación
    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height)
    
    // Colores según elevación (de bajo a alto)
    gradient.addColorStop(0, '#1a5f3a')    // Verde oscuro (bajo)
    gradient.addColorStop(0.3, '#2d8659')  // Verde medio
    gradient.addColorStop(0.5, '#8b7355')  // Marrón (colinas)
    gradient.addColorStop(0.7, '#a0a0a0')  // Gris (montañas)
    gradient.addColorStop(0.9, '#d0d0d0')  // Gris claro (picos)
    gradient.addColorStop(1, '#ffffff')    // Blanco (nieve)
    
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    
    // Agregar ruido para textura
    this.addNoiseToCanvas(ctx, canvas.width, canvas.height, 0.1)
    
    const texture = new THREE.CanvasTexture(canvas)
    texture.wrapS = THREE.RepeatWrapping
    texture.wrapT = THREE.RepeatWrapping
    texture.repeat.set(4, 4)
    
    return new THREE.MeshStandardMaterial({
      map: texture,
      roughness: 0.9,
      metalness: 0.1,
      side: THREE.DoubleSide
    })
  }
  
  /**
   * Agrega ruido a canvas para textura más realista
   */
  private addNoiseToCanvas(ctx: CanvasRenderingContext2D, width: number, height: number, intensity: number): void {
    const imageData = ctx.getImageData(0, 0, width, height)
    const data = imageData.data
    
    for (let i = 0; i < data.length; i += 4) {
      const noise = (Math.random() - 0.5) * intensity * 255
      data[i] += noise     // R
      data[i + 1] += noise // G
      data[i + 2] += noise // B
    }
    
    ctx.putImageData(imageData, 0, 0)
  }
  
  /**
   * Genera niveles LOD para optimización
   */
  private generateLOD(): void {
    if (!this.terrainMesh || !this.demData) return
    
    this.lodLevels = new THREE.LOD()
    
    // Nivel 0: Alta resolución (cerca)
    this.lodLevels.addLevel(this.terrainMesh, 0)
    
    // Nivel 1: Media resolución
    const mediumMesh = this.createLODMesh(this.config.segments / 2)
    this.lodLevels.addLevel(mediumMesh, 50)
    
    // Nivel 2: Baja resolución (lejos)
    const lowMesh = this.createLODMesh(this.config.segments / 4)
    this.lodLevels.addLevel(lowMesh, 100)
    
    this.scene.add(this.lodLevels)
  }
  
  /**
   * Crea mesh LOD con menor resolución
   */
  private createLODMesh(segments: number): THREE.Mesh {
    const geometry = new THREE.PlaneGeometry(100, 100, segments - 1, segments - 1)
    
    // Aplicar elevaciones simplificadas
    if (this.demData) {
      const positions = geometry.attributes.position.array as Float32Array
      const { width, height, data, minElevation, maxElevation } = this.demData
      
      for (let i = 0; i < positions.length / 3; i++) {
        const x = i % segments
        const y = Math.floor(i / segments)
        
        const demX = Math.floor((x / segments) * width)
        const demY = Math.floor((y / segments) * height)
        const demIndex = demY * width + demX
        
        const elevation = data[demIndex] || 0
        const normalizedElevation = (elevation - minElevation) / (maxElevation - minElevation)
        
        positions[i * 3 + 2] = normalizedElevation * 10 * this.config.exaggeration
      }
      
      geometry.computeVertexNormals()
    }
    
    const mesh = new THREE.Mesh(geometry, this.terrainMaterial!)
    mesh.rotation.x = -Math.PI / 2
    mesh.receiveShadow = true
    
    return mesh
  }
  
  /**
   * Carga datos de hidrografía (ríos, lagos)
   */
  async loadHydrography(data: HydrographyData): Promise<void> {
    this.hydrographyData = data
    
    if (this.config.enableHydrography) {
      this.renderHydrography()
    }
  }
  
  /**
   * Renderiza ríos y lagos
   */
  private renderHydrography(): void {
    if (!this.hydrographyData || !this.demData) return
    
    // Renderizar ríos
    this.hydrographyData.rivers.forEach(river => {
      this.renderRiver(river)
    })
    
    // Renderizar lagos
    this.hydrographyData.lakes.forEach(lake => {
      this.renderLake(lake)
    })
  }
  
  /**
   * Renderiza un río
   */
  private renderRiver(river: HydrographyData['rivers'][0]): void {
    const points = river.points.map(([lat, lon]) => {
      const [x, y] = this.latLonToXY(lat, lon)
      const elevation = this.getElevationAt(lat, lon)
      return new THREE.Vector3(x, elevation + 0.1, y) // +0.1 para que esté sobre el terreno
    })
    
    const curve = new THREE.CatmullRomCurve3(points)
    const geometry = new THREE.TubeGeometry(curve, points.length * 2, river.width * 0.01, 8, false)
    
    if (!this.waterMaterial) {
      this.waterMaterial = new THREE.MeshStandardMaterial({
        color: 0x1e90ff,
        roughness: 0.1,
        metalness: 0.8,
        transparent: true,
        opacity: 0.7
      })
    }
    
    const riverMesh = new THREE.Mesh(geometry, this.waterMaterial)
    this.scene.add(riverMesh)
  }
  
  /**
   * Renderiza un lago
   */
  private renderLake(lake: HydrographyData['lakes'][0]): void {
    const shape = new THREE.Shape()
    
    lake.polygon.forEach(([lat, lon], i) => {
      const [x, y] = this.latLonToXY(lat, lon)
      if (i === 0) {
        shape.moveTo(x, y)
      } else {
        shape.lineTo(x, y)
      }
    })
    
    const geometry = new THREE.ShapeGeometry(shape)
    
    if (!this.waterMaterial) {
      this.waterMaterial = new THREE.MeshStandardMaterial({
        color: 0x1e90ff,
        roughness: 0.1,
        metalness: 0.8,
        transparent: true,
        opacity: 0.7
      })
    }
    
    const lakeMesh = new THREE.Mesh(geometry, this.waterMaterial)
    lakeMesh.rotation.x = -Math.PI / 2
    
    // Posicionar a la elevación promedio del lago
    const avgLat = lake.polygon.reduce((sum, [lat]) => sum + lat, 0) / lake.polygon.length
    const avgLon = lake.polygon.reduce((sum, [, lon]) => sum + lon, 0) / lake.polygon.length
    const elevation = this.getElevationAt(avgLat, avgLon)
    lakeMesh.position.y = elevation + 0.1
    
    this.scene.add(lakeMesh)
  }
  
  /**
   * Convierte lat/lon a coordenadas XY del terreno
   */
  private latLonToXY(lat: number, lon: number): [number, number] {
    if (!this.demData) return [0, 0]
    
    const { bounds } = this.demData
    const x = ((lon - bounds.minLon) / (bounds.maxLon - bounds.minLon)) * 100 - 50
    const y = ((lat - bounds.minLat) / (bounds.maxLat - bounds.minLat)) * 100 - 50
    
    return [x, y]
  }
  
  /**
   * Obtiene elevación en una coordenada lat/lon
   */
  private getElevationAt(lat: number, lon: number): number {
    if (!this.demData) return 0
    
    const { width, height, data, bounds, minElevation, maxElevation } = this.demData
    
    const x = Math.floor(((lon - bounds.minLon) / (bounds.maxLon - bounds.minLon)) * width)
    const y = Math.floor(((lat - bounds.minLat) / (bounds.maxLat - bounds.minLat)) * height)
    
    const index = y * width + x
    const elevation = data[index] || 0
    const normalizedElevation = (elevation - minElevation) / (maxElevation - minElevation)
    
    return normalizedElevation * 10 * this.config.exaggeration
  }
  
  /**
   * Calcula resolución en metros por píxel
   */
  private calculateResolution(bounds: DEMData['bounds'], width: number): number {
    const latDiff = bounds.maxLat - bounds.minLat
    const metersPerDegree = 111320 // Aproximado
    return (latDiff * metersPerDegree) / width
  }
  
  /**
   * Actualiza configuración
   */
  updateConfig(config: Partial<TerrainConfig>): void {
    this.config = { ...this.config, ...config }
    
    // Regenerar terreno si es necesario
    if (this.demData) {
      this.dispose()
      this.generateTerrain()
      
      if (this.hydrographyData) {
        this.renderHydrography()
      }
    }
  }
  
  /**
   * Limpia recursos
   */
  dispose(): void {
    if (this.terrainMesh) {
      this.terrainMesh.geometry.dispose()
      if (this.terrainMaterial) {
        this.terrainMaterial.dispose()
      }
      this.scene.remove(this.terrainMesh)
      this.terrainMesh = null
    }
    
    if (this.lodLevels) {
      this.scene.remove(this.lodLevels)
      this.lodLevels = null
    }
    
    if (this.waterMaterial) {
      this.waterMaterial.dispose()
      this.waterMaterial = null
    }
  }
  
  /**
   * Obtiene información del terreno
   */
  getInfo(): object {
    return {
      hasDEM: !!this.demData,
      hasHydrography: !!this.hydrographyData,
      config: this.config,
      demInfo: this.demData ? {
        resolution: `${this.demData.resolution.toFixed(2)}m`,
        elevationRange: `${this.demData.minElevation.toFixed(0)}m - ${this.demData.maxElevation.toFixed(0)}m`,
        size: `${this.demData.width}x${this.demData.height}`
      } : null
    }
  }
}
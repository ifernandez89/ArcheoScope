import { useRef, useState, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import * as THREE from 'three'

interface StreamedAsset {
  id: string
  url: string
  position: THREE.Vector3
  priority: number
  loaded: boolean
  distance: number
  model?: THREE.Object3D
}

interface AssetStreamingProps {
  assets: Array<{
    id: string
    url: string
    position: [number, number, number]
    priority?: number
  }>
  maxConcurrentLoads?: number
  loadDistance?: number
  unloadDistance?: number
}

/**
 * Sistema de streaming de assets 3D
 * Carga/descarga modelos dinámicamente según distancia y prioridad
 */
export function AssetStreaming({
  assets,
  maxConcurrentLoads = 3,
  loadDistance = 100,
  unloadDistance = 200
}: AssetStreamingProps) {
  const groupRef = useRef<THREE.Group>(null)
  const [streamedAssets, setStreamedAssets] = useState<Map<string, StreamedAsset>>(new Map())
  const loadingQueue = useRef<string[]>([])
  const currentlyLoading = useRef<Set<string>>(new Set())
  const { camera } = useThree()
  
  // Inicializar assets
  useEffect(() => {
    const assetsMap = new Map<string, StreamedAsset>()
    
    assets.forEach(asset => {
      assetsMap.set(asset.id, {
        id: asset.id,
        url: asset.url,
        position: new THREE.Vector3(...asset.position),
        priority: asset.priority || 0,
        loaded: false,
        distance: Infinity
      })
    })
    
    setStreamedAssets(assetsMap)
  }, [assets])
  
  // Actualizar distancias y gestionar carga/descarga
  useFrame(() => {
    if (!groupRef.current) return
    
    const cameraPos = camera.position
    const updatedAssets = new Map(streamedAssets)
    
    // Actualizar distancias
    updatedAssets.forEach(asset => {
      asset.distance = cameraPos.distanceTo(asset.position)
    })
    
    // Determinar qué assets cargar
    const assetsToLoad: StreamedAsset[] = []
    const assetsToUnload: StreamedAsset[] = []
    
    updatedAssets.forEach(asset => {
      if (!asset.loaded && asset.distance < loadDistance && !currentlyLoading.current.has(asset.id)) {
        assetsToLoad.push(asset)
      } else if (asset.loaded && asset.distance > unloadDistance) {
        assetsToUnload.push(asset)
      }
    })
    
    // Ordenar por prioridad y distancia
    assetsToLoad.sort((a, b) => {
      if (a.priority !== b.priority) {
        return b.priority - a.priority // Mayor prioridad primero
      }
      return a.distance - b.distance // Más cerca primero
    })
    
    // Agregar a cola de carga
    assetsToLoad.forEach(asset => {
      if (!loadingQueue.current.includes(asset.id)) {
        loadingQueue.current.push(asset.id)
      }
    })
    
    // Descargar assets lejanos
    assetsToUnload.forEach(asset => {
      if (asset.model && groupRef.current) {
        groupRef.current.remove(asset.model)
        asset.model = undefined
        asset.loaded = false
      }
    })
    
    // Procesar cola de carga
    processLoadQueue()
    
    setStreamedAssets(updatedAssets)
  })
  
  // Procesar cola de carga
  const processLoadQueue = async () => {
    while (
      loadingQueue.current.length > 0 && 
      currentlyLoading.current.size < maxConcurrentLoads
    ) {
      const assetId = loadingQueue.current.shift()
      if (!assetId) continue
      
      const asset = streamedAssets.get(assetId)
      if (!asset || asset.loaded) continue
      
      currentlyLoading.current.add(assetId)
      
      try {
        await loadAsset(asset)
      } catch (error) {
        console.error(`Failed to load asset ${assetId}:`, error)
      } finally {
        currentlyLoading.current.delete(assetId)
      }
    }
  }
  
  // Cargar asset individual
  const loadAsset = async (asset: StreamedAsset) => {
    try {
      const gltf = await useGLTF.preload(asset.url)
      const model = gltf.scene.clone()
      
      model.position.copy(asset.position)
      
      if (groupRef.current) {
        groupRef.current.add(model)
      }
      
      asset.model = model
      asset.loaded = true
      
      setStreamedAssets(new Map(streamedAssets))
    } catch (error) {
      throw error
    }
  }
  
  return <group ref={groupRef} />
}

/**
 * Gestor de prioridades de carga
 */
export class LoadPriorityManager {
  private priorities: Map<string, number>
  
  constructor() {
    this.priorities = new Map()
  }
  
  setPriority(assetId: string, priority: number): void {
    this.priorities.set(assetId, priority)
  }
  
  getPriority(assetId: string): number {
    return this.priorities.get(assetId) || 0
  }
  
  increasePriority(assetId: string, amount: number): void {
    const current = this.getPriority(assetId)
    this.setPriority(assetId, current + amount)
  }
  
  decreasePriority(assetId: string, amount: number): void {
    const current = this.getPriority(assetId)
    this.setPriority(assetId, Math.max(0, current - amount))
  }
  
  clear(): void {
    this.priorities.clear()
  }
}

/**
 * Sistema de LOD para modelos cargados
 */
interface LODModelProps {
  url: string
  lodLevels: Array<{
    distance: number
    url: string
  }>
  position: [number, number, number]
}

export function LODModel({ url, lodLevels, position }: LODModelProps) {
  const groupRef = useRef<THREE.Group>(null)
  const [currentLOD, setCurrentLOD] = useState(0)
  const { camera } = useThree()
  
  // Cargar todos los niveles LOD
  const models = lodLevels.map(level => useGLTF(level.url))
  
  useFrame(() => {
    if (!groupRef.current) return
    
    const distance = camera.position.distanceTo(groupRef.current.position)
    
    // Determinar nivel LOD apropiado
    let newLOD = 0
    for (let i = lodLevels.length - 1; i >= 0; i--) {
      if (distance >= lodLevels[i].distance) {
        newLOD = i
        break
      }
    }
    
    if (newLOD !== currentLOD) {
      setCurrentLOD(newLOD)
    }
  })
  
  return (
    <group ref={groupRef} position={position}>
      {models.map((model, index) => (
        <primitive 
          key={index}
          object={model.scene} 
          visible={index === currentLOD}
        />
      ))}
    </group>
  )
}

/**
 * Preloader para assets críticos
 */
export function useAssetPreloader(urls: string[]) {
  const [loaded, setLoaded] = useState(false)
  const [progress, setProgress] = useState(0)
  
  useEffect(() => {
    let loadedCount = 0
    
    const loadAssets = async () => {
      for (const url of urls) {
        try {
          await useGLTF.preload(url)
          loadedCount++
          setProgress(loadedCount / urls.length)
        } catch (error) {
          console.error(`Failed to preload ${url}:`, error)
        }
      }
      
      setLoaded(true)
    }
    
    loadAssets()
  }, [urls])
  
  return { loaded, progress }
}

/**
 * Sistema de caché de modelos
 */
export class ModelCache {
  private cache: Map<string, THREE.Object3D>
  private maxSize: number
  private accessOrder: string[]
  
  constructor(maxSize = 50) {
    this.cache = new Map()
    this.maxSize = maxSize
    this.accessOrder = []
  }
  
  get(url: string): THREE.Object3D | undefined {
    const model = this.cache.get(url)
    
    if (model) {
      // Actualizar orden de acceso (LRU)
      const index = this.accessOrder.indexOf(url)
      if (index > -1) {
        this.accessOrder.splice(index, 1)
      }
      this.accessOrder.push(url)
    }
    
    return model
  }
  
  set(url: string, model: THREE.Object3D): void {
    // Eliminar modelos antiguos si excede el límite
    if (this.cache.size >= this.maxSize) {
      const oldestUrl = this.accessOrder.shift()
      if (oldestUrl) {
        const oldModel = this.cache.get(oldestUrl)
        if (oldModel) {
          // Liberar recursos
          oldModel.traverse(child => {
            if (child instanceof THREE.Mesh) {
              child.geometry.dispose()
              if (Array.isArray(child.material)) {
                child.material.forEach(mat => mat.dispose())
              } else {
                child.material.dispose()
              }
            }
          })
        }
        this.cache.delete(oldestUrl)
      }
    }
    
    this.cache.set(url, model)
    this.accessOrder.push(url)
  }
  
  clear(): void {
    // Liberar todos los recursos
    this.cache.forEach(model => {
      model.traverse(child => {
        if (child instanceof THREE.Mesh) {
          child.geometry.dispose()
          if (Array.isArray(child.material)) {
            child.material.forEach(mat => mat.dispose())
          } else {
            child.material.dispose()
          }
        }
      })
    })
    
    this.cache.clear()
    this.accessOrder = []
  }
  
  getSize(): number {
    return this.cache.size
  }
}

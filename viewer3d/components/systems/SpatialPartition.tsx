import { useRef, useMemo, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

interface Chunk {
  id: string
  bounds: THREE.Box3
  objects: THREE.Object3D[]
  loaded: boolean
  visible: boolean
}

interface SpatialPartitionProps {
  chunkSize?: number
  viewDistance?: number
  children?: React.ReactNode
}

/**
 * Sistema de particionamiento espacial con chunks
 * Carga/descarga regiones dinámicamente según posición de cámara
 */
export function SpatialPartition({ 
  chunkSize = 50, 
  viewDistance = 150,
  children 
}: SpatialPartitionProps) {
  const groupRef = useRef<THREE.Group>(null)
  const { camera } = useThree()
  const chunks = useRef<Map<string, Chunk>>(new Map())
  const activeChunks = useRef<Set<string>>(new Set())

  // Calcular ID de chunk basado en posición
  const getChunkId = (x: number, z: number) => {
    const chunkX = Math.floor(x / chunkSize)
    const chunkZ = Math.floor(z / chunkSize)
    return `${chunkX}_${chunkZ}`
  }

  // Crear chunk si no existe
  const getOrCreateChunk = (chunkId: string) => {
    if (!chunks.current.has(chunkId)) {
      const [chunkX, chunkZ] = chunkId.split('_').map(Number)
      const minX = chunkX * chunkSize
      const minZ = chunkZ * chunkSize
      
      const chunk: Chunk = {
        id: chunkId,
        bounds: new THREE.Box3(
          new THREE.Vector3(minX, -100, minZ),
          new THREE.Vector3(minX + chunkSize, 100, minZ + chunkSize)
        ),
        objects: [],
        loaded: false,
        visible: false
      }
      
      chunks.current.set(chunkId, chunk)
    }
    
    return chunks.current.get(chunkId)!
  }

  // Actualizar chunks visibles según posición de cámara
  useFrame(() => {
    const cameraPos = camera.position
    const currentChunkId = getChunkId(cameraPos.x, cameraPos.z)
    
    // Calcular chunks que deberían estar activos
    const newActiveChunks = new Set<string>()
    const chunksRadius = Math.ceil(viewDistance / chunkSize)
    
    const [centerX, centerZ] = currentChunkId.split('_').map(Number)
    
    for (let x = centerX - chunksRadius; x <= centerX + chunksRadius; x++) {
      for (let z = centerZ - chunksRadius; z <= centerZ + chunksRadius; z++) {
        const chunkId = `${x}_${z}`
        const chunk = getOrCreateChunk(chunkId)
        
        // Verificar si está dentro del radio de visión
        const chunkCenter = chunk.bounds.getCenter(new THREE.Vector3())
        const distance = cameraPos.distanceTo(chunkCenter)
        
        if (distance <= viewDistance) {
          newActiveChunks.add(chunkId)
          
          // Cargar chunk si no está cargado
          if (!chunk.loaded) {
            loadChunk(chunk)
          }
          
          // Hacer visible
          if (!chunk.visible) {
            chunk.visible = true
            chunk.objects.forEach(obj => obj.visible = true)
          }
        }
      }
    }
    
    // Desactivar chunks que ya no están en rango
    activeChunks.current.forEach(chunkId => {
      if (!newActiveChunks.has(chunkId)) {
        const chunk = chunks.current.get(chunkId)
        if (chunk && chunk.visible) {
          chunk.visible = false
          chunk.objects.forEach(obj => obj.visible = false)
        }
      }
    })
    
    activeChunks.current = newActiveChunks
  })

  // Cargar contenido de un chunk
  const loadChunk = (chunk: Chunk) => {
    // Aquí se cargaría el contenido del chunk
    // Por ahora solo marcamos como cargado
    chunk.loaded = true
  }

  return (
    <group ref={groupRef}>
      {children}
    </group>
  )
}

/**
 * Octree simple para frustum culling
 */
class Octree {
  bounds: THREE.Box3
  objects: THREE.Object3D[]
  children: Octree[]
  maxObjects: number
  maxLevels: number
  level: number

  constructor(bounds: THREE.Box3, level = 0, maxObjects = 10, maxLevels = 5) {
    this.bounds = bounds
    this.objects = []
    this.children = []
    this.maxObjects = maxObjects
    this.maxLevels = maxLevels
    this.level = level
  }

  split() {
    const center = this.bounds.getCenter(new THREE.Vector3())
    const size = this.bounds.getSize(new THREE.Vector3())
    const halfSize = size.multiplyScalar(0.5)

    // Crear 8 sub-octantes
    for (let x = 0; x < 2; x++) {
      for (let y = 0; y < 2; y++) {
        for (let z = 0; z < 2; z++) {
          const min = new THREE.Vector3(
            center.x + (x - 0.5) * halfSize.x,
            center.y + (y - 0.5) * halfSize.y,
            center.z + (z - 0.5) * halfSize.z
          )
          const max = min.clone().add(halfSize)
          
          this.children.push(
            new Octree(
              new THREE.Box3(min, max),
              this.level + 1,
              this.maxObjects,
              this.maxLevels
            )
          )
        }
      }
    }
  }

  insert(object: THREE.Object3D) {
    // Si tiene hijos, insertar en el hijo apropiado
    if (this.children.length > 0) {
      const index = this.getIndex(object)
      if (index !== -1) {
        this.children[index].insert(object)
        return
      }
    }

    this.objects.push(object)

    // Dividir si excede el límite
    if (this.objects.length > this.maxObjects && this.level < this.maxLevels) {
      if (this.children.length === 0) {
        this.split()
      }

      // Redistribuir objetos
      let i = 0
      while (i < this.objects.length) {
        const index = this.getIndex(this.objects[i])
        if (index !== -1) {
          this.children[index].insert(this.objects.splice(i, 1)[0])
        } else {
          i++
        }
      }
    }
  }

  getIndex(object: THREE.Object3D): number {
    const center = this.bounds.getCenter(new THREE.Vector3())
    const pos = object.position

    let index = 0
    if (pos.x > center.x) index += 1
    if (pos.y > center.y) index += 2
    if (pos.z > center.z) index += 4

    return index
  }

  retrieve(frustum: THREE.Frustum): THREE.Object3D[] {
    let objects: THREE.Object3D[] = []

    // Si el frustum no intersecta este nodo, retornar vacío
    if (!frustum.intersectsBox(this.bounds)) {
      return objects
    }

    // Agregar objetos de este nodo
    objects = objects.concat(this.objects)

    // Recursivamente buscar en hijos
    if (this.children.length > 0) {
      this.children.forEach(child => {
        objects = objects.concat(child.retrieve(frustum))
      })
    }

    return objects
  }
}

/**
 * Hook para frustum culling con octree
 */
export function useFrustumCulling(objects: THREE.Object3D[], bounds: THREE.Box3) {
  const { camera } = useThree()
  const octree = useMemo(() => {
    const tree = new Octree(bounds)
    objects.forEach(obj => tree.insert(obj))
    return tree
  }, [objects, bounds])

  useFrame(() => {
    const frustum = new THREE.Frustum()
    const projScreenMatrix = new THREE.Matrix4()
    
    projScreenMatrix.multiplyMatrices(
      camera.projectionMatrix,
      camera.matrixWorldInverse
    )
    frustum.setFromProjectionMatrix(projScreenMatrix)

    // Obtener objetos visibles
    const visibleObjects = octree.retrieve(frustum)
    
    // Actualizar visibilidad
    objects.forEach(obj => {
      obj.visible = visibleObjects.includes(obj)
    })
  })
}

import { useRef, useState, useCallback } from 'react'
import { useFrame, useThree, ThreeEvent } from '@react-three/fiber'
import * as THREE from 'three'

interface InteractionSystemProps {
  onTerrainClick?: (point: THREE.Vector3, normal: THREE.Vector3) => void
  onObjectClick?: (object: THREE.Object3D, point: THREE.Vector3) => void
  onObjectHover?: (object: THREE.Object3D | null) => void
  enableTerrainClick?: boolean
  enableObjectClick?: boolean
  enableHover?: boolean
}

/**
 * Sistema de interacción avanzado con raycasting
 * Maneja clicks en terreno, objetos, y hover
 */
export function InteractionSystem({
  onTerrainClick,
  onObjectClick,
  onObjectHover,
  enableTerrainClick = true,
  enableObjectClick = true,
  enableHover = true
}: InteractionSystemProps) {
  const { camera, scene, raycaster, pointer } = useThree()
  const [hoveredObject, setHoveredObject] = useState<THREE.Object3D | null>(null)
  
  // Manejar click
  const handleClick = useCallback((event: MouseEvent) => {
    raycaster.setFromCamera(
      new THREE.Vector2(
        (event.clientX / window.innerWidth) * 2 - 1,
        -(event.clientY / window.innerHeight) * 2 + 1
      ),
      camera
    )
    
    const intersects = raycaster.intersectObjects(scene.children, true)
    
    if (intersects.length > 0) {
      const intersection = intersects[0]
      const object = intersection.object
      const point = intersection.point
      const normal = intersection.face?.normal || new THREE.Vector3(0, 1, 0)
      
      // Determinar si es terreno u objeto
      if (object.userData.isInteractive && enableObjectClick) {
        onObjectClick?.(object, point)
      } else if (enableTerrainClick) {
        onTerrainClick?.(point, normal)
      }
    }
  }, [camera, scene, raycaster, onTerrainClick, onObjectClick, enableTerrainClick, enableObjectClick])
  
  // Manejar hover
  useFrame(() => {
    if (!enableHover) return
    
    raycaster.setFromCamera(pointer, camera)
    const intersects = raycaster.intersectObjects(scene.children, true)
    
    let newHoveredObject: THREE.Object3D | null = null
    
    if (intersects.length > 0) {
      const object = intersects[0].object
      if (object.userData.isInteractive) {
        newHoveredObject = object
      }
    }
    
    if (newHoveredObject !== hoveredObject) {
      setHoveredObject(newHoveredObject)
      onObjectHover?.(newHoveredObject)
      
      // Cambiar cursor
      document.body.style.cursor = newHoveredObject ? 'pointer' : 'default'
    }
  })
  
  // Registrar event listeners
  useFrame(() => {
    window.addEventListener('click', handleClick)
    return () => window.removeEventListener('click', handleClick)
  })
  
  return null
}

/**
 * Marcador de punto clickeado en terreno
 */
export function TerrainMarker({ position }: { position: THREE.Vector3 }) {
  const meshRef = useRef<THREE.Mesh>(null)
  
  useFrame(({ clock }) => {
    if (!meshRef.current) return
    
    // Animación de pulsación
    const scale = 1 + Math.sin(clock.elapsedTime * 3) * 0.2
    meshRef.current.scale.setScalar(scale)
    
    // Rotación
    meshRef.current.rotation.y += 0.02
  })
  
  return (
    <group position={position}>
      <mesh ref={meshRef} position={[0, 0.5, 0]}>
        <coneGeometry args={[0.3, 1, 8]} />
        <meshStandardMaterial 
          color="#ff6b6b"
          emissive="#ff0000"
          emissiveIntensity={0.5}
        />
      </mesh>
      
      {/* Anillo en el suelo */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 0]}>
        <ringGeometry args={[0.4, 0.6, 32]} />
        <meshBasicMaterial 
          color="#ff6b6b"
          transparent
          opacity={0.5}
          side={THREE.DoubleSide}
        />
      </mesh>
    </group>
  )
}

/**
 * Sistema de medición de distancias
 */
export function MeasurementTool() {
  const [points, setPoints] = useState<THREE.Vector3[]>([])
  const [measuring, setMeasuring] = useState(false)
  const lineRef = useRef<THREE.Line>(null)
  
  const handleTerrainClick = useCallback((point: THREE.Vector3) => {
    if (measuring) {
      setPoints(prev => [...prev, point.clone()])
    }
  }, [measuring])
  
  const startMeasuring = () => {
    setPoints([])
    setMeasuring(true)
  }
  
  const stopMeasuring = () => {
    setMeasuring(false)
  }
  
  const clearMeasurements = () => {
    setPoints([])
  }
  
  // Calcular distancia total
  const totalDistance = points.reduce((total, point, index) => {
    if (index === 0) return 0
    return total + point.distanceTo(points[index - 1])
  }, 0)
  
  return (
    <>
      <InteractionSystem 
        onTerrainClick={handleTerrainClick}
        enableTerrainClick={measuring}
      />
      
      {/* Línea de medición */}
      {points.length > 1 && (
        <line ref={lineRef}>
          <bufferGeometry>
            <bufferAttribute
              attach="attributes-position"
              count={points.length}
              array={new Float32Array(points.flatMap(p => [p.x, p.y, p.z]))}
              itemSize={3}
            />
          </bufferGeometry>
          <lineBasicMaterial color="#ffaa00" linewidth={2} />
        </line>
      )}
      
      {/* Marcadores en puntos */}
      {points.map((point, index) => (
        <TerrainMarker key={index} position={point} />
      ))}
      
      {/* UI de control */}
      <div style={{
        position: 'absolute',
        top: 20,
        right: 20,
        background: 'rgba(0,0,0,0.8)',
        padding: '15px',
        borderRadius: '8px',
        color: 'white',
        fontFamily: 'monospace'
      }}>
        <div>Distancia: {totalDistance.toFixed(2)}m</div>
        <div>Puntos: {points.length}</div>
        <button onClick={measuring ? stopMeasuring : startMeasuring}>
          {measuring ? 'Detener' : 'Medir'}
        </button>
        <button onClick={clearMeasurements}>Limpiar</button>
      </div>
    </>
  )
}

/**
 * Sistema de selección de objetos
 */
interface SelectableObjectProps {
  children: React.ReactNode
  onSelect?: () => void
  onDeselect?: () => void
  highlightColor?: string
}

export function SelectableObject({
  children,
  onSelect,
  onDeselect,
  highlightColor = '#ffaa00'
}: SelectableObjectProps) {
  const groupRef = useRef<THREE.Group>(null)
  const [selected, setSelected] = useState(false)
  const outlineRef = useRef<THREE.Mesh>(null)
  
  const handleClick = (event: ThreeEvent<MouseEvent>) => {
    event.stopPropagation()
    setSelected(!selected)
    
    if (!selected) {
      onSelect?.()
    } else {
      onDeselect?.()
    }
  }
  
  useFrame(() => {
    if (!outlineRef.current) return
    
    outlineRef.current.visible = selected
    
    if (selected) {
      outlineRef.current.rotation.y += 0.02
    }
  })
  
  return (
    <group ref={groupRef} onClick={handleClick} userData={{ isInteractive: true }}>
      {children}
      
      {/* Outline de selección */}
      <mesh ref={outlineRef} visible={false}>
        <torusGeometry args={[1.2, 0.05, 16, 32]} />
        <meshBasicMaterial 
          color={highlightColor}
          transparent
          opacity={0.8}
        />
      </mesh>
    </group>
  )
}

/**
 * Tooltip 3D contextual
 */
interface ContextualTooltipProps {
  position: THREE.Vector3
  title: string
  content: string
  visible?: boolean
}

export function ContextualTooltip({
  position,
  title,
  content,
  visible = true
}: ContextualTooltipProps) {
  const { camera } = useThree()
  const groupRef = useRef<THREE.Group>(null)
  
  useFrame(() => {
    if (!groupRef.current) return
    
    // Hacer que el tooltip mire a la cámara
    groupRef.current.lookAt(camera.position)
  })
  
  if (!visible) return null
  
  return (
    <group ref={groupRef} position={position}>
      {/* Panel del tooltip */}
      <mesh position={[0, 1, 0]}>
        <planeGeometry args={[2, 1]} />
        <meshBasicMaterial 
          color="#000000"
          transparent
          opacity={0.8}
          side={THREE.DoubleSide}
        />
      </mesh>
      
      {/* Texto (simplificado, usar Html de drei para texto real) */}
      <mesh position={[0, 1.3, 0.01]}>
        <boxGeometry args={[0.1, 0.1, 0.01]} />
        <meshBasicMaterial color="#ffaa00" />
      </mesh>
    </group>
  )
}

/**
 * Sistema de waypoints/marcadores
 */
export class WaypointSystem {
  private waypoints: Map<string, THREE.Vector3>
  private callbacks: Map<string, () => void>
  
  constructor() {
    this.waypoints = new Map()
    this.callbacks = new Map()
  }
  
  addWaypoint(id: string, position: THREE.Vector3, callback?: () => void): void {
    this.waypoints.set(id, position)
    if (callback) {
      this.callbacks.set(id, callback)
    }
  }
  
  removeWaypoint(id: string): void {
    this.waypoints.delete(id)
    this.callbacks.delete(id)
  }
  
  getWaypoint(id: string): THREE.Vector3 | undefined {
    return this.waypoints.get(id)
  }
  
  getAllWaypoints(): Array<{ id: string; position: THREE.Vector3 }> {
    return Array.from(this.waypoints.entries()).map(([id, position]) => ({
      id,
      position
    }))
  }
  
  triggerWaypoint(id: string): void {
    const callback = this.callbacks.get(id)
    if (callback) {
      callback()
    }
  }
  
  checkProximity(position: THREE.Vector3, radius: number): string[] {
    const nearby: string[] = []
    
    this.waypoints.forEach((waypointPos, id) => {
      if (position.distanceTo(waypointPos) <= radius) {
        nearby.push(id)
      }
    })
    
    return nearby
  }
  
  clear(): void {
    this.waypoints.clear()
    this.callbacks.clear()
  }
}

/**
 * Hook para sistema de waypoints
 */
export function useWaypoints() {
  const systemRef = useRef(new WaypointSystem())
  
  return {
    addWaypoint: systemRef.current.addWaypoint.bind(systemRef.current),
    removeWaypoint: systemRef.current.removeWaypoint.bind(systemRef.current),
    getWaypoint: systemRef.current.getWaypoint.bind(systemRef.current),
    getAllWaypoints: systemRef.current.getAllWaypoints.bind(systemRef.current),
    triggerWaypoint: systemRef.current.triggerWaypoint.bind(systemRef.current),
    checkProximity: systemRef.current.checkProximity.bind(systemRef.current),
    clear: systemRef.current.clear.bind(systemRef.current)
  }
}

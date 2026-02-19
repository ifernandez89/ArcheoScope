'use client'

import { useRef, useEffect, Children, ReactNode } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'
import { WorldCore } from '@/engines/WorldCore'

interface SmartLODProps {
  id: string
  position: [number, number, number]
  children: React.ReactNode[]
  distances?: number[]
  autoRegister?: boolean
}

/**
 * SmartLOD - Sistema LOD integrado con WorldCore
 * 
 * Uso:
 * <SmartLOD id="tree_001" position={[0, 0, 0]} distances={[50, 150, 300]}>
 *   <HighDetailTree />   // LOD 0 - cerca
 *   <MediumDetailTree /> // LOD 1 - medio
 *   <LowDetailTree />    // LOD 2 - lejos
 *   <TreeBillboard />    // LOD 3 - muy lejos
 * </SmartLOD>
 */
export function SmartLOD({ 
  id, 
  position, 
  children, 
  distances = [50, 150, 300, 500],
  autoRegister = true
}: SmartLODProps) {
  const groupRef = useRef<THREE.Group>(null)
  const { camera } = useThree()
  const currentLevel = useRef(0)
  const childRefs = useRef<(THREE.Object3D | null)[]>([])

  // Registrar en WorldCore
  useEffect(() => {
    if (!autoRegister || !groupRef.current) return

    const pos = new THREE.Vector3(...position)
    const levels = childRefs.current.filter(Boolean) as THREE.Object3D[]
    
    WorldCore.LOD.register(id, pos, levels)

    return () => {
      WorldCore.LOD.unregister(id)
    }
  }, [id, position, autoRegister])

  useFrame(() => {
    if (!groupRef.current) return

    const distance = camera.position.distanceTo(groupRef.current.position)
    
    // Calcular nivel LOD
    let newLevel = distances.length
    for (let i = 0; i < distances.length; i++) {
      if (distance < distances[i]) {
        newLevel = i
        break
      }
    }

    // Cambiar nivel si es necesario
    if (newLevel !== currentLevel.current) {
      // Ocultar nivel anterior
      if (childRefs.current[currentLevel.current]) {
        childRefs.current[currentLevel.current]!.visible = false
      }

      // Mostrar nuevo nivel
      if (childRefs.current[newLevel]) {
        childRefs.current[newLevel]!.visible = true
      }

      currentLevel.current = newLevel
    }
  })

  return (
    <group ref={groupRef} position={position}>
      {Children.map(children, (child, index) => (
        <group
          ref={(ref) => {
            childRefs.current[index] = ref
          }}
          visible={index === 0}
        >
          {child}
        </group>
      ))}
    </group>
  )
}

/**
 * TreeLOD - Ejemplo de árbol con 4 niveles de detalle
 */
export function TreeLOD({ position, id }: { position: [number, number, number]; id: string }) {
  return (
    <SmartLOD id={id} position={position} distances={[30, 80, 200, 400]}>
      {/* LOD 0 - Alta calidad (< 30m) */}
      <HighDetailTree />
      
      {/* LOD 1 - Media calidad (30-80m) */}
      <MediumDetailTree />
      
      {/* LOD 2 - Baja calidad (80-200m) */}
      <LowDetailTree />
      
      {/* LOD 3 - Billboard (200-400m) */}
      <TreeBillboard />
    </SmartLOD>
  )
}

// LOD 0 - Alta calidad: Geometría completa con ramas
function HighDetailTree() {
  return (
    <group>
      {/* Tronco detallado */}
      <mesh position={[0, 2, 0]} castShadow>
        <cylinderGeometry args={[0.3, 0.4, 4, 16]} />
        <meshStandardMaterial color="#4a3520" roughness={0.9} />
      </mesh>
      
      {/* Copa con múltiples esferas */}
      <mesh position={[0, 5, 0]} castShadow>
        <sphereGeometry args={[2, 16, 16]} />
        <meshStandardMaterial color="#2d5016" roughness={0.8} />
      </mesh>
      <mesh position={[0.8, 5.5, 0]} castShadow>
        <sphereGeometry args={[1.2, 16, 16]} />
        <meshStandardMaterial color="#2d5016" roughness={0.8} />
      </mesh>
      <mesh position={[-0.8, 5.5, 0]} castShadow>
        <sphereGeometry args={[1.2, 16, 16]} />
        <meshStandardMaterial color="#2d5016" roughness={0.8} />
      </mesh>
      
      {/* Ramas */}
      <mesh position={[1, 3, 0]} rotation={[0, 0, Math.PI / 4]}>
        <cylinderGeometry args={[0.1, 0.15, 1.5, 8]} />
        <meshStandardMaterial color="#4a3520" />
      </mesh>
      <mesh position={[-1, 3.5, 0]} rotation={[0, 0, -Math.PI / 4]}>
        <cylinderGeometry args={[0.1, 0.15, 1.5, 8]} />
        <meshStandardMaterial color="#4a3520" />
      </mesh>
    </group>
  )
}

// LOD 1 - Media calidad: Geometría simplificada
function MediumDetailTree() {
  return (
    <group>
      {/* Tronco simplificado */}
      <mesh position={[0, 2, 0]}>
        <cylinderGeometry args={[0.3, 0.4, 4, 8]} />
        <meshStandardMaterial color="#4a3520" roughness={0.9} />
      </mesh>
      
      {/* Copa simple */}
      <mesh position={[0, 5, 0]}>
        <sphereGeometry args={[2, 8, 8]} />
        <meshStandardMaterial color="#2d5016" roughness={0.8} />
      </mesh>
    </group>
  )
}

// LOD 2 - Baja calidad: Geometría muy simple
function LowDetailTree() {
  return (
    <group>
      {/* Tronco muy simple */}
      <mesh position={[0, 2, 0]}>
        <cylinderGeometry args={[0.3, 0.4, 4, 4]} />
        <meshStandardMaterial color="#4a3520" />
      </mesh>
      
      {/* Copa muy simple */}
      <mesh position={[0, 5, 0]}>
        <coneGeometry args={[2, 3, 4]} />
        <meshStandardMaterial color="#2d5016" />
      </mesh>
    </group>
  )
}

// LOD 3 - Billboard: Sprite 2D
function TreeBillboard() {
  const meshRef = useRef<THREE.Mesh>(null)
  const { camera } = useThree()

  useFrame(() => {
    if (meshRef.current) {
      // Billboard siempre mira a la cámara
      meshRef.current.lookAt(camera.position)
    }
  })

  return (
    <mesh ref={meshRef} position={[0, 3, 0]}>
      <planeGeometry args={[3, 6]} />
      <meshBasicMaterial 
        color="#2d5016" 
        transparent 
        opacity={0.8}
        side={THREE.DoubleSide}
      />
    </mesh>
  )
}

/**
 * RockLOD - Ejemplo de roca con 3 niveles
 */
export function RockLOD({ position, id }: { position: [number, number, number]; id: string }) {
  return (
    <SmartLOD id={id} position={position} distances={[40, 120, 300]}>
      {/* LOD 0 - Alta calidad */}
      <mesh castShadow>
        <dodecahedronGeometry args={[1, 2]} />
        <meshStandardMaterial color="#6b6b6b" roughness={0.95} metalness={0.1} />
      </mesh>
      
      {/* LOD 1 - Media calidad */}
      <mesh>
        <dodecahedronGeometry args={[1, 1]} />
        <meshStandardMaterial color="#6b6b6b" roughness={0.95} />
      </mesh>
      
      {/* LOD 2 - Baja calidad */}
      <mesh>
        <boxGeometry args={[1.5, 1.5, 1.5]} />
        <meshStandardMaterial color="#6b6b6b" />
      </mesh>
    </SmartLOD>
  )
}

/**
 * BuildingLOD - Ejemplo de edificio con 4 niveles
 */
export function BuildingLOD({ position, id }: { position: [number, number, number]; id: string }) {
  return (
    <SmartLOD id={id} position={position} distances={[50, 150, 400, 800]}>
      {/* LOD 0 - Alta calidad: Con ventanas y detalles */}
      <group>
        <mesh position={[0, 5, 0]} castShadow>
          <boxGeometry args={[4, 10, 4]} />
          <meshStandardMaterial color="#cccccc" />
        </mesh>
        {/* Ventanas */}
        {Array.from({ length: 8 }).map((_, i) => (
          <mesh key={i} position={[2.01, 2 + i, 0]}>
            <planeGeometry args={[0.5, 0.5]} />
            <meshStandardMaterial color="#1a1a1a" />
          </mesh>
        ))}
      </group>
      
      {/* LOD 1 - Media calidad: Sin ventanas */}
      <mesh position={[0, 5, 0]}>
        <boxGeometry args={[4, 10, 4]} />
        <meshStandardMaterial color="#cccccc" />
      </mesh>
      
      {/* LOD 2 - Baja calidad: Geometría simplificada */}
      <mesh position={[0, 5, 0]}>
        <boxGeometry args={[4, 10, 4, 1, 1, 1]} />
        <meshStandardMaterial color="#aaaaaa" />
      </mesh>
      
      {/* LOD 3 - Billboard */}
      <mesh position={[0, 5, 0]}>
        <planeGeometry args={[4, 10]} />
        <meshBasicMaterial color="#cccccc" side={THREE.DoubleSide} />
      </mesh>
    </SmartLOD>
  )
}

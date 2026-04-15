'use client'

import { useRef, useState, useMemo } from 'react'
import { useGLTF } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

interface DroppableItemProps {
  modelPath: string
  position: [number, number, number]
  onCollect?: () => void
  scale?: number
  floatHeight?: number // Altura de flotación sobre el suelo
  glowColor?: string
  itemName?: string
}

/**
 * Componente genérico para items droppeables en el mundo
 * - Flota sobre el suelo para ser visible
 * - Rotación automática
 * - Glow y outline al hacer hover
 * - Se puede recoger infinitamente (no desaparece al recoger)
 */
export default function DroppableItem({
  modelPath,
  position,
  onCollect,
  scale = 1.5,
  floatHeight = 1.5,
  glowColor = '#ffaa00',
  itemName = 'Item'
}: DroppableItemProps) {
  const { scene } = useGLTF(getAssetPath(modelPath))
  const groupRef = useRef<THREE.Group>(null)
  const [hovered, setHovered] = useState(false)

  // Calcular Y correcto sobre el piso + flotación
  const { finalScale, yOffset } = useMemo(() => {
    const box = new THREE.Box3().setFromObject(scene)
    const size = box.getSize(new THREE.Vector3())
    const sc = scale / size.y
    const yo = -box.min.y * sc + floatHeight // Elevar sobre el suelo
    return { finalScale: sc, yOffset: yo }
  }, [scene, scale, floatHeight])

  // Clonar para independencia
  const cloned = useMemo(() => scene.clone(true), [scene])

  useFrame(({ clock }) => {
    if (!groupRef.current) return
    // Rotación continua
    groupRef.current.rotation.y = clock.elapsedTime * 1.2
    // Flotación suave arriba/abajo
    groupRef.current.position.y = position[1] + yOffset + Math.sin(clock.elapsedTime * 2) * 0.15
  })

  const handleClick = (e: any) => {
    e.stopPropagation()
    if (onCollect) {
      onCollect()
      console.log(`✨ ${itemName} recogido!`)
    }
  }

  return (
    <group
      ref={groupRef}
      position={[position[0], position[1] + yOffset, position[2]]}
      scale={finalScale}
      onClick={handleClick}
      onPointerOver={(e) => {
        e.stopPropagation()
        setHovered(true)
        document.body.style.cursor = 'pointer'
      }}
      onPointerOut={(e) => {
        e.stopPropagation()
        setHovered(false)
        document.body.style.cursor = 'default'
      }}
    >
      <primitive object={cloned} />
      
      {/* Glow */}
      <pointLight 
        color={glowColor} 
        intensity={hovered ? 4 : 2} 
        distance={10} 
      />
      
      {/* Outline hover */}
      {hovered && (
        <mesh>
          <sphereGeometry args={[1.2, 16, 16]} />
          <meshBasicMaterial 
            color={glowColor} 
            wireframe 
            transparent 
            opacity={0.4} 
          />
        </mesh>
      )}
      
      {/* Partículas flotantes alrededor */}
      <pointLight 
        position={[0, 2, 0]} 
        color={glowColor} 
        intensity={1} 
        distance={5} 
      />
    </group>
  )
}

'use client'

import { useRef, useState, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

interface InventoryItemProps {
  modelPath: string
  itemName: string
  onDrop?: () => void
  show: boolean
  dropDisabled?: boolean
}

function RotatingModel({ modelPath, scale = 1 }: { modelPath: string, scale?: number }) {
  const { scene } = useGLTF(getAssetPath(modelPath))
  const groupRef = useRef<THREE.Group>(null)

  // Configuración específica por modelo — evita problemas de bounding box
  const config = useMemo(() => {
    if (modelPath.includes('escab'))         return { sc: 8,    rx: Math.PI/2, ry: 0,          rz: Math.PI,  cy: 0 }
    if (modelPath.includes('tonatiuh'))      return { sc: 0.015, rx: -Math.PI/6, ry: Math.PI/4, rz: 0,        cy: 0 }
    if (modelPath.includes('magna_bowl'))    return { sc: 1.2,  rx: 0,         ry: 0,          rz: 0,        cy: 0 }
    if (modelPath.includes('crystal-skull')) return { sc: 1.0,  rx: 0,         ry: 0,          rz: 0,        cy: 0 }
    if (modelPath.includes('maiz'))          return { sc: 0.8,  rx: 0,         ry: 0,          rz: 0,        cy: 0 }
    if (modelPath.includes('rock_blender'))  return { sc: 3.0,  rx: 0,         ry: 0,          rz: 0,        cy: 0 }
    // Fallback: auto-scale desde bounding box
    const box = new THREE.Box3().setFromObject(scene)
    const size = box.getSize(new THREE.Vector3())
    const maxDim = Math.max(size.x, size.y, size.z)
    return { sc: maxDim > 0 ? 1.8 / maxDim : 1, rx: 0, ry: 0, rz: 0, cy: 0 }
  }, [scene, modelPath])

  const clonedScene = useMemo(() => scene.clone(true), [scene])

  useFrame((_, delta) => {
    if (groupRef.current) groupRef.current.rotation.y += delta * 1.5
  })

  return (
    <group ref={groupRef} rotation={[config.rx, config.ry, config.rz]}>
      <primitive object={clonedScene} scale={scale * config.sc} />
    </group>
  )
}

export default function InventoryItem({ modelPath, itemName, onDrop, show, dropDisabled }: InventoryItemProps) {
  const [isHovered, setIsHovered] = useState(false)
  
  if (!show) return null
  
  return (
    <div
      style={{
        position: 'relative',
        width: '80px',
        height: '80px',
        background: isHovered 
          ? (dropDisabled ? 'rgba(150, 0, 0, 0.3)' : 'rgba(255, 215, 0, 0.3)') 
          : 'rgba(0, 0, 0, 0.7)',
        borderRadius: '12px',
        border: dropDisabled && isHovered 
          ? '3px solid #ff4444' 
          : (isHovered ? '3px solid #ffd700' : '2px solid #ffd700'),
        overflow: 'visible',
        cursor: dropDisabled ? 'not-allowed' : 'pointer',
        zIndex: 1000,
        transition: 'all 0.2s ease',
        transform: isHovered ? 'scale(1.1)' : 'scale(1)',
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={() => {
        if (!dropDisabled && onDrop) onDrop()
      }}
    >
      <Canvas
        key={modelPath}
        camera={{ position: [0, 0.5, 3], fov: 50 }}
        style={{ background: 'transparent' }}
      >
        <ambientLight intensity={2.5} />
        <directionalLight position={[2, 2, 2]} intensity={3} />
        <directionalLight position={[-2, 1, -2]} intensity={1.5} />
        <directionalLight position={[0, -2, 2]} intensity={1} />
        <pointLight position={[0, 3, 2]} intensity={2} color="#ffffff" />
        <RotatingModel modelPath={modelPath} scale={0.8} />
      </Canvas>
      
      {/* Tooltip cuando hover */}
      {isHovered && (
        <div
          style={{
            position: 'absolute',
            top: '-35px',
            left: '50%',
            transform: 'translateX(-50%)',
            background: dropDisabled ? 'rgba(50, 0, 0, 0.95)' : 'rgba(0, 0, 0, 0.95)',
            color: dropDisabled ? '#ff4444' : '#ffd700',
            padding: '8px 16px',
            borderRadius: '8px',
            fontSize: '14px',
            fontWeight: 'bold',
            fontFamily: '"Cinzel", serif',
            whiteSpace: 'nowrap',
            border: dropDisabled ? '2px solid #ff4444' : '2px solid #ffd700',
            boxShadow: dropDisabled ? '0 0 10px rgba(255, 0, 0, 0.5)' : '0 0 10px rgba(255, 215, 0, 0.5)',
            animation: 'pulse 1s infinite',
          }}
        >
          {dropDisabled ? '🚫 Solo en Tierra' : '🌱 Soltar'}
        </div>
      )}
      
      {/* Nombre del item */}
      <div
        style={{
          position: 'absolute',
          bottom: '2px',
          left: '0',
          right: '0',
          textAlign: 'center',
          color: '#ffd700',
          fontSize: '10px',
          fontFamily: '"Cinzel", serif',
          textShadow: '0 0 3px black',
        }}
      >
        {itemName}
      </div>
      
      <style jsx>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; transform: translateX(-50%) scale(1); }
          50% { opacity: 0.8; transform: translateX(-50%) scale(1.05); }
        }
      `}</style>
    </div>
  )
}

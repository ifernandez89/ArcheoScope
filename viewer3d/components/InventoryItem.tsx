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
}

function RotatingModel({ modelPath, scale = 1 }: { modelPath: string, scale?: number }) {
  const { scene } = useGLTF(getAssetPath(modelPath))
  const groupRef = useRef<THREE.Group>(null)
  
  // Clonar UNA sola vez con useMemo
  const clonedScene = useMemo(() => scene.clone(true), [scene])
  
  useFrame((state, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += delta * 1.5
    }
  })
  
  return (
    <group ref={groupRef}>
      <primitive object={clonedScene} scale={scale} />
    </group>
  )
}

export default function InventoryItem({ modelPath, itemName, onDrop, show }: InventoryItemProps) {
  const [isHovered, setIsHovered] = useState(false)
  
  if (!show) return null
  
  return (
    <div
      style={{
        position: 'fixed',
        top: '280px',
        right: '20px',
        width: '80px',
        height: '80px',
        background: isHovered ? 'rgba(255, 215, 0, 0.3)' : 'rgba(0, 0, 0, 0.7)',
        borderRadius: '12px',
        border: isHovered ? '3px solid #ffd700' : '2px solid #ffd700',
        overflow: 'visible',
        cursor: 'pointer',
        zIndex: 1000,
        transition: 'all 0.2s ease',
        transform: isHovered ? 'scale(1.1)' : 'scale(1)',
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={onDrop}
    >
      <Canvas
        camera={{ position: [0, 0, 3], fov: 50 }}
        style={{ background: 'transparent' }}
      >
        <ambientLight intensity={0.8} />
        <directionalLight position={[2, 2, 2]} intensity={1} />
        <RotatingModel modelPath={modelPath} scale={0.8} />
      </Canvas>
      
      {/* Tooltip "Soltar" cuando hover */}
      {isHovered && (
        <div
          style={{
            position: 'absolute',
            top: '-35px',
            left: '50%',
            transform: 'translateX(-50%)',
            background: 'rgba(0, 0, 0, 0.95)',
            color: '#ffd700',
            padding: '8px 16px',
            borderRadius: '8px',
            fontSize: '14px',
            fontWeight: 'bold',
            fontFamily: '"Cinzel", serif',
            whiteSpace: 'nowrap',
            border: '2px solid #ffd700',
            boxShadow: '0 0 10px rgba(255, 215, 0, 0.5)',
            animation: 'pulse 1s infinite',
          }}
        >
          🌱 Soltar
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

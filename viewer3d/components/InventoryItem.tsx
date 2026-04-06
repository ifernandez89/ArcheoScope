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
  
  // Clonar y centrar automáticamente
  const { clonedScene, autoScale } = useMemo(() => {
    const clone = scene.clone(true)
    if (modelPath.includes('escab')) {
      clone.rotation.x = Math.PI / 2
      clone.rotation.z = Math.PI
    }
    if (modelPath.includes('tonatiuh')) {
      // Tonatiuh: rotar para verlo de frente
      clone.rotation.y = Math.PI
    }
    // Auto-centrar: calcular bounding box y mover al origen
    const box = new THREE.Box3().setFromObject(clone)
    const center = box.getCenter(new THREE.Vector3())
    const size = box.getSize(new THREE.Vector3())
    clone.position.sub(center) // centrar en origen
    // Auto-escalar para que quepa en la ventana (max dimension = 2 unidades)
    const maxDim = Math.max(size.x, size.y, size.z)
    const autoSc = maxDim > 0 ? 2 / maxDim : 1
    return { clonedScene: clone, autoScale: autoSc }
  }, [scene, modelPath])
  
  useFrame((state, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += delta * 1.5
    }
  })
  
  const finalScale = scale * autoScale
  
  return (
    <group ref={groupRef}>
      <primitive object={clonedScene} scale={finalScale} />
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
        camera={{ position: [0, 0, 3], fov: 50 }}
        style={{ background: 'transparent' }}
      >
        <ambientLight intensity={1.5} />
        <directionalLight position={[2, 2, 2]} intensity={2} />
        <directionalLight position={[-2, 1, -2]} intensity={1} />
        <pointLight position={[0, 3, 2]} intensity={1.5} color="#ffffff" />
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

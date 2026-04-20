'use client'

import { useRef, useState, useMemo, useEffect, Suspense } from 'react'
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
  const clonedScene = useMemo(() => scene.clone(true), [scene])

  useFrame((_, delta) => {
    if (groupRef.current) groupRef.current.rotation.y += delta * 1.5
  })

  return (
    <group ref={groupRef} scale={scale}>
      <primitive object={clonedScene} />
    </group>
  )
}

export default function InventoryItem({ modelPath, itemName, onDrop, show, dropDisabled }: InventoryItemProps) {
  const [isHovered, setIsHovered] = useState(false)
  const [mountKey, setMountKey] = useState(0)
  const prevShowRef = useRef(show)

  // Forzar remontaje del Canvas cuando show cambia de false→true
  useEffect(() => {
    if (show && !prevShowRef.current) {
      setMountKey(k => k + 1)
    }
    prevShowRef.current = show
  }, [show])

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
        key={`inv-${modelPath}-${mountKey}`}
        camera={{ position: [0, 0, 2.5], fov: 45 }}
        style={{ background: 'transparent' }}
        frameloop="always"
      >
        <ambientLight intensity={2.5} />
        <directionalLight position={[2, 2, 2]} intensity={3} />
        <directionalLight position={[-2, 1, -2]} intensity={1.5} />
        <directionalLight position={[0, -2, 2]} intensity={1} />
        <pointLight position={[0, 3, 2]} intensity={2} color="#ffffff" />
        <Suspense fallback={null}>
          <RotatingModel
            modelPath={modelPath}
            scale={modelPath.includes('fuente_magna') ? 0.55 : 0.8}
          />
        </Suspense>
      </Canvas>

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
          }}
        >
          {dropDisabled ? '🚫 Bloqueado' : '🌱 Soltar'}
        </div>
      )}

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
    </div>
  )
}

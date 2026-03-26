'use client'

import { Canvas } from '@react-three/fiber'
import { OrbitControls, useGLTF } from '@react-three/drei'
import { Suspense } from 'react'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

interface ShipPreviewProps {
  shipModel: string
}

function ShipModel({ modelPath }: { modelPath: string }) {
  const { scene } = useGLTF(getAssetPath(modelPath))
  
  return (
    <primitive 
      object={scene} 
      scale={2}
      rotation={[0, Math.PI, 0]}
    />
  )
}

export default function ShipPreview({ shipModel }: ShipPreviewProps) {
  return (
    <div style={{
      width: '100%',
      height: '100%',
      background: '#0a0a0a',
      border: '2px solid #ffffff',
      borderRadius: '8px',
      overflow: 'hidden'
    }}>
      <Canvas
        camera={{ position: [0, 2, 8], fov: 50 }}
        style={{ background: '#0a0a0a' }}
      >
        {/* Luz ambiente más intensa */}
        <ambientLight intensity={1.6} />
        
        {/* Luces direccionales principales */}
        <directionalLight position={[10, 10, 10]} intensity={3.0} color="#ffffff" />
        <directionalLight position={[-10, 10, -10]} intensity={2.4} color="#ffffff" />
        <directionalLight position={[0, -10, 0]} intensity={1.6} color="#ffffff" />
        
        {/* Luces de relleno para detalles */}
        <pointLight position={[5, 0, 5]} intensity={2.0} color="#4a9eff" />
        <pointLight position={[-5, 0, -5]} intensity={2.0} color="#4a9eff" />
        <pointLight position={[0, 5, 0]} intensity={1.6} color="#ffffff" />
        
        {/* Luz de acento desde abajo */}
        <spotLight 
          position={[0, -5, 0]} 
          intensity={3.0} 
          angle={Math.PI / 3}
          penumbra={0.5}
          color="#6ab7ff"
        />
        
        <Suspense fallback={null}>
          <ShipModel modelPath={shipModel} />
        </Suspense>
        
        <OrbitControls 
          enableZoom={true}
          enablePan={false}
          minDistance={4}
          maxDistance={15}
          autoRotate
          autoRotateSpeed={2}
        />
      </Canvas>
    </div>
  )
}

'use client'

import { Canvas } from '@react-three/fiber'
import { OrbitControls, useGLTF } from '@react-three/drei'
import { Suspense, useMemo, useEffect } from 'react'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

interface ShipPreviewProps {
  shipModel: string
}

function ShipModel({ modelPath }: { modelPath: string }) {
  const { scene } = useGLTF(getAssetPath(modelPath))
  const cloned = useMemo(() => scene.clone(true), [scene])
  return (
    <primitive 
      object={cloned} 
      scale={2}
      rotation={[0, Math.PI, 0]}
    />
  )
}

export default function ShipPreview({ shipModel }: ShipPreviewProps) {
  // Configurar Draco y precargar naves en el cliente (donde window está disponible)
  useEffect(() => {
    useGLTF.setDecoderPath(getAssetPath('/draco/'))
    ;[1,2,3,4,5].forEach(n => useGLTF.preload(getAssetPath(`/ufo_${n}.glb`)))
  }, [])

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
        key={shipModel}
        camera={{ position: [0, 2, 8], fov: 50 }}
        style={{ background: '#0a0a0a' }}
      >
        <ambientLight intensity={1.6} />
        <directionalLight position={[10, 10, 10]} intensity={3.0} color="#ffffff" />
        <directionalLight position={[-10, 10, -10]} intensity={2.4} color="#ffffff" />
        <directionalLight position={[0, -10, 0]} intensity={1.6} color="#ffffff" />
        <pointLight position={[5, 0, 5]} intensity={2.0} color="#4a9eff" />
        <pointLight position={[-5, 0, -5]} intensity={2.0} color="#4a9eff" />
        <pointLight position={[0, 5, 0]} intensity={1.6} color="#ffffff" />
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

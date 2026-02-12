'use client'

import { Canvas } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera, Environment, ContactShadows, Grid } from '@react-three/drei'
import { Suspense } from 'react'
import ModelViewer from './ModelViewer'
import LoadingSpinner from './LoadingSpinner'

export default function Scene3D() {
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <Canvas
        shadows
        gl={{ 
          antialias: true,
          alpha: true,
          powerPreference: 'high-performance'
        }}
      >
        {/* Cámara con posición inicial */}
        <PerspectiveCamera makeDefault position={[5, 3, 5]} fov={50} />
        
        {/* Controles de órbita (rotar, zoom, pan) */}
        <OrbitControls
          enableDamping
          dampingFactor={0.05}
          minDistance={2}
          maxDistance={20}
          maxPolarAngle={Math.PI / 2}
        />

        {/* Iluminación */}
        <ambientLight intensity={0.5} />
        <directionalLight
          position={[10, 10, 5]}
          intensity={1}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />
        <pointLight position={[-10, -10, -5]} intensity={0.3} />
        <spotLight
          position={[0, 10, 0]}
          angle={0.3}
          penumbra={1}
          intensity={0.5}
          castShadow
        />

        {/* Entorno HDR para reflejos realistas */}
        <Environment preset="city" />

        {/* Grid de referencia */}
        <Grid
          args={[20, 20]}
          cellSize={0.5}
          cellThickness={0.5}
          cellColor="#6f6f6f"
          sectionSize={2}
          sectionThickness={1}
          sectionColor="#9d4b4b"
          fadeDistance={25}
          fadeStrength={1}
          followCamera={false}
          infiniteGrid={true}
        />

        {/* Sombras de contacto */}
        <ContactShadows
          position={[0, -0.5, 0]}
          opacity={0.4}
          scale={10}
          blur={2}
          far={4}
        />

        {/* Modelo 3D con Suspense para carga asíncrona */}
        <Suspense fallback={<LoadingSpinner />}>
          <ModelViewer modelPath="/warrior.glb" />
        </Suspense>
      </Canvas>
    </div>
  )
}

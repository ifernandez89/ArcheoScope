'use client'

import { Canvas } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera, Environment, ContactShadows, Grid } from '@react-three/drei'
import { EffectComposer, Bloom, SSAO } from '@react-three/postprocessing'
import { Suspense, useState } from 'react'
import ModelViewer from './ModelViewer'
import LoadingSpinner from './LoadingSpinner'
import PerformanceStats from './PerformanceStats'
import ScreenshotButton from './ScreenshotButton'
import ModelSelector from './ModelSelector'
import ModelTransition from './ModelTransition'
import ModelInfo from './ModelInfo'
import { useSceneStore } from '@/store/scene-store'

export default function Scene3D() {
  const showGrid = useSceneStore((state) => state.showGrid)
  const autoRotate = useSceneStore((state) => state.autoRotate)
  const [currentModel, setCurrentModel] = useState('/moai.glb') // Empezar con moai

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
          autoRotate={autoRotate}
          autoRotateSpeed={0.5}
        />

        {/* Iluminación profesional */}
        <ambientLight intensity={0.4} />
        <directionalLight
          position={[10, 10, 5]}
          intensity={1.2}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
          shadow-camera-far={50}
          shadow-camera-left={-10}
          shadow-camera-right={10}
          shadow-camera-top={10}
          shadow-camera-bottom={-10}
        />
        <pointLight position={[-10, -10, -5]} intensity={0.3} color="#4a90e2" />
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
        {showGrid && (
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
        )}

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
          <ModelViewer key={currentModel} modelPath={currentModel} />
        </Suspense>

        {/* Postprocessing Effects */}
        <EffectComposer>
          <Bloom 
            intensity={0.3} 
            luminanceThreshold={0.9} 
            luminanceSmoothing={0.9}
          />
          <SSAO 
            samples={31}
            radius={5}
            intensity={30}
          />
        </EffectComposer>
      </Canvas>

      {/* Performance Stats - Outside Canvas */}
      <PerformanceStats />

      {/* Screenshot Button - Outside Canvas */}
      <ScreenshotButton />

      {/* Model Selector - Outside Canvas */}
      <ModelSelector 
        onModelChange={setCurrentModel}
        currentModel={currentModel}
      />

      {/* Model Info Panel - Outside Canvas */}
      <ModelInfo modelPath={currentModel} />

      {/* Model Transition Effect - Outside Canvas */}
      <ModelTransition modelName={currentModel} />
    </div>
  )
}

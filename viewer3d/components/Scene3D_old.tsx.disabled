'use client'

import { Suspense, useState, useEffect, useRef } from 'react'
import ImmersiveScene from './ImmersiveScene'
import LoadingSpinner from './LoadingSpinner'
import PerformanceStats from './PerformanceStats'
import ScreenshotButton from './ScreenshotButton'
import ModelSelector from './ModelSelector'
import ModelTransition from './ModelTransition'
import ModelInfo from './ModelInfo'
import SceneNavigator from './SceneNavigator'
import AudioControls from './AudioControls'
import ConversationalAvatar from './ConversationalAvatar'
import { useSceneStore } from '@/store/scene-store'
import { SceneSystem } from '@/experience/scene-system'
import { AudioSystem } from '@/core/audio'
import { ARCHAEOLOGICAL_SCENES } from '@/data/scenes'
import { useEngine } from '@/hooks/useEngine'
import * as THREE from 'three'

export default function Scene3D() {
  const showGrid = useSceneStore((state) => state.showGrid)
  const autoRotate = useSceneStore((state) => state.autoRotate)
  const [currentModel, setCurrentModel] = useState('/moai.glb')
  
  // FASE 2: Scene System
  const [sceneSystem, setSceneSystem] = useState<SceneSystem | null>(null)
  const [audioSystem, setAudioSystem] = useState<AudioSystem | null>(null)
  const [currentSceneId, setCurrentSceneId] = useState<string | null>(null)
  const [isTransitioning, setIsTransitioning] = useState(false)
  const [useSceneMode, setUseSceneMode] = useState(false)
  
  // Referencias para Avatar
  const [loadedModel, setLoadedModel] = useState<THREE.Object3D | null>(null)
  const [camera, setCamera] = useState<THREE.Camera | null>(null)

  // Inicializar sistemas
  useEffect(() => {
    const audio = new AudioSystem()
    setAudioSystem(audio)

    return () => {
      audio.dispose()
    }
  }, [])

  // Manejar cambio de escena
  const handleSceneChange = async (sceneId: string) => {
    if (!sceneSystem || isTransitioning) return

    setIsTransitioning(true)
    try {
      await sceneSystem.loadScene(sceneId, (progress) => {
        console.log(`Cargando escena: ${progress}%`)
      })
      setCurrentSceneId(sceneId)
    } catch (error) {
      console.error('Error cargando escena:', error)
    } finally {
      setIsTransitioning(false)
    }
  }

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
          <ModelCapture onModelLoaded={setLoadedModel} />
          <CameraCapture onCameraReady={setCamera} />
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

        {/* Engine Initializer */}
        <EngineInitializer onEngineReady={(engine) => {
          const system = new SceneSystem(engine)
          system.registerScenes(ARCHAEOLOGICAL_SCENES)
          setSceneSystem(system)
        }} />
      </Canvas>

      {/* Performance Stats - Solo en modo debug */}
      {process.env.NODE_ENV === 'development' && <PerformanceStats />}

      {/* Screenshot Button - Más discreto */}
      <ScreenshotButton />

      {/* Model Selector - Mantener */}
      <ModelSelector 
        onModelChange={setCurrentModel}
        currentModel={currentModel}
      />

      {/* Model Info Panel - Oculto por defecto, se muestra al hacer hover */}
      {/* <ModelInfo modelPath={currentModel} /> */}

      {/* Model Transition Effect - Mantener */}
      <ModelTransition modelName={currentModel} />

      {/* FASE 2: Scene Navigator - Mantener pero más discreto */}
      {sceneSystem && (
        <SceneNavigator
          scenes={ARCHAEOLOGICAL_SCENES}
          currentSceneId={currentSceneId}
          onSceneChange={handleSceneChange}
          isTransitioning={isTransitioning}
        />
      )}

      {/* FASE 2: Audio Controls - Mantener */}
      <AudioControls audioSystem={audioSystem} />

      {/* Avatar Conversacional - Prioridad máxima */}
      <ConversationalAvatar 
        model={loadedModel}
        camera={camera}
      />
    </div>
  )
}

// Helper component to initialize engine inside Canvas
function EngineInitializer({ onEngineReady }: { onEngineReady: (engine: any) => void }) {
  const engine = useEngine()
  const initialized = useRef(false)

  useEffect(() => {
    if (engine && !initialized.current) {
      initialized.current = true
      onEngineReady(engine)
    }
  }, [engine, onEngineReady])

  return null
}

// Helper to capture loaded model
function ModelCapture({ onModelLoaded }: { onModelLoaded: (model: THREE.Object3D) => void }) {
  const { scene } = useThree()
  
  useEffect(() => {
    // Buscar el modelo cargado en la escena
    const model = scene.children.find(child => 
      child.type === 'Group' && child.children.length > 0
    )
    
    if (model) {
      onModelLoaded(model)
    }
  }, [scene, onModelLoaded])
  
  return null
}

// Helper to capture camera
function CameraCapture({ onCameraReady }: { onCameraReady: (camera: THREE.Camera) => void }) {
  const { camera } = useThree()
  
  useEffect(() => {
    if (camera) {
      onCameraReady(camera)
    }
  }, [camera, onCameraReady])
  
  return null
}

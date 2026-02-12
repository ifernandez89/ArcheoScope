'use client'

import { useState, useRef, useEffect } from 'react'
import { Canvas, useThree } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera } from '@react-three/drei'
import * as THREE from 'three'
import Globe3D from './Globe3D'
import ModelViewer from './ModelViewer'

interface ImmersiveSceneProps {
  onModelLoaded?: (model: THREE.Object3D) => void
  onCameraReady?: (camera: THREE.Camera) => void
}

export default function ImmersiveScene({ onModelLoaded, onCameraReady }: ImmersiveSceneProps) {
  const [mode, setMode] = useState<'globe' | 'model'>('globe')
  const [selectedModel, setSelectedModel] = useState<string>('/moai.glb')
  const [isTransitioning, setIsTransitioning] = useState(false)

  // Manejar click en ubicación del globo
  const handleLocationClick = async (lat: number, lon: number) => {
    console.log(`🌍 Teletransporte a: lat=${lat.toFixed(2)}, lon=${lon.toFixed(2)}`)
    
    setIsTransitioning(true)
    
    // Simular transición cinematográfica
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Cambiar a modo modelo
    setMode('model')
    setIsTransitioning(false)
    
    console.log('✅ Teletransporte completado')
  }

  // Volver al globo
  const handleBackToGlobe = async () => {
    setIsTransitioning(true)
    await new Promise(resolve => setTimeout(resolve, 1000))
    setMode('globe')
    setIsTransitioning(false)
  }

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      {/* Indicador de transición */}
      {isTransitioning && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          zIndex: 2000,
          background: 'rgba(0,0,0,0.8)',
          padding: '20px 40px',
          borderRadius: '12px',
          color: 'white',
          fontSize: '18px',
          fontWeight: 'bold'
        }}>
          🌍 Teletransportando...
        </div>
      )}

      {/* Botón para volver al globo */}
      {mode === 'model' && !isTransitioning && (
        <button
          onClick={handleBackToGlobe}
          style={{
            position: 'absolute',
            top: '80px',
            left: '20px',
            zIndex: 1001,
            padding: '10px 20px',
            background: 'rgba(102, 126, 234, 0.9)',
            border: '1px solid rgba(255,255,255,0.3)',
            borderRadius: '8px',
            color: 'white',
            fontSize: '14px',
            fontWeight: 'bold',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            transition: 'all 0.2s'
          }}
          onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(102, 126, 234, 1)'}
          onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(102, 126, 234, 0.9)'}
        >
          🌍 Volver al Globo
        </button>
      )}

      {/* Escena 3D */}
      {mode === 'globe' ? (
        <GlobeScene onLocationClick={handleLocationClick} />
      ) : (
        <ModelScene 
          modelPath={selectedModel}
          onModelLoaded={onModelLoaded}
          onCameraReady={onCameraReady}
        />
      )}
    </div>
  )
}

// Escena del globo
function GlobeScene({ onLocationClick }: { onLocationClick: (lat: number, lon: number) => void }) {
  return (
    <Canvas
      camera={{ position: [0, 0, 15], fov: 50 }}
      style={{ background: '#000' }}
    >
      <PerspectiveCamera makeDefault position={[0, 0, 15]} fov={50} />
      <OrbitControls
        enableDamping
        dampingFactor={0.05}
        minDistance={8}
        maxDistance={30}
        autoRotate={false}
      />
      
      {/* Estrellas de fondo */}
      <Stars />
      
      {/* Globo terráqueo */}
      <Globe3D onLocationClick={onLocationClick} />
    </Canvas>
  )
}

// Escena del modelo
function ModelScene({ 
  modelPath, 
  onModelLoaded, 
  onCameraReady 
}: { 
  modelPath: string
  onModelLoaded?: (model: THREE.Object3D) => void
  onCameraReady?: (camera: THREE.Camera) => void
}) {
  return (
    <Canvas
      shadows
      camera={{ position: [5, 3, 5], fov: 50 }}
      gl={{ 
        antialias: true,
        alpha: true,
        powerPreference: 'high-performance'
      }}
    >
      <PerspectiveCamera makeDefault position={[5, 3, 5]} fov={50} />
      <OrbitControls
        enableDamping
        dampingFactor={0.05}
        minDistance={2}
        maxDistance={20}
        maxPolarAngle={Math.PI / 2}
      />

      {/* Iluminación */}
      <ambientLight intensity={0.4} />
      <directionalLight
        position={[10, 10, 5]}
        intensity={1.2}
        castShadow
      />
      <pointLight position={[-10, -10, -5]} intensity={0.3} color="#4a90e2" />

      {/* Modelo 3D */}
      <ModelViewer modelPath={modelPath} />
      
      {/* Capturar referencias */}
      <CameraCapture onReady={onCameraReady} />
      <ModelCapture onLoaded={onModelLoaded} />
    </Canvas>
  )
}

// Componente de estrellas
function Stars() {
  const starsRef = useRef<THREE.Points>(null)
  
  useEffect(() => {
    if (!starsRef.current) return
    
    const geometry = new THREE.BufferGeometry()
    const vertices = []
    
    for (let i = 0; i < 10000; i++) {
      const x = (Math.random() - 0.5) * 2000
      const y = (Math.random() - 0.5) * 2000
      const z = (Math.random() - 0.5) * 2000
      vertices.push(x, y, z)
    }
    
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3))
    starsRef.current.geometry = geometry
  }, [])
  
  return (
    <points ref={starsRef}>
      <pointsMaterial
        size={2}
        color="#ffffff"
        transparent
        opacity={0.8}
      />
    </points>
  )
}

// Capturar cámara
function CameraCapture({ onReady }: { onReady?: (camera: THREE.Camera) => void }) {
  const { camera } = useThree()
  
  useEffect(() => {
    if (camera && onReady) {
      onReady(camera)
    }
  }, [camera, onReady])
  
  return null
}

// Capturar modelo
function ModelCapture({ onLoaded }: { onLoaded?: (model: THREE.Object3D) => void }) {
  const { scene } = useThree()
  
  useEffect(() => {
    const model = scene.children.find(child => 
      child.type === 'Group' && child.children.length > 0
    )
    
    if (model && onLoaded) {
      onLoaded(model)
    }
  }, [scene, onLoaded])
  
  return null
}

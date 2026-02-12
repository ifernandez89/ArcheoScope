'use client'

import { useState, useRef, useEffect } from 'react'
import { Canvas, useThree, useFrame } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera, PointerLockControls, Html } from '@react-three/drei'
import * as THREE from 'three'
import Globe3D from './Globe3D'
import ModelViewer from './ModelViewer'
import SiteMarkers from './SiteMarkers'
import { ArcheoEngine, AvatarEngine, type ArchaeologicalSite } from '../engines'

interface ImmersiveSceneProps {
  onModelLoaded?: (model: THREE.Object3D) => void
  onCameraReady?: (camera: THREE.Camera) => void
}

export default function ImmersiveScene({ onModelLoaded, onCameraReady }: ImmersiveSceneProps) {
  const [mode, setMode] = useState<'globe' | 'transition' | 'model'>('globe')
  const [selectedModel, setSelectedModel] = useState<string>('/moai.glb')
  const [selectedLocation, setSelectedLocation] = useState<{ lat: number, lon: number } | null>(null)
  const [selectedSite, setSelectedSite] = useState<ArchaeologicalSite | null>(null)
  const [movementMode, setMovementMode] = useState<'orbit' | 'firstPerson'>('orbit')
  const [solarSimulation, setSolarSimulation] = useState(true)

  // Manejar click en sitio arqueológico
  const handleSiteClick = async (site: ArchaeologicalSite) => {
    console.log(`🏛️ Sitio seleccionado: ${site.name}`)
    
    // Actualizar contexto del avatar
    AvatarEngine.setContext({
      siteName: site.name,
      culture: site.culture,
      period: site.period,
      location: { lat: site.lat, lon: site.lon }
    })
    
    setSelectedLocation({ lat: site.lat, lon: site.lon })
    setSelectedModel(site.model)
    setSelectedSite(site)
    setMode('transition')
    
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    setMode('model')
    
    console.log('✅ Teletransporte a sitio arqueológico completado')
  }

  // Manejar click en ubicación del globo
  const handleLocationClick = async (lat: number, lon: number) => {
    console.log(`🌍 Iniciando teletransporte a: lat=${lat.toFixed(4)}, lon=${lon.toFixed(4)}`)
    
    setSelectedLocation({ lat, lon })
    setSelectedModel('/moai.glb')
    setSelectedSite(null)
    setMode('transition')
    
    // Transición cinematográfica de 2 segundos
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Cambiar a modo modelo
    setMode('model')
    
    console.log('✅ Teletransporte completado')
    console.log('📍 Coordenadas exactas:', { lat, lon })
  }

  // Volver al globo
  const handleBackToGlobe = async () => {
    setMode('transition')
    await new Promise(resolve => setTimeout(resolve, 1500))
    setMode('globe')
    setSelectedLocation(null)
    setSelectedSite(null)
  }

  // Toggle entre modo órbita y primera persona
  const toggleMovementMode = () => {
    setMovementMode(prev => prev === 'orbit' ? 'firstPerson' : 'orbit')
  }

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      {/* Indicador de transición cinematográfica */}
      {mode === 'transition' && (
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          zIndex: 2000,
          background: 'radial-gradient(circle, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.95) 100%)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          animation: 'fadeIn 0.5s ease-in-out'
        }}>
          <div style={{
            fontSize: '48px',
            marginBottom: '20px',
            animation: 'pulse 1.5s infinite'
          }}>
            🌍
          </div>
          <div style={{
            color: 'white',
            fontSize: '24px',
            fontWeight: 'bold',
            textShadow: '0 0 20px rgba(102, 126, 234, 0.8)'
          }}>
            {selectedSite 
              ? `Viajando a ${selectedSite.name}...` 
              : selectedLocation 
                ? 'Teletransportando...' 
                : 'Regresando al globo...'}
          </div>
          {selectedLocation && (
            <div style={{
              color: '#888',
              fontSize: '14px',
              marginTop: '10px'
            }}>
              📍 Lat: {selectedLocation.lat.toFixed(4)}° | Lon: {selectedLocation.lon.toFixed(4)}°
            </div>
          )}
          {selectedSite && (
            <div style={{
              color: '#fbbf24',
              fontSize: '12px',
              marginTop: '8px'
            }}>
              {selectedSite.culture} • {selectedSite.period}
            </div>
          )}
        </div>
      )}

      {/* Botones de control */}
      {mode === 'model' && (
        <div style={{
          position: 'absolute',
          top: '20px',
          left: '20px',
          zIndex: 1001,
          display: 'flex',
          flexDirection: 'column',
          gap: '10px'
        }}>
          <button
            onClick={handleBackToGlobe}
            style={{
              padding: '12px 24px',
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
              transition: 'all 0.2s',
              boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
            }}
            onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(102, 126, 234, 1)'}
            onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(102, 126, 234, 0.9)'}
          >
            🌍 Volver al Globo
          </button>

          <button
            onClick={() => setSolarSimulation(!solarSimulation)}
            style={{
              padding: '12px 24px',
              background: solarSimulation 
                ? 'rgba(251, 191, 36, 0.9)' 
                : 'rgba(75, 85, 99, 0.9)',
              border: '1px solid rgba(255,255,255,0.3)',
              borderRadius: '8px',
              color: 'white',
              fontSize: '14px',
              fontWeight: 'bold',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              transition: 'all 0.2s',
              boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = solarSimulation 
                ? 'rgba(251, 191, 36, 1)' 
                : 'rgba(75, 85, 99, 1)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = solarSimulation 
                ? 'rgba(251, 191, 36, 0.9)' 
                : 'rgba(75, 85, 99, 0.9)'
            }}
          >
            {solarSimulation ? '☀️ Simulación Solar ON' : '🌙 Simulación Solar OFF'}
          </button>

          <button
            onClick={toggleMovementMode}
            style={{
              padding: '12px 24px',
              background: movementMode === 'firstPerson' 
                ? 'rgba(234, 179, 8, 0.9)' 
                : 'rgba(34, 197, 94, 0.9)',
              border: '1px solid rgba(255,255,255,0.3)',
              borderRadius: '8px',
              color: 'white',
              fontSize: '14px',
              fontWeight: 'bold',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              transition: 'all 0.2s',
              boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = movementMode === 'firstPerson' 
                ? 'rgba(234, 179, 8, 1)' 
                : 'rgba(34, 197, 94, 1)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = movementMode === 'firstPerson' 
                ? 'rgba(234, 179, 8, 0.9)' 
                : 'rgba(34, 197, 94, 0.9)'
            }}
          >
            {movementMode === 'orbit' ? '🎮 Modo Primera Persona' : '🔄 Modo Órbita'}
          </button>
        </div>
      )}

      {/* Instrucciones de movimiento en primera persona */}
      {mode === 'model' && movementMode === 'firstPerson' && (
        <div style={{
          position: 'absolute',
          bottom: '20px',
          left: '50%',
          transform: 'translateX(-50%)',
          zIndex: 1001,
          background: 'rgba(0, 0, 0, 0.8)',
          backdropFilter: 'blur(10px)',
          padding: '12px 24px',
          borderRadius: '8px',
          border: '1px solid rgba(255,255,255,0.2)',
          color: 'white',
          fontSize: '12px',
          display: 'flex',
          gap: '20px'
        }}>
          <span>🖱️ Click para activar</span>
          <span>W/A/S/D - Mover</span>
          <span>Mouse - Mirar</span>
          <span>ESC - Salir</span>
        </div>
      )}

      {/* Escena 3D */}
      {mode === 'globe' ? (
        <GlobeScene 
          onLocationClick={handleLocationClick}
          onSiteClick={handleSiteClick}
          markerPosition={selectedLocation}
        />
      ) : mode === 'model' ? (
        <ModelScene 
          modelPath={selectedModel}
          onModelLoaded={onModelLoaded}
          onCameraReady={onCameraReady}
          movementMode={movementMode}
          location={selectedLocation}
          site={selectedSite}
          solarSimulation={solarSimulation}
        />
      ) : null}

      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes pulse {
          0%, 100% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.2); opacity: 0.7; }
        }
      `}</style>
    </div>
  )
}

// Escena del globo
function GlobeScene({ 
  onLocationClick,
  onSiteClick,
  markerPosition
}: { 
  onLocationClick: (lat: number, lon: number) => void
  onSiteClick: (site: ArchaeologicalSite) => void
  markerPosition?: { lat: number, lon: number } | null
}) {
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
      
      {/* Globo terráqueo con marcador */}
      <Globe3D 
        onLocationClick={onLocationClick}
        markerPosition={markerPosition}
      />
      
      {/* Marcadores de sitios arqueológicos */}
      <SiteMarkers onSiteClick={onSiteClick} />
    </Canvas>
  )
}

// Escena del modelo con zoom cinematográfico
function ModelScene({ 
  modelPath, 
  onModelLoaded, 
  onCameraReady,
  movementMode,
  location,
  site,
  solarSimulation
}: { 
  modelPath: string
  onModelLoaded?: (model: THREE.Object3D) => void
  onCameraReady?: (camera: THREE.Camera) => void
  movementMode: 'orbit' | 'firstPerson'
  location?: { lat: number, lon: number } | null
  site?: ArchaeologicalSite | null
  solarSimulation: boolean
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
      
      {/* Controles según modo */}
      {movementMode === 'orbit' ? (
        <OrbitControls
          enableDamping
          dampingFactor={0.05}
          minDistance={2}
          maxDistance={20}
          maxPolarAngle={Math.PI / 2}
        />
      ) : (
        <FirstPersonControls />
      )}

      {/* Iluminación con simulación solar */}
      {solarSimulation && location ? (
        <SolarSimulation lat={location.lat} lon={location.lon} />
      ) : (
        <>
          <ambientLight intensity={0.4} />
          <directionalLight
            position={[10, 10, 5]}
            intensity={1.2}
            castShadow
            shadow-mapSize-width={2048}
            shadow-mapSize-height={2048}
          />
          <pointLight position={[-10, -10, -5]} intensity={0.3} color="#4a90e2" />
          <hemisphereLight args={['#87ceeb', '#654321', 0.3]} />
        </>
      )}

      {/* Suelo para primera persona */}
      {movementMode === 'firstPerson' && (
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1, 0]} receiveShadow>
          <planeGeometry args={[50, 50]} />
          <meshBasicMaterial color="#3a3a3a" />
        </mesh>
      )}

      {/* Modelo 3D */}
      <ModelViewer modelPath={modelPath} />
      
      {/* Info del sitio */}
      {site && (
        <SiteInfo site={site} />
      )}
      
      {/* Capturar referencias */}
      <CameraCapture onReady={onCameraReady} />
      <ModelCapture onLoaded={onModelLoaded} />
      
      {/* Zoom cinematográfico al entrar */}
      <CinematicZoom />
    </Canvas>
  )
}

// Controles de primera persona
function FirstPersonControls() {
  const { camera, gl } = useThree()
  const moveSpeed = 0.1
  const keys = useRef<{ [key: string]: boolean }>({})

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      keys.current[e.key.toLowerCase()] = true
    }
    const handleKeyUp = (e: KeyboardEvent) => {
      keys.current[e.key.toLowerCase()] = false
    }

    window.addEventListener('keydown', handleKeyDown)
    window.addEventListener('keyup', handleKeyUp)

    return () => {
      window.removeEventListener('keydown', handleKeyDown)
      window.removeEventListener('keyup', handleKeyUp)
    }
  }, [])

  useFrame(() => {
    const direction = new THREE.Vector3()
    const right = new THREE.Vector3()

    camera.getWorldDirection(direction)
    right.crossVectors(camera.up, direction).normalize()

    if (keys.current['w']) {
      camera.position.addScaledVector(direction, moveSpeed)
    }
    if (keys.current['s']) {
      camera.position.addScaledVector(direction, -moveSpeed)
    }
    if (keys.current['a']) {
      camera.position.addScaledVector(right, moveSpeed)
    }
    if (keys.current['d']) {
      camera.position.addScaledVector(right, -moveSpeed)
    }
  })

  return <PointerLockControls />
}

// Zoom cinematográfico
function CinematicZoom() {
  const { camera } = useThree()
  const startPos = useRef(new THREE.Vector3(15, 10, 15))
  const targetPos = useRef(new THREE.Vector3(5, 3, 5))
  const progress = useRef(0)

  useFrame((state, delta) => {
    if (progress.current < 1) {
      progress.current += delta * 0.5
      const t = Math.min(progress.current, 1)
      
      // Easing suave
      const eased = 1 - Math.pow(1 - t, 3)
      
      camera.position.lerpVectors(startPos.current, targetPos.current, eased)
      camera.lookAt(0, 0, 0)
    }
  })

  return null
}

// Componente de estrellas mejorado
function Stars() {
  const starsRef = useRef<THREE.Points>(null)
  
  useEffect(() => {
    if (!starsRef.current) return
    
    const geometry = new THREE.BufferGeometry()
    const vertices = []
    const colors = []
    
    for (let i = 0; i < 15000; i++) {
      const x = (Math.random() - 0.5) * 2000
      const y = (Math.random() - 0.5) * 2000
      const z = (Math.random() - 0.5) * 2000
      vertices.push(x, y, z)
      
      // Colores variados para las estrellas
      const color = new THREE.Color()
      color.setHSL(Math.random() * 0.2 + 0.5, 0.3, 0.8 + Math.random() * 0.2)
      colors.push(color.r, color.g, color.b)
    }
    
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3))
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3))
    starsRef.current.geometry = geometry
  }, [])
  
  return (
    <points ref={starsRef}>
      <pointsMaterial
        size={2}
        vertexColors
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

// Simulación solar real basada en coordenadas
function SolarSimulation({ lat, lon }: { lat: number, lon: number }) {
  const lightRef = useRef<THREE.DirectionalLight>(null)
  
  useEffect(() => {
    if (!lightRef.current) return
    
    // Calcular posición solar basada en lat/lon y hora actual
    const now = new Date()
    const dayOfYear = Math.floor((now.getTime() - new Date(now.getFullYear(), 0, 0).getTime()) / 86400000)
    const hour = now.getHours() + now.getMinutes() / 60
    
    // Declinación solar (simplificado)
    const declination = 23.45 * Math.sin((360 / 365) * (dayOfYear - 81) * Math.PI / 180)
    
    // Ángulo horario
    const hourAngle = 15 * (hour - 12)
    
    // Altura solar
    const altitude = Math.asin(
      Math.sin(lat * Math.PI / 180) * Math.sin(declination * Math.PI / 180) +
      Math.cos(lat * Math.PI / 180) * Math.cos(declination * Math.PI / 180) * Math.cos(hourAngle * Math.PI / 180)
    ) * 180 / Math.PI
    
    // Azimut solar (simplificado)
    const azimuth = hourAngle
    
    // Convertir a posición 3D
    const distance = 15
    const x = distance * Math.cos(altitude * Math.PI / 180) * Math.sin(azimuth * Math.PI / 180)
    const y = distance * Math.sin(altitude * Math.PI / 180)
    const z = distance * Math.cos(altitude * Math.PI / 180) * Math.cos(azimuth * Math.PI / 180)
    
    lightRef.current.position.set(x, Math.max(y, 2), z)
    
    // Ajustar intensidad según altura solar
    const intensity = Math.max(0.3, Math.sin(altitude * Math.PI / 180) * 1.5)
    lightRef.current.intensity = intensity
    
    // Color según hora del día
    const sunColor = altitude > 0 
      ? (altitude < 15 ? '#ff9966' : '#ffffff')  // Amanecer/atardecer vs mediodía
      : '#1a1a2e'  // Noche
    
    lightRef.current.color.set(sunColor)
    
    console.log('☀️ Simulación solar:', {
      lat: lat.toFixed(2),
      lon: lon.toFixed(2),
      altitude: altitude.toFixed(2),
      azimuth: azimuth.toFixed(2),
      intensity: intensity.toFixed(2),
      color: sunColor
    })
  }, [lat, lon])
  
  return (
    <>
      <ambientLight intensity={0.2} />
      <directionalLight
        ref={lightRef}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
      />
      <hemisphereLight args={['#87ceeb', '#654321', 0.2]} />
    </>
  )
}

// Info del sitio arqueológico
function SiteInfo({ site }: { site: ArchaeologicalSite }) {
  return (
    <Html
      position={[0, 2.5, 0]}
      center
      distanceFactor={8}
      style={{
        background: 'rgba(0, 0, 0, 0.85)',
        padding: '12px 20px',
        borderRadius: '12px',
        border: '2px solid rgba(251, 191, 36, 0.5)',
        color: 'white',
        fontSize: '13px',
        fontFamily: 'system-ui',
        pointerEvents: 'none',
        minWidth: '250px',
        boxShadow: '0 8px 32px rgba(0,0,0,0.5)'
      }}
    >
      <div style={{ fontWeight: 'bold', marginBottom: '8px', color: '#fbbf24', fontSize: '16px' }}>
        🏛️ {site.name}
      </div>
      <div style={{ fontSize: '11px', color: '#888', marginBottom: '6px' }}>
        {site.culture} • {site.period}
      </div>
      <div style={{ fontSize: '11px', color: '#ccc', lineHeight: '1.4' }}>
        {site.description}
      </div>
    </Html>
  )
}

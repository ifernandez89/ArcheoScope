'use client'

import { useState, useRef, useEffect, useMemo } from 'react'
import { Canvas, useThree, useFrame } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera, Html, useGLTF } from '@react-three/drei'
import * as THREE from 'three'
import Globe3D from './Globe3D'
import ModelViewer from './ModelViewer'
import SiteMarkers from './SiteMarkers'
import CoordinateInput from './CoordinateInput'
import LocationInfo from './LocationInfo'
import VolcanicTerrain from './VolcanicTerrain'
import IceTerrain from './IceTerrain'
import WeatherControl, { type WeatherState } from './WeatherControl'
import BasicCollisions from './BasicCollisions'
import WalkableAvatar from './WalkableAvatar'
import SolarSystemIntegrated from './SolarSystemIntegrated'
import SimpleMoon from './SimpleMoon'
import Sun from './Sun'
import Mercury from './Mercury'
import Venus from './Venus'
import Mars from './Mars'
import PlanetaryOrbits from './PlanetaryOrbits'
import EarthOrbitWrapper from './EarthOrbitWrapper'
import LunarOrbitLine from './LunarOrbitLine'
import MilkyWayBackground from './MilkyWayBackground'
import RealisticSolarSystem from './RealisticSolarSystem'
import Stars from './Stars'
import { 
  useNarrativeZoom
  // LunarOrbit, 
  // OrbitalPlane, 
  // SimpleSun, 
  // EarthOrbit, 
  // EclipticPlane 
} from './NarrativeZoom'
import { detectBiome, getSkyColorForBiome, getFogColorForBiome } from '@/utils/biome-detector'
import ProceduralTerrain from './ProceduralTerrain'
import AmbientMotion from './AmbientMotion'
import { ArcheoEngine, AvatarEngine, type ArchaeologicalSite } from '../engines'
import { getAssetPath } from '@/lib/paths'
import { loggers } from '@/core/Logger'

// 🗺️ SISTEMA DE TERRENO MEJORADO
import EnhancedTerrain from './EnhancedTerrain'
import TerrainControl from './TerrainControl'

// 🎮 SISTEMAS DE PERFORMANCE
import EngineIntegration from './EngineIntegration'

// 🔥 SISTEMAS MODULARES LAZY-LOADED
import {
  LightingSystem,
  WeatherSystem,
  EnvironmentSystem,
  PostProcessingSystem,
  AstronomicalSystem
} from '@/utils/lazy-systems'

interface ImmersiveSceneProps {
  onModelLoaded?: (model: THREE.Object3D) => void
  onCameraReady?: (camera: THREE.Camera) => void
  onModeChange?: (mode: 'globe' | 'transition' | 'model' | 'exploration') => void
  spaceUfoActive?: boolean
}

export default function ImmersiveScene({ onModelLoaded, onCameraReady, onModeChange, spaceUfoActive = false }: ImmersiveSceneProps) {
  const [mode, setMode] = useState<'globe' | 'transition' | 'model' | 'exploration'>('globe')
  const [selectedModel, setSelectedModel] = useState<string>(getAssetPath('/moai.glb'))
  const [avatarModel, setAvatarModel] = useState<string>(getAssetPath('/avenger_01.glb')) // Avenger por defecto
  const [selectedLocation, setSelectedLocation] = useState<{ lat: number, lon: number } | null>(null)
  const [selectedSite, setSelectedSite] = useState<ArchaeologicalSite | null>(null)
  const [movementMode, setMovementMode] = useState<'orbit' | 'avatar'>('avatar') // Modo avatar por defecto
  const [showLocationInfo, setShowLocationInfo] = useState(false)
  const [showGeometryField, setShowGeometryField] = useState(true) // Activado por defecto
  const [isDay, setIsDay] = useState(true) // Estado día/noche
  const [weather, setWeather] = useState<WeatherState>({ 
    snow: false, 
    rainLight: false,
    rainModerate: false,
    rainHeavy: false,
    wind: false,
    fog: false,
    storm: false,
    lightning: false,
    tornado: false,
    clouds: false
  }) // Estado del clima
  const [solarDirection, setSolarDirection] = useState({ x: 0, y: 1, z: 0 }) // Dirección del sol como objeto plano
  const [solarState, setSolarState] = useState({
    altitude: 0,
    azimuth: 0,
    declination: 0
  })
  
  // Estado del terreno mejorado - DESHABILITADO (terreno procedural por defecto)
  const [enhancedTerrainEnabled] = useState(false)
  const [terrainExaggeration] = useState(1.5)
  const [terrainLOD] = useState(true)
  const [terrainLoading, setTerrainLoading] = useState(false)

  // Notificar cambios de modo al padre
  useEffect(() => {
    if (onModeChange) {
      onModeChange(mode)
    }
  }, [mode, onModeChange])



  // Manejar click en sitio arqueológico
  const handleSiteClick = async (site: ArchaeologicalSite) => {
    loggers.world.info(`Sitio seleccionado: ${site.name}`)
    
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
    
    loggers.world.info('Teletransporte a sitio arqueológico completado')
  }

  // Manejar click en ubicación del globo
  const handleLocationClick = async (lat: number, lon: number) => {
    loggers.world.info(`Iniciando teletransporte a: lat=${lat.toFixed(4)}, lon=${lon.toFixed(4)}`)
    
    setSelectedLocation({ lat, lon })
    setSelectedModel(getAssetPath('/moai.glb'))
    setSelectedSite(null)
    setMode('transition')
    
    // Transición cinematográfica de 2 segundos
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Cambiar a modo modelo
    setMode('model')
    
    loggers.world.info('Teletransporte completado', { lat, lon })
  }

  // Volver al globo
  const handleBackToGlobe = async () => {
    setMode('transition')
    await new Promise(resolve => setTimeout(resolve, 1500))
    setMode('globe')
    setSelectedLocation(null)
    setSelectedSite(null)
  }

  // Toggle entre modos de movimiento
  const toggleMovementMode = () => {
    setMovementMode(prev => {
      if (prev === 'orbit') return 'avatar'
      return 'orbit'
    })
  }

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      {/* Input de coordenadas */}
      <CoordinateInput 
        onCoordinateSubmit={handleLocationClick}
        currentLocation={selectedLocation}
      />

      {/* Información de ubicación (desplegable) */}
      {mode === 'model' && showLocationInfo && (
        <LocationInfo 
          location={selectedLocation}
          site={selectedSite}
        />
      )}

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
            onClick={toggleMovementMode}
            style={{
              padding: '12px 24px',
              background: movementMode === 'avatar' 
                ? 'rgba(139, 92, 246, 0.9)'
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
              e.currentTarget.style.background = movementMode === 'avatar'
                ? 'rgba(139, 92, 246, 1)'
                : 'rgba(34, 197, 94, 1)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = movementMode === 'avatar'
                ? 'rgba(139, 92, 246, 0.9)'
                : 'rgba(34, 197, 94, 0.9)'
            }}
          >
            {movementMode === 'avatar' ? 'Modo: Avenger' : '🔄 Modo: Órbita'}
          </button>

          {/* Botón para mostrar/ocultar información de ubicación */}
          <button
            onClick={() => setShowLocationInfo(!showLocationInfo)}
            style={{
              padding: '12px 24px',
              background: showLocationInfo ? 'rgba(102, 126, 234, 0.9)' : 'rgba(75, 85, 99, 0.7)',
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
              e.currentTarget.style.background = showLocationInfo 
                ? 'rgba(102, 126, 234, 1)' 
                : 'rgba(75, 85, 99, 0.9)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = showLocationInfo 
                ? 'rgba(102, 126, 234, 0.9)' 
                : 'rgba(75, 85, 99, 0.7)'
            }}
          >
            📍 {showLocationInfo ? 'Ocultar Info' : 'Mostrar Info'}
          </button>
        </div>
      )}

      {/* Instrucciones de movimiento */}
      {mode === 'model' && movementMode === 'avatar' && (
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
          <span>🚶 W/S - Adelante/Atrás</span>
          <span>A/D - Izquierda/Derecha</span>
          <span>Q/E - Rotar</span>
          <span>🚀 SHIFT - Vuelo Libre (sigue el mouse)</span>
        </div>
      )}

      {/* Escena 3D */}
      {mode === 'globe' ? (
        <GlobeScene 
          onLocationClick={handleLocationClick}
          onSiteClick={handleSiteClick}
          markerPosition={selectedLocation}
          spaceUfoActive={spaceUfoActive}
        />
      ) : mode === 'model' ? (
        <ModelScene 
          modelPath={selectedModel}
          avatarModel={avatarModel}
          onModelLoaded={onModelLoaded}
          onCameraReady={onCameraReady}
          movementMode={movementMode}
          location={selectedLocation}
          site={selectedSite}
          showGeometryField={showGeometryField}
          isDay={isDay}
          onDayNightChange={setIsDay}
          solarDirection={solarDirection}
          solarState={solarState}
          onSolarUpdate={(direction, altitude, azimuth, declination) => {
            setSolarDirection(direction)
            setSolarState({ altitude, azimuth, declination })
          }}
          weather={weather}
          enhancedTerrainEnabled={enhancedTerrainEnabled}
          terrainExaggeration={terrainExaggeration}
          terrainLOD={terrainLOD}
          onTerrainLoadingChange={setTerrainLoading}
        />
      ) : null}

      {/* Control de clima */}
      {mode === 'model' && (
        <WeatherControl onWeatherChange={setWeather} />
      )}

      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes pulse {
          0%, 100% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.2); opacity: 0.7; }
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}

// Partículas ambientales sutiles para sensación de movimiento
function AmbientParticles() {
  const particlesRef = useRef<THREE.Points>(null)
  
  const particlesGeometry = useMemo(() => {
    const geometry = new THREE.BufferGeometry()
    const count = 500  // Pocas partículas, muy sutiles
    const positions = new Float32Array(count * 3)
    
    for (let i = 0; i < count; i++) {
      const i3 = i * 3
      // Distribuir en un área amplia alrededor del jugador
      positions[i3] = (Math.random() - 0.5) * 100
      positions[i3 + 1] = Math.random() * 10 + 1  // Entre 1 y 11 metros de altura
      positions[i3 + 2] = (Math.random() - 0.5) * 100
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    return geometry
  }, [])
  
  const particlesMaterial = useMemo(() => {
    return new THREE.PointsMaterial({
      size: 0.3,
      color: '#ffffff',
      transparent: true,
      opacity: 0.15,  // Muy sutil
      sizeAttenuation: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    })
  }, [])
  
  // Animación sutil de flotación
  useFrame((state) => {
    if (particlesRef.current) {
      const positions = particlesRef.current.geometry.attributes.position.array as Float32Array
      
      for (let i = 0; i < positions.length; i += 3) {
        // Movimiento vertical lento
        positions[i + 1] += Math.sin(state.clock.elapsedTime + i) * 0.001
        
        // Si la partícula baja mucho, resetearla arriba
        if (positions[i + 1] < 0.5) {
          positions[i + 1] = 11
        }
      }
      
      particlesRef.current.geometry.attributes.position.needsUpdate = true
    }
  })
  
  return <points ref={particlesRef} geometry={particlesGeometry} material={particlesMaterial} />
}

// Escena del globo
function GlobeScene({ 
  onLocationClick,
  onSiteClick,
  markerPosition,
  spaceUfoActive = false
}: { 
  onLocationClick: (lat: number, lon: number) => void
  onSiteClick: (site: ArchaeologicalSite) => void
  markerPosition?: { lat: number, lon: number } | null
  spaceUfoActive?: boolean
}) {
  return (
    <Canvas
      camera={{ position: [0, 0, 15], fov: 50 }}
      style={{ 
        background: '#000',
        cursor: spaceUfoActive ? 'none' : 'default' // Ocultar cursor cuando Avenger está activo
      }}
    >
      {/* 🎮 SISTEMAS DE PERFORMANCE - ÚNICO useFrame */}
      <EngineIntegration />
      
      <PerspectiveCamera makeDefault position={[0, 0, 15]} fov={50} />
      <OrbitControls
        enableDamping
        dampingFactor={0.05}
        minDistance={8}
        maxDistance={450} // Aumentado para ver órbita completa de Marte (304 unidades)
        autoRotate={false}
      />
      
      {/* Sistema de Zoom Narrativo */}
      <NarrativeZoomContent 
        onLocationClick={onLocationClick}
        markerPosition={markerPosition}
      />
      
      {/* Avenger Espacial controlado por mouse */}
      {spaceUfoActive && (
        <SpaceUfo />
      )}
      
      {/* Marcadores de sitios arqueológicos - Temporalmente deshabilitados */}
      {/* <SiteMarkers onSiteClick={onSiteClick} /> */}
    </Canvas>
  )
}

// Contenido que responde al zoom narrativo - AHORA CON SISTEMA REALISTA
function NarrativeZoomContent({ 
  onLocationClick,
  markerPosition
}: {
  onLocationClick: (lat: number, lon: number) => void
  markerPosition?: { lat: number, lon: number } | null
}) {
  return (
    <>
      {/* Fondo de la Vía Láctea - Esfera envolvente con textura */}
      <MilkyWayBackground />
      
      {/* Estrellas procedurales */}
      <Stars />
      
      {/* Sistema Solar Realista con posiciones astronómicas reales */}
      <RealisticSolarSystem 
        onLocationClick={onLocationClick}
        markerPosition={markerPosition}
      />
    </>
  )
}

// Escena del modelo con zoom cinematográfico
function ModelScene({ 
  modelPath, 
  avatarModel,
  onModelLoaded, 
  onCameraReady,
  movementMode,
  location,
  site,
  showGeometryField,
  isDay,
  onDayNightChange,
  solarDirection,
  solarState,
  onSolarUpdate,
  weather,
  enhancedTerrainEnabled,
  terrainExaggeration,
  terrainLOD,
  onTerrainLoadingChange
}: { 
  modelPath: string
  avatarModel: string
  onModelLoaded?: (model: THREE.Object3D) => void
  onCameraReady?: (camera: THREE.Camera) => void
  movementMode: 'orbit' | 'avatar'
  location?: { lat: number, lon: number } | null
  site?: ArchaeologicalSite | null
  showGeometryField: boolean
  isDay: boolean
  onDayNightChange: (isDay: boolean) => void
  solarDirection: { x: number, y: number, z: number }
  solarState: { altitude: number, azimuth: number, declination: number }
  onSolarUpdate: (direction: { x: number, y: number, z: number }, altitude: number, azimuth: number, declination: number) => void
  weather: WeatherState
  enhancedTerrainEnabled?: boolean
  terrainExaggeration?: number
  terrainLOD?: boolean
  onTerrainLoadingChange?: (loading: boolean) => void
}) {
  const terrainRef = useRef<THREE.Mesh>(null)
  const modelRef = useRef<THREE.Group>(null)
  const [obstacles, setObstacles] = useState<THREE.Object3D[]>([])
  
  // Detectar bioma basado en ubicación
  const biome = useMemo(() => {
    if (!location) return { type: 'default' as const, name: 'Genérico', description: '', temperature: 20, humidity: 50 }
    return detectBiome(location.lat, location.lon)
  }, [location])
  
  const isIceBiome = biome.type === 'ice'
  
  // Colores dinámicos según bioma
  const skyColor = useMemo(() => getSkyColorForBiome(biome.type, isDay), [biome.type, isDay])
  const fogColor = useMemo(() => getFogColorForBiome(biome.type), [biome.type])
  
  // Log del bioma detectado
  useEffect(() => {
    if (location) {
      loggers.world.info(`Bioma detectado: ${biome.name} (${biome.type})`, {
        temperatura: biome.temperature,
        humedad: biome.humidity
      })
    }
  }, [biome, location])
  
  // Actualizar obstáculos cuando el modelo cargue
  useEffect(() => {
    if (modelRef.current) {
      setObstacles([modelRef.current])
    }
  }, [modelRef.current])
  
  return (
    <Canvas
      shadows
      camera={{ position: [8, 4, 8], fov: 60 }}
      gl={{ 
        antialias: true,
        alpha: false,
        powerPreference: 'high-performance',
        toneMapping: THREE.ACESFilmicToneMapping,
        toneMappingExposure: 1.2
      }}
    >
      {/* 🎮 SISTEMAS DE PERFORMANCE - ÚNICO useFrame */}
      <EngineIntegration />
      
      <PerspectiveCamera makeDefault position={[8, 4, 8]} fov={60} />
      
      {/* Controles según modo */}
      {movementMode === 'orbit' ? (
        <OrbitControls
          enableDamping
          dampingFactor={0.08}
          minDistance={3}
          maxDistance={30}
          minPolarAngle={Math.PI / 8}
          maxPolarAngle={Math.PI / 2.2}
          enablePan={true}
          panSpeed={0.8}
          rotateSpeed={0.6}
          zoomSpeed={0.8}
          target={[0, 1, 0]}
        />
      ) : null}
      {/* En modo avatar, la cámara es controlada por WalkableAvatar */}

      {/* Sistema astronómico-geométrico vivo - DESHABILITADO en modo avatar */}
      <AstronomicalSystem
        location={location}
        enabled={movementMode === 'orbit'}
        showGeometry={showGeometryField}
        onDayNightChange={onDayNightChange}
        onSolarUpdate={onSolarUpdate}
        solarState={solarState}
        isDay={isDay}
        showTrajectory={true}
      />

      {/* Iluminación cinematográfica - adaptada al bioma */}
      <LightingSystem
        biomeType={biome.type}
        solarDirection={solarDirection}
        enableShadows={true}
        sunIntensity={2.5}
        hemisphereIntensity={1.2}
      />

      {/* Sistema de entorno (cielo, niebla, agua) */}
      <EnvironmentSystem
        isDay={isDay}
        skyColor={skyColor}
        fogColor={fogColor}
        stormDarkness={
          weather.storm || weather.tornado ? 0.7 : 
          weather.rainHeavy || weather.lightning ? 0.5 : 
          0
        }
        fogDensity={isIceBiome ? 0.012 : 0.008}
        showWater={!isIceBiome}
        waterPosition={[0, -0.5, 0]}
        waterSize={150}
        waterColor="#1e3a5f"
      />

      {/* Terreno - adaptado al bioma (no lazy porque necesita ref) */}
      {isIceBiome ? (
        <IceTerrain location={location} ref={terrainRef} />
      ) : (
        <VolcanicTerrain location={location} ref={terrainRef} />
      )}
      
      {/* Terreno mejorado con DEM real - se superpone al terreno procedural */}
      {enhancedTerrainEnabled && (
        <EnhancedTerrain
          location={location}
          enabled={enhancedTerrainEnabled}
          radius={0.05}
          resolution={256}
          exaggeration={terrainExaggeration || 1.5}
          enableLOD={terrainLOD !== false}
          enableHydrography={false}
          onLoadingChange={onTerrainLoadingChange}
        />
      )}

      {/* Grid sutil para referencia de movimiento - OCULTO */}
      <gridHelper 
        args={[200, 100, '#3a3a3a', '#2a2a2a']} 
        position={[0, 0.01, 0]}
        material-opacity={0}
        material-transparent={true}
        visible={false}
      />

      {/* Sistema climático completo */}
      <WeatherSystem weather={weather} isIceBiome={isIceBiome} />

      {/* Elementos del entorno: rocas y vegetación - dinámicos según ubicación */}
      <EnvironmentElements location={location} />

      {/* Modelo 3D o Avatar según modo */}
      {movementMode === 'avatar' ? (
        <WalkableAvatar 
          key={avatarModel}  // Key para forzar re-mount cuando cambia el modelo
          modelPath={avatarModel}
          terrainRef={terrainRef}
          solarDirection={solarDirection}
          isDay={isDay}
          showCosmicEffects={true}
        />
      ) : (
        <ModelViewer modelPath={avatarModel} ref={modelRef} />
      )}
      
      {/* Colisiones básicas ya no son necesarias, WalkableAvatar las maneja */}
      
      {/* Info del sitio */}
      {site && (
        <SiteInfo site={site} />
      )}
      
      {/* Capturar referencias */}
      <CameraCapture onReady={onCameraReady} />
      <ModelCapture onLoaded={onModelLoaded} />
      
      {/* Zoom cinematográfico al entrar - SOLO en modo órbita */}
      {movementMode === 'orbit' && <CinematicZoom />}

      {/* Post-processing modular */}
      <PostProcessingSystem
        enableBloom={true}
        enableVignette={true}
        bloomIntensity={0.3}
        vignetteIntensity={0.4}
      />
    </Canvas>
  )
}

// Zoom cinematográfico - SOLO en modo órbita
function CinematicZoom() {
  const { camera } = useThree()
  const startPos = useRef(new THREE.Vector3(15, 10, 15))
  const targetPos = useRef(new THREE.Vector3(5, 3, 5))
  const progress = useRef(0)
  const [isActive, setIsActive] = useState(true)

  useFrame((state, delta) => {
    if (progress.current < 1 && isActive) {
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

// Elementos decorativos del entorno - DINÁMICOS según ubicación
function EnvironmentElements({ location }: { location?: { lat: number, lon: number } | null }) {
  // Generar seed basado en coordenadas para consistencia
  const seed = useMemo(() => {
    if (!location) return 0
    return Math.floor(location.lat * 1000 + location.lon * 1000)
  }, [location?.lat, location?.lon])
  
  // Determinar bioma según ubicación
  const biome = useMemo(() => {
    if (!location) return 'temperate'
    const absLat = Math.abs(location.lat)
    
    if (absLat < 10) return 'tropical'
    if (absLat > 20 && absLat < 35) return 'desert'
    if (absLat > 60) return 'arctic'
    return 'temperate'
  }, [location])
  
  // Generar posiciones aleatorias basadas en seed
  const elements = useMemo(() => {
    const random = (index: number) => {
      const x = Math.sin(seed + index * 12.9898) * 43758.5453
      return x - Math.floor(x)
    }
    
    // Cantidad según bioma
    const counts: Record<string, Record<string, number>> = {
      tropical: { trees: 15, bushes: 20, rocks: 10, palms: 8, flowers: 25 },
      temperate: { trees: 12, bushes: 15, rocks: 15, logs: 5, flowers: 15 },
      desert: { trees: 3, bushes: 5, rocks: 25, cacti: 12, crystals: 8 },
      arctic: { trees: 5, bushes: 8, rocks: 30, crystals: 5, flowers: 5 }
    }
    
    const count = counts[biome] || counts.temperate
    
    const items: any[] = []
    let index = 0
    
    // Generar árboles
    for (let i = 0; i < count.trees; i++) {
      const angle = random(index++) * Math.PI * 2
      const radius = 15 + random(index++) * 30
      const x = Math.cos(angle) * radius + (random(index++) - 0.5) * 10
      const z = Math.sin(angle) * radius + (random(index++) - 0.5) * 10
      const height = 1.5 + random(index++) * 2.0
      items.push({ type: 'tree', x, z, height, rotation: random(index++) * Math.PI * 2 })
    }
    
    // Generar arbustos
    for (let i = 0; i < count.bushes; i++) {
      const angle = random(index++) * Math.PI * 2
      const radius = 10 + random(index++) * 35
      const x = Math.cos(angle) * radius + (random(index++) - 0.5) * 8
      const z = Math.sin(angle) * radius + (random(index++) - 0.5) * 8
      const scale = 0.3 + random(index++) * 0.5
      items.push({ type: 'bush', x, z, scale })
    }
    
    // Generar rocas
    for (let i = 0; i < count.rocks; i++) {
      const angle = random(index++) * Math.PI * 2
      const radius = 12 + random(index++) * 35
      const x = Math.cos(angle) * radius + (random(index++) - 0.5) * 10
      const z = Math.sin(angle) * radius + (random(index++) - 0.5) * 10
      const scale = 0.2 + random(index++) * 0.6
      items.push({ type: 'rock', x, z, scale, rotation: random(index++) * Math.PI * 2 })
    }
    
    // Elementos específicos por bioma
    if (biome === 'tropical' && count.palms) {
      for (let i = 0; i < count.palms; i++) {
        const angle = random(index++) * Math.PI * 2
        const radius = 18 + random(index++) * 25
        const x = Math.cos(angle) * radius
        const z = Math.sin(angle) * radius
        const height = 2.5 + random(index++) * 1.5
        items.push({ type: 'palm', x, z, height })
      }
    }
    
    if (biome === 'desert' && count.cacti) {
      for (let i = 0; i < count.cacti; i++) {
        const angle = random(index++) * Math.PI * 2
        const radius = 15 + random(index++) * 30
        const x = Math.cos(angle) * radius
        const z = Math.sin(angle) * radius
        const height = 1.0 + random(index++) * 2.0
        items.push({ type: 'cactus', x, z, height })
      }
    }
    
    if (biome === 'temperate' && count.logs) {
      for (let i = 0; i < count.logs; i++) {
        const angle = random(index++) * Math.PI * 2
        const radius = 20 + random(index++) * 25
        const x = Math.cos(angle) * radius
        const z = Math.sin(angle) * radius
        items.push({ type: 'log', x, z, rotation: random(index++) * Math.PI * 2 })
      }
    }
    
    if (count.flowers) {
      for (let i = 0; i < count.flowers; i++) {
        const angle = random(index++) * Math.PI * 2
        const radius = 8 + random(index++) * 35
        const x = Math.cos(angle) * radius + (random(index++) - 0.5) * 5
        const z = Math.sin(angle) * radius + (random(index++) - 0.5) * 5
        const scale = 0.1 + random(index++) * 0.15
        const colorIndex = Math.floor(random(index++) * 4)
        items.push({ type: 'flower', x, z, scale, colorIndex })
      }
    }
    
    if (count.crystals) {
      for (let i = 0; i < count.crystals; i++) {
        const angle = random(index++) * Math.PI * 2
        const radius = 20 + random(index++) * 25
        const x = Math.cos(angle) * radius
        const z = Math.sin(angle) * radius
        const scale = 0.3 + random(index++) * 0.5
        items.push({ type: 'crystal', x, z, scale, rotation: random(index++) * Math.PI })
      }
    }
    
    return items
  }, [seed, biome])

  return (
    <group>
      {elements.map((item, i) => {
        switch (item.type) {
          case 'tree':
            return (
              <group key={`tree-${i}`} position={[item.x, 0, item.z]}>
                {/* Tronco */}
                <mesh position={[0, item.height, 0]} castShadow receiveShadow>
                  <cylinderGeometry args={[0.15 * item.height, 0.2 * item.height, item.height * 2, 8]} />
                  <meshStandardMaterial color="#4a3520" roughness={0.95} />
                </mesh>
                {/* Copa */}
                <mesh position={[0, item.height * 2 + item.height * 1.25, 0]} castShadow receiveShadow>
                  <coneGeometry args={[item.height * 1.2, item.height * 2.5, 8]} />
                  <meshStandardMaterial color="#2d5016" roughness={0.8} />
                </mesh>
              </group>
            )
          
          case 'palm':
            return (
              <group key={`palm-${i}`} position={[item.x, 0, item.z]}>
                {/* Tronco curvo */}
                <mesh position={[0, item.height * 1.5, 0]} castShadow receiveShadow>
                  <cylinderGeometry args={[0.12, 0.15, item.height * 3, 8]} />
                  <meshStandardMaterial color="#8b6f47" roughness={0.9} />
                </mesh>
                {/* Hojas (4 direcciones) */}
                {[0, 1, 2, 3].map(dir => (
                  <mesh 
                    key={dir}
                    position={[
                      Math.cos(dir * Math.PI / 2) * 0.5,
                      item.height * 3,
                      Math.sin(dir * Math.PI / 2) * 0.5
                    ]}
                    rotation={[Math.PI / 6, dir * Math.PI / 2, 0]}
                    castShadow
                  >
                    <boxGeometry args={[0.3, 2, 0.1]} />
                    <meshStandardMaterial color="#2d5016" roughness={0.7} />
                  </mesh>
                ))}
              </group>
            )
          
          case 'cactus':
            return (
              <group key={`cactus-${i}`} position={[item.x, 0, item.z]}>
                {/* Cuerpo principal */}
                <mesh position={[0, item.height, 0]} castShadow receiveShadow>
                  <cylinderGeometry args={[0.2, 0.25, item.height * 2, 8]} />
                  <meshStandardMaterial color="#3a5a2a" roughness={0.8} />
                </mesh>
                {/* Brazos laterales */}
                <mesh position={[-0.4, item.height * 0.8, 0]} rotation={[0, 0, Math.PI / 4]} castShadow>
                  <cylinderGeometry args={[0.15, 0.18, item.height * 0.8, 6]} />
                  <meshStandardMaterial color="#3a5a2a" roughness={0.8} />
                </mesh>
              </group>
            )
          
          case 'bush':
            return (
              <mesh 
                key={`bush-${i}`}
                position={[item.x, item.scale * 0.4, item.z]}
                castShadow
                receiveShadow
              >
                <sphereGeometry args={[item.scale, 8, 8]} />
                <meshStandardMaterial color="#2d5016" roughness={0.9} />
              </mesh>
            )
          
          case 'rock':
            return (
              <mesh 
                key={`rock-${i}`}
                position={[item.x, 0, item.z]}
                rotation={[0, item.rotation, 0]}
                castShadow
                receiveShadow
              >
                <dodecahedronGeometry args={[item.scale, 0]} />
                <meshStandardMaterial color="#3a2a1a" roughness={0.95} metalness={0.05} />
              </mesh>
            )
          
          case 'log':
            return (
              <mesh 
                key={`log-${i}`}
                position={[item.x, 0.2, item.z]}
                rotation={[Math.PI / 2, 0, item.rotation]}
                castShadow
                receiveShadow
              >
                <cylinderGeometry args={[0.3, 0.35, 2, 8]} />
                <meshStandardMaterial color="#4a3520" roughness={0.95} />
              </mesh>
            )
          
          case 'flower':
            const flowerColors = ['#ff6b9d', '#ffd93d', '#a8e6cf', '#c7b3ff']
            return (
              <group key={`flower-${i}`} position={[item.x, 0, item.z]}>
                {/* Tallo */}
                <mesh position={[0, item.scale * 2, 0]}>
                  <cylinderGeometry args={[0.02, 0.02, item.scale * 4, 4]} />
                  <meshStandardMaterial color="#2d5016" />
                </mesh>
                {/* Flor */}
                <mesh position={[0, item.scale * 4, 0]} castShadow>
                  <sphereGeometry args={[item.scale, 6, 6]} />
                  <meshStandardMaterial 
                    color={flowerColors[item.colorIndex]} 
                    emissive={flowerColors[item.colorIndex]}
                    emissiveIntensity={0.2}
                  />
                </mesh>
              </group>
            )
          
          case 'crystal':
            return (
              <mesh 
                key={`crystal-${i}`}
                position={[item.x, item.scale * 0.8, item.z]}
                rotation={[0, item.rotation, 0]}
                castShadow
                receiveShadow
              >
                <coneGeometry args={[item.scale * 0.5, item.scale * 1.5, 6]} />
                <meshStandardMaterial 
                  color="#88ccff" 
                  metalness={0.3}
                  roughness={0.2}
                  transparent={true}
                  opacity={0.8}
                  emissive="#88ccff"
                  emissiveIntensity={0.3}
                />
              </mesh>
            )
          
          default:
            return null
        }
      })}
    </group>
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
    
    loggers.world.debug('Simulación solar:', {
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


// Avenger Espacial controlado por mouse
function SpaceUfo() {
  const ufoRef = useRef<THREE.Group>(null)
  const sunLightRef = useRef<THREE.DirectionalLight>(null)
  const { camera, size, scene: threeScene } = useThree()
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
  
  // Cargar modelo del Avenger
  const { scene } = useGLTF(getAssetPath('/avenger_01.glb'))
  
  // Capturar movimiento del mouse
  useEffect(() => {
    const handleMouseMove = (event: MouseEvent) => {
      // Convertir coordenadas del mouse a coordenadas normalizadas (-1 a 1)
      setMousePosition({
        x: (event.clientX / size.width) * 2 - 1,
        y: -(event.clientY / size.height) * 2 + 1
      })
    }
    
    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [size])
  
  // Actualizar posición del Avenger para seguir el mouse
  useFrame(() => {
    if (!ufoRef.current) return
    
    // Crear un raycaster desde la cámara hacia la posición del mouse
    const raycaster = new THREE.Raycaster()
    raycaster.setFromCamera(new THREE.Vector2(mousePosition.x, mousePosition.y), camera)
    
    // Calcular punto en el espacio a una distancia fija de la cámara
    const distance = 10 // Distancia desde la cámara
    const targetPosition = raycaster.ray.origin.clone().add(
      raycaster.ray.direction.multiplyScalar(distance)
    )
    
    // Suavizar movimiento del Avenger hacia la posición objetivo
    ufoRef.current.position.lerp(targetPosition, 0.1)
    
    // Hacer que el OVNI mire hacia donde se mueve
    if (raycaster.ray.direction.length() > 0) {
      const lookAtPos = ufoRef.current.position.clone().add(raycaster.ray.direction)
      ufoRef.current.lookAt(lookAtPos)
    }
    
    // Calcular escala basada en distancia a planetas REALES en la escena
    let minDistance = Infinity
    const ufoPosition = ufoRef.current.position
    
    // Buscar todos los meshes de planetas en la escena
    threeScene.traverse((object) => {
      // Buscar objetos que sean planetas (tienen geometría de esfera)
      if (object instanceof THREE.Mesh && object.geometry instanceof THREE.SphereGeometry) {
        // Calcular distancia al OVNI
        const dist = ufoPosition.distanceTo(object.getWorldPosition(new THREE.Vector3()))
        if (dist < minDistance) {
          minDistance = dist
        }
      }
    })
    
    // Calcular escala: 
    // OVNI con tamaño base 3 veces Mercurio (0.38 * 3 = 1.14)
    // - Lejos de planetas (>50 unidades): escala 1.14 (3 veces Mercurio)
    // - Cerca de planetas (<5 unidades): escala 0.0285 (40 veces más pequeño)
    const maxDistance = 50 // Distancia donde empieza a reducirse
    const minDistanceThreshold = 5 // Distancia mínima donde alcanza el tamaño mínimo
    
    const normalScale = 1.14 // 3 veces el tamaño de Mercurio (0.38 * 3)
    const minScale = 0.0285 // 40 veces más pequeño (1.14 / 40)
    
    let targetScale = normalScale // Escala normal
    if (minDistance < maxDistance) {
      // Interpolación suave entre escala normal y escala mínima
      const t = Math.max(0, Math.min(1, (maxDistance - minDistance) / (maxDistance - minDistanceThreshold)))
      targetScale = normalScale - (t * (normalScale - minScale))
    }
    
    // Suavizar cambio de escala
    const currentScale = ufoRef.current.scale.x
    const newScale = currentScale + (targetScale - currentScale) * 0.05
    ufoRef.current.scale.setScalar(newScale)
    
    // Actualizar luz del Sol para que apunte desde el Sol (0,0,0) hacia el OVNI
    if (sunLightRef.current) {
      const sunPosition = new THREE.Vector3(0, 0, 0)
      const ufoPos = ufoRef.current.position.clone()
      const direction = ufoPos.sub(sunPosition).normalize()
      
      // Posicionar la luz en dirección opuesta al OVNI (desde el Sol)
      const lightDistance = 50
      sunLightRef.current.position.copy(direction.multiplyScalar(-lightDistance))
    }
  })
  
  return (
    <group ref={ufoRef} position={[0, 0, 10]}>
      <primitive object={scene} scale={1.37} />
      
      {/* Iluminación del Sol */}
      <directionalLight 
        ref={sunLightRef}
        intensity={2.5} 
        color="#fff5e6"
        castShadow
        shadow-mapSize-width={1024}
        shadow-mapSize-height={1024}
      />
      
      {/* Luces de relleno */}
      <ambientLight intensity={0.2} />
      <pointLight position={[10, 10, 10]} intensity={0.3} color="#ffffff" />
    </group>
  )
}

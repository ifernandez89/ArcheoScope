'use client'

import { useState, useRef, useEffect, useMemo, useCallback } from 'react'
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
import { WorldCore } from '../engines/WorldCore'
import { getProceduralAudio } from '../systems/ProceduralAudio'
import { getClimateAudio } from '../systems/ClimateAudioSystem'

// ðŸ—ºï¸ SISTEMA DE TERRENO MEJORADO
import EnhancedTerrain from './EnhancedTerrain'
import TerrainControl from './TerrainControl'

// ðŸŒ³ MODELOS 3D DE VEGETACIÃ“N Y ROCAS
import Tree3DModel, { type TreeType } from './Tree3DModel'
import Rock3DModel from './Rock3DModel'
import PumaPunkuBlock from './PumaPunkuBlock'
import PumaPunkuStructure from './PumaPunkuStructure'
import SelectableObject from './SelectableObject'
import TerrainClickReceiver from './TerrainClickReceiver'
import { ObjectSelectionProvider, useObjectSelection } from './ObjectSelectionContext'

// ðŸŽ® SISTEMAS DE PERFORMANCE
import EngineIntegration from './EngineIntegration'

// ðŸ”¥ SISTEMAS MODULARES LAZY-LOADED
import {
  LightingSystem,
  WeatherSystem,
  EnvironmentSystem,
  PostProcessingSystem,
  AstronomicalSystem
} from '@/utils/lazy-systems'

// ðŸŽ¨ NUEVA ARQUITECTURA: UI Systems Layer
import UISystems from './layers/UISystems'
import AmbientAudio from './AmbientAudio'
import AmbientParticles from './AmbientParticles'
import CinematicZoom from './CinematicZoom'
import SiteInfo from './SiteInfo'
import SolarSimulation from './SolarSimulation'
import SpaceUfo from './SpaceUfo'
import PumaPunkuScene from './PumaPunkuScene'
import EnvironmentElements, { EnvironmentElementsWithTrees } from './EnvironmentElements'

interface ImmersiveSceneProps {
  onModelLoaded?: (model: THREE.Object3D) => void
  onCameraReady?: (camera: THREE.Camera) => void
  onModeChange?: (mode: 'globe' | 'transition' | 'model' | 'exploration') => void
  spaceUfoActive?: boolean
  spaceUfoNumber?: number
}

// Constantes de clima fuera del componente para estabilidad de closures
const DEFAULT_STORM_WEATHER: WeatherState = {
  snow: false, rainLight: false, rainModerate: false, rainHeavy: true,
  wind: true, fog: false, storm: true, lightning: true,
  tornado: false, clouds: true, earthquake: false
}

const CALM_WEATHER: WeatherState = {
  snow: false, rainLight: false, rainModerate: false, rainHeavy: false,
  wind: false, fog: false, storm: false, lightning: false,
  tornado: false, clouds: false, earthquake: false
}

export default function ImmersiveScene({ onModelLoaded, onCameraReady, onModeChange, spaceUfoActive = false, spaceUfoNumber = 1 }: ImmersiveSceneProps) {
  const [mode, setMode] = useState<'globe' | 'transition' | 'model' | 'exploration'>('globe')
  const [selectedModel, setSelectedModel] = useState<string>(getAssetPath('/moai.glb'))
  const [avatarModel, setAvatarModel] = useState<string>(getAssetPath('/ufo_1.glb')) // UFO 1 por defecto
  const [currentUfo, setCurrentUfo] = useState<number>(1) // UFO actual
  const [selectedLocation, setSelectedLocation] = useState<{ lat: number, lon: number } | null>(null)
  const [selectedSite, setSelectedSite] = useState<ArchaeologicalSite | null>(null)
  // Sitios donde ya se descubrió la estructura megalítica — persiste durante la sesión
  const discoveredSites = useRef<Set<string>>(new Set())
  // Ref al sitio actual para evitar stale closure en handleBlockMoved
  const selectedSiteRef = useRef<ArchaeologicalSite | null>(null)
  const [movementMode, setMovementMode] = useState<'orbit' | 'avatar'>('avatar') // Modo avatar por defecto
  const [showLocationInfo, setShowLocationInfo] = useState(false)
  const [showGeometryField, setShowGeometryField] = useState(true) // Activado por defecto
  const [showUfoSelector, setShowUfoSelector] = useState(false) // Dropdown de UFOs
  const [isDay, setIsDay] = useState(true) // Estado dÃ­a/noche
  const [weather, setWeather] = useState<WeatherState>(DEFAULT_STORM_WEATHER) // Estado del clima
  // Secuencia de clima al mover un bloque de Puma Punku
  // Mantener ref sincronizado con el estado
  useEffect(() => {
    selectedSiteRef.current = selectedSite
  }, [selectedSite])

  const handleBlockMoved = useCallback(() => {
    const siteId = selectedSiteRef.current?.id
    // Marcar este sitio como descubierto
    if (siteId) discoveredSites.current.add(siteId)
    // 1. Activar terremoto inmediatamente (coincide con inicio del fade-in de la estructura)
    setWeather(prev => ({ ...prev, earthquake: true }))
    // 2. Después de ~3.2s (duración del fade-in), calma total
    setTimeout(() => {
      setWeather(CALM_WEATHER)
    }, 3200)
  }, [])

  const [solarDirection, setSolarDirection] = useState({ x: 0, y: 1, z: 0 }) // DirecciÃ³n del sol como objeto plano
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

  // 🎵 Estado del audio
  const [audioEnabled, setAudioEnabled] = useState(false)
  const audioGenerator = getProceduralAudio()

  // 🎵 Habilitar audio automáticamente en primera interacción
  useEffect(() => {
    if (audioEnabled) return

    const enableAudioOnInteraction = async () => {
      try {
        await audioGenerator.enable()
        setAudioEnabled(true)
        loggers.world.info('🔊 Audio habilitado automáticamente')
        
        // Remover listeners después de habilitar
        window.removeEventListener('click', enableAudioOnInteraction)
        window.removeEventListener('keydown', enableAudioOnInteraction)
      } catch (error) {
        loggers.world.error('Error habilitando audio:', error)
      }
    }

    // Escuchar primera interacción
    window.addEventListener('click', enableAudioOnInteraction, { once: true })
    window.addEventListener('keydown', enableAudioOnInteraction, { once: true })

    return () => {
      window.removeEventListener('click', enableAudioOnInteraction)
      window.removeEventListener('keydown', enableAudioOnInteraction)
    }
  }, [audioEnabled, audioGenerator])

  // Notificar cambios de modo al padre
  useEffect(() => {
    if (onModeChange) {
      onModeChange(mode)
    }
  }, [mode, onModeChange])

  // 🎯 WORLDMANAGER: Garantizar solo 1 mundo activo
  useEffect(() => {
    if (mode === 'globe') {
      WorldCore.setActiveWorld('globe', undefined, { type: 'globe' })
    } else if (mode === 'model') {
      WorldCore.setActiveWorld('terrain', undefined, { 
        type: 'terrain',
        location: selectedLocation || undefined
      })
    }
    // mode === 'transition' no registra mundo (estado intermedio)
    
    // Cleanup al desmontar el componente completo
    return () => {
      loggers.world.info('🗑️ ImmersiveScene desmontado, limpiando mundos...')
      // No dispose aquí porque React maneja el desmontaje de Canvas
    }
  }, [mode, selectedLocation])

  // Sincronizar UFO seleccionado desde el globo
  useEffect(() => {
    // Sincronizar al inicio o cuando cambia
    setCurrentUfo(spaceUfoNumber)
    setAvatarModel(getAssetPath(`/ufo_${spaceUfoNumber}.glb`))
  }, [spaceUfoNumber])



  // Manejar click en sitio arqueolÃ³gico
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
    
    setWeather(discoveredSites.current.has(site.id) ? CALM_WEATHER : DEFAULT_STORM_WEATHER)
    setMode('model')
    
    loggers.world.info('Teletransporte a sitio arqueolÃ³gico completado')
  }

  // Manejar click en ubicaciÃ³n del globo
  const handleLocationClick = async (lat: number, lon: number) => {
    loggers.world.info(`Iniciando teletransporte a: lat=${lat.toFixed(4)}, lon=${lon.toFixed(4)}`)
    
    setSelectedLocation({ lat, lon })
    setSelectedModel(getAssetPath('/moai.glb'))
    setSelectedSite(null)
    setMode('transition')
    
    // TransiciÃ³n cinematogrÃ¡fica de 2 segundos
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Cambiar a modo modelo
    setWeather(DEFAULT_STORM_WEATHER)
    setMode('model')
    
    loggers.world.info('Teletransporte completado', { lat, lon })
  }

  // Volver al globo
  const handleBackToGlobe = async () => {
    // Silenciar todo el audio climático antes de salir
    getClimateAudio().updateWeather({ rain: 0, wind: 0, tornado: 0, snow: 0, thunder: false })
    setWeather(CALM_WEATHER)
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

  // Cambiar UFO en modo exploración
  const handleUfoChange = (ufoNumber: number) => {
    const newPath = getAssetPath(`/ufo_${ufoNumber}.glb`)
    console.log('🛸 Cambiando UFO:', ufoNumber, 'Path:', newPath)
    setCurrentUfo(ufoNumber)
    setAvatarModel(newPath)
  }

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      {/* Input de coordenadas */}
      <CoordinateInput 
        onCoordinateSubmit={handleLocationClick}
        currentLocation={selectedLocation}
      />

      {/* InformaciÃ³n de ubicaciÃ³n (desplegable) */}
      {mode === 'model' && showLocationInfo && (
        <LocationInfo 
          location={selectedLocation}
          site={selectedSite}
        />
      )}

      {/* Indicador de transiciÃ³n cinematogrÃ¡fica */}
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
            ðŸŒ
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
              ðŸ“ Lat: {selectedLocation.lat.toFixed(4)}Â° | Lon: {selectedLocation.lon.toFixed(4)}Â°
            </div>
          )}
          {selectedSite && (
            <div style={{
              color: '#fbbf24',
              fontSize: '12px',
              marginTop: '8px'
            }}>
              {selectedSite.culture} â€¢ {selectedSite.period}
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
            ðŸŒ Volver al Globo
          </button>

                    {/* BotÃ³n para mostrar/ocultar informaciÃ³n de ubicaciÃ³n */}
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
            ðŸ“ {showLocationInfo ? 'Ocultar Info' : 'Mostrar Info'}
          </button>

          {/* Selector de UFO en modo avatar */}
          {movementMode === 'avatar' && (
            <div style={{ position: 'relative' }}>
              <button
                onClick={() => setShowUfoSelector(!showUfoSelector)}
                style={{
                  padding: '12px 24px',
                  background: 'rgba(139, 92, 246, 0.9)',
                  border: '1px solid rgba(255,255,255,0.3)',
                  borderRadius: '8px',
                  color: 'white',
                  fontSize: '14px',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  transition: 'all 0.2s',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
                  width: '100%'
                }}
                onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(139, 92, 246, 1)'}
                onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(139, 92, 246, 0.9)'}
              >
                ðŸ
              </button>

              {/* Dropdown de UFOs */}
              {showUfoSelector && (
                <div style={{
                  position: 'absolute',
                  top: '100%',
                  left: 0,
                  marginTop: '4px',
                  background: 'rgba(0, 0, 0, 0.95)',
                  backdropFilter: 'blur(10px)',
                  borderRadius: '8px',
                  border: '1px solid rgba(255,255,255,0.2)',
                  overflow: 'hidden',
                  zIndex: 2000,
                  minWidth: '200px'
                }}>
                  {[1, 2, 3, 4, 5].map(ufoNum => (
                    <button
                      key={ufoNum}
                      onClick={() => {
                        handleUfoChange(ufoNum)
                        setShowUfoSelector(false)
                      }}
                      style={{
                        width: '100%',
                        padding: '8px 12px',
                        background: currentUfo === ufoNum ? 'rgba(139, 92, 246, 0.5)' : 'transparent',
                        border: 'none',
                        borderRadius: '4px',
                        color: 'white',
                        fontSize: '13px',
                        cursor: 'pointer',
                        textAlign: 'left',
                        transition: 'background 0.2s'
                      }}
                      onMouseEnter={(e) => {
                        if (currentUfo !== ufoNum) {
                          e.currentTarget.style.background = 'rgba(139, 92, 246, 0.3)'
                        }
                      }}
                      onMouseLeave={(e) => {
                        if (currentUfo !== ufoNum) {
                          e.currentTarget.style.background = 'transparent'
                        }
                      }}
                    >
                      ðŸ
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}
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
          <span>ðŸš¶ W/S - Adelante/AtrÃ¡s</span>
          <span>A/D - Izquierda/Derecha</span>
          <span>Q/E - Rotar</span>
          <span>ðŸš€ SHIFT + Mouseâ†• - Control de DirecciÃ³n</span>
        </div>
      )}

      {/* Escena 3D */}
      {mode === 'globe' ? (
        <GlobeScene 
          onLocationClick={handleLocationClick}
          onSiteClick={handleSiteClick}
          markerPosition={selectedLocation}
          spaceUfoActive={spaceUfoActive}
          spaceUfoNumber={spaceUfoNumber}
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
          onBlockMoved={handleBlockMoved}
        />
      ) : null}

      {/* Control de clima */}
      {mode === 'model' && (
        <WeatherControl onWeatherChange={setWeather} initialWeather={weather} />
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



// Escena del globo
function GlobeScene({ 
  onLocationClick,
  onSiteClick,
  markerPosition,
  spaceUfoActive = false,
  spaceUfoNumber = 1
}: { 
  onLocationClick: (lat: number, lon: number) => void
  onSiteClick: (site: ArchaeologicalSite) => void
  markerPosition?: { lat: number, lon: number } | null
  spaceUfoActive?: boolean
  spaceUfoNumber?: number
}) {
  return (
    <Canvas
      camera={{ position: [0, 0, 15], fov: 50 }}
      style={{ 
        background: '#000',
        cursor: spaceUfoActive ? 'none' : 'default' // Ocultar cursor cuando Avenger estÃ¡ activo
      }}
    >
      {/* ðŸŽ® SISTEMAS DE PERFORMANCE - ÃšNICO useFrame */}
      <EngineIntegration />
      
      <PerspectiveCamera makeDefault position={[0, 0, 15]} fov={50} />
      <OrbitControls
        enableDamping
        dampingFactor={0.05}
        minDistance={8}
        maxDistance={450} // Aumentado para ver Ã³rbita completa de Marte (304 unidades)
        autoRotate={false}
      />
      
      {/* Sistema de Zoom Narrativo */}
      <NarrativeZoomContent 
        onLocationClick={onLocationClick}
        markerPosition={markerPosition}
      />
      
      {/* Avenger Espacial controlado por mouse */}
      {spaceUfoActive && (
        <SpaceUfo key={spaceUfoNumber} ufoNumber={spaceUfoNumber} />
      )}
      
      {/* Marcadores de sitios arqueolÃ³gicos - Temporalmente deshabilitados */}
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
      {/* Fondo de la VÃ­a LÃ¡ctea - Esfera envolvente con textura */}
      <MilkyWayBackground />
      
      {/* Estrellas procedurales */}
      <Stars />
      
      {/* Sistema Solar Realista con posiciones astronÃ³micas reales */}
      <RealisticSolarSystem 
        onLocationClick={onLocationClick}
        markerPosition={markerPosition}
      />
    </>
  )
}

// Escena del modelo con zoom cinematogrÃ¡fico
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
  onTerrainLoadingChange,
  onBlockMoved
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
  onBlockMoved?: () => void
}) {
  const terrainRef = useRef<THREE.Mesh>(null)
  const modelRef = useRef<THREE.Group>(null)
  const [obstacles, setObstacles] = useState<THREE.Object3D[]>([])
  // Detectar bioma basado en ubicaciÃ³n
  const biome = useMemo(() => {
    if (!location) return { type: 'default' as const, name: 'GenÃ©rico', description: '', temperature: 20, humidity: 50 }
    return detectBiome(location.lat, location.lon)
  }, [location])
  
  const isIceBiome = biome.type === 'ice'
  
  // Colores dinÃ¡micos segÃºn bioma
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
  
  // Actualizar obstÃ¡culos cuando el modelo cargue
  useEffect(() => {
    if (modelRef.current) {
      setObstacles([modelRef.current])
    }
  }, [modelRef.current])
  
  return (
    <ObjectSelectionProvider onBlockMoved={onBlockMoved}>
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
      {/* ðŸŽ® SISTEMAS DE PERFORMANCE - ÃšNICO useFrame */}
      <EngineIntegration />
      
      <PerspectiveCamera makeDefault position={[8, 4, 8]} fov={60} />
      
      {/* Controles segÃºn modo */}
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
      {/* En modo avatar, la cÃ¡mara es controlada por WalkableAvatar */}

      {/* Sistema astronÃ³mico-geomÃ©trico vivo - DESHABILITADO en modo avatar */}
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

      {/* IluminaciÃ³n cinematogrÃ¡fica - adaptada al bioma */}
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

      {/* Sistema climÃ¡tico completo */}
      <WeatherSystem weather={weather} isIceBiome={isIceBiome} />

      {/* Drone atmosférico - activo en todos los modos */}
      <AmbientAudio />

      {/* Elementos del entorno: rocas y vegetaciÃ³n - NO renderizar sobre ocÃ©ano */}
      {!isIceBiome && biome.type !== 'ocean' && (
        <EnvironmentElementsWithTrees location={location} />
      )}

      {/* Modelo 3D o Avatar segÃºn modo */}
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
      
      {/* Colisiones bÃ¡sicas ya no son necesarias, WalkableAvatar las maneja */}
      
      {/* Info del sitio */}
      {site && (
        <SiteInfo site={site} />
      )}

      {/* 🗿 Escena de Puma Punku - estructura + bloques dispersos */}
      {(site?.id === 'puma-punku' || (
        location &&
        Math.abs(location.lat - (-16.5616)) < 0.05 &&
        Math.abs(location.lon - (-68.6795)) < 0.05
      )) && (
        <PumaPunkuScene />
      )}
      
      {/* Capturar referencias */}
      <CameraCapture onReady={onCameraReady} />
      <ModelCapture onLoaded={onModelLoaded} />
      
      {/* Zoom cinematogrÃ¡fico al entrar - SOLO en modo Ã³rbita */}
      {movementMode === 'orbit' && <CinematicZoom />}

      {/* Post-processing modular */}
      <PostProcessingSystem
        enableBloom={true}
        enableVignette={true}
        bloomIntensity={0.3}
        vignetteIntensity={0.4}
      />

      {/* Receptor de clicks en terreno para mover objetos seleccionados */}
      <TerrainClickReceiver />
    </Canvas>
    </ObjectSelectionProvider>
  )
}


// Capturar cámara
function CameraCapture({ onReady }: { onReady?: (camera: THREE.Camera) => void }) {
  const { camera } = useThree()
  useEffect(() => {
    if (camera && onReady) onReady(camera)
  }, [camera, onReady])
  return null
}

// Capturar modelo
function ModelCapture({ onLoaded }: { onLoaded?: (model: THREE.Object3D) => void }) {
  const { scene } = useThree()
  useEffect(() => {
    const model = scene.children.find(child => child.type === 'Group' && child.children.length > 0)
    if (model && onLoaded) onLoaded(model)
  }, [scene, onLoaded])
  return null
}

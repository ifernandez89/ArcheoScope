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

// PartÃ­culas ambientales sutiles para sensaciÃ³n de movimiento
function AmbientParticles() {
  const particlesRef = useRef<THREE.Points>(null)
  
  const particlesGeometry = useMemo(() => {
    const geometry = new THREE.BufferGeometry()
    const count = 500  // Pocas partÃ­culas, muy sutiles
    const positions = new Float32Array(count * 3)
    
    for (let i = 0; i < count; i++) {
      const i3 = i * 3
      // Distribuir en un Ã¡rea amplia alrededor del jugador
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
  
  // AnimaciÃ³n sutil de flotaciÃ³n
  useFrame((state) => {
    if (particlesRef.current) {
      const positions = particlesRef.current.geometry.attributes.position.array as Float32Array
      
      for (let i = 0; i < positions.length; i += 3) {
        // Movimiento vertical lento
        positions[i + 1] += Math.sin(state.clock.elapsedTime + i) * 0.001
        
        // Si la partÃ­cula baja mucho, resetearla arriba
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

// Zoom cinematogrÃ¡fico - SOLO en modo Ã³rbita
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

// Elementos decorativos del entorno - DINÃMICOS segÃºn ubicaciÃ³n
// Escena completa de Puma Punku
function PumaPunkuScene() {
  const { blockMoved } = useObjectSelection()
  const extraBlocks: Array<{ pos: [number, number, number]; rot: number; id: string }> = [
    { id: 'pp-b1', pos: [-12, 0,   8], rot: 0.3 },
    { id: 'pp-b2', pos: [ 15, 0,  -6], rot: 1.1 },
    { id: 'pp-b3', pos: [ -8, 0, -18], rot: 2.0 },
    { id: 'pp-b4', pos: [ 20, 0,  14], rot: 0.7 },
    { id: 'pp-b5', pos: [-20, 0, -10], rot: 1.5 },
    { id: 'pp-b6', pos: [  6, 0,  22], rot: 0.9 },
    { id: 'pp-b7', pos: [-16, 0,  18], rot: 2.4 },
    { id: 'pp-b8', pos: [ 10, 0, -22], rot: 0.2 },
  ]
  return (
    <>
      <MovablePumaPunkuStructure revealed={blockMoved} />
      <MovablePumaPunkuBlock />
      {extraBlocks.map((b) => (
        <MovableExtraBlock key={b.id} id={b.id} position={b.pos} rotation={b.rot} />
      ))}
    </>
  )
}

// Estructura principal - fija, no movible
function MovablePumaPunkuStructure({ revealed = false }: { revealed?: boolean }) {
  return (
    <PumaPunkuStructure position={[8, 0, -8]} rotation={[0, Math.PI / 6, 0]} revealed={revealed} />
  )
}

// Bloque extra movible
function MovableExtraBlock({ id, position, rotation }: { id: string; position: [number, number, number]; rotation: number }) {
  const [pos, setPos] = useState<[number, number, number]>(position)
  const { notifyBlockMoved } = useObjectSelection()
  return (
    <SelectableObject id={id} position={pos} onMove={(p) => { setPos(p); notifyBlockMoved() }}>
      <PumaPunkuBlock position={[0, 0.3, 0]} scale={0.075} rotation={[0, rotation, 0]} />
    </SelectableObject>
  )
}


// Bloque de Puma Punku movible con seleccion
function MovablePumaPunkuBlock() {
  const [pos, setPos] = useState<[number, number, number]>([0, 0, 0])
  const { notifyBlockMoved } = useObjectSelection()
  return (
    <SelectableObject id="puma-punku-block" position={pos} onMove={(p) => { setPos(p); notifyBlockMoved() }}>
      <PumaPunkuBlock
        position={[0, 0.3, 0]}
        scale={0.075}
        rotation={[0, Math.PI / 4, 0]}
      />
    </SelectableObject>
  )
}

// Arbol movible con seleccion
function MovableTree({ id, initialPosition, scale, rotation, treeType }: {
  id: string; initialPosition: [number, number, number]; scale: number; rotation: number; treeType: any
}) {
  const [pos, setPos] = useState<[number, number, number]>(initialPosition)
  return (
    <SelectableObject id={id} position={pos} onMove={setPos}>
      <Tree3DModel position={[0, 0, 0]} scale={scale} rotation={rotation} treeType={treeType} />
    </SelectableObject>
  )
}

// Roca movible con seleccion
function MovableRock({ id, initialPosition, scale, rotation }: {
  id: string; initialPosition: [number, number, number]; scale: number; rotation: number
}) {
  const [pos, setPos] = useState<[number, number, number]>(initialPosition)
  return (
    <SelectableObject id={id} position={pos} onMove={setPos}>
      <Rock3DModel position={[0, 0, 0]} scale={scale} rotation={rotation} />
    </SelectableObject>
  )
}


// Wrapper que lee blockMoved DENTRO del ObjectSelectionProvider
function EnvironmentElementsWithTrees({ location }: { location?: { lat: number, lon: number } | null }) {
  const { blockMoved } = useObjectSelection()
  return <EnvironmentElements location={location} treeMultiplier={blockMoved ? 3 : 1} />
}

function EnvironmentElements({ location, treeMultiplier = 1 }: { location?: { lat: number, lon: number } | null, treeMultiplier?: number }) {
  // Generar seed basado en coordenadas para consistencia
  const seed = useMemo(() => {
    if (!location) return 0
    return Math.floor(location.lat * 1000 + location.lon * 1000)
  }, [location?.lat, location?.lon])
  
  // Determinar bioma segÃºn ubicaciÃ³n
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
    
    // Cantidad segÃºn bioma
    const counts: Record<string, Record<string, number>> = {
      tropical: { trees: 15, bushes: 20, rocks: 10, palms: 8, flowers: 25 },
      temperate: { trees: 12, bushes: 15, rocks: 15, logs: 5, flowers: 15 },
      desert: { trees: 3, bushes: 5, rocks: 25, cacti: 12, crystals: 8 },
      arctic: { trees: 5, bushes: 8, rocks: 30, crystals: 5, flowers: 5 }
    }
    
    const count = counts[biome] || counts.temperate
    
    const items: any[] = []
    let index = 0

    // Zonas ocupadas: [x, z, radioMinimo]
    // La estructura de Puma Punku está en [8, -8], radio de exclusión 12
    const occupied: Array<[number, number, number]> = [[8, -8, 12]]

    const isTooClose = (x: number, z: number, minDist: number): boolean => {
      for (const [ox, oz, r] of occupied) {
        const d = Math.sqrt((x - ox) ** 2 + (z - oz) ** 2)
        if (d < r) return true
      }
      return false
    }

    const registerPos = (x: number, z: number, r: number) => {
      occupied.push([x, z, r])
    }
    
    // Generar árboles (con multiplicador para post-descubrimiento)
    // Los árboles extra (treeMultiplier > 1) se colocan en radio mayor para no chocar con la estructura
    for (let i = 0; i < count.trees * treeMultiplier; i++) {
      const isExtra = i >= count.trees
      let x = 0, z = 0
      let attempts = 0
      // Intentar hasta 8 veces encontrar posición libre
      do {
        const angle = random(index++) * Math.PI * 2
        // Árboles extra: radio mínimo 35 para alejarlos del centro
        const minRadius = isExtra ? 35 : 15
        const radius = minRadius + random(index++) * 25
        x = Math.cos(angle) * radius + (random(index++) - 0.5) * 8
        z = Math.sin(angle) * radius + (random(index++) - 0.5) * 8
        attempts++
      } while (isTooClose(x, z, 5) && attempts < 8)
      
      // Altura real del Ã¡rbol en metros (entre 2 y 10 metros)
      const heightInMeters = 2 + random(index++) * 8
      
      // Seleccionar tipo de Ã¡rbol aleatorio (4 tipos disponibles)
      const treeTypeRandom = random(index++)
      let treeType: 'default' | 'tree1' | 'tree2' | 'tree3'
      if (treeTypeRandom < 0.25) treeType = 'default'
      else if (treeTypeRandom < 0.5) treeType = 'tree1'
      else if (treeTypeRandom < 0.75) treeType = 'tree2'
      else treeType = 'tree3'
      
      items.push({ 
        type: 'tree', 
        x, 
        z, 
        heightInMeters, 
        rotation: random(index++) * Math.PI * 2, 
        treeType 
      })
      registerPos(x, z, 4)
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
    
    // Elementos especÃ­ficos por bioma
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
  }, [seed, biome, treeMultiplier])

  return (
    <group>
      {elements.map((item, i) => {
        switch (item.type) {
          case 'tree':
            // Escala muy pequeÃ±a para modelos GLB de Blender
            // heightInMeters entre 2-10, multiplicado por 0.05 = escala entre 0.1-0.5
            return (
              <MovableTree
                key={`tree-${seed}-${i}`}
                id={`tree-${seed}-${i}`}
                initialPosition={[item.x, 0, item.z]}
                scale={item.heightInMeters * 0.05}
                rotation={item.rotation}
                treeType={item.treeType}
              />
            )
          
          case 'rock':
            return (
              <MovableRock
                key={`rock-${seed}-${i}`}
                id={`rock-${seed}-${i}`}
                initialPosition={[item.x, 0, item.z]}
                scale={item.scale * 0.5}
                rotation={item.rotation}
              />
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

// Capturar cÃ¡mara
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

// SimulaciÃ³n solar real basada en coordenadas
function SolarSimulation({ lat, lon }: { lat: number, lon: number }) {
  const lightRef = useRef<THREE.DirectionalLight>(null)
  
  useEffect(() => {
    if (!lightRef.current) return
    
    // Calcular posiciÃ³n solar basada en lat/lon y hora actual
    const now = new Date()
    const dayOfYear = Math.floor((now.getTime() - new Date(now.getFullYear(), 0, 0).getTime()) / 86400000)
    const hour = now.getHours() + now.getMinutes() / 60
    
    // DeclinaciÃ³n solar (simplificado)
    const declination = 23.45 * Math.sin((360 / 365) * (dayOfYear - 81) * Math.PI / 180)
    
    // Ãngulo horario
    const hourAngle = 15 * (hour - 12)
    
    // Altura solar
    const altitude = Math.asin(
      Math.sin(lat * Math.PI / 180) * Math.sin(declination * Math.PI / 180) +
      Math.cos(lat * Math.PI / 180) * Math.cos(declination * Math.PI / 180) * Math.cos(hourAngle * Math.PI / 180)
    ) * 180 / Math.PI
    
    // Azimut solar (simplificado)
    const azimuth = hourAngle
    
    // Convertir a posiciÃ³n 3D
    const distance = 15
    const x = distance * Math.cos(altitude * Math.PI / 180) * Math.sin(azimuth * Math.PI / 180)
    const y = distance * Math.sin(altitude * Math.PI / 180)
    const z = distance * Math.cos(altitude * Math.PI / 180) * Math.cos(azimuth * Math.PI / 180)
    
    lightRef.current.position.set(x, Math.max(y, 2), z)
    
    // Ajustar intensidad segÃºn altura solar
    const intensity = Math.max(0.3, Math.sin(altitude * Math.PI / 180) * 1.5)
    lightRef.current.intensity = intensity
    
    // Color segÃºn hora del dÃ­a
    const sunColor = altitude > 0 
      ? (altitude < 15 ? '#ff9966' : '#ffffff')  // Amanecer/atardecer vs mediodÃ­a
      : '#1a1a2e'  // Noche
    
    lightRef.current.color.set(sunColor)
    
    loggers.world.debug('SimulaciÃ³n solar:', {
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

// Info del sitio arqueolÃ³gico
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
        ðŸ›ï¸ {site.name}
      </div>
      <div style={{ fontSize: '11px', color: '#888', marginBottom: '6px' }}>
        {site.culture} â€¢ {site.period}
      </div>
      <div style={{ fontSize: '11px', color: '#ccc', lineHeight: '1.4' }}>
        {site.description}
      </div>
    </Html>
  )
}


// Avenger Espacial controlado por mouse
function SpaceUfo({ ufoNumber = 1 }: { ufoNumber?: number }) {
  const ufoRef = useRef<THREE.Group>(null)
  const sunLightRef = useRef<THREE.DirectionalLight>(null)
  const { camera, size, scene: threeScene } = useThree()
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
  
  // Cargar modelo del UFO seleccionado
  const { scene } = useGLTF(getAssetPath(`/ufo_${ufoNumber}.glb`))
  
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
  
  // Actualizar posiciÃ³n del Avenger para seguir el mouse
  useFrame(() => {
    if (!ufoRef.current) return
    
    // Crear un raycaster desde la cÃ¡mara hacia la posiciÃ³n del mouse
    const raycaster = new THREE.Raycaster()
    raycaster.setFromCamera(new THREE.Vector2(mousePosition.x, mousePosition.y), camera)
    
    // Calcular punto en el espacio a una distancia fija de la cÃ¡mara
    const distance = 10 // Distancia desde la cÃ¡mara
    const targetPosition = raycaster.ray.origin.clone().add(
      raycaster.ray.direction.multiplyScalar(distance)
    )
    
    // Suavizar movimiento del Avenger hacia la posiciÃ³n objetivo
    ufoRef.current.position.lerp(targetPosition, 0.1)
    
    // Hacer que el OVNI mire hacia donde se mueve (excepto UFO 1 y 5 que rotan)
    if (ufoNumber !== 1 && ufoNumber !== 5 && raycaster.ray.direction.length() > 0) {
      const lookAtPos = ufoRef.current.position.clone().add(raycaster.ray.direction)
      ufoRef.current.lookAt(lookAtPos)
    }
    
    // Rotación especial para UFO 1: gira sobre su propio eje (antihorario)
    if (ufoNumber === 1) {
      ufoRef.current.rotation.y += 0.01 // Velocidad de rotación reducida
    }
    
    // Rotación especial para UFO 5: gira sobre su propio eje (antihorario, mitad de velocidad)
    if (ufoNumber === 5) {
      ufoRef.current.rotation.y += 0.005 // Mitad de velocidad que UFO 1
    }
    
    // Calcular escala basada en distancia a planetas REALES en la escena
    let minDistance = Infinity
    const ufoPosition = ufoRef.current.position
    
    // Buscar todos los meshes de planetas en la escena
    threeScene.traverse((object) => {
      // Buscar objetos que sean planetas (tienen geometrÃ­a de esfera)
      if (object instanceof THREE.Mesh && object.geometry instanceof THREE.SphereGeometry) {
        // Calcular distancia al OVNI
        const dist = ufoPosition.distanceTo(object.getWorldPosition(new THREE.Vector3()))
        if (dist < minDistance) {
          minDistance = dist
        }
      }
    })
    
    // Calcular escala: 
    // OVNI con tamaÃ±o base 3 veces Mercurio (0.38 * 3 = 1.14)
    // - Lejos de planetas (>50 unidades): escala 1.14 (3 veces Mercurio)
    // - Cerca de planetas (<5 unidades): escala 0.0285 (40 veces mÃ¡s pequeÃ±o)
    const maxDistance = 50 // Distancia donde empieza a reducirse
    const minDistanceThreshold = 5 // Distancia mÃ­nima donde alcanza el tamaÃ±o mÃ­nimo
    
    const normalScale = 1.14 // 3 veces el tamaÃ±o de Mercurio (0.38 * 3)
    const minScale = 0.0285 // 40 veces mÃ¡s pequeÃ±o (1.14 / 40)
    
    let targetScale = normalScale // Escala normal
    if (minDistance < maxDistance) {
      // InterpolaciÃ³n suave entre escala normal y escala mÃ­nima
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
      
      // Posicionar la luz en direcciÃ³n opuesta al OVNI (desde el Sol)
      const lightDistance = 50
      sunLightRef.current.position.copy(direction.multiplyScalar(-lightDistance))
    }
  })
  
  return (
    <group ref={ufoRef} position={[0, 0, 10]}>
      <primitive object={scene} scale={1.37} />
      
      {/* IluminaciÃ³n del Sol */}
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




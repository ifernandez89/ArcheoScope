'use client'

import dynamic from 'next/dynamic'
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
const RealisticSolarSystem = dynamic(() => import('./RealisticSolarSystem'), { ssr: false })
import Stars from './Stars'
import { 
  useNarrativeZoom
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

// SISTEMA DE TERRENO MEJORADO
import EnhancedTerrain from './EnhancedTerrain'
import TerrainControl from './TerrainControl'

// MODELOS 3D DE VEGETACIÓN Y ROCAS
import Tree3DModel, { type TreeType } from './Tree3DModel'
import Rock3DModel from './Rock3DModel'
import PumaPunkuBlock from './PumaPunkuBlock'
import PumaPunkuStructure from './PumaPunkuStructure'
import SelectableObject from './SelectableObject'
import TerrainClickReceiver from './TerrainClickReceiver'
import { ObjectSelectionProvider, useObjectSelection } from './ObjectSelectionContext'

// SISTEMAS DE PERFORMANCE
import EngineIntegration from './EngineIntegration'

// SISTEMAS MODULARES LAZY-LOADED
import {
  LightingSystem,
  WeatherSystem,
  EnvironmentSystem,
  PostProcessingSystem,
  AstronomicalSystem
} from '@/utils/lazy-systems'

// UI Systems Layer
import UISystems from './layers/UISystems'
import AmbientAudio from './AmbientAudio'
import AmbientParticles from './AmbientParticles'
import CinematicZoom from './CinematicZoom'
import SiteInfo from './SiteInfo'
import SolarSimulation from './SolarSimulation'

// ESCENAS PESADAS - LAZY LOADING (solo se cargan cuando se necesitan)
const SpaceUfo = dynamic(() => import('./SpaceUfo'), { ssr: false })
const PumaPunkuScene = dynamic(() => import('./PumaPunkuScene'), { ssr: false })
const GizaScene = dynamic(() => import('./GizaScene'), { ssr: false })
const EasterIslandScene = dynamic(() => import('./EasterIslandScene'), { ssr: false })
const TeotihuacanScene = dynamic(() => import('./TeotihuacanScene'), { ssr: false })
const EnvironmentElements = dynamic(() => import('./EnvironmentElements'), { ssr: false, loading: () => null })

// COMPONENTES DE DIÁLOGO - LAZY LOADING
const ViracochaDialogue = dynamic(() => import('./ViracochaDialogue'), { ssr: false })
const SphinxInteractiveDialogue = dynamic(() => import('./SphinxInteractiveDialogue'), { ssr: false })
const DiscoveredItemInWorld = dynamic(() => import('./DiscoveredItemInWorld'), { ssr: false })
const ItemCollectedMessage = dynamic(() => import('./ItemCollectedMessage'), { ssr: false })
const Compass = dynamic(() => import('./Compass'), { ssr: false })
const CompassTracker = dynamic(() => import('./CompassTracker'), { ssr: false })
const CelestialOverlayHUD = dynamic(() => import('./CelestialOverlay').then(m => ({ default: m.CelestialOverlayHUD })), { ssr: false })
const BackgroundMountains = dynamic(() => import('./BackgroundMountains'), { ssr: false, loading: () => null })
const EnhancedMoon = dynamic(() => import('./EnhancedMoon'), { ssr: false })

// EnvironmentElementsWithTrees necesita el contexto, importar directamente
import { EnvironmentElementsWithTrees } from './EnvironmentElements'
import { loadPlayerState, savePlayerState, updatePlayerLocation } from '@/types/player'
import { loadGameSettings } from '@/types/gameSettings'
import { collectItem, interactWithNPC, loadMissionState, sphinxReceivePyramidion, hasSphinxReceivedPyramidion, clearWeather, isWeatherCleared, type MissionState } from '@/types/missionState'

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
  tornado: false, clouds: true, earthquake: false, visibleSun: false
}

const CALM_WEATHER: WeatherState = {
  snow: false, rainLight: false, rainModerate: false, rainHeavy: false,
  wind: false, fog: false, storm: false, lightning: false,
  tornado: false, clouds: false, earthquake: false, visibleSun: true
}

export default function ImmersiveScene({ onModelLoaded, onCameraReady, onModeChange, spaceUfoActive = false, spaceUfoNumber = 1 }: ImmersiveSceneProps) {
  // Cargar estado del jugador
  const playerState = loadPlayerState()
  
  // Cargar modo inicial según última ubicación
  const [mode, setMode] = useState<'globe' | 'transition' | 'model' | 'exploration'>(() => {
    if (playerState?.lastLocation && playerState.lastLocation.mode === 'model') {
      return 'model'
    }
    return 'globe'
  })
  
  const [selectedModel, setSelectedModel] = useState<string>(getAssetPath('/moai.glb'))
  
  // Cargar nave del jugador si existe, sino usar UFO 1 por defecto
  const [avatarModel, setAvatarModel] = useState<string>(() => {
    if (playerState?.ship?.model) {
      return getAssetPath(playerState.ship.model)
    }
    return getAssetPath('/ufo_1.glb')
  })
  
  const [currentUfo, setCurrentUfo] = useState<number>(() => {
    if (playerState?.ship?.id) {
      const ufoNum = parseInt(playerState.ship.id.split('_')[1])
      return ufoNum || 1
    }
    return 1
  })
  
  // Cargar última ubicación si existe
  const [selectedLocation, setSelectedLocation] = useState<{ lat: number, lon: number } | null>(() => {
    if (playerState?.lastLocation) {
      return { lat: playerState.lastLocation.lat, lon: playerState.lastLocation.lon }
    }
    return null
  })
  
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
  const [cameraRotation, setCameraRotation] = useState(0) // Rotación de la cámara para la brújula
  const [showSphinxDialogue, setShowSphinxDialogue] = useState(false) // Diálogo de la Esfinge en Giza
  
  // Mostrar información del jugador al cargar
  useEffect(() => {
    if (playerState) {
      console.log('🎮 Jugador cargado:', playerState.playerName)
      console.log('🛸 Nave:', playerState.ship.name)
      console.log('📊 Progreso:', playerState.progress)
    } else {
      console.log('⚠️ No hay estado de jugador guardado')
    }
    
    // Aplicar volumen guardado desde gameSettings
    const settings = loadGameSettings()
    const audioGenerator = getProceduralAudio()
    if (settings?.audio?.masterVolume !== undefined) {
      audioGenerator.setMasterVolume(settings.audio.masterVolume)
      console.log('🔊 Volumen aplicado al iniciar desde gameSettings:', settings.audio.masterVolume)
    }
  }, [])
  
  // Escuchar cambios en el volumen desde el menú
  useEffect(() => {
    const checkVolumeChanges = () => {
      // Cargar desde gameSettings (nueva fuente de verdad)
      const settings = loadGameSettings()
      if (settings?.audio?.masterVolume !== undefined) {
        const audioGenerator = getProceduralAudio()
        const currentVolume = audioGenerator.getMasterVolume()
        const savedVolume = settings.audio.masterVolume
        
        // Solo actualizar si cambió
        if (Math.abs(currentVolume - savedVolume) > 0.01) {
          audioGenerator.setMasterVolume(savedVolume)
          console.log('🔊 Volumen actualizado desde gameSettings:', savedVolume)
        }
      }
    }
    
    // Verificar cada 500ms si el volumen cambió
    const interval = setInterval(checkVolumeChanges, 500)
    return () => clearInterval(interval)
  }, [])
  
  // Secuencia de clima al mover un bloque de Puma Punku
  // Mantener ref sincronizado con el estado
  useEffect(() => {
    selectedSiteRef.current = selectedSite
  }, [selectedSite])

  const handleBlockMoved = useCallback(() => {
    const siteId = selectedSiteRef.current?.id
    // Marcar este sitio como descubierto
    if (siteId) discoveredSites.current.add(siteId)
    
    // Limpiar clima de Puma Punku
    clearWeather('pumaPunku')
    
    // 1. Activar terremoto inmediatamente (coincide con inicio del fade-in de la estructura)
    setWeather(prev => ({ ...prev, earthquake: true }))
    // 2. Después de ~3.2s (duración del fade-in), calma total
    setTimeout(() => {
      setWeather(CALM_WEATHER)
      console.log('☀️ Clima de Puma Punku desbloqueado')
    }, 3200)
  }, [])

  // Handler para recolectar el item
  const handleCollectItem = useCallback(() => {
    console.log('📦 Item recolectado!')
    setItemCollected(true)
    setShowCollectedMessage(true)
    
    // Guardar en sessionStorage
    sessionStorage.setItem('item_magna_bowl_collected', 'true')
  }, [])
  
  // Handler para recolectar el piramidón
  const handleCollectPyramidion = useCallback(() => {
    console.log('🔶 Piramidón recolectado!')
    
    // Registrar en el sistema de misiones
    collectItem('giza', 'pyramidion')
    
    // Guardar en sessionStorage que fue recolectado
    sessionStorage.setItem('item_pyramidion_collected', 'true')
    
    // NO colocar en la punta todavía - solo marcar como recolectado
    setPyramidionCollected(true)
    
    // Mostrar mensaje
    setShowCollectedMessage(true)
    setTimeout(() => setShowCollectedMessage(false), 3000)
    
    // Desencadenar secuencia de misión completada
    console.log('🗿 Iniciando secuencia de misión completada...')
    
    // 1. PRIMERO: Clima mejora inmediatamente
    clearWeather('giza')
    setWeather(CALM_WEATHER)
    console.log('☀️ Clima de Giza desbloqueado')
    
    // 2. SEGUNDO: Mini terremoto (500ms después del clima)
    setTimeout(() => {
      setWeather(prev => ({ ...prev, earthquake: true }))
      console.log('🌍 Mini terremoto activado')
      
      // 3. TERCERO: Terminar terremoto (3.2s)
      setTimeout(() => {
        setWeather(CALM_WEATHER)
        console.log('🌍 Terremoto finalizado - Misión completada')
      }, 3200)
    }, 500)
  }, [])
  
  // Handler para cuando se mueve la momia
  const handleMummyMoved = useCallback(() => {
    console.log('🏺 Momia movida! Revelando escarabajo...')
    setScarabDiscovered(true)
  }, [])
  
  // Handler para recolectar el escarabajo
  const handleCollectScarab = useCallback(() => {
    console.log('🪲 Escarabajo recolectado!')
    
    // Registrar en el sistema de misiones
    collectItem('giza', 'scarab')
    
    // Guardar en sessionStorage
    sessionStorage.setItem('item_scarab_collected', 'true')
    
    // Marcar como recolectado
    setScarabCollected(true)
    
    // Mostrar mensaje
    setShowCollectedMessage(true)
    setTimeout(() => setShowCollectedMessage(false), 3000)
    
    // INICIAR INUNDACIÓN
    console.log('🌊 Iniciando inundación de Giza...')
    // La inundación se maneja en GizaScene
  }, [])

  const [solarDirection, setSolarDirection] = useState({ x: 0, y: 1, z: 0 }) // DirecciÃ³n del sol como objeto plano
  const [solarState, setSolarState] = useState({
    altitude: 0,
    azimuth: 0,
    declination: 0,
    // Nuevas propiedades FASE 2
    season: 'spring' as 'spring' | 'summer' | 'autumn' | 'winter',
    dayOfYear: 1,
    precessionAngle: 0,
    planets: [] as any[],
    lunarState: null as any,
    eclipse: null as any,
    simulatedTime: new Date()
  })
  
  // Estado del terreno mejorado - DESHABILITADO (terreno procedural por defecto)
  const [enhancedTerrainEnabled] = useState(false)
  const [terrainExaggeration] = useState(1.5)
  const [terrainLOD] = useState(true)
  const [terrainLoading, setTerrainLoading] = useState(false)

  // 🎵 Estado del audio
  const [audioEnabled, setAudioEnabled] = useState(false)
  const audioGenerator = getProceduralAudio()

  // 🏺 Estado del item descubierto
  const [itemDiscovered, setItemDiscovered] = useState(false)
  const [itemCollected, setItemCollected] = useState(false)
  const [showCollectedMessage, setShowCollectedMessage] = useState(false)
  
  // 🗿 Estado del diálogo de Viracocha
  const [showViracochaDialogue, setShowViracochaDialogue] = useState(false)
  const [magnaBowlCollected, setMagnaBowlCollected] = useState(false)
  const [pyramidionCollected, setPyramidionCollected] = useState(false)
  const [pyramidionOnTop, setPyramidionOnTop] = useState(false) // Si el piramidón está en la punta
  const [scarabDiscovered, setScarabDiscovered] = useState(false) // Si se movió la momia
  const [scarabCollected, setScarabCollected] = useState(false) // Si se recogió el escarabajo

  // Verificar si la Magna Bowl fue recolectada
  useEffect(() => {
    const checkMagnaBowl = () => {
      if (typeof window !== 'undefined') {
        const collected = sessionStorage.getItem('item_magna_bowl_collected') === 'true'
        setMagnaBowlCollected(collected)
      }
    }
    
    // Verificar al montar y cada segundo
    checkMagnaBowl()
    const interval = setInterval(checkMagnaBowl, 1000)
    return () => clearInterval(interval)
  }, [])
  
  // Verificar si el Piramidón fue recolectado Y entregado a la Esfinge
  useEffect(() => {
    const checkPyramidion = () => {
      if (typeof window !== 'undefined') {
        // Verificar desde missionState (fuente de verdad)
        const missionState = loadMissionState()
        const collectedFromMissions = missionState.sites.giza.itemsCollected.includes('pyramidion')
        
        // También verificar sessionStorage para compatibilidad
        const collectedFromSession = sessionStorage.getItem('item_pyramidion_collected') === 'true'
        
        const collected = collectedFromMissions || collectedFromSession
        
        // Verificar si fue entregado a la Esfinge (desde missionState)
        const delivered = hasSphinxReceivedPyramidion()
        
        // Si fue entregado, el piramidón SIEMPRE debe estar visible en la punta
        // Si solo fue recolectado (no entregado), también debe estar visible
        if (collected || delivered) {
          setPyramidionCollected(true)
        }
      }
    }
    
    // Verificar al montar y cada segundo
    checkPyramidion()
    const interval = setInterval(checkPyramidion, 1000)
    return () => clearInterval(interval)
  }, [])
  

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



  // Función helper para determinar el sitio basado en coordenadas
  const getSiteNameFromCoordinates = (lat: number, lon: number): keyof MissionState['sites'] | null => {
    // Puma Punku
    if (Math.abs(lat - (-16.5616)) < 0.05 && Math.abs(lon - (-68.6795)) < 0.05) {
      return 'pumaPunku'
    }
    // Giza
    if (Math.abs(lat - 29.9792) < 0.05 && Math.abs(lon - 31.1342) < 0.05) {
      return 'giza'
    }
    // Lago Titicaca (subsitio de Puma Punku)
    if (lat > -16.5 && lat < -15.5 && lon > -70 && lon < -68.5) {
      return 'pumaPunku'
    }
    return null
  }

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
    
    // Determinar clima basado en si la misión está completada
    const siteName = getSiteNameFromCoordinates(site.lat, site.lon)
    const weatherCleared = siteName ? isWeatherCleared(siteName) : discoveredSites.current.has(site.id)
    setWeather(weatherCleared ? CALM_WEATHER : DEFAULT_STORM_WEATHER)
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
    
    // Guardar ubicación en el estado del jugador
    updatePlayerLocation(lat, lon, 'model')
    
    // TransiciÃ³n cinematogrÃ¡fica de 2 segundos
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Determinar clima basado en si la misión está completada
    const siteName = getSiteNameFromCoordinates(lat, lon)
    const weatherCleared = siteName ? isWeatherCleared(siteName) : false
    setWeather(weatherCleared ? CALM_WEATHER : DEFAULT_STORM_WEATHER)
    setMode('model')
    
    loggers.world.info('Teletransporte completado', { lat, lon })
  }

  // Volver al globo
  const handleBackToGlobe = async () => {
    // Silenciar todo el audio climático antes de salir
    getClimateAudio().updateWeather({ rain: 0, wind: 0, tornado: 0, snow: 0, thunder: false })
    setWeather(CALM_WEATHER)
    setMode('transition')
    
    // Guardar que volvió al globo
    updatePlayerLocation(0, 0, 'globe')
    
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

  // Cambiar UFO en modo exploración (para condiciones especiales del juego)
  const handleUfoChange = (ufoNumber: number) => {
    const newPath = getAssetPath(`/ufo_${ufoNumber}.glb`)
    console.log('🛸 Cambiando UFO:', ufoNumber, 'Path:', newPath)
    setCurrentUfo(ufoNumber)
    setAvatarModel(newPath)
    
    // Actualizar estado del jugador si existe
    const currentState = loadPlayerState()
    if (currentState) {
      // Mapeo de naves (debe coincidir con player-setup)
      const ships = [
        { id: 'ufo_1', name: '🌫️ Phantom', model: '/ufo_1.glb', specialty: 'Cloaking / Invisibilidad', description: 'Especialidad: infiltración y espionaje', ability: 'Habilidad principal: camuflaje óptico', missions: 'Tipo de misiones: infiltración, espionaje, recuperar artefactos, entrar a ruinas antiguas' },
        { id: 'ufo_2', name: '🛡️ Aegis', model: '/ufo_2.glb', specialty: 'Defensa / Campo EM', description: 'Especialidad: protección y control físico', ability: 'Habilidad principal: campo electromagnético', missions: 'Tipo de misiones: atravesar campos de asteroides, rescates, misiones de escolta, limpiar escombros espaciales' },
        { id: 'ufo_3', name: '⚡ Vector', model: '/ufo_3.glb', specialty: 'Velocidad / Teletransporte', description: 'Especialidad: movilidad extrema', ability: 'Habilidad principal: salto cuántico', missions: 'Tipo de misiones: carreras, persecuciones, exploración, entrega urgente' },
        { id: 'ufo_4', name: '🔬 Oracle', model: '/ufo_4.glb', specialty: 'Ciencia / Escaneo', description: 'Especialidad: conocimiento y análisis', ability: 'Habilidad principal: escáner cuántico', missions: 'Tipo de misiones: exploración planetaria, arqueología alienígena, investigación, cartografía' },
        { id: 'ufo_5', name: '💣 Titan', model: '/ufo_5.glb', specialty: 'Fuerza Bruta / Impacto', description: 'Especialidad: potencia y resistencia', ability: 'Habilidad principal: masa + potencia', missions: 'Tipo de misiones: combate, minería pesada, abrir rutas, destruir obstáculos' }
      ]
      
      const newShip = ships[ufoNumber - 1]
      if (newShip) {
        currentState.ship = newShip
        savePlayerState(currentState)
        console.log('💾 Nave actualizada en estado del jugador:', newShip.name)
      }
    }
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


          {/* Selector de UFO eliminado - ahora se configura en /player-setup */}
        </div>
      )}

      {/* Brújula astronómica - muestra el norte real basado en la rotación de la cámara */}
      {mode === 'model' && (
        <>
          <Compass rotation={cameraRotation} solarAzimuth={solarState.azimuth} />
        </>
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
          onSolarUpdate={(direction, altitude, azimuth, declination, fullState) => {
            setSolarDirection(direction)
            if (fullState) {
              // Usar estado completo del SolarEngine
              setSolarState({
                altitude,
                azimuth,
                declination,
                season: fullState.season || 'spring',
                dayOfYear: fullState.dayOfYear || 1,
                precessionAngle: fullState.precessionAngle || 0,
                planets: fullState.planets || [],
                lunarState: fullState.lunarState || null,
                eclipse: fullState.eclipse || null,
                simulatedTime: fullState.simulatedTime || new Date()
              })
            } else {
              // Fallback al formato anterior
              setSolarState({ 
                altitude, 
                azimuth, 
                declination,
                season: 'spring',
                dayOfYear: 1,
                precessionAngle: 0,
                planets: [],
                lunarState: null,
                eclipse: null,
                simulatedTime: new Date()
              })
            }
          }}
          weather={weather}
          enhancedTerrainEnabled={enhancedTerrainEnabled}
          terrainExaggeration={terrainExaggeration}
          terrainLOD={terrainLOD}
          onTerrainLoadingChange={setTerrainLoading}
          onBlockMoved={handleBlockMoved}
          itemDiscovered={itemDiscovered}
          itemCollected={itemCollected}
          onCollectItem={handleCollectItem}
          showCollectedMessage={showCollectedMessage}
          onCloseMessage={() => setShowCollectedMessage(false)}
          showViracochaDialogue={showViracochaDialogue}
          onViracochaSpeak={() => setShowViracochaDialogue(true)}
          onCloseViracochaDialogue={() => setShowViracochaDialogue(false)}
          onPortalEnter={() => handleLocationClick(-16.031003664299448, -69.49975772335767)}
          magnaBowlCollected={magnaBowlCollected}
          onCameraRotationChange={setCameraRotation}
          onSphinxClick={() => setShowSphinxDialogue(true)}
          onPyramidionCollect={handleCollectPyramidion}
          pyramidionCollected={pyramidionCollected}
          pyramidionOnTop={pyramidionOnTop}
          onMummyMoved={handleMummyMoved}
          onScarabCollect={handleCollectScarab}
          scarabDiscovered={scarabDiscovered}
          scarabCollected={scarabCollected}
        />
      ) : null}

      {/* Control de clima */}
      {mode === 'model' && (
        <WeatherControl onWeatherChange={setWeather} initialWeather={weather} />
      )}
      
      {/* Diálogo de la Esfinge - FUERA del Canvas */}
      {showSphinxDialogue && (
        <SphinxInteractiveDialogue
          pyramidionCollected={pyramidionCollected}
          hasReceivedPyramidion={hasSphinxReceivedPyramidion()}
          onClose={() => {
            setShowSphinxDialogue(false)
            // Registrar interacción con la Esfinge
            interactWithNPC('giza', 'sphinx')
            
            // Si tiene el piramidón y aún no se lo ha dado, marcarlo como entregado
            if (pyramidionCollected && !hasSphinxReceivedPyramidion()) {
              sphinxReceivePyramidion()
              console.log('🗿 La Esfinge agradece por devolver el piramidón')
              
              // REPLICAR EXACTAMENTE el comportamiento del commit anterior
              // Simplemente activar el estado que hace aparecer el piramidón
              setPyramidionOnTop(true)
              console.log('🔶 setPyramidionOnTop(true) - Piramidón debe aparecer en la punta')
            }
          }}
          onOptionSelected={(optionId) => {
            console.log(`🗿 Opción seleccionada: ${optionId}`)
          }}
        />
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
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <CelestialOverlayHUD />
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
        enableDamping={false}
        minDistance={8}
        maxDistance={8000} // Neptuno está a ~6010 unidades (30.05 AU × 200)
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
    </div>
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
  onBlockMoved,
  itemDiscovered,
  itemCollected,
  onCollectItem,
  showCollectedMessage,
  onCloseMessage,
  showViracochaDialogue,
  onViracochaSpeak,
  onCloseViracochaDialogue,
  onPortalEnter,
  magnaBowlCollected,
  onCameraRotationChange,
  onSphinxClick,
  onPyramidionCollect,
  pyramidionCollected,
  pyramidionOnTop,
  onMummyMoved,
  onScarabCollect,
  scarabDiscovered,
  scarabCollected
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
  solarState: { 
    altitude: number, 
    azimuth: number, 
    declination: number,
    season?: 'spring' | 'summer' | 'autumn' | 'winter',
    dayOfYear?: number,
    precessionAngle?: number,
    planets?: any[],
    lunarState?: any,
    eclipse?: any,
    simulatedTime?: Date
  }
  onSolarUpdate: (direction: { x: number, y: number, z: number }, altitude: number, azimuth: number, declination: number, fullState?: any) => void
  weather: WeatherState
  enhancedTerrainEnabled?: boolean
  terrainExaggeration?: number
  terrainLOD?: boolean
  onTerrainLoadingChange?: (loading: boolean) => void
  onBlockMoved?: () => void
  itemDiscovered?: boolean
  itemCollected?: boolean
  onCollectItem?: () => void
  showCollectedMessage?: boolean
  onCloseMessage?: () => void
  showViracochaDialogue?: boolean
  onViracochaSpeak?: () => void
  onCloseViracochaDialogue?: () => void
  onPortalEnter?: () => void
  magnaBowlCollected: boolean
  onCameraRotationChange?: (rotation: number) => void
  onSphinxClick?: () => void
  onPyramidionCollect?: () => void
  pyramidionCollected?: boolean
  pyramidionOnTop?: boolean
  onMummyMoved?: () => void
  onScarabCollect?: () => void
  scarabDiscovered?: boolean
  scarabCollected?: boolean
}) {
  const terrainRef = useRef<THREE.Mesh>(null)
  const modelRef = useRef<THREE.Group>(null)
  const [obstacles, setObstacles] = useState<THREE.Object3D[]>([])
  const avatarPositionRef = useRef(new THREE.Vector3())
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
    <>
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
      {/* 🎮 SISTEMAS DE PERFORMANCE - ÚNICO useFrame */}
      <EngineIntegration />
      
      {/* 🧭 Rastreador de rotación de cámara para la brújula */}
      {onCameraRotationChange && <CompassTracker onRotationChange={onCameraRotationChange} />}
      
      <PerspectiveCamera makeDefault position={[8, 4, 8]} fov={60} />
      
      {/* Controles segÃºn modo */}
      {movementMode === 'orbit' ? (
        <OrbitControls
          enableDamping={false}
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

      {/* Sistema astronómico-geométrico vivo - SOLO en modo órbita */}
      {movementMode === 'orbit' && (
        <AstronomicalSystem
          location={location}
          enabled={true}
          showGeometry={showGeometryField}
          onDayNightChange={onDayNightChange}
          onSolarUpdate={onSolarUpdate}
          solarState={solarState}
          isDay={isDay}
          showTrajectory={true}
        />
      )}
      
      {/* Luna mejorada con fases y eclipses - SOLO en modo órbita */}
      {movementMode === 'orbit' && solarState.lunarState && (
        <EnhancedMoon
          lunarState={solarState.lunarState}
          eclipse={solarState.eclipse}
          solarDirection={solarDirection}
          visible={true}
        />
      )}

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
        fogDensity={biome.type === 'altiplano' ? 0.004 : isIceBiome ? 0.012 : 0.008}
        showWater={!isIceBiome}
        waterPosition={[0, -0.5, 0]}
        waterSize={biome.type === 'altiplano' ? 350 : 150}
        waterColor={biome.type === 'altiplano' ? '#2a5a8f' : '#1e3a5f'}
      />

      {/* Terreno - adaptado al bioma (no lazy porque necesita ref) */}
      {isIceBiome ? (
        <IceTerrain location={location} ref={terrainRef} />
      ) : (
        <VolcanicTerrain location={location} ref={terrainRef} />
      )}
      
      {/* Montañas de fondo para altiplano */}
      <BackgroundMountains biomeType={biome.type} />
      
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
      <WeatherSystem weather={weather} isIceBiome={isIceBiome} solarDirection={solarDirection} />

      {/* Drone atmosférico - activo en todos los modos */}
      <AmbientAudio />

      {/* Elementos del entorno: rocas y vegetación - NO renderizar sobre océano ni en Giza */}
      {!isIceBiome && biome.type !== 'ocean' && !(
        location &&
        Math.abs(location.lat - 29.9792) < 0.05 &&
        Math.abs(location.lon - 31.1342) < 0.05
      ) && (
        <EnvironmentElementsWithTrees location={location} />
      )}

      {/* Modelo 3D o Avatar según modo */}
      {movementMode === 'avatar' ? (
        <WalkableAvatar 
          key={avatarModel}  // Key para forzar re-mount cuando cambia el modelo
          modelPath={avatarModel}
          terrainRef={terrainRef}
          solarDirection={solarDirection}
          isDay={isDay}
          showCosmicEffects={true}
          onPositionChange={(pos) => avatarPositionRef.current.copy(pos)}
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
        <PumaPunkuScene 
          onViracochaSpeak={onViracochaSpeak}
          onPortalEnter={onPortalEnter}
          avatarPositionRef={avatarPositionRef}
        />
      )}
      
      {/* 🏜️ Escena de Giza - Gran Pirámide alineada astronómicamente */}
      {(location &&
        Math.abs(location.lat - 29.9792) < 0.05 &&
        Math.abs(location.lon - 31.1342) < 0.05
      ) && (
        <GizaScene 
          key="giza-scene-permanent"
          avatarPositionRef={avatarPositionRef}
          onSphinxClick={onSphinxClick}
          onPyramidionCollect={onPyramidionCollect}
          pyramidionCollected={pyramidionCollected || false}
          pyramidionOnTop={pyramidionOnTop || false}
          onMummyMoved={onMummyMoved}
          onScarabCollect={onScarabCollect}
          scarabDiscovered={scarabDiscovered || false}
          scarabCollected={scarabCollected || false}
        />
      )}
      
      {/* 🗿 Escena de Isla de Pascua - Moai y Atlante "charlando" */}
      {(site?.id === 'rapa-nui-ahu-tongariki' || (
        location &&
        Math.abs(location.lat - (-27.1254)) < 0.05 &&
        Math.abs(location.lon - (-109.2778)) < 0.05
      )) && (
        <EasterIslandScene 
          avatarPositionRef={avatarPositionRef}
        />
      )}
      
      {/* 🏛️ Escena de Teotihuacán - Pirámide del Sol y Templo Mayor */}
      {(site?.id === 'teotihuacan' || (
        location &&
        Math.abs(location.lat - 19.6925) < 0.05 &&
        Math.abs(location.lon - (-98.8438)) < 0.05
      )) && (
        <TeotihuacanScene 
          avatarPositionRef={avatarPositionRef}
        />
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
      {/* Item descubierto flotando en el mundo - SIEMPRE VISIBLE en Lago Titicaca */}
      {!itemCollected && location && 
       location.lat > -16.5 && location.lat < -15.5 && 
       location.lon > -70 && location.lon < -68.5 && onCollectItem && (
        <DiscoveredItemInWorld
          modelPath={getAssetPath('/magna_bowl.glb')}
          position={[0, 0.5, 0]}
          onCollect={onCollectItem}
        />
      )}
    </Canvas>
    </ObjectSelectionProvider>
    
    {/* Mensaje de item recolectado - FUERA del Canvas */}
    {showCollectedMessage && onCloseMessage && (
      <ItemCollectedMessage onClose={onCloseMessage} />
    )}
    
    {/* Diálogo de Viracocha - FUERA del Canvas */}
    {showViracochaDialogue && onCloseViracochaDialogue && (
      <ViracochaDialogue
        message={magnaBowlCollected 
          ? "¡Gracias, viajero! Has traído lo que necesitaba." 
          : "¡Atraviesa el portal, y tráeme lo que necesito!"}
        onComplete={onCloseViracochaDialogue}
      />
    )}
    
    </>
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

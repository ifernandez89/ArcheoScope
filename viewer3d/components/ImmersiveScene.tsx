'use client'

import dynamic from 'next/dynamic'
import { useState, useRef, useEffect, useMemo, useCallback } from 'react'
import { Canvas, useThree, useFrame } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera, Html, useGLTF } from '@react-three/drei'
import * as THREE from 'three'
import CoordinateInput from './CoordinateInput'
import LocationInfo from './LocationInfo'
import WeatherControl, { type WeatherState } from './WeatherControl'
import SelectableObject from './SelectableObject'
import TerrainClickReceiver from './TerrainClickReceiver'
import { ObjectSelectionProvider, useObjectSelection } from './ObjectSelectionContext'
import EngineIntegration from './EngineIntegration'
import { ArcheoEngine, AvatarEngine, type ArchaeologicalSite } from '../engines'
import { getAssetPath } from '@/lib/paths'
import { loggers } from '@/core/Logger'
import { WorldCore } from '../engines/WorldCore'
import { getProceduralAudio } from '../systems/ProceduralAudio'
import { getClimateAudio } from '../systems/ClimateAudioSystem'
import { GRAPHICS_PRESETS } from '../systems/GraphicsPresets'
import { useNarrativeZoom } from './NarrativeZoom'
import { detectBiome, getSkyColorForBiome, getFogColorForBiome } from '@/utils/biome-detector'
import { loadPlayerState, savePlayerState, updatePlayerLocation } from '@/types/player'
import { loadGameSettings } from '@/types/gameSettings'
import { collectItem, interactWithNPC, loadMissionState, sphinxReceivePyramidion, hasSphinxReceivedPyramidion, clearWeather, isWeatherCleared, completeMission, failMission, resetMissionState, isMissionCompleted, type MissionState } from '@/types/missionState'

// SISTEMAS MODULARES LAZY-LOADED
import {
  LightingSystem,
  WeatherSystem,
  EnvironmentSystem,
  PostProcessingSystem,
  AstronomicalSystem
} from '@/utils/lazy-systems'

// GLOBO - componentes lazy (solo se usan en modo globo)
const Globe3D = dynamic(() => import('./Globe3D'), { ssr: false })
const Stars = dynamic(() => import('./Stars'), { ssr: false, loading: () => null })
const MilkyWayBackground = dynamic(() => import('./MilkyWayBackground'), { ssr: false, loading: () => null })
const SolarSystemIntegrated = dynamic(() => import('./SolarSystemIntegrated'), { ssr: false, loading: () => null })
const SimpleMoon = dynamic(() => import('./SimpleMoon'), { ssr: false, loading: () => null })
const Sun = dynamic(() => import('./Sun'), { ssr: false, loading: () => null })
const Mercury = dynamic(() => import('./Mercury'), { ssr: false, loading: () => null })
const Venus = dynamic(() => import('./Venus'), { ssr: false, loading: () => null })
const Mars = dynamic(() => import('./Mars'), { ssr: false, loading: () => null })
const PlanetaryOrbits = dynamic(() => import('./PlanetaryOrbits'), { ssr: false, loading: () => null })
const EarthOrbitWrapper = dynamic(() => import('./EarthOrbitWrapper'), { ssr: false, loading: () => null })
const LunarOrbitLine = dynamic(() => import('./LunarOrbitLine'), { ssr: false, loading: () => null })
const RealisticSolarSystem = dynamic(() => import('./RealisticSolarSystem'), { ssr: false })

// TERRENO - componentes lazy (solo se usan en modo terreno)
const WalkableAvatar = dynamic(() => import('./WalkableAvatar'), { ssr: false })
const ModelViewer = dynamic(() => import('./ModelViewer'), { ssr: false })
const ProceduralTerrain = dynamic(() => import('./ProceduralTerrain'), { ssr: false, loading: () => null })
const EnhancedTerrain = dynamic(() => import('./EnhancedTerrain'), { ssr: false, loading: () => null })
const Tree3DModel = dynamic(() => import('./Tree3DModel'), { ssr: false, loading: () => null })
const Rock3DModel = dynamic(() => import('./Rock3DModel'), { ssr: false, loading: () => null })
const PumaPunkuBlock = dynamic(() => import('./PumaPunkuBlock'), { ssr: false, loading: () => null })
const PumaPunkuStructure = dynamic(() => import('./PumaPunkuStructure'), { ssr: false, loading: () => null })
const AmbientMotion = dynamic(() => import('./AmbientMotion'), { ssr: false, loading: () => null })
const VolcanicTerrain = dynamic(() => import('./VolcanicTerrain'), { ssr: false, loading: () => null })
const IceTerrain = dynamic(() => import('./IceTerrain'), { ssr: false, loading: () => null })
const SiteMarkers = dynamic(() => import('./SiteMarkers'), { ssr: false, loading: () => null })
const BasicCollisions = dynamic(() => import('./BasicCollisions'), { ssr: false, loading: () => null })
const TerrainControl = dynamic(() => import('./TerrainControl'), { ssr: false, loading: () => null })
const SiteInfo = dynamic(() => import('./SiteInfo'), { ssr: false, loading: () => null })
const SolarSimulation = dynamic(() => import('./SolarSimulation'), { ssr: false, loading: () => null })
const AmbientAudio = dynamic(() => import('./AmbientAudio'), { ssr: false, loading: () => null })
const AmbientParticles = dynamic(() => import('./AmbientParticles'), { ssr: false, loading: () => null })
const CinematicZoom = dynamic(() => import('./CinematicZoom'), { ssr: false, loading: () => null })

// ESCENAS PESADAS - LAZY LOADING
const SpaceUfo = dynamic(() => import('./SpaceUfo'), { ssr: false })
const PumaPunkuScene = dynamic(() => import('./PumaPunkuScene'), { ssr: false })
const GizaScene = dynamic(() => import('./GizaScene'), { ssr: false })
const EasterIslandScene = dynamic(() => import('./EasterIslandScene'), { ssr: false })
const TeotihuacanScene = dynamic(() => import('./TeotihuacanScene'), { ssr: false })
const VeracruzScene = dynamic(() => import('./VeracruzScene'), { ssr: false })
const MictlanScene = dynamic(() => import('./MictlanScene'), { ssr: false })
const GobekliTepeScene = dynamic(() => import('./GobekliTepeScene'), { ssr: false })
const EnvironmentElements = dynamic(() => import('./EnvironmentElements'), { ssr: false, loading: () => null })
const Geoglyph = dynamic(() => import('./Geoglyph'), { ssr: false, loading: () => null })

// COMPONENTES DE DIÁLOGO - LAZY LOADING
const ViracochaDialogue = dynamic(() => import('./ViracochaDialogue'), { ssr: false })
const ViracochaInteractiveDialogue = dynamic(() => import('./ViracochaInteractiveDialogue'), { ssr: false })
const SphinxInteractiveDialogue = dynamic(() => import('./SphinxInteractiveDialogue'), { ssr: false })
const AkhenatonDialogue = dynamic(() => import('./AkhenatonDialogue'), { ssr: false })
const QuetzalcoatlDialogue = dynamic(() => import('./QuetzalcoatlDialogue'), { ssr: false })
const OlmecInteractiveDialogue = dynamic(() => import('./OlmecInteractiveDialogue'), { ssr: false })
const DiscoveredItemInWorld = dynamic(() => import('./DiscoveredItemInWorld'), { ssr: false })
const ItemCollectedMessage = dynamic(() => import('./ItemCollectedMessage'), { ssr: false })
import InventoryItem from './InventoryItem'
import DroppableItem from './DroppableItem'
import SolarAlignmentLines, { calcAlignments } from './SolarAlignmentLines'
const Compass = dynamic(() => import('./Compass'), { ssr: false })
const ShipAbilities = dynamic(() => import('./ShipAbilities'), { ssr: false })
const CompassTracker = dynamic(() => import('./CompassTracker'), { ssr: false })
const MobileTouchControls = dynamic(() => import('./MobileTouchControls'), { ssr: false })
const CelestialOverlayHUD = dynamic(() => import('./CelestialOverlay').then(m => ({ default: m.CelestialOverlayHUD })), { ssr: false })
const BackgroundMountains = dynamic(() => import('./BackgroundMountains'), { ssr: false, loading: () => null })
const EnhancedMoon = dynamic(() => import('./EnhancedMoon'), { ssr: false })

// EnvironmentElementsWithTrees necesita el contexto, importar directamente
import { EnvironmentElementsWithTrees } from './EnvironmentElements'
import GeoglyphDirect from './Geoglyph'

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
  tornado: false, clouds: true, earthquake: false, visibleSun: false,
  volcanicEruption: false
}

const CALM_WEATHER: WeatherState = {
  snow: false, rainLight: false, rainModerate: false, rainHeavy: false,
  wind: false, fog: false, storm: false, lightning: false,
  tornado: false, clouds: false, earthquake: false, visibleSun: true,
  volcanicEruption: false
}

// Teotihuacán: lluvia ligera (menos carga GPU, más apropiado para el bioma)
const TEOTIHUACAN_WEATHER: WeatherState = {
  snow: false, rainLight: true, rainModerate: false, rainHeavy: false,
  wind: true, fog: false, storm: false, lightning: false,
  tornado: false, clouds: true, earthquake: false, visibleSun: false,
  volcanicEruption: false
}

export default function ImmersiveScene({ onModelLoaded, onCameraReady, onModeChange, spaceUfoActive = false, spaceUfoNumber = 1 }: ImmersiveSceneProps) {
  // Detectar mobile
  const [isMobile, setIsMobile] = useState(false)
  useEffect(() => {
    const check = () => setIsMobile(
      /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768
    )
    check()
    window.addEventListener('resize', check)
    return () => window.removeEventListener('resize', check)
  }, [])

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
  // Ref para la posición del avatar (para soltar items)
  const mainAvatarPositionRef = useRef(new THREE.Vector3())
  // Ref para la ubicación actual (evita stale closures en toggleAbility)
  const selectedLocationRef = useRef<{ lat: number, lon: number } | null>(null)
  const [movementMode, setMovementMode] = useState<'orbit' | 'avatar'>('avatar') // Modo avatar por defecto
  const [showLocationInfo, setShowLocationInfo] = useState(false)
  const [showAlignmentLines, setShowAlignmentLines] = useState(false)

  // Calcular estado solar para el panel científico (independiente del modo de movimiento)
  const panelSolarState = useMemo(() => {
    if (!selectedLocation || !showLocationInfo) return null
    try {
      const { SolarEngine } = require('../engines/SolarEngine')
      const engine = new SolarEngine(selectedLocation.lat, selectedLocation.lon)
      return engine.calculateSolarState()
    } catch { return null }
  }, [selectedLocation?.lat, selectedLocation?.lon, showLocationInfo])
  const biome = useMemo(() => {
    if (!selectedLocation) return { type: 'default' as const, name: 'Genérico', description: '', temperature: 20, humidity: 50 }
    return detectBiome(selectedLocation.lat, selectedLocation.lon)
  }, [selectedLocation?.lat, selectedLocation?.lon])
  const [gameTimer, setGameTimer] = useState(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('game_timer_seconds')
      return saved ? parseInt(saved) : 0
    }
    return 0
  })
  const [showGeometryField, setShowGeometryField] = useState(true) // Activado por defecto
  const [showUfoSelector, setShowUfoSelector] = useState(false) // Dropdown de UFOs
  const [isDay, setIsDay] = useState(true)

  // Sincronizar isDay con el estado solar real — al cambiar ubicación y cada minuto
  useEffect(() => {
    if (!selectedLocation) return
    const update = () => {
      try {
        const { SolarEngine } = require('../engines/SolarEngine')
        const engine = new SolarEngine(selectedLocation.lat, selectedLocation.lon)
        const state = engine.calculateSolarState()
        setIsDay(state.isDay)
      } catch {}
    }
    update() // inmediato
    const interval = setInterval(update, 60000) // cada minuto
    return () => clearInterval(interval)
  }, [selectedLocation?.lat, selectedLocation?.lon])
  const [weather, setWeather] = useState<WeatherState>(DEFAULT_STORM_WEATHER) // Estado del clima
  const [cameraRotation, setCameraRotation] = useState(0) // Rotación de la cámara para la brújula
  const [showSphinxDialogue, setShowSphinxDialogue] = useState(false)
  const [showAkhenatonDialogue, setShowAkhenatonDialogue] = useState(false)

  // 🌬️ Viento aleatorio en escenas terrestres
  useEffect(() => {
    if (mode !== 'model') return

    let windTimer: ReturnType<typeof setTimeout>

    const scheduleWind = () => {
      // Esperar entre 20-60 segundos antes del próximo evento de viento
      const delay = (20 + Math.random() * 40) * 1000
      windTimer = setTimeout(() => {
        // 60% de probabilidad de que haya viento
        if (Math.random() < 0.6) {
          setWeather(prev => {
            // No activar si hay tormenta activa (ya tiene viento implícito)
            if (prev.storm || prev.volcanicEruption) return prev
            return { ...prev, wind: true }
          })
          // Duración del viento: 8-25 segundos
          const duration = (8 + Math.random() * 17) * 1000
          setTimeout(() => {
            setWeather(prev => ({ ...prev, wind: false }))
          }, duration)
        }
        scheduleWind() // programar el siguiente
      }, delay)
    }

    scheduleWind()
    return () => clearTimeout(windTimer)
  }, [mode])

  // ⏱️ Cronómetro de partida — incrementa cada segundo y persiste
  useEffect(() => {
    const interval = setInterval(() => {
      setGameTimer(prev => {
        const next = prev + 1
        localStorage.setItem('game_timer_seconds', String(next))
        return next
      })
    }, 1000)
    return () => clearInterval(interval)
  }, [])

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

  // Escuchar cambios de volumen - polling eficiente con ref para evitar re-renders
  useEffect(() => {
    let lastVolume = -1

    const applyVolume = (volume: number) => {
      // ProceduralAudio (clima, lluvia, viento)
      const audioGenerator = getProceduralAudio()
      audioGenerator.setMasterVolume(volume)

      // ClimateAudio (usa ProceduralAudio internamente, pero forzamos)
      getClimateAudio().setMasterVolume(volume)

      // HarmoniaMundi (música cósmica) - siempre guardar aunque no esté habilitado
      import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
        const harmonia = getHarmoniaMundi()
        harmonia.setMasterVolume(volume)
      })

      console.log('🔊 Volumen aplicado a todos los sistemas:', volume)
    }

    const checkVolumeChanges = () => {
      const settings = loadGameSettings()
      const savedVolume = settings?.audio?.masterVolume ?? 0.7
      if (Math.abs(savedVolume - lastVolume) > 0.005) {
        lastVolume = savedVolume
        applyVolume(savedVolume)
      }
    }

    // Aplicar inmediatamente al montar
    checkVolumeChanges()

    // Polling cada 1s (storage event no funciona en misma pestaña)
    const interval = setInterval(checkVolumeChanges, 1000)
    return () => clearInterval(interval)
  }, [])

  // Secuencia de clima al mover un bloque de Puma Punku
  // Mantener ref sincronizado con el estado
  useEffect(() => {
    selectedSiteRef.current = selectedSite
  }, [selectedSite])

  // Mantener ref de ubicación sincronizada para evitar stale closure en Oracle scanner
  useEffect(() => {
    selectedLocationRef.current = selectedLocation
  }, [selectedLocation])

  const handleBlockMoved = useCallback(() => {
    const siteId = selectedSiteRef.current?.id
    // Marcar este sitio como descubierto
    if (siteId) discoveredSites.current.add(siteId)

    // Completar misión de Puma Punku para que la lógica secuencial funcione correctamente
    completeMission('pumaPunku', 'reveal_structure')

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
    setMagnaBowlOriginalInInventory(true)
    setShowCollectedMessage(true)
    setTimeout(() => setShowCollectedMessage(false), 3000)

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
    console.log('Iniciando secuencia de misión completada...')

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
    // Verificar si se completaron las 5 misiones previas
    const ms = loadMissionState()
    const allMissionsComplete = ms.stats.totalMissionsCompleted >= 5

    if (allMissionsComplete) {
      console.log('🪲 Escarabajo recolectado legalmente! Añadiendo al inventario...')
      collectItem('giza', 'scarab')
      setScarabCollected(true)
      setScarabInInventory(true)
      setScarabOnGround(false)

      setShowCollectedMessage(true)
      setTimeout(() => setShowCollectedMessage(false), 3000)
    } else {
      console.log('🪲 Escarabajo ROBADO — castigo divino activado')

      collectItem('giza', 'scarab')
      failMission('giza', 'return_pyramidion')
      console.log('❌ Misión "Devolver el Piramidión" FALLIDA - El jugador robó el escarabajo sagrado')

      sessionStorage.setItem('item_scarab_collected', 'true')

      // Poner en inventario (aunque sea robado, lo tiene)
      setScarabCollected(true)
      setScarabInInventory(true)
      setScarabOnGround(false)

      // Bloquear navegación — el jugador no puede escapar de la inundación
      setScarabStolenFlood(true)

      setShowCollectedMessage(true)
      setTimeout(() => setShowCollectedMessage(false), 3000)

      // INICIAR INUNDACIÓN como castigo
      console.log('🌊 Iniciando inundación de Giza como castigo divino...')
      setWeather(prev => ({ ...prev, volcanicEruption: false, storm: true, rainHeavy: true }))
    }
  }, [])

  // Handler para recolectar la calavera de cristal
  const handleCollectSkull = useCallback(() => {
    const ms = loadMissionState()
    const allMissionsComplete = ms.stats.totalMissionsCompleted >= 5

    if (allMissionsComplete) {
      console.log('💀 Calavera de cristal recolectada legalmente! Añadiendo al inventario...')
      collectItem('easterIsland', 'crystal_skull')
      setSkullInInventory(true)
      setSkullOnGround(false)

      setShowCollectedMessage(true)
      setTimeout(() => setShowCollectedMessage(false), 3000)
    } else {
      console.log('💀 Calavera robada! DISPARANDO EVENTO DE ERUPCIÓN...')
      setWeather(prev => ({ ...prev, volcanicEruption: true }))
    }
  }, [])

  // Handler para click en Quetzalcoatl
  const handleQuetzalcoatlClick = useCallback(() => {
    console.log('🐍 Quetzalcoatl clickeado!')
    setShowQuetzalcoatlDialogue(true)
  }, [])

  // Handler cuando Quetzalcoatl pide la semilla
  const handleRequestCornSeed = useCallback(() => {
    console.log('🌽 Quetzalcoatl pide plantar la semilla!')
    setCornOnGround(true) // Aparece en el piso
  }, [])

  // Ref para saber si ya se mostró el mensaje de recolección del maíz
  const cornMessageShownRef = useRef(false)

  // Handler para recolectar la semilla de maíz del piso
  const handleCollectCornSeed = useCallback(() => {
    console.log('🌽 Semilla de maíz recogida del piso!')

    // Registrar en el sistema de misiones (solo la primera vez)
    if (!cornMessageShownRef.current) {
      collectItem('teotihuacan', 'corn_seed')
      // Mostrar mensaje solo la primera vez
      setShowCollectedMessage(true)
      setTimeout(() => setShowCollectedMessage(false), 3000)
      cornMessageShownRef.current = true
    }

    // Mover al inventario
    setCornOnGround(false)
    setCornInInventory(true)
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

  // Estado del diálogo de Viracocha
  const [showViracochaDialogue, setShowViracochaDialogue] = useState(false)
  const [showViracochaInteractive, setShowViracochaInteractive] = useState(false)
  const [magnaBowlCollected, setMagnaBowlCollected] = useState(false)
  const [magnaBowlThanked, setMagnaBowlThanked] = useState(() =>
    typeof window !== 'undefined' && localStorage.getItem('magna_bowl_thanked') === 'true'
  )
  const [magnaBowlLent, setMagnaBowlLent] = useState(false) // Fuente Magna prestada por Viracocha
  const [pyramidionCollected, setPyramidionCollected] = useState(false)
  const [pyramidionOnTop, setPyramidionOnTop] = useState(false) // Si el piramidón está en la punta
  const [scarabDiscovered, setScarabDiscovered] = useState(false) // Si se movió la momia
  const [scarabCollected, setScarabCollected] = useState(false) // Si se recogió el escarabajo (para erupción/lógica)
  const [scarabInInventory, setScarabInInventory] = useState(() => {
    if (typeof window !== 'undefined') return localStorage.getItem('inv_scarab') === 'true'
    return false
  })
  const [scarabOnGround, setScarabOnGround] = useState(false) // Para soltar/recoger
  const [scarabDropPosition, setScarabDropPosition] = useState<{ x: number, z: number } | null>(null)

  const [skullInInventory, setSkullInInventory] = useState(() => {
    if (typeof window !== 'undefined') return localStorage.getItem('inv_skull') === 'true'
    return false
  })
  const [skullOnGround, setSkullOnGround] = useState(false)
  const [skullDropPosition, setSkullDropPosition] = useState<{ x: number, z: number } | null>(null)

  // 🌞 Tonatiuh — figurilla oculta en el Mictlán
  const [tonatiuhInInventory, setTonatiuhInInventory] = useState(() => {
    if (typeof window !== 'undefined') return localStorage.getItem('inv_tonatiuh') === 'true'
    return false
  })
  const [tonatiuhOnGround, setTonatiuhOnGround] = useState(false)
  const [tonatiuhDropPosition, setTonatiuhDropPosition] = useState<{ x: number, z: number } | null>(null)
  // 🪨 Roca — recolectable del entorno, solo una a la vez
  const [rockInInventory, setRockInInventory] = useState(() => {
    if (typeof window !== 'undefined') return localStorage.getItem('inv_rock') === 'true'
    return false
  })
  const [rockOnGround, setRockOnGround] = useState(false)
  const [rockDropPosition, setRockDropPosition] = useState<{ x: number, z: number } | null>(null)

  // 🏺 Fuente Magna prestada por Viracocha
  const [magnaBowlLentInInventory, setMagnaBowlLentInInventory] = useState(() => {
    if (typeof window !== 'undefined') return localStorage.getItem('inv_magna_bowl') === 'true'
    return false
  })
  const [magnaBowlOnGround, setMagnaBowlOnGround] = useState(false)
  const [magnaBowlDropPosition, setMagnaBowlDropPosition] = useState<{ x: number, z: number } | null>(null)

  // 🏺 Fuente Magna original del lago Titicaca — no se puede soltar hasta entregar a Viracocha
  const [magnaBowlOriginalInInventory, setMagnaBowlOriginalInInventory] = useState(() => {
    if (typeof window !== 'undefined') return localStorage.getItem('inv_magna_bowl_original') === 'true'
    return false
  })

  // 💾 Persistir inventario en localStorage
  useEffect(() => {
    if (typeof window === 'undefined') return
    localStorage.setItem('inv_scarab', String(scarabInInventory))
    localStorage.setItem('inv_skull', String(skullInInventory))
    localStorage.setItem('inv_tonatiuh', String(tonatiuhInInventory))
    localStorage.setItem('inv_rock', String(rockInInventory))
    localStorage.setItem('inv_magna_bowl', String(magnaBowlLentInInventory))
    localStorage.setItem('inv_magna_bowl_original', String(magnaBowlOriginalInInventory))
  }, [scarabInInventory, skullInInventory, tonatiuhInInventory, rockInInventory, magnaBowlLentInInventory, magnaBowlOriginalInInventory])

  // 🛸 Estado de habilidades de nave
  const [abilityActive, setAbilityActive] = useState(false)
  const [abilityCooldown, setAbilityCooldown] = useState(false)

  // 💀 Detectar si estamos en Mictlán (atrapados hasta 10 apariciones)
  const isMictlanLocation = !!(selectedLocation &&
    Math.abs(selectedLocation.lat - 0.0001) < 0.01 &&
    Math.abs(selectedLocation.lon - 0.0001) < 0.01)
  const [mictlanCompleted, setMictlanCompleted] = useState(false)
  const trappedInMictlan = isMictlanLocation && !mictlanCompleted

  // 🌊 Inundación por robo del escarabajo — bloquea navegación
  const [scarabStolenFlood, setScarabStolenFlood] = useState(false)

  // 🔒 Bloquear navegación: Mictlán o inundación por robo
  const navigationBlocked = trappedInMictlan || scarabStolenFlood

  const [isShaking, setIsShaking] = useState(false)
  const [scannedEntity, setScannedEntity] = useState<{ name: string, desc: string } | null>(null)

  // 📝 Datos de escaneo (Nave 4 - Oracle)
  const SCAN_DATA = {
    'Viracocha': "Arquitecto de la realidad tangible. Su función es el ordenamiento del caos primordial a través de la geometría.",
    'Sphinx': "Eterno observador del tiempo. Su silencio guarda la respuesta a la pregunta que aún no has formulado.",
    'Ramesses': "El poder de la voluntad manifestada en piedra. La verdadera herencia no es el monumento, sino la visión.",
    'Hatshepsut': "Navegante de los mares internos. La autoridad nace de la sabiduría profunda, no de la imposición.",
    'Akhenaten': "Foco de la unidad absoluta. Mira hacia la fuente única de luz que anima toda existencia consciente.",
    'Mummy': "Recipiente de la memoria biológica. El cuerpo es el templo que guarda el código del ser a través de los eones.",
    'Hotu Matua': "Rostros que miran al infinito. Su silencio es comunicación; su inmovilidad es el eje de un mundo en cambio.",
    'Quetzalcoatl': "Unión de la materia terrestre y el espíritu celeste. La evolución es el equilibrio entre tus alas y tus raíces.",
    'Atlante': "Pilar del conocimiento estelar. Sostiene la carga del cielo para que la tierra pueda florecer en paz.",
    'Mictlantecuhtli': "Transformador de la energía vital. El fin de un ciclo es solo la transmutación necesaria para el nuevo inicio.",
    'FuenteMagna': "Recipiente sagrado de origen desconocido. Sus inscripciones invocan a una diosa olvidada. Fue creado para canalizar energías cósmicas en rituales de alineación planetaria.",
    'CalendarioMaya': "Registro de ciclos solares grabado en piedra. Cada giro codifica el pulso del cosmos: nacimiento, apogeo, disolución. El tiempo no avanza — regresa.",
    'Merkaba': "Campo de luz giratoria en perfecta resonancia. Vehículo de ascensión entre planos de existencia. Su activación sincroniza la red energética planetaria.",
    'Araña': "Figura trazada sobre la tierra árida, visible solo desde las alturas. Sus líneas conectan puntos del cielo con puntos del suelo. Guardiana de portales que el ojo humano no puede ver.",
    'Cóndor': "Mensajero entre mundos, grabado en la tierra con precisión imposible. Sus alas abarcan un horizonte que ningún ser humano podría trazar desde el suelo. Marca los ejes invisibles del altiplano.",
    'Monos': "Figura espiral trazada con una sola línea continua. Su cola describe la rotación de energías cósmicas. Guardián del agua y los ciclos de la vida.",
    'Colibrí': "Símbolo de resurrección solar grabado en la tierra. Su pico apunta hacia un punto del horizonte que solo se alinea en momentos precisos del año. Mensajero entre el sol y la tierra.",
    'Perro': "Guardián del umbral entre el mundo visible y el invisible. Su figura marca el paso hacia territorios que los vivos no deberían cruzar sin guía.",
    'Ballena': "Una de las figuras más antiguas grabadas en la tierra. Representa el origen de la vida y los ciclos oceánicos que gobiernan el planeta. Su boca abierta devora el tiempo.",
    'Astronauta': "Figura humanoide que mira hacia el cielo con el brazo levantado. Su forma sugiere algo que los trazadores de líneas conocían y que nosotros apenas comenzamos a intuir.",
    'MonolitoGobekli': "Monolito de origen lejano, traído aquí intencionalmente. Representa una deidad de forma híbrida — entre lo animal y lo divino. Su presencia en este lugar es un anacronismo sagrado: un nexo entre dos puntos del tiempo que nunca deberían haberse tocado.",
    'Árbol': "Organismo vivo que conecta tres mundos: sus raíces penetran el inframundo, su tronco habita la tierra, y sus ramas tocan el cielo. Los antiguos lo consideraban el eje del cosmos — el axis mundi.",
    'Roca': "Fragmento de la corteza terrestre con millones de años de memoria geológica. Cada mineral en su interior registra las condiciones del planeta en el momento de su formación. La piedra no olvida."
  }

  const toggleAbility = useCallback(() => {
    if (abilityCooldown) return

    setAbilityActive(prev => {
      const newState = !prev

      // 🚀 Lógica UFO 3: Boost con duración y cooldown (1.8s / 4s)
      if (currentUfo === 3 && newState) {
        setTimeout(() => {
          setAbilityActive(false)
          setAbilityCooldown(true)
          setTimeout(() => setAbilityCooldown(false), 4000)
        }, 1800)
      }

      // 🔬 Lógica UFO 4: Scan con detección de NPCs (2.0s duration)
      // IMPORTANTE: Lee desde refs para evitar stale closures
      if (currentUfo === 4 && newState) {
        const currentSite = selectedSiteRef.current
        const currentLocation = selectedLocationRef.current
        const siteId = currentSite?.id || ''
        let foundNPC: string | null = null

        if (siteId === 'puma-punku' || siteId === 'pumaPunku') {
          // Puma Punku: Viracocha, Fuente Magna o Cóndor según proximidad
          const px = mainAvatarPositionRef.current.x
          const pz = mainAvatarPositionRef.current.z
          const distCondor = (px + 83) ** 2 + (pz + 67) ** 2
          const distFuente = px ** 2 + pz ** 2
          const distViracocha = (px - 14.5) ** 2 + (pz - 0.83) ** 2
          if (distCondor < 400) foundNPC = 'Cóndor'
          else foundNPC = distFuente < distViracocha ? 'FuenteMagna' : 'Viracocha'
        } else if (siteId === 'pyramids-giza' || siteId === 'giza') {
          // Giza: elegir el NPC más cercano por distancia horizontal XZ
          const gizaNPCs = [
            { name: 'Sphinx', x: 100, z: 50 },
            { name: 'Ramesses', x: -20, z: -50 },
            { name: 'Hatshepsut', x: 20, z: -50 },
            { name: 'Akhenaten', x: 0, z: 0 },
            { name: 'Mummy', x: -72, z: -2 }
          ]
          let minDistSq = Infinity
          const px = mainAvatarPositionRef.current.x
          const pz = mainAvatarPositionRef.current.z
          // Geoglifo araña en [-83, 3, -67]
          const distArana = (px + 83) ** 2 + (pz + 67) ** 2
          if (distArana < 400) { foundNPC = 'Araña' } else {
            gizaNPCs.forEach(npc => {
              const distSq = (px - npc.x) ** 2 + (pz - npc.z) ** 2
              if (distSq < minDistSq) { minDistSq = distSq; foundNPC = npc.name }
            })
          }
        } else if (siteId === 'moai-easter-island' || siteId === 'easter-island') {
          const px = mainAvatarPositionRef.current.x
          const pz = mainAvatarPositionRef.current.z
          const distBallena = (px + 55) ** 2 + (pz - 55) ** 2  // ballena en [-55,1,55]
          const distMerkaba = px ** 2 + pz ** 2
          if (distBallena < 400) foundNPC = 'Ballena'
          else foundNPC = distMerkaba < 400 ? 'Merkaba' : 'Hotu Matua'
        } else if (siteId === 'teotihuacan') {
          const px = mainAvatarPositionRef.current.x
          const pz = mainAvatarPositionRef.current.z
          const distColibri = (px + 83) ** 2 + (pz + 67) ** 2  // colibrí en [-83,0.3,-67]
          const distCalendario = px ** 2 + (pz + 20) ** 2
          if (distColibri < 400) foundNPC = 'Colibrí'
          else foundNPC = distCalendario < 625 ? 'CalendarioMaya' : 'Quetzalcoatl'
        } else if (siteId === 'tres-zapotes') {
          const px = mainAvatarPositionRef.current.x
          const pz = mainAvatarPositionRef.current.z
          const distPerro = (px + 83) ** 2 + (pz + 67) ** 2  // perro en [-83,1,-67]
          if (distPerro < 400) foundNPC = 'Perro'
          else if (currentLocation && Math.abs(currentLocation.lat) < 0.001) foundNPC = 'Mictlantecuhtli'
          else foundNPC = 'Atlante'
        } else if (currentLocation) {
          // Fallback por coordenadas GPS (para sitios sin id exacto)
          const { lat, lon } = currentLocation
          if (Math.abs(lat - (-16.5616)) < 0.1 && Math.abs(lon - (-68.6795)) < 0.1) foundNPC = 'Viracocha'
          else if (Math.abs(lat - 29.9792) < 0.1 && Math.abs(lon - 31.1342) < 0.1) {
            // En Giza por coordenadas: buscar más cercano igual que arriba
            const gizaNPCs = [
              { name: 'Sphinx', x: 100, z: 50 },
              { name: 'Ramesses', x: -20, z: -50 },
              { name: 'Hatshepsut', x: 20, z: -50 },
              { name: 'Akhenaten', x: 0, z: 0 },
              { name: 'Mummy', x: -72, z: -2 }
            ]
            let minDistSq = Infinity
            const px = mainAvatarPositionRef.current.x
            const pz = mainAvatarPositionRef.current.z
            gizaNPCs.forEach(npc => {
              const distSq = (px - npc.x) ** 2 + (pz - npc.z) ** 2
              if (distSq < minDistSq) {
                minDistSq = distSq
                foundNPC = npc.name
              }
            })
          }
          else if (Math.abs(lat - (-27.1254)) < 0.1) foundNPC = 'Hotu Matua'
          else if (Math.abs(lat - 19.6925) < 0.1) foundNPC = 'Quetzalcoatl'
          else if (Math.abs(lat - 18.4667) < 0.1) foundNPC = 'Atlante'
          else if (Math.abs(lat - 37.2231) < 0.1 && Math.abs(lon - 38.9225) < 0.1) {
            // Göbekli Tepe: astronauta en [-55,0.1,-55] o monolito central
            const px = mainAvatarPositionRef.current.x
            const pz = mainAvatarPositionRef.current.z
            const distAstro = (px + 55) ** 2 + (pz + 55) ** 2
            const distMonolito = px ** 2 + pz ** 2  // monolito en [0,0,0]
            if (distAstro < 400) foundNPC = 'Astronauta'
            else if (distMonolito < 900) foundNPC = 'MonolitoGobekli'
            else foundNPC = 'Astronauta' // default Göbekli
          }
          else if (lat > -16.5 && lat < -15.5 && lon > -70 && lon < -68.5) {
            // Titicaca: monos en [-83,0.3,-67]
            const px = mainAvatarPositionRef.current.x
            const pz = mainAvatarPositionRef.current.z
            const distMonos = (px + 83) ** 2 + (pz + 67) ** 2
            foundNPC = distMonos < 400 ? 'Monos' : 'FuenteMagna'
          }
        }

        if (foundNPC) {
          setScannedEntity({ name: foundNPC, desc: SCAN_DATA[foundNPC as keyof typeof SCAN_DATA] })
        }

        setTimeout(() => {
          setAbilityActive(false)
          setScannedEntity(null)
          setAbilityCooldown(true)
          setTimeout(() => setAbilityCooldown(false), 3000)
        }, 2000)
      }

      return newState
    })

    // Efecto de sacudida universal al activar cualquier habilidad
    setIsShaking(true)
    setTimeout(() => setIsShaking(false), 500)
    // Solo depende de currentUfo y abilityCooldown — site/location se leen por ref
  }, [currentUfo, abilityCooldown])

  // 🐍 Estado del diálogo de Quetzalcoatl
  const [showQuetzalcoatlDialogue, setShowQuetzalcoatlDialogue] = useState(false)
  const [showQuetzalcoatl, setShowQuetzalcoatl] = useState(false)

  // 🗿 Estado del diálogo Olmeca (Veracruz)
  const [showOlmecDialogue, setShowOlmecDialogue] = useState(false)
  const [olmecStoodUp, setOlmecStoodUp] = useState(false)
  const [olmecThanked, setOlmecThanked] = useState(false)
  const [caveQuestActive, setCaveQuestActive] = useState(false)
  // 💚 Jade Mask - item de la misión de Veracruz
  const [jadeMaskVisible, setJadeMaskVisible] = useState(false)
  const [jadeMaskInInventory, setJadeMaskInInventory] = useState(false)

  // Restaurar estados de TODAS las misiones desde missionState al montar
  useEffect(() => {
    const ms = loadMissionState()

    // ── VERACRUZ ──
    const veracruzItems = ms.sites.veracruz?.itemsCollected || []
    const veracruzNpcs = ms.sites.veracruz?.npcsInteracted || []
    const veracruzMissions = ms.sites.veracruz?.missionsCompleted || []
    const easterItems = ms.sites.easterIsland?.itemsCollected || []

    if (veracruzNpcs.includes('olmec_head')) {
      setOlmecStoodUp(true)
      setOlmecThanked(true)
    }

    const jadeCollected = easterItems.includes('jade_mask')
    const veracruzDone = veracruzMissions.includes('deliver_jade_mask')
    const questActivated = veracruzItems.includes('cave_quest_active')

    if (jadeCollected || veracruzDone || questActivated) {
      setCaveQuestActive(true)
    }
    if (jadeCollected && !veracruzDone) {
      setJadeMaskInInventory(true)
    }
    if (questActivated && !jadeCollected && !veracruzDone) {
      setJadeMaskVisible(true)
    }

    // ── TEOTIHUACAN ──
    const teoItems = ms.sites.teotihuacan?.itemsCollected || []
    const teoMissions = ms.sites.teotihuacan?.missionsCompleted || []
    if (teoItems.includes('corn_seed') && !teoMissions.includes('plant_corn')) {
      setCornInInventory(true)
    }
    if (teoMissions.includes('plant_corn')) {
      setCornPlanted(true)
    }

    // ── ITEMS ESPECIALES ──
    const gizaItems = ms.sites.giza?.itemsCollected || []
    const easterItemsCollected = ms.sites.easterIsland?.itemsCollected || []

    if (gizaItems.includes('scarab')) {
      setScarabInInventory(true)
      setScarabCollected(true)
    }
    if (easterItemsCollected.includes('crystal_skull')) {
      setSkullInInventory(true)
    }

    console.log('📜 Estados restaurados desde missionState')
  }, [])
  const [cornInInventory, setCornInInventory] = useState(false) // Maíz en inventario (rotando)
  const [cornOnGround, setCornOnGround] = useState(false) // Maíz en el piso (visible en escena)
  const [cornDropPosition, setCornDropPosition] = useState<{ x: number, z: number } | null>(null) // Posición donde cayó el maíz
  const [cornPlanted, setCornPlanted] = useState(false) // Si el maíz fue plantado en la tierra

  // Handler para soltar el maíz del inventario
  const handleDropCornSeed = useCallback(() => {
    if (mode === 'globe') {
      console.log('🚫 No se puede soltar el maíz en el espacio!')
      return
    }
    console.log('🌽 Soltando maíz al piso!')
    const pos = mainAvatarPositionRef.current
    if (!pos) return
    const dropX = pos.x
    const dropZ = pos.z

    const soilCenterX = 60
    const soilCenterZ = 0
    const soilSize = 8

    const isOnSoil = Math.abs(dropX - soilCenterX) <= soilSize / 2 &&
      Math.abs(dropZ - soilCenterZ) <= soilSize / 2

    if (isOnSoil && !cornPlanted) {
      console.log('🌱 ¡Maíz plantado en la tierra!')
      setCornPlanted(true)
      setCornInInventory(false)
      setCornOnGround(false)
      completeMission('teotihuacan', 'plant_corn')
      clearWeather('teotihuacan')
      setWeather(CALM_WEATHER)
    } else {
      setCornDropPosition({ x: dropX, z: dropZ })
      setCornInInventory(false)
      setCornOnGround(true)
    }
  }, [cornPlanted, mode])

  const handleDropSkull = useCallback(() => {
    if (mode === 'globe') {
      console.log('🚫 No se puede soltar la calavera en el espacio!')
      return
    }
    console.log('💀 Soltando calavera al piso!')
    const pos = mainAvatarPositionRef.current
    if (pos) {
      setSkullDropPosition({ x: pos.x, z: pos.z })
      setSkullInInventory(false)
      setSkullOnGround(true)
    }
  }, [mode])

  const handleDropScarab = useCallback(() => {
    if (mode === 'globe') {
      console.log('🚫 No se puede soltar el escarabajo en el espacio!')
      return
    }
    console.log('🪲 Soltando escarabajo al piso!')
    const pos = mainAvatarPositionRef.current
    if (pos) {
      setScarabDropPosition({ x: pos.x, z: pos.z })
      setScarabInInventory(false)
      setScarabOnGround(true)
    }
  }, [mode])

  const handleDropTonatiuh = useCallback(() => {
    if (mode === 'globe') {
      console.log('🚫 No se puede soltar Tonatiuh en el espacio!')
      return
    }
    console.log('🌞 Soltando Tonatiuh al piso!')
    const pos = mainAvatarPositionRef.current
    if (pos) {
      setTonatiuhDropPosition({ x: pos.x, z: pos.z })
      setTonatiuhInInventory(false)
      setTonatiuhOnGround(true)
    }
  }, [mode])

  const handleDropRock = useCallback(() => {
    if (mode === 'globe') return
    console.log('🪨 Soltando roca al piso!')
    const pos = mainAvatarPositionRef.current
    if (pos) {
      setRockDropPosition({ x: pos.x, z: pos.z })
      setRockInInventory(false)
      setRockOnGround(true)
    }
  }, [mode])

  const handleDropMagnaBowl = useCallback(() => {
    if (mode === 'globe') return
    console.log('🏺 Soltando Fuente Magna al piso!')
    const pos = mainAvatarPositionRef.current
    if (pos) {
      setMagnaBowlDropPosition({ x: pos.x, z: pos.z })
      setMagnaBowlLentInInventory(false)
      setMagnaBowlOnGround(true)
    }
  }, [mode])

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
    const interval = setInterval(checkMagnaBowl, 5000) // Reducido de 1000ms a 5000ms
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

        // Solo marcar como recolectado si REALMENTE fue recolectado
        if (collected) {
          setPyramidionCollected(true)
        }

        // Mostrar en la punta solo si fue entregado a la Esfinge
        if (delivered) {
          setPyramidionOnTop(true)
        }
      }
    }

    // Verificar al montar y cada 5 segundos (no necesita ser frecuente)
    checkPyramidion()
    const interval = setInterval(checkPyramidion, 5000)
    return () => clearInterval(interval)
  }, [])


  // 🎵 Habilitar audio en primera interacción + HarmoniaMundi permanente
  useEffect(() => {
    if (audioEnabled) return

    const enableAudioOnInteraction = async () => {
      try {
        // Habilitar audio climático
        await audioGenerator.enable()
        setAudioEnabled(true)
        loggers.world.info('🔊 Audio habilitado')

        // 🎼 Habilitar Harmonia Mundi PERMANENTEMENTE
        const { getHarmoniaMundi } = await import('@/systems/HarmoniaMundiSystem')
        const harmonia = getHarmoniaMundi()
        await harmonia.enable()
        loggers.world.info('🎼 Harmonia Mundi habilitado permanentemente')

        // Aplicar volumen guardado
        const settings = loadGameSettings()
        const vol = settings?.audio?.masterVolume ?? 0.7
        harmonia.setMasterVolume(vol)

        // Activar capas ya desbloqueadas por misiones previas
        const { loadMissionState: loadMS } = await import('@/types/missionState')
        const ms = loadMS()
        const totalCompleted = ms.stats.totalMissionsCompleted
        for (let i = 1; i <= totalCompleted; i++) {
          harmonia.unlockMissionLayer(`earth_mission_${i}`)
        }
        loggers.world.info(`🎵 ${totalCompleted} capas de misión restauradas`)

        window.removeEventListener('click', enableAudioOnInteraction)
        window.removeEventListener('keydown', enableAudioOnInteraction)
      } catch (error) {
        loggers.world.error('Error habilitando audio:', error)
      }
    }

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
    // Teotihuacán
    if (Math.abs(lat - 19.6925) < 0.05 && Math.abs(lon - (-98.8438)) < 0.05) {
      return 'teotihuacan'
    }
    // Isla de Pascua
    if (Math.abs(lat - (-27.1254)) < 0.05 && Math.abs(lon - (-109.2778)) < 0.05) {
      return 'easterIsland'
    }
    // Veracruz (Tres Zapotes)
    if (Math.abs(lat - 18.4667) < 0.05 && Math.abs(lon - (-95.4500)) < 0.05) {
      return 'veracruz'
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

    // Determinar clima: si hay 5+ misiones completas → siempre buen clima en todo el planeta
    const missionState = loadMissionState()
    const allMissionsComplete = missionState.stats.totalMissionsCompleted >= 5
    const siteName = getSiteNameFromCoordinates(site.lat, site.lon)
    const weatherCleared = allMissionsComplete || (siteName ? isWeatherCleared(siteName) : discoveredSites.current.has(site.id))
    // Teotihuacán: lluvia ligera en lugar de tormenta completa
    const isTeotihuacan = siteName === 'teotihuacan'
    setWeather(weatherCleared ? CALM_WEATHER : isTeotihuacan ? TEOTIHUACAN_WEATHER : DEFAULT_STORM_WEATHER)
    setMode('model')

    loggers.world.info('Teletransporte a sitio arqueolÃ³gico completado')
  }

  // 🖱️ Evento de teclado para habilidades de nave
  // Solo Space activa la habilidad — 'e' está reservado para rotar la nave
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ignorar si se está escribiendo en un input, no estamos en modo modelo, o es key-repeat
      if (mode !== 'model') return
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return
      if (e.repeat) return // ← evita que mantener Space dispare múltiples veces

      if (e.code === 'Space') {
        e.preventDefault()
        toggleAbility()
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [mode, toggleAbility])

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

    // Determinar clima: si hay 5+ misiones completas → siempre buen clima
    const ms = loadMissionState()
    const allComplete = ms.stats.totalMissionsCompleted >= 5
    const siteName = getSiteNameFromCoordinates(lat, lon)
    const weatherCleared = allComplete || (siteName ? isWeatherCleared(siteName) : false)
    // Teotihuacán: lluvia ligera en lugar de tormenta completa
    const isTeotihuacan = siteName === 'teotihuacan'
    setWeather(weatherCleared ? CALM_WEATHER : isTeotihuacan ? TEOTIHUACAN_WEATHER : DEFAULT_STORM_WEATHER)
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

  // 🌋 Erupción volcánica: el usuario pierde - reset misiones y redirige al menú
  const handleEruptionEnd = useCallback(() => {
    console.log('🌋 ERUPCIÓN VOLCÁNICA - El usuario pierde. Reseteando misiones...')

    // Resetear todas las misiones
    resetMissionState()

    // Limpiar sesión activa → el botón "Continuar" no aparecerá en el menú
    sessionStorage.removeItem('game_session_active')
    sessionStorage.clear()

    // Silenciar audio
    getClimateAudio().updateWeather({ rain: 0, wind: 0, tornado: 0, snow: 0, thunder: false })

    // Redirigir al menú después de un breve fade
    setTimeout(() => {
      window.location.href = window.location.origin + (window.location.pathname.includes('ArcheoScope') ? '/ArcheoScope/menu' : '/menu')
    }, 2000)
  }, [])

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
        { id: 'ufo_5', name: '💣 Titan', model: '/ufo_5.glb', specialty: 'Fuerza Bruta / Impacto', description: 'Especialidad: potencia y resistencia', ability: 'Habilidad principal: masa + potencia', missions: 'Tipo de misiones: combate, minería pesada, abrir rutas, destruir o detener objetos' }
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
      {/* Input de coordenadas - DESHABILITADO en Mictlán */}
      <CoordinateInput
        onCoordinateSubmit={handleLocationClick}
        currentLocation={selectedLocation}
        disabled={navigationBlocked}
      />

      {/* Panel Científico — reemplaza LocationInfo + timer */}
      {mode === 'model' && showLocationInfo && (
        <div style={{
          position: 'fixed',
          top: '130px',
          left: '20px',
          zIndex: 999,
          width: '280px',
          background: 'rgba(5, 8, 18, 0.92)',
          border: '1px solid rgba(102, 126, 234, 0.35)',
          borderRadius: '12px',
          padding: '16px',
          backdropFilter: 'blur(10px)',
          boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
          fontFamily: 'monospace',
          fontSize: '12px',
          color: 'rgba(255,255,255,0.85)',
        }}>
          {/* Header */}
          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            marginBottom: '12px', paddingBottom: '10px',
            borderBottom: '1px solid rgba(102,126,234,0.2)',
          }}>
            <span style={{ color: '#667eea', fontWeight: 'bold', letterSpacing: '2px', fontSize: '11px' }}>
              ◈ PANEL CIENTÍFICO
            </span>
            <span style={{ color: '#ffd700', letterSpacing: '1px' }}>
              ⏱ {String(Math.floor(gameTimer / 3600)).padStart(2,'0')}:{String(Math.floor((gameTimer % 3600) / 60)).padStart(2,'0')}:{String(gameTimer % 60).padStart(2,'0')}
            </span>
          </div>

          {/* Ubicación */}
          <div style={{ marginBottom: '12px' }}>
            <div style={{ color: '#667eea', fontSize: '10px', letterSpacing: '1px', marginBottom: '6px' }}>
              📍 UBICACIÓN
            </div>
            {selectedSite && (
              <div style={{ color: '#fff', fontWeight: 'bold', marginBottom: '3px', fontSize: '13px' }}>
                {selectedSite.name}
              </div>
            )}
            {selectedLocation && (
              <div style={{ color: 'rgba(255,255,255,0.6)', lineHeight: '1.6' }}>
                <div>Lat: <span style={{ color: '#a5f3fc' }}>{selectedLocation.lat.toFixed(5)}°</span></div>
                <div>Lon: <span style={{ color: '#a5f3fc' }}>{selectedLocation.lon.toFixed(5)}°</span></div>
              </div>
            )}
            {selectedSite && (
              <div style={{ color: 'rgba(255,255,255,0.4)', fontSize: '11px', marginTop: '3px' }}>
                {selectedSite.culture} · {selectedSite.period}
              </div>
            )}
          </div>

          {/* Datos Solares */}
          <div style={{ marginBottom: '12px' }}>
            <div style={{ color: '#f59e0b', fontSize: '10px', letterSpacing: '1px', marginBottom: '6px' }}>
              ☀️ ASTRONOMÍA SOLAR
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px 8px', lineHeight: '1.8' }}>
              <span style={{ color: 'rgba(255,255,255,0.5)' }}>Azimut</span>
              <span style={{ color: '#fcd34d' }}>{((panelSolarState?.solarAzimuth ?? 0) * 180 / Math.PI).toFixed(1)}°</span>
              <span style={{ color: 'rgba(255,255,255,0.5)' }}>Elevación</span>
              <span style={{ color: '#fcd34d' }}>{((panelSolarState?.solarAltitude ?? 0) * 180 / Math.PI).toFixed(1)}°</span>
              <span style={{ color: 'rgba(255,255,255,0.5)' }}>Declinación</span>
              <span style={{ color: '#fcd34d' }}>{((panelSolarState?.declination ?? 0) * 180 / Math.PI).toFixed(2)}°</span>
              <span style={{ color: 'rgba(255,255,255,0.5)' }}>Fase</span>
              <span style={{ color: (panelSolarState?.isDay ?? true) ? '#fbbf24' : '#818cf8' }}>{(panelSolarState?.isDay ?? true) ? '☀ Día' : '🌙 Noche'}</span>
              {panelSolarState?.season && (
                <>
                  <span style={{ color: 'rgba(255,255,255,0.5)' }}>Estación</span>
                  <span style={{ color: '#86efac' }}>
                    {panelSolarState.season === 'spring' ? '🌱 Primavera'
                      : panelSolarState.season === 'summer' ? '☀️ Verano'
                      : panelSolarState.season === 'autumn' ? '🍂 Otoño'
                      : '❄️ Invierno'}
                  </span>
                </>
              )}
            </div>
          </div>

          {/* Hora simulada */}
          {panelSolarState?.simulatedTime && (
            <div style={{ marginBottom: '12px' }}>
              <div style={{ color: '#818cf8', fontSize: '10px', letterSpacing: '1px', marginBottom: '6px' }}>
                🕐 TIEMPO SIMULADO
              </div>
              <div style={{ color: '#c4b5fd', lineHeight: '1.6' }}>
                <div>{panelSolarState.simulatedTime.toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' })}</div>
                <div>{panelSolarState.simulatedTime.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })} (hora local)</div>
              </div>
            </div>
          )}

          {/* Entorno */}
          <div>
            <div style={{ color: '#34d399', fontSize: '10px', letterSpacing: '1px', marginBottom: '6px' }}>
              🌍 ENTORNO
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px 8px', lineHeight: '1.8' }}>
              <span style={{ color: 'rgba(255,255,255,0.5)' }}>Bioma</span>
              <span style={{ color: '#6ee7b7', textTransform: 'capitalize' }}>{biome.type}</span>
              {biome.temperature !== undefined && (
                <>
                  <span style={{ color: 'rgba(255,255,255,0.5)' }}>Temp.</span>
                  <span style={{ color: '#6ee7b7' }}>{biome.temperature}°C</span>
                </>
              )}
              {biome.humidity !== undefined && (
                <>
                  <span style={{ color: 'rgba(255,255,255,0.5)' }}>Humedad</span>
                  <span style={{ color: '#6ee7b7' }}>{biome.humidity}%</span>
                </>
              )}
            </div>
          </div>
        </div>
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
            marginBottom: '24px',
            animation: 'logoPulse 2s ease-in-out infinite'
          }}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={process.env.NODE_ENV === 'production'
                ? '/ArcheoScope/branding/icons/logo-simple-3.png'
                : '/branding/icons/logo-simple-3.png'}
              alt="Archeoscope"
              style={{ width: '120px', height: '120px', objectFit: 'contain' }}
            />
          </div>
          <style>{`
            @keyframes logoPulse {
              0%, 100% { filter: drop-shadow(0 0 15px rgba(102,126,234,0.7)); transform: scale(1); }
              50% { filter: drop-shadow(0 0 28px rgba(102,126,234,1)); transform: scale(1.05); }
            }
          `}</style>
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

      {/* Botones de control — ocultar "Volver al Globo" y "Mostrar Info" en mobile */}
      {mode === 'model' && !isMobile && (
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
            disabled={navigationBlocked}
            style={{
              padding: '12px 24px',
              background: navigationBlocked ? 'rgba(60, 60, 60, 0.5)' : 'rgba(102, 126, 234, 0.9)',
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

      {/* 📱 Botón de Menú para mobile — esquina inferior izquierda */}
      {mode === 'model' && isMobile && (
        <button
          onClick={() => {
            if (typeof window !== 'undefined') {
              // Guardar flag de partida activa para poder volver
              sessionStorage.setItem('mobile_game_active', 'true')
              // Guardar ubicación actual
              if (selectedLocation) {
                updatePlayerLocation(selectedLocation.lat, selectedLocation.lon, 'model')
              }
              // Navegar al menú (el estado ya está en localStorage)
              window.location.href = '/menu'
            }
          }}
          style={{
            position: 'fixed',
            bottom: 16,
            left: 16,
            width: 44,
            height: 44,
            borderRadius: '50%',
            background: 'rgba(0,0,0,0.6)',
            border: '1px solid rgba(255,255,255,0.3)',
            color: '#fff',
            fontSize: '18px',
            cursor: 'pointer',
            zIndex: 1001,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          ☰
        </button>
      )}

      {/* Brújula astronómica - muestra el norte real basado en la rotación de la cámara */}
      {mode === 'model' && (
        <>
          <Compass rotation={cameraRotation} solarAzimuth={solarState.azimuth} />
        </>
      )}

      {/* 📱 Controles touch para mobile — D-pad + rotación */}
      {mode === 'model' && isMobile && (
        <MobileTouchControls visible={true} />
      )}

      {/* 🛸 Botón de Habilidad Especial */}
      {mode === 'model' && (
        <div style={{
          position: 'fixed',
          bottom: '100px',
          left: '20px',
          zIndex: 1000,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-end',
          gap: '4px'
        }}>
          <button
            onClick={toggleAbility}
            disabled={abilityCooldown}
            style={{
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              background: abilityCooldown
                ? 'rgba(50, 50, 50, 0.8)'
                : abilityActive
                  ? 'linear-gradient(135deg, #4a9eff, #667eea)'
                  : 'rgba(30, 41, 59, 0.8)',
              border: `3px solid ${abilityCooldown ? '#333' : abilityActive ? '#fff' : '#4a9eff'}`,
              color: abilityCooldown ? '#555' : 'white',
              fontSize: '28px',
              cursor: abilityCooldown ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: abilityActive ? '0 0 25px #4a9eff' : '0 4px 10px rgba(0,0,0,0.5)',
              transition: 'all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
              padding: 0,
              position: 'relative',
              overflow: 'hidden'
            }}
            title={abilityCooldown ? "Enfriamiento..." : "Activar Habilidad Especial (Espacio / E)"}
          >
            {currentUfo === 1 && '🌫️'}
            {currentUfo === 2 && '🛡️'}
            {currentUfo === 3 && '⚡'}
            {currentUfo === 4 && '🔬'}
            {currentUfo === 5 && '💣'}
            {abilityCooldown && (
              <div style={{
                position: 'absolute',
                inset: 0,
                background: 'rgba(0,0,0,0.4)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '12px'
              }}>
                ⏳
              </div>
            )}
          </button>
          <div style={{
            color: 'white',
            fontSize: '10px',
            textTransform: 'uppercase',
            letterSpacing: '1px',
            fontWeight: 'bold',
            textShadow: '0 1px 3px rgba(0,0,0,0.8)'
          }}>
          </div>
        </div>
      )}

      {/* 🎭 Efectos de Habilidades */}
      <ShipAbilities
        ufoNumber={currentUfo}
        active={abilityActive}
        onActionComplete={currentUfo >= 4 ? () => setAbilityActive(false) : undefined}
      />


      {/* Contenedor Principal con Sacudida */}
      <div className={isShaking ? 'screen-shake-active' : ''} style={{
        position: 'fixed',
        inset: 0,
        pointerEvents: 'none',
        zIndex: 998
      }} />

      {/* Inventario - horizontal abajo en mobile, vertical derecha en PC */}
      <div style={{
        position: 'fixed',
        ...(isMobile
          ? { bottom: '12px', left: '50%', transform: 'translateX(-50%)', flexDirection: 'row' as const }
          : { top: '280px', right: '20px', flexDirection: 'column' as const }
        ),
        display: 'flex',
        gap: isMobile ? '8px' : '10px',
        zIndex: 1000
      }}>
        <InventoryItem
          modelPath="/maiz.glb"
          itemName="Maíz"
          show={cornInInventory}
          onDrop={handleDropCornSeed}
          dropDisabled={mode === 'globe'}
        />
        <InventoryItem
          modelPath="/crystal-skull.glb"
          itemName="Skull"
          show={skullInInventory}
          onDrop={handleDropSkull}
          dropDisabled={mode === 'globe'}
        />
        <InventoryItem
          modelPath="/escarabajo.glb"
          itemName="Scarab"
          show={scarabInInventory}
          onDrop={handleDropScarab}
          dropDisabled={mode === 'globe'}
        />
        <InventoryItem
          modelPath="/tonatiuh_aztec_sun.glb"
          itemName="Tonatiuh"
          show={tonatiuhInInventory}
          onDrop={handleDropTonatiuh}
          dropDisabled={mode === 'globe'}
        />
        <InventoryItem
          modelPath="/rock_blender.glb"
          itemName="Roca"
          show={rockInInventory}
          onDrop={handleDropRock}
          dropDisabled={mode === 'globe'}
        />
        <InventoryItem
          modelPath="/fuente_magna.glb"
          itemName="Fuente Magna"
          show={magnaBowlLentInInventory}
          onDrop={handleDropMagnaBowl}
          dropDisabled={mode === 'globe'}
        />
        <InventoryItem
          modelPath="/fuente_magna.glb"
          itemName="Fuente"
          show={magnaBowlOriginalInInventory}
          dropDisabled={true}
        />
      </div>

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
          abilityActive={abilityActive}
          currentUfo={currentUfo}
          modelPath={selectedModel}
          avatarModel={avatarModel}
          onModelLoaded={onModelLoaded}
          onCameraReady={onCameraReady}
          movementMode={movementMode}
          location={selectedLocation}
          site={selectedSite}
          showGeometryField={showGeometryField}
          showAlignmentLines={showAlignmentLines}
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
          onViracochaSpeak={() => {
            const pumaDone = isMissionCompleted('pumaPunku', 'reveal_structure')
            const allMissionsDone = loadMissionState().stats.totalMissionsCompleted >= 5

            // Viracocha toma la fuente, así que desaparece del inventario
            if (magnaBowlOriginalInInventory) {
              setMagnaBowlOriginalInInventory(false)
            }

            // Solo permitir diálogo interactivo si las 5 misiones están completas
            if (pumaDone && magnaBowlCollected && allMissionsDone) {
              // Diálogo interactivo: usuario es digno de obtener la fuente prestada
              setShowViracochaInteractive(true)
            } else {
              // Sin todas las misiones → diálogo simple
              setShowViracochaDialogue(true)
            }
          }}
          onCloseViracochaDialogue={() => setShowViracochaDialogue(false)}
          onPortalEnter={() => handleLocationClick(-16.031003664299448, -69.49975772335767)}
          magnaBowlCollected={magnaBowlCollected}
          onCameraRotationChange={setCameraRotation}
          onMictlanExit={() => {
            setMictlanCompleted(true)
            handleLocationClick(-27.1254, -109.2778)
          }}
          jadeMaskVisible={jadeMaskVisible}
          jadeMaskInInventory={jadeMaskInInventory}
          onJadeMaskCollect={() => {
            console.log('Mascara de Jade recogida!')
            collectItem('easterIsland', 'jade_mask')
            setJadeMaskInInventory(true)
            setJadeMaskVisible(false)
            setShowCollectedMessage(true)
            setTimeout(() => setShowCollectedMessage(false), 3000)
          }}
          skullInInventory={skullInInventory}
          showSkull={skullOnGround}
          skullDropPosition={skullDropPosition}
          onSkullCollect={handleCollectSkull}
          onMerkabaActivate={() => {
            console.log('✡️ Merkaba activado! 5ta mision - ¡Sincronización Planetaria Completada!')
            completeMission('easterIsland', 'activate_merkaba')

            // Limpiar clima de TODOS los sitios del planeta permanentemente
            const sites: (keyof MissionState['sites'])[] = ['pumaPunku', 'giza', 'easterIsland', 'teotihuacan', 'veracruz', 'angkorWat']
            sites.forEach(s => clearWeather(s))

            setWeather(CALM_WEATHER)
            console.log('🌍 Clima global estabilizado. La esfera energética rosa ha aparecido.')
          }}
          onSphinxClick={() => setShowSphinxDialogue(true)}
          onAkhenatonClick={() => setShowAkhenatonDialogue(true)}
          onPyramidionCollect={handleCollectPyramidion}
          pyramidionCollected={pyramidionCollected}
          pyramidionOnTop={pyramidionOnTop}
          onMummyMoved={handleMummyMoved}
          onScarabCollect={handleCollectScarab}
          onScarabPickup={() => { setScarabInInventory(true); setScarabOnGround(false) }}
          scarabDiscovered={scarabDiscovered}
          scarabCollected={scarabCollected}
          scarabInInventory={scarabInInventory}
          showScarab={scarabOnGround}
          scarabDropPosition={scarabDropPosition}
          onQuetzalcoatlClick={handleQuetzalcoatlClick}
          onQuetzalcoatlAppear={() => setShowQuetzalcoatl(true)}
          onCornCollect={handleCollectCornSeed}
          cornInInventory={cornInInventory}
          cornOnGround={cornOnGround}
          cornDropPosition={cornDropPosition}
          cornPlanted={cornPlanted}
          mainAvatarPositionRef={mainAvatarPositionRef}
          onEruptionEnd={handleEruptionEnd}
          onTriggerEruption={handleCollectSkull}
          onOlmecClick={() => {
            if (!olmecStoodUp) {
              setOlmecStoodUp(true)
              interactWithNPC('veracruz', 'olmec_head')
            }
            setShowOlmecDialogue(true)
          }}
          caveQuestActive={caveQuestActive}
          onEnterCave={() => handleLocationClick(0.0001, 0.0001)}
          onShipChange={handleUfoChange}
          tonatiuhInInventory={tonatiuhInInventory}
          tonatiuhOnGround={tonatiuhOnGround}
          tonatiuhDropPosition={tonatiuhDropPosition}
          onTonatiuhCollect={() => {
            setTonatiuhInInventory(true)
            setTonatiuhOnGround(false)
          }}
          onGobekliTonatiuhCollect={() => { setTonatiuhInInventory(true); setTonatiuhOnGround(false) }}
          onGobekliScarabCollect={() => { setScarabInInventory(true); setScarabOnGround(false) }}
          onGobekliSkullCollect={() => { setSkullInInventory(true); setSkullOnGround(false) }}
          onGobekliMagnaCollect={() => { setMagnaBowlLentInInventory(true); setMagnaBowlOnGround(false) }}
          scarabOnGround={scarabOnGround}
          skullOnGround={skullOnGround}
          rockInInventory={rockInInventory}
          rockOnGround={rockOnGround}
          rockDropPosition={rockDropPosition}
          onRockCollect={() => { 
            setRockInInventory(true)
            setRockOnGround(false)
            setShowCollectedMessage(true)
            setTimeout(() => setShowCollectedMessage(false), 3000)
          }}
          magnaBowlLentInInventory={magnaBowlLentInInventory}
          magnaBowlOnGround={magnaBowlOnGround}
          magnaBowlDropPosition={magnaBowlDropPosition}
          onMagnaBowlCollect={() => {
            setMagnaBowlLentInInventory(true)
            setMagnaBowlOnGround(false)
          }}
          onObeliskActivate={() => handleLocationClick(37.2231, 38.9225)}
          showViracochaInteractive={showViracochaInteractive}
          onCloseViracochaInteractive={() => {
            setShowViracochaInteractive(false)
            // Marcar que ya agradeció (para próximas visitas ir directo a opciones)
            if (!magnaBowlThanked) {
              setMagnaBowlThanked(true)
              if (typeof window !== 'undefined') localStorage.setItem('magna_bowl_thanked', 'true')
            }
          }}
          onLendMagnaBowl={() => {
            setMagnaBowlLentInInventory(true)
            setMagnaBowlOnGround(false)
            setMagnaBowlOriginalInInventory(false) // Viracocha acepta la original y presta la suya
          }}
        />
      ) : null}

      {/* Control de clima - OCULTO al usuario por defecto */}
      {/* {mode === 'model' && (
        <WeatherControl onWeatherChange={setWeather} initialWeather={weather} />
      )} */}

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

              // ✅ MARCAR MISIÓN COMO COMPLETADA
              completeMission('giza', 'return_pyramidion')
              console.log('✅ Misión "Devolver el Piramidión" COMPLETADA')

              // ☀️ LIMPIAR EL CLIMA - De malo a bueno
              clearWeather('giza')
              console.log('☀️ Clima de Giza limpiado - El sol brilla de nuevo')

              // Activar el estado que hace aparecer el piramidón en la punta
              setPyramidionOnTop(true)
              console.log('🔶 setPyramidionOnTop(true) - Piramidón debe aparecer en la punta')
            }
          }}
          onOptionSelected={(optionId) => {
            console.log(` Opción seleccionada: ${optionId}`)
          }}
        />
      )}

      {/* Diálogo de Akhenaton - FUERA del Canvas */}
      {showAkhenatonDialogue && (
        <AkhenatonDialogue
          onClose={() => setShowAkhenatonDialogue(false)}
          hasSeenGeoglyphs={isMissionCompleted('giza', 'return_pyramidion')}
        />
      )}

      {/* Diálogo de Quetzalcoatl - FUERA del Canvas */}
      {showQuetzalcoatlDialogue && (
        <QuetzalcoatlDialogue
          hasCornSeed={cornInInventory}
          hasPlantedCorn={cornPlanted}
          onClose={() => {
            setShowQuetzalcoatlDialogue(false)
            interactWithNPC('teotihuacan', 'quetzalcoatl')
          }}
          onRequestSeed={handleRequestCornSeed}
        />
      )}

      {/* Diálogo Olmeca Interactivo - FUERA del Canvas */}
      {showOlmecDialogue && (
        <OlmecInteractiveDialogue
          hasStoodUp={olmecThanked}
          hasJadeMask={jadeMaskInInventory}
          missionCompleted={isMissionCompleted('veracruz', 'deliver_jade_mask')}
          onClose={() => {
            setShowOlmecDialogue(false)
            if (olmecStoodUp && !olmecThanked) {
              setOlmecThanked(true)
            }
          }}
          onEnterCave={() => {
            setCaveQuestActive(true)
            setJadeMaskVisible(true)
            // Persistir: registrar que la quest de la cueva fue activada
            collectItem('veracruz', 'cave_quest_active')
          }}
          onDeliverJade={() => {
            collectItem('veracruz', 'jade_mask')
            completeMission('veracruz', 'deliver_jade_mask')
            clearWeather('veracruz')
            setWeather(CALM_WEATHER) // Buen clima inmediato
            setJadeMaskInInventory(false)
          }}
        />
      )}

      {/* 🔬 Oracle: Scan HUD Overlay (Nave 4) */}
      {currentUfo === 4 && abilityActive && scannedEntity && (
        <div style={{
          position: 'fixed',
          top: '20%',
          left: '50%',
          transform: 'translateX(-50%)',
          background: 'rgba(0, 16, 32, 0.9)',
          borderLeft: '4px solid #00ffff',
          padding: '24px',
          borderRadius: '2px 12px 12px 2px',
          color: '#00ffff',
          fontFamily: 'monospace',
          zIndex: 9999,
          minWidth: '400px',
          boxShadow: '0 0 40px rgba(0, 255, 255, 0.3), inset 0 0 20px rgba(0, 255, 255, 0.1)',
          backdropFilter: 'blur(10px)',
          textTransform: 'uppercase',
          animation: 'scanHUDIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)'
        }}>
          <div style={{ fontSize: '10px', marginBottom: '8px', opacity: 0.8, letterSpacing: '2px' }}>
            📡 ORACLE_SCAN // SIGNATURE_IDENTIFIED
          </div>
          <div style={{ fontSize: '28px', fontWeight: '900', marginBottom: '12px', letterSpacing: '4px', textShadow: '0 0 10px #00ffff' }}>
            {scannedEntity.name}
          </div>
          <div style={{
            fontSize: '15px',
            lineHeight: '1.6',
            color: '#e0faff',
            borderTop: '1px solid rgba(0, 255, 255, 0.4)',
            paddingTop: '15px',
            textTransform: 'none',
            letterSpacing: '0.5px'
          }}>
            {scannedEntity.desc}
          </div>
          <div style={{ marginTop: '20px', height: '4px', background: 'rgba(0, 255, 255, 0.2)', position: 'relative', overflow: 'hidden' }}>
            <div style={{
              position: 'absolute',
              top: 0, left: 0, height: '100%', width: '100%',
              background: 'linear-gradient(90deg, #00ffff, #0088ff)',
              animation: 'scanHUDBar 2s linear forwards'
            }} />
          </div>

        </div>
      )}

      {/* Estilos Globales y de Componente */}
      <style jsx global>{`
        .screen-shake-active {
          animation: screenShake 0.4s ease-in-out infinite;
        }
        @keyframes screenShake {
          0%, 100% { transform: translate(0, 0); }
          20% { transform: translate(-4px, 2px); }
          40% { transform: translate(4px, -2px); }
          60% { transform: translate(-3px, 1px); }
          80% { transform: translate(3px, -1px); }
        }
      `}</style>
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
        @keyframes scanHUDIn {
          from { opacity: 0; transform: translate(-50%, -40px) scale(0.9); }
          to { opacity: 1; transform: translate(-50%, 0) scale(1); }
        }
        @keyframes scanHUDBar {
          from { transform: translateX(-100%); }
          to { transform: translateX(0); }
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
  showAlignmentLines,
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
  onAkhenatonClick,
  onPyramidionCollect,
  pyramidionCollected,
  pyramidionOnTop,
  onMummyMoved,
  onScarabCollect,
  onScarabPickup,
  scarabDiscovered,
  scarabCollected,
  onQuetzalcoatlClick,
  onQuetzalcoatlAppear,
  onCornCollect,
  cornInInventory,
  cornOnGround,
  cornDropPosition,
  cornPlanted,
  mainAvatarPositionRef,
  onEruptionEnd,
  skullInInventory,
  showSkull,
  skullDropPosition,
  onSkullCollect,
  onTriggerEruption,
  scarabInInventory,
  showScarab,
  scarabDropPosition,
  onOlmecClick,
  caveQuestActive,
  onEnterCave,
  onMictlanExit,
  jadeMaskVisible,
  jadeMaskInInventory,
  onJadeMaskCollect,
  onMerkabaActivate,
  abilityActive,
  currentUfo,
  onShipChange,
  tonatiuhInInventory,
  tonatiuhOnGround,
  tonatiuhDropPosition,
  onTonatiuhCollect,
  onMagnaBowlCollect,
  onGobekliTonatiuhCollect,
  onGobekliScarabCollect,
  onGobekliSkullCollect,
  onGobekliMagnaCollect,
  scarabOnGround,
  skullOnGround,
  rockInInventory,
  rockOnGround,
  rockDropPosition,
  onRockCollect,
  magnaBowlLentInInventory,
  magnaBowlOnGround,
  magnaBowlDropPosition,
  onObeliskActivate,
  showViracochaInteractive,
  onCloseViracochaInteractive,
  onLendMagnaBowl
}: {
  abilityActive: boolean
  currentUfo: number
  modelPath: string
  avatarModel: string
  onModelLoaded?: (model: THREE.Object3D) => void
  onCameraReady?: (camera: THREE.Camera) => void
  movementMode: 'orbit' | 'avatar'
  location?: { lat: number, lon: number } | null
  site?: ArchaeologicalSite | null
  showGeometryField: boolean
  showAlignmentLines?: boolean
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
  onAkhenatonClick?: () => void
  onPyramidionCollect?: () => void
  pyramidionCollected?: boolean
  pyramidionOnTop?: boolean
  onMummyMoved?: () => void
  onScarabCollect?: () => void
  onScarabPickup?: () => void
  scarabDiscovered?: boolean
  scarabCollected?: boolean
  onQuetzalcoatlClick?: () => void
  onQuetzalcoatlAppear?: () => void
  onCornCollect?: () => void
  cornInInventory?: boolean
  cornOnGround?: boolean
  cornDropPosition?: { x: number, z: number } | null
  cornPlanted?: boolean
  mainAvatarPositionRef?: React.RefObject<THREE.Vector3>
  onEruptionEnd?: () => void
  skullInInventory?: boolean
  showSkull?: boolean
  skullDropPosition?: { x: number, z: number } | null
  onSkullCollect?: () => void
  onTriggerEruption?: () => void
  scarabInInventory?: boolean
  showScarab?: boolean
  scarabDropPosition?: { x: number, z: number } | null
  scarabOnGround?: boolean
  skullOnGround?: boolean
  onOlmecClick?: () => void
  caveQuestActive?: boolean
  onEnterCave?: () => void
  onMictlanExit?: () => void
  jadeMaskVisible?: boolean
  jadeMaskInInventory?: boolean
  onJadeMaskCollect?: () => void
  onMerkabaActivate?: () => void
  onShipChange?: (ufoNumber: number) => void
  tonatiuhInInventory?: boolean
  tonatiuhOnGround?: boolean
  tonatiuhDropPosition?: { x: number, z: number } | null
  onTonatiuhCollect?: () => void
  onMagnaBowlCollect?: () => void
  onGobekliTonatiuhCollect?: () => void
  onGobekliScarabCollect?: () => void
  onGobekliSkullCollect?: () => void
  onGobekliMagnaCollect?: () => void
  rockInInventory?: boolean
  rockOnGround?: boolean
  rockDropPosition?: { x: number, z: number } | null
  onRockCollect?: () => void
  magnaBowlLentInInventory?: boolean
  magnaBowlOnGround?: boolean
  magnaBowlDropPosition?: { x: number, z: number } | null
  onObeliskActivate?: () => void
  showViracochaInteractive?: boolean
  onCloseViracochaInteractive?: () => void
  onLendMagnaBowl?: () => void
}) {
  const terrainRef = useRef<THREE.Mesh>(null)
  const modelRef = useRef<THREE.Group>(null)
  const [obstacles, setObstacles] = useState<THREE.Object3D[]>([])
  const avatarPositionRef = useRef(new THREE.Vector3())

  // La posición del avatar se sincroniza en onPositionChange de WalkableAvatar

  // Detectar bioma basado en ubicaciÃ³n
  const biome = useMemo(() => {
    if (!location) return { type: 'default' as const, name: 'GenÃ©rico', description: '', temperature: 20, humidity: 50 }
    return detectBiome(location.lat, location.lon)
  }, [location])

  const isIceBiome = biome.type === 'ice'

  // Detectar si estamos en el Mictlán (inframundo) - escena vacía
  const isMictlan = location && Math.abs(location.lat - 0.0001) < 0.01 && Math.abs(location.lon - 0.0001) < 0.01

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

  // 📊 Leer preset gráfico desde localStorage
  const graphicsPreset = useMemo(() => {
    if (typeof window === 'undefined') return 'MEDIUM'
    return (localStorage.getItem('graphics_preset') || 'MEDIUM') as 'LOW' | 'MEDIUM' | 'HIGH' | 'ULTRA'
  }, [])
  const gfx = GRAPHICS_PRESETS[graphicsPreset]
  // 📱 Mobile optimization: limitar pixelRatio para mejor FPS
  const dpr = useMemo(() => {
    if (typeof window === 'undefined') return gfx.pixelRatio
    // Detectar mobile síncronamente para el cálculo inicial
    const mobile = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768
    // En mobile, limitar a 1.2 máximo (ahorra GPU sin pérdida visual notable en pantallas pequeñas)
    if (mobile) {
      return Math.min(window.devicePixelRatio, 1.2)
    }
    // En PC, usar el preset o devicePixelRatio según calidad
    return graphicsPreset === 'ULTRA' ? window.devicePixelRatio : gfx.pixelRatio
  }, [gfx.pixelRatio, graphicsPreset])

  return (
    <>
      <ObjectSelectionProvider onBlockMoved={onBlockMoved}>
        <Canvas
          shadows={gfx.shadows}
          camera={{ position: [8, 4, 8], fov: 60 }}
          dpr={dpr}
          gl={{
            antialias: gfx.antialias,
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

          {/* Far plane reducido en mobile: 900 vs 1500 — menos geometría procesada */}
          <PerspectiveCamera makeDefault position={[8, 4, 8]} fov={60}
            near={0.1}
            far={typeof window !== 'undefined' && (/Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768) ? 900 : 1500}
          />

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
            isDay={isMictlan ? false : isDay}
            skyColor={isMictlan ? '#050505' : skyColor}
            fogColor={isMictlan ? '#0a0505' : fogColor}
            stormDarkness={
              isMictlan ? 0.95 :
                weather.storm || weather.tornado ? 0.7 :
                  weather.rainHeavy || weather.lightning ? 0.5 :
                    0
            }
            fogDensity={isMictlan ? 0.02 : biome.type === 'altiplano' ? 0.004 : isIceBiome ? 0.012 : 0.008}
            showWater={!isIceBiome && !isMictlan}
            solarDirection={solarDirection}
            waterPosition={[0, -0.5, 0]}
            waterSize={biome.type === 'altiplano' ? 350 : 150}
            waterColor={biome.type === 'altiplano' ? '#2a5a8f' : '#1e3a5f'}
          />

          {/* Estrellas — visibles de noche en escenas terrestres */}
          {(!isDay || isMictlan) && <Stars />}

          {/* Terreno - adaptado al bioma (no en Mictlán) */}
          {!isMictlan && (isIceBiome ? (
            <IceTerrain location={location} ref={terrainRef} />
          ) : (
            <VolcanicTerrain location={location} ref={terrainRef} />
          ))}

          {/* Montañas de fondo (no en Mictlán) */}
          {!isMictlan && <BackgroundMountains biomeType={biome.type} />}

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

          {/* Elementos del entorno: rocas y vegetación - NO en océano, Giza ni Mictlán */}
          {!isIceBiome && !isMictlan && biome.type !== 'ocean' && !(
            location &&
            Math.abs(location.lat - 29.9792) < 0.05 &&
            Math.abs(location.lon - 31.1342) < 0.05
          ) && (
              <EnvironmentElementsWithTrees location={location} rockInInventory={rockInInventory} onRockCollect={onRockCollect} />
            )}

          {/* 🪨 Roca soltada del inventario */}
          {rockOnGround && rockDropPosition && (
            <DroppableItem
              modelPath="/rock_blender.glb"
              position={[rockDropPosition.x, 0, rockDropPosition.z]}
              onCollect={onRockCollect}
              scale={0.3}
              floatHeight={0.5}
              glowColor="#aaaaaa"
              itemName="Roca"
            />
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
              abilityActive={abilityActive}
              currentUfo={currentUfo}
              onPositionChange={(pos) => {
                avatarPositionRef.current.copy(pos)
                if (mainAvatarPositionRef?.current) mainAvatarPositionRef.current.copy(pos)
              }}
            />
          ) : (
            <ModelViewer modelPath={avatarModel} ref={modelRef} />
          )}

          {/* Colisiones bÃ¡sicas ya no son necesarias, WalkableAvatar las maneja */}

          {/* Info del sitio */}
          {site && (
            <SiteInfo site={site} />
          )}

          {/* Escena de Puma Punku - estructura + bloques dispersos */}
          {(site?.id === 'puma-punku' || (
            location &&
            Math.abs(location.lat - (-16.5616)) < 0.05 &&
            Math.abs(location.lon - (-68.6795)) < 0.05
          )) && (
              <PumaPunkuScene
                onViracochaSpeak={onViracochaSpeak}
                onPortalEnter={onPortalEnter}
                avatarPositionRef={avatarPositionRef}
                onShipChange={onShipChange}
                currentUfo={currentUfo}
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
                onAkhenatonClick={onAkhenatonClick}
                onPyramidionCollect={onPyramidionCollect}
                pyramidionCollected={pyramidionCollected || false}
                pyramidionOnTop={pyramidionOnTop || false}
                onMummyMoved={onMummyMoved}
                onScarabCollect={onScarabCollect}
                onScarabPickup={onScarabPickup}
                scarabDiscovered={scarabDiscovered || false}
                scarabCollected={scarabCollected || false}
                scarabInInventory={scarabInInventory}
                showScarab={showScarab}
                scarabDropPosition={scarabDropPosition}
                totalMissionsCompleted={loadMissionState().stats.totalMissionsCompleted}
                onShipChange={onShipChange}
                currentUfo={currentUfo}
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
                volcanicEruption={weather.volcanicEruption}
                onEruptionEnd={onEruptionEnd}
                showJadeMask={jadeMaskVisible}
                jadeMaskCollected={jadeMaskInInventory}
                onJadeMaskCollect={onJadeMaskCollect}
                onMerkabaActivate={onMerkabaActivate}
                onTriggerEruption={onTriggerEruption}
                skullInInventory={skullInInventory}
                showSkull={showSkull}
                skullDropPosition={skullDropPosition}
                onSkullCollect={onSkullCollect}
                merkabaMissionDone={isMissionCompleted('easterIsland', 'activate_merkaba')}
                onShipChange={onShipChange}
                currentUfo={currentUfo}
                abilityActive={abilityActive}
                onObeliskActivate={onObeliskActivate}
                tonatiuhInInventory={tonatiuhInInventory}
                tonatiuhOnGround={tonatiuhOnGround}
                tonatiuhDropPosition={tonatiuhDropPosition}
                onTonatiuhCollect={onTonatiuhCollect}
                magnaBowlLentInInventory={magnaBowlLentInInventory}
                magnaBowlOnGround={magnaBowlOnGround}
                magnaBowlDropPosition={magnaBowlDropPosition}
                onMagnaBowlCollect={onMagnaBowlCollect}
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
                onQuetzalcoatlClick={onQuetzalcoatlClick}
                onQuetzalcoatlAppear={onQuetzalcoatlAppear}
                onCornCollect={onCornCollect}
                cornCollected={cornInInventory}
                showCornSeed={cornOnGround}
                cornDropPosition={cornDropPosition}
                cornPlanted={cornPlanted}
                onShipChange={onShipChange}
                currentUfo={currentUfo}
                abilityActive={abilityActive}
              />
            )}

          {/* Escena de Veracruz - Cabeza Colosal Olmeca */}
          {(site?.id === 'tres-zapotes' || (
            location &&
            Math.abs(location.lat - 18.4667) < 0.05 &&
            Math.abs(location.lon - (-95.4500)) < 0.05
          )) && (
              <VeracruzScene
                avatarPositionRef={avatarPositionRef}
                onOlmecClick={onOlmecClick}
                caveQuestActive={caveQuestActive}
                onEnterCave={onEnterCave}
                jadeMissionDone={isMissionCompleted('veracruz', 'deliver_jade_mask')}
                onShipChange={onShipChange}
                currentUfo={currentUfo}
              />
            )}

          {/* 💀 Escena del Mictlán - Inframundo */}
          {(site?.id === 'mictlan' || (
            location &&
            Math.abs(location.lat - 0.0001) < 0.01 &&
            Math.abs(location.lon - 0.0001) < 0.01
          )) && (
              <MictlanScene
                avatarPositionRef={avatarPositionRef}
                onExit={onMictlanExit}
                currentUfo={currentUfo}
                abilityActive={abilityActive}
                tonatiuhInInventory={tonatiuhInInventory}
                onTonatiuhCollect={onTonatiuhCollect}
              />
            )}

          {/* 🏛️ Göbekli Tepe — solo accesible via obelisco de Isla de Pascua */}
          {location &&
            Math.abs(location.lat - 37.2231) < 0.05 &&
            Math.abs(location.lon - 38.9225) < 0.05 && (
              <GobekliTepeScene
                tonatiuhDropPosition={tonatiuhDropPosition}
                tonatiuhOnGround={tonatiuhOnGround}
                onTonatiuhCollect={onGobekliTonatiuhCollect}
                scarabDropPosition={scarabDropPosition}
                scarabOnGround={scarabOnGround}
                onScarabCollect={onGobekliScarabCollect}
                skullDropPosition={skullDropPosition}
                skullOnGround={skullOnGround}
                onSkullCollect={onGobekliSkullCollect}
                magnaBowlCollected={magnaBowlCollected}
                magnaBowlDropPosition={magnaBowlDropPosition}
                magnaBowlOnGround={magnaBowlOnGround}
                onMagnaBowlCollect={onGobekliMagnaCollect}
                avatarPositionRef={avatarPositionRef}
              />
            )}

          {/* Capturar referencias */}
          <CameraCapture onReady={onCameraReady} />
          <ModelCapture onLoaded={onModelLoaded} />

          {/* Líneas de alineación solar arqueoastronómica */}
          {location && (
            <SolarAlignmentLines
              latitude={location.lat}
              visible={showAlignmentLines ?? false}
              length={120}
            />
          )}

          {/* Zoom cinematogrÃ¡fico al entrar - SOLO en modo Ã³rbita */}
          {movementMode === 'orbit' && <CinematicZoom />}

          {/* Post-processing modular — desactivado en mobile para mejor rendimiento */}
          <PostProcessingSystem
            enableBloom={typeof window !== 'undefined' ? !(/Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768) : true}
            enableVignette={typeof window !== 'undefined' ? !(/Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768) : true}
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
                modelPath={getAssetPath('/fuente_magna.glb')}
                position={[0, 0.5, 0]}
                onCollect={onCollectItem}
              />
            )}

          {/* 🐒 Geoglifo: Monos de Nazca — Lago Titicaca, sobre la montaña */}
          {location &&
            location.lat > -16.5 && location.lat < -15.5 &&
            location.lon > -70 && location.lon < -68.5 && (
              <TerrainGeoglyph svgPath="/geoglyphs/monos.svg" x={-83} z={-67} size={18} seed={Math.floor(location.lat * 1000 + location.lon * 1000)} />
            )}
        </Canvas>
      </ObjectSelectionProvider>

      {/* Mensaje de item recolectado - FUERA del Canvas */}
      {showCollectedMessage && onCloseMessage && (
        <ItemCollectedMessage onClose={onCloseMessage} />
      )}

      {/* Diálogo de Viracocha - FUERA del Canvas */}
      {showViracochaDialogue && (
        <ViracochaDialogue
          message={magnaBowlCollected
            ? "¡Gracias, viajero! Has traído lo que necesitaba."
            : "¡Atraviesa el portal, y tráeme lo que necesito!"}
          onComplete={onCloseViracochaDialogue}
        />
      )}

      {/* Diálogo Interactivo de Viracocha */}
      {showViracochaInteractive && (
        <ViracochaInteractiveDialogue
          missionCompleted={isMissionCompleted('pumaPunku', 'reveal_structure')}
          allMissionsCompleted={loadMissionState().stats.totalMissionsCompleted >= 5}
          magnaBowlReturned={magnaBowlCollected}
          onClose={onCloseViracochaInteractive || (() => { })}
          onLendMagnaBowl={onLendMagnaBowl}
        />
      )}

    </>
  )
}


// Roca soltada del inventario — clickeable para recoger
function DroppedRock({ position, onCollect, canCollect }: {
  position: [number, number, number]
  onCollect?: () => void
  canCollect?: boolean
}) {
  const { scene } = useGLTF(getAssetPath('/rock_blender.glb'))
  const cloned = useMemo(() => scene.clone(true), [scene])
  const [hovered, setHovered] = useState(false)
  return (
    <group
      position={position}
      onClick={(e) => { if (!canCollect || !onCollect) return; e.stopPropagation(); onCollect() }}
      onPointerOver={() => { if (canCollect) { setHovered(true); document.body.style.cursor = 'pointer' } }}
      onPointerOut={() => { setHovered(false); document.body.style.cursor = 'default' }}
    >
      <primitive object={cloned} scale={0.3} />
      {hovered && canCollect && (
        <mesh>
          <sphereGeometry args={[0.8, 12, 12]} />
          <meshBasicMaterial color="#ffff00" wireframe transparent opacity={0.3} />
        </mesh>
      )}
    </group>
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

// Geoglifo posicionado sobre el terreno altiplano
// Replica la función de ruido de VolcanicTerrain para calcular la altura exacta
function TerrainGeoglyph({ svgPath, x, z, size, seed }: {
  svgPath: string; x: number; z: number; size: number; seed: number
}) {
  const terrainHeight = useMemo(() => {
    const noise = (px: number, py: number, scale: number, offset: number) =>
      Math.sin((px + offset) * scale) * Math.cos((py + offset) * scale)

    const amplitudeFactor = 22.0
    const roughnessFactor = 1.4
    const s = seed * 0.001

    const baseNoise = (
      noise(x, z, 0.02, s) * 0.5 +
      noise(x, z, 0.05, s * 1.3) * 0.3 +
      noise(x, z, 0.1, s * 0.7) * 0.15 +
      noise(x, z, 0.35, s * 0.05) * 0.05
    ) * amplitudeFactor

    const ridgeNoise = (
      Math.abs(noise(x, z, 0.03, s * 2)) * 0.6 +
      Math.abs(noise(x, z, 0.08, s * 1.5)) * 0.25 +
      Math.abs(noise(x, z, 0.2, s * 0.8)) * 0.15
    ) * amplitudeFactor * roughnessFactor

    return baseNoise * 0.5 + ridgeNoise * 0.5 + 0.5 // +0.5 margen sobre la superficie
  }, [x, z, seed])

  return <GeoglyphDirect svgPath={svgPath} position={[x, terrainHeight + 3, z]} size={size} vertical={true} />
}

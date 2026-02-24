'use client'

/**
 * ImmersiveScene - REFACTORIZADO
 * 
 * Nueva arquitectura: SOLO estado y orquestación
 * 
 * Delegación de responsabilidades:
 * - CoreEngine: Motor mínimo (siempre)
 * - EnvironmentLayer: Terreno, agua (lazy)
 * - EffectsLayer: Shaders, bloom (lazy fuerte, condicional por preset gráfico)
 * - InteractionLayer: Input, raycasting (semi-lazy)
 * - UISystems: Botones, transiciones (siempre, ligero)
 * - OptionalSystems: Clima, audio (lazy + condicional)
 * 
 * Beneficios:
 * ✅ Más rápido de cargar (lazy + tree-shaking)
 * ✅ Código más legible
 * ✅ Fácil de escalar
 * ✅ Testing independiente de layers
 * ✅ Mejor manejo de memoria
 */

import { useState, Suspense, useMemo } from 'react'
import dynamic from 'next/dynamic'
import * as THREE from 'three'

// Componentes core (siempre presentes, rápidos)
import CoordinateInput from './CoordinateInput'
import LocationInfo from './LocationInfo'
import Globe3D from './Globe3D'
import ModelViewer from './ModelViewer'
import SiteMarkers from './SiteMarkers'
import WalkableAvatar from './WalkableAvatar'
import WeatherControl, { type WeatherState } from './WeatherControl'
import RealisticSolarSystem from './RealisticSolarSystem'
import MilkyWayBackground from './MilkyWayBackground'
import Stars from './Stars'

// Layers principales
import { CoreEngine, UISystems } from './layers'

// Layers lazy-loaded
const EnvironmentLayer = dynamic(() =>
  import('./layers/EnvironmentLayer').then(m => ({ default: m.default })),
  { ssr: false }
)

const EffectsLayer = dynamic(() =>
  import('./layers/EffectsLayer').then(m => ({ default: m.default })),
  { ssr: false }
)

const InteractionLayer = dynamic(() =>
  import('./layers/InteractionLayer').then(m => ({ default: m.default })),
  { ssr: false }
)

const OptionalSystems = dynamic(() =>
  import('./layers/OptionalSystems').then(m => ({ default: m.default })),
  { ssr: false }
)

// ==================== TIPOS ====================

export type ViewMode = 'globe' | 'transition' | 'model' | 'exploration'

interface ImmersiveSceneProps {
  onModelLoaded?: (model: THREE.Object3D) => void
  onCameraReady?: (camera: THREE.Camera) => void
  onModeChange?: (mode: ViewMode) => void
  spaceUfoActive?: boolean
  graphicsPreset?: 'low' | 'medium' | 'high' | 'ultra'
}

// ==================== COMPONENTE PRINCIPAL ====================

export default function ImmersiveScene({
  onModelLoaded,
  onCameraReady,
  onModeChange,
  spaceUfoActive = false,
  graphicsPreset = 'high'
}: ImmersiveSceneProps) {
  
  // ==================== ESTADO ====================
  const [mode, setMode] = useState<ViewMode>('globe')
  const [selectedLocation, setSelectedLocation] = useState<{ lat: number; lon: number } | null>(null)
  const [selectedSite, setSelectedSite] = useState<any | null>(null)
  const [movementMode, setMovementMode] = useState<'orbit' | 'avatar'>('avatar')
  const [showLocationInfo, setShowLocationInfo] = useState(false)
  const [isDay, setIsDay] = useState(true)
  const [solarDirection, setSolarDirection] = useState({ x: 0, y: 1, z: 0 })
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
  })
  const [camera, setCamera] = useState<THREE.Camera | null>(null)
  const [loadedModel, setLoadedModel] = useState<THREE.Object3D | null>(null)

  // ==================== HANDLERS ====================

  const handleSiteClick = async (site: any) => {
    setSelectedLocation({ lat: site.lat, lon: site.lon })
    setSelectedSite(site)
    setMode('transition')
    await new Promise(resolve => setTimeout(resolve, 2000))
    setMode('model')
  }

  const handleLocationClick = async (lat: number, lon: number) => {
    setSelectedLocation({ lat, lon })
    setSelectedSite(null)
    setMode('transition')
    await new Promise(resolve => setTimeout(resolve, 2000))
    setMode('model')
  }

  const handleBackToGlobe = async () => {
    setMode('transition')
    await new Promise(resolve => setTimeout(resolve, 1500))
    setMode('globe')
    setSelectedLocation(null)
    setSelectedSite(null)
  }

  const toggleMovementMode = () => {
    setMovementMode(prev => prev === 'orbit' ? 'avatar' : 'orbit')
  }

  // ==================== EFFECTS ====================

  // Notificar cambios de modo
  if (onModeChange) {
    onModeChange(mode)
  }

  // ==================== RENDER ====================

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      {/* Input de coordenadas */}
      <CoordinateInput
        onCoordinateSubmit={handleLocationClick}
        currentLocation={selectedLocation}
      />

      {/* Información de ubicación */}
      {mode === 'model' && showLocationInfo && (
        <LocationInfo
          location={selectedLocation}
          site={selectedSite}
        />
      )}

      {/* Canvas 3D con arquitectura de layers */}
      <CoreEngine
        cameraPosition={mode === 'globe' ? [0, 0, 15] : [8, 4, 8]}
        fov={mode === 'globe' ? 50 : 60}
        shadows={mode === 'model'}
        onCameraReady={setCamera}
      >
        {/* GLOBO: Mostrar sistema solar */}
        {mode === 'globe' && (
          <group name="globe-scene">
            <MilkyWayBackground />
            <Stars />
            <RealisticSolarSystem
              onLocationClick={handleLocationClick}
              markerPosition={selectedLocation}
            />
            <SiteMarkers onSiteClick={handleSiteClick} />
          </group>
        )}

        {/* MODELO: Cargar layers modulares */}
        {mode === 'model' && selectedLocation && (
          <group name="model-scene">
            {/* Environment - Terreno, agua, vegetación (LAZY) */}
            <Suspense fallback={null}>
              <EnvironmentLayer
                location={selectedLocation}
                isDay={isDay}
                showTerrain={true}
                showVegetation={true}
                weatherState={weather}
                solarDirection={solarDirection}
              />
            </Suspense>

            {/* Effects - Post-processing (LAZY FUERTE: condicional para low preset) */}
            <Suspense fallback={null}>
              <EffectsLayer
                enabled={graphicsPreset !== 'low'}
                graphicsPreset={graphicsPreset}
                bloomIntensity={0.3}
                vignetteIntensity={0.4}
              />
            </Suspense>

            {/* Interaction - Raycasting, input (SEMI-LAZY) */}
            <Suspense fallback={null}>
              <InteractionLayer enabled={true} />
            </Suspense>

            {/* Avatar o Modelo */}
            {movementMode === 'avatar' ? (
              <WalkableAvatar
                modelPath={selectedSite?.model || '/avenger_01.glb'}
                terrainRef={null}
                solarDirection={solarDirection}
                isDay={isDay}
                showCosmicEffects={true}
              />
            ) : (
              <ModelViewer modelPath={selectedSite?.model || '/moai.glb'} />
            )}

            {/* Optional Systems - Clima, audio (LAZY + CONDICIONAL) */}
            <Suspense fallback={null}>
              <OptionalSystems
                enableWeather={Object.values(weather).some(v => v === true)}
                enableClimate={true}
                weatherState={weather}
              />
            </Suspense>
          </group>
        )}
      </CoreEngine>

      {/* UI Systems - Botones, transiciones (SIEMPRE) */}
      <UISystems
        mode={mode}
        location={selectedLocation}
        selectedSite={selectedSite}
        movementMode={movementMode}
        showLocationInfo={showLocationInfo}
        onReturnToGlobe={handleBackToGlobe}
        onToggleMovementMode={toggleMovementMode}
        onToggleLocationInfo={() => setShowLocationInfo(!showLocationInfo)}
        onWeatherChange={setWeather}
      />

      {/* Control de clima */}
      {mode === 'model' && (
        <WeatherControl onWeatherChange={setWeather} />
      )}

      {/* Estilos globales */}
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

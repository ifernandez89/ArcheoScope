/**
 * ImmersiveScene - Versión Refactorizada con Arquitectura de Capas
 * 
 * Reducido de 1,243 líneas a ~250 líneas
 * Arquitectura modular con separación de responsabilidades
 */

'use client'

import { useState, useEffect } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera } from '@react-three/drei'
import * as THREE from 'three'

// Hooks especializados
import { useBiomeSystem } from '@/hooks/useBiomeSystem'
import { useTeleportSystem } from '@/hooks/useTeleportSystem'
import { useWeatherIntegration } from '@/hooks/useWeatherIntegration'

// Capas modulares
import {
  WorldLayer,
  ClimateLayer,
  EnvironmentLayer,
  AvatarLayer,
  UILayer,
  SystemsInitializer
} from './layers'

// Componentes específicos
import Globe3D from './Globe3D'
import SiteMarkers from './SiteMarkers'
import CoordinateInput from './CoordinateInput'
import ConversationalAvatar from './ConversationalAvatar'
import type { WeatherState } from './WeatherControl'
import type { ArchaeologicalSite } from '../engines'
import { getAssetPath } from '@/lib/paths'

// Performance
import EngineIntegration from './EngineIntegration'

export type ViewMode = 'globe' | 'model'

interface ImmersiveSceneProps {
  onModelLoaded?: (model: THREE.Object3D) => void
  onCameraReady?: (camera: THREE.Camera) => void
  onModeChange?: (mode: ViewMode) => void
}

export default function ImmersiveScene({ 
  onModelLoaded, 
  onCameraReady, 
  onModeChange 
}: ImmersiveSceneProps) {
  // ==================== ESTADO ====================
  const [mode, setMode] = useState<ViewMode>('globe')
  const [location, setLocation] = useState<{ lat: number; lon: number } | null>(null)
  const [selectedSite, setSelectedSite] = useState<ArchaeologicalSite | null>(null)
  const [isDay, setIsDay] = useState(true)
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
  
  // ==================== HOOKS ESPECIALIZADOS ====================
  const { biome, skyColor, fogColor, isIceBiome } = useBiomeSystem(location, isDay)
  const { stormDarkness } = useWeatherIntegration(weather)
  const { teleportToLocation, teleportToSite, returnToGlobe } = useTeleportSystem(
    setLocation,
    setMode
  )
  
  // ==================== EFECTOS ====================
  
  // Notificar cambios de modo
  useEffect(() => {
    if (onModeChange) {
      onModeChange(mode)
    }
  }, [mode, onModeChange])
  
  // Notificar cámara lista
  useEffect(() => {
    if (camera && onCameraReady) {
      onCameraReady(camera)
    }
  }, [camera, onCameraReady])
  
  // Notificar modelo cargado
  useEffect(() => {
    if (loadedModel && onModelLoaded) {
      onModelLoaded(loadedModel)
    }
  }, [loadedModel, onModelLoaded])
  
  // ==================== HANDLERS ====================
  
  const handleSiteClick = async (site: ArchaeologicalSite) => {
    setSelectedSite(site)
    await teleportToSite(site)
  }
  
  const handleLocationClick = async (lat: number, lon: number) => {
    setSelectedSite(null)
    await teleportToLocation(lat, lon)
  }
  
  const handleBackToGlobe = () => {
    setSelectedSite(null)
    setLocation(null)
    returnToGlobe()
  }
  
  const handleAvatarReady = (avatar: THREE.Object3D) => {
    setLoadedModel(avatar)
  }
  
  // ==================== CONFIGURACIÓN ====================
  
  const avatarType = selectedSite?.culture === 'Rapa Nui' ? 'moai' : 'humanoid'
  const modelUrl = selectedSite?.model || getAssetPath('/moai.glb')
  
  // ==================== RENDER ====================
  
  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      {/* Inicializar sistemas del motor */}
      <SystemsInitializer enabled={true} />
      
      {/* Canvas 3D */}
      <Canvas
        shadows
        gl={{ 
          antialias: true,
          alpha: false,
          powerPreference: 'high-performance'
        }}
        dpr={[1, 2]}
      >
        {/* Cámara */}
        <PerspectiveCamera
          makeDefault
          position={mode === 'globe' ? [0, 0, 3] : [0, 2, 5]}
          fov={60}
          ref={(cam) => {
            if (cam) setCamera(cam)
          }}
        />
        
        {/* Controles */}
        <OrbitControls
          enablePan={mode === 'model'}
          enableZoom={true}
          enableRotate={true}
          minDistance={mode === 'globe' ? 1.5 : 2}
          maxDistance={mode === 'globe' ? 5 : 50}
          maxPolarAngle={mode === 'model' ? Math.PI / 2 : Math.PI}
        />
        
        {/* Performance Systems */}
        <EngineIntegration />
        
        {/* ==================== MODO GLOBO ==================== */}
        {mode === 'globe' && (
          <group name="globe-mode">
            <Globe3D onLocationClick={handleLocationClick} />
            <SiteMarkers onSiteClick={handleSiteClick} />
            <CoordinateInput onCoordinateSubmit={handleLocationClick} />
          </group>
        )}
        
        {/* ==================== MODO MODELO ==================== */}
        {mode === 'model' && location && (
          <group name="model-mode">
            {/* Capa de Mundo */}
            <WorldLayer
              location={location}
              isDay={isDay}
              showTerrain={true}
            />
            
            {/* Capa de Entorno */}
            <EnvironmentLayer
              location={location}
              isDay={isDay}
              weather={weather}
              enabled={true}
            />
            
            {/* Capa de Clima */}
            <ClimateLayer
              weather={weather}
              isIceBiome={isIceBiome}
              enabled={true}
            />
            
            {/* Capa de Avatar */}
            <AvatarLayer
              enabled={true}
              modelUrl={modelUrl}
              avatarType={avatarType}
              camera={camera}
              onAvatarReady={handleAvatarReady}
            />
          </group>
        )}
      </Canvas>
      
      {/* ==================== UI LAYER ==================== */}
      <UILayer
        mode={mode}
        location={location}
        showLocationInfo={true}
        onWeatherChange={setWeather}
        onReturnToGlobe={handleBackToGlobe}
      />
      
      {/* Avatar Conversacional */}
      {mode === 'model' && (
        <ConversationalAvatar
          model={loadedModel}
          camera={camera}
        />
      )}
      
      {/* Estilos */}
      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
      `}</style>
    </div>
  )
}

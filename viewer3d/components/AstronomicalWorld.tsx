'use client'

/**
 * AstronomicalWorld - Sistema vivo astronómico-geométrico
 * Respiración lenta, transiciones suaves, contemplativo
 * NO crea luces, solo las controla
 */

import { useRef, useEffect, useMemo } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'
import { SolarEngine, SeasonalLight, MicroMotion, SkyEngine, GeometryField, AtmosphericSound } from '../engines'

interface AstronomicalWorldProps {
  location?: { lat: number, lon: number } | null
  enabled?: boolean
  showGeometry?: boolean
  onStateChange?: (state: any) => void
  onDayNightChange?: (isDay: boolean) => void
  onSolarUpdate?: (
    direction: { x: number, y: number, z: number }, 
    altitude: number, 
    azimuth: number, 
    declination: number,
    fullState?: any // Estado completo del SolarEngine
  ) => void
}

export default function AstronomicalWorld({
  location,
  enabled = true,
  showGeometry = false,
  onStateChange,
  onDayNightChange,
  onSolarUpdate
}: AstronomicalWorldProps) {
  const { scene, camera } = useThree()
  
  // Motores
  const solarEngine = useRef<SolarEngine | null>(null)
  const seasonalLight = useRef<SeasonalLight | null>(null)
  const microMotion = useRef<MicroMotion | null>(null)
  const skyEngine = useRef<SkyEngine | null>(null)
  const geometryField = useRef<GeometryField | null>(null)
  const atmosphericSound = useRef<AtmosphericSound | null>(null)
  
  // Cache de luces para evitar traverse cada frame
  const cachedLights = useRef<{
    directional: THREE.DirectionalLight[]
    ambient: THREE.AmbientLight[]
    hemisphere: THREE.HemisphereLight[]
    physicalSky: THREE.Object3D | null
    stars: THREE.Points | null
  }>({ directional: [], ambient: [], hemisphere: [], physicalSky: null, stars: null })
  const lightsCached = useRef(false)
  
  // Vector reutilizable
  const sunPos = useMemo(() => new THREE.Vector3(), [])
  
  // Estado de cámara
  const baseCameraPosition = useRef(new THREE.Vector3())
  const cameraOffset = useRef(new THREE.Vector3())
  
  // Inicializar motores
  useEffect(() => {
    const lat = location?.lat || 0
    const lon = location?.lon || 0
    
    solarEngine.current = new SolarEngine(lat, lon)
    seasonalLight.current = new SeasonalLight()
    microMotion.current = new MicroMotion()
    skyEngine.current = new SkyEngine(lat)
    geometryField.current = new GeometryField(scene)
    atmosphericSound.current = new AtmosphericSound()
    
    // Guardar posición base de cámara
    baseCameraPosition.current.copy(camera.position)
    
    console.log('🌍 AstronomicalWorld inicializado:', {
      latitud: lat,
      longitud: lon,
      enabled,
      showGeometry
    })
    
    // Inicializar audio al primer click (requiere interacción del usuario)
    const initAudio = async () => {
      if (atmosphericSound.current) {
        await atmosphericSound.current.initialize()
        atmosphericSound.current.setEnabled(true)
        window.removeEventListener('click', initAudio)
        window.removeEventListener('keydown', initAudio)
      }
    }
    window.addEventListener('click', initAudio, { once: true })
    window.addEventListener('keydown', initAudio, { once: true })
    
    return () => {
      // Cleanup
      if (geometryField.current) {
        const group = scene.getObjectByName('GeometryField')
        if (group) scene.remove(group)
      }
      if (atmosphericSound.current) {
        atmosphericSound.current.dispose()
      }
      window.removeEventListener('click', initAudio)
      window.removeEventListener('keydown', initAudio)
    }
  }, [location, scene, camera])
  
  // Actualizar latitud y longitud cuando cambia ubicación
  useEffect(() => {
    if (location && solarEngine.current && skyEngine.current) {
      solarEngine.current.setLocation(location.lat, location.lon)
      skyEngine.current.setLatitude(location.lat)
    }
  }, [location])
  
  // Toggle geometría
  useEffect(() => {
    if (geometryField.current) {
      if (showGeometry) {
        geometryField.current.show()
      } else {
        geometryField.current.hide()
      }
    }
  }, [showGeometry])
  
  // Notificar actividad del usuario
  useEffect(() => {
    const handleUserActivity = () => {
      if (microMotion.current) {
        microMotion.current.notifyUserActivity()
      }
    }
    
    window.addEventListener('keydown', handleUserActivity)
    window.addEventListener('mousemove', handleUserActivity)
    window.addEventListener('wheel', handleUserActivity)
    
    return () => {
      window.removeEventListener('keydown', handleUserActivity)
      window.removeEventListener('mousemove', handleUserActivity)
      window.removeEventListener('wheel', handleUserActivity)
    }
  }, [])
  
  // Loop principal - SOLO actualiza luces existentes, no crea nuevas
  useFrame((state, delta) => {
    if (!enabled) return
    if (!solarEngine.current || !seasonalLight.current || !microMotion.current) return
    if (!skyEngine.current || !geometryField.current) return
    
    // Actualizar motores
    const solarState = solarEngine.current.update(delta)
    const seasonalState = seasonalLight.current.update(delta)
    const motionState = microMotion.current.update(delta)
    const skyState = skyEngine.current.update(delta, solarState.solarAltitude)
    
    // Actualizar sonido atmosférico
    if (atmosphericSound.current) {
      atmosphericSound.current.update(delta, solarState.solarAltitude, motionState.windIntensity)
    }
    
    // Debug cada 5 segundos
    if (Math.floor(state.clock.elapsedTime) % 5 === 0 && Math.floor(state.clock.elapsedTime * 10) % 10 === 0) {
      console.log('🌞 Estado Solar:', {
        altitude: (solarState.solarAltitude * 180 / Math.PI).toFixed(2) + '°',
        azimuth: (solarState.solarAzimuth * 180 / Math.PI).toFixed(2) + '°',
        isDay: solarState.isDay,
        direction: solarState.sunDirection,
        hora: new Date().toLocaleTimeString()
      })
      console.log('🎨 Estado Estacional:', {
        factor: seasonalState.seasonFactor.toFixed(2),
        season: seasonalState.seasonName,
        color: seasonalState.lightColor
      })
      console.log('🌬️ Micro-movimiento:', {
        cameraSway: motionState.cameraSway.length().toFixed(4),
        windIntensity: motionState.windIntensity.toFixed(4)
      })
    }
    
    // Buscar y actualizar luces existentes en la escena
    // OPTIMIZACIÓN: Cachear referencias a luces para evitar traverse cada frame
    if (!lightsCached.current) {
      cachedLights.current = { directional: [], ambient: [], hemisphere: [], physicalSky: null, stars: null }
      scene.traverse((object) => {
        if (object instanceof THREE.DirectionalLight && object.castShadow) {
          cachedLights.current.directional.push(object)
        }
        if (object instanceof THREE.AmbientLight) {
          cachedLights.current.ambient.push(object)
        }
        if (object instanceof THREE.HemisphereLight) {
          cachedLights.current.hemisphere.push(object)
        }
        if (object.name === 'PhysicalSky') {
          cachedLights.current.physicalSky = object
        }
        if (object.name === 'Stars') {
          cachedLights.current.stars = object as THREE.Points
        }
      })
      lightsCached.current = true
    }
    
    // Actualizar luces cacheadas
    sunPos.copy(solarState.sunDirection).multiplyScalar(50)
    
    cachedLights.current.directional.forEach(light => {
      light.position.lerp(sunPos, 0.01)
      light.color.lerp(seasonalState.lightColor, 0.005)
      const baseIntensity = solarState.isDay ? 2.5 : 0.3
      const targetIntensity = baseIntensity + motionState.atmosphericPulse
      light.intensity += (targetIntensity - light.intensity) * 0.01
    })
    
    cachedLights.current.ambient.forEach(light => {
      const baseAmbient = solarState.isDay ? 0.4 : 0.1
      const targetIntensity = baseAmbient + motionState.atmosphericPulse
      light.intensity += (targetIntensity - light.intensity) * 0.01
    })
    
    cachedLights.current.hemisphere.forEach(light => {
      const targetIntensity = seasonalState.ambientIntensity + motionState.atmosphericPulse
      light.intensity += (targetIntensity - light.intensity) * 0.01
    })
    
    // Actualizar PhysicalSky
    if (cachedLights.current.physicalSky) {
      const material = (cachedLights.current.physicalSky as any).material
      if (material?.uniforms?.sunPosition) {
        material.uniforms.sunPosition.value.copy(solarState.sunDirection)
      }
    }
    
    // Actualizar estrellas
    if (cachedLights.current.stars?.material) {
      const material = cachedLights.current.stars.material as THREE.PointsMaterial
      const targetOpacity = solarState.isDay ? 0 : 0.8
      if (material.opacity !== undefined) {
        material.opacity += (targetOpacity - material.opacity) * 0.01
      }
    }
    
    // Micro-oscilación de cámara (solo si no está en modo avatar)
    if (motionState.cameraSway.length() > 0) {
      cameraOffset.current.lerp(motionState.cameraSway, 0.05)
      // Aplicar offset sutil
      camera.position.x = baseCameraPosition.current.x + cameraOffset.current.x
      camera.position.y = baseCameraPosition.current.y + cameraOffset.current.y
      camera.position.z = baseCameraPosition.current.z + cameraOffset.current.z
    } else {
      // Actualizar posición base
      baseCameraPosition.current.copy(camera.position)
      cameraOffset.current.multiplyScalar(0.95) // Decay suave
    }
    
    // Actualizar campo geométrico
    geometryField.current.updateSolarAxis(solarState.sunDirection)
    geometryField.current.update(delta)
    
    // Notificar cambio de día/noche
    if (onDayNightChange) {
      onDayNightChange(solarState.isDay)
    }
    
    // Notificar dirección solar con información completa
    if (onSolarUpdate) {
      onSolarUpdate(
        { x: solarState.sunDirection.x, y: solarState.sunDirection.y, z: solarState.sunDirection.z },
        solarState.solarAltitude,
        solarState.solarAzimuth,
        solarState.declination,
        solarState // Pasar estado completo
      )
    }
    
    // Notificar cambios de estado
    if (onStateChange) {
      onStateChange({
        solar: solarState,
        seasonal: seasonalState,
        motion: motionState,
        sky: skyState
      })
    }
  })
  
  // NO renderiza nada, solo controla
  return null
}

'use client'

/**
 * AstronomicalWorld - Sistema vivo astronómico-geométrico
 * Respiración lenta, transiciones suaves, contemplativo
 * NO crea luces, solo las controla
 */

import { useRef, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'
import { SolarEngine, SeasonalLight, MicroMotion, SkyEngine, GeometryField, AtmosphericSound } from '../engines'

interface AstronomicalWorldProps {
  location?: { lat: number, lon: number } | null
  enabled?: boolean
  showGeometry?: boolean
  onStateChange?: (state: any) => void
  onDayNightChange?: (isDay: boolean) => void
}

export default function AstronomicalWorld({
  location,
  enabled = true,
  showGeometry = false,
  onStateChange,
  onDayNightChange
}: AstronomicalWorldProps) {
  const { scene, camera } = useThree()
  
  // Motores
  const solarEngine = useRef<SolarEngine | null>(null)
  const seasonalLight = useRef<SeasonalLight | null>(null)
  const microMotion = useRef<MicroMotion | null>(null)
  const skyEngine = useRef<SkyEngine | null>(null)
  const geometryField = useRef<GeometryField | null>(null)
  const atmosphericSound = useRef<AtmosphericSound | null>(null)
  
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
    scene.traverse((object) => {
      if (object instanceof THREE.DirectionalLight && object.castShadow) {
        // Actualizar posición del sol basada en cálculos astronómicos reales
        const sunPos = solarState.sunDirection.clone().multiplyScalar(50)
        object.position.lerp(sunPos, 0.01)
        
        // Color estacional
        object.color.lerp(seasonalState.lightColor, 0.005)
        
        // Intensidad según altura solar REAL
        const baseIntensity = solarState.isDay ? 2.5 : 0.3
        const targetIntensity = baseIntensity + motionState.atmosphericPulse
        object.intensity += (targetIntensity - object.intensity) * 0.01
      }
      
      if (object instanceof THREE.AmbientLight) {
        const baseAmbient = solarState.isDay ? 0.4 : 0.1
        const targetIntensity = baseAmbient + motionState.atmosphericPulse
        object.intensity += (targetIntensity - object.intensity) * 0.01
      }
      
      if (object instanceof THREE.HemisphereLight) {
        const targetIntensity = seasonalState.ambientIntensity + motionState.atmosphericPulse
        object.intensity += (targetIntensity - object.intensity) * 0.01
      }
      
      // Actualizar PhysicalSky con posición solar real
      if (object.name === 'PhysicalSky' && (object as any).material) {
        const material = (object as any).material
        if (material.uniforms && material.uniforms.sunPosition) {
          // Actualizar posición del sol en el shader del cielo
          material.uniforms.sunPosition.value.copy(solarState.sunDirection)
        }
      }
      
      // Actualizar visibilidad de estrellas según hora del día
      if (object.name === 'Stars') {
        const starsGroup = object as THREE.Points
        if (starsGroup.material) {
          const material = starsGroup.material as THREE.PointsMaterial
          // Estrellas visibles solo de noche
          const targetOpacity = solarState.isDay ? 0 : 0.8
          if (material.opacity !== undefined) {
            material.opacity += (targetOpacity - material.opacity) * 0.01
          }
        }
      }
    })
    
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

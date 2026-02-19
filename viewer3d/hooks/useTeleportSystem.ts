/**
 * useTeleportSystem - Hook para gestión de teletransporte
 * Extrae lógica de navegación entre globo y escena 3D
 */

import { useState, useCallback } from 'react'
import eventBus, { EVENTS } from '@/core/EventBus'
import { loggers } from '@/core/Logger'

export type ViewMode = 'globe' | 'model'

interface Location {
  lat: number
  lon: number
}

interface ArchaeologicalSite {
  name: string
  lat: number
  lon: number
  description: string
}

export function useTeleportSystem(
  onLocationChange: (location: Location) => void,
  onModeChange: (mode: ViewMode) => void
) {
  const [isTeleporting, setIsTeleporting] = useState(false)
  
  /**
   * Teletransporte a coordenadas específicas
   */
  const teleportToLocation = useCallback(async (lat: number, lon: number) => {
    if (isTeleporting) return
    
    setIsTeleporting(true)
    
    loggers.world.info(`Teletransporte a: lat=${lat.toFixed(4)}, lon=${lon.toFixed(4)}`)
    
    // Emitir evento
    eventBus.emit(EVENTS.WORLD.TELEPORT, { lat, lon })
    
    // Actualizar ubicación
    onLocationChange({ lat, lon })
    
    // Cambiar a vista de modelo
    onModeChange('model')
    
    // Emitir evento de cambio de ubicación
    eventBus.emit(EVENTS.WORLD.LOCATION_CHANGE, { lat, lon })
    
    // Simular delay de teletransporte
    await new Promise(resolve => setTimeout(resolve, 500))
    
    setIsTeleporting(false)
    
    loggers.world.info('Teletransporte completado')
  }, [isTeleporting, onLocationChange, onModeChange])
  
  /**
   * Teletransporte a sitio arqueológico
   */
  const teleportToSite = useCallback(async (site: ArchaeologicalSite) => {
    if (isTeleporting) return
    
    loggers.world.info(`Teletransporte a sitio: ${site.name}`)
    
    await teleportToLocation(site.lat, site.lon)
  }, [isTeleporting, teleportToLocation])
  
  /**
   * Volver al globo
   */
  const returnToGlobe = useCallback(() => {
    onModeChange('globe')
    
    eventBus.emit(EVENTS.CAMERA.MODE_CHANGE, { mode: 'globe' })
    
    loggers.world.info('Regreso al globo')
  }, [onModeChange])
  
  return {
    teleportToLocation,
    teleportToSite,
    returnToGlobe,
    isTeleporting
  }
}

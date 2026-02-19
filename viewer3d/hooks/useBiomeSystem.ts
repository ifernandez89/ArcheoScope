/**
 * useBiomeSystem - Hook para gestión de biomas
 * Extrae lógica de detección y configuración de biomas
 */

import { useState, useEffect, useMemo } from 'react'
import { detectBiome, getSkyColorForBiome, getFogColorForBiome, type BiomeInfo } from '@/utils/biome-detector'
import eventBus, { EVENTS } from '@/core/EventBus'
import { loggers } from '@/core/Logger'

interface Location {
  lat: number
  lon: number
}

export function useBiomeSystem(location: Location | null, isDay: boolean) {
  // Detectar bioma
  const biome: BiomeInfo = useMemo(() => {
    if (!location) {
      return {
        type: 'default',
        name: 'Terreno Genérico',
        description: 'Paisaje variado',
        temperature: 20,
        humidity: 50
      }
    }
    return detectBiome(location.lat, location.lon)
  }, [location])
  
  // Colores dinámicos según bioma
  const skyColor = useMemo(() => 
    getSkyColorForBiome(biome.type, isDay), 
    [biome.type, isDay]
  )
  
  const fogColor = useMemo(() => 
    getFogColorForBiome(biome.type), 
    [biome.type]
  )
  
  // Verificar si es bioma helado
  const isIceBiome = biome.type === 'ice'
  
  // Emitir evento cuando cambia el bioma
  useEffect(() => {
    if (location) {
      eventBus.emit(EVENTS.WORLD.BIOME_CHANGE, {
        biome: biome.type,
        name: biome.name,
        location
      })
      
      loggers.world.debug(`Bioma: ${biome.name} (${biome.type})`)
      loggers.world.debug(`Temp: ${biome.temperature}°C, Humedad: ${biome.humidity}%`)
    }
  }, [biome, location])
  
  return {
    biome,
    skyColor,
    fogColor,
    isIceBiome
  }
}

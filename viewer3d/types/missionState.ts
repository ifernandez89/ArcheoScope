/**
 * Estado de misiones del juego
 * Registra progreso en cada sitio arqueológico
 */

export interface SiteProgress {
  discovered: boolean
  viracochaRevealed?: boolean
  sphinxReceivedPyramidion?: boolean // Para Giza - si la Esfinge ya recibió el piramidón
  weatherCleared: boolean // Si el clima ya fue desbloqueado (bueno)
  itemsCollected: string[]
  npcsInteracted: string[]
  objectsMoved: string[]
  missionsCompleted: string[]
  subSites?: {
    [key: string]: {
      discovered: boolean
      itemsCollected: string[]
      missionsCompleted: string[]
    }
  }
}

export interface MissionState {
  // Sitios principales
  sites: {
    pumaPunku: SiteProgress
    giza: SiteProgress
    easterIsland: SiteProgress
    teotihuacan: SiteProgress
    angkorWat: SiteProgress
  }
  
  // Estadísticas globales
  stats: {
    totalItemsCollected: number
    totalNPCsInteracted: number
    totalMissionsCompleted: number
    totalSitesDiscovered: number
    playTime: number // en segundos
  }
  
  // Información
  lastUpdated: string
}

export const DEFAULT_MISSION_STATE: MissionState = {
  sites: {
    pumaPunku: {
      discovered: false,
      viracochaRevealed: false,
      weatherCleared: false,
      itemsCollected: [],
      npcsInteracted: [],
      objectsMoved: [],
      missionsCompleted: [],
      subSites: {
        lagoTiticaca: {
          discovered: false,
          itemsCollected: [],
          missionsCompleted: []
        }
      }
    },
    giza: {
      discovered: false,
      sphinxReceivedPyramidion: false,
      weatherCleared: false,
      itemsCollected: [],
      npcsInteracted: [],
      objectsMoved: [],
      missionsCompleted: [],
      subSites: {
        valleyTemple: {
          discovered: false,
          itemsCollected: [],
          missionsCompleted: []
        }
      }
    },
    easterIsland: {
      discovered: false,
      weatherCleared: false,
      itemsCollected: [],
      npcsInteracted: [],
      objectsMoved: [],
      missionsCompleted: [],
      subSites: {
        ranoRaraku: {
          discovered: false,
          itemsCollected: [],
          missionsCompleted: []
        }
      }
    },
    teotihuacan: {
      discovered: false,
      weatherCleared: false,
      itemsCollected: [],
      npcsInteracted: [],
      objectsMoved: [],
      missionsCompleted: [],
      subSites: {
        temploDeLaLuna: {
          discovered: false,
          itemsCollected: [],
          missionsCompleted: []
        }
      }
    },
    angkorWat: {
      discovered: false,
      weatherCleared: false,
      itemsCollected: [],
      npcsInteracted: [],
      objectsMoved: [],
      missionsCompleted: [],
      subSites: {
        bayonTemple: {
          discovered: false,
          itemsCollected: [],
          missionsCompleted: []
        }
      }
    }
  },
  
  stats: {
    totalItemsCollected: 0,
    totalNPCsInteracted: 0,
    totalMissionsCompleted: 0,
    totalSitesDiscovered: 0,
    playTime: 0
  },
  
  lastUpdated: new Date().toISOString()
}

/**
 * Guardar estado de misiones
 */
export function saveMissionState(state: MissionState): void {
  if (typeof window !== 'undefined') {
    state.lastUpdated = new Date().toISOString()
    localStorage.setItem('mission_state', JSON.stringify(state))
    console.log('📜 Estado de misiones guardado:', state)
  }
}

/**
 * Cargar estado de misiones
 */
export function loadMissionState(): MissionState {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('mission_state')
    if (saved) {
      try {
        const state = JSON.parse(saved) as MissionState
        console.log('📜 Estado de misiones cargado:', state)
        return state
      } catch (error) {
        console.error('Error al cargar estado de misiones:', error)
        return DEFAULT_MISSION_STATE
      }
    }
  }
  return DEFAULT_MISSION_STATE
}

/**
 * Marcar sitio como descubierto
 */
export function discoverSite(siteName: keyof MissionState['sites']): void {
  const state = loadMissionState()
  if (!state.sites[siteName].discovered) {
    state.sites[siteName].discovered = true
    state.stats.totalSitesDiscovered++
    saveMissionState(state)
    console.log(`🗺️ Sitio descubierto: ${siteName}`)
  }
}

/**
 * Recolectar item en un sitio
 */
export function collectItem(siteName: keyof MissionState['sites'], itemId: string): void {
  const state = loadMissionState()
  if (!state.sites[siteName].itemsCollected.includes(itemId)) {
    state.sites[siteName].itemsCollected.push(itemId)
    state.stats.totalItemsCollected++
    saveMissionState(state)
    console.log(`📦 Item recolectado en ${siteName}: ${itemId}`)
  }
}

/**
 * Interactuar con NPC
 */
export function interactWithNPC(siteName: keyof MissionState['sites'], npcId: string): void {
  const state = loadMissionState()
  if (!state.sites[siteName].npcsInteracted.includes(npcId)) {
    state.sites[siteName].npcsInteracted.push(npcId)
    state.stats.totalNPCsInteracted++
    saveMissionState(state)
    console.log(`💬 NPC interactuado en ${siteName}: ${npcId}`)
  }
}

/**
 * Mover objeto
 */
export function moveObject(siteName: keyof MissionState['sites'], objectId: string): void {
  const state = loadMissionState()
  if (!state.sites[siteName].objectsMoved.includes(objectId)) {
    state.sites[siteName].objectsMoved.push(objectId)
    saveMissionState(state)
    console.log(`🔄 Objeto movido en ${siteName}: ${objectId}`)
  }
}

/**
 * Completar misión
 */
export function completeMission(siteName: keyof MissionState['sites'], missionId: string): void {
  const state = loadMissionState()
  if (!state.sites[siteName].missionsCompleted.includes(missionId)) {
    state.sites[siteName].missionsCompleted.push(missionId)
    state.stats.totalMissionsCompleted++
    saveMissionState(state)
    console.log(`✅ Misión completada en ${siteName}: ${missionId}`)
    
    // 🎼 Activar capa de Harmonia Mundi
    // Las 5 primeras misiones de la Tierra desbloquean capas sonoras
    if (typeof window !== 'undefined') {
      import('../systems/HarmoniaMundiSystem').then(async ({ getHarmoniaMundi }) => {
        const harmonia = getHarmoniaMundi()
        
        // Habilitar si es la primera misión
        if (!harmonia.isEnabled()) {
          try {
            await harmonia.enable()
            console.log('🎼 Harmonia Mundi habilitado por primera misión')
          } catch (error) {
            console.error('Error habilitando Harmonia Mundi:', error)
            return
          }
        }
        
        const totalMissions = state.stats.totalMissionsCompleted
        const layerId = `earth_mission_${totalMissions}`
        harmonia.unlockMissionLayer(layerId)
        
        console.log(`🎵 Capa ${layerId} desbloqueada (${totalMissions}/5 misiones completadas)`)
      })
    }
  }
}

/**
 * Revelar Viracocha en Puma Punku
 */
export function revealViracocha(): void {
  const state = loadMissionState()
  state.sites.pumaPunku.viracochaRevealed = true
  saveMissionState(state)
  console.log('🗿 Viracocha revelado en Puma Punku')
}

/**
 * Actualizar tiempo de juego
 */
export function updatePlayTime(seconds: number): void {
  const state = loadMissionState()
  state.stats.playTime += seconds
  saveMissionState(state)
}

/**
 * Resetear estado de misiones
 */
export function resetMissionState(): void {
  saveMissionState(DEFAULT_MISSION_STATE)
  
  // Limpiar sessionStorage relacionado con misiones
  if (typeof window !== 'undefined') {
    sessionStorage.removeItem('item_magna_bowl_collected')
    sessionStorage.removeItem('item_pyramidion_collected')
    sessionStorage.removeItem('giza_pyramidion_on_top')
  }
  
  console.log('🔄 Estado de misiones reseteado')
}

/**
 * Marcar que la Esfinge recibió el piramidón
 */
export function sphinxReceivePyramidion(): void {
  const state = loadMissionState()
  state.sites.giza.sphinxReceivedPyramidion = true
  saveMissionState(state)
  console.log('🗿 La Esfinge ha recibido el piramidón')
}

/**
 * Verificar si la Esfinge ya recibió el piramidón
 */
export function hasSphinxReceivedPyramidion(): boolean {
  const state = loadMissionState()
  return state.sites.giza.sphinxReceivedPyramidion === true
}

/**
 * Limpiar el clima de un sitio (marcar como completado)
 */
export function clearWeather(siteName: keyof MissionState['sites']): void {
  const state = loadMissionState()
  state.sites[siteName].weatherCleared = true
  saveMissionState(state)
  console.log(`☀️ Clima limpiado en ${siteName}`)
}

/**
 * Verificar si el clima de un sitio está limpio
 */
export function isWeatherCleared(siteName: keyof MissionState['sites']): boolean {
  const state = loadMissionState()
  return state.sites[siteName].weatherCleared === true
}

/**
 * Marcar misión como fallida (ej: robar el escarabajo en Giza)
 */
export function failMission(siteName: keyof MissionState['sites'], missionId: string): void {
  const state = loadMissionState()
  const failedId = `FAILED_${missionId}`
  if (!state.sites[siteName].missionsCompleted.includes(failedId)) {
    state.sites[siteName].missionsCompleted.push(failedId)
    saveMissionState(state)
    console.log(`❌ Misión FALLIDA en ${siteName}: ${missionId}`)
  }
}

/**
 * Verificar si una misión específica está completada
 */
export function isMissionCompleted(siteName: keyof MissionState['sites'], missionId: string): boolean {
  const state = loadMissionState()
  return state.sites[siteName].missionsCompleted.includes(missionId)
}

/**
 * Verificar si una misión específica está fallida
 */
export function isMissionFailed(siteName: keyof MissionState['sites'], missionId: string): boolean {
  const state = loadMissionState()
  return state.sites[siteName].missionsCompleted.includes(`FAILED_${missionId}`)
}

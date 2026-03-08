/**
 * Estado del jugador y su nave
 */

export interface PlayerState {
  // Información del jugador
  playerName: string
  createdAt: string
  lastPlayed: string
  
  // Nave seleccionada
  ship: {
    id: string
    name: string
    model: string
    specialty: string
    description: string
    ability: string
    missions: string
  }
  
  // Última ubicación
  lastLocation: {
    lat: number
    lon: number
    mode: 'globe' | 'model' // En qué modo estaba
  } | null
  
  // Estadísticas de juego
  stats: {
    totalPlayTime: number // en segundos
    sitesVisited: string[]
    itemsCollected: string[]
    missionsCompleted: string[]
  }
  
  // Progreso de misiones
  progress: {
    viracochaRevealed: boolean
    gateRevealed: boolean
    magnaBowlCollected: boolean
    pumaPunkuBlockMoved: boolean
  }
  
  // Configuración
  settings: {
    audioEnabled: boolean
    musicVolume: number
    sfxVolume: number
  }
}

export const DEFAULT_PLAYER_STATE: PlayerState = {
  playerName: '',
  createdAt: new Date().toISOString(),
  lastPlayed: new Date().toISOString(),
  
  ship: {
    id: 'ufo_1',
    name: '🌫️ Phantom',
    model: '/ufo_1.glb',
    specialty: 'Cloaking / Invisibilidad',
    description: 'Especialidad: infiltración y espionaje',
    ability: 'Habilidad principal: camuflaje óptico',
    missions: 'Tipo de misiones: infiltración, espionaje, recuperar artefactos, entrar a ruinas antiguas'
  },
  
  lastLocation: null,
  
  stats: {
    totalPlayTime: 0,
    sitesVisited: [],
    itemsCollected: [],
    missionsCompleted: []
  },
  
  progress: {
    viracochaRevealed: false,
    gateRevealed: false,
    magnaBowlCollected: false,
    pumaPunkuBlockMoved: false
  },
  
  settings: {
    audioEnabled: true,
    musicVolume: 0.7,
    sfxVolume: 0.8
  }
}

/**
 * Guardar estado del jugador en localStorage
 */
export function savePlayerState(state: PlayerState): void {
  if (typeof window !== 'undefined') {
    state.lastPlayed = new Date().toISOString()
    localStorage.setItem('player_state', JSON.stringify(state))
    console.log('💾 Estado del jugador guardado:', state)
  }
}

/**
 * Cargar estado del jugador desde localStorage
 */
export function loadPlayerState(): PlayerState | null {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('player_state')
    if (saved) {
      try {
        const state = JSON.parse(saved) as PlayerState
        console.log('📂 Estado del jugador cargado:', state)
        return state
      } catch (error) {
        console.error('Error al cargar estado del jugador:', error)
        return null
      }
    }
  }
  return null
}

/**
 * Actualizar progreso del jugador
 */
export function updatePlayerProgress(updates: Partial<PlayerState['progress']>): void {
  const state = loadPlayerState()
  if (state) {
    state.progress = { ...state.progress, ...updates }
    savePlayerState(state)
  }
}

/**
 * Agregar sitio visitado
 */
export function addVisitedSite(siteId: string): void {
  const state = loadPlayerState()
  if (state && !state.stats.sitesVisited.includes(siteId)) {
    state.stats.sitesVisited.push(siteId)
    savePlayerState(state)
  }
}

/**
 * Agregar item recolectado
 */
export function addCollectedItem(itemId: string): void {
  const state = loadPlayerState()
  if (state && !state.stats.itemsCollected.includes(itemId)) {
    state.stats.itemsCollected.push(itemId)
    savePlayerState(state)
  }
}

/**
 * Actualizar última ubicación del jugador
 */
export function updatePlayerLocation(lat: number, lon: number, mode: 'globe' | 'model'): void {
  const state = loadPlayerState()
  if (state) {
    state.lastLocation = { lat, lon, mode }
    savePlayerState(state)
    console.log('📍 Ubicación actualizada:', { lat, lon, mode })
  }
}

/**
 * Resetear estado del jugador
 */
export function resetPlayerState(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('player_state')
    console.log('🗑️ Estado del jugador reseteado')
  }
}

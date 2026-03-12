/**
 * Configuración global del juego
 * Maneja: Audio, Video, Controles, Información
 */

export interface GameSettings {
  // Audio
  audio: {
    masterVolume: number      // 0.0 - 1.0
    musicVolume: number        // 0.0 - 1.0
    sfxVolume: number          // 0.0 - 1.0
    audioEnabled: boolean
  }
  
  // Video/Gráficos
  video: {
    quality: 'low' | 'medium' | 'high'
    shadows: boolean
    postProcessing: boolean
    antialiasing: boolean
  }
  
  // Controles
  controls: {
    mouseSensitivity: number   // 0.1 - 2.0
    invertY: boolean
    keyBindings: {
      forward: string          // 'W'
      backward: string         // 'S'
      left: string            // 'A'
      right: string           // 'D'
      jump: string            // 'Space'
      interact: string        // 'E'
      menu: string            // 'M'
      inventory: string       // 'I'
      map: string             // 'Tab'
    }
  }
  
  // Información del juego
  info: {
    version: string
    lastUpdated: string
  }
}

export const DEFAULT_GAME_SETTINGS: GameSettings = {
  audio: {
    masterVolume: 0.7,
    musicVolume: 0.7,
    sfxVolume: 0.8,
    audioEnabled: true
  },
  
  video: {
    quality: 'high',
    shadows: true,
    postProcessing: true,
    antialiasing: true
  },
  
  controls: {
    mouseSensitivity: 1.0,
    invertY: false,
    keyBindings: {
      forward: 'W',
      backward: 'S',
      left: 'A',
      right: 'D',
      jump: 'Space',
      interact: 'E',
      menu: 'M',
      inventory: 'I',
      map: 'Tab'
    }
  },
  
  info: {
    version: '0.2.0',
    lastUpdated: new Date().toISOString()
  }
}

/**
 * Guardar configuración del juego
 */
export function saveGameSettings(settings: GameSettings): void {
  if (typeof window !== 'undefined') {
    settings.info.lastUpdated = new Date().toISOString()
    localStorage.setItem('game_settings', JSON.stringify(settings))
    console.log('⚙️ Configuración del juego guardada:', settings)
  }
}

/**
 * Cargar configuración del juego
 */
export function loadGameSettings(): GameSettings {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('game_settings')
    if (saved) {
      try {
        const settings = JSON.parse(saved) as GameSettings
        console.log('⚙️ Configuración del juego cargada:', settings)
        return settings
      } catch (error) {
        console.error('Error al cargar configuración:', error)
        return DEFAULT_GAME_SETTINGS
      }
    }
  }
  return DEFAULT_GAME_SETTINGS
}

/**
 * Actualizar solo audio
 */
export function updateAudioSettings(audio: Partial<GameSettings['audio']>): void {
  const settings = loadGameSettings()
  settings.audio = { ...settings.audio, ...audio }
  saveGameSettings(settings)
}

/**
 * Actualizar solo video
 */
export function updateVideoSettings(video: Partial<GameSettings['video']>): void {
  const settings = loadGameSettings()
  settings.video = { ...settings.video, ...video }
  saveGameSettings(settings)
}

/**
 * Actualizar solo controles
 */
export function updateControlSettings(controls: Partial<GameSettings['controls']>): void {
  const settings = loadGameSettings()
  settings.controls = { ...settings.controls, ...controls }
  saveGameSettings(settings)
}

/**
 * Resetear configuración a valores por defecto
 */
export function resetGameSettings(): void {
  saveGameSettings(DEFAULT_GAME_SETTINGS)
  console.log('🔄 Configuración reseteada a valores por defecto')
}

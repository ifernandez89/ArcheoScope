/**
 * ClimateAudioSystem - Sistema de audio climático por capas
 * 
 * Arquitectura:
 * - Escucha eventos del ClimateSystem
 * - Usa audio procedural (cero assets)
 * - Mezcla dinámica según intensidad
 * - Fades suaves entre estados
 * - Simulación realista (rayos con delay por distancia)
 * - 🌊 Modulación por resonancia dimensional
 */

import { getProceduralAudio } from './ProceduralAudio'
import ResonanceSystem, { type ResonanceState } from './ResonanceSystem'
import ResonanceAudioAdapter from './ResonanceAudioAdapter'

type WeatherAudioState = {
  rain: number // 0-1
  wind: number // 0-1
  thunder: boolean
  snow: number // 0-1
  tornado: number // 0-1
}

class ClimateAudioManager {
  private audioGenerator = getProceduralAudio()
  private resonanceSystem?: ResonanceSystem
  private currentState: WeatherAudioState = {
    rain: 0,
    wind: 0,
    thunder: false,
    snow: 0,
    tornado: 0
  }
  private initialized = false
  private lastResonanceUpdate = 0
  private resonanceUpdateInterval = 100 // ms entre actualizaciones
  
  /**
   * Inicializar sistema de audio
   */
  initialize() {
    if (this.initialized) return
    
    console.log('🌦️ ClimateAudioSystem inicializado (audio procedural + resonancia)')
    this.initialized = true
  }
  
  /**
   * 🌊 Habilitar sistema de resonancia
   */
  enableResonance(config?: {
    baseFrequency?: number
    intensity?: number
    harmonics?: number[]
  }) {
    this.resonanceSystem = new ResonanceSystem(config)
    console.log('🌊 Sistema de resonancia habilitado')
  }
  
  /**
   * 🌊 Deshabilitar sistema de resonancia
   */
  disableResonance() {
    this.resonanceSystem = undefined
    console.log('🌊 Sistema de resonancia deshabilitado')
  }
  
  /**
   * 🌊 Verificar si resonancia está habilitada
   */
  isResonanceEnabled(): boolean {
    return this.resonanceSystem !== undefined
  }
  
  /**
   * Actualizar estado del clima
   */
  updateWeather(state: Partial<WeatherAudioState>) {
    if (!this.initialized) {
      this.initialize()
    }
    
    // Actualizar estado
    const prevState = { ...this.currentState }
    this.currentState = { ...this.currentState, ...state }
    
    // Lluvia
    if (this.currentState.rain > 0) {
      if (prevState.rain === 0) {
        this.audioGenerator.startRain(this.currentState.rain)
      } else {
        this.audioGenerator.updateRain(this.currentState.rain)
      }
    } else if (prevState.rain > 0) {
      this.audioGenerator.stopRain()
    }
    
    // Viento
    if (this.currentState.wind > 0) {
      if (prevState.wind === 0) {
        this.audioGenerator.startWind(this.currentState.wind)
      } else {
        this.audioGenerator.updateWind(this.currentState.wind)
      }
    } else if (prevState.wind > 0) {
      this.audioGenerator.stopWind()
    }
    
    // Tornado
    if (this.currentState.tornado > 0) {
      if (prevState.tornado === 0) {
        this.audioGenerator.startTornado(this.currentState.tornado)
      }
    } else if (prevState.tornado > 0) {
      this.audioGenerator.stopTornado()
    }
    
    console.log('🎵 Audio actualizado:', this.currentState)
  }
  
  /**
   * 🌊 Actualizar con resonancia (llamar cada frame)
   */
  updateWithResonance(deltaTime: number) {
    if (!this.resonanceSystem) return
    
    // Throttle: solo actualizar cada X ms
    const now = Date.now()
    if (now - this.lastResonanceUpdate < this.resonanceUpdateInterval) {
      return
    }
    this.lastResonanceUpdate = now
    
    // Obtener estado de resonancia
    const resonanceState = this.resonanceSystem.update(deltaTime)
    
    // Convertir a modulación de audio
    const modulation = ResonanceAudioAdapter.toAudioModulation(resonanceState)
    
    // Aplicar al audio
    this.audioGenerator.applyResonanceModulation({
      filterFrequency: modulation.filterFrequency,
      noiseReduction: modulation.noiseReduction,
      lfoRate: modulation.lfoRate
    })
    
    // Log del perfil (solo cuando cambia)
    const profile = ResonanceAudioAdapter.getAudioProfile(resonanceState)
    if (Math.random() < 0.01) { // Log ocasional para no saturar consola
      console.log(`🌊 Resonancia: ${resonanceState.value.toFixed(2)}, Perfil: ${profile.profile}`)
    }
  }
  
  /**
   * 🌊 Obtener estado actual de resonancia
   */
  getResonanceState(): ResonanceState | null {
    if (!this.resonanceSystem) return null
    return this.resonanceSystem.update(0)
  }
  
  /**
   * Reproducir trueno con delay realista basado en distancia
   * @param distance Distancia en metros
   */
  playThunder(distance: number = 1000) {
    this.audioGenerator.playThunder(distance)
  }
  
  /**
   * Ajustar volumen master
   */
  setMasterVolume(volume: number) {
    this.audioGenerator.setMasterVolume(volume)
  }
}

// Instancia global
let climateAudio: ClimateAudioManager | null = null

export function getClimateAudio(): ClimateAudioManager {
  if (!climateAudio) {
    climateAudio = new ClimateAudioManager()
  }
  return climateAudio
}

export default ClimateAudioManager

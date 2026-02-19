/**
 * ClimateAudioSystem - Sistema de audio climático por capas
 * 
 * Arquitectura:
 * - Escucha eventos del ClimateSystem
 * - Usa audio procedural (cero assets)
 * - Mezcla dinámica según intensidad
 * - Fades suaves entre estados
 * - Simulación realista (rayos con delay por distancia)
 */

import { getProceduralAudio } from './ProceduralAudio'

type WeatherAudioState = {
  rain: number // 0-1
  wind: number // 0-1
  thunder: boolean
  snow: number // 0-1
  tornado: number // 0-1
}

class ClimateAudioManager {
  private audioGenerator = getProceduralAudio()
  private currentState: WeatherAudioState = {
    rain: 0,
    wind: 0,
    thunder: false,
    snow: 0,
    tornado: 0
  }
  private initialized = false
  
  /**
   * Inicializar sistema de audio
   */
  initialize() {
    if (this.initialized) return
    
    console.log('🌦️ ClimateAudioSystem inicializado (audio procedural)')
    this.initialized = true
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

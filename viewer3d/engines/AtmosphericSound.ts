/**
 * AtmosphericSound - Sistema de sonido procedural que respira con el mundo
 * No es música. Es un campo sonoro continuo que evoluciona con el sol, viento y noche.
 */

export interface SoundState {
  baseFrequency: number
  filterFrequency: number
  volume: number
  windIntensity: number
  droneIntensity: number
}

export class AtmosphericSound {
  private audioContext: AudioContext | null = null
  private masterGain: GainNode | null = null
  
  // Dron armónico base
  private droneOscillator: OscillatorNode | null = null
  private droneGain: GainNode | null = null
  private droneFilter: BiquadFilterNode | null = null
  
  // Viento (ruido blanco filtrado)
  private windBuffer: AudioBufferSourceNode | null = null
  private windGain: GainNode | null = null
  private windFilter: BiquadFilterNode | null = null
  
  // Estado
  private isPlaying: boolean = false
  private time: number = 0
  private enabled: boolean = false
  
  constructor() {
    // No inicializar automáticamente - esperar interacción del usuario
  }
  
  /**
   * Inicializar sistema de audio (requiere interacción del usuario)
   */
  async initialize() {
    if (this.audioContext) return // Ya inicializado
    
    try {
      this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
      
      // Master gain (volumen general muy bajo)
      this.masterGain = this.audioContext.createGain()
      this.masterGain.gain.value = 0.15 // Muy sutil
      this.masterGain.connect(this.audioContext.destination)
      
      // Crear dron armónico
      this.createDrone()
      
      // Crear viento procedural
      await this.createWind()
      
      console.log('🔊 Sistema de sonido atmosférico inicializado')
    } catch (error) {
      console.warn('⚠️ No se pudo inicializar audio:', error)
    }
  }
  
  /**
   * Crear dron armónico base (frecuencia que sigue al sol)
   */
  private createDrone() {
    if (!this.audioContext || !this.masterGain) return
    
    // Oscilador con onda sinusoidal pura
    this.droneOscillator = this.audioContext.createOscillator()
    this.droneOscillator.type = 'sine'
    this.droneOscillator.frequency.value = 120 // Frecuencia base (será modulada)
    
    // Filtro lowpass para suavizar
    this.droneFilter = this.audioContext.createBiquadFilter()
    this.droneFilter.type = 'lowpass'
    this.droneFilter.frequency.value = 400
    this.droneFilter.Q.value = 0.5
    
    // Gain del dron (casi imperceptible)
    this.droneGain = this.audioContext.createGain()
    this.droneGain.gain.value = 0.03 // Extremadamente bajo
    
    // Conectar: oscilador -> filtro -> gain -> master
    this.droneOscillator.connect(this.droneFilter)
    this.droneFilter.connect(this.droneGain)
    this.droneGain.connect(this.masterGain)
    
    this.droneOscillator.start()
  }
  
  /**
   * Crear viento procedural (ruido blanco filtrado)
   */
  private async createWind() {
    if (!this.audioContext || !this.masterGain) return
    
    // Crear buffer de ruido blanco (5 minutos para evitar loops cortos)
    const bufferSize = this.audioContext.sampleRate * 300 // 5 minutos
    const buffer = this.audioContext.createBuffer(2, bufferSize, this.audioContext.sampleRate)
    
    // Llenar con ruido blanco
    for (let channel = 0; channel < 2; channel++) {
      const data = buffer.getChannelData(channel)
      for (let i = 0; i < bufferSize; i++) {
        data[i] = Math.random() * 2 - 1
      }
    }
    
    // Source
    this.windBuffer = this.audioContext.createBufferSource()
    this.windBuffer.buffer = buffer
    this.windBuffer.loop = true
    
    // Filtro para dar carácter de viento
    this.windFilter = this.audioContext.createBiquadFilter()
    this.windFilter.type = 'bandpass'
    this.windFilter.frequency.value = 800
    this.windFilter.Q.value = 0.3
    
    // Gain del viento
    this.windGain = this.audioContext.createGain()
    this.windGain.gain.value = 0.02 // Muy bajo
    
    // Conectar: buffer -> filtro -> gain -> master
    this.windBuffer.connect(this.windFilter)
    this.windFilter.connect(this.windGain)
    this.windGain.connect(this.masterGain)
    
    this.windBuffer.start()
  }
  
  /**
   * Activar/desactivar sonido
   */
  setEnabled(enabled: boolean) {
    this.enabled = enabled
    if (this.masterGain) {
      const targetVolume = enabled ? 0.15 : 0
      this.masterGain.gain.linearRampToValueAtTime(
        targetVolume,
        this.audioContext!.currentTime + 2 // Fade de 2 segundos
      )
    }
  }
  
  /**
   * Actualizar estado sonoro basado en condiciones astronómicas
   */
  update(deltaTime: number, solarAltitude: number, windIntensity: number = 0.5) {
    if (!this.audioContext || !this.enabled) return
    
    this.time += deltaTime
    
    // Mapear altura solar a frecuencia base (80Hz noche -> 240Hz día)
    const normalizedAltitude = (solarAltitude + Math.PI / 2) / Math.PI // 0 a 1
    const baseFrequency = 80 + normalizedAltitude * 160
    
    // Actualizar dron armónico
    if (this.droneOscillator && this.droneGain && this.droneFilter) {
      // Frecuencia con micro-variación lenta
      const microVariation = Math.sin(this.time * 0.05) * 5
      this.droneOscillator.frequency.linearRampToValueAtTime(
        baseFrequency + microVariation,
        this.audioContext.currentTime + 0.5
      )
      
      // Intensidad del dron según hora (más presente al amanecer/atardecer)
      const dayProgress = Math.abs(normalizedAltitude - 0.5) * 2 // 0 en mediodía, 1 en extremos
      const droneIntensity = 0.02 + dayProgress * 0.03
      this.droneGain.gain.linearRampToValueAtTime(
        droneIntensity,
        this.audioContext.currentTime + 1
      )
      
      // Filtro según altura solar (más abierto de día)
      const filterFreq = 200 + normalizedAltitude * 1800
      this.droneFilter.frequency.linearRampToValueAtTime(
        filterFreq,
        this.audioContext.currentTime + 2
      )
    }
    
    // Actualizar viento
    if (this.windGain && this.windFilter) {
      // Volumen del viento con variación lenta
      const windVariation = Math.sin(this.time * 0.03) * 0.01
      const windVolume = 0.015 + windIntensity * 0.02 + windVariation
      this.windGain.gain.linearRampToValueAtTime(
        windVolume,
        this.audioContext.currentTime + 3
      )
      
      // Frecuencia del viento (más grave de noche)
      const windFreq = 600 + normalizedAltitude * 600
      this.windFilter.frequency.linearRampToValueAtTime(
        windFreq,
        this.audioContext.currentTime + 2
      )
    }
    
    // Respiración del volumen master (período de 90 segundos)
    if (this.masterGain) {
      const breathe = Math.sin(this.time * 0.07) * 0.02
      const targetVolume = this.enabled ? 0.15 + breathe : 0
      this.masterGain.gain.linearRampToValueAtTime(
        targetVolume,
        this.audioContext.currentTime + 0.1
      )
    }
  }
  
  /**
   * Obtener estado actual
   */
  getState(): SoundState {
    return {
      baseFrequency: this.droneOscillator?.frequency.value || 0,
      filterFrequency: this.droneFilter?.frequency.value || 0,
      volume: this.masterGain?.gain.value || 0,
      windIntensity: this.windGain?.gain.value || 0,
      droneIntensity: this.droneGain?.gain.value || 0
    }
  }
  
  /**
   * Limpiar recursos
   */
  dispose() {
    if (this.droneOscillator) this.droneOscillator.stop()
    if (this.windBuffer) this.windBuffer.stop()
    if (this.audioContext) this.audioContext.close()
    
    this.audioContext = null
    this.isPlaying = false
  }
}

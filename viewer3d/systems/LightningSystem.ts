/**
 * LightningSystem - Sistema de rayos procedural
 * 
 * Componentes:
 * 1. Flash visual (exposure + ambient light)
 * 2. Sonido procedural (crack + rumble + reverb)
 * 3. Simulación de distancia realista
 * 4. Variabilidad para evitar repetición
 */

type LightningConfig = {
  minDistance: number
  maxDistance: number
  minInterval: number
  maxInterval: number
  intensity: number // 0-1
}

type LightningStrike = {
  distance: number
  intensity: number
  direction: { x: number; y: number; z: number }
  timestamp: number
}

class LightningManager {
  private context: AudioContext | null = null
  private masterGain: GainNode | null = null
  private config: LightningConfig = {
    minDistance: 200,
    maxDistance: 3000,
    minInterval: 3000,
    maxInterval: 10000,
    intensity: 1.0
  }
  private active = false
  private intervalId: number | null = null
  private onFlashCallback: ((strike: LightningStrike) => void) | null = null
  
  constructor() {
    if (typeof window === 'undefined') return
    
    this.context = new (window.AudioContext || (window as any).webkitAudioContext)()
    this.masterGain = this.context.createGain()
    this.masterGain.gain.value = 0.7
    this.masterGain.connect(this.context.destination)
    
    console.log('⚡ LightningSystem inicializado')
  }
  
  /**
   * Iniciar sistema de rayos
   */
  start(config?: Partial<LightningConfig>) {
    if (this.active) return
    
    this.config = { ...this.config, ...config }
    this.active = true
    
    this.scheduleNextStrike()
    
    console.log('⚡ Rayos activados:', this.config)
  }
  
  /**
   * Detener sistema de rayos
   */
  stop() {
    this.active = false
    if (this.intervalId) {
      clearTimeout(this.intervalId)
      this.intervalId = null
    }
    console.log('⚡ Rayos desactivados')
  }
  
  /**
   * Programar siguiente rayo
   */
  private scheduleNextStrike() {
    if (!this.active) return
    
    const interval = this.config.minInterval + 
      Math.random() * (this.config.maxInterval - this.config.minInterval)
    
    this.intervalId = window.setTimeout(() => {
      this.triggerLightning()
      this.scheduleNextStrike()
    }, interval)
  }
  
  /**
   * Disparar un rayo (o múltiples)
   */
  triggerLightning() {
    // Número de rayos simultáneos (1-3)
    const numStrikes = 1 + Math.floor(Math.random() * 3) // 1, 2 o 3 rayos
    
    for (let i = 0; i < numStrikes; i++) {
      // Pequeño delay entre rayos (0-200ms)
      const strikeDelay = i * (Math.random() * 0.2)
      
      setTimeout(() => {
        this.triggerSingleLightning()
      }, strikeDelay * 1000)
    }
  }
  
  /**
   * Disparar un solo rayo
   */
  private triggerSingleLightning() {
    // Distancia aleatoria
    const distance = this.config.minDistance + 
      Math.random() * (this.config.maxDistance - this.config.minDistance)
    
    // Intensidad variable
    const intensity = 0.6 + Math.random() * 0.4 // 0.6-1.0
    
    // Dirección aleatoria
    const angle = Math.random() * Math.PI * 2
    const direction = {
      x: Math.cos(angle),
      y: 0.5 + Math.random() * 0.5, // Arriba
      z: Math.sin(angle)
    }
    
    const strike: LightningStrike = {
      distance,
      intensity: intensity * this.config.intensity,
      direction,
      timestamp: Date.now()
    }
    
    // Flash visual (callback para Three.js)
    if (this.onFlashCallback) {
      this.onFlashCallback(strike)
    }
    
    // Sonido con delay
    this.playThunderSound(strike)
    
    console.log(`⚡ Rayo: ${distance.toFixed(0)}m, intensidad: ${intensity.toFixed(2)}`)
  }
  
  /**
   * Reproducir sonido de trueno procedural
   */
  private playThunderSound(strike: LightningStrike) {
    if (!this.context || !this.masterGain) return
    
    // Delay basado en distancia (velocidad del sonido: 343 m/s)
    const delay = strike.distance / 343
    const startTime = this.context.currentTime + delay
    
    // Volumen basado en distancia
    const volume = Math.max(0.1, 1 - (strike.distance / 5000)) * strike.intensity
    
    // PARTE A: Crack agudo inicial (impacto eléctrico)
    this.playCrack(startTime, volume)
    
    // PARTE B: Retumbo grave (trueno)
    this.playRumble(startTime + 0.05, volume, strike.distance)
    
    // PARTE C: Cola reverberante (eco)
    this.playReverb(startTime + 0.3, volume * 0.4, strike.distance)
  }
  
  /**
   * Parte A: Crack agudo inicial
   */
  private playCrack(startTime: number, volume: number) {
    if (!this.context || !this.masterGain) return
    
    // White noise
    const bufferSize = this.context.sampleRate * 0.12 // 120ms
    const buffer = this.context.createBuffer(1, bufferSize, this.context.sampleRate)
    const data = buffer.getChannelData(0)
    
    for (let i = 0; i < bufferSize; i++) {
      data[i] = (Math.random() * 2 - 1) * (1 - i / bufferSize) // Decay
    }
    
    const source = this.context.createBufferSource()
    source.buffer = buffer
    
    // High-pass filter (solo agudos)
    const filter = this.context.createBiquadFilter()
    filter.type = 'highpass'
    filter.frequency.value = 800 + Math.random() * 400 // 800-1200Hz
    filter.Q.value = 2
    
    // Envelope rápido
    const gain = this.context.createGain()
    gain.gain.setValueAtTime(0, startTime)
    gain.gain.linearRampToValueAtTime(volume * 0.8, startTime + 0.01)
    gain.gain.exponentialRampToValueAtTime(0.01, startTime + 0.12)
    
    source.connect(filter)
    filter.connect(gain)
    gain.connect(this.masterGain)
    
    source.start(startTime)
    source.stop(startTime + 0.12)
  }
  
  /**
   * Parte B: Retumbo grave
   */
  private playRumble(startTime: number, volume: number, distance: number) {
    if (!this.context || !this.masterGain) return
    
    // Pink noise (más natural)
    const duration = 1.5 + Math.random() * 1.5 // 1.5-3s
    const bufferSize = this.context.sampleRate * duration
    const buffer = this.context.createBuffer(1, bufferSize, this.context.sampleRate)
    const data = buffer.getChannelData(0)
    
    // Pink noise con decay
    let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1
      b0 = 0.99886 * b0 + white * 0.0555179
      b1 = 0.99332 * b1 + white * 0.0750759
      b2 = 0.96900 * b2 + white * 0.1538520
      b3 = 0.86650 * b3 + white * 0.3104856
      b4 = 0.55000 * b4 + white * 0.5329522
      b5 = -0.7616 * b5 - white * 0.0168980
      data[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.11
      data[i] *= (1 - i / bufferSize * 0.7) // Decay gradual
      b6 = white * 0.115926
    }
    
    const source = this.context.createBufferSource()
    source.buffer = buffer
    
    // Low-pass filter (solo graves)
    const filter = this.context.createBiquadFilter()
    filter.type = 'lowpass'
    filter.frequency.value = 150 + Math.random() * 250 // 150-400Hz variable
    filter.Q.value = 2 + Math.random() * 2 // 2-4
    
    // LFO para oscilación (retumbo)
    const lfo = this.context.createOscillator()
    lfo.frequency.value = 2 + Math.random() * 3 // 2-5Hz
    lfo.type = 'sine'
    
    const lfoGain = this.context.createGain()
    lfoGain.gain.value = 30 // Modulación de frecuencia
    
    lfo.connect(lfoGain)
    lfoGain.connect(filter.frequency)
    
    // Envelope largo
    const gain = this.context.createGain()
    gain.gain.setValueAtTime(0, startTime)
    gain.gain.linearRampToValueAtTime(volume * 0.6, startTime + 0.2)
    gain.gain.exponentialRampToValueAtTime(0.01, startTime + duration)
    
    source.connect(filter)
    filter.connect(gain)
    gain.connect(this.masterGain)
    
    source.start(startTime)
    lfo.start(startTime)
    
    source.stop(startTime + duration)
    lfo.stop(startTime + duration)
  }
  
  /**
   * Parte C: Cola reverberante (eco simulado)
   */
  private playReverb(startTime: number, volume: number, distance: number) {
    if (!this.context || !this.masterGain) return
    
    // Noise suave
    const duration = 2
    const bufferSize = this.context.sampleRate * duration
    const buffer = this.context.createBuffer(1, bufferSize, this.context.sampleRate)
    const data = buffer.getChannelData(0)
    
    for (let i = 0; i < bufferSize; i++) {
      data[i] = (Math.random() * 2 - 1) * (1 - i / bufferSize)
    }
    
    const source = this.context.createBufferSource()
    source.buffer = buffer
    
    // Filtro oscuro
    const filter = this.context.createBiquadFilter()
    filter.type = 'lowpass'
    filter.frequency.value = 100 + Math.random() * 100 // 100-200Hz
    filter.Q.value = 1
    
    // Delay simple (eco)
    const delay = this.context.createDelay(1)
    delay.delayTime.value = 0.15 + Math.random() * 0.1 // 150-250ms
    
    const delayGain = this.context.createGain()
    delayGain.gain.value = 0.3 // Feedback bajo
    
    // Envelope muy suave
    const gain = this.context.createGain()
    gain.gain.setValueAtTime(0, startTime)
    gain.gain.linearRampToValueAtTime(volume, startTime + 0.3)
    gain.gain.exponentialRampToValueAtTime(0.01, startTime + duration)
    
    source.connect(filter)
    filter.connect(delay)
    delay.connect(delayGain)
    delayGain.connect(delay) // Feedback
    delay.connect(gain)
    gain.connect(this.masterGain)
    
    source.start(startTime)
    source.stop(startTime + duration)
  }
  
  /**
   * Registrar callback para flash visual
   */
  onFlash(callback: (strike: LightningStrike) => void) {
    this.onFlashCallback = callback
  }
  
  /**
   * Actualizar configuración
   */
  updateConfig(config: Partial<LightningConfig>) {
    this.config = { ...this.config, ...config }
  }
  
  /**
   * Ajustar volumen
   */
  setVolume(volume: number) {
    if (this.masterGain && this.context) {
      this.masterGain.gain.linearRampToValueAtTime(
        volume,
        this.context.currentTime + 0.1
      )
    }
  }
  
  /**
   * Limpiar recursos
   */
  dispose() {
    this.stop()
    if (this.context) {
      this.context.close()
    }
    console.log('⚡ LightningSystem disposed')
  }
}

// Instancia global
let lightningManager: LightningManager | null = null

export function getLightningManager(): LightningManager {
  if (!lightningManager) {
    lightningManager = new LightningManager()
  }
  return lightningManager
}

export type { LightningConfig, LightningStrike }
export default LightningManager

/**
 * ProceduralAudio - Generación de audio procedural con Web Audio API
 * 
 * Ventajas:
 * - Cero peso en bundle
 * - Cero assets externos
 * - Variación infinita
 * - Control total en tiempo real
 * - Coherencia sistémica
 */

type NoiseType = 'white' | 'pink' | 'brown'

class ProceduralAudioGenerator {
  private context?: AudioContext
  private masterGain?: GainNode
  private enabled: boolean = false
  private baseVolume: number = 0.7 // Default, se sobrescribe al cargar playerState
  
  // Generadores activos - Type safe
  private rainSource?: AudioBufferSourceNode
  private rainGain?: GainNode
  private rainFilter?: BiquadFilterNode
  
  private windSource?: AudioBufferSourceNode
  private windGain?: GainNode
  private windFilter?: BiquadFilterNode
  private windLFO?: OscillatorNode
  private windLFOGain?: GainNode
  
  private tornadoSource?: AudioBufferSourceNode
  private tornadoGain?: GainNode
  private tornadoFilter?: BiquadFilterNode
  private tornadoLFO?: OscillatorNode
  private tornadoLFOGain?: GainNode
  
  constructor() {
    // Cargar volumen guardado INMEDIATAMENTE
    this.loadSavedVolume()
    console.log('🎵 ProceduralAudio creado con volumen:', this.baseVolume)
  }
  
  /**
   * Cargar volumen guardado desde localStorage
   */
  private loadSavedVolume(): void {
    if (typeof window === 'undefined') return
    
    try {
      // Intentar cargar desde gameSettings primero
      const gameSettingsStr = localStorage.getItem('game_settings')
      if (gameSettingsStr) {
        const gameSettings = JSON.parse(gameSettingsStr)
        if (gameSettings?.audio?.masterVolume !== undefined) {
          this.baseVolume = gameSettings.audio.masterVolume
          console.log('🔊 Volumen cargado desde gameSettings:', this.baseVolume)
          return
        }
      }
      
      // Fallback: intentar cargar desde playerState (legacy)
      const playerStateStr = localStorage.getItem('player_state')
      if (playerStateStr) {
        const playerState = JSON.parse(playerStateStr)
        if (playerState?.settings?.masterVolume !== undefined) {
          this.baseVolume = playerState.settings.masterVolume
          console.log('🔊 Volumen cargado desde playerState (legacy):', this.baseVolume)
        }
      }
    } catch (error) {
      console.error('Error cargando volumen:', error)
    }
  }
  
  /**
   * Habilitar audio (requiere interacción del usuario)
   */
  async enable(): Promise<void> {
    if (this.enabled) {
      console.log('🎵 Audio ya habilitado')
      return
    }
    
    if (typeof window === 'undefined') return
    
    // Recargar volumen por si cambió antes de enable
    this.loadSavedVolume()
    
    // Crear AudioContext
    this.context = new (window.AudioContext || (window as any).webkitAudioContext)()
    
    // Resume si está suspendido
    if (this.context.state === 'suspended') {
      await this.context.resume()
    }
    
    // Crear master gain con el volumen guardado
    this.masterGain = this.context.createGain()
    this.masterGain.gain.value = this.baseVolume
    this.masterGain.connect(this.context.destination)
    
    this.enabled = true
    console.log('🎵 ProceduralAudio habilitado con volumen:', this.baseVolume)
  }
  
  /**
   * Verificar si está habilitado
   */
  isEnabled(): boolean {
    return this.enabled
  }
  
  /**
   * Generar buffer de ruido
   */
  private createNoiseBuffer(type: NoiseType = 'white', duration: number = 2): AudioBuffer {
    if (!this.context) throw new Error('AudioContext no inicializado')
    
    const sampleRate = this.context.sampleRate
    const bufferSize = sampleRate * duration
    const buffer = this.context.createBuffer(1, bufferSize, sampleRate)
    const data = buffer.getChannelData(0)
    
    if (type === 'white') {
      // White noise - todas las frecuencias iguales
      for (let i = 0; i < bufferSize; i++) {
        data[i] = Math.random() * 2 - 1
      }
    } else if (type === 'pink') {
      // Pink noise - más graves (1/f)
      let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0
      for (let i = 0; i < bufferSize; i++) {
        const white = Math.random() * 2 - 1
        b0 = 0.99886 * b0 + white * 0.0555179
        b1 = 0.99332 * b1 + white * 0.0750759
        b2 = 0.96900 * b2 + white * 0.1538520
        b3 = 0.86650 * b3 + white * 0.3104856
        b4 = 0.55000 * b4 + white * 0.5329522
        b5 = -0.7616 * b5 - white * 0.0168980
        data[i] = b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362
        data[i] *= 0.11 // Normalizar
        b6 = white * 0.115926
      }
    } else if (type === 'brown') {
      // Brown noise - aún más graves
      let lastOut = 0
      for (let i = 0; i < bufferSize; i++) {
        const white = Math.random() * 2 - 1
        data[i] = (lastOut + (0.02 * white)) / 1.02
        lastOut = data[i]
        data[i] *= 3.5 // Normalizar
      }
    }
    
    return buffer
  }
  
  /**
   * 🌧️ Lluvia procedural
   * White noise + high-pass filter
   */
  startRain(intensity: number = 0.5) {
    if (!this.context || !this.masterGain || !this.enabled) return
    
    this.stopRain() // Detener si ya existe
    
    // Crear buffer de ruido blanco
    const noiseBuffer = this.createNoiseBuffer('white', 2)
    
    // Source
    const source = this.context.createBufferSource()
    source.buffer = noiseBuffer
    source.loop = true
    
    // High-pass filter (solo frecuencias altas = gotas)
    const filter = this.context.createBiquadFilter()
    filter.type = 'highpass'
    filter.frequency.value = 1000 + (intensity * 2000) // Más agudo con más intensidad
    filter.Q.value = 0.5
    
    // Gain
    const gain = this.context.createGain()
    gain.gain.value = intensity * 0.3
    
    // Conectar
    source.connect(filter)
    filter.connect(gain)
    gain.connect(this.masterGain)
    
    source.start(0)
    
    // 🔥 FIX: Cleanup automático cuando termina
    source.onended = () => {
      source.disconnect()
      filter.disconnect()
      gain.disconnect()
    }
    
    // Guardar referencias - Type safe
    this.rainSource = source
    this.rainGain = gain
    this.rainFilter = filter
    
    console.log('🌧️ Lluvia procedural iniciada:', intensity)
  }
  
  stopRain() {
    if (this.rainSource) {
      try {
        this.rainSource.stop()
        this.rainSource.disconnect()
      } catch (e) {
        // Ya detenido
      }
      this.rainSource = undefined
    }
    if (this.rainFilter) {
      this.rainFilter.disconnect()
      this.rainFilter = undefined
    }
    if (this.rainGain) {
      this.rainGain.disconnect()
      this.rainGain = undefined
    }
  }
  
  updateRain(intensity: number) {
    if (this.rainGain && this.rainFilter && this.context) {
      // Fade suave
      this.rainGain.gain.linearRampToValueAtTime(
        intensity * 0.3,
        this.context.currentTime + 0.5
      )
      
      // Ajustar filtro
      this.rainFilter.frequency.linearRampToValueAtTime(
        1000 + (intensity * 2000),
        this.context.currentTime + 0.5
      )
    }
  }
  
  /**
   * 🌬️ Viento procedural
   * Pink noise + LFO (oscilación lenta)
   */
  startWind(intensity: number = 0.5) {
    if (!this.context || !this.masterGain || !this.enabled) return
    
    this.stopWind()
    
    // Crear buffer de ruido rosa (más natural para viento)
    const noiseBuffer = this.createNoiseBuffer('pink', 2)
    
    // Source
    const source = this.context.createBufferSource()
    source.buffer = noiseBuffer
    source.loop = true
    
    // Low-pass filter (solo graves)
    const filter = this.context.createBiquadFilter()
    filter.type = 'lowpass'
    filter.frequency.value = 500 - (intensity * 200) // Más grave con más intensidad
    filter.Q.value = 1
    
    // Gain principal
    const gain = this.context.createGain()
    gain.gain.value = intensity * 0.4
    
    // LFO para oscilación (ráfagas)
    const lfo = this.context.createOscillator()
    lfo.frequency.value = 0.3 // Oscilación lenta
    lfo.type = 'sine'
    
    const lfoGain = this.context.createGain()
    lfoGain.gain.value = intensity * 0.15 // Profundidad de modulación
    
    // Conectar LFO a gain
    lfo.connect(lfoGain)
    lfoGain.connect(gain.gain)
    
    // Conectar audio
    source.connect(filter)
    filter.connect(gain)
    gain.connect(this.masterGain)
    
    source.start(0)
    lfo.start(0)
    
    // 🔥 FIX: Cleanup automático
    source.onended = () => {
      source.disconnect()
      filter.disconnect()
      gain.disconnect()
      lfo.disconnect()
      lfoGain.disconnect()
    }
    
    // Guardar referencias - Type safe
    this.windSource = source
    this.windGain = gain
    this.windLFO = lfo
    this.windFilter = filter
    this.windLFOGain = lfoGain
    
    console.log('🌬️ Viento procedural iniciado:', intensity)
  }
  
  stopWind() {
    if (this.windSource) {
      try {
        this.windSource.stop()
        this.windSource.disconnect()
      } catch (e) {
        // Ya detenido
      }
      this.windSource = undefined
    }
    if (this.windLFO) {
      try {
        this.windLFO.stop()
        this.windLFO.disconnect()
      } catch (e) {
        // Ya detenido
      }
      this.windLFO = undefined
    }
    if (this.windFilter) {
      this.windFilter.disconnect()
      this.windFilter = undefined
    }
    if (this.windGain) {
      this.windGain.disconnect()
      this.windGain = undefined
    }
    if (this.windLFOGain) {
      this.windLFOGain.disconnect()
      this.windLFOGain = undefined
    }
  }
  
  updateWind(intensity: number) {
    if (this.windGain && this.windFilter && this.context) {
      this.windGain.gain.linearRampToValueAtTime(
        intensity * 0.4,
        this.context.currentTime + 0.5
      )
      
      this.windFilter.frequency.linearRampToValueAtTime(
        500 - (intensity * 200),
        this.context.currentTime + 0.5
      )
    }
  }
  
  /**
   * ⚡ Trueno procedural
   * Burst de ruido + low-pass + reverb
   */
  playThunder(distance: number = 1000) {
    if (!this.context || !this.masterGain) return
    
    // Delay basado en distancia (velocidad del sonido: 343 m/s)
    const delay = distance / 343
    const startTime = this.context.currentTime + delay
    
    // Volumen basado en distancia
    const volume = Math.max(0.1, 1 - (distance / 5000))
    
    // Crear burst de ruido
    const noiseBuffer = this.createNoiseBuffer('brown', 0.5)
    
    const source = this.context.createBufferSource()
    source.buffer = noiseBuffer
    
    // Low-pass filter (trueno es grave)
    const filter = this.context.createBiquadFilter()
    filter.type = 'lowpass'
    filter.frequency.value = 200
    filter.Q.value = 2
    
    // Envelope (fade in/out rápido)
    const gain = this.context.createGain()
    gain.gain.setValueAtTime(0, startTime)
    gain.gain.linearRampToValueAtTime(volume * 0.6, startTime + 0.05)
    gain.gain.exponentialRampToValueAtTime(0.01, startTime + 0.5)
    
    // Conectar
    source.connect(filter)
    filter.connect(gain)
    gain.connect(this.masterGain)
    
    source.start(startTime)
    source.stop(startTime + 0.5)
    
    console.log(`⚡ Trueno procedural: ${distance}m, delay: ${delay.toFixed(2)}s`)
  }
  
  /**
   * 🌪️ Tornado procedural
   * Brown noise + modulación circular
   */
  startTornado(intensity: number = 0.8) {
    if (!this.context || !this.masterGain || !this.enabled) return
    
    this.stopTornado()
    
    // Similar al viento pero más grave y más intenso
    const noiseBuffer = this.createNoiseBuffer('brown', 2)
    
    const source = this.context.createBufferSource()
    source.buffer = noiseBuffer
    source.loop = true
    
    // Very low-pass (rumble)
    const filter = this.context.createBiquadFilter()
    filter.type = 'lowpass'
    filter.frequency.value = 150
    filter.Q.value = 3
    
    const gain = this.context.createGain()
    gain.gain.value = intensity * 0.5
    
    // LFO más rápido (rotación)
    const lfo = this.context.createOscillator()
    lfo.frequency.value = 1.5 // Más rápido que viento
    lfo.type = 'sine'
    
    const lfoGain = this.context.createGain()
    lfoGain.gain.value = intensity * 0.2
    
    lfo.connect(lfoGain)
    lfoGain.connect(gain.gain)
    
    source.connect(filter)
    filter.connect(gain)
    gain.connect(this.masterGain)
    
    source.start(0)
    lfo.start(0)
    
    // 🔥 FIX: Cleanup automático
    source.onended = () => {
      source.disconnect()
      filter.disconnect()
      gain.disconnect()
      lfo.disconnect()
      lfoGain.disconnect()
    }
    
    // Guardar referencias - Type safe
    this.tornadoSource = source
    this.tornadoGain = gain
    this.tornadoFilter = filter
    this.tornadoLFO = lfo
    this.tornadoLFOGain = lfoGain
    
    console.log('🌪️ Tornado procedural iniciado:', intensity)
  }
  
  stopTornado() {
    if (this.tornadoSource) {
      try {
        this.tornadoSource.stop()
        this.tornadoSource.disconnect()
      } catch (e) {
        // Ya detenido
      }
      this.tornadoSource = undefined
    }
    if (this.tornadoLFO) {
      try {
        this.tornadoLFO.stop()
        this.tornadoLFO.disconnect()
      } catch (e) {
        // Ya detenido
      }
      this.tornadoLFO = undefined
    }
    if (this.tornadoFilter) {
      this.tornadoFilter.disconnect()
      this.tornadoFilter = undefined
    }
    if (this.tornadoGain) {
      this.tornadoGain.disconnect()
      this.tornadoGain = undefined
    }
    if (this.tornadoLFOGain) {
      this.tornadoLFOGain.disconnect()
      this.tornadoLFOGain = undefined
    }
  }
  
  /**
   * Ajustar volumen master
   */
  setMasterVolume(volume: number) {
    this.baseVolume = Math.max(0, Math.min(1, volume))
    
    if (this.masterGain && this.context) {
      this.masterGain.gain.linearRampToValueAtTime(
        this.baseVolume,
        this.context.currentTime + 0.1
      )
    }
  }
  
  /**
   * Obtener volumen master actual
   */
  getMasterVolume(): number {
    return this.baseVolume
  }
  
  /**
   * 🌊 Aplicar modulación de resonancia
   * Modula el audio existente sin agregar nuevos sonidos
   */
  applyResonanceModulation(modulation: {
    filterFrequency: number
    noiseReduction: number
    lfoRate?: number
  }) {
    if (!this.context || !this.enabled) return
    
    const currentTime = this.context.currentTime
    const rampTime = 0.5 // Transición suave de 500ms
    
    // Modular filtros activos
    if (this.windFilter) {
      this.windFilter.frequency.linearRampToValueAtTime(
        modulation.filterFrequency * 0.5, // Viento más grave
        currentTime + rampTime
      )
    }
    
    if (this.rainFilter) {
      this.rainFilter.frequency.linearRampToValueAtTime(
        modulation.filterFrequency * 2, // Lluvia más aguda
        currentTime + rampTime
      )
    }
    
    if (this.tornadoFilter) {
      this.tornadoFilter.frequency.linearRampToValueAtTime(
        modulation.filterFrequency * 0.3, // Tornado muy grave
        currentTime + rampTime
      )
    }
    
    // Modular gain master según reducción de ruido
    if (this.masterGain) {
      const targetGain = this.baseVolume * (1 - modulation.noiseReduction * 0.3)
      this.masterGain.gain.linearRampToValueAtTime(
        targetGain,
        currentTime + rampTime
      )
    }
    
    // Modular LFO si está disponible
    if (modulation.lfoRate) {
      if (this.windLFO) {
        this.windLFO.frequency.linearRampToValueAtTime(
          modulation.lfoRate * 0.3, // LFO más lento para viento
          currentTime + rampTime
        )
      }
      
      if (this.tornadoLFO) {
        this.tornadoLFO.frequency.linearRampToValueAtTime(
          modulation.lfoRate * 1.5, // LFO más rápido para tornado
          currentTime + rampTime
        )
      }
    }
  }
  
  /**
   * Limpiar recursos
   */
  dispose() {
    this.stopRain()
    this.stopWind()
    this.stopTornado()
    
    if (this.masterGain) {
      this.masterGain.disconnect()
      this.masterGain = undefined
    }
    
    if (this.context) {
      this.context.close()
      this.context = undefined
    }
    
    this.enabled = false
    console.log('🎵 ProceduralAudio disposed')
  }
}

// Instancia global
let proceduralAudio: ProceduralAudioGenerator | null = null

export function getProceduralAudio(): ProceduralAudioGenerator {
  if (!proceduralAudio) {
    proceduralAudio = new ProceduralAudioGenerator()
  }
  return proceduralAudio
}

export default ProceduralAudioGenerator

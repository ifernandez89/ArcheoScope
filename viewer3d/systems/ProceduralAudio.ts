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
  private context: AudioContext | null = null
  private masterGain: GainNode | null = null
  
  // Generadores activos
  private rainGenerator: AudioWorkletNode | null = null
  private windGenerator: OscillatorNode | null = null
  private windNoise: AudioBufferSourceNode | null = null
  private windLFO: OscillatorNode | null = null
  private windGain: GainNode | null = null
  
  constructor() {
    if (typeof window === 'undefined') return
    
    this.context = new (window.AudioContext || (window as any).webkitAudioContext)()
    this.masterGain = this.context.createGain()
    this.masterGain.gain.value = 0.3 // Volumen master moderado
    this.masterGain.connect(this.context.destination)
    
    console.log('🎵 ProceduralAudio inicializado')
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
    if (!this.context || !this.masterGain) return
    
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
    
    // Guardar referencia (usando any para evitar error de tipo)
    ;(this as any).rainSource = source
    ;(this as any).rainGain = gain
    ;(this as any).rainFilter = filter
    
    console.log('🌧️ Lluvia procedural iniciada:', intensity)
  }
  
  stopRain() {
    const rainSource = (this as any).rainSource
    if (rainSource) {
      rainSource.stop()
      ;(this as any).rainSource = null
      ;(this as any).rainGain = null
      ;(this as any).rainFilter = null
    }
  }
  
  updateRain(intensity: number) {
    const rainGain = (this as any).rainGain
    const rainFilter = (this as any).rainFilter
    
    if (rainGain && rainFilter && this.context) {
      // Fade suave
      rainGain.gain.linearRampToValueAtTime(
        intensity * 0.3,
        this.context.currentTime + 0.5
      )
      
      // Ajustar filtro
      rainFilter.frequency.linearRampToValueAtTime(
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
    if (!this.context || !this.masterGain) return
    
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
    
    // Guardar referencias
    ;(this as any).windSource = source
    ;(this as any).windGain = gain
    ;(this as any).windLFO = lfo
    ;(this as any).windFilter = filter
    
    console.log('🌬️ Viento procedural iniciado:', intensity)
  }
  
  stopWind() {
    const windSource = (this as any).windSource
    const windLFO = (this as any).windLFO
    
    if (windSource) {
      windSource.stop()
      ;(this as any).windSource = null
    }
    if (windLFO) {
      windLFO.stop()
      ;(this as any).windLFO = null
    }
    ;(this as any).windGain = null
    ;(this as any).windFilter = null
  }
  
  updateWind(intensity: number) {
    const windGain = (this as any).windGain
    const windFilter = (this as any).windFilter
    
    if (windGain && windFilter && this.context) {
      windGain.gain.linearRampToValueAtTime(
        intensity * 0.4,
        this.context.currentTime + 0.5
      )
      
      windFilter.frequency.linearRampToValueAtTime(
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
    if (!this.context || !this.masterGain) return
    
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
    
    ;(this as any).tornadoSource = source
    ;(this as any).tornadoLFO = lfo
    
    console.log('🌪️ Tornado procedural iniciado:', intensity)
  }
  
  stopTornado() {
    const tornadoSource = (this as any).tornadoSource
    const tornadoLFO = (this as any).tornadoLFO
    
    if (tornadoSource) {
      tornadoSource.stop()
      ;(this as any).tornadoSource = null
    }
    if (tornadoLFO) {
      tornadoLFO.stop()
      ;(this as any).tornadoLFO = null
    }
  }
  
  /**
   * Ajustar volumen master
   */
  setMasterVolume(volume: number) {
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
    this.stopRain()
    this.stopWind()
    this.stopTornado()
    
    if (this.context) {
      this.context.close()
    }
    
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

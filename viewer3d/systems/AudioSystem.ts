/**
 * AudioSystem - Sistema de audio profesional desacoplado
 * 
 * Arquitectura:
 * - Audio por capas (layered ambience)
 * - Fades suaves entre estados
 * - Mezcla dinámica según intensidad
 * - Lazy loading de assets
 * - Web Audio API nativo (no Three.js Audio)
 */

type AudioLayer = {
  name: string
  buffer: AudioBuffer | null
  source: AudioBufferSourceNode | null
  gainNode: GainNode
  targetVolume: number
  currentVolume: number
  loop: boolean
  loaded: boolean
}

type AudioConfig = {
  masterVolume: number
  ambienceVolume: number
  fxVolume: number
  fadeSpeed: number
}

class AudioManager {
  private context: AudioContext | null = null
  private masterGain: GainNode | null = null
  private ambienceGain: GainNode | null = null
  private fxGain: GainNode | null = null
  private layers: Map<string, AudioLayer> = new Map()
  private config: AudioConfig = {
    masterVolume: 0.7,
    ambienceVolume: 0.8,
    fxVolume: 0.6,
    fadeSpeed: 0.5
  }
  private updateInterval: number | null = null
  
  constructor() {
    if (typeof window === 'undefined') return
    
    // Inicializar Web Audio API
    this.context = new (window.AudioContext || (window as any).webkitAudioContext)()
    
    // Crear nodos de ganancia
    this.masterGain = this.context.createGain()
    this.masterGain.gain.value = this.config.masterVolume
    this.masterGain.connect(this.context.destination)
    
    this.ambienceGain = this.context.createGain()
    this.ambienceGain.gain.value = this.config.ambienceVolume
    this.ambienceGain.connect(this.masterGain)
    
    this.fxGain = this.context.createGain()
    this.fxGain.gain.value = this.config.fxVolume
    this.fxGain.connect(this.masterGain)
    
    // Iniciar loop de actualización para fades
    this.startUpdateLoop()
    
    console.log('🎧 AudioSystem inicializado')
  }
  
  /**
   * Cargar un archivo de audio (lazy loading)
   */
  async loadSound(name: string, path: string, loop: boolean = true, type: 'ambience' | 'fx' = 'ambience') {
    if (!this.context) return
    
    try {
      const response = await fetch(path)
      const arrayBuffer = await response.arrayBuffer()
      const audioBuffer = await this.context.decodeAudioData(arrayBuffer)
      
      const gainNode = this.context.createGain()
      gainNode.gain.value = 0 // Empezar en silencio
      gainNode.connect(type === 'ambience' ? this.ambienceGain! : this.fxGain!)
      
      this.layers.set(name, {
        name,
        buffer: audioBuffer,
        source: null,
        gainNode,
        targetVolume: 0,
        currentVolume: 0,
        loop,
        loaded: true
      })
      
      console.log(`🎵 Audio cargado: ${name}`)
    } catch (error) {
      console.error(`❌ Error cargando audio ${name}:`, error)
    }
  }
  
  /**
   * Reproducir una capa con fade in
   */
  play(name: string, volume: number = 1.0) {
    const layer = this.layers.get(name)
    if (!layer || !layer.loaded || !this.context) return
    
    // Si ya está sonando, solo ajustar volumen
    if (layer.source) {
      this.setVolume(name, volume)
      return
    }
    
    // Crear nuevo source
    layer.source = this.context.createBufferSource()
    layer.source.buffer = layer.buffer
    layer.source.loop = layer.loop
    layer.source.connect(layer.gainNode)
    layer.source.start(0)
    
    // Fade in
    layer.targetVolume = volume
    
    console.log(`▶️ Reproduciendo: ${name} (vol: ${volume})`)
  }
  
  /**
   * Detener una capa con fade out
   */
  stop(name: string) {
    const layer = this.layers.get(name)
    if (!layer || !layer.source) return
    
    // Fade out
    layer.targetVolume = 0
    
    // Detener después del fade
    setTimeout(() => {
      if (layer.source && layer.currentVolume < 0.01) {
        layer.source.stop()
        layer.source = null
        console.log(`⏹️ Detenido: ${name}`)
      }
    }, 2000)
  }
  
  /**
   * Ajustar volumen de una capa (con fade suave)
   */
  setVolume(name: string, volume: number) {
    const layer = this.layers.get(name)
    if (!layer) return
    
    layer.targetVolume = Math.max(0, Math.min(1, volume))
  }
  
  /**
   * Ajustar volumen master
   */
  setMasterVolume(volume: number) {
    if (!this.masterGain) return
    this.config.masterVolume = Math.max(0, Math.min(1, volume))
    this.masterGain.gain.value = this.config.masterVolume
  }
  
  /**
   * Ajustar volumen de ambiente
   */
  setAmbienceVolume(volume: number) {
    if (!this.ambienceGain) return
    this.config.ambienceVolume = Math.max(0, Math.min(1, volume))
    this.ambienceGain.gain.value = this.config.ambienceVolume
  }
  
  /**
   * Ajustar volumen de efectos
   */
  setFxVolume(volume: number) {
    if (!this.fxGain) return
    this.config.fxVolume = Math.max(0, Math.min(1, volume))
    this.fxGain.gain.value = this.config.fxVolume
  }
  
  /**
   * Reproducir efecto de sonido único (no loop)
   */
  playOneShot(name: string, volume: number = 1.0, delay: number = 0) {
    const layer = this.layers.get(name)
    if (!layer || !layer.loaded || !this.context) return
    
    // Crear source temporal
    const source = this.context.createBufferSource()
    source.buffer = layer.buffer
    
    const gainNode = this.context.createGain()
    gainNode.gain.value = volume
    gainNode.connect(this.fxGain!)
    
    source.connect(gainNode)
    
    if (delay > 0) {
      source.start(this.context.currentTime + delay)
    } else {
      source.start(0)
    }
    
    console.log(`🔊 OneShot: ${name} (delay: ${delay}s)`)
  }
  
  /**
   * Loop de actualización para fades suaves
   */
  private startUpdateLoop() {
    if (typeof window === 'undefined') return
    
    const update = () => {
      this.layers.forEach(layer => {
        // Fade suave hacia el volumen objetivo
        const diff = layer.targetVolume - layer.currentVolume
        if (Math.abs(diff) > 0.001) {
          layer.currentVolume += diff * this.config.fadeSpeed * 0.016 // ~60fps
          layer.gainNode.gain.value = layer.currentVolume
        }
      })
    }
    
    this.updateInterval = window.setInterval(update, 16) // ~60fps
  }
  
  /**
   * Limpiar recursos
   */
  dispose() {
    if (this.updateInterval) {
      clearInterval(this.updateInterval)
    }
    
    this.layers.forEach(layer => {
      if (layer.source) {
        layer.source.stop()
      }
    })
    
    if (this.context) {
      this.context.close()
    }
    
    console.log('🎧 AudioSystem disposed')
  }
}

// Instancia global
let audioManager: AudioManager | null = null

export function getAudioManager(): AudioManager {
  if (!audioManager) {
    audioManager = new AudioManager()
  }
  return audioManager
}

export default AudioManager

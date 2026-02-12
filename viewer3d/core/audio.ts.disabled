// Audio System for FASE 2
// Manages background music, narration, and sound effects

export interface AudioTrack {
  id: string
  url: string
  volume: number
  loop: boolean
  type: 'music' | 'narration' | 'effect'
}

export class AudioSystem {
  private audioContext: AudioContext | null = null
  private tracks: Map<string, HTMLAudioElement> = new Map()
  private masterVolume: number = 1.0
  private musicVolume: number = 0.7
  private narrationVolume: number = 1.0
  private effectsVolume: number = 0.8
  private isMuted: boolean = false

  constructor() {
    if (typeof window !== 'undefined') {
      this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
    }
  }

  // Cargar un track de audio
  async loadTrack(track: AudioTrack): Promise<void> {
    return new Promise((resolve, reject) => {
      const audio = new Audio(track.url)
      audio.volume = this.calculateVolume(track.type, track.volume)
      audio.loop = track.loop

      audio.addEventListener('canplaythrough', () => {
        this.tracks.set(track.id, audio)
        console.log(`🎵 Audio cargado: ${track.id}`)
        resolve()
      })

      audio.addEventListener('error', (e) => {
        console.error(`❌ Error cargando audio: ${track.id}`, e)
        reject(e)
      })

      audio.load()
    })
  }

  // Reproducir un track
  play(trackId: string): void {
    const audio = this.tracks.get(trackId)
    if (!audio) {
      console.warn(`⚠️ Track no encontrado: ${trackId}`)
      return
    }

    if (this.audioContext?.state === 'suspended') {
      this.audioContext.resume()
    }

    audio.play().catch(err => {
      console.error(`❌ Error reproduciendo: ${trackId}`, err)
    })
  }

  // Pausar un track
  pause(trackId: string): void {
    const audio = this.tracks.get(trackId)
    if (audio) {
      audio.pause()
    }
  }

  // Detener un track
  stop(trackId: string): void {
    const audio = this.tracks.get(trackId)
    if (audio) {
      audio.pause()
      audio.currentTime = 0
    }
  }

  // Fade in
  fadeIn(trackId: string, duration: number = 1000): void {
    const audio = this.tracks.get(trackId)
    if (!audio) return

    audio.volume = 0
    this.play(trackId)

    const steps = 20
    const stepDuration = duration / steps
    const volumeStep = audio.volume / steps

    let currentStep = 0
    const interval = setInterval(() => {
      currentStep++
      audio.volume = Math.min(volumeStep * currentStep, 1)

      if (currentStep >= steps) {
        clearInterval(interval)
      }
    }, stepDuration)
  }

  // Fade out
  fadeOut(trackId: string, duration: number = 1000): void {
    const audio = this.tracks.get(trackId)
    if (!audio) return

    const initialVolume = audio.volume
    const steps = 20
    const stepDuration = duration / steps
    const volumeStep = initialVolume / steps

    let currentStep = 0
    const interval = setInterval(() => {
      currentStep++
      audio.volume = Math.max(initialVolume - volumeStep * currentStep, 0)

      if (currentStep >= steps) {
        clearInterval(interval)
        this.stop(trackId)
      }
    }, stepDuration)
  }

  // Crossfade entre dos tracks
  crossfade(fromTrackId: string, toTrackId: string, duration: number = 2000): void {
    this.fadeOut(fromTrackId, duration)
    setTimeout(() => {
      this.fadeIn(toTrackId, duration)
    }, duration / 2)
  }

  // Calcular volumen según tipo y configuración
  private calculateVolume(type: AudioTrack['type'], trackVolume: number): number {
    if (this.isMuted) return 0

    let typeVolume = 1.0
    switch (type) {
      case 'music':
        typeVolume = this.musicVolume
        break
      case 'narration':
        typeVolume = this.narrationVolume
        break
      case 'effect':
        typeVolume = this.effectsVolume
        break
    }

    return this.masterVolume * typeVolume * trackVolume
  }

  // Actualizar volúmenes
  updateVolumes(): void {
    this.tracks.forEach((audio, trackId) => {
      const trackType = this.getTrackType(trackId)
      const trackVolume = this.getTrackVolume(trackId)
      audio.volume = this.calculateVolume(trackType, trackVolume)
    })
  }

  // Setters de volumen
  setMasterVolume(volume: number): void {
    this.masterVolume = Math.max(0, Math.min(1, volume))
    this.updateVolumes()
  }

  setMusicVolume(volume: number): void {
    this.musicVolume = Math.max(0, Math.min(1, volume))
    this.updateVolumes()
  }

  setNarrationVolume(volume: number): void {
    this.narrationVolume = Math.max(0, Math.min(1, volume))
    this.updateVolumes()
  }

  setEffectsVolume(volume: number): void {
    this.effectsVolume = Math.max(0, Math.min(1, volume))
    this.updateVolumes()
  }

  // Mute/Unmute
  setMuted(muted: boolean): void {
    this.isMuted = muted
    this.updateVolumes()
  }

  toggleMute(): void {
    this.setMuted(!this.isMuted)
  }

  // Getters
  getMasterVolume(): number {
    return this.masterVolume
  }

  getMusicVolume(): number {
    return this.musicVolume
  }

  getNarrationVolume(): number {
    return this.narrationVolume
  }

  getEffectsVolume(): number {
    return this.effectsVolume
  }

  isMutedState(): boolean {
    return this.isMuted
  }

  // Helpers privados
  private getTrackType(trackId: string): AudioTrack['type'] {
    // Inferir tipo del ID (convención: music-, narration-, effect-)
    if (trackId.startsWith('music-')) return 'music'
    if (trackId.startsWith('narration-')) return 'narration'
    if (trackId.startsWith('effect-')) return 'effect'
    return 'music' // default
  }

  private getTrackVolume(trackId: string): number {
    // Retornar volumen original del track (simplificado)
    return 1.0
  }

  // Limpiar recursos
  dispose(): void {
    this.tracks.forEach(audio => {
      audio.pause()
      audio.src = ''
    })
    this.tracks.clear()
    
    if (this.audioContext) {
      this.audioContext.close()
    }
  }

  // Obtener todos los tracks
  getAllTracks(): string[] {
    return Array.from(this.tracks.keys())
  }

  // Verificar si un track está reproduciéndose
  isPlaying(trackId: string): boolean {
    const audio = this.tracks.get(trackId)
    return audio ? !audio.paused : false
  }
}

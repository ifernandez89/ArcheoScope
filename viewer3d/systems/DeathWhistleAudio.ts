/**
 * DeathWhistleAudio - Silbato de la Muerte Azteca (procedural)
 * Vinculado a rituales de Mictlantecuhtli
 *
 * Arquitectura de audio:
 * white noise -> bandpass formant1 -> bandpass formant2 -> distortion -> tremolo LFO -> masterGain
 */

export class DeathWhistleAudio {
  private context: AudioContext | null = null
  private masterGain: GainNode | null = null
  private noiseSource: AudioBufferSourceNode | null = null
  private formant1: BiquadFilterNode | null = null
  private lfo: OscillatorNode | null = null
  private chaosInterval: ReturnType<typeof setInterval> | null = null
  private isPlaying = false

  private createNoiseBuffer(): AudioBuffer {
    const ctx = this.context!
    const bufferSize = 2 * ctx.sampleRate
    const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate)
    const data = buffer.getChannelData(0)
    for (let i = 0; i < bufferSize; i++) {
      data[i] = Math.random() * 2 - 1
    }
    return buffer
  }

  private makeDistortionCurve(amount: number): Float32Array {
    const n = 44100
    const curve = new Float32Array(n)
    for (let i = 0; i < n; i++) {
      const x = (i * 2) / n - 1
      curve[i] = ((3 + amount) * x * 20 * Math.PI) / (Math.PI + amount * Math.abs(x))
    }
    return curve
  }

  play(): void {
    if (this.isPlaying) return
    if (typeof window === 'undefined') return

    // Leer volumen desde gameSettings
    let savedVolume = 0.7
    try {
      const gs = localStorage.getItem('game_settings')
      if (gs) {
        const parsed = JSON.parse(gs)
        if (parsed?.audio?.masterVolume !== undefined) {
          savedVolume = parsed.audio.masterVolume
        }
      }
    } catch {}

    // 30% del master para equilibrarse con el audio atmosferico
    const volume = savedVolume * 0.3

    try {
      this.context = new (window.AudioContext || (window as any).webkitAudioContext)()
      const ctx = this.context
      const t = ctx.currentTime

      // Master gain con fade in/out
      this.masterGain = ctx.createGain()
      this.masterGain.gain.setValueAtTime(0, t)
      this.masterGain.gain.linearRampToValueAtTime(volume, t + 0.1)
      this.masterGain.gain.setValueAtTime(volume, t + 2.0)
      this.masterGain.gain.linearRampToValueAtTime(0, t + 2.5)
      this.masterGain.connect(ctx.destination)

      // Noise source
      this.noiseSource = ctx.createBufferSource()
      this.noiseSource.buffer = this.createNoiseBuffer()
      this.noiseSource.loop = true

      // Formant 1 - grito principal 800-2000 Hz
      this.formant1 = ctx.createBiquadFilter()
      this.formant1.type = 'bandpass'
      this.formant1.frequency.setValueAtTime(900, t)
      this.formant1.frequency.linearRampToValueAtTime(1800, t + 1.0)
      this.formant1.frequency.linearRampToValueAtTime(800, t + 2.0)
      this.formant1.Q.value = 15

      // Formant 2 - armonico superior
      const formant2 = ctx.createBiquadFilter()
      formant2.type = 'bandpass'
      formant2.frequency.setValueAtTime(1400, t)
      formant2.frequency.linearRampToValueAtTime(2200, t + 1.2)
      formant2.frequency.linearRampToValueAtTime(1100, t + 2.2)
      formant2.Q.value = 8

      // Distorsion reducida
      const distortion: WaveShaperNode = ctx.createWaveShaper()
      Object.assign(distortion, { curve: this.makeDistortionCurve(12), oversample: '2x' })

      // LFO tremolo ~8 Hz
      this.lfo = ctx.createOscillator()
      this.lfo.frequency.value = 8
      this.lfo.type = 'sine'
      const lfoGain = ctx.createGain()
      lfoGain.gain.value = 200
      this.lfo.connect(lfoGain)
      lfoGain.connect(this.formant1.frequency)

      // Cadena de senal
      this.noiseSource.connect(this.formant1)
      this.formant1.connect(formant2)
      formant2.connect(distortion)
      distortion.connect(this.masterGain)

      // Microvariaciones caoticas cada 80ms
      this.chaosInterval = setInterval(() => {
        if (this.formant1 && this.isPlaying) {
          this.formant1.frequency.value = 900 + Math.random() * 800
        }
      }, 80)

      this.lfo.start(t)
      this.noiseSource.start(t)
      this.isPlaying = true

      setTimeout(() => this.stop(), 2600)

    } catch (err) {
      console.warn('DeathWhistle: error de audio', err)
    }
  }

  stop(): void {
    if (this.chaosInterval) {
      clearInterval(this.chaosInterval)
      this.chaosInterval = null
    }
    try { this.noiseSource?.stop() } catch {}
    try { this.lfo?.stop() } catch {}
    try { this.context?.close() } catch {}
    this.context = null
    this.masterGain = null
    this.noiseSource = null
    this.formant1 = null
    this.lfo = null
    this.isPlaying = false
  }
}

let instance: DeathWhistleAudio | null = null
export function getDeathWhistle(): DeathWhistleAudio {
  if (!instance) instance = new DeathWhistleAudio()
  return instance
}

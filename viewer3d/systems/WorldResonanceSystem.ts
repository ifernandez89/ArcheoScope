/**
 * WorldResonanceSystem — "World Resonance"
 * ═══════════════════════════════════════════════════════════════════════
 * Una ÚNICA capa de resonancia subconsciente derivada de la frecuencia
 * simbólica de la escena o sitio actual.
 *
 * FILOSOFÍA:
 * El jugador NO debe pensar "estoy oyendo una frecuencia", sino sentir
 * "no sé por qué, pero este lugar se siente diferente de los demás".
 *
 * - Volumen extremadamente bajo (-32 a -40 dB) — se siente, no se escucha
 * - Un solo oscilador sine + lowpass suave
 * - Transición suave de frecuencia al cambiar de escena (~4s)
 * - Resonancia temporal: la frecuencia varía levemente con la hora del día
 *   (noche -5%, mediodía base) — cambios imperceptibles conscientemente
 *
 * Frecuencias simbólicas por escena/sitio:
 *   menu          54 Hz   (Schumann reducido por octavas — fundación/llamado)
 *   exploration   72 Hz   (9×8 — atención tranquila)
 *   discovery    108 Hz   (tradición hindú/budista/astronómica)
 *   giza         111 Hz   (monumentalidad)
 *   teotihuacan  104 Hz   (más aérea/brillante)
 *   easter-island 63 Hz   (profunda/oceánica)
 *   puma-punku   432 Hz   (identidad existente — frecuencia sagrada)
 *   veracruz      55 Hz   (subterránea/oscura)
 *   gobekli-tepe  45 Hz   (integrada con Khepri)
 */

export type ResonanceScene =
  | 'menu'
  | 'exploration'
  | 'discovery'
  | 'giza'
  | 'teotihuacan'
  | 'easter-island'
  | 'puma-punku'
  | 'veracruz'
  | 'gobekli-tepe'
  | 'default'

interface SceneResonance {
  frequency: number
  /** Ganancia base relativa — frecuencias agudas más bajas para no escucharse */
  gain: number
}

const SCENE_RESONANCES: Record<ResonanceScene, SceneResonance> = {
  menu:           { frequency: 54,  gain: 0.060 },
  exploration:    { frequency: 72,  gain: 0.055 },
  discovery:      { frequency: 108, gain: 0.040 },
  giza:           { frequency: 111, gain: 0.040 },
  teotihuacan:    { frequency: 104, gain: 0.042 },
  'easter-island':{ frequency: 63,  gain: 0.058 },
  'puma-punku':   { frequency: 432, gain: 0.022 }, // agudo → ganancia muy baja
  veracruz:       { frequency: 55,  gain: 0.060 },
  'gobekli-tepe': { frequency: 45,  gain: 0.065 },
  default:        { frequency: 72,  gain: 0.050 },
}

class WorldResonanceSystem {
  private context?: AudioContext
  private masterGain?: GainNode
  private osc?: OscillatorNode
  private oscGain?: GainNode
  private filter?: BiquadFilterNode
  private subOsc?: OscillatorNode    // octava abajo para "cuerpo" subgrave
  private subGain?: GainNode

  private enabled = false
  private currentScene: ResonanceScene = 'default'
  private baseVolume = 0.7
  private temporalFactor = 1.0 // multiplicador de frecuencia por hora del día

  constructor() {
    this.loadSavedVolume()
  }

  private loadSavedVolume(): void {
    if (typeof window === 'undefined') return
    try {
      const gs = localStorage.getItem('game_settings')
      if (gs) {
        const parsed = JSON.parse(gs)
        if (parsed?.audio?.masterVolume !== undefined) {
          this.baseVolume = parsed.audio.masterVolume
        }
      }
    } catch {}
  }

  /**
   * Habilitar la capa (requiere gesto del usuario para el AudioContext)
   */
  async enable(scene: ResonanceScene = 'default'): Promise<void> {
    if (this.enabled) {
      this.setScene(scene)
      return
    }
    if (typeof window === 'undefined') return

    this.loadSavedVolume()
    this.currentScene = scene

    this.context = new (window.AudioContext || (window as any).webkitAudioContext)()
    if (this.context.state === 'suspended') {
      await this.context.resume()
    }

    const res = SCENE_RESONANCES[scene] ?? SCENE_RESONANCES.default

    // master — escala con el volumen general del juego (capa muy sutil)
    this.masterGain = this.context.createGain()
    this.masterGain.gain.value = this.baseVolume
    this.masterGain.connect(this.context.destination)

    // filtro lowpass — suaviza, mantiene el carácter "redondo"
    this.filter = this.context.createBiquadFilter()
    this.filter.type = 'lowpass'
    this.filter.frequency.value = Math.max(res.frequency * 3, 200)
    this.filter.Q.value = 0.4
    this.filter.connect(this.masterGain)

    // oscilador principal
    this.osc = this.context.createOscillator()
    this.osc.type = 'sine'
    this.osc.frequency.value = res.frequency
    this.oscGain = this.context.createGain()
    this.oscGain.gain.value = 0
    this.osc.connect(this.oscGain)
    this.oscGain.connect(this.filter)
    this.osc.start()

    // sub-oscilador una octava abajo (cuerpo subgrave que se "siente")
    this.subOsc = this.context.createOscillator()
    this.subOsc.type = 'sine'
    this.subOsc.frequency.value = res.frequency / 2
    this.subGain = this.context.createGain()
    this.subGain.gain.value = 0
    this.subOsc.connect(this.subGain)
    this.subGain.connect(this.filter)
    this.subOsc.start()

    // fade in lento (4s) hasta la ganancia objetivo
    const now = this.context.currentTime
    this.oscGain.gain.linearRampToValueAtTime(res.gain, now + 4)
    this.subGain.gain.linearRampToValueAtTime(res.gain * 0.5, now + 4)

    this.enabled = true
    console.log(`🌍 WorldResonance habilitado: ${scene} @ ${res.frequency}Hz`)
  }

  /**
   * Cambiar la escena/sitio — transición suave de frecuencia y ganancia (~4s)
   */
  setScene(scene: ResonanceScene): void {
    if (scene === this.currentScene) return
    this.currentScene = scene
    if (!this.enabled || !this.context || !this.osc || !this.oscGain || !this.filter) return

    const res = SCENE_RESONANCES[scene] ?? SCENE_RESONANCES.default
    const now = this.context.currentTime
    const t = 4 // segundos de transición

    const f = res.frequency * this.temporalFactor
    this.osc.frequency.linearRampToValueAtTime(f, now + t)
    this.subOsc?.frequency.linearRampToValueAtTime(f / 2, now + t)
    this.filter.frequency.linearRampToValueAtTime(Math.max(f * 3, 200), now + t)
    this.oscGain.gain.linearRampToValueAtTime(res.gain, now + t)
    this.subGain?.gain.linearRampToValueAtTime(res.gain * 0.5, now + t)

    console.log(`🌍 WorldResonance → ${scene} @ ${res.frequency}Hz`)
  }

  /**
   * Resonancia temporal — la frecuencia varía levemente con la hora del día.
   * @param solarAltitude altura solar en radianes (-PI/2 nadir .. PI/2 cenit)
   *
   * noche  → -5% | amanecer/atardecer → intermedio | mediodía → base
   */
  setTimeOfDay(solarAltitude: number): void {
    if (!this.enabled || !this.context || !this.osc) return
    // norm: 0 = noche profunda, 1 = mediodía
    const norm = Math.max(0, Math.min(1, (solarAltitude + Math.PI / 2) / Math.PI))
    // noche 0.95 (-5%), mediodía 1.00 (base) — cambio imperceptible
    const factor = 0.95 + norm * 0.05
    if (Math.abs(factor - this.temporalFactor) < 0.002) return
    this.temporalFactor = factor

    const res = SCENE_RESONANCES[this.currentScene] ?? SCENE_RESONANCES.default
    const f = res.frequency * factor
    const now = this.context.currentTime
    // transición MUY lenta (20s) para que sea imperceptible
    this.osc.frequency.linearRampToValueAtTime(f, now + 20)
    this.subOsc?.frequency.linearRampToValueAtTime(f / 2, now + 20)
  }

  setMasterVolume(volume: number): void {
    this.baseVolume = Math.max(0, Math.min(1, volume))
    if (this.masterGain && this.context) {
      this.masterGain.gain.linearRampToValueAtTime(this.baseVolume, this.context.currentTime + 0.2)
    }
  }

  isEnabled(): boolean {
    return this.enabled
  }

  getCurrentScene(): ResonanceScene {
    return this.currentScene
  }

  dispose(): void {
    try { this.osc?.stop(); this.osc?.disconnect() } catch {}
    try { this.subOsc?.stop(); this.subOsc?.disconnect() } catch {}
    try { this.oscGain?.disconnect() } catch {}
    try { this.subGain?.disconnect() } catch {}
    try { this.filter?.disconnect() } catch {}
    try { this.masterGain?.disconnect() } catch {}
    try { this.context?.close() } catch {}
    this.osc = undefined
    this.subOsc = undefined
    this.oscGain = undefined
    this.subGain = undefined
    this.filter = undefined
    this.masterGain = undefined
    this.context = undefined
    this.enabled = false
    console.log('🌍 WorldResonance disposed')
  }
}

// Singleton
let instance: WorldResonanceSystem | null = null

export function getWorldResonance(): WorldResonanceSystem {
  if (!instance) {
    instance = new WorldResonanceSystem()
  }
  return instance
}

export default WorldResonanceSystem

/**
 * 🎼 Kepler Harmonices Mundi System
 * 
 * CONCEPTO FUNDAMENTAL:
 * ═══════════════════════════════════════════════════════════════════════
 * Implementación moderna del libro "Harmonices Mundi" de Johannes Kepler (1619)
 * 
 * IDEA DE KEPLER:
 * Los planetas no se mueven a velocidad constante (2da Ley de Kepler):
 * - Van más rápido en perihelio (punto más cercano al Sol)
 * - Van más lento en afelio (punto más lejano del Sol)
 * 
 * Kepler calculó: velocidad_máxima / velocidad_mínima
 * Y lo comparó con intervalos musicales:
 * 
 * ┌──────────┬─────────────────┬──────────────────────────────────┐
 * │ Planeta  │ Intervalo       │ Comportamiento Musical          │
 * ├──────────┼─────────────────┼──────────────────────────────────┤
 * │ Mercurio │ Casi una octava │ Cambios rápidos (glissando)     │
 * │ Venus    │ Pequeña var.    │ Tono muy estable                │
 * │ Tierra   │ Semitono        │ Leve vibración                  │
 * │ Marte    │ Quinta perfecta │ Oscilación marcada              │
 * │ Júpiter  │ Tercera menor   │ Nota grave profunda             │
 * │ Saturno  │ Tercera mayor   │ Nota grave estable              │
 * └──────────┴─────────────────┴──────────────────────────────────┘
 * 
 * IMPLEMENTACIÓN MODERNA:
 * ═══════════════════════════════════════════════════════════════════════
 * 1. Calculamos velocidad orbital en tiempo real
 * 2. Mapeamos velocidad → frecuencia (nota musical)
 * 3. Cada planeta genera un glissando dinámico
 * 4. Cuando todos suenan juntos → "Acorde Cósmico Dinámico"
 * 
 * ALGO QUE KEPLER NO PODÍA HACER (PERO TÚ SÍ):
 * ═══════════════════════════════════════════════════════════════════════
 * - Música en tiempo real
 * - Visualización de ondas sonoras
 * - Detección de resonancias orbitales
 * - Exportación a MIDI
 * - Geometría generada por frecuencias
 * 
 * CONEXIÓN CON FÍSICA REAL:
 * ═══════════════════════════════════════════════════════════════════════
 * Ley de Kepler: T² ∝ a³
 * Traducida a frecuencias → estructura armónica similar a escalas musicales
 * 
 * Resonancias orbitales reales:
 * - Júpiter-Saturno: 5:2
 * - Neptuno-Plutón: 3:2
 * - Tierra-Venus: 8:13 (Fibonacci!)
 * 
 * ESTADO: LISTO PARA USAR
 * ═══════════════════════════════════════════════════════════════════════
 */

import * as THREE from 'three'

// ═══════════════════════════════════════════════════════════════════════
// TIPOS Y CONSTANTES
// ═══════════════════════════════════════════════════════════════════════

/**
 * Datos orbitales de Kepler para cada planeta
 */
interface KeplerOrbitalData {
  id: string
  name: string
  semiMajorAxis: number  // AU (Unidades Astronómicas)
  eccentricity: number   // 0-1 (0 = círculo perfecto)
  perihelionVelocity: number  // km/s
  aphelionVelocity: number    // km/s
  velocityRatio: number  // v_max / v_min (intervalo musical de Kepler)
  musicalInterval: string  // Nombre del intervalo
  baseFrequency: number  // Hz (nota base)
  color: string
}

/**
 * Estado dinámico de un planeta
 */
interface PlanetaryState {
  id: string
  position: THREE.Vector3
  velocity: number  // km/s actual
  frequency: number  // Hz actual (cambia con velocidad)
  phase: number  // 0-1 (posición en órbita)
  note: string  // Nota musical actual
}

/**
 * Acorde cósmico (múltiples planetas sonando juntos)
 */
interface CosmicChord {
  timestamp: number
  planets: string[]  // IDs de planetas
  frequencies: number[]  // Hz de cada planeta
  harmonicRatio: string  // ej: "2:3:5"
  consonance: number  // 0-1 (qué tan consonante es el acorde)
  description: string
}

// ═══════════════════════════════════════════════════════════════════════
// DATOS ASTRONÓMICOS REALES DE KEPLER
// ═══════════════════════════════════════════════════════════════════════

const KEPLER_PLANETARY_DATA: Map<string, KeplerOrbitalData> = new Map([
  ['mercury', {
    id: 'mercury',
    name: 'Mercurio',
    semiMajorAxis: 0.387,
    eccentricity: 0.206,
    perihelionVelocity: 58.98,  // km/s
    aphelionVelocity: 38.86,    // km/s
    velocityRatio: 1.52,  // Casi una octava (2:1 = 2.0)
    musicalInterval: 'Octava menor',
    baseFrequency: 141.27,  // Hz (C#)
    color: '#9c9c9c'
  }],
  ['venus', {
    id: 'venus',
    name: 'Venus',
    semiMajorAxis: 0.723,
    eccentricity: 0.007,  // Casi circular!
    perihelionVelocity: 35.26,
    aphelionVelocity: 34.79,
    velocityRatio: 1.01,  // Casi ninguna variación
    musicalInterval: 'Diesis (25/24)',
    baseFrequency: 221.23,  // Hz (A)
    color: '#f5e6d3'
  }],
  ['earth', {
    id: 'earth',
    name: 'Tierra',
    semiMajorAxis: 1.000,
    eccentricity: 0.017,
    perihelionVelocity: 30.29,
    aphelionVelocity: 29.29,
    velocityRatio: 1.03,  // Semitono (16/15 = 1.067)
    musicalInterval: 'Semitono',
    baseFrequency: 136.10,  // Hz (C# - "Om cósmico")
    color: '#4A90E2'
  }],
  ['mars', {
    id: 'mars',
    name: 'Marte',
    semiMajorAxis: 1.524,
    eccentricity: 0.093,
    perihelionVelocity: 26.50,
    aphelionVelocity: 21.97,
    velocityRatio: 1.21,  // Quinta perfecta (3/2 = 1.5)
    musicalInterval: 'Quinta disminuida',
    baseFrequency: 144.72,  // Hz (D)
    color: '#E27B58'
  }],
  ['jupiter', {
    id: 'jupiter',
    name: 'Júpiter',
    semiMajorAxis: 5.203,
    eccentricity: 0.048,
    perihelionVelocity: 13.72,
    aphelionVelocity: 12.44,
    velocityRatio: 1.10,  // Tercera menor (6/5 = 1.2)
    musicalInterval: 'Tercera menor',
    baseFrequency: 183.58,  // Hz (F#)
    color: '#D4A574'
  }],
  ['saturn', {
    id: 'saturn',
    name: 'Saturno',
    semiMajorAxis: 9.537,
    eccentricity: 0.054,
    perihelionVelocity: 10.18,
    aphelionVelocity: 9.09,
    velocityRatio: 1.12,  // Tercera mayor (5/4 = 1.25)
    musicalInterval: 'Tercera mayor',
    baseFrequency: 147.85,  // Hz (D)
    color: '#FAD5A5'
  }],
  ['uranus', {
    id: 'uranus',
    name: 'Urano',
    semiMajorAxis: 19.191,
    eccentricity: 0.047,
    perihelionVelocity: 7.11,
    aphelionVelocity: 6.49,
    velocityRatio: 1.10,
    musicalInterval: 'Tercera menor',
    baseFrequency: 207.36,  // Hz (G#)
    color: '#4FD0E7'
  }],
  ['neptune', {
    id: 'neptune',
    name: 'Neptuno',
    semiMajorAxis: 30.069,
    eccentricity: 0.009,
    perihelionVelocity: 5.50,
    aphelionVelocity: 5.37,
    velocityRatio: 1.02,
    musicalInterval: 'Coma',
    baseFrequency: 211.44,  // Hz (G#)
    color: '#4166F5'
  }]
])

// ═══════════════════════════════════════════════════════════════════════
// SISTEMA PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════

export class KeplerHarmonicesSystem {
  private enabled = false
  private keplerMode = false  // Modo "Harmonices Mundi" activado
  
  // Audio
  private audioContext?: AudioContext
  private masterGain?: GainNode
  private planetaryGain?: GainNode
  
  // Osciladores planetarios (uno por planeta)
  private planetOscillators: Map<string, {
    osc: OscillatorNode
    gain: GainNode
    filter: BiquadFilterNode
  }> = new Map()
  
  // Estado de planetas
  private planetaryStates: Map<string, PlanetaryState> = new Map()
  
  // Historial de acordes cósmicos
  private cosmicChords: CosmicChord[] = []
  
  // Visualización
  private scene?: THREE.Scene
  private waveVisualizations: Map<string, THREE.Line> = new Map()
  
  constructor() {
    console.log('🎼 Kepler Harmonices System creado')
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // INICIALIZACIÓN
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Habilitar sistema de audio
   */
  async enable(): Promise<void> {
    if (this.enabled) return
    
    if (typeof window === 'undefined') return
    
    // Crear AudioContext
    this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
    
    if (this.audioContext.state === 'suspended') {
      await this.audioContext.resume()
    }
    
    // Crear cadena de ganancia
    this.masterGain = this.audioContext.createGain()
    this.masterGain.gain.value = 0.3  // Volumen moderado
    this.masterGain.connect(this.audioContext.destination)
    
    this.planetaryGain = this.audioContext.createGain()
    this.planetaryGain.gain.value = 1.0
    this.planetaryGain.connect(this.masterGain)
    
    this.enabled = true
    console.log('🎼 Kepler Harmonices habilitado')
  }
  
  /**
   * Activar modo "Harmonices Mundi"
   */
  activateKeplerMode(scene?: THREE.Scene): void {
    if (!this.enabled) {
      console.warn('Sistema no habilitado. Llama a enable() primero.')
      return
    }
    
    if (this.keplerMode) return
    
    this.keplerMode = true
    this.scene = scene
    
    // Crear osciladores para cada planeta
    KEPLER_PLANETARY_DATA.forEach((data, id) => {
      this.createPlanetOscillator(id, data)
    })
    
    console.log('🎵 Modo "Harmonices Mundi" activado')
    console.log('   Escuchando la música de las esferas...')
  }
  
  /**
   * Desactivar modo Kepler
   */
  deactivateKeplerMode(): void {
    if (!this.keplerMode) return
    
    // Detener todos los osciladores
    this.planetOscillators.forEach(({ osc, gain }) => {
      gain.gain.linearRampToValueAtTime(0, this.audioContext!.currentTime + 1)
      setTimeout(() => {
        osc.stop()
        osc.disconnect()
      }, 1000)
    })
    
    this.planetOscillators.clear()
    this.keplerMode = false
    
    console.log('🎵 Modo "Harmonices Mundi" desactivado')
  }
  
  /**
   * Crear oscilador para un planeta
   */
  private createPlanetOscillator(planetId: string, data: KeplerOrbitalData): void {
    if (!this.audioContext || !this.planetaryGain) return
    
    const osc = this.audioContext.createOscillator()
    const gain = this.audioContext.createGain()
    const filter = this.audioContext.createBiquadFilter()
    
    // Configurar oscilador
    osc.type = 'sine'  // Onda pura
    osc.frequency.value = data.baseFrequency
    
    // Configurar filtro (suaviza cambios de frecuencia)
    filter.type = 'lowpass'
    filter.frequency.value = 2000
    filter.Q.value = 1
    
    // Configurar ganancia (volumen)
    gain.gain.value = 0
    
    // Conectar: osc → filter → gain → master
    osc.connect(filter)
    filter.connect(gain)
    gain.connect(this.planetaryGain)
    
    // Iniciar oscilador
    osc.start()
    
    // Fade in suave
    gain.gain.linearRampToValueAtTime(0.08, this.audioContext.currentTime + 2)
    
    // Guardar referencia
    this.planetOscillators.set(planetId, { osc, gain, filter })
    
    console.log(`🪐 ${data.name}: ${data.baseFrequency.toFixed(2)} Hz (${data.musicalInterval})`)
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // ACTUALIZACIÓN DINÁMICA
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Actualizar sistema (llamar cada frame)
   * 
   * @param planetId - ID del planeta
   * @param position - Posición actual en el espacio
   * @param phase - Fase orbital (0-1, donde 0 = perihelio, 0.5 = afelio)
   */
  updatePlanet(planetId: string, position: THREE.Vector3, phase: number): void {
    if (!this.keplerMode || !this.audioContext) return
    
    const data = KEPLER_PLANETARY_DATA.get(planetId)
    if (!data) return
    
    const oscData = this.planetOscillators.get(planetId)
    if (!oscData) return
    
    // Calcular velocidad orbital actual basada en fase
    // Fase 0 = perihelio (más rápido)
    // Fase 0.5 = afelio (más lento)
    const velocity = this.calculateOrbitalVelocity(data, phase)
    
    // Mapear velocidad → frecuencia
    // Velocidad alta → frecuencia alta
    // Velocidad baja → frecuencia baja
    const frequency = this.velocityToFrequency(data, velocity)
    
    // Actualizar frecuencia del oscilador (glissando suave)
    oscData.osc.frequency.linearRampToValueAtTime(
      frequency,
      this.audioContext.currentTime + 0.1
    )
    
    // Determinar nota musical actual
    const note = this.frequencyToNote(frequency)
    
    // Actualizar estado
    this.planetaryStates.set(planetId, {
      id: planetId,
      position: position.clone(),
      velocity,
      frequency,
      phase,
      note
    })
  }
  
  /**
   * Calcular velocidad orbital según fase (Ley de Kepler)
   */
  private calculateOrbitalVelocity(data: KeplerOrbitalData, phase: number): number {
    // Fase 0 = perihelio (velocidad máxima)
    // Fase 0.5 = afelio (velocidad mínima)
    // Fase 1 = perihelio de nuevo
    
    // Normalizar fase a [0, 1]
    const normalizedPhase = phase % 1
    
    // Calcular velocidad usando interpolación coseno (más realista)
    // cos(0) = 1 (perihelio)
    // cos(π) = -1 (afelio)
    const angle = normalizedPhase * Math.PI * 2
    const velocityFactor = (Math.cos(angle) + 1) / 2  // 0-1
    
    // Interpolar entre velocidad mínima y máxima
    const velocity = data.aphelionVelocity + 
                    (data.perihelionVelocity - data.aphelionVelocity) * velocityFactor
    
    return velocity
  }
  
  /**
   * Mapear velocidad orbital → frecuencia musical
   */
  private velocityToFrequency(data: KeplerOrbitalData, velocity: number): number {
    // Normalizar velocidad a [0, 1]
    const velocityRange = data.perihelionVelocity - data.aphelionVelocity
    const normalizedVelocity = (velocity - data.aphelionVelocity) / velocityRange
    
    // Mapear a rango de frecuencias
    // Velocidad alta → frecuencia alta
    const minFreq = data.baseFrequency / data.velocityRatio
    const maxFreq = data.baseFrequency
    
    const frequency = minFreq + (maxFreq - minFreq) * normalizedVelocity
    
    return frequency
  }
  
  /**
   * Convertir frecuencia → nota musical
   */
  private frequencyToNote(frequency: number): string {
    const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    // Calcular número de semitonos desde A4 (440 Hz)
    const semitonesFromA4 = 12 * Math.log2(frequency / 440)
    const noteIndex = Math.round(semitonesFromA4) % 12
    const octave = Math.floor((Math.round(semitonesFromA4) + 9) / 12) + 4
    
    return `${noteNames[(noteIndex + 12) % 12]}${octave}`
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // DETECCIÓN DE ACORDES CÓSMICOS
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Analizar acorde cósmico actual
   */
  analyzeCosmicChord(): CosmicChord | null {
    if (this.planetaryStates.size < 3) return null
    
    const states = Array.from(this.planetaryStates.values())
    const frequencies = states.map(s => s.frequency).sort((a, b) => a - b)
    const planetIds = states.map(s => s.id)
    
    // Calcular ratios armónicos
    const ratios = this.calculateHarmonicRatios(frequencies)
    
    // Calcular consonancia (qué tan "agradable" suena el acorde)
    const consonance = this.calculateConsonance(ratios)
    
    // Generar descripción
    const description = this.describeChord(ratios, consonance)
    
    const chord: CosmicChord = {
      timestamp: Date.now(),
      planets: planetIds,
      frequencies,
      harmonicRatio: ratios.join(':'),
      consonance,
      description
    }
    
    // Guardar en historial si es consonante
    if (consonance > 0.7) {
      this.cosmicChords.push(chord)
      console.log(`🎵 Acorde cósmico consonante detectado: ${description}`)
    }
    
    return chord
  }
  
  /**
   * Calcular ratios armónicos entre frecuencias
   */
  private calculateHarmonicRatios(frequencies: number[]): number[] {
    if (frequencies.length < 2) return []
    
    const baseFreq = frequencies[0]
    return frequencies.map(f => Math.round((f / baseFreq) * 12) / 12)
  }
  
  /**
   * Calcular consonancia del acorde (0-1)
   */
  private calculateConsonance(ratios: number[]): number {
    // Ratios consonantes conocidos
    const consonantRatios = [
      1.0,   // Unísono
      1.5,   // Quinta perfecta (3:2)
      1.25,  // Tercera mayor (5:4)
      1.33,  // Cuarta perfecta (4:3)
      2.0,   // Octava (2:1)
      1.2,   // Tercera menor (6:5)
    ]
    
    let consonanceScore = 0
    
    ratios.forEach(ratio => {
      const closestConsonant = consonantRatios.reduce((prev, curr) => 
        Math.abs(curr - ratio) < Math.abs(prev - ratio) ? curr : prev
      )
      
      const distance = Math.abs(ratio - closestConsonant)
      consonanceScore += Math.max(0, 1 - distance * 10)
    })
    
    return consonanceScore / ratios.length
  }
  
  /**
   * Describir acorde en lenguaje musical
   */
  private describeChord(ratios: number[], consonance: number): string {
    if (consonance > 0.9) return 'Acorde perfecto'
    if (consonance > 0.7) return 'Acorde consonante'
    if (consonance > 0.5) return 'Acorde disonante suave'
    return 'Acorde disonante'
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // CONTROL Y ESTADO
  // ═══════════════════════════════════════════════════════════════════════
  
  isEnabled(): boolean {
    return this.enabled
  }
  
  isKeplerModeActive(): boolean {
    return this.keplerMode
  }
  
  /**
   * Obtener estado de todos los planetas
   */
  getPlanetaryStates(): PlanetaryState[] {
    return Array.from(this.planetaryStates.values())
  }
  
  /**
   * Obtener historial de acordes cósmicos
   */
  getCosmicChords(): CosmicChord[] {
    return [...this.cosmicChords]
  }
  
  /**
   * Ajustar volumen maestro
   */
  setMasterVolume(volume: number): void {
    if (this.masterGain && this.audioContext) {
      this.masterGain.gain.linearRampToValueAtTime(
        Math.max(0, Math.min(1, volume)),
        this.audioContext.currentTime + 0.1
      )
    }
  }
  
  /**
   * Limpiar recursos
   */
  dispose(): void {
    this.deactivateKeplerMode()
    
    if (this.audioContext) {
      this.audioContext.close()
      this.audioContext = undefined
    }
    
    this.enabled = false
    console.log('🎼 Kepler Harmonices disposed')
  }
}

// ═══════════════════════════════════════════════════════════════════════
// SINGLETON
// ═══════════════════════════════════════════════════════════════════════

let instance: KeplerHarmonicesSystem | null = null

export function getKeplerHarmonices(): KeplerHarmonicesSystem {
  if (!instance) {
    instance = new KeplerHarmonicesSystem()
  }
  return instance
}

export default KeplerHarmonicesSystem

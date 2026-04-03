/**
 * HarmoniaMundiSystem - Sistema de música cósmica procedural
 * 
 * Concepto: El universo como instrumento musical vivo
 * - Cada planeta = nota/drone
 * - Órbitas = ritmo
 * - Arquitectura = amplificadores/resonadores
 * - Misiones = desbloquean capas sonoras
 * 
 * V1: Solo Tierra (5 misiones)
 * V2+: Otros planetas
 */

interface CelestialBody {
  id: string
  name: string
  frequency: number      // Hz base (se toca 4 octavas abajo para drone)
  note: string
  orbitalPeriod: number  // días (para pulsos)
  color: string          // para visualización futura
}

interface MissionLayer {
  id: string
  name: string
  description: string
  frequency: number      // Hz específica de esta capa
  type: 'drone' | 'harmonic' | 'pulse' | 'texture' | 'resonance'
  intensity: number      // 0-1
  unlocked: boolean
}

interface ArchitectureAmplifier {
  siteId: string
  name: string
  filterType: BiquadFilterType
  frequency: number
  Q: number
  gain: number
  description: string
}

export class HarmoniaMundiSystem {
  private context?: AudioContext
  private masterGain?: GainNode
  private enabled = false
  private pendingMasterVolume: number = 0.7 // Guarda volumen aunque no esté habilitado
  
  // Capas de volumen separadas
  private planetaryGain?: GainNode      // Drones planetarios
  private harmonicGain?: GainNode       // Armónicos
  private pulseGain?: GainNode          // Pulsos orbitales
  private architectureGain?: GainNode   // Amplificación de arquitectura
  
  // Osciladores activos
  private activeOscillators: Map<string, {
    osc: OscillatorNode
    gain: GainNode
    lfo?: OscillatorNode
    lfoGain?: GainNode
  }> = new Map()
  
  // Filtros de arquitectura activos
  private activeFilters: Map<string, BiquadFilterNode> = new Map()
  
  // Configuración de cuerpos celestes (preparado para expansión)
  private celestialBodies: Map<string, CelestialBody> = new Map([
    ['earth', {
      id: 'earth',
      name: 'Tierra',
      frequency: 136.10, // C# - "Om cósmico"
      note: 'C#',
      orbitalPeriod: 365.25,
      color: '#4A90E2'
    }],
    // Preparado para V2+
    ['mars', {
      id: 'mars',
      name: 'Marte',
      frequency: 144.72,
      note: 'D',
      orbitalPeriod: 687,
      color: '#E27B58'
    }],
    ['jupiter', {
      id: 'jupiter',
      name: 'Júpiter',
      frequency: 183.58,
      note: 'F#',
      orbitalPeriod: 4333,
      color: '#D4A574'
    }]
  ])
  
  // 5 Misiones de la Tierra (V1)
  private earthMissionLayers: Map<string, MissionLayer> = new Map([
    ['earth_base_ambient', {
      id: 'earth_base_ambient',
      name: 'Silencio Cósmico',
      description: 'Ambientación base del espacio',
      frequency: 40, // Frecuencia muy baja, casi imperceptible
      type: 'drone',
      intensity: 0.08, // Muy sutil
      unlocked: true // ✅ Desbloqueado desde el inicio
    }],
    ['earth_mission_1', {
      id: 'earth_mission_1',
      name: 'Despertar Terrestre',
      description: 'Drone fundamental de la Tierra',
      frequency: 136.10 / 16, // 4 octavas abajo = 8.51 Hz (subgrave)
      type: 'drone',
      intensity: 0.15,
      unlocked: false
    }],
    ['earth_mission_2', {
      id: 'earth_mission_2',
      name: 'Pulso Vital',
      description: 'Pulso orbital sutil',
      frequency: 1 / 365.25, // Muy lento (1 ciclo por año simulado)
      type: 'pulse',
      intensity: 0.1,
      unlocked: false
    }],
    ['earth_mission_3', {
      id: 'earth_mission_3',
      name: 'Primer Armónico',
      description: 'Armónico cristalino',
      frequency: (136.10 / 16) * 2, // Primera octava arriba
      type: 'harmonic',
      intensity: 0.08,
      unlocked: false
    }],
    ['earth_mission_4', {
      id: 'earth_mission_4',
      name: 'Textura Atmosférica',
      description: 'Capa de textura ambiental',
      frequency: (136.10 / 16) * 3, // Quinta perfecta
      type: 'texture',
      intensity: 0.06,
      unlocked: false
    }],
    ['earth_mission_5', {
      id: 'earth_mission_5',
      name: 'Resonancia Completa',
      description: 'Campo de resonancia total',
      frequency: (136.10 / 16) * 4, // Segunda octava
      type: 'resonance',
      intensity: 0.12,
      unlocked: false
    }]
  ])
  
  // Amplificadores de arquitectura
  private architectureAmplifiers: Map<string, ArchitectureAmplifier> = new Map([
    ['giza', {
      siteId: 'giza',
      name: 'Pirámides de Giza',
      filterType: 'bandpass',
      frequency: 150,
      Q: 2,
      gain: 1.5,
      description: 'Amplifican frecuencias solares'
    }],
    ['teotihuacan', {
      siteId: 'teotihuacan',
      name: 'Teotihuacán',
      filterType: 'highpass',
      frequency: 200,
      Q: 1.5,
      gain: 1.3,
      description: 'Generan armónicos cristalinos'
    }],
    ['easter-island', {
      siteId: 'easter-island',
      name: 'Isla de Pascua',
      filterType: 'lowpass',
      frequency: 80,
      Q: 3,
      gain: 2.0,
      description: 'Amplifican subgraves oceánicos'
    }],
    ['puma-punku', {
      siteId: 'puma-punku',
      name: 'Puma Punku',
      filterType: 'peaking',
      frequency: 432,
      Q: 5,
      gain: 1.8,
      description: 'Resuenan en frecuencia sagrada'
    }],
    ['veracruz', {
      siteId: 'veracruz',
      name: 'Tres Zapotes',
      filterType: 'notch' as BiquadFilterType,
      frequency: 110,
      Q: 4,
      gain: 1.6,
      description: 'Resonancia olmeca del inframundo'
    }]
  ])
  
  constructor() {
    console.log('🎼 HarmoniaMundiSystem creado')
  }
  
  /**
   * Habilitar sistema (requiere interacción del usuario)
   */
  async enable(): Promise<void> {
    if (this.enabled) return
    
    if (typeof window === 'undefined') return
    
    // Crear AudioContext
    this.context = new (window.AudioContext || (window as any).webkitAudioContext)()
    
    if (this.context.state === 'suspended') {
      await this.context.resume()
    }
    
    // Crear cadena de ganancia
    this.masterGain = this.context.createGain()
    
    // Leer volumen guardado desde gameSettings
    let savedVolume = this.pendingMasterVolume
    try {
      const gs = localStorage.getItem('game_settings')
      if (gs) {
        const parsed = JSON.parse(gs)
        if (parsed?.audio?.masterVolume !== undefined) {
          savedVolume = parsed.audio.masterVolume
          this.pendingMasterVolume = savedVolume
        }
      }
    } catch {}
    
    this.masterGain.gain.value = savedVolume
    this.masterGain.connect(this.context.destination)
    
    // Capas de volumen
    this.planetaryGain = this.context.createGain()
    this.planetaryGain.gain.value = 1.0
    this.planetaryGain.connect(this.masterGain)
    
    this.harmonicGain = this.context.createGain()
    this.harmonicGain.gain.value = 0.8
    this.harmonicGain.connect(this.masterGain)
    
    this.pulseGain = this.context.createGain()
    this.pulseGain.gain.value = 0.6
    this.pulseGain.connect(this.masterGain)
    
    this.architectureGain = this.context.createGain()
    this.architectureGain.gain.value = 1.0
    this.architectureGain.connect(this.masterGain)
    
    this.enabled = true
    console.log('🎼 Harmonia Mundi habilitado con volumen:', this.masterGain.gain.value)
    
    // Activar capas ya desbloqueadas
    this.earthMissionLayers.forEach(layer => {
      if (layer.unlocked) {
        this.createLayerOscillator(layer)
        console.log(`🎵 Capa base activada: ${layer.name}`)
      }
    })
  }
  
  /**
   * Desbloquear capa de misión (V1: solo Tierra)
   */
  unlockMissionLayer(missionId: string): void {
    if (!this.enabled || !this.context) {
      console.warn('Sistema no habilitado')
      return
    }
    
    const layer = this.earthMissionLayers.get(missionId)
    if (!layer) {
      console.warn(`Misión ${missionId} no encontrada`)
      return
    }
    
    if (layer.unlocked) {
      console.log(`Capa ${layer.name} ya desbloqueada`)
      return
    }
    
    // Marcar como desbloqueada
    layer.unlocked = true
    
    // Crear oscilador según tipo
    this.createLayerOscillator(layer)
    
    console.log(`🎵 Capa desbloqueada: ${layer.name}`)
    console.log(`   ${layer.description}`)
  }
  
  /**
   * Crear oscilador para una capa
   */
  private createLayerOscillator(layer: MissionLayer): void {
    if (!this.context) return
    
    const osc = this.context.createOscillator()
    const gain = this.context.createGain()
    
    // Configurar según tipo
    switch (layer.type) {
      case 'drone':
        osc.type = 'sine'
        osc.frequency.value = layer.frequency
        gain.gain.value = 0
        gain.connect(this.planetaryGain!)
        break
        
      case 'harmonic':
        osc.type = 'triangle' // Más armónicos
        osc.frequency.value = layer.frequency
        gain.gain.value = 0
        gain.connect(this.harmonicGain!)
        break
        
      case 'pulse':
        osc.type = 'sine'
        osc.frequency.value = layer.frequency * 100 // Más audible
        gain.gain.value = 0
        
        // LFO para pulso
        const lfo = this.context.createOscillator()
        lfo.frequency.value = layer.frequency
        lfo.type = 'sine'
        
        const lfoGain = this.context.createGain()
        lfoGain.gain.value = layer.intensity * 0.5
        
        lfo.connect(lfoGain)
        lfoGain.connect(gain.gain)
        lfo.start()
        
        gain.connect(this.pulseGain!)
        
        this.activeOscillators.set(layer.id, { osc, gain, lfo, lfoGain })
        osc.connect(gain)
        osc.start()
        
        // Fade in
        gain.gain.linearRampToValueAtTime(
          layer.intensity,
          this.context.currentTime + 3
        )
        return
        
      case 'texture':
        osc.type = 'sawtooth' // Más textura
        osc.frequency.value = layer.frequency
        gain.gain.value = 0
        gain.connect(this.harmonicGain!)
        break
        
      case 'resonance':
        osc.type = 'sine'
        osc.frequency.value = layer.frequency
        gain.gain.value = 0
        gain.connect(this.planetaryGain!)
        break
    }
    
    osc.connect(gain)
    osc.start()
    
    // Fade in suave (3 segundos)
    gain.gain.linearRampToValueAtTime(
      layer.intensity,
      this.context.currentTime + 3
    )
    
    // Guardar referencia
    this.activeOscillators.set(layer.id, { osc, gain })
  }
  
  /**
   * Activar amplificador de arquitectura
   */
  activateArchitecture(siteId: string): void {
    if (!this.enabled || !this.context || !this.architectureGain) return
    
    const amplifier = this.architectureAmplifiers.get(siteId)
    if (!amplifier) return
    
    // Si ya está activo, no hacer nada
    if (this.activeFilters.has(siteId)) return
    
    // Crear filtro
    const filter = this.context.createBiquadFilter()
    filter.type = amplifier.filterType
    filter.frequency.value = amplifier.frequency
    filter.Q.value = amplifier.Q
    filter.gain.value = amplifier.gain
    
    // Insertar en la cadena
    this.architectureGain.disconnect()
    this.architectureGain.connect(filter)
    filter.connect(this.masterGain!)
    
    this.activeFilters.set(siteId, filter)
    
    console.log(`🏛️ Arquitectura activada: ${amplifier.name}`)
    console.log(`   ${amplifier.description}`)
  }
  
  /**
   * Desactivar amplificador de arquitectura
   */
  deactivateArchitecture(siteId: string): void {
    if (!this.architectureGain || !this.masterGain) return
    
    const filter = this.activeFilters.get(siteId)
    if (!filter) return
    
    // Reconectar sin filtro
    this.architectureGain.disconnect()
    this.architectureGain.connect(this.masterGain)
    
    filter.disconnect()
    this.activeFilters.delete(siteId)
    
    console.log(`🏛️ Arquitectura desactivada: ${siteId}`)
  }
  
  /**
   * Ajustar volúmenes
   */
  setMasterVolume(volume: number): void {
    this.pendingMasterVolume = Math.max(0, Math.min(1, volume))
    if (this.masterGain && this.context) {
      this.masterGain.gain.linearRampToValueAtTime(
        this.pendingMasterVolume,
        this.context.currentTime + 0.1
      )
    }
  }
  
  setPlanetaryVolume(volume: number): void {
    if (this.planetaryGain && this.context) {
      this.planetaryGain.gain.linearRampToValueAtTime(
        Math.max(0, Math.min(1, volume)),
        this.context.currentTime + 0.1
      )
    }
  }
  
  setHarmonicVolume(volume: number): void {
    if (this.harmonicGain && this.context) {
      this.harmonicGain.gain.linearRampToValueAtTime(
        Math.max(0, Math.min(1, volume)),
        this.context.currentTime + 0.1
      )
    }
  }
  
  setPulseVolume(volume: number): void {
    if (this.pulseGain && this.context) {
      this.pulseGain.gain.linearRampToValueAtTime(
        Math.max(0, Math.min(1, volume)),
        this.context.currentTime + 0.1
      )
    }
  }
  
  setArchitectureVolume(volume: number): void {
    if (this.architectureGain && this.context) {
      this.architectureGain.gain.linearRampToValueAtTime(
        Math.max(0, Math.min(1, volume)),
        this.context.currentTime + 0.1
      )
    }
  }
  
  /**
   * Obtener estado de misiones
   */
  getEarthMissionsStatus(): Array<{
    id: string
    name: string
    description: string
    unlocked: boolean
  }> {
    return Array.from(this.earthMissionLayers.values()).map(layer => ({
      id: layer.id,
      name: layer.name,
      description: layer.description,
      unlocked: layer.unlocked
    }))
  }
  
  /**
   * Verificar si está habilitado
   */
  isEnabled(): boolean {
    return this.enabled
  }
  
  /**
   * Limpiar recursos
   */
  dispose(): void {
    // Detener todos los osciladores
    this.activeOscillators.forEach(({ osc, lfo }) => {
      try {
        osc.stop()
        osc.disconnect()
        if (lfo) {
          lfo.stop()
          lfo.disconnect()
        }
      } catch (e) {
        // Ya detenido
      }
    })
    
    this.activeOscillators.clear()
    this.activeFilters.clear()
    
    if (this.context) {
      this.context.close()
      this.context = undefined
    }
    
    this.enabled = false
    console.log('🎼 Harmonia Mundi disposed')
  }
}

// Singleton
let harmoniaMundi: HarmoniaMundiSystem | null = null

export function getHarmoniaMundi(): HarmoniaMundiSystem {
  if (!harmoniaMundi) {
    harmoniaMundi = new HarmoniaMundiSystem()
  }
  return harmoniaMundi
}

export default HarmoniaMundiSystem

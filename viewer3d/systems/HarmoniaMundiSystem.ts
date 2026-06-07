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
  
  // Configuración de cuerpos celestes - TODOS LOS PLANETAS ACTIVOS
  // Frecuencias basadas en período orbital transpuestas al rango audible
  private celestialBodies: Map<string, CelestialBody> = new Map([
    ['mercury', {
      id: 'mercury',
      name: 'Mercurio',
      frequency: 141.27, // C# (88 días)
      note: 'C#',
      orbitalPeriod: 88,
      color: '#8C7853'
    }],
    ['venus', {
      id: 'venus',
      name: 'Venus',
      frequency: 221.23, // A (225 días)
      note: 'A',
      orbitalPeriod: 225,
      color: '#FFC649'
    }],
    ['earth', {
      id: 'earth',
      name: 'Tierra',
      frequency: 136.10, // C# - "Om cósmico"
      note: 'C#',
      orbitalPeriod: 365.25,
      color: '#4A90E2'
    }],
    ['mars', {
      id: 'mars',
      name: 'Marte',
      frequency: 144.72, // D (687 días)
      note: 'D',
      orbitalPeriod: 687,
      color: '#E27B58'
    }],
    ['jupiter', {
      id: 'jupiter',
      name: 'Júpiter',
      frequency: 183.58, // F# (4333 días)
      note: 'F#',
      orbitalPeriod: 4333,
      color: '#D4A574'
    }],
    ['saturn', {
      id: 'saturn',
      name: 'Saturno',
      frequency: 147.85, // D (10759 días)
      note: 'D',
      orbitalPeriod: 10759,
      color: '#FAD5A5'
    }],
    ['uranus', {
      id: 'uranus',
      name: 'Urano',
      frequency: 207.36, // G# (30687 días)
      note: 'G#',
      orbitalPeriod: 30687,
      color: '#4FD0E7'
    }],
    ['neptune', {
      id: 'neptune',
      name: 'Neptuno',
      frequency: 211.44, // G# (60190 días)
      note: 'G#',
      orbitalPeriod: 60190,
      color: '#4166F5'
    }],
    ['pluto', {
      id: 'pluto',
      name: 'Plutón',
      frequency: 140.25, // C# (90560 días) - ¡El más grave!
      note: 'C#',
      orbitalPeriod: 90560,
      color: '#A0826D'
    }]
  ])
  
  // 5 Misiones de la Tierra (V1)
  // PROGRESIÓN MEJORADA: Cada misión suma capas AUDIBLES (armónicos + volumen creciente)
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
      description: 'Drone fundamental de la Tierra + quinta armónica',
      frequency: 136.10 / 4, // 2 octavas abajo = 34 Hz (audible como rumble)
      type: 'drone',
      intensity: 0.20, // Incrementado para ser perceptible
      unlocked: false
    }],
    ['earth_mission_2', {
      id: 'earth_mission_2',
      name: 'Pulso Vital',
      description: 'Pulso rítmico + tercera mayor',
      frequency: 136.10 / 2, // 1 octava abajo = 68 Hz (grave notable)
      type: 'pulse',
      intensity: 0.25, // Incrementado
      unlocked: false
    }],
    ['earth_mission_3', {
      id: 'earth_mission_3',
      name: 'Primer Armónico',
      description: 'Armónico cristalino + coro espacial',
      frequency: 136.10, // Frecuencia base de la Tierra (audible)
      type: 'harmonic',
      intensity: 0.30, // Incrementado
      unlocked: false
    }],
    ['earth_mission_4', {
      id: 'earth_mission_4',
      name: 'Textura Atmosférica',
      description: 'Quinta perfecta + oscilación LFO',
      frequency: 136.10 * 1.5, // Quinta perfecta = 204 Hz
      type: 'texture',
      intensity: 0.35, // Incrementado
      unlocked: false
    }],
    ['earth_mission_5', {
      id: 'earth_mission_5',
      name: 'Resonancia Completa',
      description: 'Octava alta + campo de resonancia total',
      frequency: 136.10 * 2, // Octava arriba = 272 Hz
      type: 'resonance',
      intensity: 0.40, // Incrementado — cúspide sonora
      unlocked: false
    }],
    ['earth_mission_6', {
      id: 'earth_mission_6',
      name: 'Khepri Despierta',
      description: 'El escarabajo sagrado abre el portal final — Göbekli Tepe activado',
      frequency: 45, // Wingbeat grave — criatura antigua
      type: 'texture',
      intensity: 0.18,
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
    }],
    ['gobekli-tepe', {
      siteId: 'gobekli-tepe',
      name: 'Göbekli Tepe',
      filterType: 'bandpass' as BiquadFilterType,
      frequency: 45,
      Q: 8,
      gain: 3.0,
      description: 'Portal primordial — frecuencia del escarabajo sagrado'
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
   * 🪐 ACTIVAR TODOS LOS PLANETAS
   * Crea drones para todos los cuerpos celestes del sistema solar
   * Incluye frecuencias infrasonoras (< 20 Hz) que se transponen automáticamente
   */
  activateAllPlanets(): void {
    if (!this.enabled || !this.context) {
      console.warn('Sistema no habilitado. Llama a enable() primero.')
      return
    }
    
    console.log('🪐 Activando todos los planetas del sistema solar...')
    
    this.celestialBodies.forEach((body, id) => {
      // Calcular frecuencia transpuesta (3 octavas abajo para drones profundos)
      const droneFreq = body.frequency / 8 // Divide por 8 = 3 octavas abajo
      
      // Crear capa de drone para este planeta
      const planetLayer: MissionLayer = {
        id: `planet_${id}`,
        name: `Drone de ${body.name}`,
        description: `Frecuencia orbital: ${body.orbitalPeriod} días`,
        frequency: droneFreq,
        type: 'drone',
        intensity: 0.08, // Sutil para no saturar
        unlocked: true
      }
      
      // Crear oscilador (se ajustará automáticamente al rango audible)
      this.createLayerOscillator(planetLayer)
      
      const finalFreq = droneFreq < 20 ? droneFreq * Math.pow(2, Math.ceil(Math.log2(20 / droneFreq))) : droneFreq
      
      console.log(`  🎵 ${body.name}: ${body.frequency.toFixed(2)} Hz → ${droneFreq.toFixed(2)} Hz → ${finalFreq.toFixed(2)} Hz (${body.note})`)
    })
    
    console.log('✅ Todos los planetas activados - Harmonia Mundi completa')
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
   * MEJORADO: Agrega armónicos perceptibles (quintas, octavas, terceras) + LFO dinámico
   */
  private createLayerOscillator(layer: MissionLayer): void {
    if (!this.context) return
    
    const osc = this.context.createOscillator()
    const gain = this.context.createGain()
    
    // 🎵 AJUSTE DINÁMICO: Transponer al rango audible
    let finalFreq = layer.frequency
    
    // Si está por debajo de 20 Hz, subir octavas hasta ser audible
    while (finalFreq < 20 && finalFreq > 0) {
      finalFreq *= 2
    }
    
    // Si está por encima de 2000 Hz, bajar octavas para mantener drone
    while (finalFreq > 2000) {
      finalFreq /= 2
    }
    
    // ✨ ARMÓNICOS ADICIONALES según tipo de capa
    const harmonics: Array<{ freq: number, type: OscillatorType, intensity: number }> = []
    
    // Configurar según tipo
    switch (layer.type) {
      case 'drone':
        osc.type = 'sine'
        osc.frequency.value = finalFreq
        gain.gain.value = 0
        gain.connect(this.planetaryGain!)
        
        // Agregar quinta perfecta (1.5x)
        harmonics.push({ freq: finalFreq * 1.5, type: 'sine', intensity: layer.intensity * 0.6 })
        break
        
      case 'harmonic':
        osc.type = 'triangle' // Más armónicos
        osc.frequency.value = finalFreq
        gain.gain.value = 0
        gain.connect(this.harmonicGain!)
        
        // Agregar tercera mayor (1.25x) y octava (2x)
        harmonics.push({ freq: finalFreq * 1.25, type: 'triangle', intensity: layer.intensity * 0.5 })
        harmonics.push({ freq: finalFreq * 2, type: 'sine', intensity: layer.intensity * 0.4 })
        break
        
      case 'pulse':
        osc.type = 'sine'
        // Para pulsos, asegurar que sea audible
        let pulseFreq = layer.frequency
        while (pulseFreq < 40) {
          pulseFreq *= 2
        }
        osc.frequency.value = pulseFreq
        gain.gain.value = 0
        
        // LFO para pulso rítmico
        const lfo = this.context.createOscillator()
        lfo.frequency.value = 2.0 // 2 Hz = pulso perceptible
        lfo.type = 'sine'
        
        const lfoGain = this.context.createGain()
        lfoGain.gain.value = layer.intensity * 0.8 // Incrementado para ser notable
        
        lfo.connect(lfoGain)
        lfoGain.connect(gain.gain)
        lfo.start()
        
        gain.connect(this.pulseGain!)
        
        // Agregar tercera (1.2x) para riqueza
        harmonics.push({ freq: pulseFreq * 1.2, type: 'sine', intensity: layer.intensity * 0.5 })
        
        this.activeOscillators.set(layer.id, { osc, gain, lfo, lfoGain })
        osc.connect(gain)
        osc.start()
        
        // Fade in
        gain.gain.linearRampToValueAtTime(
          layer.intensity,
          this.context.currentTime + 3
        )
        
        console.log(`🎵 Pulso creado: ${pulseFreq.toFixed(2)} Hz con LFO 2 Hz`)
        
        // Crear armónicos adicionales
        this.createHarmonics(harmonics, layer.id)
        return
        
      case 'texture':
        osc.type = 'sawtooth' // Más textura
        osc.frequency.value = finalFreq
        gain.gain.value = 0
        gain.connect(this.harmonicGain!)
        
        // LFO de "respiración" para textura orgánica
        const textureLfo = this.context.createOscillator()
        textureLfo.frequency.value = 0.5 // Oscilación lenta
        textureLfo.type = 'sine'
        
        const textureLfoGain = this.context.createGain()
        textureLfoGain.gain.value = layer.intensity * 0.4
        
        textureLfo.connect(textureLfoGain)
        textureLfoGain.connect(gain.gain)
        textureLfo.start()
        
        // Agregar quinta y octava para espacialidad
        harmonics.push({ freq: finalFreq * 1.5, type: 'triangle', intensity: layer.intensity * 0.6 })
        harmonics.push({ freq: finalFreq * 2, type: 'sine', intensity: layer.intensity * 0.3 })
        
        this.activeOscillators.set(layer.id + '_texture_lfo', { osc: textureLfo, gain: textureLfoGain })
        break
        
      case 'resonance':
        osc.type = 'sine'
        osc.frequency.value = finalFreq
        gain.gain.value = 0
        gain.connect(this.planetaryGain!)
        
        // Resonancia potente: octava + quinta + tercera
        harmonics.push({ freq: finalFreq * 2, type: 'sine', intensity: layer.intensity * 0.7 })
        harmonics.push({ freq: finalFreq * 1.5, type: 'triangle', intensity: layer.intensity * 0.6 })
        harmonics.push({ freq: finalFreq * 1.25, type: 'sine', intensity: layer.intensity * 0.5 })
        
        // LFO de intensidad para "respiración épica"
        const resLfo = this.context.createOscillator()
        resLfo.frequency.value = 0.8 // Respiración notable
        resLfo.type = 'sine'
        
        const resLfoGain = this.context.createGain()
        resLfoGain.gain.value = layer.intensity * 0.6
        
        resLfo.connect(resLfoGain)
        resLfoGain.connect(gain.gain)
        resLfo.start()
        
        this.activeOscillators.set(layer.id + '_res_lfo', { osc: resLfo, gain: resLfoGain })
        break
    }
    
    osc.connect(gain)
    osc.start()
    
    // Fade in suave (3 segundos)
    gain.gain.linearRampToValueAtTime(
      layer.intensity,
      this.context.currentTime + 3
    )
    
    // Log para debug
    console.log(`🎵 Capa creada: ${layer.name} — ${finalFreq.toFixed(2)} Hz (${layer.type}) + ${harmonics.length} armónicos`)
    
    // Guardar referencia
    this.activeOscillators.set(layer.id, { osc, gain })
    
    // Crear armónicos adicionales
    if (harmonics.length > 0) {
      this.createHarmonics(harmonics, layer.id)
    }
  }
  
  /**
   * 🎼 Crear armónicos adicionales para enriquecer el sonido
   */
  private createHarmonics(harmonics: Array<{ freq: number, type: OscillatorType, intensity: number }>, baseId: string): void {
    if (!this.context) return
    
    harmonics.forEach((h, idx) => {
      const harmOsc = this.context!.createOscillator()
      const harmGain = this.context!.createGain()
      
      harmOsc.type = h.type
      harmOsc.frequency.value = h.freq
      harmGain.gain.value = 0
      
      harmOsc.connect(harmGain)
      harmGain.connect(this.harmonicGain!)
      harmOsc.start()
      
      // Fade in
      harmGain.gain.linearRampToValueAtTime(
        h.intensity,
        this.context!.currentTime + 3
      )
      
      // Guardar referencia
      this.activeOscillators.set(`${baseId}_harmonic_${idx}`, { osc: harmOsc, gain: harmGain })
      
      console.log(`  ↳ Armónico ${idx + 1}: ${h.freq.toFixed(2)} Hz (${h.type})`)
    })
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
   * 🪲 KHEPRI DESPIERTA — Sonido del escarabajo sagrado
   * Se activa al completar Göbekli Tepe (6ta misión)
   * 3 capas: wingbeat oscillator + noise turbulence + harmonic buzz
   * Efecto cinematográfico: zumbido lejano → crescendo → enjambre
   */
  playBeetleSound(): void {
    if (!this.enabled || !this.context) return

    const ctx = this.context
    const now = ctx.currentTime
    const master = this.masterGain!

    // ── Capa 1: Wingbeat oscillator (alas graves) ─────────────────────────
    const wingOsc = ctx.createOscillator()
    const wingGain = ctx.createGain()
    const wingFilter = ctx.createBiquadFilter()

    wingOsc.type = 'sawtooth'
    wingOsc.frequency.value = 45  // Grave — criatura antigua
    wingFilter.type = 'lowpass'
    wingFilter.frequency.value = 300
    wingFilter.Q.value = 2

    wingGain.gain.setValueAtTime(0, now)
    wingGain.gain.linearRampToValueAtTime(0.18, now + 4)   // fade in lento
    wingGain.gain.linearRampToValueAtTime(0.28, now + 10)  // crescendo
    wingGain.gain.linearRampToValueAtTime(0.35, now + 18)  // enjambre
    wingGain.gain.linearRampToValueAtTime(0.15, now + 30)  // settle

    wingOsc.connect(wingFilter)
    wingFilter.connect(wingGain)
    wingGain.connect(master)
    wingOsc.start(now)

    // Microinestabilidad natural del aleteo
    const jitterInterval = setInterval(() => {
      if (!this.enabled) { clearInterval(jitterInterval); return }
      wingOsc.frequency.value = 42 + Math.random() * 10
    }, 50)

    // ── Capa 2: LFO modulación de amplitud (pulso de alas) ────────────────
    const lfo = ctx.createOscillator()
    const lfoGain = ctx.createGain()

    lfo.type = 'sine'
    lfo.frequency.value = 80  // 80 pulsos/seg = aleteo rápido
    lfoGain.gain.setValueAtTime(0, now)
    lfoGain.gain.linearRampToValueAtTime(0.12, now + 3)
    lfoGain.gain.linearRampToValueAtTime(0.22, now + 12)

    lfo.connect(lfoGain)
    lfoGain.connect(wingGain.gain)  // modula la amplitud del wingbeat
    lfo.start(now)

    // ── Capa 3: Harmonic buzz (300-400 Hz — armónicos aerodinámicos) ──────
    const buzzOsc = ctx.createOscillator()
    const buzzGain = ctx.createGain()
    const buzzFilter = ctx.createBiquadFilter()

    buzzOsc.type = 'square'
    buzzOsc.frequency.value = 320
    buzzFilter.type = 'bandpass'
    buzzFilter.frequency.value = 350
    buzzFilter.Q.value = 3

    buzzGain.gain.setValueAtTime(0, now)
    buzzGain.gain.linearRampToValueAtTime(0.06, now + 6)
    buzzGain.gain.linearRampToValueAtTime(0.12, now + 15)
    buzzGain.gain.linearRampToValueAtTime(0.08, now + 30)

    buzzOsc.connect(buzzFilter)
    buzzFilter.connect(buzzGain)
    buzzGain.connect(master)
    buzzOsc.start(now)

    // Guardar referencias para cleanup
    this.activeOscillators.set('beetle_wing', { osc: wingOsc, gain: wingGain, lfo, lfoGain })
    this.activeOscillators.set('beetle_buzz', { osc: buzzOsc, gain: buzzGain })

    console.log('🪲 Khepri despierta — sonido del escarabajo sagrado activado')
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
   * 🪐 Obtener información de todos los planetas
   */
  getAllPlanetsInfo(): Array<{
    id: string
    name: string
    frequency: number
    note: string
    orbitalPeriod: number
    droneFrequency: number
    audibleFrequency: number
    isInfrasound: boolean
  }> {
    return Array.from(this.celestialBodies.values()).map(body => {
      const droneFreq = body.frequency / 8
      let audibleFreq = droneFreq
      
      // Calcular frecuencia audible
      while (audibleFreq < 20 && audibleFreq > 0) {
        audibleFreq *= 2
      }
      
      return {
        id: body.id,
        name: body.name,
        frequency: body.frequency,
        note: body.note,
        orbitalPeriod: body.orbitalPeriod,
        droneFrequency: droneFreq,
        audibleFrequency: audibleFreq,
        isInfrasound: droneFreq < 20
      }
    })
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

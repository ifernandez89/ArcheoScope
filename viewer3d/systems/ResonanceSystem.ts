/**
 * ResonanceSystem - Sistema matemático de resonancia dimensional
 * 
 * NO genera audio directamente.
 * Solo calcula valores de resonancia [-1, 1]
 * 
 * Filosofía:
 * - La resonancia es una variable matemática
 * - El audio es un subproducto de la resonancia
 * - Otras entidades pueden "ver" la frecuencia sin escucharla
 */

export interface ResonanceConfig {
  baseFrequency: number      // Frecuencia base (no Hz literal, valor relativo)
  intensity: number           // Intensidad [0, 1]
  falloff: number            // Caída con distancia
  harmonics: number[]        // Armónicos relativos [2, 3, 4, 5...]
  phase: number              // Fase inicial [0, 2π]
}

export interface ResonanceState {
  value: number              // [-1, 1] - Valor principal de resonancia
  phase: number              // [0, 2π] - Fase actual
  harmonicValues: number[]   // Valores de cada armónico
  stability: number          // [0, 1] - Estabilidad (qué tan cerca de 0)
  profile: 'harmonic' | 'dissonant' | 'neutral'  // Perfil de resonancia
}

export class ResonanceSystem {
  private time: number = 0
  private config: ResonanceConfig
  
  constructor(config: Partial<ResonanceConfig> = {}) {
    // Configuración por defecto
    this.config = {
      baseFrequency: 1.0,
      intensity: 0.5,
      falloff: 0.01,
      harmonics: [2, 3, 4, 5],
      phase: 0,
      ...config
    }
  }
  
  /**
   * Actualizar sistema (llamar cada frame)
   */
  update(deltaTime: number): ResonanceState {
    this.time += deltaTime
    
    // Calcular fase actual
    const phase = (this.time * this.config.baseFrequency + this.config.phase) % (Math.PI * 2)
    
    // Calcular resonancia base (onda senoidal)
    const baseValue = Math.sin(phase) * this.config.intensity
    
    // Calcular armónicos
    const harmonicValues = this.config.harmonics.map((harmonic, i) => {
      const harmonicPhase = phase * harmonic
      // Cada armónico es más débil (dividido por su índice + 2)
      return Math.sin(harmonicPhase) * (this.config.intensity / (i + 2))
    })
    
    // Valor final (base + suma de armónicos)
    const rawValue = baseValue + harmonicValues.reduce((a, b) => a + b, 0)
    
    // Normalizar a [-1, 1]
    const value = Math.max(-1, Math.min(1, rawValue))
    
    // Estabilidad: qué tan cerca está de 0 (equilibrio)
    // 1 = muy estable (cerca de 0)
    // 0 = muy inestable (cerca de -1 o 1)
    const stability = 1 - Math.abs(value)
    
    // Determinar perfil
    const profile = this.getProfile(value, stability)
    
    return {
      value,
      phase,
      harmonicValues,
      stability,
      profile
    }
  }
  
  /**
   * Calcular resonancia en punto específico del espacio
   */
  getResonanceAt(x: number, y: number, z: number): number {
    const distance = Math.sqrt(x * x + y * y + z * z)
    
    // Falloff exponencial con distancia
    const falloff = Math.exp(-distance * this.config.falloff)
    
    // Obtener estado actual
    const state = this.update(0)
    
    // Aplicar falloff
    return state.value * falloff
  }
  
  /**
   * Verificar si una entidad está en resonancia
   */
  isInResonance(entityFreq: number, threshold: number = 0.1): boolean {
    const diff = Math.abs(entityFreq - this.config.baseFrequency)
    return diff < threshold
  }
  
  /**
   * Calcular compatibilidad entre dos frecuencias
   */
  getCompatibility(freq1: number, freq2: number): number {
    const diff = Math.abs(freq1 - freq2)
    // Compatibilidad inversa a la diferencia
    return Math.max(0, 1 - diff)
  }
  
  /**
   * Determinar perfil de resonancia
   */
  private getProfile(value: number, stability: number): 'harmonic' | 'dissonant' | 'neutral' {
    // Armónico: alta estabilidad (cerca de equilibrio)
    if (stability > 0.7) return 'harmonic'
    
    // Disonante: baja estabilidad (extremos)
    if (stability < 0.3) return 'dissonant'
    
    // Neutral: estabilidad media
    return 'neutral'
  }
  
  /**
   * Configurar nueva frecuencia base
   */
  setBaseFrequency(frequency: number): void {
    this.config.baseFrequency = frequency
  }
  
  /**
   * Configurar intensidad
   */
  setIntensity(intensity: number): void {
    this.config.intensity = Math.max(0, Math.min(1, intensity))
  }
  
  /**
   * Agregar armónico
   */
  addHarmonic(harmonic: number): void {
    if (!this.config.harmonics.includes(harmonic)) {
      this.config.harmonics.push(harmonic)
    }
  }
  
  /**
   * Resetear tiempo (útil para sincronización)
   */
  reset(): void {
    this.time = 0
  }
  
  /**
   * Obtener configuración actual
   */
  getConfig(): ResonanceConfig {
    return { ...this.config }
  }
}

export default ResonanceSystem

/**
 * WorldTime - Sistema de tiempo del mundo
 * Responsable de: Tiempo simulado, día/noche, estaciones, ciclos
 */

export interface TimeState {
  worldTime: number // Tiempo en segundos desde inicio
  dayTime: number // 0-1 (0 = medianoche, 0.5 = mediodía)
  season: 'spring' | 'summer' | 'autumn' | 'winter'
  dayOfYear: number // 1-365
  year: number
}

export class WorldTime {
  private static instance: WorldTime
  
  private worldTime: number = 0
  private dayLength: number = 120 // segundos para un día completo
  private yearLength: number = 365 // días por año
  private startYear: number = 2024
  
  private lastUpdate: number = Date.now()
  
  private constructor() {
    console.log('⏰ WorldTime: Inicializado')
  }
  
  static getInstance(): WorldTime {
    if (!WorldTime.instance) {
      WorldTime.instance = new WorldTime()
    }
    return WorldTime.instance
  }
  
  /**
   * Actualizar tiempo del mundo
   */
  update(deltaTime: number, timeScale: number = 1.0): void {
    this.worldTime += deltaTime * timeScale
  }
  
  /**
   * Obtener estado actual del tiempo
   */
  getState(): TimeState {
    const totalDays = this.worldTime / this.dayLength
    const dayOfYear = Math.floor(totalDays % this.yearLength) + 1
    const year = this.startYear + Math.floor(totalDays / this.yearLength)
    const dayTime = (totalDays % 1)
    
    return {
      worldTime: this.worldTime,
      dayTime,
      season: this.getSeason(dayOfYear),
      dayOfYear,
      year
    }
  }
  
  /**
   * Obtener hora del día (0-24)
   */
  getHourOfDay(): number {
    const state = this.getState()
    return state.dayTime * 24
  }
  
  /**
   * Verificar si es de día
   */
  isDaytime(): boolean {
    const hour = this.getHourOfDay()
    return hour >= 6 && hour < 18
  }
  
  /**
   * Verificar si es de noche
   */
  isNighttime(): boolean {
    return !this.isDaytime()
  }
  
  /**
   * Obtener estación del año
   */
  private getSeason(dayOfYear: number): 'spring' | 'summer' | 'autumn' | 'winter' {
    if (dayOfYear < 80) return 'winter'
    if (dayOfYear < 172) return 'spring'
    if (dayOfYear < 264) return 'summer'
    if (dayOfYear < 355) return 'autumn'
    return 'winter'
  }
  
  /**
   * Establecer tiempo específico
   */
  setTime(hours: number): void {
    const state = this.getState()
    const currentDay = Math.floor(this.worldTime / this.dayLength)
    this.worldTime = currentDay * this.dayLength + (hours / 24) * this.dayLength
    console.log(`⏰ WorldTime: Tiempo establecido a ${hours}:00`)
  }
  
  /**
   * Establecer día del año
   */
  setDayOfYear(day: number): void {
    const hour = this.getHourOfDay()
    this.worldTime = (day - 1) * this.dayLength + (hour / 24) * this.dayLength
    console.log(`📅 WorldTime: Día establecido a ${day}`)
  }
  
  /**
   * Configurar velocidad del día
   */
  setDayLength(seconds: number): void {
    this.dayLength = Math.max(10, seconds)
    console.log(`⏱️ WorldTime: Duración del día = ${this.dayLength}s`)
  }
  
  /**
   * Reset
   */
  reset(): void {
    this.worldTime = 0
    this.lastUpdate = Date.now()
    console.log('🔄 WorldTime: Reset')
  }
  
  /**
   * Obtener progreso del día (0-1)
   */
  getDayProgress(): number {
    return this.getState().dayTime
  }
  
  /**
   * Obtener ángulo solar (radianes)
   */
  getSunAngle(): number {
    const dayTime = this.getState().dayTime
    return (dayTime - 0.25) * Math.PI * 2 // -90° a medianoche, 90° a mediodía
  }
}

export default WorldTime.getInstance()

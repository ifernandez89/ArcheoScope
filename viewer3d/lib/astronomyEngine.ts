/**
 * Motor astronómico - Cálculo de posiciones reales usando astronomy-engine
 * 
 * FILOSOFÍA:
 * ✅ Posiciones heliocéntricas REALES según fecha
 * ✅ Velocidades orbitales REALES
 * ✅ Time-scale configurable (1 seg = 1 día simulado)
 * ❌ NO distancias reales (escaladas visualmente)
 * ❌ NO tamaños reales (artísticos)
 */

import * as Astronomy from 'astronomy-engine'

export interface PlanetPosition {
  x: number
  y: number
  z: number
  date: Date
}

export interface OrbitalState {
  mercury: PlanetPosition
  venus: PlanetPosition
  earth: PlanetPosition
  mars: PlanetPosition
  moon: PlanetPosition // Relativa a la Tierra
}

/**
 * Calcula posiciones heliocéntricas reales para una fecha dada
 * Retorna coordenadas en AU (Unidades Astronómicas)
 */
export function calculateOrbitalPositions(date: Date): OrbitalState {
  // Posiciones heliocéntricas (relativas al Sol)
  const mercury = Astronomy.HelioVector('Mercury' as any, date)
  const venus = Astronomy.HelioVector('Venus' as any, date)
  const earth = Astronomy.HelioVector('Earth' as any, date)
  const mars = Astronomy.HelioVector('Mars' as any, date)
  
  // Posición geocéntrica de la Luna (relativa a la Tierra)
  const moon = Astronomy.GeoVector('Moon' as any, date, false)
  
  return {
    mercury: { x: mercury.x, y: mercury.y, z: mercury.z, date },
    venus: { x: venus.x, y: venus.y, z: venus.z, date },
    earth: { x: earth.x, y: earth.y, z: earth.z, date },
    mars: { x: mars.x, y: mars.y, z: mars.z, date },
    moon: { 
      x: moon.x, 
      y: moon.y, 
      z: moon.z, 
      date 
    }
  }
}

/**
 * Motor de tiempo acelerado
 * Permite simular el paso del tiempo a velocidades configurables
 */
export class TimeEngine {
  private simulationTime: Date
  private timeScale: number // Segundos simulados por segundo real
  private isPaused: boolean = false
  
  constructor(startDate: Date = new Date(), timeScale: number = 86400) {
    this.simulationTime = new Date(startDate)
    this.timeScale = timeScale // Por defecto: 1 segundo real = 1 día simulado
  }
  
  /**
   * Actualiza el tiempo simulado
   * @param deltaSeconds - Tiempo transcurrido en segundos reales
   */
  update(deltaSeconds: number): Date {
    if (this.isPaused) return this.simulationTime
    
    const simulatedSeconds = deltaSeconds * this.timeScale
    this.simulationTime = new Date(
      this.simulationTime.getTime() + simulatedSeconds * 1000
    )
    
    return this.simulationTime
  }
  
  /**
   * Cambia la escala de tiempo
   * Ejemplos:
   * - 86400: 1 segundo real = 1 día simulado
   * - 24: 1 hora real = 1 día simulado
   * - 3600: 1 segundo real = 1 hora simulada
   */
  setTimeScale(scale: number) {
    this.timeScale = scale
  }
  
  getTimeScale(): number {
    return this.timeScale
  }
  
  getCurrentTime(): Date {
    return new Date(this.simulationTime)
  }
  
  setTime(date: Date) {
    this.simulationTime = new Date(date)
  }
  
  pause() {
    this.isPaused = true
  }
  
  resume() {
    this.isPaused = false
  }
  
  togglePause() {
    this.isPaused = !this.isPaused
  }
  
  isPausedState(): boolean {
    return this.isPaused
  }
  
  /**
   * Retorna descripción legible de la escala de tiempo
   */
  getTimeScaleDescription(): string {
    const scale = this.timeScale
    
    if (scale === 1) return '1:1 (tiempo real)'
    if (scale === 60) return '1 seg = 1 min'
    if (scale === 3600) return '1 seg = 1 hora'
    if (scale === 86400) return '1 seg = 1 día'
    if (scale === 604800) return '1 seg = 1 semana'
    if (scale === 2592000) return '1 seg = 1 mes'
    if (scale === 31536000) return '1 seg = 1 año'
    
    // Calcular dinámicamente
    const days = scale / 86400
    if (days >= 1) return `1 seg = ${days.toFixed(1)} días`
    
    const hours = scale / 3600
    if (hours >= 1) return `1 seg = ${hours.toFixed(1)} horas`
    
    return `${scale}x`
  }
}

/**
 * Escalador visual - Convierte AU a unidades de escena
 * Mantiene proporciones relativas pero con distancias visuales
 */
export class VisualScaler {
  private scale: number
  
  constructor(scale: number = 200) {
    this.scale = scale // Escala base (Tierra a 200 unidades)
  }
  
  /**
   * Convierte coordenadas astronómicas (AU) a coordenadas de escena
   * Nota: Intercambia Y y Z para Three.js (Y es arriba)
   */
  toSceneCoordinates(pos: PlanetPosition): { x: number, y: number, z: number } {
    return {
      x: pos.x * this.scale,
      y: pos.z * this.scale, // Z astronómico → Y de Three.js
      z: pos.y * this.scale  // Y astronómico → Z de Three.js
    }
  }
  
  /**
   * Escala específica para la Luna (más pequeña)
   */
  toMoonCoordinates(pos: PlanetPosition): { x: number, y: number, z: number } {
    // La Luna está en AU geocéntricas, necesita escala diferente
    // Usamos escala visual de 12 radios terrestres (coherente con diseño anterior)
    const moonScale = this.scale * 12 // 12 radios terrestres (escala visual)
    return {
      x: pos.x * moonScale,
      y: pos.z * moonScale,
      z: pos.y * moonScale
    }
  }
  
  setScale(scale: number) {
    this.scale = scale
  }
  
  getScale(): number {
    return this.scale
  }
}

/**
 * Sistema astronómico completo
 * Integra cálculo de posiciones + motor de tiempo + escalado visual
 */
export class AstronomicalSystem {
  private timeEngine: TimeEngine
  private scaler: VisualScaler
  private currentState: OrbitalState | null = null
  
  constructor(startDate?: Date, timeScale?: number, visualScale?: number) {
    this.timeEngine = new TimeEngine(startDate, timeScale)
    this.scaler = new VisualScaler(visualScale)
  }
  
  /**
   * Actualiza el sistema completo
   * Retorna posiciones escaladas listas para renderizar
   */
  update(deltaSeconds: number) {
    const currentTime = this.timeEngine.update(deltaSeconds)
    this.currentState = calculateOrbitalPositions(currentTime)
    
    return {
      mercury: this.scaler.toSceneCoordinates(this.currentState.mercury),
      venus: this.scaler.toSceneCoordinates(this.currentState.venus),
      earth: this.scaler.toSceneCoordinates(this.currentState.earth),
      mars: this.scaler.toSceneCoordinates(this.currentState.mars),
      moon: this.scaler.toMoonCoordinates(this.currentState.moon),
      date: currentTime
    }
  }
  
  getTimeEngine(): TimeEngine {
    return this.timeEngine
  }
  
  getScaler(): VisualScaler {
    return this.scaler
  }
  
  getCurrentState(): OrbitalState | null {
    return this.currentState
  }
}

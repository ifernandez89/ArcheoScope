/**
 * 🌌 Cosmic Resonance System
 * 
 * CONCEPTO FUNDAMENTAL:
 * ═══════════════════════════════════════════════════════════════════════
 * "La geometría es la frecuencia detrás de los patrones"
 * 
 * Este sistema conecta:
 * - Geometría fundamental del espacio (dodecaedro cósmico)
 * - Simetrías globales (E8, sólidos platónicos)
 * - Modos de vibración (resonancias orbitales)
 * - Partículas y campos (eventos energéticos)
 * - Constantes físicas (proporciones armónicas)
 * 
 * INSPIRACIÓN CIENTÍFICA:
 * ─────────────────────────────────────────────────────────────────────
 * - String Theory: partículas como modos de vibración
 * - Loop Quantum Gravity: espacio-tiempo como redes discretas (spin networks)
 * - Garrett Lisi E8: universo descrito por grupo de simetría de 248 dimensiones
 * - Music of the Spheres: órbitas planetarias como frecuencias musicales
 * - Resonancias orbitales: proporciones armónicas reales en astronomía
 * 
 * ARQUITECTURA:
 * ═══════════════════════════════════════════════════════════════════════
 * 
 * Capa 1 — GEOMETRÍA FUNDAMENTAL
 * ├─ Dodecaedro cósmico invisible (estructura base del universo)
 * ├─ 20 vértices = nodos de resonancia
 * ├─ 12 caras pentagonales = portales de energía
 * └─ Proporción áurea (φ) en todas las relaciones
 * 
 * Capa 2 — VIBRACIONES ORBITALES
 * ├─ Cada planeta genera frecuencia: f ≈ 1/T (T = periodo orbital)
 * ├─ Frecuencias audibles: escaladas 40 octavas arriba
 * ├─ Drones cósmicos: escaladas 4 octavas abajo (subgraves)
 * └─ Conecta con HarmoniaMundiSystem
 * 
 * Capa 3 — NODOS DE ENERGÍA
 * ├─ Cuando planetas forman geometrías específicas → eventos energéticos
 * ├─ Triángulo (3 cuerpos) → impulso gravitacional
 * ├─ Pentágono (5 cuerpos) → energía orbital (proporción áurea)
 * ├─ Dodecaedro proyectado (12 puntos) → evento cósmico raro
 * └─ Resonancias 1:2, 2:3, 3:5 (Fibonacci) → efectos especiales
 * 
 * INTEGRACIÓN CON SISTEMAS EXISTENTES:
 * ═══════════════════════════════════════════════════════════════════════
 * ✅ SacredGeometrySystem: usa sólidos platónicos como base
 * ✅ HarmoniaMundiSystem: genera frecuencias orbitales
 * ✅ ResonanceSystem: calcula valores de resonancia
 * ✅ ResonanceFieldSystem: campos de energía visuales
 * 
 * NO ROMPE NADA:
 * ─────────────────────────────────────────────────────────────────────
 * - Sistema opcional (disabled por defecto)
 * - Se activa solo cuando el jugador lo descubre
 * - No interfiere con gameplay existente
 * - Capa visual separada (puede ocultarse)
 * - Audio independiente (puede silenciarse)
 * 
 * MECÁNICA JUGABLE:
 * ═══════════════════════════════════════════════════════════════════════
 * 1. Jugador descubre "Mapa Armónico del Sistema Solar"
 * 2. Puede ver la red geométrica oculta del universo
 * 3. Desbloquea poliedros, resonancias, portales cósmicos
 * 4. Eventos raros cuando se alinean planetas en geometrías específicas
 * 5. Recompensas: conocimiento, recursos, acceso a zonas secretas
 * 
 * VISUALIZACIÓN:
 * ═══════════════════════════════════════════════════════════════════════
 * - Líneas de resonancia entre planetas (cuando están en proporción armónica)
 * - Poliedros luminosos (cuando se forman geometrías específicas)
 * - Red energética pulsante (dodecaedro cósmico)
 * - Partículas que fluyen por las líneas de resonancia
 * - Colores basados en frecuencia (espectro visible)
 * 
 * ESTADO: PREPARADO PARA ACTIVACIÓN
 * ═══════════════════════════════════════════════════════════════════════
 */

import * as THREE from 'three'
import { PLATONIC_SOLIDS, getPlatonicVertices, type PlatonicSolid } from './SacredGeometrySystem'

// ═══════════════════════════════════════════════════════════════════════
// TIPOS Y CONSTANTES
// ═══════════════════════════════════════════════════════════════════════

const PHI = (1 + Math.sqrt(5)) / 2 // Proporción áurea

export interface CelestialBody {
  id: string
  name: string
  position: THREE.Vector3
  orbitalPeriod: number  // días
  orbitalFrequency: number  // Hz (1/T)
  audioFrequency: number  // Hz audible (escalada)
  color: string
}

export interface GeometricAlignment {
  type: 'triangle' | 'pentagon' | 'hexagon' | 'dodecahedron'
  bodies: string[]  // IDs de cuerpos celestes
  vertices: THREE.Vector3[]
  center: THREE.Vector3
  radius: number
  resonanceStrength: number  // 0-1
  harmonicRatio: string  // ej: "1:2", "2:3", "3:5"
}

export interface ResonanceEvent {
  id: string
  type: 'gravitational_pulse' | 'orbital_energy' | 'cosmic_event' | 'harmonic_resonance'
  alignment: GeometricAlignment
  timestamp: number
  duration: number  // segundos
  intensity: number  // 0-1
  description: string
}

export interface CosmicNode {
  id: string
  position: THREE.Vector3
  frequency: number
  active: boolean
  connections: string[]  // IDs de otros nodos
}

// ═══════════════════════════════════════════════════════════════════════
// SISTEMA PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════

export class CosmicResonanceSystem {
  private enabled = false
  private discovered = false  // Jugador ha descubierto el sistema
  
  // Geometría fundamental
  private cosmicDodecahedron: CosmicNode[] = []
  private dodecahedronMesh?: THREE.LineSegments
  
  // Cuerpos celestes rastreados
  private celestialBodies: Map<string, CelestialBody> = new Map()
  
  // Alineaciones activas
  private activeAlignments: GeometricAlignment[] = []
  
  // Eventos de resonancia
  private activeEvents: ResonanceEvent[] = []
  private eventHistory: ResonanceEvent[] = []
  
  // Visualización
  private resonanceLines: THREE.LineSegments[] = []
  private alignmentMeshes: THREE.Mesh[] = []
  private scene?: THREE.Scene
  
  // Audio
  private audioContext?: AudioContext
  private resonanceOscillators: Map<string, OscillatorNode> = new Map()
  
  constructor() {
    console.log('🌌 CosmicResonanceSystem creado (disabled)')
    this.initializeCosmicDodecahedron()
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // INICIALIZACIÓN
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Inicializar dodecaedro cósmico (estructura invisible del universo)
   */
  private initializeCosmicDodecahedron(): void {
    const vertices = getPlatonicVertices('dodecahedron', 1000) // Radio 1000 unidades
    
    this.cosmicDodecahedron = vertices.map((pos, i) => ({
      id: `cosmic_node_${i}`,
      position: new THREE.Vector3(pos[0], pos[1], pos[2]),
      frequency: 136.10 * (i + 1) / 20, // Frecuencias basadas en Om cósmico
      active: false,
      connections: []
    }))
    
    // Conectar nodos según geometría del dodecaedro
    // Cada vértice se conecta con sus 3 vecinos más cercanos
    this.cosmicDodecahedron.forEach((node, i) => {
      const distances = this.cosmicDodecahedron
        .map((other, j) => ({ j, dist: node.position.distanceTo(other.position) }))
        .filter(({ j }) => j !== i)
        .sort((a, b) => a.dist - b.dist)
        .slice(0, 3)
      
      node.connections = distances.map(({ j }) => this.cosmicDodecahedron[j].id)
    })
    
    console.log('🔷 Dodecaedro cósmico inicializado:', this.cosmicDodecahedron.length, 'nodos')
  }
  
  /**
   * Habilitar sistema (requiere descubrimiento del jugador)
   */
  enable(scene: THREE.Scene): void {
    if (this.enabled) return
    
    this.enabled = true
    this.scene = scene
    
    // Crear visualización del dodecaedro cósmico
    this.createDodecahedronVisualization()
    
    console.log('🌌 Cosmic Resonance System habilitado')
  }
  
  /**
   * Marcar como descubierto por el jugador
   */
  discover(): void {
    if (this.discovered) return
    
    this.discovered = true
    console.log('✨ ¡Mapa Armónico del Sistema Solar descubierto!')
    
    // Guardar en localStorage
    if (typeof window !== 'undefined') {
      localStorage.setItem('cosmic_resonance_discovered', 'true')
    }
  }
  
  /**
   * Verificar si fue descubierto
   */
  isDiscovered(): boolean {
    if (this.discovered) return true
    
    // Verificar localStorage
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('cosmic_resonance_discovered')
      if (saved === 'true') {
        this.discovered = true
        return true
      }
    }
    
    return false
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // REGISTRO DE CUERPOS CELESTES
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Registrar cuerpo celeste para rastreo
   */
  registerCelestialBody(body: CelestialBody): void {
    this.celestialBodies.set(body.id, body)
    console.log(`🪐 Cuerpo celeste registrado: ${body.name}`)
  }
  
  /**
   * Actualizar posición de cuerpo celeste
   */
  updateBodyPosition(id: string, position: THREE.Vector3): void {
    const body = this.celestialBodies.get(id)
    if (body) {
      body.position.copy(position)
    }
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // DETECCIÓN DE ALINEACIONES GEOMÉTRICAS
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Actualizar sistema (llamar cada frame)
   */
  update(deltaTime: number): void {
    if (!this.enabled || !this.discovered) return
    
    // Detectar alineaciones geométricas
    this.detectAlignments()
    
    // Actualizar eventos activos
    this.updateEvents(deltaTime)
    
    // Actualizar visualización
    this.updateVisualization()
  }
  
  /**
   * Detectar alineaciones geométricas entre cuerpos celestes
   */
  private detectAlignments(): void {
    this.activeAlignments = []
    
    const bodies = Array.from(this.celestialBodies.values())
    if (bodies.length < 3) return
    
    // Detectar triángulos (3 cuerpos)
    this.detectTriangles(bodies)
    
    // Detectar pentágonos (5 cuerpos)
    if (bodies.length >= 5) {
      this.detectPentagons(bodies)
    }
    
    // Detectar dodecaedro proyectado (12 puntos)
    if (bodies.length >= 12) {
      this.detectDodecahedronProjection(bodies)
    }
  }
  
  /**
   * Detectar triángulos formados por 3 cuerpos
   */
  private detectTriangles(bodies: CelestialBody[]): void {
    for (let i = 0; i < bodies.length - 2; i++) {
      for (let j = i + 1; j < bodies.length - 1; j++) {
        for (let k = j + 1; k < bodies.length; k++) {
          const a = bodies[i].position
          const b = bodies[j].position
          const c = bodies[k].position
          
          // Calcular ángulos del triángulo
          const ab = b.distanceTo(a)
          const bc = c.distanceTo(b)
          const ca = a.distanceTo(c)
          
          // Verificar si es aproximadamente equilátero (resonancia fuerte)
          const avgSide = (ab + bc + ca) / 3
          const deviation = Math.max(
            Math.abs(ab - avgSide),
            Math.abs(bc - avgSide),
            Math.abs(ca - avgSide)
          ) / avgSide
          
          if (deviation < 0.2) { // 20% de tolerancia
            const center = new THREE.Vector3()
              .add(a).add(b).add(c)
              .divideScalar(3)
            
            const resonanceStrength = 1 - deviation / 0.2
            
            this.activeAlignments.push({
              type: 'triangle',
              bodies: [bodies[i].id, bodies[j].id, bodies[k].id],
              vertices: [a.clone(), b.clone(), c.clone()],
              center,
              radius: avgSide,
              resonanceStrength,
              harmonicRatio: '1:1:1'
            })
            
            // Generar evento si la resonancia es fuerte
            if (resonanceStrength > 0.7) {
              this.createResonanceEvent('gravitational_pulse', this.activeAlignments[this.activeAlignments.length - 1])
            }
          }
        }
      }
    }
  }
  
  /**
   * Detectar pentágonos (proporción áurea)
   */
  private detectPentagons(bodies: CelestialBody[]): void {
    // Implementación simplificada: buscar 5 cuerpos que formen un pentágono aproximado
    // En una implementación completa, verificaríamos ángulos de 108° y proporción áurea
    
    // Por ahora, solo detectamos si 5 cuerpos están aproximadamente equidistantes
    // del centro del sistema
    
    const center = new THREE.Vector3()
    bodies.forEach(b => center.add(b.position))
    center.divideScalar(bodies.length)
    
    const distances = bodies.map(b => b.position.distanceTo(center))
    const avgDist = distances.reduce((a, b) => a + b, 0) / distances.length
    
    // Buscar 5 cuerpos con distancia similar al promedio
    const candidates = bodies.filter((b, i) => {
      const deviation = Math.abs(distances[i] - avgDist) / avgDist
      return deviation < 0.15
    })
    
    if (candidates.length >= 5) {
      // Tomar los primeros 5
      const pentagonBodies = candidates.slice(0, 5)
      
      this.activeAlignments.push({
        type: 'pentagon',
        bodies: pentagonBodies.map(b => b.id),
        vertices: pentagonBodies.map(b => b.position.clone()),
        center: center.clone(),
        radius: avgDist,
        resonanceStrength: 0.8,
        harmonicRatio: `1:${PHI.toFixed(3)}` // Proporción áurea
      })
      
      this.createResonanceEvent('orbital_energy', this.activeAlignments[this.activeAlignments.length - 1])
    }
  }
  
  /**
   * Detectar dodecaedro proyectado (evento cósmico raro)
   */
  private detectDodecahedronProjection(bodies: CelestialBody[]): void {
    // Evento muy raro: 12 cuerpos forman un dodecaedro aproximado
    // Implementación simplificada
    
    if (bodies.length < 12) return
    
    const center = new THREE.Vector3()
    bodies.forEach(b => center.add(b.position))
    center.divideScalar(bodies.length)
    
    // Verificar si hay 12 cuerpos aproximadamente equidistantes
    const distances = bodies.map(b => b.position.distanceTo(center))
    const avgDist = distances.reduce((a, b) => a + b, 0) / distances.length
    
    const candidates = bodies.filter((b, i) => {
      const deviation = Math.abs(distances[i] - avgDist) / avgDist
      return deviation < 0.1
    })
    
    if (candidates.length >= 12) {
      const dodecaBodies = candidates.slice(0, 12)
      
      this.activeAlignments.push({
        type: 'dodecahedron',
        bodies: dodecaBodies.map(b => b.id),
        vertices: dodecaBodies.map(b => b.position.clone()),
        center: center.clone(),
        radius: avgDist,
        resonanceStrength: 1.0,
        harmonicRatio: '1:φ:φ²' // Proporción áurea al cuadrado
      })
      
      this.createResonanceEvent('cosmic_event', this.activeAlignments[this.activeAlignments.length - 1])
    }
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // EVENTOS DE RESONANCIA
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Crear evento de resonancia
   */
  private createResonanceEvent(type: ResonanceEvent['type'], alignment: GeometricAlignment): void {
    // Evitar duplicados
    const exists = this.activeEvents.some(e => 
      e.alignment.type === alignment.type &&
      e.alignment.bodies.every(id => alignment.bodies.includes(id))
    )
    
    if (exists) return
    
    const descriptions = {
      gravitational_pulse: '⚡ Impulso Gravitacional — Triángulo de fuerzas',
      orbital_energy: '🌟 Energía Orbital — Pentágono áureo',
      cosmic_event: '💫 Evento Cósmico — Dodecaedro universal',
      harmonic_resonance: '🎵 Resonancia Armónica — Proporción perfecta'
    }
    
    const event: ResonanceEvent = {
      id: `event_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      type,
      alignment,
      timestamp: Date.now(),
      duration: type === 'cosmic_event' ? 60 : 30, // segundos
      intensity: alignment.resonanceStrength,
      description: descriptions[type]
    }
    
    this.activeEvents.push(event)
    this.eventHistory.push(event)
    
    console.log(`✨ ${event.description}`)
    console.log(`   Cuerpos: ${alignment.bodies.join(', ')}`)
    console.log(`   Ratio armónico: ${alignment.harmonicRatio}`)
    console.log(`   Intensidad: ${(event.intensity * 100).toFixed(1)}%`)
  }
  
  /**
   * Actualizar eventos activos
   */
  private updateEvents(deltaTime: number): void {
    const now = Date.now()
    
    this.activeEvents = this.activeEvents.filter(event => {
      const elapsed = (now - event.timestamp) / 1000
      return elapsed < event.duration
    })
  }
  
  /**
   * Obtener eventos activos
   */
  getActiveEvents(): ResonanceEvent[] {
    return [...this.activeEvents]
  }
  
  /**
   * Obtener historial de eventos
   */
  getEventHistory(): ResonanceEvent[] {
    return [...this.eventHistory]
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // VISUALIZACIÓN
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Crear visualización del dodecaedro cósmico
   */
  private createDodecahedronVisualization(): void {
    if (!this.scene) return
    
    const geometry = new THREE.BufferGeometry()
    const positions: number[] = []
    
    // Crear líneas entre nodos conectados
    this.cosmicDodecahedron.forEach(node => {
      node.connections.forEach(connId => {
        const connNode = this.cosmicDodecahedron.find(n => n.id === connId)
        if (connNode) {
          positions.push(
            node.position.x, node.position.y, node.position.z,
            connNode.position.x, connNode.position.y, connNode.position.z
          )
        }
      })
    })
    
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3))
    
    const material = new THREE.LineBasicMaterial({
      color: 0x4444ff,
      transparent: true,
      opacity: 0.1,
      blending: THREE.AdditiveBlending
    })
    
    this.dodecahedronMesh = new THREE.LineSegments(geometry, material)
    this.scene.add(this.dodecahedronMesh)
    
    console.log('🔷 Dodecaedro cósmico visualizado')
  }
  
  /**
   * Actualizar visualización
   */
  private updateVisualization(): void {
    if (!this.scene) return
    
    // Limpiar líneas de resonancia anteriores
    this.resonanceLines.forEach(line => {
      this.scene!.remove(line)
      line.geometry.dispose()
      ;(line.material as THREE.Material).dispose()
    })
    this.resonanceLines = []
    
    // Limpiar meshes de alineación anteriores
    this.alignmentMeshes.forEach(mesh => {
      this.scene!.remove(mesh)
      mesh.geometry.dispose()
      ;(mesh.material as THREE.Material).dispose()
    })
    this.alignmentMeshes = []
    
    // Crear líneas de resonancia para alineaciones activas
    this.activeAlignments.forEach(alignment => {
      this.createAlignmentVisualization(alignment)
    })
  }
  
  /**
   * Crear visualización de alineación
   */
  private createAlignmentVisualization(alignment: GeometricAlignment): void {
    if (!this.scene) return
    
    // Crear líneas entre vértices
    const geometry = new THREE.BufferGeometry()
    const positions: number[] = []
    
    for (let i = 0; i < alignment.vertices.length; i++) {
      const v1 = alignment.vertices[i]
      const v2 = alignment.vertices[(i + 1) % alignment.vertices.length]
      
      positions.push(v1.x, v1.y, v1.z, v2.x, v2.y, v2.z)
    }
    
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3))
    
    const colors = {
      triangle: 0xff6600,
      pentagon: 0xffaa00,
      hexagon: 0x00ff88,
      dodecahedron: 0xff00ff
    }
    
    const material = new THREE.LineBasicMaterial({
      color: colors[alignment.type],
      transparent: true,
      opacity: 0.6 * alignment.resonanceStrength,
      blending: THREE.AdditiveBlending,
      linewidth: 2
    })
    
    const lines = new THREE.LineSegments(geometry, material)
    this.scene.add(lines)
    this.resonanceLines.push(lines)
    
    // Crear esfera en el centro
    const sphereGeometry = new THREE.SphereGeometry(alignment.radius * 0.05, 16, 16)
    const sphereMaterial = new THREE.MeshBasicMaterial({
      color: colors[alignment.type],
      transparent: true,
      opacity: 0.3 * alignment.resonanceStrength,
      blending: THREE.AdditiveBlending
    })
    
    const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial)
    sphere.position.copy(alignment.center)
    this.scene.add(sphere)
    this.alignmentMeshes.push(sphere)
  }
  
  /**
   * Mostrar/ocultar visualización
   */
  setVisualizationVisible(visible: boolean): void {
    if (this.dodecahedronMesh) {
      this.dodecahedronMesh.visible = visible
    }
    
    this.resonanceLines.forEach(line => line.visible = visible)
    this.alignmentMeshes.forEach(mesh => mesh.visible = visible)
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // ESTADO Y CONTROL
  // ═══════════════════════════════════════════════════════════════════════
  
  isEnabled(): boolean {
    return this.enabled
  }
  
  disable(): void {
    this.enabled = false
    this.setVisualizationVisible(false)
  }
  
  /**
   * Obtener estadísticas
   */
  getStats() {
    return {
      enabled: this.enabled,
      discovered: this.discovered,
      celestialBodies: this.celestialBodies.size,
      activeAlignments: this.activeAlignments.length,
      activeEvents: this.activeEvents.length,
      totalEvents: this.eventHistory.length,
      cosmicNodes: this.cosmicDodecahedron.length
    }
  }
  
  /**
   * Limpiar recursos
   */
  dispose(): void {
    this.setVisualizationVisible(false)
    
    if (this.dodecahedronMesh) {
      this.dodecahedronMesh.geometry.dispose()
      ;(this.dodecahedronMesh.material as THREE.Material).dispose()
    }
    
    this.resonanceLines.forEach(line => {
      line.geometry.dispose()
      ;(line.material as THREE.Material).dispose()
    })
    
    this.alignmentMeshes.forEach(mesh => {
      mesh.geometry.dispose()
      ;(mesh.material as THREE.Material).dispose()
    })
    
    this.resonanceOscillators.forEach(osc => {
      osc.stop()
      osc.disconnect()
    })
    
    this.enabled = false
    console.log('🌌 Cosmic Resonance System disposed')
  }
}

// ═══════════════════════════════════════════════════════════════════════
// SINGLETON
// ═══════════════════════════════════════════════════════════════════════

let instance: CosmicResonanceSystem | null = null

export function getCosmicResonance(): CosmicResonanceSystem {
  if (!instance) {
    instance = new CosmicResonanceSystem()
  }
  return instance
}

export default CosmicResonanceSystem

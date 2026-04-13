/**
 * 🔷 Sacred Geometry System
 * 
 * BASE CONCEPTUAL: SÓLIDOS PLATÓNICOS
 * ─────────────────────────────────────
 * Los 5 sólidos platónicos son las formas primordiales del universo.
 * Toda geometría sagrada deriva de ellos.
 * 
 * ┌─────────────────┬──────────────┬──────────────────────────────────────┐
 * │ Sólido          │ Elemento     │ Principio                            │
 * ├─────────────────┼──────────────┼──────────────────────────────────────┤
 * │ Tetraedro       │ Fuego        │ 4 caras — transformación, voluntad   │
 * │ Hexaedro (Cubo) │ Tierra       │ 6 caras — estabilidad, materia       │
 * │ Octaedro        │ Aire         │ 8 caras — equilibrio, pensamiento    │
 * │ Dodecaedro      │ Éter/Prana   │ 12 caras — cosmos, conciencia        │
 * │ Icosaedro       │ Agua         │ 20 caras — fluidez, emoción          │
 * │ Esfera          │ Vacío/Void   │ ∞ caras — origen, totalidad          │
 * └─────────────────┴──────────────┴──────────────────────────────────────┘
 * 
 * JERARQUÍA GENERATIVA:
 * Esfera → contiene todos los sólidos
 * Dodecaedro → genera el icosaedro (duales)
 * Cubo → genera el octaedro (duales)
 * Tetraedro → es dual de sí mismo
 * 
 * CONEXIÓN CON LAS NAVES:
 * - Phantom (Cloaking)  → Icosaedro  (Agua — fluidez, invisibilidad)
 * - Aegis (Defensa)     → Cubo       (Tierra — solidez, protección)
 * - Vector (Velocidad)  → Tetraedro  (Fuego — impulso, transformación)
 * - Oracle (Ciencia)    → Dodecaedro (Éter — conocimiento, cosmos)
 * - Titan (Fuerza)      → Octaedro   (Aire — equilibrio de fuerzas)
 * 
 * CONEXIÓN CON LOS SITIOS:
 * - Puma Punku    → Cubo/Hexaedro  (bloques H, geometría modular)
 * - Giza          → Tetraedro      (pirámide = tetraedro truncado)
 * - Teotihuacán   → Octaedro       (pirámide del sol, equilibrio)
 * - Veracruz      → Icosaedro      (agua, serpiente, fluidez)
 * - Isla de Pascua→ Dodecaedro     (éter, red energética planetaria)
 * - Göbekli Tepe  → Esfera/Void    (origen, el primer templo)
 * 
 * Genera patrones de geometría sagrada procedurales basados en:
 * - Semilla del sitio (coordenadas + nombre)
 * - Tipo de nave utilizada
 * - Misión completada
 * - Bioma/planeta
 * 
 * ESTADO: DESACTIVADO — listo para activar cuando se integre al gameplay.
 * 
 * Familias matemáticas (derivadas de los sólidos platónicos):
 * - Roseta:    r = cos(kθ)            → Dodecaedro (5 pétalos = pentágono)
 * - Espiral:   r = a + bθ             → Tetraedro  (expansión desde el fuego)
 * - Toroide:   círculos concéntricos  → Icosaedro  (agua, flujo circular)
 * - Lissajous: x=sin(at+δ), y=sin(bt) → Cubo       (resonancia ortogonal)
 * - Polígono:  θ = 2π/n               → Octaedro   (simetría de 8)
 * - Hilbert:   curva fractal           → Esfera     (infinito contenido)
 * 
 * Conexión nave → geometría → sólido platónico:
 * - Cloaking  → Lissajous → Cubo       (resonancia, campo EM)
 * - Defensa   → Toroide   → Icosaedro  (agua, protección fluida)
 * - Velocidad → Espiral   → Tetraedro  (fuego, impulso)
 * - Ciencia   → Hilbert   → Dodecaedro (éter, conocimiento fractal)
 * - Fuerza    → Polígono  → Octaedro   (aire, equilibrio de fuerzas)
 */

// ─── SÓLIDOS PLATÓNICOS — BASE GENERATIVA ────────────────────────────────────

export type PlatonicSolid = 'tetrahedron' | 'hexahedron' | 'octahedron' | 'dodecahedron' | 'icosahedron' | 'sphere'

export interface PlatonicSolidData {
  name: string
  element: string
  faces: number
  vertices: number
  edges: number
  dualSolid: PlatonicSolid
  siteId: string        // sitio arqueológico asociado
  shipType: string      // nave asociada
  frequency: number     // frecuencia de resonancia (Hz)
  color: string         // color energético
  meaning: string
}

export const PLATONIC_SOLIDS: Record<PlatonicSolid, PlatonicSolidData> = {
  tetrahedron: {
    name: 'Tetraedro', element: 'Fuego',
    faces: 4, vertices: 4, edges: 6,
    dualSolid: 'tetrahedron', // autodual
    siteId: 'giza', shipType: 'speed',
    frequency: 396, // Hz — liberación, transformación
    color: '#ff6600',
    meaning: 'Transformación primordial. El fuego que convierte la materia en energía.'
  },
  hexahedron: {
    name: 'Hexaedro (Cubo)', element: 'Tierra',
    faces: 6, vertices: 8, edges: 12,
    dualSolid: 'octahedron',
    siteId: 'pumaPunku', shipType: 'defense',
    frequency: 432, // Hz — frecuencia sagrada de la Tierra
    color: '#88aa44',
    meaning: 'Estabilidad absoluta. La matriz de la materia física.'
  },
  octahedron: {
    name: 'Octaedro', element: 'Aire',
    faces: 8, vertices: 6, edges: 12,
    dualSolid: 'hexahedron',
    siteId: 'teotihuacan', shipType: 'force',
    frequency: 528, // Hz — reparación, equilibrio
    color: '#44aaff',
    meaning: 'Equilibrio perfecto. El pensamiento que ordena el caos.'
  },
  dodecahedron: {
    name: 'Dodecaedro', element: 'Éter/Prana',
    faces: 12, vertices: 20, edges: 30,
    dualSolid: 'icosahedron',
    siteId: 'easterIsland', shipType: 'science',
    frequency: 639, // Hz — conexión, conciencia cósmica
    color: '#aa44ff',
    meaning: 'El cosmos mismo. Doce pentágonos que mapean el universo.'
  },
  icosahedron: {
    name: 'Icosaedro', element: 'Agua',
    faces: 20, vertices: 12, edges: 30,
    dualSolid: 'dodecahedron',
    siteId: 'veracruz', shipType: 'cloaking',
    frequency: 741, // Hz — intuición, fluidez
    color: '#4488ff',
    meaning: 'Fluidez universal. El agua que toma la forma de todo recipiente.'
  },
  sphere: {
    name: 'Esfera', element: 'Vacío/Void',
    faces: Infinity, vertices: Infinity, edges: Infinity,
    dualSolid: 'sphere', // autodual
    siteId: 'gobekliTepe', shipType: 'default',
    frequency: 852, // Hz — intuición espiritual, origen
    color: '#ffffff',
    meaning: 'El origen de todo. Contiene todos los sólidos en potencia.'
  }
}

/** Obtener el sólido platónico asociado a un sitio */
export function getSolidForSite(siteId: string): PlatonicSolidData {
  const entry = Object.values(PLATONIC_SOLIDS).find(s => s.siteId === siteId)
  return entry || PLATONIC_SOLIDS.sphere
}

/** Obtener el sólido platónico asociado a una nave */
export function getSolidForShip(shipType: string): PlatonicSolidData {
  const entry = Object.values(PLATONIC_SOLIDS).find(s => s.shipType === shipType)
  return entry || PLATONIC_SOLIDS.sphere
}

/** Generar vértices de un sólido platónico escalado */
export function getPlatonicVertices(solid: PlatonicSolid, radius: number = 1): [number, number, number][] {
  const r = radius
  const phi = (1 + Math.sqrt(5)) / 2 // proporción áurea

  switch (solid) {
    case 'tetrahedron':
      return [
        [1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]
      ].map(([x, y, z]) => [x * r / Math.sqrt(3), y * r / Math.sqrt(3), z * r / Math.sqrt(3)])

    case 'hexahedron':
      return [
        [1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1],
        [-1,1,1],[-1,1,-1],[-1,-1,1],[-1,-1,-1]
      ].map(([x, y, z]) => [x * r / Math.sqrt(3), y * r / Math.sqrt(3), z * r / Math.sqrt(3)])

    case 'octahedron':
      return [[r,0,0],[-r,0,0],[0,r,0],[0,-r,0],[0,0,r],[0,0,-r]]

    case 'dodecahedron': {
      const verts: [number, number, number][] = []
      const s = r / Math.sqrt(3)
      // 8 vértices del cubo
      for (const x of [-1,1]) for (const y of [-1,1]) for (const z of [-1,1]) verts.push([x*s, y*s, z*s])
      // 12 vértices de los rectángulos áureos
      const t = phi * s
      for (const a of [-1,1]) for (const b of [-1,1]) {
        verts.push([0, a*s, b*t])
        verts.push([a*s, b*t, 0])
        verts.push([b*t, 0, a*s])
      }
      return verts
    }

    case 'icosahedron': {
      const verts: [number, number, number][] = []
      const n = r / Math.sqrt(1 + phi * phi)
      const m = phi * n
      for (const a of [-1,1]) for (const b of [-1,1]) {
        verts.push([0, a*n, b*m])
        verts.push([a*n, b*m, 0])
        verts.push([b*m, 0, a*n])
      }
      return verts
    }

    case 'sphere':
    default: {
      // 12 puntos distribuidos en la esfera (icosaedro inscrito)
      return getPlatonicVertices('icosahedron', radius)
    }
  }
}

// ─── TIPOS ────────────────────────────────────────────────────────────────────

export type PatternFamily = 'rosette' | 'spiral' | 'toroid' | 'lissajous' | 'polygon' | 'hilbert'

export type ShipType = 'cloaking' | 'defense' | 'speed' | 'science' | 'force' | 'default'

export interface PatternSeed {
  siteId: string
  siteLat: number
  siteLon: number
  missionId: string
  shipType: ShipType
  difficulty?: number
}

export interface SacredPattern {
  id: string
  family: PatternFamily
  points: number[]       // [x, y, z, x, y, z, ...] pares de segmentos
  seed: number
  params: PatternParams
  meaning: string
  discoveredAt: string   // ISO date
  siteId: string
  missionId: string
  shipType: ShipType
}

interface PatternParams {
  circles?: number
  radius?: number
  arms?: number
  turns?: number
  petals?: number
  freqA?: number
  freqB?: number
  delta?: number
  sides?: number
  depth?: number
}

// ─── CODEX (persistencia) ─────────────────────────────────────────────────────

const CODEX_KEY = 'sacred_geometry_codex'

export function loadCodex(): SacredPattern[] {
  if (typeof window === 'undefined') return []
  try {
    const raw = localStorage.getItem(CODEX_KEY)
    return raw ? JSON.parse(raw) : []
  } catch { return [] }
}

export function saveToCodex(pattern: SacredPattern): void {
  if (typeof window === 'undefined') return
  const codex = loadCodex()
  if (codex.some(p => p.id === pattern.id)) return // ya existe
  codex.push(pattern)
  localStorage.setItem(CODEX_KEY, JSON.stringify(codex))
}

export function getCodexCount(): number {
  return loadCodex().length
}

export function resetCodex(): void {
  if (typeof window !== 'undefined') localStorage.removeItem(CODEX_KEY)
}

// ─── GENERADOR DE SEMILLA ─────────────────────────────────────────────────────

function hashSeed(input: PatternSeed): number {
  const str = `${input.siteId}_${input.siteLat.toFixed(4)}_${input.siteLon.toFixed(4)}_${input.missionId}_${input.shipType}_${input.difficulty || 1}`
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash + str.charCodeAt(i)) | 0
  }
  return Math.abs(hash)
}

// PRNG determinista basado en semilla
function seededRandom(seed: number): () => number {
  let s = seed
  return () => {
    s = (s * 16807 + 0) % 2147483647
    return (s - 1) / 2147483646
  }
}

// ─── MAPEO NAVE → FAMILIA ─────────────────────────────────────────────────────

const SHIP_FAMILY_MAP: Record<ShipType, PatternFamily> = {
  cloaking: 'lissajous',
  defense:  'toroid',
  speed:    'spiral',
  science:  'hilbert',
  force:    'polygon',
  default:  'rosette'
}

const FAMILY_MEANING: Record<PatternFamily, string> = {
  rosette:   'Armonía — Resonancia floral del cosmos',
  spiral:    'Evolución — Movimiento perpetuo de la galaxia',
  toroid:    'Energía — Campo electromagnético primordial',
  lissajous: 'Resonancia — Vibración entre dimensiones',
  polygon:   'Estructura — Mandala estelar del universo',
  hilbert:   'Análisis — Fractal de conocimiento infinito'
}

// ─── GENERADORES DE PATRONES ──────────────────────────────────────────────────

const Y = 0.02 // altura sobre el suelo
const SEG = 96

function addCircle(pts: number[], cx: number, cz: number, r: number) {
  for (let j = 0; j < SEG; j++) {
    const a0 = (j / SEG) * Math.PI * 2
    const a1 = ((j + 1) / SEG) * Math.PI * 2
    pts.push(cx + Math.cos(a0) * r, Y, cz + Math.sin(a0) * r)
    pts.push(cx + Math.cos(a1) * r, Y, cz + Math.sin(a1) * r)
  }
}

function addLine(pts: number[], x0: number, z0: number, x1: number, z1: number) {
  pts.push(x0, Y, z0, x1, Y, z1)
}

// 🌸 Roseta: r = cos(kθ)
function generateRosette(rand: () => number): { points: number[], params: PatternParams } {
  const pts: number[] = []
  const petals = 4 + Math.floor(rand() * 12)  // 4-15 pétalos
  const R = 4 + rand() * 4
  const circles = 12 + Math.floor(rand() * 20)

  for (let i = 0; i < circles; i++) {
    const angle = (i / circles) * Math.PI * 2
    const cx = Math.cos(angle) * R
    const cz = Math.sin(angle) * R
    addCircle(pts, cx, cz, R * (0.5 + rand() * 0.5))
  }

  // Pétalos polares
  const steps = 300
  for (let j = 0; j < steps; j++) {
    const t0 = (j / steps) * Math.PI * 2
    const t1 = ((j + 1) / steps) * Math.PI * 2
    const r0 = R * Math.cos(petals * t0)
    const r1 = R * Math.cos(petals * t1)
    pts.push(Math.cos(t0) * r0, Y, Math.sin(t0) * r0)
    pts.push(Math.cos(t1) * r1, Y, Math.sin(t1) * r1)
  }

  addCircle(pts, 0, 0, R * 1.2)
  return { points: pts, params: { petals, radius: R, circles } }
}

// 🌀 Espiral: r = a + bθ
function generateSpiral(rand: () => number): { points: number[], params: PatternParams } {
  const pts: number[] = []
  const arms = 2 + Math.floor(rand() * 4)     // 2-5 brazos
  const turns = 2 + rand() * 3                 // 2-5 vueltas
  const maxR = 5 + rand() * 4
  const steps = 250

  for (let arm = 0; arm < arms; arm++) {
    const offset = (arm / arms) * Math.PI * 2
    for (let j = 0; j < steps; j++) {
      const t0 = j / steps, t1 = (j + 1) / steps
      const a0 = offset + t0 * turns * Math.PI * 2
      const a1 = offset + t1 * turns * Math.PI * 2
      const r0 = t0 * maxR, r1 = t1 * maxR
      pts.push(Math.cos(a0) * r0, Y, Math.sin(a0) * r0)
      pts.push(Math.cos(a1) * r1, Y, Math.sin(a1) * r1)
    }
  }

  addCircle(pts, 0, 0, maxR)
  addCircle(pts, 0, 0, maxR * 0.15)
  return { points: pts, params: { arms, turns, radius: maxR } }
}

// 🌐 Toroide: anillos concéntricos + roseta
function generateToroid(rand: () => number): { points: number[], params: PatternParams } {
  const pts: number[] = []
  const rings = 4 + Math.floor(rand() * 5)    // 4-8 anillos
  const N = 16 + Math.floor(rand() * 16)      // 16-31 círculos en roseta
  const ringR = 4 + rand() * 3
  const circR = ringR * (0.6 + rand() * 0.4)

  // Roseta
  for (let i = 0; i < N; i++) {
    const angle = (i / N) * Math.PI * 2
    addCircle(pts, Math.cos(angle) * ringR, Math.sin(angle) * ringR, circR)
  }

  // Anillos concéntricos
  for (let i = 1; i <= rings; i++) {
    addCircle(pts, 0, 0, (i / rings) * (ringR + circR))
  }

  return { points: pts, params: { circles: N, radius: ringR } }
}

// ✨ Lissajous: x = sin(at + δ), z = sin(bt)
function generateLissajous(rand: () => number): { points: number[], params: PatternParams } {
  const pts: number[] = []
  const freqA = 1 + Math.floor(rand() * 7)    // 1-7
  const freqB = 1 + Math.floor(rand() * 7)    // 1-7
  const delta = rand() * Math.PI
  const R = 5 + rand() * 3
  const steps = 500

  for (let j = 0; j < steps; j++) {
    const t0 = (j / steps) * Math.PI * 2
    const t1 = ((j + 1) / steps) * Math.PI * 2
    pts.push(
      Math.sin(freqA * t0 + delta) * R, Y, Math.sin(freqB * t0) * R,
      Math.sin(freqA * t1 + delta) * R, Y, Math.sin(freqB * t1) * R
    )
  }

  // Marco circular
  addCircle(pts, 0, 0, R * 1.1)
  return { points: pts, params: { freqA, freqB, delta, radius: R } }
}

// 🔷 Polígono estelar: θ = 2π/n con saltos
function generatePolygon(rand: () => number): { points: number[], params: PatternParams } {
  const pts: number[] = []
  const sides = 5 + Math.floor(rand() * 8)    // 5-12 lados
  const layers = 2 + Math.floor(rand() * 3)   // 2-4 capas
  const R = 5 + rand() * 3

  for (let layer = 1; layer <= layers; layer++) {
    const r = (layer / layers) * R
    const skip = layer % 2 === 0 ? 2 : 1      // estrella vs polígono

    for (let i = 0; i < sides; i++) {
      const a0 = (i / sides) * Math.PI * 2
      const a1 = (((i + skip) % sides) / sides) * Math.PI * 2
      addLine(pts, Math.cos(a0) * r, Math.sin(a0) * r, Math.cos(a1) * r, Math.sin(a1) * r)
    }

    // Rayos al centro
    for (let i = 0; i < sides; i++) {
      const a = (i / sides) * Math.PI * 2
      addLine(pts, 0, 0, Math.cos(a) * r, Math.sin(a) * r)
    }
  }

  addCircle(pts, 0, 0, R)
  return { points: pts, params: { sides, radius: R } }
}

// 🧬 Hilbert: curva fractal de espacio
function generateHilbert(rand: () => number): { points: number[], params: PatternParams } {
  const pts: number[] = []
  const depth = 3 + Math.floor(rand() * 2)    // 3-4 niveles
  const size = 6 + rand() * 3

  // Generar puntos de curva de Hilbert 2D
  const hilbertPoints: [number, number][] = []
  function hilbert(x: number, y: number, ax: number, ay: number, bx: number, by: number, level: number) {
    if (level <= 0) {
      hilbertPoints.push([x + (ax + bx) / 2, y + (ay + by) / 2])
      return
    }
    hilbert(x, y, bx / 2, by / 2, ax / 2, ay / 2, level - 1)
    hilbert(x + ax / 2, y + ay / 2, ax / 2, ay / 2, bx / 2, by / 2, level - 1)
    hilbert(x + ax / 2 + bx / 2, y + ay / 2 + by / 2, ax / 2, ay / 2, bx / 2, by / 2, level - 1)
    hilbert(x + ax / 2 + bx, y + ay / 2 + by, -bx / 2, -by / 2, -ax / 2, -ay / 2, level - 1)
  }

  hilbert(0, 0, size, 0, 0, size, depth)

  // Centrar
  const cx = size / 2, cz = size / 2
  for (let i = 0; i < hilbertPoints.length - 1; i++) {
    pts.push(hilbertPoints[i][0] - cx, Y, hilbertPoints[i][1] - cz)
    pts.push(hilbertPoints[i + 1][0] - cx, Y, hilbertPoints[i + 1][1] - cz)
  }

  addCircle(pts, 0, 0, size * 0.6)
  return { points: pts, params: { depth, radius: size } }
}

// ─── GENERADOR PRINCIPAL ──────────────────────────────────────────────────────

const GENERATORS: Record<PatternFamily, (rand: () => number) => { points: number[], params: PatternParams }> = {
  rosette:   generateRosette,
  spiral:    generateSpiral,
  toroid:    generateToroid,
  lissajous: generateLissajous,
  polygon:   generatePolygon,
  hilbert:   generateHilbert
}

export function generateSacredPattern(input: PatternSeed): SacredPattern {
  const seed = hashSeed(input)
  const rand = seededRandom(seed)
  const family = SHIP_FAMILY_MAP[input.shipType] || 'rosette'
  const { points, params } = GENERATORS[family](rand)
  const id = `sacred_${input.siteId}_${input.missionId}_${seed}`

  return {
    id,
    family,
    points,
    seed,
    params,
    meaning: FAMILY_MEANING[family],
    discoveredAt: new Date().toISOString(),
    siteId: input.siteId,
    missionId: input.missionId,
    shipType: input.shipType
  }
}

// ─── SISTEMA GLOBAL (singleton) ───────────────────────────────────────────────

class SacredGeometryEngine {
  private enabled = false

  enable()  { this.enabled = true }
  disable() { this.enabled = false }
  isEnabled() { return this.enabled }

  generate(input: PatternSeed): SacredPattern | null {
    if (!this.enabled) return null
    const pattern = generateSacredPattern(input)
    saveToCodex(pattern)
    return pattern
  }

  getCodex() { return loadCodex() }
  getCount() { return getCodexCount() }
  reset()    { resetCodex() }
}

let instance: SacredGeometryEngine | null = null

export function getSacredGeometry(): SacredGeometryEngine {
  if (!instance) instance = new SacredGeometryEngine()
  return instance
}

// ─── HELPERS ──────────────────────────────────────────────────────────────────

/** Convierte número de UFO (1-5) a ShipType */
export function ufoNumberToShipType(ufoNumber: number): ShipType {
  const map: Record<number, ShipType> = {
    1: 'cloaking',  // Phantom
    2: 'defense',   // Aegis
    3: 'speed',     // Vector
    4: 'science',   // Oracle
    5: 'force'      // Titan
  }
  return map[ufoNumber] || 'default'
}

/** Coordenadas de cada sitio arqueológico */
const SITE_COORDS: Record<string, { lat: number, lon: number }> = {
  pumaPunku:    { lat: -16.5596, lon: -68.6788 },
  giza:        { lat: 29.9792,  lon: 31.1342 },
  teotihuacan: { lat: 19.6925,  lon: -98.8438 },
  veracruz:    { lat: 18.4667,  lon: -95.4500 },
  easterIsland:{ lat: -27.1254, lon: -109.2778 }
}

/** Genera un patrón sagrado al completar una misión (si el sistema está activo) */
export function onMissionComplete(siteId: string, missionId: string, ufoNumber: number): SacredPattern | null {
  const engine = getSacredGeometry()
  const coords = SITE_COORDS[siteId] || { lat: 0, lon: 0 }
  return engine.generate({
    siteId,
    siteLat: coords.lat,
    siteLon: coords.lon,
    missionId,
    shipType: ufoNumberToShipType(ufoNumber)
  })
}

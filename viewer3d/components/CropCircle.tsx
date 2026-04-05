'use client'

import { useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

type CropPattern = 'flowerOfLife' | 'metatronCube' | 'spiral' | 'toroid' | 'fractalJulia' |
                   'flower' | 'metatron' | 'julia' |
                   'pyramidStar' | 'hBlock' | 'serpentSpiral' | 'solarMandala' | 'nodeNetwork' |
                   'lissajous' | 'hilbert' | 'polygon'

interface CropCircleProps {
  pattern?: CropPattern
  type?: CropPattern
  position?: [number, number, number]
  scale?: number
  visible?: boolean
}

const COLOR = new THREE.Color(0x3a4a35)
const SEG = 96
const LINE_WIDTH = 0.08

function buildRibbonGeo(points: number[], width: number): THREE.BufferGeometry {
  const positions: number[] = []
  const indices: number[] = []
  const half = width / 2
  let vi = 0
  for (let i = 0; i < points.length; i += 6) {
    const ax = points[i],   ay = points[i+1], az = points[i+2]
    const bx = points[i+3], by = points[i+4], bz = points[i+5]
    const dx = bx - ax, dz = bz - az
    const len = Math.sqrt(dx*dx + dz*dz)
    if (len < 0.0001) continue
    const nx = -dz / len * half, nz = dx / len * half
    positions.push(ax+nx, ay, az+nz,  ax-nx, ay, az-nz,
                   bx+nx, by, bz+nz,  bx-nx, by, bz-nz)
    indices.push(vi, vi+1, vi+2,  vi+1, vi+3, vi+2)
    vi += 4
  }
  const geo = new THREE.BufferGeometry()
  geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3))
  geo.setIndex(indices)
  return geo
}

function CropLines({ points }: { points: number[] }) {
  const matRef = useRef<THREE.MeshBasicMaterial>(null)
  const opacityRef = useRef(0)

  useFrame((_, delta) => {
    if (!matRef.current) return
    if (opacityRef.current < 0.9) {
      opacityRef.current = Math.min(0.9, opacityRef.current + delta * 0.4)
      matRef.current.opacity = opacityRef.current
    }
  })

  const geo = useMemo(() => buildRibbonGeo(points, LINE_WIDTH), [points])

  return (
    <mesh geometry={geo}>
      <meshBasicMaterial ref={matRef} color={COLOR} transparent opacity={0} depthWrite={false} side={THREE.DoubleSide} />
    </mesh>
  )
}

// Luz tenue que pulsa suavemente
function GlowLight({ color }: { color: string }) {
  const lightRef = useRef<THREE.PointLight>(null)
  useFrame(({ clock }) => {
    if (lightRef.current) {
      lightRef.current.intensity = 0.3 + Math.sin(clock.elapsedTime * 1.5) * 0.1
    }
  })
  return <pointLight ref={lightRef} color={color} intensity={0.3} distance={20} position={[0, 2, 0]} />
}

function addCircle(pts: number[], cx: number, cz: number, r: number, y = 0.02) {
  for (let j = 0; j < SEG; j++) {
    const a0 = (j / SEG) * Math.PI * 2
    const a1 = ((j + 1) / SEG) * Math.PI * 2
    pts.push(cx + Math.cos(a0) * r, y, cz + Math.sin(a0) * r)
    pts.push(cx + Math.cos(a1) * r, y, cz + Math.sin(a1) * r)
  }
}

function addLine(pts: number[], x0: number, z0: number, x1: number, z1: number, y = 0.02) {
  pts.push(x0, y, z0, x1, y, z1)
}

export default function CropCircle({ pattern, type, position = [0, 0.02, 0], scale = 1.5, visible = false }: CropCircleProps) {
  if (!visible) return null
  const p = pattern || type || 'solarMandala'

  return (
    <group position={position} scale={scale}>
      {p === 'lissajous'                          && <Lissajous />}
      {p === 'toroid'                             && <Toroid />}
      {(p === 'spiral' || p === 'serpentSpiral')  && <SerpentSpiral />}
      {p === 'hilbert'                            && <Hilbert />}
      {(p === 'polygon' || p === 'pyramidStar')   && <PolygonStar />}
      {p === 'solarMandala'                       && <SolarMandala />}
      {(p === 'hBlock' || p === 'metatronCube' || p === 'metatron') && <HBlockGrid />}
      {(p === 'nodeNetwork' || p === 'flowerOfLife' || p === 'flower') && <NodeNetwork />}
      {(p === 'fractalJulia' || p === 'julia')    && <Lissajous />}
    </group>
  )
}

// ─── GIZA: Estrella Piramidal ─────────────────────────────────────────────────
// Triángulos radiales + estrella de 6 puntas + proporción áurea
function PyramidStar() {
  const points = useMemo(() => {
    const pts: number[] = []
    const PHI = 1.618
    const R = 6
    const r = R / PHI

    // Estrella de 6 puntas (2 triángulos superpuestos)
    for (let t = 0; t < 2; t++) {
      const offset = t * (Math.PI / 3)
      const verts: [number, number][] = []
      for (let i = 0; i < 3; i++) {
        const a = offset + (i / 3) * Math.PI * 2
        verts.push([Math.cos(a) * R, Math.sin(a) * R])
      }
      // Triángulo exterior
      for (let i = 0; i < 3; i++) {
        const [x0, z0] = verts[i]
        const [x1, z1] = verts[(i + 1) % 3]
        addLine(pts, x0, z0, x1, z1)
      }
    }

    // Anillos concéntricos (proporción áurea)
    addCircle(pts, 0, 0, R)
    addCircle(pts, 0, 0, r)
    addCircle(pts, 0, 0, r / PHI)

    // Rayos desde el centro a cada punta
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * Math.PI * 2
      addLine(pts, 0, 0, Math.cos(a) * R, Math.sin(a) * R)
    }

    // Hexágono interior
    for (let i = 0; i < 6; i++) {
      const a0 = (i / 6) * Math.PI * 2
      const a1 = ((i + 1) / 6) * Math.PI * 2
      addLine(pts, Math.cos(a0) * r, Math.sin(a0) * r, Math.cos(a1) * r, Math.sin(a1) * r)
    }

    return pts
  }, [])
  return (
    <>
      <CropLines points={points} />
      <GlowLight color="#ffd700" />
    </>
  )
}

// ─── PUMA PUNKU: Grid Modular H-Blocks ───────────────────────────────────────
function HBlockGrid() {
  const points = useMemo(() => {
    const pts: number[] = []
    const W = 2.5, H = 1.5, gap = 0.6
    const cols = 3, rows = 3

    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        const cx = (col - 1) * (W + gap)
        const cz = (row - 1) * (H + gap)
        // Rectángulo exterior del bloque H
        addLine(pts, cx - W/2, cz - H/2, cx + W/2, cz - H/2)
        addLine(pts, cx + W/2, cz - H/2, cx + W/2, cz + H/2)
        addLine(pts, cx + W/2, cz + H/2, cx - W/2, cz + H/2)
        addLine(pts, cx - W/2, cz + H/2, cx - W/2, cz - H/2)
        // Ranura horizontal central (forma H)
        addLine(pts, cx - W/2, cz, cx - W/4, cz)
        addLine(pts, cx + W/4, cz, cx + W/2, cz)
        // Ranuras verticales
        addLine(pts, cx - W/4, cz - H/2, cx - W/4, cz + H/2)
        addLine(pts, cx + W/4, cz - H/2, cx + W/4, cz + H/2)
      }
    }

    // Marco exterior
    const ext = (W + gap) * 1.8
    addLine(pts, -ext, -ext, ext, -ext)
    addLine(pts, ext, -ext, ext, ext)
    addLine(pts, ext, ext, -ext, ext)
    addLine(pts, -ext, ext, -ext, -ext)

    return pts
  }, [])
  return (
    <>
      <CropLines points={points} />
      <GlowLight color="#88aaff" />
    </>
  )
}

// ─── VERACRUZ: Espiral Serpiente ─────────────────────────────────────────────
function SerpentSpiral() {
  const points = useMemo(() => {
    const pts: number[] = []
    const turns = 3
    const maxR = 7
    const steps = 300

    // Espiral doble (dos serpientes entrelazadas)
    for (let s = 0; s < 2; s++) {
      const phaseOffset = s * Math.PI
      for (let i = 0; i < steps; i++) {
        const t0 = i / steps
        const t1 = (i + 1) / steps
        const a0 = phaseOffset + t0 * turns * Math.PI * 2
        const a1 = phaseOffset + t1 * turns * Math.PI * 2
        // Ondulación sinusoidal sobre la espiral
        const wave0 = Math.sin(t0 * turns * Math.PI * 4) * 0.4
        const wave1 = Math.sin(t1 * turns * Math.PI * 4) * 0.4
        const r0 = t0 * maxR + wave0
        const r1 = t1 * maxR + wave1
        pts.push(Math.cos(a0) * r0, 0.02, Math.sin(a0) * r0)
        pts.push(Math.cos(a1) * r1, 0.02, Math.sin(a1) * r1)
      }
    }

    // Anillo exterior
    addCircle(pts, 0, 0, maxR)
    addCircle(pts, 0, 0, maxR * 0.15)

    return pts
  }, [])
  return (
    <>
      <CropLines points={points} />
      <GlowLight color="#00ff88" />
    </>
  )
}

// ─── TEOTIHUACÁN: Mandala Solar ───────────────────────────────────────────────
function SolarMandala() {
  const points = useMemo(() => {
    const pts: number[] = []
    const rings = [2, 3.5, 5, 6.5, 8]

    // Anillos concéntricos
    rings.forEach(r => addCircle(pts, 0, 0, r))

    // Rayos radiales (8 direcciones cardinales + intermedias)
    for (let i = 0; i < 16; i++) {
      const a = (i / 16) * Math.PI * 2
      const inner = i % 2 === 0 ? rings[0] : rings[1]
      addLine(pts, Math.cos(a) * inner, Math.sin(a) * inner,
                   Math.cos(a) * rings[4], Math.sin(a) * rings[4])
    }

    // Cuadrícula cardinal (cruz)
    const ext = rings[4]
    addLine(pts, -ext, 0, ext, 0)
    addLine(pts, 0, -ext, 0, ext)

    // Cuadrado interior rotado 45°
    const sq = rings[2] * 0.7
    addLine(pts, sq, 0, 0, sq)
    addLine(pts, 0, sq, -sq, 0)
    addLine(pts, -sq, 0, 0, -sq)
    addLine(pts, 0, -sq, sq, 0)

    return pts
  }, [])
  return (
    <>
      <CropLines points={points} />
      <GlowLight color="#ff8800" />
    </>
  )
}

// ─── ISLA DE PASCUA: Red de Nodos ─────────────────────────────────────────────
function NodeNetwork() {
  const points = useMemo(() => {
    const pts: number[] = []
    const N = 8       // nodos periféricos
    const R = 6       // radio del anillo
    const nodeR = 0.5 // radio de cada nodo

    // Nodo central
    addCircle(pts, 0, 0, nodeR * 1.5)
    addCircle(pts, 0, 0, nodeR * 0.7)

    const nodePos: [number, number][] = []
    for (let i = 0; i < N; i++) {
      const a = (i / N) * Math.PI * 2
      const cx = Math.cos(a) * R
      const cz = Math.sin(a) * R
      nodePos.push([cx, cz])
      // Círculo del nodo
      addCircle(pts, cx, cz, nodeR)
      // Línea al centro
      addLine(pts, 0, 0, cx, cz)
    }

    // Conexiones entre nodos adyacentes
    for (let i = 0; i < N; i++) {
      const [x0, z0] = nodePos[i]
      const [x1, z1] = nodePos[(i + 1) % N]
      addLine(pts, x0, z0, x1, z1)
    }

    // Conexiones cruzadas (cada nodo con el opuesto)
    for (let i = 0; i < N / 2; i++) {
      const [x0, z0] = nodePos[i]
      const [x1, z1] = nodePos[i + N / 2]
      addLine(pts, x0, z0, x1, z1)
    }

    // Anillo exterior
    addCircle(pts, 0, 0, R + nodeR)

    return pts
  }, [])
  return (
    <>
      <CropLines points={points} />
      <GlowLight color="#aa44ff" />
    </>
  )
}

// ─── NAVE 1 PHANTOM: Lissajous (Cloaking / alienígena) ───────────────────────
// x = sin(at + δ), z = sin(bt)
function Lissajous() {
  const points = useMemo(() => {
    const pts: number[] = []
    const freqA = 3, freqB = 4, delta = Math.PI / 4, R = 6
    const steps = 500
    for (let j = 0; j < steps; j++) {
      const t0 = (j / steps) * Math.PI * 2
      const t1 = ((j + 1) / steps) * Math.PI * 2
      pts.push(
        Math.sin(freqA * t0 + delta) * R, 0.02, Math.sin(freqB * t0) * R,
        Math.sin(freqA * t1 + delta) * R, 0.02, Math.sin(freqB * t1) * R
      )
    }
    // Segunda curva entrelazada
    const freqC = 5, freqD = 3, delta2 = Math.PI / 3
    for (let j = 0; j < steps; j++) {
      const t0 = (j / steps) * Math.PI * 2
      const t1 = ((j + 1) / steps) * Math.PI * 2
      pts.push(
        Math.sin(freqC * t0 + delta2) * R * 0.7, 0.02, Math.sin(freqD * t0) * R * 0.7,
        Math.sin(freqC * t1 + delta2) * R * 0.7, 0.02, Math.sin(freqD * t1) * R * 0.7
      )
    }
    addCircle(pts, 0, 0, R * 1.05)
    return pts
  }, [])
  return (
    <>
      <CropLines points={points} />
      <GlowLight color="#00ccff" />
    </>
  )
}

// ─── NAVE 2 AEGIS: Toroid (Defensa / campo EM) ────────────────────────────────
function Toroid() {
  const points = useMemo(() => {
    const pts: number[] = []
    const N = 32, ringR = 5, circR = 5
    for (let i = 0; i < N; i++) {
      const angle = (i / N) * Math.PI * 2
      addCircle(pts, Math.cos(angle) * ringR, Math.sin(angle) * ringR, circR)
    }
    addCircle(pts, 0, 0, circR * 0.4)
    addCircle(pts, 0, 0, ringR + circR)
    return pts
  }, [])
  return (
    <>
      <CropLines points={points} />
      <GlowLight color="#88aaff" />
    </>
  )
}

// ─── NAVE 4 ORACLE: Hilbert (Ciencia / fractal) ───────────────────────────────
function Hilbert() {
  const points = useMemo(() => {
    const pts: number[] = []
    const size = 7
    const hilbertPts: [number, number][] = []

    function hilbert(x: number, y: number, ax: number, ay: number, bx: number, by: number, level: number) {
      if (level <= 0) {
        hilbertPts.push([x + (ax + bx) / 2, y + (ay + by) / 2])
        return
      }
      hilbert(x, y, bx/2, by/2, ax/2, ay/2, level - 1)
      hilbert(x + ax/2, y + ay/2, ax/2, ay/2, bx/2, by/2, level - 1)
      hilbert(x + ax/2 + bx/2, y + ay/2 + by/2, ax/2, ay/2, bx/2, by/2, level - 1)
      hilbert(x + ax/2 + bx, y + ay/2 + by, -bx/2, -by/2, -ax/2, -ay/2, level - 1)
    }

    hilbert(0, 0, size, 0, 0, size, 4)
    const cx = size / 2, cz = size / 2
    for (let i = 0; i < hilbertPts.length - 1; i++) {
      pts.push(hilbertPts[i][0] - cx, 0.02, hilbertPts[i][1] - cz)
      pts.push(hilbertPts[i+1][0] - cx, 0.02, hilbertPts[i+1][1] - cz)
    }
    addCircle(pts, 0, 0, size * 0.62)
    return pts
  }, [])
  return (
    <>
      <CropLines points={points} />
      <GlowLight color="#ffdd00" />
    </>
  )
}

// ─── NAVE 5 TITAN: Polígono Estelar (Fuerza / mandala) ───────────────────────
function PolygonStar() {
  const points = useMemo(() => {
    const pts: number[] = []
    const R = 6
    const layers = [
      { sides: 5, skip: 2 },
      { sides: 7, skip: 3 },
      { sides: 9, skip: 4 },
    ]
    layers.forEach(({ sides, skip }, li) => {
      const r = R * (0.4 + li * 0.3)
      for (let i = 0; i < sides; i++) {
        const a0 = (i / sides) * Math.PI * 2 - Math.PI / 2
        const a1 = (((i + skip) % sides) / sides) * Math.PI * 2 - Math.PI / 2
        addLine(pts, Math.cos(a0) * r, Math.sin(a0) * r, Math.cos(a1) * r, Math.sin(a1) * r)
      }
      addCircle(pts, 0, 0, r)
    })
    // Rayos al centro
    for (let i = 0; i < 10; i++) {
      const a = (i / 10) * Math.PI * 2
      addLine(pts, 0, 0, Math.cos(a) * R, Math.sin(a) * R)
    }
    addCircle(pts, 0, 0, R * 1.05)
    return pts
  }, [])
  return (
    <>
      <CropLines points={points} />
      <GlowLight color="#ff4400" />
    </>
  )
}

// ─── PORTAL DE NAVE ───────────────────────────────────────────────────────────
// Detecta cuando el avatar se posiciona sobre el crop circle y cambia la nave.
// Una vez activado, persiste en localStorage y deja de evaluar proximidad.

interface CropCirclePortalProps {
  position: [number, number, number]
  ufoNumber: number
  missionDone: boolean
  avatarPositionRef?: React.RefObject<THREE.Vector3>
  onShipChange?: (ufoNumber: number) => void
  radius?: number
}

export function CropCirclePortal({
  position,
  ufoNumber,
  missionDone,
  avatarPositionRef,
  onShipChange,
  radius = 12
}: CropCirclePortalProps) {
  const storageKey = `portal_ufo_${ufoNumber}_activated`

  // Si ya fue activado en cualquier sesión anterior, no evaluar nada
  const alreadyDone = useRef(
    typeof window !== 'undefined' && localStorage.getItem(storageKey) === 'true'
  )

  useFrame(() => {
    // Cortocircuito: misión no completa, sin ref, sin callback, o ya activado
    if (!missionDone || !avatarPositionRef?.current || !onShipChange) return
    if (alreadyDone.current) return

    const av = avatarPositionRef.current
    const dx = av.x - position[0]
    const dz = av.z - position[2]

    if (dx * dx + dz * dz < radius * radius) {
      alreadyDone.current = true
      if (typeof window !== 'undefined') localStorage.setItem(storageKey, 'true')
      onShipChange(ufoNumber)
      console.log(`🛸 Portal activado → nave ${ufoNumber}`)
    }
  })

  if (!missionDone) return null

  return (
    <mesh position={[position[0], position[1] + 0.1, position[2]]} rotation={[-Math.PI / 2, 0, 0]}>
      <ringGeometry args={[radius * 0.85, radius, 48]} />
      <meshBasicMaterial color="#ffffff" transparent opacity={0.04} depthWrite={false} />
    </mesh>
  )
}

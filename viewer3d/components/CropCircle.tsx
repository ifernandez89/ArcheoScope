'use client'

import { useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

type CropPattern = 'flowerOfLife' | 'metatronCube' | 'spiral' | 'toroid' | 'fractalJulia' |
                   'flower' | 'metatron' | 'julia' |
                   'pyramidStar' | 'hBlock' | 'serpentSpiral' | 'solarMandala' | 'nodeNetwork'

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
  // Normalizar aliases
  const resolved =
    p === 'flower' ? 'flowerOfLife' :
    p === 'metatron' ? 'metatronCube' :
    p === 'julia' ? 'fractalJulia' :
    p === 'toroid' ? 'pyramidStar' :       // Giza: toroid → estrella piramidal
    p === 'spiral' ? 'serpentSpiral' :      // Veracruz: spiral → serpiente
    p

  return (
    <group position={position} scale={scale}>
      {resolved === 'pyramidStar'   && <PyramidStar />}
      {resolved === 'metatronCube'  && <HBlockGrid />}
      {resolved === 'serpentSpiral' && <SerpentSpiral />}
      {resolved === 'solarMandala'  && <SolarMandala />}
      {resolved === 'flowerOfLife'  && <NodeNetwork />}
      {resolved === 'fractalJulia'  && <SerpentSpiral />}
      {resolved === 'fractalJulia'  && <SerpentSpiral />}
      {/* fallbacks explícitos por nombre nuevo */}
      {resolved === 'nodeNetwork'   && <NodeNetwork />}
      {resolved === 'hBlock'        && <HBlockGrid />}
      {resolved === 'serpentSpiral' && null}
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

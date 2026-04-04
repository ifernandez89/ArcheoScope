'use client'

import { useMemo } from 'react'
import * as THREE from 'three'

type CropPattern = 'flowerOfLife' | 'metatronCube' | 'spiral' | 'toroid' | 'fractalJulia' | 'flower' | 'metatron' | 'julia'

interface CropCircleProps {
  pattern?: CropPattern
  type?: CropPattern
  position?: [number, number, number]
  scale?: number
  visible?: boolean
}

// Color pasto aplastado - igual que en la foto real
const C = '#a28f6a'
const OP = 0.65

// Círculo plano sobre el suelo
function Disk({ r, x = 0, z = 0 }: { r: number; x?: number; z?: number }) {
  return (
    <mesh position={[x, 0, z]} rotation={[-Math.PI / 2, 0, 0]}>
      <circleGeometry args={[r, 48]} />
      <meshBasicMaterial color={C} transparent opacity={OP} depthWrite={false} />
    </mesh>
  )
}

// Anillo plano sobre el suelo
function Ring({ inner, outer, x = 0, z = 0 }: { inner: number; outer: number; x?: number; z?: number }) {
  return (
    <mesh position={[x, 0, z]} rotation={[-Math.PI / 2, 0, 0]}>
      <ringGeometry args={[inner, outer, 48]} />
      <meshBasicMaterial color={C} transparent opacity={OP} depthWrite={false} />
    </mesh>
  )
}

export default function CropCircle({ pattern, type, position = [0, 0.02, 0], scale = 1, visible = false }: CropCircleProps) {
  if (!visible) return null
  // Normalizar: type es alias de pattern, mapear nombres cortos
  const p = pattern || type || 'flowerOfLife'
  const resolved = p === 'flower' ? 'flowerOfLife' : p === 'metatron' ? 'metatronCube' : p === 'julia' ? 'fractalJulia' : p
  return (
    <group position={position} scale={scale}>
      {resolved === 'flowerOfLife' && <FlowerOfLife />}
      {resolved === 'metatronCube' && <MetatronCube />}
      {resolved === 'spiral' && <Spiral />}
      {resolved === 'toroid' && <Toroid />}
      {resolved === 'fractalJulia' && <FractalJulia />}
    </group>
  )
}

// Flower of Life - círculos superpuestos
function FlowerOfLife() {
  const pts = useMemo(() => {
    const r = 2.5
    const out: [number, number, number][] = []
    for (let x = -3; x <= 3; x++) {
      for (let y = -3; y <= 3; y++) {
        const ox = x * r * 1.0
        const oz = y * r * 0.866
        if (Math.sqrt(ox * ox + oz * oz) < 8) out.push([ox, r, oz])
      }
    }
    return out
  }, [])
  return <>{pts.map(([x, r, z], i) => <Disk key={i} r={r} x={x} z={z} />)}</>
}

// Cubo de Metatrón - círculo central + 6 + 6 + anillos
function MetatronCube() {
  return (
    <>
      <Disk r={1.2} />
      {Array.from({ length: 6 }, (_, i) => {
        const a = (i / 6) * Math.PI * 2
        return <Disk key={i} r={1.2} x={Math.cos(a) * 3} z={Math.sin(a) * 3} />
      })}
      {Array.from({ length: 6 }, (_, i) => {
        const a = (i / 6) * Math.PI * 2 + Math.PI / 6
        return <Disk key={`o${i}`} r={0.7} x={Math.cos(a) * 5.5} z={Math.sin(a) * 5.5} />
      })}
      <Ring inner={2.5} outer={3.0} />
      <Ring inner={5.0} outer={5.5} />
    </>
  )
}

// Espiral galáctica - círculos pequeños en espiral
function Spiral() {
  const pts = useMemo(() => {
    const out: [number, number, number][] = []
    for (let i = 0; i < 120; i++) {
      const angle = i * 0.18
      const r = 0.07 * i
      out.push([Math.cos(angle) * r, 0.25 + (i / 120) * 0.5, Math.sin(angle) * r])
    }
    return out
  }, [])
  return <>{pts.map(([x, r, z], i) => <Disk key={i} r={r} x={x} z={z} />)}</>
}

// Toroide - anillos concéntricos
function Toroid() {
  return (
    <>
      {Array.from({ length: 7 }, (_, i) => (
        <Ring key={i} inner={(i + 1) * 1.5} outer={(i + 1) * 1.5 + 0.5} />
      ))}
      <Disk r={0.8} />
    </>
  )
}

// Fractal Julia - círculos en patrón fractal
function FractalJulia() {
  const pts = useMemo(() => {
    const out: [number, number, number][] = []
    for (let i = 0; i < 60; i++) {
      const angle = i * 0.2
      const r = Math.abs(Math.sin(i * 0.5)) * 6
      const size = 0.3 + Math.abs(Math.sin(i * 0.3)) * 0.5
      out.push([Math.cos(angle) * r, size, Math.sin(angle) * r])
    }
    return out
  }, [])
  return <>{pts.map(([x, r, z], i) => <Disk key={i} r={r} x={x} z={z} />)}</>
}

'use client'

import { useMemo } from 'react'
import * as THREE from 'three'
import { Html } from '@react-three/drei'
import { BRIGHT_STARS, raDecToXYZ, spectralColor } from '@/data/bright-stars'
import { CONSTELLATION_LINES } from '@/data/constellations'

/**
 * Estrellas en dos capas:
 *  - Capa base: 80.000 puntos procedurales (fondo galáctico) — igual que antes
 *  - Capa real: ~250 estrellas del catálogo Yale Bright Star con RA/Dec reales
 */
export default function Stars() {
  const layers = useMemo(() => {
    // ── Capa base: fondo galáctico procedural (IDÉNTICO AL ORIGINAL) ─────
    const baseCount = 80000
    const basePos   = new Float32Array(baseCount * 3)
    const baseCol   = new Float32Array(baseCount * 3)

    for (let i = 0; i < baseCount; i++) {
      const i3    = i * 3
      const theta = Math.random() * Math.PI * 2
      const phi   = Math.acos(2 * Math.random() - 1)
      const r = i < baseCount * 0.2
        ? 500  + Math.random() * 5500
        : 6000 + Math.random() * 14000

      basePos[i3]     = r * Math.sin(phi) * Math.cos(theta)
      basePos[i3 + 1] = r * Math.sin(phi) * Math.sin(theta)
      basePos[i3 + 2] = r * Math.cos(phi)

      const color = new THREE.Color()
      const t = Math.random()
      if      (t < 0.12) color.setHSL(0.60, 0.9, 0.92)
      else if (t < 0.28) color.setHSL(0.58, 0.5, 0.90)
      else if (t < 0.50) color.setHSL(0.13, 0.4, 0.92)
      else if (t < 0.65) color.setHSL(0.07, 0.6, 0.88)
      else if (t < 0.72) color.setHSL(0.02, 0.8, 0.82)
      else               color.setHSL(0.00, 0.0, 0.88 + Math.random() * 0.12)

      baseCol[i3]     = color.r
      baseCol[i3 + 1] = color.g
      baseCol[i3 + 2] = color.b
    }

    const baseGeo = new THREE.BufferGeometry()
    baseGeo.setAttribute('position', new THREE.BufferAttribute(basePos, 3))
    baseGeo.setAttribute('color',    new THREE.BufferAttribute(baseCol, 3))
    const baseMat = new THREE.PointsMaterial({
      size: 4.0,
      vertexColors: true,
      transparent: true,
      opacity: 0.90,
      sizeAttenuation: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    })

    // ── Capa brillante procedural (IDÉNTICO AL ORIGINAL) ─────────────────
    const brightCount = 3000
    const brightPos   = new Float32Array(brightCount * 3)
    const brightCol   = new Float32Array(brightCount * 3)

    for (let i = 0; i < brightCount; i++) {
      const i3    = i * 3
      const theta = Math.random() * Math.PI * 2
      const phi   = Math.acos(2 * Math.random() - 1)
      const r     = 3000 + Math.random() * 15000

      brightPos[i3]     = r * Math.sin(phi) * Math.cos(theta)
      brightPos[i3 + 1] = r * Math.sin(phi) * Math.sin(theta)
      brightPos[i3 + 2] = r * Math.cos(phi)

      const color = new THREE.Color()
      const t = Math.random()
      if   (t < 0.3) color.setHSL(0.60, 1.0, 1.0)
      else if (t < 0.6) color.setHSL(0.13, 0.6, 1.0)
      else           color.setHSL(0.00, 0.0, 1.0)

      brightCol[i3]     = color.r
      brightCol[i3 + 1] = color.g
      brightCol[i3 + 2] = color.b
    }

    const brightGeo = new THREE.BufferGeometry()
    brightGeo.setAttribute('position', new THREE.BufferAttribute(brightPos, 3))
    brightGeo.setAttribute('color',    new THREE.BufferAttribute(brightCol, 3))
    const brightMat = new THREE.PointsMaterial({
      size: 9.0,
      vertexColors: true,
      transparent: true,
      opacity: 0.70,
      sizeAttenuation: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    })

    // ── Capa real: catálogo Yale Bright Star ─────────────────────────────
    const R = 8000
    const realCount = BRIGHT_STARS.length
    const realPos   = new Float32Array(realCount * 3)
    const realCol   = new Float32Array(realCount * 3)

    // Mapa nombre → posición 3D para las constelaciones
    const starPositions = new Map<string, THREE.Vector3>()

    BRIGHT_STARS.forEach((star, i) => {
      const i3 = i * 3
      const [x, y, z] = raDecToXYZ(star.ra, star.dec, R)
      realPos[i3]     = x
      realPos[i3 + 1] = y
      realPos[i3 + 2] = z
      const [r, g, b] = spectralColor(star.type)
      realCol[i3]     = r
      realCol[i3 + 1] = g
      realCol[i3 + 2] = b
      if (star.name) starPositions.set(star.name, new THREE.Vector3(x, y, z))
    })

    const realGeo = new THREE.BufferGeometry()
    realGeo.setAttribute('position', new THREE.BufferAttribute(realPos, 3))
    realGeo.setAttribute('color',    new THREE.BufferAttribute(realCol, 3))
    const realMat = new THREE.PointsMaterial({
      size: 12.0,
      vertexColors: true,
      transparent: true,
      opacity: 1.0,
      sizeAttenuation: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    })

    return { baseGeo, baseMat, brightGeo, brightMat, realGeo, realMat, starPositions }
  }, [])

  // Constelaciones en componente separado para no interferir con las estrellas
  const constellationLines = useMemo(() => {
    const lines: { points: Float32Array, color: string }[] = []
    CONSTELLATION_LINES.forEach(constellation => {
      const pts: number[] = []
      constellation.stars.forEach(([nameA, nameB]) => {
        const posA = layers.starPositions.get(nameA)
        const posB = layers.starPositions.get(nameB)
        if (posA && posB) {
          pts.push(posA.x, posA.y, posA.z, posB.x, posB.y, posB.z)
        }
      })
      if (pts.length > 0) {
        lines.push({ points: new Float32Array(pts), color: constellation.color })
      }
    })
    return lines
  }, [layers.starPositions])

  // Centros de constelaciones para labels
  const constellationCenters = useMemo(() => {
    const centers: { name: string, position: THREE.Vector3, color: string }[] = []
    CONSTELLATION_LINES.forEach(constellation => {
      const positions: THREE.Vector3[] = []
      constellation.stars.forEach(([nameA, nameB]) => {
        const posA = layers.starPositions.get(nameA)
        const posB = layers.starPositions.get(nameB)
        if (posA) positions.push(posA)
        if (posB) positions.push(posB)
      })
      if (positions.length > 0) {
        const center = new THREE.Vector3()
        positions.forEach(p => center.add(p))
        center.divideScalar(positions.length)
        centers.push({ name: constellation.name, position: center, color: constellation.color })
      }
    })
    return centers
  }, [layers.starPositions])

  return (
    <group renderOrder={-1}>
      <points geometry={layers.baseGeo}   material={layers.baseMat} />
      <points geometry={layers.brightGeo} material={layers.brightMat} />
      <points geometry={layers.realGeo}   material={layers.realMat} />
      {/* Líneas de constelaciones */}
      {constellationLines.map((line, i) => (
        <lineSegments key={`const-${i}`}>
          <bufferGeometry>
            <bufferAttribute attach="attributes-position" count={line.points.length / 3} array={line.points} itemSize={3} />
          </bufferGeometry>
          <lineBasicMaterial color={line.color} transparent opacity={0.6} blending={THREE.AdditiveBlending} depthWrite={false} />
        </lineSegments>
      ))}
      {/* Nombres de constelaciones — sprite fijo, siempre visible */}
      {constellationCenters.map((c, i) => (
        <Html key={`label-${i}`} position={c.position} center sprite occlude={false}>
          <div style={{
            color: c.color,
            fontSize: '35px',
            fontFamily: 'monospace',
            letterSpacing: '4px',
            textTransform: 'uppercase',
            opacity: 0.9,
            textShadow: `0 0 20px ${c.color}, 0 0 40px ${c.color}`,
            pointerEvents: 'none',
            whiteSpace: 'nowrap',
            userSelect: 'none',
            fontWeight: 'bold',
          }}>
            {c.name}
          </div>
        </Html>
      ))}
    </group>
  )
}

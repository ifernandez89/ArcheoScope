'use client'

import { useMemo } from 'react'
import * as THREE from 'three'

/**
 * Estrellas procedurales en dos capas:
 *  - Capa base: 80.000 puntos pequeños, distribuidos hasta r=20000
 *  - Capa brillante: 3.000 puntos grandes, estrellas prominentes
 */
export default function Stars() {
  const layers = useMemo(() => {
    // ── Capa base ────────────────────────────────────────────────────────
    const baseCount = 80000
    const basePos   = new Float32Array(baseCount * 3)
    const baseCol   = new Float32Array(baseCount * 3)

    for (let i = 0; i < baseCount; i++) {
      const i3    = i * 3
      const theta = Math.random() * Math.PI * 2
      const phi   = Math.acos(2 * Math.random() - 1)
      // Distribución: 20% cerca (500-6000u), 80% lejos (6000-20000u)
      const r = i < baseCount * 0.2
        ? 500  + Math.random() * 5500
        : 6000 + Math.random() * 14000

      basePos[i3]     = r * Math.sin(phi) * Math.cos(theta)
      basePos[i3 + 1] = r * Math.sin(phi) * Math.sin(theta)
      basePos[i3 + 2] = r * Math.cos(phi)

      const color = new THREE.Color()
      const t = Math.random()
      if      (t < 0.12) color.setHSL(0.60, 0.9, 0.92)  // azul-blanco (tipo O/B)
      else if (t < 0.28) color.setHSL(0.58, 0.5, 0.90)  // blanco-azulado (tipo A)
      else if (t < 0.50) color.setHSL(0.13, 0.4, 0.92)  // amarillo-blanco (tipo F/G)
      else if (t < 0.65) color.setHSL(0.07, 0.6, 0.88)  // naranja (tipo K)
      else if (t < 0.72) color.setHSL(0.02, 0.8, 0.82)  // rojo (tipo M)
      else               color.setHSL(0.00, 0.0, 0.88 + Math.random() * 0.12) // blanco puro

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

    // ── Capa brillante ───────────────────────────────────────────────────
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
      if   (t < 0.3) color.setHSL(0.60, 1.0, 1.0)  // azul brillante
      else if (t < 0.6) color.setHSL(0.13, 0.6, 1.0) // amarillo brillante
      else           color.setHSL(0.00, 0.0, 1.0)    // blanco puro

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

    return { baseGeo, baseMat, brightGeo, brightMat }
  }, [])

  return (
    <group renderOrder={-1}>
      <points geometry={layers.baseGeo}   material={layers.baseMat} />
      <points geometry={layers.brightGeo} material={layers.brightMat} />
    </group>
  )
}

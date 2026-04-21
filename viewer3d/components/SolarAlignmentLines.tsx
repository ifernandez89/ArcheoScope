'use client'

/**
 * SolarAlignmentLines — Líneas de alineación solar arqueoastronómica
 * Muestra desde el sitio hacia dónde sale/pone el sol en:
 * - Solsticio de verano (21 jun)
 * - Solsticio de invierno (21 dic)
 * - Equinoccios (21 mar / 21 sep)
 *
 * Fórmula: cos(Az_salida) = sin(δ) / cos(φ)
 * donde δ = declinación solar, φ = latitud
 */

import { useMemo } from 'react'
import * as THREE from 'three'

interface SolarAlignmentLinesProps {
  latitude: number   // grados
  visible: boolean
  length?: number    // longitud de las líneas en unidades de escena
}

// Declinaciones solares para eventos clave (grados)
const SOLAR_EVENTS = [
  { label: 'Solsticio Verano',   decl:  23.44, color: '#ff6b00', riseColor: '#ff9500', setColor: '#ff4500' },
  { label: 'Equinoccio',         decl:  0,     color: '#00d4ff', riseColor: '#00aaff', setColor: '#0066ff' },
  { label: 'Solsticio Invierno', decl: -23.44, color: '#a78bfa', riseColor: '#c4b5fd', setColor: '#7c3aed' },
]

function azimuthRise(declDeg: number, latDeg: number): number | null {
  const decl = declDeg * Math.PI / 180
  const lat  = latDeg  * Math.PI / 180
  const cosAz = Math.sin(decl) / Math.cos(lat)
  if (Math.abs(cosAz) > 1) return null // Sol no sale/pone (circumpolar)
  return Math.acos(cosAz) // azimut de salida (E del N), en radianes
}

function azimuthToDirection(azRad: number): THREE.Vector3 {
  // Azimut 0 = Norte, 90 = Este, 180 = Sur, 270 = Oeste
  // En Three.js: X = Este, Z = Sur (eje Z positivo hacia el sur)
  return new THREE.Vector3(
    Math.sin(azRad),   // X = Este
    0,
    Math.cos(azRad)    // Z = Norte
  ).normalize()
}

export default function SolarAlignmentLines({ latitude, visible, length = 80 }: SolarAlignmentLinesProps) {
  const lines = useMemo(() => {
    return SOLAR_EVENTS.flatMap(event => {
      const azRise = azimuthRise(event.decl, latitude)
      if (azRise === null) return []

      const azSet = Math.PI * 2 - azRise // Puesta = simétrica al oeste

      const riseDir = azimuthToDirection(azRise)
      const setDir  = azimuthToDirection(azSet)

      // Geometría de línea: origen → extremo
      const riseGeo = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 0.5, 0),
        riseDir.clone().multiplyScalar(length)
      ])
      const setGeo = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 0.5, 0),
        setDir.clone().multiplyScalar(length)
      ])

      return [
        { geo: riseGeo, color: event.riseColor, label: `${event.label} ↑`, azDeg: azRise * 180 / Math.PI },
        { geo: setGeo,  color: event.setColor,  label: `${event.label} ↓`, azDeg: azSet  * 180 / Math.PI },
      ]
    })
  }, [latitude, length])

  if (!visible) return null

  return (
    <group>
      {lines.map((line, i) => (
        <primitive key={i} object={new THREE.Line(line.geo, new THREE.LineBasicMaterial({ color: line.color, transparent: true, opacity: 0.75 }))} />
      ))}
    </group>
  )
}

/**
 * Calcular datos de alineación para mostrar en el panel UI
 */
export function calcAlignments(latitude: number): Array<{
  event: string
  riseAz: number | null
  setAz: number | null
  color: string
}> {
  return SOLAR_EVENTS.map(ev => {
    const azRise = azimuthRise(ev.decl, latitude)
    const azSet  = azRise !== null ? (360 - azRise * 180 / Math.PI) : null
    return {
      event: ev.label,
      riseAz: azRise !== null ? azRise * 180 / Math.PI : null,
      setAz: azRise !== null ? (360 - azRise * 180 / Math.PI) : null,
      color: ev.color,
    }
  })
}

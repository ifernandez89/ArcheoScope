'use client'

/**
 * DynamicSky — Cielo con Rayleigh scattering real usando Sky shader de Three.js
 *
 * Día:    Sky shader con posición solar real → azul, naranja al atardecer, rojo al amanecer
 * Noche:  Esfera negra con capa interna de ~10,000 estrellas procedurales
 * Tormenta: oscurece el cielo progresivamente
 *
 * La capa interna de estrellas se desvanece de día (opacity→0) y aparece de noche (opacity→0.6).
 * Esto restaura el comportamiento original donde las estrellas siempre estaban presentes
 * y se controlaban con fade in/out según isDay.
 */

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { Sky } from '@react-three/drei'
import * as THREE from 'three'

interface DynamicSkyProps {
  isDay?: boolean
  skyColor?: string
  stormDarkness?: number
  solarDirection?: { x: number, y: number, z: number }
}

export default function DynamicSky({
  isDay = true,
  skyColor = '#87ceeb',
  stormDarkness = 0,
  solarDirection
}: DynamicSkyProps) {
  const nightSkyRef = useRef<THREE.Mesh>(null)
  const nightOpacityRef = useRef(isDay ? 0 : 1)
  const starsRef = useRef<THREE.Points>(null)
  const starsOpacityRef = useRef(isDay ? 0 : 0.6)

  // Convertir solarDirection a posición del sol para el shader Sky
  const sunPosition = useMemo((): [number, number, number] => {
    if (solarDirection) {
      return [solarDirection.x * 100, solarDirection.y * 100, solarDirection.z * 100]
    }
    return [0, 10, -100]
  }, [solarDirection?.x, solarDirection?.y, solarDirection?.z])

  // Turbidez: más alta en tormentas
  const turbidity = useMemo(() => {
    return 2 + stormDarkness * 18
  }, [stormDarkness])

  // ── Capa interna de estrellas procedurales (restaurada del DynamicSky original) ──
  const { starsGeo, starsMat } = useMemo(() => {
    const count = 10000
    const positions = new Float32Array(count * 3)
    const colors = new Float32Array(count * 3)

    for (let i = 0; i < count; i++) {
      const i3 = i * 3
      const theta = Math.random() * Math.PI * 2
      const phi = Math.acos(2 * Math.random() - 1)
      const r = 350 + Math.random() * 40 // dentro de la esfera negra (r=400)

      positions[i3]     = r * Math.sin(phi) * Math.cos(theta)
      positions[i3 + 1] = r * Math.sin(phi) * Math.sin(theta)
      positions[i3 + 2] = r * Math.cos(phi)

      const color = new THREE.Color()
      const t = Math.random()
      if      (t < 0.15) color.setHSL(0.60, 0.8, 0.90) // azuladas
      else if (t < 0.35) color.setHSL(0.13, 0.4, 0.92) // amarillentas
      else if (t < 0.50) color.setHSL(0.07, 0.6, 0.88) // anaranjadas
      else               color.setHSL(0.00, 0.0, 0.85 + Math.random() * 0.15) // blancas

      colors[i3]     = color.r
      colors[i3 + 1] = color.g
      colors[i3 + 2] = color.b
    }

    const geo = new THREE.BufferGeometry()
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3))

    const mat = new THREE.PointsMaterial({
      size: 1.5,
      vertexColors: true,
      transparent: true,
      opacity: isDay ? 0 : 0.6,
      sizeAttenuation: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    })

    return { starsGeo: geo, starsMat: mat }
  }, [])

  // Transición suave noche/día
  useFrame(() => {
    // Esfera negra
    if (nightSkyRef.current) {
      const mat = nightSkyRef.current.material as THREE.MeshBasicMaterial
      const target = isDay ? 0 : 1
      nightOpacityRef.current += (target - nightOpacityRef.current) * 0.02
      mat.opacity = nightOpacityRef.current
    }

    // Estrellas internas: fade in/out con isDay
    if (starsRef.current) {
      const mat = starsRef.current.material as THREE.PointsMaterial
      const target = isDay ? 0 : 0.6
      starsOpacityRef.current += (target - starsOpacityRef.current) * 0.02
      mat.opacity = starsOpacityRef.current
    }
  })

  return (
    <>
      {/* Cielo atmosférico con Rayleigh scattering — solo de día */}
      {isDay && (
        <Sky
          distance={450000}
          sunPosition={sunPosition}
          inclination={0}
          azimuth={0.25}
          turbidity={turbidity}
          rayleigh={0.5}
          mieCoefficient={0.005}
          mieDirectionalG={0.8}
        />
      )}

      {/* Esfera negra de noche — se hace opaca al anochecer */}
      <mesh ref={nightSkyRef} renderOrder={-2}>
        <sphereGeometry args={[400, 32, 32]} />
        <meshBasicMaterial
          color="#000814"
          side={THREE.BackSide}
          transparent
          opacity={isDay ? 0 : 1}
          fog={false}
          depthWrite={false}
        />
      </mesh>

      {/* Capa interna de estrellas — siempre montada, opacity controlada por isDay */}
      <points ref={starsRef} geometry={starsGeo} material={starsMat} renderOrder={-1} />
    </>
  )
}

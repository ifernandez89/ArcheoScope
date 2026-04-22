'use client'

/**
 * DynamicSky — Cielo con Rayleigh scattering real usando Sky shader de Three.js
 *
 * Día:    Sky shader con posición solar real → azul, naranja al atardecer, rojo al amanecer
 * Noche:  Esfera negra (las estrellas del componente Stars se ven encima)
 * Tormenta: oscurece el cielo progresivamente
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

  // Convertir solarDirection a posición del sol para el shader Sky
  // Sky espera [x, y, z] donde y es la altura (positivo = sobre horizonte)
  const sunPosition = useMemo((): [number, number, number] => {
    if (solarDirection) {
      return [solarDirection.x * 100, solarDirection.y * 100, solarDirection.z * 100]
    }
    // Fallback: sol al mediodía sur
    return [0, 10, -100]
  }, [solarDirection?.x, solarDirection?.y, solarDirection?.z])

  // Turbidez: más alta en tormentas (cielo más gris/oscuro)
  const turbidity = useMemo(() => {
    return 2 + stormDarkness * 18 // 2 (cielo limpio) → 20 (tormenta)
  }, [stormDarkness])

  // Transición suave noche/día en la esfera negra
  useFrame(() => {
    if (!nightSkyRef.current) return
    const mat = nightSkyRef.current.material as THREE.MeshBasicMaterial
    const target = isDay ? 0 : 1
    nightOpacityRef.current += (target - nightOpacityRef.current) * 0.02
    mat.opacity = nightOpacityRef.current
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
    </>
  )
}

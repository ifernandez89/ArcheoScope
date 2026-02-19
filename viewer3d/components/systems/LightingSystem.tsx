'use client'

/**
 * LightingSystem - Sistema de iluminación modular
 * Se carga solo cuando se necesita iluminación avanzada
 */

import { useMemo } from 'react'
import CinematicLighting from '../CinematicLighting'
import IceLighting from '../IceLighting'
import type { BiomeType } from '@/utils/biome-detector'

interface LightingSystemProps {
  biomeType: BiomeType
  solarDirection: { x: number; y: number; z: number }
  enableShadows?: boolean
  sunIntensity?: number
  hemisphereIntensity?: number
}

export default function LightingSystem({
  biomeType,
  solarDirection,
  enableShadows = true,
  sunIntensity = 2.5,
  hemisphereIntensity = 1.2
}: LightingSystemProps) {
  const sunPosition = useMemo(() => [
    solarDirection.x * 50,
    Math.max(solarDirection.y * 50, 10),
    solarDirection.z * 50
  ] as [number, number, number], [solarDirection])

  const isIceBiome = biomeType === 'ice'

  return isIceBiome ? (
    <IceLighting
      sunPosition={sunPosition}
      enableShadows={enableShadows}
    />
  ) : (
    <CinematicLighting
      sunIntensity={sunIntensity}
      hemisphereIntensity={hemisphereIntensity}
      sunPosition={sunPosition}
      enableShadows={enableShadows}
    />
  )
}

'use client'

/**
 * EffectsLayer - Post-processing, Bloom, Vignette, Partículas
 * 
 * Responsabilidades:
 * - Post-processing effects
 * - Bloom effect
 * - Volumetric effects
 * - Partículas
 * - Motion / DoF efectos
 * 
 * **LAZY-LOADING FUERTE**: No se carga si graphicsPreset === "low"
 * Se monta solo en: Medium, High, Ultra
 * Esto evita cargar shaders innecesarios en GPU integradas
 */

import { useMemo } from 'react'
import {
  PostProcessingSystem
} from '@/utils/lazy-systems'

interface EffectsLayerProps {
  enabled: boolean
  graphicsPreset?: 'low' | 'medium' | 'high' | 'ultra'
  bloomIntensity?: number
  vignetteIntensity?: number
  showParticles?: boolean
}

export default function EffectsLayer({
  enabled = true,
  graphicsPreset = 'high',
  bloomIntensity = 0.3,
  vignetteIntensity = 0.4,
  showParticles = true
}: EffectsLayerProps) {
  // ✋ GUARD: No cargar en preset bajo
  if (!enabled || graphicsPreset === 'low') {
    return null
  }

  // Ajustar intensidades según preset
  const adjustedBloom = useMemo(() => {
    const mapping = {
      low: 0,
      medium: 0.2,
      high: bloomIntensity,
      ultra: bloomIntensity * 1.5
    }
    return mapping[graphicsPreset]
  }, [graphicsPreset, bloomIntensity])

  const adjustedVignette = useMemo(() => {
    const mapping = {
      low: 0,
      medium: 0.2,
      high: vignetteIntensity,
      ultra: vignetteIntensity * 1.2
    }
    return mapping[graphicsPreset]
  }, [graphicsPreset, vignetteIntensity])

  return (
    <group name="effects-layer">
      {/* Post-processing modular */}
      <PostProcessingSystem
        enableBloom={true}
        enableVignette={true}
        bloomIntensity={adjustedBloom}
        vignetteIntensity={adjustedVignette}
      />

      {/* Partículas ambientales sutiles */}
      {showParticles && graphicsPreset !== 'low' && (
        <AmbientParticles enabled={graphicsPreset === 'ultra'} />
      )}
    </group>
  )
}

/**
 * Partículas ambientales para sensación de movimiento
 */
function AmbientParticles({ enabled = false }: { enabled: boolean }) {
  // Implementación lazy en useFrame
  return null
}

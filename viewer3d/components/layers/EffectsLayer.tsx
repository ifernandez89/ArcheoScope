'use client'

/**
 * EffectsLayer - Post-processing, Bloom, Partículas
 * 
 * Responsabilidades:
 * - Post-processing effects (bloom, SSAO, etc.)
 * - Partículas atmosféricas
 * - Efectos visuales avanzados
 * 
 * LAZY LOADING FUERTE: Solo en graphics preset 'high'
 * Bundle size: ~150KB
 */

import { Suspense } from 'react'
import { EffectComposer, Bloom } from '@react-three/postprocessing'

interface EffectsLayerProps {
  graphicsPreset?: 'low' | 'medium' | 'high'
  enableBloom?: boolean
}

export default function EffectsLayer({
  graphicsPreset = 'medium',
  enableBloom = true
}: EffectsLayerProps) {
  // Solo cargar en preset alto
  if (graphicsPreset !== 'high') {
    return null
  }

  return (
    <Suspense fallback={null}>
      <EffectComposer>
        <>
          {enableBloom && (
            <Bloom
              intensity={0.5}
              luminanceThreshold={0.9}
              luminanceSmoothing={0.9}
            />
          )}
        </>
      </EffectComposer>
    </Suspense>
  )
}

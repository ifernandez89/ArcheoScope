'use client'

/**
 * PostProcessingSystem - Sistema de post-procesado modular
 * Se carga SOLO cuando se necesita post-procesado
 * Esto evita cargar EffectComposer innecesariamente
 */

import SubtlePostProcessing from '../SubtlePostProcessing'

interface PostProcessingSystemProps {
  enableBloom?: boolean
  enableVignette?: boolean
  bloomIntensity?: number
  vignetteIntensity?: number
}

export default function PostProcessingSystem({
  enableBloom = true,
  enableVignette = true,
  bloomIntensity = 0.3,
  vignetteIntensity = 0.4
}: PostProcessingSystemProps) {
  return (
    <SubtlePostProcessing
      enableBloom={enableBloom}
      enableVignette={enableVignette}
      bloomIntensity={bloomIntensity}
      vignetteIntensity={vignetteIntensity}
    />
  )
}

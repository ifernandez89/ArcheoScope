'use client'

import { EffectComposer, Bloom, Vignette } from '@react-three/postprocessing'
import { BlendFunction } from 'postprocessing'

interface SubtlePostProcessingProps {
  enableBloom?: boolean
  enableVignette?: boolean
  bloomIntensity?: number
  vignetteIntensity?: number
}

export default function SubtlePostProcessing({
  enableBloom = true,
  enableVignette = true,
  bloomIntensity = 0.3,
  vignetteIntensity = 0.4
}: SubtlePostProcessingProps) {
  return (
    <EffectComposer>
      <Bloom
        intensity={enableBloom ? bloomIntensity : 0}
        luminanceThreshold={0.9}
        luminanceSmoothing={0.9}
        mipmapBlur
        blendFunction={BlendFunction.ADD}
      />
      <Vignette
        offset={0.3}
        darkness={enableVignette ? vignetteIntensity : 0}
        blendFunction={BlendFunction.NORMAL}
      />
    </EffectComposer>
  )
}

import { EffectComposer, Bloom, DepthOfField, SSAO, ChromaticAberration, Vignette } from '@react-three/postprocessing'
import { BlendFunction } from 'postprocessing'

interface AdvancedPostProcessingProps {
  enableBloom?: boolean
  enableDOF?: boolean
  enableSSAO?: boolean
  enableVignette?: boolean
  enableChromaticAberration?: boolean
  quality?: 'low' | 'medium' | 'high'
}

/**
 * Sistema de post-processing avanzado
 * Efectos visuales de alta calidad
 */
export function AdvancedPostProcessing({
  enableBloom = true,
  enableDOF = false,
  enableSSAO = true,
  enableVignette = true,
  enableChromaticAberration = false,
  quality = 'medium'
}: AdvancedPostProcessingProps) {
  
  // Configuración según calidad
  const qualitySettings = {
    low: {
      bloomLuminanceThreshold: 1.0,
      bloomIntensity: 0.5,
      ssaoSamples: 8,
      ssaoRadius: 5,
      dofBokehScale: 1
    },
    medium: {
      bloomLuminanceThreshold: 0.9,
      bloomIntensity: 1.0,
      ssaoSamples: 16,
      ssaoRadius: 10,
      dofBokehScale: 2
    },
    high: {
      bloomLuminanceThreshold: 0.8,
      bloomIntensity: 1.5,
      ssaoSamples: 32,
      ssaoRadius: 15,
      dofBokehScale: 3
    }
  }
  
  const settings = qualitySettings[quality]
  
  return (
    <EffectComposer multisampling={quality === 'high' ? 8 : 4}>
      {/* Bloom - Resplandor realista */}
      {enableBloom && (
        <Bloom
          luminanceThreshold={settings.bloomLuminanceThreshold}
          luminanceSmoothing={0.9}
          intensity={settings.bloomIntensity}
          blendFunction={BlendFunction.ADD}
        />
      )}
      
      {/* SSAO - Oclusión ambiental */}
      {enableSSAO && (
        <SSAO
          samples={settings.ssaoSamples}
          radius={settings.ssaoRadius}
          intensity={30}
          luminanceInfluence={0.6}
          color="black"
          blendFunction={BlendFunction.MULTIPLY}
        />
      )}
      
      {/* Depth of Field - Profundidad de campo */}
      {enableDOF && (
        <DepthOfField
          focusDistance={0.01}
          focalLength={0.05}
          bokehScale={settings.dofBokehScale}
          height={480}
        />
      )}
      
      {/* Vignette - Viñeta sutil */}
      {enableVignette && (
        <Vignette
          offset={0.3}
          darkness={0.5}
          blendFunction={BlendFunction.NORMAL}
        />
      )}
      
      {/* Chromatic Aberration - Aberración cromática */}
      {enableChromaticAberration && (
        <ChromaticAberration
          offset={[0.001, 0.001]}
          blendFunction={BlendFunction.NORMAL}
        />
      )}
    </EffectComposer>
  )
}

/**
 * Preset para exploración arqueológica
 */
export function ArchaeologicalPreset() {
  return (
    <AdvancedPostProcessing
      enableBloom={true}
      enableSSAO={true}
      enableVignette={true}
      enableDOF={false}
      enableChromaticAberration={false}
      quality="high"
    />
  )
}

/**
 * Preset para espacio/sistema solar
 */
export function SpacePreset() {
  return (
    <AdvancedPostProcessing
      enableBloom={true}
      enableSSAO={false}
      enableVignette={true}
      enableDOF={false}
      enableChromaticAberration={true}
      quality="high"
    />
  )
}

/**
 * Preset para performance (móviles)
 */
export function PerformancePreset() {
  return (
    <AdvancedPostProcessing
      enableBloom={true}
      enableSSAO={false}
      enableVignette={true}
      enableDOF={false}
      enableChromaticAberration={false}
      quality="low"
    />
  )
}

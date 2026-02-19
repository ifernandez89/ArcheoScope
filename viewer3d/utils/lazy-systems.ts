/**
 * Lazy loading de sistemas pesados
 * Solo sistemas OPCIONALES deben ser lazy
 * Sistemas que siempre se usan deben ser imports directos
 */

import dynamic from 'next/dynamic'

// ⚠️ SISTEMAS SIEMPRE USADOS - Import directo (NO lazy)
export { default as LightingSystem } from '@/components/systems/LightingSystem'
export { default as EnvironmentSystem } from '@/components/systems/EnvironmentSystem'
export { default as AstronomicalSystem } from '@/components/systems/AstronomicalSystem'

// ✅ SISTEMAS OPCIONALES - Lazy loading
// Sistema climático (solo se usa cuando hay clima activo)
export const WeatherSystem = dynamic(
  () => import('@/components/systems/WeatherSystem'),
  { ssr: false }
)

// Sistema de post-procesado (podría ser opcional según preset)
export const PostProcessingSystem = dynamic(
  () => import('@/components/systems/PostProcessingSystem'),
  { ssr: false }
)

// Sistema de terreno procedural
export const ProceduralTerrain = dynamic(
  () => import('@/components/ProceduralTerrain'),
  { ssr: false }
)

// Terrenos específicos (siempre se usan, pero uno u otro)
export { default as VolcanicTerrain } from '@/components/VolcanicTerrain'
export { default as IceTerrain } from '@/components/IceTerrain'

'use client'

/**
 * Lazy Loading de Engines Pesados
 * Reduce el bundle inicial cargando engines bajo demanda
 */

import dynamic from 'next/dynamic'
import React from 'react'

/**
 * WorldCore - Carga lazy del núcleo del mundo
 */
export const loadWorldCore = async () => {
  const { WorldCore } = await import('@/engines/WorldCore')
  return WorldCore
}

/**
 * ArcheoEngine - Carga lazy del motor arqueológico
 */
export const loadArcheoEngine = async () => {
  const ArcheoEngine = await import('@/engines/ArcheoEngine')
  return ArcheoEngine.default
}

/**
 * AstroEngine - Carga lazy del motor astronómico
 */
export const loadAstroEngine = async () => {
  const AstroEngine = await import('@/engines/AstroEngine')
  return AstroEngine.default
}

/**
 * SolarEngine - Carga lazy del motor solar
 */
export const loadSolarEngine = async () => {
  const { SolarEngine } = await import('@/engines/SolarEngine')
  return SolarEngine
}

/**
 * GeoEngine - Carga lazy del motor geográfico
 */
export const loadGeoEngine = async () => {
  const GeoEngine = await import('@/engines/GeoEngine')
  return GeoEngine.default
}

/**
 * Hook para cargar engines bajo demanda
 */
export function useLazyEngine<T>(
  loader: () => Promise<T>,
  deps: any[] = []
): { engine: T | null; loading: boolean; error: Error | null } {
  const [engine, setEngine] = React.useState<T | null>(null)
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState<Error | null>(null)

  React.useEffect(() => {
    let mounted = true

    loader()
      .then((loadedEngine) => {
        if (mounted) {
          setEngine(loadedEngine)
          setLoading(false)
        }
      })
      .catch((err) => {
        if (mounted) {
          setError(err)
          setLoading(false)
        }
      })

    return () => {
      mounted = false
    }
  }, deps)

  return { engine, loading, error }
}

/**
 * Componentes lazy para escenas pesadas
 */
export const LazyImmersiveScene = dynamic(
  () => import('@/components/ImmersiveScene'),
  {
    loading: () => React.createElement('div', 
      { className: 'flex items-center justify-center h-screen bg-black' },
      React.createElement('div',
        { className: 'text-white text-center' },
        React.createElement('div', 
          { className: 'animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-white mx-auto mb-4' }
        ),
        React.createElement('p', null, 'Loading 3D Scene...')
      )
    ),
    ssr: false
  }
)

/**
 * Preload de engines críticos
 */
export function preloadCriticalEngines() {
  // Precargar engines que se usan frecuentemente
  if (typeof window !== 'undefined') {
    // Preload después de que la página cargue
    window.addEventListener('load', () => {
      setTimeout(() => {
        loadWorldCore()
        loadGeoEngine()
      }, 1000)
    })
  }
}

/**
 * Cache de engines cargados
 */
const engineCache = new Map<string, any>()

export async function loadEngineWithCache<T>(
  key: string,
  loader: () => Promise<T>
): Promise<T> {
  if (engineCache.has(key)) {
    return engineCache.get(key)
  }

  const engine = await loader()
  engineCache.set(key, engine)
  return engine
}

/**
 * Limpiar cache de engines
 */
export function clearEngineCache() {
  engineCache.clear()
}

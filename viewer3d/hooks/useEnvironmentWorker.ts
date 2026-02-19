/**
 * useEnvironmentWorker - Hook para usar el worker de generación procedural
 */

import { useEffect, useRef, useState, useCallback } from 'react'
import type { 
  WorkerRequest, 
  TerrainData, 
  BiomeData, 
  EnvironmentData 
} from '@/workers/environment.worker'

export function useEnvironmentWorker() {
  const workerRef = useRef<Worker | null>(null)
  const [isReady, setIsReady] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const callbacksRef = useRef<Map<string, (data: any) => void>>(new Map())

  useEffect(() => {
    // Crear worker
    workerRef.current = new Worker(
      new URL('../workers/environment.worker.ts', import.meta.url),
      { type: 'module' }
    )

    // Handler de mensajes
    workerRef.current.onmessage = (event) => {
      const { type, data, error } = event.data

      if (type === 'error') {
        console.error('Worker error:', error)
        setIsProcessing(false)
        return
      }

      // Ejecutar callback correspondiente
      const callback = callbacksRef.current.get(type)
      if (callback) {
        callback(data)
        callbacksRef.current.delete(type)
      }

      setIsProcessing(false)
    }

    setIsReady(true)

    return () => {
      workerRef.current?.terminate()
      workerRef.current = null
    }
  }, [])

  /**
   * Generar terreno
   */
  const generateTerrain = useCallback(
    (
      location: { lat: number; lon: number },
      size: number = 50,
      resolution: number = 128,
      seed?: number
    ): Promise<TerrainData> => {
      return new Promise((resolve, reject) => {
        if (!workerRef.current || !isReady) {
          reject(new Error('Worker not ready'))
          return
        }

        setIsProcessing(true)

        callbacksRef.current.set('terrainGenerated', (data: TerrainData) => {
          resolve(data)
        })

        workerRef.current.postMessage({
          type: 'generateTerrain',
          location,
          size,
          resolution,
          seed
        } as WorkerRequest)
      })
    },
    [isReady]
  )

  /**
   * Analizar bioma
   */
  const analyzeBiome = useCallback(
    (
      location: { lat: number; lon: number },
      isDay: boolean = true
    ): Promise<BiomeData> => {
      return new Promise((resolve, reject) => {
        if (!workerRef.current || !isReady) {
          reject(new Error('Worker not ready'))
          return
        }

        setIsProcessing(true)

        callbacksRef.current.set('biomeAnalyzed', (data: BiomeData) => {
          resolve(data)
        })

        workerRef.current.postMessage({
          type: 'analyzeBiome',
          location,
          isDay
        } as WorkerRequest)
      })
    },
    [isReady]
  )

  /**
   * Generar entorno completo
   */
  const generateEnvironment = useCallback(
    (
      location: { lat: number; lon: number },
      size: number = 50,
      resolution: number = 128,
      isDay: boolean = true
    ): Promise<EnvironmentData> => {
      return new Promise((resolve, reject) => {
        if (!workerRef.current || !isReady) {
          reject(new Error('Worker not ready'))
          return
        }

        setIsProcessing(true)

        callbacksRef.current.set('environmentGenerated', (data: EnvironmentData) => {
          resolve(data)
        })

        workerRef.current.postMessage({
          type: 'generateEnvironment',
          location,
          size,
          resolution,
          isDay
        } as WorkerRequest)
      })
    },
    [isReady]
  )

  return {
    isReady,
    isProcessing,
    generateTerrain,
    analyzeBiome,
    generateEnvironment
  }
}

/**
 * Ejemplo de uso:
 * 
 * function MyComponent() {
 *   const { generateTerrain, isProcessing } = useEnvironmentWorker()
 * 
 *   const handleGenerate = async () => {
 *     const terrain = await generateTerrain(
 *       { lat: -13.163, lon: -72.545 },
 *       50,
 *       128
 *     )
 *     
 *     // Usar terrain.positions, terrain.normals, etc.
 *   }
 * 
 *   return (
 *     <button onClick={handleGenerate} disabled={isProcessing}>
 *       {isProcessing ? 'Generating...' : 'Generate Terrain'}
 *     </button>
 *   )
 * }
 */

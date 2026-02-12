// Custom Hook for Core Engine
import { useEffect, useRef } from 'react'
import { useThree } from '@react-three/fiber'
import { Engine3D } from '@/core/engine'
import type { LightingConfig } from '@/core/types'

export function useEngine(lightingConfig?: LightingConfig) {
  const { scene, camera } = useThree()
  const engineRef = useRef<Engine3D | null>(null)

  useEffect(() => {
    if (!engineRef.current && camera.type === 'PerspectiveCamera') {
      const defaultLightingConfig: LightingConfig = lightingConfig || {
        ambient: { intensity: 0.4, color: '#ffffff' },
        directional: { 
          intensity: 1.2, 
          position: [10, 10, 5], 
          castShadow: true 
        },
        point: { intensity: 0.3, position: [-10, -10, -5] }
      }

      engineRef.current = new Engine3D(
        scene,
        camera as THREE.PerspectiveCamera,
        defaultLightingConfig
      )

      console.log('🎮 Core Engine initialized')
    }

    return () => {
      if (engineRef.current) {
        engineRef.current.dispose()
        engineRef.current = null
        console.log('🎮 Core Engine disposed')
      }
    }
  }, [scene, camera, lightingConfig])

  return engineRef.current
}

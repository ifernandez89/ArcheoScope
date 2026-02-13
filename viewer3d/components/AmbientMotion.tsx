'use client'

import { useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

interface AmbientMotionProps {
  enableCameraBreathing?: boolean
  enableLightOscillation?: boolean
  intensity?: number
}

export default function AmbientMotion({
  enableCameraBreathing = true,
  enableLightOscillation = true,
  intensity = 0.5
}: AmbientMotionProps) {
  const { camera } = useThree()
  const lightRef = useRef<THREE.PointLight>(null)
  const initialCameraPos = useRef(new THREE.Vector3())
  const hasInitialized = useRef(false)

  useFrame((state) => {
    const time = state.clock.elapsedTime

    // Camera breathing (muy sutil)
    if (enableCameraBreathing && camera) {
      if (!hasInitialized.current) {
        initialCameraPos.current.copy(camera.position)
        hasInitialized.current = true
      }
      
      const breathe = Math.sin(time * 0.5) * 0.02 * intensity
      camera.position.y = initialCameraPos.current.y + breathe
    }

    // Light oscillation (muy sutil)
    if (enableLightOscillation && lightRef.current) {
      lightRef.current.intensity = 0.5 + Math.sin(time * 0.8) * 0.1 * intensity
    }
  })

  return (
    <>
      {/* Luz ambiental oscilante */}
      {enableLightOscillation && (
        <pointLight
          ref={lightRef}
          position={[0, 5, 0]}
          intensity={0.5}
          distance={20}
          decay={2}
          color="#ffa500"
        />
      )}
    </>
  )
}

'use client'

/**
 * CoreEngine - Motor mínimo y ultra-estable
 * 
 * Responsabilidades:
 * - Canvas renderer
 * - Cámara base
 * - Scene setup
 * - Engine loop (useFrame)
 * - Zustand store base
 * 
 * Cargado SIEMPRE. Sin lazy-loading.
 * Debe ser < 100KB comprimido.
 */

import { useEffect } from 'react'
import { Canvas, useThree } from '@react-three/fiber'
import { PerspectiveCamera, OrbitControls } from '@react-three/drei'
import * as THREE from 'three'
import EngineIntegration from '../EngineIntegration'

interface CoreEngineProps {
  cameraPosition?: [number, number, number]
  fov?: number
  shadows?: boolean
  onCameraReady?: (camera: THREE.Camera) => void
  children?: React.ReactNode
}

export default function CoreEngine({
  cameraPosition = [8, 4, 8],
  fov = 60,
  shadows = true,
  onCameraReady,
  children
}: CoreEngineProps) {
  return (
    <Canvas
      shadows={shadows}
      camera={{ position: cameraPosition, fov }}
      gl={{
        antialias: true,
        alpha: false,
        powerPreference: 'high-performance',
        toneMapping: THREE.ACESFilmicToneMapping,
        toneMappingExposure: 1.2
      }}
    >
      {/* Performance integration loop */}
      <EngineIntegration />

      {/* Cámara */}
      <CameraSetup 
        position={cameraPosition} 
        fov={fov}
        onReady={onCameraReady}
      />

      {/* Controles básicos - siempre presentes pero controlables */}
      <OrbitControls
        enableDamping
        dampingFactor={0.08}
        minDistance={3}
        maxDistance={30}
      />

      {/* Contenido lazy-loaded */}
      {children}
    </Canvas>
  )
}

/**
 * CameraSetup - Notifica cuando la cámara está lista
 */
function CameraSetup({
  position,
  fov,
  onReady
}: {
  position: [number, number, number]
  fov: number
  onReady?: (camera: THREE.Camera) => void
}) {
  const { camera } = useThree()

  useEffect(() => {
    if (camera && onReady) {
      onReady(camera)
    }
  }, [camera, onReady])

  return (
    <PerspectiveCamera
      makeDefault
      position={position}
      fov={fov}
    />
  )
}

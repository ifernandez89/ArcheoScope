'use client'

import { useEffect } from 'react'
import { useThree } from '@react-three/fiber'
import * as THREE from 'three'

interface CinematicLightingProps {
  sunPosition?: [number, number, number]
  sunIntensity?: number
  hemisphereIntensity?: number
  enableShadows?: boolean
}

export default function CinematicLighting({
  sunPosition = [10, 15, 5],
  sunIntensity = 2.5,
  hemisphereIntensity = 1.0,
  enableShadows = true
}: CinematicLightingProps) {
  const { gl, scene } = useThree()

  useEffect(() => {
    // Configurar tone mapping cinematográfico
    gl.toneMapping = THREE.ACESFilmicToneMapping
    gl.toneMappingExposure = 1.2
    gl.outputColorSpace = THREE.SRGBColorSpace
    
    // Habilitar sombras suaves
    if (enableShadows) {
      gl.shadowMap.enabled = true
      gl.shadowMap.type = THREE.PCFSoftShadowMap
    }
    
    console.log('🎬 Iluminación cinematográfica activada:', {
      toneMapping: 'ACESFilmic',
      exposure: 1.2,
      colorSpace: 'sRGB',
      shadows: enableShadows ? 'PCFSoft' : 'disabled'
    })
  }, [gl, enableShadows])

  return (
    <>
      {/* Sol direccional (key light) */}
      <directionalLight
        position={sunPosition}
        intensity={sunIntensity}
        castShadow={enableShadows}
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-far={50}
        shadow-camera-left={-25}
        shadow-camera-right={25}
        shadow-camera-top={25}
        shadow-camera-bottom={-25}
        shadow-bias={-0.0001}
        color="#ffffff"
      />
      
      {/* Luz hemisférica (fill light) */}
      <hemisphereLight
        args={['#87ceeb', '#8b7355', hemisphereIntensity]}
      />
      
      {/* Luz ambiental sutil */}
      <ambientLight intensity={0.3} color="#b0c4de" />
    </>
  )
}

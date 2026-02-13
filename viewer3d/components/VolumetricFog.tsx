'use client'

import { useEffect } from 'react'
import { useThree } from '@react-three/fiber'
import * as THREE from 'three'

interface VolumetricFogProps {
  color?: string
  near?: number
  far?: number
  density?: number
}

export default function VolumetricFog({
  color = '#87ceeb',
  near = 50,
  far = 300,
  density = 0.015
}: VolumetricFogProps) {
  const { scene } = useThree()

  useEffect(() => {
    // Configurar niebla exponencial (más realista que linear)
    scene.fog = new THREE.FogExp2(color, density)
    
    console.log('🌫️ Niebla volumétrica activada:', { color, density })

    return () => {
      scene.fog = null
    }
  }, [scene, color, density])

  return null
}

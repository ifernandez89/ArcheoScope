'use client'

import { useRef } from 'react'
import * as THREE from 'three'
import { useTexture } from '@react-three/drei'
import { getAssetPath } from '@/lib/paths'

interface CropCircleProps {
  type: 'julia' | 'galaxy' | 'toroid' | 'flower' | 'metatron'
  position: [number, number, number]
  scale?: number
  visible?: boolean
}

const CROP_CIRCLE_METADATA = {
  julia: { texture: '/textures/crop_circles/julia.png' },
  galaxy: { texture: '/textures/crop_circles/galaxy.png' },
  toroid: { texture: '/textures/crop_circles/toroid.png' },
  flower: { texture: '/textures/crop_circles/flower.png' },
  metatron: { texture: '/textures/crop_circles/metatron.png' }
}

/**
 * CropCircle - Versión simplificada y realista.
 * Representa patrones geométricos "aplastados" en el terreno (pasto/tierra).
 */
export default function CropCircle({ type, position, scale = 15, visible = true }: CropCircleProps) {
  const meta = CROP_CIRCLE_METADATA[type]
  const texture = useTexture(getAssetPath(meta.texture))

  if (!visible) return null

  return (
    <group position={position}>
      {/* 
        Círculo de Cosecha:
        - Casi a nivel de suelo (y=0.05) para evitar z-fighting.
        - Color oscuro/tierra para simular pasto aplastado u oscurecido.
        - Blending Multiply para integrarse con la textura subyacente.
      */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.05, 0]}>
        <planeGeometry args={[scale, scale]} />
        <meshStandardMaterial
          map={texture}
          transparent
          opacity={0.7}
          color="#424b28" // Verde oscuro/marrón para efecto de aplastamiento
          roughness={1}
          metalness={0}
          blending={THREE.MultiplyBlending}
          depthWrite={false}
        />
      </mesh>
      
      {/* Borde sutil para dar definición */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.02, 0]}>
        <planeGeometry args={[scale * 1.02, scale * 1.02]} />
        <meshBasicMaterial
          map={texture}
          transparent
          opacity={0.3}
          color="#000000"
          blending={THREE.MultiplyBlending}
          depthWrite={false}
        />
      </mesh>
    </group>
  )
}

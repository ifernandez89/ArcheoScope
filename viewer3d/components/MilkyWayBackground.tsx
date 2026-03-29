'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

export default function MilkyWayBackground() {
  const sphereRef = useRef<THREE.Mesh>(null)

  // UVMapping es el correcto para esfera skybox con BackSide
  const milkyWayTexture = useTexture(getAssetPath('/textures/2k_stars_milky_way.jpg'), (texture) => {
    texture.mapping = THREE.UVMapping
    texture.colorSpace = THREE.SRGBColorSpace
    texture.needsUpdate = true
  })

  useFrame((_, delta) => {
    if (sphereRef.current) {
      sphereRef.current.rotation.y += delta * 0.0008
    }
  })

  return (
    <mesh ref={sphereRef} renderOrder={-1}>
      {/* Radio 22000 — bien por fuera de Neptuno (~6010u) pero dentro del far plane */}
      <sphereGeometry args={[22000, 64, 64]} />
      <meshBasicMaterial
        map={milkyWayTexture}
        side={THREE.BackSide}
        depthWrite={false}
        depthTest={false}
        toneMapped={false}
      />
    </mesh>
  )
}

'use client'

import { useMemo, useEffect } from 'react'
import { useGLTF, useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

interface PumaPunkuBlockProps {
  position?: [number, number, number]
  scale?: number
  rotation?: [number, number, number]
}

export default function PumaPunkuBlock({
  position = [0, 0.3, 0],
  scale = 0.075,
  rotation = [0, 0, 0]
}: PumaPunkuBlockProps) {
  const { scene } = useGLTF(getAssetPath('/puma_punku_block.glb'))
  const rockTexture = useTexture(getAssetPath('/Rock-Texture-Surface.jpg'))

  const cloned = useMemo(() => scene.clone(true), [scene])

  // Aplicar textura en useEffect para garantizar que rockTexture ya cargó
  useEffect(() => {
    rockTexture.wrapS = THREE.RepeatWrapping
    rockTexture.wrapT = THREE.RepeatWrapping
    rockTexture.repeat.set(2, 2)
    rockTexture.needsUpdate = true

    cloned.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        child.castShadow = true
        child.receiveShadow = true
        child.material = new THREE.MeshStandardMaterial({
          map: rockTexture,
          roughness: 0.85,
          metalness: 0.05,
          color: new THREE.Color(0xb0a090),
        })
        ;(child.material as THREE.MeshStandardMaterial).needsUpdate = true
      }
    })
  }, [cloned, rockTexture])

  return (
    <primitive
      object={cloned}
      position={position}
      rotation={rotation}
      scale={[scale, scale, scale]}
    />
  )
}

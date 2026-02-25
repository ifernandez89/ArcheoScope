'use client'

/**
 * PumaPunkuBlock - Bloque H de Puma Punku con textura de roca
 * Se coloca en el suelo cuando el usuario visita Tiwanaku
 */

import { useRef, useEffect } from 'react'
import { useGLTF, useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

interface PumaPunkuBlockProps {
  position?: [number, number, number]
  scale?: number
  rotation?: [number, number, number]
}

export default function PumaPunkuBlock({
  position = [0, 0, 0],
  scale = 1,
  rotation = [0, 0, 0]
}: PumaPunkuBlockProps) {
  const groupRef = useRef<THREE.Group>(null)

  const { scene } = useGLTF(getAssetPath('/puma_punku_block.glb'))
  const rockTexture = useTexture(getAssetPath('/Rock-Texture-Surface.jpg'))

  // Clonar escena para evitar mutaciones del original
  const clonedScene = scene.clone()

  useEffect(() => {
    if (!clonedScene) return

    // Configurar textura de roca
    rockTexture.wrapS = THREE.RepeatWrapping
    rockTexture.wrapT = THREE.RepeatWrapping
    rockTexture.repeat.set(2, 2)

    clonedScene.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        child.castShadow = true
        child.receiveShadow = true

        // Aplicar textura de roca manteniendo la geometría del modelo
        child.material = new THREE.MeshStandardMaterial({
          map: rockTexture,
          roughness: 0.85,
          metalness: 0.05,
          color: new THREE.Color(0x9a8878), // tono piedra andina
        })
      }
    })
  }, [clonedScene, rockTexture])

  return (
    <group
      ref={groupRef}
      position={position}
      rotation={rotation}
      scale={[scale, scale, scale]}
    >
      <primitive object={clonedScene} />
    </group>
  )
}

useGLTF.preload(getAssetPath('/puma_punku_block.glb'))

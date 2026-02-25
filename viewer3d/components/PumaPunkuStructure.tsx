'use client'

import { useMemo } from 'react'
import { useGLTF } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

interface PumaPunkuStructureProps {
  position?: [number, number, number]
  scale?: number
  rotation?: [number, number, number]
}

export default function PumaPunkuStructure({
  position = [0, 0, 0],
  scale = 65.03,
  rotation = [0, 0, 0]
}: PumaPunkuStructureProps) {
  const { scene } = useGLTF(getAssetPath('/pm_structure.glb'))

  const { cloned, offsetY } = useMemo(() => {
    const cloned = scene.clone(true)
    cloned.scale.set(scale, scale, scale)
    cloned.updateMatrixWorld(true)

    const box = new THREE.Box3().setFromObject(cloned)
    const size = box.getSize(new THREE.Vector3())
    const minY = box.min.y
    console.log('[PumaPunkuStructure] size:', size.x.toFixed(2), size.y.toFixed(2), size.z.toFixed(2), '| minY:', minY.toFixed(2))

    cloned.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        child.castShadow = true
        child.receiveShadow = true
      }
    })

    return { cloned, offsetY: minY < 0 ? -minY : 0 }
  }, [scene, scale])

  return (
    <group position={[position[0], position[1] + offsetY, position[2]]} rotation={rotation}>
      <primitive object={cloned} />
    </group>
  )
}

useGLTF.preload(getAssetPath('/pm_structure.glb'))

/**
 * AvatarLayer - Capa de avatar (personaje, movimiento)
 * Responsabilidad: Gestionar avatar y su interacción
 */

'use client'

import { Suspense, lazy } from 'react'
import * as THREE from 'three'

const WalkableAvatar = lazy(() => import('../WalkableAvatar'))

interface AvatarLayerProps {
  enabled: boolean
  modelUrl: string | null
  avatarType: 'humanoid' | 'moai' | 'generic'
  camera: THREE.Camera | null
  onAvatarReady?: (avatar: THREE.Object3D) => void
}

export default function AvatarLayer({ 
  enabled,
  modelUrl,
  avatarType,
  camera,
  onAvatarReady
}: AvatarLayerProps) {
  if (!enabled || !modelUrl) return null
  
  return (
    <group name="avatar-layer">
      <Suspense fallback={null}>
        <WalkableAvatar
          modelPath={modelUrl}
        />
      </Suspense>
    </group>
  )
}

'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import type { HelpTip } from './HelpBubble'

export interface HelpZone {
  /** Unique key */
  id: string
  /** World position */
  position: [number, number, number]
  /** Trigger radius in world units */
  radius: number
  /** Tip data */
  tip: HelpTip
}

interface ProximityHelpDetectorProps {
  zones: HelpZone[]
  avatarPositionRef: React.RefObject<THREE.Vector3>
  onNearestChange: (zone: HelpZone | null) => void
}

/**
 * Runs inside the Canvas — checks every frame which help zone the avatar is nearest to.
 * Uses XZ-only distance (ignores Y/height) so flying avatars still trigger ground zones.
 * Calls onNearestChange with the closest zone within radius, or null if none.
 */
export default function ProximityHelpDetector({
  zones,
  avatarPositionRef,
  onNearestChange,
}: ProximityHelpDetectorProps) {
  const lastIdRef = useRef<string | null>(null)
  const frameSkip = useRef(0)

  useFrame(() => {
    // Check every 8 frames (~7.5 times/sec at 60fps)
    frameSkip.current++
    if (frameSkip.current < 8) return
    frameSkip.current = 0

    if (!avatarPositionRef.current) return
    const av = avatarPositionRef.current

    let nearest: HelpZone | null = null
    let nearestDist = Infinity

    for (const zone of zones) {
      // XZ-only distance — ignores height so flying avatars trigger ground zones
      const dx = av.x - zone.position[0]
      const dz = av.z - zone.position[2]
      const dist = Math.sqrt(dx * dx + dz * dz)

      if (dist < zone.radius && dist < nearestDist) {
        nearestDist = dist
        nearest = zone
      }
    }

    const newId = nearest?.id ?? null
    if (newId !== lastIdRef.current) {
      lastIdRef.current = newId
      onNearestChange(nearest)
    }
  })

  return null
}

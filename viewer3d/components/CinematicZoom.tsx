'use client'

import { useRef, useState } from 'react'
import { useThree, useFrame } from '@react-three/fiber'
import * as THREE from 'three'

/** Zoom cinematográfico al entrar a la escena — solo en modo órbita */
export default function CinematicZoom() {
  const { camera } = useThree()
  const startPos = useRef(new THREE.Vector3(15, 10, 15))
  const targetPos = useRef(new THREE.Vector3(5, 3, 5))
  const progress = useRef(0)
  const [isActive] = useState(true)

  useFrame((_, delta) => {
    if (progress.current < 1 && isActive) {
      progress.current += delta * 0.5
      const t = Math.min(progress.current, 1)
      const eased = 1 - Math.pow(1 - t, 3)
      camera.position.lerpVectors(startPos.current, targetPos.current, eased)
      camera.lookAt(0, 0, 0)
    }
  })

  return null
}

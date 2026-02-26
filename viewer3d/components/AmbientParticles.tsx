'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

/** Partículas ambientales sutiles para sensación de movimiento en la escena */
export default function AmbientParticles() {
  const particlesRef = useRef<THREE.Points>(null)

  const particlesGeometry = useMemo(() => {
    const geometry = new THREE.BufferGeometry()
    const count = 500
    const positions = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      const i3 = i * 3
      positions[i3]     = (Math.random() - 0.5) * 100
      positions[i3 + 1] = Math.random() * 10 + 1
      positions[i3 + 2] = (Math.random() - 0.5) * 100
    }
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    return geometry
  }, [])

  const particlesMaterial = useMemo(() => new THREE.PointsMaterial({
    size: 0.3,
    color: '#ffffff',
    transparent: true,
    opacity: 0.15,
    sizeAttenuation: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending
  }), [])

  useFrame((state) => {
    if (!particlesRef.current) return
    const positions = particlesRef.current.geometry.attributes.position.array as Float32Array
    for (let i = 0; i < positions.length; i += 3) {
      positions[i + 1] += Math.sin(state.clock.elapsedTime + i) * 0.001
      if (positions[i + 1] < 0.5) positions[i + 1] = 11
    }
    particlesRef.current.geometry.attributes.position.needsUpdate = true
  })

  return <points ref={particlesRef} geometry={particlesGeometry} material={particlesMaterial} />
}

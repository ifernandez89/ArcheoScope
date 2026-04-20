'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

/**
 * ToroidalSphere — Esfera cristalina con 3 toroides giratorios
 * Emerge del centro de Göbekli Tepe al completar los 4 altares
 */
export default function ToroidalSphere({
  position = [0, 0, 0] as [number, number, number],
  size = 9,
  visible = false
}: {
  position?: [number, number, number]
  size?: number
  visible?: boolean
}) {
  const groupRef = useRef<THREE.Group>(null)
  const toroid1Ref = useRef<THREE.Mesh>(null)
  const toroid2Ref = useRef<THREE.Mesh>(null)
  const toroid3Ref = useRef<THREE.Mesh>(null)
  const lightRef = useRef<THREE.PointLight>(null)
  const startTimeRef = useRef<number | null>(null)
  const ASCENT_DURATION = 20

  const { sphereGeo, torusGeo, torusGeo2, torusGeo3 } = useMemo(() => {
    const R = size
    const r = size * 0.1
    return {
      sphereGeo: new THREE.SphereGeometry(size * 1.05, 32, 32),
      torusGeo:  new THREE.TorusGeometry(R * 0.65, r, 16, 48),
      torusGeo2: new THREE.TorusGeometry(R * 0.65, r * 0.7, 12, 48),
      torusGeo3: new THREE.TorusGeometry(R * 0.65, r * 0.5, 12, 48),
    }
  }, [size])

  useFrame(({ clock }, delta) => {
    if (!visible || !groupRef.current) return

    if (startTimeRef.current === null) {
      startTimeRef.current = clock.elapsedTime
    }

    const elapsed = clock.elapsedTime - startTimeRef.current
    const t = clock.elapsedTime

    // Ascenso con easing
    const progress = Math.min(elapsed / ASCENT_DURATION, 1)
    const eased = Math.pow(progress, 1.5)
    groupRef.current.position.set(position[0], position[1] + eased * 200, position[2])

    // Fade in/out
    const opacity = progress < 0.05
      ? progress / 0.05
      : progress > 0.85 ? (1 - progress) / 0.15 : 1
    groupRef.current.scale.setScalar(opacity * (1 + Math.sin(t * 2) * 0.03))

    // Rotaciones
    if (toroid1Ref.current) { toroid1Ref.current.rotation.y += delta * 0.6; toroid1Ref.current.rotation.x += delta * 0.2 }
    if (toroid2Ref.current) { toroid2Ref.current.rotation.x += delta * 0.7; toroid2Ref.current.rotation.z += delta * 0.3 }
    if (toroid3Ref.current) { toroid3Ref.current.rotation.z += delta * 0.5; toroid3Ref.current.rotation.y -= delta * 0.3 }

    if (lightRef.current) {
      lightRef.current.intensity = (1.5 + Math.sin(t * 4) * 0.5) * opacity
    }
  })

  if (!visible) return null

  return (
    <group ref={groupRef} position={position}>
      {/* Esfera exterior cristalina */}
      <mesh geometry={sphereGeo}>
        <meshPhysicalMaterial
          color="#88ccff" transparent opacity={0.12}
          side={THREE.DoubleSide} roughness={0.02} metalness={0.05}
          transmission={0.9} thickness={0.5} ior={1.4}
        />
      </mesh>

      {/* 3 Toroides en ejes diferentes */}
      <mesh ref={toroid1Ref} geometry={torusGeo}>
        <meshPhysicalMaterial color="#44aaff" transparent opacity={0.55} emissive="#44aaff" emissiveIntensity={0.3} side={THREE.DoubleSide} />
      </mesh>
      <mesh ref={toroid2Ref} geometry={torusGeo2} rotation={[Math.PI / 2, 0, 0]}>
        <meshPhysicalMaterial color="#00ffcc" transparent opacity={0.45} emissive="#00ffcc" emissiveIntensity={0.3} side={THREE.DoubleSide} />
      </mesh>
      <mesh ref={toroid3Ref} geometry={torusGeo3} rotation={[Math.PI / 4, Math.PI / 4, 0]}>
        <meshPhysicalMaterial color="#ffffff" transparent opacity={0.3} emissive="#ffffff" emissiveIntensity={0.2} side={THREE.DoubleSide} />
      </mesh>

      {/* Núcleo */}
      <mesh>
        <sphereGeometry args={[size * 0.08, 16, 16]} />
        <meshBasicMaterial color="#ffffff" transparent opacity={0.9} />
      </mesh>

      {/* Luz pulsante */}
      <pointLight ref={lightRef} color="#44aaff" intensity={1.5} distance={size * 4} decay={2} />
    </group>
  )
}

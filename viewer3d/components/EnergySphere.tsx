'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

/**
 * EnergySphere - Esfera energética rosa con anillos rotativos
 * Aparece al completar las 5 misiones como símbolo de estabilización
 */
export default function EnergySphere({
  position = [0, 8, 0] as [number, number, number],
  size = 2,
  visible = false
}) {
  const groupRef = useRef<THREE.Group>(null)
  const ring1Ref = useRef<THREE.Mesh>(null)
  const ring2Ref = useRef<THREE.Mesh>(null)
  const ring3Ref = useRef<THREE.Mesh>(null)
  const outerRef = useRef<THREE.Mesh>(null)

  useFrame((_, delta) => {
    if (!groupRef.current || !visible) return
    // Anillos giran en ejes diferentes
    if (ring1Ref.current) ring1Ref.current.rotation.z += delta * 0.8
    if (ring2Ref.current) ring2Ref.current.rotation.x += delta * 0.6
    if (ring3Ref.current) ring3Ref.current.rotation.y += delta * 0.5
    // Esfera exterior pulsa
    if (outerRef.current) {
      const s = 1 + Math.sin(Date.now() * 0.001) * 0.03
      outerRef.current.scale.setScalar(s)
    }
  })

  if (!visible) return null

  return (
    <group ref={groupRef} position={position}>
      {/* Esfera central rosa brillante */}
      <mesh>
        <sphereGeometry args={[size * 0.4, 32, 32]} />
        <meshStandardMaterial
          color="#e040e0"
          emissive="#d030d0"
          emissiveIntensity={1.2}
          roughness={0.1}
          metalness={0.3}
        />
      </mesh>

      {/* Esfera exterior transparente grande */}
      <mesh ref={outerRef}>
        <sphereGeometry args={[size * 2.5, 32, 32]} />
        <meshPhysicalMaterial
          color="#c8a0e8"
          transparent
          opacity={0.08}
          side={THREE.DoubleSide}
          roughness={0.05}
          transmission={0.6}
        />
      </mesh>

      {/* Anillo 1 - horizontal, inclinado */}
      <mesh ref={ring1Ref} rotation={[0.3, 0, 0]}>
        <torusGeometry args={[size * 1.5, size * 0.06, 16, 64]} />
        <meshStandardMaterial
          color="#e060e0"
          emissive="#d040d0"
          emissiveIntensity={0.8}
          transparent
          opacity={0.7}
        />
      </mesh>

      {/* Anillo 2 - vertical */}
      <mesh ref={ring2Ref} rotation={[Math.PI / 2, 0.5, 0]}>
        <torusGeometry args={[size * 1.8, size * 0.05, 16, 64]} />
        <meshStandardMaterial
          color="#c050d0"
          emissive="#b040c0"
          emissiveIntensity={0.6}
          transparent
          opacity={0.6}
        />
      </mesh>

      {/* Anillo 3 - diagonal */}
      <mesh ref={ring3Ref} rotation={[0.8, 0, 1.2]}>
        <torusGeometry args={[size * 1.2, size * 0.04, 16, 64]} />
        <meshStandardMaterial
          color="#d070e0"
          emissive="#c060d0"
          emissiveIntensity={0.7}
          transparent
          opacity={0.65}
        />
      </mesh>

      {/* Luz central rosa */}
      <pointLight color="#e040e0" intensity={4} distance={25} decay={2} />
    </group>
  )
}

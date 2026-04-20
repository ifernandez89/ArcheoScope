'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

/**
 * ToroidalSphere — Esfera cristalina con tubo toroidal interior
 * Aparece en Göbekli Tepe al activar el sonido del escarabajo
 * 
 * Estructura:
 * - Esfera exterior transparente (cristal)
 * - Tubo toroidal interior girando (energía)
 * - Segundo toroide perpendicular (campo)
 * - Luz interna pulsante
 */
export default function ToroidalSphere({
  position = [0, 8, 0] as [number, number, number],
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
  const toroid4Ref = useRef<THREE.Mesh>(null)
  const toroid5Ref = useRef<THREE.Mesh>(null)
  const toroid6Ref = useRef<THREE.Mesh>(null)
  const lightRef = useRef<THREE.PointLight>(null)
  const startTimeRef = useRef<number | null>(null)
  const ASCENT_DURATION = 11 // segundos para llegar al cielo

  const { sphereGeo, torusGeo, torusGeo2, torusGeo3, torusGeo4, torusGeo5, torusGeo6 } = useMemo(() => {
    const R = size
    const r = size * 0.08
    const segments = 64
    return {
      sphereGeo: new THREE.SphereGeometry(size * 1.1, 64, 64),
      torusGeo:  new THREE.TorusGeometry(R * 0.7, r, 24, segments),
      torusGeo2: new THREE.TorusGeometry(R * 0.7, r, 24, segments),
      torusGeo3: new THREE.TorusGeometry(R * 0.7, r, 24, segments),
      torusGeo4: new THREE.TorusGeometry(R * 0.7, r, 24, segments),
      torusGeo5: new THREE.TorusGeometry(R * 0.7, r, 24, segments),
      torusGeo6: new THREE.TorusGeometry(R * 0.7, r, 24, segments),
    }
  }, [size])

  useFrame(({ clock }, delta) => {
    if (!visible || !groupRef.current) return

    // Registrar tiempo de inicio
    if (startTimeRef.current === null) {
      startTimeRef.current = clock.elapsedTime
    }

    const elapsed = clock.elapsedTime - startTimeRef.current
    const t = clock.elapsedTime

    // Ascenso: empieza en y=0 (piso), sube 300 unidades en ASCENT_DURATION seg
    const progress = Math.min(elapsed / ASCENT_DURATION, 1)
    const eased = Math.pow(progress, 1.5) // Un poco más rápido hacia el final
    groupRef.current.position.set(
      position[0],
      position[1] + eased * 300,
      position[2]
    )

    // Fade in rápido al inicio, fade out al final
    const opacity = progress < 0.05
      ? progress / 0.05
      : progress > 0.9
        ? (1 - progress) / 0.1
        : 1
    
    // Escala pulsante majestuosa
    const pulse = 1 + Math.sin(t * 2) * 0.05
    groupRef.current.scale.setScalar(opacity * pulse)

    // Rotaciones diferenciadas para efecto Merkaba
    if (toroid1Ref.current) toroid1Ref.current.rotation.y += delta * 0.8
    if (toroid2Ref.current) toroid2Ref.current.rotation.x += delta * 0.9
    if (toroid3Ref.current) toroid3Ref.current.rotation.z += delta * 1.1
    if (toroid4Ref.current) toroid4Ref.current.rotation.y -= delta * 0.7
    if (toroid5Ref.current) toroid5Ref.current.rotation.x -= delta * 1.2
    if (toroid6Ref.current) toroid6Ref.current.rotation.z -= delta * 0.85

    if (lightRef.current) {
      lightRef.current.intensity = (2.0 + Math.sin(t * 4) * 0.5) * opacity
    }
  })

  if (!visible) return null

  // Material cristalino — igual que el Merkaba
  const crystalMat = (
    <meshPhysicalMaterial
      color="#88ccff"
      transparent
      opacity={0.15}
      side={THREE.DoubleSide}
      roughness={0.01}
      metalness={0.1}
      transmission={0.95}
      thickness={1}
      ior={1.5}
      envMapIntensity={3}
    />
  )

  // Material del tubo toroidal — más visible, energético
  const torusMat = (color: string, opacity: number) => (
    <meshPhysicalMaterial
      color={color}
      transparent
      opacity={opacity}
      side={THREE.DoubleSide}
      roughness={0.05}
      metalness={0.5}
      transmission={0.4}
      thickness={1.5}
      ior={1.8}
      emissive={color}
      emissiveIntensity={2.5}
    />
  )

  return (
    <group ref={groupRef} position={position}>
      {/* Esfera exterior cristalina */}
      <mesh geometry={sphereGeo}>
        {crystalMat}
      </mesh>

      {/* Geometría Sagrada Interconectada (6 Toroides en diferentes ejes) */}
      <mesh ref={toroid1Ref} geometry={torusGeo}>
        {torusMat('#44aaff', 0.6)}
      </mesh>
      <mesh ref={toroid2Ref} geometry={torusGeo2} rotation={[Math.PI / 2, 0, 0]}>
        {torusMat('#00ffcc', 0.5)}
      </mesh>
      <mesh ref={toroid3Ref} geometry={torusGeo3} rotation={[0, 0, Math.PI / 2]}>
        {torusMat('#ffffff', 0.4)}
      </mesh>
      <mesh ref={toroid4Ref} geometry={torusGeo4} rotation={[Math.PI / 4, Math.PI / 4, 0]}>
        {torusMat('#44aaff', 0.45)}
      </mesh>
      <mesh ref={toroid5Ref} geometry={torusGeo5} rotation={[-Math.PI / 4, Math.PI / 4, 0]}>
        {torusMat('#00ffcc', 0.4)}
      </mesh>
      <mesh ref={toroid6Ref} geometry={torusGeo6} rotation={[0, Math.PI / 4, Math.PI / 4]}>
        {torusMat('#ffffff', 0.35)}
      </mesh>

      {/* Núcleo central — pequeña esfera de energía pura */}
      <mesh>
        <sphereGeometry args={[size * 0.1, 32, 32]} />
        <meshBasicMaterial color="#ffffff" transparent opacity={1} />
      </mesh>

      {/* Luz interna pulsante potente */}
      <pointLight
        ref={lightRef}
        color="#88ccff"
        intensity={2}
        distance={size * 10}
        decay={1.5}
      />
    </group>
  )
}

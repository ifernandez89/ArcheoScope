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
  size = 9,  // radio del toroide = tamaño del crop circle / scale
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
  const opacityRef = useRef(0)

  // Geometrías en useMemo
  const { sphereGeo, torusGeo, torusGeo2, torusGeo3 } = useMemo(() => {
    const R = size          // radio mayor del toroide
    const r = size * 0.12  // radio del tubo

    return {
      // Esfera exterior
      sphereGeo: new THREE.SphereGeometry(size * 1.05, 48, 48),
      // Toroide principal (horizontal)
      torusGeo: new THREE.TorusGeometry(R * 0.65, r, 24, 96),
      // Toroide secundario (vertical)
      torusGeo2: new THREE.TorusGeometry(R * 0.65, r * 0.7, 20, 96),
      // Toroide terciario (diagonal)
      torusGeo3: new THREE.TorusGeometry(R * 0.65, r * 0.5, 16, 96),
    }
  }, [size])

  useFrame(({ clock }, delta) => {
    if (!visible) return

    // Fade in suave al aparecer
    if (opacityRef.current < 1) {
      opacityRef.current = Math.min(1, opacityRef.current + delta * 0.3)
    }

    const t = clock.elapsedTime

    // Rotaciones independientes de cada toroide
    if (toroid1Ref.current) {
      toroid1Ref.current.rotation.y += delta * 0.4
      toroid1Ref.current.rotation.x += delta * 0.15
    }
    if (toroid2Ref.current) {
      toroid2Ref.current.rotation.x += delta * 0.5
      toroid2Ref.current.rotation.z += delta * 0.2
    }
    if (toroid3Ref.current) {
      toroid3Ref.current.rotation.z += delta * 0.35
      toroid3Ref.current.rotation.y -= delta * 0.25
    }

    // Luz pulsante sincronizada con el aleteo (80Hz → visual ~1Hz)
    if (lightRef.current) {
      lightRef.current.intensity = (0.8 + Math.sin(t * 6.28) * 0.4) * opacityRef.current
    }

    // Escala de respiración suave del grupo
    if (groupRef.current) {
      const breathe = 1 + Math.sin(t * 1.2) * 0.02
      groupRef.current.scale.setScalar(breathe * opacityRef.current)
    }
  })

  if (!visible) return null

  // Material cristalino — igual que el Merkaba
  const crystalMat = (
    <meshPhysicalMaterial
      color="#88ccff"
      transparent
      opacity={0.12}
      side={THREE.DoubleSide}
      roughness={0.02}
      metalness={0.05}
      transmission={0.9}
      thickness={0.5}
      ior={1.4}
      envMapIntensity={2}
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
      metalness={0.3}
      transmission={0.6}
      thickness={1}
      ior={1.6}
      emissive={color}
      emissiveIntensity={0.15}
    />
  )

  return (
    <group ref={groupRef} position={position}>
      {/* Esfera exterior cristalina */}
      <mesh geometry={sphereGeo}>
        {crystalMat}
      </mesh>

      {/* Toroide principal — horizontal, azul */}
      <mesh ref={toroid1Ref} geometry={torusGeo}>
        {torusMat('#44aaff', 0.55)}
      </mesh>

      {/* Toroide secundario — vertical, cyan */}
      <mesh ref={toroid2Ref} geometry={torusGeo2} rotation={[Math.PI / 2, 0, 0]}>
        {torusMat('#00ffcc', 0.45)}
      </mesh>

      {/* Toroide terciario — diagonal, blanco */}
      <mesh ref={toroid3Ref} geometry={torusGeo3} rotation={[Math.PI / 4, Math.PI / 4, 0]}>
        {torusMat('#ffffff', 0.3)}
      </mesh>

      {/* Núcleo central — pequeña esfera de energía */}
      <mesh>
        <sphereGeometry args={[size * 0.08, 16, 16]} />
        <meshBasicMaterial color="#ffffff" transparent opacity={0.9} />
      </mesh>

      {/* Luz interna pulsante */}
      <pointLight
        ref={lightRef}
        color="#44aaff"
        intensity={0.8}
        distance={size * 4}
        decay={2}
      />
    </group>
  )
}

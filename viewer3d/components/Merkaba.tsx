'use client'

import { useRef, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

/**
 * Merkaba - Dos tetraedros interpenetrados (estrella tetraédrica)
 * Un tetraedro apunta hacia arriba, el otro hacia abajo, rotados 180°
 * Gira lentamente en el aire
 */
export default function Merkaba({
  position = [0, 12, 0] as [number, number, number],
  size = 3,
  color = '#ffd700',
  speed = 0.4,
  clickable = false,
  onActivate
}: {
  position?: [number, number, number]
  size?: number
  color?: string
  speed?: number
  clickable?: boolean
  onActivate?: () => void
}) {
  const groupRef = useRef<THREE.Group>(null)
  const [spinning, setSpinning] = useState(true)
  const [activated, setActivated] = useState(false)

  useFrame((_, delta) => {
    if (groupRef.current && spinning) {
      groupRef.current.rotation.y += delta * speed
    }
  })

  const handleClick = (e: any) => {
    if (!clickable || activated) return
    e.stopPropagation()
    setSpinning(false)
    setActivated(true)
    if (onActivate) onActivate()
  }

  // Tetraedro regular: punta arriba, base equilátera abajo
  const h = size * 1.2 // altura total
  const base = size     // radio de la base

  // Tetraedro apuntando ARRIBA (punta en +Y)
  const upVerts: [number, number, number][] = [
    [0, h, 0],                                              // punta arriba
    [-base, -h * 0.33, base * 0.577],                       // base izq-frente
    [ base, -h * 0.33, base * 0.577],                       // base der-frente
    [0, -h * 0.33, -base * 1.155],                          // base atrás
  ]

  // Tetraedro apuntando ABAJO (punta en -Y)
  const downVerts: [number, number, number][] = [
    [0, -h, 0],                                             // punta abajo
    [-base, h * 0.33, -base * 0.577],                       // base izq-atrás
    [ base, h * 0.33, -base * 0.577],                       // base der-atrás
    [0, h * 0.33, base * 1.155],                            // base frente
  ]

  // Caras de un tetraedro: 4 triángulos
  const faces = [
    [0, 1, 2],
    [0, 2, 3],
    [0, 3, 1],
    [1, 3, 2],
  ]

  const buildGeo = (verts: [number, number, number][]) => {
    const positions: number[] = []
    for (const [a, b, c] of faces) {
      positions.push(...verts[a], ...verts[b], ...verts[c])
    }
    const geo = new THREE.BufferGeometry()
    geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3))
    geo.computeVertexNormals()
    return geo
  }

  const upGeo   = buildGeo(upVerts)
  const downGeo = buildGeo(downVerts)

  const mat = (
    <meshPhysicalMaterial
      color="#e8e8f0"
      transparent
      opacity={0.25}
      side={THREE.DoubleSide}
      roughness={0.05}
      metalness={0.1}
      transmission={0.85}
      thickness={1.5}
      ior={1.55}
      envMapIntensity={1.5}
    />
  )

  return (
    <group ref={groupRef} position={position}
      onClick={handleClick}
      onPointerOver={() => { if (clickable && !activated) document.body.style.cursor = 'pointer' }}
      onPointerOut={() => { document.body.style.cursor = 'default' }}
    >
      {/* Tetraedro superior */}
      <mesh geometry={upGeo}>{mat}</mesh>
      {/* Tetraedro inferior */}
      <mesh geometry={downGeo}>{mat}</mesh>

      {/* Aristas del tetraedro superior */}
      {faces.map(([a, b, c], i) => (
        <lineSegments key={`u-${i}`}>
          <edgesGeometry args={[new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(...upVerts[a]),
            new THREE.Vector3(...upVerts[b]),
            new THREE.Vector3(...upVerts[c]),
          ])]} />
          <lineBasicMaterial color="#c0c0d0" transparent opacity={0.4} />
        </lineSegments>
      ))}

      {/* Aristas del tetraedro inferior */}
      {faces.map(([a, b, c], i) => (
        <lineSegments key={`d-${i}`}>
          <edgesGeometry args={[new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(...downVerts[a]),
            new THREE.Vector3(...downVerts[b]),
            new THREE.Vector3(...downVerts[c]),
          ])]} />
          <lineBasicMaterial color="#c0c0d0" transparent opacity={0.4} />
        </lineSegments>
      ))}

      {/* Luz interna cristalina */}
      <pointLight color="#e0e0ff" intensity={0.8} distance={15} decay={2} />
    </group>
  )
}

'use client'

import { useRef, useState, useMemo } from 'react'
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

  // Geometrías en useMemo para evitar recalcular en cada render
  const { upGeo, downGeo, upVerts, downVerts, faces } = useMemo(() => {
    const h2 = size * 1.2
    const b = size

    const uVerts: [number, number, number][] = [
      [0, h2, 0],
      [-b, -h2 * 0.33, b * 0.577],
      [ b, -h2 * 0.33, b * 0.577],
      [0, -h2 * 0.33, -b * 1.155],
    ]
    const dVerts: [number, number, number][] = [
      [0, -h2, 0],
      [-b, h2 * 0.33, -b * 0.577],
      [ b, h2 * 0.33, -b * 0.577],
      [0, h2 * 0.33, b * 1.155],
    ]
    const f = [[0,1,2],[0,2,3],[0,3,1],[1,3,2]]

    const buildGeo = (verts: [number, number, number][]) => {
      const positions: number[] = []
      for (const [a, bc, c] of f) {
        positions.push(...verts[a], ...verts[bc], ...verts[c])
      }
      const geo = new THREE.BufferGeometry()
      geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3))
      geo.computeVertexNormals()
      return geo
    }

    return { upGeo: buildGeo(uVerts), downGeo: buildGeo(dVerts), upVerts: uVerts, downVerts: dVerts, faces: f }
  }, [size])

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

      {/* Esfera invisible para capturar clicks */}
      <mesh>
        <sphereGeometry args={[size * 2, 8, 8]} />
        <meshBasicMaterial transparent opacity={0} />
      </mesh>

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

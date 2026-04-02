'use client'

import { useMemo } from 'react'
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

/**
 * OlmecCave - Cueva olmeca construida con:
 * - Arco de rocas formando la entrada (visible)
 * - Túnel cilíndrico BackSide (profundidad real)
 * - Rocas decorativas alrededor
 */

function noise(x: number, z: number): number {
  return Math.sin(x * 0.8 + z * 0.5) * 0.5
       + Math.sin(x * 1.7 - z * 1.2) * 0.3
       + Math.cos(x * 0.4 + z * 2.1) * 0.2
}

export default function OlmecCave() {
  const rockTex = useTexture(getAssetPath('/textures/textura_volcanica.jpg'))
  rockTex.wrapS = rockTex.wrapT = THREE.RepeatWrapping
  rockTex.repeat.set(3, 2)

  // ── Rocas del arco de entrada (semicírculo de piedras) ────────────────────
  const archRocks = useMemo(() => {
    const rocks: { pos: [number, number, number]; scale: [number, number, number]; rot: [number, number, number] }[] = []
    const count = 12
    for (let i = 0; i < count; i++) {
      const angle = (i / (count - 1)) * Math.PI // semicírculo
      const radius = 4.5
      const x = Math.cos(angle) * radius
      const y = Math.sin(angle) * radius + 0.5
      const n = noise(i * 1.3, i * 0.7)
      const sx = 1.8 + Math.abs(n) * 1.2
      const sy = 1.5 + Math.abs(n) * 0.8
      const sz = 2.5 + Math.abs(n) * 1.0
      rocks.push({
        pos: [x, y, n * 0.3],
        scale: [sx, sy, sz],
        rot: [n * 0.2, n * 0.3, angle - Math.PI / 2]
      })
    }
    return rocks
  }, [])

  // ── Rocas superiores (techo de la cueva) ──────────────────────────────────
  const roofRocks = useMemo(() => {
    const rocks: { pos: [number, number, number]; scale: [number, number, number]; rot: [number, number, number] }[] = []
    for (let i = 0; i < 8; i++) {
      const angle = 0.3 + (i / 7) * (Math.PI - 0.6)
      const radius = 3.0
      const x = Math.cos(angle) * radius
      const y = Math.sin(angle) * radius + 1.5
      const n = noise(i * 2.1, i * 1.3)
      rocks.push({
        pos: [x, y, -1.5 + n * 0.5],
        scale: [1.5 + Math.abs(n) * 0.8, 1.2 + Math.abs(n) * 0.6, 2.0 + Math.abs(n) * 0.8],
        rot: [n * 0.3, n * 0.2, angle - Math.PI / 2 + n * 0.15]
      })
    }
    return rocks
  }, [])

  // ── Rocas de base (piso de la entrada) ────────────────────────────────────
  const baseRocks = useMemo(() => [
    [-5.5, 0.3, 1.5,  2.0, 0.8, 1.6, 0.3],
    [ 5.5, 0.3, 1.5,  1.8, 0.9, 1.7, -0.4],
    [-4.0, 0.2, 3.5,  1.5, 0.7, 1.3, 0.8],
    [ 4.0, 0.2, 3.5,  1.6, 0.6, 1.4, -0.6],
    [-2.0, 0.15, 4.5, 1.0, 0.5, 0.9, 1.1],
    [ 2.0, 0.15, 4.5, 1.1, 0.5, 1.0, -0.9],
    [ 0.0, 0.1, 5.0,  0.8, 0.4, 0.7, 0.2],
    [-7.0, 0.2, 0.5,  1.3, 0.6, 1.1, 0.5],
    [ 7.0, 0.2, 0.5,  1.2, 0.5, 1.0, -0.3],
  ], [])

  const rockMat = <meshStandardMaterial map={rockTex} color="#7a6a58" roughness={0.95} metalness={0.02} />

  return (
    <group position={[-28, 0, 0]} scale={[1.4, 1.4, 2.8]}>

      {/* Fondo oscuro interior */}
      <mesh position={[0, 3, -2]}>
        <circleGeometry args={[4, 24]} />
        <meshBasicMaterial color="#020101" />
      </mesh>

      {/* Arco de rocas - entrada principal */}
      {archRocks.map((rock, i) => (
        <mesh key={`arch-${i}`} position={rock.pos} scale={rock.scale} rotation={rock.rot} castShadow>
          <dodecahedronGeometry args={[1, 1]} />
          {rockMat}
        </mesh>
      ))}

      {/* Rocas del techo (segunda capa, más adentro) */}
      {roofRocks.map((rock, i) => (
        <mesh key={`roof-${i}`} position={rock.pos} scale={rock.scale} rotation={rock.rot} castShadow>
          <dodecahedronGeometry args={[1, 0]} />
          {rockMat}
        </mesh>
      ))}

      {/* Rocas de base */}
      {baseRocks.map(([x, y, z, sx, sy, sz, ry], i) => (
        <mesh key={`base-${i}`} position={[x, y, z]} scale={[sx, sy, sz]} rotation={[0, ry, 0]} castShadow>
          <dodecahedronGeometry args={[1, 0]} />
          {rockMat}
        </mesh>
      ))}

      {/* Luz interior naranja */}
      <pointLight position={[0, 3, -3]} color="#ff5500" intensity={2} distance={12} decay={2} />
      {/* Luz exterior suave */}
      <pointLight position={[0, 5, 3]} color="#ffe0b0" intensity={0.5} distance={10} />
    </group>
  )
}

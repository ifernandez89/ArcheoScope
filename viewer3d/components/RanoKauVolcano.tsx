'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

export type VolcanoState = 'dormant' | 'active' | 'erupting'

interface RanoKauVolcanoProps {
  state?: VolcanoState
}

// Simplex-like noise 2D (sin dependencias externas)
function noise2D(x: number, z: number): number {
  return Math.sin(x * 0.31 + z * 0.17) * 0.5
       + Math.sin(x * 0.73 - z * 0.41) * 0.3
       + Math.sin(x * 1.27 + z * 0.89) * 0.15
       + Math.cos(x * 0.53 + z * 1.13) * 0.05
}

export default function RanoKauVolcano({ state = 'dormant' }: RanoKauVolcanoProps) {
  const lavaRef    = useRef<THREE.Mesh>(null)
  const lightRef   = useRef<THREE.PointLight>(null)
  const partRef    = useRef<THREE.InstancedMesh>(null)
  const timeRef    = useRef(0)
  const tempObj    = useMemo(() => new THREE.Object3D(), [])
  const tempColor  = useMemo(() => new THREE.Color(), [])

  // Textura volcánica
  const rockTex = useTexture(getAssetPath('/textures/textura_volcanica.jpg'))
  rockTex.wrapS = rockTex.wrapT = THREE.RepeatWrapping
  rockTex.repeat.set(3, 2)

  const MAX_P = state === 'erupting' ? 180 : state === 'active' ? 50 : 0

  // ── Geometría del volcán con cráter hundido ───────────────────────────────
  const volcanoGeo = useMemo(() => {
    const HEIGHT = 36
    const TOP = HEIGHT / 2
    const geo = new THREE.ConeGeometry(30, HEIGHT, 48, 12)
    const pos = geo.attributes.position as THREE.BufferAttribute

    // Agregar vertex colors para oscurecer la cima
    const colors = new Float32Array(pos.count * 3)

    for (let i = 0; i < pos.count; i++) {
      let x = pos.getX(i)
      let y = pos.getY(i)
      let z = pos.getZ(i)
      const r = Math.sqrt(x * x + z * z)

      // 1. Base más ancha que la cima
      const heightFactor = (y + TOP) / HEIGHT // 0=base, 1=cima
      const widthScale = 1 + (1 - heightFactor) * 0.55
      x *= widthScale
      z *= widthScale

      // 2. Curvar los lados (convexo hacia afuera)
      const curve = Math.pow(r + 0.001, 1.15)
      x += x * curve * 0.018
      z += z * curve * 0.018

      // 3. Noise lateral para irregularidad
      const angle = Math.atan2(z, x)
      const n = noise2D(x * 0.12, z * 0.12)
      const lateralNoise = n * 3.0 * (1 - heightFactor * 0.7)
      x += lateralNoise * (x / (r + 0.001))
      z += lateralNoise * (z / (r + 0.001))

      // 4. Cráter hundido amplio con borde irregular
      const rFinal = Math.sqrt(x * x + z * z)
      if (y > TOP * 0.5 && rFinal < 16) {
        const craterT = Math.max(0, 1 - rFinal / 14)
        const rimNoise = Math.sin(angle * 6) * Math.cos(angle * 4 + 0.8) * 1.5
        const dip = craterT * craterT * 18 - rimNoise * craterT * 0.5
        y -= dip
      }

      pos.setX(i, x)
      pos.setY(i, y)
      pos.setZ(i, z)

      // 5. Vertex color: negro en cima, marrón en base
      const t = Math.max(0, Math.min(1, (y + TOP) / HEIGHT))
      // Arriba: gris oscuro/negro (ceniza). Abajo: marrón volcánico
      const r2 = 0.18 + t * 0.32
      const g2 = 0.12 + t * 0.22
      const b2 = 0.08 + t * 0.12
      colors[i * 3]     = r2
      colors[i * 3 + 1] = g2
      colors[i * 3 + 2] = b2
    }

    pos.needsUpdate = true
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3))
    geo.computeVertexNormals()
    return geo
  }, [])

  // Lava en el fondo del cráter
  const lavaGeo = useMemo(() => new THREE.CircleGeometry(9, 28), [])

  // ── Pool de partículas ────────────────────────────────────────────────────
  type P = { x: number; y: number; z: number; vx: number; vy: number; vz: number; life: number; maxLife: number; size: number; smoke: boolean }
  const pool = useRef<P[]>([])

  const spawn = (p: P) => {
    const a = Math.random() * Math.PI * 2
    const r = Math.random() * 2.5
    p.x = Math.cos(a) * r; p.y = 0; p.z = Math.sin(a) * r
    const spd = state === 'erupting' ? 8 + Math.random() * 10 : 1.5 + Math.random() * 2.5
    p.vx = (Math.random() - 0.5) * spd * 0.35
    p.vy = spd
    p.vz = (Math.random() - 0.5) * spd * 0.35
    p.maxLife = state === 'erupting' ? 1 + Math.random() * 1.5 : 2.5 + Math.random() * 3
    p.life = p.maxLife
    p.size = state === 'erupting' ? 0.25 + Math.random() * 0.5 : 0.5 + Math.random() * 1.0
    p.smoke = Math.random() > 0.35
  }

  if (pool.current.length === 0 && MAX_P > 0) {
    for (let i = 0; i < MAX_P; i++) {
      const p: P = { x: 0, y: 0, z: 0, vx: 0, vy: 0, vz: 0, life: 0, maxLife: 1, size: 1, smoke: false }
      spawn(p)
      p.life = Math.random() * p.maxLife
      pool.current.push(p)
    }
  }

  useFrame((_, delta) => {
    timeRef.current += delta

    // Lava pulsante
    if (lavaRef.current && state !== 'dormant') {
      const mat = lavaRef.current.material as THREE.MeshStandardMaterial
      mat.emissiveIntensity = 0.65 + Math.sin(timeRef.current * 3) * 0.3
    }

    // Luz
    if (lightRef.current) {
      lightRef.current.intensity = state === 'erupting'
        ? 14 + Math.sin(timeRef.current * 7) * 7
        : state === 'active'
          ? 4 + Math.sin(timeRef.current * 2) * 1.5
          : 0
    }

    if (!partRef.current || MAX_P === 0) return

    for (let i = 0; i < pool.current.length; i++) {
      const p = pool.current[i]
      p.life -= delta
      if (p.life <= 0) { spawn(p); continue }

      p.vy -= delta * (p.smoke ? 0.15 : 5.5)
      p.vx += (Math.random() - 0.5) * delta * 0.5
      p.vz += (Math.random() - 0.5) * delta * 0.5
      p.x += p.vx * delta
      p.y += p.vy * delta
      p.z += p.vz * delta

      const t = p.life / p.maxLife
      const sc = p.smoke ? p.size * (1 + (1 - t) * 1.2) : p.size * t
      tempObj.position.set(p.x, p.y, p.z)
      tempObj.scale.setScalar(Math.max(0.01, sc))
      tempObj.updateMatrix()
      partRef.current.setMatrixAt(i, tempObj.matrix)

      // Lava: naranja brillante → rojo. Ceniza: gris oscuro
      if (p.smoke) {
        const g = 0.18 + t * 0.28
        tempColor.setRGB(g + 0.04, g, g)
      } else {
        tempColor.setRGB(1.0, 0.18 + t * 0.42, 0.0)
      }
      partRef.current.setColorAt(i, tempColor)
    }
    partRef.current.instanceMatrix.needsUpdate = true
    if (partRef.current.instanceColor) partRef.current.instanceColor.needsUpdate = true
  })

  // Cima del cono: altura/2 = 18, cráter hunde ~14 unidades en el centro
  const CRATER_Y = 6

  return (
    <group position={[-55, 0, 55]} scale={[1, 2, 1]}>

      {/* Cuerpo del volcán con textura + vertex colors */}
      <mesh geometry={volcanoGeo} castShadow receiveShadow>
        <meshStandardMaterial
          map={rockTex}
          vertexColors
          roughness={0.92}
          metalness={0.04}
        />
      </mesh>

      {/* Lava en el cráter hundido */}
      {state !== 'dormant' && (
        <mesh
          ref={lavaRef}
          geometry={lavaGeo}
          position={[0, CRATER_Y, 0]}
          rotation={[-Math.PI / 2, 0, 0]}
        >
          <meshStandardMaterial
            color="#ff3300"
            emissive="#ff1100"
            emissiveIntensity={0.8}
            roughness={0.1}
          />
        </mesh>
      )}

      {/* Luz de lava */}
      <pointLight
        ref={lightRef}
        position={[0, CRATER_Y + 4, 0]}
        color="#ff5500"
        intensity={0}
        distance={100}
        decay={2}
      />

      {/* Partículas de lava/ceniza */}
      {MAX_P > 0 && (
        <instancedMesh
          ref={partRef}
          args={[undefined, undefined, MAX_P]}
          position={[0, CRATER_Y + 0.5, 0]}
        >
          <sphereGeometry args={[0.5, 5, 5]} />
          <meshBasicMaterial vertexColors transparent opacity={0.88} depthWrite={false} />
        </instancedMesh>
      )}
    </group>
  )
}

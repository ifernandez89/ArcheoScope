'use client'

/**
 * AsteroidBelt3D — Cinturón de asteroides con modelos GLB reales
 *
 * Estrategia de rendimiento:
 * - 10 modelos distintos, cada uno instanciado N veces
 * - Total: ~800 asteroides distribuidos en banda 2.2–3.2 AU
 * - Rotación individual por frame usando offsets aleatorios
 * - Escala, inclinación y posición radial procedurales con seed fijo
 */

import { useRef, useMemo, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import { useGLTF, useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

const SCALE         = 200          // AU → unidades de escena
const INNER_AU      = 2.2
const OUTER_AU      = 3.2
const TOTAL         = 1600          // asteroides totales
const MODEL_COUNT   = 10
const PER_MODEL     = Math.floor(TOTAL / MODEL_COUNT)  // 80 por modelo

// Velocidad orbital media del cinturón (rad/s simulados)
// Período medio ~4.5 años → ω = 2π / (4.5 * 365.25 * 86400) * TIME_SCALE
// Con TIME_SCALE = 3600 (1s = 1h): ω ≈ 0.0000397 rad/s
const ORBITAL_SPEED = 0.0000397

// Seed determinista para posiciones consistentes entre renders
function seededRandom(seed: number): number {
  const x = Math.sin(seed + 1) * 43758.5453123
  return x - Math.floor(x)
}

// ── Componente por modelo ─────────────────────────────────────────────────────

function AsteroidInstances({ modelIndex, count }: { modelIndex: number; count: number }) {
  const path = getAssetPath(`/models/asteroids/${modelIndex + 1}.glb`)
  const { scene } = useGLTF(path)

  // Texturas específicas por modelo (Albedo + Normal + MetallicSmoothness)
  const n = modelIndex + 1
  const albedo   = useTexture(getAssetPath(`/models/asteroids/textures/Asteroid${n}_AlbedoTransparency.png`))
  const normalMap = useTexture(getAssetPath(`/models/asteroids/textures/Asteroid${n}_Normal.png`))
  const metalMap  = useTexture(getAssetPath(`/models/asteroids/textures/Asteroid${n}_MetallicSmoothness.png`))

  // Extraer geometría del GLB y crear material con texturas reales
  const { geometry, material } = useMemo(() => {
    let geo: THREE.BufferGeometry | null = null

    scene.traverse((child) => {
      if (!geo && child instanceof THREE.Mesh) {
        geo = child.geometry.clone()
      }
    })

    // Material PBR con las 3 texturas
    const mat = new THREE.MeshStandardMaterial({
      map:          albedo,
      normalMap:    normalMap,
      metalnessMap: metalMap,
      roughnessMap: metalMap,   // canal G de MetallicSmoothness = roughness invertido
      metalness:    0.4,
      roughness:    0.8,
    })

    return {
      geometry: geo ?? new THREE.SphereGeometry(1, 6, 6),
      material: mat
    }
  }, [scene, albedo, normalMap, metalMap])

  // Datos orbitales por instancia (seed fijo por modelIndex)
  const instanceData = useMemo(() => {
    return Array.from({ length: count }, (_, i) => {
      const seed = modelIndex * 1000 + i
      const r       = INNER_AU + seededRandom(seed)      * (OUTER_AU - INNER_AU)
      const angle0  = seededRandom(seed + 1)             * Math.PI * 2
      const tilt    = (seededRandom(seed + 2) - 0.5)    * 0.35   // ±10° inclinación
      const scale   = 0.8 + seededRandom(seed + 3)      * 2.5    // tamaño variado
      const rotSpeedX = (seededRandom(seed + 4) - 0.5)  * 0.8
      const rotSpeedY = (seededRandom(seed + 5) - 0.5)  * 0.8
      const rotSpeedZ = (seededRandom(seed + 6) - 0.5)  * 0.8
      // Velocidad orbital ligeramente variable (ley de Kepler: más lejos = más lento)
      const orbSpeed  = ORBITAL_SPEED * Math.pow(INNER_AU / r, 1.5)

      return { r: r * SCALE, angle0, tilt, scale, rotSpeedX, rotSpeedY, rotSpeedZ, orbSpeed }
    })
  }, [modelIndex, count])

  const meshRef = useRef<THREE.InstancedMesh>(null)
  const matrix  = useMemo(() => new THREE.Matrix4(), [])
  const pos     = useMemo(() => new THREE.Vector3(), [])
  const rot     = useMemo(() => new THREE.Euler(), [])
  const quat    = useMemo(() => new THREE.Quaternion(), [])
  const scaleV  = useMemo(() => new THREE.Vector3(), [])

  // Rotaciones acumuladas por instancia
  const rotations = useRef(instanceData.map(() => ({
    x: Math.random() * Math.PI * 2,
    y: Math.random() * Math.PI * 2,
    z: Math.random() * Math.PI * 2,
  })))

  // Ángulos orbitales acumulados
  const angles = useRef(instanceData.map(d => d.angle0))

  useFrame((_, delta) => {
    const mesh = meshRef.current
    if (!mesh) return

    for (let i = 0; i < count; i++) {
      const d = instanceData[i]

      // Avanzar ángulo orbital
      angles.current[i] += d.orbSpeed * delta

      // Posición en el plano XZ con leve inclinación Y
      const a = angles.current[i]
      pos.set(
        Math.cos(a) * d.r,
        Math.sin(a * 0.7 + d.tilt) * d.r * 0.04, // leve ondulación vertical
        Math.sin(a) * d.r
      )

      // Rotación propia del asteroide
      rotations.current[i].x += d.rotSpeedX * delta
      rotations.current[i].y += d.rotSpeedY * delta
      rotations.current[i].z += d.rotSpeedZ * delta

      rot.set(rotations.current[i].x, rotations.current[i].y, rotations.current[i].z)
      quat.setFromEuler(rot)
      scaleV.setScalar(d.scale)

      matrix.compose(pos, quat, scaleV)
      mesh.setMatrixAt(i, matrix)
    }

    mesh.instanceMatrix.needsUpdate = true
  })

  if (!geometry) return null

  return (
    <instancedMesh
      ref={meshRef}
      args={[geometry, Array.isArray(material) ? material[0] : material, count]}
      castShadow={false}
      receiveShadow={false}
    />
  )
}

// ── Preload todos los modelos ─────────────────────────────────────────────────

for (let i = 1; i <= MODEL_COUNT; i++) {
  useGLTF.preload(getAssetPath(`/models/asteroids/${i}.glb`))
}

// ── Componente principal ──────────────────────────────────────────────────────

export default function AsteroidBelt3D() {
  return (
    <group>
      {Array.from({ length: MODEL_COUNT }, (_, i) => (
        <AsteroidInstances key={i} modelIndex={i} count={PER_MODEL} />
      ))}
    </group>
  )
}

'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

/**
 * Rano Kau - Volcán de Isla de Pascua
 * Ubicado al suroeste (X negativo, Z positivo) igual que el real
 * 
 * Estados:
 * - 'dormant'  → volcán inactivo, sin lava visible
 * - 'active'   → lava visible en el cráter, humo suave
 * - 'erupting' → erupción con partículas, humo denso, luz roja
 */

export type VolcanoState = 'dormant' | 'active' | 'erupting'

interface RanoKauVolcanoProps {
  state?: VolcanoState
}

// Partícula de erupción
interface Particle {
  position: THREE.Vector3
  velocity: THREE.Vector3
  life: number
  maxLife: number
  size: number
  isSmoke: boolean
}

export default function RanoKauVolcano({ state = 'dormant' }: RanoKauVolcanoProps) {
  const lavaRef = useRef<THREE.Mesh>(null)
  const smokeGroupRef = useRef<THREE.Group>(null)
  const particlesRef = useRef<THREE.InstancedMesh>(null)
  const lightRef = useRef<THREE.PointLight>(null)
  const timeRef = useRef(0)

  // Partículas de erupción
  const particles = useRef<Particle[]>([])
  const MAX_PARTICLES = state === 'erupting' ? 300 : state === 'active' ? 80 : 0
  const tempObj = useMemo(() => new THREE.Object3D(), [])
  const tempColor = useMemo(() => new THREE.Color(), [])

  // Geometría del volcán - cono deformado proceduralmente
  const volcanoGeometry = useMemo(() => {
    const geo = new THREE.ConeGeometry(28, 22, 48, 8)
    const pos = geo.attributes.position
    for (let i = 0; i < pos.count; i++) {
      const x = pos.getX(i)
      const y = pos.getY(i)
      const z = pos.getZ(i)
      // Deformar vértices para irregularidad natural
      const noise = Math.sin(x * 0.3 + z * 0.2) * 1.5 + Math.cos(x * 0.15 - z * 0.4) * 1.2
      pos.setX(i, x + noise * (1 - Math.abs(y) / 11))
      pos.setZ(i, z + noise * 0.7 * (1 - Math.abs(y) / 11))
    }
    pos.needsUpdate = true
    geo.computeVertexNormals()
    return geo
  }, [])

  // Geometría del cráter interior
  const craterGeometry = useMemo(() => {
    const geo = new THREE.CylinderGeometry(8, 10, 2, 32)
    return geo
  }, [])

  // Geometría del plano de lava
  const lavaGeometry = useMemo(() => {
    const geo = new THREE.CircleGeometry(7.5, 32)
    return geo
  }, [])

  // Inicializar partículas
  const initParticle = (p: Particle) => {
    const angle = Math.random() * Math.PI * 2
    const r = Math.random() * 3
    p.position.set(r * Math.cos(angle), 0, r * Math.sin(angle))
    const speed = state === 'erupting' ? 8 + Math.random() * 12 : 2 + Math.random() * 4
    p.velocity.set(
      (Math.random() - 0.5) * speed * 0.4,
      speed,
      (Math.random() - 0.5) * speed * 0.4
    )
    p.maxLife = state === 'erupting' ? 1.5 + Math.random() * 2 : 3 + Math.random() * 4
    p.life = p.maxLife
    p.size = state === 'erupting' ? 0.3 + Math.random() * 0.8 : 1 + Math.random() * 2
    p.isSmoke = Math.random() > 0.4
  }

  // Inicializar pool de partículas
  if (particles.current.length === 0 && MAX_PARTICLES > 0) {
    for (let i = 0; i < MAX_PARTICLES; i++) {
      const p: Particle = {
        position: new THREE.Vector3(),
        velocity: new THREE.Vector3(),
        life: 0,
        maxLife: 1,
        size: 1,
        isSmoke: false
      }
      initParticle(p)
      p.life = Math.random() * p.maxLife // Distribuir en el tiempo
      particles.current.push(p)
    }
  }

  useFrame((_, delta) => {
    timeRef.current += delta

    // Animar lava
    if (lavaRef.current && state !== 'dormant') {
      const mat = lavaRef.current.material as THREE.MeshStandardMaterial
      mat.emissiveIntensity = 0.6 + Math.sin(timeRef.current * 2) * 0.3
    }

    // Luz pulsante
    if (lightRef.current) {
      if (state === 'erupting') {
        lightRef.current.intensity = 8 + Math.sin(timeRef.current * 5) * 4
      } else if (state === 'active') {
        lightRef.current.intensity = 3 + Math.sin(timeRef.current * 1.5) * 1
      } else {
        lightRef.current.intensity = 0
      }
    }

    // Actualizar partículas
    if (MAX_PARTICLES === 0 || !particlesRef.current) return

    for (let i = 0; i < particles.current.length; i++) {
      const p = particles.current[i]
      p.life -= delta

      if (p.life <= 0) {
        initParticle(p)
        continue
      }

      // Física
      p.velocity.y -= delta * (p.isSmoke ? 0.5 : 4) // gravedad menor para humo
      p.velocity.x += (Math.random() - 0.5) * delta * 0.5
      p.velocity.z += (Math.random() - 0.5) * delta * 0.5
      p.position.addScaledVector(p.velocity, delta)

      const t = p.life / p.maxLife
      const scale = p.isSmoke ? p.size * (2 - t) : p.size * t
      tempObj.position.copy(p.position)
      tempObj.scale.setScalar(Math.max(0.01, scale))
      tempObj.updateMatrix()
      particlesRef.current.setMatrixAt(i, tempObj.matrix)

      // Color: lava = naranja→rojo, humo = gris
      if (p.isSmoke) {
        tempColor.setRGB(0.3 + t * 0.2, 0.3 + t * 0.2, 0.3 + t * 0.2)
      } else {
        tempColor.setRGB(1, 0.3 + t * 0.4, 0)
      }
      particlesRef.current.setColorAt(i, tempColor)
    }

    particlesRef.current.instanceMatrix.needsUpdate = true
    if (particlesRef.current.instanceColor) {
      particlesRef.current.instanceColor.needsUpdate = true
    }
  })

  return (
    // Rano Kau: suroeste de la isla → X=-55, Z=55 en nuestra escena
    <group position={[-55, 0, 55]}>
      {/* Cuerpo del volcán */}
      <mesh geometry={volcanoGeometry} castShadow receiveShadow>
        <meshStandardMaterial
          color="#3a3028"
          roughness={0.95}
          metalness={0.05}
        />
      </mesh>

      {/* Borde del cráter */}
      <mesh geometry={craterGeometry} position={[0, 11.5, 0]}>
        <meshStandardMaterial color="#2a2020" roughness={1} />
      </mesh>

      {/* Lava en el cráter - solo si activo o erupcionando */}
      {state !== 'dormant' && (
        <mesh
          ref={lavaRef}
          geometry={lavaGeometry}
          position={[0, 11, 0]}
          rotation={[-Math.PI / 2, 0, 0]}
        >
          <meshStandardMaterial
            color="#ff4400"
            emissive="#ff2200"
            emissiveIntensity={0.8}
            roughness={0.3}
          />
        </mesh>
      )}

      {/* Luz de lava */}
      <pointLight
        ref={lightRef}
        position={[0, 13, 0]}
        color="#ff4400"
        intensity={0}
        distance={60}
        decay={2}
      />

      {/* Partículas de erupción/humo */}
      {MAX_PARTICLES > 0 && (
        <instancedMesh
          ref={particlesRef}
          args={[undefined, undefined, MAX_PARTICLES]}
          position={[0, 12, 0]}
        >
          <sphereGeometry args={[0.5, 6, 6]} />
          <meshStandardMaterial
            vertexColors
            transparent
            opacity={0.7}
            depthWrite={false}
          />
        </instancedMesh>
      )}
    </group>
  )
}

'use client'

/**
 * RealisticWind - Sistema de viento profesional
 * 
 * Nivel 1: Vector global con dirección e intensidad
 * Nivel 2: Turbulencia con ruido Simplex
 * Nivel 3: Afecta objetos del mundo (árboles, arbustos)
 * Nivel 4: Coherencia espacial (viento por zonas)
 */

import { useRef, useEffect } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'
import { createNoise3D } from 'simplex-noise'

interface RealisticWindProps {
  strength: number // 0-1
  baseDirection?: [number, number, number]
  gustFrequency?: number
  turbulenceScale?: number
  affectObjects?: boolean
}

// Sistema de viento global
class WindSystem {
  direction: THREE.Vector3
  strength: number
  turbulence: number
  time: number
  noise3D: ReturnType<typeof createNoise3D>
  
  // Vectores reutilizables para evitar crear objetos cada frame
  private tempVec: THREE.Vector3
  private spatialTurbulence: THREE.Vector3
  private windResult: THREE.Vector3
  private rotationAxis: THREE.Vector3
  
  constructor() {
    this.direction = new THREE.Vector3(1, 0, 0.5).normalize()
    this.strength = 0
    this.turbulence = 0
    this.time = 0
    this.noise3D = createNoise3D()
    
    // Pre-alocar vectores
    this.tempVec = new THREE.Vector3()
    this.spatialTurbulence = new THREE.Vector3()
    this.windResult = new THREE.Vector3()
    this.rotationAxis = new THREE.Vector3(0, 1, 0)
  }
  
  update(delta: number, baseStrength: number, gustFrequency: number, turbulenceScale: number) {
    this.time += delta
    
    // Rotar dirección lentamente (viento cambia de dirección)
    const rotationSpeed = 0.0005
    this.direction.applyAxisAngle(this.rotationAxis, rotationSpeed)
    
    // Ráfagas (gusts) con ruido
    const gust = Math.sin(this.time * gustFrequency) * 0.3
    
    // Turbulencia global
    this.turbulence = this.noise3D(
      this.time * 0.2,
      this.time * 0.15,
      0
    ) * turbulenceScale
    
    // Fuerza final
    this.strength = baseStrength + gust + this.turbulence
    this.strength = Math.max(0, Math.min(1, this.strength))
  }
  
  // Obtener fuerza del viento en una posición específica
  getWindAtPosition(position: THREE.Vector3): THREE.Vector3 {
    // Turbulencia espacial (coherencia espacial) - reutilizar vector
    this.spatialTurbulence.set(
      this.noise3D(position.x * 0.1, position.z * 0.1, this.time * 0.2),
      this.noise3D(position.x * 0.1 + 100, position.z * 0.1, this.time * 0.2) * 0.3,
      this.noise3D(position.x * 0.1, position.z * 0.1 + 100, this.time * 0.2)
    )
    
    // Viento base + turbulencia espacial - reutilizar vector
    this.windResult.copy(this.direction)
      .multiplyScalar(this.strength)
      .add(this.spatialTurbulence.multiplyScalar(0.3))
    
    // Modificar por altura (más fuerte arriba, más débil abajo)
    const heightFactor = Math.min(1, position.y / 10)
    this.windResult.multiplyScalar(0.6 + heightFactor * 0.4)
    
    return this.windResult
  }
}

// Instancia global del sistema de viento
const globalWind = new WindSystem()

export default function RealisticWind({
  strength = 0.5,
  baseDirection = [1, 0, 0.5],
  gustFrequency = 0.5,
  turbulenceScale = 0.2,
  affectObjects = true
}: RealisticWindProps) {
  const { scene } = useThree()
  
  // Cache de objetos afectados por viento
  const windAffectedObjects = useRef<THREE.Object3D[]>([])
  const objectsCached = useRef(false)
  
  // Inicializar dirección base
  useEffect(() => {
    globalWind.direction.set(...baseDirection).normalize()
    objectsCached.current = false // Invalidar cache si cambia
  }, [baseDirection])
  
  // Actualizar sistema de viento
  useFrame((state, delta) => {
    globalWind.update(delta, strength, gustFrequency, turbulenceScale)
    
    // Afectar objetos del mundo (árboles, arbustos)
    if (affectObjects) {
      // Cachear objetos afectados una sola vez
      if (!objectsCached.current) {
        windAffectedObjects.current = []
        scene.traverse((object) => {
          if (object.userData.windAffected || 
              object.name.includes('tree') || 
              object.name.includes('bush') ||
              object.name.includes('Tree') ||
              object.name.includes('Bush')) {
            windAffectedObjects.current.push(object)
          }
        })
        objectsCached.current = true
      }
      
      // Actualizar solo objetos cacheados
      windAffectedObjects.current.forEach(object => {
        const wind = globalWind.getWindAtPosition(object.position)
        const swayAmount = wind.length() * 0.02
        object.rotation.z = Math.sin(globalWind.time * 2 + object.position.x) * swayAmount
        object.rotation.x = Math.sin(globalWind.time * 1.5 + object.position.z) * swayAmount * 0.5
      })
    }
    
    // Dispatch para que otros componentes puedan usar el viento
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('weather:wind', {
        detail: {
          direction: globalWind.direction,
          strength: globalWind.strength,
          time: globalWind.time,
          getWindAtPosition: (pos: THREE.Vector3) => globalWind.getWindAtPosition(pos)
        }
      }))
    }
  })
  
  return null
}

/**
 * WindStreaks - Visualización del viento con líneas/streaks
 * Más elegante que puntos
 */
export function WindStreaks({ strength = 0.5 }: { strength: number }) {
  const groupRef = useRef<THREE.Group>(null)
  const streaksRef = useRef<Array<{
    mesh: THREE.Mesh
    velocity: THREE.Vector3
    lifetime: number
  }>>([])
  
  // Vectores reutilizables
  const tempWind = useRef(new THREE.Vector3())
  const tempDir = useRef(new THREE.Vector3())
  const tempLookAt = useRef(new THREE.Vector3())
  
  useEffect(() => {
    if (!groupRef.current) return
    
    const group = groupRef.current
    const count = 100
    
    // Geometría y material compartidos
    const sharedGeometry = new THREE.PlaneGeometry(0.5, 0.05)
    
    for (let i = 0; i < count; i++) {
      const material = new THREE.MeshBasicMaterial({
        color: '#d4c5a0',
        transparent: true,
        opacity: 0.3,
        depthWrite: false,
        side: THREE.DoubleSide
      })
      
      const mesh = new THREE.Mesh(sharedGeometry, material)
      mesh.position.set(
        (Math.random() - 0.5) * 100,
        Math.random() * 15 + 1,
        (Math.random() - 0.5) * 100
      )
      
      group.add(mesh)
      
      streaksRef.current.push({
        mesh,
        velocity: new THREE.Vector3(
          Math.random() * 2 - 1,
          Math.random() * 0.2 - 0.1,
          Math.random() * 2 - 1
        ),
        lifetime: Math.random() * 5
      })
    }
    
    return () => {
      sharedGeometry.dispose()
      streaksRef.current.forEach(({ mesh }) => {
        ;(mesh.material as THREE.Material).dispose()
      })
      streaksRef.current = []
    }
  }, [])
  
  useFrame((state, delta) => {
    if (!groupRef.current) return
    
    streaksRef.current.forEach(({ mesh, velocity, lifetime }) => {
      // Obtener viento en esta posición
      const wind = globalWind.getWindAtPosition(mesh.position)
      
      // Mover con viento + velocidad propia (sin crear nuevos vectores)
      mesh.position.x += wind.x * delta * 3 + velocity.x * delta * strength
      mesh.position.y += wind.y * delta * 3 + velocity.y * delta * strength
      mesh.position.z += wind.z * delta * 3 + velocity.z * delta * strength
      
      // Orientar en dirección del movimiento
      tempDir.current.copy(wind).add(velocity).normalize()
      tempLookAt.current.copy(mesh.position).add(tempDir.current)
      mesh.lookAt(tempLookAt.current)
      
      // Fade in/out según lifetime
      const material = mesh.material as THREE.MeshBasicMaterial
      const fadeProgress = (state.clock.elapsedTime % lifetime) / lifetime
      material.opacity = Math.sin(fadeProgress * Math.PI) * 0.3 * strength
      
      // Reset si sale del área
      if (Math.abs(mesh.position.x) > 50 || 
          Math.abs(mesh.position.z) > 50 ||
          mesh.position.y < 0 || 
          mesh.position.y > 20) {
        mesh.position.set(
          (Math.random() - 0.5) * 100,
          Math.random() * 15 + 1,
          (Math.random() - 0.5) * 100
        )
      }
    })
  })
  
  return <group ref={groupRef} />
}

/**
 * WindDust - Polvo levantado por el viento
 * Cerca del suelo, más realista
 */
export function WindDust({ strength = 0.5, biome = 'default' }: { 
  strength: number
  biome?: 'desert' | 'default' | 'ice'
}) {
  const pointsRef = useRef<THREE.Points>(null)
  
  // Vector reutilizable para evitar crear en cada iteración
  const tempPos = useRef(new THREE.Vector3())
  
  // Color según bioma
  const dustColor = biome === 'desert' ? '#d4a574' : 
                    biome === 'ice' ? '#e0f0ff' : 
                    '#c4b5a0'
  
  const geometry = useRef(
    (() => {
      const count = 500
      const positions = new Float32Array(count * 3)
      
      for (let i = 0; i < count; i++) {
        const i3 = i * 3
        positions[i3] = (Math.random() - 0.5) * 100
        positions[i3 + 1] = Math.random() * 8
        positions[i3 + 2] = (Math.random() - 0.5) * 100
      }
      
      const geo = new THREE.BufferGeometry()
      geo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
      return geo
    })()
  ).current
  
  useFrame((state, delta) => {
    if (!pointsRef.current) return
    
    const positions = pointsRef.current.geometry.attributes.position.array as Float32Array
    
    for (let i = 0; i < positions.length; i += 3) {
      // Reutilizar vector temporal
      tempPos.current.set(positions[i], positions[i + 1], positions[i + 2])
      const wind = globalWind.getWindAtPosition(tempPos.current)
      
      // Mover con viento
      positions[i] += wind.x * delta * 3
      positions[i + 1] += wind.y * delta * 0.5
      positions[i + 2] += wind.z * delta * 3
      
      // Mantener cerca del suelo
      if (positions[i + 1] > 5) {
        positions[i + 1] = 0.5
      }
      if (positions[i + 1] < 0.2) {
        positions[i + 1] = 0.5
      }
      
      // Reset si sale del área
      if (Math.abs(positions[i]) > 50) {
        positions[i] = -Math.sign(positions[i]) * 50
      }
      if (Math.abs(positions[i + 2]) > 50) {
        positions[i + 2] = -Math.sign(positions[i + 2]) * 50
      }
    }
    
    pointsRef.current.geometry.attributes.position.needsUpdate = true
  })
  
  return (
    <points ref={pointsRef} geometry={geometry}>
      <pointsMaterial
        size={0.3}
        color={dustColor}
        transparent
        opacity={0.5 * strength}
        blending={THREE.AdditiveBlending}
        depthWrite={false}
        sizeAttenuation={true}
      />
    </points>
  )
}

/**
 * Preset ligero (recomendado para ArcheoScope)
 */
export function LightWind({ strength = 0.5, biome = 'default' }: { 
  strength: number
  biome?: 'desert' | 'default' | 'ice'
}) {
  console.log('🌬️ LightWind renderizado:', { strength, biome })
  
  return (
    <>
      <RealisticWind
        strength={strength}
        baseDirection={[1, 0, 0.5]}
        gustFrequency={0.5}
        turbulenceScale={0.2}
        affectObjects={true}
      />
      <WindDust strength={strength} biome={biome} />
    </>
  )
}

/**
 * Preset pesado (viento fuerte con streaks)
 */
export function HeavyWind({ strength = 0.8, biome = 'default' }: { 
  strength: number
  biome?: 'desert' | 'default' | 'ice'
}) {
  return (
    <>
      <RealisticWind
        strength={strength}
        baseDirection={[1, 0, 0.5]}
        gustFrequency={0.8}
        turbulenceScale={0.4}
        affectObjects={true}
      />
      <WindStreaks strength={strength} />
      <WindDust strength={strength} biome={biome} />
    </>
  )
}

// Exportar sistema global para que otros componentes puedan acceder
export { globalWind }

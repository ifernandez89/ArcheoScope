'use client'

import { Suspense, useMemo, useRef, useState, useEffect } from 'react'
import { useGLTF, Html } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'
import { getDeathWhistle } from '@/systems/DeathWhistleAudio'

interface MictlanSceneProps {
  avatarPositionRef?: React.RefObject<THREE.Vector3>
  onExit?: () => void
  currentUfo?: number
  abilityActive?: boolean
  tonatiuhInInventory?: boolean
  tonatiuhOnGround?: boolean
  tonatiuhDropPosition?: {x: number, z: number} | null
  onTonatiuhCollect?: () => void
  onTonatiuhDrop?: () => void
}

export default function MictlanScene({ avatarPositionRef, onExit, currentUfo, abilityActive, tonatiuhInInventory, tonatiuhOnGround, tonatiuhDropPosition, onTonatiuhCollect }: MictlanSceneProps) {
  return (
    <Suspense fallback={<LoadingMictlan />}>
      <MictlanSceneContent avatarPositionRef={avatarPositionRef} onExit={onExit} currentUfo={currentUfo} abilityActive={abilityActive} tonatiuhInInventory={tonatiuhInInventory} tonatiuhOnGround={tonatiuhOnGround} tonatiuhDropPosition={tonatiuhDropPosition} onTonatiuhCollect={onTonatiuhCollect} />
    </Suspense>
  )
}

function MictlanSceneContent({ avatarPositionRef, onExit, currentUfo, abilityActive, tonatiuhInInventory, tonatiuhOnGround, tonatiuhDropPosition, onTonatiuhCollect }: MictlanSceneProps) {
  const model = useGLTF(getAssetPath('/mictlantecuhtli.glb'))
  const groupRef = useRef<THREE.Group>(null)
  const flashLightRef = useRef<THREE.PointLight>(null)
  const flashPlaneRef = useRef<THREE.Mesh>(null)
  const appearanceCountRef = useRef(0)
  const exitTriggeredRef = useRef(false)

  // Activar arquitectura olmeca del inframundo
  useEffect(() => {
    import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
      const h = getHarmoniaMundi()
      if (h.isEnabled()) h.activateArchitecture('veracruz')
    })
    return () => {
      import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
        getHarmoniaMundi().deactivateArchitecture('veracruz')
      })
    }
  }, [])

  // Timers para relámpagos y visibilidad
  const nextLightningRef = useRef(3 + Math.random() * 5) // primer rayo entre 3-8s
  const flashTimerRef = useRef(0)
  const isFlashingRef = useRef(false)
  const visibleTimerRef = useRef(0)
  const [isVisible, setIsVisible] = useState(false)

  // Escala 10% menos que antes (10m * 0.9 = 9m)
  const { scale, floorY } = useMemo(() => {
    const box = new THREE.Box3().setFromObject(model.scene)
    const size = box.getSize(new THREE.Vector3())
    const sc = (10 * 0.9) / size.y // 9 metros
    const fy = -box.min.y * sc
    return { scale: sc, floorY: fy }
  }, [model.scene])

  useFrame(({ camera }, delta) => {
    // Seguir con la mirada al usuario (solo eje Y)
    if (groupRef.current) {
      const pos = groupRef.current.position
      const dx = camera.position.x - pos.x
      const dz = camera.position.z - pos.z
      groupRef.current.rotation.y = Math.atan2(dx, dz)
    }

    // Sistema de relámpagos aleatorios
    nextLightningRef.current -= delta

    if (nextLightningRef.current <= 0 && !isFlashingRef.current) {
      // ¡RELÁMPAGO!
      isFlashingRef.current = true
      flashTimerRef.current = 0
      visibleTimerRef.current = 0
      setIsVisible(true)

      // Contar apariciones
      appearanceCountRef.current += 1
      console.log(`💀 Mictlantecuhtli aparición ${appearanceCountRef.current}/10`)

      // 🎵 Silbato de la muerte azteca (volumen desde gameSettings)
      getDeathWhistle().play()

      // A la 10ª aparición → redirigir a Isla de Pascua
      if (appearanceCountRef.current >= 10 && !exitTriggeredRef.current && onExit) {
        exitTriggeredRef.current = true
        setTimeout(() => onExit(), 2000) // pequeño delay tras el último flash
      }

      nextLightningRef.current = 4 + Math.random() * 6
    }

    // Flash activo - estilo disparo de cámara
    if (isFlashingRef.current) {
      flashTimerRef.current += delta

      let opacity = 0
      let lightIntensity = 0

      if (flashTimerRef.current < 0.05) {
        // Subida instantánea - BANG
        const t = flashTimerRef.current / 0.05
        opacity = t * 0.95
        lightIntensity = t * 100
      } else if (flashTimerRef.current < 0.15) {
        // Pico máximo
        opacity = 0.95
        lightIntensity = 100
      } else if (flashTimerRef.current < 0.5) {
        // Bajada gradual
        const t = (flashTimerRef.current - 0.15) / 0.35
        opacity = (1 - t) * 0.95
        lightIntensity = (1 - t) * 100
      } else {
        isFlashingRef.current = false
      }

      if (flashLightRef.current) flashLightRef.current.intensity = lightIntensity
      if (flashPlaneRef.current) {
        const mat = flashPlaneRef.current.material as THREE.MeshBasicMaterial
        mat.opacity = opacity
      }
    }

    // Mictlantecuhtli visible 1 segundo después del flash
    if (isVisible) {
      visibleTimerRef.current += delta
      if (visibleTimerRef.current > 1.2) {
        setIsVisible(false)
      }
    }
  })

  return (
    <group>
      {/* Mictlantecuhtli - solo visible durante relámpagos */}
      <group
        ref={groupRef}
        position={[0, floorY, 0]}
        scale={scale}
        visible={isVisible}
      >
        <primitive object={model.scene} />
      </group>

      {/* Piso del inframundo */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.01, 0]} receiveShadow>
        <planeGeometry args={[200, 200]} />
        <meshStandardMaterial color="#0a0505" roughness={1} metalness={0} />
      </mesh>

      {/* Flash blanco fullscreen - disparo de cámara */}
      <mesh ref={flashPlaneRef} position={[0, 15, 0]} renderOrder={999}>
        <planeGeometry args={[500, 500]} />
        <meshBasicMaterial
          color="#ffffff"
          transparent
          opacity={0}
          depthWrite={false}
          depthTest={false}
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* Flash de relámpago - luz blanca intensa */}
      <pointLight
        ref={flashLightRef}
        position={[0, 30, 0]}
        color="#ffffff"
        intensity={0}
        distance={200}
        decay={1}
      />

      {/* Iluminación base tenebrosa (siempre) */}
      <pointLight position={[0, 8, 5]} color="#ff2200" intensity={1.5} distance={25} decay={2} />
      <pointLight position={[0, 3, -5]} color="#440000" intensity={1} distance={15} decay={2} />
      <ambientLight intensity={0.04} color="#220000" />

      {/* 🌞 Tonatiuh — visible SOLO cuando Mictlantecuhtli no está visible Y Phantom activo */}
      {!isVisible && currentUfo === 1 && abilityActive && !tonatiuhInInventory && (
        <TonatiuhItem
          position={tonatiuhOnGround && tonatiuhDropPosition
            ? [tonatiuhDropPosition.x, 0, tonatiuhDropPosition.z]
            : [0, 0, 0]}
          onCollect={onTonatiuhCollect}
        />
      )}
    </group>
  )
}

function LoadingMictlan() {
  return (
    <Html center>
      <div style={{
        background: 'rgba(10, 5, 5, 0.95)', padding: '20px 40px',
        borderRadius: '12px', color: '#ff3300',
        fontFamily: 'system-ui', textAlign: 'center',
        border: '2px solid rgba(255, 30, 0, 0.4)'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '10px' }}>💀</div>
        <div>Entrando al Mictlán...</div>
      </div>
    </Html>
  )
}

// ─── TONATIUH ITEM ────────────────────────────────────────────────────────────
// Figurilla de Tonatiuh girando — solo visible con Phantom activo y sin Mictlantecuhtli
function TonatiuhItem({ position, onCollect }: {
  position: [number, number, number]
  onCollect?: () => void
}) {
  const { scene } = useGLTF(getAssetPath('/tonatiuh_aztec_sun.glb'))
  const groupRef = useRef<THREE.Group>(null)
  const [hovered, setHovered] = useState(false)
  const [collecting, setCollecting] = useState(false)
  const collectTimerRef = useRef(0)

  // Calcular Y correcto sobre el piso
  const { scale, yOffset } = useMemo(() => {
    const box = new THREE.Box3().setFromObject(scene)
    const size = box.getSize(new THREE.Vector3())
    const sc = 1.5 / size.y  // 1.5m de alto
    const yo = -box.min.y * sc
    return { scale: sc, yOffset: yo }
  }, [scene])

  // Clonar para independencia
  const cloned = useMemo(() => scene.clone(true), [scene])

  useFrame(({ clock }, delta) => {
    if (!groupRef.current) return
    // Rotación continua
    groupRef.current.rotation.y = clock.elapsedTime * 1.2

    // Animación de recolección (escala + fade)
    if (collecting) {
      collectTimerRef.current += delta
      const progress = Math.min(collectTimerRef.current / 0.8, 1)
      groupRef.current.scale.setScalar(scale * (1 + progress * 0.5))
      cloned.traverse((child) => {
        if ((child as THREE.Mesh).isMesh) {
          const mat = (child as THREE.Mesh).material as THREE.MeshStandardMaterial
          if (mat) { mat.transparent = true; mat.opacity = 1 - progress }
        }
      })
      if (progress >= 1 && onCollect) onCollect()
    }
  })

  const handleClick = (e: any) => {
    if (collecting) return
    e.stopPropagation()
    setCollecting(true)
    console.log('🌞 Tonatiuh recogido!')
  }

  return (
    <group
      ref={groupRef}
      position={[position[0], position[1] + yOffset, position[2]]}
      scale={scale}
      onClick={handleClick}
      onPointerOver={() => { setHovered(true); document.body.style.cursor = 'pointer' }}
      onPointerOut={() => { setHovered(false); document.body.style.cursor = 'default' }}
    >
      <primitive object={cloned} />
      {/* Glow dorado */}
      <pointLight color="#ffaa00" intensity={hovered ? 3 : 1.5} distance={8} />
      {/* Outline hover */}
      {hovered && (
        <mesh>
          <sphereGeometry args={[0.8, 16, 16]} />
          <meshBasicMaterial color="#ffaa00" wireframe transparent opacity={0.3} />
        </mesh>
      )}
    </group>
  )
}

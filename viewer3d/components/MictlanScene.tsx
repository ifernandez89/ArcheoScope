'use client'

import { Suspense, useMemo, useRef, useState } from 'react'
import { useGLTF, Html } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'
import { getDeathWhistle } from '@/systems/DeathWhistleAudio'

interface MictlanSceneProps {
  avatarPositionRef?: React.RefObject<THREE.Vector3>
  onExit?: () => void
}

export default function MictlanScene({ avatarPositionRef, onExit }: MictlanSceneProps) {
  return (
    <Suspense fallback={<LoadingMictlan />}>
      <MictlanSceneContent avatarPositionRef={avatarPositionRef} onExit={onExit} />
    </Suspense>
  )
}

function MictlanSceneContent({ avatarPositionRef, onExit }: MictlanSceneProps) {
  const model = useGLTF(getAssetPath('/mictlantecuhtli.glb'))
  const groupRef = useRef<THREE.Group>(null)
  const flashLightRef = useRef<THREE.PointLight>(null)
  const flashPlaneRef = useRef<THREE.Mesh>(null)
  const appearanceCountRef = useRef(0)
  const exitTriggeredRef = useRef(false)

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

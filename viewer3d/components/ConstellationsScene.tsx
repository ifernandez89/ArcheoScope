'use client'

/**
 * ConstellationsScene — Escena nocturna para observar constelaciones
 *
 * Ubicación: desierto (20.0°N, 50.0°E) — cielo despejado
 * Features:
 * - Estrellas con constelaciones y nombres (Stars component)
 * - Luna con iluminación tipo farol
 * - Terreno desierto minimalista
 * - Nave WASD (PC) / touch D-pad (mobile) — vuelo alto
 * - Brújula
 * - Device orientation: cielo rota con el dispositivo (mobile)
 * - PC: mouse drag rota, tecla N centra norte
 */

import { Suspense, useEffect, useMemo, useState, useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { PerspectiveCamera, useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'
import dynamic from 'next/dynamic'

const Stars = dynamic(() => import('./Stars'), { ssr: false })
const WalkableAvatar = dynamic(() => import('./WalkableAvatar'), { ssr: false })
const MobileTouchControls = dynamic(() => import('./MobileTouchControls'), { ssr: false })
const Compass = dynamic(() => import('./Compass'), { ssr: false })
const CompassTracker = dynamic(() => import('./CompassTracker'), { ssr: false })
const AmbientAudio = dynamic(() => import('./AmbientAudio'), { ssr: false })
const Tree3DModel = dynamic(() => import('./Tree3DModel'), { ssr: false, loading: () => null })
const Rock3DModel = dynamic(() => import('./Rock3DModel'), { ssr: false, loading: () => null })

// ─── Luna visible con textura real e iluminación farol ───────────────────────
function DesertMoon({ moonTexture }: { moonTexture: THREE.Texture }) {
  const moonRef = useRef<THREE.Mesh>(null)

  // Billboard: la luna siempre mira hacia la cámara
  useFrame(({ camera }) => {
    if (moonRef.current) {
      moonRef.current.lookAt(camera.position)
    }
  })

  return (
    <group position={[200, 120, -300]}>
      {/* Plano con textura de luna — siempre mira a la cámara */}
      <mesh ref={moonRef}>
        <planeGeometry args={[30, 30]} />
        <meshBasicMaterial
          map={moonTexture}
          transparent
          side={THREE.DoubleSide}
        />
      </mesh>
      {/* Glow suave */}
      <mesh ref={(m) => { if (m) m.lookAt(0, 20, 0) }}>
        <planeGeometry args={[45, 45]} />
        <meshBasicMaterial color="#c8d4e8" transparent opacity={0.04} side={THREE.DoubleSide} />
      </mesh>
      {/* Luz de luna */}
      <directionalLight position={[200, 120, -300]} intensity={0.8} color="#c8d4e8" />
      <pointLight position={[200, 120, -300]} intensity={0.5} color="#d0dce8" distance={800} decay={1.5} />
    </group>
  )
}

// ─── Terreno desierto ────────────────────────────────────────────────────────
function DesertFloor() {
  const geometry = useMemo(() => {
    const geo = new THREE.PlaneGeometry(400, 400, 24, 24)
    geo.rotateX(-Math.PI / 2)
    const pos = geo.attributes.position.array as Float32Array
    for (let i = 0; i < pos.length; i += 3) {
      const x = pos[i], z = pos[i + 2]
      pos[i + 1] = Math.sin(x * 0.02) * Math.cos(z * 0.015) * 3 + Math.sin(x * 0.05 + z * 0.03) * 1.5
    }
    geo.computeVertexNormals()
    return geo
  }, [])

  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial color="#c2a66e" roughness={0.95} metalness={0.0} />
    </mesh>
  )
}

// ─── Vegetación y rocas del desierto ─────────────────────────────────────────
function DesertVegetation() {
  // Posiciones fijas dispersas — árboles y rocas en el desierto nocturno
  const trees: [number, number, number, number, string][] = [
    // [x, z, scale, rotation, type]
    [-35, -20, 1.2, 0.3,  'tree1'],
    [ 28, -45, 0.9, 1.1,  'tree2'],
    [-60,  15, 1.4, 2.4,  'tree3'],
    [ 50,  30, 1.0, 0.8,  'tree1'],
    [-15,  55, 1.3, 3.1,  'tree2'],
    [ 70, -10, 0.8, 1.7,  'tree3'],
  ]

  const rocks: [number, number, number, number][] = [
    // [x, z, scale, rotation]
    [ 20, -25, 0.8, 0.5],
    [-40,  35, 1.1, 1.2],
    [ 55, -50, 0.6, 2.0],
    [-25, -60, 0.9, 0.9],
    [ 40,  50, 1.2, 3.5],
    [-70, -30, 0.7, 1.8],
  ]

  return (
    <>
      {trees.map(([x, z, scale, rot, type], i) => (
        <Tree3DModel
          key={`tree-${i}`}
          position={[x, 0, z]}
          scale={scale}
          rotation={rot}
          treeType={type as any}
        />
      ))}
      {rocks.map(([x, z, scale, rot], i) => (
        <Rock3DModel
          key={`rock-${i}`}
          position={[x, 0, z]}
          scale={scale}
          rotation={rot}
        />
      ))}
    </>
  )
}
function SkyContent({
  onCameraRotation
}: {
  onCameraRotation?: (rotation: number) => void
}) {
  // Cargar textura de luna al nivel del componente R3F (dentro del Canvas)
  const moonTexture = useTexture(getAssetPath('/textures/beautiful-glowing-gray-full-moon.jpg'))

  // Habilitar HarmoniaMundi al primer click/touch
  useEffect(() => {
    const enableAudio = async () => {
      try {
        const { getHarmoniaMundi } = await import('@/systems/HarmoniaMundiSystem')
        const harmonia = getHarmoniaMundi()
        await harmonia.enable()
        harmonia.setMasterVolume(0.5)
      } catch {}
    }
    const handler = () => { enableAudio(); window.removeEventListener('click', handler); window.removeEventListener('touchstart', handler) }
    window.addEventListener('click', handler, { once: true })
    window.addEventListener('touchstart', handler, { once: true })
    return () => { window.removeEventListener('click', handler); window.removeEventListener('touchstart', handler) }
  }, [])

  return (
    <>
      {/* Estrellas fijas — sin rotación automática */}
      <Stars />

      {/* Luna con textura real */}
      <DesertMoon moonTexture={moonTexture} />

      {/* Terreno desierto */}
      <DesertFloor />

      {/* Árboles y rocas dispersos */}
      <DesertVegetation />

      {/* Nave — vuelo alto, posición inicial elevada, +2 velocidad */}
      <WalkableAvatar
        modelPath={getAssetPath('/ufo_3.glb')}
        solarDirection={{ x: 0.3, y: -0.5, z: -0.8 }}
        isDay={false}
        showCosmicEffects={false}
        abilityActive={false}
        currentUfo={3}
        initialPosition={[0, 20, 0]}
        disableShiftFlight={true}
        speedMultiplier={1.1}
        flyingHeightOverride={20}
      />

      {/* Rastreador de brújula */}
      {onCameraRotation && <CompassTracker onRotationChange={onCameraRotation} />}

      {/* Audio: viento ligero + drone atmosférico */}
      <AmbientAudio />

      {/* Iluminación nocturna */}
      <ambientLight intensity={0.1} color="#1a1a3a" />
      <hemisphereLight color="#0a0a2a" groundColor="#1a1008" intensity={0.2} />
    </>
  )
}

// ─── Componente principal ────────────────────────────────────────────────────
export default function ConstellationsScene() {
  const [isMobile] = useState(() =>
    typeof window !== 'undefined' &&
    (/Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768)
  )
  const [cameraRotation, setCameraRotation] = useState(0)

  // Landscape lock en mobile
  useEffect(() => {
    if (!isMobile) return
    const goLandscape = async () => {
      try {
        const el = document.documentElement as HTMLElement & { webkitRequestFullscreen?: () => Promise<void> }
        if (el.requestFullscreen) await el.requestFullscreen()
        else if (el.webkitRequestFullscreen) await el.webkitRequestFullscreen()
        const so = screen.orientation as ScreenOrientation & { lock?: (o: string) => Promise<void> }
        if (so?.lock) await so.lock('landscape')
      } catch {}
    }
    goLandscape()
    return () => {
      try { (screen.orientation as ScreenOrientation & { unlock?: () => void })?.unlock?.() } catch {}
    }
  }, [isMobile])

  return (
    <div style={{
      width: '100vw', height: '100vh',
      background: '#000', position: 'relative',
      overflow: 'hidden', touchAction: 'none',
    }}>
      <Canvas
        style={{ background: '#000' }}
        dpr={isMobile ? [1, 1.2] : [1, 1.5]}
        gl={{
          antialias: !isMobile,
          alpha: false,
          powerPreference: 'high-performance',
          toneMapping: THREE.ACESFilmicToneMapping,
          toneMappingExposure: 0.8,
        }}
      >
        <PerspectiveCamera makeDefault position={[0, 20, 10]} fov={60} far={20000} />
        <Suspense fallback={null}>
          <SkyContent onCameraRotation={setCameraRotation} />
        </Suspense>
      </Canvas>

      {/* Brújula */}
      <Compass rotation={cameraRotation} />

      {/* Mobile: D-pad touch controls — touchAction auto para no bloquear toques */}
      {isMobile && (
        <div style={{ touchAction: 'auto' }}>
          <MobileTouchControls visible={true} />
        </div>
      )}

      {/* Label sutil */}
      <div style={{
        position: 'absolute', top: 12, left: 0, right: 0,
        textAlign: 'center', color: 'rgba(255,255,255,0.3)',
        fontSize: '10px', letterSpacing: '3px', fontFamily: 'monospace',
        pointerEvents: 'none',
      }}>
        20.0000°, 50.0000° — CONSTELACIONES
      </div>

      {/* Flecha volver */}
      <div
        onClick={() => window.history.back()}
        style={{
          position: 'absolute', top: 8, left: isMobile ? 'auto' : 8, right: isMobile ? 8 : 'auto',
          width: 32, height: 32,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '16px', color: 'rgba(255,255,255,0.4)',
          cursor: 'pointer', zIndex: 10,
          background: 'rgba(0,0,0,0.3)', borderRadius: '50%',
        }}
      >
        ‹
      </div>

      {/* PC hint */}
      {!isMobile && (
        <div style={{
          position: 'absolute', bottom: 12, left: 0, right: 0,
          textAlign: 'center', color: 'rgba(255,255,255,0.2)',
          fontSize: '10px', letterSpacing: '2px', fontFamily: 'monospace',
          pointerEvents: 'none',
        }}>
          WASD mover · SHIFT+mouse subir/bajar · Q/E rotar · N centrar norte
        </div>
      )}
    </div>
  )
}

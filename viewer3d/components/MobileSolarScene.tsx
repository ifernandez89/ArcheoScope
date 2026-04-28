'use client'

/**
 * MobileSolarScene — Vista del Sistema Solar para mobile
 *
 * - Nave Vector (UFO 3) sigue el toque del dedo
 * - Pinch-to-zoom nativo via OrbitControls (enableZoom + touch)
 * - Sin botón de coordenadas, sin botones extra
 * - Fuerza orientación horizontal (landscape)
 */

import { useRef, useEffect, useMemo, Suspense } from 'react'
import { Canvas, useThree, useFrame } from '@react-three/fiber'
import { PerspectiveCamera, OrbitControls, useGLTF } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'
import MilkyWayBackground from './MilkyWayBackground'
import Stars from './Stars'
import RealisticSolarSystem from './RealisticSolarSystem'

/** UFO controlado por touch — sigue el dedo en pantalla */
function TouchSpaceUfo() {
  const ufoRef = useRef<THREE.Group>(null)
  const sunLightRef = useRef<THREE.DirectionalLight>(null)
  const { camera, size, scene: threeScene } = useThree()
  const touchPos = useRef({ x: 0, y: 0 })
  const { scene } = useGLTF(getAssetPath('/ufo_3.glb'))

  const raycaster = useMemo(() => new THREE.Raycaster(), [])
  const mouseVec = useMemo(() => new THREE.Vector2(), [])
  const tempVec = useMemo(() => new THREE.Vector3(), [])
  const targetPos = useMemo(() => new THREE.Vector3(), [])
  const lookAtPos = useMemo(() => new THREE.Vector3(), [])
  const dirVec = useMemo(() => new THREE.Vector3(), [])

  const cachedPlanets = useRef<THREE.Mesh[]>([])
  const planetsCached = useRef(false)

  useEffect(() => {
    const handleTouch = (e: TouchEvent) => {
      if (e.touches.length === 1) {
        const t = e.touches[0]
        touchPos.current = {
          x: (t.clientX / size.width) * 2 - 1,
          y: -(t.clientY / size.height) * 2 + 1
        }
      }
    }
    const handleMouse = (e: MouseEvent) => {
      touchPos.current = {
        x: (e.clientX / size.width) * 2 - 1,
        y: -(e.clientY / size.height) * 2 + 1
      }
    }
    window.addEventListener('touchmove', handleTouch, { passive: true })
    window.addEventListener('touchstart', handleTouch, { passive: true })
    window.addEventListener('mousemove', handleMouse)
    return () => {
      window.removeEventListener('touchmove', handleTouch)
      window.removeEventListener('touchstart', handleTouch)
      window.removeEventListener('mousemove', handleMouse)
    }
  }, [size])

  useFrame(() => {
    if (!ufoRef.current) return

    mouseVec.set(touchPos.current.x, touchPos.current.y)
    raycaster.setFromCamera(mouseVec, camera)

    targetPos.copy(raycaster.ray.origin).add(
      tempVec.copy(raycaster.ray.direction).multiplyScalar(10)
    )
    ufoRef.current.position.lerp(targetPos, 0.1)

    lookAtPos.copy(ufoRef.current.position).add(raycaster.ray.direction)
    ufoRef.current.lookAt(lookAtPos)

    if (!planetsCached.current) {
      cachedPlanets.current = []
      threeScene.traverse((obj) => {
        if (obj instanceof THREE.Mesh && obj.geometry instanceof THREE.SphereGeometry) {
          cachedPlanets.current.push(obj)
        }
      })
      planetsCached.current = true
    }

    let minDist = Infinity
    cachedPlanets.current.forEach(planet => {
      const d = ufoRef.current!.position.distanceTo(planet.getWorldPosition(tempVec))
      if (d < minDist) minDist = d
    })

    const normalScale = 1.14
    const minScale = 0.0285
    let targetScale = normalScale
    if (minDist < 50) {
      const t = Math.max(0, Math.min(1, (50 - minDist) / 45))
      targetScale = normalScale - t * (normalScale - minScale)
    }
    const newScale = ufoRef.current.scale.x + (targetScale - ufoRef.current.scale.x) * 0.05
    ufoRef.current.scale.setScalar(newScale)

    if (sunLightRef.current) {
      dirVec.copy(ufoRef.current.position).normalize().multiplyScalar(-50)
      sunLightRef.current.position.copy(dirVec)
    }
  })

  return (
    <group ref={ufoRef} position={[0, 0, 10]}>
      <primitive object={scene} scale={1.37} />
      <directionalLight ref={sunLightRef} intensity={2.5} color="#fff5e6" />
      <ambientLight intensity={0.2} />
    </group>
  )
}

function SolarContent() {
  return (
    <>
      <MilkyWayBackground />
      <Stars />
      <RealisticSolarSystem />
      <TouchSpaceUfo />
    </>
  )
}

export default function MobileSolarScene() {
  useEffect(() => {
    // Forzar landscape: fullscreen + orientation lock
    const goLandscape = async () => {
      try {
        const el = document.documentElement as any
        // Primero fullscreen (requerido para orientation lock en la mayoría de browsers)
        if (el.requestFullscreen) await el.requestFullscreen()
        else if (el.webkitRequestFullscreen) await el.webkitRequestFullscreen()
        // Luego lock orientation
        const so = screen.orientation as any
        await so?.lock?.('landscape')
      } catch {}
    }
    goLandscape()

    return () => {
      try { (screen.orientation as any)?.unlock?.() } catch {}
      try { if (document.fullscreenElement) document.exitFullscreen() } catch {}
    }
  }, [])

  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      background: '#000',
      position: 'relative',
      overflow: 'hidden',
      touchAction: 'none',
    }}>
      <Canvas
        camera={{ position: [0, 0, 15], fov: 50 }}
        style={{ background: '#000' }}
        dpr={[1, 1.2]}
        gl={{
          antialias: false,
          alpha: false,
          powerPreference: 'high-performance',
          toneMapping: THREE.ACESFilmicToneMapping,
          toneMappingExposure: 1.0,
        }}
      >
        <PerspectiveCamera makeDefault position={[0, 0, 15]} fov={50} />
        <OrbitControls
          enableDamping
          dampingFactor={0.08}
          minDistance={8}
          maxDistance={8000}
          autoRotate={false}
          enableRotate={true}
          enableZoom={true}
          enablePan={false}
          touches={{
            ONE: THREE.TOUCH.ROTATE,
            TWO: THREE.TOUCH.DOLLY_ROTATE,
          }}
        />
        <Suspense fallback={null}>
          <SolarContent />
        </Suspense>
      </Canvas>

      {/* Label sutil arriba */}
      <div style={{
        position: 'absolute',
        top: 16,
        left: 0,
        right: 0,
        textAlign: 'center',
        color: 'rgba(255,255,255,0.4)',
        fontSize: '11px',
        letterSpacing: '3px',
        fontFamily: 'monospace',
        pointerEvents: 'none',
      }}>
        3D SOLAR SYSTEM
      </div>

      {/* Flecha mínima para volver */}
      <div
        onClick={() => window.history.back()}
        style={{
          position: 'absolute',
          top: 6,
          left: 6,
          width: 28,
          height: 28,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '14px',
          color: 'rgba(255,255,255,0.35)',
          cursor: 'pointer',
          zIndex: 10,
        }}
      >
        ‹
      </div>
    </div>
  )
}

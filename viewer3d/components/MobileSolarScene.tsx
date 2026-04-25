'use client'

/**
 * MobileSolarScene — Simulador de nave espacial para mobile
 *
 * Controles INTACTOS:
 *   1 dedo → rotar vista (arriba/abajo/lados)
 *   2 dedos → pinch zoom in/out
 *
 * Capas visuales:
 *   - Nave sigue la cámara (cabina)
 *   - Borde interior de cabina (geometría simple)
 *   - HUD HTML overlay (planeta cercano + mitología)
 *   - Radar 2D SVG (posiciones planetarias)
 *   - Música de las esferas (Kepler Harmonices) activa
 */

import { useRef, useState, useEffect, useMemo, useCallback, Suspense } from 'react'
import { Canvas, useThree, useFrame } from '@react-three/fiber'
import { PerspectiveCamera, OrbitControls, useGLTF } from '@react-three/drei'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'
import MilkyWayBackground from './MilkyWayBackground'
import Stars from './Stars'
import RealisticSolarSystem from './RealisticSolarSystem'
import EngineIntegration from './EngineIntegration'

// ═══════════════════════════════════════════════════════════════════════
// DATOS DE PLANETAS — mitología multicultural
// ═══════════════════════════════════════════════════════════════════════
const PLANET_DATA: Record<string, {
  symbol: string
  au: number
  color: string
  mythology: { culture: string, name: string }[]
}> = {
  'Sol': {
    symbol: '☀', au: 0, color: '#ffaa00',
    mythology: [
      { culture: 'Egipto', name: 'Ra' },
      { culture: 'Maya', name: 'Kinich Ahau' },
      { culture: 'Inca', name: 'Inti' },
    ]
  },
  'Mercurio': {
    symbol: '☿', au: 0.39, color: '#9c9c9c',
    mythology: [
      { culture: 'Roma', name: 'Mercurius' },
      { culture: 'Grecia', name: 'Hermes' },
      { culture: 'Babilonia', name: 'Nabu' },
    ]
  },
  'Venus': {
    symbol: '♀', au: 0.72, color: '#f5e6d3',
    mythology: [
      { culture: 'Babilonia', name: 'Inanna' },
      { culture: 'Grecia', name: 'Afrodita' },
      { culture: 'Maya', name: 'Noh Ek (Estrella de Guerra)' },
    ]
  },
  'Tierra': {
    symbol: '🌍', au: 1.0, color: '#4A90E2',
    mythology: [
      { culture: 'Grecia', name: 'Gaia' },
      { culture: 'Inca', name: 'Pachamama' },
      { culture: 'Nórdico', name: 'Jörð' },
    ]
  },
  'Marte': {
    symbol: '♂', au: 1.52, color: '#E27B58',
    mythology: [
      { culture: 'Roma', name: 'Mars' },
      { culture: 'Grecia', name: 'Ares' },
      { culture: 'Babilonia', name: 'Nergal' },
    ]
  },
  'Júpiter': {
    symbol: '♃', au: 5.20, color: '#D4A574',
    mythology: [
      { culture: 'Roma', name: 'Iuppiter' },
      { culture: 'Grecia', name: 'Zeus' },
      { culture: 'Babilonia', name: 'Marduk' },
    ]
  },
  'Saturno': {
    symbol: '♄', au: 9.54, color: '#FAD5A5',
    mythology: [
      { culture: 'Roma', name: 'Saturnus' },
      { culture: 'Grecia', name: 'Kronos' },
      { culture: 'Babilonia', name: 'Ninurta' },
    ]
  },
  'Urano': {
    symbol: '⛢', au: 19.19, color: '#4FD0E7',
    mythology: [
      { culture: 'Grecia', name: 'Ouranos' },
      { culture: 'Moderno', name: 'Cielo primordial' },
    ]
  },
  'Neptuno': {
    symbol: '♆', au: 30.07, color: '#4166F5',
    mythology: [
      { culture: 'Roma', name: 'Neptunus' },
      { culture: 'Grecia', name: 'Poseidón' },
    ]
  },
  'Plutón': {
    symbol: '♇', au: 39.48, color: '#8c7853',
    mythology: [
      { culture: 'Roma', name: 'Pluto' },
      { culture: 'Grecia', name: 'Hades' },
    ]
  },
}

// Nombres de planetas en el orden que usa RealisticSolarSystem
const PLANET_NAMES = ['Sol', 'Mercurio', 'Venus', 'Tierra', 'Marte', 'Júpiter', 'Saturno', 'Urano', 'Neptuno', 'Plutón']

// ═══════════════════════════════════════════════════════════════════════
// CABINA — nave que sigue la cámara
// ═══════════════════════════════════════════════════════════════════════

/** Store compartido: 3D → UI para posiciones de planetas y cámara */
type PlanetPos = { name: string; x: number; y: number; z: number }
type HUDListener = (data: { planets: PlanetPos[]; camPos: THREE.Vector3; closest: string; dist: number }) => void
const hudListeners = new Set<HUDListener>()
function emitHUD(data: { planets: PlanetPos[]; camPos: THREE.Vector3; closest: string; dist: number }) {
  hudListeners.forEach(fn => fn(data))
}
function subscribeHUD(fn: HUDListener) {
  hudListeners.add(fn)
  return () => { hudListeners.delete(fn) }
}

function CockpitUfo() {
  const cockpitRef = useRef<THREE.Group>(null)
  const { camera, scene: threeScene } = useThree()
  const { scene: ufoScene } = useGLTF(getAssetPath('/ufo_3.glb'))

  // Cache de planetas (esferas con nombre)
  const cachedBodies = useRef<{ mesh: THREE.Mesh; name: string }[]>([])
  const bodiesCached = useRef(false)
  const tempVec = useMemo(() => new THREE.Vector3(), [])
  const frameCount = useRef(0)

  useFrame(() => {
    if (!cockpitRef.current) return

    // Nave sigue la cámara — offset hacia abajo y adelante
    cockpitRef.current.position.copy(camera.position)
    cockpitRef.current.quaternion.copy(camera.quaternion)
    // Mover la nave un poco abajo y adelante relativo a la cámara
    const forward = new THREE.Vector3(0, -0.6, -2.5)
    forward.applyQuaternion(camera.quaternion)
    cockpitRef.current.position.add(forward)

    // Cachear cuerpos celestes (esferas grandes)
    if (!bodiesCached.current) {
      cachedBodies.current = []
      const knownRadii = [
        { min: 50, max: 60, name: 'Júpiter' },
        { min: 35, max: 42, name: 'Saturno' },
        { min: 18, max: 22, name: 'Urano' },
        { min: 17, max: 20, name: 'Neptuno' },
        { min: 1.5, max: 2.5, name: 'Mercurio' },
        { min: 0.8, max: 1.1, name: 'Venus' },
        { min: 0.4, max: 0.6, name: 'Marte' },
        { min: 2.0, max: 3.0, name: 'Plutón' },
      ]
      threeScene.traverse((obj) => {
        if (obj instanceof THREE.Mesh && obj.geometry instanceof THREE.SphereGeometry) {
          const params = obj.geometry.parameters
          if (params.radius > 0.2) {
            cachedBodies.current.push({ mesh: obj, name: '' })
          }
        }
      })
      bodiesCached.current = true
    }

    // Emitir datos al HUD cada 6 frames (~10 Hz)
    frameCount.current++
    if (frameCount.current % 6 !== 0) return

    const planets: PlanetPos[] = []
    let closestName = ''
    let closestDist = Infinity

    cachedBodies.current.forEach(body => {
      const wp = body.mesh.getWorldPosition(tempVec)
      const d = camera.position.distanceTo(wp)
      planets.push({ name: body.name, x: wp.x, y: wp.y, z: wp.z })
      if (d < closestDist) {
        closestDist = d
        closestName = body.name
      }
    })

    emitHUD({ planets, camPos: camera.position.clone(), closest: closestName, dist: closestDist })
  })

  return (
    <group ref={cockpitRef}>
      {/* Modelo de la nave — escala pequeña, semi-transparente para efecto cabina */}
      <primitive object={ufoScene} scale={0.3} position={[0, -0.15, 0]} />

      {/* Borde interior de cabina — anillo sutil */}
      <mesh position={[0, 0, -0.5]} rotation={[Math.PI * 0.05, 0, 0]}>
        <torusGeometry args={[1.8, 0.02, 8, 32]} />
        <meshBasicMaterial color="#44ccff" transparent opacity={0.15} blending={THREE.AdditiveBlending} depthWrite={false} />
      </mesh>

      {/* Líneas de cabina laterales */}
      {[-1.2, 1.2].map((x, i) => (
        <mesh key={i} position={[x, -0.3, -1]}>
          <boxGeometry args={[0.01, 0.6, 1.5]} />
          <meshBasicMaterial color="#44ccff" transparent opacity={0.08} blending={THREE.AdditiveBlending} depthWrite={false} />
        </mesh>
      ))}
    </group>
  )
}

// ═══════════════════════════════════════════════════════════════════════
// AUDIO — inicializar música de las esferas en interacción
// ═══════════════════════════════════════════════════════════════════════
function AudioInitializer() {
  const initialized = useRef(false)
  const { scene } = useThree()

  useEffect(() => {
    if (initialized.current) return
    const enable = async () => {
      if (initialized.current) return
      initialized.current = true
      try {
        const { getKeplerHarmonices } = await import('@/systems/KeplerHarmonicesSystem')
        const kepler = getKeplerHarmonices()
        await kepler.enable()
        kepler.activateKeplerMode(scene)
      } catch {}
    }
    window.addEventListener('touchstart', enable, { once: true })
    window.addEventListener('click', enable, { once: true })
    return () => {
      window.removeEventListener('touchstart', enable)
      window.removeEventListener('click', enable)
    }
  }, [scene])

  return null
}

// ═══════════════════════════════════════════════════════════════════════
// CONTENIDO 3D
// ═══════════════════════════════════════════════════════════════════════
function SolarContent() {
  return (
    <>
      <EngineIntegration />
      <MilkyWayBackground />
      <Stars />
      <RealisticSolarSystem />
      <CockpitUfo />
      <AudioInitializer />
    </>
  )
}

// ═══════════════════════════════════════════════════════════════════════
// RADAR SVG — mini mapa circular con posiciones planetarias
// ═══════════════════════════════════════════════════════════════════════
function RadarHUD({ planets, camPos }: { planets: PlanetPos[]; camPos: THREE.Vector3 | null }) {
  const SIZE = 90
  const R = 38 // radio útil

  // Proyectar posiciones 3D a 2D (vista cenital XZ)
  const dots = useMemo(() => {
    if (!planets.length || !camPos) return []
    return planets.map((p, i) => {
      const dx = p.x - camPos.x
      const dz = p.z - camPos.z
      const dist = Math.sqrt(dx * dx + dz * dz)
      // Escala logarítmica para que quepan todos
      const logDist = Math.log10(dist + 1) / Math.log10(8001) // normalizar a 0-1
      const angle = Math.atan2(dz, dx)
      const r = logDist * R
      return {
        cx: SIZE / 2 + Math.cos(angle) * r,
        cy: SIZE / 2 + Math.sin(angle) * r,
        color: PLANET_DATA[PLANET_NAMES[i]]?.color || '#fff',
        symbol: PLANET_DATA[PLANET_NAMES[i]]?.symbol || '·',
      }
    })
  }, [planets, camPos])

  return (
    <svg width={SIZE} height={SIZE} style={{ opacity: 0.6 }}>
      {/* Círculos de referencia */}
      <circle cx={SIZE / 2} cy={SIZE / 2} r={R} fill="none" stroke="rgba(68,204,255,0.15)" strokeWidth={0.5} />
      <circle cx={SIZE / 2} cy={SIZE / 2} r={R * 0.5} fill="none" stroke="rgba(68,204,255,0.08)" strokeWidth={0.5} />
      {/* Cruz central */}
      <line x1={SIZE / 2 - 4} y1={SIZE / 2} x2={SIZE / 2 + 4} y2={SIZE / 2} stroke="rgba(68,204,255,0.2)" strokeWidth={0.5} />
      <line x1={SIZE / 2} y1={SIZE / 2 - 4} x2={SIZE / 2} y2={SIZE / 2 + 4} stroke="rgba(68,204,255,0.2)" strokeWidth={0.5} />
      {/* Planetas */}
      {dots.map((d, i) => (
        <circle key={i} cx={d.cx} cy={d.cy} r={i === 0 ? 3 : 2} fill={d.color} opacity={0.85} />
      ))}
      {/* Nave (centro) */}
      <text x={SIZE / 2} y={SIZE / 2 + 1} textAnchor="middle" fontSize={8} fill="#44ccff">🛸</text>
    </svg>
  )
}

// ═══════════════════════════════════════════════════════════════════════
// HUD — overlay HTML con info del planeta más cercano
// ═══════════════════════════════════════════════════════════════════════
function PilotHUD() {
  const [hudData, setHudData] = useState<{
    planets: PlanetPos[]
    camPos: THREE.Vector3
    closest: string
    dist: number
  } | null>(null)

  useEffect(() => subscribeHUD(setHudData), [])

  // Determinar planeta más cercano por distancia 3D
  const closestPlanet = useMemo(() => {
    if (!hudData?.planets.length || !hudData.camPos) return null
    let minDist = Infinity
    let minIdx = 0
    hudData.planets.forEach((p, i) => {
      const dx = p.x - hudData.camPos.x
      const dy = p.y - hudData.camPos.y
      const dz = p.z - hudData.camPos.z
      const d = Math.sqrt(dx * dx + dy * dy + dz * dz)
      if (d < minDist) { minDist = d; minIdx = i }
    })
    const name = PLANET_NAMES[minIdx] || 'Desconocido'
    const data = PLANET_DATA[name]
    return { name, dist: minDist, data }
  }, [hudData])

  if (!closestPlanet?.data) return null

  const { name, dist, data } = closestPlanet
  // Convertir distancia de unidades 3D a AU aproximado (escala 200 = 1 AU)
  const auDist = (dist / 200).toFixed(2)

  return (
    <>
      {/* Panel planeta cercano — abajo izquierda */}
      <div style={{
        position: 'absolute', bottom: 16, left: 12,
        background: 'rgba(0,10,20,0.75)',
        border: '1px solid rgba(68,204,255,0.25)',
        borderRadius: '8px', padding: '10px 14px',
        backdropFilter: 'blur(4px)',
        maxWidth: '200px',
        pointerEvents: 'none',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
          <span style={{ fontSize: '18px' }}>{data.symbol}</span>
          <span style={{ color: data.color, fontSize: '14px', fontWeight: 'bold', letterSpacing: '1px' }}>{name.toUpperCase()}</span>
        </div>
        <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.5)', marginBottom: '6px', fontFamily: 'monospace' }}>
          {auDist} AU · {data.au} AU (órbita)
        </div>
        {/* Mitología */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
          {data.mythology.map((m, i) => (
            <div key={i} style={{ fontSize: '9px', color: 'rgba(68,204,255,0.7)', fontFamily: 'monospace' }}>
              {m.culture}: <span style={{ color: 'rgba(255,255,255,0.6)' }}>{m.name}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Radar — abajo derecha */}
      <div style={{
        position: 'absolute', bottom: 16, right: 12,
        pointerEvents: 'none',
      }}>
        <RadarHUD planets={hudData?.planets || []} camPos={hudData?.camPos || null} />
      </div>

      {/* Líneas de cabina decorativas — bordes de pantalla */}
      <div style={{
        position: 'absolute', inset: 0, pointerEvents: 'none',
        border: '1px solid rgba(68,204,255,0.06)',
        borderRadius: '0',
      }}>
        {/* Esquinas tipo HUD */}
        {[
          { top: 0, left: 0 },
          { top: 0, right: 0 },
          { bottom: 0, left: 0 },
          { bottom: 0, right: 0 },
        ].map((pos, i) => (
          <div key={i} style={{
            position: 'absolute', ...pos,
            width: 20, height: 20,
            borderTop: pos.top !== undefined ? '1px solid rgba(68,204,255,0.2)' : 'none',
            borderBottom: pos.bottom !== undefined ? '1px solid rgba(68,204,255,0.2)' : 'none',
            borderLeft: pos.left !== undefined ? '1px solid rgba(68,204,255,0.2)' : 'none',
            borderRight: pos.right !== undefined ? '1px solid rgba(68,204,255,0.2)' : 'none',
          }} />
        ))}
      </div>
    </>
  )
}

// ═══════════════════════════════════════════════════════════════════════
// COMPONENTE PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════
export default function MobileSolarScene() {
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
        dpr={[1, 1.5]}
        gl={{
          antialias: true,
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

      {/* HUD del piloto — overlay HTML */}
      <PilotHUD />

      {/* Label sutil arriba */}
      <div style={{
        position: 'absolute',
        top: 10,
        left: 0,
        right: 0,
        textAlign: 'center',
        color: 'rgba(68,204,255,0.3)',
        fontSize: '9px',
        letterSpacing: '4px',
        fontFamily: 'monospace',
        pointerEvents: 'none',
      }}>
        ARCHEOSCOPE · SOLAR NAV
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

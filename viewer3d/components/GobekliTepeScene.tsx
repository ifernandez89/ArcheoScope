'use client'

import { Suspense, useMemo, useRef, useState, useEffect } from 'react'
import { useGLTF, Html } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import { useRouter } from 'next/navigation'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'
import CropCircle from './CropCircle'
import ToroidalSphere from './ToroidalSphere'
import Geoglyph from './Geoglyph'
import DroppableItem from './DroppableItem'

export const GOBEKLI_TEPE_COORDS = { lat: 37.2231, lon: 38.9225 }

// Altares cardinales — posición y objeto esperado
// Norte: Tonatiuh | Sur: Escarabajo | Este: Calavera | Oeste: Fuente Magna
const ALTARS = [
  { dir: 'N', label: 'Tonatiuh',     icon: '🌞', x:  0,   z: -35, color: '#ffaa00', itemKey: 'tonatiuh'  },
  { dir: 'S', label: 'Escarabajo',   icon: '🪲', x:  0,   z:  35, color: '#44cc44', itemKey: 'scarab'    },
  { dir: 'E', label: 'Calavera',     icon: '💀', x:  35,  z:  0,  color: '#aa44ff', itemKey: 'skull'     },
  { dir: 'O', label: 'Fuente Magna', icon: '🏺', x: -35,  z:  0,  color: '#4488ff', itemKey: 'magna'     },
] as const

type ItemKey = 'tonatiuh' | 'scarab' | 'skull' | 'magna'
const ALTAR_RADIUS = 14  // radio amplio para detección generosa

export interface GobekliTepeSceneProps {
  tonatiuhDropPosition?: { x: number, z: number } | null
  tonatiuhOnGround?: boolean
  onTonatiuhCollect?: () => void
  scarabDropPosition?: { x: number, z: number } | null
  scarabOnGround?: boolean
  onScarabCollect?: () => void
  skullDropPosition?: { x: number, z: number } | null
  skullOnGround?: boolean
  onSkullCollect?: () => void
  magnaBowlCollected?: boolean
  magnaBowlDropPosition?: { x: number, z: number } | null
  magnaBowlOnGround?: boolean
  onMagnaBowlCollect?: () => void
  avatarPositionRef?: React.RefObject<THREE.Vector3>
}

export default function GobekliTepeScene(props: GobekliTepeSceneProps) {
  return (
    <Suspense fallback={<LoadingGobekli />}>
      <GobekliTepeContent {...props} />
    </Suspense>
  )
}

function GobekliTepeContent({
  tonatiuhDropPosition, tonatiuhOnGround, onTonatiuhCollect,
  scarabDropPosition, scarabOnGround, onScarabCollect,
  skullDropPosition, skullOnGround, onSkullCollect,
  magnaBowlCollected, magnaBowlDropPosition, magnaBowlOnGround, onMagnaBowlCollect,
  avatarPositionRef
}: GobekliTepeSceneProps) {
  const { scene } = useGLTF(getAssetPath('/gobekli_tepe.glb'))
  const lightRef = useRef<THREE.PointLight>(null)
  const router = useRouter()
  const [showMessage, setShowMessage] = useState(false)

  const { scale, yOffset } = useMemo(() => {
    const box = new THREE.Box3().setFromObject(scene)
    const size = box.getSize(new THREE.Vector3())
    const maxDim = Math.max(size.x, size.y, size.z)
    const sc = 40 / maxDim
    const yo = -box.min.y * sc
    return { scale: sc, yOffset: yo }
  }, [scene])

  const cloned = useMemo(() => scene.clone(true), [scene])

  // Detectar qué items están en su altar correcto
  const [activated, setActivated] = useState<Record<ItemKey, boolean>>({
    tonatiuh: false, scarab: false, skull: false, magna: false
  })

  // Verificar posición de cada item contra su altar
  useEffect(() => {
    const check = (dropPos: { x: number, z: number } | null | undefined, onGround: boolean | undefined, altar: typeof ALTARS[number]) => {
      if (!dropPos || !onGround) return false
      const dx = dropPos.x - altar.x
      const dz = dropPos.z - altar.z
      return dx * dx + dz * dz < ALTAR_RADIUS * ALTAR_RADIUS
    }

    setActivated({
      tonatiuh: check(tonatiuhDropPosition, tonatiuhOnGround, ALTARS[0]),
      scarab:   check(scarabDropPosition,   scarabOnGround,   ALTARS[1]),
      skull:    check(skullDropPosition,    skullOnGround,    ALTARS[2]),
      magna:    check(magnaBowlDropPosition, magnaBowlOnGround, ALTARS[3]),
    })
  }, [tonatiuhDropPosition, tonatiuhOnGround, scarabDropPosition, scarabOnGround,
      skullDropPosition, skullOnGround, magnaBowlDropPosition, magnaBowlOnGround])

  useFrame(({ clock }) => {
    if (lightRef.current) {
      lightRef.current.intensity = 1.5 + Math.sin(clock.elapsedTime * 0.6) * 0.5
    }
  })

  const allActivated = activated.tonatiuh && activated.scarab && activated.skull && activated.magna

  // Activar arquitectura de Göbekli Tepe y sonido del escarabajo al completar
  useEffect(() => {
    import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
      const harmonia = getHarmoniaMundi()
      if (harmonia.isEnabled()) harmonia.activateArchitecture('gobekli-tepe')
    })
    return () => {
      import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
        getHarmoniaMundi().deactivateArchitecture('gobekli-tepe')
      })
    }
  }, [])

  // Cuando los 4 altares se activan → secuencia final
  useEffect(() => {
    if (!allActivated) return
    import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
      const harmonia = getHarmoniaMundi()
      if (!harmonia.isEnabled()) return
      harmonia.unlockMissionLayer('earth_mission_6')
      harmonia.playBeetleSound()
      console.log('🪲 Göbekli Tepe completado — Khepri despierta!')
    })
    // Mostrar mensaje a los 8 segundos (esfera ya visible y subiendo)
    const msgTimer = setTimeout(() => setShowMessage(true), 8000)
    // Redirigir a créditos a los 25 segundos (animación 20s + margen)
    const redirectTimer = setTimeout(() => {
      router.push('/menu/info?credits=true')
    }, 25000)
    return () => {
      clearTimeout(msgTimer)
      clearTimeout(redirectTimer)
    }
  }, [allActivated])

  return (
    <group>
      <fog attach="fog" args={['#1a1208', 30, 200]} />

      {/* Terreno */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.1, 0]} receiveShadow>
        <planeGeometry args={[400, 400]} />
        <meshStandardMaterial color="#5c4a2a" roughness={1} metalness={0} />
      </mesh>

      {/* Modelo central */}
      <group position={[0, yOffset - 2, 0]}>
        <primitive object={cloned} scale={scale} />
      </group>

      {/* Esfera toroidal — emerge del piso al completar los 4 altares */}
      <ToroidalSphere
        position={[0, 0, 0]}
        size={20}
        visible={allActivated}
      />

      {/* Luz central */}
      <pointLight ref={lightRef} position={[0, 15, 0]} color="#ffaa33" intensity={1.5} distance={80} decay={2} />
      <ambientLight intensity={0.3} color="#332211" />
      <directionalLight position={[20, 30, 10]} intensity={0.8} color="#ffcc88" />
      <directionalLight position={[-20, 20, -10]} intensity={0.3} color="#334466" />

      {/* 4 Altares cardinales */}
      {ALTARS.map((altar) => (
        <AltarCircle
          key={altar.dir}
          {...altar}
          activated={activated[altar.itemKey]}
        />
      ))}

      {/* 👽 Geoglifo: Astronauta de Nazca */}
      <Geoglyph svgPath="/geoglyphs/astronauta.svg" position={[-55, 0.1, -55]} size={18} />

      {/* Crop Circle Toroide — aparece debajo del modelo cuando los 4 están activados */}
      <CropCircle
        type="toroid"
        position={[0, 0.3, 0]}
        scale={2}
        visible={allActivated}
      />

      {/* Mensaje final — overlay HTML centrado */}
      {showMessage && (
        <Html center zIndexRange={[100, 0]}>
          <div style={{
            textAlign: 'center',
            animation: 'fadeInMsg 2s ease forwards',
            pointerEvents: 'none',
          }}>
            <p style={{
              fontSize: '42px',
              fontFamily: 'Archeoscope, serif',
              color: '#ffffff',
              letterSpacing: '6px',
              textTransform: 'uppercase',
              textShadow: '0 0 30px #44aaff, 0 0 60px #44aaff',
              margin: 0,
            }}>
              Archeoscope
            </p>
            <p style={{
              fontSize: '28px',
              fontFamily: 'Archeoscope, serif',
              color: '#88ccff',
              letterSpacing: '4px',
              textShadow: '0 0 20px #44aaff',
              marginTop: '12px',
            }}>
              Regresará...
            </p>
            <style>{`
              @keyframes fadeInMsg {
                from { opacity: 0; transform: scale(0.8); }
                to   { opacity: 1; transform: scale(1); }
              }
            `}</style>
          </div>
        </Html>
      )}

      {/* ─── ITEMS SOLTADOS EN EL SUELO ─────────────────────────────── */}
      {/* Si caen sobre su altar → flotan a 2.5m; si no → 1.5m */}

      {tonatiuhOnGround && tonatiuhDropPosition && (
        <DroppableItem
          modelPath="/tonatiuh_aztec_sun.glb"
          position={[tonatiuhDropPosition.x, 0, tonatiuhDropPosition.z]}
          onCollect={onTonatiuhCollect}
          scale={1.5}
          floatHeight={activated.tonatiuh ? 2.5 : 1.5}
          glowColor={activated.tonatiuh ? '#ffffff' : '#ffaa00'}
          itemName="Tonatiuh"
        />
      )}

      {scarabOnGround && scarabDropPosition && (
        <DroppableItem
          modelPath="/escarabajo.glb"
          position={[scarabDropPosition.x, 0, scarabDropPosition.z]}
          onCollect={onScarabCollect}
          scale={1.5}
          floatHeight={activated.scarab ? 2.5 : 1.5}
          glowColor={activated.scarab ? '#ffffff' : '#44cc44'}
          itemName="Escarabajo"
        />
      )}

      {skullOnGround && skullDropPosition && (
        <DroppableItem
          modelPath="/crystal-skull.glb"
          position={[skullDropPosition.x, 0, skullDropPosition.z]}
          onCollect={onSkullCollect}
          scale={1.5}
          floatHeight={activated.skull ? 2.5 : 1.5}
          glowColor={activated.skull ? '#ffffff' : '#aa44ff'}
          itemName="Calavera de Cristal"
        />
      )}

      {magnaBowlOnGround && magnaBowlDropPosition && (
        <DroppableItem
          modelPath="/fuente_magna.glb"
          position={[magnaBowlDropPosition.x, 0, magnaBowlDropPosition.z]}
          onCollect={onMagnaBowlCollect}
          scale={1.5}
          floatHeight={activated.magna ? 2.5 : 1.5}
          glowColor={activated.magna ? '#ffffff' : '#4488ff'}
          itemName="Fuente Magna"
        />
      )}
    </group>
  )
}

// ─── ALTAR CIRCULAR ───────────────────────────────────────────────────────────
function AltarCircle({ label, icon, x, z, color, activated }: {
  label: string; icon: string; x: number; z: number; color: string; dir: string; itemKey: string; activated: boolean
}) {
  const lightRef = useRef<THREE.PointLight>(null)

  useFrame(({ clock }) => {
    if (lightRef.current) {
      lightRef.current.intensity = activated
        ? 2.0 + Math.sin(clock.elapsedTime * 2) * 0.5
        : 0.4 + Math.sin(clock.elapsedTime * 1.2 + x) * 0.2
    }
  })

  const activeColor = activated ? '#ffffff' : color

  return (
    <group position={[x, 1.0, z]}>
      {/* Anillo exterior */}
      <mesh rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[ALTAR_RADIUS - 0.5, ALTAR_RADIUS, 64]} />
        <meshBasicMaterial color={activeColor} transparent opacity={activated ? 1 : 0.9} depthWrite={false} side={THREE.DoubleSide} />
      </mesh>

      {/* Disco interior tenue */}
      <mesh rotation={[-Math.PI / 2, 0, 0]}>
        <circleGeometry args={[ALTAR_RADIUS - 0.5, 64]} />
        <meshBasicMaterial color={color} transparent opacity={activated ? 0.35 : 0.12} depthWrite={false} side={THREE.DoubleSide} />
      </mesh>

      {/* Luz */}
      <pointLight ref={lightRef} color={activated ? '#ffffff' : color} intensity={0.4} distance={18} position={[0, 1, 0]} />
    </group>
  )
}

function LoadingGobekli() {
  return (
    <Html center>
      <div style={{
        background: 'rgba(10, 8, 5, 0.95)', padding: '20px 40px',
        borderRadius: '12px', color: '#ffaa33',
        fontFamily: 'system-ui', textAlign: 'center',
        border: '2px solid rgba(255, 170, 51, 0.4)'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '10px' }}>🏛️</div>
        <div></div>
      </div>
    </Html>
  )
}

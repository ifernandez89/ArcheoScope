'use client'

import { Suspense, useMemo, useEffect, useRef, useState } from 'react'
import { useGLTF, Html } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'
import OlmecCave from './OlmecCave'
import CropCircle from './CropCircle'
import { isMissionCompleted } from '@/types/missionState'

interface VeracruzSceneProps {
  avatarPositionRef?: React.RefObject<THREE.Vector3>
  onOlmecClick?: () => void
  caveQuestActive?: boolean
  onEnterCave?: () => void
}

export default function VeracruzScene({ avatarPositionRef, onOlmecClick, caveQuestActive, onEnterCave }: VeracruzSceneProps) {
  return (
    <Suspense fallback={<LoadingVeracruz />}>
      <VeracruzSceneContent avatarPositionRef={avatarPositionRef} onOlmecClick={onOlmecClick} caveQuestActive={caveQuestActive} onEnterCave={onEnterCave} />
    </Suspense>
  )
}

function VeracruzSceneContent({ avatarPositionRef, onOlmecClick, caveQuestActive, onEnterCave }: VeracruzSceneProps) {
  const olmecModel = useGLTF(getAssetPath('/olmec_head.glb'))
  const groupRef = useRef<THREE.Group>(null)
  const [isStanding, setIsStanding] = useState(false)
  const [clicked, setClicked] = useState(false)
  const rotationRef = useRef(-Math.PI / 2)

  // Escala para que tenga ~8m de alto + calcular Y correcto cuando está de pie
  const { scale, standY } = useMemo(() => {
    const box = new THREE.Box3().setFromObject(olmecModel.scene)
    const size = box.getSize(new THREE.Vector3())
    const sc = 8 / size.y
    // Cuando rotation.x=0, la base del modelo (box.min.y) debe estar en Y=0
    const sy = -box.min.y * sc
    console.log('🗿 Olmec standY:', sy, 'scale:', sc, 'box.min.y:', box.min.y)
    return { scale: sc, standY: sy }
  }, [olmecModel.scene])

  // ✅ POSICIÓN DEFINITIVA DE INICIO - NO MODIFICAR
  // Cabeza acostada de espaldas, cara mirando al cielo, parcialmente hundida en la tierra
  // Ajustada manualmente el 31/03/2026 - esta es la posición correcta para la misión de Veracruz
  const START_Y = -0.74  // hundida 74cm bajo el piso

  // Verificar si la misión está completa para el Crop Circle
  const [missionDone, setMissionDone] = useState(false)
  useEffect(() => {
    // Verificar periódicamente o al inicio
    const check = () => setMissionDone(isMissionCompleted('veracruz', 'deliver_jade_mask'))
    check()
    const interval = setInterval(check, 5000)
    return () => clearInterval(interval)
  }, [])

  const enteredCaveRef = useRef(false)

  // Animación de levantarse + detección de proximidad a la cueva
  useFrame((_, delta) => {
    if (groupRef.current && isStanding) {
      if (rotationRef.current < -0.01) {
        rotationRef.current = Math.min(0, rotationRef.current + delta * 1.5)
        groupRef.current.rotation.x = rotationRef.current
      } else {
        groupRef.current.rotation.x = 0
      }
      if (groupRef.current.position.y < standY - 0.01) {
        groupRef.current.position.y = Math.min(standY, groupRef.current.position.y + delta * 2)
      } else {
        groupRef.current.position.y = standY
      }
    }

    // Detectar si la nave está sobre la cueva (posición [-28, Y, 0], radio ~8)
    if (caveQuestActive && avatarPositionRef?.current && onEnterCave && !enteredCaveRef.current) {
      const pos = avatarPositionRef.current
      const dx = pos.x - (-28)
      const dz = pos.z - 0
      const dist = Math.sqrt(dx * dx + dz * dz)
      if (dist < 8) {
        enteredCaveRef.current = true
        console.log('🌀 Nave sobre la cueva! Transportando al Mictlán...')
        onEnterCave()
      }
    }
  })

  const handleClick = (e: any) => {
    e.stopPropagation()
    if (!clicked) {
      // Primer click: levantarse + diálogo de agradecimiento
      setClicked(true)
      setIsStanding(true)
      setTimeout(() => { if (onOlmecClick) onOlmecClick() }, 1500)
    } else {
      // Clicks posteriores: diálogo interactivo con 3 opciones
      if (onOlmecClick) onOlmecClick()
    }
  }

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

  return (
    <>
      <group>
        {/* Cabeza Colosal Olmeca - acostada de espaldas, hundida 80cm */}
        <group
          ref={groupRef}
          position={[0, START_Y, 0]}
          scale={scale}
          rotation={[-Math.PI / 2, 0, 0]}
          onClick={handleClick}
          onPointerOver={() => { document.body.style.cursor = 'pointer' }}
          onPointerOut={() => { document.body.style.cursor = 'default' }}
        >
          <primitive object={olmecModel.scene} />
        </group>

        <pointLight position={[0, 6, 8]} intensity={2} color="#ffe8c0" distance={30} />
        <pointLight position={[0, 6, -8]} intensity={1} color="#c0d8ff" distance={25} />
        <ambientLight intensity={0.6} />
        <directionalLight position={[10, 15, 5]} intensity={0.9} />

        {/* 🏔️ Cueva olmeca al oeste */}
        <OlmecCave />

        {/* 💠 Crop Circle: Julia Set Fractal (Portal Dimensional) */}
        <CropCircle 
          type="julia" 
          position={[14, 0.4, 12]} 
          scale={18} 
          visible={missionDone} 
        />
      </group>
    </>
  )
}

// Diálogo con el mismo estilo que Quetzalcoatl/Viracocha - exportado para uso fuera del Canvas
export function OlmecDialogue({ onClose }: { onClose: () => void }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 6000)
    return () => clearTimeout(timer)
  }, [onClose])

  return (
    <div
      style={{
        position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
        background: 'rgba(0, 0, 0, 0.7)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        zIndex: 2000,
        animation: 'fadeIn 0.3s ease-out'
      }}
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: 'rgba(20, 15, 10, 0.95)',
          border: '2px solid #c8860a',
          borderRadius: '12px',
          padding: '30px 40px',
          maxWidth: '600px',
          width: '90%',
          boxShadow: '0 0 30px rgba(200, 134, 10, 0.6)',
          animation: 'scaleIn 0.3s ease-out'
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: '20px', fontSize: '48px' }}>🗿</div>

        <div style={{
          color: '#c8860a',
          fontSize: '26px',
          fontWeight: 'bold',
          textAlign: 'center',
          marginBottom: '20px',
          fontFamily: '"Cinzel", "Trajan Pro", serif',
          letterSpacing: '3px',
          textShadow: '0 0 10px rgba(200, 134, 10, 0.8)',
        }}>
          
        </div>

        <div style={{
          color: '#ffffff',
          fontSize: '20px',
          textAlign: 'center',
          marginBottom: '20px',
          fontFamily: '"Cinzel", serif',
          letterSpacing: '1px',
          lineHeight: '1.6',
          textShadow: '0 0 5px rgba(200, 134, 10, 0.3)',
        }}>
          Gracias, viajero... Dormía desde hace milenios. Te saludo desde tiempos antiguos.
        </div>

        <button
          onClick={onClose}
          style={{
            marginTop: '10px',
            padding: '10px 30px',
            fontSize: '16px',
            color: '#c8860a',
            background: 'transparent',
            border: '2px solid #c8860a',
            borderRadius: '8px',
            cursor: 'pointer',
            fontFamily: '"Cinzel", serif',
            letterSpacing: '2px',
            display: 'block',
            margin: '10px auto 0',
            transition: 'all 0.3s ease'
          }}
          onMouseEnter={(e) => { e.currentTarget.style.background = '#c8860a'; e.currentTarget.style.color = '#000' }}
          onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = '#c8860a' }}
        >
          Cerrar
        </button>
      </div>

      <style jsx>{`
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes scaleIn { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
      `}</style>
    </div>
  )
}

function LoadingVeracruz() {
  return (
    <Html center>
      <div style={{
        background: 'rgba(0,0,0,0.8)', padding: '20px 40px',
        borderRadius: '12px', color: 'white',
        fontFamily: 'system-ui', textAlign: 'center',
        border: '2px solid rgba(200,134,10,0.3)'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '10px' }}>🗿</div>
        <div>Cargando Veracruz...</div>
      </div>
    </Html>
  )
}

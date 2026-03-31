'use client'

import { useRef, Suspense, useEffect, useMemo } from 'react'
import { useGLTF, Html } from '@react-three/drei'
import { Vector3 } from 'three'
import { getAssetPath } from '@/lib/paths'
import EasterIslandDialogue from './EasterIslandDialogue'
import RanoKauVolcano, { type VolcanoState } from './RanoKauVolcano'
import { loadMissionState } from '@/types/missionState'

/**
 * Escena de Isla de Pascua (Rapa Nui)
 * Moai y Atlante enfrentados "charlando"
 * Modelos optimizados con compresión Draco
 * Sistema de diálogo sobre la red energética planetaria
 */

/**
 * 🔄 Loading placeholder para Isla de Pascua
 */
function LoadingEasterIsland() {
  return (
    <Html center>
      <div style={{
        background: 'rgba(0, 0, 0, 0.8)',
        padding: '20px 40px',
        borderRadius: '12px',
        color: 'white',
        fontFamily: 'system-ui, sans-serif',
        textAlign: 'center',
        border: '2px solid rgba(255, 215, 0, 0.3)'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '10px' }}>🗿</div>
        <div>Cargando Isla de Pascua...</div>
      </div>
    </Html>
  )
}

interface EasterIslandSceneProps {
  avatarPositionRef?: React.RefObject<Vector3>
}

export default function EasterIslandScene({ avatarPositionRef }: EasterIslandSceneProps) {
  return (
    <Suspense fallback={<LoadingEasterIsland />}>
      <EasterIslandSceneContent avatarPositionRef={avatarPositionRef} />
    </Suspense>
  )
}

function EasterIslandSceneContent({ avatarPositionRef }: EasterIslandSceneProps) {
  const moaiModel = useGLTF(getAssetPath('/moai.glb'))
  const atlanteModel = useGLTF(getAssetPath('/atlante.glb'))

  const moaiNorth    = useMemo(() => moaiModel.scene.clone(true),    [moaiModel.scene])
  const moaiEast     = useMemo(() => moaiModel.scene.clone(true),    [moaiModel.scene])
  const atlanteSouth = useMemo(() => atlanteModel.scene.clone(true), [atlanteModel.scene])
  const atlanteWest  = useMemo(() => atlanteModel.scene.clone(true), [atlanteModel.scene])

  // Estado del volcán según misiones completadas
  const volcanoState = useMemo<VolcanoState>(() => {
    const ms = loadMissionState()
    const total = ms.stats.totalMissionsCompleted
    if (total >= 3) return 'erupting'
    if (total >= 1) return 'active'
    return 'dormant'
  }, [])
  
  // 🎼 Activar arquitectura de Isla de Pascua
  useEffect(() => {
    import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
      const harmonia = getHarmoniaMundi()
      if (harmonia.isEnabled()) {
        harmonia.activateArchitecture('easter-island')
        console.log('🏛️ Arquitectura de Isla de Pascua activada')
      }
    })
    
    return () => {
      import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
        const harmonia = getHarmoniaMundi()
        harmonia.deactivateArchitecture('easter-island')
      })
    }
  }, [])
  
  // Posiciones para el sistema de diálogo
  const moaiPosition = new Vector3(-4, 3, 0)
  const atlantePosition = new Vector3(4, 2, 0)
  
  // Radio del borde - 1 metro adentro del límite visible
  const BORDER = 29

  return (
    <group>
      {/* Moai central - posición y rotación ORIGINALES */}
      <group position={[-4, 3, 0]} rotation={[0, Math.PI / 4 - Math.PI / 6, 0]}>
        <primitive object={moaiModel.scene} scale={5} />
      </group>
      
      {/* Atlante central - posición y rotación ORIGINALES */}
      <group position={[4, 2, 0]} rotation={[0, 0, 0]}>
        <primitive object={atlanteModel.scene} scale={5} />
      </group>

      {/* BORDE NORTE: Moai mirando al sur (hacia el centro) */}
      <group position={[0, 3, -BORDER]} rotation={[0, Math.PI, 0]}>
        <primitive object={moaiNorth} scale={5} />
      </group>

      {/* BORDE SUR: Atlante mirando al norte (hacia el centro) */}
      <group position={[0, 2, BORDER]} rotation={[0, 0, 0]}>
        <primitive object={atlanteSouth} scale={5} />
      </group>

      {/* BORDE ESTE: Moai mirando al oeste (hacia el centro) */}
      <group position={[BORDER, 3, 0]} rotation={[0, -Math.PI / 2, 0]}>
        <primitive object={moaiEast} scale={5} />
      </group>

      {/* BORDE OESTE: Atlante mirando al este (hacia el centro) */}
      <group position={[-BORDER, 2, 0]} rotation={[0, Math.PI / 2, 0]}>
        <primitive object={atlanteWest} scale={5} />
      </group>
      
      {/* Sistema de diálogo entre Moai y Atlante */}
      <EasterIslandDialogue
        moaiPosition={moaiPosition}
        atlantePosition={atlantePosition}
        enabled={true}
      />
      
      {/* 🌋 Volcán Rano Kau - suroeste, igual que el real */}
      <RanoKauVolcano state={volcanoState} />

      {/* Iluminación */}
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={0.8} />
    </group>
  )
}

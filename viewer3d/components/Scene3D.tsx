'use client'

import { useState, useEffect } from 'react'
import ImmersiveScene from './ImmersiveScene'
import PerformanceStats from './PerformanceStats'
import ConversationalAvatar from './ConversationalAvatar'
// import { AudioSystem } from '@/core/audio'  // Deshabilitado para GitHub Pages
import * as THREE from 'three'

export default function Scene3D() {
  // const [audioSystem, setAudioSystem] = useState<AudioSystem | null>(null)  // Deshabilitado
  const [loadedModel, setLoadedModel] = useState<THREE.Object3D | null>(null)
  const [camera, setCamera] = useState<THREE.Camera | null>(null)
  const [showPerformance, setShowPerformance] = useState(true)
  const [spaceUfoActive, setSpaceUfoActive] = useState(false) // OVNI espacial

  // Inicializar sistemas
  useEffect(() => {
    // const audio = new AudioSystem()  // Deshabilitado
    // setAudioSystem(audio)  // Deshabilitado

    return () => {
      // audio.dispose()  // Deshabilitado
    }
  }, [])

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      {/* Escena inmersiva con Globe 3D y modelos */}
      <ImmersiveScene
        onModelLoaded={setLoadedModel}
        onCameraReady={setCamera}
        onModeChange={(mode) => {
          // Mostrar performance solo en modo globo
          setShowPerformance(mode === 'globe')
        }}
        spaceUfoActive={spaceUfoActive}
      />

      {/* Botón de OVNI Espacial - Solo en modo globo */}
      {showPerformance && (
        <button
          onClick={() => setSpaceUfoActive(!spaceUfoActive)}
          style={{
            position: 'absolute',
            top: '20px',
            left: '20px',
            zIndex: 1002,
            padding: '12px 20px',
            background: spaceUfoActive 
              ? 'rgba(139, 92, 246, 0.9)' 
              : 'rgba(75, 85, 99, 0.7)',
            border: spaceUfoActive
              ? '2px solid rgba(139, 92, 246, 1)'
              : '1px solid rgba(255,255,255,0.3)',
            borderRadius: '8px',
            color: 'white',
            fontSize: '14px',
            fontWeight: 'bold',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            transition: 'all 0.2s',
            boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
            backdropFilter: 'blur(10px)'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = spaceUfoActive
              ? 'rgba(139, 92, 246, 1)'
              : 'rgba(75, 85, 99, 0.9)'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = spaceUfoActive
              ? 'rgba(139, 92, 246, 0.9)'
              : 'rgba(75, 85, 99, 0.7)'
          }}
        >
          🛸 {spaceUfoActive ? 'OVNI Activo' : 'Activar OVNI'}
        </button>
      )}

      {/* Performance Stats - Solo en modo globo y desarrollo */}
      {process.env.NODE_ENV === 'development' && showPerformance && <PerformanceStats />}

      {/* Avatar Conversacional */}
      <ConversationalAvatar 
        model={loadedModel}
        camera={camera}
      />
    </div>
  )
}

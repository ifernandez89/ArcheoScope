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
      />

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

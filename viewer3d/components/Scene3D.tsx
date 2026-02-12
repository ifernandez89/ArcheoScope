'use client'

import { useState, useEffect } from 'react'
import ImmersiveScene from './ImmersiveScene'
import PerformanceStats from './PerformanceStats'
import ConversationalAvatar from './ConversationalAvatar'
import { AudioSystem } from '@/core/audio'
import * as THREE from 'three'

export default function Scene3D() {
  const [audioSystem, setAudioSystem] = useState<AudioSystem | null>(null)
  const [loadedModel, setLoadedModel] = useState<THREE.Object3D | null>(null)
  const [camera, setCamera] = useState<THREE.Camera | null>(null)

  // Inicializar sistemas
  useEffect(() => {
    const audio = new AudioSystem()
    setAudioSystem(audio)

    return () => {
      audio.dispose()
    }
  }, [])

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      {/* Escena inmersiva con Globe 3D y modelos */}
      <ImmersiveScene
        onModelLoaded={setLoadedModel}
        onCameraReady={setCamera}
      />

      {/* Performance Stats - Solo en desarrollo */}
      {process.env.NODE_ENV === 'development' && <PerformanceStats />}

      {/* Avatar Conversacional */}
      <ConversationalAvatar 
        model={loadedModel}
        camera={camera}
      />
    </div>
  )
}

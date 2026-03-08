'use client'

import { useState, useEffect } from 'react'
import ImmersiveScene from './ImmersiveScene'
import InGameMenu from './InGameMenu'
import * as THREE from 'three'
import { loadPlayerState, resetPlayerState } from '@/types/player'

export default function Scene3D() {
  const [loadedModel, setLoadedModel] = useState<THREE.Object3D | null>(null)
  const [camera, setCamera] = useState<THREE.Camera | null>(null)
  const [isGlobeMode, setIsGlobeMode] = useState(true)
  const [showMenu, setShowMenu] = useState(false)
  
  // Cargar nave del jugador para la escena del espacio
  const [spaceUfoNumber, setSpaceUfoNumber] = useState(() => {
    const playerState = loadPlayerState()
    if (playerState?.ship?.id) {
      const ufoNum = parseInt(playerState.ship.id.split('_')[1])
      return ufoNum || 1
    }
    return 1
  })

  // Detectar tecla M para abrir menú
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === 'm' || e.key === 'M') {
        setShowMenu(prev => !prev)
      }
      // Detectar F5 para resetear el juego
      if (e.key === 'F5') {
        e.preventDefault()
        resetPlayerState()
        if (typeof window !== 'undefined') {
          sessionStorage.clear()
        }
        console.log('🗑️ F5 presionado - Estado del juego reseteado')
        window.location.reload()
      }
    }
    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [])

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      {/* Escena inmersiva con Globe 3D y modelos */}
      <ImmersiveScene
        onModelLoaded={setLoadedModel}
        onCameraReady={setCamera}
        onModeChange={(mode) => {
          setIsGlobeMode(mode === 'globe')
        }}
        spaceUfoActive={true}
        spaceUfoNumber={spaceUfoNumber}
      />

      {/* Menú in-game */}
      <InGameMenu isOpen={showMenu} onClose={() => setShowMenu(false)} />
    </div>
  )
}

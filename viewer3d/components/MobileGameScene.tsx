'use client'

/**
 * MobileGameScene — Wrapper para el juego mobile
 *
 * Features:
 * - Fuerza modo landscape (horizontal)
 * - Muestra overlay si está en portrait
 * - Carga nave seleccionada desde playerState
 * - spaceUfoActive=true para que la nave aparezca en el espacio
 */

import { Suspense, useEffect, useState } from 'react'
import dynamic from 'next/dynamic'
import { lockLandscape, unlockOrientation, isPortrait, enterFullscreen } from '@/lib/landscapeLock'
import { loadPlayerState } from '@/types/player'

const ImmersiveScene = dynamic(() => import('./ImmersiveScene'), { ssr: false })

export default function MobileGameScene() {
  const [showPortraitOverlay, setShowPortraitOverlay] = useState(false)

  // Leer nave seleccionada del playerState — memoizado para evitar recálculo
  const [spaceUfoNumber] = useState(() => {
    if (typeof window === 'undefined') return 1
    const playerState = loadPlayerState()
    if (playerState?.ship?.id) {
      const ufoNum = parseInt(playerState.ship.id.split('_')[1])
      return ufoNum || 1
    }
    return 1
  })

  // Intentar bloquear en landscape al montar
  useEffect(() => {
    let resizeHandler: (() => void) | null = null
    let orientationHandler: (() => void) | null = null

    const initLandscape = async () => {
      await enterFullscreen()
      const locked = await lockLandscape()
      if (!locked) {
        // Fallback: detectar orientación manualmente
        const checkOrientation = () => setShowPortraitOverlay(isPortrait())
        checkOrientation()
        resizeHandler = checkOrientation
        orientationHandler = checkOrientation
        window.addEventListener('resize', checkOrientation)
        window.addEventListener('orientationchange', checkOrientation)
      }
    }
    initLandscape()

    // Cleanup: remover listeners Y desbloquear orientación
    return () => {
      if (resizeHandler) window.removeEventListener('resize', resizeHandler)
      if (orientationHandler) window.removeEventListener('orientationchange', orientationHandler)
      unlockOrientation()
    }
  }, [])

  if (showPortraitOverlay) {
    return (
      <div style={{
        width: '100vw', height: '100vh', background: '#000',
        display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center',
        color: '#fff', padding: '20px', textAlign: 'center',
      }}>
        <div style={{ fontSize: '60px', marginBottom: '20px' }}>📱↔️</div>
        <h2 style={{ fontSize: '24px', marginBottom: '10px' }}>Rota tu dispositivo</h2>
        <p style={{ fontSize: '16px', color: '#888' }}>Para una mejor experiencia, usa el modo horizontal</p>
      </div>
    )
  }

  return (
    <div style={{
      width: '100vw', height: '100vh',
      background: '#000', overflow: 'hidden', touchAction: 'none',
    }}>
      <Suspense fallback={
        <div style={{
          width: '100%', height: '100%',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          color: '#fff', fontSize: '14px',
        }}>
          Cargando...
        </div>
      }>
        {/* spaceUfoActive=true: nave aparece como puntero en escena espacial */}
        <ImmersiveScene
          spaceUfoActive={true}
          spaceUfoNumber={spaceUfoNumber}
        />
      </Suspense>
    </div>
  )
}

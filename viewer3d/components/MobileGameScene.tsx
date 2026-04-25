'use client'

/**
 * MobileGameScene — Wrapper para el juego mobile
 *
 * Features:
 * - Fuerza modo landscape (horizontal)
 * - Muestra overlay si está en portrait
 * - Usa ImmersiveScene con detección mobile
 * - Botón de menú que guarda estado y permite volver
 */

import { Suspense, useEffect, useState } from 'react'
import dynamic from 'next/dynamic'
import { lockLandscape, unlockOrientation, isPortrait, enterFullscreen } from '@/lib/landscapeLock'

const ImmersiveScene = dynamic(() => import('./ImmersiveScene'), { ssr: false })

export default function MobileGameScene() {
  const [showPortraitOverlay, setShowPortraitOverlay] = useState(false)

  // Intentar bloquear en landscape al montar
  useEffect(() => {
    const initLandscape = async () => {
      // Intentar fullscreen primero (mejora compatibilidad del lock)
      await enterFullscreen()
      // Intentar bloquear orientación
      const locked = await lockLandscape()
      
      if (!locked) {
        // Si no se pudo bloquear, mostrar overlay si está en portrait
        const checkOrientation = () => {
          setShowPortraitOverlay(isPortrait())
        }
        checkOrientation()
        window.addEventListener('resize', checkOrientation)
        window.addEventListener('orientationchange', checkOrientation)
        
        return () => {
          window.removeEventListener('resize', checkOrientation)
          window.removeEventListener('orientationchange', checkOrientation)
        }
      }
    }
    
    initLandscape()
    
    // Cleanup: desbloquear al salir
    return () => {
      unlockOrientation()
    }
  }, [])

  // Overlay para pedir que rote el dispositivo
  if (showPortraitOverlay) {
    return (
      <div style={{
        width: '100vw',
        height: '100vh',
        background: '#000',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        color: '#fff',
        padding: '20px',
        textAlign: 'center',
      }}>
        <div style={{ fontSize: '60px', marginBottom: '20px' }}>📱↔️</div>
        <h2 style={{ fontSize: '24px', marginBottom: '10px' }}>Rota tu dispositivo</h2>
        <p style={{ fontSize: '16px', color: '#888' }}>
          Para una mejor experiencia, usa el modo horizontal
        </p>
      </div>
    )
  }

  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      background: '#000',
      overflow: 'hidden',
      touchAction: 'none',
    }}>
      <Suspense fallback={
        <div style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#fff',
          fontSize: '14px',
        }}>
          Cargando...
        </div>
      }>
        <ImmersiveScene />
      </Suspense>
    </div>
  )
}

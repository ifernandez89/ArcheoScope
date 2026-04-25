'use client'

/**
 * MobileGameScene — Wrapper para el juego mobile
 *
 * Usa ImmersiveScene que ya detecta mobile internamente y ajusta:
 * - Sin botón "Volver al Globo" (solo nueva partida desde menú)
 * - Sin botón "Mostrar Info"
 * - Botón de menú pequeño (☰) en esquina inferior
 * - Botón de habilidades se mantiene
 * - Controles touch: OrbitControls con 1 dedo rota, 2 dedos zoom
 * - Tap en objetos = interactuar (ya funciona con pointer events)
 */

import { Suspense } from 'react'
import dynamic from 'next/dynamic'

const ImmersiveScene = dynamic(() => import('./ImmersiveScene'), { ssr: false })

export default function MobileGameScene() {
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

'use client'

/**
 * Mobile Game — Juego completo para mobile
 *
 * Flujo:
 * 1. Inicia en Solar System 3D (vista globo)
 * 2. Botón coordenadas para acceder a misiones
 * 3. Tap en Tierra para entrar a escenas terrestres
 * 4. Controles touch: 1 dedo rota, 2 dedos zoom, tap = interactuar
 */

import dynamic from 'next/dynamic'

const MobileGameScene = dynamic(() => import('@/components/MobileGameScene'), { ssr: false })

export default function MobileGamePage() {
  return <MobileGameScene />
}

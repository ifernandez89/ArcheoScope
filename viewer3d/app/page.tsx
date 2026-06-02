'use client'

import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { resetPlayerState } from '@/types/player'

// Ruta del logo resuelta en cliente para evitar problemas SSR
const LOGO_PATH = process.env.NODE_ENV === 'production'
  ? '/ArcheoScope/branding/icons/logo-pixel.png'
  : '/branding/icons/logo-pixel.png'

export default function Home() {
  const router = useRouter()
  const [isMobile, setIsMobile] = useState<boolean | null>(null)
  const [pressed, setPressed] = useState(false)

  useEffect(() => {
    const check = () => setIsMobile(
      /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768
    )
    check()
    window.addEventListener('resize', check)
    return () => window.removeEventListener('resize', check)
  }, [])

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === 'F5') {
        e.preventDefault()
        resetPlayerState()
        if (typeof window !== 'undefined') sessionStorage.clear()
        window.location.reload()
      }
    }
    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [])

  const handleEnter = () => router.push('/menu')

  return (
    <main style={{
      width: '100vw', height: '100vh',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: '#011613',
      margin: 0, padding: 0, overflow: 'hidden',
      position: 'relative',
      cursor: 'pointer',
    }}
      onClick={handleEnter}
    >
      {/* Logo — clickeable en toda la pantalla */}
      <div style={{
        position: 'absolute', inset: 0,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        pointerEvents: 'none',
        opacity: pressed ? 0.75 : 0.9,
        transition: 'opacity 0.15s ease',
      }}>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={LOGO_PATH}
          alt="Archeoscope — toca para entrar"
          style={{
            maxWidth: isMobile === false ? '90vw' : '95vw',
            maxHeight: isMobile === false ? '90vh' : '75vh',
            objectFit: 'contain',
            filter: 'drop-shadow(0 0 25px rgba(0,255,255,0.4))',
            userSelect: 'none',
            WebkitUserSelect: 'none',
            draggable: false,
          } as React.CSSProperties}
          draggable={false}
        />
      </div>

      {/* Indicador sutil "toca para continuar" — aparece después de que isMobile se resuelve */}
      {isMobile !== null && (
        <div style={{
          position: 'absolute',
          bottom: '32px',
          left: '50%',
          transform: 'translateX(-50%)',
          fontSize: '12px',
          color: 'rgba(255,255,255,0.3)',
          letterSpacing: '3px',
          textTransform: 'uppercase',
          fontFamily: 'inherit',
          pointerEvents: 'none',
          animation: 'pulse 2.5s ease-in-out infinite',
        }}>
          {isMobile ? 'toca para continuar' : 'click para continuar'}
        </div>
      )}

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 0.3 }
          50%       { opacity: 0.7 }
        }
        main:active { opacity: 0.9; }
      `}</style>
    </main>
  )
}

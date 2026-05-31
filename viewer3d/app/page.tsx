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

  return (
    <main style={{
      width: '100vw', height: '100vh',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: '#011613',
      margin: 0, padding: 0, overflow: 'hidden',
      position: 'relative'
    }}>
      {/* Logo pixel como fondo principal */}
      <div style={{
        position: 'absolute', inset: 0,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        pointerEvents: 'none',
        opacity: 0.9
      }}>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={LOGO_PATH}
          alt="Archeoscope"
          style={{
            maxWidth: isMobile === false ? '90vw' : '95vw',
            maxHeight: isMobile === false ? '90vh' : '75vh',
            objectFit: 'contain',
            filter: 'drop-shadow(0 0 25px rgba(0,255,255,0.4))',
            userSelect: 'none'
          }}
        />
      </div>

      {/* Botón Entrar — oculto hasta detectar dispositivo para evitar flash */}
      {isMobile !== null && (isMobile ? (
        /* MOBILE: centrado abajo, ancho generoso, fácil de tocar */
        <button
          onClick={() => router.push('/menu')}
          style={{
            position: 'absolute',
            bottom: '48px',
            left: '50%',
            transform: 'translateX(-50%)',
            zIndex: 10,
            width: 'min(320px, 80vw)',
            padding: '18px 0',
            fontSize: '18px',
            fontWeight: 'normal',
            color: '#ffffff',
            background: 'rgba(1,22,19,0.85)',
            border: '2px solid rgba(255,255,255,0.7)',
            borderRadius: '14px',
            cursor: 'pointer',
            letterSpacing: '3px',
            textTransform: 'uppercase',
            fontFamily: 'inherit',
            backdropFilter: 'blur(8px)',
            WebkitTapHighlightColor: 'transparent',
            touchAction: 'manipulation',
            transition: 'all 0.2s ease',
            minHeight: '56px',
          }}
          onTouchStart={(e) => {
            e.currentTarget.style.background = 'rgba(255,255,255,0.15)'
            e.currentTarget.style.borderColor = '#ffffff'
          }}
          onTouchEnd={(e) => {
            e.currentTarget.style.background = 'rgba(1,22,19,0.85)'
            e.currentTarget.style.borderColor = 'rgba(255,255,255,0.7)'
          }}
        >
          Entrar
        </button>
      ) : (
        /* PC: esquina inferior derecha — comportamiento original */
        <button
          onClick={() => router.push('/menu')}
          style={{
            position: 'absolute', bottom: '40px', right: '40px', zIndex: 10,
            padding: '16px 48px', fontSize: '20px', fontWeight: 'bold',
            color: '#ffffff', background: '#011613',
            border: '2px solid #ffffff', borderRadius: '8px',
            cursor: 'pointer', transition: 'all 0.3s ease',
            fontFamily: 'inherit', letterSpacing: '2px', textTransform: 'uppercase',
            backdropFilter: 'blur(4px)'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = '#ffffff'
            e.currentTarget.style.color = '#011613'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = '#011613'
            e.currentTarget.style.color = '#ffffff'
          }}
        >
          Entrar
        </button>
      ))}
    </main>
  )
}

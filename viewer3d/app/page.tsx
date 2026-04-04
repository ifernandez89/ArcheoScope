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
      background: '#061a19',
      margin: 0, padding: 0, overflow: 'hidden',
      position: 'relative'
    }}>
      {/* Logo pixel como fondo principal */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          pointerEvents: "none", // no bloquea clicks del menú
          opacity: 0.9
        }}
      >
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={LOGO_PATH}
          alt="Archeoscope"
          style={{
            maxWidth: "60vw",
            maxHeight: "60vh",
            objectFit: "contain",
            filter: "drop-shadow(0 0 25px rgba(0,255,255,0.4))",
            userSelect: "none"
          }}
        />
      </div>

      {/* Botón Entrar - esquina inferior derecha */}
      <button
        onClick={() => router.push('/menu')}
        style={{
          position: 'absolute', bottom: '40px', right: '40px', zIndex: 10,
          padding: '16px 48px', fontSize: '20px', fontWeight: 'bold',
          color: '#ffffff', background: 'rgba(0,0,0,0.6)',
          border: '2px solid #ffffff', borderRadius: '8px',
          cursor: 'pointer', transition: 'all 0.3s ease',
          fontFamily: 'inherit', letterSpacing: '2px', textTransform: 'uppercase',
          backdropFilter: 'blur(4px)'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = '#ffffff'
          e.currentTarget.style.color = '#000000'
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'rgba(0,0,0,0.6)'
          e.currentTarget.style.color = '#ffffff'
        }}
      >
        Entrar
      </button>
    </main>
  )
}

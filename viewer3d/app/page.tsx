'use client'

import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import Image from 'next/image'
import { resetPlayerState } from '@/types/player'

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
      background: '#000', margin: 0, padding: 0, overflow: 'hidden',
      position: 'relative'
    }}>
      {/* Logo pixel como fondo principal */}
      <div style={{
        position: 'absolute', inset: 0,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        opacity: 0.85
      }}>
        <Image
          src="/branding/icons/logo-pixel.png"
          alt="Archeoscope"
          fill
          style={{ objectFit: 'contain', padding: '40px' }}
          priority
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

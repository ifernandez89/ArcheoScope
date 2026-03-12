'use client'

import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { resetPlayerState } from '@/types/player'

export default function MenuPage() {
  const router = useRouter()
  const [hasActiveGame, setHasActiveGame] = useState(false)

  // NO verificar localStorage - solo mostrar Continuar si viene de una sesión activa
  useEffect(() => {
    // Verificar si hay una flag de sesión activa (no persistente)
    const sessionActive = sessionStorage.getItem('game_session_active')
    setHasActiveGame(sessionActive === 'true')
  }, [])

  // Detectar F5 para resetear el juego
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === 'F5') {
        e.preventDefault()
        // Limpiar todo el estado
        resetPlayerState()
        if (typeof window !== 'undefined') {
          sessionStorage.clear()
          localStorage.clear()
        }
        console.log('🗑️ F5 presionado - Estado del juego reseteado')
        // Recargar la página
        window.location.reload()
      }
    }
    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [])

  const menuOptions = [
    ...(hasActiveGame ? [{ label: 'Continuar', path: '/game' }] : []),
    { label: 'Player', path: '/player-setup' },
    { label: 'Audio', path: '/menu/audio' },
    { label: 'Controles', path: '/menu/controls' },
    { label: 'Video', path: '/menu/video' },
    { label: 'Información', path: '/menu/info' }
  ]

  return (
    <main style={{
      width: '100vw',
      height: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: '#000000',
      margin: 0,
      padding: 0,
      overflow: 'hidden'
    }}>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '30px',
        alignItems: 'center'
      }}>
        {menuOptions.map((option) => (
          <button
            key={option.label}
            onClick={() => router.push(option.path)}
            style={{
              padding: '20px 80px',
              fontSize: '24px',
              fontWeight: 'bold',
              color: option.label === 'Continuar' ? '#000000' : '#ffffff',
              background: option.label === 'Continuar' ? '#4a9eff' : 'transparent',
              border: option.label === 'Continuar' ? '2px solid #4a9eff' : '2px solid #ffffff',
              borderRadius: '8px',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              fontFamily: 'inherit',
              letterSpacing: '2px',
              textTransform: 'uppercase',
              width: '350px'
            }}
            onMouseEnter={(e) => {
              if (option.label === 'Continuar') {
                e.currentTarget.style.background = '#6ab7ff'
                e.currentTarget.style.borderColor = '#6ab7ff'
              } else {
                e.currentTarget.style.background = '#ffffff'
                e.currentTarget.style.color = '#000000'
              }
            }}
            onMouseLeave={(e) => {
              if (option.label === 'Continuar') {
                e.currentTarget.style.background = '#4a9eff'
                e.currentTarget.style.borderColor = '#4a9eff'
              } else {
                e.currentTarget.style.background = 'transparent'
                e.currentTarget.style.color = '#ffffff'
              }
            }}
          >
            {option.label}
          </button>
        ))}
      </div>
    </main>
  )
}

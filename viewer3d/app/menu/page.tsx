'use client'

import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { resetPlayerState } from '@/types/player'
import { resetMissionState } from '@/types/missionState'
import { resetGameSettings } from '@/types/gameSettings'
import { getAssetPath } from '@/lib/paths'

const LOGO_MAIN = process.env.NODE_ENV === 'production'
  ? '/ArcheoScope/branding/logo/logo-main.png'
  : '/branding/logo/logo-main.png'

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
        handleNewGame()
        console.log('🗑️ F5 presionado - Estado del juego reseteado')
        // Recargar la página
        window.location.reload()
      }
    }
    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [])

  // Handler para nueva partida - resetea todos los estados
  const handleNewGame = () => {
    console.log('🎮 Iniciando nueva partida - Reseteando todos los estados...')
    
    // Resetear estado del jugador
    resetPlayerState()
    
    // Resetear estado de misiones
    resetMissionState()
    
    // Resetear configuración del juego (opcional - mantiene preferencias de audio/video)
    // resetGameSettings()
    
    // Limpiar sessionStorage
    if (typeof window !== 'undefined') {
      sessionStorage.clear()
      // Limpiar inventario
      localStorage.removeItem('inv_scarab')
      localStorage.removeItem('inv_skull')
      localStorage.removeItem('inv_tonatiuh')
      localStorage.removeItem('inv_rock')
      localStorage.removeItem('inv_magna_bowl')
    }
    
    console.log('✅ Todos los estados reseteados - Comenzando nueva partida')
    
    // Ir a player-setup para configurar nueva partida
    router.push('/player-setup')
  }

  const menuOptions = [
    ...(hasActiveGame ? [{ label: 'Continuar', path: '/game', action: null }] : []),
    { label: 'Nueva', path: null, action: handleNewGame },
    { label: 'Audio', path: '/menu/audio', action: null },
    { label: 'Controles', path: '/menu/controls', action: null },
    { label: 'Información', path: '/menu/info', action: null }
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
        gap: '12px',
        alignItems: 'center'
      }}>
        {/* Logo principal con glow sutil */}
        <div style={{
          marginBottom: '10px',
          animation: 'logoPulse 3s ease-in-out infinite'
        }}>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={LOGO_MAIN}
            alt="Archeoscope: The Forgotten Relics"
            style={{ width: '200px', height: '200px', objectFit: 'contain' }}
          />
        </div>

        <style>{`
          @keyframes logoPulse {
            0%, 100% { filter: drop-shadow(0 0 18px rgba(102, 126, 234, 0.5)); }
            50% { filter: drop-shadow(0 0 30px rgba(102, 126, 234, 0.85)); }
          }
        `}</style>
        {menuOptions.map((option) => (
          <button
            key={option.label}
            onClick={() => {
              if (option.action) {
                option.action()
              } else if (option.path) {
                router.push(option.path)
              }
            }}
            style={{
              padding: '16px 64px',
              fontSize: '20px',
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

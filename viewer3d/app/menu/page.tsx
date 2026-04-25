'use client'

import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { resetPlayerState, loadPlayerState } from '@/types/player'
import { resetMissionState } from '@/types/missionState'
import { resetGameSettings } from '@/types/gameSettings'
import { getAssetPath } from '@/lib/paths'

const LOGO_MAIN = process.env.NODE_ENV === 'production'
  ? '/ArcheoScope/branding/logo/logo-main.png'
  : '/branding/logo/logo-main.png'

export default function MenuPage() {
  const router = useRouter()
  const [isMobile, setIsMobile] = useState(false)
  const [hasActiveGame, setHasActiveGame] = useState(false)

  useEffect(() => {
    const check = () => setIsMobile(
      /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768
    )
    check()
    window.addEventListener('resize', check)
    return () => window.removeEventListener('resize', check)
  }, [])

  // Detectar si hay una partida activa (para mostrar "Continuar")
  useEffect(() => {
    const mobileGameActive = sessionStorage.getItem('mobile_game_active') === 'true'
    const playerState = loadPlayerState()
    // Hay partida activa si: flag de sesión activo Y hay estado de jugador guardado
    setHasActiveGame(mobileGameActive && !!playerState?.playerName)
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
    
    // 🔇 MATAR todos los sonidos — cerrar AudioContext directamente
    if (typeof window !== 'undefined') {
      try {
        // Método nuclear: cerrar todos los AudioContext activos
        // Esto mata lluvia, viento, truenos, tornado, Harmonia Mundi, todo
        import('@/systems/ProceduralAudio').then(({ getProceduralAudio }) => {
          try { getProceduralAudio().dispose() } catch {}
        }).catch(() => {})

        import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
          try { getHarmoniaMundi().dispose() } catch {}
        }).catch(() => {})

        // Fallback: suspender todos los AudioContext del navegador
        // @ts-ignore — acceso a propiedad no estándar pero funcional
        if (window.AudioContext || (window as any).webkitAudioContext) {
          // Buscar y cerrar cualquier AudioContext huérfano
          const origClose = AudioContext.prototype.close
          document.querySelectorAll('audio, video').forEach(el => {
            try { (el as HTMLMediaElement).pause(); (el as HTMLMediaElement).src = '' } catch {}
          })
        }
      } catch {}
    }
    
    // Limpiar sessionStorage
    if (typeof window !== 'undefined') {
      sessionStorage.clear()
      localStorage.removeItem('inv_scarab')
      localStorage.removeItem('inv_skull')
      localStorage.removeItem('inv_tonatiuh')
      localStorage.removeItem('inv_rock')
      localStorage.removeItem('inv_magna_bowl')
      localStorage.removeItem('inv_magna_bowl_original')
      localStorage.removeItem('game_timer_seconds')
    }
    
    console.log('✅ Todos los estados reseteados - Comenzando nueva partida')
    router.push('/player-setup')
  }

  // Handler para nueva partida MOBILE — va a player-setup con flag mobile
  const handleNewGameMobile = () => {
    console.log('📱 Iniciando nueva partida MOBILE...')
    // Limpiar flag de partida activa
    sessionStorage.removeItem('mobile_game_active')
    handleNewGame() // Resetea todo igual
    // El flag isMobile se detecta en player-setup para saltar training
  }

  // Handler para continuar partida MOBILE — vuelve al juego
  const handleContinueGame = () => {
    console.log('📱 Continuando partida MOBILE...')
    router.push('/mobile-game')
  }

  const menuOptions = [
    { label: 'Nueva', path: null, action: handleNewGame },
    { label: 'Audio', path: '/menu/audio', action: null },
    { label: 'Video', path: '/menu/video', action: null },
    { label: 'Controles', path: '/menu/controls', action: null },
    { label: 'Astrología', path: '/menu/astrology', action: null },
    { label: 'Calendarios', path: '/menu/calendarios', action: null },
    { label: 'Información', path: '/menu/info', action: null }
  ]

  // Mobile: Continuar (si hay partida), Nueva, Audio, Controles, etc.
  const mobileOptions = [
    // Mostrar "Continuar" solo si hay partida activa
    ...(hasActiveGame ? [{ label: 'Continuar', path: null, action: handleContinueGame }] : []),
    { label: 'Nueva', path: null, action: handleNewGameMobile },
    { label: 'Audio', path: '/menu/audio', action: null },
    { label: 'Controles', path: '/menu/controls', action: null },
    { label: 'Astrología', path: '/menu/astrology', action: null },
    { label: 'Calendarios', path: '/menu/calendarios', action: null },
    { label: 'Información', path: '/menu/info', action: null },
  ]

  const visibleOptions = isMobile ? mobileOptions : menuOptions

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
        {visibleOptions.map((option) => (
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
              color: '#ffffff',
              background: 'transparent',
              border: '2px solid #ffffff',
              borderRadius: '8px',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              fontFamily: 'inherit',
              letterSpacing: '2px',
              textTransform: 'uppercase',
              width: '350px'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#ffffff'
              e.currentTarget.style.color = '#000000'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
              e.currentTarget.style.color = '#ffffff'
            }}
          >
            {option.label}
          </button>
        ))}
      </div>
    </main>
  )
}

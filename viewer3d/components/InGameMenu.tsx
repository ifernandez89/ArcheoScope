'use client'

import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { loadGameSettings, updateAudioSettings } from '@/types/gameSettings'
import { resetPlayerState } from '@/types/player'
import { resetMissionState } from '@/types/missionState'
import { isHelpEnabled, toggleHelp } from '@/systems/helpSystem'

interface InGameMenuProps {
  isOpen: boolean
  onClose: () => void
}

export default function InGameMenu({ isOpen, onClose }: InGameMenuProps) {
  const router = useRouter()
  const [showAudioSettings, setShowAudioSettings] = useState(false)
  const [masterVolume, setMasterVolume] = useState(70)   // Clima + efectos
  const [harmoniaVolume, setHarmoniaVolume] = useState(70) // Música de esferas
  const [helpOn, setHelpOn] = useState(true)

  // Cargar volumen guardado cuando se abre el menú
  useEffect(() => {
    if (isOpen) {
      const settings = loadGameSettings()
      setMasterVolume(Math.round(settings.audio.masterVolume * 100))
      setHarmoniaVolume(Math.round((settings.audio.musicVolume ?? 0.7) * 100))
      setHelpOn(isHelpEnabled())
      console.log('🔊 Volúmenes cargados en InGameMenu:', {
        master: settings.audio.masterVolume,
        harmonia: settings.audio.musicVolume
      })
    }
  }, [isOpen])

  // Sincronizar estado de ayuda con eventos externos
  useEffect(() => {
    const handler = (e: Event) => setHelpOn((e as CustomEvent).detail.enabled)
    window.addEventListener('help-toggle', handler)
    return () => window.removeEventListener('help-toggle', handler)
  }, [])

  // Cerrar con ESC
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        if (showAudioSettings) {
          setShowAudioSettings(false)
        } else {
          onClose()
        }
      }
    }
    window.addEventListener('keydown', handleEsc)
    return () => window.removeEventListener('keydown', handleEsc)
  }, [isOpen, onClose, showAudioSettings])

  // Guardar volumen
  const handleSaveVolume = () => {
    const vol = masterVolume / 100
    const harmVol = harmoniaVolume / 100

    // Guardar en gameSettings
    updateAudioSettings({
      masterVolume: vol,
      musicVolume: harmVol,
      sfxVolume: vol
    })
    
    console.log('🔊 Volúmenes guardados desde InGameMenu:', { master: vol, harmonia: harmVol })
    setShowAudioSettings(false)
  }

  // Handler para nueva partida - resetea todos los estados
  const handleNewGame = () => {
    console.log('🎮 Iniciando nueva partida desde InGameMenu - Reseteando todos los estados...')
    
    // Resetear estado del jugador
    resetPlayerState()
    
    // Resetear estado de misiones
    resetMissionState()
    
    // Limpiar sessionStorage
    if (typeof window !== 'undefined') {
      sessionStorage.clear()
    }
    
    console.log('✅ Todos los estados reseteados - Redirigiendo a player-setup')
    
    // Ir a player-setup para configurar nueva partida
    router.push('/player-setup')
  }

  if (!isOpen) return null

  // Mostrar configuración de audio
  if (showAudioSettings) {
    return (
      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          background: 'rgba(0, 0, 0, 0.85)',
          backdropFilter: 'blur(10px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 9999,
          animation: 'fadeIn 0.2s ease-out'
        }}
      >
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '40px',
            alignItems: 'center',
            padding: '40px'
          }}
        >
          <h1 style={{
            color: '#ffffff',
            fontSize: '48px',
            margin: '0',
            letterSpacing: '4px',
            textTransform: 'uppercase',
            fontFamily: 'Archeoscope, serif'
          }}>
            Audio
          </h1>

          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '40px',
            width: '600px'
          }}>
            {/* Volumen General */}
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '15px'
            }}>
              <label style={{
                color: '#ffffff',
                fontSize: '22px',
                letterSpacing: '2px',
                textTransform: 'uppercase'
              }}>
                🌦️ Volumen General: {masterVolume}%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={masterVolume}
                onChange={(e) => setMasterVolume(parseInt(e.target.value))}
                style={{
                  width: '100%',
                  height: '8px',
                  borderRadius: '4px',
                  outline: 'none',
                  background: `linear-gradient(to right, #4a9eff 0%, #4a9eff ${masterVolume}%, #333333 ${masterVolume}%, #333333 100%)`,
                  cursor: 'pointer'
                }}
              />
              <span style={{ fontSize: '16px', color: '#888' }}>
                Controla el clima, lluvia, viento y efectos de sonido
              </span>
            </div>

            {/* Separador */}
            <div style={{ height: '1px', background: '#333' }} />

            {/* Música de Esferas */}
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '15px'
            }}>
              <label style={{
                color: '#FFD700',
                fontSize: '22px',
                letterSpacing: '2px',
                textTransform: 'uppercase'
              }}>
                🎼 Música de las Esferas: {harmoniaVolume}%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={harmoniaVolume}
                onChange={(e) => setHarmoniaVolume(parseInt(e.target.value))}
                style={{
                  width: '100%',
                  height: '8px',
                  borderRadius: '4px',
                  outline: 'none',
                  background: `linear-gradient(to right, #FFD700 0%, #FFD700 ${harmoniaVolume}%, #333333 ${harmoniaVolume}%, #333333 100%)`,
                  cursor: 'pointer'
                }}
              />
              <span style={{ fontSize: '16px', color: '#888' }}>
                Música cósmica procedural — se despierta con cada misión completada
              </span>
            </div>
          </div>

          <div style={{
            display: 'flex',
            gap: '20px',
            marginTop: '20px'
          }}>
            <button
              onClick={() => setShowAudioSettings(false)}
              style={{
                padding: '15px 40px',
                fontSize: '18px',
                color: '#ffffff',
                background: 'transparent',
                border: '2px solid #ffffff',
                borderRadius: '8px',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                letterSpacing: '2px',
                textTransform: 'uppercase'
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
              Cancelar
            </button>

            <button
              onClick={handleSaveVolume}
              style={{
                padding: '15px 40px',
                fontSize: '18px',
                color: '#000000',
                background: '#4a9eff',
                border: '2px solid #4a9eff',
                borderRadius: '8px',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                letterSpacing: '2px',
                textTransform: 'uppercase'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = '#6ab7ff'
                e.currentTarget.style.borderColor = '#6ab7ff'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = '#4a9eff'
                e.currentTarget.style.borderColor = '#4a9eff'
              }}
            >
              Guardar
            </button>
          </div>

          <div style={{
            color: '#888888',
            fontSize: '17px',
            marginTop: '10px',
            letterSpacing: '1px'
          }}>
            Presiona ESC para volver
          </div>
        </div>

        <style jsx>{`
          @keyframes fadeIn {
            from {
              opacity: 0;
            }
            to {
              opacity: 1;
            }
          }
        `}</style>
      </div>
    )
  }

  // Menú principal — mismas opciones generales que el menú principal del juego
  const menuOptions = [
    { label: 'Nueva', action: handleNewGame, isHelp: false },
    { label: 'Audio', action: () => setShowAudioSettings(true), isHelp: false },
    { label: 'Video', action: () => router.push('/menu/video'), isHelp: false },
    { label: 'Controles', action: () => router.push('/menu/controls'), isHelp: false },
    { label: 'Constelaciones', action: () => router.push('/constellations'), isHelp: false },
    { label: 'Calendarios', action: () => router.push('/menu/calendarios'), isHelp: false },
    { label: helpOn ? 'Ayuda ON' : 'Ayuda OFF', action: () => { const next = toggleHelp(); setHelpOn(next) }, isHelp: true },
    { label: 'Información', action: () => router.push('/menu/info'), isHelp: false }
  ]

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        background: 'rgba(0, 0, 0, 0.85)',
        backdropFilter: 'blur(10px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 9999,
        animation: 'fadeIn 0.2s ease-out'
      }}
      onClick={onClose}
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '12px',
          alignItems: 'center',
          maxHeight: '100vh',
          overflowY: 'auto',
          padding: '20px 0',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <h1 style={{
          color: '#ffffff',
          fontSize: '40px',
          margin: '0 0 12px 0',
          letterSpacing: '4px',
          textTransform: 'uppercase',
          fontFamily: 'Archeoscope, serif'
        }}>
          Menú
        </h1>

        {menuOptions.map((option) => {
          const ayudaOn = option.label === 'Ayuda ON'
          return (
            <button
              key={option.label}
              onClick={option.action}
              style={{
                padding: '14px 60px',
                fontSize: '20px',
                fontWeight: 'bold',
                color: option.isHelp ? (ayudaOn ? '#22c55e' : 'rgba(255,255,255,0.4)') : '#ffffff',
                background: 'transparent',
                border: `2px solid ${option.isHelp ? (ayudaOn ? '#22c55e' : 'rgba(255,255,255,0.25)') : '#ffffff'}`,
                borderRadius: '8px',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                fontFamily: 'inherit',
                letterSpacing: '2px',
                textTransform: 'uppercase',
                minWidth: '350px'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = option.isHelp
                  ? (ayudaOn ? '#22c55e' : 'rgba(255,255,255,0.15)')
                  : '#ffffff'
                e.currentTarget.style.color = option.isHelp
                  ? (ayudaOn ? '#000000' : '#ffffff')
                  : '#000000'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'transparent'
                e.currentTarget.style.color = option.isHelp
                  ? (ayudaOn ? '#22c55e' : 'rgba(255,255,255,0.4)')
                  : '#ffffff'
              }}
            >
              {option.label}
            </button>
          )
        })}

        <div style={{
          color: '#888888',
          fontSize: '17px',
          marginTop: '20px',
          letterSpacing: '1px'
        }}>
          Presiona ESC o M para cerrar
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }
      `}</style>
    </div>
  )
}

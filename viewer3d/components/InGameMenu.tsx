'use client'

import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { loadGameSettings, updateAudioSettings } from '@/types/gameSettings'
import { resetPlayerState } from '@/types/player'
import { resetMissionState } from '@/types/missionState'

interface InGameMenuProps {
  isOpen: boolean
  onClose: () => void
}

export default function InGameMenu({ isOpen, onClose }: InGameMenuProps) {
  const router = useRouter()
  const [showAudioSettings, setShowAudioSettings] = useState(false)
  const [masterVolume, setMasterVolume] = useState(70)   // Clima + efectos
  const [harmoniaVolume, setHarmoniaVolume] = useState(70) // Música de esferas

  // Cargar volumen guardado cuando se abre el menú
  useEffect(() => {
    if (isOpen) {
      const settings = loadGameSettings()
      setMasterVolume(Math.round(settings.audio.masterVolume * 100))
      setHarmoniaVolume(Math.round((settings.audio.musicVolume ?? 0.7) * 100))
      console.log('🔊 Volúmenes cargados en InGameMenu:', {
        master: settings.audio.masterVolume,
        harmonia: settings.audio.musicVolume
      })
    }
  }, [isOpen])

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

  // Menú principal
  const menuOptions = [
    { label: 'Nueva', action: handleNewGame },
    { label: 'Audio', action: () => setShowAudioSettings(true) },
    { label: 'Controles', action: () => router.push('/menu/controls') },
    { label: 'Información', action: () => router.push('/menu/info') }
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
          gap: '20px',
          alignItems: 'center'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <h1 style={{
          color: '#ffffff',
          fontSize: '48px',
          margin: '0 0 20px 0',
          letterSpacing: '4px',
          textTransform: 'uppercase',
          fontFamily: 'Archeoscope, serif'
        }}>
          Menú
        </h1>

        {menuOptions.map((option) => (
          <button
            key={option.label}
            onClick={option.action}
            style={{
              padding: '20px 80px',
              fontSize: '24px',
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
              minWidth: '350px'
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

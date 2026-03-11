'use client'

import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import { loadPlayerState, savePlayerState } from '@/types/player'

export default function AudioPage() {
  const router = useRouter()
  const [masterVolume, setMasterVolume] = useState(70)
  const [musicVolume, setMusicVolume] = useState(70)
  const [sfxVolume, setSfxVolume] = useState(80)

  // Cargar volúmenes guardados
  useEffect(() => {
    const playerState = loadPlayerState()
    if (playerState?.settings) {
      const master = Math.round((playerState.settings.masterVolume || 0.7) * 100)
      
      setMasterVolume(master)
      setMusicVolume(master)
      setSfxVolume(master)
      
      console.log('🔊 Volumen cargado desde playerState:', master)
    }
  }, [])

  // Guardar cambios - SOLO masterVolume es el que importa
  const handleSave = () => {
    const playerState = loadPlayerState()
    if (playerState) {
      // SOLO guardamos masterVolume, los demás son visuales
      playerState.settings.masterVolume = masterVolume / 100
      playerState.settings.musicVolume = masterVolume / 100
      playerState.settings.sfxVolume = masterVolume / 100
      savePlayerState(playerState)
      
      console.log('🔊 Volumen guardado:', masterVolume / 100)
    }
    router.push('/menu')
  }

  return (
    <main style={{
      width: '100vw',
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      background: '#000000',
      margin: 0,
      padding: 0,
      overflow: 'hidden',
      color: '#ffffff'
    }}>
      <h1 style={{
        fontSize: '48px',
        marginBottom: '60px',
        letterSpacing: '4px'
      }}>
        AUDIO
      </h1>

      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '40px',
        width: '500px'
      }}>
        {/* Volumen General */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '15px'
        }}>
          <label style={{
            fontSize: '20px',
            letterSpacing: '2px',
            textTransform: 'uppercase'
          }}>
            Volumen General: {masterVolume}%
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={masterVolume}
            onChange={(e) => {
              const value = parseInt(e.target.value)
              setMasterVolume(value)
              setMusicVolume(value)
              setSfxVolume(value)
            }}
            style={{
              width: '100%',
              height: '8px',
              borderRadius: '4px',
              outline: 'none',
              background: `linear-gradient(to right, #4a9eff 0%, #4a9eff ${masterVolume}%, #333333 ${masterVolume}%, #333333 100%)`,
              cursor: 'pointer'
            }}
          />
        </div>

        {/* Volumen Música */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '15px'
        }}>
          <label style={{
            fontSize: '20px',
            letterSpacing: '2px',
            textTransform: 'uppercase'
          }}>
            Música: {musicVolume}%
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={musicVolume}
            onChange={(e) => setMusicVolume(parseInt(e.target.value))}
            style={{
              width: '100%',
              height: '8px',
              borderRadius: '4px',
              outline: 'none',
              background: `linear-gradient(to right, #4a9eff 0%, #4a9eff ${musicVolume}%, #333333 ${musicVolume}%, #333333 100%)`,
              cursor: 'pointer'
            }}
          />
        </div>

        {/* Volumen Efectos */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '15px'
        }}>
          <label style={{
            fontSize: '20px',
            letterSpacing: '2px',
            textTransform: 'uppercase'
          }}>
            Efectos de Sonido: {sfxVolume}%
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={sfxVolume}
            onChange={(e) => setSfxVolume(parseInt(e.target.value))}
            style={{
              width: '100%',
              height: '8px',
              borderRadius: '4px',
              outline: 'none',
              background: `linear-gradient(to right, #4a9eff 0%, #4a9eff ${sfxVolume}%, #333333 ${sfxVolume}%, #333333 100%)`,
              cursor: 'pointer'
            }}
          />
        </div>
      </div>

      {/* Botones */}
      <div style={{
        display: 'flex',
        gap: '20px',
        marginTop: '60px'
      }}>
        <button
          onClick={() => router.push('/menu')}
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
          onClick={handleSave}
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
    </main>
  )
}

'use client'

import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import { loadGameSettings, updateAudioSettings } from '@/types/gameSettings'

export default function AudioPage() {
  const router = useRouter()
  const [masterVolume, setMasterVolume] = useState(70)
  const [musicVolume, setMusicVolume] = useState(70)
  const [sfxVolume, setSfxVolume] = useState(80)

  // Cargar volúmenes guardados desde gameSettings
  useEffect(() => {
    const settings = loadGameSettings()
    const master = Math.round(settings.audio.masterVolume * 100)
    const music = Math.round(settings.audio.musicVolume * 100)
    const sfx = Math.round(settings.audio.sfxVolume * 100)
    
    setMasterVolume(master)
    setMusicVolume(music)
    setSfxVolume(sfx)
    
    console.log('🔊 Volúmenes cargados desde gameSettings:', { master, music, sfx })
  }, [])

  // Guardar cambios - SOLO masterVolume es el que importa
  const handleSave = () => {
    // Guardar en gameSettings
    updateAudioSettings({
      masterVolume: masterVolume / 100,
      musicVolume: masterVolume / 100,
      sfxVolume: masterVolume / 100
    })
    
    console.log('🔊 Volumen guardado en gameSettings:', masterVolume / 100)
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
            padding: '20px 80px',
            fontSize: '24px',
            fontWeight: 'bold',
            color: '#ffffff',
            background: 'transparent',
            border: '2px solid #ffffff',
            borderRadius: '8px',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
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
          Cancelar
        </button>

        <button
          onClick={handleSave}
          style={{
            padding: '20px 80px',
            fontSize: '24px',
            fontWeight: 'bold',
            color: '#000000',
            background: '#4a9eff',
            border: '2px solid #4a9eff',
            borderRadius: '8px',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
            letterSpacing: '2px',
            textTransform: 'uppercase',
            width: '350px'
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
